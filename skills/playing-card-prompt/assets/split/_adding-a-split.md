# Adding a new split mode

Create `assets/split/<name>.md` with a short title, an optional one-line description,
and a fenced block — a single comma-terminated phrase describing the compositional
split layout. The file stem becomes an allowed value for `layers.split.<group>`.

```markdown
# Split: <Display Name>

<optional one-line description shown while picking>

## Split line
```
<compositional split phrase>,
```
```

**Important notes:**

- `none` and `false` produce no split text in the prompt. `false` means not yet
  configured (the wizard will ask); `none` means explicitly configured as no split
  (the figure is shown full without a split). Neither requires a file here.
- Split text is the outer compositional wrapper in STYLE_BLOCK. It is appended
  **after** `figure_scale` in the assembled text (order: figure_type → figure_scale → split).
- Only add a file for split modes that contribute actual prompt text.

Keep split phrases short and comma-terminated, consistent with the existing asset files.
