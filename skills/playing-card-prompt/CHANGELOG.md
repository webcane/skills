# Changelog — playing-card-prompt

All notable changes to this skill. Released per skill as tag
`playing-card-prompt/v<version>`. The version in `SKILL.md` frontmatter
(`metadata.version`) is the source of truth.

## [Unreleased]

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
