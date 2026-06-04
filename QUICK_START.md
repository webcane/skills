# Quick Start

## 1. Set Up Repository

```bash
mkdir -p skills/content-writer-linkedin scripts dist

cp /path/to/SKILL.md skills/content-writer-linkedin/
cp /path/to/README.md skills/content-writer-linkedin/
cp package-skill.sh install-skill.sh scripts/
chmod +x scripts/*.sh

echo "dist/*.skill" >> .gitignore
echo "dist/*.json" >> .gitignore
echo ".DS_Store" >> .gitignore

git add .
git commit -m "feat: add content-writer-linkedin skill"
```

## 2. Package & Release

```bash
bash scripts/package-skill.sh content-writer-linkedin 1.0.0

git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
gh release create v1.0.0 dist/content-writer-linkedin-1.0.0.skill \
  -t "Content Writer LinkedIn v1.0.0"
```

## 3. Update Later

```bash
vim skills/content-writer-linkedin/SKILL.md
git add skills/ && git commit -m "feat: ..."
bash scripts/package-skill.sh content-writer-linkedin 1.1.0
git tag -a v1.1.0 -m "Release v1.1.0" && git push origin v1.1.0
gh release create v1.1.0 dist/content-writer-linkedin-1.1.0.skill
```