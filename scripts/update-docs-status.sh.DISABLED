#!/bin/bash
# =============================================================================
# update-docs-status.sh - Helper per aggiornare stato documenti
# =============================================================================
#
# Uso:
#   ./scripts/update-docs-status.sh                    # Mostra stato attuale
#   ./scripts/update-docs-status.sh --update "Cosa fatto"  # Aggiorna stato.md
#   ./scripts/update-docs-status.sh --step "2.18" "FATTO"  # Aggiorna step MAPPA
#
# "Docs sync = famiglia efficiente!"
#
# =============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Paths
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo ".")
STATO_FILE="$PROJECT_ROOT/.sncp/progetti/cervellaswarm/stato.md"
MAPPA_FILE="$PROJECT_ROOT/.sncp/progetti/cervellaswarm/roadmaps/MAPPA_COMPLETA_STEP_BY_STEP.md"
NORD_FILE="$PROJECT_ROOT/NORD.md"

# Functions
show_status() {
    echo ""
    echo -e "${BLUE}=================================================="
    echo "  DOCS STATUS - CervellaSwarm"
    echo "==================================================${NC}"
    echo ""

    # stato.md
    if [ -f "$STATO_FILE" ]; then
        STATO_LINES=$(wc -l < "$STATO_FILE" | tr -d ' ')
        if [[ "$OSTYPE" == "darwin"* ]]; then
            STATO_DATE=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M" "$STATO_FILE")
        else
            STATO_DATE=$(date -r "$STATO_FILE" "+%Y-%m-%d %H:%M")
        fi
        echo -e "stato.md:     ${GREEN}$STATO_LINES righe${NC} | Ultimo update: $STATO_DATE"
    else
        echo -e "stato.md:     ${RED}NON TROVATO${NC}"
    fi

    # NORD.md
    if [ -f "$NORD_FILE" ]; then
        NORD_LINES=$(wc -l < "$NORD_FILE" | tr -d ' ')
        if [[ "$OSTYPE" == "darwin"* ]]; then
            NORD_DATE=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M" "$NORD_FILE")
        else
            NORD_DATE=$(date -r "$NORD_FILE" "+%Y-%m-%d %H:%M")
        fi
        echo -e "NORD.md:      ${GREEN}$NORD_LINES righe${NC} | Ultimo update: $NORD_DATE"
    else
        echo -e "NORD.md:      ${RED}NON TROVATO${NC}"
    fi

    # MAPPA
    if [ -f "$MAPPA_FILE" ]; then
        MAPPA_LINES=$(wc -l < "$MAPPA_FILE" | tr -d ' ')
        if [[ "$OSTYPE" == "darwin"* ]]; then
            MAPPA_DATE=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M" "$MAPPA_FILE")
        else
            MAPPA_DATE=$(date -r "$MAPPA_FILE" "+%Y-%m-%d %H:%M")
        fi
        echo -e "MAPPA:        ${GREEN}$MAPPA_LINES righe${NC} | Ultimo update: $MAPPA_DATE"
    else
        echo -e "MAPPA:        ${RED}NON TROVATO${NC}"
    fi

    echo ""
    echo -e "${YELLOW}Comandi disponibili:${NC}"
    echo "  ./scripts/update-docs-status.sh --update \"Descrizione lavoro\""
    echo "  ./scripts/update-docs-status.sh --step \"2.18\" \"FATTO\""
    echo ""
}

update_stato() {
    local description="$1"
    local today=$(date +"%Y-%m-%d")
    local session=$(grep -oE "Sessione[: ]+[0-9]+" "$STATO_FILE" 2>/dev/null | tail -1 | grep -oE "[0-9]+" || echo "250")

    echo ""
    echo -e "${BLUE}Aggiornando stato.md...${NC}"

    # Backup
    cp "$STATO_FILE" "$STATO_FILE.bak"

    # Create new entry at top
    {
        echo "# STATO OGGI - $today"
        echo ""
        echo "> **Sessione:** $session"
        echo "> **Aggiornamento:** $(date +"%H:%M")"
        echo ""
        echo "---"
        echo ""
        echo "## LAVORO CORRENTE"
        echo ""
        echo "- $description"
        echo ""
        echo "---"
        echo ""
        # Keep last 40 lines of old content
        tail -40 "$STATO_FILE.bak"
    } > "$STATO_FILE"

    echo -e "${GREEN}stato.md aggiornato!${NC}"
    echo "Descrizione: $description"
    rm "$STATO_FILE.bak"
}

update_step() {
    local step="$1"
    local status="$2"

    echo ""
    echo -e "${BLUE}Aggiornando step $step in MAPPA...${NC}"

    if [ ! -f "$MAPPA_FILE" ]; then
        echo -e "${RED}MAPPA non trovata: $MAPPA_FILE${NC}"
        exit 1
    fi

    # Find and update the step
    if grep -q "STEP $step" "$MAPPA_FILE"; then
        # Update status
        if [[ "$OSTYPE" == "darwin"* ]]; then
            sed -i '' "s/\(STEP $step.*\)\[.*\]/\1[$status]/" "$MAPPA_FILE"
        else
            sed -i "s/\(STEP $step.*\)\[.*\]/\1[$status]/" "$MAPPA_FILE"
        fi
        echo -e "${GREEN}Step $step aggiornato a: $status${NC}"
    else
        echo -e "${YELLOW}Step $step non trovato in MAPPA${NC}"
    fi
}

# Main
case "${1:-}" in
    --update)
        if [ -z "${2:-}" ]; then
            echo -e "${RED}Errore: specifica descrizione${NC}"
            echo "Uso: $0 --update \"Descrizione lavoro\""
            exit 1
        fi
        update_stato "$2"
        ;;
    --step)
        if [ -z "${2:-}" ] || [ -z "${3:-}" ]; then
            echo -e "${RED}Errore: specifica step e status${NC}"
            echo "Uso: $0 --step \"2.18\" \"FATTO\""
            exit 1
        fi
        update_step "$2" "$3"
        ;;
    *)
        show_status
        ;;
esac
