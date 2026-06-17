# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

A distribution system for Claude skills. Skills are Claude Code extensions defined by a `SKILL.md` file (with YAML frontmatter and markdown instructions). This repo stores skill source files and provides tooling to package and distribute them as `.skill` files (tar.gz archives) for Claude Code/agentskills.io, and as `.zip` files for Claude.ai's skill upload (see `package-skill-claudeai.sh` below).

## Repo Structure

```
skills/<skill-name>/    # Skill source files (git-tracked)
  SKILL.md              # Required: skill definition with YAML frontmatter (holds metadata.version)
  CHANGELOG.md          # Per-skill changelog (this skill's history only)
  README.md             # Optional: user-facing documentation
dist/                   # Generated output (gitignored for .skill files)
scripts/                # Packaging and installation shell scripts
CHANGELOG.md            # Repo-tooling changelog only (scripts/CI/layout)
.github/workflows/      # CI: auto-packages skills on push to main
```

## Versioning Model

**Each skill is versioned and released independently.** There is no single
repo-wide product version.

- A skill's version is the `metadata.version` field in its `SKILL.md` frontmatter — the single source of truth.
- Each skill keeps its own `skills/<name>/CHANGELOG.md`.
- Release tags are namespaced: `<skill-name>/v<version>` (e.g. `playing-card-prompt/v1.0.0`).
- The root `CHANGELOG.md` tracks only repo tooling (scripts, CI, layout), not skill content.

## Key Commands

**Package a skill into a `.skill` file:**
```bash
bash scripts/package-skill.sh <skill-name> [version]
# e.g.: bash scripts/package-skill.sh content-writer-linkedin
```
If `[version]` is omitted it is read from the skill's `SKILL.md` frontmatter (`metadata.version`).
Outputs `dist/<skill-name>.skill` (latest), `dist/<skill-name>-<version>.skill` (versioned), and a JSON metadata file.

**Package a skill for Claude.ai (separate format):**
```bash
bash scripts/package-skill-claudeai.sh <skill-name> [version]
# e.g.: bash scripts/package-skill-claudeai.sh playing-card-prompt
```
Claude.ai's skill upload differs from the `.skill` format above: it requires
a lowercase `skill.md` (not `SKILL.md`), a `description` <= 200 chars (not
1024), and a zip with the skill files nested in a `<skill-name>/` folder
(not at the zip root). This script handles all three, producing
`dist/<skill-name>-claudeai.zip` (and a versioned copy). If the skill's
frontmatter defines `metadata.description_claudeai` (<= 200 chars), that is
used as the Claude.ai description; otherwise `description` is truncated to
fit with a warning — add `description_claudeai` to avoid that.

**Install a skill from a remote repo:**
```bash
bash scripts/install-skill.sh <skill-name> [version] [install-dir]
# e.g.: INSTALL_DIR=~/.claude/skills bash scripts/install-skill.sh content-writer-linkedin
```

**Release a skill (tag, push, GitHub release):**
```bash
bash scripts/release-skill.sh [skill-name]
# e.g.: bash scripts/release-skill.sh playing-card-prompt
```
If `[skill-name]` is omitted, prompts to choose from `skills/`. Reads the
version from `SKILL.md` frontmatter (`metadata.version`), creates and pushes
the tag `<skill-name>/v<version>`, and runs `gh release create` non-
interactively (release notes come from the skill's `[Unreleased]`
CHANGELOG section, or a title-only message if that section is empty).

**Inspect a `.skill` archive:**
```bash
tar -tzf dist/<skill-name>.skill   # list contents
tar -xzf dist/<skill-name>.skill   # extract
```

## Skill File Format

`SKILL.md` must have YAML frontmatter followed by markdown:
```markdown
---
name: skill-name
description: One-line description used for skill discovery
color: cyan
---

# Skill content...
```

## Release Workflow (per skill)

1. Edit `skills/<skill-name>/SKILL.md` and bump `metadata.version` in its frontmatter.
2. Add the change to `skills/<skill-name>/CHANGELOG.md` under `## [Unreleased]`.
3. (Optional local check) `bash scripts/package-skill.sh <skill-name>` — version is read from frontmatter.
4. `bash scripts/release-skill.sh [skill-name]` — tags, pushes, and creates the GitHub release (non-interactively). If `[skill-name]` is omitted, it prompts to choose from `skills/`.

On a published release CI parses the `<skill>/v<version>` tag, packages and
uploads **only that skill**, and promotes that skill's `[Unreleased]` CHANGELOG
section to `## [<version>] - YYYY-MM-DD`. On push to `main` CI also repackages
all skills as `<name>.skill` artifacts.

