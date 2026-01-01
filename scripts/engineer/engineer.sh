#!/bin/bash
# 🔧 L'Ingegnera - Helper Script
# Quick wrapper per analyze_codebase.py

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ANALYZE_SCRIPT="$SCRIPT_DIR/analyze_codebase.py"

# Default: progetto corrente
PROJECT="${1:-.}"

# Default output: docs/engineering/audit-[DATE].md
DATE=$(date +%Y-%m-%d)
OUTPUT="docs/engineering/audit-$DATE.md"

echo "🔧 L'Ingegnera - Engineering Audit"
echo "📂 Progetto: $PROJECT"
echo "📋 Output: $OUTPUT"
echo ""

# Crea directory se non esiste
mkdir -p "$(dirname "$OUTPUT")"

# Esegui analisi
python3 "$ANALYZE_SCRIPT" "$PROJECT" --output "$OUTPUT"

# Se successo, mostra path
if [ $? -eq 0 ]; then
  echo ""
  echo "✅ Report salvato in: $OUTPUT"
  echo ""
  echo "Per vedere il report:"
  echo "  cat $OUTPUT"
  echo ""
  echo "Per vedere solo issues CRITICHE:"
  echo "  grep -A 10 '🔴 CRITICO' $OUTPUT"
fi
