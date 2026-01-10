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
# Versione: 3.5.0
# Data: 2026-01-10
# Apple Style: Auto-close, Graceful shutdown, Notifiche macOS
# v2.0.0: Config centralizzata ~/.swarm/config
#
# CHANGELOG:
# v3.5.0: CLAUDE MAX! Unset ANTHROPIC_API_KEY per usare account Claude Max invece di API credits.
# v3.4.0: COMMON LIBRARY! Source common.sh per funzioni condivise (DRY). Backward compatible.
# v3.3.0: VALIDAZIONE PROGETTO! Non crea piu .swarm/ nel posto sbagliato. Richiede progetto valido.
# v3.2.0: OUTPUT REALTIME! stdbuf -oL per unbuffered output. Vediamo progresso worker in tempo reale!
# v3.1.0: HEADLESS DEFAULT! --headless è ora il comportamento standard. Usa --window per finestre.
# v3.0.0: HEADLESS MODE! --headless usa tmux invece di Terminal.app. Zero finestre!
# v2.9.0: FIX AUTO-SVEGLIA! Cerca watcher ANCHE in ~/.claude/scripts/ (globale). Funziona in TUTTI i progetti!
# v2.8.0: MAX WORKERS! Limite default 5 per evitare sovraccarico. Flag --max-workers N per cambiare.
# v2.7.0: AUTO-SVEGLIA SEMPRE! Default=true. Check anti-watcher-duplicati. Flag --no-auto-sveglia per disabilitare.
# v2.6.0: AUTO-SVEGLIA! Flag --auto-sveglia avvia watcher che sveglia la Regina quando worker finiscono!
# v2.5.0: FIX NOTIFICA CLICK! Apre _output.md del task invece di .log. Legge task name da file stato.
# v2.4.0: NOTIFICA DETTAGLIATA! Nome task, tempo esecuzione, esito. Click per aprire log (se terminal-notifier)
# v2.3.0: Validazione ownership config prima di source (security fix)
# v2.2.0: HEARTBEAT + Notifiche INIZIO task! Worker scrivono stato ogni 60s
# v2.1.0: Worker Health Tracking - PID/timestamp per sapere se worker e' vivo!
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
# COMMON LIBRARY (v3.4.0) - Funzioni condivise
# ============================================================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "${SCRIPT_DIR}/common.sh" ]]; then
    source "${SCRIPT_DIR}/common.sh"
fi
# Nota: Le funzioni locali sotto sono mantenute per backward compatibility
# Verranno rimosse in una versione futura quando common.sh sara' diffuso

# ============================================================================
# AUTO-SVEGLIA (v2.7.0) - SEMPRE ATTIVO! La Regina viene svegliata automaticamente!
# ============================================================================
AUTO_SVEGLIA=true

# ============================================================================
# MAX WORKERS (v2.8.0) - Limite per evitare sovraccarico sistema
# ============================================================================
MAX_WORKERS=5

# ============================================================================
# HEADLESS MODE (v3.1.0) - tmux invece di Terminal.app (DEFAULT!)
# ============================================================================
HEADLESS_MODE=true

# ============================================================================
# OUTPUT UNBUFFERED (v3.2.0) - Output realtime dai worker!
# ============================================================================
# Cerca stdbuf/gstdbuf/unbuffer per line-buffered output
# Permette di vedere progresso worker in tempo reale invece di a blocchi
STDBUF_CMD=""
if command -v stdbuf &>/dev/null; then
    STDBUF_CMD="stdbuf -oL"
elif command -v gstdbuf &>/dev/null; then
    STDBUF_CMD="gstdbuf -oL"
elif command -v unbuffer &>/dev/null; then
    STDBUF_CMD="unbuffer"
    # unbuffer mescola stdout+stderr, ma meglio di niente
fi
# Se nessuno trovato, STDBUF_CMD resta "" e output sara' bufferizzato (degraded mode)

# ============================================================================
# CONFIGURAZIONE CENTRALIZZATA (v2.0.0)
# ============================================================================

