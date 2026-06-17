# Codebase Structure

**Analysis Date:** 2026-06-17

## Directory Layout

```
skills/                          # Skill source files (git-tracked)
├── content-writer-linkedin/     # LinkedIn article writing skill
│   ├── SKILL.md                 # Skill definition + instructions
│   └── CHANGELOG.md             # Per-skill version history
├── playing-card/                # Playing card skill (ROADMAP.md only — in-progress)
│   └── ROADMAP.md
├── playing-card-prompt/         # Image-gen prompt wizard for playing cards
│   ├── SKILL.md                 # Primary skill definition (v3.20.0)
│   ├── CHANGELOG.md
│   ├── README.md
│   ├── assets/                  # Reference assets for prompt building
│   │   ├── courts/
│   │   ├── decks/
│   │   ├── engines/
│   │   ├── figure-proportion/
│   │   ├── frame/
│   │   ├── index/
│   │   ├── lettering/
│   │   ├── mood/
│   │   └── pattern/
│   ├── references/
│   └── scripts/                 # Skill-internal Python scripts (config management)
└── playing-deck/                # Playing deck skill (ROADMAP.md only — in-progress)
    └── ROADMAP.md

scripts/                         # Repo-level packaging and release tooling
├── package-skill.sh             # Package a skill as .skill (tar.gz)
├── package-skill-claudeai.sh    # Package a skill as .zip for Claude.ai upload
├── build_claudeai_skill_md.py   # Python: rewrite SKILL.md for Claude.ai constraints
├── release-skill.sh             # Create git tag + GitHub release for a skill
├── install-skill.sh             # Install a skill from remote repo
└── install-local.sh             # Install a skill from local source

.github/
└── workflows/
    └── package-skills.yml       # CI: repackage on push; package + promote on release

dist/                            # Generated artifacts (gitignored)
├── <name>.skill                 # Latest packaged skill (tar.gz)
├── <name>-<version>.skill       # Versioned packaged skill
├── <name>-<version>.json        # Metadata sidecar
└── <name>-claudeai.zip          # Claude.ai-format zip

.planning/                       # Planning documents (not gitignored)
└── codebase/                    # Codebase maps written by GSD mapper
    ├── ARCHITECTURE.md
    └── STRUCTURE.md

CLAUDE.md                        # Project instructions for Claude Code
README.md                        # User-facing documentation; skills table
CHANGELOG.md                     # Repo tooling changelog only (not skill content)
```

## Directory Purposes

**`skills/`:**
- Purpose: All skill source content; the primary deliverable of the repo
- Contains: One subdirectory per skill, each with `SKILL.md` (required), `CHANGELOG.md` (required), optional `README.md`, optional `assets/`, optional internal `scripts/`
- Key files: `skills/playing-card-prompt/SKILL.md` (most complex skill), `skills/content-writer-linkedin/SKILL.md`

**`scripts/`:**
- Purpose: Developer tooling for packaging, releasing, and installing skills
- Contains: Bash scripts and one Python helper; no runtime dependencies beyond bash, python3, tar, zip, and `gh` CLI
- Key files: `scripts/package-skill.sh` (primary packaging), `scripts/release-skill.sh` (release automation)

**`.github/workflows/`:**
- Purpose: CI automation for packaging and release promotion
- Contains: Single workflow file covering two trigger paths (push and release)
- Key files: `.github/workflows/package-skills.yml`

**`dist/`:**
- Purpose: Output directory for generated archives
- Generated: Yes — produced by packaging scripts
- Committed: No — gitignored (`.skill` files); only CI uploads them as artifacts/release assets

**`.planning/codebase/`:**
- Purpose: Codebase maps for GSD planning tools
- Generated: Yes — by GSD mapper agents
- Committed: Yes

## Key File Locations

**Skill definitions (single source of truth for version + instructions):**
- `skills/playing-card-prompt/SKILL.md`: Most developed skill; v3.20.0; has assets + internal scripts
- `skills/content-writer-linkedin/SKILL.md`: LinkedIn writing skill; v1.0.0

**Packaging scripts:**
- `scripts/package-skill.sh`: Claude Code / agentskills.io format (tar.gz, `SKILL.md` uppercase)
- `scripts/package-skill-claudeai.sh`: Claude.ai format (zip, `skill.md` lowercase, description ≤200 chars)
- `scripts/build_claudeai_skill_md.py`: Python helper invoked by `package-skill-claudeai.sh`

**Release tooling:**
- `scripts/release-skill.sh`: Tag + GitHub release; extracts notes from `[Unreleased]` CHANGELOG block

**CI:**
- `.github/workflows/package-skills.yml`: Two-job workflow (push → bulk repackage; release → single skill + CHANGELOG promotion)

**Repo-level docs:**
- `CLAUDE.md`: Authoritative guide for Claude Code working in this repo
- `README.md`: User-facing; includes skills table
- `CHANGELOG.md`: Tooling-only history (not skill content)

## Naming Conventions

**Skill directories:**
- Pattern: `kebab-case` matching the `name` field in `SKILL.md` frontmatter
- Examples: `playing-card-prompt`, `content-writer-linkedin`

**Skill files:**
- `SKILL.md` — always uppercase in source; packaging scripts rename to lowercase `skill.md` for Claude.ai
- `CHANGELOG.md` — per-skill history; must have `## [Unreleased]` section for CI promotion to work
- `README.md` — optional; user-facing

**Distribution artifacts:**
- `<name>.skill` — latest (overwritten on each packaging)
- `<name>-<version>.skill` — versioned copy
- `<name>-<version>.json` — metadata sidecar
- `<name>-claudeai.zip` / `<name>-<version>-claudeai.zip` — Claude.ai format

**Git release tags:**
- Pattern: `<skill-name>/v<semver>` — e.g., `playing-card-prompt/v3.20.0`

## Where to Add New Code

**New skill:**
1. Create `skills/<new-skill-name>/SKILL.md` with YAML frontmatter including `name`, `description`, `color`, `metadata.version` (start at `1.0.0`), `metadata.author`
2. Create `skills/<new-skill-name>/CHANGELOG.md` with `## [Unreleased]` section
3. Add entry to skills table in `README.md`
4. Optionally add `metadata.description_claudeai` (≤200 chars) to frontmatter for Claude.ai packaging
5. CI packages it automatically on next push to master

**New packaging script:**
- Location: `scripts/`
- Follow bash conventions of existing scripts: `set -e`, guard clauses for missing args, `REPO_ROOT` derivation via `dirname`

**Skill assets (complex skills):**
- Location: `skills/<name>/assets/<category>/`
- Example: `skills/playing-card-prompt/assets/courts/`

**Skill-internal scripts (config management, etc.):**
- Location: `skills/<name>/scripts/`
- Example: `skills/playing-card-prompt/scripts/`

## Special Directories

**`dist/`:**
- Purpose: Generated distribution artifacts
- Generated: Yes (by `package-skill.sh`, `package-skill-claudeai.sh`, CI)
- Committed: No (gitignored)

**`dist/claudeai-stage/`:**
- Purpose: Temporary staging directory used during Claude.ai zip creation; cleaned before each run
- Generated: Yes
- Committed: No

**`.planning/`:**
- Purpose: GSD planner/mapper output
- Generated: Yes (by GSD agents)
- Committed: Yes

---

*Structure analysis: 2026-06-17*
