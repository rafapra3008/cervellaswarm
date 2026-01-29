#!/bin/bash

# check-ripresa-size.sh - Monitor PROMPT_RIPRESA file sizes
# Author: Cervella Ingegnera
# Date: 29 Gennaio 2026
# Version: 1.0.0
# Purpose: Warn before PROMPT_RIPRESA files exceed the 150-line limit

set -uo pipefail

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Limits
LIMIT=150        # Maximum allowed lines
WARNING=120      # Warning threshold (80%)

# Help
if [[ "${1:-}" == "--help" ]] || [[ "${1:-}" == "-h" ]]; then
    echo "Usage: check-ripresa-size.sh [project]"
    echo ""
    echo "Checks PROMPT_RIPRESA file sizes against the 150-line limit."
    echo ""
    echo "Arguments:"
    echo "  project   Check specific project (optional)"
    echo ""
    echo "Thresholds:"
    echo "  OK        < 120 lines (under 80%)"
    echo "  WARNING   120-150 lines (80-100%)"
    echo "  ERROR     > 150 lines (over limit!)"
    echo ""
    echo "Examples:"
    echo "  ./check-ripresa-size.sh              # Check all projects"
    echo "  ./check-ripresa-size.sh miracollo    # Check specific project"
    exit 0
fi

SNCP_ROOT=".sncp/progetti"
SPECIFIC_PROJECT="${1:-}"

echo "=================================================="
echo -e "${BLUE}PROMPT_RIPRESA Size Monitor${NC}"
echo "=================================================="
echo ""
echo -e "Limit: ${LIMIT} lines | Warning: ${WARNING} lines"
echo ""

has_warning=false
has_error=false

check_file() {
    local file="$1"
    local project_name=$(basename "$(dirname "$file")")

    if [[ ! -f "$file" ]]; then
        return
    fi

    local lines=$(wc -l < "$file" | tr -d ' ')
    local percent=$((lines * 100 / LIMIT))

    # Determine status
    local status=""
    local color=""

    if [[ $lines -gt $LIMIT ]]; then
        status="ERROR"
        color="$RED"
        has_error=true
    elif [[ $lines -ge $WARNING ]]; then
        status="WARNING"
        color="$YELLOW"
        has_warning=true
    else
        status="OK"
        color="$GREEN"
    fi

    # Format output
    printf "%-20s %4d/%-4d (%3d%%) " "$project_name" "$lines" "$LIMIT" "$percent"
    echo -e "${color}${status}${NC}"
}

# Find and check all PROMPT_RIPRESA files
if [[ -n "$SPECIFIC_PROJECT" ]]; then
    # Check specific project
    file="$SNCP_ROOT/$SPECIFIC_PROJECT/PROMPT_RIPRESA_$SPECIFIC_PROJECT.md"
    if [[ -f "$file" ]]; then
        check_file "$file"
    else
        echo -e "${RED}Project not found: $SPECIFIC_PROJECT${NC}"
        exit 1
    fi
else
    # Check all projects
    while IFS= read -r file; do
        check_file "$file"
    done < <(find "$SNCP_ROOT" -name "PROMPT_RIPRESA_*.md" -type f 2>/dev/null | sort)

    # Also check bracci (sub-projects)
    echo ""
    echo "--- Bracci (sub-projects) ---"
    while IFS= read -r file; do
        check_file "$file"
    done < <(find "$SNCP_ROOT" -path "*/bracci/*/PROMPT_RIPRESA_*.md" -type f 2>/dev/null | sort)
fi

echo ""
echo "=================================================="

# Summary and recommendations
if [[ "$has_error" == true ]]; then
    echo -e "${RED}ACTION REQUIRED: Files over limit!${NC}"
    echo ""
    echo "To fix:"
    echo "1. Archive old sessions to archivio/"
    echo "2. Remove completed sprints (> 30 days old)"
    echo "3. Keep only recent decisions and current status"
    echo ""
    echo "Archive command:"
    echo "  mv old_content .sncp/progetti/PROJECT/archivio/YYYY-MM/"
    exit 1
elif [[ "$has_warning" == true ]]; then
    echo -e "${YELLOW}Attention: Some files approaching limit${NC}"
    echo ""
    echo "Consider archiving old sessions soon."
    exit 0
else
    echo -e "${GREEN}All files within limits!${NC}"
    exit 0
fi