# Carica configurazione globale se esiste
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

if [[ -f "$SWARM_CONFIG" ]]; then
    if validate_config_ownership "$SWARM_CONFIG"; then
        source "$SWARM_CONFIG"
    else
        echo "[!] Config $SWARM_CONFIG non caricato: ownership/permessi non validi" >&2
    fi
fi

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

# Cerca project root - VALIDA che esista davvero!
if PROJECT_ROOT="$(find_project_root)"; then
    SWARM_DIR="${PROJECT_ROOT}/.swarm"
    PROJECT_VALID=true
else
    # Non trovato .swarm/ - NON creare automaticamente!
    PROJECT_ROOT="$(pwd)"
    SWARM_DIR="${PROJECT_ROOT}/.swarm"
    PROJECT_VALID=false
fi

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
3. Quando prendi un task:
   - Crea file .working
   - Scrivi il TASK_ID in .swarm/status/worker_TUONOME.task (es: echo "TASK_123" > .swarm/status/worker_backend.task)
4. Quando finisci, crea file .done e scrivi output in _output.md
5. NON modificare file fuori dal tuo scope
6. Se hai dubbi, scrivi in .swarm/handoff/ per la Regina

HEARTBEAT (IMPORTANTE - fallo ogni 60 secondi mentre lavori!):
Scrivi il tuo stato attuale per la Regina:
echo "$(date +%s)|NOME_TASK|cosa stai facendo ora" >> .swarm/status/heartbeat_WORKER.log

Esempio:
echo "$(date +%s)|TASK_123|Analizzando file database.py" >> .swarm/status/heartbeat_backend.log

Questo permette alla Regina di vedere il tuo progresso in tempo reale!

COMANDI UTILI:
- python3 scripts/swarm/task_manager.py list
- python3 scripts/swarm/task_manager.py working TASK_ID
- python3 scripts/swarm/task_manager.py done TASK_ID

APPLE STYLE - FINITURE:

NOTIFICHE (usa SEMPRE virgolette DRITTE!):
- INIZIO TASK: osascript -e 'display notification "Inizio: NOME_TASK" with title "CervellaSwarm"'
- FINE TASK: osascript -e 'display notification "Completato: NOME_TASK" with title "CervellaSwarm" sound name "Glass"'
- ERRORE: osascript -e 'display notification "ERRORE!" with title "CervellaSwarm" sound name "Basso"'

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
        marketing)
            echo "Sei CERVELLA-MARKETING.
Specializzazione: Marketing, UX strategy, posizionamento, copywriting, user flow.
Decidi dove mettere bottoni, come guidare l'utente, messaggi che colpiscono.

${base_prompt}

FOCUS: Cerca task per 'cervella-marketing' in .swarm/tasks/"
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
# v1.6.0: PID/timestamp tracking per health check!

