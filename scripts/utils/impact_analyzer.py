"""Impact Analyzer for CervellaSwarm.

Estimates risk of code modifications using dependency analysis and PageRank.
This module helps answer: "How risky is it to modify this symbol/file?"

Usage:
    from impact_analyzer import ImpactAnalyzer

    analyzer = ImpactAnalyzer("/path/to/repo")

    # Estimate impact of modifying a symbol
    result = analyzer.estimate_impact("MyClass")
    print(f"Risk: {result.risk_level} ({result.risk_score:.2f})")
    print(f"Affects {result.files_affected} files, {result.callers_count} callers")

    # Find dependencies (what this file imports)
    deps = analyzer.find_dependencies("app/auth.py")
    print(f"Depends on: {deps}")

    # Find dependents (what imports this file)
    dependents = analyzer.find_dependents("app/auth.py")
    print(f"Used by: {dependents}")

Risk Algorithm:
    Risk score is computed as: min(base + caller_factor + type_factor, 1.0)

    - base: PageRank importance (0.0-0.3)
    - caller_factor: Number of callers (0.0-0.4)
    - type_factor: Symbol type weight (0.0-0.3)

    Risk levels:
    - low (0.0-0.3): Safe to modify, few dependencies
    - medium (0.3-0.5): Moderate impact, some callers
    - high (0.5-0.7): High impact, many callers or important
    - critical (0.7-1.0): Critical component, widely used

Requirements Implemented:
    - REQ-05: estimate_impact(symbol_name) -> ImpactResult
    - REQ-06: find_dependencies(file_path) -> [files]
    - REQ-07: find_dependents(file_path) -> [files]
    - REQ-08: Risk score algorithm with PageRank + caller count + type weight

Author: Cervella Backend
Version: 1.0.0
Date: 2026-01-19
"""

__version__ = "1.0.0"
__version_date__ = "2026-01-19"
__changelog__ = """
v1.0.0 (2026-01-19) - W3 Day 2 (REQ-05 to REQ-08)
    - Initial implementation of ImpactAnalyzer class
    - Implemented estimate_impact() for risk assessment (REQ-05)
    - Implemented find_dependencies() for file imports (REQ-06)
    - Implemented find_dependents() for reverse lookup (REQ-07)
    - Implemented _calculate_risk_score() with PageRank + callers (REQ-08)
    - Risk levels: low, medium, high, critical
    - Graceful degradation: returns None/[] on errors
    - Uses SemanticSearch (reuses existing index)
    - Logging for debugging and monitoring
"""

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set

from semantic_search import SemanticSearch

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class ImpactResult:
    """Result of impact analysis for a symbol.

    Attributes:
        symbol_name: Name of the analyzed symbol
        risk_score: Overall risk score (0.0 = safe, 1.0 = high risk)
        risk_level: Human-readable risk level ("low", "medium", "high", "critical")
        files_affected: Number of files that would be affected by changes
        callers_count: Number of symbols that call/use this symbol
        importance_score: PageRank importance score (0.0-1.0)
        reasons: List of reasons explaining the risk score
    """

    symbol_name: str
    risk_score: float
    risk_level: str
    files_affected: int
    callers_count: int
    importance_score: float
    reasons: List[str]

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"<ImpactResult '{self.symbol_name}': "
            f"{self.risk_level.upper()} ({self.risk_score:.2f}) - "
            f"{self.callers_count} callers, {self.files_affected} files>"
        )


