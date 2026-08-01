# Changelog

All notable changes to the `mm-wiki-prune` skill are documented here.

## [1.0.0] - 2026-08-01

### Added
- Initial release: LRU-Demote workflow that evicts cold pages from Logseq hub
  indexes into an `### Archive` section, with a confirm-before-write gate and
  a bundled `scripts/wiki_scan.py` helper for computing the access profile.
