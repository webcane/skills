---
name: mm-wiki-status
description: >
  Give a metrics and health overview of a Logseq wiki: page counts by namespace/type, a lightweight
  health check, and a hot/cold access profile (which pages get queried a lot, which are demote-ready).
  Use when the user asks "how's the wiki doing", "wiki status", "give me a wiki dashboard", "what's in
  the wiki", or wants a sense of scale/activity before deciding whether to run mm-wiki-prune or
  mm-wiki-lint. Read-only — makes no changes. Part of the mm-wiki-* skill family, targets Logseq,
  works from any coding agent or chat.
metadata:
  version: 1.0.0
---

# mm-wiki-status

A dashboard view, not an action. Read **`references/wiki-conventions.md`** first if you haven't this
session.

## Step 1: Metrics

Read `llm-wiki.yml` for `wiki_path`/`pages_dir`, then run the scan (if Python 3 is available):

```bash
python3 scripts/wiki_scan.py <pages_dir> --access-log <pages_dir>/Wiki___Reference___Access-Log.md
```

(path is relative to this skill's own directory — adjust if invoked from elsewhere). If Python isn't
available, list pages directly and read properties by hand.

From the report, compute:
- Total page count, broken down by namespace (filename prefix before the first `___`) and by `type::`
  (hub / entity / project / knowledge / reference)
- Oldest and newest `updated::` dates
- Total `[[cross-reference]]` count (sum of unique outgoing links across all pages)

## Step 2: Health (lightweight)

Run the same checks `mm-wiki-lint` does, but report-only — no `--fix`, no file writes, ever, in this
skill. Report just the counts: orphans, stale pages, broken refs, index-drift entries. If the user
wants the detailed per-page findings, tell them to run `mm-wiki-lint` — don't duplicate its full output
here.

## Step 3: Cache Profile

From the parsed Access-Log entries in the scan report:

- **Hot pages** — top 5 most-accessed in the last 30 days
- **Cold pages** — active (non-archived, non-exempt) pages with no access in the prune threshold
  window (default 6 months) — these are demote-ready; mention that `mm-wiki-prune` would pick them up
- **Live vs. archived index size per namespace** — count of `### Index` entries vs. `### Archive`
  entries per hub
- **Last prune run** — the newest `archived::` date found across all pages; if the cold-page count is
  high relative to total pages, recommend running `mm-wiki-prune`
- **Routing transparency** — from recent Access-Log `matched:` reasons, note if any hot page is
  consistently hit via the same grep term rather than its hub-index description. That's a signal the
  page's routing description is weak or missing — worth fixing via a re-`mm-wiki-ingest` pass on that
  page's routing line, not something this skill edits itself.

## Step 4: Activity

If `wiki_path` is a git repository, check `git log` for wiki changes in the last 7 and last 30 days,
and the most recently updated pages. If there's no git repo, skip this section rather than guessing.

## Step 5: Output

A formatted overview: metrics, health summary, cache profile, recent activity. If `Wiki/Dashboard`
exists and has a previous run's numbers recorded, note deltas (page count change, new orphans, etc.)
— otherwise just report current state.
