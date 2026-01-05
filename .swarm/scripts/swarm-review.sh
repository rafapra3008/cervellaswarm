#!/bin/bash
#
# swarm-review.sh - Attiva le Guardiane per la review dei task completati
#
# CervellaSwarm - Le Guardiane verificano!
#
# Uso:
#   swarm-review              # Mostra stato review
#   swarm-review --start      # Avvia review (crea .review_ready + spawna Guardiana)
#   swarm-review --task NOME  # Review task specifico
#   swarm-review --help       # Mostra help
#
# Versione: 1.1.0
# Data: 2026-01-05
# Cervella & Rafa

set -e

# ============================================================================
# CONFIGURAZIONE CENTRALIZZATA
# ============================================================================

# Carica configurazione globale se esiste
SWARM_CONFIG="${SWARM_CONFIG:-$HOME/.swarm/config}"
if [[ -f "$SWARM_CONFIG" ]]; then
    source "$SWARM_CONFIG"
fi

# Colori (defaults se non definiti in config)
RED="${RED:-\033[0;31m}"
GREEN="${GREEN:-\033[0;32m}"
YELLOW="${YELLOW:-\033[1;33m}"
BLUE="${BLUE:-\033[0;34m}"
PURPLE="${PURPLE:-\033[0;35m}"
CYAN="${CYAN:-\033[0;36m}"
NC="${NC:-\033[0m}"

# Progetti (da config o defaults)
if [[ -z "${SWARM_PROJECTS[*]}" ]]; then
    SWARM_PROJECTS=(
        "$HOME/Developer/CervellaSwarm"
        "$HOME/Developer/miracollogeminifocus"
        "$HOME/Developer/ContabilitaAntigravity"
    )
fi
PROJECTS=("${SWARM_PROJECTS[@]}")

# ============================================================================
# FUNZIONI UTILITY
# ============================================================================

print_header() {
    echo -e "${PURPLE}"
    echo "=============================================="
    echo "  SWARM REVIEW"
    echo "  CervellaSwarm - Le Guardiane verificano!"
    echo "=============================================="
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[X]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[i]${NC} $1"
}

# Trova la root del progetto cercando .swarm/
find_project_root() {
    local search_dir="$(pwd)"

    for i in {1..5}; do
        if [ -d "${search_dir}/.swarm" ]; then
            echo "${search_dir}"
            return 0
        fi
        if [ "${search_dir}" = "/" ]; then
            break
        fi
        search_dir="$(dirname "${search_dir}")"
    done

    echo ""
    return 1
}

# Estrae "Assegnato a:" dal file .md
get_assigned_to() {
    local task_file="$1"
    if [ -f "$task_file" ]; then
        grep -i "assegnato a:" "$task_file" 2>/dev/null | head -1 | sed 's/.*[Aa]ssegnato a:[[:space:]]*//' | sed 's/\*//g' | tr -d '\n' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//'
    else
        echo "unknown"
    fi
}

# Determina la Guardiana appropriata in base all'agente assegnato
get_guardian_for_agent() {
    local agent="$1"

    case "$agent" in
        cervella-frontend|cervella-backend|cervella-tester|cervella-docs)
            echo "cervella-guardiana-qualita"
            ;;
        cervella-devops|cervella-security)
            echo "cervella-guardiana-ops"
            ;;
        cervella-researcher|cervella-scienziata)
            echo "cervella-guardiana-ricerca"
            ;;
        *)
            # Default: guardiana qualita
            echo "cervella-guardiana-qualita"
            ;;
    esac
}

# Calcola tempo trascorso in formato leggibile
time_ago() {
    local seconds="$1"
    if [ "$seconds" -lt 60 ]; then
        echo "${seconds}s"
    elif [ "$seconds" -lt 3600 ]; then
        echo "$((seconds / 60))m"
    else
        echo "$((seconds / 3600))h $((seconds % 3600 / 60))m"
    fi
}

# ============================================================================
# FUNZIONI PRINCIPALI
# ============================================================================

