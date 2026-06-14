# Adding a new figure proportion preset

Create `assets/figure-proportion/<name>.md` with a short title, an optional one-line
description, and a "Figure proportion line" fenced block — a single comma-separated
phrase (trailing comma kept) describing how much of the figure is shown and how it's
cropped/framed within the card. The wizard (Step 8) lists every `*.md` here (except
files starting with `_`) as a figure proportion option, and uses the "Figure
proportion line" text verbatim as the `figure_proportion` config value when chosen.

```markdown
# Figure Proportion: <Display Name>

<optional one-line description shown while picking>

## Figure proportion line
```
<framing/crop phrase>,
```
```

`figure_proportion` is folded into `[STYLE_BLOCK]`, immediately after the pattern's
"Face Style" line, only when `layers.figure.<group>` is `true` for the card's group —
see "Layers and `[STYLE_BLOCK]` assembly" in `references/REFERENCE.md`. If
`figure_proportion` is empty (the default), nothing is added and the figure's framing
is left to the model's own interpretation, as before.

Custom proportion descriptions typed directly via `--config` (`figure_proportion` set
to free text not matching any preset) follow the same one-line, comma-terminated
convention but aren't saved as a file.
