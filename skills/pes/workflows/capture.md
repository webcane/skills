# Workflow: capture

Capture first, decide later (invariant 7). This is the light-touch path from
[rules/autonomy.md](../rules/autonomy.md) — no confirmation gate, but still
write → verify.

## Steps

1. Take the user's raw input verbatim — don't paraphrase, don't classify it into
   a Plan/Initiative/Task yet.
2. Call `reminders_tasks` `create`: `title` = the input (trimmed), `targetList` =
   `Inbox`. No tags, no priority, no dueDate unless the user gave one explicitly
   in the same breath ("capture: позвонить X завтра" → `dueDate` tomorrow is fine;
   don't infer a date otherwise).
3. Re-read the created reminder by its returned `id` to verify it landed
   (`reminders_tasks` `read`, `id: <id>`).
4. Show the one line that was captured. That's it — do not propose turning it
   into a Plan, do not ask clarifying questions about scope, do not decompose it.

## Mission & Goals maintenance

"capture: миссия и цели" style requests that explicitly target Strategic content
(a Value, Area, Goal, or Strategy entry) are **not** light-touch — they're a
Strategic Level edit. Route these through the full write-flow in
[rules/autonomy.md](../rules/autonomy.md) instead of this workflow's fast path:
read current `Strategic` entries, propose the specific addition/edit, show the
diff, wait for confirmation, then write and verify.

## What never happens here

- Never auto-create a Plan or Initiative from an Inbox capture.
- Never modify the current active Plan because a new idea came in mid-execution
  — it goes to Inbox regardless of how related it looks (invariant 7,
  [rules/architecture.md](../rules/architecture.md)).
