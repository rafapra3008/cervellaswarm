#!/bin/bash
# CervellaSwarm Worker Runner
# v1.5.0: Auto-close finestra Terminal quando Claude termina!
# v1.6.0: PID/timestamp tracking per health check!

# Salva il TTY di questa finestra per identificarla dopo
MY_TTY=$(tty)
# Health tracking - salva PID e timestamp
mkdir -p /Users/rafapra/Developer/CervellaSwarm/.swarm/status
WORKER_PID=$$
WORKER_NAME="devops"
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
/Users/rafapra/.nvm/versions/node/v24.11.0/bin/claude -p --append-system-prompt "$(cat /Users/rafapra/Developer/CervellaSwarm/.swarm/prompts/worker_devops.txt)" "Controlla .swarm/tasks/ per task .ready assegnati a te e inizia a lavorare. Se non ci sono task, termina dicendo 'Nessun task per me'." 2>&1 | tee "$LOG_FILE"

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
