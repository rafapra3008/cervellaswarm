#!/bin/bash

# load-daily-memory.sh - Auto-load daily memory logs (today + yesterday)
# Author: Cervella Regina (Sessione 323)
# Date: 2 Febbraio 2026
# Version: 2.0.0
# Purpose: SNCP 5.0 P2.1 - Progressive Disclosure for daily logs
#
# Inspired by:
# - OpenClaw pattern: auto-load today + yesterday for context continuity
# - ClaudeMem: progressive disclosure (10x token savings)
#
# Usage:
#   ./load-daily-memory.sh [project]              # Summary mode (default, 20 lines)
#   ./load-daily-memory.sh [project] --full       # Full content
#   ./load-daily-memory.sh [project] --json       # Output JSON (summary)
#   ./load-daily-memory.sh [project] --json --full # Output JSON (full)

set -uo pipefail

# === CONFIGURATION ===
SNCP_ROOT="${SNCP_ROOT:-/Users/rafapra/Developer/CervellaSwarm/.sncp/progetti}"
SUMMARY_LINES=20  # Lines to show in summary mode (progressive disclosure)

# Parse arguments
PROJECT=""
OUTPUT_FORMAT="markdown"
LOAD_MODE="summary"  # Default: summary (SNCP 5.0 progressive disclosure)

for arg in "$@"; do
    case "$arg" in
        --json)
            OUTPUT_FORMAT="json"
            ;;
        --full)
            LOAD_MODE="full"
            ;;
        --summary)
            LOAD_MODE="summary"
            ;;
        --help|-h)
            PROJECT="--help"
            ;;
        --all)
            PROJECT="--all"
            ;;
        *)
            # First non-flag argument is project
            if [[ -z "$PROJECT" ]]; then
                PROJECT="$arg"
            fi
            ;;
    esac
done

# Dates
TODAY=$(date +"%Y-%m-%d")
YESTERDAY=$(date -v-1d +"%Y-%m-%d" 2>/dev/null || date -d "yesterday" +"%Y-%m-%d")

# === HELP ===
if [[ "$PROJECT" == "--help" ]]; then
    cat << 'EOF'
load-daily-memory.sh - Auto-load daily memory logs (SNCP 5.0)

USAGE:
    ./load-daily-memory.sh [project]              # Summary mode (default)
    ./load-daily-memory.sh [project] --full       # Full content
    ./load-daily-memory.sh [project] --json       # JSON output (summary)
    ./load-daily-memory.sh [project] --json --full # JSON output (full)
    ./load-daily-memory.sh --all                  # All projects
    ./load-daily-memory.sh --help                 # This help

FLAGS:
    --summary   Load first 20 lines only (DEFAULT - token savings)
    --full      Load complete content (backward compatible)
    --json      Output as JSON instead of markdown

EXAMPLES:
    ./load-daily-memory.sh cervellaswarm            # Summary, markdown
    ./load-daily-memory.sh cervellaswarm --full     # Full, markdown
    ./load-daily-memory.sh miracollo --json         # Summary, JSON
    ./load-daily-memory.sh miracollo --json --full  # Full, JSON

PROGRESSIVE DISCLOSURE (SNCP 5.0):
    Default mode is --summary (first 20 lines per log).
    This saves tokens while keeping recent context.
    Use /expand-daily command to load full content on demand.

OUTPUT (markdown, --summary):
    # Daily Memory - [project] (Summary)
    ## Today (2026-02-02)
    [first 20 lines]
    *[Truncated - use /expand-daily for full content]*

OUTPUT (markdown, --full):
    # Daily Memory - [project]
    ## Today (2026-02-02)
    [complete content]

INTEGRATION:
    Called by SessionStart hook with --summary (default).
    Use --full for /expand-daily command.

EOF
    exit 0
fi

# === FUNCTIONS ===

check_daily_log_exists() {
    local project="$1"
    local date="$2"
    local log_path="$SNCP_ROOT/$project/memoria/$date.md"
    [[ -f "$log_path" ]]
}

load_daily_log() {
    local project="$1"
    local date="$2"
    local mode="$3"  # "summary" or "full"
    local log_path="$SNCP_ROOT/$project/memoria/$date.md"

    if [[ -f "$log_path" ]]; then
        if [[ "$mode" == "summary" ]]; then
            # Progressive disclosure: first N lines only
            head -n "$SUMMARY_LINES" "$log_path"
        else
            # Full content
            cat "$log_path"
        fi
    fi
    # Returns empty if file doesn't exist (no echo)
}

# Check if daily log has more than SUMMARY_LINES
log_is_truncated() {
    local project="$1"
    local date="$2"
    local log_path="$SNCP_ROOT/$project/memoria/$date.md"

    if [[ -f "$log_path" ]]; then
        local total_lines=$(wc -l < "$log_path")
        [[ "$total_lines" -gt "$SUMMARY_LINES" ]]
    else
        return 1
    fi
}

