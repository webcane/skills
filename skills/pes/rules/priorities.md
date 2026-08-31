# Priorities — two independent dimensions, plus urgency

Never conflate these three. A request that mixes them ("this is urgent so make it
P0") is exactly the mistake this file exists to catch.

## 1. Strategic Priority (P0 > P1 > P2 > P3)

Belongs to the **portfolio** — lives on Priority entries in `Strategic`, and via
the `p0`..`p3` tag on Initiatives (and, inherited for display, on their Plans).
Example: `P0 — Financial Stability`, `P1 — Long-term Capitalization`,
`P2 — Optional Growth`, `P3 — Hobby`.

**Never appears on a Task.** A Task doesn't carry Strategic Priority — it inherits
context through `plan-<slug>` → the Plan's Initiative → that Initiative's `p0..p3`
tag, if anyone needs to trace it that far. Don't add a `p0..p3` tag to a Task
reminder.

Changing a P0/P1/P2/P3 assignment is a **Strategic Level change** — always goes
through the full propose → confirm loop in [autonomy.md](autonomy.md), never
inferred silently from Task activity (invariant 14).

## 2. Operational Priority (Reminders' native priority field)

Lives on Task reminders only: `High | Medium | Low` (mapped to Reminders' `1 | 5 |
9`; `0`/none = unset). This is about the Task's importance, decided when the Task
is created or triaged — see [data-model.md](data-model.md) for the exact field
mapping.

## 3. Urgency (separate from both)

Expressed only through `dueDate` (and, at the Plan level, the Time Horizon).
**Urgency never changes Strategic Priority** (invariant 11): a P3 Task with a
looming deadline stays P3-context — it can legitimately get `priority: High` and
an imminent `dueDate` (both Operational-Priority and urgency moves), but that
never turns into "so this Initiative should be P0 now." If a pattern of urgent P3
work suggests the *portfolio* ranking is actually wrong, that's Review/Retrospective
material — surface it as a proposal (invariant 14), don't apply it.

## Quick check before writing a priority-looking field

1. Is this about the *portfolio* (which Initiative/Goal matters more)? → Strategic
   Priority, P0–P3, Strategic-Level change, needs confirmation.
2. Is this about *this Task's* importance relative to other Tasks? → Operational
   Priority, High/Medium/Low, light-touch (no confirmation gate — see
   [autonomy.md](autonomy.md)).
3. Is this about *when*? → `dueDate`. Doesn't touch either priority dimension.
