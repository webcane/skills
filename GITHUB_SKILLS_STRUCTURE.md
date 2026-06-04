# Optimal GitHub Skills Repository Structure

## Recommended Structure

```
your-skills-repo/
│
├── .github/
│   └── workflows/
│       └── package-skills.yml          # Auto-package skills on release
│
├── skills/
│   ├── content-writer-linkedin/
│   │   ├── SKILL.md                   # Source (development)
│   │   ├── README.md
│   │   └── package.json               # Metadata (optional)
│   │
│   └── [other-skill]/
│       ├── SKILL.md
│       └── README.md
│
├── dist/                              # Packaged .skill files (generated)
│   ├── content-writer-linkedin.skill
│   ├── content-writer-linkedin-1.0.0.skill
│   └── [other-skill].skill
│
├── scripts/
│   ├── package-skill.sh               # Package single skill
│   ├── install-skill.sh               # Installation helper
│   └── publish-release.sh             # Automate releases
│
├── LICENSE
├── README.md
└── CHANGELOG.md
```

---

## 1. Keep Source in Repo (For Development)

**Why:** Version control, collaboration, easy diffs

```bash
skills/
└── content-writer-linkedin/
    ├── SKILL.md          # Main skill file
    └── README.md         # Usage docs
```

**Commit messages:**
```bash
git commit -m "feat(content-writer-linkedin): add review loop"
git commit -m "docs(content-writer-linkedin): update examples"
```

---

## 2. Package into `.skill` Files (For Distribution)

### Create `scripts/package-skill.sh`:

```bash
#!/bin/bash

# Package a single skill into .skill file
SKILL_NAME=$1
SKILL_DIR="skills/${SKILL_NAME}"
DIST_DIR="dist"

if [ ! -d "$SKILL_DIR" ]; then
    echo "Error: Skill not found at $SKILL_DIR"
    exit 1
fi

# Create dist directory
mkdir -p "$DIST_DIR"

# Package as tar.gz with .skill extension
# (Claude expects .skill to be valid zip/tar)
cd "$SKILL_DIR"
tar -czf "../../$DIST_DIR/${SKILL_NAME}.skill" \
    SKILL.md README.md

echo "✓ Packaged: $DIST_DIR/${SKILL_NAME}.skill"

# Also create versioned file
VERSION=$(grep "^version:" package.json 2>/dev/null | cut -d'"' -f2 || echo "1.0.0")
cp "$DIST_DIR/${SKILL_NAME}.skill" \
   "$DIST_DIR/${SKILL_NAME}-${VERSION}.skill"

echo "✓ Versioned: $DIST_DIR/${SKILL_NAME}-${VERSION}.skill"
```

### Run packaging:
```bash
bash scripts/package-skill.sh content-writer-linkedin
```

---

## 3. Use GitHub Releases (For Easy Downloads)

### Create release with packaged files:

```bash
# Create git tag
git tag -a v1.0.0 -m "Release: content-writer-linkedin v1.0.0"

# Push tag
git push origin v1.0.0
```

### Create GitHub Release:
```bash
# Using GitHub CLI:
gh release create v1.0.0 \
  dist/content-writer-linkedin-1.0.0.skill \
  -t "Content Writer LinkedIn v1.0.0" \
  -n "Initial release with three-mode operation and review loop"
```

**Result:** Release page shows packaged `.skill` files ready to download

---

## 4. Installation via curl

### Method A: Direct Download from Raw GitHub

```bash
# Download and install in one command
curl -L https://raw.githubusercontent.com/yourusername/skills/main/dist/content-writer-linkedin.skill \
  -o content-writer-linkedin.skill

# Or from releases
curl -L https://github.com/yourusername/skills/releases/download/v1.0.0/content-writer-linkedin-1.0.0.skill \
  -o content-writer-linkedin.skill
```

### Method B: Installation Script

Create `scripts/install-skill.sh`:

```bash
#!/bin/bash

SKILL_NAME=${1:-content-writer-linkedin}
VERSION=${2:-latest}
INSTALL_DIR="${INSTALL_DIR:-.}"

echo "📥 Installing $SKILL_NAME..."

# Determine download URL
if [ "$VERSION" = "latest" ]; then
    URL="https://raw.githubusercontent.com/yourusername/skills/main/dist/${SKILL_NAME}.skill"
else
    URL="https://github.com/yourusername/skills/releases/download/v${VERSION}/${SKILL_NAME}-${VERSION}.skill"
fi

# Download
TEMP_FILE=$(mktemp)
if curl -L "$URL" -o "$TEMP_FILE" 2>/dev/null; then
    # Extract and install
    mkdir -p "$INSTALL_DIR/$SKILL_NAME"
    tar -xzf "$TEMP_FILE" -C "$INSTALL_DIR/$SKILL_NAME"
    rm "$TEMP_FILE"
    
    echo "✓ Installed: $INSTALL_DIR/$SKILL_NAME"
    echo "✓ Files:"
    ls -la "$INSTALL_DIR/$SKILL_NAME/"
else
    echo "✗ Download failed: $URL"
    exit 1
fi
```

