#!/bin/bash
#
# swarm-roadmaps.sh - Vista aggregata roadmap multi-progetto!
#
# Uso:
#   swarm-roadmaps                 # Mostra tutti i progetti
#   swarm-roadmaps --add PATH      # Aggiungi progetto alla lista
#   swarm-roadmaps --remove PATH   # Rimuovi progetto
#   swarm-roadmaps --list          # Lista progetti tracciati
#   swarm-roadmaps --refresh       # Forza refresh
#
# Legge NORD.md e ROADMAP_SACRA.md di ogni progetto
#
# Versione: 1.0.0
# Data: 2026-01-06
# Cervella & Rafa

set -e

# Colori
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

# Config
CONFIG_DIR="$HOME/.swarm"
PROJECTS_FILE="$CONFIG_DIR/projects.txt"

mkdir -p "$CONFIG_DIR"

# Inizializza con progetti default se non esiste
if [[ ! -f "$PROJECTS_FILE" ]]; then
    cat > "$PROJECTS_FILE" << EOF
# Lista progetti CervellaSwarm
# Un progetto per riga (path assoluto)
$HOME/Developer/CervellaSwarm
$HOME/Developer/miracollogeminifocus
$HOME/Developer/ContabilitaAntigravity
EOF
fi

# Funzione per aggiungere progetto
add_project() {
    local path="$1"

    # Espandi ~ e rendi assoluto
    path="${path/#\~/$HOME}"
    path="$(cd "$path" 2>/dev/null && pwd)" || {
        echo -e "${RED}[X]${NC} Path non valido: $path"
        exit 1
    }

    # Verifica che abbia NORD.md o .swarm
    if [[ ! -f "$path/NORD.md" && ! -d "$path/.swarm" ]]; then
        echo -e "${YELLOW}[!]${NC} Progetto non ha NORD.md o .swarm/"
        echo "    Vuoi aggiungerlo comunque? (y/n)"
        read -r response
        [[ "$response" != "y" ]] && exit 0
    fi

    # Aggiungi se non già presente
    if grep -qF "$path" "$PROJECTS_FILE" 2>/dev/null; then
        echo -e "${YELLOW}[!]${NC} Progetto già nella lista: $path"
    else
        echo "$path" >> "$PROJECTS_FILE"
        echo -e "${GREEN}[OK]${NC} Aggiunto: $path"
    fi
}

# Funzione per rimuovere progetto
remove_project() {
    local path="$1"
    path="${path/#\~/$HOME}"

    if grep -qF "$path" "$PROJECTS_FILE" 2>/dev/null; then
        grep -vF "$path" "$PROJECTS_FILE" > "$PROJECTS_FILE.tmp"
        mv "$PROJECTS_FILE.tmp" "$PROJECTS_FILE"
        echo -e "${GREEN}[OK]${NC} Rimosso: $path"
    else
        echo -e "${YELLOW}[!]${NC} Progetto non trovato: $path"
    fi
}

