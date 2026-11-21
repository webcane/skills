#!/usr/bin/env python3
"""Check that a study has enough sources of each required class (gate G0).

Example:
    scripts/check_sources.py --lang rust
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (  # noqa: E402
    Parser,
    EXIT_INVALID,
    EXIT_OK,
    EXIT_USAGE,
    KIND_LABELS,
    KIND_REQUIRED,
    KINDS,
    fail,
    load_json,
    ok,
    slugify,
    studies_root,
    study_dir,
    warn,
)


def build_parser() -> argparse.ArgumentParser:
    parser = Parser(
        prog="check_sources.py",
        description=(
            "Verify that the manifest covers all five source classes. Exits 4 when a "
            "class is under its minimum, so the agent cannot start writing on a thin base."
        ),
        epilog=(
            "examples:\n"
            "  scripts/check_sources.py --lang rust\n"
            "  scripts/check_sources.py --lang zig --min-papers 3 --json\n"
            "\n"
            "minimums: spec=1, essay=1, paper=2, release=1, retro=1\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--lang", required=True, help="language of the study")
    parser.add_argument(
        "--min-papers", type=int, default=None, help="override the paper minimum (default 2)"
    )
    parser.add_argument(
        "--min-retros", type=int, default=None, help="override the retrospective minimum (default 1)"
    )
    parser.add_argument("--root", default=None, help="studies directory (default: ./studies)")
    parser.add_argument("--json", action="store_true", help="machine-readable result on stdout")
    return parser


def main(argv: list[str]) -> int:
    script = "check_sources"
    parser = build_parser()
    if not argv:
        parser.print_usage(sys.stderr)
        print("  hint: --lang is required, e.g. --lang rust\n  run --help", file=sys.stderr)
        return EXIT_USAGE
    args = parser.parse_args(argv)

    required = dict(KIND_REQUIRED)
    if args.min_papers is not None:
        required["paper"] = max(0, args.min_papers)
    if args.min_retros is not None:
        required["retro"] = max(0, args.min_retros)

    directory = study_dir(studies_root(args.root), slugify(args.lang))
    manifest = load_json(directory / "manifest.json", script)
    counts = {kind: 0 for kind in KINDS}
    missing_files = []
    for item in manifest.get("sources", []):
        kind = item.get("kind")
        if kind in counts:
            counts[kind] += 1
        snapshot = item.get("snapshot", "")
        if snapshot and not (directory / snapshot).exists():
            missing_files.append(f"{item.get('id')}: {snapshot}")

    rows = []
    failed = False
    for kind in KINDS:
        need = required.get(kind, 0)
        have = counts[kind]
        good = have >= need
        failed = failed or not good
        rows.append(
            {
                "kind": kind,
                "label": KIND_LABELS[kind],
                "have": have,
                "need": need,
                "ok": good,
            }
        )

    if args.json:
        print(
            json.dumps(
                {
                    "language": manifest.get("language"),
                    "slug": manifest.get("slug"),
                    "rows": rows,
                    "missing_snapshots": missing_files,
                    "ok": not failed and not missing_files,
                },
                indent=2,
            )
        )
    else:
        ok(f"Sources for {manifest.get('language')} ({len(manifest.get('sources', []))} total)")
        ok("")
        ok(f"{'KIND':<8} {'HAVE':>4} {'NEED':>4}  CLASS")
        for row in rows:
            flag = "ok  " if row["ok"] else "MISS"
            ok(f"{row['kind']:<8} {row['have']:>4} {row['need']:>4}  {flag} {row['label']}")
        ok("")
        for kind in KINDS:
            if counts[kind] == 0:
                warn(script, f"no {kind} source yet ({KIND_LABELS[kind]})")
        for broken in missing_files:
            warn(script, f"snapshot listed in manifest but absent: {broken}")

    if failed or missing_files:
        fail(
            script,
            EXIT_INVALID,
            "source base is incomplete",
            "writing now would force unsourced claims and break comparability",
            "add the missing classes with scripts/add_source.py, then re-run this check",
        )
    if not args.json:
        ok("gate G0 passed: every required source class is covered")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
