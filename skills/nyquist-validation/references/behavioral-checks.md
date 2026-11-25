# Selecting observations that expose violations

An invariant describes permitted system behavior across relevant states and
event sequences. Observe the effect that can violate it, not merely the event
that initiates the operation.

## Example: idempotent payment creation

Requirement: requests sharing an idempotency key create at most one financial
operation. Two successful HTTP responses are compatible with either one payment
or duplicate payments, so response codes alone cannot discriminate the cases.

| Scenario | Observe | Assert |
| --- | --- | --- |
| First request | Persisted operation and returned ID | One operation with expected amount |
| Sequential retry | Operations for key; returned IDs | One operation; same operation ID |
| Concurrent same-key calls | Committed operations after both complete | At most one operation; contract-compatible responses |
| Commit succeeds, response is lost | Retry result and durable records | Retry resolves to the existing operation |
| Worker restarts before acknowledging message | Durable effect after redelivery | No duplicate effect |

Use the real persistence boundary for these integration assertions. Mocking the
repository to always return the same ID cannot demonstrate durable idempotency.
An isolated unit test can still verify local decision logic; label its scope.
Use barriers, transactions, or supported fault injection to control ordering.
If that setup is unavailable, record a concurrency gap rather than substituting
a sequential test and claiming full coverage.

## Independent expectations

Derive expected values from the requirement, a reviewed fixture, an independent
reference model, or a specified property. Computing both actual and expected
with the same production function produces a circular oracle. An assertion on
object existence may be valid for existence requirements, but cannot establish
correct amount, authorization, ordering, or uniqueness.

For each proposed test ask: what plausible broken implementation would still
pass? Strengthen the observation if it misses the requirement's central failure.
Do not introduce unrelated edge cases just to inflate a test suite.

## Coverage boundaries

Separate requirement coverage, scenario coverage, and line coverage. A
requirement mapped to a test is only a candidate until its assertions and run
have been inspected. Property-based and model-based tests can extend exploration
when useful; neither establishes universal correctness.

Production telemetry can support diagnosis and detect violations that occur in
production. It does not automatically establish automated test coverage. A metric
that returns to its original value can hide a transient duplicate effect; prefer
durable effect counts and correlation identifiers when that is the invariant.
