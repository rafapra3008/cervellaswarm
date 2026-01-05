#!/bin/bash
#
# swarm-status.sh - Stato del Beehive in tempo reale
#
# CervellaSwarm - La Regina vede TUTTO!
#
# Uso:
#   swarm-status              # Mostra stato progetto corrente
#   swarm-status --all        # Mostra tutti i progetti
#   swarm-status --cleanup    # Rimuove task STALE
#   swarm-status --help       # Mostra help
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

# Soglia STALE (default: 30 minuti = 1800 secondi)
STALE_THRESHOLD="${STALE_THRESHOLD:-1800}"

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
    echo "  🐝 BEEHIVE STATUS"
    echo "  CervellaSwarm - La Regina vede TUTTO!"
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

# Mostra stato di un singolo progetto
show_project_status() {
    local project_path="$1"
    local project_name
    project_name=$(basename "$project_path")
    
    local swarm_dir="${project_path}/.swarm"
    local tasks_dir="${swarm_dir}/tasks"
    
    # Check se .swarm esiste
    if [ ! -d "$swarm_dir" ]; then
        echo ""
        echo -e "📍 ${CYAN}Progetto:${NC} ${project_name}"
        echo -e "   ${YELLOW}(Nessun .swarm/ trovato)${NC}"
        return
    fi
    
    # Contatori
    local completed=0
    local working=0
    local ready=0
    local stale=0
    
    # Liste per output dettagliato
    local stale_tasks=""
    local working_tasks=""
    local ready_tasks=""
    local completed_tasks=""
    
    local now
    now=$(date +%s)
    
    # Trova tutti i task .md
    if [ -d "$tasks_dir" ]; then
        for task_file in "$tasks_dir"/*.md; do
            [ -e "$task_file" ] || continue
            
            local task_name
            task_name=$(basename "$task_file" .md)
            local assigned_to
            assigned_to=$(get_assigned_to "$task_file")
            
            local done_file="${tasks_dir}/${task_name}.done"
            local working_file="${tasks_dir}/${task_name}.working"
            local ready_file="${tasks_dir}/${task_name}.ready"
            
            if [ -f "$done_file" ]; then
                # Completato
                completed=$((completed + 1))
                local done_time
                done_time=$(stat -f %m "$done_file" 2>/dev/null || stat -c %Y "$done_file" 2>/dev/null)
                local done_date
                done_date=$(date -r "$done_time" "+%H:%M" 2>/dev/null || date -d "@$done_time" "+%H:%M" 2>/dev/null)
                completed_tasks="${completed_tasks}   - ${task_name} (${done_date})\n"
                
            elif [ -f "$working_file" ]; then
                # In lavorazione
                local working_time
                working_time=$(stat -f %m "$working_file" 2>/dev/null || stat -c %Y "$working_file" 2>/dev/null)
                local elapsed=$((now - working_time))
                local elapsed_str
                elapsed_str=$(time_ago "$elapsed")
                
                if [ "$elapsed" -gt "$STALE_THRESHOLD" ]; then
                    # STALE!
                    stale=$((stale + 1))
                    stale_tasks="${stale_tasks}   - ${task_name} (${elapsed_str} fa) -> ${assigned_to}\n"
                else
                    # In lavorazione normale
                    working=$((working + 1))
                    working_tasks="${working_tasks}   - ${task_name} (${elapsed_str} fa) -> ${assigned_to}\n"
                fi
                
            elif [ -f "$ready_file" ]; then
                # In coda
                ready=$((ready + 1))
                ready_tasks="${ready_tasks}   - ${task_name} -> ${assigned_to}\n"
            fi
        done
    fi
    
    # Output
    echo ""
    echo -e "📍 ${CYAN}Progetto:${NC} ${project_name}"
    echo -e "   Path: ${project_path}"
    echo ""
    echo -e "📊 ${BLUE}RIEPILOGO${NC}"
    echo -e "   ${GREEN}✅ Completati:${NC}     ${completed}"
    echo -e "   ${YELLOW}🔄 In lavorazione:${NC} ${working}"
    echo -e "   ${BLUE}📋 In coda:${NC}        ${ready}"
    if [ "$stale" -gt 0 ]; then
        echo -e "   ${RED}⚠️  STALE:${NC}         ${stale}"
    fi
    
    # Task STALE (se ci sono)
    if [ -n "$stale_tasks" ]; then
        echo ""
        echo -e "${RED}🔴 TASK STALE (working > 30 min, no done):${NC}"
        echo -e "$stale_tasks"
    fi
    
    # Task in lavorazione
    if [ -n "$working_tasks" ]; then
        echo ""
        echo -e "${YELLOW}🟡 TASK IN LAVORAZIONE:${NC}"
        echo -e "$working_tasks"
    fi
    
    # Task in coda
    if [ -n "$ready_tasks" ]; then
        echo ""
        echo -e "${BLUE}🟢 TASK IN CODA (.ready):${NC}"
        echo -e "$ready_tasks"
    fi
    
    # Ultimi 5 completati
    if [ -n "$completed_tasks" ]; then
        echo ""
        echo -e "${GREEN}✅ ULTIMI COMPLETATI:${NC}"
        echo -e "$completed_tasks" | head -5
    fi
}

# Cleanup task STALE
cleanup_stale() {
    local project_path="$1"
    local tasks_dir="${project_path}/.swarm/tasks"
    
    if [ ! -d "$tasks_dir" ]; then
        print_warning "Directory tasks non trovata"
        return
    fi
    
    local now
    now=$(date +%s)
    local cleaned=0
    
    for working_file in "$tasks_dir"/*.working; do
        [ -e "$working_file" ] || continue
        
        local task_name
        task_name=$(basename "$working_file" .working)
        local done_file="${tasks_dir}/${task_name}.done"
        
        # Se c'e' .done, non e' stale
        if [ -f "$done_file" ]; then
            continue
        fi
        
        local working_time
        working_time=$(stat -f %m "$working_file" 2>/dev/null || stat -c %Y "$working_file" 2>/dev/null)
        local elapsed=$((now - working_time))
        
        if [ "$elapsed" -gt "$STALE_THRESHOLD" ]; then
            print_warning "Rimuovo ${task_name}.working (stale ${elapsed}s)"
            rm -f "$working_file"
            cleaned=$((cleaned + 1))
        fi
    done
    
    if [ "$cleaned" -gt 0 ]; then
        print_success "Rimossi ${cleaned} file .working stale"
    else
        print_info "Nessun task stale da pulire"
    fi
}

show_usage() {
    echo "Uso: swarm-status [opzioni]"
    echo ""
    echo "Opzioni:"
    echo "  (nessuna)     Mostra stato del progetto corrente"
    echo "  --all         Mostra stato di TUTTI i progetti"
    echo "  --cleanup     Rimuove file .working stale (> 30 min)"
    echo "  --help, -h    Mostra questo help"
    echo ""
    echo "Esempi:"
    echo "  swarm-status              # Stato progetto corrente"
    echo "  swarm-status --all        # Stato tutti i progetti"
    echo "  swarm-status --cleanup    # Pulisce task stale"
    echo ""
}

# ============================================================================
# MAIN
# ============================================================================

main() {
    # Parse argomenti
    local show_all=false
    local do_cleanup=false
    
    while [ $# -gt 0 ]; do
        case "$1" in
            --all)
                show_all=true
                ;;
            --cleanup)
                do_cleanup=true
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
    
    if [ "$show_all" = true ]; then
        # Mostra tutti i progetti
        for project in "${PROJECTS[@]}"; do
            if [ -d "$project" ]; then
                show_project_status "$project"
                echo ""
                echo "----------------------------------------------"
            fi
        done
    else
        # Trova progetto corrente
        local project_root
        project_root=$(find_project_root)
        
        if [ -z "$project_root" ]; then
            print_error "Nessun progetto .swarm/ trovato!"
            print_info "Esegui da una directory con .swarm/ o usa --all"
            exit 1
        fi
        
        if [ "$do_cleanup" = true ]; then
            cleanup_stale "$project_root"
        else
            show_project_status "$project_root"
        fi
    fi
    
    echo ""
    print_info "Fatto!"
    echo ""
}

# Esegui
main "$@"
