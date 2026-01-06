#!/bin/bash
#
# swarm-progress.sh - Mostra progresso worker in tempo reale!
#
# Uso:
#   swarm-progress              # Stato attuale
#   swarm-progress --watch      # Aggiorna ogni 5 secondi
#   swarm-progress --compact    # Vista compatta
#
# Legge:
#   - .swarm/status/heartbeat_*.log
#   - .swarm/status/worker_*.pid
#   - .swarm/tasks/*.working
#
# Versione: 1.0.0
# Data: 2026-01-06
# Cervella & Rafa

set -e

# Colori
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

# Trova project root
find_project_root() {
    local search_dir="$(pwd)"
    for i in {1..5}; do
        if [ -d "${search_dir}/.swarm" ]; then
            echo "${search_dir}"
            return 0
        fi
        if [ "${search_dir}" = "/" ]; then
            break
        fi
        search_dir="$(dirname "${search_dir}")"
    done
    echo "$(pwd)"
    return 1
}

PROJECT_ROOT="$(find_project_root)"
SWARM_DIR="${PROJECT_ROOT}/.swarm"
STATUS_DIR="${SWARM_DIR}/status"
TASKS_DIR="${SWARM_DIR}/tasks"

# Default
WATCH_MODE=false
COMPACT_MODE=false
WATCH_INTERVAL=5

# Parse argomenti
while [[ $# -gt 0 ]]; do
    case "$1" in
        --watch|-w)
            WATCH_MODE=true
            ;;
        --compact|-c)
            COMPACT_MODE=true
            ;;
        --interval|-i)
            shift
            WATCH_INTERVAL="$1"
            ;;
        --help|-h)
            echo "Uso: swarm-progress [opzioni]"
            echo ""
            echo "Opzioni:"
            echo "  --watch, -w          Aggiorna ogni 5 secondi"
            echo "  --compact, -c        Vista compatta"
            echo "  --interval, -i SEC   Intervallo aggiornamento (default: 5)"
            echo "  --help, -h           Mostra questo help"
            echo ""
            exit 0
            ;;
        *)
            echo "Opzione sconosciuta: $1"
            exit 1
            ;;
    esac
    shift
done

# Formatta tempo
format_time() {
    local seconds=$1
    if [[ $seconds -lt 60 ]]; then
        echo "${seconds}s"
    else
        local minutes=$((seconds / 60))
        local secs=$((seconds % 60))
        echo "${minutes}m${secs}s"
    fi
}