class ImpactAnalyzer:
    """Analyze impact of code modifications using dependency analysis.

    This class uses SemanticSearch to build a symbol index and compute
    risk scores for code changes. It helps answer:
    - How risky is it to modify this symbol?
    - What files will be affected?
    - What code depends on this file?

    Attributes:
        search: SemanticSearch instance with built index
        repo_root: Absolute path to repository root
    """

    def __init__(self, repo_root: str):
        """Initialize impact analyzer with repository root.

        Builds semantic index by scanning all Python, TypeScript, and JavaScript
        files in the repository. This may take a few seconds for large repos.

        Args:
            repo_root: Path to repository root directory

        Raises:
            ValueError: If repo_root doesn't exist or is not a directory

        Example:
            >>> analyzer = ImpactAnalyzer("/path/to/repo")
            >>> # Index is built automatically
        """
        self.repo_root = Path(repo_root).resolve()

        if not self.repo_root.exists():
            raise ValueError(f"Repository root does not exist: {repo_root}")
        if not self.repo_root.is_dir():
            raise ValueError(f"Repository root is not a directory: {repo_root}")

        logger.info(f"Initializing ImpactAnalyzer for: {self.repo_root}")

        # Initialize semantic search (this builds the index)
        self.search = SemanticSearch(str(self.repo_root))

        logger.info("ImpactAnalyzer initialized")

    def estimate_impact(self, symbol_name: str) -> Optional[ImpactResult]:
        """Estimate impact of modifying a symbol (REQ-05).

        Analyzes the symbol's dependencies, callers, and importance to compute
        a risk score. Higher score = higher risk of breaking things if modified.

        Args:
            symbol_name: Name of symbol to analyze (e.g., "MyClass", "login")

        Returns:
            ImpactResult with risk score and details, or None if symbol not found

        Example:
            >>> result = analyzer.estimate_impact("UserService")
            >>> if result:
            ...     print(f"Risk: {result.risk_level}")
            ...     print(f"Reasons: {result.reasons}")
            ... else:
            ...     print("Symbol not found")
        """
        logger.debug(f"Estimating impact for: {symbol_name}")

        # Get symbol info
        symbol = self.search.get_symbol_info(symbol_name)
        if not symbol:
            logger.debug(f"Symbol not found: {symbol_name}")
            return None

        # Get callers (who uses this symbol)
        callers = self.search.find_callers(symbol_name)
        callers_count = len(callers)

        # Get affected files (unique files where callers are)
        affected_files = set(file_path for file_path, _, _ in callers)
        # Also include the file where symbol is defined
        affected_files.add(symbol.file)
        files_affected = len(affected_files)

        # Get importance score from PageRank
        importance_score = self.search.graph.get_symbol_importance(symbol)

        # Calculate risk score (REQ-08)
        risk_score = self._calculate_risk_score(symbol, callers_count, importance_score)

        # Determine risk level
        risk_level = self._get_risk_level(risk_score)

        # Generate reasons for this risk score
        reasons = self._generate_reasons(
            symbol, callers_count, files_affected, importance_score, risk_score
        )

        result = ImpactResult(
            symbol_name=symbol_name,
            risk_score=risk_score,
            risk_level=risk_level,
            files_affected=files_affected,
            callers_count=callers_count,
            importance_score=importance_score,
            reasons=reasons,
        )

        logger.debug(
            f"Impact for '{symbol_name}': {risk_level.upper()} "
            f"({risk_score:.2f}) - {callers_count} callers, {files_affected} files"
        )

        return result

    def find_dependencies(self, file_path: str) -> List[str]:
        """Find all files that this file depends on (REQ-06).

        Analyzes imports and references to find which files this file uses.
        Returns absolute file paths.

        Args:
            file_path: Path to file to analyze (relative or absolute)

        Returns:
            List of absolute file paths that this file imports/uses.
            Returns [] if file not found or has no dependencies.

        Example:
            >>> deps = analyzer.find_dependencies("app/auth.py")
            >>> for dep in deps:
            ...     print(f"Depends on: {dep}")
        """
        # Normalize path to absolute
        abs_path = str(Path(file_path).resolve())
        logger.debug(f"Finding dependencies for: {abs_path}")

        # Get all symbols defined in this file
        try:
            symbols = self.search.extractor.extract_symbols(abs_path)
        except Exception as e:
            logger.warning(f"Failed to extract symbols from {abs_path}: {e}")
            return []

        if not symbols:
            logger.debug(f"No symbols found in {abs_path}")
            return []

        # Collect all references from all symbols in this file
        all_references = set()
        for symbol in symbols:
            all_references.update(symbol.references)

        # Map reference names to files
        dependencies = set()
        for ref_name in all_references:
            # Find where this reference is defined
            location = self.search.find_symbol(ref_name)
            if location:
                ref_file, _ = location
                # Only include if it's a different file
                if ref_file != abs_path:
                    dependencies.add(ref_file)

        result = sorted(dependencies)
        logger.debug(f"Found {len(result)} dependencies for {abs_path}")
        return result

    def find_dependents(self, file_path: str) -> List[str]:
        """Find all files that depend on this file (REQ-07).

        Analyzes reverse dependencies to find which files import/use symbols
        from this file. Returns absolute file paths.

        Args:
            file_path: Path to file to analyze (relative or absolute)

        Returns:
            List of absolute file paths that import/use this file.
            Returns [] if file not found or has no dependents.

        Example:
            >>> dependents = analyzer.find_dependents("app/utils.py")
            >>> for dep in dependents:
            ...     print(f"Used by: {dep}")
        """
        # Normalize path to absolute
        abs_path = str(Path(file_path).resolve())
        logger.debug(f"Finding dependents for: {abs_path}")

        # Get all symbols defined in this file
        try:
            symbols = self.search.extractor.extract_symbols(abs_path)
        except Exception as e:
            logger.warning(f"Failed to extract symbols from {abs_path}: {e}")
            return []

        if not symbols:
            logger.debug(f"No symbols found in {abs_path}")
            return []

        # For each symbol, find who calls it
        dependents = set()
        for symbol in symbols:
            callers = self.search.find_callers(symbol.name)
            for caller_file, _, _ in callers:
                # Only include if it's a different file
                if caller_file != abs_path:
                    dependents.add(caller_file)

        result = sorted(dependents)
        logger.debug(f"Found {len(result)} dependents for {abs_path}")
        return result

    def _calculate_risk_score(
        self, symbol, callers_count: int, importance_score: float
    ) -> float:
        """Calculate risk score for a symbol (REQ-08).

        Risk formula: min(base + caller_factor + type_factor, 1.0)

        - base: PageRank importance (0.0-0.3)
        - caller_factor: Number of callers (0.0-0.4)
        - type_factor: Symbol type weight (0.0-0.3)

        Args:
            symbol: Symbol object
            callers_count: Number of callers
            importance_score: PageRank importance (0.0-1.0)

        Returns:
            Risk score (0.0-1.0)
        """
        # Base score from PageRank (0.0-0.3)
        # Scale PageRank (typically 0.0-0.1) to 0.0-0.3
        base = min(importance_score * 10, 0.3)

        # Caller factor (0.0-0.4)
        # 20+ callers = max score
        caller_factor = min(callers_count / 20, 0.4)

        # Type factor (0.0-0.3)
        # Classes are riskier than functions (more impact if changed)
        type_weights = {
            "class": 0.3,
            "interface": 0.25,
            "function": 0.2,
            "type": 0.1,
        }
        type_factor = type_weights.get(symbol.type, 0.15)

        risk_score = min(base + caller_factor + type_factor, 1.0)

        logger.debug(
            f"Risk calculation for '{symbol.name}': "
            f"base={base:.3f}, caller_factor={caller_factor:.3f}, "
            f"type_factor={type_factor:.3f} -> {risk_score:.3f}"
        )

        return risk_score

    def _get_risk_level(self, risk_score: float) -> str:
        """Convert risk score to human-readable level.

        Args:
            risk_score: Risk score (0.0-1.0)

        Returns:
            Risk level string ("low", "medium", "high", "critical")
        """
        if risk_score < 0.3:
            return "low"
        elif risk_score < 0.5:
            return "medium"
        elif risk_score < 0.7:
            return "high"
        else:
            return "critical"

    def _generate_reasons(
        self,
        symbol,
        callers_count: int,
        files_affected: int,
        importance_score: float,
        risk_score: float,
    ) -> List[str]:
        """Generate human-readable reasons for risk score.

        Args:
            symbol: Symbol object
            callers_count: Number of callers
            files_affected: Number of affected files
            importance_score: PageRank importance
            risk_score: Computed risk score

        Returns:
            List of reason strings
        """
        reasons = []

        # Caller-based reasons
        if callers_count == 0:
            reasons.append("No callers found - safe to modify")
        elif callers_count <= 3:
            reasons.append(f"Only {callers_count} callers - low impact")
        elif callers_count <= 10:
            reasons.append(f"{callers_count} callers - moderate impact")
        elif callers_count <= 20:
            reasons.append(f"{callers_count} callers - high impact")
        else:
            reasons.append(f"{callers_count} callers - critical component")

        # File impact reasons
        if files_affected == 1:
            reasons.append("Only used in 1 file - localized changes")
        elif files_affected <= 3:
            reasons.append(f"Used in {files_affected} files - limited scope")
        elif files_affected <= 10:
            reasons.append(f"Used in {files_affected} files - moderate scope")
        else:
            reasons.append(f"Used in {files_affected} files - wide scope")

        # Importance-based reasons
        if importance_score > 0.05:
            reasons.append(
                f"High PageRank importance ({importance_score:.4f}) - central to codebase"
            )
        elif importance_score > 0.02:
            reasons.append(
                f"Moderate PageRank importance ({importance_score:.4f})"
            )

        # Type-based reasons
        if symbol.type == "class":
            reasons.append("Class type - changes may affect multiple methods")
        elif symbol.type == "interface":
            reasons.append("Interface type - changes may break implementations")

        # Overall assessment
        if risk_score >= 0.7:
            reasons.append("CRITICAL: Carefully review all changes and test thoroughly")
        elif risk_score >= 0.5:
            reasons.append("HIGH RISK: Review callers and add tests before modifying")
        elif risk_score >= 0.3:
            reasons.append("MODERATE RISK: Check callers and test changes")
        else:
            reasons.append("LOW RISK: Safe to modify with standard testing")

        return reasons

    def get_stats(self) -> Dict:
        """Get statistics about the analyzed codebase.

        Returns:
            Dictionary with statistics from SemanticSearch

        Example:
            >>> stats = analyzer.get_stats()
            >>> print(f"Total symbols: {stats['total_symbols']}")
        """
        return self.search.get_stats()


