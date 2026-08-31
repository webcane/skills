# Workflow: routines

Calendar-side, via `calendar_events`/`calendar_calendars` — Calendar stores
*when*, Reminders stores *what* (invariant 16). Routines (Daily Planning, Weekly
Planning, Weekly/Monthly/Quarterly Review, Execution blocks, …) are **not**
Tasks — never create them in Reminders.

**Read the recurrence gap first:** [rules/mcp-tools.md](../rules/mcp-tools.md)
§"Routines gap" — the MCP cannot set a recurrence rule. Every `create`/`update`
below that involves a repeating cadence follows that gap's workaround. Every
Calendar write requires confirmation (spec §14, §18) — routines are never
light-touch.

## list

`calendar_events` `read` with a `search`/`filterCalendar` scoped to however
routines are distinguished in this user's calendar (agree a convention on first
use — e.g. a dedicated `Routines` calendar, or a consistent title prefix — and
record that choice back to the user, don't silently pick one). `calendar_calendars`
`read` to show what calendars exist if that convention isn't set yet.

## create

1. Propose: name, cadence in words ("every Monday"), time, duration, which
   calendar.
2. Confirm.
3. `calendar_events` `create` — **one single occurrence** for the first date.
4. Verify by re-reading the created event.
5. Tell the user explicitly: open Calendar.app once, find that event, set
   **Repeat** to the agreed cadence — the MCP can't do this step. Don't say
   "routine created" as if the series exists yet; say the first occurrence is
   created and the repeat rule is the one manual step left.

## update

If the user wants to change time/duration/title going forward:
`calendar_events` `update` with `span: "future-events"` (works once a real
recurrence exists in Calendar.app — see create step 5). Changing just one
occurrence: `span: "this-event"`. Propose + confirm as usual.

## delete

Same `span` scoping. Confirm which scope (this occurrence vs. the whole future
series) before calling delete — this is destructive and not easily undone via
the MCP.

## inspect conflicts

Read events in the proposed window (`calendar_events` `read`, `startDate`/
`endDate` around the proposed time) and flag overlaps before creating/updating.
Report conflicts plainly; let the user decide whether to proceed, pick another
time, or accept the overlap.

## propose schedule

Given a set of routines to establish (e.g. onboarding a fresh weekly rhythm),
read the week's existing events first, then propose non-conflicting slots for
each routine. Show the full proposed weekly schedule before creating anything —
this is a batch of Calendar writes, so confirm the whole batch once, then create
each occurrence and verify each, same as `create` above.
