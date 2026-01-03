#!/bin/bash
#
# shutdown-sequence.sh - Chiusura pulita sessione swarm
#
# CervellaSwarm - Graceful Shutdown con verifica e report
#
# Quando chiudi una sessione swarm:
# 1. VERIFICA -> Nessun task in corso
# 2. PULISCI  -> File temporanei .swarm/active/
# 3. REPORT   -> Genera riepilogo in reports/
# 4. COMMIT   -> Git commit se ci sono modifiche
# 5. CHIUDI   -> Riepilogo finale
#
# Uso:
#   ./shutdown-sequence.sh                    # Shutdown normale
#   ./shutdown-sequence.sh --force            # Forza shutdown (ignora task attivi)
#   ./shutdown-sequence.sh --no-report        # Senza generazione report
#
# Versione: 1.0.0
# Data: 2026-01-03
# Cervella DevOps & Rafa
# "Chiusura pulita = Ripartenza facile"

set -e

# ============================================================================
# CONFIGURAZIONE
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
SWARM_DIR="${PROJECT_ROOT}/.swarm"
REPORTS_DIR="${PROJECT_ROOT}/reports"

# Crea directories se non esistono
mkdir -p "$REPORTS_DIR"
mkdir -p "${SWARM_DIR}/archive"

# Colori
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Opzioni
FORCE_SHUTDOWN=false
GENERATE_REPORT=true

# ============================================================================
# FUNZIONI HELPER
# ============================================================================

log_info() {
    echo -e "${BLUE}[SHUTDOWN]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SHUTDOWN]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[SHUTDOWN]${NC} $1"
}

log_error() {
    echo -e "${RED}[SHUTDOWN]${NC} $1"
}

# Conta task attivi
count_active_tasks() {
    local count=0

    # Verifica file .working
    if [ -d "${SWARM_DIR}/tasks" ]; then
        count=$(find "${SWARM_DIR}/tasks" -name "*.working" 2>/dev/null | wc -l | tr -d ' ')
    fi

    echo "$count"
}

# Verifica se ci sono modifiche git
has_git_changes() {
    if git diff --quiet && git diff --cached --quiet; then
        return 1
    else
        return 0
    fi
}

# ============================================================================
# PARSE ARGOMENTI
# ============================================================================

while [[ $# -gt 0 ]]; do
    case "$1" in
        --force)
            FORCE_SHUTDOWN=true
            shift
            ;;
        --no-report)
            GENERATE_REPORT=false
            shift
            ;;
        --help|-h)
            echo "Uso: $0 [opzioni]"
            echo ""
            echo "Opzioni:"
            echo "  --force          Forza shutdown (ignora task attivi)"
            echo "  --no-report      Non genera report finale"
            echo "  --help, -h       Mostra questo help"
            echo ""
            echo "Esempi:"
            echo "  $0                  # Shutdown normale"
            echo "  $0 --force          # Forza shutdown"
            echo "  $0 --no-report      # Senza report"
            exit 0
            ;;
        *)
            log_error "Opzione sconosciuta: $1"
            exit 1
            ;;
    esac
done

# ============================================================================
# MAIN SCRIPT
# ============================================================================

echo ""
log_info "========================================="
log_info "  SHUTDOWN SEQUENCE INIZIATO"
log_info "========================================="
echo ""

# Step 1: Verifica task attivi
log_info "[1/5] Verifica task in corso..."

ACTIVE_TASKS=$(count_active_tasks)

if [ "$ACTIVE_TASKS" -gt 0 ]; then
    log_warning "Trovati ${ACTIVE_TASKS} task ancora attivi!"

    if [ "$FORCE_SHUTDOWN" = true ]; then
        log_warning "Flag --force attivo: procedo comunque"
    else
        log_error "Impossibile chiudere con task attivi"
        log_error "Usa --force per forzare la chiusura"
        exit 1
    fi
else
    log_success "Nessun task attivo - OK!"
fi

# Step 2: Pulizia file temporanei
log_info "[2/5] Pulizia file temporanei..."

CLEANED=0

