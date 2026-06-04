# Skills Distribution Guide

## TL;DR (Quick Start)

Your GitHub structure should be:

```
your-skills-repo/
├── skills/                              # Development (source)
│   └── content-writer-linkedin/
│       ├── SKILL.md
│       └── README.md
├── dist/                                # Distribution (.skill files)
│   ├── content-writer-linkedin.skill
│   └── content-writer-linkedin-1.0.0.skill
└── scripts/
    ├── package-skill.sh
    └── install-skill.sh
```

Users install with:
```bash
curl -L https://raw.githubusercontent.com/yourusername/skills/main/dist/content-writer-linkedin.skill \
  -o content-writer-linkedin.skill
```

---

## Why This Structure?

### ✅ Advantages

| Approach | Dev | Distribution | Versioning | Easy to Share |
|----------|-----|--------------|-----------|--------------|
| **Directory** | ⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐ |
| **.skill files** | ⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **This hybrid** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

---

## Step-by-Step Implementation

### 1. Organize Your Repository

```bash
# Create the structure
cd your-skills-repo

# Create directories
mkdir -p skills/content-writer-linkedin
mkdir -p scripts
mkdir -p dist

# Move your skill source
cp /path/to/SKILL.md skills/content-writer-linkedin/
cp /path/to/README.md skills/content-writer-linkedin/

# Copy scripts
cp package-skill.sh scripts/
cp install-skill.sh scripts/
chmod +x scripts/*.sh

# Commit
git add skills/ scripts/
git commit -m "chore: organize skills structure"
```

### 2. Add to .gitignore

```bash
# Don't version control generated files
echo "dist/*.skill" >> .gitignore
echo ".DS_Store" >> .gitignore
git add .gitignore
git commit -m "chore: update gitignore for dist files"
```

### 3. Package Your Skill

```bash
# First time
bash scripts/package-skill.sh content-writer-linkedin 1.0.0

# This creates:
# dist/content-writer-linkedin.skill          (always latest)
# dist/content-writer-linkedin-1.0.0.skill    (versioned)
# dist/content-writer-linkedin-1.0.0.json     (metadata)
```

### 4. Create GitHub Release

```bash
# Create git tag
git tag -a v1.0.0 -m "Release: content-writer-linkedin v1.0.0"

# Push tag
git push origin v1.0.0

# Using GitHub CLI
gh release create v1.0.0 \
  dist/content-writer-linkedin-1.0.0.skill \
  -t "Content Writer LinkedIn v1.0.0" \
  -n "Initial release with three-mode operation and review loop"
```

### 5. Share Installation URLs

**Latest version** (from main branch):
```
https://raw.githubusercontent.com/yourusername/skills/main/dist/content-writer-linkedin.skill
```

**Specific version** (from release):
```
https://github.com/yourusername/skills/releases/download/v1.0.0/content-writer-linkedin-1.0.0.skill
```

---

## Installation Methods for Users

### Method 1: Direct curl (Simplest)

```bash
# Download latest
curl -L https://raw.githubusercontent.com/yourusername/skills/main/dist/content-writer-linkedin.skill \
  -o content-writer-linkedin.skill

# Extract (if needed)
tar -xzf content-writer-linkedin.skill
```

### Method 2: Installation Script

```bash
# Download and run installer
bash scripts/install-skill.sh content-writer-linkedin

# Or install to specific location
INSTALL_DIR=~/.claude/skills bash scripts/install-skill.sh content-writer-linkedin 1.0.0
```

### Method 3: From Release (GitHub)

```bash
# Download specific version from releases
curl -L https://github.com/yourusername/skills/releases/download/v1.0.0/content-writer-linkedin-1.0.0.skill \
  -o content-writer-linkedin-1.0.0.skill
```

### Method 4: For Claude Code Users

```bash
# Install to Claude Code config directory
mkdir -p ~/.claude/skills
curl -L https://raw.githubusercontent.com/yourusername/skills/main/dist/content-writer-linkedin.skill \
  -o ~/.claude/skills/content-writer-linkedin.skill

# Verify
ls -la ~/.claude/skills/
```

---

## .skill File Format

`.skill` files are **tar.gz archives** containing:
- `SKILL.md` — The skill definition
- `README.md` — Documentation
- (optional) `package.json` — Metadata

**Creating manually:**
```bash
cd skills/content-writer-linkedin
tar -czf ../../dist/content-writer-linkedin.skill SKILL.md README.md
```

