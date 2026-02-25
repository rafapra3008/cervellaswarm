"""Tests for DependencyGraph module - Core operations.

Test suite for dependency graph core: init, add_symbol, add_reference,
compute_importance, get_top_symbols, get_symbol_importance.

Target: 70%+ coverage on dependency_graph.py

Author: Cervella Tester
Version: 1.0.0
Date: 2026-02-10
"""

from unittest.mock import patch

import pytest

from cervellaswarm_code_intelligence.dependency_graph import DependencyGraph
from cervellaswarm_code_intelligence.symbol_types import Symbol


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
        symbol_id = "app.py:10:my_function"
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
        assert "app.py:10:func1" in graph.nodes
        assert "app.py:20:func2" in graph.nodes

    def test_add_symbols_different_files(self):
        """Test adding symbols from different files."""
        graph = DependencyGraph()

        symbol1 = Symbol("func", "function", "app.py", 10, "def func():")
        symbol2 = Symbol("func", "function", "utils.py", 10, "def func():")

        graph.add_symbol(symbol1)
        graph.add_symbol(symbol2)

        # Same name, different files = different IDs
        assert len(graph.nodes) == 2
        assert "app.py:10:func" in graph.nodes
        assert "utils.py:10:func" in graph.nodes

    def test_add_symbol_overwrites_existing(self):
        """Test adding symbol with same ID overwrites."""
        graph = DependencyGraph()

        symbol1 = Symbol("func", "function", "app.py", 10, "def func():")
        symbol2 = Symbol("func", "function", "app.py", 10, "def func(): # updated")

        graph.add_symbol(symbol1)
        graph.add_symbol(symbol2)

        assert len(graph.nodes) == 1
        assert graph.nodes["app.py:10:func"].signature == "def func(): # updated"

    def test_add_symbol_same_name_different_lines_no_collision(self):
        """Test same name at different lines are stored separately.

        Bug H4: Old format 'file:name' caused __init__ in multiple classes
        to collide. New format 'file:line:name' prevents this.
        """
        graph = DependencyGraph()

        init1 = Symbol("__init__", "function", "models.py", 5, "def __init__(self):")
        init2 = Symbol("__init__", "function", "models.py", 25, "def __init__(self):")

        graph.add_symbol(init1)
        graph.add_symbol(init2)

        # Both should be stored (different line numbers = different IDs)
        assert len(graph.nodes) == 2
        assert "models.py:5:__init__" in graph.nodes
        assert "models.py:25:__init__" in graph.nodes


