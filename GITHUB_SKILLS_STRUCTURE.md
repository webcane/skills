# Optimal GitHub Skills Repository Structure

Technical deep-dive on structure, scripts, and best practices. For quick setup, see **[QUICK_START.md](QUICK_START.md)**. For step-by-step walkthrough, see **[DISTRIBUTION_GUIDE.md](DISTRIBUTION_GUIDE.md)**.

---

## Recommended Structure

```
your-skills-repo/
├── .github/workflows/
│   └── package-skills.yml          # Auto-package on release
├── skills/
│   └── content-writer-linkedin/
│       ├── SKILL.md                # Source (development)
│       ├── README.md               # Usage docs
│       └── package.json            # Metadata (optional)
├── dist/                           # Packaged .skill files (generated)
│   ├── content-writer-linkedin.skill
│   └── content-writer-linkedin-1.0.0.skill
├── scripts/
│   ├── package-skill.sh            # Package single skill
│   ├── install-skill.sh            # Installation helper
│   └── publish-release.sh          # Automate releases
├── LICENSE
├── README.md
└── CHANGELOG.md
```

---

## 1. Source in Repo (Development)

Keep source in `skills/` for version control, collaboration, and easy diffs.

**Commit convention:**
```bash
git commit -m "feat(content-writer-linkedin): add review loop"
git commit -m "docs(content-writer-linkedin): update examples"
```

---

## 2. Packaging Script

**File:** `scripts/package-skill.sh`

Converts a skill directory into `.skill` files (latest + versioned).

**Usage:** `bash scripts/package-skill.sh content-writer-linkedin`

---

## 3. Installation Script

**File:** `scripts/install-skill.sh`

Downloads and extracts a `.skill` file from GitHub.

**Usage:**
```bash
bash scripts/install-skill.sh content-writer-linkedin        # latest
bash scripts/install-skill.sh content-writer-linkedin 1.0.0  # specific version
INSTALL_DIR=~/.claude/skills bash scripts/install-skill.sh content-writer-linkedin
```

---

## 4. GitHub Actions

**File:** `.github/workflows/package-skills.yml`

Automatically packages all skills on push to `main` and uploads `.skill` files to GitHub Releases when published.

---

## Summary: Best Practices

| Aspect | Approach |
|--------|----------|
| Source Storage | Directory in repo (`skills/`) |
| Version Control | Git tags + semantic versioning |
| Distribution | GitHub Releases + raw.githubusercontent.com |
| Installation | curl downloads + helper scripts |
| Documentation | README + CHANGELOG in repo |
| Automation | GitHub Actions for packaging |
| Packaging Format | `.skill` (tar.gz) files |
