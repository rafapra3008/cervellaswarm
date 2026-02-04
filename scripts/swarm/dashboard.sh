#!/bin/bash
#
# CervellaSwarm Dashboard - Wrapper Bash
#
# Wrapper per il modulo dashboard (refactoring S335).
# Assicura di essere nella directory corretta per import Python.
#

__version__="2.0.0"
__version_date__="2026-02-04"

# Trova la directory base di CervellaSwarm
SWARM_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

# Esegui il modulo dashboard passando tutti gli argomenti
cd "$SWARM_DIR"
exec python3 -m scripts.swarm.dashboard.cli "$@"
