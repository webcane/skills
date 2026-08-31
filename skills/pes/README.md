# pes — PML over Apple Reminders

A Personal Management Lifecycle (PML) agent: Strategic → Tactical → Operational
→ Results → Review, running entirely on top of **Apple Reminders + Calendar**
via the [`mcp-server-apple-events`](https://github.com/FradSer/mcp-server-apple-events)
MCP server. Reminders is the only source of truth — nothing is cached in the
skill or the conversation.

## Requirements

- macOS, with the `mcp-server-apple-events` MCP server connected (`claude mcp add
  apple-events -- npx -y mcp-server-apple-events`, or the Claude Desktop
  equivalent — see that project's README).
- Reminders access (and, for `routines`, Calendar access) granted to whichever
  host process launches the MCP server, in **System Settings → Privacy &
  Security → Reminders / Calendar**. Without this the server errors with
  `Permission denied: Reminders access was denied.` — the skill will surface
  that verbatim rather than pretending to work.

## Concepts

Three levels, each depending only on the one above it:

```
L1 Strategic  — Values, Areas, Goals, Priorities (P0–P3), Strategy
L2 Tactical   — Initiatives, Plans (Initiative + Expected Outcome + time horizon required)
L3 Operational — Tasks (atomic, with a Done criterion)
```

Plus, outside the three levels: **Inbox** (capture first, decide later),
**Results** (what actually happened — not the same as a completed Task), and
**Review/Retrospective** (the feedback loop back up the levels, always gated by
the user's explicit decision).

Every Task is one of two kinds, always explicit — never a silent default: a
**pes task** (tagged `plan-<slug>`, tied to a Plan) or an **ad-hoc task**
(tagged `adhoc`, deliberately outside the model — a plain reminder). `pes` asks
which one applies whenever it's genuinely ambiguous, rather than creating an
unclassified bare reminder.

See [rules/architecture.md](rules/architecture.md) for the full model,
[rules/data-model.md](rules/data-model.md) for exactly how it's represented in
Reminders (six lists, tag conventions, notes-field keys), and
[rules/mcp-tools.md](rules/mcp-tools.md) for the verified MCP tool schemas and
their gaps (no recurring-event creation, no `flag` field, no nested lists).

## Commands

| Command | What it does |
|---|---|
| `init` | Bootstrap check: creates the six-list skeleton (+ WIP Limit entry) if missing. Idempotent. |
| `capture` | Capture a raw idea/task/link into Inbox. Never auto-creates a Plan. |
| `lint` | Read-only integrity check across all three levels + Outcomes, classified ERROR/WARNING/INFO. |
| `status` | Read-only dashboard: active Plans vs WIP, Tasks by priority, overdue, Outcome Rate, activity-over-outcome flag. |
| `tasks` | list/create/update/complete/reschedule/reprioritize/decompose/move/review Tasks. |
| `plans` | list/create/update/complete/cancel/defer/review Plans — create is gated on Initiative + Expected Outcome + time horizon + WIP. |
| `results` | record/list/review Results, distinct from completed Tasks. |
| `review` | Daily / Weekly / Monthly / Quarterly review — propose changes, apply only what's confirmed. |
| `retrospective` | Post-period retrospective: what produced Results, what stalled, why. |
| `routines` | Manage recurring Calendar blocks (Weekly Review, Planning, …) — first occurrence via MCP, repeat rule set once by hand in Calendar.app. |
| `plan-week` | Weekly planning: Strategic context → Initiatives → Plans → WIP → Inbox → 1–3 Weekly Outcomes → propose → confirm → apply. |
| (execution) | Day-to-day "what should I do now" help, without touching Strategy. |

Full behavior for each command lives in `workflows/<command>.md`.

## The write-flow

Every write except two light-touch paths (Inbox capture; a single unambiguous
Task) follows:

```
READ → ANALYZE → PROPOSE → SHOW DIFF → USER ACCEPTS → WRITE → VERIFY
```

No "done" is reported without a verified re-read. See
[rules/autonomy.md](rules/autonomy.md) for exactly which operations require
confirmation and which don't.

## Layout

```
SKILL.md                 router — dispatches to the twelve workflows
rules/
  architecture.md         L1→L2→L3 dependency model, entities per level
  invariants.md            the 17 hard rules and what enforces each
  priorities.md            Strategic Priority vs Operational Priority vs urgency
  outcomes.md              Task vs Expected Outcome vs Result, activity-over-outcome
  autonomy.md              confirmation boundaries + the full write-flow
  data-model.md            Reminders lists/tags/notes conventions
  mcp-tools.md             verified MCP tool schemas + unsupported-operation gaps
workflows/
  init.md capture.md planning.md execution.md review.md retrospective.md
  lint.md status.md tasks.md plans.md results.md routines.md
```

## Known MCP gaps (see rules/mcp-tools.md for the full table)

- No recurring Calendar event creation — `routines` creates the first occurrence
  and asks the user to set Repeat once, by hand, in Calendar.app.
- No `flag` field on reminders — urgency is expressed via `dueDate` only.
- No nested reminder lists/sections and no cross-reminder parent/child link —
  Plan↔Initiative↔Task relationships are tag/notes conventions, not a native
  EventKit relation.
