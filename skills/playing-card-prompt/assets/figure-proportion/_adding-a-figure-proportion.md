# Adding a new figure proportion preset

> **Deprecated (v4):** `figure_proportion` is no longer a live, settable field.
> It has been replaced by two persistent fields: `figure_scale` (applies to ALL
> figure types) and `character_framing` (character-only) — see those fields in
> `references/CONFIG.md`. A pre-4.0 `config.json` that still has `figure_proportion`
> is migrated automatically on load (`_migrate_figure_proportion` in
> `manage_config.py`). This directory's presets are kept only to back that
> migration path and are no longer offered as a live wizard choice; new presets
> should be added under `assets/character-framing/` instead (see
> `assets/character-framing/_adding-a-character-framing.md` if present, or follow
> the `character_framing` docs in `references/CONFIG.md`).

This format is preserved below for historical/migration reference only — it is no
longer wired into the live wizard. A legacy preset file looked like this:

```markdown
# Figure Proportion: <Display Name>

<optional one-line description shown while picking>

## Figure proportion line
```
<framing/crop phrase>,
```
```

Pre-4.0, `figure_proportion` was folded into `[STYLE_BLOCK]`, immediately after the
pattern's "Face Style" line, only when `layers.figure.<group>` was `true` for the
card's group. That role is now split across `character_framing` (character-only
framing/crop) and `figure_scale` (deck-wide scale, all figure types) — see both in
`references/CONFIG.md` and "Figure type, face style, framing & scale" in
`references/REFERENCE.md` for the current assembly order.
