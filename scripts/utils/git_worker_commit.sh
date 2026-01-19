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
# Versione: 1.2.2
# Data: 2026-01-19
# Basato su: Studio Aider Git Integration (docs/studio/STUDIO_GIT_FLOW_AI_AGENTS.md)
#
# CHANGELOG:
# v1.2.2: Day 2 Audit Completo - Sessione 272
#   - FIX CRITICO: undo --hard → --soft (preserva modifiche staged!)
#   - FIX: orchestrator aggiunto a worker_attribution.json (16/16)
# v1.2.1: Day 2 Fix - Audit Guardiana 9.5+ (Sessione 272)
#   - FIX: doppio fallback || → check esplicito stringa vuota
#   - FIX: concatenazione newline → printf leggibile
#   - FIX: grep -c . → logica semplificata (no count needed)
#   - NUOVO: pattern src/* per scope detection (13 patterns totali)
#   - DOCS: scope patterns documentati in --help
# v1.2.0: Day 2 - Type & Scope Auto-Detection (Sessione 272)
#   - NUOVO: auto_detect_type() - suggerisce tipo commit dai file
#   - NUOVO: --auto flag per auto-detect completo
#   - MIGLIORATO: scope detection con 12 patterns (+4 nuovi: sncp, reports, config, db)
#   - Pattern migliorati per: docs, scripts, api, ui, test
#   - Info feedback quando tipo/scope auto-detectati
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
AUTO_DETECT=false

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
# TYPE AUTO-DETECTION (Day 2 Feature)
# ============================================================================

