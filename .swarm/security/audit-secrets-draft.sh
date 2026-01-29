#!/bin/bash

# audit-secrets.sh - Security scan for secrets in SNCP memory files
# Author: Cervella Security
# Date: 29 Gennaio 2026
# Purpose: Prevent accidental secrets leakage in memory files (SNCP 2.0)

set -euo pipefail

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

CRITICAL_COUNT=0
HIGH_COUNT=0
MEDIUM_COUNT=0

SNCP_ROOT="${1:-.sncp/progetti}"

echo "=================================================="
echo "🔒 Cervella Security - SNCP Secrets Audit"
echo "=================================================="
echo ""
echo "Scanning: $SNCP_ROOT"
echo ""

# Pattern definitions
# These are patterns that should NEVER appear in memory files

# CRITICAL: Actual secrets (keys, passwords, tokens)
declare -A CRITICAL_PATTERNS=(
    ["OpenAI API Key"]='sk-[a-zA-Z0-9]{48}'
    ["JWT Token"]='eyJ[a-zA-Z0-9_-]+\.eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+'
    ["GitHub Token"]='ghp_[a-zA-Z0-9]{36}'
    ["Google API Key"]='AIza[a-zA-Z0-9_-]{35}'
    ["AWS Secret"]='aws_secret_access_key\s*=\s*[A-Za-z0-9/+=]{40}'
    ["Database Connection String"]='(mysql|postgresql|mongodb|postgres)://[^:]+:[^@]+@'
    ["Private Key"]='-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----'
)

# HIGH: Likely secrets (patterns that look like credentials)
declare -A HIGH_PATTERNS=(
    ["Password in Plain"]='[Pp]assword["\s]*[:=]["\s]*[^"\s]{8,}'
    ["Secret Value"]='[Ss]ecret["\s]*[:=]["\s]*[^"\s]{8,}'
    ["API Key Value"]='[Aa][Pp][Ii][_-]?[Kk]ey["\s]*[:=]["\s]*[^"\s]{16,}'
    ["Token Value"]='[Tt]oken["\s]*[:=]["\s]*[^"\s]{16,}'
    ["Bearer Token"]='Bearer\s+[a-zA-Z0-9_-]{20,}'
    ["Authorization Header"]='Authorization:\s+Basic\s+[A-Za-z0-9+/=]{20,}'
)

# MEDIUM: Suspicious patterns (need review)
declare -A MEDIUM_PATTERNS=(
    ["IP + Port Pattern"]='[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:[0-9]+'
    ["Credential Comment"]='(username|password|credential|secret|api[_-]?key)\s*:\s*[^#\n]+'
)

# Files to exclude from scan
EXCLUDE_FILES=(
    "RICERCA_ENCRYPTION_TOKENS_SQLITE.md"  # Research about encryption (legitimate)
    "audit-secrets-draft.sh"                # This script itself
    "AUDIT_SNCP_SECRETS.md"                 # Audit report (contains safe examples)
)

should_exclude() {
    local file="$1"
    for exclude in "${EXCLUDE_FILES[@]}"; do
        if [[ "$file" == *"$exclude"* ]]; then
            return 0
        fi
    done
    return 1
}

scan_pattern() {
    local severity="$1"
    local description="$2"
    local pattern="$3"
    local color="$4"

    while IFS= read -r file; do
        if should_exclude "$file"; then
            continue
        fi

        # Use grep with Perl regex for advanced patterns
        if grep -qP "$pattern" "$file" 2>/dev/null; then
            echo -e "${color}[$severity] $description${NC}"
            echo "  File: $file"

            # Show line numbers but NOT the actual content (security!)
            grep -nP "$pattern" "$file" 2>/dev/null | while IFS=: read -r line_num _; do
                echo "  Line: $line_num (content hidden for security)"
            done
            echo ""

            case "$severity" in
                CRITICAL) ((CRITICAL_COUNT++)) ;;
                HIGH) ((HIGH_COUNT++)) ;;
                MEDIUM) ((MEDIUM_COUNT++)) ;;
            esac
        fi
    done < <(find "$SNCP_ROOT" -type f -name "*.md" 2>/dev/null)
}

echo "🔍 Scanning for CRITICAL secrets..."
echo "-----------------------------------"
for desc in "${!CRITICAL_PATTERNS[@]}"; do
    pattern="${CRITICAL_PATTERNS[$desc]}"
    scan_pattern "CRITICAL" "$desc" "$pattern" "$RED"
done

echo "🔍 Scanning for HIGH risk patterns..."
echo "--------------------------------------"
for desc in "${!HIGH_PATTERNS[@]}"; do
    pattern="${HIGH_PATTERNS[$desc]}"
    scan_pattern "HIGH" "$desc" "$pattern" "$YELLOW"
done

echo "🔍 Scanning for MEDIUM risk patterns..."
echo "----------------------------------------"
for desc in "${!MEDIUM_PATTERNS[@]}"; do
    pattern="${MEDIUM_PATTERNS[$desc]}"
    scan_pattern "MEDIUM" "$desc" "$pattern" "$YELLOW"
done

# Summary
echo "=================================================="
echo "📊 SUMMARY"
echo "=================================================="
echo ""
echo -e "${RED}CRITICAL: $CRITICAL_COUNT findings${NC}"
echo -e "${YELLOW}HIGH: $HIGH_COUNT findings${NC}"
echo -e "${YELLOW}MEDIUM: $MEDIUM_COUNT findings${NC}"
echo ""

if [ $CRITICAL_COUNT -gt 0 ]; then
    echo "🚨 ACTION REQUIRED: CRITICAL secrets found!"
    echo ""
    echo "IMMEDIATE ACTIONS:"
    echo "1. Remove secrets from memory files"
    echo "2. Move to .env or environment variables"
    echo "3. Rotate exposed credentials"
    echo "4. Update .gitignore if needed"
    echo ""
    exit 1
elif [ $HIGH_COUNT -gt 0 ]; then
    echo "⚠️  WARNING: HIGH risk patterns found"
    echo "Review findings and ensure no actual secrets are exposed"
    echo ""
    exit 1
elif [ $MEDIUM_COUNT -gt 0 ]; then
    echo "⚠️  INFO: MEDIUM risk patterns found"
    echo "Review findings for context"
    echo ""
fi

echo "✅ Scan complete!"
echo ""
echo "BEST PRACTICES:"
echo "- Store secrets in .env files (excluded from git)"
echo "- Use environment variables for credentials"
echo "- Never commit API keys, passwords, tokens to memory files"
echo "- Document WHAT system needs, not the actual credentials"
echo ""
echo "Example:"
echo "  ❌ Password: abc123xyz"
echo "  ✅ Password: [stored in .env as DB_PASSWORD]"
echo ""

exit 0
