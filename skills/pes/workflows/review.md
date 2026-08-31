# Workflow: review

Daily / Weekly / Monthly / Quarterly review — the feedback mechanism that closes
the PML loop (spec §7). Every review is READ + ANALYZE + PROPOSE; **applying**
any proposed change (closing a Plan, adjusting a Priority, starting a new
Initiative) is a separate, normally-gated write in its own workflow — a review
never writes on its own authority.

## Daily Review (light)

1. Read Tasks due today / overdue, active Plans' `Expected Outcome`s.
2. Report what closed today, what's still open, anything overdue.
3. Propose (don't apply) at most 1–3 key Tasks for tomorrow (Rule of 3, spec
   §16) — offer to hand off to `execution` once accepted.

## Weekly Review

Follow this order (spec §15 lists these ten steps explicitly — keep them, don't
compress):

1. Get actual state from Reminders (fresh read, all six lists).
2. Completed Tasks this week.
3. Active Plans.
4. Their Expected Outcomes.
5. Results recorded this week — compare against step 4's Outcomes.
6. Detect deviations (Plans with activity but no Result; Plans stalled with no
   Task activity; overdue Tasks piling up).
7. Check WIP against the limit.
8. Check Inbox — how much is unprocessed, how old is the oldest item.
9. Propose changes: which Plans to continue/adjust/complete/cancel, whether a new
   Plan is warranted, whether Inbox items should become Tasks/Plans/discarded.
10. **Show every proposed change to the user before applying any of it.** Then
    apply only what's confirmed, each through its own workflow's write-flow
    (`plans.md`, `tasks.md`, `results.md`) — don't batch-apply everything under
    one umbrella confirmation if the changes are heterogeneous (a Plan cancel and
    a Task reschedule are different risk levels; confirm them as what they are).

## Monthly Review

Weekly Review's checks, over a month window, plus: sweep completed/cancelled
Plans for missing Results (invariant 6), recompute Outcome Rate for the month.

## Quarterly Review

Monthly's checks, over a quarter, plus: read `Strategic` Goals and ask whether
each still holds — this is the point where a Strategic Level change proposal is
most appropriate (still requires the user's explicit yes per invariant 14; the
review only surfaces the question, e.g. "Goal X has had zero Initiative activity
this quarter — still a Goal, or time to retire it?").

## Monthly rocks↔goals check

Cross-check active Initiatives/Plans against `Strategic` Goals: any Goal with no
Initiative behind it, any Initiative that's drifted from its stated Goal. Report
only — routes any resulting change through the normal Strategic-edit confirmation.