# Detecta tipo commit automaticamente dai file modificati
auto_detect_type() {
    local changed_files
    local new_files
    local modified_files

    if [ "$STAGED_ONLY" = true ]; then
        changed_files=$(git diff --cached --name-only 2>/dev/null)
        new_files=$(git diff --cached --name-only --diff-filter=A 2>/dev/null)
        modified_files=$(git diff --cached --name-only --diff-filter=M 2>/dev/null)
    else
        # Fix: check empty string, not exit code (git returns 0 even with empty output)
        changed_files=$(git diff --cached --name-only 2>/dev/null)
        if [ -z "$changed_files" ]; then
            changed_files=$(git diff --name-only 2>/dev/null)
        fi
        new_files=$(git status --porcelain | grep "^??" | cut -c4-)
        modified_files=$(git status --porcelain | grep "^ M\|^M " | cut -c4-)
    fi

    if [ -z "$changed_files" ] && [ -z "$new_files" ]; then
        echo "chore"
        return
    fi

    # Conta pattern per tipo
    local docs_count=0
    local test_count=0
    local feat_count=0
    local config_count=0
    local style_count=0

    # Analizza file modificati/nuovi (Fix: readable concatenation)
    local all_files
    all_files=$(printf '%s\n%s' "$changed_files" "$new_files")

    while IFS= read -r file; do
        [ -z "$file" ] && continue
        case "$file" in
            # Documentazione
            *.md|docs/*|*.txt|*.rst) docs_count=$((docs_count + 1)) ;;
            # Test
            *test*|*spec*|__tests__/*|tests/*) test_count=$((test_count + 1)) ;;
            # Config/Chore
            package.json|tsconfig.json|*.config.js|*.config.ts|.eslintrc*|.prettierrc*|Makefile|Dockerfile)
                config_count=$((config_count + 1)) ;;
            # Style (CSS, formatting)
            *.css|*.scss|*.sass|*.less) style_count=$((style_count + 1)) ;;
            # Codice (potenziale feature)
            *.ts|*.tsx|*.js|*.jsx|*.py|*.sh|*.go|*.rs)
                feat_count=$((feat_count + 1)) ;;
        esac
    done <<< "$all_files"

    # Logica decisionale
    local total=$((docs_count + test_count + feat_count + config_count + style_count))

    # Se SOLO docs → docs
    if [ $docs_count -gt 0 ] && [ $docs_count -eq $total ]; then
        echo "docs"
        return
    fi

    # Se SOLO test → test
    if [ $test_count -gt 0 ] && [ $test_count -eq $total ]; then
        echo "test"
        return
    fi

    # Se SOLO style → style
    if [ $style_count -gt 0 ] && [ $style_count -eq $total ]; then
        echo "style"
        return
    fi

    # Se SOLO config → chore
    if [ $config_count -gt 0 ] && [ $config_count -eq $total ]; then
        echo "chore"
        return
    fi

    # Se ci sono file nuovi → feat (nuova feature)
    # Fix: simplified logic - if new_files is non-empty, there are new files
    if [ -n "$new_files" ]; then
        echo "feat"
        return
    fi

    # Default: feat per codice, chore per altro
    if [ $feat_count -gt 0 ]; then
        echo "feat"
    else
        echo "chore"
    fi
}

# ============================================================================
# SCOPE AUTO-DETECTION (Day 2 Enhanced)
# ============================================================================

# Detecta scope automaticamente dai file modificati
auto_detect_scope() {
    local changed_files
    local untracked_files

    if [ "$STAGED_ONLY" = true ]; then
        changed_files=$(git diff --cached --name-only 2>/dev/null)
    else
        # Include sia file staged/modified che untracked
        changed_files=$(git diff --cached --name-only 2>/dev/null)
        [ -z "$changed_files" ] && changed_files=$(git diff --name-only 2>/dev/null)
        untracked_files=$(git status --porcelain | grep "^??" | cut -c4-)
        if [ -n "$untracked_files" ]; then
            changed_files="${changed_files}
${untracked_files}"
        fi
    fi

    if [ -z "$changed_files" ]; then
        echo ""
        return
    fi

    # Conta file per directory (Day 2 Enhanced - more patterns)
    local cli_count=0
    local mcp_count=0
    local docs_count=0
    local scripts_count=0
    local api_count=0
    local ui_count=0
    local test_count=0
    local hooks_count=0
    local src_count=0
    local sncp_count=0
    local reports_count=0
    local config_count=0
    local db_count=0

    while IFS= read -r file; do
        [ -z "$file" ] && continue
        case "$file" in
            # CervellaSwarm specific
            packages/cli/*) cli_count=$((cli_count + 1)) ;;
            packages/mcp-server/*) mcp_count=$((mcp_count + 1)) ;;
            # Common src directory (many projects use this)
            src/*) src_count=$((src_count + 1)) ;;
            # SNCP (memoria esterna)
            .sncp/*) sncp_count=$((sncp_count + 1)) ;;
            # Reports
            reports/*) reports_count=$((reports_count + 1)) ;;
            # Documentation
            docs/*|*.md) docs_count=$((docs_count + 1)) ;;
            # Scripts
            scripts/*|*.sh) scripts_count=$((scripts_count + 1)) ;;
            # API/Backend
            *api*|*endpoint*|*route*|*handler*|*controller*) api_count=$((api_count + 1)) ;;
            # UI/Frontend
            *component*|*.tsx|*.jsx|*.css|*.scss|*page*|*view*) ui_count=$((ui_count + 1)) ;;
            # Test
            *test*|*spec*|__tests__/*|tests/*) test_count=$((test_count + 1)) ;;
            # Hooks/Config Claude
            .claude/*|hooks/*) hooks_count=$((hooks_count + 1)) ;;
            # Config files
            package.json|tsconfig.json|*.config.*|.eslintrc*|.prettierrc*|Makefile|Dockerfile)
                config_count=$((config_count + 1)) ;;
            # Database
            *migration*|*schema*|*.sql|*model*) db_count=$((db_count + 1)) ;;
        esac
    done <<< "$changed_files"

    # Trova il maggiore (Day 2 Enhanced - priority order)
    local max=0
    local scope=""

    # Priority: specific > generic
    if [ $cli_count -gt $max ]; then max=$cli_count; scope="cli"; fi
    if [ $mcp_count -gt $max ]; then max=$mcp_count; scope="mcp"; fi
    if [ $src_count -gt $max ]; then max=$src_count; scope="src"; fi
    if [ $sncp_count -gt $max ]; then max=$sncp_count; scope="sncp"; fi
    if [ $reports_count -gt $max ]; then max=$reports_count; scope="reports"; fi
    if [ $api_count -gt $max ]; then max=$api_count; scope="api"; fi
    if [ $ui_count -gt $max ]; then max=$ui_count; scope="ui"; fi
    if [ $db_count -gt $max ]; then max=$db_count; scope="db"; fi
    if [ $test_count -gt $max ]; then max=$test_count; scope="test"; fi
    if [ $scripts_count -gt $max ]; then max=$scripts_count; scope="scripts"; fi
    if [ $hooks_count -gt $max ]; then max=$hooks_count; scope="hooks"; fi
    if [ $config_count -gt $max ]; then max=$config_count; scope="config"; fi
    if [ $docs_count -gt $max ]; then max=$docs_count; scope="docs"; fi

    echo "$scope"
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

    # Auto-detect type se non fornito o se --auto attivo
    if [ -z "$commit_type" ] || [ "$AUTO_DETECT" = true ]; then
        local detected_type
        detected_type=$(auto_detect_type)
        if [ -z "$commit_type" ]; then
            commit_type="$detected_type"
            print_info "Tipo auto-detectato: $commit_type"
        elif [ "$AUTO_DETECT" = true ] && [ "$commit_type" != "$detected_type" ]; then
            print_info "Tipo fornito: $commit_type (suggerito: $detected_type)"
        fi
    fi

    if [ -z "$commit_type" ]; then
        print_error "Commit type richiesto! Usa --type <feat|fix|docs|...> o --auto"
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
        if [ -n "$scope" ]; then
            print_info "Scope auto-detectato: $scope"
        fi
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

    # Esegui undo (--soft preserva le modifiche staged, come da spec)
    git reset --soft HEAD^

    print_success "Commit annullato!"
    print_info "Le modifiche sono ora staged (pronte per nuovo commit):"
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
    echo "  --auto              Auto-detect tipo e scope dai file (Day 2 feature)"
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
    echo "  $0 --worker backend --auto --message \"Update feature\" --dry-run  # auto-detect tipo+scope"
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
    echo "Scope Auto-Detection (priority order, most files wins):"
    echo "  cli      packages/cli/*"
    echo "  mcp      packages/mcp-server/*"
    echo "  src      src/*"
    echo "  sncp     .sncp/*"
    echo "  reports  reports/*"
    echo "  api      *api*, *endpoint*, *route*, *handler*, *controller*"
    echo "  ui       *component*, *.tsx, *.jsx, *.css, *page*, *view*"
    echo "  db       *migration*, *schema*, *.sql, *model*"
    echo "  test     *test*, *spec*, __tests__/*, tests/*"
    echo "  scripts  scripts/*, *.sh"
    echo "  hooks    .claude/*, hooks/*"
    echo "  config   package.json, tsconfig.json, *.config.*, Dockerfile"
    echo "  docs     docs/*, *.md"
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
            --auto)
                AUTO_DETECT=true
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
