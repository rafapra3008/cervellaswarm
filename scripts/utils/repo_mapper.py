"""Repository Mapper - Orchestrate tree-sitter components to map repositories.

This module combines TreesitterParser, SymbolExtractor, and DependencyGraph
to generate concise repository maps within a specified token budget. It's
designed for context-aware AI assistants that need repository overviews.

Usage:
    from repo_mapper import RepoMapper

    mapper = RepoMapper(repo_path=".")
    map_text = mapper.build_map(token_budget=2000)
    print(map_text)

CLI Usage:
    # Generate map for current directory
    python3 scripts/utils/repo_mapper.py --repo-path . --budget 2000

    # Save to file
    python3 scripts/utils/repo_mapper.py --repo-path . --budget 2000 --output map.md

    # Filter specific files
    python3 scripts/utils/repo_mapper.py --repo-path . --filter "**/*.py"

Features:
    - Auto-discovers source files in repository
    - Extracts symbols (functions, classes, interfaces)
    - Computes importance via PageRank
    - Fits top symbols within token budget
    - Formats readable markdown output

Author: Cervella Backend
Version: 1.0.0
Date: 2026-01-19
"""

__version__ = "1.0.0"
__version_date__ = "2026-01-19"

import argparse
import logging
from pathlib import Path
from typing import Dict, List, Optional

# Handle imports for both direct execution and module import
try:
    from dependency_graph import DependencyGraph
    from symbol_extractor import Symbol, SymbolExtractor
    from treesitter_parser import TreesitterParser
except ImportError:
    from scripts.utils.dependency_graph import DependencyGraph
    from scripts.utils.symbol_extractor import Symbol, SymbolExtractor
    from scripts.utils.treesitter_parser import TreesitterParser

# Configure logging
logger = logging.getLogger(__name__)


