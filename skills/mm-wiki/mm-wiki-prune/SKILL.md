---
name: mm-wiki-prune
description: >
  Run LRU-Demote on a Logseq wiki: evict pages nobody has queried in N months (default 6) from their
  hub's live `### Index` into `### Archive`, keeping the routing index sharp as the wiki grows. Use
  this when the user says "prune the wiki", "clean up the wiki index", "run wiki maintenance", asks
  why wiki queries feel slow or noisy, or on a periodic schedule they've set up. This never deletes a
  page or breaks a [[link]] — the file stays exactly where it is; only its routing line moves.
  Always show the demotion candidate list and get confirmation before writing anything. Part of the
  mm-wiki-* skill family, targets Logseq, works from any coding agent or chat.
metadata:
  version: 1.0.0
---

# mm-wiki-prune

The hub index only stays useful as a routing table if it stays small and current. Every page that gets
added and never gets demoted is dead weight `mm-wiki-query`'s routing pass has to consider on every
question. This is the maintenance job that keeps that from happening — think of it as evicting a cold
line from a cache, not deleting data. The file survives, every `[[link]]` to it keeps working, and it's
still findable via the L3 grep fallback — it just stops being a routing candidate.

Read **`references/wiki-conventions.md`** first if you haven't this session.

This is meant to run periodically (default: every 6 months) — it does not self-schedule. If the user
wants it recurring, that's a job for whatever scheduling mechanism their environment offers (a cron
skill, a calendar reminder) — not something this skill sets up itself.

## Step 0: Config and Scan

Read `llm-wiki.yml` for `wiki_path`/`pages_dir`. If Python 3 is available in your environment, run:

```bash
python3 scripts/wiki_scan.py <pages_dir> --access-log <pages_dir>/Wiki___Reference___Access-Log.md
```

(path is relative to this skill's own directory — adjust if your environment invokes it from
elsewhere)

This gives you every page's properties and the parsed Access-Log in one JSON report — use it instead
of manually grepping dates out of every page. If Python isn't available, do the equivalent by reading
`Wiki/Reference/Access-Log` directly and each candidate page's properties.

## Step 1: Build the Access Profile

For each page, find its most recent Access-Log entry. If a page has never been logged, use its
`created::` date as a stand-in for "last touched."

Threshold: no access in **N months** (default 6; the user may override with `--months N` or by just
saying a different number).

**Exempt from demotion, regardless of age:**
- Hub pages (`type:: hub`)
- `Wiki/Schema`, `Wiki/Dashboard`, `Wiki/Reference/Access-Log` itself
- Any page with `status:: active` (in-flight projects — never evict work still underway just because
  nobody's queried it recently)

## Step 2: Propose Candidates — Do Not Write Yet

List every candidate as `page -- last access -- age in months` and show it to the user. Wait for
confirmation (explicit "yes"/"go ahead", or the user editing the list) before touching any file. This
step is the whole safety net for a bulk structural edit — don't skip it even if the user asked you to
"just run prune."

## Step 3: Demote Confirmed Candidates

For each page the user confirmed:

1. Set `archived:: <today, ISO date>` on the page. This is the canonical "demoted" marker and is valid
   on any page type. **Never touch `created::` or `updated::`** — those describe the content, not the
   routing state.
2. If the page is an `entity` type (its `status::` enum includes `archived`), also set
   `status:: archived`. For `project`/`knowledge` pages, set `archived::` **only** — do not invent an
   out-of-enum `status::` value; check `Wiki/Schema` for the actual enum if unsure.
3. Move the page's routing line **verbatim** from its hub's `### Index` into that hub's `### Archive`
   section. Move, don't delete — someone querying via L3 grep, or re-promoting later, needs the
   description still there.
4. **Do not rename the page or move the file to a different namespace.** Logseq links by page name; a
   rename breaks every incoming `[[link]]` across the graph. The file stays exactly where it is —
   demotion is a routing-index change, nothing else.

## Step 4: Report and Commit

Report: pages demoted, the new live-index size per namespace (before/after), and a few hot pages (most
recently/frequently accessed) for contrast so the user sees what's staying.

If `wiki_path` is a git repo, commit now — this is a structural change (hub indexes + page
properties), unlike the Access-Log appends that ride along with other commits. Skip silently if there's
no git repo available.

Note when the next prune is due (today + N months) — mention it, but don't try to schedule it yourself
unless the user explicitly asks and your environment has a way to do that.
