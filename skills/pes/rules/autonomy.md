# Autonomy boundaries

## Allowed without confirmation

READ, ANALYZE, LINT, STATUS, REPORT, PROPOSE. All of `capture` (see the light-touch
note below), `lint`, `status`, `results list/review`, and the read side of
`tasks`/`plans`/`routines` run freely.

## Requires explicit confirmation (full write-flow, below)

- Create/modify/complete/cancel a **Plan**
- Create an **Initiative**
- Any **Strategic Level** edit (Value, Area, Goal, Priority, Strategy)
- Any **Priority** change (Strategic P0–P3 *or* reassigning several Tasks' Operational
  Priority at once)
- **Bulk** Task changes (more than one Task in a single operation)
- Recording a **Result**
- Create/modify/delete a **Calendar routine**

Never automatically: change Values, Goals, Strategy, or Strategic Priorities.
The skill's only move there is detect → propose → wait (invariant 14).

## Light-touch path (no yes/no gate, but still read → write → verify)

Two narrow exceptions, because gating them defeats their purpose:

- **`capture`** — Inbox capture is "capture first, decide later" by design (spec
  §6). Write immediately, then read back to confirm it landed, then show the one
  line captured. No Plan/Initiative is touched, so there's nothing to gate.
- **A single, unambiguous, explicitly-requested Task** create/update/complete/
  reschedule — e.g. the user says "создай задачу X" with no ambiguity about which
  Plan (or explicitly none). Show the one line you're about to write, write it,
  read it back, confirm. This is *not* a diff-and-wait — it's write-then-show,
  matching spec §25 ("минимально необходимый workflow").

Everything else in the confirmation list above follows the full loop:

```
READ → ANALYZE → PROPOSE → SHOW DIFF → USER ACCEPTS → WRITE → VERIFY
```

1. **READ** — pull current state from the MCP. Never reuse a value read earlier in
   the conversation without re-reading if state might have changed.
2. **ANALYZE** — check the relevant invariants ([invariants.md](invariants.md)),
   WIP if a Plan is involved, atomicity if a Task is involved.
3. **PROPOSE** — state exactly what you intend to write: which tool, which
   action, which fields, in plain language (not raw JSON) — a title, a due date,
   a list, tags.
4. **SHOW DIFF** — for an update, show before → after per changed field. For a
   create, show the full new entry as it will appear.
5. **USER ACCEPTS** — wait for an explicit yes. A vague "sure" on a specific
   proposal counts; silence doesn't.
6. **WRITE** — call the MCP tool exactly as proposed. If the call errors, report
   the error verbatim — don't retry silently with different fields.
7. **VERIFY** — re-read the entity that was just written (by the `id` the tool
   returned) and confirm the fields match what was proposed. **Only then** say
   "done." If verification fails or the MCP gives no confirmation, say so — never
   report success on an unconfirmed write (invariant 17).

## Planning vs Execution

**Planning mode** may: analyze Inbox, analyze Plans, weigh Priorities, propose
Plans, decompose Plans into Tasks, set Weekly Outcomes, check WIP, propose changes.

**Execution mode** helps: surface current Tasks, surface priority, show the next
action set, close Tasks, record Results.

**During Execution, never** revisit Strategy or start a new Initiative on your own
initiative (pun intended) — a new idea that surfaces mid-execution goes to Inbox
(invariant 7), full stop, even if it looks urgent.
