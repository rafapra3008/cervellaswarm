#!/bin/bash
# ==============================================================================
# START-SESSION - Avvia sessione su qualsiasi progetto
# ==============================================================================
#
# Uso: start-session <progetto>
#      start-session --list
#
# Progetti supportati:
#   cervellaswarm, miracollo, contabilita, cervellacostruzione, cervellabrasil, chavefy
#
# ==============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# SNCP root
SNCP_ROOT="/Users/rafapra/Developer/CervellaSwarm/.sncp/progetti"

# ==============================================================================
# PROGETTI - Funzioni per ottenere path e descrizioni
# ==============================================================================

get_project_path() {
    case "$1" in
        cervellaswarm)     echo "/Users/rafapra/Developer/CervellaSwarm" ;;
        miracollo)         echo "/Users/rafapra/Developer/miracollogeminifocus" ;;
        contabilita)       echo "/Users/rafapra/Developer/ContabilitaAntigravity" ;;
        cervellacostruzione) echo "/Users/rafapra/Developer/cervellacostruzione" ;;
        cervellabrasil)    echo "/Users/rafapra/Developer/CervellaBrasil" ;;
        chavefy)           echo "/Users/rafapra/Developer/Chavefy" ;;
        *)                 echo "" ;;
    esac
}

get_project_desc() {
    case "$1" in
        cervellaswarm)     echo "AI Team - 17 Cervelle" ;;
        miracollo)         echo "Sistema alberghiero + Miracollook + Room" ;;
        contabilita)       echo "Sistema contabilita" ;;
        cervellacostruzione) echo "Business costruzione case Brasile" ;;
        cervellabrasil)    echo "Projeto financeiro estrategico IT->BR" ;;
        chavefy)           echo "SaaS Property Management Brasil" ;;
        *)                 echo "" ;;
    esac
}

# Lista progetti
PROJECTS="cervellaswarm miracollo contabilita cervellacostruzione cervellabrasil chavefy"

# ==============================================================================
# FUNCTIONS
# ==============================================================================

show_help() {
    echo ""
    echo -e "${BLUE}+================================================================+${NC}"
    echo -e "${BLUE}|                    START-SESSION                               |${NC}"
    echo -e "${BLUE}+================================================================+${NC}"
    echo ""
    echo -e "Uso: ${GREEN}start-session <progetto>${NC}"
    echo -e "     ${GREEN}start-session --list${NC}"
    echo ""
    echo "Progetti disponibili:"
    for project in $PROJECTS; do
        desc=$(get_project_desc "$project")
        echo -e "  ${CYAN}$project${NC} - $desc"
    done
    echo ""
}

list_projects() {
    echo ""
    echo -e "${BLUE}+================================================================+${NC}"
    echo -e "${BLUE}|                 PROGETTI DISPONIBILI                           |${NC}"
    echo -e "${BLUE}+================================================================+${NC}"
    echo ""

    for project in $PROJECTS; do
        path=$(get_project_path "$project")
        desc=$(get_project_desc "$project")
        ripresa="$SNCP_ROOT/$project/PROMPT_RIPRESA_$project.md"

        # Check if project exists
        if [ -d "$path" ]; then
            status="${GREEN}✓${NC}"
        else
            status="${RED}✗${NC}"
        fi

        # Check PROMPT_RIPRESA
        if [ -f "$ripresa" ]; then
            ripresa_status="${GREEN}✓${NC}"
            last_mod=$(stat -f "%Sm" -t "%Y-%m-%d" "$ripresa" 2>/dev/null || echo "?")
        else
            ripresa_status="${RED}✗${NC}"
            last_mod="-"
        fi

        echo -e "  $status ${CYAN}$project${NC}"
        echo -e "    Path: $path"
        echo -e "    RIPRESA: $ripresa_status (ultimo update: $last_mod)"
        echo -e "    Desc: $desc"
        echo ""
    done
}

start_session() {
    local project="$1"
    local path=$(get_project_path "$project")

    # Validate project
    if [ -z "$path" ]; then
        echo -e "${RED}Errore: Progetto '$project' non trovato!${NC}"
        echo ""
        echo "Progetti disponibili:"
        for p in $PROJECTS; do
            echo "  - $p"
        done
        exit 1
    fi

    local ripresa="$SNCP_ROOT/$project/PROMPT_RIPRESA_$project.md"

    # Check directory exists
    if [ ! -d "$path" ]; then
        echo -e "${RED}Errore: Directory non esiste: $path${NC}"
        exit 1
    fi

    # Header
    echo ""
    echo -e "${BLUE}+================================================================+${NC}"
    echo -e "${BLUE}|              INIZIA SESSIONE: ${CYAN}$project${NC}"
    echo -e "${BLUE}+================================================================+${NC}"
    echo ""

    # Show PROMPT_RIPRESA preview
    if [ -f "$ripresa" ]; then
        echo -e "${GREEN}PROMPT_RIPRESA trovato!${NC}"
        echo -e "${YELLOW}Preview (prime 30 righe):${NC}"
        echo ""
        echo "---"
        head -30 "$ripresa"
        echo "..."
        echo "---"
        echo ""

        # Count lines
        lines=$(wc -l < "$ripresa" | tr -d ' ')
        echo -e "Totale: ${CYAN}$lines righe${NC}"
        echo ""
    else
        echo -e "${YELLOW}[!] PROMPT_RIPRESA non trovato: $ripresa${NC}"
        echo ""
    fi

    # Change to project directory
    echo -e "${GREEN}Cambio directory a: $path${NC}"
    cd "$path"

    # Show NORD.md if exists
    if [ -f "NORD.md" ]; then
        echo -e "${GREEN}NORD.md trovato!${NC}"
    fi

    echo ""
    echo -e "${BLUE}+================================================================+${NC}"
    echo -e "${BLUE}|                    AVVIO CLAUDE CODE                           |${NC}"
    echo -e "${BLUE}+================================================================+${NC}"
    echo ""
    echo -e "Directory: ${CYAN}$(pwd)${NC}"
    echo ""

    # Launch Claude Code
    exec claude
}

# ==============================================================================
# MAIN
# ==============================================================================

case "${1:-}" in
    ""|"-h"|"--help")
        show_help
        ;;
    "--list"|"-l")
        list_projects
        ;;
    *)
        start_session "$1"
        ;;
esac
