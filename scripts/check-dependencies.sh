#!/bin/bash
# check-dependencies.sh - Verifica dipendenze di un task
# Controlla se tutti i segnali richiesti sono presenti
#
# Uso: check-dependencies.sh TASK_ID [PROJECT_PATH]
#
# Il task deve essere definito in .swarm/dipendenze/sessione_corrente.md
# o passare le dipendenze come variabile ambiente TASK_DEPS
#
# Esempi:
#   check-dependencies.sh TASK-002
#   check-dependencies.sh TASK-003 /path/to/project
#   TASK_DEPS="TASK-001,TASK-002" check-dependencies.sh TASK-003
#
# CervellaSwarm Multi-Instance Coordination v2.0

set -e

# Colori
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
BLUE='\033[0;34m'
NC='\033[0m'

# Parametri
TASK_ID="${1:-}"
PROJECT_PATH="${2:-.}"

# Validazione
if [ -z "$TASK_ID" ]; then
    echo -e "${RED}ERRORE: TASK_ID mancante${NC}"
    echo ""
    echo "Uso: check-dependencies.sh TASK_ID [PROJECT_PATH]"
    echo ""
    echo "Esempi:"
    echo "  check-dependencies.sh TASK-002"
    echo "  TASK_DEPS=\"TASK-001\" check-dependencies.sh TASK-002"
    exit 1
fi

# Setup paths
PROJECT_PATH=$(cd "$PROJECT_PATH" && pwd)
SIGNALS_DIR="$PROJECT_PATH/.swarm/segnali"
DEPS_DIR="$PROJECT_PATH/.swarm/dipendenze"

# Header
echo ""
echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}   CHECK DIPENDENZE: $TASK_ID${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

# Trova dipendenze
DEPENDENCIES=""

# 1. Prima controlla variabile ambiente
if [ -n "$TASK_DEPS" ]; then
    DEPENDENCIES="$TASK_DEPS"
    echo -e "${BLUE}Dipendenze (da env):${NC} $DEPENDENCIES"
fi

# 2. Poi controlla sessione_corrente.md
if [ -z "$DEPENDENCIES" ] && [ -f "$DEPS_DIR/sessione_corrente.md" ]; then
    # Cerca la sezione del task
    DEPS_LINE=$(grep -A 3 "### $TASK_ID:" "$DEPS_DIR/sessione_corrente.md" 2>/dev/null | grep "Dipende da:" | head -1 || echo "")

    if [ -n "$DEPS_LINE" ]; then
        # Estrai dipendenze (formato: "- **Dipende da:** TASK-001, TASK-002")
        # Rimuovi markdown (**), trim spazi iniziali/finali
        DEPENDENCIES=$(echo "$DEPS_LINE" | sed 's/.*Dipende da:[[:space:]]*//' | sed 's/\*\*//g' | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')
        echo -e "${BLUE}Dipendenze (da file):${NC} $DEPENDENCIES"
    fi
fi

# 3. Controlla grafo.json
if [ -z "$DEPENDENCIES" ] && [ -f "$DEPS_DIR/grafo.json" ]; then
    # Estrai edges che puntano a questo task
    DEPS_FROM_GRAPH=$(jq -r ".edges[] | select(.[1] == \"$TASK_ID\") | .[0]" "$DEPS_DIR/grafo.json" 2>/dev/null | tr '\n' ',' | sed 's/,$//')
    if [ -n "$DEPS_FROM_GRAPH" ]; then
        DEPENDENCIES="$DEPS_FROM_GRAPH"
        echo -e "${BLUE}Dipendenze (da grafo):${NC} $DEPENDENCIES"
    fi
fi

# Nessuna dipendenza trovata
if [ -z "$DEPENDENCIES" ] || [ "$DEPENDENCIES" = "nessuno" ] || [ "$DEPENDENCIES" = "-" ]; then
    echo ""
    echo -e "${GREEN}Nessuna dipendenza trovata per $TASK_ID${NC}"
    echo -e "${GREEN}Puoi iniziare subito!${NC}"
    echo ""
    exit 0
fi

echo ""
echo -e "${YELLOW}Verifico dipendenze...${NC}"
echo ""

# Verifica ogni dipendenza
ALL_MET=true
MISSING=()
FOUND=()

# Converti in array (supporta virgola o spazio come separatore)
IFS=', ' read -ra DEPS_ARRAY <<< "$DEPENDENCIES"

for dep in "${DEPS_ARRAY[@]}"; do
    # Pulisci whitespace
    dep=$(echo "$dep" | tr -d '[:space:]')

    if [ -z "$dep" ]; then
        continue
    fi

    # Cerca segnale (pattern: DEP-complete.signal.json)
    SIGNAL_FILE="$SIGNALS_DIR/${dep}-complete.signal.json"

    if [ -f "$SIGNAL_FILE" ]; then
        # Verifica che sia success
        STATUS=$(jq -r '.status' "$SIGNAL_FILE" 2>/dev/null || echo "unknown")

        if [ "$STATUS" = "success" ]; then
            echo -e "  ${GREEN}OK${NC} $dep - COMPLETATO"
            FOUND+=("$dep")
        else
            echo -e "  ${RED}!!${NC} $dep - Status: $STATUS (non success)"
            MISSING+=("$dep")
            ALL_MET=false
        fi
    else
        echo -e "  ${YELLOW}..${NC} $dep - IN ATTESA"
        MISSING+=("$dep")
        ALL_MET=false
    fi
done

echo ""
echo "----------------------------------------"
echo ""

# Risultato finale
if [ "$ALL_MET" = true ]; then
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}   TUTTE LE DIPENDENZE SODDISFATTE!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "${GREEN}$TASK_ID puo' iniziare!${NC}"
    echo ""
    exit 0
else
    echo -e "${YELLOW}========================================${NC}"
    echo -e "${YELLOW}   DIPENDENZE MANCANTI${NC}"
    echo -e "${YELLOW}========================================${NC}"
    echo ""
    echo -e "Completate: ${#FOUND[@]}"
    echo -e "Mancanti:   ${#MISSING[@]}"
    echo ""
    echo -e "In attesa di:"
    for m in "${MISSING[@]}"; do
        echo -e "  - $m"
    done
    echo ""
    echo -e "${YELLOW}$TASK_ID deve aspettare.${NC}"
    echo ""
    exit 1
fi
