# Task vs Expected Outcome vs Result

Three different things, easy to blur:

```
Task            = activity            — "решить 10 задач Python"
Expected Outcome = the target state    — "быть готовым к Python technical interview"
Result          = what actually happened — "успешно пройти mock interview с оценкой 8/10"
```

- **Task** lives on a Task reminder in `Tasks`. It's something you *do*.
- **Expected Outcome** lives in a Plan's notes (`Expected Outcome:` line). It's the
  state the Plan is aimed at — set once, at Plan creation, and only changed through
  the Plan `update` write-flow.
- **Result** lives on its own reminder in `Results`, linked to the Plan via
  `Plan:` in notes. It's the state that actually happened, recorded after the
  fact — not inferred from Tasks being checked off.

**Results matter more than Activities** (invariant 12). Completing Tasks is not
the same as producing a Result, and the skill must say so when the data shows a
gap.

## Detecting activity-over-outcome

When Tasks in `Tasks` tagged `plan-<slug>` are being completed at a steady rate but
`Results` has no reminder tagged/noted for that same `plan-<slug>` over a
comparable window, that's the pattern. Report it plainly:

```
WARNING: High activity, low outcome — <Plan title> has N Tasks completed in the
last <period> and no recorded Result. Activity ≠ Outcome. Consider recording a
Result, or revisiting whether these Tasks are actually moving the Expected
Outcome.
```

This check is read-only analysis — it never auto-creates a Result or auto-closes
the Plan. Surface it in `status`, `lint`, `review`, and `retrospective`.

## Outcome Rate (metric, not a KPI dashboard)

`Outcome Rate` = (Plans with at least one recorded Result) / (Plans that reached
`status-completed` or `status-cancelled` in the period). Report it as one number
in `status`/`review`, not broken into sub-metrics — this system is decision
support, not a dashboard (spec §20).

## Rule of 3 (a focus limiter, not a hard cap)

Weekly planning and daily execution should each converge on **1–3 key
Outcomes/Tasks**. If the user wants more, don't block it — name the risk once
("you're setting N key outcomes this week — more than 3 tends to dilute focus")
and proceed with what they chose.
