#!/bin/bash
# ============================================================================
# CervellaSwarm - Common Functions Library
# ============================================================================
# Funzioni condivise tra tutti gli script dello swarm.
# Elimina duplicazione di codice (DRY principle).
#
# Uso:
#   source "$(dirname "$0")/common.sh"
#   oppure
#   source "$HOME/.claude/scripts/common.sh"
#
# Versione: 1.0.0
# Data: 2026-01-09
# ============================================================================

# ============================================================================
# COLORI
# ============================================================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ============================================================================
# FUNZIONI OUTPUT
# ============================================================================

print_header() {
    local title="${1:-CervellaSwarm}"
    echo ""
    echo -e "${PURPLE}============================================${NC}"
    echo -e "${PURPLE}  ${title}${NC}"
    echo -e "${PURPLE}============================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[X]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[i]${NC} $1"
}

# ============================================================================
# CONFIGURAZIONE
# ============================================================================

# Path configurazione globale swarm
SWARM_CONFIG="${SWARM_CONFIG:-$HOME/.swarm/config}"

# Valida che il file config sia sicuro da caricare (ownership check)
validate_config_ownership() {
    local file="$1"
    [[ -f "$file" ]] || return 1

    local file_owner current_uid
    if [[ "$OSTYPE" == "darwin"* ]]; then
        file_owner=$(stat -f %u "$file")
    else
        file_owner=$(stat -c %u "$file")
    fi
    current_uid=$(id -u)

    # Deve essere di proprieta dell'utente corrente
    [[ "$file_owner" == "$current_uid" ]] || return 1

    # Verifica che non sia world-writable
    local perms
    if [[ "$OSTYPE" == "darwin"* ]]; then
        perms=$(stat -f %Lp "$file")
    else
        perms=$(stat -c %a "$file")
    fi
    # Rifiuta se world-writable (ultimo digit 2, 3, 6, 7)
    [[ ! "${perms: -1}" =~ [2367] ]] || return 1

    return 0
}

# Carica configurazione se valida
load_swarm_config() {
    if [[ -f "$SWARM_CONFIG" ]]; then
        if validate_config_ownership "$SWARM_CONFIG"; then
            source "$SWARM_CONFIG"
            return 0
        else
            echo "[!] Config $SWARM_CONFIG non caricato: ownership/permessi non validi" >&2
            return 1
        fi
    fi
    return 1
}

# ============================================================================
# CLAUDE CLI
# ============================================================================

# Trova Claude CLI (usa config o auto-detect)
get_claude_bin() {
    if [[ -n "$CLAUDE_BIN" && -x "$CLAUDE_BIN" ]]; then
        echo "$CLAUDE_BIN"
    elif command -v claude &>/dev/null; then
        which claude
    else
        # Cerca qualsiasi versione Node in NVM (non hardcodata!)
        local nvm_claude
        nvm_claude=$(ls -t "$HOME"/.nvm/versions/node/*/bin/claude 2>/dev/null | head -1)
        if [[ -n "$nvm_claude" && -x "$nvm_claude" ]]; then
            echo "$nvm_claude"
        else
            echo ""
        fi
    fi
}

# ============================================================================
# PROJECT DETECTION
# ============================================================================

# Trova la root del progetto cercando .swarm/
# Restituisce 0 se trovato, 1 se non trovato
find_project_root() {
    local search_dir="${1:-$(pwd)}"

    # Cerca .swarm/ nella directory corrente o nelle superiori (max 5 livelli)
    for i in {1..5}; do
        if [ -d "${search_dir}/.swarm" ]; then
            echo "${search_dir}"
            return 0
        fi
        # Se siamo alla root, fermiamoci
        if [ "${search_dir}" = "/" ]; then
            break
        fi
        search_dir="$(dirname "${search_dir}")"
    done

    # Non trovato
    echo "$(pwd)"
    return 1
}

# Verifica che siamo in un progetto CervellaSwarm valido
require_swarm_project() {
    local project_root
    if ! project_root="$(find_project_root)"; then
        print_error "Non sei in un progetto CervellaSwarm!"
        print_error "Nessuna directory .swarm/ trovata."
        print_info "Per inizializzare: mkdir -p .swarm/tasks"
        exit 1
    fi
    echo "$project_root"
}

# ============================================================================
# STDBUF DETECTION (per output realtime)
# ============================================================================

# Trova comando per unbuffered output
get_stdbuf_cmd() {
    if command -v stdbuf &>/dev/null; then
        echo "stdbuf -oL"
    elif command -v gstdbuf &>/dev/null; then
        echo "gstdbuf -oL"
    elif command -v unbuffer &>/dev/null; then
        echo "unbuffer"
    else
        echo ""
    fi
}

# ============================================================================
# UTILITY
# ============================================================================

# Verifica che un comando esista
require_command() {
    local cmd="$1"
    local msg="${2:-Comando '$cmd' non trovato!}"
    if ! command -v "$cmd" &>/dev/null; then
        print_error "$msg"
        return 1
    fi
    return 0
}

# Timestamp formattato
timestamp() {
    date '+%Y-%m-%d %H:%M:%S'
}

# Timestamp per filename
timestamp_file() {
    date '+%Y%m%d_%H%M%S'
}

# ============================================================================
# SECURITY - Escaping per notifiche macOS
# ============================================================================

# Sanitizza stringa per uso sicuro in osascript
# Rimuove/escapa caratteri che potrebbero causare injection
sanitize_for_osascript() {
    local input="$1"
    # Rimuove backslash, virgolette, newline
    # Limita lunghezza a 200 caratteri per notifiche
    echo "$input" | tr -d '\\\"' | tr '\n' ' ' | cut -c1-200
}

# Invia notifica macOS in modo sicuro
notify_macos() {
    local title="$1"
    local message="$2"
    local sound="${3:-Glass}"

    # Sanitizza input
    title=$(sanitize_for_osascript "$title")
    message=$(sanitize_for_osascript "$message")

    # Invia notifica
    osascript -e "display notification \"$message\" with title \"$title\" sound name \"$sound\"" 2>/dev/null || true
}

# Notifica con terminal-notifier se disponibile (supporta click action)
notify_macos_advanced() {
    local title="$1"
    local message="$2"
    local sound="${3:-Glass}"
    local open_url="${4:-}"

    title=$(sanitize_for_osascript "$title")
    message=$(sanitize_for_osascript "$message")

    if command -v terminal-notifier &>/dev/null && [[ -n "$open_url" ]]; then
        terminal-notifier \
            -title "$title" \
            -message "$message" \
            -sound "$sound" \
            -open "$open_url" 2>/dev/null
    else
        notify_macos "$title" "$message" "$sound"
    fi
}
