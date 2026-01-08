#!/bin/bash

# swarm-helper.sh - Helper comandi rapidi per CervellaSwarm
# Versione: 1.0.0
# Data: 8 Gennaio 2026

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Trova root progetto (cerca .swarm/)
find_project_root() {
    local dir="$PWD"
    while [[ "$dir" != "/" ]]; do
        if [[ -d "$dir/.swarm" ]]; then
            echo "$dir"
            return 0
        fi
        dir=$(dirname "$dir")
    done
    echo ""
    return 1
}

PROJECT_ROOT=$(find_project_root)
if [[ -z "$PROJECT_ROOT" ]]; then
    echo -e "${RED}[X]${NC} Non in progetto CervellaSwarm (.swarm/ non trovato)"
    echo -e "${YELLOW}[!]${NC} Crea struttura con: mkdir -p .swarm/{tasks,feedback,logs}"
    exit 1
fi

TASKS_DIR="$PROJECT_ROOT/.swarm/tasks"
TEMPLATES_DIR="$PROJECT_ROOT/.swarm/templates"

# Help
show_help() {
    cat << EOF
${MAGENTA}
==============================================
  SWARM HELPER - Comandi Rapidi
  CervellaSwarm v1.0.0
==============================================
${NC}

${CYAN}TASK MANAGEMENT:${NC}
  swarm task list              Lista tutti i task
  swarm task status            Status task (ready/working/done)
  swarm task create [tipo]     Crea task da template
  swarm task clean             Pulisci task vecchi

${CYAN}WORKER MANAGEMENT:${NC}
  swarm worker list            Lista worker disponibili
  swarm worker status          Worker attivi
  swarm worker spawn [tipo]    Spawna worker

${CYAN}MONITORING:${NC}
  swarm status                 Status generale sistema
  swarm logs                   Mostra ultimi log

${CYAN}CLEANUP:${NC}
  swarm clean                  Pulizia generale
  swarm clean tasks            Solo task vecchi
  swarm clean logs             Solo log vecchi

${CYAN}EXAMPLES:${NC}
  swarm task create ricerca    Crea task ricerca da template
  swarm worker spawn backend   Spawna backend worker
  swarm status                 Mostra tutto

EOF
}

# Task list
task_list() {
    echo -e "${CYAN}[i]${NC} Task in $TASKS_DIR"
    echo ""

    local total=$(find "$TASKS_DIR" -name "*.md" -not -name "TEMPLATE_*" | wc -l | tr -d ' ')
    local ready=$(find "$TASKS_DIR" -name "*.ready" | wc -l | tr -d ' ')
    local working=$(find "$TASKS_DIR" -name "*.working" | wc -l | tr -d ' ')
    local done=$(find "$TASKS_DIR" -name "*.done" | wc -l | tr -d ' ')

    echo -e "  ${BLUE}Total:${NC} $total task"
    echo -e "  ${YELLOW}Ready:${NC} $ready task"
    echo -e "  ${CYAN}Working:${NC} $working task"
    echo -e "  ${GREEN}Done:${NC} $done task"
    echo ""

    if [[ $total -gt 0 ]]; then
        echo -e "${CYAN}[i]${NC} Task file:"
        find "$TASKS_DIR" -name "*.md" -not -name "TEMPLATE_*" -exec basename {} .md \; | sort
    fi
}

