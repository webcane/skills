# mm-gtd Conventions (Logseq planning graph)

Shared reference for the `mm-gtd` router's three sub-agent commands (`ingest`, `query`,
`planning`). Every command reads this file before touching the planning graph. The target
system is a **Logseq** graph — plain-markdown outliner, no database, no plugin API. The
skill runs from any coding agent or chat; where a step says "run this command", execute it
with whatever shell/file access your environment gives you.

The methodology is **Covey 4th-generation** (roles → big rocks → week → day) with **GTD
capture** (everything lands in an Inbox first, then gets processed).

## Why this architecture (L1/L2)

- **L1 = the agent's memory/system-prompt**: rules, identity, credentials. Small, always present.
- **L2 = this planning graph**: roles, tasks, weekly plans, mission. Loaded on demand via the commands.

Routing rule for new information: *would getting this wrong be dangerous or embarrassing?*
→ L1 memory, not the graph. *Merely inconvenient to re-derive?* → the graph.

Two mechanisms keep the graph cheap to query:

- **Hub-Index-Routing** — `Planning/Index` carries a short `### Index` list, one line per
  routable page (`[[link]] -- description`). A query reads the index first (cheap), then
  opens only the 3-5 pages the index points to (expensive).
- **Access-Log** — every full page read is logged. Later this feeds pruning of old weeks
  and stale role content (a future `prune`-style command), keeping routing sharp.

## Configuration: `config.yaml`

Every command starts by reading `config.yaml` from the planning root (current directory,
then walking up parents). If it's missing, stop and ask the user to create one (or offer to
scaffold it) rather than guessing paths.

```yaml
tool: logseq                    # fixed — targets a Logseq graph
planning_path: /path/to/graph   # the Logseq graph root (contains logseq/, pages/, journals/)
pages_dir: pages                # relative to planning_path
journals_dir: journals          # relative to planning_path — daily pages AND week pages
inbox_dir: inbox                # relative to planning_path — the capture dropzone
raw_dir: raw                    # relative to planning_path — processed-capture archive
roles:                          # the Covey roles; each with a belonging test
  - name: Family
    test: "про семью и дом"
  - name: Work
    test: "рабочие задачи"
  - name: Sharpening            # «Заточка пилы»
    test: "спорт, чтение, обучение, хобби, отдых"
quadrants: [I, II, III, IV]     # I=important+urgent, II=important-not-urgent (big rocks),
                                # III=urgent-not-important, IV=neither
week_naming: "YYYY-Www"         # ISO week; week page file = journals/<week_naming>.md
```

If `roles` is absent, discover them from existing role pages (filenames
`Planning___Role___*.md`) instead of failing.

## Graph layout

```
<planning_path>/
├── config.yaml
├── inbox/                     # capture dropzone (gitignored) — unprocessed captures
├── raw/                       # processed-capture archive (gitignored, append-only)
├── journals/                  # dated pages + week pages
│   ├── 2026_08_10.md          # daily journal (Logseq built-in)
│   └── 2026-W33.md            # week page
└── pages/                     # stable pages
    ├── Planning___Index.md            # routing hub
    ├── Planning___Role___Family.md    # one per role
    ├── Planning___Role___Work.md
    ├── Planning___Mission-Goals.md
    └── Planning___Reference___Access-Log.md
```

## The capture cycle (inbox/ → raw/)

This is the GTD heart of the system and mirrors the wiki dropzone pattern:

1. `ingest` («Выгрузка») captures new material **into `inbox/`** — never anywhere else.
   Pasted text / verbal dumps are saved as a structured capture file
   `inbox/YYYY-MM-DD_<slug>.md`; URLs are fetched and saved; local files are copied
   **byte-for-byte**, preserving the original filename.
2. `planning` («Разбор» / «Недельный ритуал») is the only command that reads `inbox/`.
   It turns captures into tasks on the right pages and **archives each processed file to
   `raw/` byte-for-byte** (append-only, never re-read). Collision in `raw/` → date-prefix
   `YYYY-MM-DD_<name>`.
3. **Failed or unclear captures stay in `inbox/`** — left behind with a reason; they'll be
   re-read on the next run. The move to `raw/` is the commit point: only genuinely
   processed captures leave `inbox/`.

`.gitignore` must cover `inbox/` and `raw/` (raw captures can contain sensitive material
before filtering). Offer to add the two lines if they're missing.

## Logseq file format

- Every `pages/` page is a flat file directly under `pages_dir` — no folder hierarchy.
  Namespaces are encoded in the filename with triple underscores:
  `Planning___Role___Work.md` = page `Planning/Role/Work`.
- **Journals** live in `journals_dir` as `YYYY_MM_DD.md` (daily) and week pages per
  `week_naming` (e.g. `2026-W33.md`).
- **Outliner format**: every line is a bullet starting with `- `. Sub-items indent one tab
  (or two spaces — match the file).
