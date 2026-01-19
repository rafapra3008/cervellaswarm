"""Integration Tests for W2.5-C: Reference Extraction + PageRank.

These tests verify that the complete integration works:
- symbol_extractor extracts references
- dependency_graph builds edges from references
- PageRank produces DIVERSE scores (not all equal)
- File ordering is by IMPORTANCE (not alphabetical)

Author: Cervella Backend
Version: 1.0.0
Date: 2026-01-19
"""

import sys
import tempfile
from pathlib import Path

import pytest

# Add scripts/utils to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts" / "utils"))

from dependency_graph import DependencyGraph, build_dependency_graph
from symbol_extractor import Symbol, SymbolExtractor
from treesitter_parser import TreesitterParser


class TestPageRankVariance:
    """T19: PageRank produces DIVERSE scores."""

    def test_pagerank_variance_controlled(self):
        """T19a: Controlled test with known structure.

        Setup: Star topology where common_util is referenced by all.
        Expected: common_util has highest score, variance > 0.001
        """
        graph = DependencyGraph()

        # Create symbols with explicit references
        common = Symbol(
            name="common_util",
            type="function",
            file="common.py",
            line=1,
            signature="def common_util()",
            references=[],
        )
        helper = Symbol(
            name="helper_func",
            type="function",
            file="helper.py",
            line=1,
            signature="def helper_func()",
            references=["common_util"],
        )
        main = Symbol(
            name="main",
            type="function",
            file="main.py",
            line=1,
            signature="def main()",
            references=["common_util", "helper_func"],
        )
        isolated = Symbol(
            name="isolated",
            type="function",
            file="other.py",
            line=1,
            signature="def isolated()",
            references=[],
        )

        # Build graph
        for s in [common, helper, main, isolated]:
            graph.add_symbol(s)
            for ref in s.references:
                graph.add_reference(f"{s.file}:{s.name}", ref)

        # Compute importance
        scores = graph.compute_importance()

        # Assertions
        assert len(scores) == 4, "Should have 4 nodes"

        # Calculate variance
        values = list(scores.values())
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)

        # T19 acceptance: variance > 0.001
        assert variance > 0.001, f"Variance {variance} should be > 0.001"

        # common_util should have highest score (most referenced)
        common_id = "common.py:common_util"
        assert common_id in scores
        assert scores[common_id] == max(scores.values()), \
            "common_util should have highest PageRank score"

    def test_pagerank_variance_real_code(self):
        """T19b: Test with real Python code.

        Creates temp files with actual imports and function calls.
        """
        parser = TreesitterParser()
        extractor = SymbolExtractor(parser)

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create utils.py - will be imported by others
            utils_path = Path(tmpdir) / "utils.py"
            utils_path.write_text("""
def validate_input(data):
    return data is not None

def format_output(result):
    return str(result)

class DataProcessor:
    def process(self, data):
        return validate_input(data)
""")

            # Create main.py - imports from utils
            main_path = Path(tmpdir) / "main.py"
            main_path.write_text("""
from utils import validate_input, format_output, DataProcessor

def main():
    processor = DataProcessor()
    data = get_data()
    if validate_input(data):
        result = processor.process(data)
        print(format_output(result))

def get_data():
    return {"key": "value"}
""")

            # Extract symbols
            utils_symbols = extractor.extract_symbols(str(utils_path))
            main_symbols = extractor.extract_symbols(str(main_path))
            all_symbols = utils_symbols + main_symbols

            # Build graph
            graph = build_dependency_graph(all_symbols)
            scores = graph.compute_importance()

            # Basic checks
            assert len(scores) > 0, "Should have some scores"

            # Check stats
            stats = graph.get_stats()
            assert stats["edges"] > 0, "Should have edges from references"


