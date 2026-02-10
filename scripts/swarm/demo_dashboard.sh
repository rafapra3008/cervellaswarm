#!/bin/bash
#
# Demo Dashboard - Simula attività dello sciame
#
# Questo script crea alcuni task di esempio e li segna come
# working/done per mostrare la dashboard in azione.
#

set -e

echo "🐝 CervellaSwarm Dashboard Demo"
echo ""
echo "Creo task di esempio..."

# Cleanup vecchi task demo
python3 task_manager.py cleanup TASK_DEMO1 2>/dev/null || true
python3 task_manager.py cleanup TASK_DEMO2 2>/dev/null || true
python3 task_manager.py cleanup TASK_DEMO3 2>/dev/null || true

# Rimuovi file se esistono
rm -f .swarm/tasks/TASK_DEMO*.md
rm -f .swarm/tasks/TASK_DEMO*.ready
rm -f .swarm/tasks/TASK_DEMO*.working
rm -f .swarm/tasks/TASK_DEMO*.done
rm -f .swarm/tasks/TASK_DEMO*.ack_*

# Crea 3 task demo (usa TASK_ prefix per essere riconosciuti)
echo "Creando TASK_DEMO1 (backend)..."
python3 task_manager.py create TASK_DEMO1 cervella-backend "Implementare endpoint API users" 1

echo "Creando TASK_DEMO2 (frontend)..."
python3 task_manager.py create TASK_DEMO2 cervella-frontend "Creare form login" 2

echo "Creando TASK_DEMO3 (tester)..."
python3 task_manager.py create TASK_DEMO3 cervella-tester "Test integrazione" 1

# Simula workflow
echo ""
echo "Simulando workflow..."
echo ""

# Task 1: READY → WORKING
python3 task_manager.py ready TASK_DEMO1
echo "✓ TASK_DEMO1 → READY"
sleep 1

python3 task_manager.py working TASK_DEMO1
echo "✓ TASK_DEMO1 → WORKING"
sleep 1

# Task 2: READY
python3 task_manager.py ready TASK_DEMO2
echo "✓ TASK_DEMO2 → READY"
sleep 1

# Mostra dashboard
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  DASHBOARD SNAPSHOT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
python3 -m scripts.swarm.dashboard.cli
echo ""

# Task 1: DONE
python3 task_manager.py done TASK_DEMO1
echo "✓ TASK_DEMO1 → DONE"
sleep 1

# Task 2: WORKING
python3 task_manager.py working TASK_DEMO2
echo "✓ TASK_DEMO2 → WORKING"
sleep 1

# Mostra dashboard aggiornata
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  DASHBOARD SNAPSHOT (Aggiornata)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
python3 -m scripts.swarm.dashboard.cli
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Demo completata!"
echo ""
echo "  Prova ora:"
echo "    ./dashboard.sh --watch    # Watch mode con refresh"
echo "    ./dashboard.sh --json     # Output JSON"
echo ""
echo "  Cleanup task demo:"
echo "    rm -f .swarm/tasks/TASK_DEMO*"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
