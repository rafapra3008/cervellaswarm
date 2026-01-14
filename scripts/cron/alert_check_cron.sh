#!/bin/bash
# ==============================================================================
# ALERT CHECK CRON - Controllo periodico alert
# ==============================================================================
#
# Esegue check alert periodico e notifica se trova problemi.
# Da aggiungere a crontab per esecuzione automatica.
#
# Uso manuale: ./alert_check_cron.sh
#
# Crontab (ogni 5 minuti):
#   */5 * * * * /path/to/alert_check_cron.sh >> ~/.swarm/logs/alert_cron.log 2>&1
#
# ==============================================================================

set -e

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PYTHON_SCRIPT="$PROJECT_ROOT/src/alerting/alert_system.py"

# Log
LOG_FILE="${HOME}/.swarm/logs/alert_cron.log"
mkdir -p "$(dirname "$LOG_FILE")"

# Timestamp
NOW=$(date "+%Y-%m-%d %H:%M:%S")

# ==============================================================================
# MAIN
# ==============================================================================

echo "[$NOW] Alert check starting..."

# Verifica Python script esiste
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "[$NOW] ERROR: Script not found: $PYTHON_SCRIPT"
    exit 1
fi

# Esegui check (non monitoring continuo)
cd "$PROJECT_ROOT"
python3 "$PYTHON_SCRIPT" 2>&1

RESULT=$?

if [ $RESULT -eq 0 ]; then
    echo "[$NOW] Alert check completed successfully"
else
    echo "[$NOW] Alert check failed with code: $RESULT"
fi

exit $RESULT
