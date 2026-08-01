# mm-wiki shared-asset manifest

Managed files are copied from `shared/` (or `overrides/`) into each member
skill by `scripts/sync-mm-wiki.sh`. **Only these files are managed** — anything
else inside a member skill dir (`SKILL.md`, `CHANGELOG.md`, per-skill
references) is hand-maintained and never overwritten by the sync.

## File → consumers

| Canonical source | Destinations (inside each `skills/mm-wiki/mm-wiki-<skill>/`) |
|---|---|
| `shared/wiki-conventions.md` | `mm-wiki-import/references/wiki-conventions.md`, `mm-wiki-query/references/wiki-conventions.md`, `mm-wiki-lint/references/wiki-conventions.md`, `mm-wiki-prune/references/wiki-conventions.md`, `mm-wiki-status/references/wiki-conventions.md` |
| `overrides/mm-wiki-ingest.wiki-conventions.md` | `mm-wiki-ingest/references/wiki-conventions.md` (canonical + ingest-flow section) |
| `shared/wiki_scan.py` | `mm-wiki-lint/scripts/wiki_scan.py`, `mm-wiki-prune/scripts/wiki_scan.py`, `mm-wiki-status/scripts/wiki_scan.py` |

## Why ingest has an override

`mm-wiki-ingest` is the only member that reads `inbox/` and writes `raw/` (the
dropzone cycle). Its `wiki-conventions.md` therefore extends the canonical file
with the "Ingest Flow: inbox → raw → pages" section and the `inbox_dir` /
`raw_dir` config keys. Rather than making the canonical file carry
ingest-specific content for all five other skills, the extended variant lives
in `overrides/` and is copied verbatim to `mm-wiki-ingest`.

## Drift detection

```bash
bash scripts/sync-mm-wiki.sh --check   # exit 1 + lists files that drifted
```

Drift happens when someone hand-edits a managed copy in a member skill. Re-run
`bash scripts/sync-mm-wiki.sh` to restore the canonical content.
