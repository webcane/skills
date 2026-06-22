# Changelog — playing-card-prompt

All notable changes to this skill. Released per skill as tag
`playing-card-prompt/v<version>`. The version in `SKILL.md` frontmatter
(`metadata.version`) is the source of truth.

## [4.1.0] - 2026-06-22

### Changed
- **`layers.seamless.<group>` no longer restricted to court/pip/ace/joker** — removed the D-05 validation restriction in `manage_config.py` (`options_for`) that forced `back`/`special` to `"false"` only; all six groups now accept the same `false` | `true` | `<alias>` | `<custom_text>` values. Updated `references/CONFIG.md`, `references/STYLE-COMPONENTS.md`, `references/WIZARD-STEP-MAP.md`, and `SKILL.md` Step 8f to drop the now-inaccurate "court/pip/ace/joker only" framing. Defaults remain `"false"` for every group, so behavior is unchanged unless a user explicitly opts a `back`/`special` group in.

### Fixed
- **`references/CONFIG.md`'s schema example still showed `title.enabled` as a bare JSON boolean (CR-01)** — `"title": {"enabled": false}` corrected to `"title": {"enabled": "false"}`, matching the quoted-string convention used by every other boolean-like cell in the same example block and the code's actual `DEFAULTS["title"]["enabled"]` value (fixed in `7ff975d`, but this doc example was missed).
- **No load-path migration for a stale literal `layers.seamless.<group>="true"`, asymmetric with `figure` (WR-01)** — added `_migrate_seamless_true_to_alias()`, mirroring `_migrate_figure_true_to_character()`: resolves a stale `"true"` cell to the first discovered non-`"false"` preset from `allowed_seamless()`, same resolution logic as the existing `cmd_set` write-path fix (CR-02). Wired into `load_raw()` so it runs unconditionally on every load, catching values written by a hand-edited `config.json` or any non-CLI path — previously such a value passed `validate`, round-tripped through `get`/`profile create --from` unresolved, and would have produced a broken `true,` literal in assembled prompts.
- **Shipped `config.json` was missing `layers.seamless` and `title` entirely (WR-02)** — regenerated the default profile from `BUILTIN_CONFIG` (same `reset` + `save_raw` method used in SYNC-01's `d1e72f2`) so it again mirrors `manage_config.py`'s `DEFAULTS`/`LAYER_DEFAULTS` exactly, restoring `CONFIG.md`'s "source of truth for defaults" guarantee for this file.

## [4.0.1] - 2026-06-22

### Fixed
- **`title.enabled` default was a Python `bool`, breaking `validate` and `profile create --from` (CR-01)** — `DEFAULTS["title"]["enabled"]` is now the string `"false"`, matching the string convention used by every other boolean-like field in the schema (`BOOL_VALUES = ["true", "false"]`). Previously, `manage_config.py validate` failed on any profile (including a fresh `profile create --from default`) with `title.enabled must be one of: true, false`, even though the on-disk JSON value was valid — the `str(False)` coercion in `cmd_validate` produced the capitalized `"False"`, which doesn't match the lowercase enum.
- **`layers.seamless.<group> = "true"` was never resolved on write, contradicting documented behavior (CR-02)** — `cmd_set`'s write-path `"true"`-resolution block gained a `seamless` branch (alongside the existing `figure`/`split` branches): it now resolves to the first discovered non-`"false"` preset from `allowed_seamless()`, matching the already-shipped documentation (CHANGELOG, `SKILL.md` Step 8f, `_adding-a-seamless.md`, `CONFIG.md`, `REFERENCE.md`) which stated `"true"` "is never persisted literally." Previously the literal string `"true"` was written to disk, and prompt assembly would have appended a broken `true,` phrase into the generated `[STYLE_BLOCK]` (no `assets/seamless/true.md` exists).
- **`cmd_validate`'s `str(v)` coercion hardened against non-string `DEFAULTS` values (WR-02)** — explicit Python-bool-to-lowercase-string normalization added before validation, so a future boolean field stored as a Python `bool` (the root cause of CR-01) fails clearly instead of producing a confusing validation error.
- **`WIZARD-STEP-MAP.md` row order corrected to match actual wizard execution order (WR-01)** — the "Seamless step" row moved from between `8b`/`8c` to directly after `8e` (its real position as Step 8f, after the figure-type/character-framing steps); the "Title step" row moved to after row `12` (its real position as Step T, which runs for all six card groups, including `back`/`special`, and is not part of the figure block at all).

## [4.0.0] - 2026-06-22

### Changed
- **SKILL.md size optimization (OPT-01)** — extracted five self-contained instruction blocks into lazy-loaded `references/` files, each replaced in `SKILL.md` by a 1-line trigger pointer: File map → `references/FILE-MAP.md`, Config-wizard 11-step block → `references/CONFIG-WIZARD.md`, Joker Steps 4.1–4.2 → `references/JOKER-WIZARD.md`, Back Steps B1–B7 → `references/WIZARD-BACK.md`, Special Steps S1–S5 → `references/WIZARD-SPECIAL.md`. Pure relocation — no wizard behavior changed. `SKILL.md` shrinks from 986 to 636 lines, reducing what's loaded in full on every invocation.
- `references/WIZARD-STEP-MAP.md` documents the new Joker-steps file location with a footer note matching the existing Back/Special rank-group notes (DOCS-02).
- **SKILL.md further size optimization (OPT-02/OPT-03)** — removed "config-only, not asked here" explanatory footnotes from Steps 6 and 7 (frame/highlights/group-wide figure trait/technique/mood per-group additions); collapsed the standalone Step 8d (Face style gate) into Step 8c's existing gate paragraph; condensed the "Assembling the prompt" section's `[INDEX_LINE]` and `[STYLE_BLOCK]`/`[FRAME_LINE]` steps into terse decision bullets that delegate rule detail to `references/REFERENCE.md` instead of restating it inline. No wizard question removed, no Generate-mode behavior changed — `SKILL.md` shrinks further from 636 to 583 lines.
- **Generate-mode first-run redirect (FIX-06)** — when no valid config exists (`config.json` missing, or just reset via `manage_config.py reset` — treated identically, one code path), Generate mode no longer runs the full wizard inline against empty/default state. It now redirects into the Config wizard (`references/CONFIG-WIZARD.md`, the same 11-step flow `--config` uses) to set deck type, lettering, and the other persistent settings, saves them to the active `default` profile, then continues to per-card steps. `--config` entry and Config mode itself are unchanged.
- **Mood schema consolidation (MOOD-01)** — removed the deck-wide root `mood` field; `layers.mood.<group>` is now the single mood schema (`"false"` = off, `"true"` = on with no specific line, any other text = the mood line itself, appended verbatim as `[MOOD_LINE]`). A new `_migrate_root_mood` function in `manage_config.py` migrates existing configs that still carry a root `mood` value into the per-group cells (upgrading `"true"` cells to the old root text; custom per-group text is left untouched) on next load. `references/REFERENCE.md`'s `[MOOD_LINE]` assembly rule (step 8) and the layers-overview Mood bullet updated to describe the unified one-level model.

### Added
- **`seamless` layer + `title.enabled` (SEAM-01, SEAM-03, SEAM-04, TITL-01)** — `manage_config.py` gains a new `"seamless"` entry in `LAYERS`, giving `layers.seamless.<group>` the same `false | true | <alias> | <custom_text>` shape as `figure`/`split`. Valid for `court`/`pip`/`ace`/`joker`; `back`/`special` are restricted to `"false"` only (no figure-bearing seamless use case identified). A new `allowed_seamless()` discovers preset aliases from `assets/seamless/*.md` (mirroring `allowed_splits()`); `"true"` is accepted as input and resolves to a discovered alias rather than being persisted literally. A new persistent `title.enabled` boolean (default `false`) is also added (`DEFAULTS`, `PERSISTENT_KEYS`, `options_for()`). No cross-field validation against `figure_scale` was added (D-08, explicitly rejected).
- **`assets/seamless/` directory (SEAM-04, SEAM-06)** — new `_adding-a-seamless.md` authoring guide (mirroring `assets/figure-scale/_adding-a-figure-scale.md`) plus two preset files, `continuous-border.md` (edges align to form one unbroken pattern across the layout) and `interlocking-motif.md` (interlocking repeating motif that tiles edge-to-edge with neighbouring cards). Both are discovered by `allowed_seamless()`.
- **Seamless + title assembly spec documented (SEAM-02, SEAM-05, TITL-03, TITL-05)** — `references/REFERENCE.md`'s `[STYLE_BLOCK]` figure block gains a new step 6e: appends the seamless phrase (file-lookup against `assets/seamless/<alias>.md`, or custom text verbatim) for court/pip/ace/joker when `layers.seamless.<group>` is non-`"false"`. The `structure: illustration` rule list grows from 4 to 5 items — the new item 5 drops both the title named element and the seamless instruction under `illustration`, regardless of configured values (one shared structure gate for both features). A new "Title text" subsection documents the title named element: present only when `title.enabled` AND `structure == "full"`, with no position/font/styling specified (left to the user's SVG template) and the per-card title text itself ephemeral (never persisted). `references/CONFIG.md` gains field-reference rows for `layers.seamless.<group>` and `title.enabled` (plus matching schema-example fields), and corrects the `layers.figure.<group>` row (`"true"` is accepted input, not rejected) and `layers.split.<group>` row (`"true"` → `"none"`, free/custom text supported). `references/WIZARD-STEP-MAP.md` gains Title step and Seamless step rows and extends the `structure` note to cover both. `references/STYLE-COMPONENTS.md` component #5 now mentions `layers.seamless.<group>` coverage.
- **Title and Seamless wizard steps added to `SKILL.md` (TITL-02, TITL-04, TITL-05, SEAM-02, SEAM-03, SEAM-05)** — new Step T ("Title text") asks per-card title text for all six card groups (court/pip/ace/joker/back/special) when `title.enabled` is `"true"` AND `structure == "full"`; skipped entirely when `title.enabled` is `"false"` or `structure` is `"illustration"`. New Step 8f ("Seamless design") asks per-group seamless design for court/pip/ace/joker only (skipped for back/special, skipped when the figure layer is off, skipped under `structure: illustration`), offering no-seamless/continuous-border/interlocking-motif/custom-text and saving via `layers.seamless.<group>`. Step 8b's (split) and the figure-block intro's guidance updated to state `layers.figure.<group>` and `layers.split.<group>` accept `"true"` as input (FIG-09, SPLT-05) rather than describing it as invalid.

