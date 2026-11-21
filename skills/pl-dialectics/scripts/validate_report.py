#!/usr/bin/env python3
"""Validate study.md and decision.md, and emit comparability.json.

Examples:
    scripts/validate_report.py --lang rust
    scripts/validate_report.py --lang rust --stage run1
    scripts/validate_report.py --lang rust --emit-json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (  # noqa: E402
    Parser,
    AXES,
    DECISION_SECTIONS,
    EXIT_INVALID,
    EXIT_OK,
    EXIT_USAGE,
    SCHEMA_VERSION,
    TASK_H_FIELDS,
    TASK_ORDER,
    TASK_TITLES,
    citation_stats,
    die_for_columns,
    fail,
    find_section,
    header_has,
    ids_in,
    load_json,
    ok,
    parse_tables,
    read_text,
    save_json,
    slugify,
    split_h2,
    studies_root,
    study_dir,
    warn,
    word_count,
)

COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)
TABLE_ROW_RE = re.compile(r"^\s*\|")


def strip_comments(text: str) -> str:
    return COMMENT_RE.sub("", text).strip()


def parse_frontmatter(text: str) -> dict:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    data = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def check_tables(path_label: str, body: str, findings: list) -> list[dict]:
    tables = parse_tables(body)
    for table in tables:
        for row in table["rows"]:
            if len(row) != table["n_cols"]:
                findings.append(
                    (
                        "error",
                        f"{path_label}: row with {len(row)} cells in a {table['n_cols']}-column "
                        f"table near line {table['start_line']}",
                    )
                )
    return tables


def require_sections(path_label: str, sections, stage: str, findings: list) -> dict:
    found = {}
    order_seen = []
    for task in TASK_ORDER:
        section = find_section(sections, task)
        title = TASK_TITLES[task]
        if section is None:
            findings.append(("error", f"{path_label}: missing heading '{title}'"))
            continue
        found[task] = section
        order_seen.append(task)
        body = strip_comments(section[1])
        needs_content = (stage == "final") or (stage == "run1" and task in {"A", "B"}) or (
            stage == "run2" and task in set("CDEFGH")
        )
        if needs_content and not body:
            findings.append(("error", f"{path_label}: section '{title}' is empty"))
    expected = [task for task in TASK_ORDER if task in found]
    if order_seen != expected:
        findings.append(("error", f"{path_label}: TASK sections are out of order"))
    return found


def validate_study(study_path: Path, manifest: dict, stage: str, warn_ratio: float):
    findings: list[tuple[str, str]] = []
    label = str(study_path)
    text = read_text(study_path, "validate_report")
    front = parse_frontmatter(text)
    if front.get("schema_version") != SCHEMA_VERSION:
        findings.append(
            (
                "error",
                f"{label}: schema_version is {front.get('schema_version')!r}, expected {SCHEMA_VERSION!r}",
            )
        )
    if manifest.get("language") and front.get("language") != manifest["language"]:
        findings.append(
            (
                "error",
                f"{label}: language is {front.get('language')!r} but manifest says "
                f"{manifest.get('language')!r}",
            )
        )
    if "{{" in text:
        findings.append(("error", f"{label}: unresolved template placeholder '{{{{' remains"))

    _, sections = split_h2(text)
    found = require_sections(label, sections, stage, findings)

    defined: set[str] = set()
    citations = 0
    unsourced = 0

    for task, (title, body) in found.items():
        clean = strip_comments(body)
        stats = citation_stats(clean)
        citations += stats["citations"]
        unsourced += stats["unsourced"]
        for broken in stats["invalid_brackets"]:
            findings.append(("error", f"{label}: malformed citation {broken!r} (need '[Source: name, locator]')"))
        if not clean:
            continue
        tables = check_tables(label, clean, findings)

        if task == "A":
            count = word_count(clean)
            if count > 150:
                findings.append(
                    ("error", f"{label}: Task A is {count} words, the cap is 150")
                )

        if task == "B":
            required_headers = {
                "B1": ("ID", "Pole A", "Pole B", "Evidence"),
                "B2": ("ID", "Threshold", "Milestones", "Evidence"),
                "B3": ("ID", "Negated", "Preserved", "Evidence"),
            }
            for sub, prefix, min_cols in (("B1", "C", 7), ("B2", "J", 7), ("B3", "S", 6)):
                if sub not in clean:
                    findings.append(("error", f"{label}: missing subsection {sub}"))
                    continue
                subtree = clean.split(sub, 1)[1]
                subtree = re.split(r"###\s+B[23]\.", subtree)[0]
                sub_tables = parse_tables(subtree)
                if not sub_tables:
                    findings.append(("error", f"{label}: {sub} has no table"))
                    continue
                table = sub_tables[0]
                die_for_columns("validate_report", study_path, table, min_cols)
                for header in required_headers[sub]:
                    if not header_has(table["header"], header):
                        findings.append(
                            ("error", f"{label}: {sub} table is missing column '{header}'")
                        )
                for row in table["rows"]:
                    kind = row[0].strip()
                    if not re.fullmatch(rf"{prefix}\d+", kind):
                        findings.append(
                            ("error", f"{label}: {sub} row ID {kind!r} must match {prefix}N")
                        )
                    else:
                        defined.add(kind)

        if task == "C":
            table = next((t for t in tables if header_has(t["header"], "Axis ID")), None)
            if table is None:
                table = next((t for t in tables if header_has(t["header"], "axis id")), None)
            if table is None:
                findings.append(("error", f"{label}: Task C has no axis table with an 'Axis ID' column"))
            else:
                die_for_columns("validate_report", study_path, table, 6)
                present = {row[0].strip() for row in table["rows"] if row}
                for axis in AXES:
                    if axis not in present:
                        findings.append(("error", f"{label}: Task C is missing row {axis}"))
                for axis in sorted(present - set(AXES)):
                    findings.append(
                        (
                            "error",
                            f"{label}: Task C has unknown row {axis}; the seed set is AX1-AX19",
                        )
                    )
                defined.update(present)

        if task == "D":
            table = tables[0] if tables else None
            if table is None:
                findings.append(("error", f"{label}: Task D has no table"))
            else:
                die_for_columns("validate_report", study_path, table, 4)
                for header in ("Problem", "Solution", "Dialectical move", "Evidence"):
                    if not header_has(table["header"], header):
                        findings.append(("error", f"{label}: Task D missing column '{header}'"))
                if len(table["rows"]) < 9:
                    findings.append(
                        ("error", f"{label}: Task D has {len(table['rows'])} rows, expected 9")
                    )

        if task == "E":
            table = tables[0] if tables else None
            if table is None:
                findings.append(("error", f"{label}: Task E has no table"))
            else:
                die_for_columns("validate_report", study_path, table, 7)
                for header in ("ID", "Tension", "Pole A", "Pole B", "Evidence"):
                    if not header_has(table["header"], header):
                        findings.append(("error", f"{label}: Task E missing column '{header}'"))
                for row in table["rows"]:
                    kind = row[0].strip()
                    if not re.fullmatch(r"T\d+", kind):
                        findings.append(("error", f"{label}: Task E row ID {kind!r} must match TN"))
                    else:
                        defined.add(kind)

        if task == "F":
            if not clean:
                findings.append(("error", f"{label}: Task F is empty; write axes or 'None identified.'"))

        if task == "G":
            table = tables[0] if tables else None
            if table is None:
                findings.append(("error", f"{label}: Task G has no table"))
            else:
                die_for_columns("validate_report", study_path, table, 4)
                for header in ("ID", "Hypothesis", "Evidence", "Falsification"):
                    if not header_has(table["header"], header):
                        findings.append(("error", f"{label}: Task G missing column '{header}'"))
                if not 3 <= len(table["rows"]) <= 7:
                    findings.append(
                        ("error", f"{label}: Task G has {len(table['rows'])} hypotheses, expected 3-7")
                    )

        if task == "H":
            table = tables[0] if tables else None
            if table is None:
                findings.append(("error", f"{label}: Task H has no Field/Value table"))
            else:
                fields = {row[0].strip() for row in table["rows"] if row}
                for field_name in TASK_H_FIELDS:
                    if field_name not in fields:
                        findings.append(("error", f"{label}: Task H missing field '{field_name}'"))

    all_defined = defined
    for task, (title, body) in found.items():
        for ref in ids_in(strip_comments(body)):
            if ref.startswith("AX") and ref in AXES:
                continue
            if ref not in all_defined:
                findings.append(
                    ("error", f"{label}: {title} references undefined ID {ref}")
                )

    ratio = unsourced / (citations + unsourced) if citations + unsourced else 0.0
    if ratio > warn_ratio:
        findings.append(
            (
                "warning",
                f"{label}: {ratio:.0%} of source markers are [UNSOURCED] (threshold {warn_ratio:.0%})",
            )
        )
    if citations == 0 and stage == "final":
        findings.append(("error", f"{label}: no citations at all; the study is not grounded"))

    return findings, {
        "citations": citations,
        "unsourced": unsourced,
        "unsourced_ratio": round(ratio, 3),
        "words": word_count(text),
    }


def validate_decision(path: Path, findings: list[tuple[str, str]]) -> None:
    label = str(path)
    if not path.exists():
        findings.append(("error", f"{label}: missing 7-section decision record"))
        return
    text = read_text(path, "validate_report")
    _, sections = split_h2(text)
    titles = [title for title, _ in sections]
    cursor = 0
    for number, keywords in DECISION_SECTIONS:
        index = None
        for position in range(cursor, len(titles)):
            title = titles[position]
            if re.match(rf"^{number}\.", title) and any(
                keyword.lower() in title.lower() for keyword in keywords
            ):
                index = position
                break
        if index is None:
            findings.append(
                (
                    "error",
                    f"{label}: missing section '{number}. {' / '.join(keywords)}' (order matters)",
                )
            )
            continue
        cursor = index + 1
        if not strip_comments(sections[index][1]):
            findings.append(("error", f"{label}: section {number} is empty"))
    body = strip_comments(text)
    if not ids_in(body):
        findings.append(
            (
                "error",
                f"{label}: no C/J/S/T/AX references; the decision is not traceable to the study",
            )
        )


def build_comparability(study_path: Path, manifest: dict, metrics: dict) -> dict:
    text = read_text(study_path, "validate_report")
    front = parse_frontmatter(text)
    _, sections = split_h2(text)

    axes = {}
    section_c = find_section(sections, "C")
    if section_c:
        table = next(
            (t for t in parse_tables(section_c[1]) if header_has(t["header"], "Axis ID")), None
        )
        if table:
            header = [re.sub(r"\s+", " ", cell).strip() for cell in table["header"]]
            exact = {name.lower(): position for position, name in enumerate(header)}

            def col(*names, exclude=()):
                for name in names:
                    if name.lower() in exact:
                        return exact[name.lower()]
                for name in names:
                    for key, position in exact.items():
                        if name.lower() in key and not any(bad in key for bad in exclude):
                            return position
                return None

            id_pos = col("Axis ID", "ID")
            axis_pos = col("Axis", exclude=("axis id", "id"))
            pos_pos = col("Position")
            just_pos = col("Justification")
            ev_pos = col("Evidence")
            for row in table["rows"]:
                if not row:
                    continue
                axis_id = row[id_pos].strip()
                axes[axis_id] = {
                    "axis": row[axis_pos].strip() if axis_pos is not None and axis_pos < len(row) else "",
                    "position": row[pos_pos].strip() if pos_pos is not None and pos_pos < len(row) else "",
                    "justification": row[just_pos].strip() if just_pos is not None and just_pos < len(row) else "",
                    "evidence": row[ev_pos].strip() if ev_pos is not None and ev_pos < len(row) else "",
                }

    collected = {"C": [], "J": [], "S": [], "T": []}
    for task in ("B", "E"):
        section = find_section(sections, task)
        if not section:
            continue
        body = section[1]
        if task == "B":
            for sub, prefix in (("B1", "C"), ("B2", "J"), ("B3", "S")):
                if sub not in body:
                    continue
                subtree = body.split(sub, 1)[1]
                subtree = re.split(r"###\s+B[23]\.", subtree)[0]
                for table in parse_tables(subtree)[:1]:
                    for row in table["rows"]:
                        if row and re.fullmatch(rf"{prefix}\d+", row[0].strip()):
                            collected[prefix].append(row[0].strip())
        else:
            for table in parse_tables(body)[:1]:
                for row in table["rows"]:
                    if row and re.fullmatch(r"T\d+", row[0].strip()):
                        collected["T"].append(row[0].strip())

    verdict = ""
    discovered = ""
    section_h = find_section(sections, "H")
    if section_h:
        table = next((t for t in parse_tables(section_h[1]) if t["n_cols"] >= 2), None)
        if table:
            rows = {row[0].strip(): row[1].strip() for row in table["rows"] if len(row) >= 2}
            verdict = rows.get("One-line dialectical verdict", "")
            discovered = rows.get("Discovered axes", "")

    counts = {}
    for item in manifest.get("sources", []):
        counts[item.get("kind", "unknown")] = counts.get(item.get("kind", "unknown"), 0) + 1

    return {
        "schema_version": SCHEMA_VERSION,
        "study_id": f"{front.get('slug', slugify(front.get('language', 'unknown')))}-v{SCHEMA_VERSION}",
        "language": front.get("language", manifest.get("language")),
        "slug": front.get("slug", manifest.get("slug")),
        "era": front.get("era", manifest.get("era")),
        "axes": axes,
        "core_contradictions": collected["C"],
        "qualitative_jumps": collected["J"],
        "major_syntheses": collected["S"],
        "new_tensions": collected["T"],
        "discovered_axes": discovered,
        "verdict": verdict,
        "source_counts": counts,
        "metrics": metrics,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = Parser(
        prog="validate_report.py",
        description=(
            "Check heading order, table columns, ID integrity, axis coverage, citation "
            "format and the 7-section decision record. Optionally emit comparability.json."
        ),
        epilog=(
            "examples:\n"
            "  scripts/validate_report.py --lang rust --stage run1\n"
            "  scripts/validate_report.py --lang rust --emit-json\n"
            "  scripts/validate_report.py --lang rust --scope decision\n"
            "\n"
            "exit codes: 0 clean, 2 usage, 3 missing artifacts, 4 validation failed\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--lang", required=True, help="language of the study")
    parser.add_argument("--root", default=None, help="studies directory (default: ./studies)")
    parser.add_argument(
        "--scope",
        choices=("study", "decision", "all"),
        default="all",
        help="which artifact to validate (default: all)",
    )
    parser.add_argument(
        "--stage",
        choices=("run1", "run2", "final"),
        default="final",
        help="run1 requires A-B filled; run2 requires C-H; final requires everything",
    )
    parser.add_argument(
        "--emit-json",
        action="store_true",
        help="write comparability.json next to study.md after a clean validation",
    )
    parser.add_argument("--json", action="store_true", help="machine-readable findings on stdout")
    parser.add_argument(
        "--warn-unsourced",
        type=float,
        default=0.25,
        help="warn when the [UNSOURCED] share exceeds this ratio (default 0.25)",
    )
    return parser


def main(argv: list[str]) -> int:
    script = "validate_report"
    parser = build_parser()
    if not argv:
        parser.print_usage(sys.stderr)
        print("  hint: --lang is required, e.g. --lang rust\n  run --help", file=sys.stderr)
        return EXIT_USAGE
    args = parser.parse_args(argv)

    directory = study_dir(studies_root(args.root), slugify(args.lang))
    study_path = directory / "study.md"
    decision_path = directory / "decision.md"
    manifest = load_json(directory / "manifest.json", script)

    findings: list[tuple[str, str]] = []
    metrics = {"citations": 0, "unsourced": 0, "unsourced_ratio": 0.0, "words": 0}

    if args.scope in ("study", "all"):
        study_findings, metrics = validate_study(
            study_path, manifest, args.stage, args.warn_unsourced
        )
        findings.extend(study_findings)
    if args.scope in ("decision", "all"):
        validate_decision(decision_path, findings)

    errors = [message for level, message in findings if level == "error"]
    warnings = [message for level, message in findings if level == "warning"]

    if args.json:
        print(
            json.dumps(
                {
                    "language": manifest.get("language"),
                    "stage": args.stage,
                    "scope": args.scope,
                    "errors": errors,
                    "warnings": warnings,
                    "metrics": metrics,
                    "ok": not errors,
                },
                indent=2,
            )
        )
    else:
        ok(f"Validated {manifest.get('language')} (stage {args.stage}, scope {args.scope})")
        ok(f"  citations: {metrics['citations']}  unsourced: {metrics['unsourced']}  "
           f"ratio: {metrics['unsourced_ratio']:.0%}")
        for message in warnings:
            warn(script, message)
        if errors:
            ok("")
            for message in errors:
                ok(f"  ERROR {message}")
        else:
            ok("  no structural errors")

    if errors:
        if args.json:
            raise SystemExit(EXIT_INVALID)
        fail(
            script,
            EXIT_INVALID,
            f"{len(errors)} validation error(s)",
            "the report breaks the comparability contract",
            "fix the items above; do not renumber IDs or rename headings",
        )

    if args.emit_json:
        payload = build_comparability(study_path, manifest, metrics)
        save_json(directory / "comparability.json", payload)
        if not args.json:
            ok(f"  wrote {directory / 'comparability.json'}")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
