<!-- refreshed: 2026-06-17 -->
# Architecture

**Analysis Date:** 2026-06-17

## System Overview

```text
┌─────────────────────────────────────────────────────────────────────┐
│                        Skill Sources (git-tracked)                  │
│   skills/<name>/SKILL.md  ·  CHANGELOG.md  ·  README.md  ·  assets │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
 ┌────────────────────┐ ┌──────────────┐ ┌─────────────────────────┐
 │ package-skill.sh   │ │package-skill-│ │   release-skill.sh      │
 │ (tar.gz → .skill)  │ │claudeai.sh   │ │ (git tag + gh release)  │
 │ scripts/           │ │(zip for ai)  │ │ scripts/                │
 └────────┬───────────┘ └──────┬───────┘ └──────────┬──────────────┘
          │                    │                     │
          ▼                    ▼                     ▼
 ┌────────────────────────────────────────────────────────────────────┐
 │                          dist/  (gitignored)                       │
 │  <name>.skill  ·  <name>-<version>.skill  ·  <name>-<version>.json│
 │  <name>-claudeai.zip  ·  <name>-<version>-claudeai.zip            │
 └────────────────────────────────────────────────────────────────────┘
                                 ▲
              ┌──────────────────┘
              │
 ┌────────────────────────────────┐
 │  CI: .github/workflows/        │
 │  package-skills.yml            │
 │  • push→master: repackage all  │
 │  • published release: package  │
 │    one skill + promote CL      │
 └────────────────────────────────┘
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

**Overall:** Convention-over-configuration monorepo with independent per-skill versioning.

**Key Characteristics:**
- Each skill is a self-contained directory under `skills/`; adding a new skill requires no tooling changes.
- `SKILL.md` frontmatter (`metadata.version`) is the single source of truth for version; scripts extract it via `grep`/`sed` — no package registry or lockfile involved.
- Two distribution targets (Claude Code `.skill` tar.gz and Claude.ai `.zip`) diverge only in packaging format and description length; skill source is the same.
- Release lifecycle is fully automated via CI once a tag matching `<skill-name>/v<version>` is pushed.

## Layers

**Skill content layer:**
- Purpose: The actual deliverable — instructions consumed by Claude at runtime
- Location: `skills/<name>/`
- Contains: `SKILL.md` (required), `CHANGELOG.md` (required), `README.md` (optional), asset subdirectories for complex skills
- Depends on: Nothing (standalone markdown)
- Used by: Packaging scripts, CI, end-users who install skills

**Packaging layer:**
- Purpose: Transforms skill source into distributable archives
- Location: `scripts/`
- Contains: `package-skill.sh`, `package-skill-claudeai.sh`, `build_claudeai_skill_md.py`
- Depends on: Skill content layer (`skills/<name>/SKILL.md` must exist)
- Used by: Developers locally and by CI

**Release layer:**
- Purpose: Manages versioned git tags and GitHub releases
- Location: `scripts/release-skill.sh`, `.github/workflows/package-skills.yml`
- Contains: Tag creation, release note extraction from `[Unreleased]` CHANGELOG block, CI promotion of CHANGELOG
- Depends on: Packaging layer (calls `package-skill.sh`), `gh` CLI, git
- Used by: Developers triggering releases; CI on published release events

**Output layer:**
- Purpose: Distributable artifacts consumed by end-users
- Location: `dist/`
- Contains: `<name>.skill` (latest), `<name>-<version>.skill` (versioned), `<name>-<version>.json` (metadata), `<name>-claudeai.zip`
- Generated: Yes — gitignored, produced by packaging scripts and CI artifacts

## Data Flow

### Local Packaging

1. Developer edits `skills/<name>/SKILL.md`, bumps `metadata.version`
2. `bash scripts/package-skill.sh <name>` — reads version from frontmatter via grep/sed
3. `tar -czf dist/<name>.skill` from within `skills/<name>/`
4. Copies to `dist/<name>-<version>.skill` and writes `dist/<name>-<version>.json`

### Claude.ai Packaging

1. `bash scripts/package-skill-claudeai.sh <name>`
2. Copies skill files into staging dir `dist/claudeai-stage/<name>/`
3. `build_claudeai_skill_md.py` rewrites `SKILL.md` → `skill.md`, truncating or substituting description
4. `zip -r dist/<name>-claudeai.zip dist/claudeai-stage/<name>/`

### Release Flow

1. Developer runs `bash scripts/release-skill.sh <name>`
2. Script reads version from `skills/<name>/SKILL.md` frontmatter
3. Extracts `[Unreleased]` content from `skills/<name>/CHANGELOG.md` as release notes
4. Creates annotated tag `<name>/v<version>` and pushes to origin
5. Calls `gh release create` with the tag and notes file
6. CI `release-skill` job triggers: packages the skill, uploads `.skill` files to the release, promotes `[Unreleased]` → `[<version>] - YYYY-MM-DD` in `CHANGELOG.md`, commits and pushes

### CI Push-to-master Flow

1. Any `skills/**` change pushed to master triggers `package-all` job
2. Iterates all `skills/*/` directories, tars each to `dist/<name>.skill`
3. Uploads all as GitHub Actions artifact named `skills`

## Key Abstractions

**Skill:**
- Purpose: A named, versioned Claude Code extension distributed as a markdown file with YAML frontmatter
- Examples: `skills/playing-card-prompt/SKILL.md`, `skills/content-writer-linkedin/SKILL.md`
- Pattern: YAML frontmatter block (`---`) containing `name`, `description`, `color`, `metadata.version`, `metadata.author`; followed by free-form markdown instructions

**Namespaced release tag:**
- Purpose: Allows per-skill independent releases within a single git repo
- Pattern: `<skill-name>/v<semver>` — e.g., `playing-card-prompt/v3.20.0`
- Used by: `release-skill.sh`, CI workflow tag parser

**Distribution formats:**
- `.skill` (tar.gz): for Claude Code CLI / agentskills.io; files at archive root; `SKILL.md` uppercase; description up to 1024 chars
- `-claudeai.zip`: for Claude.ai upload; files nested under `<skill-name>/` folder; `skill.md` lowercase; description ≤ 200 chars

## Entry Points

**Local packaging:**
- Location: `scripts/package-skill.sh`
- Triggers: Developer invocation or CI `package-all` job
- Responsibilities: Version extraction, tar creation, versioned copy, metadata JSON

**Local release:**
- Location: `scripts/release-skill.sh`
- Triggers: Developer invocation
- Responsibilities: Version read, tag creation, push, `gh release create`

**CI:**
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

**Strategy:** Fail-fast (`set -e`) in all shell scripts; explicit guard clauses for missing arguments or files.

**Patterns:**
- Missing `SKILL.md`: scripts exit 1 with a human-readable error before doing any work
- Missing version in frontmatter: scripts exit 1 with guidance to add `metadata.version`
- Tag already exists: `release-skill.sh` detects and exits before pushing
- CI tag format mismatch: workflow exits with `::error::` annotation

---

*Architecture analysis: 2026-06-17*
