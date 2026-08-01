---
name: mm-wiki-lint
description: >
  Run a structural health check on a Logseq wiki: orphan pages, stale content, broken [[links]],
  missing required properties, index drift (routing lines pointing nowhere, or active pages with no
  routing line at all), credential leaks, and empty pages. Use when the user says "lint the wiki",
  "check wiki health", "is the wiki in good shape", or after a big mm-wiki-ingest/import run to catch
  problems before they compound. Reports findings by severity; only writes to files when the user adds
  `--fix`. Part of the mm-wiki-* skill family, targets Logseq, works from any coding agent or chat.
metadata:
  version: 1.0.0
---

# mm-wiki-lint

You're checking whether the wiki's structure still supports `mm-wiki-query`'s two-stage routing —
that's the lens for every rule below. A broken `[[link]]` is bad because a human clicking it hits a
dead end; an unroutable page is worse, because no amount of clicking finds it at all, and neither does
the routing pass. Read **`references/wiki-conventions.md`** first if you haven't this session.

## Step 1: Scan

Read `llm-wiki.yml` for `wiki_path`/`pages_dir`. If Python 3 is available:

```bash
python3 scripts/wiki_scan.py <pages_dir> --access-log <pages_dir>/Wiki___Reference___Access-Log.md
```

This one JSON report already computes most of the checks below (broken refs, orphans, index drift,
credential hits, empty pages, no-outgoing-link pages) — use it instead of re-deriving them by hand. If
Python isn't available in your environment, read each page and check manually against the rules
below; it's slower but the rules are the same.

## Step 2: Check Rules

- **Orphan** — a page with zero incoming `[[links]]`, excluding hubs and the Access-Log (which are
  exempt by design).
- **Stale** — `updated::` more than 90 days ago *and* `confidence:: high`. High confidence claiming to
  be current but untouched for three months is the specific combination worth flagging — old-and-
  already-marked-stale isn't new information.
- **Missing properties** — a page missing a property its `type::` requires (check `Wiki/Schema` if it
  exists; otherwise the fallback table in the conventions reference).
- **Broken references** — a `[[link]]` pointing to a page that doesn't exist as a file.
- **Hub completeness** — a hub whose namespace clearly has pages (by filename prefix) not reflected in
  either its `### Index` or `### Archive`.
- **Index drift** — two shapes: (a) a routing line in some hub's `### Index` pointing to a page that
  no longer exists (orphaned line — the page was deleted or renamed without cleaning up the hub), or
  (b) an active, non-archived page with **no** routing line in any hub at all (unroutable — only
  findable by luck via L3 grep).
- **Missing index description** — a routing line with nothing after the `--` separator. A blank
  description can't be matched against during routing, so the line is dead weight even though it looks
  present.
- **Archived-in-live-index** — a page with `archived::` set whose routing line is still sitting in
  `### Index` instead of `### Archive` (a prune that didn't finish cleanly).
- **Credential leak** — regex scan for token/password/API-key/private-key patterns. Treat any hit as
  urgent regardless of how the rest of the lint report looks.
- **Empty pages** — a page with properties but no actual content blocks.
- **Cross-ref minimum** — a page (excluding hubs, Access-Log) with zero outgoing `[[links]]`. Not
  necessarily wrong, but worth a second look — most real pages relate to something.
- **L1/L2 duplicate** — if `memory_path` is set in `llm-wiki.yml`, spot-check whether something in
  agent memory (L1) duplicates something in the wiki (L2). This one's a judgment call, not a script
  output — flag as a warning, not a hard finding.

## Step 3: Report

Group findings by severity:
- **Critical**: credential leaks
- **Warning**: broken refs, index drift, missing required properties, archived-in-live-index
- **Info**: orphans, stale, missing descriptions, empty pages, cross-ref minimum, L1/L2 duplicates

For each finding give the page name, the issue, and a one-line suggested fix. Include counts: total
pages, pages with zero issues, issues found by category.

## Step 4: Auto-Fix (only when the user passes `--fix`)

Without `--fix`, stop after the report — do not modify anything.

With `--fix`, apply only the mechanical fixes below (nothing that requires judgment — leave those as
report items for the user to act on):

- Backfill a missing routing line: for an active page with no index entry, generate
  `[[Wiki/NS/Page]] -- <description> #tags` from the page title, its first content block (as the
  description), and its own `#tags`, and insert it into the correct hub's `### Index`.
- Clean index drift: remove routing lines pointing to pages that no longer exist; move
  archived-in-live-index entries from `### Index` to `### Archive`.
- Downgrade `confidence:: high` to `confidence:: stale` on pages flagged stale.
- Create minimal stub pages for broken `[[links]]` (properties only, `type:: knowledge`,
  `confidence:: stale`, a one-line note that this is a stub) rather than leaving a dead link — cheap
  and lets a human fill it in later.
- Add cross-references only where the connection is unambiguous from content already on both pages
  (e.g., page A already prose-mentions page B by name) — don't invent relationships.

Do **not** auto-fix: missing required properties (the value depends on facts you don't have), empty
pages (deleting or filling them requires judgment), credential leaks (redacting requires knowing what
replaces the secret — flag for the user to handle by hand).

If `wiki_path` is a git repo, commit after applying fixes. List exactly what changed.

## Step 5: Dashboard

If `Wiki/Dashboard` exists, update it with the current health metrics and timestamp this lint run. If
it doesn't exist, mention to the user that creating one would give them a running view of wiki health —
don't create it unprompted.
