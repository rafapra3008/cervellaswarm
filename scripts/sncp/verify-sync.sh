#!/bin/bash
# ==============================================================================
# VERIFY-SYNC - Verifica coerenza tra documentazione e codice
# ==============================================================================
#
# PROBLEMA CHE RISOLVE:
#   Cervella A fa lavoro -> NON aggiorna docs
#   Cervella B legge docs -> Pensa sia TODO
#   TEMPO PERSO!
#
# Uso:
#   verify-sync.sh                    # Check tutti i progetti
#   verify-sync.sh miracollo          # Check singolo progetto
#   verify-sync.sh --verbose          # Output dettagliato
#
# Versione: 1.0.0
# Data: 14 Gennaio 2026
# Cervella & Rafa
# ==============================================================================

set -e

# ==============================================================================
# CONFIG
# ==============================================================================

SNCP_ROOT="${SNCP_ROOT:-/Users/rafapra/Developer/CervellaSwarm/.sncp}"
DEVELOPER_ROOT="${DEVELOPER_ROOT:-$HOME/Developer}"
TODAY=$(date +%Y-%m-%d)
VERSION="1.0.0"
VERBOSE=false

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Counters
TOTAL_WARNINGS=0
TOTAL_ERRORS=0

# ==============================================================================
# PROJECT MAPPINGS (compatibile bash 3.x macOS)
# ==============================================================================

get_project_path() {
    local project="$1"
    case "$project" in
        miracollo)     echo "$DEVELOPER_ROOT/miracollogeminifocus" ;;
        cervellaswarm) echo "$DEVELOPER_ROOT/CervellaSwarm" ;;
        contabilita)   echo "$DEVELOPER_ROOT/ContabilitaAntigravity" ;;
        *)             echo "" ;;
    esac
}

# ==============================================================================
# FUNCTIONS
# ==============================================================================

print_header() {
    echo ""
    echo -e "${PURPLE}+================================================================+${NC}"
    echo -e "${PURPLE}|              VERIFY-SYNC - Coerenza Docs/Codice               |${NC}"
    echo -e "${PURPLE}|               v$VERSION - \"La verita' sincronizzata\"            |${NC}"
    echo -e "${PURPLE}+================================================================+${NC}"
    echo ""
}

print_usage() {
    echo "Uso: verify-sync.sh [progetto] [opzioni]"
    echo ""
    echo "Progetti disponibili:"
    echo "  miracollo      - MiracolloGeminiFocus"
    echo "  cervellaswarm  - CervellaSwarm"
    echo "  contabilita    - ContabilitaAntigravity"
    echo "  (vuoto)        - Tutti i progetti"
    echo ""
    echo "Opzioni:"
    echo "  --verbose, -v  Output dettagliato"
    echo "  --help, -h     Mostra questo messaggio"
    echo ""
}

log_info() {
    echo -e "${BLUE}[i]${NC} $1"
}

log_ok() {
    echo -e "${GREEN}[OK]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[!]${NC} $1"
    ((TOTAL_WARNINGS++))
}

log_error() {
    echo -e "${RED}[X]${NC} $1"
    ((TOTAL_ERRORS++))
}

# ------------------------------------------------------------------------------
# Check 1: stato.md aggiornato di recente
# ------------------------------------------------------------------------------
check_stato_freshness() {
    local project="$1"
    local stato_file="$SNCP_ROOT/progetti/$project/stato.md"

    if [ ! -f "$stato_file" ]; then
        log_error "$project: stato.md NON ESISTE"
        return 1
    fi

    # Get file modification date
    local file_date=$(stat -f "%Sm" -t "%Y-%m-%d" "$stato_file" 2>/dev/null)

    # Calculate days since last update
    local file_epoch=$(date -j -f "%Y-%m-%d" "$file_date" +%s 2>/dev/null)
    local today_epoch=$(date +%s)
    local days_diff=$(( (today_epoch - file_epoch) / 86400 ))

    if [ "$days_diff" -eq 0 ]; then
        log_ok "$project: stato.md aggiornato oggi"
        return 0
    elif [ "$days_diff" -le 2 ]; then
        log_warn "$project: stato.md non aggiornato da $days_diff giorni"
        return 1
    else
        log_error "$project: stato.md STALE ($days_diff giorni fa!)"
        return 1
    fi
}

