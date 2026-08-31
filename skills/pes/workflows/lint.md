# Workflow: lint

Read-only. No confirmation needed — this is pure analysis
([rules/autonomy.md](../rules/autonomy.md)). Classify every finding as `ERROR`,
`WARNING`, or `INFO`.

## Reads required

- `reminders_lists` `read` — confirm the six expected lists exist (`Inbox`,
  `Strategic`, `Initiatives`, `Plans`, `Tasks`, `Results`). Any missing → `ERROR`
  — the skeleton isn't set up; point at [init.md](init.md) rather than proposing
  an inline fix here.
- `reminders_tasks` `read` per list, `showCompleted: true` where the check needs
  completed items (e.g. Results-vs-Activity), `false` otherwise.

## Checks

### Strategic
- Goal entries (`type-goal`) with no Area/Value context referenced anywhere →
  `INFO` — Goals don't strictly require it, but flag for the user to consider.
- Priority entries (`type-priority`) whose `p0..p3` tag is missing or duplicated
  (two entries claiming the same tier) → `WARNING`.

### Tactical
- Plan missing `init-<slug>` tag or `Initiative:` note line → `ERROR` (invariant 1).
- Plan missing `Expected Outcome:` note line → `ERROR` (invariant 2).
- Plan missing a deadline/time horizon (`dueDate` and no `Time Horizon:` line) →
  `WARNING`.
- Active Plans (`status-active`) count > WIP limit (read from `Strategic` /
  `WIP Limit`, default 3) → `WARNING` — "WIP limit exceeded."
- Initiative with no `goal-<slug>` tag and no justification in notes → `WARNING`
  (invariant 3 — belonging to Strategic context; a standalone Initiative is
  allowed but should be explicit, not silent).

### Operational
- Task in `Tasks` with **neither** a `plan-<slug>` tag **nor** an `adhoc`
  tag → `WARNING` — unclassified (see
  [rules/data-model.md](../rules/data-model.md); every Task must carry exactly
  one). Typically means it predates `pes`, was created outside the skill, or
  slipped through an old version of the create flow — propose classifying it
  (ask which Plan, or confirm `adhoc`) rather than guessing.
- Task with **both** `plan-<slug>` and `adhoc` tags → `WARNING` —
  contradictory classification, ask the user which one is correct.
- Task tagged `plan-<slug>` where that Plan no longer exists or isn't
  `status-active` → `WARNING` — orphaned link, worth confirming the Task still
  makes sense.
- Task title that reads as multiple independent actions (heuristic: contains
  " и ", " and ", multiple verbs, a list-like structure) → `WARNING`, "non-atomic
  — propose decomposition" (point at [tasks.md](tasks.md) decompose step, don't
  decompose from inside lint).
- Task with no discernible action verb / no `Done when:` note → `WARNING`.
- `dueWithin: overdue` Tasks not completed → `WARNING`.
- Tasks sharing the same `dueDate` day with conflicting `priority: High` in large
  numbers (heuristic threshold: more than ~5 High-priority Tasks due the same
  day) → `INFO` — possible overcommitment.
- Count of Tasks with `priority: High` and no completion in the lookback window →
  `INFO`, feeds into activity/outcome check below.

### Outcome / Result
- Plan with `status-completed` and no `Results` entry noting that Plan (and no
  explicit cancellation reason on the Plan itself) → `ERROR` (invariant 6).
- Plan with several completed Tasks tagged to it but zero `Results` entries in a
  comparable window → `WARNING` — "activity without outcome", see
  [rules/outcomes.md](../rules/outcomes.md).
- `Results` entry with no `Plan:` note line → `WARNING` (orphaned Result).

## Output

Group by ERROR / WARNING / INFO, each line: `[LEVEL] <entity> — <what> — <fix
proposal, one clause>`. End with counts. Do not auto-fix anything — lint reports,
it doesn't write.
