# Changelog — repo tooling

Changes to the distribution tooling itself (scripts, CI, repo layout).
**Per-skill changes live in each skill's own `skills/<name>/CHANGELOG.md`**,
and each skill is versioned and released independently.

## [Unreleased]

### Added
- `scripts/release-skill.sh`: tags, pushes, and creates a GitHub release for a skill, with an interactive picker when no skill name is given. Reads the version from `SKILL.md` frontmatter (`metadata.version`), tags `<skill-name>/v<version>`, and runs `gh release create` non-interactively using the skill's `[Unreleased]` CHANGELOG section as release notes (falling back to a title-only message)
- `scripts/install-local.sh`: build a skill from source and install/reinstall it into a local Claude skills directory, with an interactive picker when no skill name is given
- Documented local build/install/reinstall workflow in `README.md`
- `scripts/package-skill-claudeai.sh` (with helper `scripts/build_claudeai_skill_md.py`): packages a skill for Claude.ai's skill upload, which has different requirements than the `.skill` (tar.gz) format — lowercase `skill.md` instead of `SKILL.md`, a `description` <= 200 chars instead of 1024, and a zip with the skill files nested in a `<skill-name>/` folder instead of at the zip root. Outputs `dist/<skill-name>-claudeai.zip` and a versioned copy. Honors an optional `metadata.description_claudeai` frontmatter field for a purpose-written short description; otherwise truncates `description` to fit with a warning
- Documented the Claude.ai packaging workflow and `metadata.description_claudeai` field in `README.md` and `CLAUDE.md`
- `dist/*.zip` added to `.gitignore`

### Changed
- `scripts/install-local.sh`: interactive picker now lists skill names (e.g. `playing-card-prompt`) instead of full directory paths
- Bumped CI actions to Node.js 24-compatible versions: `actions/checkout@v5`, `actions/upload-artifact@v6`
- Fixed `package-skills.yml` referencing a non-existent `main` branch (repo's branch is `master`), which caused `actions/checkout` to fail fetching `refs/heads/main*` on every release run
- Switched to **per-skill versioning**: each skill carries its version in `SKILL.md` frontmatter (`metadata.version`), keeps its own `CHANGELOG.md`, and is released under a namespaced tag `<skill>/v<version>`
- `package-skill.sh` now reads the version from `SKILL.md` frontmatter when no version argument is passed
- CI (`package-skills.yml`) parses the release tag, packages and uploads only the tagged skill, and promotes that skill's `[Unreleased]` CHANGELOG section to a versioned one
- Synced `README.md`, `QUICK_START.md`, and `CLAUDE.md` to the per-skill release workflow

### Fixed
- `scripts/install-skill.sh`: pinned-version download URL built a bare `v${VERSION}` tag that never exists; now uses the namespaced `${SKILL_NAME}%2Fv${VERSION}` release tag so versioned installs resolve instead of 404ing
- `scripts/install-skill.sh`: `BRANCH` defaulted to `main`; now defaults to `master` (the repo's actual default branch)
- `scripts/install-skill.sh`: `SKILL_NAME` argument was used unsanitized in `mkdir`/`tar -C` paths, allowing path traversal (e.g. `../../../etc`); now validated against a `[A-Za-z0-9_-]+` allowlist before use
- `package-skills.yml`: `package-all` job's loop now skips `skills/*` directories that have no `SKILL.md` (via `|| continue`) instead of failing the bulk-package job on a stub dir

### Removed
- Deleted the stray `.github/workflows/asd` file (a non-workflow garbage file in the workflows dir)

## Versioning

We follow [Semantic Versioning](https://semver.org/) **per skill**:
- PATCH: Bug fixes (1.0.1)
- MINOR: New features (1.1.0)
- MAJOR: Breaking changes (2.0.0)

Tag format: `<skill-name>/v<version>` (e.g. `playing-card-prompt/v1.0.0`).
