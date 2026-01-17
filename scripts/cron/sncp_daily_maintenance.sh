#!/bin/bash
# ==============================================================================
# SNCP DAILY MAINTENANCE - Manutenzione giornaliera automatica
# ==============================================================================
#
# Eseguito da cron ogni giorno alle 8:00
# Genera report stato SNCP e pulisce file temporanei
#
# Crontab entry:
#   0 8 * * * /Users/rafapra/Developer/CervellaSwarm/scripts/cron/sncp_daily_maintenance.sh
#
# Versione: 1.0.0
# Data: 14 Gennaio 2026
# Cervella & Rafa - "Automatizzare TUTTO!"
# ==============================================================================

set -e

# === CONFIGURAZIONE ===

SNCP_ROOT="/Users/rafapra/Developer/CervellaSwarm/.sncp"
REPORTS_DIR="$SNCP_ROOT/reports/daily"
LOG_FILE="/Users/rafapra/Developer/CervellaSwarm/logs/sncp_daily.log"
HEALTH_CHECK="/Users/rafapra/Developer/CervellaSwarm/scripts/sncp/health-check.sh"
COMPLIANCE_CHECK="/Users/rafapra/Developer/CervellaSwarm/scripts/sncp/compliance-check.sh"
COMPACT_SCRIPT="/Users/rafapra/Developer/CervellaSwarm/scripts/sncp/compact-state.sh"

# Limiti per auto-compaction
AUTO_COMPACT_TRIGGER=400  # Compatta automaticamente se > 400 righe
AUTO_COMPACT_KEEP=250     # Mantiene 250 righe dopo compaction

TODAY=$(date +%Y-%m-%d)
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# === FUNZIONI ===

log() {
    echo "[$TIMESTAMP] $1" >> "$LOG_FILE"
    echo "$1"
}

ensure_dirs() {
    mkdir -p "$REPORTS_DIR"
    mkdir -p "$(dirname "$LOG_FILE")"
}

# === TASK 1: Health Check ===

run_health_check() {
    log "=== SNCP Daily Health Check ==="

    if [ -x "$HEALTH_CHECK" ]; then
        # Esegui health check e salva output
        local report_file="$REPORTS_DIR/health_$TODAY.txt"

        # Cattura output senza colori
        TERM=dumb "$HEALTH_CHECK" > "$report_file" 2>&1 || true

        log "Health check salvato: $report_file"

        # Conta warnings
        local warnings=$(grep -c "\[!\]" "$report_file" 2>/dev/null | tr -d '[:space:]' || echo "0")
        local errors=$(grep -c "\[X\]" "$report_file" 2>/dev/null | tr -d '[:space:]' || echo "0")

        if [ "$errors" -gt 0 ]; then
            log "ATTENZIONE: $errors errori trovati!"
            # Notifica macOS
            osascript -e "display notification \"SNCP: $errors errori, $warnings warnings\" with title \"Daily Maintenance\" sound name \"Basso\"" 2>/dev/null || true
        elif [ "$warnings" -gt 0 ]; then
            log "Warning: $warnings issue trovati"
        else
            log "Tutto OK!"
        fi
    else
        log "ERRORE: health-check.sh non trovato o non eseguibile"
    fi
}

# === TASK 2: Cleanup file temporanei ===

cleanup_temp_files() {
    log "=== Cleanup file temporanei ==="

    local cleaned=0

    # Rimuovi file .DS_Store
    find "$SNCP_ROOT" -name ".DS_Store" -delete 2>/dev/null && ((cleaned++)) || true

    # Rimuovi file backup vecchi (> 7 giorni)
    find "$SNCP_ROOT" -name "*.bak" -mtime +7 -delete 2>/dev/null && ((cleaned++)) || true
    find "$SNCP_ROOT" -name "*~" -mtime +7 -delete 2>/dev/null && ((cleaned++)) || true

    # Rimuovi report daily vecchi (> 30 giorni)
    find "$REPORTS_DIR" -name "health_*.txt" -mtime +30 -delete 2>/dev/null && ((cleaned++)) || true

    log "Cleanup completato"
}

# === TASK 3: Verifica dimensioni file ===

