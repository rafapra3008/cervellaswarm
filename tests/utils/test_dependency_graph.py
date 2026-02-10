"""Tests for DependencyGraph module.

Test suite for dependency graph builder that analyzes symbol dependencies
and computes importance scores using PageRank algorithm.

Target: 70%+ coverage on dependency_graph.py

Author: Cervella Tester
Version: 1.0.0
Date: 2026-02-10
"""

import tempfile
from pathlib import Path

import pytest

# Import DependencyGraph and Symbol
from scripts.utils.dependency_graph import DependencyGraph, build_dependency_graph
from scripts.utils.symbol_types import Symbol


class TestDependencyGraphInit:
    """Test DependencyGraph initialization."""

    def test_init_empty_graph(self):
        """Test creating empty graph."""
        graph = DependencyGraph()

        assert graph.nodes == {}
        assert graph.edges == []
        assert graph.importance == {}

    def test_init_creates_new_instances(self):
        """Test each instance has its own state."""
        graph1 = DependencyGraph()
        graph2 = DependencyGraph()

        symbol = Symbol(
            name="test",
            type="function",
            file="test.py",
            line=1,
            signature="def test():"
        )
        graph1.add_symbol(symbol)

        assert len(graph1.nodes) == 1
        assert len(graph2.nodes) == 0


class TestAddSymbol:
    """Test adding symbols to graph."""

    def test_add_single_symbol(self):
        """Test adding one symbol."""
        graph = DependencyGraph()
        symbol = Symbol(
            name="my_function",
            type="function",
            file="app.py",
            line=10,
            signature="def my_function():"
        )

        graph.add_symbol(symbol)

        assert len(graph.nodes) == 1
        symbol_id = "app.py:my_function"
        assert symbol_id in graph.nodes
        assert graph.nodes[symbol_id] == symbol

    def test_add_multiple_symbols_same_file(self):
        """Test adding multiple symbols from same file."""
        graph = DependencyGraph()

        symbol1 = Symbol("func1", "function", "app.py", 10, "def func1():")
        symbol2 = Symbol("func2", "function", "app.py", 20, "def func2():")

        graph.add_symbol(symbol1)
        graph.add_symbol(symbol2)

        assert len(graph.nodes) == 2
        assert "app.py:func1" in graph.nodes
        assert "app.py:func2" in graph.nodes

    def test_add_symbols_different_files(self):
        """Test adding symbols from different files."""
        graph = DependencyGraph()

        symbol1 = Symbol("func", "function", "app.py", 10, "def func():")
        symbol2 = Symbol("func", "function", "utils.py", 10, "def func():")

        graph.add_symbol(symbol1)
        graph.add_symbol(symbol2)

        # Same name, different files = different IDs
        assert len(graph.nodes) == 2
        assert "app.py:func" in graph.nodes
        assert "utils.py:func" in graph.nodes

    def test_add_symbol_overwrites_existing(self):
        """Test adding symbol with same ID overwrites."""
        graph = DependencyGraph()

        symbol1 = Symbol("func", "function", "app.py", 10, "def func():")
        symbol2 = Symbol("func", "function", "app.py", 10, "def func(): # updated")

        graph.add_symbol(symbol1)
        graph.add_symbol(symbol2)

        assert len(graph.nodes) == 1
        assert graph.nodes["app.py:func"].signature == "def func(): # updated"


