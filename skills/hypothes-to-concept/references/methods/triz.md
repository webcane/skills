# TRIZ — Theory of Inventive Problem Solving

> When a problem seems to require a specific implementation or forces a
> trade-off, TRIZ helps find the abstract solution that satisfies both
> requirements without compromise. If the only solutions are
> workarounds, the problem is not yet well-formed.

## Origin

Developed by Genrich Altshuller and colleagues starting in 1946. TRIZ
is based on the observation that technical problems and their solutions
repeat across industries — and that contradictions can be resolved
systematically by applying known inventive principles rather than by
compromise.

## Application to Problem Analysis

When two requirements are in tension, TRIZ tests whether both can be
satisfied by separating concerns rather than compromising.

### 1. Identify the Apparent Contradiction

> "To implement [feature], the [system] must [specific behaviour],
> which contradicts [constraint]."

Example: "To guarantee safety, the system must check every input at
runtime — but the embedded target has no latency budget."

### 2. Apply Separation Principles

Resolve the contradiction by separating concerns:

- **Separation in time** — the behaviour occurs at different times
  (compile vs. runtime, setup vs. steady state).
- **Separation in space** — different parts live in different layers
  or subsystems.
- **Separation on condition** — the definition does not change, but
  each case implements it differently.
- **Separation by scale** — the concept is defined at one level;
  detail lives below that level.

### 3. Consult Known Patterns

Has a similar "must satisfy both requirements" problem been solved
elsewhere?

- How does the existing system handle analogous tensions?
- How do other systems in the same domain solve this?
- Does an existing higher-level principle already resolve it?

### 4. Formulate the Abstract Solution

Define the solution purely in terms of what it does:

> "[Thing] transforms [input] into [output] with [guarantee]. Each
> case realises this according to its own constraints."

If the abstract formulation is empty or requires case-specific
language, the problem is not yet well-formed.

## When to Use

This method suits problems that name a tension: "but that conflicts
with", "can't have both", "trade-off between X and Y".

## Output

The identified contradiction, the separation principle applied, known
patterns consulted, and the abstract solution (or the finding that the
problem is not yet well-formed).