# Convenience function for one-off analysis
def estimate_symbol_impact(
    repo_root: str, symbol_name: str
) -> Optional[ImpactResult]:
    """Estimate impact of modifying a symbol (convenience function).

    Creates an ImpactAnalyzer instance, performs the analysis, and returns result.
    For repeated analysis, create an ImpactAnalyzer instance to avoid rebuilding
    the index every time.

    Args:
        repo_root: Path to repository root
        symbol_name: Symbol name to analyze

    Returns:
        ImpactResult if found, None otherwise

    Example:
        >>> from impact_analyzer import estimate_symbol_impact
        >>> result = estimate_symbol_impact("/path/to/repo", "UserService")
        >>> if result:
        ...     print(f"Risk: {result.risk_level} ({result.risk_score:.2f})")
    """
    analyzer = ImpactAnalyzer(repo_root)
    return analyzer.estimate_impact(symbol_name)


if __name__ == "__main__":
    # Simple CLI for testing
    import sys

    if len(sys.argv) < 3:
        print(f"Usage: python {sys.argv[0]} <repo_root> <symbol_name>")
        print("\nEstimate impact of modifying a symbol")
        print("\nExample:")
        print(f"  python {sys.argv[0]} /path/to/repo UserService")
        sys.exit(1)

    # Enable logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    repo_root = sys.argv[1]
    symbol_name = sys.argv[2]

    try:
        # Initialize analyzer
        print(f"\n🔍 Initializing impact analyzer for: {repo_root}")
        analyzer = ImpactAnalyzer(repo_root)

        # Show stats
        stats = analyzer.get_stats()
        print(f"\n📊 Repository Statistics:")
        print(f"   Total symbols: {stats['total_symbols']}")
        print(f"   Unique names: {stats['unique_names']}")
        print(f"   Graph nodes: {stats['graph_nodes']}")
        print(f"   Graph edges: {stats['graph_edges']}")

        # Analyze symbol
        print(f"\n⚡ Analyzing impact: {symbol_name}")
        result = analyzer.estimate_impact(symbol_name)

        if result:
            print(f"\n{'='*60}")
            print(f"IMPACT ANALYSIS: {result.symbol_name}")
            print(f"{'='*60}")
            print(f"\n🎯 Risk Level: {result.risk_level.upper()}")
            print(f"📊 Risk Score: {result.risk_score:.2f} / 1.00")
            print(f"\n📈 Impact Metrics:")
            print(f"   Callers: {result.callers_count}")
            print(f"   Files affected: {result.files_affected}")
            print(f"   PageRank importance: {result.importance_score:.6f}")
            print(f"\n💡 Reasons:")
            for i, reason in enumerate(result.reasons, 1):
                print(f"   {i}. {reason}")
            print(f"\n{'='*60}")

            # Show callers if any
            if result.callers_count > 0:
                callers = analyzer.search.find_callers(symbol_name)
                print(f"\n📞 Callers ({len(callers)}):")
                for file_path, line_number, caller_name in callers[:10]:
                    print(f"   {caller_name} at {file_path}:{line_number}")
                if len(callers) > 10:
                    print(f"   ... and {len(callers) - 10} more")
        else:
            print(f"\n❌ Symbol not found: {symbol_name}")

    except ValueError as e:
        print(f"\n❌ {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
