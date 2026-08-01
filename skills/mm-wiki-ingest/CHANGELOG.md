# Changelog

All notable changes to the `mm-wiki-ingest` skill are documented here.

## [Unreleased]

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
