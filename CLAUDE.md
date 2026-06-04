# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

A distribution system for Claude skills. Skills are Claude Code extensions defined by a `SKILL.md` file (with YAML frontmatter and markdown instructions). This repo stores skill source files and provides tooling to package and distribute them as `.skill` files (tar.gz archives).

## Repo Structure

```
skills/<skill-name>/    # Skill source files (git-tracked)
  SKILL.md              # Required: skill definition with YAML frontmatter
  README.md             # Optional: user-facing documentation
dist/                   # Generated output (gitignored for .skill files)
scripts/                # Packaging and installation shell scripts
.github/workflows/      # CI: auto-packages skills on push to main
```

## Key Commands

**Package a skill into a `.skill` file:**
```bash
bash scripts/package-skill.sh <skill-name> [version]
# e.g.: bash scripts/package-skill.sh content-writer-linkedin 1.0.0
```
Outputs `dist/<skill-name>.skill` (latest), `dist/<skill-name>-<version>.skill` (versioned), and a JSON metadata file.

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

## Release Workflow

1. Edit `skills/<skill-name>/SKILL.md`
2. Run `bash scripts/package-skill.sh <skill-name> <version>`
3. Update `CHANGELOG.md`
4. `git tag -a v<version> -m "Release v<version>"` and push
5. `gh release create v<version> dist/<skill-name>-<version>.skill`

CI (`.github/workflows/package-skills.yml`) automatically packages all skills on push to `main` when files under `skills/` change, and uploads `.skill` files to GitHub Releases on published releases.

## Adding a New Skill

Create `skills/<new-skill-name>/SKILL.md` with the required frontmatter, then run the package script. The CI will pick it up automatically on push.

## After Any Change

Update `CLAUDE.md` (if structure/workflow changed) and add an entry to `CHANGELOG.md` under `## [Unreleased]`.

When releasing a new skill version, move the `## [Unreleased]` entries into a new versioned section (e.g. `## [1.1.0] - YYYY-MM-DD`) before tagging and publishing.
