# mm-wiki Conventions (Logseq)

Shared reference for the mm-wiki-* skill family (`mm-wiki-ingest`, `mm-wiki-query`,
`mm-wiki-prune`, `mm-wiki-lint`, `mm-wiki-status`, `mm-wiki-import`). Every one of
these skills reads this file's rules before touching the wiki. The target system is
always **Logseq** — a plain-markdown outliner graph, no database, no plugin API
required. Any of these skills can be run from any code agent (Claude Code, OpenCode,
Cursor, etc.) and any model — nothing here depends on Claude-specific tools. Where a
step says "run this command," it means: execute it with whatever shell/file access
your environment gives you (bash tool, terminal, or manual file read/write if no
shell is available).

## Why This Architecture (L1/L2 Cache Model)

- **L1 = the agent's memory/system-prompt** (auto-loaded every session): rules,
  gotchas, identity, credentials. Small and always present.
- **L2 = this wiki** (loaded on demand, via these skills): projects, workflows,
  research, deep knowledge. Large and queried, not loaded wholesale.

Routing rule for new information: *would getting this wrong be dangerous or
embarrassing?* → belongs in L1 memory, not here. *Merely inconvenient to
re-derive?* → belongs here, in L2.

As the wiki grows, two mechanisms keep L2 cheap to query instead of turning into
"grep everything and hope":

- **Hub-Index-Routing** — every hub page carries a short `### Index` list, one line
  per child page (`[[link]] -- description #tags`). A query reads the *index* first
  (cheap) and only opens the 3-5 pages the index says are relevant (expensive),
  instead of reading every page in the namespace.
- **LRU-Demote** — every full-page read gets logged. Pages nobody has queried in a
  long time get moved out of the live index into an `### Archive` section. The file
  is never deleted and every `[[link]]` to it keeps working — it just stops being a
  candidate during routing, so the index stays sharp instead of growing forever.

## Configuration: `llm-wiki.yml`

Every skill in this family starts by reading `llm-wiki.yml` from the wiki root. If
it's missing, stop and ask the user to create one (or offer to scaffold it) rather
than guessing paths.

```yaml
tool: logseq                  # fixed — this family targets Logseq only
wiki_path: /path/to/graph     # the Logseq graph root (contains logseq/ and pages/)
pages_dir: pages              # relative to wiki_path
memory_path: null             # optional: path to the agent's L1 memory dir, for L1/L2-duplicate checks
namespaces:                   # top-level namespaces this wiki uses
  - Tech
  - Projects
  - Business
  - People
  - Learning
  - Reference
```

If `namespaces` is absent, discover them by listing the distinct first segments of
existing page names instead of failing.

## Logseq File Format

- Every page is a flat file directly under `<wiki_path>/<pages_dir>/`. There is no
  folder hierarchy — namespaces are encoded in the filename.
- **Filename**: triple-underscore separates namespace segments, e.g. the page
  `Wiki/Tech/Strapi` is the file `Wiki___Tech___Strapi.md`.
- **Outliner format**: every line of content is a bullet starting with `- `.
  Sub-items are indented one tab (or two spaces, match whatever the file already
  uses) plus `- `.
- **Properties**: `key:: value` on bullet lines at the very top of the page (before
  any other content). No YAML frontmatter — Logseq does not use it.
- **Headings**: `- ## Heading` / `- ### Subheading` as their own bullet.
- **Cross-references**: `[[Wiki/Namespace/Page]]` — always the full page name,
  matching the `/`-joined form (not the `___`-joined filename). Logseq resolves
  these bidirectionally (backlinks), so a `[[link]]` from A to B is enough; you do
  not need to also add a manual "referenced by" line on B.
- **Tags**: `#tag` inline, lowercase, hyphenated for multi-word (`#deploy-gotcha`).
- **Dates**: ISO 8601 (`YYYY-MM-DD`) everywhere — `created::`, `updated::`,
  `archived::`, and inside the Access-Log.

## Hub-Index-Routing (format)

A **hub page** is `type:: hub`, one per top-level namespace (e.g.
`Wiki___Tech.md` is the hub for the `Tech` namespace). Every hub carries two
sections:

```
- ## Tech
  - type:: hub
  - ### Index
    - [[Wiki/Tech/Strapi]] -- Strapi 5 CMS, ports, deploy + migration gotchas #strapi #deploy
    - [[Wiki/Tech/PM2]] -- PM2 process management on the VPS, cwd/reload bug #pm2 #deploy
  - ### Archive
    - [[Wiki/Tech/Legacy-Foo]] -- (demoted 2026-06-07) old Foo stack, replaced by Bar #archived
```

