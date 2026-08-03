# Changelog

All notable changes to the `mm-wiki-lint` skill are documented here.

## [1.0.0] - 2026-08-03

### Changed
- Adopts the family-wide Content Depth (Distillation Depth) standard from the
  shared conventions (the "golden middle" for page content). Reference-only
  change; lint behaviour is unchanged.
- `wiki_scan.py` is synced from the family `mm-wiki/scripts/` pool into this
  skill's `scripts/` (not copied to every member); invocation stays
  `scripts/wiki_scan.py`.

## [1.0.0] - 2026-08-01

### Added
- Initial release: structural health check (orphans, stale pages, broken
  refs, index drift, credential leaks, empty pages) for a Logseq wiki, with
  an optional `--fix` mode for mechanical repairs and a bundled
  `scripts/wiki_scan.py` helper.
