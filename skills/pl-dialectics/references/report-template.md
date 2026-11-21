# study.md — exact skeleton

This file is the single source of truth for headings and columns. `init_study.py` writes it;
`validate_report.py` enforces it. Any edit here is a schema change and requires a version bump.

```markdown
---
schema_version: "1"
language: "{{LANGUAGE}}"
slug: {{slug}}
era: "{{FOCUS_ERA}}"
created: YYYY-MM-DD
---

# {{LANGUAGE}} — dialectical study

## TASK A — SNAPSHOT (≤150 words)

## TASK B — THE THREE LAWS

### B1. Unity and struggle of opposites — WHY (source of development)

| ID | Contradiction | Pole A (thesis) | Pole B (antithesis) | Where they clash | Impulse produced | Evidence |

### B2. Quantity → quality — HOW (mechanism)

| ID | Gradual accumulation | Threshold crossed | Qualitative jump | What jumped | Milestones | Evidence |

### B3. Negation of negation — WHERE (vector, spiral)

| ID | Negated | Negation of the negation | Preserved at a higher level | New contradiction | Evidence |

## TASK C — AXIS GRID (fixed seed taxonomy)

| Axis ID | Axis | Pole A | Pole B | Position | Justification | Evidence |

## TASK D — CLASSICAL PROBLEMS

| Problem | Solution | Dialectical move | Evidence |

## TASK E — NEW TENSIONS

| ID | Tension | Pole A | Pole B | Why not dissolved | Possible synthesis | Evidence |

## TASK F — CATEGORY DISCOVERY

## TASK G — HYPOTHESES

| ID | Hypothesis | Evidence | Falsification test |

## TASK H — COMPARABILITY BLOCK

| Field | Value |
```

## Content rules per section

- **A** — prose only, maximum 150 words, at least two citations. No tables.
- **B1** — 3 to 5 rows. Each row names a concrete design decision, not a vague theme.
- **B2** — one row per qualitative jump. `Milestones` carries versions, dates, RFC ids.
- **B3** — last column is mandatory and must name a *new* contradiction, not a benefit.
- **C** — exactly 19 rows, `AX1` through `AX19`, in order. No extra axes.
- **D** — exactly the 9 listed problems, in the listed order.
- **E** — 3 or more rows. `Possible synthesis` starts with `HYPOTHESIS:`.
- **F** — either candidate axes with poles and position, or the single sentence
  `None identified.`
- **G** — 3 to 7 rows, each with a falsification test another language could run.
- **H** — the 8 fields in the specified order, values are compact ID lists or one sentence.

## Run split

`runs/run1-ids.json` is written at the end of Run 1 and read at the start of Run 2. The file is
not part of the report and is not validated.