### Fixed
- **`layers.figure.<group>` and `layers.split.<group>` re-accept `"true"` (FIG-09, SPLT-05)** — `cmd_set` now resolves `"true"` immediately on write: `layers.figure.<group>="true"` resolves to the group's default figure-type alias (`character` for court/joker, `false` for pip/ace, per `LAYER_DEFAULTS["figure"]`); `layers.split.<group>="true"` resolves to `"none"`. Neither persists a literal `"true"` figure/split cell. `_migrate_figure_true_to_character()` (the load-path migration) is unchanged.
- **`figure_scale` wiring completed (FIG-10)** — `manage_config.py` now discovers allowed `figure_scale` values from `assets/figure-scale/` (via a new `allowed_figure_scales()` function, mirroring `allowed_figure_types()`) instead of a hardcoded 3-item list, so `cross-a-frame` (already shipped as an asset file) is now accepted. `references/REFERENCE.md`'s `[STYLE_BLOCK]` step 6c assembler now looks up the matching `assets/figure-scale/<value>.md` "Scale phrase" for named presets, falling back to the literal value only for custom free text (previously it always appended the raw config value verbatim, never reading the asset files). `references/CONFIG.md` and `references/STYLE-COMPONENTS.md` updated to list all 4 presets and describe the file-lookup-with-fallback behavior.
- **Code review fixes (CR-01, CR-02, WR-01, WR-03)** — `references/CONFIG.md` documented a `$AGENT_SKILLS_SETTINGS`/global `settings.json` lookup tier and a `layers.figure.<group>` free-text addition grammar that `manage_config.py` never implements (`effective()` has no global-settings merge; the field is `strict=True` and rejects free text); both removed from `references/CONFIG.md` and `references/REFERENCE.md`. `references/WIZARD-STEP-MAP.md` still listed a "Step 8d" row removed from `SKILL.md` earlier this phase; folded into Step 8c's row to match. `manage_config.py`'s `cmd_options` ignored the `--profile` flag (unlike `cmd_show`/`cmd_get`/`cmd_set`), producing wrong category-aware `back_pattern` lists for non-active profiles; now parses `--profile` via the existing `_pop_profile_flag` helper.
- **`LAYER_DEFAULTS` corrected to match its own stated intent (SYNC-01)** — "plain pips get only background + center motif + finish, aces keep their ornamental flourish" wasn't actually true before this fix: `decor.ace`, `ornaments.ace`, `technique.pip`, `technique.ace`, `mood.pip`, `mood.ace` were `"false"` (should be `"true"`) and `frame.pip` was `"true"` (a plain pip has no border per the field reference, should be `"false"`). All seven cells corrected in `manage_config.py`; the shipped `config.json` default profile regenerated from the corrected code so it no longer drifts from `LAYER_DEFAULTS`. `references/REFERENCE.md`'s Defaults table and surrounding prose updated to match.
- **`references/CONFIG.md` resynced with the shipped v4 schema (SYNC-02/SYNC-03/DOCS-01/DOCS-03)** — the schema JSON example's `decor.ace`/`ornaments.ace`/`frame.pip`/`mood.*`/`technique.*` cells, a stale root `"mood": ""` key, and the `gothic-deck` example profile's flat `mood` field were all left over from before SYNC-01/MOOD-01 landed in code; all now match `LAYER_DEFAULTS`/`DEFAULTS` exactly. The `layers.figure.<group>` field-reference row is rewritten as `false \| alias \| alias addition_text` with a note that bare `"true"` is accepted only for backward-compatible migration (never write it directly). `character_framing`'s row now lists all five shipped presets (`bust`/`waist-up`/`three-quarter`/`seven-eighths`/`full-body`). A migration note for the removed `figure_proportion` field is added near `figure_scale`/`character_framing`. `assets/figure-proportion/_adding-a-figure-proportion.md` now carries a deprecation banner pointing to `figure_scale`/`character_framing` instead of presenting `figure_proportion` as a live setting.

