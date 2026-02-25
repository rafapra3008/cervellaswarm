#!/bin/bash
# =============================================================================
# sync-to-public.sh - Safe sync from private repo to public
# =============================================================================
# Version: 3.3.0 (S400 - Worktree cleanup, .git/.example exclusion, --no-verify push)
#
# HOW IT WORKS:
# 1. Creates temporary worktree from public/main
# 2. Copies ONLY public files to worktree (whitelist)
# 3. Security verification: blacklist + CONTENT SCANNING (all text files)
# 4. Commit and push from worktree
# 5. Removes worktree
#
# USAGE:
#   ./scripts/git/sync-to-public.sh [commit-message]
#   ./scripts/git/sync-to-public.sh --dry-run    # Preview without push
#
# CHANGELOG:
#   v3.2.0 (S367) - Scan ALL text files via grep -rI (was: 9 specific extensions)
#                  - Added Check 5: sensitive config files (.env, secrets, credentials)
#                  - Added .env to filename blacklist
#                  - Added "famiglia digitale" content pattern
#                  - All messages and comments translated to English
#   v3.0.0 (S363) - Content scanning with 12 patterns
#   v2.0.0 (S362) - Whitelist approach + blacklist
#   v1.0.0        - Initial dual-repo sync
# =============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
WORKTREE_DIR="/tmp/cervellaswarm-public-sync-$$"
WORKTREE_BRANCH="public-sync-temp-$$"
DRY_RUN=0

# Parse arguments
for arg in "$@"; do
    if [ "$arg" = "--dry-run" ]; then
        DRY_RUN=1
        shift
    fi
done

# Public files/directories (whitelist - ONLY these go to public repo)
PUBLIC_FILES=(
    "packages"
    "README.md"
    "CHANGELOG.md"
    "LICENSE"
    "NOTICE"
    "CONTRIBUTING.md"
    "CODE_OF_CONDUCT.md"
    "SECURITY.md"
    ".github"
    ".gitignore"
    "docs/AGENTS_REFERENCE.md"
    "docs/ARCHITECTURE.md"
    "docs/GETTING_STARTED.md"
    "docs/SNCP_GUIDE.md"
    "docs/SEMANTIC_SEARCH.md"
    "docs/ARCHITECT_PATTERN.md"
    "docs/GIT_ATTRIBUTION.md"
    "docs/DUAL_REPO_STRATEGY.md"
    "docs/blog"
)

# Files/directories that must NEVER appear in public root
BLACKLIST_ROOT_PATHS=(
    ".sncp"
    ".swarm"
    ".mcp.json"
    "NORD.md"
    "COSTITUZIONE.md"
    "MANIFESTO.md"
    "data"
    "reports"
    "logs"
    "config"
    "cervellaswarm-extension"
)

# Patterns that must NOT appear in any filename
BLACKLIST_FILENAME_PATTERNS=(
    "PROMPT_RIPRESA"
    "MAPPA_"
    "_PRIVATO"
    "_INTERNO"
    "RESEARCH_"
    "RICERCA_"
    "PASSAGGIO_CONSEGNA"
    "HANDOFF_"
    "CREDENZIALI"
    ".env"
)

# Directories that must NOT exist in public
BLACKLIST_DIRS=(
    "docs/studio"
    "scripts/memory"
    "scripts/learning"
    "scripts/engineer"
    "scripts/cron"
)

# Content patterns that must NOT appear in any published file
# These are scanned INSIDE file content (all text files via grep -rI)
BLACKLIST_CONTENT_PATTERNS=(
    "/Users/rafapra"
    "~/Developer/"
    '$HOME/Developer'
    # NOTE: rafapra3008 is the PUBLIC GitHub username (repo URL) - NOT blacklisted
    # Email is already caught by @gmail.com, local paths by /Users/rafapra
    "@gmail.com"
    "192.168."
    "acct_1"
    "data-frame-476309"
    "miracollogeminifocus"
    "ContabilitaAntigravity"
    "CervellaBrasil"
    "cervellabrasil"
    "chavefy"
    "progetti/cervellacostruzione"
    # NOTE: "contabilita" removed - common Italian word (=accounting), repo name
    # "ContabilitaAntigravity" (above) already catches the private repo name.
    # MCP code uses "contabilita" as SNCP project alias - will be made configurable in F3.
    "famiglia digitale"
)

cleanup() {
    echo -e "\n${CYAN}Cleaning up...${NC}"
    cd "$REPO_ROOT"
    git worktree remove "$WORKTREE_DIR" --force 2>/dev/null || true
    git branch -D "$WORKTREE_BRANCH" 2>/dev/null || true
}

trap cleanup EXIT

# Copy function that excludes node_modules and dist
copy_excluding() {
    local src="$1"
    local dst="$2"
    
    if [ -d "$src" ]; then
        # For directories, use rsync to exclude node_modules etc.
        rsync -a --exclude='node_modules' --exclude='dist' --exclude='.turbo' "$src/" "$dst/"
    else
        cp "$src" "$dst"
    fi
}

