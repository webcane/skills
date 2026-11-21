#!/usr/bin/env python3
"""Report pilot quality: structure, grounding, axis coverage, traceability.

Examples:
    scripts/self_review.py --root studies
    scripts/self_review.py --root studies --json
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (  # noqa: E402
    Parser,
    AXES,
    DECISION_SECTIONS,
    EXIT_OK,
    EXIT_USAGE,
    KIND_REQUIRED,
    KINDS,
    citation_stats,
    fail,
    find_section,
    load_json,
    ok,
    read_text,
    split_h2,
    studies_root,
    word_count,
)

UNSOURCED_LIMIT = 0.25


def run_validator(directory: Path, slug: str, root: Path) -> dict:
    result = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).with_name("validate_report.py")),
            "--lang",
            slug,
            "--root",
            str(root),
            "--json",
        ],
        capture_output=True,
        text=True,
    )
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"errors": [f"validator crashed: {result.stderr.strip()[:200]}"], "warnings": []}


def decision_sections(path: Path) -> tuple[int, int, list[str]]:
    if not path.exists():
        return 0, 0, ["decision.md missing"]
    text = read_text(path, "self_review")
    _, sections = split_h2(text)
    titles = [title for title, _ in sections]
    matched = 0
    missing = []
    for number, keywords in DECISION_SECTIONS:
        hit = any(
            re.match(rf"^{number}\.", title)
            and any(keyword.lower() in title.lower() for keyword in keywords)
            for title in titles
        )
        if hit:
            matched += 1
        else:
            missing.append(str(number))
    backlinks = len(re.findall(r"\b(C|J|S|T|AX)\d{1,2}\b", text))
    return matched, backlinks, missing


def main(argv: list[str]) -> int:
    script = "self_review"
    parser = Parser(
        prog="self_review.py",
        description=(
            "Aggregate the pilot: per-language structure, citation density, axis coverage, "
            "decision completeness, source class coverage, and a pass/fail verdict per criterion."
        ),
        epilog=(
            "examples:\n"
            "  scripts/self_review.py --root studies\n"
            "  scripts/self_review.py --root studies --json > review.json\n"
            "\n"
            "This script reports; it never edits studies.\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--root", default=None, help="studies directory (default: ./studies)")
    parser.add_argument("--json", action="store_true", help="machine-readable report on stdout")
    if not argv:
        parser.print_usage(sys.stderr)
        print("  hint: defaults are fine: scripts/self_review.py --root studies\n  run --help", file=sys.stderr)
        return EXIT_USAGE
    args = parser.parse_args(argv)

    root = studies_root(args.root)
    directories = sorted(path.parent for path in root.glob("*/study.md"))
    if not directories:
        fail(
            script,
            EXIT_USAGE,
            f"no studies under {root}",
            "nothing to review yet",
            "run scripts/init_study.py --lang <language> and complete at least one run",
        )

    report = []
    for directory in directories:
        slug = directory.name
        manifest = load_json(directory / "manifest.json", script)
        study_text = read_text(directory / "study.md", script)
        _, sections = split_h2(study_text)
        stats = citation_stats(study_text)
        structure = run_validator(directory, slug, root)

        comparability = directory / "comparability.json"
        coverage = 0
        if comparability.exists():
            data = load_json(comparability, script)
            coverage = sum(1 for axis in AXES if (data.get("axes") or {}).get(axis))
        else:
            section_c = find_section(sections, "C")
            if section_c:
                coverage = sum(1 for axis in AXES if axis in section_c[1])

        counts = {kind: 0 for kind in KINDS}
        for item in manifest.get("sources", []):
            if item.get("kind") in counts:
                counts[item["kind"]] += 1
        source_ok = all(counts[kind] >= need for kind, need in KIND_REQUIRED.items())

        matched, backlinks, missing = decision_sections(directory / "decision.md")
        words = word_count(study_text)
        errors = structure.get("errors", [])
        ratio = stats["unsourced_ratio"]

        criteria = {
            "structure": not errors,
            "grounding": ratio <= UNSOURCED_LIMIT,
            "axes": coverage == len(AXES),
            "decision": matched == len(DECISION_SECTIONS),
            "traceability": backlinks > 0,
            "sources": source_ok,
        }
        report.append(
            {
                "language": manifest.get("language", slug),
                "slug": slug,
                "words": words,
                "citations": stats["citations"],
                "unsourced": stats["unsourced"],
                "unsourced_ratio": ratio,
                "citations_per_100_words": round(100 * stats["citations"] / words, 2) if words else 0,
                "axis_coverage": f"{coverage}/{len(AXES)}",
                "decision_sections": f"{matched}/{len(DECISION_SECTIONS)}",
                "decision_missing": missing,
                "backlinks": backlinks,
                "sources": counts,
                "structure_errors": errors,
                "criteria": criteria,
                "verdict": "pass" if all(criteria.values()) else "fail",
            }
        )

    if args.json:
        print(json.dumps({"root": str(root), "studies": report}, indent=2))
        return EXIT_OK

    ok(f"Pilot self-review — {len(report)} study(ies) under {root}")
    ok("")
    ok(
        f"{'LANGUAGE':<12} {'WORDS':>6} {'CITE':>5} {'UNSRC':>6} {'AXES':>6} "
        f"{'DEC':>5} {'LINK':>5}  VERDICT"
    )
    for item in report:
        ok(
            f"{item['language']:<12} {item['words']:>6} {item['citations']:>5} "
            f"{item['unsourced_ratio']:>6.0%} {item['axis_coverage']:>6} "
            f"{item['decision_sections']:>5} {item['backlinks']:>5}  {item['verdict'].upper()}"
        )

    ok("")
    ok("Criteria")
    for criterion in ("structure", "grounding", "axes", "decision", "traceability", "sources"):
        passed = [item["language"] for item in report if item["criteria"][criterion]]
        failed = [item["language"] for item in report if not item["criteria"][criterion]]
        state = "pass" if not failed else f"FAIL ({', '.join(failed)})"
        ok(f"  {criterion:<13} {state}")

    cross = [item for item in report if item["structure_errors"]]
    if cross:
        ok("")
        ok("Blocking structure errors")
        for item in cross:
            for message in item["structure_errors"][:5]:
                ok(f"  {item['language']}: {message}")

    ok("")
    ok("Cross-study comparability: identical headings and axis set are enforced by")
    ok("validate_report.py; run scripts/merge_matrix.py to verify the merged grid.")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
