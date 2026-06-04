# Quick Start: Set Up Your Skills Repository

Copy-paste these commands to set up your GitHub skills repo.

## 1. Prepare Repository Structure

```bash
cd ~/projects/skills  # or your repo path

mkdir -p skills/content-writer-linkedin scripts dist

# Copy skill files
cp /path/to/SKILL.md skills/content-writer-linkedin/
cp /path/to/README.md skills/content-writer-linkedin/

# Copy scripts and make executable
cp package-skill.sh scripts/
cp install-skill.sh scripts/
chmod +x scripts/*.sh

# Create .gitignore
echo "dist/*.skill" >> .gitignore
echo "dist/*.json" >> .gitignore
echo ".DS_Store" >> .gitignore
```

## 2. Commit and Package

```bash
git add .gitignore skills/ scripts/
git commit -m "feat: add content-writer-linkedin skill"

# Package the skill
bash scripts/package-skill.sh content-writer-linkedin 1.0.0
```

## 3. Create GitHub Release

```bash
git tag -a v1.0.0 -m "Release: content-writer-linkedin v1.0.0"
git push origin v1.0.0

gh release create v1.0.0 \
  dist/content-writer-linkedin-1.0.0.skill \
  -t "Content Writer LinkedIn v1.0.0" \
  -n "Initial release: three-mode operation with collaborative review loop"
```

## 4. Share Installation URLs

```bash
# Latest version
curl -L https://raw.githubusercontent.com/yourusername/skills/main/dist/content-writer-linkedin.skill \
  -o content-writer-linkedin.skill

# Specific version
curl -L https://github.com/yourusername/skills/releases/download/v1.0.0/content-writer-linkedin-1.0.0.skill \
  -o content-writer-linkedin.skill
```

## 5. Future Updates

```bash
# Edit → Commit → Package → Release
vim skills/content-writer-linkedin/SKILL.md
git add skills/content-writer-linkedin/
git commit -m "feat: improve content-writer-linkedin"
bash scripts/package-skill.sh content-writer-linkedin 1.1.0
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin v1.1.0
gh release create v1.1.0 dist/content-writer-linkedin-1.1.0.skill
```

## Done! 🎉

Your skill is now:
- ✅ Stored in version control
- ✅ Packaged as distributable `.skill` files
- ✅ Released on GitHub
- ✅ Installable via curl

For detailed explanations, see **[DISTRIBUTION_GUIDE.md](DISTRIBUTION_GUIDE.md)** or **[GITHUB_SKILLS_STRUCTURE.md](GITHUB_SKILLS_STRUCTURE.md)**.