# =============================================================================
# MAIN
# =============================================================================

echo -e "${BOLD}${CYAN}"
echo "=============================================="
echo "  SYNC TO PUBLIC - v3.2 (Extended Scanning)"
if [ "$DRY_RUN" -eq 1 ]; then
    echo -e "  ${YELLOW}[DRY RUN - no push]${CYAN}"
fi
echo "=============================================="
echo -e "${NC}"

cd "$REPO_ROOT"

# Verify we're in a git repo root
if [ ! -d ".git" ]; then
    echo -e "${RED}ERROR: Not in a git repo root!${NC}"
    exit 1
fi

# Verify public remote exists
if ! git remote get-url public &>/dev/null; then
    echo -e "${RED}ERROR: Remote 'public' not configured!${NC}"
    echo "Run: git remote add public https://github.com/rafapra3008/cervellaswarm.git"
    exit 1
fi

echo -e "${YELLOW}Private repo:${NC}  $(git remote get-url origin)"
echo -e "${YELLOW}Public repo:${NC}  $(git remote get-url public)"
echo ""

# =============================================================================
# STEP 1: Fetch public and create worktree
# =============================================================================

echo -e "${CYAN}[1/6] Fetch public/main...${NC}"
git fetch public

echo -e "${CYAN}[2/6] Creating isolated worktree...${NC}"
git worktree add -b "$WORKTREE_BRANCH" "$WORKTREE_DIR" public/main

# =============================================================================
# STEP 2: Copy public files to worktree (exclude node_modules)
# =============================================================================

echo -e "${CYAN}[3/6] Copying public files (excluding node_modules/dist)...${NC}"
cd "$WORKTREE_DIR"

# Clean worktree: remove all tracked content, keep only .git
# This ensures ONLY whitelisted files end up in the public repo
git rm -rf . > /dev/null 2>&1 || true
git checkout -- .gitignore 2>/dev/null || true

for item in "${PUBLIC_FILES[@]}"; do
    src="$REPO_ROOT/$item"
    if [ -e "$src" ]; then
        # Create parent directory if needed
        parent_dir=$(dirname "$item")
        if [ "$parent_dir" != "." ]; then
            mkdir -p "$parent_dir"
        fi
        
        # Copy (file or directory)
        if [ -d "$src" ]; then
            rm -rf "$item" 2>/dev/null || true
            mkdir -p "$item"
            copy_excluding "$src" "$item"
            echo -e "  ${GREEN}+${NC} $item/ (excluding node_modules)"
        else
            cp "$src" "$item"
            echo -e "  ${GREEN}+${NC} $item"
        fi
    fi
done

# =============================================================================
# STEP 3: Security verification - no private files
# =============================================================================

echo ""
echo -e "${CYAN}[4/6] Security verification (6 checks)...${NC}"

SECURITY_FAIL=0

# Check 1: Root paths that must not exist
for item in "${BLACKLIST_ROOT_PATHS[@]}"; do
    if [ -e "$item" ]; then
        echo -e "  ${RED}PRIVATE FILE/DIR IN ROOT: ${item}${NC}"
        SECURITY_FAIL=1
    fi
done

# Check 2: Filename patterns (exclude node_modules and .git)
for pattern in "${BLACKLIST_FILENAME_PATTERNS[@]}"; do
    matches=$(find . -path "./node_modules" -prune -o -path "./.git" -prune -o -path "./packages/*/node_modules" -prune -o -name "*${pattern}*" -print 2>/dev/null | /usr/bin/grep -v "^$" | /usr/bin/grep -v "\.example$" || true)
    if [ -n "$matches" ]; then
        echo -e "  ${RED}PRIVATE FILENAME PATTERN: ${pattern}${NC}"
        echo "$matches"
        SECURITY_FAIL=1
    fi
done

# Check 3: Directories that must not exist
for dir in "${BLACKLIST_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo -e "  ${RED}PRIVATE DIRECTORY: ${dir}${NC}"
        SECURITY_FAIL=1
    fi
done

# Check 4: node_modules must not have been copied
if find . -type d -name "node_modules" 2>/dev/null | /usr/bin/grep -q .; then
    echo -e "  ${RED}FOUND node_modules - must not be in public!${NC}"
    SECURITY_FAIL=1
fi

# Check 5: Sensitive config files (.env, secrets, credentials)
env_files=$(find . -name ".env" -o -name ".env.local" -o -name ".env.production" -o -name "secrets.*" -o -name "credentials.*" 2>/dev/null | /usr/bin/grep -v '.git/' || true)
if [ -n "$env_files" ]; then
    echo -e "  ${RED}SENSITIVE CONFIG FILES FOUND:${NC}"
    echo "$env_files"
    SECURITY_FAIL=1
fi

