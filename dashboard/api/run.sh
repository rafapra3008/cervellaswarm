#!/bin/bash
# CervellaSwarm Dashboard API - Avvio

# Vai alla directory dello script
cd "$(dirname "$0")"

echo "=================================="
echo "CervellaSwarm Dashboard API"
echo "=================================="

# Controlla se uvicorn e' installato
if ! command -v uvicorn &> /dev/null; then
    echo "uvicorn non trovato. Installazione dipendenze..."
    pip install -r requirements.txt
fi

echo ""
echo "Avvio server su http://localhost:8100"
echo "Docs: http://localhost:8100/docs"
echo "Press Ctrl+C to stop"
echo ""
echo "NOTA: Porta 8100 dedicata a CervellaSwarm!"
echo "      (8000 e' riservata per Contabilita')"
echo ""

# Avvia uvicorn - PORTA 8100 DEDICATA CERVELLASWARM
uvicorn main:app --reload --host 0.0.0.0 --port 8100
