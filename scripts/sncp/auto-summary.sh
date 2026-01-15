#!/bin/bash
#
# auto-summary.sh - Salva summary automatici dei task completati
#
# Uso:
#   auto-summary.sh "Nome Task" "Summary breve" [progetto]
#   auto-summary.sh "Fix login bug" "Corretto validazione email" miracollo
#   auto-summary.sh "API endpoint" "Creato /users endpoint"
#
# Output:
#   Appende a .sncp/progetti/{progetto}/workflow/TASK_LOG.md
#
# Versione: 1.0.0
# Data: 2026-01-15
# Sessione 217 - GAP #2 Implementation
#
# "Checkpoint automatici per non perdere progressi!" - Cervella & Rafa
#

set -e

# Colori
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Path base
SNCP_BASE="$HOME/Developer/CervellaSwarm/.sncp"
PROGETTI_DIR="$SNCP_BASE/progetti"

# Funzione: Mostra help
show_help() {
    echo "auto-summary.sh - Salva summary automatici dei task"
    echo ""
    echo "Uso:"
    echo "  auto-summary.sh \"Nome Task\" \"Summary\" [progetto]"
    echo "  auto-summary.sh --list [progetto]    Mostra ultimi task"
    echo "  auto-summary.sh --help               Mostra questo help"
    echo ""
    echo "Esempi:"
    echo "  auto-summary.sh \"Fix login\" \"Corretto validazione\""
    echo "  auto-summary.sh \"API users\" \"Endpoint CRUD\" miracollo"
    echo ""
    echo "Output: .sncp/progetti/{progetto}/workflow/TASK_LOG.md"
}

# Funzione: Determina progetto
get_project() {
    local PROJECT="${1:-}"

    if [ -n "$PROJECT" ]; then
        echo "$PROJECT"
        return
    fi

    # Auto-detect da CWD
    local CWD=$(pwd)
    if [[ "$CWD" == *"miracollo"* ]]; then
        echo "miracollo"
    elif [[ "$CWD" == *"Contabilita"* ]]; then
        echo "contabilita"
    else
        echo "cervellaswarm"
    fi
}

# Funzione: Salva summary
save_summary() {
    local TASK_NAME="$1"
    local SUMMARY="$2"
    local PROJECT="$3"

    local PROJECT_DIR="$PROGETTI_DIR/$PROJECT"
    local WORKFLOW_DIR="$PROJECT_DIR/workflow"
    local LOG_FILE="$WORKFLOW_DIR/TASK_LOG.md"

    # Verifica progetto esiste
    if [ ! -d "$PROJECT_DIR" ]; then
        echo -e "${RED}Progetto '$PROJECT' non trovato!${NC}"
        return 1
    fi

    # Crea directory workflow se non esiste
    mkdir -p "$WORKFLOW_DIR"

    # Timestamp
    local TIMESTAMP=$(date +"%Y-%m-%d %H:%M")
    local DATE=$(date +"%Y-%m-%d")

    # Crea file se non esiste
    if [ ! -f "$LOG_FILE" ]; then
        cat > "$LOG_FILE" << EOF
# Task Log - $PROJECT

> Log automatico dei task completati.
> Generato da auto-summary.sh

---

EOF
    fi

    # Controlla se c'è già una sezione per oggi
    if ! grep -q "## $DATE" "$LOG_FILE" 2>/dev/null; then
        echo "" >> "$LOG_FILE"
        echo "## $DATE" >> "$LOG_FILE"
        echo "" >> "$LOG_FILE"
    fi

    # Appendi task
    echo "- **$TIMESTAMP** - $TASK_NAME" >> "$LOG_FILE"
    echo "  - $SUMMARY" >> "$LOG_FILE"

    echo -e "${GREEN}OK${NC} - Task salvato in: $LOG_FILE"

    # Mantieni file sotto 200 righe (archivia vecchio)
    local LINES=$(wc -l < "$LOG_FILE")
    if [ "$LINES" -gt 200 ]; then
        local ARCHIVE_FILE="$WORKFLOW_DIR/TASK_LOG_$(date +%Y%m).md"
        head -n 150 "$LOG_FILE" > "$ARCHIVE_FILE"
        tail -n 50 "$LOG_FILE" > "${LOG_FILE}.tmp"
        mv "${LOG_FILE}.tmp" "$LOG_FILE"
        echo -e "${YELLOW}Archiviato:${NC} $ARCHIVE_FILE"
    fi

    return 0
}

# Funzione: Mostra ultimi task
list_tasks() {
    local PROJECT=$(get_project "$1")
    local LOG_FILE="$PROGETTI_DIR/$PROJECT/workflow/TASK_LOG.md"

    if [ ! -f "$LOG_FILE" ]; then
        echo -e "${YELLOW}Nessun task log per $PROJECT${NC}"
        return 0
    fi

    echo -e "${BLUE}Ultimi task - $PROJECT${NC}"
    echo ""
    tail -20 "$LOG_FILE"
}

# Main
case "${1:-}" in
    --help|-h)
        show_help
        exit 0
        ;;
    --list)
        list_tasks "${2:-}"
        exit 0
        ;;
    "")
        show_help
        exit 1
        ;;
    *)
        # Salva summary
        TASK_NAME="${1:-}"
        SUMMARY="${2:-Completato}"
        PROJECT=$(get_project "${3:-}")

        if [ -z "$TASK_NAME" ]; then
            echo -e "${RED}Errore: Nome task richiesto${NC}"
            show_help
            exit 1
        fi

        save_summary "$TASK_NAME" "$SUMMARY" "$PROJECT"
        ;;
esac

exit 0