# Archivia file .working se esistono (in caso di --force)
if [ -d "${SWARM_DIR}/tasks" ]; then
    WORKING_FILES=$(find "${SWARM_DIR}/tasks" -name "*.working" 2>/dev/null || true)

    if [ -n "$WORKING_FILES" ]; then
        TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
        ARCHIVE_DIR="${SWARM_DIR}/archive/shutdown_${TIMESTAMP}"
        mkdir -p "$ARCHIVE_DIR"

        echo "$WORKING_FILES" | while read -r file; do
            if [ -f "$file" ]; then
                mv "$file" "$ARCHIVE_DIR/"
                CLEANED=$((CLEANED + 1))
            fi
        done

        log_warning "Archiviati ${CLEANED} file .working in ${ARCHIVE_DIR}"
    fi
fi

# Pulisci locks vecchi (> 1 ora)
if [ -d "${SWARM_DIR}/locks" ]; then
    OLD_LOCKS=$(find "${SWARM_DIR}/locks" -name "*.lock" -mmin +60 2>/dev/null || true)

    if [ -n "$OLD_LOCKS" ]; then
        echo "$OLD_LOCKS" | while read -r lock; do
            if [ -f "$lock" ]; then
                rm -f "$lock"
                CLEANED=$((CLEANED + 1))
            fi
        done
    fi
fi

log_success "Pulizia completata (${CLEANED} file)"

# Step 3: Genera report finale
if [ "$GENERATE_REPORT" = true ]; then
    log_info "[3/5] Generazione report finale..."

    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    REPORT_FILE="${REPORTS_DIR}/shutdown_${TIMESTAMP}.md"

    cat > "$REPORT_FILE" << EOF
# Shutdown Report - $(date +"%Y-%m-%d %H:%M:%S")

## Sessione Info

- **Branch**: $(git rev-parse --abbrev-ref HEAD)
- **Ultimo commit**: $(git log -1 --oneline)
- **Task attivi**: ${ACTIVE_TASKS}
- **File puliti**: ${CLEANED}

## Git Status

\`\`\`
$(git status --short)
\`\`\`

## Task Completati

$(find "${SWARM_DIR}/tasks" -name "*.done" 2>/dev/null | wc -l | tr -d ' ') task completati in questa sessione

## Note

Shutdown completato con successo.
EOF

    log_success "Report generato: ${REPORT_FILE}"
else
    log_info "[3/5] Report saltato (--no-report)"
fi

# Step 4: Git commit se necessario
log_info "[4/5] Verifica modifiche git..."

if has_git_changes; then
    log_warning "Trovate modifiche non committate"

    echo ""
    git status --short
    echo ""

    read -p "Vuoi committare le modifiche? (y/N): " -n 1 -r
    echo ""

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add -A
        TIMESTAMP=$(date +"%Y-%m-%d %H:%M")
        git commit -m "Shutdown sequence: ${TIMESTAMP}"
        log_success "Commit creato!"

        read -p "Vuoi pushare? (y/N): " -n 1 -r
        echo ""

        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git push
            log_success "Push completato!"
        else
            log_warning "Push saltato (ricordati di pushare!)"
        fi
    else
        log_warning "Commit saltato"
    fi
else
    log_success "Nessuna modifica da committare"
fi

# Step 5: Riepilogo finale
log_info "[5/5] Riepilogo finale..."

echo ""
log_success "========================================="
log_success "  SHUTDOWN COMPLETATO!"
log_success "========================================="
echo ""
log_info "Branch:        $(git rev-parse --abbrev-ref HEAD)"
log_info "Ultimo commit: $(git log -1 --oneline)"
log_info "Task attivi:   ${ACTIVE_TASKS}"
log_info "File puliti:   ${CLEANED}"

if [ "$GENERATE_REPORT" = true ]; then
    log_info "Report:        ${REPORT_FILE}"
fi

echo ""
log_success "✅ Sessione chiusa correttamente!"
log_success "La prossima Cervella puo riprendere da PROMPT_RIPRESA.md"
echo ""

exit 0
