#!/bin/bash
# ==============================================================================
# POST-SESSION-UPDATE - SNCP Update Prompt at Session End
# ==============================================================================
#
# Esegue alla fine di una sessione:
# - Mostra summary di cosa aggiornare
# - Crea backup se necessario
# - Prompt per aggiornamento stato.md
#
# Uso: ./post-session-update.sh [progetto] [sessione_numero]
#
# ==============================================================================

set -e

SNCP_ROOT="${SNCP_ROOT:-/Users/rafapra/Developer/CervellaSwarm/.sncp}"
TODAY=$(date +%Y-%m-%d)
NOW=$(date +"%Y-%m-%d %H:%M")
PROJECT="${1:-}"
SESSION="${2:-}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# ==============================================================================
# FUNCTIONS
# ==============================================================================

print_header() {
    echo ""
    echo -e "${MAGENTA}+================================================================+${NC}"
    echo -e "${MAGENTA}|              POST-SESSION UPDATE                              |${NC}"
    echo -e "${MAGENTA}+================================================================+${NC}"
    echo ""
}

# Backup file before update
backup_file() {
    local file="$1"
    local backup_dir="$SNCP_ROOT/archivio/$(date +%Y-%m)"

    if [ ! -f "$file" ]; then
        return 0
    fi

    mkdir -p "$backup_dir"

    local basename=$(basename "$file")
    local backup_name="${basename%.md}_$(date +%Y%m%d_%H%M%S).md"

    cp "$file" "$backup_dir/$backup_name"
    echo -e "  ${GREEN}[OK]${NC} Backup: $backup_dir/$backup_name"
}

# Check if file needs compaction
check_compaction_needed() {
    local file="$1"
    local max_lines="${2:-300}"

    if [ ! -f "$file" ]; then
        return 1
    fi

    local line_count=$(wc -l < "$file" | tr -d ' ')

    if [ "$line_count" -gt "$max_lines" ]; then
        return 0  # Needs compaction
    fi

    return 1  # OK
}

# Run compaction on file
run_compaction() {
    local file="$1"
    local max_lines="${2:-300}"
    local keep_lines="${3:-200}"

    echo -e "  ${YELLOW}[!]${NC} Running compaction on $file..."

    # Backup first
    backup_file "$file"

    local line_count=$(wc -l < "$file" | tr -d ' ')

    # Create temp file with header + recent content
    local temp_file="${file}.tmp"

    # Keep only recent lines
    tail -n "$keep_lines" "$file" > "$temp_file"

    # Add compaction header
    cat > "${file}.new" << EOF
# Stato - Auto-compacted

> **Data:** $NOW
> **Auto-compacted:** Si (da $line_count a $keep_lines righe)
> **Archivio:** Vedi .sncp/archivio/$(date +%Y-%m)/

---

EOF

    cat "$temp_file" >> "${file}.new"
    mv "${file}.new" "$file"
    rm -f "$temp_file"

    echo -e "  ${GREEN}[OK]${NC} Compacted: $line_count -> $(wc -l < "$file" | tr -d ' ') righe"
}

# Show checklist
show_checklist() {
    echo -e "${BLUE}--- CHECKLIST POST-SESSIONE ---${NC}"
    echo ""

    echo "  Hai fatto questi aggiornamenti?"
    echo ""

    if [ -n "$PROJECT" ]; then
        echo -e "  [ ] ${CYAN}stato.md${NC} di $PROJECT aggiornato"
    fi

    echo -e "  [ ] ${CYAN}oggi.md${NC} aggiornato"
    echo -e "  [ ] ${CYAN}PROMPT_RIPRESA.md${NC} aggiornato"
    echo -e "  [ ] ${CYAN}Decisioni${NC} documentate (se prese)"
    echo -e "  [ ] ${CYAN}Lezioni${NC} documentate (se apprese)"
    echo ""
}

# Show what to update
show_update_summary() {
    echo -e "${BLUE}--- COSA AGGIORNARE ---${NC}"
    echo ""

    # Check oggi.md
    local oggi_file="$SNCP_ROOT/stato/oggi.md"
    local oggi_date=$(stat -f "%Sm" -t "%Y-%m-%d" "$oggi_file" 2>/dev/null || echo "unknown")

    if [ "$oggi_date" != "$TODAY" ]; then
        echo -e "  ${YELLOW}[!]${NC} oggi.md: Non aggiornato oggi (ultimo: $oggi_date)"
    else
        echo -e "  ${GREEN}[OK]${NC} oggi.md: Aggiornato oggi"
    fi

    # Check project stato.md
    if [ -n "$PROJECT" ]; then
        local stato_file="$SNCP_ROOT/progetti/$PROJECT/stato.md"
        if [ -f "$stato_file" ]; then
            local stato_date=$(stat -f "%Sm" -t "%Y-%m-%d" "$stato_file" 2>/dev/null || echo "unknown")
            if [ "$stato_date" != "$TODAY" ]; then
                echo -e "  ${YELLOW}[!]${NC} $PROJECT/stato.md: Non aggiornato oggi"
            else
                echo -e "  ${GREEN}[OK]${NC} $PROJECT/stato.md: Aggiornato oggi"
            fi
        fi
    fi

    # Check for compaction needs
    if check_compaction_needed "$SNCP_ROOT/stato/oggi.md" 300; then
        echo -e "  ${RED}[!]${NC} oggi.md: SERVE COMPACTION!"
    fi

    echo ""
}

# Create session handoff file
create_handoff() {
    local session="$1"
    local project="$2"

    if [ -z "$session" ]; then
        echo -e "  ${YELLOW}[!]${NC} Numero sessione non specificato - skip handoff"
        return
    fi

    local handoff_dir="$SNCP_ROOT/handoff"
    mkdir -p "$handoff_dir"

    local handoff_file="$handoff_dir/HANDOFF_SESSIONE_${session}.md"

    if [ -f "$handoff_file" ]; then
        echo -e "  ${YELLOW}[!]${NC} Handoff gia esiste: $handoff_file"
        return
    fi

    cat > "$handoff_file" << EOF
# HANDOFF - Sessione $session

> **Data:** $NOW
> **Progetto:** ${project:-"Multi-progetto"}

---

## COMPLETATO

- [TODO: lista cosa completato]

## IN CORSO

- [TODO: lista cosa in corso]

## BLOCCANTI

- [TODO: lista bloccanti]

## PROSSIMA SESSIONE

- [TODO: cosa fare prossima sessione]

---

*"Se documentiamo = facciamo!"*
EOF

    echo -e "  ${GREEN}[OK]${NC} Handoff creato: $handoff_file"
}

# Print footer
print_footer() {
    echo ""
    echo -e "${MAGENTA}+================================================================+${NC}"
    echo -e "${MAGENTA}|   \"Un po' ogni giorno fino al 100000%!\"                       |${NC}"
    echo -e "${MAGENTA}+================================================================+${NC}"
    echo ""
}

# ==============================================================================
# MAIN
# ==============================================================================

print_header
show_update_summary
show_checklist

# Create handoff if session specified
if [ -n "$SESSION" ]; then
    create_handoff "$SESSION" "$PROJECT"
fi

# Check and run compaction if needed
if check_compaction_needed "$SNCP_ROOT/stato/oggi.md" 300; then
    echo ""
    echo -e "${YELLOW}ATTENZIONE: oggi.md serve compaction!${NC}"
    read -p "Eseguire compaction automatica? [y/N] " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        run_compaction "$SNCP_ROOT/stato/oggi.md" 300 200
    fi
fi

print_footer
