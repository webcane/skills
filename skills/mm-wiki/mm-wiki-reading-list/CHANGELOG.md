# Changelog

All notable changes to the `mm-wiki-reading-list` skill are documented here.

## [Unreleased]

### Added
- Initial release in this repository: Reminders → book conspects pipeline for a Logseq
  wiki. Pulls books from a macOS Reminders list via the `apple-events` MCP server,
  classifies each by genre against `Wiki/Prompts/*` pages discovered by their tag triple,
  generates a multi-page conspect, files it through `mm-wiki-ingest`, and tags the
  Reminder afterwards. Three modes: `list` (read-only report), `single [title]` (one book,
  inline), `full` (every untagged candidate, one sequential subagent per book).
- `references/mcp-apple-events.md` — the Apple Events MCP subset this skill depends on
  (pre-flight and permission errors, `reminders_lists` / `reminders_tasks` fields, the
  `[#tag]`-in-`note` tag caveat), vendored so the skill is self-contained and carries no
  runtime dependency on the `pes` skill's rule files.
- `references/role-prompts.md` — human-readable criteria table for the book-brief
  categories (the mechanism itself stays the tag grep in the wiki).
- Family integration: joins the `mm-wiki-*` family under `skills/mm-wiki/`, reads the
  synced `references/wiki-conventions.md`, honours the `inbox_dir` config key instead of
  hardcoding `inbox/`, and declares its MCP + sibling-skill requirements in frontmatter
  (`compatibility`).
