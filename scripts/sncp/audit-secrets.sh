#!/bin/bash

# audit-secrets.sh - Security scan for secrets in SNCP memory files
# Author: Cervella Security
# Date: 29 Gennaio 2026
# Version: 1.0.1
# Purpose: Prevent accidental secrets leakage in memory files

set -uo pipefail

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

CRITICAL_COUNT=0
HIGH_COUNT=0

# Help
if [[ "${1:-}" == "--help" ]] || [[ "${1:-}" == "-h" ]]; then
    echo "Usage: audit-secrets.sh [path]"
    echo ""
    echo "Scans markdown files for potential secrets."
    echo ""
    echo "Arguments:"
    echo "  path    Directory to scan (default: .sncp/progetti/)"
    echo ""
    echo "Exit codes:"
    echo "  0       No findings"
    echo "  1       Findings detected - action required"
    exit 0
fi

SNCP_ROOT="${1:-.sncp/progetti}"

if [[ ! -d "$SNCP_ROOT" ]]; then
    echo -e "${RED}Error: Directory not found: $SNCP_ROOT${NC}"
    exit 1
fi

echo "=================================================="
echo -e "${BLUE}CervellaSwarm - Security Audit${NC}"
echo "=================================================="
echo ""
echo "Scanning: $SNCP_ROOT"
echo ""

# CRITICAL patterns (actual API keys, tokens)
CRITICAL_PATTERNS=(
    "sk-[a-zA-Z0-9]{20,}"                    # OpenAI/Anthropic
    "ghp_[a-zA-Z0-9]{36}"                    # GitHub PAT
    "AIza[a-zA-Z0-9_-]{35}"                  # Google API Key
    "sk_live_[a-zA-Z0-9]{24}"                # Stripe
    "-----BEGIN.*PRIVATE KEY-----"           # Private keys
)

CRITICAL_NAMES=(
    "OpenAI/Anthropic API Key"
    "GitHub Token"
    "Google API Key"
    "Stripe Secret Key"
    "Private Key"
)

# HIGH patterns (password/secret assignments)
HIGH_PATTERNS=(
    "[Pp]ass(word)?[[:space:]]*[:=][[:space:]]*[^[:space:]\[\]\"]{8,40}"
    "[Ss]ecret[[:space:]]*[:=][[:space:]]*[^[:space:]\[\]\"]{8,40}"
)

HIGH_NAMES=(
    "Password Assignment"
    "Secret Assignment"
)

should_skip_file() {
    local file="$1"
    case "$file" in
        *audit-secrets*|*AUDIT_SNCP*|*BEST_PRACTICES*|*.env.example*|*test*|*mock*)
            return 0 ;;
    esac
    return 1
}

is_sanitized() {
    local line="$1"
    case "$line" in
        *"[stored in .env"*|*"[REDACTED"*|*"YOUR_"*"_HERE"*|*"your_"*"_here"*)
            return 0 ;;
    esac
    return 1
}

scan_files() {
    local severity="$1"
    local pattern="$2"
    local name="$3"
    local color="$4"

    while IFS= read -r file; do
        if should_skip_file "$file"; then
            continue
        fi

        while IFS=: read -r line_num line_content; do
            if ! is_sanitized "$line_content"; then
                echo -e "${color}[$severity] $name${NC}"
                echo "  File: $file"
                echo "  Line: $line_num (content hidden)"
                echo ""

                if [[ "$severity" == "CRITICAL" ]]; then
                    CRITICAL_COUNT=$((CRITICAL_COUNT + 1))
                else
                    HIGH_COUNT=$((HIGH_COUNT + 1))
                fi
            fi
        done < <(grep -nE "$pattern" "$file" 2>/dev/null || true)
    done < <(find "$SNCP_ROOT" -type f -name "*.md" 2>/dev/null)
}

echo -e "${RED}Scanning for CRITICAL secrets...${NC}"
echo "-----------------------------------"
for i in "${!CRITICAL_PATTERNS[@]}"; do
    scan_files "CRITICAL" "${CRITICAL_PATTERNS[$i]}" "${CRITICAL_NAMES[$i]}" "$RED"
done

echo -e "${YELLOW}Scanning for HIGH risk patterns...${NC}"
echo "-----------------------------------"
for i in "${!HIGH_PATTERNS[@]}"; do
    scan_files "HIGH" "${HIGH_PATTERNS[$i]}" "${HIGH_NAMES[$i]}" "$YELLOW"
done

# Summary
echo "=================================================="
echo -e "${BLUE}SUMMARY${NC}"
echo "=================================================="
echo ""
echo -e "CRITICAL: $CRITICAL_COUNT"
echo -e "HIGH: $HIGH_COUNT"
echo ""

if [ $CRITICAL_COUNT -gt 0 ] || [ $HIGH_COUNT -gt 0 ]; then
    echo -e "${RED}ACTION REQUIRED!${NC}"
    echo ""
    echo "Steps:"
    echo "1. Remove secrets from files"
    echo "2. Add to .env file"
    echo "3. Replace with: [stored in .env as VAR_NAME]"
    echo ""
    exit 1
fi

echo -e "${GREEN}No secrets found! Files are clean.${NC}"
echo ""
exit 0
