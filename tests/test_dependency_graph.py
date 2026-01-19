"""Test suite for DependencyGraph class.

Tests cover:
- Symbol addition
- Reference addition
- PageRank importance computation
- Top symbols retrieval
- Statistics
- Edge cases (empty graph, isolated nodes)

Author: Cervella Tester
Date: 2026-01-19
"""

import pytest
from scripts.utils.dependency_graph import DependencyGraph, build_dependency_graph
from scripts.utils.symbol_extractor import Symbol


# Fixtures

@pytest.fixture
def graph():
    """Empty DependencyGraph."""
    return DependencyGraph()


@pytest.fixture
def sample_symbol():
    """Sample symbol for testing."""
    return Symbol(
        name="login",
        type="function",
        file="auth.py",
        line=10,
        signature="def login(username, password)",
        docstring="User login function",
        references=[]
    )


@pytest.fixture
def graph_with_symbols():
    """Graph with 3 symbols pre-added."""
    graph = DependencyGraph()

    # A references B and C
    # B references C
    # C is referenced by both (should have highest score)

    symbol_a = Symbol(
        name="function_a",
        type="function",
        file="test.py",
        line=1,
        signature="def function_a()",
        references=[]
    )

    symbol_b = Symbol(
        name="function_b",
        type="function",
        file="test.py",
        line=10,
        signature="def function_b()",
        references=[]
    )

    symbol_c = Symbol(
        name="function_c",
        type="function",
        file="test.py",
        line=20,
        signature="def function_c()",
        references=[]
    )

    graph.add_symbol(symbol_a)
    graph.add_symbol(symbol_b)
    graph.add_symbol(symbol_c)

    # A -> B, A -> C, B -> C
    graph.add_reference("test.py:function_a", "test.py:function_b")
    graph.add_reference("test.py:function_a", "test.py:function_c")
    graph.add_reference("test.py:function_b", "test.py:function_c")

    return graph


# Test: add_symbol()

def test_add_symbol_single(graph, sample_symbol):
    """Test adding a single symbol."""
    graph.add_symbol(sample_symbol)

    assert len(graph.nodes) == 1
    assert "auth.py:login" in graph.nodes
    assert graph.nodes["auth.py:login"] == sample_symbol


def test_add_symbol_multiple(graph):
    """Test adding multiple symbols."""
    symbol1 = Symbol(
        name="login",
        type="function",
        file="auth.py",
        line=10,
        signature="def login()",
        references=[]
    )

    symbol2 = Symbol(
        name="logout",
        type="function",
        file="auth.py",
        line=20,
        signature="def logout()",
        references=[]
    )

    graph.add_symbol(symbol1)
    graph.add_symbol(symbol2)

    assert len(graph.nodes) == 2
    assert "auth.py:login" in graph.nodes
    assert "auth.py:logout" in graph.nodes


def test_add_symbol_duplicate(graph, sample_symbol):
    """Test adding same symbol twice (should overwrite)."""
    graph.add_symbol(sample_symbol)
    graph.add_symbol(sample_symbol)

    # Should still have only 1 node
    assert len(graph.nodes) == 1


# Test: add_reference()

def test_add_reference(graph):
    """Test adding a reference between two symbols."""
    graph.add_reference("auth.py:login", "auth.py:verify")

    assert len(graph.edges) == 1
    assert ("auth.py:login", "auth.py:verify") in graph.edges


def test_add_reference_duplicate(graph):
    """Test adding same reference twice (should not duplicate)."""
    graph.add_reference("auth.py:login", "auth.py:verify")
    graph.add_reference("auth.py:login", "auth.py:verify")

    # Should only have 1 edge
    assert len(graph.edges) == 1


def test_add_reference_multiple(graph):
    """Test adding multiple references."""
    graph.add_reference("auth.py:login", "auth.py:verify")
    graph.add_reference("auth.py:login", "auth.py:hash_password")
    graph.add_reference("auth.py:logout", "auth.py:clear_session")

    assert len(graph.edges) == 3


# Test: compute_importance() - PageRank

def test_compute_importance_empty(graph):
    """Test computing importance on empty graph."""
    result = graph.compute_importance()

    # Empty graph should return empty dict
    assert result == {}
    assert graph.importance == {}


def test_compute_importance_single_node(graph, sample_symbol):
    """Test computing importance with single isolated node."""
    graph.add_symbol(sample_symbol)
    result = graph.compute_importance()

    # Single node should have score of 1.0
    assert "auth.py:login" in result
    assert result["auth.py:login"] == 1.0


def test_compute_importance_pagerank(graph_with_symbols):
    """Test PageRank correctly identifies most referenced symbol."""
    graph = graph_with_symbols
    graph.compute_importance()

    # function_c is referenced by both A and B
    # Should have highest importance score
    score_a = graph.importance["test.py:function_a"]
    score_b = graph.importance["test.py:function_b"]
    score_c = graph.importance["test.py:function_c"]

    # C should have highest score (most referenced)
    assert score_c > score_b
    assert score_c > score_a

    # All scores should sum to ~1.0 (within tolerance)
    total = score_a + score_b + score_c
    assert 0.95 <= total <= 1.05


