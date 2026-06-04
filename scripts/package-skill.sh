#!/bin/bash

###############################################################################
# Package Skill Script
# Converts a skill directory into a distributable .skill file (tar.gz)
#
# Usage:
#   ./scripts/package-skill.sh <skill-name> [version]
#
# Examples:
#   ./scripts/package-skill.sh content-writer-linkedin
#   ./scripts/package-skill.sh content-writer-linkedin 1.0.0
#
###############################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SKILL_NAME="${1:-}"
VERSION="${2:-1.0.0}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="$REPO_ROOT/skills"
DIST_DIR="$REPO_ROOT/dist"
SKILL_DIR="$SKILLS_DIR/$SKILL_NAME"

# Functions
print_error() {
    echo -e "${RED}✗ Error: $1${NC}" >&2
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

show_usage() {
    echo "Usage: $0 <skill-name> [version]"
    echo ""
    echo "Examples:"
    echo "  $0 content-writer-linkedin"
    echo "  $0 content-writer-linkedin 1.0.0"
    echo ""
    echo "Available skills:"
    if [ -d "$SKILLS_DIR" ]; then
        ls -d "$SKILLS_DIR"/*/ 2>/dev/null | xargs -I {} basename {} | sed 's/^/  - /'
    else
        echo "  (skills directory not found)"
    fi
}

# Validation
if [ -z "$SKILL_NAME" ]; then
    print_error "Skill name is required"
    echo ""
    show_usage
    exit 1
fi

if [ ! -d "$SKILL_DIR" ]; then
    print_error "Skill not found: $SKILL_NAME"
    echo "Expected location: $SKILL_DIR"
    echo ""
    show_usage
    exit 1
fi

if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    print_error "SKILL.md not found in $SKILL_DIR"
    exit 1
fi

# Create dist directory
mkdir -p "$DIST_DIR"

print_info "Packaging skill: ${BLUE}${SKILL_NAME}${NC}"
print_info "Version: ${BLUE}${VERSION}${NC}"
print_info "From: ${BLUE}${SKILL_DIR}${NC}"

# List files to be packaged
echo ""
print_info "Files to include:"
ls -lh "$SKILL_DIR" | tail -n +2 | awk '{print "  - " $9 " (" $5 ")"}'

# Create the .skill file (tar.gz format)
cd "$SKILL_DIR"
SKILL_FILE="${DIST_DIR}/${SKILL_NAME}.skill"
tar -czf "$SKILL_FILE" --exclude='.DS_Store' --exclude='*.swp' .

# Verify package was created
if [ ! -f "$SKILL_FILE" ]; then
    print_error "Failed to create skill file"
    exit 1
fi

SKILL_SIZE=$(du -h "$SKILL_FILE" | cut -f1)
print_success "Created: $SKILL_FILE ($SKILL_SIZE)"

# Create versioned copy
VERSIONED_FILE="${DIST_DIR}/${SKILL_NAME}-${VERSION}.skill"
cp "$SKILL_FILE" "$VERSIONED_FILE"
print_success "Created: $VERSIONED_FILE"

# Create metadata file
METADATA_FILE="${DIST_DIR}/${SKILL_NAME}-${VERSION}.json"
cat > "$METADATA_FILE" << EOF
{
  "name": "${SKILL_NAME}",
  "version": "${VERSION}",
  "created": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "source": "https://github.com/yourusername/skills",
  "size": "$(du -b "$SKILL_FILE" | cut -f1) bytes",
  "files": [
    "SKILL.md",
    "README.md"
  ]
}
EOF
print_success "Created metadata: $METADATA_FILE"

# Summary
echo ""
echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo -e "${GREEN}Packaging Complete!${NC}"
echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo ""
print_info "Unversioned (always latest):"
echo "    $SKILL_FILE"
echo ""
print_info "Versioned (pinned to ${VERSION}):"
echo "    $VERSIONED_FILE"
echo ""
print_info "Metadata:"
echo "    $METADATA_FILE"
echo ""
print_info "Download URLs:"
echo "    Latest (main): https://raw.githubusercontent.com/yourusername/skills/main/dist/${SKILL_NAME}.skill"
echo "    Version ${VERSION}: https://github.com/yourusername/skills/releases/download/v${VERSION}/${SKILL_NAME}-${VERSION}.skill"
echo ""
print_info "Installation (curl):"
echo "    curl -L https://raw.githubusercontent.com/yourusername/skills/main/dist/${SKILL_NAME}.skill -o ${SKILL_NAME}.skill"
echo ""
