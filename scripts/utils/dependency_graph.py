"""Dependency Graph Builder for Repository Mapping.

This module builds a directed graph of symbol dependencies ("who uses who")
and computes importance scores using PageRank algorithm. Symbols that are
referenced more frequently are considered more important.

The graph is used by RepoMapper to prioritize which symbols to include in
the repository map based on their importance score.

Usage:
    from symbol_extractor import Symbol
    from dependency_graph import DependencyGraph

    graph = DependencyGraph()
    graph.add_symbol(symbol1)
    graph.add_symbol(symbol2)
    graph.add_reference(symbol1.name, symbol2.name)

    graph.compute_importance()
    top = graph.get_top_symbols(n=10)

Importance Algorithm:
    - Uses PageRank (via NetworkX) to compute symbol importance
    - Nodes = symbols defined in codebase
    - Edges = references (function calls, class usage, etc.)
    - Higher score = more referenced = more important

Author: Cervella Backend
Version: 1.0.0
Date: 2026-01-19
"""

__version__ = "1.0.0"
__version_date__ = "2026-01-19"

import logging
from typing import Dict, List, Optional

import networkx as nx

# Import Symbol from symbol_extractor
try:
    from symbol_extractor import Symbol
except ImportError:
    # Fallback for direct execution
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))
    from symbol_extractor import Symbol

# Configure logging
logger = logging.getLogger(__name__)