def test_compute_importance_isolated_node(graph):
    """Test importance with isolated node (no edges)."""
    symbol1 = Symbol(
        name="isolated",
        type="function",
        file="test.py",
        line=1,
        signature="def isolated()",
        references=[]
    )

    symbol2 = Symbol(
        name="connected_a",
        type="function",
        file="test.py",
        line=10,
        signature="def connected_a()",
        references=[]
    )

    symbol3 = Symbol(
        name="connected_b",
        type="function",
        file="test.py",
        line=20,
        signature="def connected_b()",
        references=[]
    )

    graph.add_symbol(symbol1)
    graph.add_symbol(symbol2)
    graph.add_symbol(symbol3)

    # Only connect 2 and 3, leave 1 isolated
    graph.add_reference("test.py:connected_a", "test.py:connected_b")

    graph.compute_importance()

    # All nodes should have some importance (PageRank handles isolated nodes)
    assert "test.py:isolated" in graph.importance
    assert graph.importance["test.py:isolated"] > 0

    # Connected_b should have higher score than isolated
    assert graph.importance["test.py:connected_b"] > graph.importance["test.py:isolated"]


# Test: get_top_symbols()

def test_get_top_symbols(graph_with_symbols):
    """Test retrieving top N symbols."""
    graph = graph_with_symbols
    graph.compute_importance()

    top = graph.get_top_symbols(n=2)

    assert len(top) == 2
    assert all(isinstance(s, Symbol) for s in top)

    # First symbol should be function_c (most referenced)
    assert top[0].name == "function_c"


def test_get_top_symbols_auto_compute(graph_with_symbols):
    """Test get_top_symbols computes importance if not done."""
    graph = graph_with_symbols
    # Don't call compute_importance()

    top = graph.get_top_symbols(n=1)

    # Should auto-compute and return result
    assert len(top) == 1
    assert len(graph.importance) > 0


def test_get_top_symbols_limit(graph_with_symbols):
    """Test n parameter limits results."""
    graph = graph_with_symbols
    graph.compute_importance()

    top = graph.get_top_symbols(n=1)
    assert len(top) == 1

    top = graph.get_top_symbols(n=10)
    # Should return all 3 symbols (max available)
    assert len(top) == 3


# Test: get_stats()

def test_get_stats_empty(graph):
    """Test stats on empty graph."""
    stats = graph.get_stats()

    assert stats["nodes"] == 0
    assert stats["edges"] == 0
    assert stats["isolated"] == 0


def test_get_stats_with_data(graph_with_symbols):
    """Test stats on populated graph."""
    stats = graph_with_symbols.get_stats()

    assert stats["nodes"] == 3
    assert stats["edges"] == 3
    assert stats["isolated"] == 0  # All nodes are connected


def test_get_stats_with_isolated(graph):
    """Test stats correctly counts isolated nodes."""
    symbol1 = Symbol("func1", "function", "test.py", 1, "def func1()", references=[])
    symbol2 = Symbol("func2", "function", "test.py", 2, "def func2()", references=[])
    symbol3 = Symbol("func3", "function", "test.py", 3, "def func3()", references=[])

    graph.add_symbol(symbol1)
    graph.add_symbol(symbol2)
    graph.add_symbol(symbol3)

    # Only connect func1 -> func2, leave func3 isolated
    graph.add_reference("test.py:func1", "test.py:func2")

    stats = graph.get_stats()

    assert stats["nodes"] == 3
    assert stats["edges"] == 1
    assert stats["isolated"] == 1  # func3 is isolated


# Test: get_symbol_importance()

def test_get_symbol_importance(graph_with_symbols, sample_symbol):
    """Test retrieving importance score for specific symbol."""
    graph = graph_with_symbols
    graph.compute_importance()

    # Get symbol_c (should have highest score)
    symbol_c = graph.nodes["test.py:function_c"]
    score = graph.get_symbol_importance(symbol_c)

    assert score > 0
    assert isinstance(score, float)


def test_get_symbol_importance_not_found(graph, sample_symbol):
    """Test getting importance for symbol not in graph."""
    graph.compute_importance()

    score = graph.get_symbol_importance(sample_symbol)

    # Should return 0.0 for not found
    assert score == 0.0


# Test: get_symbol_references()

def test_get_symbol_references(graph_with_symbols):
    """Test getting symbols referenced by a symbol."""
    graph = graph_with_symbols

    symbol_a = graph.nodes["test.py:function_a"]
    refs = graph.get_symbol_references(symbol_a)

    # A references B and C
    assert len(refs) == 2
    assert "test.py:function_b" in refs
    assert "test.py:function_c" in refs


def test_get_symbol_references_none(graph, sample_symbol):
    """Test symbol with no references."""
    graph.add_symbol(sample_symbol)

    refs = graph.get_symbol_references(sample_symbol)

    assert refs == []


# Test: get_symbol_referenced_by()

def test_get_symbol_referenced_by(graph_with_symbols):
    """Test getting symbols that reference a symbol."""
    graph = graph_with_symbols

    symbol_c = graph.nodes["test.py:function_c"]
    referenced_by = graph.get_symbol_referenced_by(symbol_c)

    # C is referenced by A and B
    assert len(referenced_by) == 2
    assert "test.py:function_a" in referenced_by
    assert "test.py:function_b" in referenced_by


