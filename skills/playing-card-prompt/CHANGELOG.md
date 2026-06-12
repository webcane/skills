# Changelog — playing-card-prompt

All notable changes to this skill. Released per skill as tag
`playing-card-prompt/v<version>`. The version in `SKILL.md` frontmatter
(`metadata.version`) is the source of truth.

## [Unreleased]

### Added
- `content_style.pip`/`content_style.ace` and `frame.pip`/`frame.ace` config fields (default: pip = off/off, ace = on/on) controlling how `[STYLE_BLOCK]` and the bordered-index-area line resolve on PIP/ACE cards
- New persistent wizard Step 5a — "PIP card decoration": **Plain** (default; suit-color pips only, no accent colors, no border) or **Decorated** (keeps the style's accent line, adds the border, and asks for `pip_decoration_extra` — free text describing what extra decoration to add)
- `references/example-pip-two.md` — fully assembled PIP example (Two of Spades, Austrian style) showing both the plain default and the decorated variant
- "Style block on PIP/ACE cards" section in `references/REFERENCE.md` defining `[STYLE_BLOCK_PIP]`/`[STYLE_BLOCK_ACE]`/`[FRAME_LINE]` resolution from the pattern's accent/figure-only lines

### Changed
- Each `assets/pattern/*.md` now marks which `[STYLE_BLOCK]` line is the "accent" line (extra decoration, suppressed on plain PIP/ACE) and which (if any) is "figure-only" (e.g. Austrian's `warm ochre skin tones,` — always dropped on PIP/ACE, which have no portrait)
- `scripts/manage_config.py` generalized its nested-group handling (previously `index`-only) to also cover `content_style` and `frame`, and added free-text support for `pip_decoration_extra`

### Fixed
- Reworded the figure-specific wording in each `[STYLE_BLOCK]` (Austrian, French, English patterns) so the same verbatim block reads correctly on PIP/ACE cards, which have no portrait — "on face, hair, costume and fabric folds" / "stylized faces" became generic phrasing covering pip symbols and ornamental details
- Removed the `thin black horizontal dividing line through the exact center of the card,` line from the PIP template — that line exists for COURT cards' reversible two-way (double-headed) layout and doesn't apply to pip cards, which the ACE template already omits it for
- PIP cards now default to a plain look (no extra accent colors, no border) matching traditional simple number-card designs, instead of inheriting the full court-card style block's decoration

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
