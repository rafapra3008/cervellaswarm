#!/bin/bash
#
# watcher-regina.sh - Sveglia la Regina quando i worker finiscono!
#
# LA MAGIA SOPRA MAGIA!
#
# Uso:
#   ./watcher-regina.sh                    # Default: .swarm/tasks, VS Code
#   ./watcher-regina.sh .swarm/tasks Code  # Esplicito
#
# Versione: 1.6.0
# Data: 9 Gennaio 2026
# Cervella & Rafa
#
# v1.5.0: HEADLESS SUPPORT!
#         - Log notifiche in ~/.swarm/notifications.log
#         - Double bell (terminal bell + macOS notification)
#         - Monitoraggio sessioni tmux headless
# v1.4.0: ESTENSIONE COMUNICAZIONE!
#         - Check heartbeat periodico (ogni 2min)
#         - Watch .swarm/feedback/ per feedback worker
#         - Dashboard ASCII opzionale (--dashboard)
# v1.1.0: RIMOSSO keystroke! Solo notifiche.
#         Sicuro con multiple finestre aperte.
#         Click notifica apre output direttamente.
# v1.6.0: SECURITY FIX! Usa notify_macos per notifiche sicure (no injection)

set -e

# Source common functions
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "${SCRIPT_DIR}/common.sh" ]]; then
    source "${SCRIPT_DIR}/common.sh"
fi

# Configurazione
WATCH_DIR="${1:-.swarm/tasks}"
SHOW_DASHBOARD=0
LAST_STUCK_CHECK=0
LAST_TMUX_CHECK=0
CHECK_STUCK_INTERVAL=120  # 2 minuti
CHECK_TMUX_INTERVAL=30    # 30 secondi per tmux
NOTIFICATION_LOG="$HOME/.swarm/notifications.log"

# Assicura che la directory per il log esista
mkdir -p "$HOME/.swarm"

# Parse arguments
if [[ "${1:-}" == "--dashboard" ]]; then
  SHOW_DASHBOARD=1
  shift
  WATCH_DIR="${1:-.swarm/tasks}"
fi

# NOTA: Non usiamo piu' keystroke nella finestra
# Solo notifiche - sicuro con multiple finestre!

# Colori
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Funzione per loggare notifiche
log_notification() {
    local msg="$1"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $msg" >> "$NOTIFICATION_LOG"
}

echo -e "${BLUE}"
echo "=============================================="
echo "  WATCHER-REGINA - La Magia Sopra Magia!"
echo "=============================================="
echo -e "${NC}"

# Verifica fswatch installato
if ! command -v fswatch &>/dev/null; then
    echo -e "${YELLOW}[!] ERRORE: fswatch non installato!${NC}"
    echo "    Installa con: brew install fswatch"
    exit 1
fi

# Verifica directory esiste
if [[ ! -d "$WATCH_DIR" ]]; then
    echo -e "${YELLOW}[!] Directory $WATCH_DIR non esiste!${NC}"
    exit 1
fi

echo -e "${GREEN}[OK]${NC} Monitoring: $WATCH_DIR"
echo -e "${GREEN}[OK]${NC} Monitoring: .swarm/feedback/"
echo -e "${GREEN}[OK]${NC} Check stuck: ogni ${CHECK_STUCK_INTERVAL}s"
echo -e "${GREEN}[OK]${NC} Check tmux: ogni ${CHECK_TMUX_INTERVAL}s"
echo -e "${GREEN}[OK]${NC} Log notifiche: $NOTIFICATION_LOG"
echo -e "${GREEN}[OK]${NC} Double bell + notifica macOS"
echo ""
echo "In attesa di:"
echo "  - file .done (task completati)"
echo "  - feedback worker (.swarm/feedback/)"
echo "  - worker stuck (heartbeat monitoring)"
echo "  - sessioni tmux headless terminate"
echo ""
echo "(Ctrl+C per terminare)"
echo ""

# Funzione per svegliare la Regina (task completato)
sveglia_regina() {
    local task_name="$1"

    echo -e "${GREEN}[!]${NC} Rilevato: $task_name completato!"

    # Terminal bell (attenzione immediata) - double bell per affidabilita
    printf '\a'
    sleep 0.3
    printf '\a'

    # Log della notifica
    log_notification "TASK_DONE: $task_name"

    # Notifica macOS (sempre) - SICURA con multiple finestre!
    # Click sulla notifica apre l'output del task
    if command -v terminal-notifier &>/dev/null; then
        # Cerca il file output per aprirlo al click
        local output_file=""
        if [[ -f ".swarm/tasks/${task_name}_output.md" ]]; then
            output_file=".swarm/tasks/${task_name}_output.md"
        fi

        terminal-notifier \
            -title "Worker Completato!" \
            -subtitle "$task_name" \
            -message "Click per vedere output" \
            -sound Glass \
            ${output_file:+-open "$output_file"} \
            2>/dev/null
    else
        # Usa notify_macos se disponibile (da common.sh), altrimenti fallback
        if type notify_macos &>/dev/null; then
            notify_macos "CervellaSwarm" "$task_name completato!" "Glass"
        else
            osascript -e "display notification \"$(echo "$task_name" | tr -d '\"')\" with title \"CervellaSwarm\" sound name \"Glass\"" 2>/dev/null
        fi
    fi

    # RIMOSSO: keystroke nella finestra
    # Era rischioso con multiple finestre aperte!
    # Ora usiamo solo notifiche - piu' sicuro e pulito.
}

