# Skills Distribution Guide

Detailed step-by-step walkthrough. For quick setup, see **[QUICK_START.md](QUICK_START.md)**.

---

## 1. Organize Your Repository

```bash
cd your-skills-repo
mkdir -p skills/content-writer-linkedin scripts dist
cp /path/to/SKILL.md skills/content-writer-linkedin/
cp /path/to/README.md skills/content-writer-linkedin/
cp package-skill.sh scripts/
cp install-skill.sh scripts/
chmod +x scripts/*.sh
git add skills/ scripts/
git commit -m "chore: organize skills structure"
```

## 2. Add to .gitignore

```bash
echo "dist/*.skill" >> .gitignore
echo ".DS_Store" >> .gitignore
git add .gitignore
git commit -m "chore: update gitignore"
```

## 3. Package Your Skill

```bash
bash scripts/package-skill.sh content-writer-linkedin 1.0.0
```

Creates:
- `dist/content-writer-linkedin.skill` (always latest)
- `dist/content-writer-linkedin-1.0.0.skill` (versioned)
- `dist/content-writer-linkedin-1.0.0.json` (metadata)

## 4. Create GitHub Release

```bash
git tag -a v1.0.0 -m "Release: content-writer-linkedin v1.0.0"
git push origin v1.0.0
gh release create v1.0.0 \
  dist/content-writer-linkedin-1.0.0.skill \
  -t "Content Writer LinkedIn v1.0.0" \
  -n "Initial release with three-mode operation and review loop"
```

## 5. Installation Methods for Users

### Method 1: Direct curl (Simplest)
```bash
curl -L https://raw.githubusercontent.com/yourusername/skills/main/dist/content-writer-linkedin.skill \
  -o content-writer-linkedin.skill
tar -xzf content-writer-linkedin.skill  # extract if needed
```

### Method 2: Installation Script
```bash
bash scripts/install-skill.sh content-writer-linkedin
INSTALL_DIR=~/.claude/skills bash scripts/install-skill.sh content-writer-linkedin 1.0.0
```

### Method 3: From Release (GitHub)
```bash
curl -L https://github.com/yourusername/skills/releases/download/v1.0.0/content-writer-linkedin-1.0.0.skill \
  -o content-writer-linkedin-1.0.0.skill
```

### Method 4: For Claude Code
```bash
mkdir -p ~/.claude/skills
curl -L https://raw.githubusercontent.com/yourusername/skills/main/dist/content-writer-linkedin.skill \
  -o ~/.claude/skills/content-writer-linkedin.skill
ls -la ~/.claude/skills/
```

## 6. .skill File Format

`.skill` files are **tar.gz archives** containing `SKILL.md` and `README.md`.

**Manual creation:**
```bash
cd skills/content-writer-linkedin
tar -czf ../../dist/content-writer-linkedin.skill SKILL.md README.md
```

**Manual extraction:**
```bash
tar -tzf content-writer-linkedin.skill  # List contents
tar -xzf content-writer-linkedin.skill  # Extract all
```

## 7. Versioning Strategy

```
MAJOR.MINOR.PATCH
  │      │      └─ Bug fixes (1.0.1)
  │      └────────  New features (1.1.0)
  └───────────────  Breaking changes (2.0.0)
```

### Release Workflow
```bash
# Develop → Package → Tag → Release
git add skills/content-writer-linkedin/
git commit -m "feat: add new feature"
bash scripts/package-skill.sh content-writer-linkedin 1.1.0
git tag -a v1.1.0 -m "Release v1.1.0"
gh release create v1.1.0 dist/content-writer-linkedin-1.1.0.skill
git push origin v1.1.0
```

## 8. Automation with GitHub Actions

Create `.github/workflows/package-skills.yml`:

```yaml
name: Package Skills
on:
  push:
    branches: [main]
    paths: ['skills/**']
  release:
    types: [published]
jobs:
  package:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Package all skills
        run: |
          mkdir -p dist
          for skill_dir in skills/*/; do
            skill_name=$(basename "$skill_dir")
            tar -czf "dist/${skill_name}.skill" -C skills "$skill_name"
          done
      - name: Upload to release
        if: github.event_name == 'release'
        uses: softprops/action-gh-release@v1
        with:
          files: dist/*.skill
```

This automatically packages all skills on push and uploads to releases.

## 9. Complete Installation Example

```bash
# 1. Download latest version
curl -L https://raw.githubusercontent.com/yourusername/skills/main/dist/content-writer-linkedin.skill \
  -o content-writer-linkedin.skill

# 2. Verify
file content-writer-linkedin.skill  # Should show: gzip compressed data

# 3. Extract (if needed)
mkdir -p content-writer-linkedin
tar -xzf content-writer-linkedin.skill -C content-writer-linkedin

# 4. Use in Claude, Code, or wherever
# Claude: Upload the .skill file
# Code: Place in ~/.claude/skills/
```

## 10. Maintenance Checklist

- [ ] Make changes in `skills/skill-name/` directory
- [ ] Test locally
- [ ] Update version number
- [ ] Run `bash scripts/package-skill.sh skill-name VERSION`
- [ ] Verify `.skill` file created
- [ ] Update `CHANGELOG.md`
- [ ] Create git tag: `git tag -a vX.X.X`
- [ ] Push tag: `git push origin vX.X.X`
- [ ] Create GitHub release with `.skill` file

## Summary

| Aspect | Implementation |
|--------|----------------|
| Source Storage | `skills/` directory (git tracked) |
| Distribution | `dist/` directory (generated, gitignored) |
| Versioning | Git tags + semantic versioning |
| Releases | GitHub Releases with `.skill` files |
| Installation | curl + helper scripts |
| Automation | GitHub Actions for packaging |

For technical deep-dive on scripts and structure, see **[GITHUB_SKILLS_STRUCTURE.md](GITHUB_SKILLS_STRUCTURE.md)**.
