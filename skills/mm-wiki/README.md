# mm-wiki — Logseq wiki skill family

A family of skills that manage a personal/team **Logseq** wiki through the
Hub-Index-Routing pattern. Each skill is a self-contained directory and is
packaged/released independently (see the repo root `CLAUDE.md`); this directory
is the *logical home* of the family and the canonical source for its shared
assets.

## Members

| Skill | Purpose |
|---|---|
| `mm-wiki-ingest` | Distill new source material (paste, URL, file) into pages via the `inbox/ → raw/ → pages` dropzone cycle |
| `mm-wiki-query` | Answer questions by searching the wiki (two-stage routing, read-only) |
| `mm-wiki-prune` | LRU-Demote cold pages from live hub indexes into `### Archive` |
| `mm-wiki-lint` | Structural health check: orphans, stale content, broken links, index drift, credentials |
| `mm-wiki-status` | Metrics + health overview (page counts, hot/cold profile) |
| `mm-wiki-import` | Bulk-import a whole folder of pre-existing markdown (e.g. Slab export) |
| `mm-wiki-reading-list` | Pull books from a macOS Reminders list, generate conspects from the wiki's own prompts, file them through `mm-wiki-ingest` |

The family is agent-agnostic with one deliberate exception: `mm-wiki-reading-list` drives
macOS **Reminders** through the `apple-events` MCP server and uses the host agent's
`Skill` / `Agent` tools, so it runs in Claude Code only — with the sibling
`mm-wiki-ingest` (the only writer) and `mm-wiki-query` (duplicate detection) installed
alongside it. What it can't take from a sibling (the MCP schemas, the tag caveat) is
vendored into its own `references/`, so it carries no runtime dependency on `pes`.

## Layout

```
skills/mm-wiki/
├── README.md                  ← this file (family overview)
├── MANIFEST.md                ← which skill consumes which shared asset
├── shared/                    ← canonical conventions/docs (single source of truth)
│   └── wiki-conventions.md    ← copied to every member's references/
├── scripts/                   ← canonical family scripts
│   └── wiki_scan.py           ← single scanner (lint / prune / status)
└── mm-wiki-<skill>/           ← self-contained skill dirs (packaged as-is)
    ├── references/
    │   ├── wiki-conventions.md         ← synced from shared/ (every member)
    │   ├── wiki-conventions.extra.md   ← INGEST ONLY: hand-maintained ingest rules
    │   ├── mcp-apple-events.md         ← READING-LIST ONLY: vendored MCP subset
    │   └── role-prompts.md             ← READING-LIST ONLY: category criteria
    └── scripts/wiki_scan.py            ← lint / prune / status only, synced from scripts/
```

## Editing shared assets

Do **not** hand-edit the synced copies inside a member skill (`references/` and
`scripts/`) — they are generated from `shared/*` and `scripts/*` by
`scripts/sync-mm-wiki.sh`. Edit the canonical file in `shared/` (or `scripts/`),
then run:

```bash
bash scripts/sync-mm-wiki.sh          # push canonical → all member skills
bash scripts/sync-mm-wiki.sh --check  # verify no drift (exit 1 if any)
```

`sync-mm-wiki.sh` only ever writes files that exist in the canonical pools:
`shared/*` → every member's `references/`, `scripts/*` → the scanner members'
`scripts/` (lint / prune / status). `SKILL.md`, `CHANGELOG.md`, and per-skill
custom references (e.g. `mm-wiki-ingest/references/wiki-conventions.extra.md`)
are never touched by the sync.

## Packaging note

The packaging pipeline (`scripts/package-skill.sh`, `install-local.sh`,
`release-skill.sh`, CI) treats each skill as `skills/<name>` and derives
artifact names with `basename`. So `skills/mm-wiki/mm-wiki-ingest` is addressed
as `mm-wiki/mm-wiki-ingest` on the command line, but installs/artifacts land as
flat `mm-wiki-ingest`. See `scripts/` for details.
