---
name: mm-wiki-ingest
description: >
  Process source material (a pasted conversation, a document, a URL, a decision someone just made)
  and distribute the knowledge it contains across a Logseq personal/team wiki, creating or updating
  pages and keeping hub routing indexes and cross-references intact. Use this whenever the user says
  things like "add this to the wiki", "capture this", "log this decision in the wiki", "remember this
  in the wiki" (as opposed to "remember this" alone, which means agent memory), or pastes in research,
  meeting notes, an article, or a technical finding and wants it filed somewhere durable. Also trigger
  it proactively when the user has just worked through a non-trivial decision, workaround, or piece of
  research in the conversation and a wiki is configured (an `llm-wiki.yml` exists) — offer to file it
  rather than letting it evaporate at the end of the chat. Sources land in the wiki's `inbox/` (a
  dropzone) and are archived byte-for-byte to `raw/` once distilled. Part of the mm-wiki-* skill family
  (mm-wiki-ingest/query/prune/lint/status/import) targeting Logseq; works from any coding agent or
  chat, not only Claude Code.
metadata:
  version: 1.2.0
---

# mm-wiki-ingest

You are filing knowledge into a Logseq wiki that an agent (possibly a different model, in a different
tool, next week) will later query through `mm-wiki-query`. That agent will only read the 3-5 pages a
hub's index points it to — so the value of everything you do here rides on two things: getting the
content onto the *right* pages, and keeping the routing index honest about what's on them. A well-
written page nobody can find is as useless as no page at all.

This skill runs on a **dropzone-driven cycle**: sources land in the wiki's `inbox/`, you read *only*
`inbox/`, and once a source is fully processed you archive it byte-for-byte into `raw/` (append-only,
never re-read). Nothing gets re-read on a later run — the read-path stays tiny.

Read **`references/wiki-conventions.md`** now if you haven't already this session — it defines the
inbox/raw layout, the Logseq file format, the Hub-Index-Routing scheme, the Access-Log, and the
constraints (never overwrite content, never store credentials, dates in ISO 8601) that every step
below assumes.

## Step 0: Find and Read the Config

Look for `llm-wiki.yml` in the current directory, then walk up parent directories. If you can't find
one, ask the user where their wiki lives (or offer to scaffold a new one — an `inbox/` dir, a
`pages/` dir with a `Wiki___Schema.md` and one hub page is enough to start). Read it to get
`wiki_path`, `pages_dir`, `inbox_dir`, `raw_dir`, and `namespaces`. `inbox_dir`/`raw_dir` default to
`inbox`/`raw` relative to `wiki_path` when absent.

Before doing anything else:

- Ensure `inbox_dir` and `raw_dir` exist — create them if missing (ask first if the wiki looks
  hand-managed and you're unsure).
- If `wiki_path` is a git repo, make sure `.gitignore` covers `inbox/` and `raw/` (raw material can
  contain secrets before filtering). Offer to add the two lines if they're missing.

## Step 1: Route the Source into the Inbox

Everything you ingest goes through `inbox/` first — there is no other entry point. Depending on how
you were invoked:

- **No source given** → list the files in `inbox_dir`. If it's empty, tell the user there's nothing
  to ingest and suggest dropping a file in `inbox/` or pasting content — then stop.
- **Text pasted inline** → save it to `inbox_dir` as `YYYY-MM-DD_<slug>.md`, where `<slug>` comes
  from the topic or first heading (today's ISO date).
- **A URL** → fetch the content and save it to `inbox_dir` as `YYYY-MM-DD_<slug>.md` (slug from the
  title/domain).
- **A local file path** → copy the file(s) into `inbox_dir` **byte-for-byte**, preserving the
  original filename. You only ever read the source, never edit it.

Now process the resulting batch (every file in `inbox_dir`). For each file, **compute its target
`raw/` name up front**: if `raw_dir/<name>` already exists, the archived name becomes
`YYYY-MM-DD_<name>` — so the provenance you write in Step 4 points at the name that will actually
exist after Step 5.

## Step 2: Analyze Each Inbox File

For each file in the batch, read it and extract: entities (people, tools, services), facts,
relationships, dates, decisions and their rationale. Classify each finding into a namespace (Tech,
Projects, Business, People, Learning, Reference, or whatever this wiki's `namespaces` list defines).

**L1/L2 check, before you write anything**: for each finding, ask *"would getting this wrong next
session be dangerous or embarrassing?"* If yes, it belongs in the agent's own memory system (L1), not
the wiki. Tell the user that instead of filing it. Only file findings that are merely inconvenient to
re-derive later — deep knowledge, not standing rules.

## Step 3: Scan the Wiki Before Writing

- Read `Wiki/Schema` (file `Wiki___Schema.md`) for this wiki's page-type conventions, if it exists.
- For each namespace you're about to touch, check whether the target pages already exist (list the
  `pages_dir` and match filenames, or grep for the page name).
- Read the existing content of any page you're about to update — you're appending, not replacing, so
  you need to know what's already there to avoid duplicating a fact that's already recorded.
- Identify: which pages are new, which are updates, which cross-references need adding.

## Step 4: Write the Pages

Target 5-15 page touches per ingest run. Fewer than 5 often means you under-extracted (re-check the
source for findings you skipped); more than 20 usually means you're over-fragmenting — group related
facts onto fewer, richer pages instead of one page per sentence.

Write page content in the **same language as the source material** — do not translate. Only the
structural keys stay in English (property names, page filenames, `[[links]]`), per the conventions
reference.

- **New pages**: include every property the Schema requires for that type (`type::`, `created::`,
  plus type-specific ones — see the conventions reference's Schema table if this wiki has none of its
  own yet). Add a **`source:: raw/<archived-name>`** provenance line (the name computed in Step 1) so
  the page's origin is auditable.
- **Existing pages**: append new facts as new bullet blocks. Never rewrite or delete an existing
  block — if new information contradicts something already there, add a block noting the contradiction
  and today's date, and let a human resolve it later. The user edits this wiki by hand too; silently
  overwriting their edits breaks trust in the whole system.
- **Hub routing line (required for every page you create or meaningfully refocus)**: in the page's
  namespace hub, under `### Index`, add or refresh the line:
  `[[Wiki/NS/Page]] -- <one-sentence description, <=120 chars> #tag #tag`.
  New page → append a line. Existing page whose focus shifted → update the description in place so it
  stays the accurate routing key. Do not touch other pages' routing lines while you're at it.
- **Cross-references**: add `[[links]]` between pages you touched that are actually related — this is
  what makes multi-hop queries and the backlinks panel work. Don't force links that aren't real.
- Set `updated::` (or add `created::` for new pages) with today's ISO date on everything you touch.

## Step 5: Archive Processed Files to raw/

After a file's findings are fully distilled into pages, move it to `raw_dir`:

- Move **byte-for-byte** — you only read the original, never edit it. The move is the **commit
  point**: only genuinely processed sources leave `inbox/`.
- Use the archived name computed in Step 1 (collision → `YYYY-MM-DD_<name>`). Never overwrite an
  existing file in `raw/`.
- **Failed or unclear files stay in `inbox/`** — leave them and report why; they'll be re-read on the
  next run. Don't archive something you weren't able to distill.

## Step 6: Maintain the Ingest-Workflow Doc

Keep the wiki's own copy of this workflow current so the convention survives a change of agent or
session. Ensure a `Wiki/Reference/Ingest-Workflow` page exists (file
`Wiki___Reference___Ingest-Workflow.md`) describing the inbox → raw → pages cycle, the `.gitignore`
rule, collision handling, and `source::` provenance; create it if missing, refresh it if it has
drifted. (If this wiki prefers, a section in `Wiki/Schema` instead.)

## Step 7: Quality Gate — Check Before You Report Done

- [ ] Every new page has the properties its type requires
- [ ] Every new page records its provenance via `source:: raw/<archived-name>`
- [ ] Every page you touched has at least one outgoing `[[cross-reference]]`
- [ ] Every new/updated active page has a routing line in its hub's `### Index` — a page without one
      is unroutable, only findable later by luck via grep
- [ ] No credentials, tokens, or passwords ended up in any page (if you saw one in the source, you
      should have already skipped it and flagged it to the user, per L1/L2 check in Step 2)
- [ ] Page-touch count is in the 5-15 range, or you have a good reason it isn't
- [ ] Every fully-processed source file was archived to `raw/` byte-for-byte; nothing processed was
      left behind in `inbox/`

If `wiki_path` is a git repository, commit the change now (`inbox/` and `raw/` are gitignored, so the
commit carries only pages/hub/workflow-doc changes — skip silently if there's no git repo or your
environment has no git access).

## Step 8: Report

Tell the user: pages created (with names), pages updated (with a one-line summary of what was added to
each), cross-references added, files archived to `raw/` (with names), any files left in `inbox/` and
why, and anything you skipped (credentials, judged-not-worth-filing, or L1 recommendations instead).
