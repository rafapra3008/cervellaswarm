#!/bin/bash
# log_rotate_cron.sh - Script cron per log rotation completa
#
# Ruota TUTTI i log di CervellaSwarm:
# - .swarm/logs/ (worker logs)
# - data/logs/ (hook, subagent debug)
# - logs/ (SwarmLogger jsonl)
#
# SETUP CRON:
#   crontab -e
#   # Aggiungi questa riga (aggiorna il path al tuo repo):
#   0 3 * * * $HOME/Developer/CervellaSwarm/scripts/cron/log_rotate_cron.sh
#
# Creato: 14 Gennaio 2026 - Sessione 201

set -e

# Path di base (computed from script location)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SWARM_DIR="${SWARM_DIR:-$(cd "$SCRIPT_DIR/../.." && pwd)}"
LOG_FILE="$SWARM_DIR/data/logs/log_rotate_cron.log"

# Configurazione
MAX_SIZE="5M"  # Max 5MB per file
MAX_FILES=5    # Mantieni solo 5 versioni

# Timestamp
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

rotate_file() {
    local file="$1"
    local max_bytes=$((5 * 1024 * 1024))  # 5MB

    if [[ ! -f "$file" ]]; then
        return 0
    fi

    # Get file size (macOS compatible)
    local size=$(stat -f %z "$file" 2>/dev/null || echo 0)

    if [[ $size -gt $max_bytes ]]; then
        local basename="${file%.log}"

        # Shift existing rotated files
        for i in $(seq 4 -1 1); do
            if [[ -f "${basename}.log.${i}" ]]; then
                mv "${basename}.log.${i}" "${basename}.log.$((i + 1))"
            fi
        done

        # Rotate current file
        mv "$file" "${basename}.log.1"
        touch "$file"

        log "ROTATED: $file (was $(( size / 1024 / 1024 ))MB)"
        return 1
    fi

    return 0
}

cleanup_old() {
    local dir="$1"
    local removed=0

    # Remove rotated files older than 5
    for f in "$dir"/*.log.[6-9] "$dir"/*.log.1[0-9]; do
        if [[ -f "$f" ]]; then
            rm -f "$f"
            ((removed++))
        fi
    done

    if [[ $removed -gt 0 ]]; then
        log "CLEANUP: Removed $removed old files from $dir"
    fi
}

# Main
main() {
    log "=========================================="
    log "Log Rotation STARTED"

    local rotated=0

    # 1. Rotate data/logs/ (debug logs)
    for log_file in "$SWARM_DIR/data/logs"/*.log; do
        [[ -f "$log_file" ]] || continue
        rotate_file "$log_file" && true || ((rotated++))
    done
    cleanup_old "$SWARM_DIR/data/logs"

    # 2. Rotate .swarm/logs/ (worker logs - cleanup old)
    # Worker logs are small but many, just cleanup old ones
    local old_workers=$(find "$SWARM_DIR/.swarm/logs" -name "worker_*.log" -mtime +7 2>/dev/null | wc -l)
    if [[ $old_workers -gt 0 ]]; then
        find "$SWARM_DIR/.swarm/logs" -name "worker_*.log" -mtime +7 -delete 2>/dev/null
        log "CLEANUP: Removed $old_workers worker logs older than 7 days"
    fi

    # 3. Rotate logs/ (SwarmLogger jsonl)
    for log_file in "$SWARM_DIR/logs"/*.jsonl; do
        [[ -f "$log_file" ]] || continue
        rotate_file "$log_file" && true || ((rotated++))
    done
    cleanup_old "$SWARM_DIR/logs"

    log "Log Rotation COMPLETED - Rotated: $rotated files"
    log "=========================================="
}

main "$@"
