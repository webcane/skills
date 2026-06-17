# Adding a new character framing preset

Create `assets/character-framing/<name>.md` with a short title, an optional one-line
description, and a "Character framing line" fenced block — a single comma-terminated
phrase describing how much of the character is shown and how they're cropped or framed
within the card. The wizard lists every `*.md` here (except files starting with `_`) as
a character framing option, and uses the "Character framing line" text verbatim as the
`character_framing` config value when chosen.

```markdown
# Character Framing: <Display Name>

<optional one-line description shown while picking>

## Character framing line
```
<framing/crop phrase>,
```
```

`character_framing` is folded into `[STYLE_BLOCK]` only when
`layers.figure.<group>` is `"character"` — it is character-specific and skipped for
building, animal, and custom figure types. If `character_framing` is empty (the
default), nothing is added and the figure's framing is left to the model's own
interpretation.

Custom framing descriptions typed directly via `--config` (`character_framing` set
to free text not matching any preset) follow the same one-line, comma-terminated
convention but aren't saved as a file.
