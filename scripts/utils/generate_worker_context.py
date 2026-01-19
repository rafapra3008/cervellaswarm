#!/usr/bin/env python3
"""Generate intelligent context for CervellaSwarm workers.

This script uses repo_mapper to generate a concise repository map
that can be injected into worker prompts. It provides workers with
understanding of the codebase structure without overwhelming context.

Usage:
    # Generate context for current directory (default 1500 tokens)
    python3 scripts/utils/generate_worker_context.py

    # Specify token budget
    python3 scripts/utils/generate_worker_context.py --budget 2000

    # Filter specific files (e.g., only Python)
    python3 scripts/utils/generate_worker_context.py --filter "**/*.py"

    # For specific project path
    python3 scripts/utils/generate_worker_context.py --repo-path /path/to/project

Output:
    Prints context string to stdout (for shell script capture)

Author: Cervella Backend
Version: 1.0.0
Date: 2026-01-19
"""

__version__ = "1.0.0"

import argparse
import sys
from pathlib import Path

# Handle imports
try:
    from repo_mapper import RepoMapper
except ImportError:
    # Running from project root
    sys.path.insert(0, str(Path(__file__).parent))
    from repo_mapper import RepoMapper


def generate_context(
    repo_path: str = ".",
    token_budget: int = 1500,
    filter_pattern: str = None,
    include_header: bool = True
) -> str:
    """Generate context string for worker prompts.

    Args:
        repo_path: Path to repository root
        token_budget: Maximum tokens for context (default: 1500)
        filter_pattern: Optional glob pattern to filter files
        include_header: Whether to include context header (default: True)

    Returns:
        Context string ready to inject into worker prompt
    """
    try:
        mapper = RepoMapper(repo_path)
        repo_map = mapper.build_map(
            token_budget=token_budget,
            filter_pattern=filter_pattern
        )

        if include_header:
            context = f"""
CONTESTO CODEBASE (auto-generato da repo_mapper):
{repo_map}
---
Usa questo contesto per capire la struttura del progetto.
I simboli sono ordinati per importanza (PageRank).
"""
        else:
            context = repo_map

        return context.strip()

    except FileNotFoundError:
        return f"[WARN] Repository path not found: {repo_path}"
    except Exception as e:
        return f"[WARN] Failed to generate context: {e}"


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate context for CervellaSwarm workers"
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
        default=1500,
        help='Token budget for context (default: 1500)'
    )

    parser.add_argument(
        '--filter',
        type=str,
        default=None,
        help='Glob pattern to filter files (e.g., "**/*.py")'
    )

    parser.add_argument(
        '--no-header',
        action='store_true',
        help='Exclude context header (raw map only)'
    )

    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress warnings (for shell script usage)'
    )

    args = parser.parse_args()

    context = generate_context(
        repo_path=args.repo_path,
        token_budget=args.budget,
        filter_pattern=args.filter,
        include_header=not args.no_header
    )

    # Output context (for shell capture)
    if context.startswith("[WARN]"):
        if not args.quiet:
            print(context, file=sys.stderr)
        sys.exit(1)  # Exit code 1 signals failure to caller
    else:
        print(context)
        sys.exit(0)


if __name__ == "__main__":
    main()
