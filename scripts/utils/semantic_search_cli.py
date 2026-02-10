#!/usr/bin/env python3
"""CLI entry point for Semantic Search API.

Extracted from semantic_search.py (S342) to keep library under 500 lines.
"""

import sys
import logging
from pathlib import Path

# Ensure local imports work when run directly
_dir = Path(__file__).parent
if str(_dir) not in sys.path:
    sys.path.insert(0, str(_dir))

from semantic_search import SemanticSearch


def main():
    if len(sys.argv) < 3:
        print(f"Usage: python {sys.argv[0]} <repo_root> <symbol_name> [command]")
        print("\nCommands:")
        print("  find      - Find symbol definition (default)")
        print("  callers   - Find all callers")
        print("  callees   - Find all callees")
        print("  refs      - Find all references")
        print("  info      - Show detailed symbol info")
        print("  stats     - Show repository statistics")
        print("\nExample:")
        print(f"  python {sys.argv[0]} /path/to/repo MyClass")
        print(f"  python {sys.argv[0]} /path/to/repo login callers")
        sys.exit(1)

    # Enable logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    repo_root = sys.argv[1]
    symbol_name = sys.argv[2]
    command = sys.argv[3] if len(sys.argv) > 3 else "find"

    try:
        print(f"\nInitializing semantic search for: {repo_root}")
        search = SemanticSearch(repo_root)

        stats = search.get_stats()
        print(f"\nRepository Statistics:")
        print(f"   Total symbols: {stats['total_symbols']}")
        print(f"   Unique names: {stats['unique_names']}")
        print(f"   Graph nodes: {stats['graph_nodes']}")
        print(f"   Graph edges: {stats['graph_edges']}")

        if command == "find":
            print(f"\nFinding symbol: {symbol_name}")
            location = search.find_symbol(symbol_name)
            if location:
                file_path, line_number = location
                print(f"\nFound at: {file_path}:{line_number}")
            else:
                print(f"\nSymbol not found: {symbol_name}")

        elif command == "callers":
            print(f"\nFinding callers of: {symbol_name}")
            callers = search.find_callers(symbol_name)
            if callers:
                print(f"\nFound {len(callers)} callers:")
                for file_path, line_number, caller_name in callers:
                    print(f"   {caller_name} at {file_path}:{line_number}")
            else:
                print(f"\nNo callers found for: {symbol_name}")

        elif command == "callees":
            print(f"\nFinding callees of: {symbol_name}")
            callees = search.find_callees(symbol_name)
            if callees:
                print(f"\nFound {len(callees)} callees:")
                for callee in callees:
                    print(f"   {callee}")
            else:
                print(f"\nNo callees found for: {symbol_name}")

        elif command == "refs":
            print(f"\nFinding references to: {symbol_name}")
            refs = search.find_references(symbol_name)
            if refs:
                print(f"\nFound {len(refs)} references:")
                for file_path, line_number in refs:
                    print(f"   {file_path}:{line_number}")
            else:
                print(f"\nNo references found for: {symbol_name}")

        elif command == "info":
            print(f"\nSymbol info: {symbol_name}")
            info = search.get_symbol_info(symbol_name)
            if info:
                print(f"\nSymbol found:")
                print(f"   Name: {info.name}")
                print(f"   Type: {info.type}")
                print(f"   File: {info.file}:{info.line}")
                print(f"   Signature: {info.signature}")
                if info.docstring:
                    print(f"   Docstring: {info.docstring[:100]}...")
                print(f"   References: {len(info.references)} symbols")
                importance = search.graph.get_symbol_importance(info)
                print(f"   Importance: {importance:.6f}")
            else:
                print(f"\nSymbol not found: {symbol_name}")

        elif command == "stats":
            pass  # Already printed above

        else:
            print(f"\nUnknown command: {command}")
            sys.exit(1)

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
