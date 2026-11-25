# Sources and design provenance

Read on 2026-11-25. Source wiki: `cane-wiki`, commit
`f22d7decb92c8cc0e9181a1f979ba6cceb679f65` (working-tree pages read directly).
The skill is self-contained; source links are attribution, not runtime dependencies.

## Explicitly selected wiki pages

- [[Wiki/Engineering/Process/Nyquist-Validation]] — `confidence: medium`, updated
  2026-11-04; upstream listed as `raw/2026-10-03_Nyquist-Validation.md`.
  The page distinguishes invariant observability from the mathematical theorem
  and from the GSD use of the name. We retain its uncertainty and limits.
- [[Wiki/Engineering/AI/GSD/GSD-Validate-Phase]] — `confidence: high`, updated
  2026-10-03; upstream listed as `raw/2026-08-13_GSD.md`.
  Describes requirement-to-check mapping and test-only retrospective auditing.

Raw documents are provenance recorded by the pages; they were not independently
verified for this extraction. Neither page declares lifecycle/tier; both were
explicitly selected by the user, rather than certified by a maturity filter.

## GSD primary implementation inspected

- [Auditor](https://github.com/gsd-build/get-shit-done/blob/main/agents/gsd-nyquist-auditor.md):
  generates executable behavioral checks; production implementation is read-only;
  failing test diagnosis is bounded; implementation defects are escalated.
- [Workflow](https://github.com/gsd-build/get-shit-done/blob/main/get-shit-done/workflows/validate-phase.md):
  detects phase artifacts, discovers coverage gaps, and reconciles the report.
- [Command](https://github.com/gsd-build/get-shit-done/blob/main/commands/gsd/validate-phase.md):
  phase-targeted entry point for existing and reconstructed validation contracts.
- [Template](https://github.com/gsd-build/get-shit-done/blob/main/get-shit-done/templates/VALIDATION.md):
  infrastructure, execution cadence, per-task checks, scaffolding and manual checks.

These links track `main`, not an immutable upstream version. They describe the
retrieved source, not a guarantee about the user's installed GSD version.

## Adaptation authored for this skill

The combined invariant-to-observation chain, portable modes, explicit evidence
statuses, aggregate verdict rules, and permission-aware execution are our design
synthesis. GSD is retained only as provenance, with no runtime adapter. No Nyquist
sampling formula is claimed to validate software completeness.

## OpenSpec integration sources

Inspected 2026-11-25 against upstream `main` (not an immutable version):

- [Concepts](https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md):
  current specs, change deltas, requirement headings, and behavioral scenarios.
- [Spec-driven schema](https://github.com/Fission-AI/OpenSpec/blob/main/schemas/spec-driven/schema.yaml):
  default artifacts, delta operations, and project-specific capability paths.
- [CLI](https://github.com/Fission-AI/OpenSpec/blob/main/docs/cli.md):
  optional artifact discovery and specification validation commands.
- [Workflows](https://github.com/Fission-AI/OpenSpec/blob/main/docs/workflows.md):
  iterative changes, configurable artifacts, and sync/archive as separate actions.

The in-memory effective-contract audit, report-local scenario keys,
`coverage_complete` flag and VALIDATION.md destination are this skill's design,
not additions to the OpenSpec standard schema. Local artifact formats and
installed CLI help take precedence over assumptions from upstream documentation.