# Mostra stato review
show_review_status() {
    local project_path="$1"
    local project_name
    project_name=$(basename "$project_path")

    local tasks_dir="${project_path}/.swarm/tasks"

    if [ ! -d "$tasks_dir" ]; then
        print_error "Directory tasks non trovata"
        return 1
    fi

    local now
    now=$(date +%s)

    # Liste per output
    local pending_review=""
    local pending_count=0
    local approved_tasks=""
    local approved_count=0
    local rejected_tasks=""
    local rejected_count=0
    local in_review=""
    local in_review_count=0

    # Trova tutti i task .md
    for task_file in "$tasks_dir"/*.md; do
        [ -e "$task_file" ] || continue

        # Salta i file _output.md e _review.md
        [[ "$task_file" == *"_output.md" ]] && continue
        [[ "$task_file" == *"_review.md" ]] && continue

        local task_name
        task_name=$(basename "$task_file" .md)
        local assigned_to
        assigned_to=$(get_assigned_to "$task_file")

        local done_file="${tasks_dir}/${task_name}.done"
        local approved_file="${tasks_dir}/${task_name}.approved"
        local rejected_file="${tasks_dir}/${task_name}.rejected"
        local review_ready_file="${tasks_dir}/${task_name}.review_ready"

        # Solo task completati (.done)
        if [ -f "$done_file" ]; then
            local done_time
            done_time=$(stat -f %m "$done_file" 2>/dev/null || stat -c %Y "$done_file" 2>/dev/null)
            local elapsed=$((now - done_time))
            local elapsed_str
            elapsed_str=$(time_ago "$elapsed")

            if [ -f "$approved_file" ]; then
                # Approvato
                approved_count=$((approved_count + 1))
                local approved_time
                approved_time=$(stat -f %m "$approved_file" 2>/dev/null || stat -c %Y "$approved_file" 2>/dev/null)
                local approved_date
                approved_date=$(date -r "$approved_time" "+%H:%M" 2>/dev/null || date -d "@$approved_time" "+%H:%M" 2>/dev/null)
                approved_tasks="${approved_tasks}   - ${task_name} (${approved_date})\n"

            elif [ -f "$rejected_file" ]; then
                # Rifiutato
                rejected_count=$((rejected_count + 1))
                rejected_tasks="${rejected_tasks}   - ${task_name} -> ${assigned_to}\n"

            elif [ -f "$review_ready_file" ]; then
                # In review
                in_review_count=$((in_review_count + 1))
                local guardian
                guardian=$(get_guardian_for_agent "$assigned_to")
                in_review="${in_review}   - ${task_name} -> ${guardian}\n"

            else
                # Completato ma non ancora in review
                pending_count=$((pending_count + 1))
                pending_review="${pending_review}   - ${task_name} -> ${assigned_to} -> pronto da ${elapsed_str}\n"
            fi
        fi
    done

    # Output
    echo ""
    echo -e "   ${CYAN}Progetto:${NC} ${project_name}"
    echo ""

    # Task da verificare (done senza approved/rejected/review_ready)
    if [ "$pending_count" -gt 0 ]; then
        echo -e "${YELLOW}TASK DA VERIFICARE (done senza review):${NC}"
        echo -e "$pending_review"
    else
        echo -e "${GREEN}Nessun task in attesa di review${NC}"
        echo ""
    fi

    # Task in review
    if [ "$in_review_count" -gt 0 ]; then
        echo -e "${BLUE}IN REVIEW:${NC}"
        echo -e "$in_review"
    fi

    # Approvati
    if [ "$approved_count" -gt 0 ]; then
        echo -e "${GREEN}GIA' APPROVATI:${NC}"
        echo -e "$approved_tasks"
    fi

    # Rifiutati
    if [ "$rejected_count" -gt 0 ]; then
        echo -e "${RED}RIFIUTATI (fix richiesti):${NC}"
        echo -e "$rejected_tasks"
    fi

    # Suggerimento
    if [ "$pending_count" -gt 0 ]; then
        echo ""
        print_info "Usa: swarm-review --start per avviare review"
    fi
}

# Avvia review per tutti i task pending
start_review() {
    local project_path="$1"
    local specific_task="$2"

    local tasks_dir="${project_path}/.swarm/tasks"

    if [ ! -d "$tasks_dir" ]; then
        print_error "Directory tasks non trovata"
        return 1
    fi

    # File temporanei per raccogliere task per ogni guardiana
    local tmp_dir="/tmp/swarm-review-$$"
    mkdir -p "$tmp_dir"

    local total_pending=0

    for task_file in "$tasks_dir"/*.md; do
        [ -e "$task_file" ] || continue

        # Salta i file _output.md e _review.md
        case "$task_file" in
            *_output.md|*_review.md) continue ;;
        esac

        local task_name
        task_name=$(basename "$task_file" .md)

        # Se task specifico richiesto, salta gli altri
        if [ -n "$specific_task" ] && [ "$task_name" != "$specific_task" ]; then
            continue
        fi

        local done_file="${tasks_dir}/${task_name}.done"
        local approved_file="${tasks_dir}/${task_name}.approved"
        local rejected_file="${tasks_dir}/${task_name}.rejected"
        local review_ready_file="${tasks_dir}/${task_name}.review_ready"

        # Solo task completati e non ancora reviewati
        if [ -f "$done_file" ] && [ ! -f "$approved_file" ] && [ ! -f "$rejected_file" ] && [ ! -f "$review_ready_file" ]; then
            local assigned_to
            assigned_to=$(get_assigned_to "$task_file")
            local guardian
            guardian=$(get_guardian_for_agent "$assigned_to")

            # Crea .review_ready
            touch "$review_ready_file"
            print_success "Creato ${task_name}.review_ready"

            # Aggiungi alla lista della guardiana (file temporaneo)
            echo "${task_name}|${assigned_to}" >> "${tmp_dir}/${guardian}.txt"

            total_pending=$((total_pending + 1))
        fi
    done

    if [ "$total_pending" -eq 0 ]; then
        print_info "Nessun task da revieware"
        rm -rf "$tmp_dir"
        return 0
    fi

    echo ""
    print_success "Trovati ${total_pending} task da revieware"
    echo ""

    # Spawna una Guardiana per ogni file
    for guardian_file in "$tmp_dir"/*.txt; do
        [ -e "$guardian_file" ] || continue

        local guardian
        guardian=$(basename "$guardian_file" .txt)

        echo -e "${PURPLE}Spawnando ${guardian}...${NC}"

        # Costruisci il prompt per la Guardiana
        local prompt="Sei stata attivata per REVIEW.

Task da verificare:"

        while IFS='|' read -r task_name assigned_to; do
            [ -z "$task_name" ] && continue
            prompt="${prompt}
- ${task_name} (${tasks_dir}/${task_name}.md)
  Output: ${tasks_dir}/${task_name}_output.md
  Assegnato a: ${assigned_to}"
        done < "$guardian_file"

        prompt="${prompt}

Per ogni task:
1. Leggi il task originale (.md)
2. Leggi l'output (_output.md) SE ESISTE
3. Verifica con la tua checklist
4. Crea .approved O .rejected
5. Se rejected, scrivi motivazione in _review.md"

        # Spawna la Guardiana
        spawn_guardian "$guardian" "$prompt" "$project_path"
    done

    # Cleanup
    rm -rf "$tmp_dir"

    echo ""
    print_success "Review avviata!"
}

# Spawna una Guardiana in una nuova finestra
spawn_guardian() {
    local guardian="$1"
    local prompt="$2"
    local project_path="$3"

    # Escape per AppleScript
    local escaped_prompt="${prompt//\\/\\\\}"
    escaped_prompt="${escaped_prompt//\"/\\\"}"
    escaped_prompt="${escaped_prompt//$'\n'/\\n}"

    # Usa osascript per aprire Terminal e lanciare claude
    osascript << EOF
tell application "Terminal"
    activate
    do script "cd '${project_path}' && claude --agent ${guardian} -p \"${escaped_prompt}\""
end tell
EOF

    print_success "Spawnata ${guardian}"
}

show_usage() {
    echo "Uso: swarm-review [opzioni]"
    echo ""
    echo "Opzioni:"
    echo "  (nessuna)        Mostra stato review"
    echo "  --start          Avvia review (crea .review_ready + spawna Guardiane)"
    echo "  --task NOME      Review solo task specifico"
    echo "  --help, -h       Mostra questo help"
    echo ""
    echo "Stati dei task:"
    echo "  .ready           In coda"
    echo "  .working         In lavorazione"
    echo "  .done            Completato"
    echo "  .review_ready    Pronto per Guardiana"
    echo "  .approved        Guardiana ha approvato"
    echo "  .rejected        Guardiana ha rifiutato"
    echo ""
    echo "Guardiane:"
    echo "  cervella-guardiana-qualita   Per frontend/backend/tester/docs"
    echo "  cervella-guardiana-ops       Per devops/security"
    echo "  cervella-guardiana-ricerca   Per researcher/scienziata"
    echo ""
    echo "Esempi:"
    echo "  swarm-review                # Vedi stato review"
    echo "  swarm-review --start        # Avvia review di tutti i task pending"
    echo "  swarm-review --task MYFIX   # Review solo task MYFIX"
    echo ""
}

# ============================================================================
# MAIN
# ============================================================================

main() {
    local do_start=false
    local specific_task=""

    while [ $# -gt 0 ]; do
        case "$1" in
            --start)
                do_start=true
                ;;
            --task)
                shift
                specific_task="$1"
                do_start=true
                ;;
            --help|-h)
                show_usage
                exit 0
                ;;
            *)
                print_error "Opzione sconosciuta: $1"
                show_usage
                exit 1
                ;;
        esac
        shift
    done

    print_header

    # Trova progetto corrente
    local project_root
    project_root=$(find_project_root)

    if [ -z "$project_root" ]; then
        print_error "Nessun progetto .swarm/ trovato!"
        print_info "Esegui da una directory con .swarm/"
        exit 1
    fi

    if [ "$do_start" = true ]; then
        start_review "$project_root" "$specific_task"
    else
        show_review_status "$project_root"
    fi

    echo ""
    print_info "Fatto!"
    echo ""
}

# Esegui
main "$@"
