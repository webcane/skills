# Codebase Concerns

**Analysis Date:** 2026-06-17

## Summary

The repo is a small, well-structured skill distribution system with two active skills and healthy tooling. The main risks are: a broken versioned-download URL in `install-skill.sh` (uses the old tag format), two planned skills (`playing-card`, `playing-deck`) that exist only as ROADMAP stubs with no `SKILL.md`, and a stray untracked file in `.github/workflows/` that contains what appears to be leftover prompt/test content.

---

## Critical Concerns

**Broken versioned release download URL in `install-skill.sh`:**
- Issue: When `VERSION` is supplied, the download URL is constructed as `https://github.com/$GITHUB_REPO/releases/download/v${VERSION}/${SKILL_NAME}-${VERSION}.skill`. The `v` prefix path segment (`/v${VERSION}/`) reflects the old single-product release tag format (`v1.0.0`). The repo now uses per-skill namespaced tags (`<skill-name>/v<version>`), so the actual release asset path is `releases/download/<skill-name>%2Fv<version>/...`. Versioned installs via `install-skill.sh <name> <version>` will 404.
- File: `scripts/install-skill.sh` line 19
- Impact: Any user who attempts to pin a specific skill version via the install script gets a download failure. The `latest` path (raw GitHub URL) works fine.
- Fix: Reconstruct the URL as `releases/download/${SKILL_NAME}%2Fv${VERSION}/${SKILL_NAME}-${VERSION}.skill` or use `gh release download` with the correct tag.

**Planned skills exist only as ROADMAP stubs:**
- Issue: `skills/playing-card/` and `skills/playing-deck/` each contain only a `ROADMAP.md` file. Neither has a `SKILL.md`. The CI `package-all` job iterates `skills/*/` and runs `tar -czf "dist/${name}.skill" -C skills "$name"` for every directory, so it will produce a `playing-card.skill` and `playing-deck.skill` containing only the ROADMAP document. These artifacts would be silently broken.
- Files: `skills/playing-card/ROADMAP.md`, `skills/playing-deck/ROADMAP.md`, `.github/workflows/package-skills.yml` lines 19–22
- Impact: CI uploads unusable skill artifacts to every push-to-master run for stub skills. Users who install them get a ROADMAP file, not a working skill.
- Fix: Either guard `package-all` with a `[ -f "skills/$name/SKILL.md" ]` check, or move stub skills to a `planning/` or `docs/` directory outside `skills/`.

**Stray untracked file `.github/workflows/asd`:**
- Issue: `.github/workflows/asd` is untracked (confirmed via `git status`). Its content is a block of playing-card prompt text — almost certainly a paste/test artifact. GitHub Actions will attempt to parse any YAML file in `.github/workflows/`; a non-YAML file named without `.yml`/`.yaml` is currently ignored by GitHub but represents clutter and a risk if renamed.
- File: `.github/workflows/asd`
- Fix: Delete the file (`git rm --force .github/workflows/asd` or simply `rm`).

---

## Technical Debt

**`install-skill.sh` defaults to `webcane/skills` and `main` branch, not `master`:**
- Issue: `GITHUB_REPO` defaults to `webcane/skills` (line 4 comment, line 11). The actual remote may differ (this repo is `mniedre/git/skills` locally). `BRANCH` defaults to `main` but the repo uses `master` (confirmed in CI and git status).
- File: `scripts/install-skill.sh` lines 11–12
- Impact: `latest` installs using the default settings silently hit the wrong branch, returning a 404 for the raw URL.
- Fix: Change default `BRANCH` to `master`. Document that `GITHUB_REPO` must be set by the user, or derive it from `git remote get-url origin`.

**`dist/` contains accumulated versioned `.skill` and `.json` artifacts committed to the repo:**
- Issue: `.gitignore` excludes `dist/*.skill`, `dist/*.json`, and `dist/*.zip` from tracking, yet the `dist/` directory physically contains 20+ versioned `.skill` files and paired `.json` files for `playing-card-prompt` going back to v1.1.0. These are not tracked by git (confirmed: `git ls-files dist/` returns 0 results) but accumulate locally and get re-created on every local package run, potentially causing confusion about which files are authoritative.
- Files: `dist/` (local only)
- Impact: Developer confusion; no production risk since files aren't tracked. Disk clutter grows with each release.
- Fix: Document in `README.md` that `dist/` is build-only and can be safely cleared. Optionally add a `make clean` / `scripts/clean.sh` convenience.

