# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Intent parser: natural-looking notation for CervellaSwarm protocols.

A higher-level, human-readable syntax that compiles down to the same
:class:`Protocol` objects produced by the Scribble-like DSL.  Designed
to be readable by non-developers while remaining fully deterministic.

Syntax overview::

    protocol RecipeApp:
        roles: regina, backend, guardiana

        regina asks backend to do task
        backend returns result to regina
        regina asks guardiana to verify
        guardiana returns verdict to regina

    protocol PlanAndBuild:
        roles: regina, architect, worker, guardiana

        regina asks architect to plan
        architect proposes plan to regina

        when regina decides:
            approve:
                regina tells architect decision
                regina asks worker to do task
                worker returns result to regina
                regina asks guardiana to verify
                guardiana returns verdict to regina
            reject:
                regina tells architect decision
                architect proposes plan to regina

Grammar (EBNF)::

    intent_protocol ::= 'protocol' IDENT ':' NEWLINE body
    body            ::= roles_decl element+
    roles_decl      ::= INDENT 'roles' ':' IDENT (',' IDENT)* NEWLINE
    element         ::= step | choice
    step            ::= INDENT sender action receiver NEWLINE
    action          ::= 'asks' receiver 'to' verb
                      | 'returns' verb 'to'
                      | 'tells' receiver verb
                      | 'proposes' verb 'to'
                      | 'sends' verb 'to'
    verb            ::= 'do' 'task' | 'verify' | 'result' | 'verdict'
                      | 'plan' | 'decision' | 'report' | 'research'
                      | 'message' | 'broadcast' | 'shutdown' | 'context'
    choice          ::= INDENT 'when' IDENT 'decides' ':' NEWLINE branch+
    branch          ::= INDENT INDENT IDENT ':' NEWLINE step+

