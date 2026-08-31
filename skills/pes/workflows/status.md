# Workflow: status

Read-only dashboard. Every number must come from a fresh MCP read this turn —
never reuse a count from earlier in the conversation (invariant 15).

## Pull

- `Plans`: all, `showCompleted: true` (need both active and recently-closed for
  the Outcome Rate).
- `Tasks`: `showCompleted: true`, plus filtered views: `dueWithin: overdue`,
  `dueWithin: today`.
- `Results`: recent window (e.g. last 30 days by `Recorded:` note or completion
  date).
- `Strategic` `WIP Limit` entry (default 3 if absent).
- `calendar_events` `read` for the current routines window (today/this week) —
  see [routines.md](routines.md) for what counts as a routine event.

## Report, in this order

1. **Active Plans** — count vs WIP limit; flag `WIP limit exceeded` if over.
2. **Tasks in progress** — not completed, has a `dueDate` or is tagged to an
   active Plan.
3. **Overdue Tasks** — from `dueWithin: overdue`.
4. **Tasks due today** — from `dueWithin: today`.
5. **Tasks by Operational Priority** — High / Medium / Low counts.
6. **Tasks by Strategic Priority** — via each Task's `plan-<slug>` →
   Plan's `init-<slug>` → Initiative's `p0..p3` tag; report as best-effort (some
   Tasks won't trace to a tier — put those in "untagged").
7. **Completed Tasks** in the period asked (default: this week).
8. **Results** recorded in the period.
9. **Plans without Expected Outcome / without Initiative** — should normally be
   zero (see `lint`); list any that exist.
10. **Activity-over-outcome indicator** — per [rules/outcomes.md](../rules/outcomes.md).
11. **Current routines** — today's/this week's recurring blocks from Calendar.

Keep it to numbers and short lists — this is decision support, not a KPI
dashboard (spec §20). Don't editorialize beyond the activity-over-outcome flag;
that one's explicitly meant to prompt a decision.
