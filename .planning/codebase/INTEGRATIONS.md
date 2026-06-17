# INTEGRATIONS
> Generated: 2026-06-17 | Focus: tech | Project: skills

## Summary

This repo integrates with GitHub (via `gh` CLI and GitHub Actions) as its sole external service — for release management, artifact hosting, and CI. There are no databases, auth providers, third-party SDKs, or external APIs consumed at runtime. The distributed skill files themselves target Claude Code and Claude.ai as downstream consumers, but this repo does not call those platforms' APIs directly.

## APIs & External Services

**GitHub:**
- GitHub Releases API — skill `.skill` and `.zip` archives are uploaded as release assets
  - Client: `gh` CLI (`gh release create`, invoked in `scripts/release-skill.sh`)
  - Auth: `GITHUB_TOKEN` (GitHub Actions secret, auto-injected by Actions runner)
- GitHub Actions — CI/CD pipeline defined in `.github/workflows/package-skills.yml`
  - Triggers: push to `master` (paths: `skills/**`) and published releases
  - Artifact storage: `actions/upload-artifact@v6` (stores packaged `.skill` files as workflow artifacts)
  - Release uploads: `softprops/action-gh-release@v2`

**Claude Code / agentskills.io (distribution target):**
- `.skill` files (tar.gz) are the install format for Claude Code skill extensions
- This repo does not call the agentskills.io API; it only produces the artifact format

**Claude.ai (distribution target):**
- `.zip` files produced by `scripts/package-skill-claudeai.sh` are the upload format for Claude.ai's skill import
- SKILL.md is renamed to lowercase `skill.md` and the `description` field is capped at 200 chars
- This repo does not call the Claude.ai API; it only produces the artifact format

## Data Storage

**Databases:** None

**File Storage:**
- `dist/` directory — local and CI artifact staging (gitignored)
- GitHub Release assets — permanent versioned artifact hosting

**Caching:** None

## Authentication & Identity

**Auth Provider:** None (no user-facing auth)

**GitHub Actions auth:**
- `GITHUB_TOKEN` secret — scoped `contents: write` permission in the `release-skill` job for committing CHANGELOG promotions and uploading release assets

## Monitoring & Observability

**Error Tracking:** None

**Logs:** GitHub Actions job logs only

## Webhooks & Callbacks

**Incoming:** None

**Outgoing:** None (GitHub Actions events are triggered by git push/release, not webhooks from this repo)

## Environment Configuration

**Required env vars / secrets:**
- `GITHUB_TOKEN` — required in GitHub Actions for release uploads and CHANGELOG commit push (auto-provided by Actions runner with `permissions: contents: write`)

**Local development:**
- No env vars required for packaging (`package-skill.sh`, `package-skill-claudeai.sh`)
- `gh` CLI must be authenticated locally to run `scripts/release-skill.sh`

## Gaps / Unknowns

- `scripts/install-skill.sh` likely fetches from a remote URL (agentskills.io or GitHub releases) — the exact endpoint and any auth requirements were not confirmed
- No webhook integration with agentskills.io or Claude.ai was found, but cannot rule out future integration
