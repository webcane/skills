# Behavioral smoke evaluation

Initial version 1.0.0 run on 2026-11-25 against three bundled minimal fixtures, with the new skill
and an ordinary-assistance baseline. Each configuration used one separate agent
for its three cases; cases were not independently isolated contexts.

| Case | Observed with skill |
| --- | --- |
| Misleading green tests | Existing suite: 1 pass, 1 skip. Read-only behavioral probe exposes duplicate ledger entries; audit leaves all fixture files unchanged. |
| Fill a sequential retry gap | Two new assertions execute and fail on duplicate count / changed ID; implementation unchanged, report escalates and remains noncompliant. |
| Standalone planning | Requirements mapped to observations and proposed commands; missing scaffolding recorded, PLANNED and noncompliant, no claimed test pass. |

Both configurations satisfied 12/12 expectations. Parent verification compared
implementation bytes and reran the defect-revealing suites. These checks support
basic workflow correctness, not superiority over the baseline. Timing and token
metrics were unavailable. Real persistence and actual concurrency still need
integration evaluation on a representative project.

Version 1.1.0 adds `openspec-delta`: an active change tightens deletion permissions
and renames a requirement while stale current/archive specs allow the former
behavior. Its tasks are checked and existing tests pass. The case checks effective
delta resolution, scenario traceability, and test-only defect escalation. Local
comparison outputs are under `studies/nyquist-validation/openspec-update/`.
Both versions satisfied 5/5 expectations in this case. Independent reruns found
two passing scenarios and one failing member-denial assertion; production and
OpenSpec inputs were unchanged. This verifies MODIFIED/RENAMED integration, not
superiority over the prior version. ADDED/REMOVED, custom schemas, and actual
CLI integration were not exercised.

Local outputs and review viewer live under the gitignored
`studies/nyquist-validation/`; prompts and source fixtures are retained here for
repeatable future evaluations. Source fixture failures are intentional: the
payment implementation does not honor its idempotency requirement.
