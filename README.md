# 🎓 Professional Skills Distribution Package

Complete solution for distributing Claude skills on GitHub with easy curl-based installation.

## 📦 What's Inside

| File | Purpose |
|------|---------|
| **SUMMARY.md** | Big-picture overview (5 min read) |
| **QUICK_START.md** | Copy-paste commands to get running |
| **DISTRIBUTION_GUIDE.md** | Detailed step-by-step walkthrough |
| **GITHUB_SKILLS_STRUCTURE.md** | Technical deep-dive and best practices |
| `scripts/package-skill.sh` | Convert skill → `.skill` file |
| `scripts/install-skill.sh` | Download and install skills |
| `skills/content-writer-linkedin/` | Your LinkedIn skill (ready to use) |

---

## 🚀 Start Here

1. **Read [SUMMARY.md](SUMMARY.md)** — understand the concept (5 min)
2. **Follow [QUICK_START.md](QUICK_START.md)** — copy-paste commands to set up your repo
3. **Dive deeper with [DISTRIBUTION_GUIDE.md](DISTRIBUTION_GUIDE.md)** or **[GITHUB_SKILLS_STRUCTURE.md](GITHUB_SKILLS_STRUCTURE.md)**

---

## 🎯 The Concept at a Glance

```
Source (development)          Distribution (users)
└─ skills/                   └─ dist/
   └─ content-writer/           ├─ content-writer-linkedin.skill (latest)
      ├─ SKILL.md               └─ content-writer-linkedin-1.0.0.skill (v1.0.0)
      └─ README.md
```

Users install with one curl command:
```bash
curl -L https://raw.githubusercontent.com/yourusername/skills/main/dist/content-writer-linkedin.skill \
  -o content-writer-linkedin.skill
```

---

## ✨ Key Benefits

| For Developers | For Users |
|----------------|-----------|
| Version control of source files | One-line curl installation |
| Easy updates and maintenance | Version pinning for reproducibility |
| Clear change history | Works everywhere (Claude, Code, custom tools) |
| Professional release management | No manual extraction needed |
| Automated packaging (GitHub Actions) | Clear, verifiable downloads |

---

## 🔗 Installation URLs (After Setup)

**Latest version** (from main branch):
```
https://raw.githubusercontent.com/yourusername/skills/main/dist/content-writer-linkedin.skill
```

**Specific version** (from releases):
```
https://github.com/yourusername/skills/releases/download/v1.0.0/content-writer-linkedin-1.0.0.skill
```

---

## ✅ Checklist

- [ ] Read [SUMMARY.md](SUMMARY.md) for overview
- [ ] Follow [QUICK_START.md](QUICK_START.md) commands
- [ ] Test locally
- [ ] Push to GitHub
- [ ] Create GitHub Release
- [ ] Share installation URL

---

## 📋 CHANGELOG

See **[CHANGELOG.md](CHANGELOG.md)** for version history.
