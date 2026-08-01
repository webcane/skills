# Five Whys — Root Cause Analysis

> Keep asking "Why?" until the answer stops being a symptom and becomes
> a cause. Each answer feeds the next question. The goal is not to fix
> the symptom or blame a person — it is to find the systemic failure
> that produced the symptom.

## Origin

Developed at Toyota as part of the Toyota Production System. The name
is a rule of thumb: five iterations is usually enough to reach a root
cause, but the real rule is "keep going until the cause stops
changing".

## Application to Problem Analysis

When a problem presents as a single visible symptom, Five Whys pushes
past the symptom to the underlying process failure.

### 1. State the Symptom

Name the observed problem exactly as it appeared.

### 2. Ask Why — and Chain the Answers

"Why did this happen?" — write the answer. Then ask "Why?" about that
answer. Chain until the answer stops being a symptom of something else.

Example:

- Why did the machine break? → It overheated.
- Why did it overheat? → The cooling system failed.
- Why did it fail? → The filter clogged.
- Why did it clog? → It was never replaced on time.
- Why was it never replaced? → No maintenance schedule exists.

### 3. Find the Systemic Failure, Not the Culprit

The root cause is the point where a process, schedule, or rule is
missing — not where a person erred. Stop when you reach a cause that a
change in the system (not in someone's diligence) would prevent.

### 4. Form the Hypothesis

Restate the root cause as a testable hypothesis:

> "The absence of a maintenance schedule is the root cause of the
> breakdowns."

## When to Use

A problem keeps recurring, the visible symptom keeps being treated
while the problem returns, or someone asks "but what actually caused
it?" one level deeper than everyone else.

## Output

The Why-chain, the systemic (non-blaming) root cause, and the root
cause restated as a hypothesis.
