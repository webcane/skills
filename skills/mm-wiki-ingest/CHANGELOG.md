# Changelog

All notable changes to the `mm-wiki-ingest` skill are documented here.

## [Unreleased]

### Added
- Language policy: page content, hub-index descriptions, and tags follow the
  source material's language (do not translate); only structural keys (property
  names, page filenames, `[[links]]`) stay in English.

## [1.0.0] - 2026-08-01

### Added
- Initial release: ingest workflow for filing source material into a Logseq
  wiki with Hub-Index-Routing, split out of the original monolithic `/wiki`
  command spec into an independent, agent-agnostic skill.
