#!/bin/bash
# run_qw_all_tests.sh - Run ALL SNCP 4.0 Quick Wins tests
# Author: Cervella Tester
# Date: 2026-02-02
# Target: Validate FASE 1 SNCP 4.0 complete!

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_DIR="$SCRIPT_DIR"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Header
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}  SNCP 4.0 FASE 1 - QUICK WINS TEST SUITE                ${BLUE}║${NC}"
echo -e "${BLUE}║${NC}  Author: Cervella Tester                                 ${BLUE}║${NC}"
echo -e "${BLUE}║${NC}  Date: 2026-02-02                                        ${BLUE}║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Track results
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
QW_RESULTS=()

# Function to run single QW test
run_qw_test() {
    local qw_num="$1"
    local qw_name="$2"
    local test_file="$3"
    local score_target="$4"

    echo -e "${YELLOW}═══════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}QW${qw_num}: ${qw_name}${NC}"
    echo -e "${YELLOW}Target: ${score_target}/10${NC}"
    echo -e "${YELLOW}═══════════════════════════════════════════════════════${NC}"
    echo ""

    # Run pytest
    if pytest "$TEST_DIR/$test_file" -v --tb=short; then
        echo ""
        echo -e "${GREEN}✅ QW${qw_num} PASSED${NC}"
        QW_RESULTS+=("$qw_num:PASS")
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo ""
        echo -e "${RED}❌ QW${qw_num} FAILED${NC}"
        QW_RESULTS+=("$qw_num:FAIL")
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi

    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    echo ""
}

# Run all QW tests
echo -e "${BLUE}Starting Quick Wins test suite...${NC}"
echo ""

run_qw_test "1" "Auto-load Daily Logs" "test_qw1_daily_memory.py" "9.5"
run_qw_test "2" "Memory Flush Token Trigger" "test_qw2_memory_flush_trigger.py" "9.5"
run_qw_test "3" "SessionEnd Hook Flush" "test_qw3_session_end_flush.py" "9.5"
run_qw_test "4" "BM25 Search" "test_qw4_bm25_search.py" "9.5"

# Summary
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}                      SUMMARY                               ${BLUE}║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Individual QW results
for result in "${QW_RESULTS[@]}"; do
    qw_num="${result%%:*}"
    status="${result##*:}"

    if [[ "$status" == "PASS" ]]; then
        echo -e "  QW${qw_num}: ${GREEN}✅ PASSED${NC}"
    else
        echo -e "  QW${qw_num}: ${RED}❌ FAILED${NC}"
    fi
done

echo ""
echo -e "Total Tests: ${TOTAL_TESTS}"
echo -e "${GREEN}Passed: ${PASSED_TESTS}${NC}"

if [[ $FAILED_TESTS -gt 0 ]]; then
    echo -e "${RED}Failed: ${FAILED_TESTS}${NC}"
fi

echo ""

# Final verdict
if [[ $FAILED_TESTS -eq 0 ]]; then
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║${NC}  🚀 FASE 1 SNCP 4.0 - VALIDATION COMPLETE! 🚀           ${GREEN}║${NC}"
    echo -e "${GREEN}║${NC}  All Quick Wins tests passed!                            ${GREEN}║${NC}"
    echo -e "${GREEN}║${NC}  Score: 9.5/10 ❤️‍🔥                                        ${GREEN}║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
    exit 0
else
    echo -e "${RED}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║${NC}  ⚠️  SOME TESTS FAILED                                    ${RED}║${NC}"
    echo -e "${RED}║${NC}  Review failures and fix before declaring success.       ${RED}║${NC}"
    echo -e "${RED}╚════════════════════════════════════════════════════════════╝${NC}"
    exit 1
fi
