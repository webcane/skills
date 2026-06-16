# playing-deck — Roadmap

`playing-deck` is a planned skill that builds on `playing-card-prompt`'s output to
produce a fully assembled deck: per-card images (via an image-gen tool/MCP),
SVG card structure (frame, index, suit symbols), composited final card files,
and the full deck.

Two architectural roadmaps were explored. They are evaluated sequentially —
Roadmap 1 first, Roadmap 2 to follow.

---

## Human-in-the-loop policy (applies to both roadmaps)

Card generation is not a fire-and-forget pipeline. The image-gen model
is non-deterministic and the prompt is complex; the first result will
often be close but not right. **HITL is mandatory at two moments:**

1. **Golden-card gate (before the deck loop starts):** Generate one card,
   show it to the user, and get explicit approval. If the result misses the
   mark — wrong style, wrong framing, wrong mood — collect feedback, adjust
   the prompt (re-run the `playing-card-prompt` wizard, edit the captured
   `[STYLE_BLOCK]`/`[FRAME_LINE]`, or tweak mood/theme phrases directly),
   and re-generate. Repeat until the user approves. The approved prompt is
   the template for all 52+ cards; catching a style issue here saves
   re-generating the entire deck.

2. **Per-batch checkpoints (during the deck loop):** After each configurable
   batch (default: one suit = 13 cards), pause and show the results. The
   user can approve and continue, flag individual cards for re-generation
   (per-card prompt fix), or flag a systemic issue (deck-wide prompt fix +
   re-generate all affected cards). The loop resumes only after the user
   explicitly continues.

**Prompt correction workflow:** When a card fails review, the agent must:
- Identify the failure mode (lighting, composition, character accuracy,
  style drift, etc.)
- Propose a concrete prompt edit (add/remove a phrase, adjust a layer value)
- Re-generate that card with the corrected prompt
- Present the new result for approval before moving on

The corrected prompt fragment is saved back to the manifest so the same fix
applies to all remaining cards of the same group.

---

## Roadmap 1 — playing-deck wraps playing-card-prompt as-is

Core principle: `playing-card-prompt` is **not modified for the core flow**
(zero changes for the standard rank set / existing config). Both skills run
in the same Claude session, so `playing-deck` can capture the intermediate
resolved values (RANK_LETTER, SUIT_SYMBOL/COLOR, resolved FRAME_LINE,
ASPECT_RATIO, theme/mood phrases, double-headed-ness) while
`playing-card-prompt`'s wizard runs, without needing a new structured output
format.

### Phase 0 — Scaffolding + prerequisites
- Prerequisite: `playing-card-prompt` installed as a sibling skill (version ≥
  the release that adds JOKER/CARD_BACK/SUMMARY templates — see "Special
  cards" below; tracked as a separate, additive, minor-version change in
  `playing-card-prompt`, not part of this roadmap).