Rules:
- One routing line per child page: `[[link]] -- description #tags`.
- Description ≤120 chars, distinctive (it IS the routing key — "Notes about X" is
  useless, "Strapi 5 CMS, ports, deploy + migration gotchas" is not).
- Tags mirror the child page's own `#tags`.
- `### Index` = live, routable via the two-stage query. `### Archive` = evicted,
  only findable by grepping the wiki directly (the L3 fallback).
- The hub's child list **is** the routing index — there's no separate index file to
  keep in sync.
- Every active (non-archived) page belongs in exactly **one** hub's `### Index`. A
  page with no routing line anywhere is unroutable — findable only by luck via
  grep. `mm-wiki-lint --fix` backfills missing lines.

## Access-Log (format)

Page: `Wiki/Reference/Access-Log` (file `Wiki___Reference___Access-Log.md`) — an
append-only record of every full-page read, the input to LRU-Demote and to the
hot/cold profile in `mm-wiki-status`.

```
- access-log:: true
- type:: reference
- ## Log (append-only, newest at bottom)
  - 2026-06-07 -- [[Wiki/Tech/Strapi]] -- query -- matched: "Strapi 5 -- ports, deploy, migration"
  - 2026-06-07 -- [[Wiki/Projects/GEO]] -- query -- matched: "L3-grep: geo strategy"
```

Rules:
- Log only pages actually opened and read in full — not the cheap hub-index reads.
- `matched:` = why the page was picked: the hub-index description/tag that matched
  (index routing) or the grep term that found it (L3 fallback). ≤60 chars, quoted.
  This is what makes the routing auditable later — not just *which* page loaded but
  *why*.
- Append-only. Do not create a version-control commit just for a log append — let
  it ride along with the next structural commit (ingest/lint/prune) so the wiki's
  git history doesn't turn into read-noise.
- This page is exempt from every lint/prune health rule (orphan, stale, demote).

## Page Properties (Schema)

Every wiki should have a `Wiki/Schema` page (file `Wiki___Schema.md`) documenting
its own conventions — page types, required properties per type, confidence levels,
status enums. Read it before creating or classifying pages; these are the defaults
if the wiki has none yet:

| type | required properties | notes |
|---|---|---|
| `hub` | `type::`, `created::` | one per namespace, carries Index/Archive |
| `entity` | `type::`, `status::`, `created::`, `updated::` | people, tools, services — `status::` enum includes `archived` |
| `project` | `type::`, `status::`, `created::`, `updated::` | `status::` enum is `active`/`paused`/`done` — **not** `archived` (see Constraints) |
| `knowledge` | `type::`, `confidence::`, `created::`, `updated::` | concepts, research, how-tos — `confidence::` is `high`/`medium`/`stale` |
| `reference` | `type::`, `created::` | Access-Log, Schema, Dashboard |

If the wiki's own `Wiki/Schema` page defines different types/properties, follow
that instead — this table is only the fallback for a brand-new wiki.

## Constraints (apply to every skill in this family)

- **Never store credentials, tokens, or passwords in the wiki.** It is normally
  git-tracked. If source material contains a secret, flag it and skip it — tell the
  user it belongs in their L1 memory/secrets manager instead.
- **Never overwrite an existing content block.** Append new blocks; if a fact
  contradicts an existing one, add a new block noting the contradiction and the
  date rather than deleting the old one. The user edits pages by hand too — don't
  clobber that.
- **Never touch files outside the wiki** (journals, unrelated notes, source repos).
- **Demotion (`archived::`) is never a rename or a move.** Logseq links by page
  name; moving or renaming a file breaks every incoming `[[link]]` across the whole
  graph. Demote = routing line moves from `### Index` to `### Archive` + an
  `archived::` property. The file stays exactly where it is.
- **`archived::` is safe to set on any page type. An out-of-enum `status::` value
  is not.** For `entity` pages (whose `status::` enum includes `archived`), set
  both. For `project`/`knowledge` pages, set `archived::` only — do not invent a
  `status:: archived` value outside their enum.
- Every active page needs exactly one routing line in some hub's `### Index`.
- Version control: if `wiki_path` is inside a git repository, commit after each
  structural change (new/changed pages, hub index edits, archived:: changes). If
  there's no git repo, or the agent has no git access, skip silently — this family
  does not require git.
- **Language of content**: page content, hub-index descriptions, and tags are
  written in the **same language as the source material** — do not translate. Only
  the structural keys stay in English: property names (`type::`, `created::`, …),
  page filenames, and `[[links]]`, which the Logseq format requires.
- Dates: ISO 8601, always.
