# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""DSL parser and renderer for CervellaSwarm protocol notation.

Provides a human-readable textual notation for defining communication
protocols between AI agents.  The syntax is inspired by Scribble (the
standard session-type DSL) adapted for the CervellaSwarm ecosystem.

Syntax overview::

    protocol DelegateTask {
        roles regina, worker, guardiana;

        regina    -> worker    : TaskRequest;
        worker    -> regina    : TaskResult;
        regina    -> guardiana : AuditRequest;
        guardiana -> regina    : AuditVerdict;
    }

    protocol ArchitectFlow {
        roles regina, architect, worker, guardiana;

        regina    -> architect : PlanRequest;
        architect -> regina    : PlanProposal;

        choice at regina {
            approve: {
                regina    -> architect  : PlanDecision;
                regina    -> worker     : TaskRequest;
                worker    -> regina     : TaskResult;
                regina    -> guardiana  : AuditRequest;
                guardiana -> regina     : AuditVerdict;
            }
            reject: {
                regina    -> architect  : PlanDecision;
                architect -> regina     : PlanProposal;
            }
        }
    }

Grammar (EBNF)::

    protocol_decl  ::= 'protocol' IDENT '{' roles_decl element* '}'
    roles_decl     ::= 'roles' IDENT (',' IDENT)* ';'
    element        ::= step | choice
    step           ::= IDENT '->' IDENT ':' IDENT ';'
    choice         ::= 'choice' 'at' IDENT '{' branch+ '}'
    branch         ::= IDENT ':' '{' step+ '}'

Message types use PascalCase (e.g., ``TaskRequest``), mapped to
:class:`~cervellaswarm_lingua_universale.types.MessageKind` enum values.

Round-trip fidelity: ``parse_protocol(render_protocol(P))`` preserves all
structural information (name, roles, elements).  The ``description``
fields on Protocol/ProtocolStep/ProtocolChoice are metadata not
represented in the DSL and default to ``""`` after parsing.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum, auto

from .protocols import Protocol, ProtocolChoice, ProtocolElement, ProtocolStep
from .types import MessageKind


# ============================================================
# Errors
# ============================================================


class DSLError(Exception):
    """Base error for DSL operations."""


class DSLParseError(DSLError):
    """Error during DSL parsing with location information."""

    def __init__(self, message: str, line: int = 0, col: int = 0) -> None:
        self.line = line
        self.col = col
        loc = f"line {line}" if line else "unknown location"
        if col:
            loc += f", col {col}"
        super().__init__(f"{loc}: {message}")


# ============================================================
# Tokenizer
# ============================================================


class _TokenKind(Enum):
    KEYWORD = auto()
    IDENT = auto()
    ARROW = auto()
    COLON = auto()
    SEMICOLON = auto()
    LBRACE = auto()
    RBRACE = auto()
    COMMA = auto()
    EOF = auto()


_KEYWORDS = frozenset({"protocol", "roles", "choice", "at"})


@dataclass(frozen=True)
class _Token:
    kind: _TokenKind
    value: str
    line: int
    col: int


_TOKEN_SPEC = [
    ("COMMENT", r"//[^\n]*"),
    ("ARROW", r"->"),
    ("LBRACE", r"\{"),
    ("RBRACE", r"\}"),
    ("SEMICOLON", r";"),
    ("COLON", r":"),
    ("COMMA", r","),
    ("IDENT", r"[A-Za-z_][A-Za-z0-9_]*"),
    ("NEWLINE", r"\n"),
    ("WS", r"[ \t\r]+"),
    ("ERROR", r"."),
]

_MASTER_RE = re.compile(
    "|".join(f"(?P<{name}>{pattern})" for name, pattern in _TOKEN_SPEC)
)


def _tokenize(source: str) -> list[_Token]:
    """Tokenize DSL source into a list of tokens.

    Skips whitespace, newlines, and ``//`` comments.
    Raises :class:`DSLParseError` on unrecognised characters.
    """
    tokens: list[_Token] = []
    line = 1
    line_start = 0

    for match in _MASTER_RE.finditer(source):
        kind_name = match.lastgroup
        value = match.group()
        col = match.start() - line_start + 1

        if kind_name == "NEWLINE":
            line += 1
            line_start = match.end()
            continue
        if kind_name in ("WS", "COMMENT"):
            continue
        if kind_name == "ERROR":
            raise DSLParseError(
                f"unexpected character: {value!r}", line=line, col=col
            )

        if kind_name == "IDENT" and value in _KEYWORDS:
            kind = _TokenKind.KEYWORD
        else:
            kind = _TokenKind[kind_name]

        tokens.append(_Token(kind=kind, value=value, line=line, col=col))

    tokens.append(_Token(kind=_TokenKind.EOF, value="", line=line, col=0))
    return tokens


