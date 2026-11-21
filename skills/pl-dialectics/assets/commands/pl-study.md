---
description: Run one dialectical language study (Tasks A-H) plus the 7-section decision record
argument-hint: "<language> [era] [run1|run2] [--root studies]"
---

Run one language study using the `pl-dialectics` skill.

Arguments: `$ARGUMENTS`

Parse the arguments as:

- first token — the language name (required). Everything else is optional.
- `--era <value>` or a bare year range — focus era, default "whole history".
- `--run 1` or `--run 2` — run only that half. Default: both halves in one session.
- `--root <dir>` — studies directory, default `./studies`.

Then:

1. Load `pl-dialectics/SKILL.md` and follow it. Do not restate its rules here.
2. If `studies/<slug>/manifest.json` does not exist, run
   `scripts/init_study.py --lang "<language>" --era "<era>" --root <root>`.
3. Run gate G0 (`scripts/check_sources.py`). If it fails, collect the missing source classes
   with `scripts/add_source.py` before writing a single line of the report.
4. Execute the requested run(s), writing into `studies/<slug>/study.md`.
5. Finish with `scripts/validate_report.py --lang <slug> --stage final --emit-json`.
   Do not report success while it exits non-zero.

Report back: the language, the artifact paths, the gate results, and the IDs that were
assigned. Do not paste the full study into chat — it lives on disk.