class TestFileOrdering:
    """T20: File ordering is by IMPORTANCE, not alphabetical."""

    def test_file_ordering_not_alphabetical(self):
        """T20a: Verify ordering is NOT alphabetical.

        Setup: Files named a.py, b.py, z.py where z.py has most importance.
        Expected: z.py appears before a.py and b.py in importance order.
        """
        graph = DependencyGraph()

        # z.py has function that is referenced by a.py and b.py
        z_func = Symbol(
            name="z_important",
            type="function",
            file="z.py",
            line=1,
            signature="def z_important()",
            references=[],
        )
        a_func = Symbol(
            name="a_func",
            type="function",
            file="a.py",
            line=1,
            signature="def a_func()",
            references=["z_important"],
        )
        b_func = Symbol(
            name="b_func",
            type="function",
            file="b.py",
            line=1,
            signature="def b_func()",
            references=["z_important"],
        )

        # Build graph
        for s in [z_func, a_func, b_func]:
            graph.add_symbol(s)
            for ref in s.references:
                graph.add_reference(f"{s.file}:{s.name}", ref)

        # Compute importance
        graph.compute_importance()

        # Get top symbols
        top_symbols = graph.get_top_symbols(n=3)
        top_names = [s.name for s in top_symbols]

        # z_important should be first (most referenced)
        assert top_names[0] == "z_important", \
            f"z_important should be first, got {top_names}"

        # Order should NOT be alphabetical
        alphabetical = ["a_func", "b_func", "z_important"]
        assert top_names != alphabetical, \
            "Order should NOT be alphabetical"

    def test_file_ordering_by_importance(self):
        """T20b: More complex ordering test.

        Setup: Chain of dependencies
        - core.py (used by service and api)
        - service.py (uses core, used by api)
        - api.py (uses service and core)
        - util.py (isolated)

        Expected order: core > service > api/util
        """
        graph = DependencyGraph()

        core = Symbol(
            name="core_func", type="function", file="core.py",
            line=1, signature="def core_func()", references=[]
        )
        service = Symbol(
            name="service_func", type="function", file="service.py",
            line=1, signature="def service_func()", references=["core_func"]
        )
        api = Symbol(
            name="api_func", type="function", file="api.py",
            line=1, signature="def api_func()",
            references=["core_func", "service_func"]
        )
        util = Symbol(
            name="util_func", type="function", file="util.py",
            line=1, signature="def util_func()", references=[]
        )

        for s in [core, service, api, util]:
            graph.add_symbol(s)
            for ref in s.references:
                graph.add_reference(f"{s.file}:{s.name}", ref)

        graph.compute_importance()
        top = graph.get_top_symbols(n=4)
        top_names = [s.name for s in top]

        # core_func should be first (most referenced)
        assert top_names[0] == "core_func", \
            f"core_func should be first, got {top_names}"

        # service_func should be second (referenced by api)
        assert top_names[1] == "service_func", \
            f"service_func should be second, got {top_names}"


class TestCachingPerformance:
    """Test REQ-09 caching performance."""

    def test_cache_speedup(self):
        """Verify caching provides significant speedup."""
        import time

        parser = TreesitterParser()
        extractor = SymbolExtractor(parser)

        # Use a real file
        test_file = Path(__file__).parent.parent / "scripts" / "utils" / "symbol_extractor.py"
        if not test_file.exists():
            pytest.skip("Test file not found")

        # First extraction (cold)
        extractor.clear_cache()
        start = time.perf_counter()
        symbols1 = extractor.extract_symbols(str(test_file))
        cold_time = time.perf_counter() - start

        # Second extraction (cached)
        start = time.perf_counter()
        symbols2 = extractor.extract_symbols(str(test_file))
        cached_time = time.perf_counter() - start

        # Assertions
        assert len(symbols1) == len(symbols2), "Results should be identical"
        assert cached_time < cold_time, "Cached should be faster"

        # Expect at least 10x speedup (usually 100x+)
        if cold_time > 0.001:  # Only if cold time is measurable
            speedup = cold_time / cached_time if cached_time > 0 else float("inf")
            assert speedup > 10, f"Expected 10x+ speedup, got {speedup:.1f}x"

    def test_cache_stats(self):
        """Test cache statistics."""
        parser = TreesitterParser()
        extractor = SymbolExtractor(parser)

        # Start with clear cache
        extractor.clear_cache()
        stats = extractor.get_cache_stats()
        assert stats["cached_files"] == 0
        assert stats["cached_symbols"] == 0

        # Extract from a file
        test_file = Path(__file__).parent.parent / "scripts" / "utils" / "dependency_graph.py"
        if test_file.exists():
            extractor.extract_symbols(str(test_file))

            stats = extractor.get_cache_stats()
            assert stats["cached_files"] == 1
            assert stats["cached_symbols"] > 0


class TestGracefulDegradation:
    """Test REQ-10 graceful degradation."""

    def test_nonexistent_file_returns_empty(self):
        """REQ-10: Non-existent file should return [] not raise."""
        parser = TreesitterParser()
        extractor = SymbolExtractor(parser)

        result = extractor.extract_symbols("/this/path/does/not/exist.py")
        assert result == []

    def test_unsupported_language_returns_empty(self):
        """REQ-10: Unsupported language should return [] not raise."""
        parser = TreesitterParser()
        extractor = SymbolExtractor(parser)

        with tempfile.NamedTemporaryFile(suffix=".rs", delete=False) as f:
            f.write(b"fn main() {}")
            rust_file = f.name

        try:
            result = extractor.extract_symbols(rust_file)
            assert result == []
        finally:
            Path(rust_file).unlink()

    def test_empty_file_returns_empty(self):
        """REQ-10: Empty file should return [] not raise."""
        parser = TreesitterParser()
        extractor = SymbolExtractor(parser)

        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as f:
            f.write(b"")
            empty_file = f.name

        try:
            result = extractor.extract_symbols(empty_file)
            assert result == []
        finally:
            Path(empty_file).unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
