# Claude Skills Repository

Distribute Claude skills via GitHub with version control and one-line installation.

## How It Works

```
skills/          →   package-skill.sh   →   dist/*.skill   →   GitHub Release   →   curl install
(source, git)                               (generated)
```

## Quick Setup

```bash
# 1. Set metadata.version in skills/<skillname>/SKILL.md, then package
bash scripts/package-skill.sh <skillname>          # version read from frontmatter

# 2. Release (per-skill, namespaced tag)
git tag -a <skillname>/v1.0.0 -m "<skillname> v1.0.0"
git push origin <skillname>/v1.0.0
gh release create <skillname>/v1.0.0 --title "<skillname> v1.0.0"

# 3. Users install
curl -L https://raw.githubusercontent.com/webcane/skills/main/dist/<skillname>.skill \
  -o <skillname>.skill
```

Each skill is versioned and released independently. The version lives in the
skill's `SKILL.md` frontmatter (`metadata.version`); release tags are
`<skillname>/v<version>`.

For full setup instructions, see [QUICK_START.md](QUICK_START.md).

## Local Build & Install (Reinstall)

Build a skill from source and install/reinstall it into your local Claude
skills directory (`~/.claude/skills` by default) without going through
GitHub releases:

```bash
# Pick a skill interactively from skills/
bash scripts/install-local.sh

# Or specify it directly
bash scripts/install-local.sh <skillname>

# Install elsewhere
INSTALL_DIR=/path/to/skills bash scripts/install-local.sh <skillname>
```

This packages the skill (version read from `SKILL.md` frontmatter) and
re-extracts it over any existing local copy — safe to re-run after every
local change to pick up edits.

## Packaging for Claude.ai

Claude.ai's skill upload has different requirements than the `.skill`
(tar.gz) format above: the definition file must be lowercase `skill.md`, its
`description` must be <= 200 chars (vs. 1024), and the zip must contain a
top-level folder named after the skill rather than loose files at the root.

```bash
bash scripts/package-skill-claudeai.sh <skillname>          # version read from frontmatter
```

This produces `dist/<skillname>-claudeai.zip` (and a versioned copy), with
`SKILL.md` renamed to `skill.md` inside a `<skillname>/` folder. If the
skill's frontmatter defines `metadata.description_claudeai` (<= 200 chars),
that short description is used; otherwise the main `description` is
truncated to fit, with a warning.

## Repository Structure

```
├── skills/content-writer-linkedin/   # Source (git tracked)
│   ├── SKILL.md                      # frontmatter holds metadata.version
│   ├── CHANGELOG.md                  # per-skill changelog
│   └── README.md
├── scripts/
│   ├── package-skill.sh              # skill dir → .skill file
│   ├── package-skill-claudeai.sh     # skill dir → Claude.ai-compatible .zip
│   ├── build_claudeai_skill_md.py    # SKILL.md → skill.md frontmatter rewrite
│   └── install-skill.sh             # download & extract .skill
├── dist/                             # Generated, gitignored
├── .github/workflows/package-skills.yml
├── CHANGELOG.md
└── .gitignore
```

## Skills

| Skill | Description |
|-------|-------------|
| [content-writer-linkedin](skills/content-writer-linkedin/) | Write authentic LinkedIn articles |
| [hr-answer-coach](skills/hr-answer-coach/) | Interactive wizard that flags HR-interview red flags and rewrites the answer |
| [playing-card-prompt](skills/playing-card-prompt/) | Interactive wizard that builds stylized playing card image prompts |
| [thesis-to-text](skills/thesis-to-text/) | Interactive wizard that turns raw theses/notes into a finished, audience-ready text |

## Installation URLs

```bash
# Latest
curl -L https://raw.githubusercontent.com/webcane/skills/main/dist/content-writer-linkedin.skill \
  -o content-writer-linkedin.skill

# Pinned version (release tag is <skill>/v<version>)
curl -L https://github.com/webcane/skills/releases/download/content-writer-linkedin/v1.0.0/content-writer-linkedin-1.0.0.skill \
  -o content-writer-linkedin.skill
```