#!/bin/bash
# ==============================================================================
# PRE-SESSION-CHECK - SNCP Health Check at Session Start
# ==============================================================================
#
# Esegue controlli SNCP prima di iniziare una sessione:
# - Verifica stato.md aggiornato oggi
# - Controlla file size limits
# - Mostra warning se problemi
#
# Uso: ./pre-session-check.sh [progetto]
#      progetto: miracollo|cervellaswarm|contabilita (default: tutti)
#
# ==============================================================================

set -e

SNCP_ROOT="${SNCP_ROOT:-/Users/rafapra/Developer/CervellaSwarm/.sncp}"
TODAY=$(date +%Y-%m-%d)
PROJECT="${1:-all}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ==============================================================================
# FUNCTIONS
# ==============================================================================

print_header() {
    echo ""
    echo -e "${BLUE}+================================================================+${NC}"
    echo -e "${BLUE}|              SNCP PRE-SESSION CHECK                           |${NC}"
    echo -e "${BLUE}+================================================================+${NC}"
    echo ""
}

check_file_updated_today() {
    local file="$1"
    local name="$2"

    if [ ! -f "$file" ]; then
        echo -e "  ${YELLOW}[!]${NC} $name: FILE NON ESISTE"
        return 1
    fi

    # Check if file was modified today
    local file_date=$(stat -f "%Sm" -t "%Y-%m-%d" "$file" 2>/dev/null || date -r "$file" +%Y-%m-%d)

    if [ "$file_date" == "$TODAY" ]; then
        echo -e "  ${GREEN}[OK]${NC} $name: Aggiornato oggi ($file_date)"
        return 0
    else
        echo -e "  ${YELLOW}[!]${NC} $name: Ultimo update $file_date (oggi: $TODAY)"
        return 1
    fi
}

check_file_size() {
    local file="$1"
    local name="$2"
    local max_lines="${3:-300}"

    if [ ! -f "$file" ]; then
        return 0  # Skip if file doesn't exist
    fi

    local line_count=$(wc -l < "$file" | tr -d ' ')

    if [ "$line_count" -le "$max_lines" ]; then
        echo -e "  ${GREEN}[OK]${NC} $name: $line_count righe (max: $max_lines)"
        return 0
    else
        echo -e "  ${RED}[X]${NC} $name: $line_count righe > $max_lines - SERVE COMPACTION!"
        return 1
    fi
}

check_project() {
    local project="$1"
    local project_dir="$SNCP_ROOT/progetti/$project"

    echo ""
    echo -e "${BLUE}--- Progetto: $project ---${NC}"

    if [ ! -d "$project_dir" ]; then
        echo -e "  ${YELLOW}[!]${NC} Directory non esiste: $project_dir"
        return 1
    fi

    local issues=0

    # Check stato.md
    if [ -f "$project_dir/stato.md" ]; then
        check_file_updated_today "$project_dir/stato.md" "stato.md" || ((issues++))
        check_file_size "$project_dir/stato.md" "stato.md" 300 || ((issues++))
    else
        echo -e "  ${YELLOW}[!]${NC} stato.md: NON ESISTE"
        ((issues++))
    fi

    return $issues
}

check_global() {
    echo ""
    echo -e "${BLUE}--- File Globali ---${NC}"

    local issues=0

    # Check oggi.md
    check_file_updated_today "$SNCP_ROOT/stato/oggi.md" "oggi.md" || ((issues++))
    check_file_size "$SNCP_ROOT/stato/oggi.md" "oggi.md" 300 || ((issues++))

    # Check mappa_viva.md
    check_file_size "$SNCP_ROOT/stato/mappa_viva.md" "mappa_viva.md" 200 || ((issues++))

    return $issues
}

print_summary() {
    local total_issues="$1"

    echo ""
    echo -e "${BLUE}+================================================================+${NC}"

    if [ "$total_issues" -eq 0 ]; then
        echo -e "${GREEN}|              SNCP OK - Buona sessione!                        |${NC}"
    elif [ "$total_issues" -le 2 ]; then
        echo -e "${YELLOW}|              SNCP WARNING - $total_issues issue da risolvere               |${NC}"
    else
        echo -e "${RED}|              SNCP CRITICO - $total_issues issues! Risolvi prima!            |${NC}"
    fi

    echo -e "${BLUE}+================================================================+${NC}"
    echo ""
}

# ==============================================================================
# MAIN
# ==============================================================================

print_header

total_issues=0

# Check global files
check_global
((total_issues+=$?))

# Check projects
if [ "$PROJECT" == "all" ]; then
    for proj in miracollo cervellaswarm contabilita; do
        if [ -d "$SNCP_ROOT/progetti/$proj" ]; then
            check_project "$proj"
            ((total_issues+=$?))
        fi
    done
else
    check_project "$PROJECT"
    ((total_issues+=$?))
fi

print_summary "$total_issues"

exit $total_issues
