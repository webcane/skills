# Changelog

All notable changes to the `mm-wiki-query` skill are documented here.

## [Unreleased]

### Changed
- Adopts the family-wide Content Depth (Distillation Depth) standard from the
  shared conventions, so pages it routes to and reads carry richer
  demonstrations and rationale (the "golden middle"). Reference-only change;
  query behaviour is unchanged.

## [1.0.0] - 2026-08-01

### Added
- Initial release: read-only two-stage (hub-index then targeted-read) query
  workflow against a Logseq wiki, with Access-Log write-back for LRU tracking.
