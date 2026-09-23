---
name: mm-wiki-reading-list
description: >
  Pull books from a macOS Reminders list ("Книги") via the mcp-server-apple-events MCP
  server, classify each by genre, generate a deep book-brief conspect from the matching
  Wiki/Prompts/*-Book-Brief template, and file it into mm-wiki through mm-wiki-ingest —
  without the user manually copying the reading list into chat. Use when the user says
  things like "прогони книги из Reminders", "разбери список книг", "какие книги ждут в
  списке", or invokes `/mm-wiki-reading-list`. Three modes: `list` (read-only report),
  `single [title]` (one book, inline, no subagent), `full` (every untagged candidate, one
  sequential subagent per book). Depends on the `apple-events` MCP server being connected
  in the current project, and on the sibling skills mm-wiki-ingest (the only writer into
  the wiki) and mm-wiki-query (duplicate detection) being installed alongside it. Part of
  the mm-wiki-* skill family, targets Logseq; Claude Code only — it needs the Skill and
  Agent tools, so it does not work from an agent-agnostic chat.
argument-hint: "list | single [title] | full [--auto-approve] [--model=sonnet|opus]"
compatibility: >
  macOS with Reminders access granted to the host app; the apple-events MCP server
  (mcp-server-apple-events) connected in the project; sibling skills mm-wiki-ingest and
  mm-wiki-query installed; Claude Code (uses the Skill and Agent tools).
metadata:
  version: 1.0.0
  author: mniedre
---

# mm-wiki-reading-list

You are a thin orchestrator between three systems that each own exactly one thing:
**Reminders** owns what's on the reading list, **the wiki** owns what's already filed and
which prompt belongs to which genre, and **`mm-wiki-ingest`** owns every write into that
wiki. Your own work is only the glue — talk to Reminders, classify a book's genre, generate
the conspect from the matching wiki prompt, hand it to `mm-wiki-ingest`, tag the Reminder
afterwards. Nothing here should re-implement what one of those three already owns: ingest
is the only writer into `pages/`, the book-brief prompts are read live out of the wiki
every run, and the reading list is never cached between runs.

Read **`references/wiki-conventions.md`** now if you haven't already this session — it is
the synced family-wide reference for the Logseq format, the hub-index routing scheme, and
the config file. Read **`references/mcp-apple-events.md`** before the first Reminders call
of a run: it carries the tool schemas this skill uses and the tag caveat referenced in
Step 6.

## Step 0: Preflight (Reminders MCP)

1. `reminders_lists` `action: read`. If the tool isn't callable at all, tell the user the
   `apple-events` MCP server isn't connected in this project and stop — never fabricate a
   book list.
2. On a permission error, pass on the fix from `references/mcp-apple-events.md` (grant
   Reminders access in System Settings → Privacy & Security → Reminders, for whichever
   process launches the MCP server) and retry.
3. Confirm **"Книги"** is among the returned list names. If it isn't, show the names you
   actually got and stop — a typo'd list name must never be silently read as "zero
   candidates".

## Step 1: Wiki config

Find and read `llm-wiki.yml` the same way every other family skill does (see
`references/wiki-conventions.md` §Configuration) for `wiki_path` and `pages_dir`. Read
`inbox_dir` too (default `inbox`, relative to `wiki_path`): that's where conspects are
staged, and it's the only path this skill ever writes to. Moving a staged source into
`raw_dir` is `mm-wiki-ingest`'s archiving step and its commit point — not yours.

## Step 2: Discover book-brief prompts by tag

Grep `Wiki___Prompts___*.md` for a `tags::` line carrying all three of `#KB`, `#Books`,
`#mm-wiki` on the same line. Each match is one available category, and this grep is the
**only** source of truth for which prompts exist: don't hardcode page names, don't
special-case any page in your own logic. A new category is just a new `Wiki/Prompts/<X>`
page with that tag triple; nothing here has to change when one appears. As of 2026-09-23
this resolves to two pages — [references/role-prompts.md](references/role-prompts.md)
explains the criteria behind them in human-readable form, which documents the *criteria*,
not the mechanism.

Never copy a prompt body into this skill's files: read the `Wiki/Prompts/<X>` page's code
block fresh every time you generate, so a later edit to the wiki prompt is picked up
without touching the skill.

## Step 3: Read the list

`reminders_tasks` `action: read`, `filterList: "Книги"`, `showCompleted: true`. Include
completed reminders deliberately: `completed` records whether the *user* has finished
reading the book, which has nothing to do with whether it was ever filed in the wiki.
Split what comes back into:

- **tagged** — `tags` includes `KB` (case-insensitive) → already filed, ignore. A run that
  wants to be cheap can ask the server for the same thing with `filterTags: ["KB"]`.
- **candidates** — everything else.

Keep each candidate's `note` alongside its `title`: Reminders has no author field, so the
author — and any book quotes the user wanted preserved — live in that free-form note. Step
4 parses them out. Also collect the topic tags already in use across this list's items;
that existing vocabulary is what Step 4 reuses instead of inventing synonyms each run.

## Step 4: Identify, extract, and classify each candidate

One **haiku** call per candidate — cheap, and none of this needs a deeper model.
(Evaluated and rejected an external typed-classification API for this: a paid service plus
a Python SDK is disproportionate for two categories that a plain prompt already handles;
revisit only if the category list grows large enough that prompt-based classification
stops being reliable.)

Give it the raw `title` and `note` (there is no separate author field — whatever the user
typed is all there is) and ask for, structured:

- **Identification** — does this clearly name a real, recognizable book? If it's genuinely
  unclear (garbled, too vague, could be several different books), flag `unidentified` and
  stop here for this candidate: report "не удалось идентифицировать книгу". Never guess at
  an identity you aren't confident of.
- **Canonical title** (as best understood) and **author**, when the note states one.
  Authors are often absent — don't invent one when it's missing, and prefer a note-stated
  author over your own guess when both exist, since the user's note is the better signal
  for which edition or book they mean.
- **Quotes** — any passage in `note` that reads as an excerpt from the book itself, not a
  task comment like "дочитать до пятницы" — extracted **verbatim**, never paraphrased.
  Most candidates have none; that's normal, not an error.
- **Category** — exactly one match from the Step 2 list (page name plus the scope
  description on that page), or `unsure` when nothing fits confidently. Never force a fit;
  report "нужен новый промпт для категории".
- **Topic tags** — 1-3 short lowercase tags (hyphenated if multi-word), decided **once,
  here**. Reuse the vocabulary collected in Step 3 wherever it genuinely fits; invent a new
  tag only when nothing existing applies. This exact list is the single source of truth for
  both the Reminder's tags and the `tags::` line on the resulting `Wiki/Books` overview
  page — the two must never diverge, so nothing downstream re-derives or re-invents them.

Both skip reasons (`unidentified`, `unsure` category) behave the same way downstream:
`list`/`single` surface the reason, and `full` drops the book from the batch and lists it
separately in the final report as a hand-off — the user either clarifies the Reminder or
writes a new `Wiki/Prompts/<X>-Book-Brief` page tagged `#KB #Books #mm-wiki`. Guessing
past either reason is never the answer.

Carry the extracted title/author/quotes/topic tags forward to Steps 5 and 6.

## Step 5: Duplicate check

For each classified candidate, ask `mm-wiki-query` (via the `Skill` tool) something like
"есть ли в вики конспект книги `<canonical title from Step 4>` (`<author, если найден>`)?" —
deliberately not a raw grep against `Wiki___Books.md`. Title forms vary too much for exact
match (`"Bullshit Jobs"` in a Reminder vs `Wiki/Books/Bullshit-Jobs` vs
`«Дэвид Грэбер "Bullshit Jobs"»` in a note), and `mm-wiki-query`'s hub-routed search
handles that variance where a substring grep does not.

- **Confident match** → the book is already filed but its Reminder was never tagged
  (drift). Regenerating would duplicate the conspect: go straight to Step 6 for the tagging
  only, and report it as "skipped — already existed, tag restored", never as "processed".
- **Ambiguous** → don't guess in either direction. Mark "похоже на существующую
  [[Wiki/Books/X]], нужна ручная проверка", exclude it from the `full` batch, and leave it
  reachable only through an explicit `single <title>` where the user pointed at it.
- **No match** → genuinely new. Proceed to Step 6.

## Step 6: Generate + ingest (per book)

For every book that reached this step (new, not a duplicate, with a resolved category):

1. Read the matching `Wiki/Prompts/<X>` page's code-block template in full.
2. Fill it from your own knowledge of the book. There is no pasted source text — this is
   memory reconstruction, same as the existing precedents in `Wiki/Books`:
   `confidence:: medium`, the overview page's first section is "Статус конспекта —
   реконструкция по памяти", and no quote or page number is ever invented. Write the
   conspect **in Russian, always**, whatever language the book was written in — every other
   page in `Wiki/Books` does this (Ledin, Дао дэ цзин, Bullshit Jobs, …).
   - **Author** — a Step 4 author is definitive; don't second-guess it against your own
     knowledge. If Step 4 found none, use your own knowledge when confident, otherwise
     leave the author unstated rather than guessing.
   - **Quotes** — the ones extracted in Step 4 are the one exception to "quotes stay
     empty" in reconstruction mode, because they are real and user-supplied rather than
     reconstructed. Put them in "Ключевые цитаты" verbatim, sourced honestly as
     `> «<quote>» — источник: заметка в Reminder (страница неизвестна)`, never with a
     fabricated page number. Quotes the note didn't provide still stay `—`.
   - **Tags** — the overview page's tags line must include the Step 4 topic tags verbatim:
     same words, same set, not re-derived from the generated content. Add them alongside
     whatever other topical `#tags` the page would naturally carry per the `Wiki/Books`
     convention — plain `#tag` words; book pages do **not** carry the `#KB #Books
     #mm-wiki` triple, which belongs to `Wiki/Prompts` meta-pages.
3. Do **not** compress. A book is several linked pages in `Wiki/Books` (overview + 4-7
   thematic sub-pages + an author entity page when useful), the same shape as the existing
   Pareto/Ledin conspects. This was a hard lesson from the first Pareto attempt in this
   project: a compressed single-page conspect got rejected outright.
4. Save the full conspect to `<inbox_dir>/YYYY-MM-DD_<slug>.md`.
5. Hand it to `mm-wiki-ingest` (via the `Skill` tool) and let it run its own full pipeline —
   inbox → pages → raw, quality gate, git commit. Never write into `pages/` yourself, even
   when ingest seems slow; retrying ingest is always the answer, working around it never is.
6. Only once ingest has committed: tag the Reminder (`reminders_tasks` `action: update`,
   `addTags: ["KB", "books", ...topics]`, where `topics` is exactly the Step 4 list). As
   `references/mcp-apple-events.md` explains, this writes `[#tag]` markers into the
   Reminder's `note` rather than a real Apple Reminders tag chip — a limitation of the MCP
   server, not something to work around. It's still enough for `filterTags` and the Step 3
   dedup to work.

**Retry budget** (the `Agent` tool exposes no `max_tokens`/`max_retries`, so this is an
explicit behavioural instruction rather than an SDK setting): on a failed write — either
`mm-wiki-ingest` or the Reminders tag update — retry at most twice. Still failing: stop
that book, report the exact error, move on. Never fall back to writing pages directly, and
never silently skip the tag.

## Modes

### `list`

Run Steps 0-5 (identification, extraction, classification and dup-check included, so the
report is accurate) but **write nothing** — no wiki pages, no Reminder tags. Report: total
books, how many already tagged, how many real candidates (with inferred category, topic
tags, and author/quotes where the note had them), how many couldn't be identified, how many
need a new category prompt, and how many are ambiguous duplicates awaiting manual review.

### `single [title]`

One book, with Step 6 running **inline in this conversation, no subagent** — that's the
point of `single`: a cheap, visible path for testing one book or self-healing a drift case.
Selection: no `title` argument → the first untagged candidate in list order; with a `title`
→ substring-match against `title`/`note`. Without `--auto-approve`, show the resolved book,
its category, and the plan, then wait for confirmation before writing. With
`--auto-approve`, go straight to Step 6.

### `full`

Every untagged, classified, non-ambiguous candidate, with Step 6 running **inside one
separate `Agent` call per book** — `subagent_type: general-purpose`, which needs
unrestricted tool access to read the prompt page, write `<inbox_dir>/`, call `Skill`, and
call `reminders_tasks` — model per the table below.

**Strictly sequential: one book at a time, never batched.** Call `Agent`, wait for its
result, then call the next one. Never put two `Agent` calls in one message (that is the
tool's only mechanism for parallelism): several subagents committing to the same wiki git
repo, or writing tags to the same Reminders list, concurrently is a real corruption risk,
not a hypothetical one. Each book therefore lands as its own `mm-wiki-ingest` commit —
`full` on N books is N commits, which is intentional (atomic and revertible per book) but
worth stating in the final report so a run of commits isn't a surprise.

Without `--auto-approve`, show the whole candidate list once and get a single confirmation
for the batch (not per book — that would defeat the point of `full`). With
`--auto-approve`, go straight through.

**Subagent prompt template** (fill the placeholders per book):

```
Process one book for mm-wiki. Book: "<title>" (Reminder note: "<note>"). Identified as:
"<canonical title>" by <author, or "unknown"> — taken from the Reminder note when the note
stated it, so treat it as definitive and don't second-guess it. Category: <category> → read
the full code-block template at Wiki/Prompts/<X> and follow it without shortening it.

Quotes found in the note (verbatim, already extracted): <quotes list, or "none">. If any are
listed they are real and user-supplied, and they MUST appear verbatim in the "Ключевые
цитаты" section of the final article, sourced as `источник: заметка в Reminder (страница
неизвестна)` — never with a fabricated page number. This is the one exception to "don't
invent quotes": these were not invented, they came from the user's own note.

No real book text beyond those quotes is available — work in memory-reconstruction mode for
everything else: confidence:: medium, and the overview page's first section is "Статус
конспекта — реконструкция по памяти" (Pareto-Elite-Theory / Modern-Computer-Architecture in
Wiki/Books are the precedent). Never invent quotes beyond the ones listed above, and never
invent page numbers.

Write the conspect in Russian, always — regardless of the book's original language.

Do not compress it into one page. A book is several linked pages in Wiki/Books (overview +
4-7 thematic sub-pages), the same shape as the existing Wiki/Books examples — look at a
couple of them before writing.

Topic tags (already decided upstream, do not re-derive): <topic tags list>. These exact
words, lowercase/hyphenated, MUST appear verbatim in the overview page's tags line
(alongside whatever other topical #tags the page naturally carries per the Wiki/Books
convention — plain #tag words, not the #KB #Books #mm-wiki triple, which belongs to
Wiki/Prompts meta-pages) AND unchanged in the Reminder's addTags call in step 4. The wiki
page and the Reminder must end up with the same topic tag words — that is the whole point of
deciding them once, upstream.

Budget: at most 2 retries on a failed write (mm-wiki-ingest or the Reminders tag update).
After 2 failures, stop — do not write into pages/ directly as a workaround — and report the
exact error instead.

Steps: 1) generate the full conspect → 2) save it to <inbox_dir>/YYYY-MM-DD_<slug>.md →
3) Skill(skill:"mm-wiki-ingest") and let it run its full pipeline → 4) only once that
commits successfully, reminders_tasks update addTags:["KB","books",...topics] on Reminder id
<id> → 5) report back: pages created, tags applied, any problems.
```

## Model per step

| Step | Model | Why |
|---|---|---|
| Classification (Step 4) | `haiku` | cheap, simple closed-set task |
| Generation + ingest (Step 6) | `sonnet` default, `--model=opus` override | the actual content work — the tier used for the existing conspects in this wiki |
| Tagging Reminders | no model — a direct MCP call | not a generative step |

## What this skill deliberately does not do

- **Does not write into `pages/`** — `mm-wiki-ingest` is the only writer, and retrying it
  is always preferable to going around it.
- **Does not move staged files into `raw_dir`** — that archiving step is `mm-wiki-ingest`'s
  commit point.
- **Does not keep a copy of the book-brief prompts** — they're read live from
  `Wiki/Prompts/<X>`, discovered by tag, so an edit to a wiki prompt needs no change here.
- **Does not mark Reminders `completed`** — tagging only, by explicit user decision;
  `completed` stays whatever the user's own reading status says.
- **Does not batch `Agent` calls** for speed in `full` — sequential only, see the mode
  section for why.

## Report (end of any run)

Books processed, with the `Wiki/Books` pages created and whether author/quotes were carried
over from the Reminder note. Books skipped and why — the four distinct reasons, never
collapsed into one generic "skipped":

1. already tagged (nothing to do);
2. duplicate found via `mm-wiki-query` and self-healed (tag restored, not regenerated);
3. could not be identified, or identification was in doubt (never guessed through);
4. identified but no matching category prompt (genre needs a new
   `Wiki/Prompts/<X>-Book-Brief`).

Plus: tags applied per book, any book that failed after its retry budget (with the exact
error), and — for `full` — the reminder that each book landed as its own git commit.