## [3.25.0] - 2026-06-20

### Fixed
- B1-B6 skip behavior now matches v1 scope (D-17): skipping an already-configured persistent back-wizard step is silent, with no consolidated summary printed.
- Stale duplicate reference to the deprecated singular `assets/back/symmetry.md` in SKILL.md's "Assembling the prompt" step 4 corrected to the alias-based `assets/back/symmetry/<back_symmetry>.md` path (canonical instructions in Step B5 and REFERENCE.md step 10 were already correct).
- **Duplicated finish guardrail** — removed the redundant `flat graphic design, vector style, centered on a clean transparent background,` phrase from the default `back_symmetry` asset (`assets/back/symmetry/rotational-180.md`); it was already appended unconditionally by the assembly step, so default-config back prompts contained it twice.
- **Prospect card layout hardcoding** — `assets/special/prospect.md` and SKILL.md's Step S4 assembly no longer hardcode a "4 suits × 3 ranks grid" layout into `[SPECIAL_TYPE_LINE]`/`[FIGURE_DESCRIPTION]`; the user's actual layout choice from Step S3 (12-row list, rank-grouped rows, free-form collage, or grid) is now honored.
- **Step B3 missing pattern options** — all 4 on-disk pattern files per back-design category are now surfaced as `AskUserQuestion` options (previously only 3 of 4 were reachable without typing the exact filename as custom text).
- **Step 8c figure-type guidance** — clarified that the persisted `layers.figure.<group>` value must be the enum keyword, not free text, matching `manage_config.py`'s strict validation (previously caused CLI rejection on the documented custom path).
- **`back_pattern` validation** — `manage_config.py` now validates `back_pattern` against the options for its configured `back_design` category instead of accepting any string.
- **Missing negative-list seed** — added `no watermark` to the BACK/SPECIAL `[NEGATIVE_LIST]` seed in `references/REFERENCE.md`, matching the COURT template.
- **Stale CONFIG.md schema example** — synced the schema example and figure-content prose in `references/CONFIG.md` with the shipped schema.
- **`_migrate_layers_extras` false-positive** — `manage_config.py` no longer reports a migration as having occurred when no fields actually changed.

## [3.24.0] - 2026-06-19

### Added
- **Back card group** — `back` is a full peer card group (alongside court/pip/ace/joker/special) with `layers.*.back` config entries in `manage_config.py` and `config.json`. Defaults: figure off, split off, frame on, full decoration (background/decor/ornaments/mood/technique on). Selecting Back as rank in Step 3 skips Step 4 (suit) and enters the Back design wizard (Steps B1–B7).
- **Special card group** — `special` is a full peer card group with `layers.*.special` config entries. Defaults: figure off, frame off (non-standard layout), full decoration otherwise. Selecting Special as rank in Step 3 skips Step 4 and enters a five-step wizard (Steps S1–S5): card title (S1), special type from `assets/special/` (S2), visual content description (S3), optional named figure for prospect-type cards (S4, per-card, no persistence in v1), exclusions (S5). Back and special group defaults documented in `references/REFERENCE.md` Defaults table and `references/CONFIG.md`.
- **Prospect card support** — for prospect-type special cards, Step S4 collects 12 named figure assignments (King/Queen/Jack × 4 suits with optional suit theme labels) and a layout preference. The wizard generates a single composite-card prompt showing all 12 court figures in one image. Step S3 offers four explicit layout choices via `AskUserQuestion`: 4 suits × 3 ranks grid, 12-row list, 3 rows grouped by rank, free-form collage.
- **SPECIAL prompt template** — new template in `references/REFERENCE.md` assembles special card prompts using `[CARD_NAME]`, `[SPECIAL_TYPE_LINE]`, `[STYLE_BLOCK]`, `[FRAME_LINE]`, `[FIGURE_DESCRIPTION]`, `[SPECIAL_ATTRIBUTES]`, and `[NEGATIVE_LIST]`. Hardcoded `no corner indices, no standard rank letters, no suit symbols,` inline (no INDEX_LINE placeholder). New `assets/special/` directory: `prospect.md`, `marketing.md`, `_adding-a-special.md`.
- **Config schema update** — `back` and `special` added to all `layers.*` groups; `layers.frame.special` defaults to `false`; `layers.figure.back` defaults to `false`.
- **figure-scale asset files** — added `assets/figure-scale/` with four named presets (`inscribed-in-frame`, `full-bleed`, `small-centered`, `cross-a-frame`) and an `_adding-a-figure-scale.md` authoring guide. Each preset file defines the exact comma-terminated prompt phrase for that scale mode (FIG-10).
- **Back card wizard steps B1–B7** — replaced the three generic B1–B3 paths (suggested/freeform/ref-image) with seven structured criteria steps: B1 purpose, B2 design category, B3 specific pattern, B4 palette, B5 symmetry, B6 frame, B7 exclusions. Steps B1–B6 are persistent (deck-wide, skipped if already set); B7 exclusions remain per-card.
- **`[BACK_DESIGN]` assembly** — now assembled from three asset lines: purpose line + pattern line + palette line. Symmetry excluded from `[BACK_DESIGN]` (goes via STYLE_BLOCK step 10); frame excluded (goes via `[FRAME_LINE]`). Previous `[BACK_MODIFICATIONS]` placeholder removed from BACK template (now part of `[NEGATIVE_LIST]`).
- **26 new back card asset files** across 7 subdirectories: `assets/back/purpose/` (3: classic, designer, casino), `assets/back/design/geometric/` (4: diamond, cross-hatch, hexgrid, wave), `assets/back/design/botanical/` (4: vine, floral, leaf, branch), `assets/back/design/abstract/` (4: interlacing, color-field, paint-stroke, fractal), `assets/back/design/illustrated/` (4: thematic, portrait, landscape, heraldic), `assets/back/palette/` (4: classic-red, classic-blue, dark, gold), `assets/back/symmetry/` (3: rotational-180 from old symmetry.md, bilateral, asymmetric).
- **Five new persistent config fields**: `back_purpose` (default: `classic`), `back_design` (default: `geometric`), `back_pattern` (default: `diamond`), `back_palette` (default: `classic-blue`), `back_symmetry` (default: `rotational-180`). All allow custom text.
- **D-21 fallback** in B3: when `back_design` is custom text (not a known category alias), B3 falls back to geometric category options.
- **REFERENCE.md STYLE_BLOCK step 10** updated to load from `assets/back/symmetry/<back_symmetry>.md` (conditional on config field) instead of always `assets/back/symmetry.md`.
- **WIZARD-STEP-MAP.md** updated: B1–B3 rows replaced with B1–B7 rows; S1–S5 rows added for the Special wizard path.
- **CONFIG.md** updated: five new `back_*` persistent fields documented; `<group>` footnote expanded to include `back` and `special`.
- **Finish guardrails** — every assembled prompt now ends with `flat graphic design, vector style,` and `centered on a clean transparent background,` (or `isolated on a solid black background,` for users compositing into their own template) immediately before the negative list. Prevents unwanted 3D shading, photorealistic surface lighting, and texture artifacts. Applied to all card types including back cards (added to the symmetry line in `assets/back/symmetry.md`). Additionally embedded in the Finish sections of the French and Art Nouveau patterns (where the flat/vector descriptor is consistent with their existing style intent); Austrian, English, and Japanese patterns intentionally excluded — their engraving, cross-hatching, and woodblock-texture aesthetics would conflict.

