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

Four steps — package, package for Claude.ai, install locally, then release:

```bash
# 1. Package as .skill (tar.gz) for Claude Code / agentskills.io
bash scripts/package-skill.sh <skill-name>

# 2. Package as .zip for Claude.ai upload
bash scripts/package-skill-claudeai.sh <skill-name>

# 3. Install/reinstall locally (optional — validates the package works)
bash scripts/install-local.sh <skill-name>

# 4. Tag, push, and create GitHub release (version read from SKILL.md frontmatter)
bash scripts/release-skill.sh <skill-name>
```

On a published release, CI packages and uploads only the tagged skill and
promotes its `[Unreleased]` CHANGELOG section — so you don't need to attach the
`.skill` file or bump the changelog by hand.

## 3. Update Later

```bash
vim skills/<skill-name>/SKILL.md          # bump metadata.version (e.g. 1.1.0 → 1.2.0)
# add the change under ## [Unreleased] in skills/<skill-name>/CHANGELOG.md
git add skills/ && git commit -m "<skill-name>: description of change"

# Then repeat the 4 release steps:
bash scripts/package-skill.sh <skill-name>
bash scripts/package-skill-claudeai.sh <skill-name>
bash scripts/install-local.sh <skill-name>
bash scripts/release-skill.sh <skill-name>
```
