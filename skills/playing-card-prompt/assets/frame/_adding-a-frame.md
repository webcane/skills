# Adding a new frame preset

Create `assets/frame/<name>.md` with a short title, an optional one-line description,
and a "Frame line" fenced block — a single comma-separated phrase (trailing comma kept)
describing the card's border/frame treatment, ending in `framing the index areas,` (or
an equivalent placement phrase). The wizard (Step 6) lists every `*.md` here (except
files starting with `_`) as a frame option, and uses the "Frame line" text verbatim as
`[FRAME_LINE]` / the `frame` config value when chosen.

```markdown
# Frame: <Display Name>

<optional one-line description shown while picking>

## Frame line
```
<border/frame phrase>, framing the index areas,
```
```

`[FRAME_LINE]` is its own template slot (not part of `[STYLE_BLOCK]`), included only
when `layers.frame.<group>` is `true` for the card's group — see "Layers and
`[STYLE_BLOCK]` assembly" in `references/REFERENCE.md`. If `extras.frame.<group>` is
set (free text, tunable via `--config`, e.g. `manage_config.py set extras.frame.court
"gold foil edging,"`), append it as its own comma phrase after the preset's "Frame
line" text.
Custom frame descriptions typed directly via `--config` (`frame` set to free text not
matching any preset) follow the same one-line, comma-terminated convention but aren't
saved as a file.
