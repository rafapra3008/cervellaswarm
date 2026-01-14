#!/bin/bash
# ==============================================================================
# SNCP WEEKLY ARCHIVE - Archiviazione settimanale file vecchi
# ==============================================================================
#
# Eseguito da cron ogni Lunedi alle 6:00
# Archivia file vecchi (> 30 giorni) per mantenere SNCP pulito
#
# Crontab entry:
#   0 6 * * 1 /Users/rafapra/Developer/CervellaSwarm/scripts/cron/sncp_weekly_archive.sh
#
# Versione: 1.0.0
# Data: 14 Gennaio 2026
# Cervella & Rafa - "Automatizzare TUTTO!"
# ==============================================================================

set -e

# === CONFIGURAZIONE ===

SNCP_ROOT="/Users/rafapra/Developer/CervellaSwarm/.sncp"
ARCHIVE_DIR="$SNCP_ROOT/archivio"
LOG_FILE="/Users/rafapra/Developer/CervellaSwarm/logs/sncp_weekly.log"

TODAY=$(date +%Y-%m-%d)
WEEK=$(date +%Y-W%V)
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Giorni dopo i quali archiviare
ARCHIVE_AFTER_DAYS=30

# Cartelle da archiviare (file vecchi)
ARCHIVE_SOURCES=(
    "idee"
    "reports"
    "decisioni"
    "sessioni_parallele"
)

# Cartelle da NON archiviare MAI
NEVER_ARCHIVE=(
    "stato.md"
    "roadmaps"
    "workflow"
)

# === FUNZIONI ===

log() {
    echo "[$TIMESTAMP] $1" >> "$LOG_FILE"
    echo "$1"
}

ensure_dirs() {
    mkdir -p "$ARCHIVE_DIR/$WEEK"
    mkdir -p "$(dirname "$LOG_FILE")"
}

# Archivia file vecchi da una directory
archive_old_files() {
    local source_dir="$1"
    local project_name="$2"
    local folder_name="$3"

    local archive_dest="$ARCHIVE_DIR/$WEEK/$project_name/$folder_name"

    # Trova file vecchi
    local old_files=$(find "$source_dir" -type f -mtime +$ARCHIVE_AFTER_DAYS 2>/dev/null)

    if [ -z "$old_files" ]; then
        return 0
    fi

    # Crea directory archivio
    mkdir -p "$archive_dest"

    local count=0
    while IFS= read -r file; do
        if [ -f "$file" ]; then
            # Muovi file in archivio
            mv "$file" "$archive_dest/" 2>/dev/null && ((count++)) || true
        fi
    done <<< "$old_files"

    if [ "$count" -gt 0 ]; then
        log "  Archiviati $count file da $project_name/$folder_name"
    fi

    return $count
}

# Processa un progetto
process_project() {
    local project_dir="$1"
    local project_name=$(basename "$project_dir")

    log "--- Progetto: $project_name ---"

    local total_archived=0

    for folder in "${ARCHIVE_SOURCES[@]}"; do
        local source_path="$project_dir/$folder"

        if [ -d "$source_path" ]; then
            archive_old_files "$source_path" "$project_name" "$folder"
            ((total_archived+=$?)) || true
        fi
    done

    if [ "$total_archived" -eq 0 ]; then
        log "  Nessun file da archiviare"
    fi
}

# Pulisci archivi vecchi (> 90 giorni)
cleanup_old_archives() {
    log "=== Pulizia archivi vecchi (> 90 giorni) ==="

    local deleted=0

    # Trova e rimuovi archivi vecchi
    find "$ARCHIVE_DIR" -type d -mtime +90 -empty -delete 2>/dev/null && ((deleted++)) || true

    # Rimuovi file archiviati > 90 giorni
    find "$ARCHIVE_DIR" -type f -mtime +90 -delete 2>/dev/null && ((deleted++)) || true

    log "Pulizia archivi completata"
}

# Genera report settimanale
generate_weekly_report() {
    log "=== Report Settimanale ==="

    local report_file="$ARCHIVE_DIR/$WEEK/REPORT.md"

    cat > "$report_file" << EOF
# SNCP Weekly Archive Report
> Settimana: $WEEK
> Data: $TODAY

## Archiviazione Completata

File archiviati da:
EOF

    # Conta file archiviati per progetto
    for project_dir in "$ARCHIVE_DIR/$WEEK"/*/; do
        if [ -d "$project_dir" ]; then
            local project_name=$(basename "$project_dir")
            local file_count=$(find "$project_dir" -type f ! -name "REPORT.md" | wc -l | tr -d ' ')
            echo "- **$project_name**: $file_count file" >> "$report_file"
        fi
    done

    cat >> "$report_file" << EOF

## Statistiche SNCP

EOF

    # Dimensione totale SNCP
    local sncp_size=$(du -sh "$SNCP_ROOT" 2>/dev/null | cut -f1)
    local archive_size=$(du -sh "$ARCHIVE_DIR" 2>/dev/null | cut -f1)

    echo "- Dimensione SNCP attivo: $sncp_size" >> "$report_file"
    echo "- Dimensione archivio: $archive_size" >> "$report_file"

    cat >> "$report_file" << EOF

---
*Generato automaticamente da sncp_weekly_archive.sh*
*"Automatizzare TUTTO!"*
EOF

    log "Report generato: $report_file"
}

# === MAIN ===

main() {
    ensure_dirs

    log ""
    log "============================================"
    log "SNCP WEEKLY ARCHIVE - $WEEK"
    log "============================================"
    log ""

    # Processa ogni progetto
    for project_dir in "$SNCP_ROOT/progetti"/*/; do
        if [ -d "$project_dir" ]; then
            process_project "$project_dir"
        fi
    done

    echo ""

    # Pulisci archivi vecchi
    cleanup_old_archives

    # Genera report
    generate_weekly_report

    log ""
    log "Archiviazione settimanale completata!"
    log "============================================"

    # Notifica macOS
    osascript -e "display notification \"Archiviazione SNCP completata\" with title \"Weekly Archive\" sound name \"Glass\"" 2>/dev/null || true
}

main
