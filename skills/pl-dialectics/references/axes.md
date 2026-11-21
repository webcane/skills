# Axes AX1–AX19 and the third-pole protocol

Axes are fixed for every study. Do not add, rename, merge or reorder them inside `study.md`.
New axes go to Task F only; promotion into the seed list requires a schema version bump.

| ID | Axis | Pole A | Pole B |
|----|------|--------|--------|
| AX1 | Identity | nominal | structural |
| AX2 | Ownership | GC | manual |
| AX3 | Mutation | mutable-by-default | immutable-by-default |
| AX4 | Evaluation | eager | lazy |
| AX5 | Visibility | closed module | open |
| AX6 | Lifetime | GC-liveness | deterministic destruction |
| AX7 | Data primitives | minimal built-in | rich built-in |
| AX8 | Data operations | library-level | language-level |
| AX9 | Typing discipline | dynamic | static |
| AX10 | Behavior attachment | methods-on-class (OOP) | functions-on-data (FP) |
| AX11 | Data extensibility | open (subtyping) | closed (ADT) |
| AX12 | Null | null sentinel | Option |
| AX13 | Errors | exceptions | monadic Result |
| AX14 | Concurrency / async | synchronous | colored async |
| AX15 | Metaprogramming | text macros | AST macros |
| AX16 | Syntax philosophy | symbolic | verbose |
| AX17 | Library boundary | core-bloat | tiny-core |
| AX18 | Module & effects | implicit effects | explicit effects |
| AX19 | Memory safety/perf | unsafe-fast | safe-slow |

## Position values

Use exactly one of:

- `THESIS` — the language adopts Pole A as its primary mechanism.
- `ANTITHESIS` — the language adopts Pole B as its primary mechanism.
- `SYNTHESIS` — the language holds both poles with a mechanism that preserves each.
- `N/A` — the axis does not apply; state why in Justification.
- `THIRD POLE: <name>` — the language resolves the pair by moving outside it.

A cell may combine, e.g. `SYNTHESIS (THIRD POLE: comptime)`, when both facts matter. Never
leave a cell blank: a blank is indistinguishable from an oversight.

## Known multi-stage axes

These seven carry a documented third pole. Put it in the position cell, not in Pole A/B.

| Axis | Third pole family | What it means |
|------|-------------------|---------------|
| AX2 | borrow checker / region / linear types | ownership checked statically instead of GC or manual free |
| AX3 | controlled mutation (`val`/`var`, `let mut`) | mutability is per-binding and checked, not per-type default |
| AX9 | gradual typing | static and dynamic coexist with boundary checks |
| AX10 | traits / protocols / type classes | behavior attached to type families, not classes or free functions |
| AX13 | error unions / effect types | errors are values but not a monadic wrapper |
| AX14 | colorless async / structured concurrency | async is not a function-color split |
| AX15 | syntactic comptime / hygienic AST macros | expansion at type-check time with typed input |

## Rules

1. One axis, one position. If two mechanisms compete inside the language (e.g. `unsafe` and
   safe Rust), the position describes the default surface, and Evidence names the escape.
2. Justification is one sentence. Evidence is a citation, not an argument.
3. A language can be `THESIS` on one axis and `ANTITHESIS` on another; there is no required
   coherence. Coherence claims belong in Task A or H, and must be argued.
4. Do not score. No "more modern", "better". Position is descriptive.
5. If sources disagree about the position, record `[DISPUTED]` and cite both sides.
6. Task F candidates are not scored here. They are proposals for the next schema version.
