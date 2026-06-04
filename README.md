# Claude Skills Repository

Distribute Claude skills via GitHub with version control and one-line installation.

## How It Works

```
skills/          →   package-skill.sh   →   dist/*.skill   →   GitHub Release   →   curl install
(source, git)                               (generated)
```

## Quick Setup

```bash
# 1. Package your skill
bash scripts/package-skill.sh <skillname> 1.0.0

# 2. Release
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
gh release create v1.0.0 dist/<skillname>-1.0.0.skill

# 3. Users install
curl -L https://raw.githubusercontent.com/webcane/skills/main/dist/<skillname>.skill \
  -o <skillname>.skill
```

For full setup instructions, see [QUICK_START.md](QUICK_START.md).

## Repository Structure

```
├── skills/content-writer-linkedin/   # Source (git tracked)
│   ├── SKILL.md
│   └── README.md
├── scripts/
│   ├── package-skill.sh              # skill dir → .skill file
│   └── install-skill.sh             # download & extract .skill
├── dist/                             # Generated, gitignored
├── .github/workflows/package-skills.yml
├── CHANGELOG.md
└── .gitignore
```

## Skills

| Skill | Description |
|-------|-------------|
| [content-writer-linkedin](skills/content-writer-linkedin/) | Write authentic LinkedIn articles |

## Installation URLs

```bash
# Latest
curl -L https://raw.githubusercontent.com/webcane/skills/main/dist/content-writer-linkedin.skill \
  -o content-writer-linkedin.skill

# Pinned version
curl -L https://github.com/webcane/skills/releases/download/v1.0.0/content-writer-linkedin-1.0.0.skill \
  -o content-writer-linkedin.skill
```