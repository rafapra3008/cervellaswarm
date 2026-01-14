#!/bin/bash
# weekly_retro_cron.sh - Script per cron weekly retrospective
#
# Esegue weekly_retro.py e salva report in data/retro/
# Destinato per cron: ogni lunedì alle 8:00
#
# SETUP CRON:
#   crontab -e
#   # Aggiungi questa riga:
#   0 8 * * 1 /Users/rafapra/Developer/CervellaSwarm/scripts/cron/weekly_retro_cron.sh
#
# FORMATO CRON: minuto ora giorno-mese mese giorno-settimana
#   0 8 * * 1 = ogni lunedì alle 8:00
#
# Creato: 14 Gennaio 2026 - Sessione 201

set -e

# Path di base
SWARM_DIR="/Users/rafapra/Developer/CervellaSwarm"
SCRIPT="$SWARM_DIR/scripts/memory/weekly_retro.py"
LOG_FILE="$SWARM_DIR/data/logs/weekly_retro_cron.log"

# Crea directory log se non esiste
mkdir -p "$(dirname "$LOG_FILE")"

# Timestamp
echo "========================================" >> "$LOG_FILE"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Weekly Retro STARTED" >> "$LOG_FILE"

# Esegui weekly_retro con save e quiet mode
cd "$SWARM_DIR"

if python3 "$SCRIPT" --save --quiet >> "$LOG_FILE" 2>&1; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Weekly Retro COMPLETED" >> "$LOG_FILE"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Weekly Retro FAILED" >> "$LOG_FILE"
    exit 1
fi

echo "========================================" >> "$LOG_FILE"
