# Empirical Analysis

> A claim about observable behaviour cannot be assumed from intuition —
> it must be proven. Skip the structural scan and the round-trip test,
> and a proposal that "feels right" may hide the exact ambiguity that
> causes failure once real use begins.

## Origin

Empirical Analysis combines two established engineering practices,
applied here to problem analysis rather than to running code.
**Structural (static) analysis** inspects a specification for known
defect patterns without executing anything — the same discipline used
by linters and formal reviewers to catch ambiguity early. **Round-trip
testing** verifies that a representation survives serialization and
deserialization without loss of information — the same guarantee schema
and protocol designers demand before trusting a format to carry meaning
intact across a boundary. Applied together, they let a proposal be
judged against evidence rather than against how sound it seems.

## Application to Problem Analysis

When evaluating an empirically verifiable claim (correctness,
reliability, generability), Empirical Analysis formalises the two
complementary approaches, then scores the result against explicit
criteria.

### 1. Run the Structural Scan

Examine the proposal's specification for known defect patterns:
ambiguity, special cases, context-dependent behaviour, and
format misalignment. Walk each sub-construct in turn and record which
are clean and which carry risk — an open, undecided concrete form is
exactly the "context-dependent behaviour not yet fixed" pattern this
scan is built to catch.

### 2. Attempt the Round-Trip

Express the proposal fully in a machine-readable or canonical form
(schema, grammar, contract), then ask whether a consumer relying only
on that form would have enough information to reproduce the behaviour
correctly. Distinguish three outcomes per sub-construct: a **full**
round-trip (the form carries every constraint), a **partial** round-trip
(some constraint is lost or under-specified), or **no** round-trip (the
behaviour cannot be represented in that form at all).

### 3. Score Against Explicit Criteria

Reproduce the claim's own criteria — do not invent new criteria or
reorder existing ones. Score each as pass / flag / fail.

### 4. Determine the Verdict

Read the scored table as a whole:

- **All Pass** — the claim holds outright.
- **Any Flag with no Fail** — the claim may proceed; record the
  flagged criterion's root cause so it can be resolved before the final
  verdict.
- **Any Fail** — the proposal must be revised to address the specific
  fail condition before re-entering the test.

## When to Use

This method suits empirically verifiable behaviour claims: "it will
generate correctly", "always works", "no failure mode".

## Output

The structural-scan results, round-trip outcomes per sub-construct, the
scored criteria table, and the verdict.
