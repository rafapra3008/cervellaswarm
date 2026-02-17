#!/bin/bash
# weekly_retro_cron.sh - Script per cron weekly retrospective
#
# Esegue scripts.memory.retro.cli (modulo Python) e salva report in data/retro/
# Destinato per cron: ogni lunedì alle 8:00
#
# SETUP CRON:
#   crontab -e
#   # Aggiungi questa riga (aggiorna il path al tuo repo):
#   0 8 * * 1 $HOME/Developer/CervellaSwarm/scripts/cron/weekly_retro_cron.sh
#
# FORMATO CRON: minuto ora giorno-mese mese giorno-settimana
#   0 8 * * 1 = ogni lunedì alle 8:00
#
# Creato: 14 Gennaio 2026 - Sessione 201

set -e

# Path di base (computed from script location)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SWARM_DIR="${SWARM_DIR:-$(cd "$SCRIPT_DIR/../.." && pwd)}"
# NOTA: Refactoring S335 - ora usa modulo Python
LOG_FILE="$SWARM_DIR/data/logs/weekly_retro_cron.log"

# Crea directory log se non esiste
mkdir -p "$(dirname "$LOG_FILE")"

# Timestamp
echo "========================================" >> "$LOG_FILE"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Weekly Retro STARTED" >> "$LOG_FILE"

# Esegui weekly_retro con save e quiet mode
cd "$SWARM_DIR"

if python3 -m scripts.memory.retro.cli --save --quiet >> "$LOG_FILE" 2>&1; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Weekly Retro COMPLETED" >> "$LOG_FILE"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Weekly Retro FAILED" >> "$LOG_FILE"
    exit 1
fi

echo "========================================" >> "$LOG_FILE"
