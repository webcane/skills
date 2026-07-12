# Changelog — repo tooling

Changes to the distribution tooling itself (scripts, CI, repo layout).
**Per-skill changes live in each skill's own `skills/<name>/CHANGELOG.md`**,
and each skill is versioned and released independently.

## [Unreleased]

### Added
- `skills/python-quiz/`: новый скилл — интерактивный тест Python по .md файлам в директории (single/multi-choice, short answer, coding task, bash-таймер, разбор ошибок)
- `scripts/release-skill.sh`: packages skill before release and uploads `.skill` + versioned `.skill` + `.json` metadata as release assets via `gh release create`
- `scripts/release-skill.sh`: tags, pushes, and creates a GitHub release for a skill, with an interactive picker when no skill name is given. Reads the version from `SKILL.md` frontmatter (`metadata.version`), tags `<skill-name>/v<version>`, and runs `gh release create` non-interactively using the skill's `[Unreleased]` CHANGELOG section as release notes (falling back to a title-only message)
- `scripts/install-local.sh`: build a skill from source and install/reinstall it into a local Claude skills directory, with an interactive picker when no skill name is given
- `scripts/package-skill-claudeai.sh` (with helper `scripts/build_claudeai_skill_md.py`): packages a skill for Claude.ai's skill upload — lowercase `skill.md`, description ≤ 200 chars, zip with files nested in `<skill-name>/` folder. Honors `metadata.description_claudeai` frontmatter field; otherwise truncates `description` with a warning
- Documented local build/install/reinstall and Claude.ai packaging workflows in `README.md` and `CLAUDE.md`
- `dist/*.zip` added to `.gitignore`

### Changed
- `scripts/install-local.sh`: interactive picker now lists skill names instead of full directory paths
- Bumped CI actions to Node.js 24-compatible versions: `actions/checkout@v5`, `actions/upload-artifact@v6`
- Switched to **per-skill versioning**: each skill carries its version in `SKILL.md` frontmatter (`metadata.version`), keeps its own `CHANGELOG.md`, and is released under a namespaced tag `<skill>/v<version>`
- `package-skill.sh` now reads the version from `SKILL.md` frontmatter when no version argument is passed
- CI (`package-skills.yml`) parses the release tag, packages and uploads only the tagged skill, and promotes that skill's `[Unreleased]` CHANGELOG section to a versioned one
- Synced `README.md`, `QUICK_START.md`, and `CLAUDE.md` to the per-skill release workflow
- `CLAUDE.md`: updated release workflow docs — clarified that `release-skill.sh` promotes CHANGELOG locally; added explicit rule against writing versioned headers by hand; repositioned CI as fallback for manual tag pushes

### Fixed
- `scripts/release-skill.sh`: promotes `[Unreleased]` CHANGELOG locally before tagging so CI's promotion step is always a no-op — eliminates post-release push that diverged local master from origin
- `scripts/release-skill.sh`: `git fetch origin master --tags` so remote-only tags are detected by the tag-existence guard before any modifications are made
- `scripts/release-skill.sh`: guard — aborts if local master is behind `origin/master` before any changes are made
- `scripts/release-skill.sh`: guard — warns explicitly when `[Unreleased]` section has no content (silent title-only was confusing)
- `.github/workflows/package-skills.yml`: `git push origin master` in the promote step is now conditional on an actual commit — avoids redundant no-op push when promotion was already done locally
- `package-skills.yml`: fixed reference to non-existent `main` branch (repo uses `master`)
- `package-skills.yml`: `package-all` job's loop skips `skills/*` dirs with no `SKILL.md` instead of failing
- `scripts/install-skill.sh`: pinned-version download URL now uses namespaced `${SKILL_NAME}%2Fv${VERSION}` release tag (bare `v${VERSION}` never existed → 404)
- `scripts/install-skill.sh`: `BRANCH` defaulted to `main`; now defaults to `master`
- `scripts/install-skill.sh`: `SKILL_NAME` validated against `[A-Za-z0-9_-]+` allowlist to prevent path traversal

### Removed
- Deleted the stray `.github/workflows/asd` file (a non-workflow garbage file in the workflows dir)

## Versioning

We follow [Semantic Versioning](https://semver.org/) **per skill**:
- PATCH: Bug fixes (1.0.1)
- MINOR: New features (1.1.0)
- MAJOR: Breaking changes (2.0.0)

Tag format: `<skill-name>/v<version>` (e.g. `playing-card-prompt/v1.0.0`).
