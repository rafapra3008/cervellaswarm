#!/bin/bash
# health-check.sh - Verifica sintassi file Python
# Creato da: cervella-devops
# Data: 2026-01-04

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== Health Check - Verifica Sintassi Python ==="
echo "Directory: $PROJECT_DIR"
echo ""

# Trova tutti i file Python
PYTHON_FILES=$(find "$PROJECT_DIR" -name "*.py" -type f 2>/dev/null)

if [ -z "$PYTHON_FILES" ]; then
    echo "Nessun file Python trovato."
    exit 0
fi

ERRORS=0
CHECKED=0

for file in $PYTHON_FILES; do
    CHECKED=$((CHECKED + 1))
    if python3 -m py_compile "$file" 2>/dev/null; then
        echo "[OK] $file"
    else
        echo "[ERRORE] $file"
        ERRORS=$((ERRORS + 1))
    fi
done

echo ""
echo "=== Risultato ==="
echo "File controllati: $CHECKED"
echo "Errori: $ERRORS"

if [ $ERRORS -gt 0 ]; then
    echo "STATO: FALLITO"
    exit 1
else
    echo "STATO: OK"
    exit 0
fi
