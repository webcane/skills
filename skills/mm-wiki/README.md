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

## Layout

```
skills/mm-wiki/
├── README.md                  ← this file (family overview)
├── MANIFEST.md                ← which skill consumes which shared asset
├── shared/                    ← canonical shared assets (single source of truth)
│   ├── wiki-conventions.md    ← canonical conventions (5 skills)
│   └── wiki_scan.py           ← shared scanner (lint / prune / status)
├── overrides/                 ← per-skill variants of shared files
│   └── mm-wiki-ingest.wiki-conventions.md   ← ingest's extended conventions
└── mm-wiki-<skill>/           ← self-contained skill dirs (packaged as-is)
```

## Editing shared assets

Do **not** hand-edit the copies inside `skills/mm-wiki/mm-wiki-<skill>/` — they
are generated from `shared/` (and `overrides/`) by `scripts/sync-mm-wiki.sh`.
Edit the canonical file here, then run:

```bash
bash scripts/sync-mm-wiki.sh          # push canonical → all member skills
bash scripts/sync-mm-wiki.sh --check  # verify no drift (exit 1 if any)
```

`sync-mm-wiki.sh` only ever writes the *managed* files listed in `MANIFEST.md`
(`references/wiki-conventions.md`, `scripts/wiki_scan.py`). `SKILL.md` and
`CHANGELOG.md` are never touched by the sync.

## Packaging note

The packaging pipeline (`scripts/package-skill.sh`, `install-local.sh`,
`release-skill.sh`, CI) treats each skill as `skills/<name>` and derives
artifact names with `basename`. So `skills/mm-wiki/mm-wiki-ingest` is addressed
as `mm-wiki/mm-wiki-ingest` on the command line, but installs/artifacts land as
flat `mm-wiki-ingest`. See `scripts/` for details.
