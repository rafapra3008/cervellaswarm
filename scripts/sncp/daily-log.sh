#!/bin/bash

# daily-log.sh - Append notes to daily memory log
# Author: Cervella Ingegnera
# Date: 29 Gennaio 2026
# Version: 1.0.0
# Purpose: Temporal organization of session notes (inspired by Moltbot)
#
# Usage:
#   ./daily-log.sh [project] "note to add"
#   ./daily-log.sh [project] --view     # View today's log
#   ./daily-log.sh [project] --init     # Create today's log from template

set -uo pipefail

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Arguments
PROJECT="${1:-}"
ACTION="${2:-}"

# Paths
SNCP_ROOT=".sncp/progetti"
DATE=$(date +"%Y-%m-%d")
MONTH=$(date +"%Y-%m")

# Help
if [[ "${1:-}" == "--help" ]] || [[ "${1:-}" == "-h" ]]; then
    echo "Usage: daily-log.sh [project] [note|--view|--init]"
    echo ""
    echo "Manages daily memory logs for temporal organization."
    echo ""
    echo "Arguments:"
    echo "  project   Project name (cervellaswarm, miracollo, etc)"
    echo "  note      Text to append to today's log"
    echo "  --view    View today's log"
    echo "  --init    Create today's log from template"
    echo ""
    echo "Structure:"
    echo "  .sncp/progetti/[project]/memoria/"
    echo "    ├── 2026-01-29.md    # Today's log"
    echo "    ├── 2026-01-28.md    # Yesterday"
    echo "    └── archivio/        # Old months"
    echo "        └── 2026-01/     # Archived logs"
    echo ""
    echo "Examples:"
    echo "  ./daily-log.sh miracollo --init"
    echo "  ./daily-log.sh miracollo 'Completato Sprint S320'"
    echo "  ./daily-log.sh cervellaswarm --view"
    exit 0
fi

# Validate project
if [[ -z "$PROJECT" ]]; then
    echo "Error: Project name required"
    echo "Usage: daily-log.sh [project] [note|--view|--init]"
    exit 1
fi

PROJECT_DIR="$SNCP_ROOT/$PROJECT"
MEMORIA_DIR="$PROJECT_DIR/memoria"
TODAY_LOG="$MEMORIA_DIR/$DATE.md"

if [[ ! -d "$PROJECT_DIR" ]]; then
    echo -e "${YELLOW}Project not found: $PROJECT${NC}"
    exit 1
fi

# Ensure memoria directory exists
mkdir -p "$MEMORIA_DIR"
mkdir -p "$MEMORIA_DIR/archivio"

# Create today's log if doesn't exist
create_daily_log() {
    if [[ ! -f "$TODAY_LOG" ]]; then
        cat > "$TODAY_LOG" << EOF
# Daily Log - $DATE

**Progetto:** $PROJECT
**Data:** $DATE

---

## Sessioni

<!-- Aggiungi note delle sessioni qui -->

---

## Decisioni

<!-- Decisioni importanti prese oggi -->

---

## Prossimi Step

<!-- Cosa fare domani -->

---

*Creato automaticamente da daily-log.sh*
EOF
        echo -e "${GREEN}Created: $TODAY_LOG${NC}"
    fi
}

# Main logic
case "${ACTION:-}" in
    --view)
        if [[ -f "$TODAY_LOG" ]]; then
            cat "$TODAY_LOG"
        else
            echo "No log for today. Use --init to create one."
        fi
        ;;

    --init)
        create_daily_log
        ;;

    "")
        # No action specified - show status
        create_daily_log
        lines=$(wc -l < "$TODAY_LOG" | tr -d ' ')
        echo -e "${BLUE}Daily Log Status - $PROJECT${NC}"
        echo "----------------------------"
        echo "File: $TODAY_LOG"
        echo "Lines: $lines"
        echo ""
        echo "Recent logs:"
        ls -la "$MEMORIA_DIR"/*.md 2>/dev/null | tail -5 || echo "No logs yet"
        ;;

    *)
        # Append note
        create_daily_log

        TIMESTAMP=$(date +"%H:%M")
        echo "" >> "$TODAY_LOG"
        echo "### [$TIMESTAMP] Note" >> "$TODAY_LOG"
        echo "" >> "$TODAY_LOG"
        echo "$ACTION" >> "$TODAY_LOG"
        echo "" >> "$TODAY_LOG"

        echo -e "${GREEN}Added to $TODAY_LOG${NC}"
        ;;
esac

exit 0
