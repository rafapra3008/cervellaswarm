#!/bin/bash
#
# swarm-logs.sh - Vedere output worker in tempo reale!
#
# Uso:
#   swarm-logs                    # Tutti i log recenti
#   swarm-logs --follow           # Live tail (Ctrl+C per uscire)
#   swarm-logs --worker backend   # Solo un worker specifico
#   swarm-logs --last 50          # Ultime N righe
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
LOGS_DIR="${SWARM_DIR}/logs"

# Default
FOLLOW=false
WORKER=""
LAST_LINES=30

# Parse argomenti
while [[ $# -gt 0 ]]; do
    case "$1" in
        --follow|-f)
            FOLLOW=true
            ;;
        --worker|-w)
            shift
            WORKER="$1"
            ;;
        --last|-n)
            shift
            LAST_LINES="$1"
            ;;
        --help|-h)
            echo "Uso: swarm-logs [opzioni]"
            echo ""
            echo "Opzioni:"
            echo "  --follow, -f        Live tail (Ctrl+C per uscire)"
            echo "  --worker, -w NAME   Solo worker specifico (es: backend)"
            echo "  --last, -n N        Ultime N righe (default: 30)"
            echo "  --help, -h          Mostra questo help"
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

# Verifica directory esiste
if [[ ! -d "$LOGS_DIR" ]]; then
    echo -e "${YELLOW}[!] Directory logs non esiste: $LOGS_DIR${NC}"
    echo "    Nessun worker ha ancora scritto log."
    exit 0
fi

echo -e "${PURPLE}"
echo "=============================================="
echo "  SWARM-LOGS - Output Worker Live"
echo "=============================================="
echo -e "${NC}"

if [[ "$FOLLOW" == true ]]; then
    echo -e "${BLUE}[i]${NC} Modalità LIVE - Ctrl+C per uscire"
    echo ""

    if [[ -n "$WORKER" ]]; then
        # Solo un worker specifico
        LOG_PATTERN="${LOGS_DIR}/worker_*${WORKER}*.log"
        LATEST=$(ls -t $LOG_PATTERN 2>/dev/null | head -1)
        if [[ -n "$LATEST" ]]; then
            echo -e "${GREEN}[>]${NC} Following: $(basename "$LATEST")"
            echo ""
            tail -f "$LATEST"
        else
            echo -e "${YELLOW}[!]${NC} Nessun log trovato per worker: $WORKER"
        fi
    else
        # Tutti i log recenti
        echo -e "${GREEN}[>]${NC} Following tutti i log recenti..."
        echo ""
        # Trova i log più recenti (ultimi 5 minuti)
        find "$LOGS_DIR" -name "worker_*.log" -mmin -5 -exec tail -f {} + 2>/dev/null || \
            tail -f "${LOGS_DIR}"/worker_*.log 2>/dev/null || \
            echo "Nessun log attivo."
    fi
else
    # Mostra ultime righe
    if [[ -n "$WORKER" ]]; then
        LOG_PATTERN="${LOGS_DIR}/worker_*${WORKER}*.log"
        LATEST=$(ls -t $LOG_PATTERN 2>/dev/null | head -1)
        if [[ -n "$LATEST" ]]; then
            echo -e "${GREEN}[>]${NC} Log: $(basename "$LATEST")"
            echo ""
            tail -n "$LAST_LINES" "$LATEST"
        else
            echo -e "${YELLOW}[!]${NC} Nessun log trovato per worker: $WORKER"
        fi
    else
        # Mostra ultimi log di tutti i worker
        echo -e "${BLUE}[i]${NC} Ultimi $LAST_LINES righe per worker:"
        echo ""

        for log in $(ls -t "${LOGS_DIR}"/worker_*.log 2>/dev/null | head -5); do
            echo -e "${GREEN}━━━ $(basename "$log") ━━━${NC}"
            tail -n "$LAST_LINES" "$log"
            echo ""
        done

        if [[ ! -f "${LOGS_DIR}"/worker_*.log ]]; then
            echo -e "${YELLOW}[!]${NC} Nessun log trovato."
        fi
    fi
fi
