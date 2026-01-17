#!/bin/bash
# ==============================================================================
# COMPACT-STATE - SNCP File Compaction
# ==============================================================================
#
# Compatta file SNCP che superano i limiti:
# - Crea backup in archivio/
# - Mantiene solo le righe recenti
# - Aggiunge header con metadata
#
# Uso: ./compact-state.sh [--auto] [file] [max_lines] [keep_lines]
#      --auto: esegue senza conferma (per automazione)
#      file: path al file (default: .sncp/stato/oggi.md)
#      max_lines: trigger compaction (default: 300)
#      keep_lines: righe da mantenere (default: 200)
#
# ==============================================================================

set -e

SNCP_ROOT="${SNCP_ROOT:-/Users/rafapra/Developer/CervellaSwarm/.sncp}"
NOW=$(date +"%Y-%m-%d %H:%M")
TODAY=$(date +%Y-%m-%d)

# Auto mode (no confirmation)
AUTO_MODE=false
if [ "$1" = "--auto" ]; then
    AUTO_MODE=true
    shift
fi

# Defaults
FILE="${1:-$SNCP_ROOT/stato/oggi.md}"
MAX_LINES="${2:-300}"
KEEP_LINES="${3:-200}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ==============================================================================
# FUNCTIONS
# ==============================================================================

print_header() {
    echo ""
    echo -e "${BLUE}+================================================================+${NC}"
    echo -e "${BLUE}|              SNCP COMPACTION                                  |${NC}"
    echo -e "${BLUE}+================================================================+${NC}"
    echo ""
}

check_file() {
    if [ ! -f "$FILE" ]; then
        echo -e "${RED}[ERROR]${NC} File non esiste: $FILE"
        exit 1
    fi
}

get_line_count() {
    wc -l < "$FILE" | tr -d ' '
}

needs_compaction() {
    local line_count=$(get_line_count)

    if [ "$line_count" -gt "$MAX_LINES" ]; then
        return 0  # Needs compaction
    fi

    return 1  # OK
}

backup_file() {
    local backup_dir="$SNCP_ROOT/archivio/$(date +%Y-%m)"
    mkdir -p "$backup_dir"

    local basename=$(basename "$FILE")
    local backup_name="${basename%.md}_$(date +%Y%m%d_%H%M%S).md"

    cp "$FILE" "$backup_dir/$backup_name"
    echo -e "  ${GREEN}[BACKUP]${NC} $backup_dir/$backup_name"
}

run_compaction() {
    local original_lines=$(get_line_count)

    echo -e "  ${YELLOW}[COMPACT]${NC} $FILE: $original_lines righe -> ~$KEEP_LINES righe"

    # Backup first
    backup_file

    # Create temp file with recent content
    local temp_file="${FILE}.tmp"
    tail -n "$KEEP_LINES" "$FILE" > "$temp_file"

    # Determine file type for appropriate header
    local basename=$(basename "$FILE")
    local header_title="Stato"

    case "$basename" in
        oggi.md)
            header_title="STATO OGGI"
            ;;
        stato.md)
            header_title="STATO PROGETTO"
            ;;
        mappa_viva.md)
            header_title="MAPPA VIVA"
            ;;
        *)
            header_title="FILE COMPATTATO"
            ;;
    esac

    # Create new file with header
    cat > "${FILE}.new" << EOF
# $header_title

> **Data:** $NOW
> **Auto-compacted:** Da $original_lines a $KEEP_LINES righe
> **Archivio completo:** .sncp/archivio/$(date +%Y-%m)/

---

EOF

    # Append recent content
    cat "$temp_file" >> "${FILE}.new"

    # Replace original
    mv "${FILE}.new" "$FILE"
    rm -f "$temp_file"

    local new_lines=$(get_line_count)
    echo -e "  ${GREEN}[DONE]${NC} Compattato: $original_lines -> $new_lines righe (-$((original_lines - new_lines)))"
}

print_status() {
    local line_count=$(get_line_count)

    echo -e "  File: ${BLUE}$FILE${NC}"
    echo -e "  Righe attuali: $line_count"
    echo -e "  Limite: $MAX_LINES"
    echo -e "  Mantenere: $KEEP_LINES"
    echo ""

    if [ "$line_count" -le "$MAX_LINES" ]; then
        echo -e "  ${GREEN}[OK]${NC} Nessuna compaction necessaria"
    else
        echo -e "  ${YELLOW}[!]${NC} Compaction necessaria ($line_count > $MAX_LINES)"
    fi
}

# ==============================================================================
# MAIN
# ==============================================================================

print_header
check_file
print_status

if needs_compaction; then
    echo ""

    if [ "$AUTO_MODE" = true ]; then
        # Auto mode: esegui senza conferma
        echo -e "  ${BLUE}[AUTO]${NC} Esecuzione automatica..."
        run_compaction
    else
        # Interactive mode: chiedi conferma
        read -p "Eseguire compaction? [y/N] " -n 1 -r
        echo ""

        if [[ $REPLY =~ ^[Yy]$ ]]; then
            run_compaction
        else
            echo -e "  ${YELLOW}[SKIP]${NC} Compaction annullata"
        fi
    fi
fi

echo ""
echo -e "${BLUE}+================================================================+${NC}"
echo ""