Each action verb phrase maps deterministically to a
:class:`~cervellaswarm_lingua_universale.types.MessageKind`.
"""

from __future__ import annotations

import re
import textwrap
from dataclasses import dataclass
from enum import Enum, auto
from .protocols import Protocol, ProtocolChoice, ProtocolElement, ProtocolStep
from .types import MessageKind


# ============================================================
# Errors
# ============================================================


class IntentParseError(Exception):
    """Error during intent parsing with location information."""

    def __init__(self, message: str, line: int = 0) -> None:
        self.line = line
        loc = f"line {line}" if line else "unknown location"
        super().__init__(f"{loc}: {message}")


# ============================================================
# Result type
# ============================================================


@dataclass(frozen=True)
class IntentParseResult:
    """Result of parsing intent notation.

    Attributes:
        protocol: The parsed Protocol object, ready for downstream use
            (SessionChecker, Lean4Generator, PythonGenerator).
        source_text: The original source for traceability.
        warnings: Non-fatal issues encountered during parsing.
    """

    protocol: Protocol
    source_text: str
    warnings: tuple[str, ...] = ()


# ============================================================
# Action verb -> MessageKind mapping (deterministic)
# ============================================================

# Each tuple of keywords maps to exactly one MessageKind.
# Order matters: longer phrases are checked first.
_ACTION_MAP: dict[tuple[str, ...], MessageKind] = {
    ("asks", "to", "do", "task"): MessageKind.TASK_REQUEST,
    ("returns", "result", "to"): MessageKind.TASK_RESULT,
    ("asks", "to", "verify"): MessageKind.AUDIT_REQUEST,
    ("returns", "verdict", "to"): MessageKind.AUDIT_VERDICT,
    ("asks", "to", "plan"): MessageKind.PLAN_REQUEST,
    ("proposes", "plan", "to"): MessageKind.PLAN_PROPOSAL,
    ("tells", "decision"): MessageKind.PLAN_DECISION,
    ("asks", "to", "research"): MessageKind.RESEARCH_QUERY,
    ("returns", "report", "to"): MessageKind.RESEARCH_REPORT,
    ("sends", "message", "to"): MessageKind.DM,
    ("sends", "broadcast", "to"): MessageKind.BROADCAST,
    ("sends", "shutdown", "to"): MessageKind.SHUTDOWN_REQUEST,
    ("sends", "ack", "to"): MessageKind.SHUTDOWN_ACK,
    ("sends", "context", "to"): MessageKind.CONTEXT_INJECT,
}

# Reverse map for rendering: MessageKind -> canonical action phrase.
# Reserved for future render_intent() -- see Fase B backlog.
# Current design: intent is input-only, DSL is the canonical bidirectional format.
_KIND_TO_ACTION: dict[MessageKind, tuple[str, ...]] = {
    v: k for k, v in _ACTION_MAP.items()
}


# ============================================================
# Tokenizer (line-oriented, indent-aware)
# ============================================================


class _TokKind(Enum):
    WORD = auto()
    COLON = auto()
    COMMA = auto()
    NEWLINE = auto()
    INDENT = auto()
    EOF = auto()


@dataclass(frozen=True)
class _Tok:
    kind: _TokKind
    value: str
    line: int


_WORD_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def _tokenize_intent(source: str) -> list[_Tok]:
    """Tokenize intent notation into a flat token list.

    Indent-aware: leading spaces on each line produce INDENT tokens
    (one per 4-space group).  Tabs are rejected.

    The source is ``textwrap.dedent``-ed first so that triple-quoted
    strings with arbitrary base indentation are handled naturally.
    """
    tokens: list[_Tok] = []
    source = textwrap.dedent(source)
    lines = source.split("\n")

    for line_no, raw_line in enumerate(lines, start=1):
        if "\t" in raw_line:
            raise IntentParseError(
                "tabs are not allowed, use 4 spaces for indentation",
                line=line_no,
            )

        stripped = raw_line.rstrip()
        if not stripped or stripped.lstrip().startswith("#"):
            # blank or comment line
            continue

        # Count leading spaces -> indent level (4 spaces = 1 level)
        leading = len(stripped) - len(stripped.lstrip())
        indent_level = leading // 4
        if leading % 4 != 0 and leading > 0:
            raise IntentParseError(
                f"indentation must be a multiple of 4 spaces "
                f"(got {leading})",
                line=line_no,
            )

        for _ in range(indent_level):
            tokens.append(_Tok(_TokKind.INDENT, "    ", line_no))

        # Tokenize the content (after stripping leading whitespace)
        content = stripped.lstrip()
        pos = 0
        while pos < len(content):
            ch = content[pos]
            if ch == " ":
                pos += 1
                continue
            if ch == ":":
                tokens.append(_Tok(_TokKind.COLON, ":", line_no))
                pos += 1
                continue
            if ch == ",":
                tokens.append(_Tok(_TokKind.COMMA, ",", line_no))
                pos += 1
                continue

            m = _WORD_RE.match(content, pos)
            if m:
                tokens.append(_Tok(_TokKind.WORD, m.group(), line_no))
                pos = m.end()
                continue

            raise IntentParseError(
                f"unexpected character: {ch!r}",
                line=line_no,
            )

        tokens.append(_Tok(_TokKind.NEWLINE, "\n", line_no))

    tokens.append(_Tok(_TokKind.EOF, "", len(lines)))
    return tokens


# ============================================================
# Parser (recursive descent)
# ============================================================


class _IntentParser:
    """Recursive descent parser for intent notation."""

    def __init__(self, tokens: list[_Tok]) -> None:
        self._tokens = tokens
        self._pos = 0

    def _peek(self) -> _Tok:
        return self._tokens[self._pos]

    def _advance(self) -> _Tok:
        tok = self._tokens[self._pos]
        self._pos += 1
        return tok

    def _expect_word(self, value: str | None = None) -> _Tok:
        tok = self._peek()
        if tok.kind != _TokKind.WORD:
            expected = f"'{value}'" if value else "a word"
            raise IntentParseError(
                f"expected {expected}, got {tok.kind.name} ({tok.value!r})",
                line=tok.line,
            )
        if value is not None and tok.value != value:
            raise IntentParseError(
                f"expected '{value}', got '{tok.value}'",
                line=tok.line,
            )
        return self._advance()

    def _expect(self, kind: _TokKind, value: str | None = None) -> _Tok:
        tok = self._peek()
        if tok.kind != kind:
            expected = f"'{value}'" if value else kind.name
            raise IntentParseError(
                f"expected {expected}, got {tok.kind.name} ({tok.value!r})",
                line=tok.line,
            )
        if value is not None and tok.value != value:
            raise IntentParseError(
                f"expected '{value}', got '{tok.value}'",
                line=tok.line,
            )
        return self._advance()

    def _skip_newlines(self) -> None:
        while self._peek().kind == _TokKind.NEWLINE:
            self._advance()

    def _count_indents(self) -> int:
        """Count and consume consecutive INDENT tokens at current position."""
        count = 0
        while self._peek().kind == _TokKind.INDENT:
            self._advance()
            count += 1
        return count

    def _peek_indent_level(self) -> int:
        """Look ahead to count indents without consuming them."""
        saved = self._pos
        count = 0
        while self._tokens[saved].kind == _TokKind.INDENT:
            saved += 1
            count += 1
        return count

    def _skip_indents(self) -> None:
        """Skip any INDENT tokens (e.g. leading indentation)."""
        while self._peek().kind == _TokKind.INDENT:
            self._advance()

    def parse(self) -> Protocol:
        """Parse a complete intent protocol declaration."""
        self._skip_newlines()
        self._skip_indents()

        # 'protocol' NAME ':'
        self._expect_word("protocol")
        name_tok = self._expect_word()
        self._expect(_TokKind.COLON)
        self._expect(_TokKind.NEWLINE)

        # roles declaration (indent level 1)
        self._skip_newlines()
        indent = self._count_indents()
        if indent < 1:
            raise IntentParseError(
                "expected indented 'roles:' declaration",
                line=self._peek().line,
            )
        roles = self._parse_roles()

        # elements
        self._skip_newlines()
        elements = self._parse_elements(base_indent=1)

        return Protocol(
            name=name_tok.value,
            roles=tuple(roles),
            elements=tuple(elements),
        )

    def _parse_roles(self) -> list[str]:
        """Parse: 'roles' ':' IDENT (',' IDENT)* NEWLINE"""
        self._expect_word("roles")
        self._expect(_TokKind.COLON)

        roles = [self._expect_word().value]
        while self._peek().kind == _TokKind.COMMA:
            self._advance()  # skip comma
            roles.append(self._expect_word().value)

        self._expect(_TokKind.NEWLINE)
        return roles

    def _parse_elements(self, base_indent: int) -> list[ProtocolElement]:
        """Parse a sequence of steps and choices at the given indent level."""
        elements: list[ProtocolElement] = []

        while True:
            self._skip_newlines()

            if self._peek().kind == _TokKind.EOF:
                break

            # Check indent level
            level = self._peek_indent_level()
            if level < base_indent:
                break  # dedent = end of this block

            # Consume the indents
            self._count_indents()

            # Decide: choice or step
            tok = self._peek()
            if tok.kind == _TokKind.WORD and tok.value == "when":
                elements.append(self._parse_choice(base_indent))
            elif tok.kind == _TokKind.WORD:
                elements.append(self._parse_step())
            else:
                raise IntentParseError(
                    f"expected a step or 'when' choice, got {tok.value!r}",
                    line=tok.line,
                )

        return elements

    def _parse_step(self) -> ProtocolStep:
        """Parse a single step: sender action receiver NEWLINE.

        Supported forms::

            regina asks backend to do task
            backend returns result to regina
            regina asks guardiana to verify
            guardiana returns verdict to regina
            regina tells architect decision
            architect proposes plan to regina
            regina sends message to worker
        """
        sender_tok = self._expect_word()
        sender = sender_tok.value

        # Collect all remaining words on this line to match against ACTION_MAP
        words: list[str] = []
        while self._peek().kind == _TokKind.WORD:
            words.append(self._advance().value)

        self._expect(_TokKind.NEWLINE)

        # Try to match the action pattern and extract the receiver
        return self._resolve_step(sender, words, sender_tok.line)

    def _resolve_step(
        self, sender: str, words: list[str], line: int
    ) -> ProtocolStep:
        """Match a sequence of words against ACTION_MAP to find MessageKind.

        The receiver is extracted from the words that are NOT part of the
        action phrase.  For example::

            words = ["asks", "backend", "to", "do", "task"]
            action = ("asks", "to", "do", "task") -> TASK_REQUEST
            receiver = "backend"

            words = ["returns", "result", "to", "regina"]
            action = ("returns", "result", "to") -> TASK_RESULT
            receiver = "regina"

            words = ["tells", "architect", "decision"]
            action = ("tells", "decision") -> PLAN_DECISION
            receiver = "architect"
        """
        # Try each action pattern (sorted longest first for greedy match)
        best_kind: MessageKind | None = None
        best_receiver: str | None = None
        best_len = 0

        for action_words, kind in _ACTION_MAP.items():
            receiver = _try_match_action(words, action_words)
            if receiver is not None and len(action_words) > best_len:
                best_kind = kind
                best_receiver = receiver
                best_len = len(action_words)

        if best_kind is None or best_receiver is None:
            word_str = " ".join(words)
            valid = _format_valid_actions()
            raise IntentParseError(
                f"cannot parse action: '{sender} {word_str}'. "
                f"Valid action patterns:\n{valid}",
                line=line,
            )

        return ProtocolStep(
            sender=sender,
            receiver=best_receiver,
            message_kind=best_kind,
        )

    def _parse_choice(self, parent_indent: int) -> ProtocolChoice:
        """Parse: 'when' IDENT 'decides' ':' NEWLINE branch+"""
        self._expect_word("when")
        decider_tok = self._expect_word()
        self._expect_word("decides")
        self._expect(_TokKind.COLON)
        self._expect(_TokKind.NEWLINE)

        branch_indent = parent_indent + 1
        branches: dict[str, tuple[ProtocolStep, ...]] = {}

        while True:
            self._skip_newlines()

            if self._peek().kind == _TokKind.EOF:
                break

            level = self._peek_indent_level()
            if level < branch_indent:
                break

            # Consume indents for the branch label
            self._count_indents()

            tok = self._peek()
            if tok.kind != _TokKind.WORD:
                raise IntentParseError(
                    f"expected branch label, got {tok.kind.name}",
                    line=tok.line,
                )

            label_tok = self._advance()
            self._expect(_TokKind.COLON)
            self._expect(_TokKind.NEWLINE)

            if label_tok.value in branches:
                raise IntentParseError(
                    f"duplicate branch label: '{label_tok.value}'",
                    line=label_tok.line,
                )

            # Parse steps at branch_indent + 1
            steps = self._parse_branch_steps(branch_indent + 1)
            if not steps:
                raise IntentParseError(
                    f"branch '{label_tok.value}' must have at least one step",
                    line=label_tok.line,
                )

            branches[label_tok.value] = tuple(steps)

        if not branches:
            raise IntentParseError(
                "choice must have at least one branch",
                line=decider_tok.line,
            )

        return ProtocolChoice(
            decider=decider_tok.value,
            branches=branches,
        )

    def _parse_branch_steps(self, step_indent: int) -> list[ProtocolStep]:
        """Parse steps inside a branch at the given indent level."""
        steps: list[ProtocolStep] = []

        while True:
            self._skip_newlines()

            if self._peek().kind == _TokKind.EOF:
                break

            level = self._peek_indent_level()
            if level < step_indent:
                break

            self._count_indents()

            tok = self._peek()
            if tok.kind != _TokKind.WORD:
                raise IntentParseError(
                    f"expected step, got {tok.kind.name}",
                    line=tok.line,
                )

            steps.append(self._parse_step())

        return steps


# ============================================================
# Action matching helpers
# ============================================================


def _try_match_action(
    words: list[str], action: tuple[str, ...]
) -> str | None:
    """Try to match an action pattern against a word list.

    The action pattern words must all appear in ``words`` in order,
    with exactly one remaining word being the receiver.

    Returns the receiver name if matched, None otherwise.

    Examples::

        words   = ["asks", "backend", "to", "do", "task"]
        action  = ("asks", "to", "do", "task")
        result  = "backend"

        words   = ["returns", "result", "to", "regina"]
        action  = ("returns", "result", "to")
        result  = "regina"

        words   = ["tells", "architect", "decision"]
        action  = ("tells", "decision")
        result  = "architect"
    """
    if len(words) != len(action) + 1:
        return None

    # The receiver is the one word in `words` not in the action pattern.
    # Try each position as the receiver candidate.
    for skip_idx in range(len(words)):
        remaining = [w for i, w in enumerate(words) if i != skip_idx]
        if tuple(remaining) == action:
            return words[skip_idx]

    return None


def _format_valid_actions() -> str:
    """Format valid action patterns for error messages."""
    lines: list[str] = []
    for action, kind in sorted(_ACTION_MAP.items(), key=lambda x: x[1].value):
        phrase = " ".join(action)
        lines.append(f"  sender {phrase} -> {kind.value}")
    return "\n".join(lines)


# ============================================================
# Public API
# ============================================================


def parse_intent(source: str) -> IntentParseResult:
    """Parse intent notation into a Protocol with metadata.

    The returned :class:`IntentParseResult` contains the parsed
    :class:`Protocol` and any warnings generated during parsing.

    Raises :class:`IntentParseError` on syntax errors with line info.

    Example::

        result = parse_intent('''
            protocol RecipeApp:
                roles: regina, backend, guardiana

                regina asks backend to do task
                backend returns result to regina
                regina asks guardiana to verify
                guardiana returns verdict to regina
        ''')
        print(result.protocol.name)  # "RecipeApp"
    """
    tokens = _tokenize_intent(source)
    parser = _IntentParser(tokens)
    protocol = parser.parse()

    # Check for trailing content
    parser._skip_newlines()
    if parser._peek().kind != _TokKind.EOF:
        tok = parser._peek()
        raise IntentParseError(
            f"unexpected content after protocol: {tok.value!r}",
            line=tok.line,
        )

    return IntentParseResult(
        protocol=protocol,
        source_text=source,
    )


def parse_intent_protocol(source: str) -> Protocol:
    """Convenience: parse intent notation and return just the Protocol.

    Equivalent to ``parse_intent(source).protocol``.

    Raises :class:`IntentParseError` on syntax errors.
    """
    return parse_intent(source).protocol
