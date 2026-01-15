#!/bin/bash
#
# memory-persist.sh - Salva stato critico per recovery
#
# Uso:
#   memory-persist.sh [progetto]
#   memory-persist.sh miracollo
#   memory-persist.sh --all
#
# Cosa salva:
#   - stato.md corrente
#   - PROMPT_RIPRESA corrente
#   - Ultimo commit git
#   - Timestamp
#
# Output:
#   .sncp/progetti/{progetto}/memoria/session_{timestamp}.json
#
# Versione: 1.0.0
# Data: 2026-01-15
# Sessione 217 - GAP #1 Implementation
#
# "Mai perdere il contesto!" - Cervella & Rafa
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

# Progetti disponibili
PROGETTI=("cervellaswarm" "miracollo" "contabilita")

# Funzione: Mostra help
show_help() {
    echo "memory-persist.sh - Salva stato critico per recovery"
    echo ""
    echo "Uso:"
    echo "  memory-persist.sh [progetto]    Salva stato di un progetto"
    echo "  memory-persist.sh --all         Salva tutti i progetti"
    echo "  memory-persist.sh --help        Mostra questo help"
    echo ""
    echo "Progetti disponibili:"
    for p in "${PROGETTI[@]}"; do
        echo "  - $p"
    done
    echo ""
    echo "Output: .sncp/progetti/{progetto}/memoria/session_{timestamp}.json"
}

# Funzione: Salva stato di un progetto
persist_project() {
    local PROJECT="$1"
    local PROJECT_DIR="$PROGETTI_DIR/$PROJECT"
    local MEMORIA_DIR="$PROJECT_DIR/memoria"
    local TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    local OUTPUT_FILE="$MEMORIA_DIR/session_${TIMESTAMP}.json"

    # Verifica progetto esiste
    if [ ! -d "$PROJECT_DIR" ]; then
        echo -e "${RED}Progetto '$PROJECT' non trovato!${NC}"
        return 1
    fi

    # Crea directory memoria se non esiste
    mkdir -p "$MEMORIA_DIR"

    # Leggi stato.md
    local STATO_CONTENT=""
    if [ -f "$PROJECT_DIR/stato.md" ]; then
        STATO_CONTENT=$(cat "$PROJECT_DIR/stato.md" | head -100 | sed 's/"/\\"/g' | tr '\n' '\\n')
    fi

    # Leggi PROMPT_RIPRESA
    local PROMPT_CONTENT=""
    local PROMPT_FILE="$PROJECT_DIR/PROMPT_RIPRESA_${PROJECT}.md"
    if [ -f "$PROMPT_FILE" ]; then
        PROMPT_CONTENT=$(cat "$PROMPT_FILE" | sed 's/"/\\"/g' | tr '\n' '\\n')
    fi

    # Ultimo commit git
    local GIT_COMMIT=""
    local GIT_MESSAGE=""
    if [ -d "$HOME/Developer/CervellaSwarm/.git" ]; then
        GIT_COMMIT=$(cd "$HOME/Developer/CervellaSwarm" && git rev-parse --short HEAD 2>/dev/null || echo "unknown")
        GIT_MESSAGE=$(cd "$HOME/Developer/CervellaSwarm" && git log -1 --format="%s" 2>/dev/null || echo "unknown")
    fi

    # Crea JSON
    cat > "$OUTPUT_FILE" << EOF
{
  "project": "$PROJECT",
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "timestamp_local": "$(date +"%Y-%m-%d %H:%M:%S")",
  "git": {
    "commit": "$GIT_COMMIT",
    "message": "$GIT_MESSAGE"
  },
  "files_saved": {
    "stato_md": "$PROJECT_DIR/stato.md",
    "prompt_ripresa": "$PROMPT_FILE"
  },
  "stato_summary": "$(echo "$STATO_CONTENT" | head -c 500)",
  "prompt_summary": "$(echo "$PROMPT_CONTENT" | head -c 500)",
  "recovery_instructions": "Per ripristinare: leggi questo file e stato.md del progetto"
}
EOF

    echo -e "${GREEN}OK${NC} - Salvato: $OUTPUT_FILE"

    # Pulisci vecchi file (mantieni ultimi 10)
    local COUNT=$(ls -1 "$MEMORIA_DIR"/session_*.json 2>/dev/null | wc -l)
    if [ "$COUNT" -gt 10 ]; then
        ls -1t "$MEMORIA_DIR"/session_*.json | tail -n +11 | xargs rm -f
        echo -e "${YELLOW}Pulizia:${NC} rimossi $(($COUNT - 10)) file vecchi"
    fi

    return 0
}

# Main
case "${1:-}" in
    --help|-h)
        show_help
        exit 0
        ;;
    --all)
        echo -e "${BLUE}Memory Persist - Tutti i progetti${NC}"
        echo ""
        for p in "${PROGETTI[@]}"; do
            echo -e "Progetto: ${YELLOW}$p${NC}"
            persist_project "$p" || true
        done
        echo ""
        echo -e "${GREEN}Fatto!${NC}"
        ;;
    "")
        # Default: progetto corrente basato su CWD
        CWD=$(pwd)
        if [[ "$CWD" == *"miracollo"* ]]; then
            persist_project "miracollo"
        elif [[ "$CWD" == *"Contabilita"* ]]; then
            persist_project "contabilita"
        else
            persist_project "cervellaswarm"
        fi
        ;;
    *)
        # Progetto specifico
        persist_project "$1"
        ;;
esac

exit 0
