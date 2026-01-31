#!/bin/bash

# load-daily-memory.sh - Auto-load daily memory logs (today + yesterday)
# Author: Cervella Regina (Sessione 323)
# Date: 31 Gennaio 2026
# Version: 1.0.0
# Purpose: SNCP 4.0 QW1 - Load daily logs automatically at session start
#
# Inspired by OpenClaw pattern: auto-load today + yesterday for context continuity
#
# Usage:
#   ./load-daily-memory.sh [project]           # Output markdown
#   ./load-daily-memory.sh [project] --json    # Output JSON

set -uo pipefail

# === CONFIGURATION ===
SNCP_ROOT="${SNCP_ROOT:-/Users/rafapra/Developer/CervellaSwarm/.sncp/progetti}"

# Arguments
PROJECT="${1:-}"
OUTPUT_FORMAT="${2:-markdown}"

# Dates
TODAY=$(date +"%Y-%m-%d")
YESTERDAY=$(date -v-1d +"%Y-%m-%d" 2>/dev/null || date -d "yesterday" +"%Y-%m-%d")

# === HELP ===
if [[ "${1:-}" == "--help" ]] || [[ "${1:-}" == "-h" ]]; then
    cat << 'EOF'
load-daily-memory.sh - Auto-load daily memory logs

USAGE:
    ./load-daily-memory.sh [project]           # Output markdown
    ./load-daily-memory.sh [project] --json    # Output JSON
    ./load-daily-memory.sh --all               # All projects
    ./load-daily-memory.sh --help              # This help

EXAMPLES:
    ./load-daily-memory.sh cervellaswarm
    ./load-daily-memory.sh miracollo --json
    ./load-daily-memory.sh --all

OUTPUT (markdown):
    # Daily Memory - [project]
    ## Today (2026-01-31)
    [content]
    ## Yesterday (2026-01-30)
    [content]

OUTPUT (--json):
    {
      "project": "cervellaswarm",
      "today": { "date": "...", "content": "...", "exists": true },
      "yesterday": { "date": "...", "content": "...", "exists": false }
    }

INTEGRATION:
    This script is called by SessionStart hook to inject daily context.
    Pattern inspired by OpenClaw: always load today + yesterday.

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
    local log_path="$SNCP_ROOT/$project/memoria/$date.md"

    if [[ -f "$log_path" ]]; then
        cat "$log_path"
    fi
    # Returns empty if file doesn't exist (no echo)
}

output_markdown() {
    local project="$1"
    local today_content="$2"
    local yesterday_content="$3"

    echo "# Daily Memory - $project"
    echo ""
    echo "---"
    echo ""

    if [[ -n "$today_content" ]]; then
        echo "## 📅 Today ($TODAY)"
        echo ""
        echo "$today_content"
        echo ""
    else
        echo "## 📅 Today ($TODAY)"
        echo ""
        echo "*No daily log for today. Use \`daily-log.sh $project --init\` to create one.*"
        echo ""
    fi

    echo "---"
    echo ""

    if [[ -n "$yesterday_content" ]]; then
        echo "## 📅 Yesterday ($YESTERDAY)"
        echo ""
        echo "$yesterday_content"
        echo ""
    else
        echo "## 📅 Yesterday ($YESTERDAY)"
        echo ""
        echo "*No daily log for yesterday.*"
        echo ""
    fi

    echo "---"
    echo "*Auto-loaded by SNCP 4.0 - load-daily-memory.sh*"
}

output_json() {
    local project="$1"
    local today_content="$2"
    local yesterday_content="$3"
    local today_exists="$4"
    local yesterday_exists="$5"

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
  "today": {
    "date": "$TODAY",
    "content": $today_escaped,
    "exists": $today_exists
  },
  "yesterday": {
    "date": "$YESTERDAY",
    "content": $yesterday_escaped,
    "exists": $yesterday_exists
  }
}
EOF
}

process_project() {
    local project="$1"
    local format="$2"

    local project_dir="$SNCP_ROOT/$project"

    if [[ ! -d "$project_dir" ]]; then
        if [[ "$format" == "--json" ]]; then
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

    # Load daily logs
    local today_content=$(load_daily_log "$project" "$TODAY")
    local yesterday_content=$(load_daily_log "$project" "$YESTERDAY")

    # Output
    if [[ "$format" == "--json" ]]; then
        output_json "$project" "$today_content" "$yesterday_content" "$today_exists" "$yesterday_exists"
    else
        output_markdown "$project" "$today_content" "$yesterday_content"
    fi
}

process_all_projects() {
    local format="$1"

    for project_dir in "$SNCP_ROOT"/*/; do
        local project=$(basename "$project_dir")

        # Skip non-project directories
        [[ "$project" == "archivio" ]] && continue
        [[ "$project" == "shared" ]] && continue

        if [[ "$format" == "--json" ]]; then
            process_project "$project" "$format"
            echo ","
        else
            process_project "$project" "$format"
            echo ""
            echo "=========================================="
            echo ""
        fi
    done
}

# === MAIN ===

if [[ -z "$PROJECT" ]]; then
    echo "Error: Project name required"
    echo "Usage: load-daily-memory.sh [project|--all] [--json]"
    exit 1
fi

if [[ "$PROJECT" == "--all" ]]; then
    process_all_projects "$OUTPUT_FORMAT"
else
    process_project "$PROJECT" "$OUTPUT_FORMAT"
fi

exit 0