## [3.22.0] - 2026-06-18

### Fixed
- **Step S1 label**: renamed "Card display name" → "Card title" in wizard step and WIZARD-STEP-MAP.md.
- **Prospect card S4 scope note**: added explicit note that selecting the 12 named figures is a structural/content task outside this skill — the skill expects assignments to arrive pre-prepared.
- **Prospect card concept**: a prospect card is now correctly implemented as ONE card showing all 12 court figures (King/Queen/Jack × 4 suits) in a single image. The wizard collects all 12 named figure assignments (with optional suit theme labels and layout preference) and generates ONE prompt. Previously the wizard generated 12 separate individual card prompts instead of one composite card prompt.

### Added
- **Card back group** — `back` is a new card group (peer to court/pip/ace/joker) with
  `layers.*.back` config entries in `manage_config.py` and `config.json`. Defaults:
  figure off, split off, frame on, full decoration (background/decor/ornaments/mood/technique on).
- **Special card group** — `special` is a new card group with `layers.*.special` config
  entries. Defaults: figure off, frame off (non-standard layout), full decoration otherwise.
- **`assets/back/symmetry.md`** — symmetry/repeat-pattern/frame-margin instruction for
  the BACK group STYLE_BLOCK; always included when assembling a back card prompt.
- **`assets/special/prospect.md`** — prospect special card type template (named
  historical/thematic figure, portrait composition).
- **`assets/special/marketing.md`** — marketing special card type template (promotional
  card, branded layout).
- **`assets/special/_adding-a-special.md`** — guide for adding user-defined special card
  types; follows the same `_adding-a-*` convention as mood and frame guides.
- **Back rank wizard path (Steps B1–B3)** — `Back → BACK` rank option in Step 3; three
  design paths (suggested from style+mood / freeform / reference-image + modifications);
  refinement step B2 for the suggested path; exclusions step B3.
- **BACK template** — new prompt template in `references/REFERENCE.md` with
  `[BACK_DESIGN]`, `[BACK_MODIFICATIONS]` placeholders; symmetry line always included.
- **Special rank wizard path (Steps S1–S5)** — `Special → SPECIAL` rank option in Step 3;
  display name (S1), type selection from `assets/special/` (S2), visual content description
  (S3), named figure for prospect-type (S4, per-card, v1 no persistence), exclusions (S5).
- **SPECIAL template** — new prompt template in `references/REFERENCE.md` with
  `[CARD_NAME]`, `[SPECIAL_TYPE_LINE]`, `[FIGURE_DESCRIPTION]`, `[SPECIAL_ATTRIBUTES]`
  placeholders; hardcoded `no corner indices, no standard rank letters, no suit symbols,`.
- **`references/REFERENCE.md` Defaults table** — `back` and `special` columns added
  documenting all 9 layer default values per group.
- **`references/CONFIG.md`** — `<group>` footnote expanded to include `back` and
  `special`; back and special group default notes added.

## [3.21.0] - 2026-06-17

### Added
- **Figure type classification** — `layers.figure.<group>` values extended from
  `true`/`false` to `false`/`character`/`building`/`animal`/`custom`. Non-`"false"`
  value enables the figure layer AND encodes the figure type. New
  `assets/figure-type/` directory with `character.md`, `building.md`, `animal.md`,
  `custom.md` — each supplying the canonical prompt preamble for that figure type.
  Character figures additionally include Face Style + character framing in
  `[STYLE_BLOCK]`; building/animal/custom skip those character-specific sources
  (see FIG-08 pattern).
- **Figure scale** — new deck-wide persistent field `figure_scale` (values:
  `full-bleed`, `inscribed-in-frame`, `small-centered`) replacing `figure_proportion`
  for scale/cropping control. Applies to all figure types. Appears as Step 8a in the
  wizard figure block.
- **Character framing** — new deck-wide persistent field `character_framing`
  (character-only; values: bust, waist-up, three-quarter, seven-eighths, full-body, or
  custom text). Replaces the role of `figure_proportion` for character-type figures;
  framing asset content moved to `assets/character-framing/`. Appears as Step 8e
  (after face_style gate) in the wizard figure block.
- **Split layout** — new per-group layer `layers.split.<group>` with values
  `false`/`none`/`horizontal-mirrored`/`angled-mirrored`. Adds a compositional
  split wrapper to `[STYLE_BLOCK]` as the outer layer after figure_scale. New
  `assets/split/` directory with `horizontal-mirrored.md` and `angled-mirrored.md`.
  Appears as Step 8b in the wizard figure block.
- **Figure block wizard steps** — figure block reordered to: Step 8a (figure_scale)
  → Step 8b (split) → Step 8c (figure_type) → Step 8d (face_style gate, character
  only) → Step 8e (character_framing, character only) → Steps 9–12 (per-card). All
  figure-block persistent fields are per-group (asked first time, skipped thereafter).
- **`assets/character-framing/` directory** — five framing files (bust, waist-up,
  three-quarter, seven-eighths, full-body) with prompt text; content sourced from the
  prior `assets/figure-proportion/` files.

### Changed
- **`figure_proportion` removed** — replaced by `figure_scale` (deck-wide scale, all
  figure types) and `character_framing` (character-only framing). A silent migration
  read path in `manage_config.py` maps existing `figure_proportion` configs on first
  load: `figure_proportion` value → `character_framing`; `figure_scale` set to
  `"inscribed-in-frame"` as default; `layers.figure.<group> = "true"` →
  `"character"`. The new schema is persisted on next write.
