#!/bin/bash

# consolidate-ripresa.sh - Auto-consolidate PROMPT_RIPRESA when approaching limit
# Author: Cervella Regina (Sessione 328)
# Date: 2 Febbraio 2026
# Version: 1.0.0
# Purpose: SNCP 5.0 P2.2 - Consolidation Scheduler
#
# Inspired by:
# - MCP-Memory: consolidation achieves 88% token reduction
# - ClaudeMem: progressive disclosure pattern
#
# Usage:
#   ./consolidate-ripresa.sh [project]           # Consolidate specific project
#   ./consolidate-ripresa.sh --all               # Check all projects
#   ./consolidate-ripresa.sh --check [project]   # Dry-run (no changes)
#   ./consolidate-ripresa.sh --help              # Help

set -euo pipefail

# === CONFIGURATION ===
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SNCP_ROOT="${SNCP_ROOT:-$REPO_ROOT/.sncp/progetti}"

# Thresholds
LIMIT=150          # Maximum allowed lines
WARNING=120        # Trigger consolidation threshold (80%)
TARGET=80          # Target lines after consolidation

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Modes
DRY_RUN=false
VERBOSE=false

# === HELP ===
show_help() {
    cat << 'EOF'
consolidate-ripresa.sh - Auto-consolidate PROMPT_RIPRESA (SNCP 5.0 P2.2)

USAGE:
    ./consolidate-ripresa.sh [project]           # Consolidate specific project
    ./consolidate-ripresa.sh --all               # Check all projects
    ./consolidate-ripresa.sh --check [project]   # Dry-run (no changes)
    ./consolidate-ripresa.sh --help              # This help

OPTIONS:
    --check, -c     Dry-run mode (shows what would be consolidated)
    --verbose, -v   Show detailed output
    --force, -f     Force consolidation even if under threshold

THRESHOLDS:
    WARNING:  120 lines (80% of limit) - triggers consolidation
    LIMIT:    150 lines (maximum allowed)
    TARGET:   80 lines (goal after consolidation)

PROCESS:
    1. Detect PROMPT_RIPRESA > 120 lines
    2. Send to Claude Haiku for intelligent consolidation
    3. Haiku identifies:
       - Duplicates → merge
       - Obsolete (>30 days) → archive
       - Contradictions → resolve
    4. Write consolidated version
    5. Archive original to archivio/YYYY-MM/

REQUIREMENTS:
    - ANTHROPIC_API_KEY environment variable (for Haiku API)
    - jq installed (for JSON parsing)

EXAMPLES:
    ./consolidate-ripresa.sh cervellaswarm       # Consolidate cervellaswarm
    ./consolidate-ripresa.sh --check miracollo   # Dry-run for miracollo
    ./consolidate-ripresa.sh --all               # Process all projects

OUTPUT:
    - Consolidated PROMPT_RIPRESA_*.md (in place)
    - Original archived to archivio/YYYY-MM/
    - Log in .swarm/logs/consolidation_*.log

EOF
    exit 0
}

# === UTILITY FUNCTIONS ===

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    # Check jq
    if ! command -v jq &> /dev/null; then
        log_error "jq is required but not installed. Install with: brew install jq"
        exit 1
    fi

    # Check ANTHROPIC_API_KEY
    if [[ -z "${ANTHROPIC_API_KEY:-}" ]]; then
        log_error "ANTHROPIC_API_KEY environment variable not set"
        echo ""
        echo "To set it:"
        echo "  export ANTHROPIC_API_KEY='your-api-key'"
        echo ""
        echo "Or add to ~/.zshrc for persistence"
        exit 1
    fi

    log_success "Prerequisites OK (jq installed, API key set)"
}

# Get line count of a file
get_line_count() {
    local file="$1"
    if [[ -f "$file" ]]; then
        wc -l < "$file" | tr -d ' '
    else
        echo "0"
    fi
}

# Find PROMPT_RIPRESA file for a project
find_ripresa_file() {
    local project="$1"
    local file="$SNCP_ROOT/$project/PROMPT_RIPRESA_$project.md"

    if [[ -f "$file" ]]; then
        echo "$file"
    else
        echo ""
    fi
}

# Create archive directory
ensure_archive_dir() {
    local project="$1"
    local year_month=$(date +"%Y-%m")
    local archive_dir="$SNCP_ROOT/$project/archivio/$year_month"

    mkdir -p "$archive_dir"
    echo "$archive_dir"
}

