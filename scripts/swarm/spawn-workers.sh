#!/bin/bash
#
# spawn-workers.sh - LA MAGIA! Apre finestre worker automaticamente
#
# CervellaSwarm Multi-Finestra - Apertura automatica worker
#
# Uso:
#   ./spawn-workers.sh --backend              # Solo backend
#   ./spawn-workers.sh --frontend             # Solo frontend
#   ./spawn-workers.sh --backend --frontend   # Backend + Frontend
#   ./spawn-workers.sh --tester               # Solo tester
#   ./spawn-workers.sh --all                  # Tutti i worker comuni
#   ./spawn-workers.sh --list                 # Lista worker disponibili
#
# Versione: 1.4.0
# Data: 2026-01-04
# Apple Style: Auto-close, Graceful shutdown, Notifiche macOS
# v1.4.0: Fix notifica + exit (notifica PRIMA di exit!)
# Cervella & Rafa
# Aggiunto: Supporto Guardiane (Opus)

set -e

# ============================================================================
# CONFIGURAZIONE
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
SWARM_DIR="${PROJECT_ROOT}/.swarm"

# Colori
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Lista worker comuni (per --all)
COMMON_WORKERS="backend frontend tester"

# Lista tutti i worker disponibili
ALL_WORKERS="backend frontend tester docs reviewer devops researcher data security"

# Lista Guardiane (Opus - supervisione)
ALL_GUARDIANS="guardiana-qualita guardiana-ops guardiana-ricerca"

# ============================================================================
# PROMPT WORKER
# ============================================================================

# Prompt base per tutti i worker
get_base_prompt() {
    cat << 'BASEEOF'
MODALITA WORKER CERVELLASWARM

Tu sei un WORKER dello sciame CervellaSwarm.
NON sei la Regina - sei un agente specializzato.

REGOLE WORKER:
1. Controlla .swarm/tasks/ per task assegnati a te
2. Prendi SOLO task con stato .ready
3. Quando prendi un task, crea file .working
4. Quando finisci, crea file .done e scrivi output in _output.md
5. NON modificare file fuori dal tuo scope
6. Se hai dubbi, scrivi in .swarm/handoff/ per la Regina

COMANDI UTILI:
- python3 scripts/swarm/task_manager.py list
- python3 scripts/swarm/task_manager.py working TASK_ID
- python3 scripts/swarm/task_manager.py done TASK_ID

APPLE STYLE - FINITURE:

DOPO OGNI TASK COMPLETATO:
1. Invia notifica macOS con questo comando Bash:
   osascript -e 'display notification "Task completato!" with title "CervellaSwarm" sound name "Glass"'

QUANDO NON CI SONO PIU TASK PER TE:
1. Controlla ancora una volta .swarm/tasks/ per task .ready
2. Se non ci sono task per te, esegui questo comando (notifica + exit insieme):
   osascript -e 'display notification "Nessun task, chiudo!" with title "CervellaSwarm" sound name "Glass"' && exit

IMPORTANTE: La notifica DEVE venire PRIMA di exit!
Se fai exit prima, non puoi piu notificare!
BASEEOF
}

# Prompt specifico per worker
get_worker_prompt() {
    local worker_name="$1"
    local base_prompt
    base_prompt=$(get_base_prompt)

    case "$worker_name" in
        backend)
            echo "Sei CERVELLA-BACKEND.
Specializzazione: Python, FastAPI, Database, API REST, logica business.

${base_prompt}

FOCUS: Cerca task per 'cervella-backend' in .swarm/tasks/"
            ;;
        frontend)
            echo "Sei CERVELLA-FRONTEND.
Specializzazione: React, CSS, Tailwind, UI/UX, componenti.

${base_prompt}

FOCUS: Cerca task per 'cervella-frontend' in .swarm/tasks/"
            ;;
        tester)
            echo "Sei CERVELLA-TESTER.
Specializzazione: Testing, Debug, QA, validazione.

${base_prompt}

FOCUS: Cerca task per 'cervella-tester' in .swarm/tasks/"
            ;;
        docs)
            echo "Sei CERVELLA-DOCS.
Specializzazione: Documentazione, README, guide, tutorial.

${base_prompt}

FOCUS: Cerca task per 'cervella-docs' in .swarm/tasks/"
            ;;
        reviewer)
            echo "Sei CERVELLA-REVIEWER.
Specializzazione: Code review, best practices, architettura.

${base_prompt}

FOCUS: Cerca task per 'cervella-reviewer' in .swarm/tasks/"
            ;;
        devops)
            echo "Sei CERVELLA-DEVOPS.
Specializzazione: Deploy, CI/CD, Docker, infrastruttura.

${base_prompt}

FOCUS: Cerca task per 'cervella-devops' in .swarm/tasks/"
            ;;
        researcher)
            echo "Sei CERVELLA-RESEARCHER.
Specializzazione: Ricerca tecnica, studi, analisi.

${base_prompt}

