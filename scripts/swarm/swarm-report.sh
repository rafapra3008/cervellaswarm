#!/bin/bash
#
# swarm-report.sh - Report centralizzato task completati
# Versione: 1.0.0
# Data: 6 Gennaio 2026
#
# Uso: swarm-report [--today|--week|--all]
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

# Trova directory task
find_tasks_dir() {
    if [ -d ".swarm/tasks" ]; then
        echo ".swarm/tasks"
    elif [ -d "$HOME/Developer/CervellaSwarm/.swarm/tasks" ]; then
        echo "$HOME/Developer/CervellaSwarm/.swarm/tasks"
    else
        echo ""
    fi
}

TASKS_DIR=$(find_tasks_dir)

if [ -z "$TASKS_DIR" ]; then
    echo -e "${RED}[ERRORE]${NC} Nessuna directory .swarm/tasks trovata"
    exit 1
fi

print_header() {
    echo ""
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC}  ${BOLD}CERVELLASWARM - REPORT TASK${NC}                                      ${BLUE}║${NC}"
    echo -e "${BLUE}║${NC}  ${CYAN}$(date '+%Y-%m-%d %H:%M')${NC}                                            ${BLUE}║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

count_tasks() {
    local pattern="$1"
    find "$TASKS_DIR" -name "*.done" -newermt "$pattern" 2>/dev/null | wc -l | tr -d ' '
}

list_tasks() {
    local pattern="$1"
    local limit="${2:-10}"

    find "$TASKS_DIR" -name "*.done" -newermt "$pattern" 2>/dev/null | \
        while read -r file; do
            basename "$file" .done | sed 's/TASK_//' | sed 's/_/ /g'
        done | head -n "$limit"
}

get_file_time() {
    local file="$1"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        stat -f "%Sm" -t "%Y-%m-%d %H:%M" "$file" 2>/dev/null || echo "unknown"
    else
        stat -c "%y" "$file" 2>/dev/null | cut -d'.' -f1 || echo "unknown"
    fi
}

show_today() {
    print_header

    local today_start="today 00:00"
    local count=$(count_tasks "$today_start")

    echo -e "${YELLOW}━━━ TASK COMPLETATI OGGI ━━━${NC}"
    echo ""
    echo -e "  ${GREEN}Totale:${NC} ${BOLD}$count${NC} task completati"
    echo ""

    if [ "$count" -gt 0 ]; then
        echo -e "  ${CYAN}Ultimi task:${NC}"
        list_tasks "$today_start" 15 | while read -r task; do
            echo -e "    ${GREEN}✓${NC} $task"
        done
    fi
    echo ""
}

show_week() {
    print_header

    local week_start="7 days ago"
    local count=$(count_tasks "$week_start")

    echo -e "${YELLOW}━━━ TASK ULTIMI 7 GIORNI ━━━${NC}"
    echo ""
    echo -e "  ${GREEN}Totale:${NC} ${BOLD}$count${NC} task completati"
    echo ""

    # Breakdown per giorno
    echo -e "  ${CYAN}Per giorno:${NC}"
    for i in {0..6}; do
        local day_start="$i days ago 00:00"
        local day_end="$i days ago 23:59"
        local day_name=$(date -v-${i}d '+%a %d/%m' 2>/dev/null || date -d "$i days ago" '+%a %d/%m')
        local day_count=$(find "$TASKS_DIR" -name "*.done" -newermt "$day_start" ! -newermt "$((i-1)) days ago 00:00" 2>/dev/null | wc -l | tr -d ' ')

        if [ "$day_count" -gt 0 ]; then
            printf "    ${GREEN}%-10s${NC} %s task\n" "$day_name" "$day_count"
        fi
    done
    echo ""
}

show_all() {
    print_header

    local total=$(find "$TASKS_DIR" -name "*.done" 2>/dev/null | wc -l | tr -d ' ')
    local ready=$(find "$TASKS_DIR" -name "*.ready" 2>/dev/null | wc -l | tr -d ' ')
    local pending=$(find "$TASKS_DIR" -name "*.md" ! -name "*.done" ! -name "*.ready" 2>/dev/null | wc -l | tr -d ' ')

    echo -e "${YELLOW}━━━ STATISTICHE COMPLETE ━━━${NC}"
    echo ""
    echo -e "  ${GREEN}Completati:${NC} ${BOLD}$total${NC}"
    echo -e "  ${YELLOW}In attesa:${NC}  ${BOLD}$ready${NC}"
    echo -e "  ${CYAN}Pending:${NC}    ${BOLD}$pending${NC}"
    echo ""

    # Top task types
    echo -e "  ${CYAN}Per tipo:${NC}"
    find "$TASKS_DIR" -name "*.done" 2>/dev/null | \
        xargs -I {} basename {} .done | \
        grep -o 'RICERCA\|BUG\|FEATURE\|REVIEW\|CODE_REVIEW\|STUDIO' | \
        sort | uniq -c | sort -rn | head -5 | \
        while read -r count type; do
            printf "    ${GREEN}%-15s${NC} %s\n" "$type" "$count"
        done
    echo ""
}

show_summary() {
    local today_count=$(count_tasks "today 00:00")
    local week_count=$(count_tasks "7 days ago")

    echo ""
    echo -e "${BOLD}Quick Summary:${NC}"
    echo -e "  Oggi: ${GREEN}$today_count${NC} | Settimana: ${GREEN}$week_count${NC}"
    echo ""
}

# Main
case "${1:---today}" in
    --today|-t)
        show_today
        ;;
    --week|-w)
        show_week
        ;;
    --all|-a)
        show_all
        ;;
    --summary|-s)
        show_summary
        ;;
    -h|--help)
        echo "Uso: swarm-report [opzione]"
        echo ""
        echo "Opzioni:"
        echo "  --today, -t    Task completati oggi (default)"
        echo "  --week, -w     Task ultimi 7 giorni"
        echo "  --all, -a      Statistiche complete"
        echo "  --summary, -s  Riassunto veloce"
        echo ""
        ;;
    *)
        echo -e "${RED}[ERRORE]${NC} Opzione sconosciuta: $1"
        echo "Usa: swarm-report --help"
        exit 1
        ;;
esac
