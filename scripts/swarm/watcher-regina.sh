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
# Versione: 1.1.0
# Data: 5 Gennaio 2026
# Cervella & Rafa
#
# v1.1.0: RIMOSSO keystroke! Solo notifiche.
#         Sicuro con multiple finestre aperte.
#         Click notifica apre output direttamente.

set -e

# Configurazione
WATCH_DIR="${1:-.swarm/tasks}"
# NOTA: Non usiamo piu' keystroke nella finestra
# Solo notifiche - sicuro con multiple finestre!

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
echo -e "${GREEN}[OK]${NC} Solo notifiche - sicuro con multiple finestre!"
echo ""
echo "In attesa di file .done..."
echo "(Ctrl+C per terminare)"
echo ""

# Funzione per svegliare la Regina
sveglia_regina() {
    local task_name="$1"

    echo -e "${GREEN}[!]${NC} Rilevato: $task_name completato!"

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
        osascript -e "display notification \"$task_name completato!\" with title \"CervellaSwarm\" sound name \"Glass\"" 2>/dev/null
    fi

    # RIMOSSO: keystroke nella finestra
    # Era rischioso con multiple finestre aperte!
    # Ora usiamo solo notifiche - piu' sicuro e pulito.
}

# Monitor con fswatch
fswatch -0 "$WATCH_DIR" | while read -d "" event; do
    # Solo file .done
    if [[ "$event" == *.done ]]; then
        TASK_NAME=$(basename "$event" .done)
        sveglia_regina "$TASK_NAME"
    fi
done
