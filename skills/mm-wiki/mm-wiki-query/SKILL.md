---
name: mm-wiki-query
description: >
  Answer a question by searching a Logseq wiki configured via `llm-wiki.yml`, using a cheap two-stage
  routing pass (hub indexes first, full pages only for the top 3-5 matches) instead of reading every
  page. Use this whenever the user asks something like "what do I know about X", "check the wiki for
  Y", "have we dealt with this before", "what's our stance on Z", or any question where the answer
  might already be recorded rather than something to figure out fresh. Also use it for multi-hop
  questions — "how is X connected to Y", "what does X depend on" — answered by walking [[links]]
  across pages. This skill is READ-ONLY: it never creates or edits wiki pages except a single
  append-only line to the Access-Log; if the user wants something written to the wiki, route them to
  mm-wiki-ingest instead. Part of the mm-wiki-* skill family, targets Logseq, works from any coding
  agent or chat.
metadata:
  version: 1.0.0
---

# mm-wiki-query

You're answering a question against a wiki that was deliberately built so you *don't* have to read
every page to answer it. The hub `### Index` sections are a routing table — read those first (cheap),
and only open the handful of full pages the index actually points you to (expensive). Reading every
page "to be thorough" defeats the entire point of the architecture and will not scale as the wiki
grows — resist the urge.

Read **`references/wiki-conventions.md`** now if you haven't already this session.

## This skill is read-only

The only write this skill ever makes is the single Access-Log append in Step 3. Never create or edit
any other page, even when the answer to the question is obviously "someone should update the wiki with
this." Answer the question, then **propose** the update and point the user at `mm-wiki-ingest` — don't
do it yourself here.

## Step 0: Config

Find and read `llm-wiki.yml` (current directory, then parents). Get `wiki_path`, `pages_dir`,
`namespaces`.

## Step 1: Classify the Question

- **Factual lookup** — "what is X" → find the page(s) about X
- **Relationship** — "how does X relate to Y" → find both pages and any typed edges/cross-refs between
  them
- **Multi-hop / path** — "how is X connected to Y", "what does X depend on transitively" → X and Y
  probably don't link directly; you'll need to walk through intermediate pages via `[[links]]`
- **Synthesis** — "what's our current thinking on X" → gather everything touching X, combine it
- **Gap** — "what don't we know about X" → look for what's missing / open questions

## Step 2: Routing Pass (Stage 1 — cheap)

Do not open content pages yet.

1. From the question, guess which namespace(s) are relevant (Tech, Projects, Business, People,
   Learning, Reference, or whatever this wiki's `namespaces` are).
2. Read **only the hub page** for each candidate namespace — just the `### Index` list, not any
   content pages.
3. Match the question against the routing lines (`[[link]] -- description #tags`). Pick the **3
   most relevant** child pages (5 max). This is the whole point of the hub index — a page table, not a
   full scan.

**L3 fallback** — use this only when routing genuinely comes up empty: namespace unclear, hub index
missing or empty, nothing in it matches. Then, and only then, grep across all pages in `pages_dir` for
the question's key terms and take the top 3-5 hits. This is the slow path; it should be the exception.

## Step 3: Targeted Read (Stage 2) + Access Logging

Open the 3-5 pages chosen above (batch the reads; load at most 3 at once if your environment charges
per-file-in-context). For each page **actually read in full**, append one line to
`Wiki/Reference/Access-Log` (file `Wiki___Reference___Access-Log.md`):

```
- <today, ISO date> -- [[Wiki/NS/Page]] -- query -- matched: "<reason, <=60 chars, quoted>"
```

`matched:` = the hub-index description/tag that pointed you here (routing pass) or the grep term that
found it (L3 fallback). This is what makes the routing auditable later via `mm-wiki-status`.

Do not log the hub-index reads from Step 2, only full pages you actually opened. Don't create a
version-control commit for this append — it's non-structural, let it ride along with the next
ingest/lint/prune commit.

**Re-hit on an archived page**: if the L3 fallback surfaces a page with `archived::` set, that's a
signal it's still useful — offer to re-promote it (move its routing line from `### Archive` back into
`### Index`, drop `archived::`). Don't do it silently; ask first, since it's a structural wiki edit.

## Step 4: Synthesize

Combine what the pages say. Note each page's `confidence::` if it has one, and flag anything whose
`updated::` date is old relative to how fast the topic changes. If pages disagree, say so rather than
picking one silently.

## Step 5: Answer

- Give the answer with source attribution: `Sources: [[Wiki/Tech/Deployment]], [[Wiki/Reference/Gotchas]]`
- Flag any stale or low-confidence source you relied on
- If the question exposed a real gap in the wiki (nothing found, or what's there is thin/contradictory),
  say so and offer — don't just do it — to file it via `mm-wiki-ingest`
- Suggest related pages if the hub index surfaced any near-misses worth mentioning
