#!/bin/bash
#
# swarm-feedback.sh - Sistema Feedback Cervelle!
#
# Uso:
#   swarm-feedback add            # Aggiungi feedback interattivo
#   swarm-feedback add "testo"    # Aggiungi feedback diretto
#   swarm-feedback list           # Lista feedback recenti
#   swarm-feedback analyze        # Analizza pattern
#   swarm-feedback export         # Esporta a JSON
#
# Il feedback viene salvato in ~/.swarm/feedback/
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

# Directory feedback globale
FEEDBACK_DIR="$HOME/.swarm/feedback"
FEEDBACK_FILE="$FEEDBACK_DIR/feedback.jsonl"

# Crea directory se non esiste
mkdir -p "$FEEDBACK_DIR"

# Trova progetto corrente
find_project_name() {
    local search_dir="$(pwd)"
    for i in {1..5}; do
        if [ -d "${search_dir}/.swarm" ]; then
            basename "${search_dir}"
            return 0
        fi
        if [ "${search_dir}" = "/" ]; then
            break
        fi
        search_dir="$(dirname "${search_dir}")"
    done
    echo "unknown"
}

PROJECT_NAME="$(find_project_name)"

# Funzione per aggiungere feedback
add_feedback() {
    local feedback_text="$1"
    local feedback_type="${2:-general}"
    local timestamp=$(date +%s)
    local date_str=$(date '+%Y-%m-%d %H:%M:%S')
    local session_id="${SESSION_ID:-$(date +%Y%m%d)}"

    # Se nessun testo, chiedi interattivamente
    if [[ -z "$feedback_text" ]]; then
        echo -e "${PURPLE}"
        echo "╔══════════════════════════════════════════════════════════════╗"
        echo "║           🐝 FEEDBACK CERVELLA - Fine Sessione               ║"
        echo "╚══════════════════════════════════════════════════════════════╝"
        echo -e "${NC}"

        echo -e "${BLUE}Progetto:${NC} $PROJECT_NAME"
        echo -e "${BLUE}Data:${NC} $date_str"
        echo ""

        echo -e "${CYAN}1. Cosa ha funzionato BENE oggi?${NC}"
        read -r worked_well

        echo ""
        echo -e "${CYAN}2. Cosa NON ha funzionato?${NC}"
        read -r didnt_work

        echo ""
        echo -e "${CYAN}3. Cosa hai imparato?${NC}"
        read -r learned

        echo ""
        echo -e "${CYAN}4. Suggerimenti per migliorare?${NC}"
        read -r suggestions

        # Costruisci JSON
        local json=$(cat << EOF
{"timestamp":$timestamp,"date":"$date_str","project":"$PROJECT_NAME","session":"$session_id","type":"session_end","worked_well":"$worked_well","didnt_work":"$didnt_work","learned":"$learned","suggestions":"$suggestions"}
EOF
)
        echo "$json" >> "$FEEDBACK_FILE"

        echo ""
        echo -e "${GREEN}[OK]${NC} Feedback salvato!"
        echo -e "${BLUE}File:${NC} $FEEDBACK_FILE"
    else
        # Feedback diretto
        local json=$(cat << EOF
{"timestamp":$timestamp,"date":"$date_str","project":"$PROJECT_NAME","session":"$session_id","type":"$feedback_type","text":"$feedback_text"}
EOF
)
        echo "$json" >> "$FEEDBACK_FILE"
        echo -e "${GREEN}[OK]${NC} Feedback salvato: $feedback_text"
    fi
}