**Extracting manually:**
```bash
tar -tzf content-writer-linkedin.skill  # List contents
tar -xzf content-writer-linkedin.skill  # Extract all
```

---

## Versioning Strategy

### Semantic Versioning

```
MAJOR.MINOR.PATCH
  │      │      └─ Bug fixes (1.0.1)
  │      └────────  New features (1.1.0)
  └───────────────  Breaking changes (2.0.0)
```

### Release Workflow

```bash
# Develop and make changes in skills/ directory
git add skills/content-writer-linkedin/
git commit -m "feat: add new feature"

# When ready to release
bash scripts/package-skill.sh content-writer-linkedin 1.1.0

# Create release tag
git tag -a v1.1.0 -m "Release v1.1.0"

# Create GitHub release with .skill file
gh release create v1.1.0 dist/content-writer-linkedin-1.1.0.skill

# Push
git push origin v1.1.0
```

---

## Automation with GitHub Actions

Create `.github/workflows/package-skills.yml`:

```yaml
name: Package Skills

on:
  push:
    branches: [main]
    paths:
      - 'skills/**'
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
            echo "Packaged: ${skill_name}.skill"
          done
      
      - name: Upload to release
        if: github.event_name == 'release'
        uses: softprops/action-gh-release@v1
        with:
          files: dist/*.skill
```

This automatically:
- Packages all skills on push to main
- Uploads to GitHub Releases when you publish
- Keeps `.skill` files up to date

---

## README.md Template for Your Repo

```markdown
# Skills Repository

Professional Claude skills for enhanced productivity.

## Available Skills

### Content Writer (LinkedIn)
Create authentic LinkedIn articles with structured narrative and collaborative review loop.

**Install:**
```bash
curl -L https://raw.githubusercontent.com/yourusername/skills/main/dist/content-writer-linkedin.skill \
  -o content-writer-linkedin.skill
```

**Version:** 1.0.0  
**Size:** 28KB  
**Documentation:** [content-writer-linkedin/README.md](skills/content-writer-linkedin/README.md)

## Installation

### Option 1: Direct Download
```bash
# Latest version
curl -L https://raw.githubusercontent.com/yourusername/skills/main/dist/content-writer-linkedin.skill \
  -o content-writer-linkedin.skill

# Specific version
curl -L https://github.com/yourusername/skills/releases/download/v1.0.0/content-writer-linkedin-1.0.0.skill \
  -o content-writer-linkedin.skill
```

### Option 2: Using Installation Script
```bash
bash scripts/install-skill.sh content-writer-linkedin
INSTALL_DIR=~/.claude/skills bash scripts/install-skill.sh content-writer-linkedin 1.0.0
```

### Option 3: Claude Code
```bash
mkdir -p ~/.claude/skills
curl -L https://raw.githubusercontent.com/yourusername/skills/main/dist/content-writer-linkedin.skill \
  -o ~/.claude/skills/content-writer-linkedin.skill
```

## Usage

See individual skill documentation for usage instructions.

## Versioning

We follow [Semantic Versioning](https://semver.org/).

[View Changelog](CHANGELOG.md)

## License

MIT License - See [LICENSE](LICENSE)
```

---

## Maintenance Checklist

When updating a skill:

- [ ] Make changes in `skills/skill-name/` directory
- [ ] Test the changes locally
- [ ] Update version number in commits
- [ ] Run `bash scripts/package-skill.sh skill-name VERSION`
- [ ] Verify `.skill` file is created
- [ ] Update `CHANGELOG.md`
- [ ] Create git tag: `git tag -a vX.X.X`
- [ ] Push tag: `git push origin vX.X.X`
- [ ] Create GitHub release with `.skill` file
- [ ] Update docs if needed

---

## Summary

| Aspect | Implementation |
|--------|-----------------|
| **Source Storage** | `skills/` directory (git tracked) |
| **Distribution** | `dist/` directory (generated, can be gitignored) |
| **Versioning** | Git tags + semantic versioning |
| **Releases** | GitHub Releases with `.skill` files |
| **Installation** | curl + helper scripts |
| **URLs** | raw.githubusercontent.com for latest, releases for versions |
| **Automation** | GitHub Actions for packaging |

This gives you:
- ✅ Easy local development with version control
- ✅ Simple distribution via one-line curl commands
- ✅ Version pinning for reproducibility
- ✅ Works everywhere (Claude, Code, custom tools)
- ✅ Professional release management