# Salva il TTY di questa finestra per identificarla dopo
MY_TTY=$(tty)
RUNNEREOF

    # Aggiungi tracking PID/timestamp (v1.6.0)
    echo "# Health tracking - salva PID e timestamp" >> "$runner_script"
    echo "mkdir -p ${SWARM_DIR}/status" >> "$runner_script"
    echo "WORKER_PID=\$\$" >> "$runner_script"
    echo "WORKER_NAME=\"${worker_name}\"" >> "$runner_script"
    echo "echo \$WORKER_PID > \"${SWARM_DIR}/status/worker_\${WORKER_NAME}.pid\"" >> "$runner_script"
    echo "date +%s > \"${SWARM_DIR}/status/worker_\${WORKER_NAME}.start\"" >> "$runner_script"
    echo "" >> "$runner_script"
    # Cleanup function per rimuovere i file quando il worker termina
    echo "cleanup_health_files() {" >> "$runner_script"
    echo "    rm -f \"${SWARM_DIR}/status/worker_\${WORKER_NAME}.pid\"" >> "$runner_script"
    echo "    rm -f \"${SWARM_DIR}/status/worker_\${WORKER_NAME}.start\"" >> "$runner_script"
    echo "}" >> "$runner_script"
    echo "trap cleanup_health_files EXIT" >> "$runner_script"
    echo "" >> "$runner_script"
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
    # v2.4.0: Salva SWARM_DIR come variabile nel runner per usarla nella notifica finale
    echo "SWARM_DIR=\"${SWARM_DIR}\"" >> "$runner_script"
    # v3.0.0: CERVELLASWARM_WORKER=1 permette ai Worker di bypassare hook blocco edit!
    echo "export CERVELLASWARM_WORKER=1" >> "$runner_script"
    # v3.5.0: Unset ANTHROPIC_API_KEY per usare account Claude Max invece di API
    echo "unset ANTHROPIC_API_KEY" >> "$runner_script"
    # v3.2.0: STDBUF_CMD per output realtime
    echo "${STDBUF_CMD} ${claude_path} -p --append-system-prompt \"\$(cat ${prompt_file})\" \"${initial_prompt}\" 2>&1 | tee \"\$LOG_FILE\"" >> "$runner_script"

    # Aggiungi chiusura automatica finestra Terminal con notifica dettagliata (v2.4.0)
    cat >> "$runner_script" << 'CLOSEWINDOWEOF'

# ============================================================================
# AUTO-CLOSE: Claude terminato - chiudi questa finestra Terminal
# v2.5.0: Click notifica apre _output.md del task (non piu .log!)
# ============================================================================

# Salva exit code di Claude
CLAUDE_EXIT=$?

echo ""
echo "[CervellaSwarm] Claude terminato. Preparo notifica..."

# Calcola durata (v2.4.0)
START_FILE="${SWARM_DIR}/status/worker_${WORKER_NAME}.start"
if [ -f "$START_FILE" ]; then
    START_TIME=$(cat "$START_FILE")
    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))
    MINUTES=$((DURATION / 60))
    SECONDS_REMAIN=$((DURATION % 60))
    DURATION_STR="${MINUTES}m ${SECONDS_REMAIN}s"
else
    DURATION_STR="N/A"
fi

# Determina esito
if [ "$CLAUDE_EXIT" -eq 0 ]; then
    ESITO="Completato"
    SOUND="Glass"
else
    ESITO="Errore (exit $CLAUDE_EXIT)"
    SOUND="Basso"
fi

# v2.5.0: Trova l'ultimo task completato (.done piu recente) per questo worker
# Cerca file _output.md corrispondente al task
TASK_OUTPUT_FILE=""
TASK_FILE="${SWARM_DIR}/status/worker_${WORKER_NAME}.task"
if [ -f "$TASK_FILE" ]; then
    # Se il worker ha scritto quale task stava processando, usa quello
    TASK_NAME=$(cat "$TASK_FILE")
    POTENTIAL_OUTPUT="${SWARM_DIR}/tasks/${TASK_NAME}_output.md"
    if [ -f "$POTENTIAL_OUTPUT" ]; then
        TASK_OUTPUT_FILE="$POTENTIAL_OUTPUT"
    fi
fi

# Fallback: cerca il .done piu recente e deriva l'output
if [ -z "$TASK_OUTPUT_FILE" ]; then
    LATEST_DONE=$(ls -t "${SWARM_DIR}/tasks/"*.done 2>/dev/null | head -1)
    if [ -n "$LATEST_DONE" ]; then
        # Estrai nome task dal file .done (rimuovi .done)
        TASK_BASE=$(basename "$LATEST_DONE" .done)
        POTENTIAL_OUTPUT="${SWARM_DIR}/tasks/${TASK_BASE}_output.md"
        if [ -f "$POTENTIAL_OUTPUT" ]; then
            TASK_OUTPUT_FILE="$POTENTIAL_OUTPUT"
        fi
    fi
fi

# Fallback finale: usa il log
if [ -z "$TASK_OUTPUT_FILE" ]; then
    TASK_OUTPUT_FILE="$LOG_FILE"
