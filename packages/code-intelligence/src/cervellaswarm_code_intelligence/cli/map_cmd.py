#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors
"""CLI entry point for Repository Mapper.

Extracted from repo_mapper.py (S342) to keep library under 500 lines.
"""

import sys
import logging
import argparse

from ..repo_mapper import RepoMapper


def main():
    """CLI entry point for repository mapper."""
    parser = argparse.ArgumentParser(
        description="Generate repository map using tree-sitter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/utils/repo_mapper.py --repo-path .
  python3 scripts/utils/repo_mapper.py --repo-path . --budget 3000
  python3 scripts/utils/repo_mapper.py --repo-path . --output repo_map.md
  python3 scripts/utils/repo_mapper.py --repo-path . --filter "**/*.py"
        """
    )

    parser.add_argument(
        '--repo-path', type=str, default='.',
        help='Path to repository root (default: current directory)'
    )
    parser.add_argument(
        '--budget', type=int, default=2000,
        help='Token budget for map (default: 2000)'
    )
    parser.add_argument(
        '--filter', type=str, default=None,
        help='Glob pattern to filter files (e.g., "**/*.py")'
    )
    parser.add_argument(
        '--output', type=str, default=None,
        help='Output file path (if not specified, prints to stdout)'
    )
    parser.add_argument(
        '--verbose', action='store_true',
        help='Enable verbose logging'
    )
    parser.add_argument(
        '--stats', action='store_true',
        help='Show statistics after generating map'
    )

    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    try:
        print(f"\nGenerating repository map for: {args.repo_path}")
        print(f"Token budget: {args.budget}")
        if args.filter:
            print(f"Filter pattern: {args.filter}")
        print()

        mapper = RepoMapper(args.repo_path)
        map_text = mapper.build_map(
            token_budget=args.budget,
            filter_pattern=args.filter
        )

        if args.output:
            with open(args.output, 'w') as f:
                f.write(map_text)
            print(f"Map saved to: {args.output}")
        else:
            print(map_text)

        if args.stats:
            stats = mapper.get_stats()
            print(f"\nStatistics:")
            print(f"  Total symbols: {stats['symbols']}")
            print(f"  Graph nodes: {stats['graph_nodes']}")
            print(f"  Graph edges: {stats['graph_edges']}")
            print(f"  Isolated symbols: {stats['graph_isolated']}")
            actual_tokens = mapper._estimate_tokens(map_text)
            print(f"  Estimated tokens: {actual_tokens} / {args.budget}")

    except FileNotFoundError as e:
        print(f"\n{e}")
        return 1
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
