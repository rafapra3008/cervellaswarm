# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors
"""CervellaSwarm Code Intelligence - AST-based code analysis toolkit.

Provides tree-sitter powered symbol extraction, dependency graphs,
semantic search, impact analysis, and repository mapping for Python,
TypeScript, and JavaScript codebases.
"""

__version__ = "0.1.0"

from cervellaswarm_code_intelligence.symbol_types import Symbol
from cervellaswarm_code_intelligence.treesitter_parser import TreesitterParser
from cervellaswarm_code_intelligence.symbol_extractor import SymbolExtractor
from cervellaswarm_code_intelligence.dependency_graph import DependencyGraph
from cervellaswarm_code_intelligence.semantic_search import SemanticSearch
from cervellaswarm_code_intelligence.impact_analyzer import ImpactAnalyzer
from cervellaswarm_code_intelligence.repo_mapper import RepoMapper

__all__ = [
    "Symbol",
    "TreesitterParser",
    "SymbolExtractor",
    "DependencyGraph",
    "SemanticSearch",
    "ImpactAnalyzer",
    "RepoMapper",
]
