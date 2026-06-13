# Changelog — repo tooling

Changes to the distribution tooling itself (scripts, CI, repo layout).
**Per-skill changes live in each skill's own `skills/<name>/CHANGELOG.md`**,
and each skill is versioned and released independently.

## [Unreleased]

### Added
- `scripts/install-local.sh`: build a skill from source and install/reinstall it into a local Claude skills directory, with an interactive picker when no skill name is given
- Documented local build/install/reinstall workflow in `README.md`
- `scripts/package-skill-claudeai.sh` (with helper `scripts/build_claudeai_skill_md.py`): packages a skill for Claude.ai's skill upload, which has different requirements than the `.skill` (tar.gz) format — lowercase `skill.md` instead of `SKILL.md`, a `description` <= 200 chars instead of 1024, and a zip with the skill files nested in a `<skill-name>/` folder instead of at the zip root. Outputs `dist/<skill-name>-claudeai.zip` and a versioned copy. Honors an optional `metadata.description_claudeai` frontmatter field for a purpose-written short description; otherwise truncates `description` to fit with a warning
- Documented the Claude.ai packaging workflow and `metadata.description_claudeai` field in `README.md` and `CLAUDE.md`
- `dist/*.zip` added to `.gitignore`

### Changed
- Bumped CI actions to Node.js 24-compatible versions: `actions/checkout@v5`, `actions/upload-artifact@v6`
- Switched to **per-skill versioning**: each skill carries its version in `SKILL.md` frontmatter (`metadata.version`), keeps its own `CHANGELOG.md`, and is released under a namespaced tag `<skill>/v<version>`
- `package-skill.sh` now reads the version from `SKILL.md` frontmatter when no version argument is passed
- CI (`package-skills.yml`) parses the release tag, packages and uploads only the tagged skill, and promotes that skill's `[Unreleased]` CHANGELOG section to a versioned one
- Synced `README.md`, `QUICK_START.md`, and `CLAUDE.md` to the per-skill release workflow

## Versioning

We follow [Semantic Versioning](https://semver.org/) **per skill**:
- PATCH: Bug fixes (1.0.1)
- MINOR: New features (1.1.0)
- MAJOR: Breaking changes (2.0.0)

Tag format: `<skill-name>/v<version>` (e.g. `playing-card-prompt/v1.0.0`).
