# ID scheme

IDs are the join key between runs, between artifacts and between languages. They are stable
and monotonically assigned; they are never reused and never renumbered.

## Namespaces

| Prefix | Meaning | Where defined | Where referenced |
|--------|---------|---------------|------------------|
| `C1..Cn` | contradiction | B1 table | A, D, E, decision.md |
| `J1..Jn` | quantitative jump | B2 table | D, E, decision.md |
| `S1..Sn` | synthesis | B3 table | D, E, decision.md |
| `T1..Tn` | new tension | E table | H, decision.md |
| `AX1..AX19` | axis | Task C, fixed | D, E, F, decision.md |
| `SRC-nn` | source | manifest.json | every citation |

Hypotheses in Task G are numbered `H1..H7` in the first column but are not referenced across
languages; they stay local to the study.

## Assignment rules

1. Assign IDs in the order the item appears in the table, starting at 1.
2. Determine the ID map **before** writing prose. Run 1 fixes `C*`, `J*`, `S*`; Run 2 adds
   `T*` and may not change any earlier ID.
3. Gaps are allowed; renumbering is not. If a contradiction is deleted, keep the number and
   write `C4 — withdrawn: <reason>` in place rather than shifting C5 to C4.
4. Referencing an ID that is not defined in the study is a validation error. If you need a
   forward reference (Run 1 citing a `T*` from Run 2), write `T?` and resolve it in Run 2 —
   the validator rejects a bare `T?` in the final stage.
5. `AX` references are global and need no definition beyond Task C.

## Two-run protocol

Split only when the output is truncated:

- **Run 1** writes frontmatter, Task A, Task B (B1–B3). It ends by writing the ID map to
  `studies/<lang>/runs/run1-ids.json` (`{"C": [...], "J": [...], "S": [...]}`).
- **Run 2** reads that map first, then writes Tasks C–H, then `decision.md`.
- Both runs write into the same files on disk. Chat history is not the handoff; the artifact
  directory is.

If Run 2 needs a new contradiction discovered while filling Task C, it appends `C(n+1)` and
notes the addition in `runs/run2-additions.md`. It does not reorder.

## Cross-language merging

Language-local IDs never collide because the merge key is `(language, id)`. When a synthesis
is shared across languages (e.g. "errors as values"), do not reuse the ID; it is a new row in
`matrix.md` with the same axis reference and a different language.
