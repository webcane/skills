#!/usr/bin/env python3
"""Shared helpers for the pl-dialectics scripts.

Stdlib only. Every public helper raises SystemExit through fail() with a
message that names the problem, the reason and the fix.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

SCHEMA_VERSION = "1"

EXIT_OK = 0
EXIT_USAGE = 2
EXIT_PRECONDITION = 3
EXIT_INVALID = 4
EXIT_REFUSED = 5


class Parser(argparse.ArgumentParser):
    """ArgumentParser whose errors follow the ERROR/why/fix contract."""

    def error(self, message: str) -> None:  # type: ignore[override]
        print(f"ERROR [{self.prog}] {message}", file=sys.stderr)
        print(f"  fix: run {self.prog} --help for the full option list", file=sys.stderr)
        raise SystemExit(EXIT_USAGE)

KINDS = ("spec", "essay", "paper", "release", "retro")
KIND_REQUIRED = {
    "spec": 1,
    "essay": 1,
    "paper": 2,
    "release": 1,
    "retro": 1,
}
KIND_LABELS = {
    "spec": "official specification or language reference",
    "essay": "creator essay (why the language is like this)",
    "paper": "academic paper",
    "release": "release history or RFC index",
    "retro": "critical retrospective",
}

TASK_ORDER = ["A", "B", "C", "D", "E", "F", "G", "H"]
TASK_TITLES = {
    "A": "TASK A — SNAPSHOT",
    "B": "TASK B — THE THREE LAWS",
    "C": "TASK C — AXIS GRID",
    "D": "TASK D — CLASSICAL PROBLEMS",
    "E": "TASK E — NEW TENSIONS",
    "F": "TASK F — CATEGORY DISCOVERY",
    "G": "TASK G — HYPOTHESES",
    "H": "TASK H — COMPARABILITY BLOCK",
}
TASK_H_FIELDS = (
    "Language",
    "Era covered",
    "Core contradictions",
    "Major qualitative jumps",
    "Major syntheses",
    "New tensions",
    "Discovered axes",
    "One-line dialectical verdict",
)
AXES = [f"AX{i}" for i in range(1, 20)]

DECISION_SECTIONS = (
    ("1", ("Decision", "Решение")),
    ("2", ("Rationale", "Обоснование")),
    ("3", ("Scope", "Boundaries", "Границы")),
    ("4", ("Implementation", "Детали")),
    ("5", ("Verification", "Проверка")),
    ("6", ("Risks", "Риски")),
    ("7", ("Open questions", "Открытые вопросы")),
)

ID_RE = re.compile(r"\b(C|J|S|T|AX)(\d{1,2})\b")
CITE_RE = re.compile(r"\[Source:\s*[^\]\n]+?,\s*[^\]\n]+?\]")
MARKER_RE = re.compile(r"\[(?:UNSOURCED|DISPUTED|NO CLEAR INSTANCE)\]")
H2_RE = re.compile(r"^##\s+(.+?)\s*$")
H1_RE = re.compile(r"^#\s+(.+?)\s*$")


def fail(script: str, code: int, message: str, why: str = "", fix: str = "") -> None:
    print(f"ERROR [{script}] {message}", file=sys.stderr)
    if why:
        print(f"  why: {why}", file=sys.stderr)
    if fix:
        print(f"  fix: {fix}", file=sys.stderr)
    raise SystemExit(code)


def warn(script: str, message: str) -> None:
    print(f"WARN  [{script}] {message}", file=sys.stderr)


def ok(message: str) -> None:
    print(message)


def skill_root() -> Path:
    return Path(__file__).resolve().parent.parent


def slugify(language: str) -> str:
    text = language.strip().lower()
    text = text.replace("c++", "cpp").replace("c#", "csharp").replace("f#", "fsharp")
    text = text.replace("+", "plus").replace("#", "sharp")
    slug = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return slug or "language"


def studies_root(explicit: str | None) -> Path:
    return Path(explicit).expanduser().resolve() if explicit else (Path.cwd() / "studies")


def study_dir(root: Path, language: str) -> Path:
    return root / slugify(language)


def require_slug(value: str, script: str) -> str:
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", value or ""):
        fail(
            script,
            EXIT_USAGE,
            f"invalid language slug {value!r}",
            "a study directory name must be lowercase letters, digits and hyphens",
            "pass a real language name, e.g. --lang rust or --lang 'C++'",
        )
    return value


def read_text(path: Path, script: str, fix: str = "") -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(
            script,
            EXIT_PRECONDITION,
            f"{path} does not exist",
            "the study has not been initialised or the path is wrong",
            fix or "run scripts/init_study.py --lang <language> first",
        )
    except OSError as exc:
        fail(script, EXIT_PRECONDITION, f"cannot read {path}: {exc}", "", fix)


def load_json(path: Path, script: str, fix: str = "") -> dict:
    if not path.exists():
        fail(
            script,
            EXIT_PRECONDITION,
            f"{path} does not exist",
            "the manifest or comparability block is missing",
            fix or "run scripts/init_study.py --lang <language> first",
        )
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(
            script,
            EXIT_INVALID,
            f"{path} is not valid JSON: {exc}",
            "the file was edited by hand or truncated",
            "restore it from git, or re-run the step that writes it",
        )
    return {}


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def split_h2(markdown: str) -> tuple[str, list[tuple[str, str]]]:
    """Return the preamble and an ordered list of (level-2 heading, body)."""
    preamble: list[str] = []
    sections: list[tuple[str, str]] = []
    current_title: str | None = None
    current_body: list[str] = []
    for line in markdown.splitlines():
        match = H2_RE.match(line)
        if match:
            if current_title is not None:
                sections.append((current_title, "\n".join(current_body).strip()))
            current_title = match.group(1)
            current_body = []
        elif current_title is None:
            preamble.append(line)
        else:
            current_body.append(line)
    if current_title is not None:
        sections.append((current_title, "\n".join(current_body).strip()))
    return "\n".join(preamble).strip(), sections


def find_section(sections: list[tuple[str, str]], task: str) -> tuple[str, str] | None:
    prefix = f"TASK {task} "
    marker = f"TASK {task} —"
    for title, body in sections:
        if title.startswith(marker) or title.startswith(prefix):
            return title, body
    return None


def parse_tables(body: str) -> list[dict]:
    """Extract pipe tables. Returns dicts with header list, rows, and line numbers."""
    tables: list[dict] = []
    lines = body.splitlines()
    index = 0
    while index < len(lines):
        if not lines[index].lstrip().startswith("|"):
            index += 1
            continue
        start = index
        block: list[str] = []
        while index < len(lines) and lines[index].lstrip().startswith("|"):
            block.append(lines[index].strip())
            index += 1
        if len(block) >= 2 and re.fullmatch(r"\|[\s:|-]+\|?", block[1]):
            header = _cells(block[0])
            rows = [_cells(row) for row in block[2:]]
            tables.append(
                {"header": header, "rows": rows, "start_line": start + 1, "n_cols": len(header)}
            )
    return tables


def _cells(row: str) -> list[str]:
    row = row.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|"):
        row = row[:-1]
    return [cell.strip() for cell in row.split("|")]


def normalise(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def header_has(header: list[str], needle: str) -> bool:
    target = normalise(needle)
    return any(target in normalise(cell) for cell in header)


def word_count(text: str) -> int:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    return len(re.findall(r"[A-Za-z0-9µ][A-Za-z0-9'’\-_.+]*", text))


def citation_stats(body: str) -> dict:
    citations = CITE_RE.findall(body)
    markers = MARKER_RE.findall(body)
    unsourced = len(re.findall(r"\[UNSOURCED\]", body))
    denominator = len(citations) + unsourced
    ratio = (unsourced / denominator) if denominator else 0.0
    return {
        "citations": len(citations),
        "unsourced": unsourced,
        "markers": len(markers),
        "unsourced_ratio": round(ratio, 3),
        "invalid_brackets": _malformed_source_brackets(body),
    }


def _malformed_source_brackets(body: str) -> list[str]:
    broken = []
    for match in re.finditer(r"\[Source:[^\]]*\]", body):
        if not CITE_RE.fullmatch(match.group(0)):
            broken.append(match.group(0))
    return broken


def ids_in(text: str) -> set[str]:
    found = set()
    for prefix, number in ID_RE.findall(text):
        found.add(f"{prefix}{int(number)}")
    return found


def table_rows_by_id(table: dict) -> dict[str, list[str]]:
    """Map the first column value to its row when the header marks it as an ID."""
    if not table["rows"] or not header_has(table["header"], "id"):
        return {}
    result = {}
    for row in table["rows"]:
        if not row:
            continue
        key = row[0].strip()
        if key:
            result[key] = row
    return result


def cell(row: list[str], index: int) -> str:
    return row[index].strip() if index < len(row) else ""


def die_for_columns(script: str, path: Path, table: dict, expected_min: int) -> None:
    if table["n_cols"] < expected_min:
        fail(
            script,
            EXIT_INVALID,
            f"{path}: table has {table['n_cols']} columns, expected at least {expected_min}",
            f"header read as: {' | '.join(table['header'])}",
            "restore the column set from references/report-template.md and re-run validation",
        )
