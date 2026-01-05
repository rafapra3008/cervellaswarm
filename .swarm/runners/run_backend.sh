#!/bin/bash
# CervellaSwarm Worker Runner
# v1.5.0: Auto-close finestra Terminal quando Claude termina!
# v1.6.0: PID/timestamp tracking per health check!

# Salva il TTY di questa finestra per identificarla dopo
MY_TTY=$(tty)
# Health tracking - salva PID e timestamp
mkdir -p /Users/rafapra/Developer/CervellaSwarm/.swarm/status
WORKER_PID=$$
WORKER_NAME="backend"
echo $WORKER_PID > "/Users/rafapra/Developer/CervellaSwarm/.swarm/status/worker_${WORKER_NAME}.pid"
date +%s > "/Users/rafapra/Developer/CervellaSwarm/.swarm/status/worker_${WORKER_NAME}.start"

cleanup_health_files() {
    rm -f "/Users/rafapra/Developer/CervellaSwarm/.swarm/status/worker_${WORKER_NAME}.pid"
    rm -f "/Users/rafapra/Developer/CervellaSwarm/.swarm/status/worker_${WORKER_NAME}.start"
}
trap cleanup_health_files EXIT

cd /Users/rafapra/Developer/CervellaSwarm
echo ''
echo '🐝 [CervellaSwarm] Worker avviato'
echo ''
mkdir -p /Users/rafapra/Developer/CervellaSwarm/.swarm/logs
LOG_FILE="/Users/rafapra/Developer/CervellaSwarm/.swarm/logs/worker_$(date +%Y%m%d_%H%M%S).log"
SWARM_DIR="/Users/rafapra/Developer/CervellaSwarm/.swarm"
/Users/rafapra/.nvm/versions/node/v24.11.0/bin/claude -p --append-system-prompt "$(cat /Users/rafapra/Developer/CervellaSwarm/.swarm/prompts/worker_backend.txt)" "Controlla .swarm/tasks/ per task .ready assegnati a te e inizia a lavorare. Se non ci sono task, termina dicendo 'Nessun task per me'." 2>&1 | tee "$LOG_FILE"

# ============================================================================
# AUTO-CLOSE: Claude terminato - chiudi questa finestra Terminal
# v2.4.0: Notifica DETTAGLIATA con tempo esecuzione!
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

# Notifica dettagliata prima di chiudere (v2.4.0)
# Prova terminal-notifier (se installato) per click action, altrimenti osascript
if command -v terminal-notifier &>/dev/null; then
    terminal-notifier \
        -title "CervellaSwarm" \
        -subtitle "Worker terminato" \
        -message "cervella-${WORKER_NAME}: ${ESITO} (${DURATION_STR})" \
        -sound "$SOUND" \
        -open "file://${LOG_FILE}" 2>/dev/null
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