# ------------------------------------------------------------------------------
# Check 2: Commit recenti non documentati
# ------------------------------------------------------------------------------
check_undocumented_commits() {
    local project="$1"
    local project_path="$(get_project_path "$project")"
    local stato_file="$SNCP_ROOT/progetti/$project/stato.md"

    if [ -z "$project_path" ] || [ ! -d "$project_path" ]; then
        if [ "$VERBOSE" = true ]; then
            log_warn "$project: Path non configurato o non esistente"
        fi
        return 0
    fi

    if [ ! -d "$project_path/.git" ]; then
        if [ "$VERBOSE" = true ]; then
            log_info "$project: Non e' un repo git, skip check commit"
        fi
        return 0
    fi

    # Get recent commits (last 5)
    local recent_commits=$(cd "$project_path" && git log --oneline -5 --format="%h %s" 2>/dev/null)

    if [ -z "$recent_commits" ]; then
        return 0
    fi

    # Check if any commit hash is mentioned in stato.md
    local undocumented=0
    local stato_content=$(cat "$stato_file" 2>/dev/null || echo "")

    while IFS= read -r commit; do
        local hash=$(echo "$commit" | cut -d' ' -f1)
        if ! echo "$stato_content" | grep -q "$hash" 2>/dev/null; then
            ((undocumented++))
            if [ "$VERBOSE" = true ]; then
                echo -e "    ${CYAN}Commit non in docs:${NC} $commit"
            fi
        fi
    done <<< "$recent_commits"

    if [ "$undocumented" -gt 0 ]; then
        log_warn "$project: $undocumented commit recenti non in stato.md"
        return 1
    else
        log_ok "$project: Commit documentati in stato.md"
        return 0
    fi
}

# ------------------------------------------------------------------------------
# Check 3: Migrations non documentate (per progetti con DB)
# ------------------------------------------------------------------------------
check_migrations() {
    local project="$1"
    local project_path="$(get_project_path "$project")"
    local stato_file="$SNCP_ROOT/progetti/$project/stato.md"

    if [ -z "$project_path" ] || [ ! -d "$project_path" ]; then
        return 0
    fi

    # Find migrations directory
    local migrations_dir=""
    if [ -d "$project_path/backend/migrations" ]; then
        migrations_dir="$project_path/backend/migrations"
    elif [ -d "$project_path/migrations" ]; then
        migrations_dir="$project_path/migrations"
    elif [ -d "$project_path/alembic/versions" ]; then
        migrations_dir="$project_path/alembic/versions"
    fi

    if [ -z "$migrations_dir" ]; then
        if [ "$VERBOSE" = true ]; then
            log_info "$project: Nessuna cartella migrations trovata"
        fi
        return 0
    fi

    # Count migrations
    local migration_count=$(find "$migrations_dir" -name "*.sql" -o -name "*.py" 2>/dev/null | wc -l | tr -d ' ')

    if [ "$migration_count" -eq 0 ]; then
        return 0
    fi

    # Check if migration count is mentioned in stato.md
    local stato_content=$(cat "$stato_file" 2>/dev/null || echo "")

    # Look for migration mentions
    local doc_migrations=$(echo "$stato_content" | grep -ci "migration" || echo "0")

    if [ "$doc_migrations" -eq 0 ]; then
        log_warn "$project: $migration_count migrations ma nessuna menzionata in stato.md"
        return 1
    else
        if [ "$VERBOSE" = true ]; then
            log_ok "$project: Migrations menzionate in stato.md"
        fi
        return 0
    fi
}