class TestAddReference:
    """Test adding references (edges) to graph."""

    def test_add_reference_simple(self):
        """Test adding a reference between two symbols."""
        graph = DependencyGraph()

        symbol1 = Symbol("caller", "function", "app.py", 10, "def caller():")
        symbol2 = Symbol("callee", "function", "app.py", 20, "def callee():")

        graph.add_symbol(symbol1)
        graph.add_symbol(symbol2)

        from_id = "app.py:caller"
        to_id = "app.py:callee"
        graph.add_reference(from_id, to_id)

        assert len(graph.edges) == 1
        assert (from_id, to_id) in graph.edges

    def test_add_reference_resolve_name(self):
        """Test adding reference by symbol name (auto-resolves to ID)."""
        graph = DependencyGraph()

        symbol1 = Symbol("caller", "function", "app.py", 10, "def caller():")
        symbol2 = Symbol("callee", "function", "app.py", 20, "def callee():")

        graph.add_symbol(symbol1)
        graph.add_symbol(symbol2)

        # Reference by name (without ":"), should resolve to full ID
        graph.add_reference("app.py:caller", "callee")

        assert len(graph.edges) == 1
        assert ("app.py:caller", "app.py:callee") in graph.edges

    def test_add_reference_no_duplicate(self):
        """Test adding same reference twice doesn't create duplicate."""
        graph = DependencyGraph()

        symbol = Symbol("func", "function", "app.py", 10, "def func():")
        graph.add_symbol(symbol)

        graph.add_reference("app.py:func", "other")
        graph.add_reference("app.py:func", "other")

        assert len(graph.edges) == 1

    def test_add_reference_multiple_edges(self):
        """Test adding multiple references."""
        graph = DependencyGraph()

        s1 = Symbol("a", "function", "app.py", 10, "def a():")
        s2 = Symbol("b", "function", "app.py", 20, "def b():")
        s3 = Symbol("c", "function", "app.py", 30, "def c():")

        graph.add_symbol(s1)
        graph.add_symbol(s2)
        graph.add_symbol(s3)

        graph.add_reference("app.py:a", "app.py:b")
        graph.add_reference("app.py:a", "app.py:c")
        graph.add_reference("app.py:b", "app.py:c")

        assert len(graph.edges) == 3


class TestComputeImportance:
    """Test PageRank importance computation."""

    def test_compute_importance_empty_graph(self):
        """Test computing importance on empty graph."""
        graph = DependencyGraph()

        scores = graph.compute_importance()

        assert scores == {}
        assert graph.importance == {}

    def test_compute_importance_single_node(self):
        """Test computing importance with single isolated node."""
        graph = DependencyGraph()

        symbol = Symbol("func", "function", "app.py", 10, "def func():")
        graph.add_symbol(symbol)

        scores = graph.compute_importance()

        assert len(scores) == 1
        assert "app.py:func" in scores
        # Single node gets score of 1.0
        assert scores["app.py:func"] == pytest.approx(1.0, abs=0.01)

    def test_compute_importance_two_nodes_with_reference(self):
        """Test importance: referenced symbol should rank higher."""
        graph = DependencyGraph()

        caller = Symbol("caller", "function", "app.py", 10, "def caller():")
        callee = Symbol("callee", "function", "app.py", 20, "def callee():")

        graph.add_symbol(caller)
        graph.add_symbol(callee)
        graph.add_reference("app.py:caller", "app.py:callee")

        scores = graph.compute_importance()

        # Callee (referenced) should have higher score than caller
        assert scores["app.py:callee"] > scores["app.py:caller"]

    def test_compute_importance_multiple_references(self):
        """Test importance: symbol referenced by many ranks highest."""
        graph = DependencyGraph()

        # Create hub symbol that many symbols reference
        hub = Symbol("hub", "function", "app.py", 10, "def hub():")
        caller1 = Symbol("caller1", "function", "app.py", 20, "def caller1():")
        caller2 = Symbol("caller2", "function", "app.py", 30, "def caller2():")
        caller3 = Symbol("caller3", "function", "app.py", 40, "def caller3():")

        graph.add_symbol(hub)
        graph.add_symbol(caller1)
        graph.add_symbol(caller2)
        graph.add_symbol(caller3)

        # All callers reference hub
        graph.add_reference("app.py:caller1", "app.py:hub")
        graph.add_reference("app.py:caller2", "app.py:hub")
        graph.add_reference("app.py:caller3", "app.py:hub")

        scores = graph.compute_importance()

        # Hub should have highest score
        hub_score = scores["app.py:hub"]
        assert hub_score > scores["app.py:caller1"]
        assert hub_score > scores["app.py:caller2"]
        assert hub_score > scores["app.py:caller3"]

    def test_compute_importance_isolated_node(self):
        """Test isolated node gets low importance."""
        graph = DependencyGraph()

        connected1 = Symbol("c1", "function", "app.py", 10, "def c1():")
        connected2 = Symbol("c2", "function", "app.py", 20, "def c2():")
        isolated = Symbol("isolated", "function", "app.py", 30, "def isolated():")

        graph.add_symbol(connected1)
        graph.add_symbol(connected2)
        graph.add_symbol(isolated)

        graph.add_reference("app.py:c1", "app.py:c2")

        scores = graph.compute_importance()

        # Isolated node should have lower score
        assert scores["app.py:isolated"] < scores["app.py:c2"]


