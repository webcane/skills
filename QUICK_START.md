# Quick Start

Each skill is versioned and released independently. A skill's version lives in
its `SKILL.md` frontmatter (`metadata.version`); release tags are namespaced as
`<skill>/v<version>`. See [CLAUDE.md](CLAUDE.md) for the full model.

## 1. Set Up Repository

```bash
mkdir -p skills/content-writer-linkedin scripts dist

cp /path/to/SKILL.md skills/content-writer-linkedin/
cp /path/to/CHANGELOG.md skills/content-writer-linkedin/   # per-skill changelog
cp /path/to/README.md skills/content-writer-linkedin/
cp package-skill.sh install-skill.sh scripts/
chmod +x scripts/*.sh

echo "dist/*.skill" >> .gitignore
echo "dist/*.json" >> .gitignore
echo ".DS_Store" >> .gitignore

git add .
git commit -m "feat: add content-writer-linkedin skill"
```

Make sure the skill's `SKILL.md` frontmatter carries a version:

```yaml
metadata:
  version: 1.0.0
```

## 2. Release a New Version

Three steps — build all packages, optionally install locally, then release:

```bash
# 1. Build universal .skill and Codex, Claude Code, Claude.ai ZIPs
bash scripts/package-skill.sh <skill-name>

# 2. Install/reinstall into Codex, OpenCode, and Claude Code
bash scripts/install-local.sh <skill-name>
# Or choose only one: --target codex|opencode|claude-code

# 3. Tag, push, and create GitHub release (version read from SKILL.md frontmatter)
bash scripts/release-skill.sh <skill-name>
```

`<skill-name>` is the path relative to the active `skills/` directory
(`content-writer-linkedin`, for example). Archived skills under
`archive/skills/` are not included. Artifacts and install dirs use the skill's
flat basename. `INSTALL_DIR` installs only in the specified directory; use
`--target` to select its format for a custom path. Existing selected skill
folders are replaced. Packaging requires Python 3 with PyYAML, tar, and zip;
installation also requires unzip.

On a published release, CI packages and uploads only the tagged skill and
promotes its `[Unreleased]` CHANGELOG section — so you don't need to attach the
`.skill` file or bump the changelog by hand.

For cane-wiki, the Claude agent owns the wiki workflow and
`scripts/build-codex-agent.py` generates its Codex TOML version. The
`cane-wiki-init` uses the Agent Skills format for setup and dependencies.
Package skill variants with `scripts/package-skill-claude-code.sh` or
`scripts/package-skill-codex.sh`. Use `scripts/install-cane-wiki-claude.sh` or
`scripts/install-cane-wiki-codex.sh` for local installation; the Codex installer
also installs the three external Obsidian skill dependencies.

## 3. Update Later

```bash
vim skills/<skill-name>/SKILL.md          # bump metadata.version (e.g. 1.1.0 → 1.2.0)
# add the change under ## [Unreleased] in skills/<skill-name>/CHANGELOG.md
git add skills/ && git commit -m "<skill-name>: description of change"

# Then repeat the 3 release steps:
bash scripts/package-skill.sh <skill-name>
bash scripts/install-local.sh <skill-name>
bash scripts/release-skill.sh <skill-name>
```
