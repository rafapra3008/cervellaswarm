# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Unified tokenizer for the Lingua Universale.

This module provides the lexical analysis layer for the unified parser
(C1.3).  It replaces the two duplicate inline tokenizers in ``intent.py``
and ``spec.py`` with a single, richer implementation that supports all
terminals required by the 64-production EBNF grammar.

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
    """Exhaustive set of token kinds for Lingua Universale."""

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


def _check_tabs(source: str) -> None:
    """Reject tabs before textwrap.dedent (which can silently strip them).

    Comment lines (starting with optional whitespace + ``#``) are skipped
    because tabs inside comments don't affect indentation.
    """
    for line_no, line in enumerate(source.split("\n"), start=1):
        stripped = line.lstrip()
        if stripped.startswith("#"):
            continue
        if "\t" in line:
            raise TokenizeError(
                "tabs are not allowed; use 4 spaces for indentation",
                line=line_no,
                col=line.index("\t"),
            )


def _tokenize_line_content(
    content: str, pos: int, tokens: list[Tok], line_no: int, paren_depth: int,
) -> int:
    """Scan one line of content starting at *pos*, appending tokens.

    Returns the updated *paren_depth* (may change on ``(``, ``)``, etc.).
    """
    while pos < len(content):
        col = pos
        ch = content[pos]

        if ch == " ":
            pos += 1
            continue

        if ch == "#":
            break

        two = content[pos : pos + 2]
        if two in _MULTI_CHAR_OPS:
            tokens.append(Tok(_MULTI_CHAR_OPS[two], two, line_no, col))
            pos += 2
            continue

        if ch in _SINGLE_CHAR_MAP:
            tokens.append(Tok(_SINGLE_CHAR_MAP[ch], ch, line_no, col))
            if ch in "([":
                paren_depth += 1
            elif ch in ")]":
                paren_depth = max(0, paren_depth - 1)
            pos += 1
            continue

        if ch in ('"', "'"):
            end = content.find(ch, pos + 1)
            if end == -1:
                raise TokenizeError(
                    "unterminated string literal", line=line_no, col=col,
                )
            tokens.append(Tok(TokKind.STRING, content[pos : end + 1], line_no, col))
            pos = end + 1
            continue

        if ch.isdigit():
            m = _NUMBER_RE.match(content, pos)
            if m:
                tokens.append(Tok(TokKind.NUMBER, m.group(), line_no, col))
                pos = m.end()
                continue

        m = _IDENT_RE.match(content, pos)
        if m:
            tokens.append(Tok(TokKind.IDENT, m.group(), line_no, col))
            pos = m.end()
            continue

        raise TokenizeError(f"unexpected character: {ch!r}", line=line_no, col=col)

    return paren_depth


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
    _check_tabs(source)

    source = textwrap.dedent(source)
    lines = source.split("\n")

    tokens: list[Tok] = []
    indent_stack: list[int] = [0]
    paren_depth: int = 0
    last_line: int = 1

    for line_no, raw_line in enumerate(lines, start=1):
        last_line = line_no
        stripped = raw_line.rstrip()

        if not stripped or stripped.lstrip().startswith("#"):
            continue

        leading_spaces = len(stripped) - len(stripped.lstrip())

        if leading_spaces % 4 != 0:
            raise TokenizeError(
                f"indentation must be a multiple of 4 spaces (got {leading_spaces})",
                line=line_no,
                col=0,
            )

        # INDENT / DEDENT logic (suppressed inside parentheses)
        if paren_depth == 0:
            if leading_spaces > indent_stack[-1]:
                indent_stack.append(leading_spaces)
                tokens.append(Tok(TokKind.INDENT, "", line_no, 0))
            elif leading_spaces < indent_stack[-1]:
                while indent_stack and leading_spaces < indent_stack[-1]:
                    indent_stack.pop()
                    tokens.append(Tok(TokKind.DEDENT, "", line_no, 0))
                if leading_spaces != indent_stack[-1]:
                    raise TokenizeError(
                        "dedent does not match any outer indentation level",
                        line=line_no,
                        col=0,
                    )

        paren_depth = _tokenize_line_content(
            stripped, leading_spaces, tokens, line_no, paren_depth,
        )

        if paren_depth == 0:
            tokens.append(Tok(TokKind.NEWLINE, "", line_no, len(stripped)))

    while len(indent_stack) > 1:
        indent_stack.pop()
        tokens.append(Tok(TokKind.DEDENT, "", last_line, 0))

    tokens.append(Tok(TokKind.EOF, "", last_line, 0))
    return tokens