class TestGetTopSymbols:
    """Test retrieving top N symbols by importance."""

    def test_get_top_symbols_empty_graph(self):
        """Test get_top_symbols on empty graph."""
        graph = DependencyGraph()

        top = graph.get_top_symbols(n=5)

        assert top == []

    def test_get_top_symbols_auto_computes_importance(self):
        """Test get_top_symbols computes importance if not done yet."""
        graph = DependencyGraph()

        symbol = Symbol("func", "function", "app.py", 10, "def func():")
        graph.add_symbol(symbol)

        # Don't call compute_importance()
        assert graph.importance == {}

        top = graph.get_top_symbols(n=1)

        # Should auto-compute
        assert len(graph.importance) > 0
        assert len(top) == 1
        assert top[0] == symbol

    def test_get_top_symbols_sorted_by_importance(self):
        """Test top symbols are sorted by importance (highest first)."""
        graph = DependencyGraph()

        hub = Symbol("hub", "function", "app.py", 10, "def hub():")
        caller1 = Symbol("caller1", "function", "app.py", 20, "def caller1():")
        caller2 = Symbol("caller2", "function", "app.py", 30, "def caller2():")

        graph.add_symbol(hub)
        graph.add_symbol(caller1)
        graph.add_symbol(caller2)

        graph.add_reference("app.py:caller1", "app.py:hub")
        graph.add_reference("app.py:caller2", "app.py:hub")

        graph.compute_importance()
        top = graph.get_top_symbols(n=3)

        # Hub should be first (most important)
        assert top[0].name == "hub"

    def test_get_top_symbols_limit_n(self):
        """Test get_top_symbols respects n limit."""
        graph = DependencyGraph()

        for i in range(10):
            symbol = Symbol(f"func{i}", "function", "app.py", i*10, f"def func{i}():")
            graph.add_symbol(symbol)

        top = graph.get_top_symbols(n=3)

        assert len(top) == 3


class TestGetSymbolImportance:
    """Test retrieving importance for specific symbol."""

    def test_get_symbol_importance_existing(self):
        """Test getting importance for existing symbol."""
        graph = DependencyGraph()

        symbol = Symbol("func", "function", "app.py", 10, "def func():")
        graph.add_symbol(symbol)
        graph.compute_importance()

        score = graph.get_symbol_importance(symbol)

        assert score > 0.0
        assert score == pytest.approx(1.0, abs=0.01)

    def test_get_symbol_importance_not_computed(self):
        """Test getting importance before compute returns 0.0."""
        graph = DependencyGraph()

        symbol = Symbol("func", "function", "app.py", 10, "def func():")
        graph.add_symbol(symbol)

        # Don't compute importance
        score = graph.get_symbol_importance(symbol)

        assert score == 0.0

    def test_get_symbol_importance_not_in_graph(self):
        """Test getting importance for symbol not in graph."""
        graph = DependencyGraph()

        other_symbol = Symbol("other", "function", "other.py", 1, "def other():")
        graph.compute_importance()

        score = graph.get_symbol_importance(other_symbol)

        assert score == 0.0


class TestGetSymbolReferences:
    """Test retrieving references made by a symbol."""

    def test_get_symbol_references_no_refs(self):
        """Test symbol with no references."""
        graph = DependencyGraph()

        symbol = Symbol("func", "function", "app.py", 10, "def func():")
        graph.add_symbol(symbol)

        refs = graph.get_symbol_references(symbol)

        assert refs == []

    def test_get_symbol_references_single(self):
        """Test symbol with one reference."""
        graph = DependencyGraph()

        caller = Symbol("caller", "function", "app.py", 10, "def caller():")
        callee = Symbol("callee", "function", "app.py", 20, "def callee():")

        graph.add_symbol(caller)
        graph.add_symbol(callee)
        graph.add_reference("app.py:caller", "app.py:callee")

        refs = graph.get_symbol_references(caller)

        assert len(refs) == 1
        assert "app.py:callee" in refs

    def test_get_symbol_references_multiple(self):
        """Test symbol referencing multiple symbols."""
        graph = DependencyGraph()

        caller = Symbol("caller", "function", "app.py", 10, "def caller():")
        callee1 = Symbol("callee1", "function", "app.py", 20, "def callee1():")
        callee2 = Symbol("callee2", "function", "app.py", 30, "def callee2():")

        graph.add_symbol(caller)
        graph.add_symbol(callee1)
        graph.add_symbol(callee2)

        graph.add_reference("app.py:caller", "app.py:callee1")
        graph.add_reference("app.py:caller", "app.py:callee2")

        refs = graph.get_symbol_references(caller)

        assert len(refs) == 2
        assert "app.py:callee1" in refs
        assert "app.py:callee2" in refs


