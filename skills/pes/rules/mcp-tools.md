# MCP tools — verified reference

Source of truth: `mcp-server-apple-events` (npm), verified 2026-08-30 by reading its
published TypeScript source (`dist/tools/definitions.js`, `dist/validation/schemas.js`,
v1.5.0) — not the README, not guessed. If a future server version changes these
schemas, **re-verify before trusting this file**: call `tools/list` on the live MCP
connection and diff against the tables below before using any tool this file
doesn't cover.

## Pre-flight check

Before any command that touches Reminders/Calendar, confirm the server is usable:

1. The MCP connection must be live (tools named `reminders_tasks`, `reminders_lists`,
   `reminders_subtasks`, `calendar_events`, `calendar_calendars` must be callable).
2. Make one cheap read call (`reminders_lists` action `read`). If it errors with
   `Permission denied: Reminders access was denied. Please grant access in System
   Settings > Privacy & Security > Reminders.` (this exact message has been observed
   from the underlying CLI), **stop** — do not fabricate state, do not claim a write
   succeeded. Tell the user: grant Reminders access (and separately, Calendar access)
   to the host app in **System Settings → Privacy & Security → Reminders / Calendar**,
   then retry. This is a one-time macOS grant per host app (e.g. Terminal, or
   whichever process launches the MCP server).
3. If the MCP server isn't connected at all, tell the user and stop — do not
   substitute Notes, a local file, or conversation memory as a stand-in source of
   truth (invariant 15 in [invariants.md](invariants.md)).

## Tools (exact names — do not invent others)

### `reminders_tasks`
Read / create / update / delete reminders.
**Read-only via this tool** (configure in Reminders.app instead): alarms, recurrence
rules, location-based triggers.

| Field | Type | Notes |
|---|---|---|
| `action` | `read\|create\|update\|delete` | required |
| `id` | string | required for update/delete |
| `title` | string | required for create |
| `dueDate` | string | `'YYYY-MM-DD HH:mm:ss'` recommended; also `YYYY-MM-DD`, ISO 8601 |
| `note` | string | free text |
| `url` | string (uri) | any scheme except `file:`/`javascript:`/`data:`/etc.; http(s) hosts are SSRF-checked |
| `completed` | boolean | update only |
| `priority` | int enum `0,1,5,9` | 0=none, 1=high, 5=medium, 9=low |
| `targetList` | string | list name, create/update |
| `filterList` | string | read filter |
| `showCompleted` | boolean | read filter, default false |
| `search` | string | read filter, title/notes |
| `dueWithin` | `today\|tomorrow\|this-week\|overdue\|no-date` | read filter |
| `startDate` / `endDate` | string | read: due-date window (day granularity); update: `startDate` sets the reminder's start date |
| `filterPriority` | `high\|medium\|low\|none` | read filter |
| `filterRecurring` | boolean | read filter |
| `filterLocationBased` | boolean | read filter |
| `filterTags` | string[] | read filter, ALL must match |
| `tags` | string[] | create: sets tags (replace) |
| `addTags` / `removeTags` | string[] | update only |
| `subtasks` | string[] | create only — initial checklist titles |

No `flag` field is exposed by this tool. Urgency is expressed via `dueDate` only.

### `reminders_lists`
Read / create / update / delete reminder **lists** (flat — no nesting/sections/groups
exposed).

| Field | Notes |
|---|---|
| `action` | `read\|create\|update\|delete` |
| `name` | current name (update/delete) or new list's name (create) |
| `newName` | update only |

### `reminders_subtasks`
Checklist items **inside one reminder's notes field** (`---SUBTASKS---` /
`---END SUBTASKS---` markers, rendered natively by Reminders.app). This is **not**
a cross-reminder parent/child relationship — it cannot link a Task reminder to a
Plan reminder. Use it only for literal in-task checklists.

| Field | Notes |
|---|---|
| `action` | `read\|create\|update\|delete\|toggle\|reorder` |
| `reminderId` | required for all actions |
| `subtaskId` | required for update/delete/toggle |
| `title` | required for create |
| `completed` | update |
| `order` | string[] of subtask IDs, required for reorder |

### `calendar_events`
Read / create / update / delete calendar events (time blocks).
**Read-only via this tool** (configure in Calendar.app instead): URL, structured
location object, explicit all-day toggle (inferred from date format instead),
availability (settable only in Calendar.app — the tool's `availability` field is a
**read filter**, not a create/update field), alarms, **recurrence rules**.

| Field | Notes |
|---|---|
| `action` | `read\|create\|update\|delete` |
| `id` | required update/delete |
| `title` | required create |
| `startDate` / `endDate` | required create; `'YYYY-MM-DD HH:mm:ss'` for timed, bare `'YYYY-MM-DD'` for all-day |
| `note`, `location` | free text |
| `timezone` | IANA id, timed events only |
| `availability` | read filter only: `not-supported\|busy\|free\|tentative\|unavailable` |
| `span` | `this-event\|future-events` — scope for update/delete on a recurring series |
| `targetCalendar` | create only; events cannot be moved between calendars via update (delete + recreate) |
| `filterCalendar`, `search` | read filters |

**Critical gap:** there is no field to set an RRULE. **The MCP cannot create a
recurring event.** See [Routines gap](#routines-gap-no-recurrence-write) below.

### `calendar_calendars`
Read-only. Lists calendars; with `startDate`+`endDate` returns only calendars that
have events in that window (annotated with in-range event count).

## Unsupported operations — do not simulate these

| Requested capability | Status | Workaround |
|---|---|---|
| Set a `flag` on a reminder | Not exposed | Use `priority` + `dueDate` instead |
| Nested reminder lists / sections / folders | Not exposed | Flat lists + tags only ([data-model.md](data-model.md)) |
| Cross-reminder parent/child (e.g. Task → Plan as a "real" link) | Not exposed | Convention: linking tags in notes/tags ([data-model.md](data-model.md)) |
| Create/update a **recurring** calendar event (set RRULE) | Not exposed (read-only) | See below |
| Set event availability (busy/free/etc.) on create/update | Not exposed (read filter only) | Tell user to set it in Calendar.app |
| Set alarms on reminders or events | Not exposed (read-only) | Tell user to set it in the native app |

### Routines gap: no recurrence write

`calendar_events` `create`/`update` cannot set a recurrence rule — recurrence is
read-only via this MCP. The `routines` workflow's write path is therefore:

1. Propose the routine (name, cadence in words, time, duration) and get confirmation.
2. Create **one single (non-recurring) occurrence** via `calendar_events` `create`.
3. Tell the user explicitly: open Calendar.app once, find that event, and set
   **Repeat** to the cadence they chose — the MCP cannot do this step.
4. After that manual step, the skill *can* still manage the series going forward:
   `calendar_events` `read`/`update`/`delete` all accept `span: this-event|future-events`,
   so once a recurrence exists (created by the human in step 3), later routine edits
   and conflict checks work normally through the MCP.

Never tell the user a recurring routine was "created" if only step 2 ran — say
plainly that the first occurrence was created and the repeat rule still needs to be
set by hand, once.