def test_get_symbol_referenced_by_none(graph, sample_symbol):
    """Test symbol not referenced by anyone."""
    graph.add_symbol(sample_symbol)

    referenced_by = graph.get_symbol_referenced_by(sample_symbol)

    assert referenced_by == []


# Test: build_dependency_graph() convenience function

def test_build_dependency_graph():
    """Test convenience function builds graph correctly."""
    symbol1 = Symbol(
        name="func1",
        type="function",
        file="test.py",
        line=1,
        signature="def func1()",
        references=["test.py:func2"]
    )

    symbol2 = Symbol(
        name="func2",
        type="function",
        file="test.py",
        line=10,
        signature="def func2()",
        references=[]
    )

    symbols = [symbol1, symbol2]
    graph = build_dependency_graph(symbols)

    # Should have 2 nodes
    assert len(graph.nodes) == 2

    # Should have 1 edge (func1 -> func2)
    assert len(graph.edges) == 1
    assert ("test.py:func1", "test.py:func2") in graph.edges


def test_build_dependency_graph_empty():
    """Test building graph from empty list."""
    graph = build_dependency_graph([])

    assert len(graph.nodes) == 0
    assert len(graph.edges) == 0


# Edge Cases

def test_pagerank_chain_graph(graph):
    """Test PageRank with chain: A -> B -> C."""
    symbol_a = Symbol("a", "function", "test.py", 1, "def a()", references=[])
    symbol_b = Symbol("b", "function", "test.py", 2, "def b()", references=[])
    symbol_c = Symbol("c", "function", "test.py", 3, "def c()", references=[])

    graph.add_symbol(symbol_a)
    graph.add_symbol(symbol_b)
    graph.add_symbol(symbol_c)

    graph.add_reference("test.py:a", "test.py:b")
    graph.add_reference("test.py:b", "test.py:c")

    graph.compute_importance()

    # C should have highest score (end of chain)
    score_a = graph.importance["test.py:a"]
    score_b = graph.importance["test.py:b"]
    score_c = graph.importance["test.py:c"]

    assert score_c > score_b
    assert score_b > score_a


def test_pagerank_star_graph(graph):
    """Test PageRank with star: A,B,C all reference D."""
    symbol_a = Symbol("a", "function", "test.py", 1, "def a()", references=[])
    symbol_b = Symbol("b", "function", "test.py", 2, "def b()", references=[])
    symbol_c = Symbol("c", "function", "test.py", 3, "def c()", references=[])
    symbol_d = Symbol("d", "function", "test.py", 4, "def d()", references=[])

    graph.add_symbol(symbol_a)
    graph.add_symbol(symbol_b)
    graph.add_symbol(symbol_c)
    graph.add_symbol(symbol_d)

    graph.add_reference("test.py:a", "test.py:d")
    graph.add_reference("test.py:b", "test.py:d")
    graph.add_reference("test.py:c", "test.py:d")

    graph.compute_importance()

    # D should have highest score (referenced by everyone)
    score_d = graph.importance["test.py:d"]
    score_a = graph.importance["test.py:a"]
    score_b = graph.importance["test.py:b"]
    score_c = graph.importance["test.py:c"]

    assert score_d > score_a
    assert score_d > score_b
    assert score_d > score_c


def test_symbol_id_format(graph, sample_symbol):
    """Test _get_symbol_id creates correct format."""
    symbol_id = graph._get_symbol_id(sample_symbol)

    assert symbol_id == "auth.py:login"
    assert ":" in symbol_id


def test_symbols_different_files(graph):
    """Test symbols with same name in different files."""
    symbol1 = Symbol("login", "function", "auth.py", 10, "def login()", references=[])
    symbol2 = Symbol("login", "function", "admin.py", 20, "def login()", references=[])

    graph.add_symbol(symbol1)
    graph.add_symbol(symbol2)

    # Should have 2 distinct nodes
    assert len(graph.nodes) == 2
    assert "auth.py:login" in graph.nodes
    assert "admin.py:login" in graph.nodes


# Test: Exception handling

def test_compute_importance_fallback(graph, monkeypatch):
    """Test PageRank fallback on exception."""
    # Add symbols
    symbol1 = Symbol("func1", "function", "test.py", 1, "def func1()", references=[])
    symbol2 = Symbol("func2", "function", "test.py", 2, "def func2()", references=[])
    graph.add_symbol(symbol1)
    graph.add_symbol(symbol2)

    # Mock pagerank to raise exception
    import networkx as nx

    def mock_pagerank(*args, **kwargs):
        raise ValueError("Simulated PageRank failure")

    monkeypatch.setattr(nx, "pagerank", mock_pagerank)

    # Should fallback to equal importance
    result = graph.compute_importance()

    # Each symbol should have equal importance (1/N)
    assert len(result) == 2
    assert result["test.py:func1"] == pytest.approx(0.5)
    assert result["test.py:func2"] == pytest.approx(0.5)
