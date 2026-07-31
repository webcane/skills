# Logical Analysis

> Derive the consequences of a proposal from explicit premises and
> verify they are consistent with the architecture. A proposal that
> requires hidden premises to justify its place is not yet ready.

## Origin

Rooted in deductive reasoning and formal logic (Aristotle, Frege).
Logical analysis tests whether conclusions follow necessarily from
premises — and whether those premises are themselves valid.

## Application to Problem Analysis

When evaluating architectural fit, Logical Analysis tests whether the
proposal's implications are compatible with the project's stated rules.

### 1. State the Premises

Identify the rules the proposal explicitly depends on:

- "Layers are independent."
- "The core has no dependencies on higher layers."
- "Each construct has exactly one form."
- (Add specific rules from the project's architecture.)

### 2. Deduce the Consequences

If the proposal is accepted, what must be true?

- What must the system do differently?
- What must components support?
- What must the user or stakeholder understand?
- Which existing documents or contracts would need to change?

### 3. Test for Contradiction

Do any deduced consequences contradict the stated premises?

- "The proposal requires [layer A] to access [layer B] internals — but
  premise 1 says layers are independent. Contradiction."

### 4. Identify Hidden Premises

What unstated assumptions does the deduction require?

- "The proposal assumes [capability] is available — but this has never
  been stated as a constraint."
- "The proposal assumes all targets support [mechanism]."

Hidden premises must either be explicitly accepted (and documented) or
the proposal must be revised to remove the dependency.

## When to Use

This method suits architectural-fit questions: "does this fit?",
"consistent with our architecture", "layering".

## Output

The stated premises, deduced consequences, contradiction test results,
and any hidden premises found.