FOCUS: Cerca task per 'cervella-researcher' in .swarm/tasks/"
            ;;
        data)
            echo "Sei CERVELLA-DATA.
Specializzazione: SQL, analytics, query, database design.

${base_prompt}

FOCUS: Cerca task per 'cervella-data' in .swarm/tasks/"
            ;;
        security)
            echo "Sei CERVELLA-SECURITY.
Specializzazione: Sicurezza, audit, vulnerabilita.

${base_prompt}

FOCUS: Cerca task per 'cervella-security' in .swarm/tasks/"
            ;;
        guardiana-qualita)
            echo "Sei CERVELLA-GUARDIANA-QUALITA (Opus).
Ruolo: Verifica qualita output agenti, standard codice, test, file size.
LIVELLO INTERMEDIO tra Regina e Api.

${base_prompt}

FOCUS SPECIALE GUARDIANA:
- Verifica che l'output risponda al PERCHE originale
- Controlla qualita codice (naming, struttura, best practices)
- Valida che i test passino e siano significativi
- APPROVA o RIFIUTA con motivazione chiara

Cerca task con .review_ready in .swarm/tasks/"
            ;;
        guardiana-ops)
            echo "Sei CERVELLA-GUARDIANA-OPS (Opus).
Ruolo: Supervisiona devops, security, data. Verifica sicurezza, performance, best practices.

${base_prompt}

FOCUS SPECIALE GUARDIANA:
- Verifica sicurezza (no secrets, no injection, no vulnerabilita)
- Controlla performance e scalabilita
- Valida configurazioni infrastruttura
- APPROVA o BLOCCA operazioni critiche

Cerca task con .review_ready in .swarm/tasks/"
            ;;
        guardiana-ricerca)
            echo "Sei CERVELLA-GUARDIANA-RICERCA (Opus).
Ruolo: Verifica qualita e affidabilita delle ricerche dello sciame.

${base_prompt}

FOCUS SPECIALE GUARDIANA:
- Verifica che le ricerche siano complete e accurate
- Controlla fonti e affidabilita
- Valida che rispondano al PERCHE originale
- Suggerisci approfondimenti se necessario

Cerca task con .review_ready in .swarm/tasks/"
            ;;
        *)
            echo ""
            return 1
            ;;
    esac
}

# ============================================================================
# FUNZIONI
# ============================================================================

