# Changelog

All notable changes to the `mm-wiki-prune` skill are documented here.

## [1.0.0] - 2026-08-03

### Changed
- Adopts the family-wide Content Depth (Distillation Depth) standard from the
  shared conventions (the "golden middle" for page content). Reference-only
  change; prune behaviour is unchanged.
- `wiki_scan.py` is synced from the family `mm-wiki/scripts/` pool into this
  skill's `scripts/` (not copied to every member); invocation stays
  `scripts/wiki_scan.py`.

## [1.0.0] - 2026-08-01

### Added
- Initial release: LRU-Demote workflow that evicts cold pages from Logseq hub
  indexes into an `### Archive` section, with a confirm-before-write gate and
  a bundled `scripts/wiki_scan.py` helper for computing the access profile.