class RepoMapper:
    """Generate repository maps using tree-sitter and PageRank.

    This class orchestrates the complete repository mapping pipeline:
    1. Discover source files in repository
    2. Parse files and extract symbols
    3. Build dependency graph
    4. Compute importance scores
    5. Select top symbols that fit token budget
    6. Format as readable markdown map

    Attributes:
        repo_path: Root path of repository to map
        parser: TreesitterParser for AST parsing
        extractor: SymbolExtractor for symbol extraction
        graph: DependencyGraph for importance computation
    """

    def __init__(self, repo_path: str):
        """Initialize repository mapper.

        Args:
            repo_path: Absolute or relative path to repository root

        Example:
            >>> mapper = RepoMapper(repo_path=".")
            >>> mapper = RepoMapper(repo_path="/path/to/CervellaSwarm")
        """
        self.repo_path = Path(repo_path).resolve()
        self.parser = TreesitterParser()
        self.extractor = SymbolExtractor(self.parser)
        self.graph = DependencyGraph()

        logger.debug(f"RepoMapper initialized for: {self.repo_path}")

        if not self.repo_path.exists():
            raise FileNotFoundError(f"Repository path not found: {self.repo_path}")

    def build_map(
        self,
        relevant_files: Optional[List[str]] = None,
        token_budget: int = 2000,
        filter_pattern: Optional[str] = None
    ) -> str:
        """Build repository map within token budget.

        This is the main entry point. It orchestrates the complete pipeline:
        1. Discover files (or use provided list)
        2. Extract symbols from all files
        3. Build dependency graph
        4. Compute importance scores
        5. Select top symbols that fit budget
        6. Generate formatted markdown map

        Args:
            relevant_files: Optional list of file paths to map. If None, auto-discovers.
            token_budget: Maximum tokens to use for the map (default: 2000)
            filter_pattern: Optional glob pattern to filter files (e.g., "**/*.py")

        Returns:
            Markdown-formatted repository map string

        Example:
            >>> mapper = RepoMapper(".")
            >>> map_text = mapper.build_map(token_budget=2000)
            >>> print(map_text)
            # REPOSITORY MAP
            ...
        """
        logger.info(f"Building repository map with budget: {token_budget} tokens")

        # 1. Discover source files
        if relevant_files is None:
            logger.debug("Auto-discovering source files...")
            relevant_files = self._discover_source_files(filter_pattern=filter_pattern)

        if not relevant_files:
            logger.warning("No source files found")
            return "# REPOSITORY MAP\n\n*No source files found*\n"

        logger.info(f"Found {len(relevant_files)} source files")

        # 2. Extract symbols from all files
        logger.debug("Extracting symbols from files...")
        all_symbols = []
        for file_path in relevant_files:
            try:
                symbols = self.extractor.extract_symbols(str(file_path))
                all_symbols.extend(symbols)
            except Exception as e:
                logger.warning(f"Failed to extract symbols from {file_path}: {e}")
                continue

        if not all_symbols:
            logger.warning("No symbols extracted")
            return "# REPOSITORY MAP\n\n*No symbols found in source files*\n"

        logger.info(f"Extracted {len(all_symbols)} symbols total")

        # 3. Build dependency graph
        logger.debug("Building dependency graph...")
        for symbol in all_symbols:
            self.graph.add_symbol(symbol)

            # Add references if available (NOTE: reference extraction is W2.5 enhancement)
            for ref in symbol.references:
                self.graph.add_reference(
                    self.graph._get_symbol_id(symbol),
                    ref
                )

        # 4. Compute importance
        logger.debug("Computing importance scores...")
        self.graph.compute_importance()

        # 5. Select symbols that fit budget
        logger.debug(f"Selecting symbols within {token_budget} token budget...")
        selected_symbols = self._fit_to_budget(all_symbols, token_budget)

        logger.info(f"Selected {len(selected_symbols)} symbols for map")

        # 6. Generate formatted map
        logger.debug("Formatting map...")
        map_text = self._format_map(selected_symbols)

        # Verify final token count
        final_tokens = self._estimate_tokens(map_text)
        logger.info(f"Generated map: {final_tokens} tokens (budget: {token_budget})")

        return map_text

    def _discover_source_files(
        self,
        filter_pattern: Optional[str] = None
    ) -> List[Path]:
        """Find all source files in repository.

        Args:
            filter_pattern: Optional glob pattern (e.g., "**/*.py")

        Returns:
            List of Path objects for source files

        Example:
            >>> files = mapper._discover_source_files()
            >>> print(len(files))
            42
        """
        # Patterns to include
        if filter_pattern:
            patterns = [filter_pattern]
        else:
            patterns = [
                "**/*.py",
                "**/*.ts",
                "**/*.tsx",
                "**/*.js",
                "**/*.jsx",
            ]

        # Directories to exclude
        exclude_dirs = {
            "node_modules",
            "__pycache__",
            ".git",
            "dist",
            "build",
            ".venv",
            "venv",
            ".eggs",
            "*.egg-info",
            ".pytest_cache",
            ".mypy_cache",
            ".tox",
            "htmlcov",
        }

        found_files = []

        for pattern in patterns:
            for file_path in self.repo_path.glob(pattern):
                # Skip if in excluded directory
                if any(excluded in file_path.parts for excluded in exclude_dirs):
                    continue

                # Skip if not a file
                if not file_path.is_file():
                    continue

                found_files.append(file_path)

        # Remove duplicates and sort
        found_files = sorted(set(found_files))

        logger.debug(f"Discovered {len(found_files)} source files")
        return found_files

    def _fit_to_budget(self, symbols: List[Symbol], budget: int) -> List[Symbol]:
        """Select symbols that fit within token budget.

        Symbols are sorted by importance (PageRank score) and added until
        the budget is reached. This ensures the most important symbols
        are included in the map.

        Args:
            symbols: List of all extracted symbols
            budget: Maximum number of tokens

        Returns:
            List of symbols that fit within budget, sorted by importance

        Example:
            >>> selected = mapper._fit_to_budget(all_symbols, budget=2000)
            >>> print(len(selected))
            38
        """
        # Sort symbols by importance (highest first)
        sorted_symbols = sorted(
            symbols,
            key=lambda s: self.graph.get_symbol_importance(s),
            reverse=True
        )

        # Add symbols until budget is reached
        selected = []
        current_tokens = 0

        # Reserve tokens for header and file grouping (approx 200 tokens)
        header_overhead = 200
        available_budget = budget - header_overhead

        for symbol in sorted_symbols:
            # Estimate tokens for this symbol's signature
            symbol_text = f"{symbol.signature}\n"
            symbol_tokens = self._estimate_tokens(symbol_text)

            # Check if adding this symbol exceeds budget
            if current_tokens + symbol_tokens > available_budget:
                logger.debug(
                    f"Budget reached: {current_tokens} tokens "
                    f"(skipping {len(sorted_symbols) - len(selected)} symbols)"
                )
                break

            selected.append(symbol)
            current_tokens += symbol_tokens

        return selected

    def _estimate_tokens(self, text: str) -> int:
        """Rough token estimation.

        Uses the common heuristic: 4 characters ≈ 1 token
        This is approximate but sufficient for budget management.

        Args:
            text: Text to estimate

        Returns:
            Estimated number of tokens

        Example:
            >>> tokens = mapper._estimate_tokens("def login(): pass")
            >>> print(tokens)
            5
        """
        return len(text) // 4

    def _format_map(self, symbols: List[Symbol]) -> str:
        """Format symbols into readable markdown map.

        Groups symbols by file and shows only signatures (no implementations).

        Args:
            symbols: List of symbols to include in map

        Returns:
            Markdown-formatted map string

        Example:
            >>> map_text = mapper._format_map(selected_symbols)
            >>> print(map_text)
            # REPOSITORY MAP

            ## app/auth.py

            def login(username: str) -> bool
            class AuthService
        """
        if not symbols:
            return "# REPOSITORY MAP\n\n*No symbols selected*\n"

        # Group symbols by file (use relative paths)
        by_file: Dict[str, List[Symbol]] = {}
        for symbol in symbols:
            # Convert to relative path for readability
            try:
                file_path = str(Path(symbol.file).relative_to(self.repo_path))
            except ValueError:
                # If file is outside repo, use absolute path
                file_path = symbol.file

            if file_path not in by_file:
                by_file[file_path] = []
            by_file[file_path].append(symbol)

        # Build markdown output
        lines = ["# REPOSITORY MAP", ""]

        # Sort files alphabetically
        for file_path in sorted(by_file.keys()):
            file_symbols = by_file[file_path]

            # File header
            lines.append(f"## {file_path}")
            lines.append("")

            # Sort symbols by line number
            file_symbols.sort(key=lambda s: s.line)

            # Add symbol signatures
            for symbol in file_symbols:
                lines.append(symbol.signature)

            lines.append("")  # Blank line between files

        return "\n".join(lines)

    def get_stats(self) -> Dict[str, int]:
        """Get statistics about the repository map.

        Returns:
            Dictionary with mapping statistics

        Example:
            >>> stats = mapper.get_stats()
            >>> print(stats)
            {'symbols': 156, 'files': 12, 'graph_nodes': 156, 'graph_edges': 423}
        """
        graph_stats = self.graph.get_stats()

        return {
            'symbols': graph_stats['nodes'],
            'graph_nodes': graph_stats['nodes'],
            'graph_edges': graph_stats['edges'],
            'graph_isolated': graph_stats['isolated'],
        }


