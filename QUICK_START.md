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

## 2. Package & Release

```bash
# Version is read from SKILL.md frontmatter (omit to use it; pass to override)
bash scripts/package-skill.sh content-writer-linkedin

git tag -a content-writer-linkedin/v1.0.0 -m "content-writer-linkedin v1.0.0"
git push origin content-writer-linkedin/v1.0.0
gh release create content-writer-linkedin/v1.0.0 \
  -t "content-writer-linkedin v1.0.0"
```

On a published release, CI packages and uploads only the tagged skill and
promotes its `[Unreleased]` CHANGELOG section — so you don't need to attach the
`.skill` file or bump the changelog by hand.

## 3. Update Later

```bash
vim skills/content-writer-linkedin/SKILL.md          # bump metadata.version to 1.1.0
# add the change under ## [Unreleased] in skills/content-writer-linkedin/CHANGELOG.md
git add skills/ && git commit -m "feat: ..."

git tag -a content-writer-linkedin/v1.1.0 -m "content-writer-linkedin v1.1.0"
git push origin content-writer-linkedin/v1.1.0
gh release create content-writer-linkedin/v1.1.0 -t "content-writer-linkedin v1.1.0"
```