- **Properties**: `key:: value` bullet lines at the very top of the page. No YAML frontmatter.
- **Headings**: `- ## Heading` / `- ### Subheading` as their own bullet.
- **Cross-references**: `[[Planning/Role/Work]]` — always the full `/`-joined page name.
  Logseq resolves these bidirectionally (backlinks).
- **Tags**: `#tag` inline, lowercase, hyphenated for multi-word.
- **Dates**: ISO 8601 (`YYYY-MM-DD`) everywhere — `created::`, `updated::`, `due::`,
  `archived::`, and inside the Access-Log.

## Page types

| page | file | type:: | purpose |
|---|---|---|---|
| Index hub | `pages/Planning___Index.md` | `hub` | `### Index` routing to every routable page (roles, current week, mission) |
| Role hub | `pages/Planning___Role___<Name>.md` | `role` | active tasks for the role |
| Mission & goals | `pages/Planning___Mission-Goals.md` | `mission` | mission + yearly goals |
| Week page | `journals/<YYYY-Www>.md` | `week` | big rocks (QII) first, then supporting tasks by role |
| Daily journal | `journals/YYYY_MM_DD.md` | — | day plan / «Итог дня» (Logseq built-in) |
| Access-Log | `pages/Planning___Reference___Access-Log.md` | `reference` | append-only full-read log (see below) |

## Task properties and naming

Every task (a task bullet) carries:

- `role::` — one of the config roles. If nothing fits → `role:: ?` and ask the user; never
  invent a role silently.
- `quadrant::` — `I` / `II` / `III` / `IV`. If not obvious → `quadrant:: ?` and batch-ask.
- `status::` — `Inbox → Разобрано → В работе → Сделано`. Captured items start as `Inbox`;
  «Разбор» advances them.
- `due::` — optional, ISO date.
- `week::` — optional link to the week page it's scheduled on (e.g. `[[2026-W33]]`).
- `created::` / `updated::` — ISO dates.

**Naming rule**: a task is «глагол + результат» — "Записать выпуск про X", not "подкаст".
If a captured item is a reminder without a verb+result, rephrase it during «Выгрузка» or
mark it unclear and ask.

## Hub-Index-Routing

`Planning/Index` (file `pages/Planning___Index.md`) is the routing hub:

```
- ## Planning
  - type:: hub
  - ### Index
    - [[Planning/Role/Family]] -- семейные дела и дом
    - [[Planning/Role/Work]] -- рабочие задачи
    - [[Planning/Role/Sharpening]] -- спорт, чтение, хобби, отдых
    - [[Planning/Mission-Goals]] -- миссия и годовые цели
    - [[2026-W33]] -- план недели 33
    - inbox/ -- неразобранные захваты (N файлов)
```

Rules:

- One routing line per routable page; description ≤120 chars and distinctive (it IS the
  routing key).
- The current week page is re-pointed by `planning` every ritual; old week pages move to
  `### Archive` (see Constraints — never rename the file).
- A routable page with no routing line anywhere is findable only by luck — `planning`
  and `ingest` backfill lines on every write.

## Access-Log

Page `Planning/Reference/Access-Log` (file `pages/Planning___Reference___Access-Log.md`):
an append-only record of every full-page read — the input to future pruning of old weeks.

```
- access-log:: true
- type:: reference
- ## Log (append-only, newest at bottom)
  - 2026-08-10 -- [[2026-W33]] -- query -- matched: "what today"
```

Rules:

- Log only pages actually opened and read in full — not the cheap `Planning/Index` read.
- `matched:` = why the page was picked (the routing description or the grep term). ≤60 chars, quoted.
- Append-only; don't create a git commit just for a log append — let it ride with the next
  structural commit.
- This page is exempt from any future health/prune rules.

## Constraints (apply to every command)

- **Never store credentials, tokens, or passwords in the graph.** If a capture contains a
  secret, skip it and tell the user it belongs in L1 memory / a secrets manager.
- **Never overwrite an existing task block.** Append new blocks; if new info contradicts an
  existing block, add a new block noting the contradiction and the date, and let the user
  resolve it later. The user edits this graph by hand too — don't clobber that.
- **Never touch files outside the planning graph** (other wikis, source repos, unrelated notes).
- **Demotion (`archived::`) is never a rename or a move.** Logseq links by page name; moving
  or renaming breaks every incoming `[[link]]`. Demote = move the routing line to
  `### Archive` + set `archived::`. The file stays where it is.
- **Boundary rule**: a task that fits no role → ask the user, don't create a role silently.
- **Imbalance watch** (Covey): if a role has had no big rock for two consecutive weeks, or a
  week is dominated by quadrants I/III, say so out loud on the weekly ritual / in a query answer.

## Language policy

Content (task bodies, week-page prose, journal entries) is written in the **language of the
user's request** — do not translate. Structural keys stay English: property names
(`role::`, `quadrant::`, `status::`), page filenames, `[[links]]`, and section headings.
