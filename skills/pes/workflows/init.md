# Workflow: init

Bootstrap check for the six-list skeleton (see
[rules/data-model.md](../rules/data-model.md)). Idempotent — safe to run any
time, including automatically as part of pre-flight (see `SKILL.md`). Structural
writes (creating a missing list) still go through confirmation — this is not one
of the two light-touch paths in [rules/autonomy.md](../rules/autonomy.md).

## Steps

1. **READ** — `reminders_lists` `read`. Compare against the required six:
   `Inbox`, `Strategic`, `Initiatives`, `Plans`, `Tasks`, `Results`.
2. If all six exist: also check for the `Strategic` / `WIP Limit` reminder
   (`reminders_tasks` `read`, `filterList: "Strategic"`, `search: "WIP Limit"`).
   If everything is present, report **"already set up"** and stop — no writes,
   no confirmation prompt.
3. If anything is missing: **PROPOSE** the exact set of creates —
   `reminders_lists` `create` for each missing list, and (if missing)
   `reminders_tasks` `create` for a `WIP Limit` reminder in `Strategic`
   (`title: "WIP Limit"`, `note: "3"`, `completed: false`). Show the full list
   of what will be created.
4. **CONFIRM** once for the whole batch (this is a one-time structural setup,
   not an ongoing bulk edit — a single yes covers it).
5. **WRITE** each missing list, then the `WIP Limit` reminder if needed.
6. **VERIFY** — re-read `reminders_lists` and confirm all six now exist; re-read
   the `WIP Limit` reminder by its returned `id`.
7. Report exactly what was created vs. what already existed. Don't seed any
   example Values/Areas/Goals/Initiatives/Plans — `init` only creates the empty
   skeleton (the six lists + the WIP Limit config entry). Populating Strategic
   content is the user's call, made through the normal `plans`/Strategic-edit
   write-flows, not implied by running `init`.

## When this runs

- **Explicitly**: user says "инициализируй", "setup", "первый запуск", or runs
  `/pes init`.
- **Automatically offered** (not silently run) whenever pre-flight in `SKILL.md`
  finds the six-list skeleton incomplete, before proceeding with whatever the
  user originally asked. Offer once per session at most — if the user declines,
  proceed with their original request against whatever partial structure exists
  rather than asking again on every turn.
- **From `lint`**: a missing-list `INFO` finding should point here rather than
  proposing an inline fix of its own.

## What this does not do

- Does not migrate or reclassify anything already sitting in a `Tasks` (or
  similar) list that predates `pes` — e.g. a bare reminder created by hand, or
  by another skill, in a list that happens to share a name. Existing items are
  left exactly as they are; `lint` will flag ones that don't fit the tag
  convention ([tasks.md](tasks.md), [lint.md](lint.md)) so the user can decide
  case by case whether to bring them into the model.
