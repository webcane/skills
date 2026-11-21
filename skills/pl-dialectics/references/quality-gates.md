# Quality gates

Run the gates in order. Do not skip a gate because the report "looks fine" — the whole point
is that a structurally valid report is comparable and a beautiful report is not.

## G0 — Sourcing

```bash
scripts/check_sources.py --lang <lang>
```

Pass: all five classes at minimum. Fail: exit 4 with a per-class table.
If a class genuinely does not exist, record the exception in `runs/source-exception.md` before
reducing the minimum.

## G1 — Skeleton and ID map

```bash
scripts/init_study.py --lang <lang>
```

Before writing prose, fill `runs/run1-ids.json` with the planned `C*`, `J*`, `S*` ids. This is
cheap and prevents renumbering later. Not enforced by a script, enforced by review.

## G2 — Run 1 (Tasks A + B)

```bash
scripts/validate_report.py --lang <lang> --stage run1
```

Pass: A and B present, A ≤150 words, B1–B3 tables well-formed, IDs unique.
Write `runs/run1-ids.json` before ending the run.

## G3 — Run 2 (Tasks C–H)

```bash
scripts/validate_report.py --lang <lang> --stage final
```

Pass: 19 axes, 9 problems, 3–7 hypotheses, Task H with 8 fields, no dangling IDs.
If truncated, stop at a task boundary and resume with the same stage flag; never renumber.

## G4 — Comparability emission

```bash
scripts/validate_report.py --lang <lang> --emit-json
scripts/merge_matrix.py --root studies
```

Pass: `comparability.json` exists, schema versions match across studies, matrix has no empty
axis cells. A warning about empty cells is acceptable for a single-language run; it is a
failure once three languages are in.

## G5 — Decision record

```bash
scripts/validate_report.py --lang <lang> --scope decision
```

Pass: 7 sections in order, non-empty, at least one ID backlink.

## G6 — Self-review (after the pilot)

```bash
scripts/self_review.py --root studies
```

| Criterion | Pass condition |
|-----------|----------------|
| structure | zero validator errors |
| grounding | `[UNSOURCED]` share ≤ 25% of source markers |
| axes | 19/19 positions filled |
| decision | 7/7 sections |
| traceability | decision.md has ID backlinks |
| sources | every class at minimum |

Self-review **reports**; it never edits a study. Fix findings by editing the study, then
re-run the gate.

## Manual checks a script cannot do

- Does Task B1 name real design decisions, or restate the axis grid?
- Does B3's last column name a new contradiction, or a benefit dressed as one?
- Does Task D's "dialectical move" column say something other than "synthesis" nine times?
- Does Task E's synthesis read as a hypothesis, not as a roadmap promise?
- Does Task G's falsification test name a language and an observation, or just say "compare"?