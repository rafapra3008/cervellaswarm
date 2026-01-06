#!/bin/bash
#
# swarm-timeout.sh - Monitora worker e avvisa se bloccati!
#
# Uso:
#   swarm-timeout                  # Check singolo
#   swarm-timeout --watch          # Monitora continuo (ogni 60s)
#   swarm-timeout --timeout 300    # Timeout custom (default: 300s = 5 min)
#
# Controlla:
#   - File .working senza .done dopo timeout
#   - Worker PID attivi ma senza heartbeat recente
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
TASKS_DIR="${SWARM_DIR}/tasks"
STATUS_DIR="${SWARM_DIR}/status"

# Default
WATCH_MODE=false
TIMEOUT_SECONDS=300  # 5 minuti
CHECK_INTERVAL=60    # Check ogni 60 secondi in watch mode

# Parse argomenti
while [[ $# -gt 0 ]]; do
    case "$1" in
        --watch|-w)
            WATCH_MODE=true
            ;;
        --timeout|-t)
            shift
            TIMEOUT_SECONDS="$1"
            ;;
        --interval|-i)
            shift
            CHECK_INTERVAL="$1"
            ;;
        --help|-h)
            echo "Uso: swarm-timeout [opzioni]"
            echo ""
            echo "Opzioni:"
            echo "  --watch, -w          Monitora continuo"
            echo "  --timeout, -t SEC    Timeout in secondi (default: 300 = 5 min)"
            echo "  --interval, -i SEC   Intervallo check in watch mode (default: 60)"
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

# Funzione per formattare tempo
format_time() {
    local seconds=$1
    local minutes=$((seconds / 60))
    local secs=$((seconds % 60))
    echo "${minutes}m ${secs}s"
}

# Funzione check timeout
check_timeouts() {
    local now=$(date +%s)
    local found_issues=false

    echo -e "${BLUE}[i]${NC} Checking worker timeout (limite: $(format_time $TIMEOUT_SECONDS))..."
    echo ""

    # Check 1: Task .working senza .done
    if [[ -d "$TASKS_DIR" ]]; then
        for working_file in "$TASKS_DIR"/*.working 2>/dev/null; do
            [[ -f "$working_file" ]] || continue

            local task_name=$(basename "$working_file" .working)
            local done_file="$TASKS_DIR/${task_name}.done"

            # Se già completato, skip
            [[ -f "$done_file" ]] && continue

            # Controlla età del file .working
            local working_time
            if [[ "$OSTYPE" == "darwin"* ]]; then
                working_time=$(stat -f %m "$working_file")
            else
                working_time=$(stat -c %Y "$working_file")
            fi

            local elapsed=$((now - working_time))

            if [[ $elapsed -gt $TIMEOUT_SECONDS ]]; then
                found_issues=true
                echo -e "${RED}[TIMEOUT]${NC} Task: $task_name"
                echo -e "          In lavorazione da: $(format_time $elapsed)"
                echo -e "          File: $working_file"
                echo ""

                # Notifica
                if command -v terminal-notifier &>/dev/null; then
                    terminal-notifier \
                        -title "⚠️ Worker Timeout!" \
                        -subtitle "$task_name" \
                        -message "In lavorazione da $(format_time $elapsed)" \
                        -sound Basso 2>/dev/null
                else
                    osascript -e "display notification \"$task_name in lavorazione da $(format_time $elapsed)\" with title \"Worker Timeout!\" sound name \"Basso\"" 2>/dev/null
                fi
            else
                local remaining=$((TIMEOUT_SECONDS - elapsed))
                echo -e "${GREEN}[OK]${NC} Task: $task_name - attivo da $(format_time $elapsed) (timeout in $(format_time $remaining))"
            fi
        done
    fi

    # Check 2: Worker PID senza heartbeat recente
    if [[ -d "$STATUS_DIR" ]]; then
        for pid_file in "$STATUS_DIR"/worker_*.pid 2>/dev/null; do
            [[ -f "$pid_file" ]] || continue

            local worker_name=$(basename "$pid_file" .pid | sed 's/worker_//')
            local pid=$(cat "$pid_file")
            local start_file="$STATUS_DIR/worker_${worker_name}.start"
            local heartbeat_file="$STATUS_DIR/heartbeat_${worker_name}.log"

            # Controlla se processo ancora vivo
            if ! kill -0 "$pid" 2>/dev/null; then
                echo -e "${YELLOW}[MORTO]${NC} Worker: $worker_name (PID $pid non risponde)"
                rm -f "$pid_file" "$start_file"
                continue
            fi

            # Controlla heartbeat
            if [[ -f "$heartbeat_file" ]]; then
                local last_heartbeat
                if [[ "$OSTYPE" == "darwin"* ]]; then
                    last_heartbeat=$(stat -f %m "$heartbeat_file")
                else
                    last_heartbeat=$(stat -c %Y "$heartbeat_file")
                fi

                local heartbeat_age=$((now - last_heartbeat))

                if [[ $heartbeat_age -gt $TIMEOUT_SECONDS ]]; then
                    found_issues=true
                    echo -e "${RED}[STALLO]${NC} Worker: $worker_name"
                    echo -e "          Ultimo heartbeat: $(format_time $heartbeat_age) fa"
                    echo ""

                    # Notifica
                    if command -v terminal-notifier &>/dev/null; then
                        terminal-notifier \
                            -title "⚠️ Worker Stallo!" \
                            -subtitle "$worker_name" \
                            -message "Nessun heartbeat da $(format_time $heartbeat_age)" \
                            -sound Basso 2>/dev/null
                    fi
                fi
            fi
        done
    fi

    if [[ "$found_issues" == false ]]; then
        echo -e "${GREEN}[OK]${NC} Nessun timeout rilevato."
    fi

    echo ""
}

# Main
echo -e "${PURPLE}"
echo "=============================================="
echo "  SWARM-TIMEOUT - Monitor Worker"
echo "=============================================="
echo -e "${NC}"

if [[ "$WATCH_MODE" == true ]]; then
    echo -e "${BLUE}[i]${NC} Modalità WATCH - Check ogni ${CHECK_INTERVAL}s (Ctrl+C per uscire)"
    echo ""

    while true; do
        echo -e "${BLUE}--- $(date '+%H:%M:%S') ---${NC}"
        check_timeouts
        sleep "$CHECK_INTERVAL"
    done
else
    check_timeouts
fi
