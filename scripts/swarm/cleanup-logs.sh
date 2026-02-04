#!/bin/bash

# cleanup-logs.sh - Archive old swarm logs
# Author: Cervella Backend
# Date: 4 Febbraio 2026
# Version: 1.0.0
#
# Purpose: Prevent log accumulation by archiving old files
# Strategy: Move (not delete) logs > 30 days to archive
#
# Usage:
#   cleanup-logs.sh              # Dry-run (shows what would be archived)
#   cleanup-logs.sh --execute    # Actually archive files
#   cleanup-logs.sh --days 60    # Custom retention (dry-run)
#   cleanup-logs.sh --execute --days 60  # Archive > 60 days

set -euo pipefail

# Colors
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Defaults
DAYS=30
DRY_RUN=true
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SWARM_DIR="$PROJECT_ROOT/.swarm"
ARCHIVE_DIR="$SWARM_DIR/archive"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --execute)
            DRY_RUN=false
            shift
            ;;
        --days)
            DAYS="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: cleanup-logs.sh [OPTIONS]"
            echo ""
            echo "Archive old swarm logs to prevent accumulation."
            echo ""
            echo "Options:"
            echo "  --execute        Actually archive files (default: dry-run)"
            echo "  --days N         Retention days (default: 30)"
            echo "  --help           Show this help"
            echo ""
            echo "Examples:"
            echo "  cleanup-logs.sh                    # Dry-run, 30 days"
            echo "  cleanup-logs.sh --execute          # Archive > 30 days"
            echo "  cleanup-logs.sh --days 60          # Dry-run, 60 days"
            echo "  cleanup-logs.sh --execute --days 7 # Archive > 7 days"
            echo ""
            echo "What it does:"
            echo "  1. Find logs/heartbeat files > N days old"
            echo "  2. Move to .swarm/archive/YYYY-MM/"
            echo "  3. Log operation to cleanup.log"
            echo "  4. Never deletes (only moves)"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage"
            exit 1
            ;;
    esac
done

# Validate retention
if ! [[ "$DAYS" =~ ^[0-9]+$ ]] || [[ "$DAYS" -lt 1 ]]; then
    echo -e "${RED}Error: --days must be a positive number${NC}"
    exit 1
fi

# Header
echo -e "${BLUE}=== Swarm Log Cleanup ===${NC}"
echo ""
if [[ "$DRY_RUN" == "true" ]]; then
    echo -e "${YELLOW}MODE: DRY-RUN (use --execute to archive)${NC}"
else
    echo -e "${GREEN}MODE: EXECUTE${NC}"
fi
echo "Retention: $DAYS days"
echo ""

# Ensure directories exist
mkdir -p "$ARCHIVE_DIR"

# Function to archive a file
archive_file() {
    local file="$1"
    local relative_path="${file#$SWARM_DIR/}"
    local year_month=$(date -r "$file" +"%Y-%m")
    local dest_dir="$ARCHIVE_DIR/$year_month"
    local dest_file="$dest_dir/$(basename "$file")"

    if [[ "$DRY_RUN" == "true" ]]; then
        echo "  [DRY-RUN] $relative_path → archive/$year_month/"
    else
        mkdir -p "$dest_dir"
        mv "$file" "$dest_file"
        echo "  ✓ $relative_path → archive/$year_month/"
    fi
}

# Find and archive old logs
echo -e "${BLUE}Checking logs directory...${NC}"
old_logs=$(find "$SWARM_DIR/logs" -type f -mtime +$DAYS 2>/dev/null || true)
log_count=0

if [[ -n "$old_logs" ]]; then
    while IFS= read -r file; do
        archive_file "$file"
        ((log_count++))
    done <<< "$old_logs"
else
    echo "  No old logs found"
fi

# Find and archive old heartbeat/status files
echo ""
echo -e "${BLUE}Checking status directory...${NC}"
old_status=$(find "$SWARM_DIR/status" -type f -mtime +$DAYS 2>/dev/null || true)
status_count=0

if [[ -n "$old_status" ]]; then
    while IFS= read -r file; do
        archive_file "$file"
        ((status_count++))
    done <<< "$old_status"
else
    echo "  No old status files found"
fi

# Summary
echo ""
echo -e "${BLUE}=== Summary ===${NC}"
echo "Logs archived:   $log_count"
echo "Status archived: $status_count"
echo "Total:           $((log_count + status_count))"

if [[ "$DRY_RUN" == "true" ]]; then
    echo ""
    echo -e "${YELLOW}This was a dry-run. Use --execute to archive files.${NC}"
else
    # Log operation
    cleanup_log="$SWARM_DIR/logs/cleanup.log"
    echo "[$TIMESTAMP] Archived $((log_count + status_count)) files (retention: $DAYS days)" >> "$cleanup_log"
    echo ""
    echo -e "${GREEN}Cleanup complete!${NC}"
fi

echo ""
exit 0
