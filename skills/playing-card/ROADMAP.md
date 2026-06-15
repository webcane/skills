# playing-card — Roadmap

`playing-card` is the figure-centric fork produced by Roadmap 2 (variant 2c)
of [playing-deck/ROADMAP.md](../playing-deck/ROADMAP.md): a lightweight
prompt generator for a single **centered figure/portrait**, with no card
"structure" (no `[INDEX_LINE]`/`[FRAME_LINE]`, explicit negatives instead).
All deck-wide settings (deck/lettering/style/frame/mood/theme/aspect_ratio/
engine) live in `playing-deck` and are passed into `playing-card` as
parameters per card.

`playing-card-prompt` (v3.18.0+) is frozen as the legacy standalone
full-card generator and is not modified by this roadmap.

---

## Phase 0 — Fork & trim (bootstrap)

- Fork `skills/playing-card-prompt` → `skills/playing-card` (v1.0.0, own
  CHANGELOG) per Roadmap 2 Phase 0/1.
- Strip Steps 1, 2, 4, 5, 6, 7, 8, 13, 14 and their config/assets (`decks`,
  `pattern`, `frame`, `mood`, `figure-proportion`, `engines`, `CONFIG.md`,
  the persistent-settings surface of `manage_config.py`/`config.json`).
- Keep Step 3 (rank → court/pip/ace group + traditional attributes from
  `assets/courts/*.md`), Steps 9–12 (character description, attributes,
  transfers, exclusions), and `layers.technique.<group>` /
  `layers.figure.<group>` resolution.
- Replace the COURT/PIP/ACE full-card templates with a single
  **figure-prompt-fragment template**: figure description + resolved
  attributes + Technique/Finish (as supplied) + negatives for card
  structure ("no border, no card frame, no index letters/numbers, no corner
  symbols") — i.e. this *is* the "card structure separately" mode from
  `playing-card-prompt`'s `TODO.md`, now the default and only mode.
- New input contract (parameters, not wizard questions): Technique/Finish/
  Face-Style text, `figure_proportion` text, theme/mood phrases,
  `layers.technique/figure.<group>` values.
- Output: figure-prompt fragment text + `[CHARACTER_NAME]` /
  `[RESOLVED_ATTRIBUTES]` / additional negatives, per Roadmap 2 Phase 3's
  interface contract.

## Phase 1 — Standalone usability

- When invoked without `playing-deck`-supplied parameters, ask compact
  fallback questions for the dropped inputs (pick a pattern → derive
  Technique/Face-Style; pick `figure_proportion`) so `playing-card` remains
  independently useful for a single-portrait prompt.
- Keep this fallback config minimal (no profile system) — it's a
  convenience path, not a parallel settings surface to `playing-deck`'s.

## Phase 2 — Joker support

- New group: **Joker** — has a figure, no rank letter/suit.
- New traditional-attribute reference (`assets/courts/joker.md`) with
  jester/fool iconography defaults, following the existing
  `king.md`/`queen.md`/`jack.md` format.
- Extend Step 3's rank options to include Joker.
- Addresses the "Joker card" item from `playing-card-prompt`'s `TODO.md`.

## Phase 3 — Special/custom figure cards

- Generalize Step 3's group resolution to accept a user-defined custom card
  concept (name/role) outside the standard rank set, for decks with extra
  non-standard cards.
- Addresses the "Special card" item from `playing-card-prompt`'s `TODO.md`.

## Phase 4 — Output polish & validation

- Update the post-validation checklist for the figure-fragment output:
  no leftover structure placeholders, negatives present, traditional vs.
  custom attributes merged without contradiction.
- Add worked-example reference files for the figure-fragment output,
  parallel to `playing-card-prompt`'s `references/example-*.md`.

## Out of scope (tracked under playing-deck instead)

The following `playing-card-prompt` `TODO.md` items are deck-wide or
structural concerns and belong to `playing-deck`, not `playing-card`:
- **Card back** — no figure, pure pattern/decoration (Steps 5/6).
- **Title / text overlay** — rendered in the SVG layer, not the AI prompt.
- **Split** (mirrored halves vs. full body) — resolved by `playing-deck`'s
  SVG `<use>` + `rotate(180)` mirroring (Roadmap 1 Phase 2); `playing-card`
  only ever produces a single portrait.
- **Seamless design** (across the card/deck) — deck-wide composition.
- **Config mode / layers overview** — `layers.*` config now lives in
  `playing-deck`.
