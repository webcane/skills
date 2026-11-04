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
update, lint, and prune workflow. The [cane-wiki-critic agent](agents/cane-wiki-critic/cane-wiki-critic.md)
reviews explanatory quality, writes daily reports, and delegates edits and factual checks to cane-wiki.
`scripts/build-codex-agent.py` renders Codex custom agents from both Markdown sources. `cane-wiki-init` prepares a vault when the
agent finds no `llm-wiki.yml` or the user requests reconfiguration. It also
installs missing Obsidian skill dependencies without changing the vault. Its neutral `{{ASK_USER}}` and
`{{MULTI_SELECT}}` markers are resolved in platform packages.

Install the Claude Code plugin from this repository's marketplace. It bundles
both agents and `cane-wiki-init`:

```bash
claude plugin marketplace add webcane/skills
claude plugin install cane-wiki@webcane-skills
```

Install the Codex plugin, then install the custom agents from a checkout.
Codex plugins provide skills but do not register custom agent TOML files:

```bash
codex plugin marketplace add webcane/skills
codex plugin add cane-wiki@webcane-skills
git clone https://github.com/webcane/skills.git
bash skills/scripts/install-cane-wiki-agents-codex.sh
```

Start a new session after installation. The plugin's `cane-wiki-init` skill
sets up the vault; the agents handle wiki work. The three external Obsidian
skills are installed when first needed. If automatic installation cannot run,
use `npx` for the relevant host:

```bash
npx skills add https://github.com/kepano/obsidian-skills --skill obsidian-markdown --skill obsidian-cli --skill defuddle -g -a claude-code -y
npx skills add https://github.com/kepano/obsidian-skills --skill obsidian-markdown --skill obsidian-cli --skill defuddle -g -a codex -y
```

`npx skills add` installs skills, not the `cane-wiki` agents. The existing
all-in-one installers remain available from a checkout:

```bash
bash scripts/install-cane-wiki-claude.sh
bash scripts/install-cane-wiki-codex.sh
```

The Codex installer places both custom agents in `~/.codex/agents` and
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

The plugin directories under `plugins/` are built from the canonical agent and
skill sources. After changing either source, run
`python3 scripts/build-cane-wiki-plugins.py` and commit the updated bundles;
`python3 scripts/build-cane-wiki-plugins.py --check` detects stale copies.

For platform packages, use `scripts/package-skill-claude-code.sh`,
`scripts/package-skill-codex.sh`, or `scripts/package-skill-claudeai.sh` with
`cane-wiki-init`. The existing `package-skill.sh` keeps the
neutral Agent Skills source. Its release attaches Claude Code and Codex
variants. To publish an agent in both formats, update its `VERSION` and changelog,
commit, then run `bash scripts/release-agent.sh <agent-name>`. A released Codex agent
can be installed with `bash scripts/install-agent-codex.sh <agent-name> <version>`.

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
├── agents/cane-wiki-critic/          # Editorial critic for both platforms
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
| [pes](skills/pes/) | Personal Management Lifecycle (Strategic/Tactical/Operational) agent over Apple Reminders + Calendar via MCP — WIP limits, Expected-Outcome gates, Results-vs-Activity tracking |

The former `mm-gtd` and `mm-wiki-*` skills are preserved in
[archive/skills/](archive/skills/) and are not part of the active skill catalog.

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