# Convenience function for simple usage
def generate_repo_map(
    repo_path: str,
    token_budget: int = 2000,
    filter_pattern: Optional[str] = None,
    output_file: Optional[str] = None
) -> str:
    """Generate repository map without managing a mapper instance.

    This is a convenience function for one-off map generation.

    Args:
        repo_path: Path to repository root
        token_budget: Maximum tokens for map (default: 2000)
        filter_pattern: Optional glob pattern to filter files
        output_file: Optional path to save map (if None, returns string)

    Returns:
        Generated map as string

    Example:
        >>> from repo_mapper import generate_repo_map
        >>> map_text = generate_repo_map(".", token_budget=2000)
        >>> print(map_text)
    """
    mapper = RepoMapper(repo_path)
    map_text = mapper.build_map(
        token_budget=token_budget,
        filter_pattern=filter_pattern
    )

    if output_file:
        with open(output_file, 'w') as f:
            f.write(map_text)
        logger.info(f"Saved map to: {output_file}")

    return map_text


def main():
    """CLI entry point for repository mapper."""
    parser = argparse.ArgumentParser(
        description="Generate repository map using tree-sitter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate map for current directory
  python3 scripts/utils/repo_mapper.py --repo-path .

  # Specify token budget
  python3 scripts/utils/repo_mapper.py --repo-path . --budget 3000

  # Save to file
  python3 scripts/utils/repo_mapper.py --repo-path . --output repo_map.md

  # Filter only Python files
  python3 scripts/utils/repo_mapper.py --repo-path . --filter "**/*.py"

  # Filter specific directory
  python3 scripts/utils/repo_mapper.py --repo-path . --filter "scripts/**/*.py"
        """
    )

    parser.add_argument(
        '--repo-path',
        type=str,
        default='.',
        help='Path to repository root (default: current directory)'
    )

    parser.add_argument(
        '--budget',
        type=int,
        default=2000,
        help='Token budget for map (default: 2000)'
    )

    parser.add_argument(
        '--filter',
        type=str,
        default=None,
        help='Glob pattern to filter files (e.g., "**/*.py")'
    )

    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Output file path (if not specified, prints to stdout)'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show statistics after generating map'
    )

    args = parser.parse_args()

    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    try:
        # Generate map
        print(f"\n🗺️  Generating repository map for: {args.repo_path}")
        print(f"Token budget: {args.budget}")
        if args.filter:
            print(f"Filter pattern: {args.filter}")
        print()

        mapper = RepoMapper(args.repo_path)
        map_text = mapper.build_map(
            token_budget=args.budget,
            filter_pattern=args.filter
        )

        # Output map
        if args.output:
            with open(args.output, 'w') as f:
                f.write(map_text)
            print(f"✅ Map saved to: {args.output}")
        else:
            print(map_text)

        # Show statistics if requested
        if args.stats:
            stats = mapper.get_stats()
            print(f"\n📊 Statistics:")
            print(f"  Total symbols: {stats['symbols']}")
            print(f"  Graph nodes: {stats['graph_nodes']}")
            print(f"  Graph edges: {stats['graph_edges']}")
            print(f"  Isolated symbols: {stats['graph_isolated']}")

            # Estimate actual tokens used
            actual_tokens = mapper._estimate_tokens(map_text)
            print(f"  Estimated tokens: {actual_tokens} / {args.budget}")

    except FileNotFoundError as e:
        print(f"\n❌ {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
