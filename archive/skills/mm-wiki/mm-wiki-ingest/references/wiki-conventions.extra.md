# mm-wiki-ingest — Conventions Additions (ingest-specific)

Hand-maintained supplement to `wiki-conventions.md` for `mm-wiki-ingest` only.

`references/wiki-conventions.md` is a **synced** copy of
`shared/wiki-conventions.md` — the sync (`scripts/sync-mm-wiki.sh`) overwrites
it, so do not edit it here. Anything ingest-specific that the rest of the family
does not need lives in THIS file, which is hand-maintained and never touched by
the sync. Read this file **in addition to** `wiki-conventions.md`.

## Configuration: extra keys for `llm-wiki.yml`

`mm-wiki-ingest` adds two keys to the shared config block:

```yaml
inbox_dir: inbox              # optional: dropzone ingest reads (default: inbox, relative to wiki_path)
raw_dir: raw                  # optional: append-only archive of originals (default: raw)
```

## Ingest Flow: inbox → raw → pages

The wiki runs a **dropzone-driven ingest cycle**. `mm-wiki-ingest` reads *only*
`inbox/`; `raw/` is an append-only archive it never re-reads. This keeps the read
path tiny (just what's new) and preserves every original source byte-for-byte.

```
wiki-root/
├── inbox/     ← dropzone. New sources land here (pasted text, fetched URLs, copied files)
├── raw/       ← append-only archive of originals. ingest never reads this.
├── pages/     ← result (Wiki___*.md)
└── llm-wiki.yml
```

Cycle, per ingest run:

1. Read **all** files in `inbox/` (a small set — nothing is "re-read").
2. Distill each into pages under `pages/`, keeping hubs and cross-refs intact.
3. Fully-processed source → move **byte-for-byte** to `raw/`. The move is the
   **commit point**: only genuinely processed sources leave `inbox/`.
4. Failed / unclear source → stays in `inbox/`, re-read on the next run.

Rules:

- **`raw/` is append-only and never read** by any ingest step. It exists to preserve
  the original, not to be re-processed.
- **`.gitignore`**: both `inbox/` and `raw/` should be git-ignored. Raw material can
  contain secrets before ingest filtering, and the wiki is usually git-tracked —
  keep secrets out of history.
- **Name collisions in `raw/`**: if a target filename already exists there, prefix
  with today's date (`2026-08-01_notes.md`). Never overwrite an existing original.
- **Provenance**: pages created from a source record `source:: raw/<filename>` (the
  archive name actually used), so each page's origin is auditable and
  `mm-wiki-prune` can trace it.
- **Duplicates on re-upload**: dropping an already-processed file back into `inbox/`
  is safe — the "never duplicate a fact already recorded" rule (see Constraints)
  prevents block duplication.
- `inbox/` and `raw/` live outside `pages_dir`; lint/status/prune scan only
  `pages_dir` and never touch them.

## Constraint: Language of content

- **Language of content**: page content, hub-index descriptions, and tags are
  written in the **same language as the source material** — do not translate. Only
  the structural keys stay in English: property names (`type::`, `created::`, …),
  page filenames, and `[[links]]`, which the Logseq format requires.
