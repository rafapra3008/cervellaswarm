#!/bin/bash
# ==============================================================================
# SNCP HEALTH CHECK - Dashboard ASCII Completa
# ==============================================================================
#
# Mostra lo stato di salute completo di SNCP:
# - File count per progetto
# - Size analysis
# - File obsoleti (>30 giorni)
# - Cartelle vuote
# - Statistiche globali
#
# Uso: ./health-check.sh [--full] [--json]
#
# ==============================================================================

set -e

SNCP_ROOT="${SNCP_ROOT:-/Users/rafapra/Developer/CervellaSwarm/.sncp}"
TODAY=$(date +%Y-%m-%d)
FULL_MODE="${1:-}"
JSON_MODE=""

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

print_dashboard_header() {
    echo ""
    echo -e "${CYAN}+================================================================+${NC}"
    echo -e "${CYAN}|                                                                |${NC}"
    echo -e "${CYAN}|   ${MAGENTA}SNCP HEALTH DASHBOARD${CYAN}                                       |${NC}"
    echo -e "${CYAN}|   ${NC}Sistema Nervoso Centrale Progetti${CYAN}                            |${NC}"
    echo -e "${CYAN}|                                                                |${NC}"
    echo -e "${CYAN}|   Data: $(date '+%Y-%m-%d %H:%M')                                       |${NC}"
    echo -e "${CYAN}+================================================================+${NC}"
    echo ""
}

# Count files in directory
count_files() {
    local dir="$1"
    local pattern="${2:-*.md}"

    if [ -d "$dir" ]; then
        find "$dir" -name "$pattern" -type f 2>/dev/null | wc -l | tr -d ' '
    else
        echo "0"
    fi
}

# Count obsolete files (>30 days)
count_obsolete() {
    local dir="$1"

    if [ -d "$dir" ]; then
        find "$dir" -name "*.md" -type f -mtime +30 2>/dev/null | wc -l | tr -d ' '
    else
        echo "0"
    fi
}

# Get file line count
get_line_count() {
    local file="$1"

    if [ -f "$file" ]; then
        wc -l < "$file" | tr -d ' '
    else
        echo "0"
    fi
}

# Check file freshness
get_file_age() {
    local file="$1"

    if [ ! -f "$file" ]; then
        echo "N/A"
        return
    fi

    local file_date=$(stat -f "%Sm" -t "%Y-%m-%d" "$file" 2>/dev/null || date -r "$file" +%Y-%m-%d 2>/dev/null)
    echo "$file_date"
}

# Print progress bar
progress_bar() {
    local current="$1"
    local max="$2"
    local width="${3:-20}"

    local percent=$((current * 100 / max))
    local filled=$((current * width / max))
    local empty=$((width - filled))

    printf "["
    printf "%${filled}s" | tr ' ' '#'
    printf "%${empty}s" | tr ' ' '-'
    printf "] %3d%%" "$percent"
}

# Print project stats
print_project_stats() {
    local project="$1"
    local project_dir="$SNCP_ROOT/progetti/$project"

    if [ ! -d "$project_dir" ]; then
        echo -e "  ${YELLOW}$project${NC}: (non esiste)"
        return
    fi

    local total_files=$(count_files "$project_dir")
    local obsolete=$(count_obsolete "$project_dir")
    local stato_lines=$(get_line_count "$project_dir/stato.md")
    local stato_date=$(get_file_age "$project_dir/stato.md")

    # Status indicator
    local status_icon="${GREEN}OK${NC}"
    if [ "$obsolete" -gt 5 ]; then
        status_icon="${RED}!!${NC}"
    elif [ "$obsolete" -gt 0 ]; then
        status_icon="${YELLOW}! ${NC}"
    fi

    # stato.md size check
    local stato_icon="${GREEN}OK${NC}"
    if [ "$stato_lines" -gt 300 ]; then
        stato_icon="${RED}!!${NC}"
    elif [ "$stato_lines" -gt 200 ]; then
        stato_icon="${YELLOW}! ${NC}"
    fi

    printf "  %-15s | %3d files | stato: %3d righe [%b] | obsoleti: %2d [%b]\n" \
        "$project" "$total_files" "$stato_lines" "$stato_icon" "$obsolete" "$status_icon"
}

