#!/bin/bash
#
# swarm-session-check.sh - Verifica roadmap inizio sessione
# Versione: 1.0.0
# Data: 6 Gennaio 2026
#
# Uso: swarm-session-check [progetto]
#

set -e

# Colori
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

VERSION="1.0.0"

# Progetti conosciuti
PROJECTS_BASE="$HOME/Developer"
PROJECTS=("miracollogeminifocus" "CervellaSwarm" "ContabilitaAntigravity")

print_header() {
    echo ""
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC}  ${BOLD}CERVELLASWARM - SESSION CHECK${NC}                                    ${BLUE}║${NC}"
    echo -e "${BLUE}║${NC}  ${CYAN}Buongiorno! Verifichiamo dove siamo...${NC}                           ${BLUE}║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

check_day() {
    local day=$(date +%u)  # 1=Monday, 7=Sunday
    local day_name=$(date +%A)

    if [ "$day" = "1" ]; then
        echo -e "${YELLOW}━━━ OGGI E' LUNEDI'! ━━━${NC}"
        echo -e "  ${RED}ATTENZIONE:${NC} Giorno di CODE REVIEW settimanale!"
        echo -e "  Comando: ${GREEN}spawn-workers --reviewer${NC}"
        echo ""
    elif [ "$day" = "5" ]; then
        echo -e "${YELLOW}━━━ OGGI E' VENERDI'! ━━━${NC}"
        echo -e "  ${CYAN}TIP:${NC} Buon giorno per fare CODE REVIEW!"
        echo ""
    fi
}

check_project_roadmap() {
    local project_path="$1"
    local project_name=$(basename "$project_path")

    echo -e "${CYAN}━━━ $project_name ━━━${NC}"

    # Check ROADMAP.md
    if [ -f "$project_path/ROADMAP.md" ]; then
        echo -e "  ${GREEN}✓${NC} ROADMAP.md trovata"
        # Mostra prime righe utili
        local summary=$(grep -A3 "## Stato Attuale\|## Dove Siamo\|## Status" "$project_path/ROADMAP.md" 2>/dev/null | head -5)
        if [ -n "$summary" ]; then
            echo "$summary" | sed 's/^/    /'
        fi
    elif [ -f "$project_path/ROADMAP_SACRA.md" ]; then
        echo -e "  ${YELLOW}~${NC} Solo ROADMAP_SACRA.md (nessun riassunto)"
    else
        echo -e "  ${RED}✗${NC} Nessuna roadmap trovata"
    fi

    # Check NORD.md
    if [ -f "$project_path/NORD.md" ]; then
        echo -e "  ${GREEN}✓${NC} NORD.md presente"
    fi

    # Check PROMPT_RIPRESA.md
    if [ -f "$project_path/PROMPT_RIPRESA.md" ]; then
        local last_update=$(grep -i "ultimo aggiornamento\|last update" "$project_path/PROMPT_RIPRESA.md" | head -1)
        echo -e "  ${GREEN}✓${NC} PROMPT_RIPRESA.md - $last_update"
    fi

    # Task pendenti
    if [ -d "$project_path/.swarm/tasks" ]; then
        local ready_count=$(find "$project_path/.swarm/tasks" -name "*.ready" 2>/dev/null | wc -l | tr -d ' ')
        if [ "$ready_count" -gt 0 ]; then
            echo -e "  ${YELLOW}!${NC} $ready_count task in attesa"
        fi
    fi

    echo ""
}

check_single_project() {
    local project="$1"
    local project_path=""

    # Trova il progetto
    if [ -d "$PROJECTS_BASE/$project" ]; then
        project_path="$PROJECTS_BASE/$project"
    elif [ -d "./$project" ]; then
        project_path="./$project"
    elif [ -d "$project" ]; then
        project_path="$project"
    else
        echo -e "${RED}[ERRORE]${NC} Progetto non trovato: $project"
        exit 1
    fi

    print_header
    check_day
    check_project_roadmap "$project_path"
}

check_all_projects() {
    print_header
    check_day

    echo -e "${YELLOW}━━━ STATO PROGETTI ━━━${NC}"
    echo ""

    for project in "${PROJECTS[@]}"; do
        local project_path="$PROJECTS_BASE/$project"
        if [ -d "$project_path" ]; then
            check_project_roadmap "$project_path"
        fi
    done
}

check_current() {
    print_header
    check_day

    # Verifica progetto corrente
    if [ -f "ROADMAP.md" ] || [ -f "ROADMAP_SACRA.md" ] || [ -f "NORD.md" ]; then
        check_project_roadmap "$(pwd)"
    else
        echo -e "${YELLOW}[i]${NC} Non sembra un progetto CervellaSwarm"
        echo -e "    Usa: ${GREEN}swarm-session-check --all${NC} per vedere tutti i progetti"
        echo ""
    fi
}

show_tips() {
    echo -e "${CYAN}━━━ TIPS SESSIONE ━━━${NC}"
    echo ""
    echo -e "  1. Leggi ${GREEN}PROMPT_RIPRESA.md${NC} per capire dove eravamo"
    echo -e "  2. Controlla ${GREEN}NORD.md${NC} per la direzione"
    echo -e "  3. Usa ${GREEN}swarm-report${NC} per vedere task recenti"
    echo -e "  4. Usa ${GREEN}swarm-help${NC} per la guida comandi"
    echo ""
}

# Main
case "${1:-}" in
    --all|-a)
        check_all_projects
        show_tips
        ;;
    --tips|-t)
        show_tips
        ;;
    -h|--help)
        echo "Uso: swarm-session-check [opzione|progetto]"
        echo ""
        echo "Opzioni:"
        echo "  (nessuna)      Verifica progetto corrente"
        echo "  --all, -a      Verifica tutti i progetti"
        echo "  --tips, -t     Mostra tips sessione"
        echo "  <progetto>     Verifica progetto specifico"
        echo ""
        ;;
    "")
        check_current
        show_tips
        ;;
    *)
        check_single_project "$1"
        show_tips
        ;;
esac
