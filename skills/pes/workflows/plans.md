# Workflow: plans

Tactical Level, via `reminders_tasks` (Plans are reminders in the `Plans` list —
see [rules/data-model.md](../rules/data-model.md)). Every write here goes through
the **full** flow in [rules/autonomy.md](../rules/autonomy.md) — Plans are never
light-touch.

## list

`reminders_tasks` `read`, `filterList: "Plans"`. Filter by `filterTags:
["status-active"]` etc. as asked. Read-only.

## create

**Required before proposing the write** (invariants 1, 2, plus WIP, plus time
horizon — spec §15 "При создании Plan обязательно проверить: Initiative,
Expected Outcome, Time horizon, WIP"):

1. **Initiative** — ask which Initiative this Plan implements if not given.
   Read `Initiatives` to confirm it exists; if not, that's a separate `ERROR` to
   surface (don't silently create an Initiative to unblock the Plan — that's its
   own Strategic-context write, propose it separately).
2. **Expected Outcome** — if missing, don't create the Plan. Say plainly:
   `WARNING: Expected Outcome missing.` and propose a phrasing based on what the
   user described, then wait for them to confirm or correct it. This is
   invariant 2 — a hard gate, not a nudge.
3. **Time horizon** — a deadline or period. If missing, ask for one; don't
   default silently.
4. **WIP check** — read `Plans` filtered `status-active`, compare count to the
   `Strategic` / `WIP Limit` entry (default 3). If creating this Plan would
   exceed it: say `WIP limit exceeded.` and offer the alternatives from spec §9 —
   complete an existing Plan, defer one, cancel one, or raise the WIP limit
   (each of those is itself a confirmed write). **Do not create the new Plan
   silently past the limit** even if the user seems to want it — get an explicit
   choice among the alternatives, including "raise the limit," first.

Once all four are satisfied: propose the full entry (title, `Initiative:`,
`Expected Outcome:`, `Time Horizon:`, `Status: active`, `init-<slug>` tag,
inherited `p0..p3` tag from the Initiative), show it, confirm, write, verify.

## update

Same fields as create; show a before→after diff for whatever changed. Changing
`Initiative:` or `Expected Outcome:` after the fact is still a normal update, not
a Strategic edit — but flag if it looks like it's erasing history rather than
correcting it (ask instead of assuming).

## complete

Requires (invariant 6): either a `Results` entry already exists tagged/noted to
this Plan, or an explicit statement from the user of *what actually happened*
(which then gets recorded as a Result — see [results.md](results.md) — as part
of the same confirmed operation) or an explicit cancellation-style reason if
there's genuinely no Result. Then `reminders_tasks` `update`: `completed: true`,
swap `status-active` tag for `status-completed` (`removeTags`/`addTags`).

## cancel

Same tag swap to `status-cancelled`. Always ask for and record the reason in
`note` — invariant 6 requires either a Result *or* an explicit cancellation
reason; cancel is the branch that supplies the reason.

## defer

Tag swap to `status-deferred`, keep `completed: false`. Useful as the WIP-limit
escape valve — a deferred Plan drops out of the `status-active` count.

## review

Walk active Plans with the user: current `Expected Outcome`, Tasks status, any
Results so far, WIP standing. Feeds into [review.md](review.md) and
[retrospective.md](retrospective.md) rather than being a separate write path.

## decompose into Tasks

List the Plan's Expected Outcome and ask/propose which Tasks would move it
forward. This is the `tasks` bulk-create flow, scoped to this Plan
(`plan-<slug>` tag on each new Task) — hand off to
[tasks.md](tasks.md#create--multiple--bulk) rather than duplicating the create
logic here.
