# Changelog

All notable changes to the `mm-wiki-ingest` skill are documented here.

## [Unreleased]

### Changed
- Distillation Depth (golden middle): ingest now keeps one short code example
  per key idea, preserves comparison tables, retains one "why" per block, files
  gotchas as their own block, and ends pages with a depth-pointer to the raw
  source — see the new Content Depth section in `references/wiki-conventions.md`.
- Enrichment carve-out: a page materially thinner than its source may be
  rewritten to meet the depth bar (guarded by not touching user-authored blocks,
  an `enriched::` marker, and append-and-flag when unsure) — previously the
  never-overwrite rule made over-compressed pages unfixable.
- Language: section headings are structural keys and may follow the wiki's
  canonical heading language (e.g. EN headings over a RU body); body stays in
  the source language.
- Conventions layout: ingest now reads the synced family-wide
  `references/wiki-conventions.md` plus a hand-maintained
  `references/wiki-conventions.extra.md` (ingest flow, `inbox_dir`/`raw_dir`,
  language policy). The `overrides/` mechanism was removed; shared assets are
  synced generically from `shared/*`.
- Version bumped to 1.3.0.

### Added
- Language policy: page content, hub-index descriptions, and tags follow the
  source material's language (do not translate); only structural keys (property
  names, page filenames, `[[links]]`) stay in English.
- Inbox/raw dropzone flow: sources land in the wiki's `inbox/`, ingest reads only
  `inbox/`, and fully-processed files are archived byte-for-byte to `raw/`
  (append-only, never re-read); failed/unclear files stay in `inbox/` for the next
  run.
- `inbox_dir`/`raw_dir` config keys (default `inbox`/`raw`, relative to
  `wiki_path`); directories auto-created and `.gitignore` coverage offered when
  missing.
- `raw/` name-collision handling (prefix today's date, e.g. `2026-08-01_notes.md`).
- `source:: raw/<file>` provenance added to new pages.
- Step to maintain a wiki-internal `Wiki/Reference/Ingest-Workflow` page.

## [1.0.0] - 2026-08-01

### Added
- Initial release: ingest workflow for filing source material into a Logseq
  wiki with Hub-Index-Routing, split out of the original monolithic `/wiki`
  command spec into an independent, agent-agnostic skill.
