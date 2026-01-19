"""Tree-sitter Parser for Repository Mapping.

This module provides parsing capabilities using tree-sitter to generate
Abstract Syntax Trees (AST) from source code files. It supports multiple
languages and includes robust error handling for incomplete or malformed code.

Usage:
    from treesitter_parser import TreesitterParser

    parser = TreesitterParser()
    tree = parser.parse_file("app/main.py")
    print(tree.root_node.type)  # "module"

Supported Languages:
    - Python (.py)
    - TypeScript (.ts)
    - TSX (.tsx)
    - JavaScript (.js)
    - JSX (.jsx)

Author: Cervella Backend
Version: 1.0.0
Date: 2026-01-19
"""

__version__ = "1.0.0"
__version_date__ = "2026-01-19"

import logging
from pathlib import Path
from typing import Dict, Optional

from tree_sitter import Parser, Tree
from tree_sitter_language_pack import get_language

# Configure logging
logger = logging.getLogger(__name__)


class TreesitterParser:
    """Tree-sitter parser with caching and multi-language support.

    This class provides a high-level interface for parsing source code files
    using tree-sitter. It includes:
    - Language auto-detection from file extension
    - Parser caching for performance
    - AST caching for repeated access
    - Robust error handling for incomplete/malformed code
    - Support for Python, TypeScript, JavaScript, and JSX variants

    Attributes:
        parsers (Dict[str, Parser]): Cache of language parsers
        trees (Dict[str, Tree]): Cache of parsed AST trees
        languages (Dict[str, Language]): Cache of language objects
    """

    def __init__(self):
        """Initialize parser with empty caches."""
        self.parsers: Dict[str, Parser] = {}
        self.trees: Dict[str, Tree] = {}
        self.languages: Dict[str, object] = {}

        logger.debug("TreesitterParser initialized")

    def parse_file(self, file_path: str) -> Optional[Tree]:
        """Parse a source file and return its AST.

        Args:
            file_path: Absolute or relative path to source file

        Returns:
            Tree object containing the parsed AST, or None if parsing failed

        Raises:
            FileNotFoundError: If the file does not exist
            ValueError: If the file language is not supported

        Example:
            >>> parser = TreesitterParser()
            >>> tree = parser.parse_file("app/main.py")
            >>> print(tree.root_node.type)
            'module'
        """
        path = Path(file_path)

        # Check file exists
        if not path.exists():
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")

        # Check cache
        cache_key = str(path.resolve())
        if cache_key in self.trees:
            logger.debug(f"Using cached tree for: {file_path}")
            return self.trees[cache_key]

        # Detect language
        try:
            language = self.detect_language(file_path)
        except ValueError as e:
            logger.warning(f"Unsupported file type: {file_path} - {e}")
            return None

        # Get parser
        parser = self.get_parser(language)
        if parser is None:
            logger.error(f"Failed to get parser for language: {language}")
            return None

        # Read and parse file
        try:
            with open(path, 'rb') as f:
                source_code = f.read()

            tree = parser.parse(source_code)

            # Check for parse errors
            if tree.root_node.has_error:
                logger.warning(
                    f"Parse errors found in {file_path}, but continuing with partial tree"
                )

            # Cache the tree
            self.trees[cache_key] = tree
            logger.debug(f"Successfully parsed: {file_path}")

            return tree

        except Exception as e:
            logger.error(f"Error parsing {file_path}: {e}")
            return None

    def detect_language(self, file_path: str) -> str:
        """Detect programming language from file extension.

        Args:
            file_path: Path to the source file

        Returns:
            Language name (e.g., 'python', 'typescript', 'javascript')

        Raises:
            ValueError: If the file extension is not supported

        Example:
            >>> parser = TreesitterParser()
            >>> parser.detect_language("app.py")
            'python'
            >>> parser.detect_language("index.tsx")
            'tsx'
        """
        ext_map = {
            '.py': 'python',
            '.ts': 'typescript',
            '.tsx': 'tsx',
            '.js': 'javascript',
            '.jsx': 'jsx',
        }

        ext = Path(file_path).suffix.lower()

        if ext not in ext_map:
            raise ValueError(
                f"Unsupported file extension: {ext}. "
                f"Supported: {list(ext_map.keys())}"
            )

        return ext_map[ext]

    def get_parser(self, language: str) -> Optional[Parser]:
        """Get or create a parser for the specified language.

        Parsers are cached after first creation for performance.

        Args:
            language: Language name (e.g., 'python', 'typescript')

        Returns:
            Parser object for the language, or None if creation failed

        Example:
            >>> parser = TreesitterParser()
            >>> py_parser = parser.get_parser('python')
            >>> print(type(py_parser))
            <class 'tree_sitter.Parser'>
        """
        # Check cache
        if language in self.parsers:
            logger.debug(f"Using cached parser for: {language}")
            return self.parsers[language]

        # Create new parser
        try:
            # Get language binding first
            lang = self.get_language(language)
            if lang is None:
                return None

            # Create parser with language
            parser = Parser(lang)
            self.parsers[language] = parser
            logger.debug(f"Created parser for: {language}")
            return parser

        except Exception as e:
            logger.error(f"Failed to create parser for {language}: {e}")
            return None

    def get_language(self, language: str) -> Optional[object]:
        """Get or create a Language object for the specified language.

        Language objects are needed for query operations.

        Args:
            language: Language name (e.g., 'python', 'typescript')

        Returns:
            Language object, or None if creation failed

        Example:
            >>> parser = TreesitterParser()
            >>> lang = parser.get_language('python')
            >>> print(lang)
            <tree_sitter.Language object at 0x...>
        """
        # Check cache
        if language in self.languages:
            logger.debug(f"Using cached language for: {language}")
            return self.languages[language]

        # Create new language
        try:
            lang = get_language(language)
            self.languages[language] = lang
            logger.debug(f"Created language object for: {language}")
            return lang

        except Exception as e:
            logger.error(f"Failed to create language for {language}: {e}")
            return None

    def clear_cache(self) -> None:
        """Clear all cached parsers and trees.

        Useful when you need to free memory or force re-parsing.

        Example:
            >>> parser = TreesitterParser()
            >>> parser.parse_file("app.py")
            >>> parser.clear_cache()  # Free memory
        """
        self.trees.clear()
        logger.info("Cleared AST cache")

    def invalidate_file(self, file_path: str) -> None:
        """Invalidate cached tree for a specific file.

        Use this when a file has been modified and needs re-parsing.

        Args:
            file_path: Path to the file to invalidate

        Example:
            >>> parser = TreesitterParser()
            >>> parser.parse_file("app.py")
            >>> # ... file modified externally ...
            >>> parser.invalidate_file("app.py")
            >>> tree = parser.parse_file("app.py")  # Will re-parse
        """
        cache_key = str(Path(file_path).resolve())
        if cache_key in self.trees:
            del self.trees[cache_key]
            logger.debug(f"Invalidated cache for: {file_path}")

    def get_cache_stats(self) -> Dict[str, int]:
        """Get statistics about cache usage.

        Returns:
            Dictionary with cache statistics

        Example:
            >>> parser = TreesitterParser()
            >>> parser.parse_file("a.py")
            >>> parser.parse_file("b.py")
            >>> stats = parser.get_cache_stats()
            >>> print(stats)
            {'parsers': 1, 'trees': 2, 'languages': 0}
        """
        return {
            'parsers': len(self.parsers),
            'trees': len(self.trees),
            'languages': len(self.languages),
        }


