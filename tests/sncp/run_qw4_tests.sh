#!/bin/bash
# Run QW4 BM25 Search Tests
# Author: Cervella Tester
# Date: 2026-02-02

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}==============================================================${NC}"
echo -e "${BLUE}  QW4 BM25 Search Test Suite${NC}"
echo -e "${BLUE}==============================================================${NC}"
echo ""

# Determine mode
MODE=${1:-all}

case "$MODE" in
  all)
    echo -e "${GREEN}Running all tests...${NC}"
    python3 -m pytest tests/sncp/test_qw4_bm25_search.py -v
    ;;

  fast)
    echo -e "${GREEN}Running fast tests (skip integration)...${NC}"
    python3 -m pytest tests/sncp/test_qw4_bm25_search.py -v -m "not integration"
    ;;

  performance)
    echo -e "${GREEN}Running performance tests only...${NC}"
    python3 -m pytest tests/sncp/test_qw4_bm25_search.py::TestPerformance -v
    ;;

  accuracy)
    echo -e "${GREEN}Running accuracy tests only...${NC}"
    python3 -m pytest tests/sncp/test_qw4_bm25_search.py::TestAccuracy -v
    ;;

  unit)
    echo -e "${GREEN}Running unit tests only...${NC}"
    python3 -m pytest tests/sncp/test_qw4_bm25_search.py::TestPreprocessText -v
    python3 -m pytest tests/sncp/test_qw4_bm25_search.py::TestReadMarkdownFiles -v
    python3 -m pytest tests/sncp/test_qw4_bm25_search.py::TestExtractSnippet -v
    ;;

  integration)
    echo -e "${GREEN}Running integration tests only...${NC}"
    python3 -m pytest tests/sncp/test_qw4_bm25_search.py::TestSearchBM25 -v
    python3 -m pytest tests/sncp/test_qw4_bm25_search.py::TestRealProjects -v
    ;;

  edge)
    echo -e "${GREEN}Running edge case tests only...${NC}"
    python3 -m pytest tests/sncp/test_qw4_bm25_search.py::TestEdgeCases -v
    ;;

  watch)
    echo -e "${GREEN}Running tests in watch mode...${NC}"
    python3 -m pytest tests/sncp/test_qw4_bm25_search.py -v --looponfail
    ;;

  help|*)
    echo "Usage: $0 [mode]"
    echo ""
    echo "Modes:"
    echo "  all          - Run all tests (default)"
    echo "  fast         - Run all tests except integration"
    echo "  performance  - Run performance tests only"
    echo "  accuracy     - Run accuracy tests only"
    echo "  unit         - Run unit tests only"
    echo "  integration  - Run integration tests only"
    echo "  edge         - Run edge case tests only"
    echo "  watch        - Run tests in watch mode (loop on fail)"
    echo "  help         - Show this help"
    echo ""
    echo "Examples:"
    echo "  $0              # Run all tests"
    echo "  $0 fast         # Skip integration tests"
    echo "  $0 performance  # Check performance only"
    exit 0
    ;;
esac

echo ""
echo -e "${BLUE}==============================================================${NC}"
echo -e "${GREEN}Tests complete!${NC}"
echo -e "${BLUE}==============================================================${NC}"
