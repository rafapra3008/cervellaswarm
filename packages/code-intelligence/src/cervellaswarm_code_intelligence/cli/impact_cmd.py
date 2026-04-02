#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors
"""CLI entry point for Impact Analyzer.

Extracted from impact_analyzer.py (S342) to keep library under 500 lines.
"""

import sys
import logging

from ..impact_analyzer import ImpactAnalyzer


def main():
    if len(sys.argv) < 3:
        print(f"Usage: python {sys.argv[0]} <repo_root> <symbol_name>")
        print("\nEstimate impact of modifying a symbol")
        print("\nExample:")
        print(f"  python {sys.argv[0]} /path/to/repo UserService")
        sys.exit(1)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    repo_root = sys.argv[1]
    symbol_name = sys.argv[2]

    try:
        print(f"\nInitializing impact analyzer for: {repo_root}")
        analyzer = ImpactAnalyzer(repo_root)

        stats = analyzer.get_stats()
        print("\nRepository Statistics:")
        print(f"   Total symbols: {stats['total_symbols']}")
        print(f"   Unique names: {stats['unique_names']}")
        print(f"   Graph nodes: {stats['graph_nodes']}")
        print(f"   Graph edges: {stats['graph_edges']}")

        print(f"\nAnalyzing impact: {symbol_name}")
        result = analyzer.estimate_impact(symbol_name)

        if result:
            print(f"\n{'='*60}")
            print(f"IMPACT ANALYSIS: {result.symbol_name}")
            print(f"{'='*60}")
            print(f"\nRisk Level: {result.risk_level.upper()}")
            print(f"Risk Score: {result.risk_score:.2f} / 1.00")
            print("\nImpact Metrics:")
            print(f"   Callers: {result.callers_count}")
            print(f"   Files affected: {result.files_affected}")
            print(f"   PageRank importance: {result.importance_score:.6f}")
            print("\nReasons:")
            for i, reason in enumerate(result.reasons, 1):
                print(f"   {i}. {reason}")
            print(f"\n{'='*60}")

            if result.callers_count > 0:
                callers = analyzer.search.find_callers(symbol_name)
                print(f"\nCallers ({len(callers)}):")
                for file_path, line_number, caller_name in callers[:10]:
                    print(f"   {caller_name} at {file_path}:{line_number}")
                if len(callers) > 10:
                    print(f"   ... and {len(callers) - 10} more")
        else:
            print(f"\nSymbol not found: {symbol_name}")

    except ValueError as e:
        print(f"\n{e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
