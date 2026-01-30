#!/bin/bash

# checkpoint.sh - Automated checkpoint for CervellaSwarm sessions
# Author: Cervella Regina
# Date: 30 Gennaio 2026
# Version: 1.0.0
#
# Usage:
#   checkpoint.sh [session_number] [description]
#   checkpoint.sh 321 "SNCP 3.0 Memory & Security"

set -euo pipefail

# Colors
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Arguments
SESSION="${1:-}"
DESCRIPTION="${2:-}"

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Help
if [[ "${1:-}" == "--help" ]] || [[ "${1:-}" == "-h" ]]; then
    echo "Usage: checkpoint.sh [session_number] [description]"
    echo ""
    echo "Creates a checkpoint commit with standard format."
    echo ""
    echo "Arguments:"
    echo "  session_number   Session number (e.g., 321)"
    echo "  description      Short description of work done"
    echo ""
    echo "Examples:"
    echo "  checkpoint.sh 321 'SNCP 3.0 Memory & Security'"
    echo "  checkpoint.sh 322 'Test Coverage Improvement'"
    echo ""
    echo "What it does:"
    echo "  1. Runs file limits check"
    echo "  2. Shows git status"
    echo "  3. Adds relevant files"
    echo "  4. Creates checkpoint commit"
    echo "  5. Pushes to origin"
    exit 0
fi

# Validate arguments
if [[ -z "$SESSION" ]]; then
    echo -e "${YELLOW}Session number required${NC}"
    read -p "Enter session number: " SESSION
fi

if [[ -z "$DESCRIPTION" ]]; then
    echo -e "${YELLOW}Description required${NC}"
    read -p "Enter description: " DESCRIPTION
fi

cd "$PROJECT_ROOT"

echo -e "${BLUE}=== CHECKPOINT S${SESSION} ===${NC}"
echo ""

# 1. Run file limits check
echo -e "${BLUE}1. Checking file limits...${NC}"
if [[ -f "scripts/sncp/check-ripresa-size.sh" ]]; then
    ./scripts/sncp/check-ripresa-size.sh || true
fi
echo ""

# 2. Show git status
echo -e "${BLUE}2. Git status:${NC}"
git status --short
echo ""

# 3. Check for changes
if [[ -z "$(git status --porcelain)" ]]; then
    echo -e "${YELLOW}No changes to commit${NC}"
    exit 0
fi

# 4. Add files (excluding sensitive)
echo -e "${BLUE}3. Adding files...${NC}"
git add -A
git reset HEAD -- '*.env' '*credentials*' '*secret*' 2>/dev/null || true
echo ""

# 5. Create commit
COMMIT_MSG="checkpoint(S${SESSION}): ${DESCRIPTION}"
echo -e "${BLUE}4. Creating commit: ${COMMIT_MSG}${NC}"
git commit -m "$COMMIT_MSG"
echo ""

# 6. Push
echo -e "${BLUE}5. Pushing to origin...${NC}"
git push origin HEAD
echo ""

echo -e "${GREEN}=== CHECKPOINT COMPLETE ===${NC}"
echo ""
echo "Commit: $COMMIT_MSG"
echo ""
