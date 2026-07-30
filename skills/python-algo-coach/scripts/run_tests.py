#!/usr/bin/env python3
"""
Test harness for the python-algo-coach skill.

Loads one problem from references/PROBLEMS.json, runs a solution file against
its test cases, and prints a verdict. This is the only moving part of the
skill: the coach never eyeballs code correctness, it runs this.

Usage:
  python3 scripts/run_tests.py --list [--difficulty easy] [--pattern hash_map]
  python3 scripts/run_tests.py --patterns
  python3 scripts/run_tests.py --show two_sum
  python3 scripts/run_tests.py --hint two_sum [--level 2]
  python3 scripts/run_tests.py --scaffold two_sum [--out FILE]
  python3 scripts/run_tests.py two_sum FILE          # test a solution
  python3 scripts/run_tests.py --reference two_sum   # test the shipped answer
  python3 scripts/run_tests.py --all-reference       # self-check the whole bank
  python3 scripts/run_tests.py --random [--difficulty medium] [--pattern stack]

Exit code: 0 = all tests passed, 1 = at least one failure, 2 = usage error.
"""

import argparse
import ast
import copy
import importlib.util
import inspect
import json
import random
import signal
import sys
import textwrap
import time
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANK = ROOT / "references" / "PROBLEMS.json"
SOLUTIONS_DIR = ROOT / "references" / "solutions"

DEFAULT_TIMEOUT = 5  # seconds per test case


# --------------------------------------------------------------------------
# Node types. Solutions are duck-typed: any object with .val/.next (list) or
# .val/.left/.right (tree) is accepted back, so a solution file can define its
# own classes exactly like on LeetCode.
# --------------------------------------------------------------------------


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        return f"ListNode({dump_list(self)})"


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f"TreeNode({dump_tree(self)})"


