# Changelog — repo tooling

Changes to the distribution tooling itself (scripts, CI, repo layout).
**Per-skill changes live in each skill's own `skills/<name>/CHANGELOG.md`**,
and each skill is versioned and released independently.

## [Unreleased]

### Added
- `scripts/install-local.sh`: build a skill from source and install/reinstall it into a local Claude skills directory, with an interactive picker when no skill name is given
- Documented local build/install/reinstall workflow in `README.md`

### Changed
- Bumped CI actions to Node.js 24-compatible versions: `actions/checkout@v4`, `actions/upload-artifact@v4`, `softprops/action-gh-release@v2`
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