## Adding a New Skill

Create `skills/<new-skill-name>/SKILL.md` with the required frontmatter (include
`metadata.version`, start at `1.0.0`) and a `skills/<new-skill-name>/CHANGELOG.md`.
Add it to the Skills table in `README.md`. CI packages it automatically on push.

## After Any Change

- Skill content change → add an entry to that skill's `skills/<name>/CHANGELOG.md` under `## [Unreleased]`.
- Any change to a skill's `SKILL.md` → bump `metadata.version` (minor version, e.g. `1.1.1` → `1.2.0`) in that same change.
- Tooling/CI/layout change → add an entry to the root `CHANGELOG.md` under `## [Unreleased]`.
- Update `CLAUDE.md` if structure/workflow changed.

Releasing is handled by CI (it promotes `[Unreleased]` on a published release); only promote a CHANGELOG section by hand if releasing without CI.

<!-- GSD:project-start source:PROJECT.md -->
## Project

**playing-card-prompt: Feature Expansion (v4)**

The `playing-card-prompt` skill is an interactive Claude wizard that builds
image-generation prompts for stylized playing cards. It supports four deck
systems, six court-lettering systems, rich style/layer configuration, and
persistent profiles. This project extends the skill with six new features:
figure type classification, split layout control, card back generation,
special/prospect cards, title overlay, and seamless group design.

**Core Value:** Give the user precise, repeatable control over every meaningful aspect of a
card's figure and layout — so prompts produce consistent results across a
full deck.

### Constraints

- **Compatibility**: `manage_config.py` schema change (`figure_proportion` →
  `figure_scale` + `character_framing`) must not break existing `config.json`
  files — provide a migration/fallback read path.
- **Scope**: No SVG or image output from this skill; output remains a text
  prompt in a code block.
- **Wizard UX**: AskUserQuestion max 4 options per question; new steps must
  fit this limit.
- **Asset file convention**: new persistent fields need entries in
  `references/CONFIG.md`; new wizard steps need entries in
  `references/WIZARD-STEP-MAP.md`.
<!-- GSD:project-end -->

<!-- GSD:stack-start source:codebase/STACK.md -->
## Technology Stack

## Summary
## Languages
- Bash — all packaging, release, and install scripts in `scripts/`
- Python 3 — `scripts/build_claudeai_skill_md.py` (YAML frontmatter rewriter for Claude.ai packaging)
- Markdown with YAML frontmatter — skill definition files (`skills/*/SKILL.md`)
## Runtime
- Any POSIX shell environment (bash, macOS zsh-compatible)
- Python 3 (standard library + `yaml` / PyYAML) required for `package-skill-claudeai.sh`
- None — no `package.json`, `requirements.txt`, `Cargo.toml`, or `go.mod`
- Python dependency: `PyYAML` (imported as `yaml` in `scripts/build_claudeai_skill_md.py`); must be available in the environment
## Frameworks
- `tar` (gzip) — produces `.skill` archives (`dist/<name>.skill`, `dist/<name>-<version>.skill`)
- `zip` — produces Claude.ai-compatible archives (`dist/<name>-claudeai.zip`)
- `gh` (GitHub CLI) — used in `scripts/release-skill.sh` for tagging and `gh release create`
- `git` — tagging and pushing releases
- Not detected — no test framework present
## Key Scripts
| Script | Purpose | Path |
|--------|---------|------|
| `package-skill.sh` | Package a skill as `.skill` (tar.gz) | `scripts/package-skill.sh` |
| `package-skill-claudeai.sh` | Package a skill as Claude.ai `.zip` | `scripts/package-skill-claudeai.sh` |
| `build_claudeai_skill_md.py` | Rewrite SKILL.md frontmatter for Claude.ai 200-char description limit | `scripts/build_claudeai_skill_md.py` |
| `release-skill.sh` | Tag, push, and create GitHub release | `scripts/release-skill.sh` |
| `install-skill.sh` | Install a skill from remote repo | `scripts/install-skill.sh` |
| `install-local.sh` | Install a skill from local source | `scripts/install-local.sh` |
## CI/CD
- `package-skills.yml` (`.github/workflows/package-skills.yml`) — two jobs:
- `actions/checkout@v5`
- `actions/upload-artifact@v6`
- `softprops/action-gh-release@v2`
## Output Artifacts
- `dist/<name>.skill` — latest tar.gz archive (gitignored)
- `dist/<name>-<version>.skill` — versioned tar.gz archive (gitignored)
- `dist/<name>-<version>.json` — metadata JSON (gitignored)
- `dist/<name>-claudeai.zip` — Claude.ai-compatible zip (gitignored)
- `dist/<name>-claudeai-<version>.zip` — versioned Claude.ai zip (gitignored)
## Configuration
- No `.env` files or environment variables required for local packaging
- `GITHUB_TOKEN` secret required in GitHub Actions for release uploads
## Platform Requirements
- macOS or Linux with bash, tar, zip, git, gh (GitHub CLI), Python 3 + PyYAML
- `ubuntu-latest` GitHub Actions runner
## Gaps / Unknowns
- PyYAML install method not specified — assumed pre-installed or available via system Python on the developer's machine and CI runner
- `install-skill.sh` and `install-local.sh` were not read in detail; their dependencies (e.g. curl, specific install dirs) are not fully mapped
- No lockfile for any language runtime — Python version not pinned
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

