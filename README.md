# Agent Skills Repository

Distribute Agent Skills and custom agents for Claude Code and Codex from shared sources.

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

## cane-wiki for Claude Code and Codex

The [cane-wiki agent](agents/cane-wiki/cane-wiki.md) owns the query, ingest,
update, lint, and prune workflow. `scripts/build-codex-agent.py` renders a
Codex custom agent from that source. `cane-wiki-init` prepares a vault when the
agent finds no `llm-wiki.yml` or the user requests reconfiguration. It also
installs missing Obsidian skill dependencies without changing the vault. Its neutral `{{ASK_USER}}` and
`{{MULTI_SELECT}}` markers are resolved in platform packages.

Install for Claude Code from this checkout:

```bash
bash scripts/install-cane-wiki-claude.sh
```

Install for Codex from this checkout:

```bash
bash scripts/install-cane-wiki-codex.sh
```

The Codex installer places the custom agent in `~/.codex/agents` and
`cane-wiki-init` plus its three required external skills in `${CODEX_HOME:-~/.codex}/skills`.
It fetches external skills from
[kepano/obsidian-skills](https://github.com/kepano/obsidian-skills); set
`OBSIDIAN_SKILLS_SOURCE` to an existing local `skills/` directory for offline
installation. `INSTALL_DIR` overrides the skills destination for either
installer; `AGENT_INSTALL_DIR` overrides the agent destination. The Claude
installer uses `~/.claude/skills` and `~/.claude/agents` by default.
On first use, the agent checks for the three external skills and tries to install any
missing ones. If network or filesystem access prevents that, it gives the user
the matching `npx skills add` command to run manually.

For platform packages, use `scripts/package-skill-claude-code.sh`,
`scripts/package-skill-codex.sh`, or `scripts/package-skill-claudeai.sh` with
`cane-wiki-init`. The existing `package-skill.sh` keeps the
neutral Agent Skills source. Its release attaches Claude Code and Codex
variants. To publish both agent formats, update
`agents/cane-wiki/VERSION` and its changelog, commit, then run
`bash scripts/release-agent.sh cane-wiki`. A released Codex agent can be
installed with `bash scripts/install-agent-codex.sh cane-wiki 0.1.0`.

The three external skills used by the agent are `obsidian-markdown`, `obsidian-cli`, and
`defuddle`. `obsidian-bases`, `json-canvas`, and `knap` are optional for related
Obsidian tasks. The external skills are not copied into this repository. The
workflow uses Obsidian CLI when available and falls back to file search.

## Repository Structure

```
├── skills/content-writer-linkedin/   # Source (git tracked)
│   ├── SKILL.md                      # frontmatter holds metadata.version
│   ├── CHANGELOG.md                  # per-skill changelog
│   └── README.md
├── skills/cane-wiki-init/            # Obsidian vault initialization skill
├── agents/cane-wiki/                 # Claude source and generated Codex agent
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
| [cane-wiki-init](skills/cane-wiki-init/) | Prepare an Obsidian vault for the cane-wiki agent |
| [content-writer-linkedin](skills/content-writer-linkedin/) | Write authentic LinkedIn articles |
| [hr-answer-coach](skills/hr-answer-coach/) | Interactive wizard that flags HR-interview red flags and rewrites the answer |
| [idea-to-concept](skills/idea-to-concept/) | Structured reasoning: analyze, clarify, or solve a problem via a rigorous method, surfacing assumptions and resolving contradictions |
| [thesis-to-text](skills/thesis-to-text/) | Interactive wizard that turns raw theses/notes into a finished, audience-ready text |
| [python-quiz](skills/python-quiz/) | Интерактивный квиз по Python по .md файлам в директории: выбор, открытые вопросы, задача на код, таймер и оценка в % |
| [python-algo-coach](skills/python-algo-coach/) | Тренер по алгоритмам на Python (LeetCode Easy/Medium): 41 задача, 14 паттернов, прогон решений через тестовый харнесс |
| [mm-gtd](skills/mm-gtd/) | Router for a Covey/GTD planning system in a Logseq graph: ingest (capture → inbox/), planning (weekly ritual + day-end), query (what-today, summaries) |
| [pes](skills/pes/) | Personal Management Lifecycle (Strategic/Tactical/Operational) agent over Apple Reminders + Calendar via MCP — WIP limits, Expected-Outcome gates, Results-vs-Activity tracking |
| [mm-wiki-ingest](skills/mm-wiki/mm-wiki-ingest/) | Distill source material into a Logseq wiki with hub-index routing and cross-references |
| [mm-wiki-query](skills/mm-wiki/mm-wiki-query/) | Read-only two-stage (hub-index then targeted-read) search and synthesis over a Logseq wiki |
| [mm-wiki-prune](skills/mm-wiki/mm-wiki-prune/) | LRU-Demote: evict cold pages from live hub indexes into an archive section |
| [mm-wiki-lint](skills/mm-wiki/mm-wiki-lint/) | Structural health check for a Logseq wiki (orphans, broken links, index drift, credential leaks) |
| [mm-wiki-status](skills/mm-wiki/mm-wiki-status/) | Metrics, health, and hot/cold access-profile dashboard for a Logseq wiki |
| [mm-wiki-import](skills/mm-wiki/mm-wiki-import/) | Bulk-import existing markdown notes (incl. Slab exports) into a Logseq wiki |
| [mm-wiki-reading-list](skills/mm-wiki/mm-wiki-reading-list/) | Pull books from a macOS Reminders list via MCP, generate conspects from the wiki's own prompts, file them through mm-wiki-ingest |

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
