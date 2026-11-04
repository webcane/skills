# mm-wiki shared-asset manifest

Managed files are copied from two canonical pools by `scripts/sync-mm-wiki.sh`:

1. `shared/*` — conventions/docs: copied into **every member's `references/`**
   (only `wiki-conventions.md` today).
2. `scripts/*` (family-level) — executable helpers: copied only into the
   scanner members' `scripts/` (lint, prune, status) — a single scanner, not
   duplicated to everyone.

**Only files that exist in these pools are managed** — anything else inside a
member skill dir (`SKILL.md`, `CHANGELOG.md`, and per-skill custom references)
is hand-maintained and never overwritten by the sync.

## File → consumers

| Canonical source | Destinations (inside each `skills/mm-wiki/mm-wiki-<skill>/`) |
|---|---|
| `shared/wiki-conventions.md` | `references/wiki-conventions.md` — in ALL seven members (ingest, import, query, lint, prune, status, reading-list) |
| `scripts/wiki_scan.py` | `scripts/wiki_scan.py` — in the scanner members only (mm-wiki-lint, mm-wiki-prune, mm-wiki-status) |

## Per-skill custom files (hand-maintained, not synced)

`mm-wiki-ingest` is the only member that reads `inbox/` and writes `raw/` (the
dropzone cycle). Its ingest-specific rules live in a hand-maintained sibling
file that the sync never touches:

- `mm-wiki-ingest/references/wiki-conventions.extra.md` — the "Ingest Flow:
  inbox → raw → pages" section, the `inbox_dir` / `raw_dir` config keys, and the
  language policy. Read alongside the synced `wiki-conventions.md`.

`mm-wiki-reading-list` carries two hand-maintained references of its own — the sync
never touches them and no other member reads them:

- `mm-wiki-reading-list/references/mcp-apple-events.md` — the Apple Events MCP
  subset this skill depends on (pre-flight and permission errors,
  `reminders_lists` / `reminders_tasks` fields, the `[#tag]`-in-`note` tag caveat),
  vendored so the skill is self-contained and needs no `pes` rule files at runtime.
- `mm-wiki-reading-list/references/role-prompts.md` — human-readable criteria for
  the `Wiki/Prompts/*-Book-Brief` categories; the mechanism stays the tag grep in
  the wiki.

## Drift detection

```bash
bash scripts/sync-mm-wiki.sh --check   # exit 1 + lists files that drifted
```

Drift happens when someone hand-edits a managed copy in a member skill. Re-run
`bash scripts/sync-mm-wiki.sh` to restore the canonical content.