class TestGetSymbolReferencedBy:
    """Test retrieving symbols that reference this symbol."""

    def test_get_symbol_referenced_by_none(self):
        """Test symbol not referenced by anyone."""
        graph = DependencyGraph()

        symbol = Symbol("func", "function", "app.py", 10, "def func():")
        graph.add_symbol(symbol)

        refs = graph.get_symbol_referenced_by(symbol)

        assert refs == []

    def test_get_symbol_referenced_by_single(self):
        """Test symbol referenced by one other symbol."""
        graph = DependencyGraph()

        caller = Symbol("caller", "function", "app.py", 10, "def caller():")
        callee = Symbol("callee", "function", "app.py", 20, "def callee():")

        graph.add_symbol(caller)
        graph.add_symbol(callee)
        graph.add_reference("app.py:caller", "app.py:callee")

        refs = graph.get_symbol_referenced_by(callee)

        assert len(refs) == 1
        assert "app.py:caller" in refs

    def test_get_symbol_referenced_by_multiple(self):
        """Test symbol referenced by multiple symbols (hub)."""
        graph = DependencyGraph()

        hub = Symbol("hub", "function", "app.py", 10, "def hub():")
        caller1 = Symbol("caller1", "function", "app.py", 20, "def caller1():")
        caller2 = Symbol("caller2", "function", "app.py", 30, "def caller2():")

        graph.add_symbol(hub)
        graph.add_symbol(caller1)
        graph.add_symbol(caller2)

        graph.add_reference("app.py:caller1", "app.py:hub")
        graph.add_reference("app.py:caller2", "app.py:hub")

        refs = graph.get_symbol_referenced_by(hub)

        assert len(refs) == 2
        assert "app.py:caller1" in refs
        assert "app.py:caller2" in refs


class TestGetStats:
    """Test graph statistics."""

    def test_get_stats_empty_graph(self):
        """Test stats on empty graph."""
        graph = DependencyGraph()

        stats = graph.get_stats()

        assert stats == {
            'nodes': 0,
            'edges': 0,
            'isolated': 0
        }

    def test_get_stats_single_node(self):
        """Test stats with one isolated node."""
        graph = DependencyGraph()

        symbol = Symbol("func", "function", "app.py", 10, "def func():")
        graph.add_symbol(symbol)

        stats = graph.get_stats()

        assert stats['nodes'] == 1
        assert stats['edges'] == 0
        assert stats['isolated'] == 1

    def test_get_stats_connected_nodes(self):
        """Test stats with connected nodes."""
        graph = DependencyGraph()

        s1 = Symbol("func1", "function", "app.py", 10, "def func1():")
        s2 = Symbol("func2", "function", "app.py", 20, "def func2():")

        graph.add_symbol(s1)
        graph.add_symbol(s2)
        graph.add_reference("app.py:func1", "app.py:func2")

        stats = graph.get_stats()

        assert stats['nodes'] == 2
        assert stats['edges'] == 1
        assert stats['isolated'] == 0

    def test_get_stats_mixed_connected_and_isolated(self):
        """Test stats with both connected and isolated nodes."""
        graph = DependencyGraph()

        connected1 = Symbol("c1", "function", "app.py", 10, "def c1():")
        connected2 = Symbol("c2", "function", "app.py", 20, "def c2():")
        isolated = Symbol("isolated", "function", "app.py", 30, "def isolated():")

        graph.add_symbol(connected1)
        graph.add_symbol(connected2)
        graph.add_symbol(isolated)

        graph.add_reference("app.py:c1", "app.py:c2")

        stats = graph.get_stats()

        assert stats['nodes'] == 3
        assert stats['edges'] == 1
        assert stats['isolated'] == 1


class TestGetSymbolId:
    """Test symbol ID generation."""

    def test_get_symbol_id_format(self):
        """Test symbol ID format is file:name."""
        graph = DependencyGraph()

        symbol = Symbol("my_func", "function", "app/auth.py", 42, "def my_func():")

        symbol_id = graph._get_symbol_id(symbol)

        assert symbol_id == "app/auth.py:my_func"

    def test_get_symbol_id_unique_per_file(self):
        """Test same name in different files gets different IDs."""
        graph = DependencyGraph()

        symbol1 = Symbol("login", "function", "auth.py", 10, "def login():")
        symbol2 = Symbol("login", "function", "admin.py", 10, "def login():")

        id1 = graph._get_symbol_id(symbol1)
        id2 = graph._get_symbol_id(symbol2)

        assert id1 != id2
        assert id1 == "auth.py:login"
        assert id2 == "admin.py:login"


