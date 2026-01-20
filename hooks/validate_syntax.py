#!/usr/bin/env python3
"""Validate syntax of staged files using Tree-sitter.

This hook validates the syntax of Python, TypeScript, and JavaScript files
before commit, using Tree-sitter for accurate parsing.

Usage:
    python validate_syntax.py <file1> [file2] ...
    python validate_syntax.py --staged  # Validate all staged files

Exit codes:
    0: All files have valid syntax
    1: One or more files have syntax errors
    2: Internal error (parser setup, etc.)

Author: Cervella Backend
Version: 1.0.0
Date: 2026-01-20
"""

__version__ = "1.0.0"

import sys
import subprocess
from pathlib import Path
from typing import List, Tuple, Optional

# Add scripts/utils to path for TreesitterParser import
SCRIPTS_DIR = Path(__file__).parent.parent / "scripts" / "utils"
sys.path.insert(0, str(SCRIPTS_DIR))

try:
    from treesitter_parser import TreesitterParser
except ImportError as e:
    print(f"ERROR: Cannot import TreesitterParser: {e}")
    print(f"       Make sure tree-sitter packages are installed")
    sys.exit(2)


# Colors for terminal output
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
NC = '\033[0m'  # No Color


def get_staged_files() -> List[str]:
    """Get list of staged files from git.

    Returns:
        List of staged file paths (only added, copied, modified)
    """
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
            capture_output=True,
            text=True,
            check=True
        )
        return [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]
    except subprocess.CalledProcessError:
        return []


def filter_supported_files(files: List[str]) -> List[str]:
    """Filter files to only include supported languages.

    Args:
        files: List of file paths

    Returns:
        List of supported file paths (.py, .ts, .tsx, .js, .jsx)
    """
    supported_extensions = {'.py', '.ts', '.tsx', '.js', '.jsx'}
    return [f for f in files if Path(f).suffix.lower() in supported_extensions]


def validate_file(parser: TreesitterParser, file_path: str) -> Tuple[bool, Optional[str]]:
    """Validate syntax of a single file.

    Args:
        parser: TreesitterParser instance
        file_path: Path to file to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    path = Path(file_path)

    if not path.exists():
        return False, f"File not found: {file_path}"

    try:
        tree = parser.parse_file(file_path)

        if tree is None:
            return False, f"Failed to parse: {file_path}"

        if tree.root_node.has_error:
            # Find the error location
            error_nodes = find_error_nodes(tree.root_node)
            if error_nodes:
                first_error = error_nodes[0]
                line = first_error.start_point[0] + 1
                col = first_error.start_point[1] + 1
                return False, f"Syntax error at line {line}, column {col}"
            return False, "Syntax error detected"

        return True, None

    except Exception as e:
        return False, f"Error: {str(e)}"


def find_error_nodes(node, errors=None) -> List:
    """Recursively find error nodes in the AST.

    Args:
        node: Tree-sitter node to search
        errors: List to accumulate errors

    Returns:
        List of error nodes
    """
    if errors is None:
        errors = []

    if node.type == 'ERROR' or node.is_missing:
        errors.append(node)

    for child in node.children:
        find_error_nodes(child, errors)

    return errors


def main() -> int:
    """Main entry point.

    Returns:
        Exit code (0 = success, 1 = syntax errors, 2 = internal error)
    """
    # Parse arguments
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <file1> [file2] ...")
        print(f"       {sys.argv[0]} --staged")
        return 2

    # Get files to validate
    if sys.argv[1] == '--staged':
        files = get_staged_files()
    else:
        files = sys.argv[1:]

    # Filter to supported files
    supported_files = filter_supported_files(files)

    if not supported_files:
        # No supported files to check
        return 0

    print(f"\n{YELLOW}>> Validating syntax ({len(supported_files)} files)...{NC}")

    # Initialize parser
    try:
        parser = TreesitterParser()
    except Exception as e:
        print(f"{RED}ERROR:{NC} Failed to initialize parser: {e}")
        return 2

    # Validate each file
    errors = 0
    for file_path in supported_files:
        is_valid, error_msg = validate_file(parser, file_path)

        if is_valid:
            print(f"  {GREEN}OK:{NC} {file_path}")
        else:
            print(f"  {RED}FAIL:{NC} {file_path}")
            print(f"        {error_msg}")
            errors += 1

    # Summary
    if errors > 0:
        print(f"\n{RED}Syntax validation failed: {errors} file(s) with errors{NC}")
        return 1
    else:
        print(f"{GREEN}Syntax validation passed{NC}")
        return 0


if __name__ == "__main__":
    sys.exit(main())