**`content-writer-linkedin` SKILL.md lacks `version` in frontmatter metadata:**
- Issue: `skills/content-writer-linkedin/SKILL.md` frontmatter has `metadata:` with no `version:` field. `package-skill.sh` will fail with "no version found" if run without an explicit version argument.
- File: `skills/content-writer-linkedin/SKILL.md` line 7
- Impact: `bash scripts/package-skill.sh content-writer-linkedin` (no version arg) errors. CI `release-skill` job would also fail for this skill.
- Fix: Add `version: 1.0.0` under `metadata:` in `skills/content-writer-linkedin/SKILL.md`.

**CI `package-all` does not exclude `.DS_Store` or dev-only files:**
- Issue: The `package-all` job uses a bare `tar -czf "dist/${name}.skill" -C skills "$name"` with no excludes. The local `package-skill.sh` excludes `.DS_Store`, `*.swp`, and `config.json.bak*`. CI-produced artifacts may differ from locally-produced ones if `.DS_Store` files exist in the skill directories at the time CI runs.
- File: `.github/workflows/package-skills.yml` lines 19–22
- Fix: Align CI `tar` command with `package-skill.sh` excludes, or call `scripts/package-skill.sh` from CI.

---

## Missing Pieces

**No test suite for scripts:**
- `scripts/package-skill.sh`, `scripts/release-skill.sh`, `scripts/install-skill.sh`, and `scripts/package-skill-claudeai.sh` have no automated tests. Edge cases (malformed frontmatter, missing CHANGELOG sections, tag collision) are only caught at runtime.

**No schema validation for `SKILL.md` frontmatter:**
- Required fields (`name`, `description`, `metadata.version`) are never validated as part of CI. A skill with a missing or malformed frontmatter would pass CI's `package-all` and produce a malformed artifact silently.

**`playing-card` and `playing-deck` skills have no implementation yet:**
- Both have detailed ROADMAPs (`skills/playing-card/ROADMAP.md`, `skills/playing-deck/ROADMAP.md`) but zero implementation. The fork from `playing-card-prompt` described in the roadmaps (Phase 0) has not started.

**No README for `playing-card-prompt` skill:**
- `skills/content-writer-linkedin/` has a `README.md`; `skills/playing-card-prompt/` does not. Users browsing GitHub have no human-readable overview of the skill's purpose and usage.

---

## Security Considerations

**No secrets detected:** No `.env` files, credential files, or hardcoded secrets found in tracked files.

**`gh release create` requires `GITHUB_TOKEN` ambient auth:**
- `scripts/release-skill.sh` calls `gh release create` and relies on the user's local `gh` CLI auth. No secrets are embedded. CI uses `secrets.GITHUB_TOKEN` correctly.

**`install-skill.sh` extracts a remote tar.gz into a user-specified directory:**
- If `INSTALL_DIR` is set to a sensitive location, a malicious `.skill` archive could overwrite files. This is a standard risk for any tar-based install and is mitigated by the fact that the source is a trusted GitHub repo. No path-traversal protection (e.g., `--strip-components` + whitelist) is present.
- File: `scripts/install-skill.sh` lines 35–36

---

## Recommendations

1. **Fix the versioned `install-skill.sh` download URL** — update line 19 of `scripts/install-skill.sh` to use the correct namespaced tag path (`${SKILL_NAME}%2Fv${VERSION}`) so pinned-version installs work.

2. **Guard CI `package-all` against SKILL.md-less directories** — add `[ -f "skills/$name/SKILL.md" ] || continue` before the `tar` line in `.github/workflows/package-skills.yml` to prevent broken artifacts for stub-only skill directories.

3. **Delete `.github/workflows/asd`** — remove this stray non-YAML file from the workflows directory.

4. **Add `version: 1.0.0` to `skills/content-writer-linkedin/SKILL.md`** — makes the skill releasable via the standard tooling without requiring an explicit version argument.

5. **Fix `BRANCH` default in `install-skill.sh`** — change `BRANCH="${BRANCH:-main}"` to `BRANCH="${BRANCH:-master}"` to match the repo's actual default branch.

---

## Gaps / Unknowns

- **Actual GitHub remote URL** — the hardcoded `webcane/skills` default in `install-skill.sh` may or may not match the intended public distribution repo. Could not confirm without network access.
- **Claude.ai skill upload format stability** — `package-skill-claudeai.sh` works around Claude.ai's 200-char description limit and zip layout requirements; if Claude.ai changes its upload spec these heuristics will silently break.
- **`playing-card-prompt` complexity ceiling** — at 620 lines, `SKILL.md` is the largest file in the repo. No complexity or token-count limit is enforced; further growth could exceed Claude's context window for skill loading.

---

*Concerns audit: 2026-06-17*