## Summary
## Skill File Conventions
## Versioning
- **PATCH** (x.y.Z): bug fixes
- **MINOR** (x.Y.z): new features
- **MAJOR** (X.y.z): breaking changes
## Git Commit Message Conventions
- `chore:` — tooling, CI, CHANGELOG promotion (e.g., `chore: promote playing-card-prompt CHANGELOG for v3.19.0`)
- `<skill-name>:` — skill-specific changes prefixed with skill name (e.g., `playing-card-prompt: add Joker card support (v3.20.0)`)
- `fix:` — bug fixes
- `Merge ...` — merge commits (standard git format)
## Git Tag Convention
- `playing-card-prompt/v3.20.0`
- `content-writer-linkedin/v1.0.0`
## CHANGELOG Conventions
- `CHANGELOG.md` (root) — repo tooling only (scripts, CI, layout). Never skill content.
- `skills/<name>/CHANGELOG.md` — that skill's history only.
## Directory and File Naming
- `SKILL.md` — skill definition (uppercase, required)
- `CHANGELOG.md` — version history (uppercase)
- `README.md` — user documentation (uppercase)
- `TODO.md` — open work items (uppercase)
- `ROADMAP.md` — future plans (uppercase)
- `config.json` — runtime config (lowercase, gitignored if user-modified)
## Shell Script Style
- Start with `#!/bin/bash`
- Use `set -e` for early exit on errors
- Block comment header explaining usage at top
- Guard clauses with inline error messages: `[ -z "$VAR" ] && echo "..." && exit 1`
- Use `SCREAMING_SNAKE_CASE` for all variable names
- Derive paths from `BASH_SOURCE[0]` rather than assuming cwd
## Skill Content Style
- H1 (`#`) for the skill title
- H2 (`##`) for major sections
- Tables for option/trigger mapping
- Bold for key terms and modes
- Code blocks for exact strings and commands
## Gaps / Unknowns
- No linting or formatting tools configured (no `.eslintrc`, `.prettierrc`, `pyproject.toml`)
- No enforced commit message hook (conventions are by practice, not tooling)
- `color` field in frontmatter appears optional; no documented list of valid values
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