# Funzione per listare progetti
list_projects() {
    echo -e "${PURPLE}Progetti tracciati:${NC}"
    echo ""

    while IFS= read -r line; do
        [[ "$line" =~ ^#.*$ || -z "$line" ]] && continue

        if [[ -d "$line" ]]; then
            local name=$(basename "$line")
            echo -e "  ${GREEN}●${NC} $name"
            echo -e "    ${BLUE}$line${NC}"
        else
            local name=$(basename "$line")
            echo -e "  ${RED}○${NC} $name (non trovato)"
            echo -e "    ${RED}$line${NC}"
        fi
    done < "$PROJECTS_FILE"
}

# Funzione per estrarre stato da NORD.md
extract_status() {
    local nord_file="$1"

    if [[ -f "$nord_file" ]]; then
        # Cerca box "DOVE SIAMO" o simili
        local status=$(grep -A5 "DOVE SIAMO\|STATO\|## SESSIONE" "$nord_file" 2>/dev/null | head -8)
        echo "$status"
    fi
}

# Funzione per contare task completati in ROADMAP
count_tasks() {
    local roadmap_file="$1"

    if [[ -f "$roadmap_file" ]]; then
        local done=$(grep -c '\[x\]' "$roadmap_file" 2>/dev/null || echo "0")
        local todo=$(grep -c '\[ \]' "$roadmap_file" 2>/dev/null || echo "0")

        # Pulisci valori
        done=$(echo "$done" | tr -d '[:space:]')
        todo=$(echo "$todo" | tr -d '[:space:]')

        # Default a 0 se vuoto
        [[ -z "$done" ]] && done=0
        [[ -z "$todo" ]] && todo=0

        local total=$((done + todo))

        if [[ $total -gt 0 ]]; then
            local percent=$((done * 100 / total))
            echo "$done/$total ($percent%)"
        else
            echo "N/A"
        fi
    else
        echo "N/A"
    fi
}

# Funzione principale - mostra roadmaps
show_roadmaps() {
    echo -e "${PURPLE}"
    echo "╔══════════════════════════════════════════════════════════════════════╗"
    echo "║                  🗺️  ROADMAPS MULTI-PROGETTO                         ║"
    echo "╚══════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"

    local project_count=0

    while IFS= read -r line; do
        [[ "$line" =~ ^#.*$ || -z "$line" ]] && continue
        [[ ! -d "$line" ]] && continue

        project_count=$((project_count + 1))
        local name=$(basename "$line")
        local nord_file="$line/NORD.md"
        local roadmap_file="$line/ROADMAP_SACRA.md"

        # Ultimo aggiornamento
        local last_update="?"
        if [[ -f "$nord_file" ]]; then
            if [[ "$OSTYPE" == "darwin"* ]]; then
                last_update=$(stat -f "%Sm" -t "%d/%m %H:%M" "$nord_file")
            else
                last_update=$(date -r "$nord_file" "+%d/%m %H:%M")
            fi
        fi

        # Progress
        local progress=$(count_tasks "$roadmap_file")

        # Status box
        echo -e "${CYAN}┌──────────────────────────────────────────────────────────────────────┐${NC}"
        echo -e "${CYAN}│${NC} ${GREEN}📁 $name${NC}"
        echo -e "${CYAN}│${NC}   ${BLUE}Path:${NC} $line"
        echo -e "${CYAN}│${NC}   ${BLUE}Progress:${NC} $progress"
        echo -e "${CYAN}│${NC}   ${BLUE}Ultimo update:${NC} $last_update"

        # Estrai e mostra stato breve
        if [[ -f "$nord_file" ]]; then
            # Cerca ultima sessione
            local session=$(grep -m1 "SESSIONE\|Sessione" "$nord_file" | head -1)
            if [[ -n "$session" ]]; then
                # Pulisci asterischi e caratteri speciali
                session=$(echo "$session" | sed 's/[*#]//g' | xargs)
                echo -e "${CYAN}│${NC}   ${YELLOW}$session${NC}"
            fi
        fi

        echo -e "${CYAN}└──────────────────────────────────────────────────────────────────────┘${NC}"
        echo ""
    done < "$PROJECTS_FILE"

    if [[ $project_count -eq 0 ]]; then
        echo -e "${YELLOW}Nessun progetto trovato.${NC}"
        echo "Aggiungi progetti con: swarm-roadmaps --add PATH"
    else
        echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${BLUE}Progetti tracciati: ${GREEN}$project_count${NC}"
        echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    fi
}

# Main
case "${1:-show}" in
    show|"")
        show_roadmaps
        ;;
    --add|-a)
        shift
        add_project "$1"
        ;;
    --remove|-r)
        shift
        remove_project "$1"
        ;;
    --list|-l)
        list_projects
        ;;
    --refresh)
        show_roadmaps
        ;;
    --help|-h)
        echo "Uso: swarm-roadmaps [comando]"
        echo ""
        echo "Comandi:"
        echo "  (nessuno)        Mostra roadmaps di tutti i progetti"
        echo "  --add PATH       Aggiungi progetto alla lista"
        echo "  --remove PATH    Rimuovi progetto dalla lista"
        echo "  --list           Lista progetti tracciati"
        echo "  --refresh        Forza refresh"
        echo "  --help           Mostra questo help"
        echo ""
        ;;
    *)
        echo "Comando sconosciuto: $1"
        echo "Usa: swarm-roadmaps --help"
        exit 1
        ;;
esac
