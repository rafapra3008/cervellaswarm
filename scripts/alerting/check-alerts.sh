#!/bin/bash
# ==============================================================================
# CHECK-ALERTS - Controlla alert nel sistema
# ==============================================================================
#
# Uso:
#   ./check-alerts.sh              # Check singolo
#   ./check-alerts.sh --monitor    # Monitoring continuo
#   ./check-alerts.sh --patterns   # Solo pattern detection
#
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ==============================================================================
# FUNCTIONS
# ==============================================================================

print_header() {
    echo ""
    echo -e "${BLUE}+================================================================+${NC}"
    echo -e "${BLUE}|              CERVELLASWARM ALERT CHECK                        |${NC}"
    echo -e "${BLUE}+================================================================+${NC}"
    echo ""
}

check_db() {
    local db_path="${HOME}/.swarm/logs/swarm_events.db"

    if [ -f "$db_path" ]; then
        echo -e "${GREEN}[OK]${NC} Database trovato: $db_path"
        return 0
    else
        echo -e "${YELLOW}[!]${NC} Database non trovato: $db_path"
        echo -e "    Il sistema di logging potrebbe non essere attivo."
        return 1
    fi
}

run_check() {
    cd "$PROJECT_ROOT"
    PYTHONPATH="$PROJECT_ROOT/src" python3 -c "
from alerting import AlertSystem
system = AlertSystem()
alerts = system.run_checks()
print(f'\\nFound {len(alerts)} alert(s)')
"
}

run_patterns() {
    cd "$PROJECT_ROOT"
    PYTHONPATH="$PROJECT_ROOT/src" python3 -c "
from alerting.detectors import PatternDetector
from pathlib import Path

db_path = str(Path.home() / '.swarm' / 'logs' / 'swarm_events.db')
detector = PatternDetector(db_path)
patterns = detector.detect_all()

print(f'\\nDetected {len(patterns)} pattern(s)')
for p in patterns:
    print(f'  [{p.severity}] {p.pattern_type}: {p.description}')
"
}

run_monitor() {
    cd "$PROJECT_ROOT"
    PYTHONPATH="$PROJECT_ROOT/src" python3 -c "
from alerting import AlertSystem
system = AlertSystem()
system.start_monitoring()
"
}

# ==============================================================================
# MAIN
# ==============================================================================

print_header

# Check database exists
check_db || {
    echo ""
    echo -e "${YELLOW}Continuando comunque...${NC}"
    echo ""
}

case "${1:-}" in
    --monitor|-m)
        echo "Avviando monitoring continuo (Ctrl+C per fermare)..."
        run_monitor
        ;;
    --patterns|-p)
        echo "Eseguendo pattern detection..."
        run_patterns
        ;;
    *)
        echo "Eseguendo check singolo..."
        run_check
        ;;
esac

echo ""
echo -e "${BLUE}+================================================================+${NC}"
echo ""
