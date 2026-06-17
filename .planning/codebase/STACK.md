# STACK
> Generated: 2026-06-17 | Focus: tech | Project: skills

## Summary

This repo is a shell-script-based distribution system for Claude Code skills. The primary tooling is Bash (packaging, releasing, installing) with one Python 3 helper for YAML frontmatter processing. There are no Node.js, npm, or compiled-language dependencies — the entire build pipeline runs on standard POSIX tools plus `gh` (GitHub CLI).

## Languages

**Primary:**
- Bash — all packaging, release, and install scripts in `scripts/`

**Secondary:**
- Python 3 — `scripts/build_claudeai_skill_md.py` (YAML frontmatter rewriter for Claude.ai packaging)
- Markdown with YAML frontmatter — skill definition files (`skills/*/SKILL.md`)

## Runtime

**Environment:**
- Any POSIX shell environment (bash, macOS zsh-compatible)
- Python 3 (standard library + `yaml` / PyYAML) required for `package-skill-claudeai.sh`

**Package Manager:**
- None — no `package.json`, `requirements.txt`, `Cargo.toml`, or `go.mod`
- Python dependency: `PyYAML` (imported as `yaml` in `scripts/build_claudeai_skill_md.py`); must be available in the environment

## Frameworks

**Build/Dev:**
- `tar` (gzip) — produces `.skill` archives (`dist/<name>.skill`, `dist/<name>-<version>.skill`)
- `zip` — produces Claude.ai-compatible archives (`dist/<name>-claudeai.zip`)
- `gh` (GitHub CLI) — used in `scripts/release-skill.sh` for tagging and `gh release create`
- `git` — tagging and pushing releases

**Testing:**
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

**Platform:** GitHub Actions

**Workflows:**
- `package-skills.yml` (`.github/workflows/package-skills.yml`) — two jobs:
  - `package-all`: triggered on push to `master` when `skills/**` changes; packages every skill with `tar -czf` and uploads artifacts via `actions/upload-artifact@v6`
  - `release-skill`: triggered on published GitHub release; parses `<skill-name>/v<version>` tag, runs `scripts/package-skill.sh`, uploads `.skill` files to the release via `softprops/action-gh-release@v2`, then promotes the skill's `[Unreleased]` CHANGELOG section with a commit back to `master`

**Actions used:**
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

**Skill version source of truth:** `metadata.version` field in `skills/<name>/SKILL.md` YAML frontmatter

**Environment:**
- No `.env` files or environment variables required for local packaging
- `GITHUB_TOKEN` secret required in GitHub Actions for release uploads

## Platform Requirements

**Development:**
- macOS or Linux with bash, tar, zip, git, gh (GitHub CLI), Python 3 + PyYAML

**Production (CI):**
- `ubuntu-latest` GitHub Actions runner

## Gaps / Unknowns

- PyYAML install method not specified — assumed pre-installed or available via system Python on the developer's machine and CI runner
- `install-skill.sh` and `install-local.sh` were not read in detail; their dependencies (e.g. curl, specific install dirs) are not fully mapped
- No lockfile for any language runtime — Python version not pinned
