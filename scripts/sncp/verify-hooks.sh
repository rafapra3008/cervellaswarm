#!/bin/bash
# verify-hooks.sh - Wrapper per verify-hooks.py
# Verifica integrita di tutti gli hook Claude Code
# Usage: ./scripts/sncp/verify-hooks.sh [--verbose]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/verify-hooks.py" "$@"