fi

# Notifica dettagliata prima di chiudere (v2.5.0)
# Prova terminal-notifier (se installato) per click action, altrimenti osascript
if command -v terminal-notifier &>/dev/null; then
    terminal-notifier \
        -title "CervellaSwarm" \
        -subtitle "Worker terminato" \
        -message "cervella-${WORKER_NAME}: ${ESITO} (${DURATION_STR})" \
        -sound "$SOUND" \
        -open "file://${TASK_OUTPUT_FILE}" 2>/dev/null
else
    osascript -e "display notification \"cervella-${WORKER_NAME}: ${ESITO} (${DURATION_STR})\" with title \"CervellaSwarm\" sound name \"${SOUND}\"" 2>/dev/null
fi

echo "[CervellaSwarm] Chiudo finestra..."

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
    # SICUREZZA: Usa heredoc invece di interpolazione per evitare command injection
    osascript << APPLESCRIPTEOF
tell application "Terminal"
    do script "$runner_script"
end tell
APPLESCRIPTEOF
    osascript -e 'tell application "Terminal" to activate'

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

# ============================================================================
# HEADLESS MODE (v3.0.0) - Spawn worker in tmux invece di Terminal.app
# ============================================================================
spawn_worker_headless() {
    local worker_name="$1"
    local prompt
    prompt=$(get_worker_prompt "$worker_name")

    if [ -z "$prompt" ]; then
        print_error "Worker '$worker_name' non trovato!"
        return 1
    fi

    print_info "Spawning cervella-${worker_name} (headless)..."

    # Salva prompt in file temporaneo
    local prompt_file="${SWARM_DIR}/prompts/worker_${worker_name}.txt"
    mkdir -p "${SWARM_DIR}/prompts"
    printf '%s' "$prompt" > "$prompt_file"

    # Nome sessione tmux univoco
    local session_name="swarm_${worker_name}_$(date +%s)"

    # Trova claude
    local claude_path
    claude_path=$(get_claude_bin)
    if [[ -z "$claude_path" ]]; then
        print_error "Claude CLI non trovato!"
        return 1
    fi

    # Crea directories
    mkdir -p "${SWARM_DIR}/status"
    mkdir -p "${SWARM_DIR}/logs"

    # Prompt iniziale
    local initial_prompt="Controlla .swarm/tasks/ per task .ready assegnati a te e inizia a lavorare. Se non ci sono task, termina dicendo 'Nessun task per me'."

    # Log file
    local log_file="${SWARM_DIR}/logs/worker_${worker_name}_$(date +%Y%m%d_%H%M%S).log"

    # Salva session name per tracking
    echo "$session_name" > "${SWARM_DIR}/status/worker_${worker_name}.session"

    # Salva timestamp start
    date +%s > "${SWARM_DIR}/status/worker_${worker_name}.start"

    # Spawn in tmux detached (NESSUNA FINESTRA!)
    # v3.2.0: Aggiunto STDBUF_CMD per output realtime
    # v3.5.0: Unset ANTHROPIC_API_KEY per usare account Claude Max invece di API
    tmux new-session -d -s "$session_name" \
        "cd ${PROJECT_ROOT} && \
         export CERVELLASWARM_WORKER=1 && \
         unset ANTHROPIC_API_KEY && \
         ${STDBUF_CMD} ${claude_path} -p --append-system-prompt \"\$(cat ${prompt_file})\" \"${initial_prompt}\" 2>&1 | tee \"${log_file}\"; \
         echo 'WORKER_DONE' >> \"${log_file}\""

    # Imposta remain-on-exit per catturare output dopo fine
    tmux set-option -t "$session_name" remain-on-exit on 2>/dev/null

    if tmux has-session -t "$session_name" 2>/dev/null; then
        print_success "cervella-${worker_name} spawned (headless)! Session: ${session_name}"
        echo "$(date '+%Y-%m-%d %H:%M:%S') - SPAWNED (headless): cervella-${worker_name} [${session_name}]" >> "${SWARM_DIR}/logs/spawn.log"
        return 0
    else
        print_error "Errore spawn headless cervella-${worker_name}"
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
    echo "  --marketing            Spawna cervella-marketing"
    echo "  --guardiana-qualita    Spawna cervella-guardiana-qualita (Opus)"
    echo "  --guardiana-ops        Spawna cervella-guardiana-ops (Opus)"
    echo "  --guardiana-ricerca    Spawna cervella-guardiana-ricerca (Opus)"
    echo "  --all                  Spawna worker comuni (backend, frontend, tester)"
    echo "  --guardiane            Spawna tutte le guardiane"
    echo "  --list                 Lista worker disponibili"
    echo "  --no-auto-sveglia      Disabilita AUTO-SVEGLIA (default: attivo!)"
    echo "  --headless             Usa tmux headless (DEFAULT)"
    echo "  --window               Apre finestra Terminal (vecchio comportamento)"
    echo "  --help                 Mostra questo help"
    echo ""
    echo "  AUTO-SVEGLIA e' ATTIVO di default! La Regina viene svegliata automaticamente."
    echo ""
    echo "Esempi:"
    echo "  $0 --backend               # Spawna backend (AUTO-SVEGLIA attivo!)"
    echo "  $0 --all                   # Spawna tutti i worker comuni"
    echo "  $0 --guardiane             # Spawna tutte le guardiane (Opus)"
    echo "  $0 --docs --no-auto-sveglia  # Docs senza svegliare la Regina"
    echo "  $0 --headless --backend    # Backend in tmux (no finestre!)"
    echo ""
}

