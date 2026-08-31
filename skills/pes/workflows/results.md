# Workflow: results

See [rules/outcomes.md](../rules/outcomes.md) for the Task/Outcome/Result
distinction before using this workflow — a Result is what *actually happened*,
not a checked-off Task.

## record Result

Full write-flow (recording a Result requires confirmation per
[rules/autonomy.md](../rules/autonomy.md)):

1. Ask (or take from context) which Plan this Result belongs to; read `Plans` to
   confirm it exists and resolve its slug.
2. Propose the Result entry: `title` = the actual outcome statement (not the
   activity — if the user describes an activity, ask "what actually happened as
   a result of that?" once, don't force it if they resist), `targetList:
   "Results"`, `completed: true` (it's a log entry), `note` = `Plan: <plan
   title>` + optional `Task(s):` + `Recorded: <today>`.
3. Confirm, write, verify (re-read by `id`).

## list

`reminders_tasks` `read`, `filterList: "Results"`, `showCompleted: true`
(they're always completed). Read-only.

## link Result to Plan

Always done at creation time via the `Plan:` note line — there's no separate
"link" MCP call (no cross-reminder relation exists, see
[rules/mcp-tools.md](../rules/mcp-tools.md)). If a Result was recorded without a
`Plan:` line (an orphan flagged by `lint`), fixing it is a normal `update` on
that Result reminder — still needs confirmation, since it's writing to a Results
entry.

## review Results

Read Results in the asked period, group by Plan. For each Plan with Results,
show Expected Outcome next to what was actually recorded — that comparison is
the point of this command, not a bare list.

## analyze Results over a period

Feed into `Outcome Rate` (see [rules/outcomes.md](../rules/outcomes.md)):
Plans closed (`status-completed`/`status-cancelled`) in the period vs. Plans in
that set with at least one Result. Report the ratio plus which Plans have none.
This is analysis only — no write.