# Funzione per listare feedback
list_feedback() {
    local limit="${1:-10}"

    echo -e "${PURPLE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║              🐝 FEEDBACK RECENTI                             ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"

    if [[ ! -f "$FEEDBACK_FILE" ]]; then
        echo -e "${YELLOW}Nessun feedback ancora.${NC}"
        echo "Usa: swarm-feedback add"
        return
    fi

    local count=0
    while IFS= read -r line; do
        count=$((count + 1))
        if [[ $count -gt $limit ]]; then
            break
        fi

        # Parse JSON (semplice, senza jq)
        local date=$(echo "$line" | grep -o '"date":"[^"]*"' | cut -d'"' -f4)
        local project=$(echo "$line" | grep -o '"project":"[^"]*"' | cut -d'"' -f4)
        local type=$(echo "$line" | grep -o '"type":"[^"]*"' | cut -d'"' -f4)

        echo -e "${CYAN}━━━ $date | $project | $type ━━━${NC}"

        if [[ "$type" == "session_end" ]]; then
            local worked=$(echo "$line" | grep -o '"worked_well":"[^"]*"' | cut -d'"' -f4)
            local didnt=$(echo "$line" | grep -o '"didnt_work":"[^"]*"' | cut -d'"' -f4)
            local learned=$(echo "$line" | grep -o '"learned":"[^"]*"' | cut -d'"' -f4)

            [[ -n "$worked" ]] && echo -e "  ${GREEN}✅ Funzionato:${NC} $worked"
            [[ -n "$didnt" ]] && echo -e "  ${RED}❌ Problemi:${NC} $didnt"
            [[ -n "$learned" ]] && echo -e "  ${BLUE}📚 Imparato:${NC} $learned"
        else
            local text=$(echo "$line" | grep -o '"text":"[^"]*"' | cut -d'"' -f4)
            echo "  $text"
        fi
        echo ""
    done < <(tail -r "$FEEDBACK_FILE" 2>/dev/null || tac "$FEEDBACK_FILE" 2>/dev/null || cat "$FEEDBACK_FILE")

    echo -e "${BLUE}Totale feedback: $(wc -l < "$FEEDBACK_FILE" | xargs)${NC}"
}

# Funzione per analizzare pattern
analyze_feedback() {
    echo -e "${PURPLE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║              🔍 ANALISI FEEDBACK                             ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"

    if [[ ! -f "$FEEDBACK_FILE" ]]; then
        echo -e "${YELLOW}Nessun feedback da analizzare.${NC}"
        return
    fi

    local total=$(wc -l < "$FEEDBACK_FILE" | xargs)
    echo -e "${BLUE}Feedback totali:${NC} $total"
    echo ""

    # Conta per progetto
    echo -e "${CYAN}Per Progetto:${NC}"
    grep -o '"project":"[^"]*"' "$FEEDBACK_FILE" | cut -d'"' -f4 | sort | uniq -c | sort -rn | head -5
    echo ""

    # Problemi frequenti (parole chiave)
    echo -e "${CYAN}Parole chiave problemi:${NC}"
    grep -o '"didnt_work":"[^"]*"' "$FEEDBACK_FILE" | cut -d'"' -f4 | \
        tr ' ' '\n' | tr '[:upper:]' '[:lower:]' | \
        grep -E '^[a-z]{4,}$' | sort | uniq -c | sort -rn | head -10

    echo ""

    # Pattern positivi
    echo -e "${CYAN}Parole chiave successi:${NC}"
    grep -o '"worked_well":"[^"]*"' "$FEEDBACK_FILE" | cut -d'"' -f4 | \
        tr ' ' '\n' | tr '[:upper:]' '[:lower:]' | \
        grep -E '^[a-z]{4,}$' | sort | uniq -c | sort -rn | head -10
}

# Funzione export
export_feedback() {
    local output_file="${1:-feedback_export_$(date +%Y%m%d).json}"

    if [[ ! -f "$FEEDBACK_FILE" ]]; then
        echo -e "${YELLOW}Nessun feedback da esportare.${NC}"
        return
    fi

    echo "[" > "$output_file"
    local first=true
    while IFS= read -r line; do
        if [[ "$first" == true ]]; then
            first=false
        else
            echo "," >> "$output_file"
        fi
        echo "$line" >> "$output_file"
    done < "$FEEDBACK_FILE"
    echo "]" >> "$output_file"

    echo -e "${GREEN}[OK]${NC} Esportato in: $output_file"
}

# Main
case "${1:-help}" in
    add)
        shift
        add_feedback "$@"
        ;;
    list)
        shift
        list_feedback "$@"
        ;;
    analyze)
        analyze_feedback
        ;;
    export)
        shift
        export_feedback "$@"
        ;;
    help|--help|-h)
        echo "Uso: swarm-feedback <comando>"
        echo ""
        echo "Comandi:"
        echo "  add [testo]    Aggiungi feedback (interattivo se senza testo)"
        echo "  list [N]       Lista ultimi N feedback (default: 10)"
        echo "  analyze        Analizza pattern nei feedback"
        echo "  export [file]  Esporta a JSON"
        echo "  help           Mostra questo help"
        echo ""
        ;;
    *)
        echo "Comando sconosciuto: $1"
        echo "Usa: swarm-feedback help"
        exit 1
        ;;
esac
