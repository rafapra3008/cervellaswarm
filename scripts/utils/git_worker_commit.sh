#!/bin/bash
#
# git_worker_commit.sh - Auto-commit con Conventional Commits + Attribution
#
# CervellaSwarm 2.0 - Git Flow Integration
#
# Uso:
#   ./git_worker_commit.sh --worker backend --type feat --scope api --message "Add login endpoint"
#   ./git_worker_commit.sh --worker frontend --type fix --message "Fix button alignment"
#   ./git_worker_commit.sh --save-user-work   # Salva dirty files prima di edit Worker
#   ./git_worker_commit.sh --check-dirty      # Verifica se ci sono uncommitted changes
#   ./git_worker_commit.sh --dry-run ...      # Mostra commit senza eseguirlo
#
# Versione: 1.1.0
# Data: 2026-01-19
# Basato su: Studio Aider Git Integration (docs/studio/STUDIO_GIT_FLOW_AI_AGENTS.md)
#
# CHANGELOG:
# v1.1.0: Fix audit Guardiana Qualita (9.5 target)
#   - Single source of truth: legge attribution da JSON con jq
#   - Aggiunto --allow-hooks per eseguire pre-commit hooks
#   - Aggiunto --staged-only per committare solo staged files
#   - Aggiunto --dry-run per preview commit
#   - Validazione worker name con warning
#   - Allineato header a 50 chars (best practice)
# v1.0.0: Initial release
#
# Cervella & Rafa - CervellaSwarm 2.0

set -e

# ============================================================================
# CONFIGURAZIONE
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
ATTRIBUTION_JSON="${SCRIPT_DIR}/worker_attribution.json"

# Colori
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

# Attribution email
CERVELLASWARM_EMAIL="noreply@cervellaswarm.com"

# Flags globali
ALLOW_HOOKS=false
STAGED_ONLY=false
DRY_RUN=false

# ============================================================================
# WORKER ATTRIBUTION - SINGLE SOURCE OF TRUTH (JSON)
# ============================================================================

# Lista worker validi (per validazione)
VALID_WORKERS="backend frontend tester docs reviewer devops researcher data security scienziata ingegnera marketing guardiana-qualita guardiana-ops guardiana-ricerca regina orchestrator"

# Verifica se worker e' valido
is_valid_worker() {
    local worker_name="$1"
    echo "$VALID_WORKERS" | grep -qw "$worker_name"
}

# Legge attribution dal JSON (single source of truth)
get_worker_attribution() {
    local worker_name="$1"

    # Verifica che jq sia disponibile
    if ! command -v jq &>/dev/null; then
        # Fallback se jq non disponibile
        print_warning "jq non installato - usando fallback attribution"
        echo "worker/claude-sonnet-4-5"
        return
    fi

    # Verifica che il JSON esista
    if [ ! -f "$ATTRIBUTION_JSON" ]; then
        print_warning "Attribution JSON non trovato: $ATTRIBUTION_JSON"
        echo "worker/claude-sonnet-4-5"
        return
    fi

    local role=""
    local model=""

    # Cerca nei workers
    role=$(jq -r ".workers[\"$worker_name\"].role // empty" "$ATTRIBUTION_JSON" 2>/dev/null)
    model=$(jq -r ".workers[\"$worker_name\"].model // empty" "$ATTRIBUTION_JSON" 2>/dev/null)

    # Se non trovato, cerca nelle guardiane
    if [ -z "$role" ]; then
        role=$(jq -r ".guardiane[\"$worker_name\"].role // empty" "$ATTRIBUTION_JSON" 2>/dev/null)
        model=$(jq -r ".guardiane[\"$worker_name\"].model // empty" "$ATTRIBUTION_JSON" 2>/dev/null)
    fi

    # Se non trovato, cerca negli special
    if [ -z "$role" ]; then
        role=$(jq -r ".special[\"$worker_name\"].role // empty" "$ATTRIBUTION_JSON" 2>/dev/null)
        model=$(jq -r ".special[\"$worker_name\"].model // empty" "$ATTRIBUTION_JSON" 2>/dev/null)
    fi

    # Se ancora non trovato, usa default
    if [ -z "$role" ] || [ -z "$model" ]; then
        echo "worker/claude-sonnet-4-5"
    else
        echo "${role}/${model}"
    fi
}

