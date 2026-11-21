# Changelog

## [Unreleased]

### Added
- Read-only orchestrator and generated OpenCode V2 profiles for four participant roles.
- Deterministic profile builder with model override and freshness checks.
- Installation and capability boundaries documented in the agent README.
- `verification.md`: configuration checks that were actually run, plus the behavioral scenarios still pending.
- `question` permission for the orchestrator so an unresolved priority can be returned to the user.

### Changed
- Blindness is recorded explicitly as `full` / `partial` / `compromised`; model selection is documented as owned by the user or `--model`, not by the orchestrator.
