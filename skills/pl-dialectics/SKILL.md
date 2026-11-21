---
name: pl-dialectics
description: >
  Build a dialectical study of a programming language from primary sources: snapshot what the
  language is, reconstruct its contradictions (C), quantitative jumps (J) and syntheses (S) via
  the three laws, place it on a fixed 19-axis grid (AX1-AX19), derive new tensions (T), propose
  comparison axes and falsifiable hypotheses, and emit a stable comparability block plus a
  7-section decision record for the language being designed (Orthon). Use when asked to study
  why a language is the way it is, to compare languages structurally, to run a
  "language dialectics" report, or to decide what to borrow from Rust, Zig, Swift, Kotlin or
  any other language.
license: MIT
compatibility: Requires Python 3.11+ (stdlib only) and network access for source snapshots.
metadata:
  author: webcane
  version: 1.0.0
  description_claudeai: >
    Dialectical study of a programming language: contradictions, jumps, syntheses, 19-axis
    grid, new tensions, and a 7-section decision record for Orthon.
---

# PL Dialectics — language study pipeline

One run studies one language. The language name is the only variable; everything else —
headings, columns, ID namespaces, axis set — is fixed so that studies of different languages
can be merged without translation.

Rules and task definitions live in `references/method.md`. This file is the operating
procedure: artifacts, gates, order of operations. Do not restate the method in chat.

## Artifacts

```
studies/<slug>/
  manifest.json          # sources: id, kind, title, locator, sha256
  MANIFEST.md            # human rendering of the manifest
  sources/SRC-nn.*       # snapshots + .txt extraction
  study.md               # Tasks A-H, the comparable report
  decision.md            # 7-section record: what Orthon should take
  comparability.json     # machine-readable Task H + axis positions
  runs/run1-ids.json     # ID map written at the end of Run 1
studies/matrix.md        # cross-language axis grid
studies/synthesis/decision.md  # cross-language decision, written last
```

Per-language `decision.md` files are never merged into one another. The synthesis document
references them; it does not absorb them.

## Procedure

### 1. Initialise

```bash
scripts/init_study.py --lang "<language>" [--era "<era>"] [--root studies]
```

The script writes the exact skeleton from `references/report-template.md` and an empty
manifest. It refuses to overwrite an existing study without `--force`; never pass `--force` on
a study that already has content.

### 2. Collect sources (gate G0)

Five classes are mandatory: `spec`, `essay`, `paper` (≥2), `release`, `retro`.
See `references/sources.md` for what counts.

```bash
scripts/add_source.py --lang <slug> --kind spec --url <url> --title "<title>"
scripts/add_source.py --lang <slug> --kind paper --file ~/papers/x.pdf --title "<title>"
scripts/check_sources.py --lang <slug>
```

Do not start writing while `check_sources.py` exits non-zero. A thin source base is the main
cause of a study that reads well and compares badly.

### 3. Fix the ID map

Before prose, decide the 3–5 contradictions (`C*`), their jumps (`J*`) and syntheses (`S*`) and
write `runs/run1-ids.json`:

```json
{"C": ["C1", "C2", "C3"], "J": ["J1", "J2"], "S": ["S1", "S2"]}
```

Renumbering later is forbidden; see `references/id-scheme.md`.

### 4. Run 1 — Tasks A + B

Write A, B1, B2, B3 into `study.md`. Then:

```bash
scripts/validate_report.py --lang <slug> --stage run1
```

If the output is truncated mid-report, stop at a task boundary and continue in Run 2 of the
same directory. Chat history is not the handoff — the files are.

### 5. Run 2 — Tasks C–H

Read `runs/run1-ids.json` first. Fill the 19 axes, the 9 classical problems, new tensions,
category discovery, hypotheses and the comparability block. Then:

```bash
scripts/validate_report.py --lang <slug> --stage final --emit-json
```

`--emit-json` writes `comparability.json`. Run it only after the study validates.

### 6. Decision record

Write `decision.md` using `references/decision-template.md` (7 sections, bilingual headings,
English body). Every decision cites `S*`, `T*` or `AX*`; a decision with no backlink is an
opinion.

```bash
scripts/validate_report.py --lang <slug> --scope decision
```

### 7. Merge and review (after ≥2 languages)

```bash
scripts/merge_matrix.py --root studies
scripts/self_review.py --root studies
```

`merge_matrix.py` refuses to mix schema versions. `self_review.py` reports pass/fail per
criterion and never edits a study.

## Scripts

All scripts are self-documenting: `--help` lists every flag with an example, and every error
names the problem, the reason and the fix. **When a script exits non-zero, read its message and
run `--help` before retrying.** Do not guess flags; do not bypass a gate.

| Script | Purpose | Exit codes |
|--------|---------|-----------|
| `init_study.py` | create the artifact skeleton | 0 ok, 2 usage, 5 refused (exists) |
| `add_source.py` | snapshot one source, assign `SRC-nn` | 0 ok, 2 usage/duplicate, 3 unreachable |
| `check_sources.py` | gate G0, per-class coverage | 0 ok, 3 no manifest, 4 incomplete |
| `validate_report.py` | structure, IDs, citations, axes, decision; emits JSON | 0 ok, 3 missing, 4 invalid |
| `merge_matrix.py` | cross-language matrix (md + csv) | 0 ok, 3 no studies / schema mismatch |
| `self_review.py` | pilot metrics and verdicts | 0 always (report) |
| `install_commands.py` | copy the slash commands into a host | 0 ok, 2 usage |

Scripts share `scripts/_common.py` and use the standard library only.

## Hard rules

1. Cite as `[Source: SRC-nn <title>, <locator>]`. Never cite a source missing from the
   manifest. Unsupported inference is `[UNSOURCED]`.
2. Keep the three layers apart: declared intent, actual mechanism, historical outcome.
3. If a law has no instance, write `NO CLEAR INSTANCE` and explain. An empty cell is a defect.
4. Never rename headings, reorder tasks, add axes to Task C, or renumber IDs.
5. Output in English; keep the language's own terminology before the PLT term.
6. Task A is capped at 150 words. Long snapshots are where ungrounded generalities hide.
7. Do not claim a gate passed unless the script said so.

## Optional slash commands

`assets/commands/pl-study.md` and `pl-merge.md` are thin wrappers. Install them with:

```bash
scripts/install_commands.py --host opencode --dest .
scripts/install_commands.py --host claude --dest .
```

The skill is fully usable without them; the Agent Skills standard has no command concept, so
commands are a host extension, not part of the portable package.

## Non-goals

- Not a language tutorial and not a ranking. Positions are descriptive, never scored.
- Not a substitute for reading the specification: the snapshot is evidence, not a summary of
  everything.
- Not a place to design Orthon. Design decisions go to `decision.md`, one language at a time.