# Archive original file before consolidation
archive_original() {
    local file="$1"
    local project="$2"
    local archive_dir=$(ensure_archive_dir "$project")
    local timestamp=$(date +"%Y%m%d_%H%M%S")
    local filename=$(basename "$file")
    local archive_name="${filename%.md}_${timestamp}.md"

    cp "$file" "$archive_dir/$archive_name"
    log_success "Archived original to: $archive_dir/$archive_name"
    echo "$archive_dir/$archive_name"
}

# === HAIKU API CONSOLIDATION ===

call_haiku_api() {
    local content="$1"
    local project="$2"

    # Build the prompt for Haiku
    local system_prompt="You are a PROMPT_RIPRESA consolidator for the CervellaSwarm project.

Your task is to consolidate the given PROMPT_RIPRESA file to reduce its size while preserving all important information.

RULES:
1. TARGET: Reduce to ~80 lines maximum
2. KEEP: Current status, active decisions, recent sessions (last 2-3)
3. MERGE: Duplicate information, similar entries
4. ARCHIVE: Sessions older than 30 days → summarize in 1-2 lines each
5. REMOVE: Completed TODOs (marked done), obsolete decisions (superseded)
6. PRESERVE: All version numbers, links, code blocks, critical decisions

FORMAT:
- Keep the exact markdown structure
- Keep headers (##, ###)
- Output ONLY the consolidated content, no explanations
- Start directly with the first line of the consolidated file"

    local user_prompt="Consolidate this PROMPT_RIPRESA file for project '$project':

---
$content
---

Remember: Output ONLY the consolidated markdown, nothing else. Target ~80 lines."

    # API call with curl
    local response
    response=$(curl -s https://api.anthropic.com/v1/messages \
        -H "Content-Type: application/json" \
        -H "x-api-key: ${ANTHROPIC_API_KEY}" \
        -H "anthropic-version: 2023-06-01" \
        -d "$(jq -n \
            --arg model "claude-3-haiku-20240307" \
            --arg system "$system_prompt" \
            --arg user "$user_prompt" \
            '{
                model: $model,
                max_tokens: 4096,
                system: $system,
                messages: [{role: "user", content: $user}]
            }'
        )" 2>&1)

    # Check for errors
    if echo "$response" | jq -e '.error' > /dev/null 2>&1; then
        local error_msg=$(echo "$response" | jq -r '.error.message')
        log_error "API error: $error_msg"
        return 1
    fi

    # Extract content
    local consolidated
    consolidated=$(echo "$response" | jq -r '.content[0].text')

    if [[ -z "$consolidated" || "$consolidated" == "null" ]]; then
        log_error "Empty response from Haiku API"
        return 1
    fi

    echo "$consolidated"
}

# === CONSOLIDATION LOGIC ===

consolidate_project() {
    local project="$1"
    local force="${2:-false}"

    log_info "Processing project: $project"

    # Find PROMPT_RIPRESA file
    local file=$(find_ripresa_file "$project")
    if [[ -z "$file" ]]; then
        log_warning "No PROMPT_RIPRESA found for project: $project"
        return 1
    fi

    # Get current line count
    local lines=$(get_line_count "$file")
    local percent=$((lines * 100 / LIMIT))

    log_info "Current size: $lines lines ($percent% of limit)"

    # Check if consolidation needed
    if [[ "$force" != "true" && "$lines" -lt "$WARNING" ]]; then
        log_success "Under threshold ($WARNING lines). No consolidation needed."
        return 0
    fi

    if [[ "$lines" -ge "$WARNING" ]]; then
        log_warning "Above threshold! Consolidation recommended."
    fi

    # Dry-run mode
    if [[ "$DRY_RUN" == "true" ]]; then
        echo ""
        echo -e "${CYAN}[DRY-RUN] Would consolidate:${NC}"
        echo "  File: $file"
        echo "  Current: $lines lines"
        echo "  Target: ~$TARGET lines"
        echo "  Savings: ~$((lines - TARGET)) lines"
        return 0
    fi

    # Archive original first
    log_info "Archiving original..."
    local archived_file=$(archive_original "$file" "$project")

    # Read current content
    local content
    content=$(cat "$file")

    # Call Haiku API
    log_info "Calling Claude Haiku for consolidation..."
    local consolidated
    consolidated=$(call_haiku_api "$content" "$project")

    if [[ $? -ne 0 || -z "$consolidated" ]]; then
        log_error "Consolidation failed. Restoring original..."
        cp "$archived_file" "$file"
        return 1
    fi

    # Write consolidated version
    echo "$consolidated" > "$file"

    # Verify result
    local new_lines=$(get_line_count "$file")
    local savings=$((lines - new_lines))
    local savings_percent=$((savings * 100 / lines))

    log_success "Consolidation complete!"
    echo ""
    echo "  Before: $lines lines"
    echo "  After:  $new_lines lines"
    echo "  Saved:  $savings lines ($savings_percent%)"
    echo "  Original archived: $archived_file"

    # Log the consolidation
    local log_dir="$REPO_ROOT/.swarm/logs"
    mkdir -p "$log_dir"
    local log_file="$log_dir/consolidation_$(date +%Y%m%d_%H%M%S).log"

    cat > "$log_file" << EOF
# Consolidation Log

Date: $(date +"%Y-%m-%d %H:%M:%S")
Project: $project
File: $file

## Results
- Before: $lines lines
- After: $new_lines lines
- Saved: $savings lines ($savings_percent%)

## Archive
- Original: $archived_file

## API
- Model: claude-3-haiku-20240307
- Status: SUCCESS

---
*Generated by consolidate-ripresa.sh v1.0.0*
EOF

    log_info "Log saved: $log_file"
}

