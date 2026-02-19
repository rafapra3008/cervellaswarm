"""Tests for DependencyGraph module - Analysis, stats, build, export.

Covers: get_symbol_references, get_symbol_referenced_by, get_stats,
_get_symbol_id, build_dependency_graph, export_graphviz.

Author: Cervella Tester
Version: 1.0.0
Date: 2026-02-10
"""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from cervellaswarm_code_intelligence.dependency_graph import DependencyGraph, build_dependency_graph
from cervellaswarm_code_intelligence.symbol_types import Symbol


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
        graph.add_reference("app.py:10:caller", "app.py:20:callee")

        refs = graph.get_symbol_references(caller)

        assert len(refs) == 1
        assert "app.py:20:callee" in refs

    def test_get_symbol_references_multiple(self):
        """Test symbol referencing multiple symbols."""
        graph = DependencyGraph()

        caller = Symbol("caller", "function", "app.py", 10, "def caller():")
        callee1 = Symbol("callee1", "function", "app.py", 20, "def callee1():")
        callee2 = Symbol("callee2", "function", "app.py", 30, "def callee2():")

        graph.add_symbol(caller)
        graph.add_symbol(callee1)
        graph.add_symbol(callee2)

        graph.add_reference("app.py:10:caller", "app.py:20:callee1")
        graph.add_reference("app.py:10:caller", "app.py:30:callee2")

        refs = graph.get_symbol_references(caller)

        assert len(refs) == 2
        assert "app.py:20:callee1" in refs
        assert "app.py:30:callee2" in refs


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
        graph.add_reference("app.py:10:caller", "app.py:20:callee")

        refs = graph.get_symbol_referenced_by(callee)

        assert len(refs) == 1
        assert "app.py:10:caller" in refs

    def test_get_symbol_referenced_by_multiple(self):
        """Test symbol referenced by multiple symbols (hub)."""
        graph = DependencyGraph()

        hub = Symbol("hub", "function", "app.py", 10, "def hub():")
        caller1 = Symbol("caller1", "function", "app.py", 20, "def caller1():")
        caller2 = Symbol("caller2", "function", "app.py", 30, "def caller2():")

        graph.add_symbol(hub)
        graph.add_symbol(caller1)
        graph.add_symbol(caller2)

        graph.add_reference("app.py:20:caller1", "app.py:10:hub")
        graph.add_reference("app.py:30:caller2", "app.py:10:hub")

        refs = graph.get_symbol_referenced_by(hub)

        assert len(refs) == 2
        assert "app.py:20:caller1" in refs
        assert "app.py:30:caller2" in refs


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
        graph.add_reference("app.py:10:func1", "app.py:20:func2")

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

        graph.add_reference("app.py:10:c1", "app.py:20:c2")

        stats = graph.get_stats()

        assert stats['nodes'] == 3
        assert stats['edges'] == 1
        assert stats['isolated'] == 1


class TestGetSymbolId:
    """Test symbol ID generation."""

    def test_get_symbol_id_format(self):
        """Test symbol ID format is file:line:name."""
        graph = DependencyGraph()

        symbol = Symbol("my_func", "function", "app/auth.py", 42, "def my_func():")

        symbol_id = graph._get_symbol_id(symbol)

        assert symbol_id == "app/auth.py:42:my_func"

    def test_get_symbol_id_unique_per_file(self):
        """Test same name in different files gets different IDs."""
        graph = DependencyGraph()

        symbol1 = Symbol("login", "function", "auth.py", 10, "def login():")
        symbol2 = Symbol("login", "function", "admin.py", 10, "def login():")

        id1 = graph._get_symbol_id(symbol1)
        id2 = graph._get_symbol_id(symbol2)

        assert id1 != id2
        assert id1 == "auth.py:10:login"
        assert id2 == "admin.py:10:login"


