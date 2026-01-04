#!/bin/bash
#
# anti-compact.sh - ANTI-COMPACT AUTOMATICO (CRITICO!)
#
# CervellaSwarm - Salvavita quando Claude sta per fare compact
#
# Quando Claude sta per fare compact (perdere contesto):
# 1. RILEVA  -> Segnale di compact imminente
# 2. FERMA   -> Stop tutto, niente a meta
# 3. SALVA   -> git add + commit + push
# 4. APRI    -> Nuova finestra automaticamente (opzionale)
# 5. CONTINUA -> La nuova Cervella riprende
#
# Uso:
#   ./anti-compact.sh                     # Checkpoint + push
#   ./anti-compact.sh --no-spawn          # Solo checkpoint, no nuova finestra
#   ./anti-compact.sh --message "testo"   # Con messaggio custom
#
# Versione: 1.1.0
# Data: 2026-01-04
# Fix: comando claude corretto (era 'claudecode')
# Cervella DevOps & Rafa
# "ZERO PERDITA. ZERO PANICO. MAGIA PURA."

set -e

# ============================================================================
# CONFIGURAZIONE
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
SWARM_DIR="${PROJECT_ROOT}/.swarm"
PROMPT_RIPRESA="${PROJECT_ROOT}/PROMPT_RIPRESA.md"

# Colori
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Opzioni
SPAWN_NEW_WINDOW=true
CUSTOM_MESSAGE=""

# ============================================================================
# FUNZIONI HELPER
# ============================================================================

log_info() {
    echo -e "${BLUE}[ANTI-COMPACT]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[ANTI-COMPACT]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[ANTI-COMPACT]${NC} $1"
}

log_error() {
    echo -e "${RED}[ANTI-COMPACT]${NC} $1"
}

# ============================================================================
# PARSE ARGOMENTI
# ============================================================================

while [[ $# -gt 0 ]]; do
    case "$1" in
        --no-spawn)
            SPAWN_NEW_WINDOW=false
            shift
            ;;
        --message)
            CUSTOM_MESSAGE="$2"
            shift 2
            ;;
        --help|-h)
            echo "Uso: $0 [opzioni]"
            echo ""
            echo "Opzioni:"
            echo "  --no-spawn          Non apre nuova finestra Claude Code"
            echo "  --message TEXT      Messaggio custom per commit"
            echo "  --help, -h          Mostra questo help"
            echo ""
            echo "Esempi:"
            echo "  $0                              # Checkpoint completo + spawn"
            echo "  $0 --no-spawn                   # Solo checkpoint"
            echo "  $0 --message 'Sprint 9.2 WIP'   # Con messaggio custom"
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

log_info "⚠️  COMPACT IMMINENTE! Salvataggio automatico..."

# Step 1: Timestamp
TIMESTAMP=$(date +"%Y-%m-%d %H:%M")
log_info "Timestamp: ${TIMESTAMP}"

# Step 2: Aggiorna PROMPT_RIPRESA.md con checkpoint automatico
log_info "Aggiornamento PROMPT_RIPRESA.md..."

if [ -f "$PROMPT_RIPRESA" ]; then
    # Aggiungi sezione auto-checkpoint alla fine
    cat >> "$PROMPT_RIPRESA" << EOF

---

## AUTO-CHECKPOINT: ${TIMESTAMP} (compact)

### Stato Git
- **Branch**: $(git rev-parse --abbrev-ref HEAD)
- **Ultimo commit**: $(git log -1 --oneline)
- **File modificati** ($(git status --porcelain | wc -l | tr -d ' ')):
$(git status --porcelain | head -10 | sed 's/^/  - /')

### Note
- Checkpoint automatico generato da anti-compact.sh
- Claude stava per perdere contesto
- Tutto salvato e pushato

---
EOF
    log_success "PROMPT_RIPRESA.md aggiornato!"
else
    log_warning "PROMPT_RIPRESA.md non trovato!"
fi

# Step 3: Git add + commit + push
log_info "Git: staging modifiche..."
git add -A

# Messaggio commit
if [ -n "$CUSTOM_MESSAGE" ]; then
    COMMIT_MSG="ANTI-COMPACT: ${CUSTOM_MESSAGE}"
else
    COMMIT_MSG="ANTI-COMPACT checkpoint: ${TIMESTAMP}"
fi

log_info "Git: commit..."
if git diff --cached --quiet; then
    log_warning "Nessuna modifica da committare"
else
    git commit -m "$COMMIT_MSG"
    log_success "Commit creato: ${COMMIT_MSG}"
fi

log_info "Git: push..."
if git push; then
    log_success "Push completato!"
else
    log_warning "Push fallito (verificare connessione)"
fi

# Step 4: Mostra riepilogo
echo ""
log_success "========================================="
log_success "✅ CHECKPOINT SALVATO!"
log_success "========================================="
echo ""
log_info "Branch:   $(git rev-parse --abbrev-ref HEAD)"
log_info "Commit:   $(git log -1 --oneline)"
log_info "Remote:   Pushato su origin"
echo ""
log_success "La nuova sessione puo riprendere da qui!"
echo ""

# Step 5: Spawn nuova finestra (opzionale)
if [ "$SPAWN_NEW_WINDOW" = true ]; then
    # Verifica se siamo su macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        log_info "Apertura nuova finestra Claude Code..."

        # AppleScript per aprire nuova finestra Terminal con claude
        osascript << APPLESCRIPT
        tell application "Terminal"
            do script "cd ${PROJECT_ROOT} && /Users/rafapra/.nvm/versions/node/v24.11.0/bin/claude"
            activate
        end tell
APPLESCRIPT

        log_success "Nuova finestra aperta! Continua li!"
    else
        log_warning "Apertura automatica finestra disponibile solo su macOS"
        log_info "Apri manualmente una nuova finestra e riprendi da PROMPT_RIPRESA.md"
    fi
else
    log_info "Riapri manualmente Claude Code quando pronto"
    log_info "La nuova Cervella leggera PROMPT_RIPRESA.md"
fi

echo ""
log_success "🚀 ANTI-COMPACT COMPLETATO!"
echo ""

exit 0