# ============================================================
# Parser (recursive descent)
# ============================================================


class _Parser:
    """Recursive descent parser for the protocol DSL."""

    def __init__(self, tokens: list[_Token]) -> None:
        self._tokens = tokens
        self._pos = 0

    def peek(self) -> _Token:
        """Return the current token without advancing."""
        return self._tokens[self._pos]

    def _advance(self) -> _Token:
        tok = self._tokens[self._pos]
        self._pos += 1
        return tok

    def _expect(self, kind: _TokenKind, value: str | None = None) -> _Token:
        tok = self.peek()
        if tok.kind != kind:
            expected = f"'{value}'" if value else kind.name
            raise DSLParseError(
                f"expected {expected}, got {tok.kind.name} ({tok.value!r})",
                line=tok.line,
                col=tok.col,
            )
        if value is not None and tok.value != value:
            raise DSLParseError(
                f"expected '{value}', got '{tok.value}'",
                line=tok.line,
                col=tok.col,
            )
        return self._advance()

    def parse_protocol(self) -> Protocol:
        """Parse a single protocol declaration."""
        self._expect(_TokenKind.KEYWORD, "protocol")
        name_tok = self._expect(_TokenKind.IDENT)
        self._expect(_TokenKind.LBRACE)

        roles = self._parse_roles()
        elements = self._parse_elements()

        self._expect(_TokenKind.RBRACE)

        return Protocol(
            name=name_tok.value,
            roles=tuple(roles),
            elements=tuple(elements),
        )

    def _parse_roles(self) -> list[str]:
        """Parse: ``roles`` IDENT (``,`` IDENT)* ``;``"""
        self._expect(_TokenKind.KEYWORD, "roles")
        roles = [self._expect(_TokenKind.IDENT).value]
        while self.peek().kind == _TokenKind.COMMA:
            self._advance()  # skip comma
            roles.append(self._expect(_TokenKind.IDENT).value)
        self._expect(_TokenKind.SEMICOLON)
        return roles

    def _parse_elements(self) -> list[ProtocolElement]:
        """Parse sequence of steps and choices until ``}``."""
        elements: list[ProtocolElement] = []
        while self.peek().kind != _TokenKind.RBRACE:
            if (
                self.peek().kind == _TokenKind.KEYWORD
                and self.peek().value == "choice"
            ):
                elements.append(self._parse_choice())
            elif self.peek().kind == _TokenKind.IDENT:
                elements.append(self._parse_step())
            elif self.peek().kind == _TokenKind.EOF:
                raise DSLParseError(
                    "unexpected end of input, expected '}'",
                    line=self.peek().line,
                )
            else:
                tok = self.peek()
                raise DSLParseError(
                    f"expected step or 'choice', got {tok.value!r}",
                    line=tok.line,
                    col=tok.col,
                )
        return elements

    def _parse_step(self) -> ProtocolStep:
        """Parse: IDENT ``->`` IDENT ``:`` IDENT ``;``"""
        sender_tok = self._expect(_TokenKind.IDENT)
        self._expect(_TokenKind.ARROW)
        receiver_tok = self._expect(_TokenKind.IDENT)
        self._expect(_TokenKind.COLON)
        msg_tok = self._expect(_TokenKind.IDENT)
        self._expect(_TokenKind.SEMICOLON)

        kind = _message_kind_from_name(msg_tok.value, msg_tok.line, msg_tok.col)
        return ProtocolStep(
            sender=sender_tok.value,
            receiver=receiver_tok.value,
            message_kind=kind,
        )

    def _parse_choice(self) -> ProtocolChoice:
        """Parse: ``choice`` ``at`` IDENT ``{`` branch+ ``}``"""
        self._expect(_TokenKind.KEYWORD, "choice")
        self._expect(_TokenKind.KEYWORD, "at")
        decider_tok = self._expect(_TokenKind.IDENT)
        self._expect(_TokenKind.LBRACE)

        branches: dict[str, tuple[ProtocolStep, ...]] = {}
        while self.peek().kind != _TokenKind.RBRACE:
            label, steps = self._parse_branch()
            if label in branches:
                raise DSLParseError(
                    f"duplicate branch label: {label!r}",
                    line=self.peek().line,
                    col=self.peek().col,
                )
            branches[label] = tuple(steps)

        self._expect(_TokenKind.RBRACE)

        if not branches:
            raise DSLParseError(
                "choice must have at least one branch",
                line=decider_tok.line,
            )

        return ProtocolChoice(decider=decider_tok.value, branches=branches)

    def _parse_branch(self) -> tuple[str, list[ProtocolStep]]:
        """Parse: IDENT ``:`` ``{`` step+ ``}``"""
        label_tok = self._expect(_TokenKind.IDENT)
        self._expect(_TokenKind.COLON)
        self._expect(_TokenKind.LBRACE)

        steps: list[ProtocolStep] = []
        while self.peek().kind != _TokenKind.RBRACE:
            if self.peek().kind == _TokenKind.EOF:
                raise DSLParseError(
                    f"unexpected end of input in branch '{label_tok.value}'",
                    line=self.peek().line,
                )
            steps.append(self._parse_step())

        self._expect(_TokenKind.RBRACE)

        if not steps:
            raise DSLParseError(
                f"branch '{label_tok.value}' must have at least one step",
                line=label_tok.line,
                col=label_tok.col,
            )

        return label_tok.value, steps


