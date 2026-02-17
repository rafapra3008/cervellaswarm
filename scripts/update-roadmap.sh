#!/bin/bash

# =============================================================================
# UPDATE-ROADMAP.SH - Aggiornamento automatico ROADMAP
# =============================================================================
#
# Uso:
#   ./scripts/update-roadmap.sh [progetto] [task] [stato]
#
# Esempi:
#   ./scripts/update-roadmap.sh                     # Interattivo
#   ./scripts/update-roadmap.sh miracollo 2.1 done  # Diretto
#
# =============================================================================

set -e

# Colori
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Emoji
BEE="🐝"
CHECK="✅"
PROGRESS="🔄"
TODO="⬜"
CROWN="👑"

echo ""
echo -e "${PURPLE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${PURPLE}   ${BEE} CERVELLASWARM - Aggiornamento ROADMAP ${CROWN}${NC}"
echo -e "${PURPLE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# Progetti conosciuti
DEVELOPER_ROOT="${DEVELOPER_ROOT:-$HOME/Developer}"
declare -A PROGETTI
PROGETTI["miracollo"]="$DEVELOPER_ROOT/miracollogeminifocus"
PROGETTI["contabilita"]="$DEVELOPER_ROOT/ContabilitaAntigravity"
PROGETTI["cervellaswarm"]="$DEVELOPER_ROOT/CervellaSwarm"
PROGETTI["libertaio"]="$DEVELOPER_ROOT/million-dollar-ideas"

# Funzione per mostrare progetti disponibili
show_projects() {
    echo -e "${CYAN}Progetti disponibili:${NC}"
    echo ""
    for key in "${!PROGETTI[@]}"; do
        if [ -d "${PROGETTI[$key]}" ]; then
            echo -e "  ${GREEN}$key${NC} → ${PROGETTI[$key]}"
        else
            echo -e "  ${RED}$key${NC} → ${PROGETTI[$key]} (non trovato)"
        fi
    done
    echo ""
}

# Funzione per trovare ROADMAP
find_roadmap() {
    local project_path=$1

    # Cerca in ordine di priorita
    local paths=(
        "$project_path/ROADMAP_SACRA.md"
        "$project_path/ROADMAP.md"
        "$project_path/docs/ROADMAP.md"
    )

    for path in "${paths[@]}"; do
        if [ -f "$path" ]; then
            echo "$path"
            return 0
        fi
    done

    echo ""
    return 1
}

# Funzione per aggiornare task
update_task() {
    local roadmap_file=$1
    local task_id=$2
    local new_status=$3
    local date_today=$(date +"%d %b %Y")

    # Backup
    cp "$roadmap_file" "${roadmap_file}.bak"

    # Converti status in simbolo
    local status_symbol=""
    case $new_status in
        "done"|"completed"|"fatto")
            status_symbol="DONE"
            ;;
        "progress"|"inprogress"|"incorso")
            status_symbol="IN PROGRESS"
            ;;
        "todo"|"pending"|"dafate")
            status_symbol="TODO"
            ;;
        *)
            echo -e "${RED}Stato non riconosciuto: $new_status${NC}"
            echo "Usa: done, progress, todo"
            return 1
            ;;
    esac

    # Cerca e aggiorna la riga con il task
    if grep -q "| $task_id |" "$roadmap_file"; then
        # Aggiorna lo stato
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            sed -i '' "s/| $task_id |.*|.*|.*|/| $task_id | ... | $status_symbol | $date_today |/g" "$roadmap_file"
        else
            # Linux
            sed -i "s/| $task_id |.*|.*|.*|/| $task_id | ... | $status_symbol | $date_today |/g" "$roadmap_file"
        fi

        echo -e "${GREEN}${CHECK} Task $task_id aggiornato a: $status_symbol${NC}"
        return 0
    else
        echo -e "${YELLOW}Task $task_id non trovato nella roadmap${NC}"
        return 1
    fi
}

