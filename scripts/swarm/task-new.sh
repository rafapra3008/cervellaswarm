#!/bin/bash
#
# task-new.sh - Crea task da template
# Versione: 1.0.0
# Data: 6 Gennaio 2026
#
# Uso: task-new <tipo> "<titolo>" [--spawn]
# Tipi: ricerca, bug, feature, review
#

set -e

# Colori
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m'

TEMPLATES_DIR="$HOME/.claude/scripts/templates"
VERSION="1.0.0"

# Determina directory task
if [ -d ".swarm/tasks" ]; then
    TASKS_DIR=".swarm/tasks"
elif [ -d "$HOME/Developer/CervellaSwarm/.swarm/tasks" ]; then
    TASKS_DIR="$HOME/Developer/CervellaSwarm/.swarm/tasks"
else
    TASKS_DIR=".swarm/tasks"
    mkdir -p "$TASKS_DIR"
fi

show_help() {
    echo ""
    echo -e "${GREEN}task-new${NC} - Crea task da template in 5 secondi!"
    echo ""
    echo "Uso: task-new <tipo> \"<titolo>\" [--spawn]"
    echo ""
    echo "Tipi disponibili:"
    echo "  ricerca   - Ricerca approfondita (-> cervella-researcher)"
    echo "  bug       - Fix bug (-> cervella-backend/frontend)"
    echo "  feature   - Nuova feature (-> cervella-backend/frontend)"
    echo "  review    - Code review (-> cervella-reviewer)"
    echo ""
    echo "Opzioni:"
    echo "  --spawn   Lancia worker automaticamente dopo creazione"
    echo ""
    echo "Esempi:"
    echo "  task-new ricerca \"studio performance database\""
    echo "  task-new bug \"fix login timeout\" --spawn"
    echo "  task-new feature \"aggiungere dark mode\""
    echo ""
}

get_template() {
    case "$1" in
        ricerca|research)
            echo "TASK_TEMPLATE_RICERCA.md"
            ;;
        bug|fix)
            echo "TASK_TEMPLATE_FIX_BUG.md"
            ;;
        feature|feat)
            echo "TASK_TEMPLATE_FEATURE.md"
            ;;
        review)
            echo "TASK_TEMPLATE_REVIEW.md"
            ;;
        *)
            echo ""
            ;;
    esac
}

get_worker() {
    case "$1" in
        ricerca|research)
            echo "researcher"
            ;;
        bug|fix)
            echo "backend"
            ;;
        feature|feat)
            echo "backend"
            ;;
        review)
            echo "reviewer"
            ;;
        *)
            echo ""
            ;;
    esac
}

# Validazione argomenti
if [ $# -lt 2 ]; then
    show_help
    exit 1
fi

TYPE="$1"
TITLE="$2"
SPAWN_AFTER=false

# Check --spawn flag
if [ "${3:-}" = "--spawn" ]; then
    SPAWN_AFTER=true
fi

# Trova template
TEMPLATE=$(get_template "$TYPE")
if [ -z "$TEMPLATE" ]; then
    echo -e "${RED}[ERRORE]${NC} Tipo sconosciuto: $TYPE"
    echo "Tipi validi: ricerca, bug, feature, review"
    exit 1
fi

TEMPLATE_PATH="$TEMPLATES_DIR/$TEMPLATE"
if [ ! -f "$TEMPLATE_PATH" ]; then
    echo -e "${RED}[ERRORE]${NC} Template non trovato: $TEMPLATE_PATH"
    exit 1
fi

# Genera nome file
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SAFE_TITLE=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | tr ' ' '_' | tr -cd '[:alnum:]_')
TASK_FILE="TASK_${TIMESTAMP}_${SAFE_TITLE}.md"
TASK_PATH="$TASKS_DIR/$TASK_FILE"

# Copia template e sostituisci placeholders
cp "$TEMPLATE_PATH" "$TASK_PATH"

# Sostituisci placeholder (compatibile macOS e Linux)
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/{{TITOLO}}/$TITLE/g" "$TASK_PATH"
    sed -i '' "s/{{DATA}}/$(date '+%Y-%m-%d %H:%M')/g" "$TASK_PATH"
else
    sed -i "s/{{TITOLO}}/$TITLE/g" "$TASK_PATH"
    sed -i "s/{{DATA}}/$(date '+%Y-%m-%d %H:%M')/g" "$TASK_PATH"
fi

# Marca come ready
touch "${TASK_PATH%.md}.ready"

echo -e "${GREEN}[OK]${NC} Task creato: $TASK_FILE"
echo -e "     Path: $TASK_PATH"

# Spawn worker se richiesto
if [ "$SPAWN_AFTER" = true ]; then
    WORKER=$(get_worker "$TYPE")
    echo -e "${GREEN}[i]${NC} Lancio worker: cervella-$WORKER"
    spawn-workers "--$WORKER"
else
    WORKER=$(get_worker "$TYPE")
    echo ""
    echo -e "${YELLOW}[TIP]${NC} Per lanciare il worker:"
    echo -e "     spawn-workers --$WORKER"
fi
