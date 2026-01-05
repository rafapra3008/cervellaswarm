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
# Versione: 1.0.0
# Data: 5 Gennaio 2026
# Cervella & Rafa

set -e

# Configurazione
WATCH_DIR="${1:-.swarm/tasks}"
REGINA_WINDOW="${2:-Code}"  # "Code" per VS Code

# Colori
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

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
echo -e "${GREEN}[OK]${NC} Regina window: $REGINA_WINDOW"
echo ""
echo "In attesa di file .done..."
echo "(Ctrl+C per terminare)"
echo ""

# Funzione per svegliare la Regina
sveglia_regina() {
    local task_name="$1"

    echo -e "${GREEN}[!]${NC} Rilevato: $task_name completato!"

    # Notifica macOS (sempre)
    if command -v terminal-notifier &>/dev/null; then
        terminal-notifier \
            -title "CervellaSwarm Watcher" \
            -subtitle "Worker completato!" \
            -message "$task_name" \
            -sound Glass 2>/dev/null
    else
        osascript -e "display notification \"$task_name completato!\" with title \"CervellaSwarm\" sound name \"Glass\"" 2>/dev/null
    fi

    # Sveglia Regina con keystroke
    osascript << EOF
tell application "System Events"
    if exists process "$REGINA_WINDOW" then
        tell application "$REGINA_WINDOW" to activate
        delay 0.5
        tell process "$REGINA_WINDOW"
            keystroke "WORKER COMPLETATO: $task_name - Leggi output!"
            delay 0.2
            key code 36
        end tell
        return "OK"
    else
        return "Regina non trovata: $REGINA_WINDOW"
    end if
end tell
EOF
}

# Monitor con fswatch
fswatch -0 "$WATCH_DIR" | while read -d "" event; do
    # Solo file .done
    if [[ "$event" == *.done ]]; then
        TASK_NAME=$(basename "$event" .done)
        sveglia_regina "$TASK_NAME"
    fi
done