# Funzione per mostrare stato attuale
show_status() {
    local roadmap_file=$1

    echo -e "${CYAN}═══ STATO ATTUALE ═══${NC}"
    echo ""

    # Conta task per stato
    local done=$(grep -c "DONE" "$roadmap_file" 2>/dev/null || echo "0")
    local progress=$(grep -c "IN PROGRESS" "$roadmap_file" 2>/dev/null || echo "0")
    local todo=$(grep -c "TODO" "$roadmap_file" 2>/dev/null || echo "0")
    local total=$((done + progress + todo))

    if [ $total -gt 0 ]; then
        local percent=$((done * 100 / total))
        echo -e "  ${GREEN}${CHECK} Completati:${NC} $done"
        echo -e "  ${YELLOW}${PROGRESS} In corso:${NC} $progress"
        echo -e "  ${BLUE}${TODO} Da fare:${NC} $todo"
        echo ""
        echo -e "  ${PURPLE}Progresso: $percent%${NC}"
    else
        echo "  Nessun task trovato nel formato atteso"
    fi

    echo ""
}

# Funzione per aggiungere entry al changelog
add_changelog() {
    local roadmap_file=$1
    local entry=$2
    local date_today=$(date +"%d %B %Y")

    # Cerca sezione CHANGELOG e aggiungi entry
    if grep -q "## CHANGELOG" "$roadmap_file"; then
        # Trova la prima riga dopo "## CHANGELOG" o "### [data]"
        # e inserisci la nuova entry
        echo -e "${GREEN}Entry aggiunta al changelog${NC}"
    fi
}

# ===== MAIN =====

# Modalita diretta con argomenti
if [ $# -eq 3 ]; then
    PROJECT=$1
    TASK=$2
    STATUS=$3

    if [ -z "${PROGETTI[$PROJECT]}" ]; then
        echo -e "${RED}Progetto non trovato: $PROJECT${NC}"
        show_projects
        exit 1
    fi

    ROADMAP=$(find_roadmap "${PROGETTI[$PROJECT]}")

    if [ -z "$ROADMAP" ]; then
        echo -e "${RED}ROADMAP non trovata per $PROJECT${NC}"
        exit 1
    fi

    update_task "$ROADMAP" "$TASK" "$STATUS"
    exit 0
fi

# Modalita interattiva
echo -e "${YELLOW}Modalita interattiva${NC}"
echo ""

show_projects

echo -n "Quale progetto? "
read PROJECT

if [ -z "${PROGETTI[$PROJECT]}" ]; then
    echo -e "${RED}Progetto non trovato${NC}"
    exit 1
fi

ROADMAP=$(find_roadmap "${PROGETTI[$PROJECT]}")

if [ -z "$ROADMAP" ]; then
    echo -e "${RED}ROADMAP non trovata${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}Trovata: $ROADMAP${NC}"
echo ""

show_status "$ROADMAP"

echo "Opzioni:"
echo "  1) Segna task come completato"
echo "  2) Segna task in progress"
echo "  3) Mostra roadmap"
echo "  4) Esci"
echo ""
echo -n "Cosa vuoi fare? "
read CHOICE

case $CHOICE in
    1)
        echo -n "ID del task (es. 2.1): "
        read TASK_ID
        update_task "$ROADMAP" "$TASK_ID" "done"
        ;;
    2)
        echo -n "ID del task (es. 2.1): "
        read TASK_ID
        update_task "$ROADMAP" "$TASK_ID" "progress"
        ;;
    3)
        cat "$ROADMAP"
        ;;
    4)
        echo "Ciao! ${BEE}"
        exit 0
        ;;
    *)
        echo "Scelta non valida"
        ;;
esac

echo ""
echo -e "${PURPLE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}${CHECK} Fatto!${NC}"
echo -e "${PURPLE}═══════════════════════════════════════════════════════════════${NC}"