check_file_sizes() {
    log "=== Verifica dimensioni file ==="

    local large_files=0
    local compacted_files=0

    # Trova file troppo grandi nei progetti
    for project_dir in "$SNCP_ROOT/progetti"/*/; do
        if [ -d "$project_dir" ]; then
            local project_name=$(basename "$project_dir")

            # Check stato.md
            local stato_file="$project_dir/stato.md"
            if [ -f "$stato_file" ]; then
                local lines=$(wc -l < "$stato_file" | tr -d ' ')

                # AUTO-COMPACT se > 400 righe
                if [ "$lines" -gt "$AUTO_COMPACT_TRIGGER" ]; then
                    log "AUTO-COMPACT: $project_name/stato.md ha $lines righe (> $AUTO_COMPACT_TRIGGER)"
                    if [ -x "$COMPACT_SCRIPT" ]; then
                        "$COMPACT_SCRIPT" --auto "$stato_file" "$AUTO_COMPACT_TRIGGER" "$AUTO_COMPACT_KEEP" >> "$LOG_FILE" 2>&1 || true
                        ((compacted_files++))
                        log "  -> Compattato automaticamente"
                    fi
                # WARNING se > 300 righe
                elif [ "$lines" -gt 300 ]; then
                    log "WARNING: $project_name/stato.md ha $lines righe (max 300, auto-compact a $AUTO_COMPACT_TRIGGER)"
                    ((large_files++))
                fi
            fi

            # Check PROMPT_RIPRESA
            local pr_file="$project_dir/PROMPT_RIPRESA_${project_name}.md"
            if [ -f "$pr_file" ]; then
                local pr_lines=$(wc -l < "$pr_file" | tr -d ' ')
                if [ "$pr_lines" -gt 150 ]; then
                    log "WARNING: $project_name/PROMPT_RIPRESA ha $pr_lines righe (max 150)"
                    ((large_files++))
                fi
            fi
        fi
    done

    # Check oggi.md
    local oggi_file="$SNCP_ROOT/stato/oggi.md"
    if [ -f "$oggi_file" ]; then
        local oggi_lines=$(wc -l < "$oggi_file" | tr -d ' ')
        if [ "$oggi_lines" -gt "$AUTO_COMPACT_TRIGGER" ]; then
            log "AUTO-COMPACT: oggi.md ha $oggi_lines righe (> $AUTO_COMPACT_TRIGGER)"
            if [ -x "$COMPACT_SCRIPT" ]; then
                "$COMPACT_SCRIPT" --auto "$oggi_file" "$AUTO_COMPACT_TRIGGER" "$AUTO_COMPACT_KEEP" >> "$LOG_FILE" 2>&1 || true
                ((compacted_files++))
                log "  -> Compattato automaticamente"
            fi
        elif [ "$oggi_lines" -gt 60 ]; then
            log "WARNING: oggi.md ha $oggi_lines righe (max 60, auto-compact a $AUTO_COMPACT_TRIGGER)"
            ((large_files++))
        fi
    fi

    # Summary
    if [ "$compacted_files" -gt 0 ]; then
        log "AUTO-COMPACT: $compacted_files file compattati automaticamente"
        osascript -e "display notification \"$compacted_files file compattati\" with title \"SNCP Auto-Compact\" sound name \"Glass\"" 2>/dev/null || true
    fi

    if [ "$large_files" -gt 0 ]; then
        log "WARNING: $large_files file sopra limite (ma sotto auto-compact)"
    else
        log "Dimensioni file OK"
    fi
}

# === TASK 4: Compliance Check ===

run_compliance_check() {
    log "=== Compliance Check ==="

    if [ -x "$COMPLIANCE_CHECK" ]; then
        local report_file="$REPORTS_DIR/compliance_$TODAY.txt"

        # Esegui compliance check
        TERM=dumb "$COMPLIANCE_CHECK" > "$report_file" 2>&1 || true

        log "Compliance check salvato: $report_file"

        # Conta violazioni
        local violations=$(grep -c "FAIL\|ERRORE\|ERROR" "$report_file" 2>/dev/null | tr -d '[:space:]' || echo "0")

        if [ "$violations" -gt 0 ]; then
            log "ATTENZIONE: $violations violazioni trovate!"
            osascript -e "display notification \"SNCP: $violations violazioni compliance\" with title \"Daily Maintenance\" sound name \"Basso\"" 2>/dev/null || true
        else
            log "Compliance OK!"
        fi
    else
        log "WARNING: compliance-check.sh non trovato"
    fi
}

# === TASK 5: Statistiche ===

generate_stats() {
    log "=== Statistiche SNCP ==="

    # Conta file per progetto
    for project_dir in "$SNCP_ROOT/progetti"/*/; do
        if [ -d "$project_dir" ]; then
            local project_name=$(basename "$project_dir")
            local file_count=$(find "$project_dir" -type f | wc -l | tr -d ' ')
            log "  $project_name: $file_count file"
        fi
    done

    # Dimensione totale SNCP
    local total_size=$(du -sh "$SNCP_ROOT" 2>/dev/null | cut -f1)
    log "  Dimensione totale SNCP: $total_size"
}

# === MAIN ===

main() {
    ensure_dirs

    log ""
    log "============================================"
    log "SNCP DAILY MAINTENANCE - $TODAY"
    log "============================================"

    run_health_check
    cleanup_temp_files
    check_file_sizes
    run_compliance_check
    generate_stats

    log ""
    log "Manutenzione completata!"
    log "============================================"
}

main
