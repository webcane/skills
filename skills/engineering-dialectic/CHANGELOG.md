# Changelog

## [Unreleased]

### Added
- Independent solver/discriminator protocol, positions and hybrid modes.
- Evidence contracts, selective expert falsification and decision template.
- Application examples and comparison of methods, benefits and limitations.
- Optional `/dialectic` entry command and `scripts/install_commands.py` for OpenCode, Claude Code and Codex.
- `blindness` marker (`full` / `partial` / `compromised`) in the protocol and decision template.
- README with provenance: what is borrowed from the upstream dialectic skill and what was redesigned.

### Changed
- Model choice belongs to the user or the profile builder; the orchestrator records the actual model instead of selecting the strongest.
- Russian trigger phrases added to the skill description.
