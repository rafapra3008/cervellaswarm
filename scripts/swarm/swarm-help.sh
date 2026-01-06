#!/bin/bash
#
# swarm-help.sh - Guida completa comandi CervellaSwarm
# Versione: 1.0.0
# Data: 6 Gennaio 2026
#
# Uso: swarm-help [categoria]
# Categorie: all, essential, session, monitor, task
#

set -e

# Colori
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

VERSION="1.0.0"

print_header() {
    echo ""
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC}  ${BOLD}CERVELLASWARM - GUIDA COMANDI${NC}                                    ${BLUE}║${NC}"
    echo -e "${BLUE}║${NC}  ${CYAN}v${VERSION}${NC} - La famiglia digitale!                                ${BLUE}║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_section() {
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BOLD}${1}${NC}"
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

print_cmd() {
    printf "  ${GREEN}%-25s${NC} %s\n" "$1" "$2"
}

show_essential() {
    print_section "COMANDI ESSENZIALI (usa questi!)"
    echo ""
    print_cmd "spawn-workers --tipo" "Lancia worker (backend/frontend/docs/reviewer/etc)"
    print_cmd "quick-task \"desc\" --tipo" "Crea task + lancia worker in un comando"
    print_cmd "task-new tipo \"titolo\"" "Crea task da template (ricerca/bug/feature/review)"
    print_cmd "swarm-status" "Mostra stato worker attivi"
    print_cmd "swarm-help [categoria]" "Questa guida (categorie: essential, session, monitor, task)"
    echo ""
}

show_session() {
    print_section "COMANDI SESSIONE"
    echo ""
    print_cmd "swarm-session-check" "Verifica roadmap inizio sessione"
    print_cmd "swarm-report" "Report task completati oggi"
    print_cmd "swarm-feedback" "Gestisce feedback (add/list/analyze)"
    print_cmd "swarm-roadmaps" "Vista tutti i progetti attivi"
    echo ""
}

show_monitor() {
    print_section "COMANDI MONITORAGGIO"
    echo ""
    print_cmd "swarm-logs [worker]" "Log live worker (tutti o specifico)"
    print_cmd "swarm-progress" "Progresso task in tempo reale"
    print_cmd "swarm-timeout [min]" "Avvisa se worker bloccato (default: 5min)"
    print_cmd "swarm-health" "Health check sistema completo"
    print_cmd "swarm-heartbeat" "Verifica heartbeat worker attivi"
    echo ""
}

show_task() {
    print_section "COMANDI TASK"
    echo ""
    print_cmd "task-new ricerca \"desc\"" "Template ricerca approfondita"
    print_cmd "task-new bug \"desc\"" "Template fix bug"
    print_cmd "task-new feature \"desc\"" "Template nuova feature"
    print_cmd "task-new review \"desc\"" "Template code review"
    echo ""
    echo -e "  ${CYAN}Templates in:${NC} ~/.claude/scripts/templates/"
    echo ""
}

show_setup() {
    print_section "COMANDI SETUP"
    echo ""
    print_cmd "swarm-init [progetto]" "Inizializza swarm in nuovo progetto"
    print_cmd "swarm-cleanup" "Pulisce task vecchi e log"
    print_cmd "swarm-review" "Review post-task automatica"
    echo ""
}

show_tips() {
    print_section "TIPS RAPIDI"
    echo ""
    echo -e "  ${CYAN}1.${NC} Per vedere worker attivi: ${GREEN}swarm-status${NC}"
    echo -e "  ${CYAN}2.${NC} Per lanciare worker veloce: ${GREEN}quick-task \"fai X\" --backend${NC}"
    echo -e "  ${CYAN}3.${NC} Per creare task con template: ${GREEN}task-new feature \"nuova funzione\"${NC}"
    echo -e "  ${CYAN}4.${NC} Per vedere log live: ${GREEN}swarm-logs${NC}"
    echo -e "  ${CYAN}5.${NC} Per report fine giornata: ${GREEN}swarm-report${NC}"
    echo ""
    echo -e "  ${YELLOW}Regola d'oro:${NC} ${BOLD}DELEGA SEMPRE! La Regina coordina, non esegue!${NC}"
    echo ""
}

show_all() {
    print_header
    show_essential
    show_session
    show_monitor
    show_task
    show_setup
    show_tips
}

# Main
case "${1:-all}" in
    all)
        show_all
        ;;
    essential|e)
        print_header
        show_essential
        ;;
    session|s)
        print_header
        show_session
        ;;
    monitor|m)
        print_header
        show_monitor
        ;;
    task|t)
        print_header
        show_task
        ;;
    setup)
        print_header
        show_setup
        ;;
    tips)
        print_header
        show_tips
        ;;
    -h|--help)
        echo "Uso: swarm-help [categoria]"
        echo ""
        echo "Categorie:"
        echo "  all        Mostra tutto (default)"
        echo "  essential  Comandi essenziali"
        echo "  session    Comandi sessione"
        echo "  monitor    Comandi monitoraggio"
        echo "  task       Comandi task/template"
        echo "  setup      Comandi setup"
        echo "  tips       Tips rapidi"
        ;;
    *)
        echo -e "${YELLOW}Categoria sconosciuta: ${1}${NC}"
        echo "Usa: swarm-help --help"
        exit 1
        ;;
esac
