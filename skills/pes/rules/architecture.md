# Architecture — Personal Management Lifecycle (PML)

```
L1 — STRATEGIC
        ↓
L2 — TACTICAL
        ↓
L3 — OPERATIONAL
        ↓
     RESULTS
        ↓
     REVIEW
        ↺
```

Exactly three levels: L1 → L2 → L3. **Each level depends only on the level directly
above it.**

- L2 never rewrites L1 on its own.
- L3 never rewrites L2 on its own.
- Feedback from a lower level can **propose** a change to the level above; applying
  that change always needs the user's explicit decision (invariants 13, 14).

Never invent a shortcut edge (e.g. a Task field that sets Strategic Priority
directly, or a lint auto-fix that closes a Plan without asking). If a workflow
seems to need one, that's a sign the request belongs in a **proposal**, not a
silent write.

## L1 — Strategic

Answers: what matters, what states to reach, what has precedence right now, what's
the general approach.

| Entity | Answers |
|---|---|
| Value | long-lived principle (autonomy, mastery, security, creativity, freedom, …) — never a mandatory Task field |
| Area | a sphere of life/responsibility — context, not a hierarchy rung |
| Goal | a desired future state |
| Priority (P0–P3) | strategic ranking of the portfolio — **not** the same dimension as Task priority ([priorities.md](priorities.md)) |
| Strategy | the general approach to move Goals forward within current Priorities |

## L2 — Tactical

Answers: what are we changing right now to move along the Strategy?

| Entity | Answers |
|---|---|
| Initiative | a long-lived direction of change, `type: project\|hypothesis\|initiative`, connects a Plan back to Strategic context |
| Plan | a time-bound tactical commitment implementing one Initiative. Must have: Initiative, Expected Outcome, time horizon, status, its Tasks. **No direct Plan → Goal field** — Goal is reached through Initiative, so the dependency chain stays one-hop (Plan → Initiative → Strategic) instead of a shortcut. |

## L3 — Operational

Answers: what am I doing right now?

| Entity | Answers |
|---|---|
| Task | one atomic action, with a clear Done criterion, belonging to a Plan when it's tactical work |

Not every Task is tactical work — a Task is either a **pes task** (tied to a
Plan) or an **ad-hoc task** (a bare reminder with no PML linkage), and it's
always one or the other explicitly, never left ambiguous. See
[data-model.md](data-model.md) and [workflows/tasks.md](../workflows/tasks.md)
for how creation resolves which one applies.

## Outside the three levels

**Inbox** — capture buffer. "Capture first, decide later": a new idea during
Execution never silently touches the current Plan; it lands in Inbox.
**Review** — the feedback mechanism that closes the loop back toward Strategic,
gated by explicit user decisions at every level it touches.
**Routines** — Calendar-side infrastructure (when Reviews/Planning *happen*), not
a management entity itself. See [routines workflow](../workflows/routines.md).

## The dialectical framing (methodology, not metadata)

Treat PML as a feedback loop: Direction → Commitment → Execution → Result →
Reflection → Learning → New Commitment. Each level carries a structural tension —
don't resolve it by fiat, and don't tag every Task with a category for it:

- **Strategic:** stability vs growth, exploration vs exploitation, short-term vs long-term.
- **Tactical:** commitment vs flexibility, starting vs finishing, breadth vs focus.
- **Operational:** important vs urgent, plan vs reality, execution vs interruption.

This is interpretive context for how you phrase a Review or Lint finding — not a
field to fill in on every entity.
