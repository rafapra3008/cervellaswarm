#!/bin/bash
# CervellaSwarm Worker Runner
# v1.5.0: Auto-close finestra Terminal quando Claude termina!

# Salva il TTY di questa finestra per identificarla dopo
MY_TTY=$(tty)
cd /Users/rafapra/Developer/CervellaSwarm
/Users/rafapra/.nvm/versions/node/v24.11.0/bin/claude --append-system-prompt "$(cat /Users/rafapra/Developer/CervellaSwarm/.swarm/prompts/worker_tester.txt)" "Controlla .swarm/tasks/ per task .ready assegnati a te e inizia a lavorare. Se non ci sono task per te, fai /exit SUBITO!"

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