class DependencyGraph:
    """Build and analyze dependency graph of code symbols.

    This class constructs a directed graph where:
    - Nodes = symbols (functions, classes, interfaces, types)
    - Edges = references (from_symbol references to_symbol)

    It computes importance scores using PageRank algorithm, which assigns
    higher scores to symbols that are referenced more frequently by other
    symbols.

    Attributes:
        nodes: Dictionary mapping symbol_id to Symbol object
        edges: List of tuples (from_id, to_id) representing references
        importance: Dictionary mapping symbol_id to importance score
    """

    def __init__(self):
        """Initialize empty dependency graph."""
        self.nodes: Dict[str, Symbol] = {}
        self.edges: List[tuple] = []
        self.importance: Dict[str, float] = {}

        logger.debug("DependencyGraph initialized")

    def add_symbol(self, symbol: Symbol) -> None:
        """Add a symbol as node in the graph.

        The symbol ID is constructed as "{file}:{name}" to ensure uniqueness
        across files.

        Args:
            symbol: Symbol object to add

        Example:
            >>> graph = DependencyGraph()
            >>> symbol = Symbol(name="login", type="function", ...)
            >>> graph.add_symbol(symbol)
        """
        symbol_id = self._get_symbol_id(symbol)
        self.nodes[symbol_id] = symbol
        logger.debug(f"Added symbol: {symbol_id}")

    def add_reference(self, from_symbol: str, to_symbol: str) -> None:
        """Add edge representing a reference.

        Records that from_symbol references/uses to_symbol.

        Args:
            from_symbol: ID of the symbol making the reference
            to_symbol: ID of the symbol being referenced

        Example:
            >>> graph.add_reference("auth.py:login", "auth.py:verify_credentials")
            >>> # login() calls verify_credentials()
        """
        edge = (from_symbol, to_symbol)
        if edge not in self.edges:
            self.edges.append(edge)
            logger.debug(f"Added reference: {from_symbol} -> {to_symbol}")

    def compute_importance(self) -> Dict[str, float]:
        """Compute importance scores via PageRank algorithm.

        Uses NetworkX's pagerank implementation. Symbols that are referenced
        more frequently by other symbols will have higher importance scores.

        Returns:
            Dictionary mapping symbol_id to importance score (0.0 to 1.0)

        Example:
            >>> graph = DependencyGraph()
            >>> # ... add symbols and references ...
            >>> scores = graph.compute_importance()
            >>> print(scores["auth.py:verify_credentials"])
            0.15  # High score = important
        """
        if not self.nodes:
            logger.warning("No nodes in graph, cannot compute importance")
            return {}

        # Build NetworkX directed graph
        G = nx.DiGraph()

        # Add all nodes (even isolated ones)
        G.add_nodes_from(self.nodes.keys())

        # Add edges (references)
        if self.edges:
            G.add_edges_from(self.edges)
            logger.debug(f"Added {len(self.edges)} edges to graph")

        # Compute PageRank
        try:
            pagerank = nx.pagerank(
                G,
                alpha=0.85,  # Standard damping factor
                max_iter=100,
                tol=1e-6
            )

            # Store importance scores
            self.importance = pagerank

            logger.info(
                f"Computed importance for {len(self.nodes)} symbols "
                f"with {len(self.edges)} references"
            )

            return self.importance

        except Exception as e:
            logger.error(f"Failed to compute PageRank: {e}")
            # Fallback: assign equal importance to all
            fallback = {node: 1.0 / len(self.nodes) for node in self.nodes.keys()}
            self.importance = fallback
            return fallback

    def get_top_symbols(self, n: int = 10) -> List[Symbol]:
        """Get top N most important symbols.

        Returns symbols sorted by importance score in descending order.

        Args:
            n: Number of top symbols to return

        Returns:
            List of Symbol objects, sorted by importance (highest first)

        Example:
            >>> graph = DependencyGraph()
            >>> # ... build graph ...
            >>> graph.compute_importance()
            >>> top_10 = graph.get_top_symbols(n=10)
            >>> for symbol in top_10:
            ...     print(f"{symbol.name}: {graph.importance[symbol_id]}")
        """
        if not self.importance:
            logger.warning("Importance not computed yet, computing now...")
            self.compute_importance()

        # Sort symbol IDs by importance score
        sorted_ids = sorted(
            self.importance.items(),
            key=lambda x: x[1],
            reverse=True
        )[:n]

        # Return Symbol objects
        top_symbols = [self.nodes[symbol_id] for symbol_id, _ in sorted_ids]

        logger.debug(f"Retrieved top {len(top_symbols)} symbols")
        return top_symbols

    def get_symbol_importance(self, symbol: Symbol) -> float:
        """Get importance score for a specific symbol.

        Args:
            symbol: Symbol object

        Returns:
            Importance score (0.0 to 1.0), or 0.0 if not found

        Example:
            >>> score = graph.get_symbol_importance(symbol)
            >>> print(f"Importance: {score:.4f}")
        """
        symbol_id = self._get_symbol_id(symbol)
        return self.importance.get(symbol_id, 0.0)

    def get_symbol_references(self, symbol: Symbol) -> List[str]:
        """Get all symbols that this symbol references.

        Args:
            symbol: Symbol object

        Returns:
            List of symbol IDs that this symbol references

        Example:
            >>> refs = graph.get_symbol_references(login_symbol)
            >>> print(refs)
            ['auth.py:verify_credentials', 'auth.py:generate_token']
        """
        symbol_id = self._get_symbol_id(symbol)
        return [to_id for from_id, to_id in self.edges if from_id == symbol_id]

    def get_symbol_referenced_by(self, symbol: Symbol) -> List[str]:
        """Get all symbols that reference this symbol.

        Args:
            symbol: Symbol object

        Returns:
            List of symbol IDs that reference this symbol

        Example:
            >>> callers = graph.get_symbol_referenced_by(verify_symbol)
            >>> print(callers)
            ['auth.py:login', 'auth.py:refresh_token']
        """
        symbol_id = self._get_symbol_id(symbol)
        return [from_id for from_id, to_id in self.edges if to_id == symbol_id]

    def get_stats(self) -> Dict[str, int]:
        """Get statistics about the dependency graph.

        Returns:
            Dictionary with graph statistics

        Example:
            >>> stats = graph.get_stats()
            >>> print(stats)
            {'nodes': 42, 'edges': 128, 'isolated': 3}
        """
        # Count isolated nodes (no incoming or outgoing edges)
        connected_nodes = set()
        for from_id, to_id in self.edges:
            connected_nodes.add(from_id)
            connected_nodes.add(to_id)

        isolated = len(self.nodes) - len(connected_nodes)

        return {
            'nodes': len(self.nodes),
            'edges': len(self.edges),
            'isolated': isolated
        }

    def _get_symbol_id(self, symbol: Symbol) -> str:
        """Generate unique ID for a symbol.

        Format: "{file}:{name}"

        Args:
            symbol: Symbol object

        Returns:
            Unique symbol ID string

        Example:
            >>> id = graph._get_symbol_id(symbol)
            >>> print(id)
            'app/auth.py:login'
        """
        return f"{symbol.file}:{symbol.name}"

    def export_graphviz(self, output_path: str, top_n: Optional[int] = None) -> None:
        """Export graph to GraphViz DOT format for visualization.

        Args:
            output_path: Path to save DOT file
            top_n: If specified, only export top N important symbols

        Example:
            >>> graph.export_graphviz("graph.dot", top_n=20)
            >>> # Then: dot -Tpng graph.dot -o graph.png
        """
        try:
            G = nx.DiGraph()

            # Select symbols to include
            if top_n:
                top_symbols = self.get_top_symbols(n=top_n)
                symbol_ids = {self._get_symbol_id(s) for s in top_symbols}
            else:
                symbol_ids = set(self.nodes.keys())

            # Add nodes with labels
            for symbol_id in symbol_ids:
                symbol = self.nodes[symbol_id]
                label = f"{symbol.name}\\n({symbol.type})"
                G.add_node(symbol_id, label=label)

            # Add edges (only between included nodes)
            for from_id, to_id in self.edges:
                if from_id in symbol_ids and to_id in symbol_ids:
                    G.add_edge(from_id, to_id)

            # Write DOT file
            nx.drawing.nx_pydot.write_dot(G, output_path)
            logger.info(f"Exported graph to: {output_path}")

        except Exception as e:
            logger.error(f"Failed to export GraphViz: {e}")