def build_list(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def dump_list(node, limit=10_000):
    out = []
    seen = set()
    while node is not None:
        if id(node) in seen:
            raise ValueError("cycle detected in returned linked list")
        seen.add(id(node))
        out.append(node.val)
        node = node.next
        if len(out) > limit:
            raise ValueError("returned linked list is suspiciously long")
    return out


def build_tree(values):
    """LeetCode level-order encoding, None for a missing child."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    while queue and i < len(values):
        node = queue.pop(0)
        if i < len(values):
            v = values[i]
            i += 1
            if v is not None:
                node.left = TreeNode(v)
                queue.append(node.left)
        if i < len(values):
            v = values[i]
            i += 1
            if v is not None:
                node.right = TreeNode(v)
                queue.append(node.right)
    return root


def dump_tree(root):
    if root is None:
        return []
    out = []
    queue = [root]
    while queue:
        node = queue.pop(0)
        if node is None:
            out.append(None)
            continue
        out.append(node.val)
        queue.append(node.left)
        queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


BUILDERS = {"linked_list": build_list, "tree": build_tree}
DUMPERS = {"linked_list": dump_list, "tree": dump_tree}


# --------------------------------------------------------------------------
# Comparators. `compare` in PROBLEMS.json picks one.
# --------------------------------------------------------------------------


def _sortable(seq):
    return sorted(seq, key=lambda x: (str(type(x)), x))


def cmp_exact(result, expected, args):
    return result == expected


def cmp_unordered(result, expected, args):
    """Order of the returned elements does not matter."""
    if result is None or not isinstance(result, (list, tuple)):
        return False
    return _sortable(result) == _sortable(expected)


def cmp_groups(result, expected, args):
    """List of groups; neither group order nor order inside a group matters."""
    if result is None or not isinstance(result, (list, tuple)):
        return False
    try:
        got = _sortable([tuple(_sortable(g)) for g in result])
        want = _sortable([tuple(_sortable(g)) for g in expected])
    except TypeError:
        return False
    return got == want


def cmp_inplace(result, expected, args):
    """Solution mutates args[0]; the return value is ignored."""
    return args[0] == expected


def cmp_inplace_k(result, expected, args):
    """Returns k; the first k elements of args[0] must match in any order."""
    if not isinstance(result, int) or isinstance(result, bool):
        return False
    if result != expected["k"]:
        return False
    return _sortable(args[0][: result]) == _sortable(expected["remaining"])


COMPARATORS = {
    "exact": cmp_exact,
    "unordered": cmp_unordered,
    "groups": cmp_groups,
    "inplace": cmp_inplace,
    "inplace_k": cmp_inplace_k,
}


# --------------------------------------------------------------------------
# Bank access
# --------------------------------------------------------------------------


def load_bank():
    with BANK.open(encoding="utf-8") as fh:
        return json.load(fh)["problems"]


def find_problem(problems, pid):
    for p in problems:
        if p["id"] == pid:
            return p
    aliases = {a: p for p in problems for a in p.get("aliases", [])}
    if pid in aliases:
        return aliases[pid]
    sys.exit(f"error: unknown problem id '{pid}'. Try --list.")


def filter_problems(problems, difficulty=None, pattern=None):
    out = problems
    if difficulty:
        out = [p for p in out if p["difficulty"] == difficulty]
    if pattern:
        out = [p for p in out if pattern in p["patterns"]]
    return out


# --------------------------------------------------------------------------
# Running
# --------------------------------------------------------------------------


class Timeout(Exception):
    pass


def _alarm(signum, frame):
    raise Timeout()


def load_solution(path, func_name):
    path = Path(path)
    if not path.exists():
        sys.exit(f"error: solution file not found: {path}")
    spec = importlib.util.spec_from_file_location(f"_algo_sol_{path.stem}", path)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception:
        print(f"FAIL: solution file raised on import: {path}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)
    fn = getattr(module, func_name, None)
    if fn is None:
        candidates = [
            v
            for k, v in vars(module).items()
            if callable(v) and not k.startswith("_") and getattr(v, "__module__", None) == module.__name__
        ]
        if len(candidates) == 1:
            fn = candidates[0]
        else:
            sys.exit(
                f"error: {path} defines no function '{func_name}' "
                f"(found: {', '.join(sorted(c.__name__ for c in candidates)) or 'nothing'})"
            )
    return fn


def is_unimplemented(fn):
    """Тело функции — незаполненная заглушка из скаффолда?

    Нужно потому, что `pass` возвращает None молча: на задачах вроде move_zeroes
    часть тестов тогда «проходит» (ничего не делать случайно совпадает с
    ответом), и пользователь видит 3/5 вместо честного «решение не написано».
    """
    try:
        source = textwrap.dedent(inspect.getsource(fn))
        node = ast.parse(source).body[0]
    except (OSError, TypeError, SyntaxError, IndexError):
        return False
    if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return False
    body = list(node.body)
    if body and isinstance(body[0], ast.Expr) and isinstance(getattr(body[0].value, "value", None), str):
        body = body[1:]                      # выкинуть docstring
    if len(body) != 1:
        return False
    stmt = body[0]
    if isinstance(stmt, ast.Pass):
        return True
    if isinstance(stmt, ast.Expr) and getattr(stmt.value, "value", "") is Ellipsis:
        return True
    if isinstance(stmt, ast.Raise):
        exc = stmt.exc
        name = getattr(exc, "id", None) or getattr(getattr(exc, "func", None), "id", None)
        return name == "NotImplementedError"
    return False


def prepare_args(problem, raw_args):
    args = copy.deepcopy(raw_args)
    for i, kind in enumerate(problem.get("arg_types", [])):
        if kind and i < len(args):
            args[i] = BUILDERS[kind](args[i])
    return args


def fmt(value, width=70):
    text = repr(value)
    return text if len(text) <= width else text[: width - 3] + "..."


def run_problem(problem, solution_path, timeout=DEFAULT_TIMEOUT, verbose=True):
    fn = load_solution(solution_path, problem["func"])
    if is_unimplemented(fn):
        if verbose:
            print(f"\nРешение не написано: тело {problem['func']}() — это заглушка из скаффолда.")
            print("Тесты не запускались. Замени pass на своё решение и запусти снова.")
        return None, None, []
    compare = COMPARATORS[problem.get("compare", "exact")]
    ret_kind = problem.get("return_type")
    passed = failed = 0
    failures = []

    prev = signal.signal(signal.SIGALRM, _alarm)
    try:
        for idx, case in enumerate(problem["tests"], start=1):
            args = prepare_args(problem, case["args"])
            shown = fmt(case["args"])
            signal.setitimer(signal.ITIMER_REAL, timeout)
            start = time.perf_counter()
            try:
                result = fn(*args)
                if ret_kind in DUMPERS and result is not None:
                    result = DUMPERS[ret_kind](result)
                elif ret_kind in DUMPERS and result is None:
                    result = []
                ok = compare(result, case["expected"], args)
                err = None
            except Timeout:
                result, ok, err = None, False, f"timeout after {timeout}s (infinite loop?)"
            except Exception as exc:
                result, ok, err = None, False, f"{type(exc).__name__}: {exc}"
            finally:
                signal.setitimer(signal.ITIMER_REAL, 0)
            elapsed = (time.perf_counter() - start) * 1000

            if ok:
                passed += 1
                if verbose:
                    print(f"  ✓ test {idx}  {shown}  [{elapsed:.2f} ms]")
            else:
                failed += 1
                detail = err or f"got {fmt(result)}, expected {fmt(case['expected'])}"
                if not err and problem.get("compare") in ("inplace", "inplace_k"):
                    detail = f"array after call {fmt(args[0])}, expected {fmt(case['expected'])}"
                failures.append((idx, shown, detail))
                if verbose:
                    print(f"  ✗ test {idx}  {shown}")
                    print(f"      {detail}")
    finally:
        signal.signal(signal.SIGALRM, prev)

    return passed, failed, failures


# --------------------------------------------------------------------------
# Output helpers
# --------------------------------------------------------------------------


def show_problem(problem):
    print(f"[{problem['id']}]  {problem['title']}  (LeetCode {problem['leetcode']}, {problem['difficulty']})")
    print()
    print("Условие:")
    print(f"  {problem['statement']}")
    print()
    print(f"Подпись: {problem['signature']}:")
    print()
    print("Примеры:")
    for case in problem["tests"][:3]:
        expected = case["expected"]
        if problem.get("compare") == "inplace_k":
            shown = f"вернуть {expected['k']}, первые {expected['k']} элементов = {expected['remaining']}"
        elif problem.get("compare") == "inplace":
            shown = f"массив становится {fmt(expected, 90)}"
        else:
            shown = fmt(expected, 90)
        print(f"  {fmt(case['args'], 90)}  ->  {shown}")
    if problem.get("compare") == "inplace":
        print("  (решение меняет первый аргумент in-place; возвращаемое значение игнорируется)")
    if problem.get("compare") == "inplace_k":
        print("  (решение меняет первый аргумент in-place и возвращает k)")
    if problem.get("compare") == "unordered":
        print("  (порядок элементов в ответе не важен)")
    if problem.get("compare") == "groups":
        print("  (порядок групп и порядок внутри группы не важны)")
    # Подвал: спойлеры идут последними — и в свёрнутом выводе терминала попадают
    # в скрытую часть, а условие с примерами видно. Паттерн спойлерит Шаг 2,
    # целевая сложность — Шаг 4, где пользователь оценивает своё решение слепо.
    print()
    print("-- спойлеры " + "-" * 57)
    print(f"Паттерны: {', '.join(problem['patterns'])}          # не называй до Шага 2")
    print(
        f"Цель: время {problem['target']['time']}, память {problem['target']['space']}"
        "          # не называй до Шага 4"
    )


def scaffold_text(problem):
    # Целевая сложность в скаффолд НЕ попадает: пользователь оценивает сложность
    # своего решения сам на Шаге 4, и оценка должна быть слепой.
    lines = ['"""', f"{problem['title']} — LeetCode {problem['leetcode']} ({problem['difficulty']})", ""]
    lines.append(problem["statement"])
    lines.append('"""')
    lines.append("")
    if "linked_list" in problem.get("arg_types", []) or problem.get("return_type") == "linked_list":
        lines += [
            "",
            "class ListNode:",
            "    def __init__(self, val=0, next=None):",
            "        self.val = val",
            "        self.next = next",
            "",
        ]
    if "tree" in problem.get("arg_types", []) or problem.get("return_type") == "tree":
        lines += [
            "",
            "class TreeNode:",
            "    def __init__(self, val=0, left=None, right=None):",
            "        self.val = val",
            "        self.left = left",
            "        self.right = right",
            "",
        ]
    lines.append("")
    lines.append(f"{problem['signature']}:")
    lines.append("    pass")
    lines.append("")
    return "\n".join(lines)


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------


def main(argv=None):
    parser = argparse.ArgumentParser(add_help=True, description="python-algo-coach test harness")
    parser.add_argument("problem", nargs="?", help="problem id")
    parser.add_argument("solution", nargs="?", help="path to the solution .py file")
    parser.add_argument("--list", action="store_true", help="list problems")
    parser.add_argument("--patterns", action="store_true", help="list patterns with problem counts")
    parser.add_argument("--show", metavar="ID", help="print the problem statement")
    parser.add_argument("--hint", metavar="ID", help="print a hint")
    parser.add_argument("--target", metavar="ID", help="reveal target complexity (Шаг 4, after the user's own estimate)")
    parser.add_argument("--level", type=int, default=1, help="hint level (1..3)")
    parser.add_argument("--scaffold", metavar="ID", help="print a starter file for a problem")
    parser.add_argument("--out", metavar="FILE", help="write --scaffold output to FILE")
    parser.add_argument("--reference", metavar="ID", help="run the shipped reference solution")
    parser.add_argument("--all-reference", action="store_true", help="run every reference solution")
    parser.add_argument("--random", action="store_true", help="pick a random problem id")
    parser.add_argument("--difficulty", choices=["easy", "medium"], help="filter")
    parser.add_argument("--pattern", help="filter by pattern")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="per-test timeout, seconds")
    args = parser.parse_args(argv)

    problems = load_bank()

    if args.patterns:
        counts = {}
        for p in problems:
            for pat in p["patterns"]:
                counts[pat] = counts.get(pat, 0) + 1
        for pat in sorted(counts):
            print(f"{pat:<22} {counts[pat]} задач")
        return 0

    if args.list:
        selected = filter_problems(problems, args.difficulty, args.pattern)
        for p in selected:
            print(f"{p['id']:<42} {p['difficulty']:<7} {', '.join(p['patterns'])}")
        print(f"\n{len(selected)} задач(и) из {len(problems)}")
        return 0

    if args.random:
        selected = filter_problems(problems, args.difficulty, args.pattern)
        if not selected:
            sys.exit("error: no problem matches those filters")
        print(random.choice(selected)["id"])
        return 0

    if args.show:
        show_problem(find_problem(problems, args.show))
        return 0

    if args.hint:
        problem = find_problem(problems, args.hint)
        hints = problem["hints"]
        level = max(1, min(args.level, len(hints)))
        print(f"Подсказка {level}/{len(hints)}: {hints[level - 1]}")
        return 0

    if args.target:
        problem = find_problem(problems, args.target)
        print(f"Цель: время {problem['target']['time']}, память {problem['target']['space']}")
        print(f"Паттерны: {', '.join(problem['patterns'])}")
        print(f"Типичная ошибка: {problem['trap']}")
        return 0

    if args.scaffold:
        problem = find_problem(problems, args.scaffold)
        text = scaffold_text(problem)
        if args.out:
            Path(args.out).parent.mkdir(parents=True, exist_ok=True)
            Path(args.out).write_text(text, encoding="utf-8")
            print(f"written: {args.out}")
        else:
            print(text, end="")
        return 0

    if args.all_reference:
        bad = []
        for p in problems:
            path = SOLUTIONS_DIR / f"{p['id']}.py"
            if not path.exists():
                print(f"MISSING  {p['id']}")
                bad.append(p["id"])
                continue
            passed, failed, _ = run_problem(p, path, args.timeout, verbose=False)
            if passed is None:
                print(f"STUB  {p['id']:<42} эталон не реализован")
                bad.append(p["id"])
                continue
            mark = "ok  " if failed == 0 else "FAIL"
            print(f"{mark}  {p['id']:<42} {passed}/{passed + failed}")
            if failed:
                bad.append(p["id"])
        print(f"\n{len(problems) - len(bad)}/{len(problems)} reference solutions pass")
        if bad:
            print("failing: " + ", ".join(bad))
            return 1
        return 0

    if args.reference:
        problem = find_problem(problems, args.reference)
        path = SOLUTIONS_DIR / f"{problem['id']}.py"
        print(f"Эталонное решение: {problem['id']}")
        passed, failed, _ = run_problem(problem, path, args.timeout)
        if passed is None:
            return 1
        print(f"\n{passed}/{passed + failed} тестов пройдено")
        return 0 if failed == 0 else 1

    if not args.problem or not args.solution:
        parser.print_help()
        return 2

    problem = find_problem(problems, args.problem)
    print(f"Задача: {problem['title']} ({problem['difficulty']})  —  {problem['id']}")
    passed, failed, failures = run_problem(problem, args.solution, args.timeout)
    if passed is None:
        return 1
    total = passed + failed
    print(f"\n{passed}/{total} тестов пройдено")
    if failed == 0:
        # Целевую сложность здесь НЕ печатаем: сначала оценка пользователя (Шаг 4),
        # только потом сверка через --target.
        print(f"ВСЁ ЗЕЛЁНОЕ. Шаг 4: оцени время и память своего решения,")
        print(f"затем сверься:  python3 scripts/run_tests.py --target {problem['id']}")
        return 0
    print(f"Провалено тестов: {failed}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
