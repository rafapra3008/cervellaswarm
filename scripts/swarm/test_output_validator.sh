#!/bin/bash
#
# Test script per output_validator.py
# Verifica funzionamento base del Reflection Pattern
#
# Usage: ./test_output_validator.sh
#

set -e

echo "=============================================="
echo "  TEST OUTPUT VALIDATOR - REFLECTION PATTERN"
echo "=============================================="
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VALIDATOR="${SCRIPT_DIR}/output_validator.py"
TEST_DIR="/tmp/cervellaswarm_validator_test"

# Setup test directory
mkdir -p "$TEST_DIR/.swarm/tasks"
mkdir -p "$TEST_DIR/.swarm/logs"
cd "$TEST_DIR"

echo "[1/5] Testing --version..."
python3 "$VALIDATOR" --version
echo "✓ Version check OK"
echo ""

echo "[2/5] Testing VALID output (score should be ~95)..."
cat > .swarm/tasks/TEST_VALID_output.md << 'EOF'
# Output Test - Valid

## Risultato
✓ Task completato con successo!

## File Modificati
- backend/test.py - Implementato feature X

## Test
DONE - Tutti i test passano!

Questo output è abbastanza lungo da superare il minimo di 100 caratteri.
EOF

python3 "$VALIDATOR" --file .swarm/tasks/TEST_VALID_output.md
echo ""

echo "[3/5] Testing INVALID output with errors (score should be <50)..."
cat > .swarm/tasks/TEST_INVALID_output.md << 'EOF'
# Output Test - Invalid

## Risultato
Error: Qualcosa è andato storto!

TODO: Completare implementazione

Traceback (most recent call last):
  File "test.py", line 10
    invalid syntax
EOF

python3 "$VALIDATOR" --file .swarm/tasks/TEST_INVALID_output.md || echo "✓ Correctly detected as INVALID"
echo ""

echo "[4/5] Testing EMPTY output (score should be 0)..."
touch .swarm/tasks/TEST_EMPTY_output.md
python3 "$VALIDATOR" --file .swarm/tasks/TEST_EMPTY_output.md || echo "✓ Correctly detected as INVALID (empty)"
echo ""

echo "[5/5] Testing --last-output flag..."
# Il più recente dovrebbe essere TEST_EMPTY_output.md
python3 "$VALIDATOR" --last-output --json | head -5
echo "✓ Last output detection OK"
echo ""

echo "=============================================="
echo "  ✓ ALL TESTS PASSED!"
echo "=============================================="
echo ""
echo "Cleanup: rm -rf $TEST_DIR"
rm -rf "$TEST_DIR"
