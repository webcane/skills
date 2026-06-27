# Adding a new figure type

Create `assets/figure-type/<name>.md` with a short title, an optional one-line
description, and a fenced block — a single comma-terminated phrase describing the
central subject type. The file stem becomes an allowed value for `layers.figure.<group>`.

```markdown
# Figure Type: <Display Name>

<optional one-line description shown while picking>

## Figure type line
```
<central subject phrase>,
```
```

**Special case — `character.md`:** The character type is the only figure type whose
STYLE_BLOCK also pulls in the pattern's "Face Style" section and `character_framing`
(from `assets/character-framing/`). Building, animal, and custom types receive only
their figure-type line plus `figure_scale` and `split`. When adding a new type that
also needs character-specific fields, add the gate logic to the STYLE_BLOCK assembly
in SKILL.md.

Keep prompt phrases short and comma-terminated, consistent with the rest of the
asset files. Do not include multi-sentence descriptions or newlines inside the fenced
block.
