#!/bin/bash

# memory-flush.sh - Auto-save important memories before context limit
# Author: Cervella Ingegnera
# Date: 29 Gennaio 2026
# Version: 1.0.0
# Purpose: Prevent memory loss in long sessions (inspired by Moltbot)
#
# Usage:
#   Called automatically by spawn-workers before session end
#   Can also be called manually: ./memory-flush.sh [project] [worker]

set -uo pipefail

# Colors (used only for manual invocation)
BLUE='\033[0;34m'
GREEN='\033[0;32m'
NC='\033[0m'

# Arguments
PROJECT="${1:-}"
WORKER="${2:-}"
SILENT="${3:-false}"

# Paths
SNCP_ROOT=".sncp/progetti"
SWARM_LOGS=".swarm/logs"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
DATE=$(date +"%Y-%m-%d")

# Help
if [[ "${1:-}" == "--help" ]] || [[ "${1:-}" == "-h" ]]; then
    echo "Usage: memory-flush.sh [project] [worker] [silent]"
    echo ""
    echo "Saves current session state before context limit."
    echo ""
    echo "Arguments:"
    echo "  project   Project name (cervellaswarm, miracollo, etc)"
    echo "  worker    Worker name (optional, for logging)"
    echo "  silent    'true' for no output (default: false)"
    echo ""
    echo "What it does:"
    echo "  1. Checks PROMPT_RIPRESA size"
    echo "  2. If approaching limit, suggests archiving"
    echo "  3. Logs flush event"
    echo ""
    echo "Examples:"
    echo "  ./memory-flush.sh miracollo backend"
    echo "  ./memory-flush.sh cervellaswarm frontend true"
    exit 0
fi

# Validate project
if [[ -z "$PROJECT" ]]; then
    if [[ "$SILENT" != "true" ]]; then
        echo "Error: Project name required"
    fi
    exit 1
fi

PROJECT_DIR="$SNCP_ROOT/$PROJECT"
PROMPT_RIPRESA="$PROJECT_DIR/PROMPT_RIPRESA_$PROJECT.md"

if [[ ! -d "$PROJECT_DIR" ]]; then
    if [[ "$SILENT" != "true" ]]; then
        echo "Error: Project not found: $PROJECT"
    fi
    exit 1
fi

# Ensure log directory exists
mkdir -p "$SWARM_LOGS"

log_message() {
    local msg="$1"
    echo "[$TIMESTAMP] [$PROJECT] [$WORKER] $msg" >> "$SWARM_LOGS/memory_flush.log"
}

output() {
    if [[ "$SILENT" != "true" ]]; then
        echo -e "$1"
    fi
}

# Main flush logic
output "${BLUE}Memory Flush - $PROJECT${NC}"
output "----------------------------"

# 1. Check PROMPT_RIPRESA size
if [[ -f "$PROMPT_RIPRESA" ]]; then
    lines=$(wc -l < "$PROMPT_RIPRESA" | tr -d ' ')
    output "PROMPT_RIPRESA: $lines/250 lines"

    if [[ $lines -gt 200 ]]; then
        log_message "WARNING: PROMPT_RIPRESA at $lines lines (>200)"
        output "⚠️  Approaching limit! Consider archiving old sessions."
    fi
else
    output "No PROMPT_RIPRESA found - creating placeholder"
    log_message "Created new PROMPT_RIPRESA"
fi

# 2. Log flush event
log_message "Memory flush triggered"

# 3. Check for handoff files from today (to avoid duplicates)
handoff_today="$SNCP_ROOT/../handoff/HANDOFF_${DATE}_*.md"
handoff_count=$(ls $handoff_today 2>/dev/null | wc -l | tr -d ' ')

if [[ $handoff_count -gt 0 ]]; then
    output "Handoffs today: $handoff_count"
    log_message "Found $handoff_count handoff files from today"
fi

# 4. Summary
output ""
output "${GREEN}Flush complete!${NC}"
output ""
output "Reminder for Workers:"
output "- Write key decisions to PROMPT_RIPRESA before ending"
output "- Create handoff if session was productive"

log_message "Flush completed successfully"

exit 0
