#!/bin/bash
#
# semantic-search.sh - CLI Wrapper for Semantic Search
#
# CervellaSwarm W5 Dogfooding - Day 3
# Wraps scripts/utils/semantic_search.py with JSON output
#
# Usage:
#   ./semantic-search.sh find-symbol "MyClass"
#   ./semantic-search.sh find-callers "my_function"
#   ./semantic-search.sh find-references "my_function"
#   ./semantic-search.sh --help
#
# Output:
#   JSON with schema: {"found": bool, "results": [...], "command": str, "symbol": str}
#
# Exit codes:
#   0 - Symbol found (or help displayed)
#   1 - Symbol not found
#   2 - Error (invalid args, Python error)
#
# Version: 1.0.0
# Date: 2026-01-20
# Author: Cervella Backend (W5 Day 3)
#

# Note: NOT using set -e because we need to handle Python exit codes

# ============================================================================
# CONFIGURATION
# ============================================================================

VERSION="1.0.0"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CERVELLASWARM_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
UTILS_DIR="${CERVELLASWARM_ROOT}/scripts/utils"
SEMANTIC_SEARCH_PY="${UTILS_DIR}/semantic_search.py"

# ============================================================================
# FUNCTIONS
# ============================================================================

show_help() {
    cat << EOF
semantic-search.sh - Semantic Code Search CLI

USAGE:
    semantic-search.sh <command> <symbol_name> [--repo <path>]
    semantic-search.sh --help
    semantic-search.sh --version

COMMANDS:
    find-symbol       Find where a symbol is defined
    find-callers      Find all functions that call this symbol
    find-references   Find all references to this symbol

OPTIONS:
    --repo <path>     Repository root (default: git root or current dir)
    --help            Show this help message
    --version         Show version

OUTPUT:
    JSON with schema:
    {
        "found": true/false,
        "results": [...],
        "command": "find-symbol",
        "symbol": "MyClass",
        "repo": "/path/to/repo"
    }

EXIT CODES:
    0 - Symbol found (or help/version displayed)
    1 - Symbol not found
    2 - Error (invalid args, missing dependencies)

EXAMPLES:
    # Find where SemanticSearch class is defined
    semantic-search.sh find-symbol "SemanticSearch"

    # Find all callers of extract_symbols function
    semantic-search.sh find-callers "extract_symbols"

    # Find all references to DependencyGraph
    semantic-search.sh find-references "DependencyGraph"

    # Search in specific repo
    semantic-search.sh find-symbol "MyClass" --repo /path/to/repo

DEPENDENCIES:
    - Python 3.10+
    - tree-sitter, tree-sitter-python, tree-sitter-typescript
    - networkx

Part of CervellaSwarm W5 Dogfooding Integration.
EOF
    exit 0
}

show_version() {
    echo "semantic-search.sh version ${VERSION}"
    echo "CervellaSwarm W5 Day 3 - Dogfooding Integration"
    exit 0
}

error_json() {
    local message="$1"
    local command="${2:-unknown}"
    local symbol="${3:-}"

    cat << EOF
{"found": false, "results": [], "command": "${command}", "symbol": "${symbol}", "error": "${message}"}
EOF
    exit 2
}

# Get git root or current directory
get_repo_root() {
    local custom_repo="$1"

    if [[ -n "${custom_repo}" ]]; then
        echo "${custom_repo}"
    elif git rev-parse --show-toplevel &>/dev/null; then
        git rev-parse --show-toplevel
    else
        pwd
    fi
}

# ============================================================================
# MAIN
# ============================================================================

# Parse arguments
COMMAND=""
SYMBOL=""
REPO_ROOT=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --help|-h)
            show_help
            ;;
        --version|-v)
            show_version
            ;;
        --repo)
            REPO_ROOT="$2"
            shift 2
            ;;
        find-symbol|find-callers|find-references)
            COMMAND="$1"
            shift
            ;;
        *)
            if [[ -z "${SYMBOL}" ]]; then
                SYMBOL="$1"
            fi
            shift
            ;;
    esac
done

# Validate command
if [[ -z "${COMMAND}" ]]; then
    error_json "No command specified. Use --help for usage." "none" ""
fi

# Validate symbol
if [[ -z "${SYMBOL}" ]]; then
    error_json "No symbol name specified." "${COMMAND}" ""
fi

# Get repo root
REPO_ROOT=$(get_repo_root "${REPO_ROOT}")

# Check if Python script exists
if [[ ! -f "${SEMANTIC_SEARCH_PY}" ]]; then
    error_json "semantic_search.py not found at ${SEMANTIC_SEARCH_PY}" "${COMMAND}" "${SYMBOL}"
fi

# Check Python is available
if ! command -v python3 &>/dev/null; then
    error_json "Python 3 not found" "${COMMAND}" "${SYMBOL}"
fi

# Map command to Python command
case "${COMMAND}" in
    find-symbol)
        PY_COMMAND="find"
        ;;
    find-callers)
        PY_COMMAND="callers"
        ;;
    find-references)
        PY_COMMAND="refs"
        ;;
esac

# Run Python script and capture output
# We need to suppress logging and only capture the result
export PYTHONPATH="${UTILS_DIR}:${PYTHONPATH}"

# Create temp file for output
TEMP_OUTPUT=$(mktemp)
TEMP_ERROR=$(mktemp)

# Run Python with custom JSON output wrapper
python3 << PYTHON_EOF > "${TEMP_OUTPUT}" 2>"${TEMP_ERROR}"
import sys
import json
import logging

# Suppress all logging
logging.disable(logging.CRITICAL)

sys.path.insert(0, "${UTILS_DIR}")

try:
    from semantic_search import SemanticSearch

    search = SemanticSearch("${REPO_ROOT}")

    command = "${PY_COMMAND}"
    symbol = "${SYMBOL}"

    result = {
        "found": False,
        "results": [],
        "command": "${COMMAND}",
        "symbol": symbol,
        "repo": "${REPO_ROOT}"
    }

    if command == "find":
        location = search.find_symbol(symbol)
        if location:
            file_path, line_number = location
            result["found"] = True
            result["results"] = [{
                "file": file_path,
                "line": line_number
            }]

    elif command == "callers":
        callers = search.find_callers(symbol)
        if callers:
            result["found"] = True
            result["results"] = [
                {"file": f, "line": l, "caller": c}
                for f, l, c in callers
            ]

    elif command == "refs":
        refs = search.find_references(symbol)
        if refs:
            result["found"] = True
            result["results"] = [
                {"file": f, "line": l}
                for f, l in refs
            ]

    print(json.dumps(result, indent=2))

    # Exit with appropriate code
    sys.exit(0 if result["found"] else 1)

except ImportError as e:
    error_result = {
        "found": False,
        "results": [],
        "command": "${COMMAND}",
        "symbol": "${SYMBOL}",
        "error": f"Import error: {str(e)}. Check tree-sitter dependencies."
    }
    print(json.dumps(error_result, indent=2))
    sys.exit(2)

except Exception as e:
    error_result = {
        "found": False,
        "results": [],
        "command": "${COMMAND}",
        "symbol": "${SYMBOL}",
        "error": str(e)
    }
    print(json.dumps(error_result, indent=2))
    sys.exit(2)
PYTHON_EOF

# Capture exit code
PY_EXIT_CODE=$?

# Output result
cat "${TEMP_OUTPUT}"

# Cleanup
rm -f "${TEMP_OUTPUT}" "${TEMP_ERROR}"

# Exit with Python's exit code
exit ${PY_EXIT_CODE}
