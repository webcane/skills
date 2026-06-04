#!/bin/bash

###############################################################################
# Install Skill Script
# Downloads and installs a .skill file from the repository
#
# Usage:
#   ./scripts/install-skill.sh <skill-name> [version] [install-dir]
#
# Examples:
#   ./scripts/install-skill.sh content-writer-linkedin
#   ./scripts/install-skill.sh content-writer-linkedin 1.0.0
#   INSTALL_DIR=~/.claude/skills ./scripts/install-skill.sh content-writer-linkedin
#
# Environment Variables:
#   INSTALL_DIR     - Where to install the skill (default: current directory)
#   GITHUB_REPO     - GitHub repository URL (default: yourusername/skills)
#   BRANCH          - Git branch for latest (default: main)
#
###############################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
SKILL_NAME="${1:-}"
VERSION="${2:-latest}"
INSTALL_DIR="${INSTALL_DIR:-.}"
GITHUB_REPO="${GITHUB_REPO:-yourusername/skills}"
BRANCH="${BRANCH:-main}"
GITHUB_RAW="https://raw.githubusercontent.com/$GITHUB_REPO"
GITHUB_RELEASES="https://github.com/$GITHUB_REPO/releases/download"

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

print_step() {
    echo -e "${YELLOW}➜ $1${NC}"
}

show_usage() {
    echo "Usage: $0 <skill-name> [version] [install-dir]"
    echo ""
    echo "Arguments:"
    echo "  skill-name    - Name of the skill to install"
    echo "  version       - Version to install (default: latest)"
    echo "  install-dir   - Where to install (default: current directory)"
    echo ""
    echo "Examples:"
    echo "  $0 content-writer-linkedin"
    echo "  $0 content-writer-linkedin 1.0.0"
    echo "  $0 content-writer-linkedin latest ~/.claude/skills"
    echo ""
    echo "Environment Variables:"
    echo "  INSTALL_DIR   - Installation directory"
    echo "  GITHUB_REPO   - GitHub repo (default: yourusername/skills)"
    echo "  BRANCH        - Branch for latest (default: main)"
}

# Validation
if [ -z "$SKILL_NAME" ]; then
    print_error "Skill name is required"
    echo ""
    show_usage
    exit 1
fi

# Build download URL
if [ "$VERSION" = "latest" ]; then
    DOWNLOAD_URL="$GITHUB_RAW/$BRANCH/dist/${SKILL_NAME}.skill"
    DISPLAY_VERSION="latest"
else
    DOWNLOAD_URL="$GITHUB_RELEASES/v${VERSION}/${SKILL_NAME}-${VERSION}.skill"
    DISPLAY_VERSION="${VERSION}"
fi

# Start installation
echo ""
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo -e "${BLUE}Installing ${SKILL_NAME} (${DISPLAY_VERSION})${NC}"
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo ""

print_step "Preparing installation..."
print_info "Skill: ${BLUE}${SKILL_NAME}${NC}"
print_info "Version: ${BLUE}${DISPLAY_VERSION}${NC}"
print_info "Install directory: ${BLUE}${INSTALL_DIR}${NC}"

# Create install directory
if [ ! -d "$INSTALL_DIR" ]; then
    print_step "Creating directory: $INSTALL_DIR"
    mkdir -p "$INSTALL_DIR"
    print_success "Directory created"
fi

# Download the skill
echo ""
print_step "Downloading from:"
echo "    $DOWNLOAD_URL"

TEMP_DIR=$(mktemp -d)
TEMP_FILE="$TEMP_DIR/${SKILL_NAME}.skill"

if ! curl -L --progress-bar -f "$DOWNLOAD_URL" -o "$TEMP_FILE" 2>/dev/null; then
    print_error "Failed to download skill"
    print_info "URL: $DOWNLOAD_URL"
    echo ""
    
    if [ "$VERSION" != "latest" ]; then
        print_info "Check if version v${VERSION} exists: ${BLUE}${GITHUB_RELEASES}/v${VERSION}${NC}"
    else
        print_info "Check if branch '${BRANCH}' exists"
    fi
    
    rm -rf "$TEMP_DIR"
    exit 1
fi

print_success "Downloaded"

# Verify file
print_step "Verifying archive..."
if ! file "$TEMP_FILE" | grep -q "gzip\|tar\|compressed"; then
    print_error "Invalid file format (expected tar.gz)"
    rm -rf "$TEMP_DIR"
    exit 1
fi
print_success "Archive is valid"

# Extract
echo ""
print_step "Extracting files..."
SKILL_INSTALL_DIR="$INSTALL_DIR/$SKILL_NAME"

# Remove existing if present
if [ -d "$SKILL_INSTALL_DIR" ]; then
    print_info "Removing existing installation..."
    rm -rf "$SKILL_INSTALL_DIR"
fi

mkdir -p "$SKILL_INSTALL_DIR"

if ! tar -xzf "$TEMP_FILE" -C "$SKILL_INSTALL_DIR" 2>/dev/null; then
    print_error "Failed to extract skill archive"
    rm -rf "$TEMP_DIR" "$SKILL_INSTALL_DIR"
    exit 1
fi

print_success "Extracted"

# Verify essential files
echo ""
print_step "Verifying installation..."

if [ ! -f "$SKILL_INSTALL_DIR/SKILL.md" ]; then
    print_error "SKILL.md not found in archive"
    rm -rf "$TEMP_DIR" "$SKILL_INSTALL_DIR"
    exit 1
fi

print_success "SKILL.md found"

if [ -f "$SKILL_INSTALL_DIR/README.md" ]; then
    print_success "README.md found"
fi

# Cleanup
rm -rf "$TEMP_DIR"

# Summary
echo ""
echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo -e "${GREEN}Installation Complete!${NC}"
echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo ""
print_info "Installed to:"
echo "    $SKILL_INSTALL_DIR"
echo ""
print_info "Files:"
ls -lh "$SKILL_INSTALL_DIR" | tail -n +2 | awk '{printf "    %-20s %s\n", $9, $5}'
echo ""
print_info "Next steps:"
echo "    1. Review: cat $SKILL_INSTALL_DIR/README.md"
echo "    2. Use in Claude Code or upload .skill file to Claude.ai"
echo ""

exit 0
