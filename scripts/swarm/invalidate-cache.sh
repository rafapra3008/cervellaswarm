#!/bin/bash
# Script: Invalidate Claude Code Prompt Cache
# Autore: Cervella Researcher
# Data: 11 Gennaio 2026
#
# SCOPO:
#   Triggera invalidation della cache modificando temporaneamente CLAUDE.md
#   Utile prima di task importanti o quando context > 70%
#
# USO:
#   ./scripts/swarm/invalidate-cache.sh
#
# COSA FA:
#   1. Aggiunge timestamp temporaneo a CLAUDE.md
#   2. Aspetta 10 secondi (permette cache invalidation)
#   3. Ripristina CLAUDE.md originale
#   4. Result: Cache invalidata, pronta per nuova sessione!

set -e

CLAUDE_MD="$HOME/.claude/CLAUDE.md"
BACKUP_FILE="/tmp/claude_md_backup_$(date +%s).md"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔄 CACHE INVALIDATION - CervellaSwarm"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Verifica che CLAUDE.md esista
if [ ! -f "$CLAUDE_MD" ]; then
  echo "❌ ERRORE: $CLAUDE_MD non trovato!"
  exit 1
fi

# Backup del file originale
echo "📋 Backup CLAUDE.md → $BACKUP_FILE"
cp "$CLAUDE_MD" "$BACKUP_FILE"

# Aggiunge timestamp temporaneo (invalida cache system)
echo "" >> "$CLAUDE_MD"
echo "<!-- Cache invalidation trigger: $(date '+%Y-%m-%d %H:%M:%S') -->" >> "$CLAUDE_MD"

echo "✅ CLAUDE.md modificato"
echo ""
echo "⏱️  Aspetto 10 secondi per cache invalidation..."
echo "   (Questo permette a Claude Code di rilevare la modifica)"
echo ""

# Progress bar visuale
for i in {1..10}; do
  echo -n "▓"
  sleep 1
done
echo ""
echo ""

# Ripristina file originale
echo "🔙 Ripristino CLAUDE.md originale"
cp "$BACKUP_FILE" "$CLAUDE_MD"

# Cleanup backup
rm "$BACKUP_FILE"

echo "✅ File ripristinato"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ CACHE INVALIDATA!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Prossimo messaggio a Claude Code userà cache pulita."
echo "Context dovrebbe scendere da ~70% a ~50% (core base)."
echo ""
echo "💡 TIP: Controlla context usage nella statusbar di Claude Code"
echo "        per confermare la riduzione."
echo ""