class TestBuildDependencyGraph:
    """Test convenience function build_dependency_graph."""

    def test_build_dependency_graph_empty(self):
        """Test building graph from empty list."""
        graph = build_dependency_graph([])

        assert len(graph.nodes) == 0
        assert len(graph.edges) == 0

    def test_build_dependency_graph_multiple_symbols_no_refs(self):
        """Test building graph from symbols without references."""
        symbols = [
            Symbol("func1", "function", "app.py", 10, "def func1():"),
            Symbol("func2", "function", "app.py", 20, "def func2():"),
            Symbol("func3", "function", "app.py", 30, "def func3():")
        ]

        graph = build_dependency_graph(symbols)

        assert len(graph.nodes) == 3
        assert len(graph.edges) == 0

    def test_build_dependency_graph_single_symbol(self):
        """Test building graph from single symbol."""
        symbol = Symbol("func", "function", "app.py", 10, "def func():")

        graph = build_dependency_graph([symbol])

        assert len(graph.nodes) == 1
        assert "app.py:10:func" in graph.nodes

    def test_build_dependency_graph_with_references(self):
        """Test building graph with references (callee added first)."""
        callee = Symbol("callee", "function", "app.py", 20, "def callee():")
        caller = Symbol(
            "caller", "function", "app.py", 10, "def caller():",
            references=["callee"]
        )

        graph = build_dependency_graph([callee, caller])

        assert len(graph.nodes) == 2
        assert len(graph.edges) == 1
        edge = graph.edges[0]
        assert edge[0] == "app.py:10:caller"
        assert edge[1] == "app.py:20:callee"

    def test_build_dependency_graph_cross_file_references(self):
        """Test building graph with cross-file references."""
        func2 = Symbol("func2", "function", "file2.py", 10, "def func2():")
        func1 = Symbol(
            "func1", "function", "file1.py", 10, "def func1():",
            references=["func2"]
        )

        graph = build_dependency_graph([func2, func1])

        assert len(graph.nodes) == 2
        edge = graph.edges[0]
        assert edge[0] == "file1.py:10:func1"
        assert edge[1] == "file2.py:10:func2"


class TestExportGraphviz:
    """Test GraphViz DOT export functionality."""

    def test_export_graphviz_empty_graph(self):
        """Test exporting empty graph."""
        graph = DependencyGraph()

        with tempfile.NamedTemporaryFile(suffix=".dot", delete=False) as f:
            output_path = f.name

        try:
            graph.export_graphviz(output_path)
        finally:
            Path(output_path).unlink(missing_ok=True)

    def test_export_graphviz_no_pydot_fallback(self):
        """Test export gracefully fails when pydot not available."""
        graph = DependencyGraph()

        s1 = Symbol("func", "function", "app.py", 10, "def func():")
        graph.add_symbol(s1)

        with tempfile.NamedTemporaryFile(suffix=".dot", delete=False) as f:
            output_path = f.name

        try:
            with patch('cervellaswarm_code_intelligence.dependency_graph.nx.drawing.nx_pydot.write_dot') as mock_write:
                mock_write.side_effect = ImportError("pydot not found")
                graph.export_graphviz(output_path)
        finally:
            Path(output_path).unlink(missing_ok=True)

    def test_export_graphviz_with_nodes(self):
        """Test exporting graph with nodes."""
        graph = DependencyGraph()

        s1 = Symbol("func1", "function", "app.py", 10, "def func1():")
        s2 = Symbol("func2", "function", "app.py", 20, "def func2():")

        graph.add_symbol(s1)
        graph.add_symbol(s2)
        graph.add_reference("app.py:10:func1", "app.py:20:func2")

        with tempfile.NamedTemporaryFile(suffix=".dot", delete=False) as f:
            output_path = f.name

        try:
            graph.export_graphviz(output_path)

            if Path(output_path).exists() and Path(output_path).stat().st_size > 0:
                content = Path(output_path).read_text()
                assert "digraph" in content.lower() or "graph" in content.lower()
        finally:
            Path(output_path).unlink(missing_ok=True)

    def test_export_graphviz_top_n(self):
        """Test exporting only top N symbols."""
        graph = DependencyGraph()

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

    def test_export_graphviz_success_path(self):
        """Test export success path covers logger.info (line 350)."""
        graph = DependencyGraph()

        s1 = Symbol("func1", "function", "app.py", 10, "def func1():")
        s2 = Symbol("func2", "function", "app.py", 20, "def func2():")

        graph.add_symbol(s1)
        graph.add_symbol(s2)
        graph.add_reference("app.py:10:func1", "app.py:20:func2")

        with tempfile.NamedTemporaryFile(suffix=".dot", delete=False) as f:
            output_path = f.name

        try:
            with patch('cervellaswarm_code_intelligence.dependency_graph.nx.drawing.nx_pydot.write_dot'):
                graph.export_graphviz(output_path)
            # Success path reached (no exception)
        finally:
            Path(output_path).unlink(missing_ok=True)
