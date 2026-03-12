#!/bin/bash
# rotate-reports.sh - Archivia report SNCP > 60 giorni
# Versione: 1.0.0
# Data: 2026-03-12 - Sessione 442
#
# Policy: report con data nel nome > 60 giorni -> reports/archivio/YYYY-MM/
# Report senza data nel nome: non vengono toccati (potrebbero essere referenziati).
# Uso: ./scripts/sncp/rotate-reports.sh [--dry-run]
#
# "Il diamante si lucida nei dettagli."

set -euo pipefail

SNCP_ROOT="$(cd "$(dirname "$0")/../.." && pwd)/.sncp/progetti"
DRY_RUN=false
DAYS=60
MOVED=0
SKIPPED=0

if [[ "${1:-}" == "--dry-run" ]]; then
    DRY_RUN=true
    echo "[DRY RUN] Nessun file sara spostato."
fi

# Cutoff date (60 days ago) in YYYYMMDD format
if [[ "$(uname)" == "Darwin" ]]; then
    CUTOFF=$(date -v-${DAYS}d +%Y%m%d)
else
    CUTOFF=$(date -d "-${DAYS} days" +%Y%m%d)
fi

echo "=== ROTATE REPORTS ==="
echo "Cutoff: $(echo $CUTOFF | sed 's/\(....\)\(..\)\(..\)/\1-\2-\3/') (> $DAYS giorni)"
echo ""

# Find all report directories
for reports_dir in "$SNCP_ROOT"/*/reports; do
    [ -d "$reports_dir" ] || continue

    project=$(basename "$(dirname "$reports_dir")")
    count=0

    for file in "$reports_dir"/*.md; do
        [ -f "$file" ] || continue

        filename=$(basename "$file")

        # Extract YYYYMMDD date from filename
        # Patterns: RESEARCH_20260215_topic.md, 20260114_AUDIT.md, etc.
        file_date=$(echo "$filename" | command grep -oE '[0-9]{8}' | head -1 || true)

        if [ -z "$file_date" ] || [[ ! "$file_date" =~ ^20[0-9]{6}$ ]]; then
            SKIPPED=$((SKIPPED + 1))
            continue
        fi

        # Compare: if file_date < cutoff, archive it
        if [ "$file_date" -lt "$CUTOFF" ]; then
            # Archive dir: reports/archivio/YYYY-MM/
            year_month="${file_date:0:4}-${file_date:4:2}"
            archive_dir="$reports_dir/archivio/$year_month"

            if $DRY_RUN; then
                echo "  [MOVE] $project: $filename -> archivio/$year_month/"
            else
                mkdir -p "$archive_dir"
                mv "$file" "$archive_dir/"
            fi
            MOVED=$((MOVED + 1))
            count=$((count + 1))
        fi
    done

    if [ $count -gt 0 ]; then
        if $DRY_RUN; then
            echo "  $project: $count report da archiviare"
        else
            echo "  $project: $count report archiviati"
        fi
    fi
done

echo ""
echo "=== RISULTATO ==="
echo "Archiviati: $MOVED"
echo "Senza data (skipped): $SKIPPED"

if $DRY_RUN && [ $MOVED -gt 0 ]; then
    echo ""
    echo "Esegui senza --dry-run per applicare."
fi
