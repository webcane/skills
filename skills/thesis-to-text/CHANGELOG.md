# Changelog — thesis-to-text

All notable changes to this skill. Released per skill as tag
`thesis-to-text/v<version>`. The version in `SKILL.md` frontmatter
(`metadata.version`) is the source of truth.

## [Unreleased]

### Fixed
- Removed non-standard `color` frontmatter field — fails `skills-ref validate` (only `allowed-tools`, `compatibility`, `description`, `license`, `metadata`, `name` are permitted)

## [1.0.0] - 2026-06-21

### Added
- Initial release
- 8-block interview (role/style, context, audience, raw theses, goal, format, constraints, extra requests)
- Internal analysis stage (core problem, gaps, success criteria, decomposition)
- Validation stage that surfaces contradictions across interview blocks before drafting
- Plan summary with explicit approval gate before writing
- Outline → Write → Review loop for the final draft
