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
4. Tag and push: `git tag -a <skill-name>/v<version> -m "<skill-name> v<version>"` then `git push origin <skill-name>/v<version>`.
5. `gh release create <skill-name>/v<version> --title "<skill-name> v<version>"`.

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