# ============================================================
# MessageKind <-> PascalCase name conversion
# ============================================================

# Pre-computed lookup tables for O(1) conversion
_NAME_TO_KIND: dict[str, MessageKind] = {}
_KIND_TO_NAME: dict[MessageKind, str] = {}

for _kind in MessageKind:
    _name = "".join(part.capitalize() for part in _kind.value.split("_"))
    _NAME_TO_KIND[_name] = _kind
    _KIND_TO_NAME[_kind] = _name


def _message_kind_from_name(
    name: str, line: int = 0, col: int = 0
) -> MessageKind:
    """Convert PascalCase name to MessageKind.  ``TaskRequest`` -> ``TASK_REQUEST``."""
    kind = _NAME_TO_KIND.get(name)
    if kind is None:
        valid = ", ".join(sorted(_NAME_TO_KIND))
        raise DSLParseError(
            f"unknown message type '{name}'. Valid types: {valid}",
            line=line,
            col=col,
        )
    return kind


def _message_kind_to_name(kind: MessageKind) -> str:
    """Convert MessageKind to PascalCase.  ``TASK_REQUEST`` -> ``TaskRequest``."""
    return _KIND_TO_NAME[kind]


# ============================================================
# Renderer (Protocol -> DSL text)
# ============================================================


def render_protocol(protocol: Protocol) -> str:
    """Render a Protocol object to DSL notation.

    The output is valid DSL that can be parsed back with
    :func:`parse_protocol` (round-trip fidelity).
    """
    lines: list[str] = []
    lines.append(f"protocol {protocol.name} {{")
    lines.append(f"    roles {', '.join(protocol.roles)};")

    if protocol.elements:
        lines.append("")
        for elem in protocol.elements:
            _render_element(elem, lines, indent=1)

    lines.append("}")
    return "\n".join(lines) + "\n"


def render_protocols(protocols: list[Protocol] | tuple[Protocol, ...]) -> str:
    """Render multiple protocols separated by blank lines."""
    return "\n".join(render_protocol(p) for p in protocols)


def _render_element(
    elem: ProtocolElement, lines: list[str], indent: int
) -> None:
    if isinstance(elem, ProtocolStep):
        prefix = "    " * indent
        _render_step(elem, lines, prefix)
    elif isinstance(elem, ProtocolChoice):
        _render_choice(elem, lines, indent)
    else:
        raise TypeError(f"unknown protocol element type: {type(elem).__name__}")


def _render_step(step: ProtocolStep, lines: list[str], prefix: str) -> None:
    msg_name = _message_kind_to_name(step.message_kind)
    lines.append(f"{prefix}{step.sender} -> {step.receiver} : {msg_name};")


def _render_choice(
    choice: ProtocolChoice, lines: list[str], indent: int
) -> None:
    prefix = "    " * indent
    inner = "    " * (indent + 1)
    step_prefix = "    " * (indent + 2)

    lines.append(f"{prefix}choice at {choice.decider} {{")

    for label, steps in choice.branches.items():
        lines.append(f"{inner}{label}: {{")
        for step in steps:
            _render_step(step, lines, step_prefix)
        lines.append(f"{inner}}}")

    lines.append(f"{prefix}}}")


# ============================================================
# Public API
# ============================================================


def parse_protocol(source: str) -> Protocol:
    """Parse DSL source containing a single protocol definition.

    Raises :class:`DSLParseError` on syntax errors with line/col info.
    """
    tokens = _tokenize(source)
    parser = _Parser(tokens)
    protocol = parser.parse_protocol()

    if parser.peek().kind != _TokenKind.EOF:
        tok = parser.peek()
        raise DSLParseError(
            f"unexpected token after protocol: {tok.value!r}",
            line=tok.line,
            col=tok.col,
        )
    return protocol


def parse_protocols(source: str) -> list[Protocol]:
    """Parse DSL source containing one or more protocol definitions.

    Raises :class:`DSLParseError` on syntax errors with line/col info.
    """
    tokens = _tokenize(source)
    parser = _Parser(tokens)
    protocols: list[Protocol] = []

    while parser.peek().kind != _TokenKind.EOF:
        protocols.append(parser.parse_protocol())

    if not protocols:
        raise DSLParseError("no protocols found in source", line=1)
    return protocols