class TestAddReference:
    """Test adding references (edges) to graph."""

    def test_add_reference_simple(self):
        """Test adding a reference between two symbols."""
        graph = DependencyGraph()

        symbol1 = Symbol("caller", "function", "app.py", 10, "def caller():")
        symbol2 = Symbol("callee", "function", "app.py", 20, "def callee():")

        graph.add_symbol(symbol1)
        graph.add_symbol(symbol2)

        from_id = "app.py:10:caller"
        to_id = "app.py:20:callee"
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
        graph.add_reference("app.py:10:caller", "callee")

        assert len(graph.edges) == 1
        assert ("app.py:10:caller", "app.py:20:callee") in graph.edges

    def test_add_reference_no_duplicate(self):
        """Test adding same reference twice doesn't create duplicate."""
        graph = DependencyGraph()

        symbol = Symbol("func", "function", "app.py", 10, "def func():")
        graph.add_symbol(symbol)

        graph.add_reference("app.py:10:func", "other")
        graph.add_reference("app.py:10:func", "other")

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

        graph.add_reference("app.py:10:a", "app.py:20:b")
        graph.add_reference("app.py:10:a", "app.py:30:c")
        graph.add_reference("app.py:20:b", "app.py:30:c")

        assert len(graph.edges) == 3

    def test_add_reference_unresolved_name(self):
        """Test adding reference to non-existent symbol (doesn't resolve)."""
        graph = DependencyGraph()

        symbol = Symbol("caller", "function", "app.py", 10, "def caller():")
        graph.add_symbol(symbol)

        # Reference to symbol not in graph (won't resolve)
        graph.add_reference("app.py:10:caller", "unknown_function")

        assert len(graph.edges) == 1
        # Edge stored with unresolved name
        assert ("app.py:10:caller", "unknown_function") in graph.edges


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
        assert "app.py:10:func" in scores
        # Single node gets score of 1.0
        assert scores["app.py:10:func"] == pytest.approx(1.0, abs=0.01)

    def test_compute_importance_two_nodes_with_reference(self):
        """Test importance: referenced symbol should rank higher."""
        graph = DependencyGraph()

        caller = Symbol("caller", "function", "app.py", 10, "def caller():")
        callee = Symbol("callee", "function", "app.py", 20, "def callee():")

        graph.add_symbol(caller)
        graph.add_symbol(callee)
        graph.add_reference("app.py:10:caller", "app.py:20:callee")

        scores = graph.compute_importance()

        # Callee (referenced) should have higher score than caller
        assert scores["app.py:20:callee"] > scores["app.py:10:caller"]

    def test_compute_importance_multiple_references(self):
        """Test importance: symbol referenced by many ranks highest."""
        graph = DependencyGraph()

        hub = Symbol("hub", "function", "app.py", 10, "def hub():")
        caller1 = Symbol("caller1", "function", "app.py", 20, "def caller1():")
        caller2 = Symbol("caller2", "function", "app.py", 30, "def caller2():")
        caller3 = Symbol("caller3", "function", "app.py", 40, "def caller3():")

        graph.add_symbol(hub)
        graph.add_symbol(caller1)
        graph.add_symbol(caller2)
        graph.add_symbol(caller3)

        graph.add_reference("app.py:20:caller1", "app.py:10:hub")
        graph.add_reference("app.py:30:caller2", "app.py:10:hub")
        graph.add_reference("app.py:40:caller3", "app.py:10:hub")

        scores = graph.compute_importance()

        hub_score = scores["app.py:10:hub"]
        assert hub_score > scores["app.py:20:caller1"]
        assert hub_score > scores["app.py:30:caller2"]
        assert hub_score > scores["app.py:40:caller3"]

    def test_compute_importance_isolated_node(self):
        """Test isolated node gets low importance."""
        graph = DependencyGraph()

        connected1 = Symbol("c1", "function", "app.py", 10, "def c1():")
        connected2 = Symbol("c2", "function", "app.py", 20, "def c2():")
        isolated = Symbol("isolated", "function", "app.py", 30, "def isolated():")

        graph.add_symbol(connected1)
        graph.add_symbol(connected2)
        graph.add_symbol(isolated)

        graph.add_reference("app.py:10:c1", "app.py:20:c2")

        scores = graph.compute_importance()

        assert scores["app.py:30:isolated"] < scores["app.py:20:c2"]

    def test_compute_importance_pagerank_failure_fallback(self):
        """Test fallback when PageRank computation fails."""
        graph = DependencyGraph()

        s1 = Symbol("func1", "function", "app.py", 10, "def func1():")
        s2 = Symbol("func2", "function", "app.py", 20, "def func2():")

        graph.add_symbol(s1)
        graph.add_symbol(s2)

        with patch('cervellaswarm_code_intelligence.dependency_graph.nx.pagerank') as mock_pr:
            mock_pr.side_effect = Exception("PageRank failed")

            scores = graph.compute_importance()

            assert len(scores) == 2
            assert scores["app.py:10:func1"] == pytest.approx(0.5)
            assert scores["app.py:20:func2"] == pytest.approx(0.5)


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

        assert graph.importance == {}

        top = graph.get_top_symbols(n=1)

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

        graph.add_reference("app.py:20:caller1", "app.py:10:hub")
        graph.add_reference("app.py:30:caller2", "app.py:10:hub")

        graph.compute_importance()
        top = graph.get_top_symbols(n=3)

        assert top[0].name == "hub"

    def test_get_top_symbols_limit_n(self):
        """Test get_top_symbols respects n limit."""
        graph = DependencyGraph()

        for i in range(10):
            symbol = Symbol(f"func{i}", "function", "app.py", i*10, f"def func{i}():")
            graph.add_symbol(symbol)

        top = graph.get_top_symbols(n=3)

        assert len(top) == 3

    def test_get_top_symbols_with_phantom_nodes(self):
        """Test get_top_symbols filters out phantom nodes from edges.

        Bug H3: add_edges_from() in NetworkX adds implicit nodes for
        unresolved references. PageRank computes scores for these phantom
        nodes, but they don't exist in self.nodes, causing KeyError.
        """
        graph = DependencyGraph()

        sym1 = Symbol("foo", "function", "a.py", 1, "def foo():")
        sym2 = Symbol("bar", "function", "a.py", 10, "def bar():")
        graph.add_symbol(sym1)
        graph.add_symbol(sym2)

        # Add edge to a symbol NOT in the graph (phantom node)
        graph.add_reference("a.py:1:foo", "nonexistent_function")

        graph.compute_importance()

        # Should NOT raise KeyError
        top = graph.get_top_symbols(10)
        assert len(top) == 2
        # All returned symbols should be real Symbol objects
        for sym in top:
            assert isinstance(sym, Symbol)


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

        score = graph.get_symbol_importance(symbol)

        assert score == 0.0

    def test_get_symbol_importance_not_in_graph(self):
        """Test getting importance for symbol not in graph."""
        graph = DependencyGraph()

        other_symbol = Symbol("other", "function", "other.py", 1, "def other():")
        graph.compute_importance()

        score = graph.get_symbol_importance(other_symbol)

        assert score == 0.0
