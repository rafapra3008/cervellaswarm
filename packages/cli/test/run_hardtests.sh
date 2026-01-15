#!/bin/bash

# =============================================================================
# CervellaSwarm CLI - Hardtests Runner
# =============================================================================
#
# Script per eseguire tutti gli hardtests della CLI.
# Usato per CI/CD e validazione locale.
#
# "Un progresso al giorno = 365 progressi all'anno."
#
# Usage:
#   ./test/run_hardtests.sh           # Run all tests
#   ./test/run_hardtests.sh commands  # Run only command tests
#   ./test/run_hardtests.sh --watch   # Run in watch mode
#
# =============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CLI_DIR="$( dirname "$SCRIPT_DIR" )"

echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║       CervellaSwarm CLI - Hardtests                       ║${NC}"
echo -e "${CYAN}║       \"Fatto BENE > Fatto VELOCE\"                        ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Change to CLI directory
cd "$CLI_DIR"

# Parse arguments
TEST_PATH=""
WATCH_MODE=false
COVERAGE=false

for arg in "$@"; do
  case $arg in
    --watch|-w)
      WATCH_MODE=true
      ;;
    --coverage|-c)
      COVERAGE=true
      ;;
    commands)
      TEST_PATH="test/commands/"
      ;;
    agents)
      TEST_PATH="test/agents/"
      ;;
    session)
      TEST_PATH="test/session/"
      ;;
    edge)
      TEST_PATH="test/edge-cases.test.js"
      ;;
    *)
      # Unknown option, use as path
      if [ -e "$arg" ]; then
        TEST_PATH="$arg"
      fi
      ;;
  esac
done

# Build command
CMD="node --test"

if [ "$WATCH_MODE" = true ]; then
  CMD="$CMD --watch"
fi

if [ "$COVERAGE" = true ]; then
  CMD="$CMD --experimental-test-coverage"
fi

if [ -n "$TEST_PATH" ]; then
  CMD="$CMD $TEST_PATH"
fi

# Run tests
echo -e "${YELLOW}Running: $CMD${NC}"
echo ""

START_TIME=$(date +%s)

if $CMD; then
  END_TIME=$(date +%s)
  DURATION=$((END_TIME - START_TIME))

  echo ""
  echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
  echo -e "${GREEN}║  ✓ All tests passed!                                      ║${NC}"
  echo -e "${GREEN}║  Duration: ${DURATION}s                                          ${NC}"
  echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
  echo ""

  exit 0
else
  END_TIME=$(date +%s)
  DURATION=$((END_TIME - START_TIME))

  echo ""
  echo -e "${RED}╔═══════════════════════════════════════════════════════════╗${NC}"
  echo -e "${RED}║  ✗ Some tests failed                                      ║${NC}"
  echo -e "${RED}║  Duration: ${DURATION}s                                          ${NC}"
  echo -e "${RED}╚═══════════════════════════════════════════════════════════╝${NC}"
  echo ""

  exit 1
fi