process_all_projects() {
    log_info "Scanning all projects..."
    echo ""

    local needs_consolidation=()

    for project_dir in "$SNCP_ROOT"/*/; do
        local project=$(basename "$project_dir")

        # Skip non-project directories
        [[ "$project" == "archivio" ]] && continue
        [[ "$project" == "shared" ]] && continue

        local file=$(find_ripresa_file "$project")
        if [[ -z "$file" ]]; then
            continue
        fi

        local lines=$(get_line_count "$file")
        local percent=$((lines * 100 / LIMIT))

        # Determine status
        local status=""
        local color=""

        if [[ $lines -gt $LIMIT ]]; then
            status="OVER LIMIT"
            color="$RED"
            needs_consolidation+=("$project")
        elif [[ $lines -ge $WARNING ]]; then
            status="NEEDS CONSOLIDATION"
            color="$YELLOW"
            needs_consolidation+=("$project")
        else
            status="OK"
            color="$GREEN"
        fi

        printf "%-20s %4d/%-4d (%3d%%) " "$project" "$lines" "$LIMIT" "$percent"
        echo -e "${color}${status}${NC}"
    done

    echo ""

    if [[ ${#needs_consolidation[@]} -gt 0 ]]; then
        echo "=================================================="
        echo -e "${YELLOW}Projects needing consolidation:${NC}"
        for project in "${needs_consolidation[@]}"; do
            echo "  - $project"
        done
        echo ""
        echo "Run with project name to consolidate:"
        echo "  ./consolidate-ripresa.sh <project>"
    else
        echo -e "${GREEN}All projects within limits!${NC}"
    fi
}

# === MAIN ===

# Parse arguments
PROJECT=""
FORCE=false

for arg in "$@"; do
    case "$arg" in
        --help|-h)
            show_help
            ;;
        --check|-c)
            DRY_RUN=true
            ;;
        --verbose|-v)
            VERBOSE=true
            ;;
        --force|-f)
            FORCE=true
            ;;
        --all)
            PROJECT="--all"
            ;;
        *)
            if [[ -z "$PROJECT" ]]; then
                PROJECT="$arg"
            fi
            ;;
    esac
done

# Header
echo ""
echo "=================================================="
echo -e "${BLUE}SNCP 5.0 - Consolidation Scheduler${NC}"
echo "=================================================="
echo ""

# Prerequisites needed only for actual consolidation (not --all scan or --check dry-run)
if [[ "$DRY_RUN" != "true" && "$PROJECT" != "--all" ]]; then
    check_prerequisites
fi

# Execute
if [[ -z "$PROJECT" ]]; then
    echo "Usage: consolidate-ripresa.sh [project|--all] [--check] [--force]"
    echo ""
    echo "Run with --help for full documentation"
    exit 1
fi

if [[ "$PROJECT" == "--all" ]]; then
    process_all_projects
else
    consolidate_project "$PROJECT" "$FORCE"
fi

exit 0
