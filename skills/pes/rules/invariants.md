# Core invariants

These are hard rules, not preferences. Every workflow file enforces the ones
relevant to it; this file is the canonical list to check a workflow (or an ad-hoc
request) against when something feels off.

| # | Invariant | Enforced by |
|---|---|---|
| 1 | Every Plan has an Initiative | `plans` create/update checklist; `lint` |
| 2 | Every Plan has an Expected Outcome | `plans` create/update checklist; `lint` |
| 3 | Every Initiative belongs to Strategic context (a Goal, or explicit standalone justification) | `plans`/`lint` |
| 4 | Every Task must be actionable | `tasks` create; `lint` |
| 5 | Non-atomic Tasks should be decomposed — proposal shown, never silent | `tasks` decompose |
| 6 | Every completed Plan has an actual Result or an explicit cancellation reason | `plans` complete/cancel; `lint` |
| 7 | New ideas go to Inbox before becoming commitments | `capture` |
| 8 | Planning and Execution are separate modes | [autonomy.md](autonomy.md) |
| 9 | WIP is limited (configurable, default 3) | `plans` create; `status`; `lint` |
| 10 | Strategic Priority and Operational Priority are different dimensions | [priorities.md](priorities.md) |
| 11 | Urgency does not change Strategic Priority | [priorities.md](priorities.md) |
| 12 | Results matter more than Activities | `status`; `lint`; `retrospective` |
| 13 | Lower levels do not autonomously modify upper levels | [architecture.md](architecture.md) |
| 14 | Strategic changes require explicit user confirmation | [autonomy.md](autonomy.md) |
| 15 | Reminders is the only source of truth — never cache Plans/Tasks/Results in skill memory or conversation history across turns | every workflow |
| 16 | Calendar stores *when*; Reminders stores *what* | [architecture.md](architecture.md); `routines` |
| 17 | Every write operation is proposed first, then confirmed, then executed, then verified — except the light-touch paths named explicitly in [autonomy.md](autonomy.md) | [autonomy.md](autonomy.md) |

When a user request would violate one of these, don't refuse outright and don't
silently "fix" it either: say which invariant is at stake, in one sentence, and
propose the smallest correction (add the missing Expected Outcome, decompose the
Task, ask which Plan to cancel to stay under WIP, …). Then wait for their call.
