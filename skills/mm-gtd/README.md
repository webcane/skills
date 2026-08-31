# mm-gtd — Covey/GTD planning in Logseq

A single router skill with three sub-agent commands that run a personal planning system
(Stephen Covey 4th-generation + David Allen GTD capture) in a **Logseq** graph:
roles → big rocks → week → day, with everything captured into an `inbox/` dropzone first.

## Commands

| Command | What it does |
|---|---|
| `ingest` | «Выгрузка»: capture a stream of tasks/ideas/URLs into the `inbox/` dropzone. «Миссия и цели»: maintain mission + yearly goals. |
| `planning` | «Разбор» / «Недельный ритуал»: turn `inbox/` into a weekly plan page in `journals/` (big rocks = QII first), archive captures to `raw/`. «Итог дня»: evening wrap-up into the daily journal. |
| `query` | «Что сегодня» (≤3 priorities, ≥1 from QII), ad-hoc summaries (inbox, per-role counts, overdue), monthly rocks↔goals check. Read-only. |

## Requirements

- A Logseq graph (plain-markdown outliner, no plugins needed).
- A `config.yaml` at the graph root (roles, quadrants, paths) — the router offers to
  scaffold one.
- `inbox/` (capture dropzone) and `raw/` (processed archive), gitignored.

## Usage

Say it in plain words: "выгрузка", "разбор", "недельный ритуал", "что сегодня", "итог дня",
"миссия и цели", "что в инбоксе", "что просрочено" — the router dispatches to the right
sub-agent. Or call explicitly: `/mm-gtd ingest|query|planning`.

## Layout

```
SKILL.md                  router — dispatches to the three sub-agents
references/
  gtd-conventions.md      shared: config.yaml schema, page schema, task properties, routing
  ingest.md               capture sub-agent
  query.md                read-only query sub-agent
  planning.md             weekly ritual + day-end sub-agent
```
