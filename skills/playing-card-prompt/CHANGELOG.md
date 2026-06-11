# Changelog — playing-card-prompt

All notable changes to this skill. Released per skill as tag
`playing-card-prompt/v<version>`. The version in `SKILL.md` frontmatter
(`metadata.version`) is the source of truth.

## [Unreleased]

### Added
- `scripts/manage_config.py` — dependency-free CLI to read/write/validate `config.json` (`show`, `get`, `set`, `unset`, `validate`, `reset`, `options`, `path`); validates `deck`/`style` against the files in `assets/` and enforces the index/lettering/aspect enums

### Changed
- Trimmed the config section of SKILL.md — removed lookup-order/schema/field tables already covered in `references/CONFIG.md`, leaving only short pointers and the per-mode CLI commands
- Restructured the COURT/PIP/ACE templates and assembly steps in `references/REFERENCE.md` and `SKILL.md` to follow general-purpose image-prompt best practices: format constraints (aspect ratio, full card visible, transparent background) and the style block now come first; the old `CHARACTER-SPECIFIC FEATURES` / `STANDARD <RANK> RANK ATTRIBUTES` / `ADDITIONAL / REPLACED ATTRIBUTES` / `TRANSFERRED FROM REFERENCE IMAGE` / `EXCLUSIONS` section labels are gone — traditional, additional, and reference-transfer attributes are now resolved into a single deduplicated, contradiction-free `[RESOLVED_ATTRIBUTES]` list, and all "no …" exclusions are merged into one trailing `[NEGATIVE_LIST]` (which engines with a negative-prompt field can take verbatim)
- Updated `references/example-court-king.md` to the new merged structure and added presenting-the-result tips (negative-prompt field, Midjourney `--ar`, optional shortened ~50–80 token version)
