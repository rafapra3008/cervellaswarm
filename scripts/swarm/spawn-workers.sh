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
# Versione: 2.0.0
# Data: 2026-01-05
# Apple Style: Auto-close, Graceful shutdown, Notifiche macOS
# v2.0.0: Config centralizzata ~/.swarm/config
#
# CHANGELOG:
# v1.4.0: Fix notifica + exit
# v1.5.0: Auto-close finestra Terminal tramite TTY
# v1.6.0: Background close = no conferma macOS
# v1.7.0: Fix virgolette + auto-exit se no task
# v1.8.0: FIX ELEGANTE! -p mode = uscita automatica dopo task!
#         HARDTEST PASSATI: singolo, guardiana, 3x parallelo!
# v1.9.0: PROJECT-AWARE! Funziona da qualsiasi progetto con .swarm/
#         Symlink globale in ~/.local/bin/spawn-workers
# Cervella & Rafa
# Aggiunto: Supporto Guardiane (Opus)

set -e

# ============================================================================
# CONFIGURAZIONE CENTRALIZZATA (v2.0.0)
# ============================================================================

# Carica configurazione globale se esiste
SWARM_CONFIG="${SWARM_CONFIG:-$HOME/.swarm/config}"
if [[ -f "$SWARM_CONFIG" ]]; then
    source "$SWARM_CONFIG"
fi

# Trova Claude CLI (usa config o auto-detect)
get_claude_bin() {
    if [[ -n "$CLAUDE_BIN" && -x "$CLAUDE_BIN" ]]; then
        echo "$CLAUDE_BIN"
    elif command -v claude &>/dev/null; then
        which claude
    elif [[ -x "$HOME/.nvm/versions/node/v24.11.0/bin/claude" ]]; then
        echo "$HOME/.nvm/versions/node/v24.11.0/bin/claude"
    else
        echo ""
    fi
}

# ============================================================================
# PROJECT-AWARE (v1.9.0)
# ============================================================================

# Trova la root del progetto cercando .swarm/
# Funziona sia da symlink globale che da chiamata diretta
find_project_root() {
    local search_dir="$(pwd)"

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

    # Non trovato - restituisci pwd e lascia che main() gestisca l'errore
    echo "$(pwd)"
    return 1
}

PROJECT_ROOT="$(find_project_root)"
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
ALL_WORKERS="backend frontend tester docs reviewer devops researcher data security scienziata ingegnera"

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
1. Invia notifica macOS con virgolette DRITTE ("):
   osascript -e 'display notification "Task completato" with title "CervellaSwarm" sound name "Glass"'

QUANDO NON CI SONO PIU TASK PER TE:
1. Controlla .swarm/tasks/ per task .ready assegnati a te
2. Se non ci sono task, FAI /exit SUBITO!
   La finestra si chiudera automaticamente.

IMPORTANTE - VIRGOLETTE:
Quando scrivi comandi osascript, usa SEMPRE virgolette DRITTE: "
MAI virgolette curve: " o "
Esempio CORRETTO: osascript -e 'display notification "testo" with title "titolo"'
Esempio SBAGLIATO: osascript -e 'display notification "testo" with title "titolo"'

IMPORTANTE - NESSUN TASK:
Se non ci sono task per te:
1. NON aspettare
2. NON scrivere "Faccio /exit" - ESEGUILO!
3. Scrivi esattamente questo nel terminale: /exit
4. Premi invio
La finestra si chiudera automaticamente.

CRITICO: Quando dico "fai /exit", intendo che devi DIGITARE /exit come comando.
Non basta DIRE che lo farai - devi FARLO!
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
        scienziata)
            echo "Sei CERVELLA-SCIENZIATA.
Specializzazione: Ricerca STRATEGICA, trend di mercato, competitor analysis, opportunita business.
Diversa da researcher (tecnica), tu guardi il BUSINESS e le STRATEGIE.

${base_prompt}

FOCUS: Cerca task per 'cervella-scienziata' in .swarm/tasks/"
            ;;
        ingegnera)
            echo "Sei CERVELLA-INGEGNERA.
Specializzazione: Analisi codebase, technical debt, refactoring, ottimizzazioni.
Analizzi e proponi, NON modifichi direttamente.

${base_prompt}

FOCUS: Cerca task per 'cervella-ingegnera' in .swarm/tasks/"
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
# CervellaSwarm Worker Runner
# v1.5.0: Auto-close finestra Terminal quando Claude termina!

# Salva il TTY di questa finestra per identificarla dopo
MY_TTY=$(tty)
RUNNEREOF
    echo "cd ${PROJECT_ROOT}" >> "$runner_script"
    # Output visivo
    echo "echo ''" >> "$runner_script"
    echo "echo '🐝 [CervellaSwarm] Worker avviato'" >> "$runner_script"
    echo "echo ''" >> "$runner_script"
    # Prompt iniziale
    local initial_prompt="Controlla .swarm/tasks/ per task .ready assegnati a te e inizia a lavorare. Se non ci sono task, termina dicendo 'Nessun task per me'."
    # v2.0.0: Usa get_claude_bin() per trovare claude dinamicamente
    local claude_path
    claude_path=$(get_claude_bin)
    if [[ -z "$claude_path" ]]; then
        print_error "Claude CLI non trovato! Configura CLAUDE_BIN in ~/.swarm/config"
        return 1
    fi
    echo "mkdir -p ${SWARM_DIR}/logs" >> "$runner_script"
    echo "LOG_FILE=\"${SWARM_DIR}/logs/worker_\$(date +%Y%m%d_%H%M%S).log\"" >> "$runner_script"
    echo "${claude_path} -p --append-system-prompt \"\$(cat ${prompt_file})\" \"${initial_prompt}\" 2>&1 | tee \"\$LOG_FILE\"" >> "$runner_script"

    # Aggiungi chiusura automatica finestra Terminal
    cat >> "$runner_script" << 'CLOSEWINDOWEOF'

# ============================================================================
# AUTO-CLOSE: Claude terminato - chiudi questa finestra Terminal
# ============================================================================
echo ""
echo "[CervellaSwarm] Claude terminato. Chiudo finestra..."

# Notifica prima di chiudere
osascript -e 'display notification "Worker terminato, chiudo finestra!" with title "CervellaSwarm" sound name "Glass"' 2>/dev/null

# TRUCCO: Lancia chiusura in background, poi termina lo script
# Cosi quando osascript chiude la finestra, bash e' gia terminato = NO dialogo!
(
    sleep 1
    osascript << EOF
tell application "Terminal"
    repeat with w in windows
        repeat with t in tabs of w
            try
                if tty of t is "$MY_TTY" then
                    close w
                    return
                end if
            end try
        end repeat
    end repeat
end tell
EOF
) &

# Exit subito - la chiusura avverra in background dopo 1 secondo
exit 0
CLOSEWINDOWEOF
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
    echo "  --scienziata           Spawna cervella-scienziata"
    echo "  --ingegnera            Spawna cervella-ingegnera"
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
            --scienziata)
                workers_to_spawn="${workers_to_spawn} scienziata"
                ;;
            --ingegnera)
                workers_to_spawn="${workers_to_spawn} ingegnera"
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
