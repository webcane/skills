# Changelog

All notable changes to the `mm-wiki-import` skill are documented here.

## [Unreleased]

### Changed
- Adopts the family-wide Content Depth (Distillation Depth) standard from the
  shared conventions: bulk-imported pages keep code examples, comparison tables,
  one "why" per block, gotchas blocks, and a depth-pointer to the source instead
  of being compressed to fact-headings.

## [1.0.0] - 2026-08-01

### Added
- Initial release: bulk import workflow for converting existing markdown
  folders (with explicit Slab "Export to Markdown" handling — link
  resolution, asset migration, missing-frontmatter title recovery) into a
  Logseq wiki's Hub-Index-Routing format.
