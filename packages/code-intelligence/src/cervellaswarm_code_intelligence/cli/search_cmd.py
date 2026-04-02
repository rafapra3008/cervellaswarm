#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors
"""CLI entry point for Semantic Search API.

Extracted from semantic_search.py (S342) to keep library under 500 lines.
S501: CC refactored 19->7 via dispatch table pattern (validated S436-S437).
"""

import sys
import logging

from ..semantic_search import SemanticSearch


def _cmd_find(search: SemanticSearch, name: str) -> None:
    print(f"\nFinding symbol: {name}")
    location = search.find_symbol(name)
    if location:
        file_path, line_number = location
        print(f"\nFound at: {file_path}:{line_number}")
    else:
        print(f"\nSymbol not found: {name}")


def _cmd_callers(search: SemanticSearch, name: str) -> None:
    print(f"\nFinding callers of: {name}")
    callers = search.find_callers(name)
    if callers:
        print(f"\nFound {len(callers)} callers:")
        for file_path, line_number, caller_name in callers:
            print(f"   {caller_name} at {file_path}:{line_number}")
    else:
        print(f"\nNo callers found for: {name}")


def _cmd_callees(search: SemanticSearch, name: str) -> None:
    print(f"\nFinding callees of: {name}")
    callees = search.find_callees(name)
    if callees:
        print(f"\nFound {len(callees)} callees:")
        for callee in callees:
            print(f"   {callee}")
    else:
        print(f"\nNo callees found for: {name}")


def _cmd_refs(search: SemanticSearch, name: str) -> None:
    print(f"\nFinding references to: {name}")
    refs = search.find_references(name)
    if refs:
        print(f"\nFound {len(refs)} references:")
        for file_path, line_number in refs:
            print(f"   {file_path}:{line_number}")
    else:
        print(f"\nNo references found for: {name}")


def _cmd_info(search: SemanticSearch, name: str) -> None:
    print(f"\nSymbol info: {name}")
    info = search.get_symbol_info(name)
    if info:
        print("\nSymbol found:")
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
        print(f"\nSymbol not found: {name}")


_COMMANDS = {
    "find": _cmd_find,
    "callers": _cmd_callers,
    "callees": _cmd_callees,
    "refs": _cmd_refs,
    "info": _cmd_info,
    "stats": lambda _search, _name: None,  # no-op: repo stats printed unconditionally above
}


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
        print("\nRepository Statistics:")
        print(f"   Total symbols: {stats['total_symbols']}")
        print(f"   Unique names: {stats['unique_names']}")
        print(f"   Graph nodes: {stats['graph_nodes']}")
        print(f"   Graph edges: {stats['graph_edges']}")

        handler = _COMMANDS.get(command)
        if handler:
            handler(search, symbol_name)
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