# Convenience function for simple usage
def build_dependency_graph(symbols: List[Symbol]) -> DependencyGraph:
    """Build a dependency graph from a list of symbols.

    This is a convenience function for simple use cases. It builds the graph
    but does not compute importance automatically (call compute_importance()).

    Args:
        symbols: List of Symbol objects

    Returns:
        DependencyGraph with symbols added

    Example:
        >>> from symbol_extractor import extract_symbols
        >>> symbols = extract_symbols("app.py")
        >>> graph = build_dependency_graph(symbols)
        >>> graph.compute_importance()
        >>> top = graph.get_top_symbols(10)
    """
    graph = DependencyGraph()

    for symbol in symbols:
        graph.add_symbol(symbol)

        # Add references if symbol has them
        for ref in symbol.references:
            graph.add_reference(
                graph._get_symbol_id(symbol),
                ref
            )

    return graph


if __name__ == "__main__":
    # Simple CLI for testing
    import sys

    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <file_path> [top_n]")
        print("\nBuild dependency graph from a source file")
        print("\nExample:")
        print(f"  python {sys.argv[0]} app.py 10")
        sys.exit(1)

    # Enable debug logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    file_path = sys.argv[1]
    top_n = int(sys.argv[2]) if len(sys.argv) > 2 else 10

    try:
        # Import extraction function
        from symbol_extractor import extract_symbols

        # Extract symbols from file
        print(f"\n📊 Extracting symbols from: {file_path}")
        symbols = extract_symbols(file_path)

        if not symbols:
            print(f"\n⚠️  No symbols found in: {file_path}")
            sys.exit(0)

        print(f"✅ Found {len(symbols)} symbols")

        # Build dependency graph
        print(f"\n🔗 Building dependency graph...")
        graph = build_dependency_graph(symbols)

        # Show stats
        stats = graph.get_stats()
        print(f"\nGraph Statistics:")
        print(f"  Nodes: {stats['nodes']}")
        print(f"  Edges: {stats['edges']}")
        print(f"  Isolated: {stats['isolated']}")

        # Compute importance
        print(f"\n⚡ Computing importance scores...")
        graph.compute_importance()

        # Show top N
        print(f"\n🏆 Top {top_n} Most Important Symbols:")
        top_symbols = graph.get_top_symbols(n=top_n)

        for i, symbol in enumerate(top_symbols, 1):
            score = graph.get_symbol_importance(symbol)
            refs = graph.get_symbol_referenced_by(symbol)
            print(f"\n{i}. {symbol.name} ({symbol.type})")
            print(f"   Score: {score:.6f}")
            print(f"   File: {symbol.file}:{symbol.line}")
            print(f"   Referenced by: {len(refs)} symbols")
            if symbol.signature:
                print(f"   Signature: {symbol.signature}")

    except FileNotFoundError:
        print(f"\n❌ File not found: {file_path}")
        sys.exit(1)
    except ValueError as e:
        print(f"\n❌ {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
