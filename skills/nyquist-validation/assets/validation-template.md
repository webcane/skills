---
scope: "<feature or change>"
mode: audit
result: PARTIAL
coverage_complete: false
created: "<YYYY-MM-DD>"
---

# Validation — <scope>

## Contract and environment

- Requirements source and revision / relevant working-tree changes:
- OpenSpec change / capability and baseline + delta sources, if applicable:
- Scope boundaries and explicitly inferred assumptions:
- Runner, configuration, working directory, isolated services:
- Quick command / regression command:
- Measured feedback latency or unknown; chosen execution cadence:

## Behavioral verification map

| Requirement / source heading | Invariant | Violation and scenario | Observable assertion | Test / selector | Exact command | Status | Evidence / limits |
| --- | --- | --- | --- | --- | --- | --- | --- |
| <ID> | <property> | <failure sequence> | <independent expected effect> | <path::test> | <command> | MISSING | <actual evidence> |

## Executions

| Command and working directory | Environment / revision | Exit | Executed / skipped | Outcome | Evidence location |
| --- | --- | --- | --- | --- | --- |
| <exact non-watch command> | <actual> | <code or not run> | <counts> | <observed result> | <log or concise output> |

## Gaps and prerequisites

| Requirement | Remaining scenario / prerequisite | Reason | Next action / owner |
| --- | --- | --- | --- |

## Test-debug attempts

| Gap | Attempt (max 3) | Failure type | Test-only correction | Result |
| --- | --- | --- | --- | --- |

## Manual checks and escalations

| Requirement | Expected vs actual / why manual or blocked | Reproduction / human steps | Owner if known |
| --- | --- | --- | --- |

## Verdict and audit trail

- Result: <COMPLIANT / PARTIAL / ESCALATE / PLANNED>.
- Unique requirements: <total>; fully verified: <count>; remaining: <count>.
- Changed test/report files; implementation diff check:
- Relevant regression results and pre-existing failures:
- Open risks and next action:
- Audit date and relationship to previous evidence:

Evidence is limited to the recorded scenarios, revision, and environment.
