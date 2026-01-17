#!/bin/bash
# =================================================================
# ARCHIVE OLD REPORTS - CervellaSwarm
# =================================================================
# Archivia automaticamente i reports più vecchi di N giorni
# Esegui: ./scripts/archive_old_reports.sh [giorni]
# Default: 7 giorni
# DRY_RUN=true ./scripts/archive_old_reports.sh  (per test)
# =================================================================

set -e

DAYS_OLD="${1:-7}"
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPORTS_DIR="$PROJECT_ROOT/reports"
SNCP_REPORTS_DIR="$PROJECT_ROOT/.sncp/reports"
DRY_RUN="${DRY_RUN:-false}"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=================================================="
echo "  ARCHIVE OLD REPORTS"
echo "  Archiviando file più vecchi di $DAYS_OLD giorni"
if [ "$DRY_RUN" = "true" ]; then
    echo -e "  ${YELLOW}MODALITA: DRY-RUN (nessun file spostato)${NC}"
fi
echo "=================================================="
echo ""

TOTAL_ARCHIVED=0

archive_dir_files() {
    local source_dir="$1"
    local archive_base="$2"
    local dir_name="$3"

    [ ! -d "$source_dir" ] && return

    echo ">> $dir_name"

    find "$source_dir" -maxdepth 1 -type f \( -name "*.json" -o -name "*.md" -o -name "*.txt" \) -mtime +$DAYS_OLD 2>/dev/null | while read -r file; do
        # Estrai anno-mese dal nome file o dalla data modifica
        if [[ "$file" =~ ([0-9]{4})([0-9]{2})([0-9]{2}) ]]; then
            year="${BASH_REMATCH[1]}"
            month="${BASH_REMATCH[2]}"
        else
            year=$(date -r "$file" "+%Y")
            month=$(date -r "$file" "+%m")
        fi

        archive_dir="$archive_base/${year}-${month}"
        filename=$(basename "$file")

        if [ "$DRY_RUN" = "true" ]; then
            echo -e "   ${YELLOW}[DRY]${NC} $filename -> ${year}-${month}/"
        else
            mkdir -p "$archive_dir"
            mv "$file" "$archive_dir/"
            echo -e "   ${GREEN}OK${NC} $filename -> ${year}-${month}/"
        fi
        ((TOTAL_ARCHIVED++)) || true
    done
    echo ""
}

# Archivia entrambe le directory
archive_dir_files "$REPORTS_DIR" "$REPORTS_DIR/archive" "reports/"
archive_dir_files "$SNCP_REPORTS_DIR" "$SNCP_REPORTS_DIR/archive" ".sncp/reports/"

echo "=================================================="
echo -e "${GREEN}COMPLETATO!${NC}"
echo "=================================================="

if [ "$DRY_RUN" = "true" ]; then
    echo ""
    echo -e "${YELLOW}DRY-RUN: nessun file spostato.${NC}"
    echo "Esegui senza DRY_RUN per archiviare realmente."
fi
