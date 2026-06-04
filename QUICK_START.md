# Quick Start: Set Up Your Skills Repository

Copy-paste these commands to set up your GitHub skills repo.

## 1. Prepare Repository Structure

```bash
# Navigate to your skills repo
cd ~/projects/skills  # or your repo path

# Create directories
mkdir -p skills/content-writer-linkedin
mkdir -p scripts
mkdir -p dist

# Copy the skill files
cp /path/to/SKILL.md skills/content-writer-linkedin/
cp /path/to/README.md skills/content-writer-linkedin/

# Copy helper scripts (make them executable)
cp package-skill.sh scripts/
cp install-skill.sh scripts/
chmod +x scripts/*.sh

# Create .gitignore (don't version .skill files)
echo "dist/*.skill" >> .gitignore
echo "dist/*.json" >> .gitignore
echo ".DS_Store" >> .gitignore
```

## 2. Update .gitignore

```bash
git add .gitignore
git commit -m "chore: ignore generated .skill files"
```

## 3. Add Files to Git

```bash
git add skills/ scripts/
git commit -m "feat: add content-writer-linkedin skill

- Three-mode operation (Outline, Research/Verify, Write)
- Collaborative review loop
- LinkedIn-optimized for authentic content
"
```

## 4. Package the Skill

```bash
# Create the .skill file
bash scripts/package-skill.sh content-writer-linkedin 1.0.0

# This creates:
# - dist/content-writer-linkedin.skill (latest)
# - dist/content-writer-linkedin-1.0.0.skill (versioned)
```

## 5. Create GitHub Release

```bash
# Create git tag
git tag -a v1.0.0 -m "Release: content-writer-linkedin v1.0.0"

# Push tag
git push origin v1.0.0

# Upload to GitHub Releases (using GitHub CLI)
gh release create v1.0.0 \
  dist/content-writer-linkedin-1.0.0.skill \
  -t "Content Writer LinkedIn v1.0.0" \
  -n "Initial release: Three-mode operation with collaborative review loop"
```

## 6. Share Installation URLs

Users can now install with:

```bash
# Latest version from main branch
curl -L https://raw.githubusercontent.com/yourusername/skills/main/dist/content-writer-linkedin.skill \
  -o content-writer-linkedin.skill

# Specific version from release
curl -L https://github.com/yourusername/skills/releases/download/v1.0.0/content-writer-linkedin-1.0.0.skill \
  -o content-writer-linkedin.skill
```

## 7. Updates in the Future

When you update your skill:

```bash
# Make changes in skills/ directory
vim skills/content-writer-linkedin/SKILL.md

# Commit changes
git add skills/content-writer-linkedin/
git commit -m "feat: add new feature to content-writer-linkedin"

# Package new version
bash scripts/package-skill.sh content-writer-linkedin 1.1.0

# Create and push release
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
- ✅ Ready for Claude, Code, and everywhere else

Share the installation URL:
```
https://raw.githubusercontent.com/yourusername/skills/main/dist/content-writer-linkedin.skill
```
