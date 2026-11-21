#!/usr/bin/env python3
"""Create the artifact skeleton for one language study.

Example:
    scripts/init_study.py --lang rust --era "2010-2026"
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (  # noqa: E402
    Parser,
    EXIT_OK,
    EXIT_REFUSED,
    EXIT_USAGE,
    SCHEMA_VERSION,
    TASK_TITLES,
    KIND_LABELS,
    fail,
    ok,
    require_slug,
    save_json,
    slugify,
    studies_root,
    study_dir,
)

STUDY_SKELETON = """---
schema_version: "{schema}"
language: "{language}"
slug: {slug}
era: "{era}"
created: {today}
---

# {language} — dialectical study

<!-- Fill tasks in order. Do not rename headings or renumber IDs. -->

## {a}

<!-- Snapshot: what the language is today as a design, and which predecessor
contradictions it claims to resolve. Maximum 150 words. Cite every claim. -->

## {b}

### B1. Unity and struggle of opposites — WHY

<!-- Table: ID | Contradiction | Pole A | Pole B | Where they clash | Impulse produced | Evidence -->

### B2. Quantity to quality — HOW

<!-- Table: ID | Gradual accumulation | Threshold crossed | Qualitative jump | What jumped | Milestones | Evidence -->

### B3. Negation of negation — WHERE

<!-- Table: ID | Negated | Negation of the negation | Preserved at a higher level | New contradiction | Evidence -->

## {c}

<!-- Table: Axis ID | Axis | Pole A | Pole B | Position | Justification | Evidence -->

## {d}

<!-- Table: Problem | Solution | Dialectical move | Evidence -->

## {e}

<!-- Table: ID | Tension | Pole A | Pole B | Why not dissolved | Possible synthesis | Evidence -->

## {f}

<!-- Candidate axes, or the sentence "None identified." -->

## {g}

<!-- Table: ID | Hypothesis | Evidence | Falsification test -->

## {h}

<!-- Table: Field | Value -->
"""

DECISION_SKELETON = """---
schema_version: "{schema}"
language: "{language}"
slug: {slug}
role: decision-record
created: {today}
---

# {language} — what Orthon should take

## 1. Decision / Решение

<!-- One option chosen, or the synthesis of several. Reference S*, T*, AX* IDs. -->

## 2. Rationale / Обоснование

<!-- Why this option beats the alternatives. Reference C*, J* IDs. -->

## 3. Scope / Границы применимости

<!-- When it works, when it does not. -->

## 4. Implementation details / Детали реализации

<!-- Modules, interfaces, data, state, errors, permissions, security,
performance, migration, rollback. -->

## 5. Verification plan / План проверки

<!-- Tests, monitoring, staged rollout, acceptance criteria. -->

## 6. Risks and forecast / Риски и прогноз

<!-- Short term, medium-term evolution, debt, extension paths. -->

## 7. Open questions / Открытые вопросы

<!-- What the user or the team must confirm. -->
"""

MANIFEST_RENDER = """# Sources — {language}

Schema version {schema}. Machine-readable twin: `manifest.json`.
Add sources with `scripts/add_source.py`; do not edit by hand.

| ID | Kind | Title | Locator | Snapshot | SHA-256 |
|----|------|-------|---------|----------|---------|
"""


def build_parser() -> argparse.ArgumentParser:
    parser = Parser(
        prog="init_study.py",
        description=(
            "Create studies/<lang>/ with sources/, MANIFEST.md, study.md and decision.md. "
            "Refuses to overwrite an existing study unless --force is given."
        ),
        epilog=(
            "examples:\n"
            "  scripts/init_study.py --lang rust\n"
            "  scripts/init_study.py --lang zig --era 2015-2026\n"
            "  scripts/init_study.py --lang swift --root studies --force\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--lang", required=True, help="language name, e.g. rust, 'C++', zig")
    parser.add_argument(
        "--era",
        default="whole history",
        help="focus era, e.g. '2010-2015'; default: whole history",
    )
    parser.add_argument(
        "--root",
        default=None,
        help="studies directory (default: ./studies); override for a shared corpus",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="overwrite study.md and decision.md if they already exist",
    )
    return parser


def main(argv: list[str]) -> int:
    script = "init_study"
    parser = build_parser()
    if not argv:
        parser.print_usage(sys.stderr)
        print(
            "  hint: --lang is required, e.g. scripts/init_study.py --lang rust\n"
            "  run --help for all options",
            file=sys.stderr,
        )
        return EXIT_USAGE
    args = parser.parse_args(argv)

    language = args.lang.strip()
    if not language:
        fail(
            script,
            EXIT_USAGE,
            "--lang is empty",
            "a study is keyed by language name",
            "pass e.g. --lang rust",
        )
    slug = require_slug(slugify(language), script)
    directory = study_dir(studies_root(args.root), slug)
    study_path = directory / "study.md"
    decision_path = directory / "decision.md"

    if directory.exists() and not args.force:
        existing = [p.name for p in (study_path, decision_path) if p.exists()]
        if existing:
            fail(
                script,
                EXIT_REFUSED,
                f"study already exists at {directory} ({', '.join(existing)})",
                "overwriting would destroy completed runs and stable IDs",
                "edit the existing files, or pass --force to reset the skeleton",
            )

    (directory / "sources").mkdir(parents=True, exist_ok=True)
    (directory / "runs").mkdir(parents=True, exist_ok=True)

    today = date.today().isoformat()
    fields = dict(
        schema=SCHEMA_VERSION,
        language=language,
        slug=slug,
        era=args.era.strip() or "whole history",
        today=today,
    )
    study_path.write_text(
        STUDY_SKELETON.format(
            **fields,
            a=TASK_TITLES["A"],
            b=TASK_TITLES["B"],
            c=TASK_TITLES["C"],
            d=TASK_TITLES["D"],
            e=TASK_TITLES["E"],
            f=TASK_TITLES["F"],
            g=TASK_TITLES["G"],
            h=TASK_TITLES["H"],
        ),
        encoding="utf-8",
    )
    decision_path.write_text(DECISION_SKELETON.format(**fields), encoding="utf-8")

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "language": language,
        "slug": slug,
        "era": fields["era"],
        "created": today,
        "sources": [],
    }
    save_json(directory / "manifest.json", manifest)
    (directory / "MANIFEST.md").write_text(
        MANIFEST_RENDER.format(language=language, schema=SCHEMA_VERSION), encoding="utf-8"
    )

    ok(f"created {directory}")
    ok("  study.md        Tasks A-H skeleton")
    ok("  decision.md     7-section decision record")
    ok("  manifest.json   sources manifest (empty)")
    ok(f"  sources/        snapshots; required kinds: {', '.join(KIND_LABELS)}")
    ok("")
    ok(f"next: scripts/add_source.py --lang {slug} --kind spec --url <url> --title <title>")
    ok(f"      then scripts/check_sources.py --lang {slug}")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
