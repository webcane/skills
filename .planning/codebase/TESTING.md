# TESTING
> Generated: 2026-06-17 | Focus: quality | Project: skills

## Summary
This repository has no automated tests. The primary artifacts are markdown skill definitions and bash packaging scripts, and there is no test framework, test runner, or test files present. Quality assurance relies entirely on manual review, CI packaging verification, and the CHANGELOG/review process.

## Test Framework

**Runner:** None
**Assertion Library:** None
**Test Files:** None found

No `jest.config.*`, `vitest.config.*`, `pytest.ini`, `pyproject.toml` test sections, or `*.test.*` / `*.spec.*` files exist in the repository.

## What CI Validates

The only automated quality gate is `package-skills.yml`:

1. **On push to `master`** (when `skills/**` changes): packages all skills as `.skill` tar.gz archives and uploads as GitHub Actions artifacts. This validates that `tar -czf` succeeds on each skill directory — a minimal structural check that files exist and are readable.

2. **On published release**: parses the `<skill-name>/v<version>` tag, verifies `skills/<skill-name>/SKILL.md` exists, runs `bash scripts/package-skill.sh <skill> <version>`, uploads release assets, and promotes the CHANGELOG. Validates that the skill packages without error.

Neither job runs functional tests, linting, schema validation, or content checks.

## Manual Quality Process

Based on CHANGELOG entries, quality checks happen manually during development:
- New skill features are described in detail in `## [Unreleased]` CHANGELOG entries, listing every file touched
- Reference docs (`skills/playing-card-prompt/references/`) serve as human-readable test cases and expected-output specs
- Example files (`references/example-court-king.md`, `references/example-pip-two.md`, `references/example-engine-variants.md`) document expected prompt outputs for review

## Script Validation

`scripts/package-skill.sh` performs lightweight validation:
- Checks `SKILL_NAME` argument is provided
- Checks `skills/<name>/SKILL.md` exists
- Checks `metadata.version` can be extracted from frontmatter

No validation of frontmatter field values, description length, or content correctness.

## Test Coverage Gaps

**No coverage for:**
- SKILL.md frontmatter schema validation (required fields, value constraints)
- `metadata.description_claudeai` length (<= 200 chars) — `package-skill-claudeai.sh` warns but does not fail
- Skill content correctness or completeness
- Script behavior on edge cases (missing files, malformed frontmatter, etc.)
- Python helper `scripts/build_claudeai_skill_md.py` — no unit tests

**Priority gaps:**
- **High:** Frontmatter schema validation (name, version, description fields present and well-formed) — would catch common authoring errors before release
- **Medium:** `description_claudeai` length enforcement — currently only a warning
- **Low:** Script smoke tests for `install-skill.sh`, `release-skill.sh`

## Gaps / Unknowns
- No test infrastructure exists to add to — any testing would require choosing and setting up a framework from scratch
- The `scripts/manage_config.py` skill-internal Python script has no tests; it manages `config.json` state for the playing-card-prompt skill at runtime
- CI artifact uploads are not verified for correctness of packaged content