# ============================================================================
# SCOPE AUTO-DETECTION
# ============================================================================

# Detecta scope automaticamente dai file modificati
auto_detect_scope() {
    local changed_files

    if [ "$STAGED_ONLY" = true ]; then
        changed_files=$(git diff --cached --name-only 2>/dev/null)
    else
        changed_files=$(git diff --cached --name-only 2>/dev/null || git diff --name-only 2>/dev/null)
    fi

    if [ -z "$changed_files" ]; then
        echo ""
        return
    fi

    # Conta file per directory
    local cli_count=0
    local mcp_count=0
    local docs_count=0
    local scripts_count=0
    local api_count=0
    local ui_count=0
    local test_count=0
    local hooks_count=0

    while IFS= read -r file; do
        case "$file" in
            packages/cli/*) cli_count=$((cli_count + 1)) ;;
            packages/mcp-server/*) mcp_count=$((mcp_count + 1)) ;;
            docs/*) docs_count=$((docs_count + 1)) ;;
            scripts/*) scripts_count=$((scripts_count + 1)) ;;
            *api*|*endpoint*|*route*) api_count=$((api_count + 1)) ;;
            *component*|*.tsx|*.jsx|*.css) ui_count=$((ui_count + 1)) ;;
            *test*|*spec*) test_count=$((test_count + 1)) ;;
            .claude/*|hooks/*) hooks_count=$((hooks_count + 1)) ;;
        esac
    done <<< "$changed_files"

    # Trova il maggiore
    local max=$cli_count
    local scope="cli"

    if [ $mcp_count -gt $max ]; then max=$mcp_count; scope="mcp"; fi
    if [ $docs_count -gt $max ]; then max=$docs_count; scope="docs"; fi
    if [ $scripts_count -gt $max ]; then max=$scripts_count; scope="scripts"; fi
    if [ $api_count -gt $max ]; then max=$api_count; scope="api"; fi
    if [ $ui_count -gt $max ]; then max=$ui_count; scope="ui"; fi
    if [ $test_count -gt $max ]; then max=$test_count; scope="test"; fi
    if [ $hooks_count -gt $max ]; then max=$hooks_count; scope="hooks"; fi

    if [ $max -eq 0 ]; then
        echo ""
    else
        echo "$scope"
    fi
}

# ============================================================================
# COMMIT TYPE VALIDATION
# ============================================================================

# Valida che il tipo sia un Conventional Commit valido
validate_commit_type() {
    local type="$1"

    case "$type" in
        feat|fix|docs|style|refactor|test|chore|perf|ci|build)
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

# ============================================================================
# FUNZIONI PRINCIPALI
# ============================================================================

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

# Verifica se ci sono uncommitted changes
check_dirty() {
    if ! git diff --quiet 2>/dev/null || ! git diff --cached --quiet 2>/dev/null; then
        return 0  # Dirty
    else
        return 1  # Clean
    fi
}

# Salva lavoro utente prima di edit Worker
save_user_work() {
    if check_dirty; then
        print_info "Salvando lavoro utente prima di edit Worker..."

        git add -A
        git commit -m "chore: Save user work before CervellaSwarm edit

This commit saves uncommitted changes before a CervellaSwarm worker modifies files.

Co-authored-by: CervellaSwarm (auto-save) <${CERVELLASWARM_EMAIL}>"

        print_success "Lavoro utente salvato!"
        return 0
    else
        print_info "Nessun file dirty da salvare."
        return 0
    fi
}

# Commit principale con attribution
do_commit() {
    local worker_name="$1"
    local commit_type="$2"
    local scope="$3"
    local message="$4"
    local body="$5"

    # Validazione worker name
    if [ -z "$worker_name" ]; then
        print_error "Worker name richiesto! Usa --worker <name>"
        exit 1
    fi

    # Validazione worker name (warning se sconosciuto)
    if ! is_valid_worker "$worker_name"; then
        print_warning "Worker '$worker_name' non riconosciuto - usando attribution generica"
        print_info "Worker validi: $VALID_WORKERS"
    fi

    if [ -z "$commit_type" ]; then
        print_error "Commit type richiesto! Usa --type <feat|fix|docs|...>"
        exit 1
    fi

    if ! validate_commit_type "$commit_type"; then
        print_error "Tipo commit invalido: $commit_type"
        print_info "Tipi validi: feat, fix, docs, style, refactor, test, chore, perf, ci, build"
        exit 1
    fi

    if [ -z "$message" ]; then
        print_error "Message richiesto! Usa --message \"descrizione\""
        exit 1
    fi

    # Auto-detect scope se non fornito
    if [ -z "$scope" ]; then
        scope=$(auto_detect_scope)
    fi

    # Costruisci header commit
    local commit_header
    if [ -n "$scope" ]; then
        commit_header="${commit_type}(${scope}): ${message}"
    else
        commit_header="${commit_type}: ${message}"
    fi

    # Verifica lunghezza header (max 50 chars - best practice)
    if [ ${#commit_header} -gt 50 ]; then
        print_warning "Header commit troppo lungo (${#commit_header} chars, max 50)"
        print_warning "Troncando..."
        commit_header="${commit_header:0:47}..."
    fi

    # Attribution (legge da JSON - single source of truth)
    local attribution
    attribution=$(get_worker_attribution "$worker_name")

    # Costruisci messaggio completo
    local full_message="${commit_header}"

    if [ -n "$body" ]; then
        full_message="${full_message}

${body}"
    fi

    full_message="${full_message}

Co-authored-by: CervellaSwarm (${attribution}) <${CERVELLASWARM_EMAIL}>"

    # DRY RUN - mostra senza eseguire
    if [ "$DRY_RUN" = true ]; then
        echo ""
        echo -e "${PURPLE}=== DRY RUN - Commit Preview ===${NC}"
        echo ""
        echo -e "${BLUE}Files da committare:${NC}"
        if [ "$STAGED_ONLY" = true ]; then
            git diff --cached --name-only
        else
            git status --short
        fi
        echo ""
        echo -e "${PURPLE}--- Commit Message ---${NC}"
        echo "$full_message"
        echo -e "${PURPLE}----------------------${NC}"
        echo ""
        echo -e "${YELLOW}Hooks: $([ "$ALLOW_HOOKS" = true ] && echo "ABILITATI" || echo "DISABILITATI")${NC}"
        echo -e "${YELLOW}Staged only: $([ "$STAGED_ONLY" = true ] && echo "SI" || echo "NO (add -A)")${NC}"
        echo ""
        print_info "Usa senza --dry-run per eseguire il commit"
        return 0
    fi

    # Stage changes
    if [ "$STAGED_ONLY" = false ]; then
        git add -A
    fi

    # Verifica che ci sia qualcosa da committare
    if git diff --cached --quiet; then
        print_warning "Nessuna modifica da committare."
        return 0
    fi

    # Commit
    local commit_flags=""
    if [ "$ALLOW_HOOKS" = false ]; then
        commit_flags="--no-verify"
    fi

    git commit $commit_flags -m "$full_message"

    print_success "Commit creato!"
    echo ""
    echo -e "${PURPLE}--- Commit Message ---${NC}"
    echo "$full_message"
    echo -e "${PURPLE}----------------------${NC}"
    echo ""

    return 0
}

# Verifica se ultimo commit e' di CervellaSwarm (per /undo safety)
is_last_commit_cervellaswarm() {
    local last_commit_msg
    last_commit_msg=$(git log -1 --pretty=%B 2>/dev/null)

    if echo "$last_commit_msg" | grep -q "CervellaSwarm"; then
        return 0  # E' un commit CervellaSwarm
    else
        return 1  # Non e' un commit CervellaSwarm
    fi
}

# Undo ultimo commit (solo se CervellaSwarm)
undo_last_commit() {
    if ! is_last_commit_cervellaswarm; then
        print_error "L'ultimo commit NON e' di CervellaSwarm!"
        print_error "Per sicurezza, /undo funziona solo su commit CervellaSwarm."
        echo ""
        print_info "Ultimo commit:"
        git log -1 --oneline
        exit 1
    fi

    local last_commit
    last_commit=$(git log -1 --oneline)

    print_warning "Stai per annullare: $last_commit"
    echo ""

    # Esegui undo
    git reset --hard HEAD^

    print_success "Commit annullato!"
    print_info "Stato attuale:"
    git status --short
}

# ============================================================================
# HELP
# ============================================================================

show_usage() {
    echo "git_worker_commit.sh - CervellaSwarm 2.0 Git Flow"
    echo ""
    echo "Uso:"
    echo "  $0 --worker <name> --type <type> [--scope <scope>] --message \"msg\" [opzioni]"
    echo "  $0 --save-user-work"
    echo "  $0 --check-dirty"
    echo "  $0 --undo"
    echo ""
    echo "Opzioni commit:"
    echo "  --worker <name>     Nome worker (backend, frontend, tester, ...)"
    echo "  --type <type>       Tipo commit (feat, fix, docs, refactor, chore, test, ...)"
    echo "  --scope <scope>     Scope opzionale (cli, mcp, api, ui, ...) - auto-detected se omesso"
    echo "  --message \"msg\"     Descrizione breve del commit (max 50 chars)"
    echo "  --body \"body\"       Corpo opzionale con dettagli"
    echo ""
    echo "Opzioni avanzate:"
    echo "  --dry-run           Mostra preview commit senza eseguirlo"
    echo "  --staged-only       Committa solo file staged (non fa git add -A)"
    echo "  --allow-hooks       Esegue pre-commit hooks (default: skippati)"
    echo ""
    echo "Altre opzioni:"
    echo "  --save-user-work    Salva dirty files prima di edit Worker"
    echo "  --check-dirty       Verifica se ci sono uncommitted changes"
    echo "  --undo              Annulla ultimo commit (solo se CervellaSwarm)"
    echo "  --help              Mostra questo help"
    echo ""
    echo "Worker validi:"
    echo "  $VALID_WORKERS"
    echo ""
    echo "Esempi:"
    echo "  $0 --worker backend --type feat --scope api --message \"Add login\""
    echo "  $0 --worker frontend --type fix --message \"Fix button\" --dry-run"
    echo "  $0 --worker tester --type test --staged-only --allow-hooks"
    echo "  $0 --save-user-work"
    echo "  $0 --undo"
    echo ""
    echo "Tipi Conventional Commits:"
    echo "  feat     Nuova feature"
    echo "  fix      Bug fix"
    echo "  docs     Documentazione"
    echo "  style    Formatting (no logic change)"
    echo "  refactor Ristrutturazione (no behavior change)"
    echo "  test     Aggiunta/modifica test"
    echo "  chore    Manutenzione"
    echo "  perf     Performance"
    echo "  ci       CI/CD"
    echo "  build    Build system"
    echo ""
}

# ============================================================================
# MAIN
# ============================================================================

main() {
    # Se nessun argomento, mostra help
    if [ $# -eq 0 ]; then
        show_usage
        exit 0
    fi

    # Verifica che siamo in un repo git
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_error "Non sei in un repository Git!"
        exit 1
    fi

    # Parse argomenti
    local worker_name=""
    local commit_type=""
    local scope=""
    local message=""
    local body=""

    while [ $# -gt 0 ]; do
        case "$1" in
            --worker)
                shift
                worker_name="$1"
                ;;
            --type)
                shift
                commit_type="$1"
                ;;
            --scope)
                shift
                scope="$1"
                ;;
            --message|-m)
                shift
                message="$1"
                ;;
            --body)
                shift
                body="$1"
                ;;
            --dry-run)
                DRY_RUN=true
                ;;
            --staged-only)
                STAGED_ONLY=true
                ;;
            --allow-hooks)
                ALLOW_HOOKS=true
                ;;
            --save-user-work)
                save_user_work
                exit $?
                ;;
            --check-dirty)
                if check_dirty; then
                    print_warning "Ci sono uncommitted changes!"
                    git status --short
                    exit 1
                else
                    print_success "Working directory pulita."
                    exit 0
                fi
                ;;
            --undo)
                undo_last_commit
                exit $?
                ;;
            --help|-h)
                show_usage
                exit 0
                ;;
            *)
                print_error "Opzione sconosciuta: $1"
                show_usage
                exit 1
                ;;
        esac
        shift
    done

    # Se abbiamo argomenti per commit, esegui commit
    if [ -n "$worker_name" ] || [ -n "$commit_type" ] || [ -n "$message" ]; then
        do_commit "$worker_name" "$commit_type" "$scope" "$message" "$body"
    fi
}

# Esegui
main "$@"