output_markdown() {
    local project="$1"
    local today_content="$2"
    local yesterday_content="$3"
    local mode="$4"
    local today_truncated="$5"
    local yesterday_truncated="$6"

    local mode_label=""
    if [[ "$mode" == "summary" ]]; then
        mode_label=" (Summary - first $SUMMARY_LINES lines)"
    fi

    echo "# Daily Memory - $project$mode_label"
    echo ""
    echo "---"
    echo ""

    if [[ -n "$today_content" ]]; then
        echo "## Today ($TODAY)"
        echo ""
        echo "$today_content"
        if [[ "$today_truncated" == "true" && "$mode" == "summary" ]]; then
            echo ""
            echo "*[Truncated] Use \`/expand-daily $TODAY\` for full content*"
        fi
        echo ""
    else
        echo "## Today ($TODAY)"
        echo ""
        echo "*No daily log for today. Use \`daily-log.sh $project --init\` to create one.*"
        echo ""
    fi

    echo "---"
    echo ""

    if [[ -n "$yesterday_content" ]]; then
        echo "## Yesterday ($YESTERDAY)"
        echo ""
        echo "$yesterday_content"
        if [[ "$yesterday_truncated" == "true" && "$mode" == "summary" ]]; then
            echo ""
            echo "*[Truncated] Use \`/expand-daily $YESTERDAY\` for full content*"
        fi
        echo ""
    else
        echo "## Yesterday ($YESTERDAY)"
        echo ""
        echo "*No daily log for yesterday.*"
        echo ""
    fi

    echo "---"
    echo "*Auto-loaded by SNCP 5.0 - load-daily-memory.sh v2.0.0*"
}

output_json() {
    local project="$1"
    local today_content="$2"
    local yesterday_content="$3"
    local today_exists="$4"
    local yesterday_exists="$5"
    local mode="$6"
    local today_truncated="$7"
    local yesterday_truncated="$8"

    # Escape content for JSON (handle empty strings)
    local today_escaped
    local yesterday_escaped

    if [[ -n "$today_content" ]]; then
        today_escaped=$(printf '%s' "$today_content" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')
    else
        today_escaped='""'
    fi

    if [[ -n "$yesterday_content" ]]; then
        yesterday_escaped=$(printf '%s' "$yesterday_content" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')
    else
        yesterday_escaped='""'
    fi

    cat << EOF
{
  "project": "$project",
  "mode": "$mode",
  "summary_lines": $SUMMARY_LINES,
  "today": {
    "date": "$TODAY",
    "content": $today_escaped,
    "exists": $today_exists,
    "truncated": $today_truncated
  },
  "yesterday": {
    "date": "$YESTERDAY",
    "content": $yesterday_escaped,
    "exists": $yesterday_exists,
    "truncated": $yesterday_truncated
  }
}
EOF
}

process_project() {
    local project="$1"
    local format="$2"
    local mode="$3"

    local project_dir="$SNCP_ROOT/$project"

    if [[ ! -d "$project_dir" ]]; then
        if [[ "$format" == "json" ]]; then
            echo "{\"error\": \"Project not found: $project\"}"
        else
            echo "Error: Project not found: $project"
        fi
        return 1
    fi

    # Create memoria directory if not exists
    mkdir -p "$project_dir/memoria"
    mkdir -p "$project_dir/memoria/archivio"

    # Check if daily logs exist
    local today_exists="false"
    local yesterday_exists="false"
    check_daily_log_exists "$project" "$TODAY" && today_exists="true"
    check_daily_log_exists "$project" "$YESTERDAY" && yesterday_exists="true"

    # Check if logs would be truncated in summary mode
    local today_truncated="false"
    local yesterday_truncated="false"
    log_is_truncated "$project" "$TODAY" && today_truncated="true"
    log_is_truncated "$project" "$YESTERDAY" && yesterday_truncated="true"

    # Load daily logs (with mode: summary or full)
    local today_content=$(load_daily_log "$project" "$TODAY" "$mode")
    local yesterday_content=$(load_daily_log "$project" "$YESTERDAY" "$mode")

    # Output
    if [[ "$format" == "json" ]]; then
        output_json "$project" "$today_content" "$yesterday_content" "$today_exists" "$yesterday_exists" "$mode" "$today_truncated" "$yesterday_truncated"
    else
        output_markdown "$project" "$today_content" "$yesterday_content" "$mode" "$today_truncated" "$yesterday_truncated"
    fi
}

process_all_projects() {
    local format="$1"
    local mode="$2"

    for project_dir in "$SNCP_ROOT"/*/; do
        local project=$(basename "$project_dir")

        # Skip non-project directories
        [[ "$project" == "archivio" ]] && continue
        [[ "$project" == "shared" ]] && continue

        if [[ "$format" == "json" ]]; then
            process_project "$project" "$format" "$mode"
            echo ","
        else
            process_project "$project" "$format" "$mode"
            echo ""
            echo "=========================================="
            echo ""
        fi
    done
}

# === MAIN ===

if [[ -z "$PROJECT" ]]; then
    echo "Error: Project name required"
    echo "Usage: load-daily-memory.sh [project|--all] [--summary|--full] [--json]"
    exit 1
fi

if [[ "$PROJECT" == "--all" ]]; then
    process_all_projects "$OUTPUT_FORMAT" "$LOAD_MODE"
else
    process_project "$PROJECT" "$OUTPUT_FORMAT" "$LOAD_MODE"
fi

exit 0