## System Overview
```text
```
## Component Responsibilities
| Component | Responsibility | Path |
|-----------|----------------|------|
| Skill source directory | All content and assets for one skill | `skills/<name>/` |
| `SKILL.md` | Skill definition: YAML frontmatter (version, description, color) + markdown instructions | `skills/<name>/SKILL.md` |
| `package-skill.sh` | Packages a skill into a `.skill` (tar.gz) for Claude Code / agentskills.io | `scripts/package-skill.sh` |
| `package-skill-claudeai.sh` | Packages a skill into a `.zip` for Claude.ai upload (different naming + description constraints) | `scripts/package-skill-claudeai.sh` |
| `build_claudeai_skill_md.py` | Python helper: rewrites `SKILL.md` → `skill.md` and truncates description to ≤200 chars | `scripts/build_claudeai_skill_md.py` |
| `release-skill.sh` | Creates namespaced git tag `<skill>/v<version>`, pushes it, and calls `gh release create` | `scripts/release-skill.sh` |
| `install-skill.sh` | Downloads and installs a skill from a remote repo to a local install dir | `scripts/install-skill.sh` |
| `install-local.sh` | Local installation helper | `scripts/install-local.sh` |
| CI workflow | Repackages all skills on push to master; packages one skill and promotes CHANGELOG on release | `.github/workflows/package-skills.yml` |
| `dist/` | Generated output: `.skill` archives, versioned `.skill` copies, `.json` metadata, Claude.ai zips | `dist/` (gitignored) |
## Pattern Overview
- Each skill is a self-contained directory under `skills/`; adding a new skill requires no tooling changes.
- `SKILL.md` frontmatter (`metadata.version`) is the single source of truth for version; scripts extract it via `grep`/`sed` — no package registry or lockfile involved.
- Two distribution targets (Claude Code `.skill` tar.gz and Claude.ai `.zip`) diverge only in packaging format and description length; skill source is the same.
- Release lifecycle is fully automated via CI once a tag matching `<skill-name>/v<version>` is pushed.
## Layers
- Purpose: The actual deliverable — instructions consumed by Claude at runtime
- Location: `skills/<name>/`
- Contains: `SKILL.md` (required), `CHANGELOG.md` (required), `README.md` (optional), asset subdirectories for complex skills
- Depends on: Nothing (standalone markdown)
- Used by: Packaging scripts, CI, end-users who install skills
- Purpose: Transforms skill source into distributable archives
- Location: `scripts/`
- Contains: `package-skill.sh`, `package-skill-claudeai.sh`, `build_claudeai_skill_md.py`
- Depends on: Skill content layer (`skills/<name>/SKILL.md` must exist)
- Used by: Developers locally and by CI
- Purpose: Manages versioned git tags and GitHub releases
- Location: `scripts/release-skill.sh`, `.github/workflows/package-skills.yml`
- Contains: Tag creation, release note extraction from `[Unreleased]` CHANGELOG block, CI promotion of CHANGELOG
- Depends on: Packaging layer (calls `package-skill.sh`), `gh` CLI, git
- Used by: Developers triggering releases; CI on published release events
- Purpose: Distributable artifacts consumed by end-users
- Location: `dist/`
- Contains: `<name>.skill` (latest), `<name>-<version>.skill` (versioned), `<name>-<version>.json` (metadata), `<name>-claudeai.zip`
- Generated: Yes — gitignored, produced by packaging scripts and CI artifacts
## Data Flow
### Local Packaging
### Claude.ai Packaging
### Release Flow
### CI Push-to-master Flow
## Key Abstractions
- Purpose: A named, versioned Claude Code extension distributed as a markdown file with YAML frontmatter
- Examples: `skills/playing-card-prompt/SKILL.md`, `skills/content-writer-linkedin/SKILL.md`
- Pattern: YAML frontmatter block (`---`) containing `name`, `description`, `color`, `metadata.version`, `metadata.author`; followed by free-form markdown instructions
- Purpose: Allows per-skill independent releases within a single git repo
- Pattern: `<skill-name>/v<semver>` — e.g., `playing-card-prompt/v3.20.0`
- Used by: `release-skill.sh`, CI workflow tag parser
- `.skill` (tar.gz): for Claude Code CLI / agentskills.io; files at archive root; `SKILL.md` uppercase; description up to 1024 chars
- `-claudeai.zip`: for Claude.ai upload; files nested under `<skill-name>/` folder; `skill.md` lowercase; description ≤ 200 chars
## Entry Points
- Location: `scripts/package-skill.sh`
- Triggers: Developer invocation or CI `package-all` job
- Responsibilities: Version extraction, tar creation, versioned copy, metadata JSON
- Location: `scripts/release-skill.sh`
- Triggers: Developer invocation
- Responsibilities: Version read, tag creation, push, `gh release create`
- Location: `.github/workflows/package-skills.yml`
- Triggers: Push to master (paths: `skills/**`) or published GitHub release
- Responsibilities: Two distinct jobs — bulk repackage on push, single-skill release + CHANGELOG promotion on release
## Architectural Constraints
- **No build system:** No npm, Make, or task runner — all tooling is plain bash scripts and one Python helper.
- **No lockfile / registry:** Skill versions are stored only in `SKILL.md` frontmatter; `grep`/`sed` extracts them.
- **`dist/` is gitignored:** Generated artifacts are never committed; CI uploads them as release assets or workflow artifacts.
- **Tag namespace isolation:** The `<skill-name>/v<version>` tag convention is load-bearing — the CI workflow's `release-skill` job parses it to identify which skill to package.
- **Case sensitivity hazard:** On macOS (case-insensitive filesystem), `SKILL.md` and `skill.md` are the same file. `build_claudeai_skill_md.py` writes to a temp file first to avoid clobbering the original.
- **`gh` CLI dependency:** `release-skill.sh` and CI require the GitHub CLI (`gh`) to be authenticated.
## Error Handling
- Missing `SKILL.md`: scripts exit 1 with a human-readable error before doing any work
- Missing version in frontmatter: scripts exit 1 with guidance to add `metadata.version`
- Tag already exists: `release-skill.sh` detects and exits before pushing
- CI tag format mismatch: workflow exits with `::error::` annotation
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->
## Project Skills

No project skills found. Add skills to any of: `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, `.github/skills/`, or `.codex/skills/` with a `SKILL.md` index file.
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->

<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
