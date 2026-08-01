---
name: idea-to-concept
description: >
  Analyze, clarify, reformulate, or solve a problem using a structured reasoning method
  (socratic, TRIZ, Einstein, 5 Whys, six hats, inversion, reframing, etc.), generate
  alternative hypotheses, and validate them (HADI, ICE, RAT). Use when you need to
  stress-test a proposal, find hidden assumptions, simplify a concept, resolve a
  contradiction, find a root cause, validate a decision, or converge a raw idea into a
  well-formed, testable concept. Two modes: auto-recommend the best-fit method from the
  problem description, or explicit method selection (user choice or input parameter).
  Usable as a sub-agent by other skills — pass a structured analyze: block and receive a
  structured result.
metadata:
  author: webcane
  version: 1.3.0
  description_claudeai: >
    Analyze, clarify, or solve problems with structured reasoning methods (socratic, TRIZ,
    5 Whys, six hats, etc.), generate and validate hypotheses (HADI, ICE, RAT).
---

# Idea-to-Concept — Structured Reasoning Skill

A problem (or raw idea, proposal, or decision) enters. A well-formed result leaves: the
problem restated, analyzed through a rigorous method, with assumptions surfaced,
contradictions resolved or named, a reformulated concept or hypothesis — and, when a
hypothesis is produced, a suggested way to validate it (hadi, ice, rat).

## Three Modes

### Mode 0 — Help (`--help`)
Print the full method catalog — all available methods, when to use each, and the routing
decision rule — then stop. No analysis is run. Invoke with `--help` (user mode) or
`mode: help` (sub-agent mode). This is the built-in reference; useful before choosing a
method.

### Mode 1 — Auto (recommend and run)
Classify the problem type from the description, route to the best-fit method (see
`references/method-selection.md`), then run it end to end.

### Mode 2 — Explicit (method chosen)
The caller names the method (as a user choice or an input parameter). Run that method
even if auto-detection would have chosen differently.

## Input Format (Sub-agent Mode)

When spawned by another skill, you receive a block like:

```
idea-to-concept analyze:
  problem: "<the problem, proposal, or decision to work through>"
  mode: auto | <method-name>
  context: "<optional project constraints, prior decisions, relevant docs>"
```

Parse the block. `mode: auto` triggers Mode 1; a method name triggers Mode 2;
`mode: help` (or `mode: --help`) triggers Mode 0.

## Input Format (User Mode)

The user describes the problem directly, or invokes `/idea-to-concept <problem>`.
`/idea-to-concept --help` (or asking "help" / "list the methods") triggers Mode 0.
If `mode` is not given, default to auto.

## Method Selection (Mode 1)

Consult `references/method-selection.md` for the full routing table (20 methods, three
roles: analysis, generation, validation). Summary:

| Symptom in the problem | Method |
|---|---|
| Ambiguous terms, hidden assumptions, possible contradictions | socratic |
| Depth of understanding to verify | feynman |
| A conclusion claimed to follow from general rules | deduction |
| Two requirements in tension — both must be satisfied | triz |
| Concept too complex, unclear, or must age well | einstein |
| A visible symptom whose root cause is unknown | five-whys |
| An emotional or automatic reaction to a problem | three-questions |
| Unclear value — "is this actually useful?" | working-backwards |
| A claim that needs testing — "is this the simplest way?" | scientific-method |
| Fit with existing architecture / stated premises | logical-analysis |
| An empirically verifiable behavior claim | empirical-analysis |
| An overconfident claim that needs its opposite | dialectic |
| A proposal to review from every side | six-hats |
| A problem framed only as a liability | reframing |
| A hypothesis that only considers one direction | inversion |
| A stuck problem needing a fresh angle | analogy |
| A complex hypothesis to decompose and map | mind-map |
| A formed hypothesis to test fast | hadi |
| Many hypotheses — pick the most promising | ice |
| One do-or-die assumption — test it first | rat |

## Execution Protocol

### Step 1 — Restate the problem
Restate in one or two sentences. If you cannot, the problem is under-specified — flag it
and ask for the missing context before proceeding (Mode 1 may still choose a method; note
the restatement as a WARN).

### Step 2 — Load the method
Read the selected method from `references/methods/<method>.md`. Apply its steps to the
problem, substituting "the problem/proposal" wherever the method says "the concept".
Respect any project-specific context in the `context:` field (architecture docs,
terminology source, stated principles).

### Step 3 — Run the method
Execute each step of the method explicitly against the problem. Do not skip steps. Record
findings per step.

### Step 4 — Produce the result
Return a structured report (see Output Format). Where a method surfaces a contradiction,
assumption, or gap, name it precisely and, when possible, offer the resolution.

### Step 5 — Offer hypothesis validation
If the analysis produced a hypothesis (a reformulated concept, a new direction, a claim
about behavior), offer to run it through the validation methods — **hadi** (fast test
cycle), **ice** (prioritize when several hypotheses exist), **rat** (test the riskiest
assumption first). If the result is not a hypothesis, note in one line that validation
does not apply.

## Output Format

