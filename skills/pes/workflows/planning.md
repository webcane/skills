# Workflow: plan-week (weekly planning)

Planning mode ([rules/autonomy.md](../rules/autonomy.md)). Follow the ten steps
from spec §15 in order — this is the one workflow that touches every level, so
skipping a step is how L3 ends up silently driving L1.

1. **Strategic context** — read `Strategic` (Goals, current Priorities, WIP
   Limit entry).
2. **Active Initiatives** — read `Initiatives`.
3. **Active Plans** — read `Plans` filtered `status-active`.
4. **WIP check** — active Plans count vs. limit; if already at/over, that
   constrains everything downstream (don't plan toward a 4th active Plan without
   resolving WIP first — point back to [plans.md](plans.md)'s WIP handling).
5. **Inbox** — read `Inbox`; note age/volume of unprocessed items.
6. **Unfinished Tasks** — read `Tasks`, overdue + due-this-week, grouped by Plan.
7. **1–3 key Weekly Outcomes** — propose, don't impose (Rule of 3,
   [rules/outcomes.md](../rules/outcomes.md)). Draw candidates from active
   Plans' Expected Outcomes and any Inbox items worth promoting.
8. **Propose Plans/Tasks** — for each Weekly Outcome, propose the specific Tasks
   (and, only if genuinely warranted, a new Plan — subject to the same WIP/
   Initiative/Expected-Outcome gate as any Plan creation). Don't auto-promote
   every Inbox item; be selective and say why each one made the cut.
9. **Show diff** — the full proposed week: new/updated Tasks, any new Plan, any
   Inbox items being promoted or explicitly left for later.
10. **Apply only after confirmation** — write each piece through its own
    workflow ([plans.md](plans.md), [tasks.md](tasks.md)), verify each, then
    summarize what actually landed.

## Boundaries

- Don't revisit Strategic Priorities or Goals mid weekly-planning unless step 1's
  read turns up something that clearly warrants flagging (invariant 14 still
  applies — flag it, don't change it here).
- If the user wants more than 3 Weekly Outcomes, name the focus risk once (spec
  §16) and proceed with their choice.