- **`STYLE_BLOCK` figure-block assembly** rewritten: character type gets figure-type
  preamble + Figure detail (pattern) + Face Style (pattern) + group addition +
  character_framing + figure_scale + split; non-character types get figure-type
  preamble + figure_scale + split only (FIG-08 + SPLT-03 patterns).
- **Reference docs updated** — `references/WIZARD-STEP-MAP.md` maps the new figure
  block steps (8a–8e) to components, layers, placeholders, and asset files;
  `references/POST-VALIDATION.md` replaces the figure-proportion checklist item with
  new checks for figure type preamble, figure scale, character framing, and split;
  `references/STYLE-COMPONENTS.md` (#5 Composition/rhythm) updated to reference
  `character_framing`, `figure_scale`, and `layers.split`.

- **Joker card support** — new `joker` card group, available in all four deck systems
  (French, German, Swiss, Latin). Selecting Joker as the rank runs a JOKER-specific
  wizard flow: Step 4 is replaced by Step 4.1 (Joker color: Multicolor / Red / Black,
  per-card) and Step 4.2 (Joker index glyph: `✪`, `★`, `Jkr`, `none`, or custom —
  persistent, deck-wide). The Joker uses its own JOKER template (non-reversible
  full-card single-figure composition, no suit fields, no central dividing line) and
  its own `[INDEX_LINE]` construction (corner glyph only, no rank+suit stack). A new
  `assets/courts/joker.md` supplies traditional Joker attributes (jester's cap, motley
  costume, bauble, theatrical pose). Joker defaults to fully decorated with a figure
  (like Court cards): all layers on except highlights. Added `index.symbol` (Joker
  corner glyph, named string — `star-in-circle` default), `index.type`
  (`standard`/`joker`), and extended `index.count` with `top-only` and `none` (Menu D2
  Joker placement) to `scripts/manage_config.py`, `config.json`,
  `assets/index/options.md`, `references/CONFIG.md`, `references/REFERENCE.md`, and
  `references/POST-VALIDATION.md`; updated `references/WIZARD-STEP-MAP.md`, all four
  deck files, and `TODO.md`. Added new Joker role variants: Big / Little / Wild.

## [3.19.0] - 2026-06-16

### Added
- New persistent `structure` setting (`full` default, or `illustration`) for users
  who composite the AI-generated artwork into their own SVG/HTML card template (with
  its own frame, corner indices, fonts, and margins). Under `structure: illustration`,
  the assembled prompt drops `[INDEX_LINE]` and `[FRAME_LINE]` entirely (without
  modifying `layers.frame.<group>` in `config.json`), replaces the templates' opening
  line with an illustration-only variant, and appends a fixed block to
  `[NEGATIVE_LIST]`; `[STYLE_BLOCK]` and the Center motif (including `[RANK_COUNT]`)
  are unaffected. Added a new "`structure` setting" section to
  `references/REFERENCE.md`, a field-reference row and persistent-settings entry to
  `references/CONFIG.md`, a `structure` step (config mode item 9) and assembly
  branches (steps 1–4) to `SKILL.md`, a Structure check to
  `references/POST-VALIDATION.md`, a cross-reference note to
  `references/WIZARD-STEP-MAP.md`, and `structure`/`STRUCTURE` handling to
  `scripts/manage_config.py` and the shipped `config.json` default profile.

### Changed
- **`[STYLE_BLOCK]` "Finish" lines now share `layers.technique.<group>`'s gate**
  instead of always being included. Technique and Finish both describe *how* the card
  is rendered (medium/linework vs. print-quality descriptor), so turning
  `layers.technique.<group>` off for a group now drops both together (e.g. a fully
  unstyled plain pip face has no medium or print-quality descriptor at all). Updated
  `references/REFERENCE.md` (step 7 of `[STYLE_BLOCK]` resolution, the Technique
  bullet, the "Each `assets/pattern/<style>.md` provides..." paragraph, and the
  Defaults table notes), `references/STYLE-COMPONENTS.md` (renamed "Technique vs.
  function" to "Technique & Finish vs. Decor/Ornaments/Highlights" and regrouped
  Finish with Technique), `assets/pattern/_adding-a-pattern.md` ("Technique & Finish
  vs. content layers" section and the "Finish" section's gating note),
  `references/POST-VALIDATION.md` (Style block integrity check),
  `references/WIZARD-STEP-MAP.md` (Step 5 row and the technique bullet), `SKILL.md`
  Step 6, and `references/example-pip-two.md`'s "Technique off" variant (Finish lines
  now also dropped).

## [3.17.0] - 2026-06-15

### Added
- New `layers.technique.<group>` layer (default `true` for all groups), gating the
  pattern's "Technique" section (renamed from "Center motif style" — the
  linework/medium rendering applied to whatever sits in the center: portrait, pip
  layout, or suit symbol alike). Independent of `layers.figure.<group>`: a card can
  have Technique on with Figure off (e.g. a plain pip card that still follows the
  pattern's linework), or Technique off with Figure on. Updated
  `scripts/manage_config.py` (added `"technique"` to `LAYERS`/`LAYER_DEFAULTS`),
  `config.json`, and `references/CONFIG.md` (field reference, dotted-key list,
  addition-cell description).

### Added
- `assets/pattern/_adding-a-pattern.md` "Technique" section now lists example
  mediums (linework, tonal/area-fill, painterly, textures, gradients, collage) with
  short sample phrases, to give pattern authors more vocabulary beyond "and so on".

### Changed
- Renamed the "Center motif style" pattern-file section to "Technique" across all
  five `assets/pattern/*.md` files, `assets/pattern/_adding-a-pattern.md`,
  `references/REFERENCE.md` (`[STYLE_BLOCK]` resolution — now step 5, grouped with
  the other gated layers instead of the "always" group — layer-list bullets, "Each
  `assets/pattern/<style>.md` provides..." paragraph, "Figure, face style &
  proportion", Defaults table), `references/STYLE-COMPONENTS.md` (#1, #6, #12, plus a
  new "Technique vs. function" section distinguishing *how* the center motif is drawn
  from *what*/*where* is added by Decor/Ornaments/Highlights/Finish),
  `references/WIZARD-STEP-MAP.md`, `references/POST-VALIDATION.md` (Style block
  integrity, Figure detail line, Face style line checks), the example prompts
  (including a new "Technique off" variant in `references/example-pip-two.md`
  showing the engraving/illustration lines dropped from a plain pip while Finish
  stays), and `SKILL.md`'s file map / Step 5 / Step 6 (documents
  `layers.technique.<group>` as a config-only per-group toggle/addition alongside
  `layers.background`/`layers.decor`).
- Restructured `assets/pattern/<style>.md` so pattern files contain no
  config/assembly logic: the figure-only "skin tones" line that used to be
  duplicated inside "Center motif style" and re-referenced via a
  `layers.figure.<group>`-aware "Figure-only line" annotation is now its own
  plain "Figure detail" section (or `(none)`), and "Face Style" no longer
  carries an "Applies only if `layers.figure.<group>` is on" sentence.
  Whether "Figure detail"/"Face Style" are folded into `[STYLE_BLOCK]` for a
  group is now decided entirely by `references/REFERENCE.md` via
  `layers.figure.<group>` — pattern files never mention `layers.*`. Updated
  all five `assets/pattern/*.md` files, `assets/pattern/_adding-a-pattern.md`,
  `references/REFERENCE.md` (layer descriptions, `[STYLE_BLOCK]` resolution
  steps 5-6, "Figure, face style & proportion", Defaults, PIP/ACE templates),
  `references/POST-VALIDATION.md` (added a dedicated "Figure detail line"
  check and updated "Style block integrity"/"Face style line"),
  `references/CONFIG.md`, `references/STYLE-COMPONENTS.md`,
  `references/WIZARD-STEP-MAP.md`, the example prompts, and `SKILL.md`'s file
  map / Step 5.

## [3.7.1] - 2026-06-13

### Changed
- Merged the `extras.<layer>.<group>` namespace into `layers.<layer>.<group>`:
  each cell is now a free-text string with three meanings — `"false"` (layer
  off for this group), `"true"` (layer on, no group-wide addition), or any
  other text (layer on, and that text is appended as the group's addition on
  top of the layer's own pattern/preset text). The `extras` namespace is
  dropped entirely; theme-derived fallback for ornaments/highlights/frame now
  triggers when the cell is exactly `"true"`. Updated `scripts/manage_config.py`
  (removed `EXTRA_LAYERS`, added `_migrate_layers_extras` to fold pre-3.13
  `extras.*` into `layers.*` on load), `config.json`, `references/CONFIG.md`,
  `references/REFERENCE.md`, `references/POST-VALIDATION.md`,
  `references/STYLE-COMPONENTS.md`, `references/WIZARD-STEP-MAP.md`,
  `references/example-pip-two.md`, `assets/frame/_adding-a-frame.md`,
  `assets/pattern/_adding-a-pattern.md`, and `SKILL.md` (Steps 6-8 and
  "Assembling the prompt").

### Added
- New `extras.figure.<group>` config field — a group-wide figure trait (e.g. "all
  court figures shown with a slight hunch") layered on top of the chosen pattern's
  Face Style line, applied only while `layers.figure.<group>` is `true`. Distinct
  from the pattern's Face Style (deck-wide) and `[CHARACTER_FEATURES]`/Steps 10-12
  (per-card). Updated `references/REFERENCE.md` ("Layers and `[STYLE_BLOCK]`
  assembly" step 6 and "Figure, face style & proportion"), `references/CONFIG.md`
  (schema, field reference, dotted-key list), `SKILL.md` Step 6, `config.json`, and
  `scripts/manage_config.py` (`EXTRA_LAYERS`)
- New `figure_proportion` config field and `assets/figure-proportion/` presets
  (`bust`, `waist-up`, `three-quarter`, `seven-eighths`, `full-body`, or custom
  text) — a deck-wide figure framing/cropping description, folded into
  `[STYLE_BLOCK]` right after the pattern's Face Style line and
  `extras.figure.<group>`, applied only while `layers.figure.<group>` is `true`.
  Asked once via a new persistent wizard Step 8 ("Figure proportion / framing"),
  gated by the figure check after Step 7; old Steps 8-13 are renumbered to 9-14
  throughout `SKILL.md` and the reference docs. Updated `references/REFERENCE.md`,
  `references/CONFIG.md`, `references/WIZARD-STEP-MAP.md`,
  `references/STYLE-COMPONENTS.md`, `references/POST-VALIDATION.md`,
  `references/example-court-king.md`, `config.json`, and `scripts/manage_config.py`
  (`DEFAULTS`, `PERSISTENT_KEYS`, `allowed_figure_proportions`, `options_for`)

### Fixed
- `SKILL.md` now defines `<SKILL_DIR>` (this file's own parent directory) and
  instructs all `scripts/manage_config.py` invocations to use
  `python3 <SKILL_DIR>/scripts/manage_config.py ...`. Previously the bare
  relative path `scripts/manage_config.py` resolved against the shell's
  current working directory, which fails whenever the agent isn't running
  from the skill's own install directory.

### Added
- New `assets/frame/boxed-index.md` frame preset — a thin perimeter border plus a
  separate thin border individually boxing each corner index, leaving a cross-shaped
  central field, with no stepped cut-ins. Now the default `frame` (replacing
  `stepped-corners`, which remains available as a preset). Updated `config.json`,
  `scripts/manage_config.py` (`DEFAULTS["frame"]`), `SKILL.md` Step 6's frame option
  list, and the default-frame references in `references/REFERENCE.md`,
  `references/POST-VALIDATION.md`, and `references/CONFIG.md`

### Changed
- Reduced `SKILL.md`'s token footprint: moved the 16-item post-validation checklist
  out to new `references/POST-VALIDATION.md` (linked from Step 8 of "Assembling the
  prompt" and the file map), and trimmed duplicated layer-defaults/theme-derivation/
  mood-resolution prose in Steps 6-7 that re-explained material already covered by
  `references/REFERENCE.md`'s "Layers and `[STYLE_BLOCK]` assembly" and "Theme-derived
  ornaments/highlights/frame" sections — those sections remain the single source of
  truth, SKILL.md now just points to them.

### Added
- New `metadata.description_claudeai` frontmatter field: a <= 200-char description used
  by `scripts/package-skill-claudeai.sh` when building the Claude.ai-compatible package
  (Claude.ai enforces a 200-char limit vs. the 1024 chars allowed for Claude Code /
  agentskills.io)
- New `extras.<layer>.<group>` config namespace generalizes the per-group free-text
  addition mechanism to every text layer: `extras.background.<group>` and
  `extras.decor.<group>` are new (config-only) additions appended after the pattern's
  Background/Decor lines, and `extras.mood.<group>` is a new (config-only) per-group
  mood addition appended after `[MOOD_LINE]` on top of the deck-wide `mood`.
- New `assets/frame/` library of border/frame presets (Stepped Corners (default),
  Double Rule, Ornate Scrollwork, Art Deco Geometric, Rope Twist), each providing a
  "Frame line" for `[FRAME_LINE]`, plus `_adding-a-frame.md` for custom presets. New
  persistent `frame` setting selects the preset (Step 6), and new per-group
  `frame_extra.<group>` config field (config-only, like `ornaments_extra`/
  `highlights_extra`) appends extra border text when `layers.frame.<group>` is on.
  `[FRAME_LINE]` is now resolved from `assets/frame/<frame>.md` + `frame_extra.<group>`
  instead of a single hardcoded line, with the same theme-derived fallback as
  ornaments/highlights when `theme` is set and `frame_extra.<group>` is empty. Updated
  `references/REFERENCE.md`, `references/CONFIG.md`, `references/STYLE-COMPONENTS.md`,
  `references/WIZARD-STEP-MAP.md`, `config.json`, and `scripts/manage_config.py`
  accordingly
- New `assets/mood/` library of mood/atmosphere presets (Gothic & Brooding, Warm &
  Whimsical, Eerie Nocturnal, Regal & Opulent, Serene Pastoral, Noir & Mysterious),
  each providing a "Mood line" for `[MOOD_LINE]`, plus `_adding-a-mood.md` for custom
  presets
- **Mood is now its own wizard step (Step 7), inserted after Step 6** and always
  asked regardless of whether the card has a figure. Offers preset moods from
  `assets/mood/` (or any other preset by name via "Other") as well as custom free
  text, and additionally asks which card groups (`court`/`pip`/`ace`) carry the mood,
  setting `layers.mood.<group>` directly — previously this was buried inside Step 6
  and the per-group `layers.mood.*` toggle was config-only. Renumbered the figure
  block to Steps 8-11, aspect ratio to Step 12, and image generator to Step 13;
  updated all cross-references in `references/REFERENCE.md`,
  `references/STYLE-COMPONENTS.md`, `references/WIZARD-STEP-MAP.md`, and
  `references/example-court-king.md`

### Changed
- **Wizard steps renumbered 1-12, sequential (no more 5/5a/5b/5c).** The
  decoration/mood/theme step is now Step 6, and the figure block (character,
  attributes, reference transfer, exclusions) is Steps 7-10, followed by aspect
  ratio (11) and image generator (12). The branch after Step 6 now checks
  `layers.figure.<group>` (true by default for `court`, configurable for `pip`/`ace`
  on transformation decks) instead of "is this a court card" — so Steps 7-10 apply
  to any card with a figure, not just court. Updated all cross-references in
  `references/REFERENCE.md`, `references/STYLE-COMPONENTS.md`,
  `references/WIZARD-STEP-MAP.md`, `references/example-court-king.md`,
  `assets/courts/*.md`, and `assets/engines/_config.md`
- **Face style is now per-pattern, not a config setting.** Each
  `assets/pattern/<style>.md` gains a "Face Style" section (placed after "Center
  motif style") describing how a figure's face reads in that pattern's aesthetic —
  folded into `[STYLE_BLOCK]` whenever `layers.figure.<group>` is true. Removed the
  generic `face_style.<group>` config field (`individual`/`archetypal`/`expressive`/
  `faceless`), its wizard question (formerly part of Step 5b), and the `[FACE_STYLE_LINE]`
  template slot in COURT/PIP/ACE — there's no longer a separate per-deck choice to
  make. Updated `references/REFERENCE.md`, `references/CONFIG.md`,
  `references/STYLE-COMPONENTS.md`, `references/WIZARD-STEP-MAP.md`, `config.json`,
  and `scripts/manage_config.py` accordingly

### Added
- New `references/WIZARD-STEP-MAP.md` mapping each wizard step (1-12) to the
  style components it touches (per `STYLE-COMPONENTS.md`), the
  `layers.*` it configures, the prompt placeholders it feeds, and the `assets/`
  files it loads; also notes silent/assembly-only mechanisms (e.g. `[INDEX_LINE]`)
  not covered by any wizard step. Linked from SKILL.md's reference file map

### Added
- New `references/STYLE-COMPONENTS.md` documenting the deck's style component
  model and mapping each component (medium, palette, era, mood, composition,
  line character, stylization, figure proportions, poses, costume, typage,
  pip/suit design, typography, decoration, theme) to the config field/layer/
  template that addresses it, flagging open gaps (figure proportions/plasticity,
  composition/rhythm, degree of stylization, pip/suit symbol design, pip/ace
  poses). Card-back design is excluded — planned as a separate card type
  alongside court/pip/ace. Linked from SKILL.md's reference file map

### Added
- **Profiles**: `config.json` now wraps settings in named profiles plus an
  `active_profile` pointer (`{"active_profile": "default", "profiles": {"default":
  {...}}}`), so users can save multiple "looks" (e.g. an Austrian gothic deck and a
  separate ukiyo-e deck) and switch between them without redoing the config wizard
- `scripts/manage_config.py` gained `profile list|show|create|switch|rename|delete|
  reset`, plus a `--profile <name>` flag on `get`/`set`/`unset`/`show` to target a
  non-active profile; a pre-3.0 flat `config.json` is auto-migrated into a `default`
  profile on first read
- The skill now ships `config.json` at its root, pre-populated with a `default`
  profile holding every factory setting — this file is the canonical source of
  default values (previously only documented, scattered across `CONFIG.md`'s field
  table and `manage_config.py`'s `DEFAULTS` dict)
- `scripts/install-skill.sh` backs up an existing `config.json` (as
  `config.json.bak.<timestamp>`) before extraction overwrites it with the shipped
  default, so upgrading the skill doesn't silently drop a user's saved profiles
- New **Profile** subcommand mode and a Step 0 (profile selection: continue, switch,
  or create-from-clone) in Config mode

### Changed
- `references/CONFIG.md`: documents the profile concept, schema, and CLI; lookup
  order is now "active profile → global `settings.json` → built-in defaults"
- SKILL.md Reset mode now clarifies that `--reset` deletes **all** profiles, and
  points to `profile reset <name> --yes` for clearing a single profile instead

### Added
- Two new configurable layers, `figure` and `mood`, extending the `layers.<layer>.<group>`
  matrix to 7×3: `figure` gates whether a card group's center motif carries a
  figure/portrait at all (and thus its figure-only style line and `[FACE_STYLE_LINE]`),
  default on for court / off for pip and ace (transformation decks can flip
  `layers.figure.pip`/`.ace` on); `mood` gates `[MOOD_LINE]`, default on everywhere but
  inert until `mood` is set
- New deck-wide free-text config fields `mood` (overall atmosphere, e.g. "gothic and
  brooding") and `theme` (deck-wide concept/symbolism, e.g. "celestial mythology"), each
  asked once in Step 5a and persisted
- New `face_style.<group>` config field (`individual` default, `archetypal`,
  `expressive`, `faceless`) controlling `[FACE_STYLE_LINE]` — asked once for
  `face_style.court` alongside Step 5b; see "Figure & face style resolution" in
  `references/REFERENCE.md` for the text mapping
- "Theme-derived ornaments/highlights": when `theme` is set and an enabled
  ornaments/highlights layer's `_extra` field is empty, a short thematic phrase is
  derived and reused consistently across the deck — explicit `_extra` values always win
- Two new pattern presets: `assets/pattern/art-nouveau.md` (Mucha-era Art Nouveau) and
  `assets/pattern/japanese.md` (Edo-period ukiyo-e woodblock)
- `_adding-a-pattern.md` now requires new patterns to be grounded in a specific era/
  cultural context, shaping palette, ornament motifs, and center-motif linework together

### Changed
- `references/REFERENCE.md`: `[STYLE_BLOCK]` resolution step 5 (Center motif style) now
  includes the figure-only line based on `layers.figure.<group>` instead of a hardcoded
  "drop for PIP/ACE"; added step 7 appending `[MOOD_LINE]`; the PIP "plain fallback"
  condition now also requires `layers.highlights.pip = false`; the Defaults table is now
  7×3; COURT/PIP/ACE templates gained a `[FACE_STYLE_LINE]` slot
- `scripts/manage_config.py`: `LAYERS`/`LAYER_DEFAULTS` extended with `figure`/`mood`;
  added `FACE_STYLES`, `mood`, `theme`, `face_style.<group>` to `DEFAULTS`,
  `PERSISTENT_KEYS`, `NESTED_GROUPS`, and `options_for()`
- `assets/pattern/_adding-a-pattern.md` and `austrian.md`: figure-only-line wording now
  references `layers.figure.<group>` instead of a hardcoded PIP/ACE drop
- SKILL.md Step 5a ("Card decoration, mood, and theme") and Step 5b gained mood/theme/
  face_style questions; pattern menu in Step 5 lists the two new presets; Assembling
  step 4 and the Post-validation checklist updated for `[MOOD_LINE]`,
  `[FACE_STYLE_LINE]`, and theme-derived ornaments/highlights

### Fixed
- Wizard steps now call the `AskUserQuestion` tool (tappable choices) instead of the
  non-existent `ask_user_input_v0`, which was never callable and made every
  fixed-choice step degrade to plain printed lists requiring the user to type an
  answer. Also documents `AskUserQuestion`'s 4-option-per-question limit and how to
  handle steps with more than 4 fixed choices (default + top ~3, "Other" for the rest)

### Added
- Layer-based visual system replacing the old monolithic `[STYLE_BLOCK]`: every card
  is now composed of **Background**, **Decor** (background pattern/accents),
  **Ornaments**, **Highlights/Overlays**, and **Frame**, plus the structural
  **Index** and **Center motif** (figure/pips/ace pip) layers that are always present
  — see "Layers and `[STYLE_BLOCK]` assembly" in `references/REFERENCE.md`
- `config.json` `layers.<background|decor|ornaments|highlights|frame>.<court|pip|ace>`
  boolean matrix controlling which layers contribute per card group, plus
  `ornaments_extra.<group>` and `highlights_extra.<group>` free-text fields
- New optional "Highlights / overlays" question in Step 5a — free text describing
  gilding/lacquer/glow/shine accents, applied across Court/Pip/Ace when given
- `assets/pattern/*.md` now define named layer sections (Background, Decor,
  Ornaments, Highlights, Center motif style, Finish) instead of one undifferentiated
  `[STYLE_BLOCK]`; `_adding-a-pattern.md` documents the new per-layer template
- Court cards' layers are now configurable via `--config` /
  `manage_config.py set layers.<layer>.court <bool>` (previously hardcoded "always
  full"), defaulting to fully on to match prior behavior

### Changed
- Replaced `content_style.{pip,ace}` / `frame.{pip,ace}` / `pip_decoration_extra`
  with the `layers.*` / `ornaments_extra.*` / `highlights_extra.*` schema;
  `scripts/manage_config.py` now supports arbitrary-depth dotted keys (deep merge,
  recursive get/set/unset/validate) instead of one-level nested groups
- Step 5a renamed "Card decoration layers" — the existing Plain/Decorated choice for
  number cards now bundles `layers.decor.pip` / `layers.ornaments.pip` /
  `layers.frame.pip` (was `content_style.pip` / `frame.pip`)
- `references/REFERENCE.md`: "Style block on PIP/ACE cards" replaced by "Layers and
  `[STYLE_BLOCK]` assembly", describing one resolution algorithm shared by
  Court/Pip/Ace; COURT template now uses `[FRAME_LINE]` instead of a hardcoded border
  line
- Updated `references/example-court-king.md`, `references/example-pip-two.md`, and
  `references/example-engine-variants.md` to the new layer ordering (Background →
  Decor → Ornaments → Highlights → Center motif style → Finish)

### Added
- `scripts/manage_config.py` — dependency-free CLI to read/write/validate `config.json` (`show`, `get`, `set`, `unset`, `validate`, `reset`, `options`, `path`); validates `deck`/`style` against the files in `assets/` and enforces the index/lettering/aspect enums
- New optional Step 9 — image generator selection (NanoBanana default, Stable Diffusion, Midjourney, DALL·E, kaze.ai, or custom), persisted via the new `image_generator` config field (`assets/engines/_config.md`)
- `assets/engines/` — one file per engine (`nanobanana`, `stable-diffusion`, `midjourney`, `dalle`, `kaze`) describing how to adapt the assembled prompt: negative-list placement (inline vs. separate block/`--no`/avoidance clause), aspect-ratio syntax (inline phrase, pixel size, `--ar`, fixed size), and extra suffix parameters
- New assembly step 7, "Engine-aware prompt formatting", and a matching Post-validation check, applying the chosen engine's deltas to the finished prompt before presenting it
- `references/example-engine-variants.md` — the King of Spades example adapted for Midjourney, Stable Diffusion, kaze.ai, and DALL·E
- `manage_config.py` gained `image_generator` as a persistent config key, with allowed values discovered from `assets/engines/`

### Changed
- Replaced the inline "Consistency check" assembly step with a full **Post-validation**
  checklist (placeholders, lettering, suit, attribute resolution, style block integrity,
  character description, negative list, aspect ratio, template match) that must pass
  before presenting the prompt — fix and re-check in place rather than presenting a
  failing draft
- Trimmed the config section of SKILL.md — removed lookup-order/schema/field tables already covered in `references/CONFIG.md`, leaving only short pointers and the per-mode CLI commands
- Restructured the COURT/PIP/ACE templates and assembly steps in `references/REFERENCE.md` and `SKILL.md` to follow general-purpose image-prompt best practices: format constraints (aspect ratio, full card visible, transparent background) and the style block now come first; the old `CHARACTER-SPECIFIC FEATURES` / `STANDARD <RANK> RANK ATTRIBUTES` / `ADDITIONAL / REPLACED ATTRIBUTES` / `TRANSFERRED FROM REFERENCE IMAGE` / `EXCLUSIONS` section labels are gone — traditional, additional, and reference-transfer attributes are now resolved into a single deduplicated, contradiction-free `[RESOLVED_ATTRIBUTES]` list, and all "no …" exclusions are merged into one trailing `[NEGATIVE_LIST]` (which engines with a negative-prompt field can take verbatim)
- Updated `references/example-court-king.md` to the new merged structure and added presenting-the-result tips (negative-prompt field, Midjourney `--ar`, optional shortened ~50–80 token version)
