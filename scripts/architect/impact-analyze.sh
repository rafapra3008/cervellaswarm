#!/bin/bash
#
# impact-analyze.sh - CLI Wrapper for Impact Analyzer
#
# CervellaSwarm W5 Dogfooding - Day 4
# Wraps scripts/utils/impact_analyzer.py with JSON output
#
# Usage:
#   ./impact-analyze.sh estimate "MyClass"
#   ./impact-analyze.sh dependencies "app/auth.py"
#   ./impact-analyze.sh --help
#
# Output:
#   JSON with schema: {"found": bool, "result": {...}, "command": str, "target": str}
#
# Exit codes:
#   0 - Analysis successful (symbol/file found)
#   1 - Target not found
#   2 - Error (invalid args, Python error)
#
# Version: 1.0.0
# Date: 2026-01-20
# Author: Cervella Backend (W5 Day 4)
#

# Note: NOT using set -e because we need to handle Python exit codes

# ============================================================================
# CONFIGURATION
# ============================================================================

VERSION="1.0.0"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CERVELLASWARM_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
UTILS_DIR="${CERVELLASWARM_ROOT}/scripts/utils"
IMPACT_ANALYZER_PY="${UTILS_DIR}/impact_analyzer.py"

# ============================================================================
# FUNCTIONS
# ============================================================================

show_help() {
    cat << EOF
impact-analyze.sh - Code Impact Analysis CLI

USAGE:
    impact-analyze.sh <command> <target> [--repo <path>]
    impact-analyze.sh --help
    impact-analyze.sh --version

COMMANDS:
    estimate          Estimate impact of modifying a symbol
    dependencies      Find file dependencies (imports) and dependents (used by)

OPTIONS:
    --repo <path>     Repository root (default: git root or current dir)
    --help            Show this help message
    --version         Show version

OUTPUT:
    JSON with schema:

    For 'estimate':
    {
        "found": true/false,
        "command": "estimate",
        "target": "MyClass",
        "repo": "/path/to/repo",
        "result": {
            "risk_score": 0.45,
            "risk_level": "medium",
            "files_affected": 5,
            "callers_count": 8,
            "importance_score": 0.023,
            "reasons": ["8 callers - moderate impact", ...]
        }
    }

    For 'dependencies':
    {
        "found": true/false,
        "command": "dependencies",
        "target": "app/auth.py",
        "repo": "/path/to/repo",
        "result": {
            "dependencies": ["/path/to/file1.py", ...],
            "dependents": ["/path/to/file2.py", ...],
            "dependencies_count": 3,
            "dependents_count": 7
        }
    }

EXIT CODES:
    0 - Analysis successful (target found)
    1 - Target not found
    2 - Error (invalid args, missing dependencies)

EXAMPLES:
    # Estimate impact of modifying AuthService class
    impact-analyze.sh estimate "AuthService"

    # Find dependencies for a file
    impact-analyze.sh dependencies "scripts/utils/semantic_search.py"

    # Analyze in specific repo
    impact-analyze.sh estimate "MyClass" --repo /path/to/repo

RISK LEVELS:
    low (0.0-0.3)      Safe to modify, few dependencies
    medium (0.3-0.5)   Moderate impact, some callers
    high (0.5-0.7)     High impact, many callers
    critical (0.7-1.0) Critical component, widely used

DEPENDENCIES:
    - Python 3.10+
    - tree-sitter, tree-sitter-python, tree-sitter-typescript
    - networkx

Part of CervellaSwarm W5 Dogfooding Integration.
EOF
    exit 0
}

show_version() {
    echo "impact-analyze.sh version ${VERSION}"
    echo "CervellaSwarm W5 Day 4 - Dogfooding Integration"
    exit 0
}

error_json() {
    local message="$1"
    local command="${2:-unknown}"
    local target="${3:-}"

    cat << EOF
{"found": false, "result": null, "command": "${command}", "target": "${target}", "error": "${message}"}
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
TARGET=""
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
        estimate|dependencies)
            COMMAND="$1"
            shift
            ;;
        *)
            if [[ -z "${TARGET}" ]]; then
                TARGET="$1"
            fi
            shift
            ;;
    esac
done

# Validate command
if [[ -z "${COMMAND}" ]]; then
    error_json "No command specified. Use --help for usage." "none" ""
fi

# Validate target
if [[ -z "${TARGET}" ]]; then
    error_json "No target specified." "${COMMAND}" ""
fi

# Get repo root
REPO_ROOT=$(get_repo_root "${REPO_ROOT}")

# Check if Python script exists
if [[ ! -f "${IMPACT_ANALYZER_PY}" ]]; then
    error_json "impact_analyzer.py not found at ${IMPACT_ANALYZER_PY}" "${COMMAND}" "${TARGET}"
fi

# Check Python is available
if ! command -v python3 &>/dev/null; then
    error_json "Python 3 not found" "${COMMAND}" "${TARGET}"
fi

# Run Python script and capture output
export PYTHONPATH="${UTILS_DIR}:${PYTHONPATH}"

# Create temp file for output
TEMP_OUTPUT=$(mktemp)
TEMP_ERROR=$(mktemp)

# Run Python with custom JSON output wrapper
python3 << PYTHON_EOF > "${TEMP_OUTPUT}" 2>"${TEMP_ERROR}"
import sys
import json
import logging
from pathlib import Path

# Suppress all logging
logging.disable(logging.CRITICAL)

sys.path.insert(0, "${UTILS_DIR}")

try:
    from impact_analyzer import ImpactAnalyzer

    analyzer = ImpactAnalyzer("${REPO_ROOT}")

    command = "${COMMAND}"
    target = "${TARGET}"

    result = {
        "found": False,
        "result": None,
        "command": command,
        "target": target,
        "repo": "${REPO_ROOT}"
    }

    if command == "estimate":
        impact = analyzer.estimate_impact(target)
        if impact:
            result["found"] = True
            result["result"] = {
                "risk_score": round(impact.risk_score, 3),
                "risk_level": impact.risk_level,
                "files_affected": impact.files_affected,
                "callers_count": impact.callers_count,
                "importance_score": round(impact.importance_score, 6),
                "reasons": impact.reasons
            }

    elif command == "dependencies":
        # For file dependencies, resolve path
        target_path = target
        if not Path(target_path).is_absolute():
            target_path = str(Path("${REPO_ROOT}") / target)

        dependencies = analyzer.find_dependencies(target_path)
        dependents = analyzer.find_dependents(target_path)

        # Check if file exists and has any results
        if Path(target_path).exists():
            result["found"] = True
            result["result"] = {
                "dependencies": dependencies,
                "dependents": dependents,
                "dependencies_count": len(dependencies),
                "dependents_count": len(dependents)
            }

    print(json.dumps(result, indent=2))

    # Exit with appropriate code
    sys.exit(0 if result["found"] else 1)

except ImportError as e:
    error_result = {
        "found": False,
        "result": None,
        "command": "${COMMAND}",
        "target": "${TARGET}",
        "error": f"Import error: {str(e)}. Check tree-sitter dependencies."
    }
    print(json.dumps(error_result, indent=2))
    sys.exit(2)

except Exception as e:
    error_result = {
        "found": False,
        "result": None,
        "command": "${COMMAND}",
        "target": "${TARGET}",
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