print_header() {
    echo -e "${PURPLE}"
    echo "=============================================="
    echo "  SPAWN-WORKERS.SH - LA MAGIA!"
    echo "  CervellaSwarm Multi-Finestra"
    echo "=============================================="
    echo -e "${NC}"
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

list_workers() {
    echo -e "${BLUE}Worker disponibili:${NC}"
    echo ""
    for worker in $ALL_WORKERS; do
        echo "  --${worker}"
    done
    echo ""
    echo "  --all    (spawna: ${COMMON_WORKERS})"
    echo ""
    echo -e "${PURPLE}Guardiane (Opus):${NC}"
    for guardian in $ALL_GUARDIANS; do
        echo "  --${guardian}"
    done
    echo ""
    echo "  --guardiane    (spawna tutte le guardiane)"
    echo ""
}

spawn_worker() {
    local worker_name="$1"
    local prompt
    prompt=$(get_worker_prompt "$worker_name")

    if [ -z "$prompt" ]; then
        print_error "Worker '$worker_name' non trovato!"
        return 1
    fi

    print_info "Spawning cervella-${worker_name}..."

    # Salva prompt in file
    local prompt_file="${SWARM_DIR}/prompts/worker_${worker_name}.txt"
    mkdir -p "${SWARM_DIR}/prompts"
    printf '%s' "$prompt" > "$prompt_file"

    # Crea runner script
    local runner_script="${SWARM_DIR}/runners/run_${worker_name}.sh"
    mkdir -p "${SWARM_DIR}/runners"

    cat > "$runner_script" << 'RUNNEREOF'
#!/bin/bash
RUNNEREOF
    echo "cd ${PROJECT_ROOT}" >> "$runner_script"
    # Prompt iniziale che fa partire il worker automaticamente
    local initial_prompt="Controlla .swarm/tasks/ per task assegnati a te e inizia a lavorare. Se non ci sono task, aspetta istruzioni."
    echo "/Users/rafapra/.nvm/versions/node/v24.11.0/bin/claude --append-system-prompt \"\$(cat ${prompt_file})\" \"${initial_prompt}\"" >> "$runner_script"
    chmod +x "$runner_script"

    # Apre nuova finestra Terminal eseguendo lo script runner
    osascript -e "tell application \"Terminal\" to do script \"${runner_script}\""
    osascript -e "tell application \"Terminal\" to activate"

    if [ $? -eq 0 ]; then
        print_success "cervella-${worker_name} spawned!"
        mkdir -p "${SWARM_DIR}/logs"
        echo "$(date '+%Y-%m-%d %H:%M:%S') - SPAWNED: cervella-${worker_name}" >> "${SWARM_DIR}/logs/spawn.log"
        return 0
    else
        print_error "Errore spawn cervella-${worker_name}"
        return 1
    fi
}

show_usage() {
    echo "Uso: $0 [opzioni]"
    echo ""
    echo "Opzioni:"
    echo "  --backend              Spawna cervella-backend"
    echo "  --frontend             Spawna cervella-frontend"
    echo "  --tester               Spawna cervella-tester"
    echo "  --docs                 Spawna cervella-docs"
    echo "  --reviewer             Spawna cervella-reviewer"
    echo "  --devops               Spawna cervella-devops"
    echo "  --researcher           Spawna cervella-researcher"
    echo "  --data                 Spawna cervella-data"
    echo "  --security             Spawna cervella-security"
    echo "  --guardiana-qualita    Spawna cervella-guardiana-qualita (Opus)"
    echo "  --guardiana-ops        Spawna cervella-guardiana-ops (Opus)"
    echo "  --guardiana-ricerca    Spawna cervella-guardiana-ricerca (Opus)"
    echo "  --all                  Spawna worker comuni (backend, frontend, tester)"
    echo "  --guardiane            Spawna tutte le guardiane"
    echo "  --list                 Lista worker disponibili"
    echo "  --help                 Mostra questo help"
    echo ""
    echo "Esempi:"
    echo "  $0 --backend --frontend    # Spawna backend e frontend"
    echo "  $0 --all                   # Spawna tutti i worker comuni"
    echo "  $0 --guardiane             # Spawna tutte le guardiane (Opus)"
    echo ""
}

# ============================================================================
# MAIN
# ============================================================================

main() {
    print_header

    # Verifica .swarm/ esiste
    if [ ! -d "${SWARM_DIR}" ]; then
        print_warning ".swarm/ non trovato. Creo struttura..."
        mkdir -p "${SWARM_DIR}/tasks"
        mkdir -p "${SWARM_DIR}/status"
        mkdir -p "${SWARM_DIR}/logs"
        mkdir -p "${SWARM_DIR}/handoff"
        print_success "Struttura .swarm/ creata!"
    fi

    # Parse argomenti
    if [ $# -eq 0 ]; then
        show_usage
        exit 0
    fi

    workers_to_spawn=""

    while [ $# -gt 0 ]; do
        case "$1" in
            --backend)
                workers_to_spawn="${workers_to_spawn} backend"
                ;;
            --frontend)
                workers_to_spawn="${workers_to_spawn} frontend"
                ;;
            --tester)
                workers_to_spawn="${workers_to_spawn} tester"
                ;;
            --docs)
                workers_to_spawn="${workers_to_spawn} docs"
                ;;
            --reviewer)
                workers_to_spawn="${workers_to_spawn} reviewer"
                ;;
            --devops)
                workers_to_spawn="${workers_to_spawn} devops"
                ;;
            --researcher)
                workers_to_spawn="${workers_to_spawn} researcher"
                ;;
            --data)
                workers_to_spawn="${workers_to_spawn} data"
                ;;
            --security)
                workers_to_spawn="${workers_to_spawn} security"
                ;;
            --guardiana-qualita)
                workers_to_spawn="${workers_to_spawn} guardiana-qualita"
                ;;
            --guardiana-ops)
                workers_to_spawn="${workers_to_spawn} guardiana-ops"
                ;;
            --guardiana-ricerca)
                workers_to_spawn="${workers_to_spawn} guardiana-ricerca"
                ;;
            --all)
                workers_to_spawn="${workers_to_spawn} ${COMMON_WORKERS}"
                ;;
            --guardiane)
                workers_to_spawn="${workers_to_spawn} ${ALL_GUARDIANS}"
                ;;
            --list)
                list_workers
                exit 0
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

    # Trim e verifica
    workers_to_spawn=$(echo "$workers_to_spawn" | xargs)

    if [ -z "$workers_to_spawn" ]; then
        print_warning "Nessun worker specificato!"
        show_usage
        exit 1
    fi

    # Conta worker
    worker_count=$(echo "$workers_to_spawn" | wc -w | xargs)

    echo ""
    print_info "Spawning ${worker_count} worker(s)..."
    echo ""

    spawned=0
    failed=0

    for worker in $workers_to_spawn; do
        if spawn_worker "$worker"; then
            spawned=$((spawned + 1))
        else
            failed=$((failed + 1))
        fi
        # Piccola pausa tra spawn per evitare race condition
        sleep 0.5
    done

    echo ""
    echo "=============================================="
    print_success "Spawned: ${spawned} worker(s)"
    if [ $failed -gt 0 ]; then
        print_error "Failed: ${failed} worker(s)"
    fi
    echo "=============================================="
    echo ""
    print_info "Le finestre Terminal sono aperte!"
    print_info "I worker stanno cercando task in .swarm/tasks/"
    echo ""
}

# Esegui
main "$@"
