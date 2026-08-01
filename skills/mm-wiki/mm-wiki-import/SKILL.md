---
name: mm-wiki-import
description: >
  Bulk-import existing markdown notes into a Logseq wiki's Hub-Index-Routing format — including a
  Slab knowledge-base export (Slab's "Export to Markdown" produces a folder of .md files plus an
  assets/images folder). Use this when the user says "import my notes into the wiki", "migrate our
  Slab docs to the wiki", "bring in this folder of markdown files", or points at an export folder from
  Slab, Notion, Confluence, or a plain notes directory and wants it folded into the existing wiki
  structure with proper page properties, hub routing, and cross-references. Different from
  mm-wiki-ingest: ingest distills a single piece of source material into a few pages; import converts
  a whole pre-existing folder of already-written articles in bulk. Part of the mm-wiki-* skill family,
  targets Logseq, works from any coding agent or chat.
metadata:
  version: 1.0.0
---

# mm-wiki-import

Bulk conversion, not distillation — unlike `mm-wiki-ingest`, you're not deciding what's worth keeping,
you're carrying over content someone already wrote and organized elsewhere, and turning it into pages
that fit the wiki's Hub-Index-Routing scheme so they're actually findable afterward. Read
**`references/wiki-conventions.md`** first if you haven't this session — this skill produces the same
Logseq format ingest and query rely on.

## Step 1: Inventory the Source

Scan the source directory for markdown files. Classify what you're looking at:

- **Slab export** — a folder of `.md` files (Slab's "Export to Markdown" feature), usually with an
  `assets/` or `images/` subfolder for embedded images, and internal links either as relative paths to
  other exported files or as full Slab URLs. Slab exports typically have **no** YAML frontmatter — the
  title is just the first `# H1` line of the file. Nested Slab topics/collections may show up as a
  folder hierarchy; flatten that hierarchy into the namespace path.
- **Notion/Confluence export** — similar shape, but usually does carry frontmatter or an index/TOC file
  worth reading first for the intended structure.
- **Plain notes folder** — no particular export tool's fingerprint; treat each file as its own unit.

For each file, note: title, apparent topic/namespace, any internal links to other files in the same
export, any images it embeds. Propose a namespace mapping (which top-level namespace each file's
content belongs under) and show it to the user before converting anything — get this wrong and every
page lands in the wrong hub.

## Step 2: Slab-Specific Conversion Notes

If the source is a Slab export, handle these before generic conversion:

- **Title**: take it from the first `# Heading` line (Slab doesn't emit frontmatter); use it as both
  the page name and the `## Heading` that becomes the top content block.
- **Internal links**: Slab's exported links are either relative file paths (`[text](./other-doc.md)`
  or `[text](../folder/other-doc.md)`) or full `https://<team>.slab.com/posts/...` URLs. Resolve both
  forms by matching against the file being imported in the same batch (by filename or by matching the
  link text against another doc's title) and rewrite as `[[Wiki/NS/Page]]`. A link Slab exported that
  points to a doc **not** in this batch can't be resolved — leave it as a plain markdown link and note
  it in the Step 4 report rather than guessing.
- **Images**: Slab exports images into a sibling `assets/`/`images/` folder with generated filenames.
  Copy each referenced image into this wiki's own asset location (check `llm-wiki.yml` or
  `wiki_path/assets/` by convention) and rewrite the reference to point there — don't leave pages
  pointing at a source folder that won't exist once the import is done.
- **Callouts/embeds**: Slab markdown callouts (`> 📌 Note: ...`-style blockquotes) and embeds convert
  fine as plain Logseq blocks/blockquotes — no special handling needed beyond the outliner-format
  conversion in Step 3.
- **Slab metadata Slab doesn't export** (author, last-edited date, doc owner) isn't recoverable from
  the markdown export alone. If the user has it from elsewhere (a CSV export, Slab's admin panel), ask
  for it before assuming `created::`/`updated::` — otherwise fall back to the file's own mtime with a
  note that the date is approximate.

## Step 3: Convert to Wiki Format

For every file being imported, regardless of source:

- Reformat into Logseq outliner style: every content line becomes a `- ` bullet; nested structure
  (subheadings, sub-lists) becomes indented bullets.
- Add required properties per the Schema (`type::`, `created::`, `updated::`, plus a `source::`
  property recording where this page came from, e.g. `source:: slab-export`, since imported content
  has different provenance than something an agent distilled).
- Rewrite internal links to `[[Wiki/...]]` cross-references (per Step 2 for Slab; analogous resolution
  for other sources — match against other files in the same import batch).
- Rename the file to the wiki's convention: `Wiki___<NS>___<Page>.md`.

## Step 4: Create Pages

1. **Hub pages first** — ensure every namespace you're importing into has a hub page (`type:: hub`)
   with `### Index` / `### Archive` sections; create one if it doesn't exist yet.
2. **Content pages** — write the converted files into `pages_dir`.
3. **Update hubs** — add a routing line for every imported page to its hub's `### Index`:
   `[[Wiki/NS/Page]] -- <description> #tags`. Write a real, distinctive description per page — don't
   default to "Imported from Slab" for every line, that defeats routing entirely. Base it on the page's
   actual content, the same way `mm-wiki-ingest` would.

## Step 5: Verify

Run `mm-wiki-lint` (or perform the same checks manually if that skill isn't available in your
environment) against the newly-imported pages specifically: broken refs (especially unresolved Slab
links from Step 2), missing properties, index drift. Report: pages imported, issues found, unresolved
links that need a human to sort out. If `wiki_path` is a git repo, commit with a summary message
listing the import source and page count.
