#!/bin/bash
# sync-agents.sh - Verifica e sincronizza agenti main <-> insiders
# Previene bug S358: 13 agenti insiders non sincronizzati
# Usage: ./scripts/sncp/sync-agents.sh [--sync] [--dry-run] [--verbose]
#
# Senza flag: solo report divergenze
# --sync: copia agenti da main a insiders (main e la fonte di verita)
# --dry-run: mostra cosa farebbe --sync senza eseguire
# --verbose: mostra dettagli per ogni agente

set -euo pipefail

MAIN_DIR="$HOME/.claude/agents"
INSIDERS_DIR="$HOME/.claude-insiders/agents"
SYNC_MODE=false
DRY_RUN=false
VERBOSE=false

# Parse args
for arg in "$@"; do
    case "$arg" in
        --sync) SYNC_MODE=true ;;
        --dry-run) DRY_RUN=true ;;
        --verbose) VERBOSE=true ;;
        -h|--help)
            echo "Usage: $0 [--sync] [--dry-run] [--verbose]"
            echo ""
            echo "  --sync     Copia agenti da main a insiders"
            echo "  --dry-run  Mostra cosa farebbe --sync senza eseguire"
            echo "  --verbose  Mostra dettagli per ogni agente"
            echo ""
            echo "Main ($MAIN_DIR) e la fonte di verita."
            exit 0
            ;;
        *)
            echo "Argomento sconosciuto: $arg"
            echo "Usa $0 --help per la lista completa."
            exit 1
            ;;
    esac
done

# Check directories exist
if [ ! -d "$MAIN_DIR" ]; then
    echo "ERRORE: Directory main non trovata: $MAIN_DIR"
    exit 1
fi

if [ ! -d "$INSIDERS_DIR" ]; then
    echo "ERRORE: Directory insiders non trovata: $INSIDERS_DIR"
    exit 1
fi

# Count agents
TOTAL=0
OK=0
DIVERGENT=0
MISSING_INSIDERS=0
EXTRA_INSIDERS=0
SYNCED=0

# Check each agent in main
for agent_file in "$MAIN_DIR"/*.md; do
    [ -f "$agent_file" ] || continue
    filename=$(basename "$agent_file")
    TOTAL=$((TOTAL + 1))

    insiders_file="$INSIDERS_DIR/$filename"

    if [ ! -f "$insiders_file" ]; then
        MISSING_INSIDERS=$((MISSING_INSIDERS + 1))
        echo "MISSING in insiders: $filename"

        if $DRY_RUN; then
            echo "  -> [DRY-RUN] COPIEREBBE a insiders"
        elif $SYNC_MODE; then
            cp "$agent_file" "$insiders_file"
            SYNCED=$((SYNCED + 1))
            echo "  -> COPIATO a insiders"
        fi
    elif ! diff -q "$agent_file" "$insiders_file" > /dev/null 2>&1; then
        DIVERGENT=$((DIVERGENT + 1))
        if $VERBOSE; then
            main_lines=$(wc -l < "$agent_file" | tr -d ' ')
            insiders_lines=$(wc -l < "$insiders_file" | tr -d ' ')
            echo "DIVERGENT: $filename (main: ${main_lines}L, insiders: ${insiders_lines}L)"
        else
            echo "DIVERGENT: $filename"
        fi

        if $DRY_RUN; then
            echo "  -> [DRY-RUN] SINCRONIZZEREBBE da main"
        elif $SYNC_MODE; then
            cp "$agent_file" "$insiders_file"
            SYNCED=$((SYNCED + 1))
            echo "  -> SINCRONIZZATO da main"
        fi
    else
        OK=$((OK + 1))
        if $VERBOSE; then
            echo "OK: $filename"
        fi
    fi
done

# Check for extra agents in insiders (not in main)
for insiders_file in "$INSIDERS_DIR"/*.md; do
    [ -f "$insiders_file" ] || continue
    filename=$(basename "$insiders_file")
    main_file="$MAIN_DIR/$filename"

    if [ ! -f "$main_file" ]; then
        EXTRA_INSIDERS=$((EXTRA_INSIDERS + 1))
        echo "EXTRA in insiders (not in main): $filename"
    fi
done

# Summary
echo ""
echo "=== Sync Report ==="
echo "Total agenti main: $TOTAL"
echo "OK (identici):     $OK"
echo "Divergenti:        $DIVERGENT"
echo "Missing insiders:  $MISSING_INSIDERS"
echo "Extra insiders:    $EXTRA_INSIDERS"

if $SYNC_MODE && [ $SYNCED -gt 0 ]; then
    echo "Sincronizzati:     $SYNCED"
fi

# Exit code
if [ $DIVERGENT -eq 0 ] && [ $MISSING_INSIDERS -eq 0 ] && [ $EXTRA_INSIDERS -eq 0 ]; then
    echo ""
    echo "Tutto OK! $OK/$TOTAL agenti sincronizzati."
    exit 0
else
    echo ""
    ISSUES=$((DIVERGENT + MISSING_INSIDERS + EXTRA_INSIDERS))
    if $SYNC_MODE && [ $SYNCED -gt 0 ]; then
        echo "Fixati $SYNCED/$ISSUES issue. Ri-esegui senza --sync per verificare."
    elif $SYNC_MODE; then
        echo "$ISSUES issue trovati (extra in insiders - richiede intervento manuale)."
    else
        echo "$ISSUES issue trovati. Usa --sync per sincronizzare."
    fi
    exit 1
fi