# Task status
task_status() {
    echo -e "${CYAN}[i]${NC} Task Status"
    echo ""

    echo -e "${YELLOW}⏳ READY:${NC}"
    for ready in "$TASKS_DIR"/*.ready; do
        [[ -e "$ready" ]] || continue
        local name=$(basename "$ready" .ready)
        echo "  - $name"
    done

    echo ""
    echo -e "${CYAN}🔄 WORKING:${NC}"
    for working in "$TASKS_DIR"/*.working; do
        [[ -e "$working" ]] || continue
        local name=$(basename "$working" .working)
        echo "  - $name"
    done

    echo ""
    echo -e "${GREEN}✅ DONE:${NC}"
    for done in "$TASKS_DIR"/*.done; do
        [[ -e "$done" ]] || continue
        local name=$(basename "$done" .done)
        local date=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M" "$done" 2>/dev/null || stat -c "%y" "$done" 2>/dev/null | cut -d'.' -f1)
        echo "  - $name ($date)"
    done | tail -10
}

# Task create
task_create() {
    local tipo="$1"

    if [[ -z "$tipo" ]]; then
        echo -e "${YELLOW}[!]${NC} Specifica tipo task"
        echo ""
        echo "Tipi disponibili:"
        if [[ -d "$TEMPLATES_DIR" ]]; then
            find "$TEMPLATES_DIR" -name "TEMPLATE_TASK_*.md" -exec basename {} \; | sed 's/TEMPLATE_TASK_/  - /' | sed 's/.md//' | tr '[:upper:]' '[:lower:]'
        else
            echo "  - ricerca"
            echo "  - implementazione"
            echo "  - bugfix"
            echo "  - review"
            echo "  - docs"
            echo "  - hardtest"
        fi
        echo ""
        echo "Uso: swarm task create [tipo]"
        return 1
    fi

    # Map tipo a template
    local template_name=""
    case "${tipo,,}" in  # Lowercase
        ricerca|researcher)
            template_name="TEMPLATE_TASK_RICERCA_TECNICA.md"
            ;;
        implementazione|impl|backend|frontend)
            template_name="TEMPLATE_TASK_IMPLEMENTAZIONE.md"
            ;;
        bug|bugfix|fix)
            template_name="TEMPLATE_TASK_BUG_FIX.md"
            ;;
        review|code-review)
            template_name="TEMPLATE_TASK_CODE_REVIEW.md"
            ;;
        docs|doc|documentazione)
            template_name="TEMPLATE_TASK_DOCUMENTAZIONE.md"
            ;;
        hardtest|test)
            template_name="TEMPLATE_TASK_HARDTEST.md"
            ;;
        *)
            echo -e "${RED}[X]${NC} Tipo '$tipo' non riconosciuto"
            return 1
            ;;
    esac

    local template_path="$TEMPLATES_DIR/$template_name"
    if [[ ! -f "$template_path" ]]; then
        echo -e "${RED}[X]${NC} Template non trovato: $template_path"
        echo -e "${YELLOW}[!]${NC} Copia template da CervellaSwarm con:"
        echo "    cp ~/Developer/CervellaSwarm/.swarm/templates/* .swarm/templates/"
        return 1
    fi

    # Genera nome file
    local timestamp=$(date +%s)
    local task_name="TASK_${tipo^^}_$timestamp"
    local task_path="$TASKS_DIR/${task_name}.md"

    cp "$template_path" "$task_path"

    echo -e "${GREEN}[OK]${NC} Task creato: $task_name"
    echo -e "${CYAN}[i]${NC} File: $task_path"
    echo ""
    echo -e "${YELLOW}[!]${NC} Prossimi step:"
    echo "  1. Modifica file task (sostituisci [PLACEHOLDER])"
    echo "  2. Marca ready: touch $TASKS_DIR/${task_name}.ready"
    echo "  3. Spawna worker appropriato"
    echo ""
    echo "Apri con: ${CYAN}open $task_path${NC}"
}

# Worker list
worker_list() {
    spawn-workers --list
}

# Worker status
worker_status() {
    echo -e "${CYAN}[i]${NC} Worker Attivi"
    echo ""

    local count=$(tmux list-sessions 2>/dev/null | grep -c "swarm_" || echo "0")

    if [[ $count -eq 0 ]]; then
        echo -e "${YELLOW}[!]${NC} Nessun worker attivo"
        echo ""
        echo "Spawna worker con: swarm worker spawn [tipo]"
    else
        echo -e "${GREEN}[OK]${NC} $count worker attivi:"
        tmux list-sessions 2>/dev/null | grep "swarm_" | awk '{print "  - " $1}' | sed 's/://'
    fi
}

# Worker spawn
worker_spawn() {
    local tipo="$1"

    if [[ -z "$tipo" ]]; then
        echo -e "${YELLOW}[!]${NC} Specifica tipo worker"
        echo ""
        echo "Uso: swarm worker spawn [tipo]"
        echo "Tipi: backend, frontend, docs, researcher, tester, etc."
        echo ""
        echo "Lista completa: swarm worker list"
        return 1
    fi

    spawn-workers --"$tipo"
}

# Status generale
show_status() {
    echo -e "${MAGENTA}
==============================================
  SWARM STATUS - Sistema Generale
==============================================
${NC}"

    # Agents
    echo -e "${CYAN}📋 AGENTS:${NC}"
    local agents_count=$(ls ~/.claude/agents/*.md 2>/dev/null | wc -l | tr -d ' ')
    echo -e "  Installati: ${GREEN}$agents_count${NC}/16"

    # Tasks
    echo ""
    echo -e "${CYAN}📋 TASKS:${NC}"
    local total=$(find "$TASKS_DIR" -name "*.md" -not -name "TEMPLATE_*" 2>/dev/null | wc -l | tr -d ' ')
    local ready=$(find "$TASKS_DIR" -name "*.ready" 2>/dev/null | wc -l | tr -d ' ')
    local working=$(find "$TASKS_DIR" -name "*.working" 2>/dev/null | wc -l | tr -d ' ')
    local done=$(find "$TASKS_DIR" -name "*.done" 2>/dev/null | wc -l | tr -d ' ')
    echo -e "  Total: $total | Ready: ${YELLOW}$ready${NC} | Working: ${CYAN}$working${NC} | Done: ${GREEN}$done${NC}"

    # Workers
    echo ""
    echo -e "${CYAN}🐝 WORKERS:${NC}"
    local workers=$(tmux list-sessions 2>/dev/null | grep -c "swarm_" || echo "0")
    if [[ $workers -gt 0 ]]; then
        echo -e "  Attivi: ${GREEN}$workers${NC}"
    else
        echo -e "  Attivi: ${YELLOW}0${NC}"
    fi

    # Watcher
    echo ""
    echo -e "${CYAN}👁️  WATCHER:${NC}"
    local watcher_count=$(ps aux | grep watcher-regina | grep -v grep | wc -l | tr -d ' ')
    if [[ $watcher_count -gt 0 ]]; then
        echo -e "  Status: ${GREEN}ATTIVO${NC} ($watcher_count istanze)"
    else
        echo -e "  Status: ${YELLOW}NON ATTIVO${NC}"
    fi

    # Memoria
    echo ""
    echo -e "${CYAN}🧠 MEMORIA:${NC}"
    if [[ -f "$PROJECT_ROOT/data/swarm_memory.db" ]]; then
        local lessons=$(sqlite3 "$PROJECT_ROOT/data/swarm_memory.db" "SELECT COUNT(*) FROM lessons_learned" 2>/dev/null || echo "?")
        echo -e "  Lezioni apprese: ${GREEN}$lessons${NC}"
    else
        echo -e "  Database: ${YELLOW}Non presente${NC}"
    fi

    echo ""
    echo -e "${GREEN}[OK]${NC} Sistema operativo!"
}

# Logs
show_logs() {
    local log_file="$PROJECT_ROOT/.swarm/logs/swarm.log"

    if [[ -f "$log_file" ]]; then
        echo -e "${CYAN}[i]${NC} Ultimi 20 log:"
        echo ""
        tail -20 "$log_file"
    else
        echo -e "${YELLOW}[!]${NC} Nessun log trovato"
    fi
}

# Clean
clean_all() {
    echo -e "${CYAN}[i]${NC} Pulizia generale..."

    # Task done vecchi (>7 giorni)
    local task_count=$(find "$TASKS_DIR" -name "*.done" -mtime +7 2>/dev/null | wc -l | tr -d ' ')
    if [[ $task_count -gt 0 ]]; then
        find "$TASKS_DIR" -name "*.done" -mtime +7 -delete
        find "$TASKS_DIR" -name "*.working" -mtime +7 -delete
        find "$TASKS_DIR" -name "*.ready" -mtime +7 -delete
        echo -e "${GREEN}[OK]${NC} Rimossi $task_count task vecchi (>7 giorni)"
    fi

    # Log vecchi (>30 giorni)
    local log_count=$(find "$PROJECT_ROOT/.swarm/logs" -name "*.log" -mtime +30 2>/dev/null | wc -l | tr -d ' ')
    if [[ $log_count -gt 0 ]]; then
        find "$PROJECT_ROOT/.swarm/logs" -name "*.log" -mtime +30 -delete
        echo -e "${GREEN}[OK]${NC} Rimossi $log_count log vecchi (>30 giorni)"
    fi

    echo -e "${GREEN}[OK]${NC} Pulizia completata!"
}

# Main
CMD="${1:-help}"
shift || true

case "$CMD" in
    help|--help|-h)
        show_help
        ;;
    task)
        SUBCMD="${1:-list}"
        shift || true
        case "$SUBCMD" in
            list) task_list ;;
            status) task_status ;;
            create) task_create "$@" ;;
            clean) find "$TASKS_DIR" -name "*.done" -mtime +7 -delete && echo "Cleaned!" ;;
            *) echo "Unknown: swarm task $SUBCMD"; exit 1 ;;
        esac
        ;;
    worker)
        SUBCMD="${1:-list}"
        shift || true
        case "$SUBCMD" in
            list) worker_list ;;
            status) worker_status ;;
            spawn) worker_spawn "$@" ;;
            *) echo "Unknown: swarm worker $SUBCMD"; exit 1 ;;
        esac
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs
        ;;
    clean)
        clean_all
        ;;
    *)
        echo -e "${RED}[X]${NC} Comando sconosciuto: $CMD"
        echo ""
        show_help
        exit 1
        ;;
esac