# ============================================================================
# MAIN
# ============================================================================

main() {
    print_header

    # v3.2.0: Warning se stdbuf non trovato
    if [ -z "$STDBUF_CMD" ]; then
        print_warning "stdbuf non trovato - output worker potrebbe essere ritardato"
        print_info "Per output realtime: brew install coreutils"
        echo ""
    fi

    # VALIDAZIONE PROGETTO (v3.3.0): Non creare .swarm/ nel posto sbagliato!
    if [ "$PROJECT_VALID" = false ]; then
        print_error "Non sei in un progetto CervellaSwarm!"
        print_error "Nessuna directory .swarm/ trovata in questa cartella o superiori."
        echo ""
        print_info "Per usare spawn-workers devi essere in un progetto con .swarm/"
        print_info "Oppure crea la struttura manualmente: mkdir -p .swarm/tasks"
        echo ""
        exit 1
    fi

    # Verifica struttura .swarm/ completa
    if [ ! -d "${SWARM_DIR}/tasks" ]; then
        print_warning "Struttura .swarm/ incompleta. Completo..."
        mkdir -p "${SWARM_DIR}/tasks"
        mkdir -p "${SWARM_DIR}/status"
        mkdir -p "${SWARM_DIR}/logs"
        mkdir -p "${SWARM_DIR}/handoff"
        print_success "Struttura .swarm/ completata!"
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
            --marketing)
                workers_to_spawn="${workers_to_spawn} marketing"
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
            --auto-sveglia)
                AUTO_SVEGLIA=true
                ;;
            --no-auto-sveglia)
                AUTO_SVEGLIA=false
                ;;
            --max-workers)
                shift
                if [[ -n "$1" && "$1" =~ ^[0-9]+$ ]]; then
                    MAX_WORKERS="$1"
                else
                    print_error "--max-workers richiede un numero!"
                    exit 1
                fi
                ;;
            --headless)
                HEADLESS_MODE=true
                ;;
            --window)
                HEADLESS_MODE=false
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

    # CHECK MAX WORKERS (v2.8.0): Previene sovraccarico sistema
    if [ "$worker_count" -gt "$MAX_WORKERS" ]; then
        print_warning "Richiesti ${worker_count} worker, ma MAX_WORKERS=${MAX_WORKERS}!"
        print_warning "Spawning solo i primi ${MAX_WORKERS} worker."
        print_info "Usa --max-workers N per cambiare il limite."
        echo ""
        # Tronca la lista
        workers_to_spawn=$(echo "$workers_to_spawn" | xargs -n1 | head -n "$MAX_WORKERS" | xargs)
        worker_count=$MAX_WORKERS
    fi

    echo ""
    print_info "Spawning ${worker_count} worker(s)... (max: ${MAX_WORKERS})"
    echo ""

    spawned=0
    failed=0

    for worker in $workers_to_spawn; do
        if [ "$HEADLESS_MODE" = true ]; then
            if spawn_worker_headless "$worker"; then
                spawned=$((spawned + 1))
            else
                failed=$((failed + 1))
            fi
        else
            if spawn_worker "$worker"; then
                spawned=$((spawned + 1))
            else
                failed=$((failed + 1))
            fi
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
    if [ "$HEADLESS_MODE" = true ]; then
        print_info "Worker in background (tmux headless)!"
        print_info "Usa 'tmux list-sessions' per vedere le sessioni"
    else
        print_info "Le finestre Terminal sono aperte!"
    fi
    print_info "I worker stanno cercando task in .swarm/tasks/"
    echo ""

    # ============================================================================
    # AUTO-SVEGLIA (v2.6.0) - Avvia watcher se richiesto
    # ============================================================================
    if [ "$AUTO_SVEGLIA" = true ]; then
        # Cerca watcher: prima nel progetto, poi globalmente
        if [ -x "${PROJECT_ROOT}/scripts/swarm/watcher-regina.sh" ]; then
            WATCHER_SCRIPT="${PROJECT_ROOT}/scripts/swarm/watcher-regina.sh"
        elif [ -x "$HOME/.claude/scripts/watcher-regina.sh" ]; then
            WATCHER_SCRIPT="$HOME/.claude/scripts/watcher-regina.sh"
        else
            WATCHER_SCRIPT=""
        fi
        WATCHER_PID_FILE="${SWARM_DIR}/status/watcher.pid"

        # CHECK ANTI-DUPLICATI (v2.7.0): Se watcher gia' attivo, non avviarne un altro!
        if [ -f "$WATCHER_PID_FILE" ]; then
            EXISTING_PID=$(cat "$WATCHER_PID_FILE" 2>/dev/null)
            if [ -n "$EXISTING_PID" ] && kill -0 "$EXISTING_PID" 2>/dev/null; then
                print_info "AUTO-SVEGLIA gia' attivo! (PID: $EXISTING_PID)"
                print_info "La Regina verra' svegliata quando i worker finiscono!"
                echo ""
                # Skip avvio nuovo watcher
            else
                # PID file esiste ma processo morto - pulisci e riavvia
                rm -f "$WATCHER_PID_FILE"
            fi
        fi

        # Avvia watcher solo se non gia' attivo e script esiste
        if [ ! -f "$WATCHER_PID_FILE" ] && [ -n "$WATCHER_SCRIPT" ] && [ -x "$WATCHER_SCRIPT" ]; then
            echo ""
            print_info "Avvio AUTO-SVEGLIA watcher..."

            # Avvia watcher in background
            "$WATCHER_SCRIPT" "${SWARM_DIR}/tasks" "Code" &
            WATCHER_PID=$!

            # Salva PID per cleanup futuro
            echo $WATCHER_PID > "$WATCHER_PID_FILE"

            print_success "Watcher AUTO-SVEGLIA avviato! (PID: $WATCHER_PID)"
            print_info "La Regina verra' svegliata quando i worker finiscono!"
            echo ""
        elif [ -z "$WATCHER_SCRIPT" ]; then
            print_warning "Watcher script non trovato!"
            print_warning "Cercato in: ${PROJECT_ROOT}/scripts/swarm/ e ~/.claude/scripts/"
            print_warning "AUTO-SVEGLIA non attivato."
        fi
    fi
}

# Esegui
main "$@"