# Funzione per notificare feedback worker
notifica_feedback() {
    local feedback_file="$1"
    local filename=$(basename "$feedback_file")

    # Parse filename: TIPO_TASKID_TIMESTAMP.md
    local tipo=$(echo "$filename" | cut -d'_' -f1)

    echo -e "${YELLOW}[!]${NC} Rilevato feedback: $tipo"

    # Terminal bell (attenzione immediata)
    printf '\a'

    # Log della notifica
    log_notification "FEEDBACK: $tipo - $filename"

    # Notifica macOS
    local emoji="💬"
    case "$tipo" in
        QUESTION)
            emoji="💬"
            ;;
        ISSUE)
            emoji="⚠️"
            ;;
        BLOCKER)
            emoji="🚫"
            ;;
        SUGGESTION)
            emoji="💡"
            ;;
    esac

    if command -v terminal-notifier &>/dev/null; then
        terminal-notifier \
            -title "${emoji} Feedback: ${tipo}" \
            -message "Worker needs attention" \
            -sound Glass \
            -open "$feedback_file" \
            2>/dev/null
    else
        if type notify_macos &>/dev/null; then
            notify_macos "${emoji} Feedback" "Worker feedback: ${tipo}" "Glass"
        else
            osascript -e "display notification \"Worker feedback: $(echo "$tipo" | tr -d '\"')\" with title \"${emoji} Feedback\" sound name \"Glass\"" 2>/dev/null
        fi
    fi
}

# Funzione check stuck periodico
check_stuck_periodico() {
    local now=$(date +%s)

    # Controlla se è passato abbastanza tempo
    if [ $((now - LAST_STUCK_CHECK)) -gt $CHECK_STUCK_INTERVAL ]; then
        # Run check-stuck.sh
        if [[ -x "scripts/swarm/check-stuck.sh" ]]; then
            # Controlla in background (non bloccare il watcher)
            if ! scripts/swarm/check-stuck.sh --notify &>/dev/null; then
                # Stuck detected - già notificato da check-stuck.sh
                echo -e "${YELLOW}[!]${NC} Worker stuck detected"
            fi
        fi

        LAST_STUCK_CHECK=$now
    fi
}

# Funzione per monitorare sessioni tmux headless
check_tmux_sessions() {
    local now=$(date +%s)

    # Controlla se è passato abbastanza tempo
    if [ $((now - LAST_TMUX_CHECK)) -lt $CHECK_TMUX_INTERVAL ]; then
        return
    fi

    LAST_TMUX_CHECK=$now

    # Verifica se tmux è disponibile
    if ! command -v tmux &>/dev/null; then
        return
    fi

    # Lista sessioni swarm
    local sessions=$(tmux list-sessions 2>/dev/null | grep "^swarm_" | cut -d: -f1)

    for session in $sessions; do
        # Check se il pane è "dead" (comando terminato)
        local status=$(tmux display-message -t "$session" -p '#{pane_dead}' 2>/dev/null)
        if [ "$status" = "1" ]; then
            echo -e "${GREEN}[!]${NC} Sessione tmux terminata: $session"

            # Terminal bell
            printf '\a'

            # Log
            log_notification "TMUX_DONE: $session"

            # Notifica macOS
            if command -v terminal-notifier &>/dev/null; then
                terminal-notifier \
                    -title "Worker Headless Completato!" \
                    -subtitle "$session" \
                    -message "Sessione tmux terminata" \
                    -sound Glass \
                    2>/dev/null
            else
                if type notify_macos &>/dev/null; then
                    notify_macos "CervellaSwarm" "$session terminato!" "Glass"
                else
                    osascript -e "display notification \"$(echo "$session" | tr -d '\"') terminato!\" with title \"CervellaSwarm\" sound name \"Glass\"" 2>/dev/null
                fi
            fi

            # Opzionale: termina la sessione morta
            # tmux kill-session -t "$session" 2>/dev/null
        fi
    done
}

# Monitor con fswatch - watch multiple directories!
# Watcher .swarm/tasks/ e .swarm/feedback/
fswatch -0 "$WATCH_DIR" .swarm/feedback 2>/dev/null | while read -d "" event; do
    # Check periodico stuck workers
    check_stuck_periodico

    # Check periodico sessioni tmux headless
    check_tmux_sessions

    # Handler file .done (task completati)
    if [[ "$event" == *.done ]]; then
        TASK_NAME=$(basename "$event" .done)
        sveglia_regina "$TASK_NAME"
    fi

    # Handler feedback files
    if [[ "$event" == *".swarm/feedback/"* ]] && [[ "$event" == *.md ]] && [[ "$event" != *"_RESPONSE.md" ]]; then
        notifica_feedback "$event"
    fi
done
