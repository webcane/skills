# Adding a new figure-scale preset

Create `assets/figure-scale/<name>.md` with a short title, an optional one-line description,
and a fenced block — a single comma-terminated phrase describing how the figure sits in the
card frame. The file stem becomes an allowed value for `figure_scale`.

```markdown
# Figure scale: <Display Name>

<optional one-line description shown while picking>

## Scale phrase
```
<figure scale prompt phrase>,
```
```

**Important notes:**

- The assembler looks up the file by `figure_scale` key and injects the phrase verbatim.
  Custom free text (any value not matching a file stem) is used as-is — no file needed.
- Scale phrases describe the spatial relationship between the figure and the card border.
  Keep them short, precise, and comma-terminated, consistent with the existing presets.
- `figure_scale` is deck-wide (set once in Step 8a, applied to every figure card).
- The four built-in presets are: `inscribed-in-frame`, `full-bleed`, `small-centered`,
  `cross-a-frame`.