### Usage:

```bash
# Install latest from main branch
bash scripts/install-skill.sh content-writer-linkedin

# Install specific version
bash scripts/install-skill.sh content-writer-linkedin 1.0.0

# Install to specific directory
INSTALL_DIR=~/.claude/skills bash scripts/install-skill.sh content-writer-linkedin
```

---

## 5. Installation URLs (Share These)

### For Claude:
```
https://raw.githubusercontent.com/yourusername/skills/main/dist/content-writer-linkedin.skill
```

### For Code/CLI:
```bash
curl -L https://raw.githubusercontent.com/yourusername/skills/main/dist/content-writer-linkedin.skill \
  -o ~/.claude/skills/content-writer-linkedin.skill
```

### From Release:
```bash
curl -L https://github.com/yourusername/skills/releases/download/v1.0.0/content-writer-linkedin-1.0.0.skill \
  -o content-writer-linkedin.skill
```

---

## 6. GitHub Actions Auto-Packaging

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
      
      - name: Create dist directory
        run: mkdir -p dist
      
      - name: Package skills
        run: |
          for skill_dir in skills/*/; do
            skill_name=$(basename "$skill_dir")
            tar -czf "dist/${skill_name}.skill" -C "skills" "$skill_name"
            echo "✓ Packaged: ${skill_name}.skill"
          done
      
      - name: Upload as artifacts
        uses: actions/upload-artifact@v3
        with:
          name: skills
          path: dist/
      
      - name: Upload to release
        if: github.event_name == 'release'
        uses: softprops/action-gh-release@v1
        with:
          files: dist/*.skill
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## 7. README.md Installation Instructions

```markdown
# Skills Repository

Install skills with curl:

### Latest Version (from main branch)

```bash
curl -L https://raw.githubusercontent.com/yourusername/skills/main/dist/content-writer-linkedin.skill \
  -o content-writer-linkedin.skill
```

### Specific Version (from releases)

```bash
curl -L https://github.com/yourusername/skills/releases/download/v1.0.0/content-writer-linkedin-1.0.0.skill \
  -o content-writer-linkedin.skill
```

### Using Installation Script

```bash
curl -L https://raw.githubusercontent.com/yourusername/skills/main/scripts/install-skill.sh | bash
# Or with options:
bash scripts/install-skill.sh content-writer-linkedin 1.0.0
```

### For Claude Code
```bash
# Install to Claude Code config
curl -L https://raw.githubusercontent.com/yourusername/skills/main/dist/content-writer-linkedin.skill \
  -o ~/.claude/skills/content-writer-linkedin.skill
```

## Available Skills

- **content-writer-linkedin** - Authentic LinkedIn articles with review loop
- [other-skill] - Description

## Installation Locations

- **Claude.ai:** Uploaded via UI
- **Claude Code:** `~/.claude/skills/`
- **Custom:** Any directory via curl

See [CHANGELOG.md](CHANGELOG.md) for version history.
```

---

## 8. CHANGELOG.md Template

```markdown
# Changelog

## [1.0.0] - 2026-06-04

### Added
- Initial release of content-writer-linkedin skill
- Three-mode operation (Outline, Research/Verify, Write)
- Collaborative review loop
- Sentence rhythm guidance with examples
- Flesch-Kincaid 6-8th grade readability target
- 40+ word/phrase avoidance list
- Word count targets per section

### Changed
- Merged best practices from original content-writer skill

### Features
- Personal narrative focus
- Minto Pyramid principle structure
- LinkedIn-optimized guidelines

## Versioning

We follow [Semantic Versioning](https://semver.org/):
- PATCH: Bug fixes (1.0.1)
- MINOR: New features (1.1.0)
- MAJOR: Breaking changes (2.0.0)
```

---

## Complete Installation Example

### Scenario: User wants to install your skill

```bash
# 1. Download latest version
curl -L https://raw.githubusercontent.com/yourusername/skills/main/dist/content-writer-linkedin.skill \
  -o content-writer-linkedin.skill

# 2. Verify file
file content-writer-linkedin.skill
# Should show: gzip compressed data

# 3. Extract (if needed)
mkdir -p content-writer-linkedin
tar -xzf content-writer-linkedin.skill -C content-writer-linkedin
ls content-writer-linkedin/

# 4. Use in Claude, Code, or wherever
# Claude: Upload the .skill file
# Code: Place in ~/.claude/skills/
```

---

## Summary: Best Practices

| Aspect | Approach |
|--------|----------|
| **Source Storage** | Directory in repo (`skills/`) |
| **Version Control** | Git tags and semantic versioning |
| **Distribution** | GitHub Releases + raw.githubusercontent.com |
| **Installation** | curl downloads + helper scripts |
| **Documentation** | README + CHANGELOG in repo |
| **Automation** | GitHub Actions for packaging |
| **Packaging Format** | `.skill` (tar.gz) files |

This setup lets users:
✅ Download latest with curl  
✅ Pin to specific versions  
✅ Use installation scripts  
✅ Easy URL sharing  
✅ Works everywhere (Claude, Code, custom tools)