# Mostra progresso
show_progress() {
    local now=$(date +%s)

    if [[ "$COMPACT_MODE" == false ]]; then
        echo -e "${PURPLE}"
        echo "╔══════════════════════════════════════════════════════════════╗"
        echo "║               🐝 SWARM PROGRESS - Live Status                ║"
        echo "╚══════════════════════════════════════════════════════════════╝"
        echo -e "${NC}"
    else
        echo -e "${PURPLE}═══ SWARM PROGRESS $(date '+%H:%M:%S') ═══${NC}"
    fi

    local active_workers=0
    local completed_today=0

    # Conta task completati oggi
    if [[ -d "$TASKS_DIR" ]]; then
        local today=$(date +%Y%m%d)
        for done_file in "$TASKS_DIR"/*.done 2>/dev/null; do
            [[ -f "$done_file" ]] || continue
            local file_date
            if [[ "$OSTYPE" == "darwin"* ]]; then
                file_date=$(stat -f %Sm -t %Y%m%d "$done_file")
            else
                file_date=$(date -r "$done_file" +%Y%m%d)
            fi
            if [[ "$file_date" == "$today" ]]; then
                completed_today=$((completed_today + 1))
            fi
        done
    fi

    # Mostra worker attivi
    if [[ -d "$STATUS_DIR" ]]; then
        for pid_file in "$STATUS_DIR"/worker_*.pid 2>/dev/null; do
            [[ -f "$pid_file" ]] || continue

            local worker_name=$(basename "$pid_file" .pid | sed 's/worker_//')
            local pid=$(cat "$pid_file")
            local start_file="$STATUS_DIR/worker_${worker_name}.start"
            local heartbeat_file="$STATUS_DIR/heartbeat_${worker_name}.log"
            local task_file="$STATUS_DIR/worker_${worker_name}.task"

            # Verifica se processo vivo
            if ! kill -0 "$pid" 2>/dev/null; then
                continue
            fi

            active_workers=$((active_workers + 1))

            # Calcola tempo attivo
            local elapsed="?"
            if [[ -f "$start_file" ]]; then
                local start_time=$(cat "$start_file")
                elapsed=$(format_time $((now - start_time)))
            fi

            # Leggi task corrente
            local current_task="(sconosciuto)"
            if [[ -f "$task_file" ]]; then
                current_task=$(cat "$task_file")
            fi

            # Leggi ultimo heartbeat
            local last_activity="(nessun heartbeat)"
            local heartbeat_age="?"
            if [[ -f "$heartbeat_file" ]]; then
                local last_line=$(tail -1 "$heartbeat_file")
                if [[ -n "$last_line" ]]; then
                    local hb_time=$(echo "$last_line" | cut -d'|' -f1)
                    last_activity=$(echo "$last_line" | cut -d'|' -f3)
                    if [[ -n "$hb_time" && "$hb_time" =~ ^[0-9]+$ ]]; then
                        heartbeat_age=$(format_time $((now - hb_time)))
                    fi
                fi
            fi

            if [[ "$COMPACT_MODE" == true ]]; then
                echo -e "${CYAN}●${NC} ${GREEN}$worker_name${NC} [$elapsed] → $current_task"
            else
                echo -e "${CYAN}┌──────────────────────────────────────────────────────────────┐${NC}"
                echo -e "${CYAN}│${NC} ${GREEN}🐝 $worker_name${NC}"
                echo -e "${CYAN}│${NC}   Task: ${YELLOW}$current_task${NC}"
                echo -e "${CYAN}│${NC}   Tempo: $elapsed | Ultimo heartbeat: $heartbeat_age fa"
                if [[ "$last_activity" != "(nessun heartbeat)" ]]; then
                    echo -e "${CYAN}│${NC}   Attività: $last_activity"
                fi
                echo -e "${CYAN}└──────────────────────────────────────────────────────────────┘${NC}"
            fi
        done
    fi

    # Mostra task in lavorazione senza worker (orfani)
    if [[ -d "$TASKS_DIR" ]]; then
        for working_file in "$TASKS_DIR"/*.working 2>/dev/null; do
            [[ -f "$working_file" ]] || continue

            local task_name=$(basename "$working_file" .working)
            local done_file="$TASKS_DIR/${task_name}.done"

            # Se già completato, skip
            [[ -f "$done_file" ]] && continue

            # Controlla età
            local working_time
            if [[ "$OSTYPE" == "darwin"* ]]; then
                working_time=$(stat -f %m "$working_file")
            else
                working_time=$(stat -c %Y "$working_file")
            fi
            local elapsed=$(format_time $((now - working_time)))

            if [[ "$COMPACT_MODE" == true ]]; then
                echo -e "${YELLOW}○${NC} $task_name [$elapsed] (in lavorazione)"
            else
                echo -e "${YELLOW}○ Task in lavorazione: $task_name [$elapsed]${NC}"
            fi
        done
    fi

    # Riepilogo
    echo ""
    if [[ "$COMPACT_MODE" == true ]]; then
        echo -e "${BLUE}Workers: $active_workers | Completati oggi: $completed_today${NC}"
    else
        echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${BLUE}Worker attivi: ${GREEN}$active_workers${NC} | ${BLUE}Completati oggi: ${GREEN}$completed_today${NC}"
        echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    fi

    if [[ $active_workers -eq 0 ]]; then
        echo ""
        echo -e "${YELLOW}Nessun worker attivo al momento.${NC}"
        echo "Lancia worker con: spawn-workers --backend"
    fi
}

# Main
if [[ "$WATCH_MODE" == true ]]; then
    while true; do
        clear
        show_progress
        echo ""
        echo -e "${BLUE}[Aggiornamento ogni ${WATCH_INTERVAL}s - Ctrl+C per uscire]${NC}"
        sleep "$WATCH_INTERVAL"
    done
else
    show_progress
fi