```
## idea-to-concept Report

**Problem (restated):** <one-to-two sentence restatement>

**Method used:** <method-name> (<auto | explicit>)

### Step-by-step findings
<per-step results of the method>

### Assumptions surfaced
- <assumption> — <why it matters>

### Contradictions / tensions
- <finding> — <resolution or open>

### Reformulated problem / concept
<the sharper statement this analysis produces>

### Hypothesis validation (if the result is a hypothesis)
- **hadi** — <why a fast test cycle fits, or "n/a">
- **ice** — <ranking note if multiple hypotheses, or "n/a">
- **rat** — <the riskiest assumption to test first, or "n/a">

### Recommendation
<what to do next, if any>
```

## Help Output Format (Mode 0)

When `--help` is invoked, return this catalog and stop — do not restate the problem, do
not load or run any method.

```
## idea-to-concept Help

**Usage:** `/idea-to-concept <problem>` · `/idea-to-concept <method> <problem>` · `/idea-to-concept --help`

**Modes:** `auto` (recommend + run) · `<method-name>` (explicit) · `--help` (this catalog)

### Method roles

- **Analysis** — clarify, simplify, and root-cause a problem into a well-formed concept or hypothesis.
- **Generation** — shift perspective and produce alternative hypotheses.
- **Validation** — prioritize and test a formed hypothesis (offer after a hypothesis exists).

### Methods — when to use which

#### Analysis — clarify, simplify, root-cause

| Method | Use when… |
|---|---|
| socratic | Terms ambiguous, assumptions hidden, contradictions possible ("it should work", "obviously") — lowest-cost probe; default tie-breaker |
| feynman | Depth of understanding to verify — "do I actually understand this?", "everyone knows how this works" |
| deduction | A conclusion claimed to follow from general rules ("follows from our principles", "by definition") |
| triz | Two requirements in tension, both must hold ("can't have both", "trade-off between X and Y") |
| einstein | Concept too complex, unclear, or must age well ("too complex", "hard to explain") |
| five-whys | A visible symptom whose root cause is unknown ("it keeps breaking", "why does this keep happening") |
| three-questions | An emotional or automatic reaction — pause and ask Why? (motive), What? (facts), How? (response) |
| working-backwards | Value unclear — "is this actually useful?", "who benefits?" |
| scientific-method | A simplicity/capability claim needs testing ("this is the simplest", "obviously better") |
| logical-analysis | Fit with existing architecture or stated premises ("does this fit?", "consistent with our architecture") |
| empirical-analysis | An empirically verifiable behavior claim ("always works", "no failure mode") |

#### Generation — shift perspective, produce alternatives

| Method | Use when… |
|---|---|
| dialectic | An overconfident claim that needs to face its opposite — thesis · antithesis · synthesis |
| six-hats | A proposal to review from every side — facts, emotion, risk, optimism, creativity, process |
| reframing | A problem framed only as a liability — "high price scares customers" vs. "high price filters for premium buyers" |
| inversion | A hypothesis that only considers one direction — "how to guarantee failure?" |
| analogy | A stuck problem; transfer a solution from a distant domain (chef → recommendations) |
| mind-map | A complex hypothesis to decompose and see non-linear connections |

#### Validation — prioritize and test (offer after a hypothesis exists)

| Method | Use when… |
|---|---|
| hadi | A formed hypothesis to test fast — Hypothesis → Action → Data → Insights |
| ice | Many hypotheses, need to pick the most promising — Impact × Confidence × Ease |
| rat | One do-or-die assumption — test the riskiest assumption first, cheapest and fastest |

### Decision rule (quick)
1. Names a tension ("but…", "conflicts with") → **triz**
2. Fuzzy terms / hidden assumption → **socratic**
3. "Is it worth it / who benefits" → **working-backwards**
4. Complexity / clarity / longevity → **einstein**
5. Depth-of-understanding check → **feynman**
6. "Follows from our principles" → **deduction**
7. Symptom without a root cause → **five-whys**
8. Emotional / automatic reaction → **three-questions**
9. Review from every side → **six-hats**
10. Obstacle that could be an asset → **reframing**
11. Overconfident claim → **dialectic**
12. Only one direction considered → **inversion**
13. Stuck, need a fresh angle → **analogy**
14. Complex web of ideas → **mind-map**
15. Simplicity or capability claim to test → **scientific-method**
16. Architectural fit → **logical-analysis**
17. Behavior measurable empirically → **empirical-analysis**

Ties → **socratic**

**After a hypothesis is formed:** test it fast → **hadi** · many hypotheses → **ice** · one do-or-die assumption → **rat**
```

## Usage Notes

- Be rigorous, not encouraging. The value of this skill is finding the flaw before it
  becomes expensive.
- If the problem resists the chosen method (produces nothing), say so and suggest the
  alternate method from the routing table.
- The validation methods (hadi, ice, rat) do not generate hypotheses — they are offered
  after a hypothesis exists. Do not route to them in Mode 1 before a hypothesis is
  formed.
- This skill is domain-agnostic. It works for language design, software architecture,
  DevOps changes, business decisions, and research questions.
