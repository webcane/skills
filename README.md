# Claude Skills Repository

Distribute Claude skills via GitHub with version control and one-line installation.

## How It Works

```
skills/          →   package-skill.sh   →   dist/*.skill   →   GitHub Release   →   curl install
(source, git)                               (generated)
```

## Quick Setup

See **[QUICK_START.md](QUICK_START.md)** for the full release workflow
(4 commands: package → package-claudeai → install-local → release).

Users install a skill with:

```bash
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
| [idea-to-concept](skills/idea-to-concept/) | Structured reasoning: analyze, clarify, or solve a problem via a rigorous method, surfacing assumptions and resolving contradictions |
| [thesis-to-text](skills/thesis-to-text/) | Interactive wizard that turns raw theses/notes into a finished, audience-ready text |
| [python-quiz](skills/python-quiz/) | Интерактивный квиз по Python по .md файлам в директории: выбор, открытые вопросы, задача на код, таймер и оценка в % |
| [python-algo-coach](skills/python-algo-coach/) | Тренер по алгоритмам на Python (LeetCode Easy/Medium): 41 задача, 14 паттернов, прогон решений через тестовый харнесс |
| [mm-wiki-ingest](skills/mm-wiki/mm-wiki-ingest/) | Distill source material into a Logseq wiki with hub-index routing and cross-references |
| [mm-wiki-query](skills/mm-wiki/mm-wiki-query/) | Read-only two-stage (hub-index then targeted-read) search and synthesis over a Logseq wiki |
| [mm-wiki-prune](skills/mm-wiki/mm-wiki-prune/) | LRU-Demote: evict cold pages from live hub indexes into an archive section |
| [mm-wiki-lint](skills/mm-wiki/mm-wiki-lint/) | Structural health check for a Logseq wiki (orphans, broken links, index drift, credential leaks) |
| [mm-wiki-status](skills/mm-wiki/mm-wiki-status/) | Metrics, health, and hot/cold access-profile dashboard for a Logseq wiki |
| [mm-wiki-import](skills/mm-wiki/mm-wiki-import/) | Bulk-import existing markdown notes (incl. Slab exports) into a Logseq wiki |

The mm-wiki skills are grouped under [skills/mm-wiki/](skills/mm-wiki/) — their
[shared assets](skills/mm-wiki/MANIFEST.md) (conventions, scanner) are kept there
and synced into each skill by `scripts/sync-mm-wiki.sh`.

## Installation URLs

```bash
# Latest
curl -L https://raw.githubusercontent.com/webcane/skills/main/dist/content-writer-linkedin.skill \
  -o content-writer-linkedin.skill
curl -L https://raw.githubusercontent.com/webcane/skills/main/dist/idea-to-concept.skill \
  -o idea-to-concept.skill

# Pinned version (release tag is <skill>/v<version>)
curl -L https://github.com/webcane/skills/releases/download/content-writer-linkedin/v1.0.0/content-writer-linkedin-1.0.0.skill \
  -o content-writer-linkedin.skill
```