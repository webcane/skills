# Workflow: tasks

Operational Level, all via `reminders_tasks` (+ `reminders_subtasks` for
in-task checklists). See [rules/data-model.md](../rules/data-model.md) for the
Task shape and [rules/mcp-tools.md](../rules/mcp-tools.md) for the exact schema.

## list

`reminders_tasks` `read`, filters as requested (`filterList: "Tasks"`,
`filterTags`, `dueWithin`, `filterPriority`, `search`). Read-only, no gate.

## create — single, unambiguous (light-touch)

The common case ("создай задачу X"): follow the light-touch path in
[rules/autonomy.md](../rules/autonomy.md) — show the one line, write, verify.

Before writing, check atomicity (see **decompose** below) — if the title reads as
several independent actions, don't create it as-is; propose the split first.

### Classify before writing — never leave a Task unclassified

`pes` is specifically about running PML, so every Task gets exactly one of two
tags, chosen deliberately, not defaulted silently:

- **pes task** — tag `plan-<slug>`, tied to an active Plan.
- **ad-hoc task** — tag `adhoc`, a bare reminder with no PML linkage
  (spec §4: a Task belongs to a Plan "if it's part of tactical work" — not every
  Task has to be). Not "Activity" — `rules/outcomes.md` already uses
  `Task = activity` for the Task/Outcome/Result distinction; "ad-hoc" avoids
  that collision.

Resolve which one applies, in order:

1. User named a Plan explicitly → **pes task**, `plan-<slug>` (resolve by
   reading `Plans` and matching title; if the named Plan doesn't exist, say so
   — don't silently fall back to ad-hoc).
2. User explicitly said it's not part of PML ("просто напоминание", "не по
   плану", "отдельная задача") → **ad-hoc task**, tag `adhoc`, no question asked.
3. Otherwise, read `Plans` filtered `status-active`:
   - Zero active Plans → nothing to link to; create as `adhoc` and say so
     in the one-line confirmation ("активных Plans нет — создаю как ad-hoc").
   - One or more active Plans → ask **one** short question before writing:
     which Plan, or "ad-hoc задача (вне PES)". Then proceed light-touch with
     the answer — this is still a single quick choice, not a lecture.

Fields: `title` (action-oriented), `targetList: "Tasks"`, `dueDate` if given,
`priority` if given (map High/Medium/Low → 1/5/9), `tags` = the classification
tag from above plus `area-*` if an Area is clear from context. If a "Done when"
criterion is stated or obviously implied, put it in `note` as `Done when:
<criterion>`.

## create — multiple / bulk

More than one Task in a single request is a **bulk change** — full write-flow
(propose the whole batch, show it as a list, confirm once for the batch, write
each, verify each) per [rules/autonomy.md](../rules/autonomy.md). Classify each
item the same way as above (`plan-<slug>` or `adhoc`) before showing the
proposed batch — don't leave any item's tag implicit.

## update / reschedule / reprioritize (single, explicit)

Light-touch if it's one Task and the user's instruction is unambiguous (e.g.
"перенеси задачу X на завтра", "повысь приоритет Y"). `reminders_tasks` `update`
with the changed field(s) only. Reprioritizing several Tasks at once is bulk →
full write-flow.

## complete

`reminders_tasks` `update`, `id`, `completed: true`. Light-touch for one Task.
After completing a Task tagged `plan-<slug>`, don't auto-suggest recording a
Result — that's a separate, user-initiated act (see [results.md](results.md)); it's
fine to *mention* that the option exists if several Tasks on that Plan have just
closed with no Result yet (ties into the activity-over-outcome check).

## decompose

Trigger: a Task title/description contains multiple independent actions, or the
user says it's too big. **Never decompose silently** (invariant 5, spec §4).

1. Show the proposed split as a numbered list of smaller Task titles, each with
   its own Done criterion.
2. Wait for confirmation (or edits to the split).
3. On confirmation: create the new Tasks (bulk create flow), then ask whether to
   delete/complete the original oversized Task or leave it as a parent note.
   Default suggestion: delete the original once the split is confirmed to avoid
   duplicate tracking — but this is the user's call, not automatic.

## move

Changing a Task's `targetList`, or swapping its classification tag (`plan-<slug>`
↔ `adhoc`, or from one Plan's `plan-<slug>` to another's — always
`removeTags` the old one and `addTags` the new one, never leave both or neither
present). Single + explicit → light-touch update; otherwise → bulk flow.

## review

Not a distinct MCP action — this is "show me these Tasks so I can decide on
each," i.e. a `list` read followed by walking through the results with the user
and routing each one to update/complete/reschedule/decompose as they decide.