# Convenience function for simple usage
def parse_file(file_path: str) -> Optional[Tree]:
    """Parse a file without managing a parser instance.

    This is a convenience function for one-off parsing. For repeated parsing,
    create a TreesitterParser instance to benefit from caching.

    Args:
        file_path: Path to source file

    Returns:
        Parsed tree or None if parsing failed

    Example:
        >>> from treesitter_parser import parse_file
        >>> tree = parse_file("app.py")
        >>> print(tree.root_node.type)
        'module'
    """
    parser = TreesitterParser()
    return parser.parse_file(file_path)


if __name__ == "__main__":
    # Simple CLI for testing
    import sys

    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <file_path>")
        sys.exit(1)

    # Enable debug logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    file_path = sys.argv[1]

    try:
        parser = TreesitterParser()
        tree = parser.parse_file(file_path)

        if tree:
            print(f"\n✅ Successfully parsed: {file_path}")
            print(f"Root node type: {tree.root_node.type}")
            print(f"Has errors: {tree.root_node.has_error}")
            print(f"Number of children: {tree.root_node.child_count}")

            # Show first few child nodes
            print(f"\nFirst 5 child nodes:")
            for i, child in enumerate(tree.root_node.children[:5]):
                print(f"  {i+1}. {child.type} at line {child.start_point[0]}")

            stats = parser.get_cache_stats()
            print(f"\nCache stats: {stats}")
        else:
            print(f"\n❌ Failed to parse: {file_path}")
            sys.exit(1)

    except FileNotFoundError:
        print(f"\n❌ File not found: {file_path}")
        sys.exit(1)
    except ValueError as e:
        print(f"\n❌ {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
