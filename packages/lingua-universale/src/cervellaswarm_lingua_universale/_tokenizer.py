# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Unified tokenizer for the Lingua Universale v0.2.

This module provides the lexical analysis layer for the unified parser
(C1.3).  It replaces the two duplicate inline tokenizers in ``intent.py``
and ``spec.py`` with a single, richer implementation that supports all
terminals required by the 62-production EBNF grammar.

Key design decisions (full rationale in PLAN_C1_3_1_TOKENIZER.md):

- **Keywords are IDENT**: the tokenizer does *not* distinguish keyword
  from identifier.  The parser dispatches on ``tok.value``.
- **Indent stack (CPython pattern)**: the stack stores absolute column
  counts (0, 4, 8, …), not logical levels. Emits explicit INDENT and
  DEDENT tokens.  Every INDENT is paired with a DEDENT before EOF.
- **Paren depth tracking**: inside ``()`` and ``[]`` the tokenizer
  suppresses NEWLINE, INDENT, and DEDENT (line-continuation semantics).
- **4-space indent unit**: tabs are rejected.  Indent not a multiple of
  4 raises :class:`TokenizeError`.
- **textwrap.dedent** is applied first so triple-quoted source strings
  with arbitrary base indentation work naturally.
- **No external dependencies**: only Python stdlib.
"""

from __future__ import annotations

import re
import textwrap
from dataclasses import dataclass
from enum import Enum, auto


# ---------------------------------------------------------------------------
# Token kinds
# ---------------------------------------------------------------------------


class TokKind(Enum):
    """Exhaustive set of token kinds for Lingua Universale v0.2."""

    # Structural
    INDENT = auto()    # increase in indentation (one token per increase)
    DEDENT = auto()    # decrease in indentation (one token per level closed)
    NEWLINE = auto()   # end of a logical line
    EOF = auto()       # end of source

    # Literals
    IDENT = auto()     # identifier or keyword (parser distinguishes)
    NUMBER = auto()    # integer or float: 80, 3.14
    STRING = auto()    # string literal: "hello", 'world' (includes quotes)

    # Multi-char comparison operators (must be scanned before single-char)
    GTE = auto()       # >=
    LTE = auto()       # <=
    EQ = auto()        # ==
    NEQ = auto()       # !=

    # Single-char comparison operators
    GT = auto()        # >
    LT = auto()        # <

    # Single-char symbols
    COLON = auto()     # :
    COMMA = auto()     # ,
    DOT = auto()       # .
    QUESTION = auto()  # ?
    PIPE = auto()      # |
    LBRACKET = auto()  # [
    RBRACKET = auto()  # ]
    LPAREN = auto()    # (
    RPAREN = auto()    # )
    EQUALS = auto()    # =


# ---------------------------------------------------------------------------
# Token dataclass
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Tok:
    """A single token with its kind, original text, and source position.

    Args:
        kind:  The token kind.
        value: Original source text.  Empty string for INDENT, DEDENT,
               NEWLINE, and EOF.
        line:  1-indexed source line number.
        col:   0-indexed column of the first character.
    """

    kind: TokKind
    value: str
    line: int
    col: int


# ---------------------------------------------------------------------------
# Tokenize error
# ---------------------------------------------------------------------------


class TokenizeError(Exception):
    """Lexical error raised by :func:`tokenize`.

    Attributes:
        line: 1-indexed source line where the error occurred.
        col:  0-indexed column where the error occurred.
    """

    def __init__(self, message: str, line: int = 0, col: int = 0) -> None:
        self.line = line
        self.col = col
        loc = f"line {line}, col {col}" if line else "unknown location"
        super().__init__(f"{loc}: {message}")


# ---------------------------------------------------------------------------
# Internal compiled regexes
# ---------------------------------------------------------------------------

_IDENT_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_NUMBER_RE = re.compile(r"\d+(?:\.\d+)?")

# Map two-char operators to their TokKind
_MULTI_CHAR_OPS: dict[str, TokKind] = {
    ">=": TokKind.GTE,
    "<=": TokKind.LTE,
    "==": TokKind.EQ,
    "!=": TokKind.NEQ,
}

# Map single characters to their TokKind
_SINGLE_CHAR_MAP: dict[str, TokKind] = {
    ":": TokKind.COLON,
    ",": TokKind.COMMA,
    ".": TokKind.DOT,
    "?": TokKind.QUESTION,
    "|": TokKind.PIPE,
    "[": TokKind.LBRACKET,
    "]": TokKind.RBRACKET,
    "(": TokKind.LPAREN,
    ")": TokKind.RPAREN,
    "=": TokKind.EQUALS,
    ">": TokKind.GT,
    "<": TokKind.LT,
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def tokenize(source: str) -> list[Tok]:
    """Tokenize Lingua Universale source into a flat token list.

    Indent-aware: emits explicit INDENT and DEDENT tokens using an
    indent stack (CPython pattern).  Inside ``()`` and ``[]``,
    INDENT/DEDENT and NEWLINE are suppressed (line-continuation
    semantics).

    The source is ``textwrap.dedent()``-ed first, so triple-quoted
    strings with arbitrary base indentation work naturally.

    Args:
        source: The source text to tokenize.

    Returns:
        A list of :class:`Tok` objects, always ending with EOF.
        Every INDENT has a matching DEDENT.

    Raises:
        TokenizeError: On lexical errors: tabs, bad indent alignment,
            unterminated string literal, or unexpected character.
    """
    # Check for tabs before dedent so they are never silently stripped.
    # textwrap.dedent can consume a common leading tab, hiding the error.
    pre_dedent_lines = source.split("\n")
    for pre_no, pre_line in enumerate(pre_dedent_lines, start=1):
        if "\t" in pre_line:
            tab_col = pre_line.index("\t")
            raise TokenizeError(
                "tabs are not allowed; use 4 spaces for indentation",
                line=pre_no,
                col=tab_col,
            )

    source = textwrap.dedent(source)
    lines = source.split("\n")

    tokens: list[Tok] = []
    indent_stack: list[int] = [0]  # absolute column counts
    paren_depth: int = 0
    last_line: int = 1

    for line_no, raw_line in enumerate(lines, start=1):
        last_line = line_no
        stripped = raw_line.rstrip()

        # Skip blank lines and comment-only lines (no tokens produced)
        if not stripped or stripped.lstrip().startswith("#"):
            continue

        # Count leading spaces (after dedent, raw_line is the source)
        leading_spaces = len(stripped) - len(stripped.lstrip())

        # Validate: must be multiple of 4
        if leading_spaces % 4 != 0:
            raise TokenizeError(
                f"indentation must be a multiple of 4 spaces (got {leading_spaces})",
                line=line_no,
                col=0,
            )

        # INDENT / DEDENT logic (suppressed inside parentheses)
        if paren_depth == 0:
            if leading_spaces > indent_stack[-1]:
                # Deeper: push and emit ONE INDENT
                indent_stack.append(leading_spaces)
                tokens.append(Tok(TokKind.INDENT, "", line_no, 0))

            elif leading_spaces < indent_stack[-1]:
                # Shallower: pop and emit DEDENT for each level closed
                while indent_stack and leading_spaces < indent_stack[-1]:
                    indent_stack.pop()
                    tokens.append(Tok(TokKind.DEDENT, "", line_no, 0))
                # After popping, the top must match exactly
                if leading_spaces != indent_stack[-1]:
                    raise TokenizeError(
                        "dedent does not match any outer indentation level",
                        line=line_no,
                        col=0,
                    )
            # else: same level, no indent token

        # Tokenize content (everything after the leading whitespace)
        content = stripped  # keep full stripped line, use pos with offset
        pos = leading_spaces  # start after indentation

        while pos < len(content):
            col = pos  # col is position in the full stripped line
            ch = content[pos]

            # 1. Skip spaces
            if ch == " ":
                pos += 1
                continue

            # 2. Inline comment -> stop processing this line
            if ch == "#":
                break

            # 3. Multi-char operators (MUST be before single-char checks)
            two = content[pos : pos + 2]
            if two in _MULTI_CHAR_OPS:
                tokens.append(Tok(_MULTI_CHAR_OPS[two], two, line_no, col))
                pos += 2
                continue

            # 4. Single-char symbols
            if ch in _SINGLE_CHAR_MAP:
                tokens.append(Tok(_SINGLE_CHAR_MAP[ch], ch, line_no, col))
                # Track paren depth for line-continuation suppression
                if ch in "([":
                    paren_depth += 1
                elif ch in ")]":
                    paren_depth = max(0, paren_depth - 1)
                pos += 1
                continue

            # 5. String literal (single or double quote)
            if ch in ('"', "'"):
                end = content.find(ch, pos + 1)
                if end == -1:
                    raise TokenizeError(
                        "unterminated string literal",
                        line=line_no,
                        col=col,
                    )
                value = content[pos : end + 1]  # includes surrounding quotes
                tokens.append(Tok(TokKind.STRING, value, line_no, col))
                pos = end + 1
                continue

            # 6. Number literal
            if ch.isdigit():
                m = _NUMBER_RE.match(content, pos)
                if m:
                    tokens.append(Tok(TokKind.NUMBER, m.group(), line_no, col))
                    pos = m.end()
                    continue

            # 7. Identifier (also captures keywords -- parser distinguishes)
            m = _IDENT_RE.match(content, pos)
            if m:
                tokens.append(Tok(TokKind.IDENT, m.group(), line_no, col))
                pos = m.end()
                continue

            # 8. Unknown character
            raise TokenizeError(
                f"unexpected character: {ch!r}",
                line=line_no,
                col=col,
            )

        # Emit NEWLINE at end of logical line (suppressed inside parens)
        if paren_depth == 0:
            tokens.append(Tok(TokKind.NEWLINE, "", line_no, len(content)))

    # After all lines: close all open indentation levels
    while len(indent_stack) > 1:
        indent_stack.pop()
        tokens.append(Tok(TokKind.DEDENT, "", last_line, 0))

    tokens.append(Tok(TokKind.EOF, "", last_line, 0))
    return tokens
