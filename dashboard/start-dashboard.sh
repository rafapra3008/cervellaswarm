#!/bin/bash
# ============================================
# CERVELLASWARM DASHBOARD - AVVIO COMPLETO
# ============================================
#
# Questo script avvia:
# - Backend FastAPI su porta 8100
# - Frontend React su porta 5173
#
# PORTE DEDICATE:
# - 8100 = CervellaSwarm Dashboard API
# - 5173 = CervellaSwarm Dashboard Frontend
# - 8000 = Contabilita' (NON TOCCARE!)
#
# ============================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
API_DIR="$SCRIPT_DIR/api"
FRONTEND_DIR="$SCRIPT_DIR/frontend"

echo ""
echo "============================================"
echo "  CERVELLASWARM DASHBOARD"
echo "  La MAPPA visuale dello sciame!"
echo "============================================"
echo ""

# Funzione per cleanup quando si chiude
cleanup() {
    echo ""
    echo "Chiusura Dashboard..."
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    echo "Dashboard chiusa. Arrivederci!"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Controlla dipendenze
echo "[1/4] Verifico dipendenze..."

if ! command -v uvicorn &> /dev/null; then
    echo "  Installazione dipendenze Python..."
    pip install -r "$API_DIR/requirements.txt" -q
fi

if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
    echo "  Installazione dipendenze Node..."
    cd "$FRONTEND_DIR" && npm install
fi

echo "  OK!"

# Avvia Backend
echo ""
echo "[2/4] Avvio Backend API (porta 8100)..."
cd "$API_DIR"
uvicorn main:app --host 0.0.0.0 --port 8100 --reload &
BACKEND_PID=$!
sleep 2

# Verifica Backend
if curl -s http://localhost:8100/health > /dev/null 2>&1; then
    echo "  Backend OK! http://localhost:8100"
else
    echo "  Backend in avvio..."
fi

# Avvia Frontend
echo ""
echo "[3/4] Avvio Frontend (porta 5173)..."
cd "$FRONTEND_DIR"
npm run dev &
FRONTEND_PID=$!
sleep 3

echo ""
echo "[4/4] Dashboard PRONTA!"
echo ""
echo "============================================"
echo ""
echo "  DASHBOARD:  http://localhost:5173"
echo "  API DOCS:   http://localhost:8100/docs"
echo ""
echo "  Press Ctrl+C to stop"
echo ""
echo "============================================"
echo ""
echo "  'Prima la MAPPA, poi il VIAGGIO!'"
echo ""

# Aspetta
wait