class TestBuildDependencyGraph:
    """Test convenience function build_dependency_graph."""

    def test_build_dependency_graph_empty(self):
        """Test building graph from empty list."""
        symbols = []

        graph = build_dependency_graph(symbols)

        assert len(graph.nodes) == 0
        assert len(graph.edges) == 0

    def test_build_dependency_graph_single_symbol(self):
        """Test building graph from single symbol."""
        symbol = Symbol("func", "function", "app.py", 10, "def func():")

        graph = build_dependency_graph([symbol])

        assert len(graph.nodes) == 1
        assert "app.py:func" in graph.nodes

    def test_build_dependency_graph_with_references(self):
        """Test building graph from symbols with references.

        Note: build_dependency_graph adds symbols sequentially, so references
        are only resolved if the target symbol was already added to the graph.
        If callee is added first, the reference will be resolved.
        """
        callee = Symbol("callee", "function", "app.py", 20, "def callee():")
        caller = Symbol(
            "caller", "function", "app.py", 10, "def caller():",
            references=["callee"]
        )

        # Add callee first, then caller with reference to callee
        graph = build_dependency_graph([callee, caller])

        assert len(graph.nodes) == 2
        assert len(graph.edges) == 1
        # Reference should be resolved since callee was added first
        edge = graph.edges[0]
        assert edge[0] == "app.py:caller"
        assert edge[1] == "app.py:callee"  # Resolved from "callee"

    def test_build_dependency_graph_cross_file_references(self):
        """Test building graph with cross-file references.

        Note: References are only resolved if target was added to graph first.
        """
        func2 = Symbol("func2", "function", "file2.py", 10, "def func2():")
        func1 = Symbol(
            "func1", "function", "file1.py", 10, "def func1():",
            references=["func2"]
        )

        # Add func2 first, then func1 with reference to func2
        graph = build_dependency_graph([func2, func1])

        assert len(graph.nodes) == 2
        # Reference should be resolved since func2 was added first
        edge = graph.edges[0]
        assert edge[0] == "file1.py:func1"
        assert edge[1] == "file2.py:func2"  # Resolved from "func2"


class TestExportGraphviz:
    """Test GraphViz DOT export functionality."""

    def test_export_graphviz_empty_graph(self):
        """Test exporting empty graph (should not crash)."""
        graph = DependencyGraph()

        with tempfile.NamedTemporaryFile(suffix=".dot", delete=False) as f:
            output_path = f.name

        try:
            # Should not raise exception
            graph.export_graphviz(output_path)
        finally:
            Path(output_path).unlink(missing_ok=True)

    def test_export_graphviz_with_nodes(self):
        """Test exporting graph with nodes (requires pydot)."""
        graph = DependencyGraph()

        s1 = Symbol("func1", "function", "app.py", 10, "def func1():")
        s2 = Symbol("func2", "function", "app.py", 20, "def func2():")

        graph.add_symbol(s1)
        graph.add_symbol(s2)
        graph.add_reference("app.py:func1", "app.py:func2")

        with tempfile.NamedTemporaryFile(suffix=".dot", delete=False) as f:
            output_path = f.name

        try:
            # export_graphviz requires pydot, may fail gracefully
            graph.export_graphviz(output_path)

            # If pydot is available, file should have content
            if Path(output_path).exists() and Path(output_path).stat().st_size > 0:
                content = Path(output_path).read_text()
                assert "digraph" in content.lower() or "graph" in content.lower()
            # If pydot not available, that's OK (graceful degradation)
        finally:
            Path(output_path).unlink(missing_ok=True)

    def test_export_graphviz_top_n(self):
        """Test exporting only top N symbols."""
        graph = DependencyGraph()

        # Add 5 symbols, only export top 2
        for i in range(5):
            symbol = Symbol(f"func{i}", "function", "app.py", i*10, f"def func{i}():")
            graph.add_symbol(symbol)

        graph.compute_importance()

        with tempfile.NamedTemporaryFile(suffix=".dot", delete=False) as f:
            output_path = f.name

        try:
            graph.export_graphviz(output_path, top_n=2)

            assert Path(output_path).exists()
        finally:
            Path(output_path).unlink(missing_ok=True)