# ------------------------------------------------------------------------------
# Check 4: File grandi modificati recentemente
# ------------------------------------------------------------------------------
check_recent_large_changes() {
    local project="$1"
    local project_path="$(get_project_path "$project")"

    if [ -z "$project_path" ] || [ ! -d "$project_path" ]; then
        return 0
    fi

    if [ ! -d "$project_path/.git" ]; then
        return 0
    fi

    # Get files changed in last commit with >50 lines changed
    local large_changes=$(cd "$project_path" && git diff --stat HEAD~1 2>/dev/null | grep -E "\+[0-9]{2,}" | head -5)

    if [ -n "$large_changes" ]; then
        if [ "$VERBOSE" = true ]; then
            log_warn "$project: File con modifiche significative nell'ultimo commit:"
            echo "$large_changes" | while read line; do
                echo -e "    ${CYAN}$line${NC}"
            done
        fi
        return 1
    fi

    return 0
}

# ------------------------------------------------------------------------------
# Check progetto completo
# ------------------------------------------------------------------------------
check_project() {
    local project="$1"

    echo ""
    echo -e "${BLUE}=== Progetto: ${CYAN}$project${NC} ==="

    local project_issues=0

    check_stato_freshness "$project" || ((project_issues++))
    check_undocumented_commits "$project" || ((project_issues++))
    check_migrations "$project" || ((project_issues++))
    check_recent_large_changes "$project" || ((project_issues++))

    if [ "$project_issues" -eq 0 ]; then
        echo -e "${GREEN}Progetto $project: TUTTO OK${NC}"
    fi

    return $project_issues
}

# ------------------------------------------------------------------------------
# Summary
# ------------------------------------------------------------------------------
print_summary() {
    echo ""
    echo -e "${PURPLE}+================================================================+${NC}"

    if [ "$TOTAL_ERRORS" -gt 0 ]; then
        echo -e "${RED}|              ERRORI: $TOTAL_ERRORS | WARNINGS: $TOTAL_WARNINGS                          |${NC}"
        echo -e "${RED}|              SINCRONIZZAZIONE NECESSARIA!                      |${NC}"
    elif [ "$TOTAL_WARNINGS" -gt 0 ]; then
        echo -e "${YELLOW}|              WARNINGS: $TOTAL_WARNINGS - Attenzione richiesta                |${NC}"
    else
        echo -e "${GREEN}|              TUTTO SINCRONIZZATO!                              |${NC}"
    fi

    echo -e "${PURPLE}+================================================================+${NC}"
    echo ""

    if [ "$TOTAL_WARNINGS" -gt 0 ] || [ "$TOTAL_ERRORS" -gt 0 ]; then
        echo -e "${CYAN}Suggerimenti:${NC}"
        echo "  1. Aggiorna stato.md con le modifiche recenti"
        echo "  2. Documenta i commit importanti"
        echo "  3. Verifica che le migrations siano menzionate"
        echo ""
    fi
}

# ==============================================================================
# MAIN
# ==============================================================================

# Parse arguments
TARGET_PROJECT=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --help|-h)
            print_usage
            exit 0
            ;;
        *)
            if [ -z "$TARGET_PROJECT" ]; then
                TARGET_PROJECT="$1"
            fi
            shift
            ;;
    esac
done

print_header

if [ -n "$TARGET_PROJECT" ]; then
    # Check singolo progetto
    if [ ! -d "$SNCP_ROOT/progetti/$TARGET_PROJECT" ]; then
        log_error "Progetto '$TARGET_PROJECT' non trovato in SNCP"
        echo "Progetti disponibili:"
        ls -1 "$SNCP_ROOT/progetti/" 2>/dev/null || echo "  (nessuno)"
        exit 1
    fi
    check_project "$TARGET_PROJECT"
else
    # Check tutti i progetti
    for project_dir in "$SNCP_ROOT/progetti"/*/; do
        if [ -d "$project_dir" ]; then
            project_name=$(basename "$project_dir")
            # Skip crypto-research e altri non-codice
            if [[ "$project_name" != "crypto-research" ]] && [[ "$project_name" != "menumaster" ]]; then
                check_project "$project_name"
            fi
        fi
    done
fi

print_summary

# Exit code based on issues
if [ "$TOTAL_ERRORS" -gt 0 ]; then
    exit 2
elif [ "$TOTAL_WARNINGS" -gt 0 ]; then
    exit 1
else
    exit 0
fi