# Check 6 (was 5): CONTENT SCANNING - search ALL text files for sensitive patterns
# Uses grep -rI to automatically skip binary files (images, fonts, etc.)
# This is more thorough than scanning specific extensions (v3.0 approach)
echo -e "  ${CYAN}Scanning ALL text files for sensitive patterns...${NC}"
CONTENT_SCAN_COUNT=0
for pattern in "${BLACKLIST_CONTENT_PATTERNS[@]}"; do
    # -r: recursive, -l: filenames only, -I: skip binary files
    # Exclude .git/ and node_modules/ directories
    matches=$(/usr/bin/grep -rlI "$pattern" . --exclude-dir='.git' --exclude='.git' --exclude-dir='node_modules' 2>/dev/null || true)
    if [ -n "$matches" ]; then
        echo -e "  ${RED}SENSITIVE CONTENT FOUND: '${pattern}'${NC}"
        echo "$matches" | head -5
        match_count=$(echo "$matches" | wc -l | tr -d ' ')
        if [ "$match_count" -gt 5 ]; then
            echo "  ... and $((match_count - 5)) more files"
        fi
        SECURITY_FAIL=1
    else
        CONTENT_SCAN_COUNT=$((CONTENT_SCAN_COUNT + 1))
    fi
done
echo -e "  ${GREEN}Content scan: ${CONTENT_SCAN_COUNT}/${#BLACKLIST_CONTENT_PATTERNS[@]} patterns clear${NC}"

if [ "$SECURITY_FAIL" -eq 1 ]; then
    echo ""
    echo -e "${RED}=============================================="
    echo -e "  SECURITY FAILED! Sync aborted."
    echo -e "  Fix the files above before syncing."
    echo -e "==============================================${NC}"
    exit 1
fi

echo -e "  ${GREEN}OK - No private files or sensitive content found${NC}"

# =============================================================================
# STEP 4: Show diff and ask for confirmation
# =============================================================================

echo ""
echo -e "${CYAN}[5/6] Changes to sync:${NC}"
git add -A

# Show only modified files
CHANGES=$(git status --porcelain | wc -l | tr -d ' ')

if [ "$CHANGES" -eq 0 ]; then
    echo ""
    echo -e "${YELLOW}No changes to sync.${NC}"
    echo "Public repo is already up to date."
    exit 0
fi

# Show summary
echo ""
echo "Modified: $(git status --porcelain | /usr/bin/grep '^M' | wc -l | tr -d ' ')"
echo "Added:    $(git status --porcelain | /usr/bin/grep '^A' | wc -l | tr -d ' ')"
echo "Deleted:  $(git status --porcelain | /usr/bin/grep '^D' | wc -l | tr -d ' ')"
echo ""

# Show first 20 files
echo "First 20 changes:"
git status --short | head -20
if [ "$CHANGES" -gt 20 ]; then
    echo "... and $((CHANGES - 20)) more files"
fi

echo ""
echo -e "${YELLOW}=============================================="
echo -e "  TOTAL: $CHANGES files to sync"
echo -e "==============================================${NC}"
echo ""
echo "You are about to push to the PUBLIC repo:"
echo "  $(git remote get-url public 2>/dev/null || echo 'public')"
echo ""

# Commit message
if [ -n "$1" ]; then
    COMMIT_MSG="$1"
else
    # Default: read version from package.json if available
    if [ -f "packages/cli/package.json" ]; then
        VERSION=$(/usr/bin/grep '"version"' packages/cli/package.json | head -1 | sed 's/.*"version": "\([^"]*\)".*/\1/')
        COMMIT_MSG="sync: v${VERSION} from private"
    else
        COMMIT_MSG="sync: from private - $(date +%Y-%m-%d)"
    fi
fi

echo -e "Commit message: ${CYAN}${COMMIT_MSG}${NC}"
echo ""

if [ "$DRY_RUN" -eq 1 ]; then
    echo -e "${YELLOW}=============================================="
    echo -e "  DRY RUN COMPLETE"
    echo -e "  $CHANGES files ready for sync"
    echo -e "  Security: PASS (6 checks passed)"
    echo -e "==============================================${NC}"
    exit 0
fi

read -p "Proceed? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo -e "${YELLOW}Sync cancelled.${NC}"
    exit 0
fi

# =============================================================================
# STEP 5: Commit and push
# =============================================================================

echo ""
echo -e "${CYAN}[6/6] Commit and push...${NC}"

# Commit with --no-verify to skip hooks from the main repo
git commit --no-verify -m "$COMMIT_MSG

Co-Authored-By: CervellaSwarm Bot <noreply@users.noreply.github.com>"

# Push from worktree (use HEAD since we're on a temp branch)
# --no-verify: skip pre-push hooks from the main repo (they check against origin, not public)
git push --no-verify public HEAD:main

# =============================================================================
# DONE
# =============================================================================

echo ""
echo -e "${GREEN}=============================================="
echo -e "  SYNC COMPLETE!"
echo -e "==============================================${NC}"
echo ""
echo "Public repo has been updated."
echo ""
echo "Next steps (if release):"
echo "  1. Verify on GitHub"
echo "  2. npm publish (if needed)"
echo "  3. Create tag: git tag vX.Y.Z && git push public vX.Y.Z"
