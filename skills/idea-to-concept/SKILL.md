---
name: idea-to-concept
description: >
  Analyze, clarify, reformulate, or solve a problem using a structured reasoning method
  (socratic, TRIZ, Einstein, working-backwards, scientific-method, etc.). Use when you
  need to stress-test a proposal, find hidden assumptions, simplify a concept, resolve a
  contradiction, validate a decision, or converge a raw idea into a well-formed concept.
  Two modes: auto-recommend the best-fit method from the problem description, or explicit
  method selection (user choice or input parameter). Usable as a sub-agent by other
  skills — pass a structured analyze: block and receive a structured result.
metadata:
  author: webcane
  version: 1.1.0
  description_claudeai: >
    Analyze, clarify, or solve problems with structured reasoning methods (socratic, TRIZ,
    Einstein, etc.). Stress-test proposals, surface assumptions, resolve contradictions,
    turn ideas into concepts.
---

# Idea-to-Concept — Structured Reasoning Skill

A problem (or raw idea, proposal, or decision) enters. A well-formed result leaves: the
problem restated, analyzed through a rigorous method, with assumptions surfaced,
contradictions resolved or named, and a reformulated concept or recommendation.

## Two Modes

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

Parse the block. `mode: auto` triggers Mode 1; a method name triggers Mode 2.

## Input Format (User Mode)

The user describes the problem directly, or invokes `/idea-to-concept <problem>`.
If `mode` is not given, default to auto.

## Method Selection (Mode 1)

Consult `references/method-selection.md` for the full routing table. Summary:

| Symptom in the problem | Method |
|---|---|
| Ambiguous terms, hidden assumptions, possible contradictions | socratic |
| Two requirements in tension — both must be satisfied | triz |
| Concept too complex, unclear, or must age well | einstein |
| Unclear value — "is this actually useful?" | working-backwards |
| A claim that needs testing — "is this the simplest way?" | scientific-method |
| Fit with existing architecture / stated premises | logical-analysis |
| An empirically verifiable behavior claim | empirical-analysis |

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

### Recommendation
<what to do next, if any>
```

## Usage Notes

- Be rigorous, not encouraging. The value of this skill is finding the flaw before it
  becomes expensive.
- If the problem resists the chosen method (produces nothing), say so and suggest the
  alternate method from the routing table.
- This skill is domain-agnostic. It works for language design, software architecture,
  DevOps changes, business decisions, and research questions.
