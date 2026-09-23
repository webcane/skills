# Apple Events MCP — the subset this skill uses

This file is intentionally self-contained: the skill must work with nothing but its
own directory, so it carries the MCP facts it depends on instead of pointing at
another skill's rules.

Provenance: fields below were verified against `mcp-server-apple-events` v1.5.0
(npm) by reading its published TypeScript source (`dist/tools/definitions.js`,
`dist/validation/schemas.js`) — the same source the `pes` skill's full
Reminders+Calendar table is built from, which is where to look for anything not
covered here. If a future server version changes these schemas, re-verify with
`tools/list` on the live connection and diff before trusting this file.

## Pre-flight — before the first Reminders call of a run

1. The MCP connection must be live: `reminders_lists` and `reminders_tasks` must be
   callable. If the server isn't connected at all, say so and stop — never
   substitute conversation memory, a cached list, or another source for the
   Reminders list.
2. Make one cheap read first (`reminders_lists` `action: read`). If it fails with
   `Permission denied: Reminders access was denied. Please grant access in System
   Settings > Privacy & Security > Reminders.`, stop and tell the user to grant
   Reminders access to whichever process launches the MCP server (one-time macOS
   grant per host app), then retry. Do not report a book list you could not read.
3. If the server was just added with
   `claude mcp add --scope project apple-events -- npx -y mcp-server-apple-events`,
   the current session won't see it — a new session in that project is needed.

## `reminders_lists`

Read / create / update / delete reminder lists. Lists are flat — no nesting,
sections, or groups are exposed.

| Field | Notes |
|---|---|
| `action` | `read \| create \| update \| delete` |
| `name` | current name (update/delete) or the new list's name (create) |
| `newName` | update only |

## `reminders_tasks`

Fields used by this skill (the server exposes more — see provenance above).

| Field | Notes |
|---|---|
| `action` | `read \| create \| update \| delete` |
| `id` | required for update/delete |
| `title` | the reminder's title — for a book, the only reliable "which book is this" signal alongside `note` |
| `note` | free text. This skill's carrier for author names, quotes, and tags; there is **no** author field in Reminders |
| `completed` | boolean, update only. Reading completed reminders is a `showCompleted` filter, not a state mutation |
| `filterList` | read: restrict to one list name |
| `showCompleted` | read filter, default `false` — set `true` to include reminders the user already ticked off |
| `search` | read filter over title/notes |
| `filterTags` | read filter, `string[]`; **all** given tags must match |
| `tags` | create: sets tags (replaces) |
| `addTags` / `removeTags` | update only; `addTags` is additive and idempotent per tag |

## Tags are a note convention, not real Reminders tags

`tags` / `addTags` / `removeTags` do **not** write Apple Reminders tag chips. The
server hard-codes `--no-shortcuts` on every create/update, so the only path that
would produce a genuine EventKit tag is never taken; instead it prepends `[#tag]`
markers to the `note` field (`tagUtils.js` `formatTags` / `addTagsToNotes`).

Two consequences that matter here:

- **Read-side filtering still works.** `extractTags` parses both `[#tag]` and a
  bare `#tag` out of `note`, so `filterTags` (and reading the `tags` array) is a
  reliable way to find books already filed — even though the user will never see
  tag chips in Reminders.app.
- **`note` is not a clean field.** After tagging, the note begins with `[#tag]`
  noise before the user's own text. Parse author/quotes out of the note with that
  in mind, and don't rewrite or normalize the note — tag writes are the only note
  edits this skill makes.

Tag shape accepted by the server: `^#?[\p{L}\p{N}_-]+$` — no spaces, no colons.
Multi-word topics are hyphenated lowercase (`behavioral-economics`), which is also
what the wiki page's `tags::` line wants, so the same string serves both sides.