# Print global stats
print_global_stats() {
    echo -e "${BLUE}--- STATISTICHE GLOBALI ---${NC}"
    echo ""

    local total_files=$(count_files "$SNCP_ROOT")
    local total_obsolete=$(count_obsolete "$SNCP_ROOT")

    # oggi.md
    local oggi_lines=$(get_line_count "$SNCP_ROOT/stato/oggi.md")
    local oggi_date=$(get_file_age "$SNCP_ROOT/stato/oggi.md")
    local oggi_icon="${GREEN}OK${NC}"
    if [ "$oggi_lines" -gt 300 ]; then
        oggi_icon="${RED}CRITICO${NC}"
    elif [ "$oggi_lines" -gt 200 ]; then
        oggi_icon="${YELLOW}WARNING${NC}"
    fi

    echo -e "  ${CYAN}SNCP Root:${NC} $SNCP_ROOT"
    echo -e "  ${CYAN}Totale file MD:${NC} $total_files"
    echo -e "  ${CYAN}File obsoleti (>30gg):${NC} $total_obsolete"
    echo ""
    echo -e "  ${CYAN}oggi.md:${NC} $oggi_lines righe [$oggi_icon] - ultimo update: $oggi_date"
}

# Print projects section
print_projects_section() {
    echo ""
    echo -e "${BLUE}--- PROGETTI ---${NC}"
    echo ""
    echo "  Progetto        | Files    | stato.md         | Obsoleti"
    echo "  ----------------|----------|------------------|----------"

    for proj in miracollo cervellaswarm contabilita; do
        print_project_stats "$proj"
    done
}

# Print recommendations
print_recommendations() {
    echo ""
    echo -e "${BLUE}--- RACCOMANDAZIONI ---${NC}"
    echo ""

    local recommendations=0

    # Check oggi.md size
    local oggi_lines=$(get_line_count "$SNCP_ROOT/stato/oggi.md")
    if [ "$oggi_lines" -gt 300 ]; then
        echo -e "  ${RED}[!]${NC} oggi.md ha $oggi_lines righe - esegui compaction!"
        ((recommendations++))
    fi

    # Check obsolete files
    local total_obsolete=$(count_obsolete "$SNCP_ROOT")
    if [ "$total_obsolete" -gt 10 ]; then
        echo -e "  ${YELLOW}[!]${NC} $total_obsolete file obsoleti - considera archiviazione"
        ((recommendations++))
    fi

    # Check today update
    local oggi_date=$(get_file_age "$SNCP_ROOT/stato/oggi.md")
    if [ "$oggi_date" != "$TODAY" ]; then
        echo -e "  ${YELLOW}[!]${NC} oggi.md non aggiornato oggi (ultimo: $oggi_date)"
        ((recommendations++))
    fi

    # Check projects stato.md
    for proj in miracollo cervellaswarm contabilita; do
        local stato_file="$SNCP_ROOT/progetti/$proj/stato.md"
        if [ -f "$stato_file" ]; then
            local lines=$(get_line_count "$stato_file")
            if [ "$lines" -gt 300 ]; then
                echo -e "  ${YELLOW}[!]${NC} $proj/stato.md ha $lines righe - considera split"
                ((recommendations++))
            fi
        fi
    done

    if [ "$recommendations" -eq 0 ]; then
        echo -e "  ${GREEN}Nessuna raccomandazione - SNCP in ottimo stato!${NC}"
    fi
}

# Print summary score
print_score() {
    echo ""
    echo -e "${BLUE}--- SCORE SNCP ---${NC}"
    echo ""

    local score=100
    local issues=""

    # Deduct for oggi.md size
    local oggi_lines=$(get_line_count "$SNCP_ROOT/stato/oggi.md")
    if [ "$oggi_lines" -gt 300 ]; then
        score=$((score - 20))
        issues="$issues file_size"
    elif [ "$oggi_lines" -gt 200 ]; then
        score=$((score - 10))
    fi

    # Deduct for obsolete files
    local total_obsolete=$(count_obsolete "$SNCP_ROOT")
    if [ "$total_obsolete" -gt 10 ]; then
        score=$((score - 15))
        issues="$issues obsolete"
    elif [ "$total_obsolete" -gt 5 ]; then
        score=$((score - 5))
    fi

    # Deduct for not updated today
    local oggi_date=$(get_file_age "$SNCP_ROOT/stato/oggi.md")
    if [ "$oggi_date" != "$TODAY" ]; then
        score=$((score - 10))
        issues="$issues freshness"
    fi

    # Score color
    local score_color="${GREEN}"
    if [ "$score" -lt 70 ]; then
        score_color="${RED}"
    elif [ "$score" -lt 85 ]; then
        score_color="${YELLOW}"
    fi

    echo -e "  SNCP Health Score: ${score_color}$score/100${NC}"
    echo ""

    # Visual bar
    printf "  "
    progress_bar "$score" 100 30
    echo ""
}

# Print footer
print_footer() {
    echo ""
    echo -e "${CYAN}+================================================================+${NC}"
    echo -e "${CYAN}|   ${NC}\"Se documentiamo = facciamo!\"${CYAN}                               |${NC}"
    echo -e "${CYAN}+================================================================+${NC}"
    echo ""
}

# ==============================================================================
# MAIN
# ==============================================================================

print_dashboard_header
print_global_stats
print_projects_section
print_recommendations
print_score
print_footer
