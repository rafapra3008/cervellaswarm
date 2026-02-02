#!/bin/bash

# expand-daily.sh - Load full content of a specific daily log
# Author: Cervella Regina (Sessione 327)
# Date: 2 Febbraio 2026
# Version: 1.0.0
# Purpose: SNCP 5.0 P2.1 - On-demand expansion for progressive disclosure
#
# This script complements load-daily-memory.sh (--summary mode)
# When user sees "[Truncated]", they can use /expand-daily to get full content
#
# Usage:
#   ./expand-daily.sh [project] [date]     # Load full content for date
#   ./expand-daily.sh cervellaswarm today  # Shortcut for today
#   ./expand-daily.sh miracollo yesterday  # Shortcut for yesterday

set -uo pipefail

# === CONFIGURATION ===
SNCP_ROOT="${SNCP_ROOT:-/Users/rafapra/Developer/CervellaSwarm/.sncp/progetti}"

# === HELP ===
if [[ "${1:-}" == "--help" ]] || [[ "${1:-}" == "-h" ]] || [[ $# -lt 2 ]]; then
    cat << 'EOF'
expand-daily.sh - Load full content of a specific daily log (SNCP 5.0)

USAGE:
    ./expand-daily.sh [project] [date]
    ./expand-daily.sh [project] today
    ./expand-daily.sh [project] yesterday

EXAMPLES:
    ./expand-daily.sh cervellaswarm 2026-02-02
    ./expand-daily.sh miracollo today
    ./expand-daily.sh contabilita yesterday

PURPOSE:
    Progressive disclosure complement to load-daily-memory.sh
    Use when you see "[Truncated] Use /expand-daily for full content"

OUTPUT:
    Full markdown content of the daily log

EOF
    exit 0
fi

# === ARGUMENTS ===
PROJECT="${1:-}"
DATE_ARG="${2:-}"

# Resolve date shortcuts
resolve_date() {
    local arg="$1"
    case "$arg" in
        today)
            date +"%Y-%m-%d"
            ;;
        yesterday)
            date -v-1d +"%Y-%m-%d" 2>/dev/null || date -d "yesterday" +"%Y-%m-%d"
            ;;
        *)
            # Assume it's already a date
            echo "$arg"
            ;;
    esac
}

TARGET_DATE=$(resolve_date "$DATE_ARG")

# === VALIDATION ===
PROJECT_DIR="$SNCP_ROOT/$PROJECT"
LOG_PATH="$PROJECT_DIR/memoria/$TARGET_DATE.md"

if [[ ! -d "$PROJECT_DIR" ]]; then
    echo "Error: Project not found: $PROJECT"
    echo "Available projects:"
    ls -1 "$SNCP_ROOT" 2>/dev/null | grep -v "archivio\|shared"
    exit 1
fi

if [[ ! -f "$LOG_PATH" ]]; then
    echo "Error: Daily log not found: $LOG_PATH"
    echo ""
    echo "Available logs for $PROJECT:"
    ls -1 "$PROJECT_DIR/memoria/"*.md 2>/dev/null | head -10 || echo "  (none)"
    echo ""
    echo "Create a new log with: daily-log.sh $PROJECT --init"
    exit 1
fi

# === OUTPUT ===
echo "# Daily Log - $PROJECT - $TARGET_DATE (Full Content)"
echo ""
echo "---"
echo ""
cat "$LOG_PATH"
echo ""
echo "---"
echo "*Expanded by SNCP 5.0 - expand-daily.sh v1.0.0*"

exit 0
