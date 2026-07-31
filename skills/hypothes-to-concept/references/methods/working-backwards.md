# Working Backwards

> Start from the desired experience and reason backwards to what the
> system must provide. If you cannot articulate who benefits and how,
> the idea does not yet deserve a specification.

## Origin

Developed at Amazon as a product-development discipline. The core
practice is to write a fictional **press release** and **FAQ** before
any design work begins — forcing the team to clarify *who* the feature
is for and *why* it matters before considering *how* to build it.

## Application to Problem Analysis

When evaluating a proposed feature, construct, or change, apply Working
Backwards as a value test: it tests whether the proposal solves a real
problem or is merely technically interesting.

### 1. Write the User Story

```
As a [stakeholder role],
I want to [use this]
so that [concrete benefit].
```

If the story feels contrived or the benefit is vague, the proposal
needs more work before it can be evaluated.

### 2. Write the Press Release

Draft a one-paragraph announcement. It should answer:

- What is it called?
- What problem does it solve?
- Why should the stakeholder care?
- How does their daily work change?

If the press release reads like an implementation note rather than a
stakeholder-facing benefit, the proposal fails this test.

### 3. Write the FAQ

Anticipate the questions a working stakeholder would ask:

- "How is this different from [existing thing]?"
- "When would I use this instead of [alternative]?"
- "What do I lose by not using it?"
- "Is there a migration path from current practice?"

Unexplained or dismissed questions reveal gaps in the proposal.

### 4. Derive Requirements

From the story, press release, and FAQ, extract what the system must
provide. If the requirements list is empty or duplicates existing
capabilities, the feature is not needed.

## When to Use

This method suits value questions: "is this useful?", "who benefits?",
speculative use cases.

## Output

The user story, press release, FAQ, and the derived requirements — or
the finding that the benefit is not articulable.
