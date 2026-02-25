# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors
"""Symbol type definitions for code extraction.

This module defines the Symbol dataclass used to represent extracted
code symbols (functions, classes, interfaces, types).

Usage:
    from symbol_types import Symbol

    symbol = Symbol(
        name="my_function",
        type="function",
        file="/path/to/file.py",
        line=42,
        signature="def my_function(x: int) -> str"
    )

Author: Cervella Backend (F1.1 Tech Debt Cleanup)
Version: 1.0.0
Date: 2026-02-02
"""

__version__ = "1.0.0"
__version_date__ = "2026-02-02"

from dataclasses import dataclass, field
from typing import List


@dataclass
class Symbol:
    """Represents a code symbol (function, class, interface, etc).

    Attributes:
        name: Symbol name (e.g., "login", "UserService")
        type: Symbol type ("function", "class", "interface", "type")
        file: File path where symbol is defined
        line: Line number where symbol starts
        signature: Concise signature (no function body)
        docstring: Documentation string if available
        references: List of other symbols this symbol references
    """
    name: str
    type: str  # "function", "class", "interface", "type"
    file: str
    line: int
    signature: str
    docstring: str = ""
    references: List[str] = field(default_factory=list)

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"<Symbol {self.type} '{self.name}' at {self.file}:{self.line}>"