- Prerequisite: an image-gen tool/MCP is available (engine selected via
  `playing-deck`'s own `config.json`); if unavailable, confirm "prompt-only
  handoff" mode at this step.
- Scaffold `skills/playing-deck/` per repo conventions (SKILL.md,
  CHANGELOG.md, starting at v1.0.0).
- Establish sibling-path convention to read `playing-card-prompt`'s
  `config.json`/`assets/` (single source of truth for deck-wide settings —
  deck, lettering, style, frame, mood, theme, aspect_ratio, layers.*).
- `playing-deck`'s own `config.json`: image-gen engine config, SVG template
  paths, output directory, **retry/timeout policy** (see Phase 1).

### Phase 1 — Single card: prompt → image
- Run `playing-card-prompt`'s Generate mode (as-is) for one card → capture
  the final prompt + the resolved intermediate values noted above.
- Call the image-gen tool with a **retry/timeout policy**: per-call timeout,
  N retries with backoff, and after exhaustion fall back to manual
  prompt-handoff (recorded in the deck manifest). Policy is configurable via
  `config.json`.
- **Human-in-the-loop (mandatory):** After generating the first card image,
  present it to the user for approval before proceeding. If the result does
  not match expectations, collect feedback, adjust the prompt (e.g. re-run
  `playing-card-prompt` in Generate mode with revised style/mood/theme, or
  directly edit the captured intermediate values), and re-generate. Repeat
  until the user approves the "golden card." Only then continue to Phase 2
  and beyond. The approved prompt fragments and resolved values become the
  reference for all subsequent cards.

### Phase 2 — SVG assembly for a single card
- Pre-built base SVG frame templates for the frame presets in
  `assets/frame/*.md` (Boxed Index, Stepped Corners, Double Rule, Ornate
  Scrollwork) with placeholder slots.
- Inline-SVG suit-symbol library per deck system.
- Compose: pick the template matching the resolved `frame`, fill
  index/suit/portrait slots, embed the generated portrait via `<image>`, and
  mirror double-headed figures via `<use>` + `transform="rotate(180 ...)"`.
- Decorative pattern effects (gilding, lacquer, glow...) stay out of the SVG
  frame — it remains structural/geometric; painterly effects belong to the
  image-gen output in "full illustrated card" mode.

### Phase 3 — Deck assembly loop
- Loop over the 52 standard cards plus **Joker(s) / Card Back / Summary**
  (new groups added to `playing-card-prompt`, see "Special cards" below).
  Card Back and Summary are generated once (deck-wide); Jokers per the
  lettering/deck system's joker count.
- Reuse the same resolved `[STYLE_BLOCK]`/`[FRAME_LINE]`/theme phrases across
  all cards of a group for visual consistency.
- Delegate image-gen calls to subagents (per card or batch) to keep the main
  context clean.
- **Human-in-the-loop checkpoints (mandatory):** Pause for user review at
  configurable intervals (default: after each suit completes, i.e. every
  13 cards). Present the batch of generated images; if any card fails the
  visual check, identify whether the issue is per-card (character prompt
  needs adjustment) or deck-wide (style/mood/frame phrase needs adjustment).
  For a per-card issue: correct that card's prompt and re-generate only that
  card. For a deck-wide issue: stop the loop, correct the shared prompt
  fragments, and re-generate all already-failed cards before continuing.
  The user can also approve the batch and continue, or request a full restart
  with revised settings. Checkpoint interval is configurable via `config.json`.
- Produce a manifest of all output files.

### Phase 4 — Validate deck results
- Structural check: all expected cards present (52 + back + jokers +
  summary), manifest complete, consistent file naming.
- Visual-consistency check: resolved `[STYLE_BLOCK]`/`[FRAME_LINE]`/theme
  phrases are identical across cards within the same group.
- Per-card SVG validation: no leftover `[PLACEHOLDER]` tokens, valid SVG,
  dimensions match `[ASPECT_RATIO]`.
- Produce a pass/fail report with a list of issues for manual follow-up.

### Phase 5 — Polish + Box/Cover
- `playing-deck` config/profile (output format, resolution).
- Box/cover/prospectus: a separate composition step that arranges
  already-rendered cards into a presentation scene (deck box mockup, card
  fan, etc.) — operates on rendered assets, not on new per-card prompts.
  May become its own skill if it grows large.
- Documentation, packaging.

### Special cards (Card Back / Joker / Summary)
These reuse all of `playing-card-prompt`'s deck-wide settings and
`[STYLE_BLOCK]` resolution machinery, so they are added as **new groups**
in `playing-card-prompt` (new CARD_BACK/JOKER/SUMMARY templates in
`references/REFERENCE.md`, new Step-3 rank options, minimal extra
questions per group — Card Back has no figure, Joker has a figure but no
rank/suit, Summary is a text/layout-heavy card). This is an additive,
non-breaking, minor-version change to `playing-card-prompt` — already
tracked in its `TODO.md` (Card back, Joker card, Special card items).
Box/cover/prospectus composition belongs to `playing-deck`, since it
composites already-rendered card images rather than generating a new
per-card prompt.

---

## Roadmap 2 — playing-card-prompt lightened to figure-only prompts

Three variants were considered:

- **2a — full migration**: move all deck-wide settings/resolution logic out
  of `playing-card-prompt` into `playing-deck`. Rejected — major breaking
  change to a published skill (v3.18.0, existing profiles), and just
  relocates the duplication problem rather than solving it.
- **2b — additive figure-fragment mode**: keep `playing-card-prompt`'s
  existing full-card mode + config for standalone users, add a new
  lightweight "figure prompt" output mode consumed by `playing-deck`. Low
  risk, but mixes two modes in one skill's docs/triggering.
- **2c — fork into two skills** (chosen): fork `playing-card-prompt` into
  `playing-card` (figure-centric) and `playing-deck` (deck-wide
  orchestrator + assembly). `playing-card-prompt` is frozen as a legacy
  standalone full-card generator — no further changes, so the
  duplicated/forked static assets in each new skill never need to be kept
  in sync with it.

### Phase 0 — Double fork (bootstrap)
- Fork `playing-card-prompt` (frozen at v3.18.0 as legacy standalone) into
  two new skills, both starting as full copies:
  - `playing-card` (v1.0.0) — figure-centric prompt generator
  - `playing-deck` (v1.0.0) — deck-wide orchestrator + assembly (supersedes
    the placeholder scaffold from Roadmap 1 Phase 0)
- This gives `playing-deck` the proven `config.json`/`manage_config.py`/
  profile machinery, `assets/decks|pattern|frame|mood|figure-proportion|
  engines`, `references/CONFIG.md`, and the `[STYLE_BLOCK]`/`[FRAME_LINE]`/
  `[INDEX_LINE]` assembly logic from `REFERENCE.md` — essentially for free,
  instead of building it from scratch.
- No ongoing duplication-sync burden: the original `playing-card-prompt` is
  frozen from this point, so the two forks' overlapping starting material
  diverges permanently without needing to track upstream changes.

### Phase 1 — Trim `playing-card`
- Remove Steps 1,2,5,6,7,8,13,14 and their config schema/assets (decks,
  pattern, frame, mood, figure-proportion, engines, `CONFIG.md`).
- Keep Step 3 (rank → court/pip/ace group, `assets/courts/*.md`), Steps
  9–12 (character/attributes/transfers/exclusions), and the
  `layers.technique.<group>` / `layers.figure.<group>` resolution.
- Redefine the wizard's inputs: Technique/Finish/Face-Style text,
  `figure_proportion` text, theme/mood phrases, and
  `layers.technique/figure.<group>` are now **parameters passed by
  `playing-deck`**, not asked.

### Phase 2 — Trim & extend `playing-deck`
- Remove Step 3, Steps 9–12, `assets/courts/*.md`, and the
  character/figure-description wizard — now `playing-card`'s job.
- Keep Steps 1,2,5,6,7,8,13,14, the config/profile machinery, `assets/
  decks|pattern|frame|mood|figure-proportion|engines`, and the
  `[STYLE_BLOCK]`/`[FRAME_LINE]`/`[INDEX_LINE]` assembly logic.
- Add per-card orchestration: resolve the deck-wide context, extract the
  Technique/Finish/Face-Style lines for the chosen pattern, call
  `playing-card` with these as parameters to get the figure-prompt
  fragment, then combine it with the assembled `[STYLE_BLOCK]`/
  `[FRAME_LINE]`/`[INDEX_LINE]` for the image-gen prompt.

### Phase 3 — Interface contract
- Input to `playing-card` per card: rank, Technique/Finish/Face-Style text,
  `figure_proportion` text, theme/mood phrases,
  `layers.technique/figure.<group>` values, plus user-provided character
  details.
- Output from `playing-card`: figure-prompt fragment text +
  `[CHARACTER_NAME]` / `[RESOLVED_ATTRIBUTES]` / additional negatives.

### Phase 4 — New `playing-deck` capabilities
- Apply Roadmap 1's Phases 1–5 (image-gen with retry/timeout, SVG assembly,
  deck loop, validation, special cards via `playing-card`'s
  CARD_BACK/JOKER/SUMMARY groups, box/cover) on top of the
  `playing-card` + `playing-deck` pair instead of
  `playing-card-prompt` + `playing-deck`.
- The HITL policy from Roadmap 1 (golden-card approval after Phase 1,
  per-suit checkpoints in Phase 3) applies identically here. The key
  difference: when a deck-wide issue is found during a checkpoint, the
  correction target is `playing-deck`'s assembled `[STYLE_BLOCK]`/
  `[FRAME_LINE]` rather than `playing-card-prompt`'s wizard output.

### Phase 5 — `playing-card-prompt` fate
- Remains as a frozen, standalone full-card prompt generator (v3.18.0+) for
  users who don't need `playing-deck`. Documented as the
  "standalone/legacy" path; the new deck-building workflow points users to
  `playing-card` + `playing-deck`.
