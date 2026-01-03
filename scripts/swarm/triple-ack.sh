#!/bin/bash
#
# triple-ack.sh - Triple ACK Pattern per comunicazione agenti
#
# CervellaSwarm - Sistema di acknowledgement a 3 livelli
#
# Pattern Triple ACK:
# 1. ACK_RECEIVED    -> "Ho ricevuto il task"
# 2. ACK_UNDERSTOOD  -> "Ho capito cosa devo fare"
# 3. ACK_COMPLETED   -> "Ho completato il task"
#
# Uso:
#   ./triple-ack.sh TASK_ID AGENT_NAME RECEIVED
#   ./triple-ack.sh TASK_ID AGENT_NAME UNDERSTOOD
#   ./triple-ack.sh TASK_ID AGENT_NAME COMPLETED
#   ./triple-ack.sh TASK_ID --status          # Mostra stato ACK
#
# Versione: 1.0.0
# Data: 2026-01-03
# Cervella DevOps & Rafa
# "Comunicazione chiara = Zero casino"

set -e

# ============================================================================
# CONFIGURAZIONE
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
SWARM_DIR="${PROJECT_ROOT}/.swarm"
ACK_DIR="${SWARM_DIR}/acks"

# Crea directory se non esiste
mkdir -p "$ACK_DIR"

# Colori
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# ACK types validi
VALID_ACK_TYPES=("RECEIVED" "UNDERSTOOD" "COMPLETED")

# ============================================================================
# FUNZIONI HELPER
# ============================================================================

log_info() {
    echo -e "${BLUE}[TRIPLE-ACK]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[TRIPLE-ACK]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[TRIPLE-ACK]${NC} $1"
}

log_error() {
    echo -e "${RED}[TRIPLE-ACK]${NC} $1"
}

# Verifica se ACK type e valido
is_valid_ack_type() {
    local ack_type="$1"
    for valid in "${VALID_ACK_TYPES[@]}"; do
        if [ "$ack_type" = "$valid" ]; then
            return 0
        fi
    done
    return 1
}

# Mostra stato ACK per un task
show_ack_status() {
    local task_id="$1"
    local ack_file="${ACK_DIR}/${task_id}.json"

    if [ ! -f "$ack_file" ]; then
        log_warning "Nessun ACK trovato per task: ${task_id}"
        return 1
    fi

    echo ""
    log_info "Status ACK per task: ${task_id}"
    echo ""

    # Parsing JSON base (senza jq per compatibilita)
    local received=$(grep -o '"RECEIVED"[^}]*' "$ack_file" || echo "")
    local understood=$(grep -o '"UNDERSTOOD"[^}]*' "$ack_file" || echo "")
    local completed=$(grep -o '"COMPLETED"[^}]*' "$ack_file" || echo "")

    if [ -n "$received" ]; then
        echo -e "${GREEN}✓${NC} RECEIVED"
    else
        echo -e "${YELLOW}○${NC} RECEIVED"
    fi

    if [ -n "$understood" ]; then
        echo -e "${GREEN}✓${NC} UNDERSTOOD"
    else
        echo -e "${YELLOW}○${NC} UNDERSTOOD"
    fi

    if [ -n "$completed" ]; then
        echo -e "${GREEN}✓${NC} COMPLETED"
    else
        echo -e "${YELLOW}○${NC} COMPLETED"
    fi

    echo ""
    log_info "File: ${ack_file}"
    echo ""
}

# ============================================================================
# PARSE ARGOMENTI
# ============================================================================

if [ $# -lt 2 ]; then
    echo "Uso: $0 TASK_ID AGENT_NAME ACK_TYPE"
    echo "      $0 TASK_ID --status"
    echo ""
    echo "ACK_TYPE: RECEIVED | UNDERSTOOD | COMPLETED"
    echo ""
    echo "Esempi:"
    echo "  $0 task_001 cervella-backend RECEIVED"
    echo "  $0 task_001 cervella-backend UNDERSTOOD"
    echo "  $0 task_001 cervella-backend COMPLETED"
    echo "  $0 task_001 --status"
    exit 1
fi

TASK_ID="$1"
AGENT_NAME="$2"

# Check se richiesto status
if [ "$AGENT_NAME" = "--status" ]; then
    show_ack_status "$TASK_ID"
    exit 0
fi

# Altrimenti procedi con salvataggio ACK
if [ $# -lt 3 ]; then
    log_error "ACK_TYPE mancante!"
    exit 1
fi

ACK_TYPE="$3"

# Valida ACK_TYPE
if ! is_valid_ack_type "$ACK_TYPE"; then
    log_error "ACK_TYPE invalido: ${ACK_TYPE}"
    log_error "ACK_TYPE validi: ${VALID_ACK_TYPES[*]}"
    exit 1
fi

# ============================================================================
# MAIN SCRIPT
# ============================================================================

ACK_FILE="${ACK_DIR}/${TASK_ID}.json"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

log_info "Salvataggio ACK: ${TASK_ID} -> ${ACK_TYPE}"

# Crea o aggiorna file JSON
if [ -f "$ACK_FILE" ]; then
    # File esiste: aggiorna
    log_info "Aggiornamento ACK esistente..."

    # Backup
    cp "$ACK_FILE" "${ACK_FILE}.backup"

    # Leggi contenuto esistente
    EXISTING_CONTENT=$(cat "$ACK_FILE")

    # Rimuovi ultima parentesi graffa
    EXISTING_CONTENT="${EXISTING_CONTENT%\}}"

    # Aggiungi nuovo ACK (sovrascrive se esiste)
    cat > "$ACK_FILE" << EOF
${EXISTING_CONTENT},
  "${ACK_TYPE}": {
    "timestamp": "${TIMESTAMP}",
    "agent": "${AGENT_NAME}"
  }
}
EOF

    # Rimuovi backup se tutto ok
    rm -f "${ACK_FILE}.backup"
else
    # File non esiste: crea nuovo
    log_info "Creazione nuovo file ACK..."

    cat > "$ACK_FILE" << EOF
{
  "task_id": "${TASK_ID}",
  "${ACK_TYPE}": {
    "timestamp": "${TIMESTAMP}",
    "agent": "${AGENT_NAME}"
  }
}
EOF
fi

# Verifica creazione
if [ -f "$ACK_FILE" ]; then
    log_success "ACK salvato!"
    echo ""
    log_info "Task:     ${TASK_ID}"
    log_info "Agent:    ${AGENT_NAME}"
    log_info "ACK Type: ${ACK_TYPE}"
    log_info "Time:     ${TIMESTAMP}"
    log_info "File:     ${ACK_FILE}"
    echo ""

    # Mostra status completo
    show_ack_status "$TASK_ID"

    log_success "✅ TRIPLE-ACK COMPLETATO!"
else
    log_error "Errore nella creazione del file ACK"
    exit 1
fi

exit 0
