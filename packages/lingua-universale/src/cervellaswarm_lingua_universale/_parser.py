# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Recursive descent parser for Lingua Universale v0.2.

Converts a flat token list (produced by :mod:`._tokenizer`) into an AST
whose node types are defined in :mod:`._ast`.

Design notes:

- Uses INDENT/DEDENT explicit tokens from the tokenizer.  No
  ``_count_indents()`` or ``_peek_indent_level()`` needed: the tokenizer
  already emits one INDENT per level-increase and one DEDENT per
  level-decrease.
- LL(1) everywhere except:
    - ``step`` (pattern matching on action words, not a fixed token)
    - ``primary`` (LL(3) lookahead: IDENT '.' IDENT '(' vs IDENT '.' IDENT)
- ``_parse_agent``, ``_parse_type_decl``, ``_parse_use_decl`` are stubs
  that raise :class:`ParseError`.  They will be implemented in C1.3.4.

Public API::

    from cervellaswarm_lingua_universale._parser import parse, ParseError

    ast = parse(source)   # -> ProgramNode
"""

from __future__ import annotations

from ._tokenizer import Tok, TokKind, TokenizeError, tokenize  # noqa: F401
from ._ast import (
    AgentNode,
    AllParticipate,
    AlwaysTerminates,
    AttrExpr,
    BinOpExpr,
    BranchNode,
    ChoiceNode,
    ConfidenceProp,
    Declaration,
    ExclusionProp,
    Expr,
    FieldNode,
    GenericType,
    GroupExpr,
    IdentExpr,
    Loc,
    MethodCallExpr,
    NoDeadlock,
    NotExpr,
    NumberExpr,
    OrderingProp,
    ProgramNode,
    Property,
    ProtocolNode,
    RecordTypeDecl,
    SimpleType,
    StepNode,
    StepOrChoice,
    StringExpr,
    TrustProp,
    TypeExpr,
    UseNode,
    VariantTypeDecl,
)


# ---------------------------------------------------------------------------
# ParseError
# ---------------------------------------------------------------------------


class ParseError(Exception):
    """Syntax error with source location.

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
# Parser
# ---------------------------------------------------------------------------


class Parser:
    """Recursive descent parser for Lingua Universale v0.2.

    Instantiate with a token list from :func:`._tokenizer.tokenize`, then
    call :meth:`parse_program`.
    """

    def __init__(self, tokens: list[Tok]) -> None:
        self._tokens = tokens
        self._pos = 0

    # ------------------------------------------------------------------
    # Core token utilities
    # ------------------------------------------------------------------

    def _peek(self) -> Tok:
        """Return current token without consuming it."""
        return self._tokens[min(self._pos, len(self._tokens) - 1)]

    def _peek_at(self, offset: int) -> Tok:
        """Look ahead by *offset* tokens without consuming.  Used for LL(3)."""
        idx = self._pos + offset
        return self._tokens[min(idx, len(self._tokens) - 1)]

    def _advance(self) -> Tok:
        """Consume and return the current token."""
        tok = self._tokens[self._pos]
        if self._pos < len(self._tokens) - 1:
            self._pos += 1
        return tok

    def _at(self, kind: TokKind) -> bool:
        return self._peek().kind == kind

    def _at_ident(self, value: str) -> bool:
        tok = self._peek()
        return tok.kind == TokKind.IDENT and tok.value == value

    def _expect(self, kind: TokKind) -> Tok:
        """Consume a token of *kind* or raise :class:`ParseError`."""
        tok = self._peek()
        if tok.kind != kind:
            raise ParseError(
                f"expected {kind.name}, got {tok.kind.name} ({tok.value!r})",
                line=tok.line,
                col=tok.col,
            )
        return self._advance()

    def _expect_ident(self, value: str | None = None) -> Tok:
        """Consume an IDENT token, optionally checking its *value*."""
        tok = self._peek()
        if tok.kind != TokKind.IDENT:
            expected = f"'{value}'" if value else "an identifier"
            raise ParseError(
                f"expected {expected}, got {tok.kind.name} ({tok.value!r})",
                line=tok.line,
                col=tok.col,
            )
        if value is not None and tok.value != value:
            raise ParseError(
                f"expected '{value}', got '{tok.value}'",
                line=tok.line,
                col=tok.col,
            )
        return self._advance()

    def _loc(self) -> Loc:
        """Source location of the current (not-yet-consumed) token."""
        tok = self._peek()
        return Loc(tok.line, tok.col)

    def _tok_loc(self, tok: Tok) -> Loc:
        return Loc(tok.line, tok.col)

    # ------------------------------------------------------------------
    # Whitespace helpers
    # ------------------------------------------------------------------

    def _skip_newlines(self) -> None:
        while self._at(TokKind.NEWLINE):
            self._advance()

    # ------------------------------------------------------------------
    # program
    # ------------------------------------------------------------------

    def parse_program(self) -> ProgramNode:
        """Parse: program ::= declaration*

        Returns a :class:`ProgramNode` with zero or more declarations.
        """
        loc = self._loc()
        declarations: list[Declaration] = []

        self._skip_newlines()
        while not self._at(TokKind.EOF):
            decl = self._parse_declaration()
            declarations.append(decl)
            self._skip_newlines()

        return ProgramNode(declarations=tuple(declarations), loc=loc)

    # ------------------------------------------------------------------
    # declaration dispatch
    # ------------------------------------------------------------------

    def _parse_declaration(self) -> Declaration:
        """Parse: declaration ::= protocol_decl | agent_decl | type_decl | use_decl"""
        tok = self._peek()
        if tok.kind != TokKind.IDENT:
            raise ParseError(
                f"expected 'protocol', 'agent', 'type', or 'use', "
                f"got {tok.kind.name} ({tok.value!r})",
                line=tok.line,
                col=tok.col,
            )
        if tok.value == "protocol":
            return self._parse_protocol()
        if tok.value == "agent":
            return self._parse_agent()
        if tok.value == "type":
            return self._parse_type_decl()
        if tok.value == "use":
            return self._parse_use_decl()
        raise ParseError(
            f"expected 'protocol', 'agent', 'type', or 'use', got '{tok.value}'",
            line=tok.line,
            col=tok.col,
        )

    # ------------------------------------------------------------------
    # protocol_decl
    # ------------------------------------------------------------------

    def _parse_protocol(self) -> ProtocolNode:
        """Parse: protocol_decl ::= 'protocol' IDENT ':' NEWLINE INDENT protocol_body DEDENT"""
        loc = self._loc()
        self._expect_ident("protocol")
        name_tok = self._expect_ident()
        self._expect(TokKind.COLON)
        self._expect(TokKind.NEWLINE)
        self._expect(TokKind.INDENT)

        roles = self._parse_roles()

        steps: list[StepOrChoice] = []
        properties: list[Property] = []

        while not self._at(TokKind.DEDENT) and not self._at(TokKind.EOF):
            self._skip_newlines()
            if self._at(TokKind.DEDENT) or self._at(TokKind.EOF):
                break

            tok = self._peek()
            if tok.kind == TokKind.IDENT and tok.value == "properties":
                properties = self._parse_properties_block()
            elif tok.kind == TokKind.IDENT and tok.value == "when":
                steps.append(self._parse_choice())
            elif tok.kind == TokKind.IDENT:
                steps.append(self._parse_step())
            else:
                raise ParseError(
                    f"expected step, 'when', or 'properties:', "
                    f"got {tok.kind.name} ({tok.value!r})",
                    line=tok.line,
                    col=tok.col,
                )

        self._expect(TokKind.DEDENT)

        if not steps:
            raise ParseError(
                "protocol must have at least one step",
                line=name_tok.line,
                col=name_tok.col,
            )

        return ProtocolNode(
            name=name_tok.value,
            roles=tuple(roles),
            steps=tuple(steps),
            properties=tuple(properties),
            loc=loc,
        )

    def _parse_roles(self) -> list[str]:
        """Parse: roles_clause ::= 'roles' ':' ident_list NEWLINE"""
        self._expect_ident("roles")
        self._expect(TokKind.COLON)

        roles = [self._expect_ident().value]
        while self._at(TokKind.COMMA):
            self._advance()
            roles.append(self._expect_ident().value)

        self._expect(TokKind.NEWLINE)
        return roles

    # ------------------------------------------------------------------
    # step
    # ------------------------------------------------------------------

    def _parse_step(self) -> StepNode:
        """Parse: step ::= IDENT action NEWLINE

        Collects all IDENT tokens until NEWLINE, then delegates to
        :meth:`_resolve_step` for pattern matching.
        """
        sender_tok = self._expect_ident()
        sender = sender_tok.value
        loc = self._tok_loc(sender_tok)

        words: list[str] = []
        while self._peek().kind == TokKind.IDENT:
            words.append(self._advance().value)

        self._expect(TokKind.NEWLINE)
        return self._resolve_step(sender, words, loc)

    def _resolve_step(self, sender: str, words: list[str], loc: Loc) -> StepNode:
        """Match *words* against the 5 action patterns from the grammar.

        Patterns::

            asks IDENT to VERB+        -> action="asks"
            returns NOUN+ to IDENT     -> action="returns"
            tells IDENT NOUN+          -> action="tells"
            proposes NOUN+ to IDENT    -> action="proposes"
            sends NOUN+ to IDENT       -> action="sends"

        The receiver and payload are extracted from the word positions.
        """
        if not words:
            raise ParseError(
                f"expected action after '{sender}', got end-of-line",
                line=loc.line,
                col=loc.col,
            )

        verb = words[0]

        # asks IDENT to VERB+
        if verb == "asks" and len(words) >= 4 and words[2] == "to":
            receiver = words[1]
            payload = " ".join(words[3:])
            return StepNode(
                sender=sender, action="asks", receiver=receiver,
                payload=payload, loc=loc,
            )

        # returns NOUN+ to IDENT (needs >= 4 words: returns noun to X)
        if verb == "returns" and len(words) >= 4 and words[-2] == "to":
            receiver = words[-1]
            payload = " ".join(words[1:-2])
            return StepNode(
                sender=sender, action="returns", receiver=receiver,
                payload=payload, loc=loc,
            )

        # tells IDENT NOUN+
        if verb == "tells" and len(words) >= 3:
            receiver = words[1]
            payload = " ".join(words[2:])
            return StepNode(
                sender=sender, action="tells", receiver=receiver,
                payload=payload, loc=loc,
            )

        # proposes NOUN+ to IDENT (needs >= 4 words: proposes noun to X)
        if verb == "proposes" and len(words) >= 4 and words[-2] == "to":
            receiver = words[-1]
            payload = " ".join(words[1:-2])
            return StepNode(
                sender=sender, action="proposes", receiver=receiver,
                payload=payload, loc=loc,
            )

        # sends NOUN+ to IDENT (needs >= 4 words: sends noun to X)
        if verb == "sends" and len(words) >= 4 and words[-2] == "to":
            receiver = words[-1]
            payload = " ".join(words[1:-2])
            return StepNode(
                sender=sender, action="sends", receiver=receiver,
                payload=payload, loc=loc,
            )

        word_str = " ".join(words)
        raise ParseError(
            f"cannot parse action: '{sender} {word_str}'. "
            f"Valid actions: "
            f"'asks X to verb', 'returns noun to X', "
            f"'tells X noun', 'proposes noun to X', 'sends noun to X'",
            line=loc.line,
            col=loc.col,
        )

    # ------------------------------------------------------------------
    # choice_block
    # ------------------------------------------------------------------

    def _parse_choice(self) -> ChoiceNode:
        """Parse: choice_block ::= 'when' IDENT 'decides' ':' NEWLINE INDENT branch+ DEDENT"""
        loc = self._loc()
        self._expect_ident("when")
        decider_tok = self._expect_ident()
        self._expect_ident("decides")
        self._expect(TokKind.COLON)
        self._expect(TokKind.NEWLINE)
        self._expect(TokKind.INDENT)

        branches: list[BranchNode] = []
        while not self._at(TokKind.DEDENT) and not self._at(TokKind.EOF):
            self._skip_newlines()
            if self._at(TokKind.DEDENT) or self._at(TokKind.EOF):
                break
            branches.append(self._parse_branch())

        self._expect(TokKind.DEDENT)

        if not branches:
            raise ParseError(
                "choice must have at least one branch",
                line=decider_tok.line,
                col=decider_tok.col,
            )

        return ChoiceNode(
            decider=decider_tok.value,
            branches=tuple(branches),
            loc=loc,
        )

    def _parse_branch(self) -> BranchNode:
        """Parse: branch ::= IDENT ':' NEWLINE INDENT step+ DEDENT"""
        label_tok = self._expect_ident()
        loc = self._tok_loc(label_tok)
        self._expect(TokKind.COLON)
        self._expect(TokKind.NEWLINE)
        self._expect(TokKind.INDENT)

        steps: list[StepNode] = []
        while not self._at(TokKind.DEDENT) and not self._at(TokKind.EOF):
            self._skip_newlines()
            if self._at(TokKind.DEDENT) or self._at(TokKind.EOF):
                break
            steps.append(self._parse_step())

        self._expect(TokKind.DEDENT)

        if not steps:
            raise ParseError(
                f"branch '{label_tok.value}' must have at least one step",
                line=label_tok.line,
                col=label_tok.col,
            )

        return BranchNode(label=label_tok.value, steps=tuple(steps), loc=loc)

    # ------------------------------------------------------------------
    # properties_block
    # ------------------------------------------------------------------

    def _parse_properties_block(self) -> list[Property]:
        """Parse: properties_block ::= 'properties' ':' NEWLINE INDENT property+ DEDENT"""
        self._expect_ident("properties")
        self._expect(TokKind.COLON)
        self._expect(TokKind.NEWLINE)
        self._expect(TokKind.INDENT)

        props: list[Property] = []
        while not self._at(TokKind.DEDENT) and not self._at(TokKind.EOF):
            self._skip_newlines()
            if self._at(TokKind.DEDENT) or self._at(TokKind.EOF):
                break
            props.append(self._parse_property())

        self._expect(TokKind.DEDENT)
        return props

    def _parse_property(self) -> Property:
        """Parse one property line from the grammar's 7 variants.

        Variants::

            'always' 'terminates' NEWLINE
            'no' 'deadlock' NEWLINE
            'all' 'roles' 'participate' NEWLINE
            'confidence' '>=' confidence_level NEWLINE
            'trust' '>=' trust_tier NEWLINE
            IDENT 'before' IDENT NEWLINE
            IDENT 'cannot' 'send' IDENT NEWLINE
        """
        tok = self._peek()
        loc = self._loc()

        if tok.kind != TokKind.IDENT:
            raise ParseError(
                f"expected property keyword, got {tok.kind.name} ({tok.value!r})",
                line=tok.line,
                col=tok.col,
            )

        # 'always' 'terminates'
        if tok.value == "always":
            self._advance()
            self._expect_ident("terminates")
            self._expect(TokKind.NEWLINE)
            return AlwaysTerminates(loc=loc)

        # 'no' 'deadlock'
        if tok.value == "no":
            self._advance()
            self._expect_ident("deadlock")
            self._expect(TokKind.NEWLINE)
            return NoDeadlock(loc=loc)

        # 'all' 'roles' 'participate'
        if tok.value == "all":
            self._advance()
            self._expect_ident("roles")
            self._expect_ident("participate")
            self._expect(TokKind.NEWLINE)
            return AllParticipate(loc=loc)

        # 'confidence' '>=' confidence_level
        if tok.value == "confidence":
            self._advance()
            self._expect(TokKind.GTE)
            level_tok = self._expect_ident()
            _VALID_CONFIDENCE = ("certain", "high", "medium", "low", "speculative")
            if level_tok.value not in _VALID_CONFIDENCE:
                raise ParseError(
                    f"invalid confidence level: '{level_tok.value}'. "
                    f"Valid: {', '.join(_VALID_CONFIDENCE)}",
                    line=level_tok.line,
                    col=level_tok.col,
                )
            self._expect(TokKind.NEWLINE)
            return ConfidenceProp(level=level_tok.value, loc=loc)

        # 'trust' '>=' trust_tier
        if tok.value == "trust":
            self._advance()
            self._expect(TokKind.GTE)
            tier_tok = self._expect_ident()
            _VALID_TRUST = ("verified", "trusted", "standard", "untrusted")
            if tier_tok.value not in _VALID_TRUST:
                raise ParseError(
                    f"invalid trust tier: '{tier_tok.value}'. "
                    f"Valid: {', '.join(_VALID_TRUST)}",
                    line=tier_tok.line,
                    col=tier_tok.col,
                )
            self._expect(TokKind.NEWLINE)
            return TrustProp(tier=tier_tok.value, loc=loc)

        # IDENT 'before' IDENT  or  IDENT 'cannot' 'send' IDENT
        # Require LL(2) lookahead: check word at offset 1.
        next_tok = self._peek_at(1)

        if next_tok.kind == TokKind.IDENT and next_tok.value == "before":
            before_tok = self._advance()  # IDENT (first role/event)
            self._advance()              # 'before'
            after_tok = self._expect_ident()
            self._expect(TokKind.NEWLINE)
            return OrderingProp(
                before=before_tok.value, after=after_tok.value, loc=loc,
            )

        if next_tok.kind == TokKind.IDENT and next_tok.value == "cannot":
            role_tok = self._advance()  # IDENT (role)
            self._advance()             # 'cannot'
            self._expect_ident("send")
            msg_tok = self._expect_ident()
            self._expect(TokKind.NEWLINE)
            return ExclusionProp(
                role=role_tok.value, message=msg_tok.value, loc=loc,
            )

        raise ParseError(
            f"unknown property starting with '{tok.value}'. "
            f"Expected: 'always terminates', 'no deadlock', "
            f"'X before Y', 'X cannot send Y', "
            f"'confidence >= level', 'trust >= tier', 'all roles participate'",
            line=tok.line,
            col=tok.col,
        )

    # ------------------------------------------------------------------
    # Stubs for C1.3.4
    # ------------------------------------------------------------------

    def _parse_agent(self) -> AgentNode:
        """Stub: agent declarations are implemented in C1.3.4."""
        tok = self._peek()
        raise ParseError(
            "agent declarations not yet implemented",
            line=tok.line,
            col=tok.col,
        )

    def _parse_type_decl(self) -> VariantTypeDecl | RecordTypeDecl:
        """Stub: type declarations are implemented in C1.3.4."""
        tok = self._peek()
        raise ParseError(
            "type declarations not yet implemented",
            line=tok.line,
            col=tok.col,
        )

    def _parse_use_decl(self) -> UseNode:
        """Stub: use declarations are implemented in C1.3.4."""
        tok = self._peek()
        raise ParseError(
            "use declarations not yet implemented",
            line=tok.line,
            col=tok.col,
        )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def parse(source: str) -> ProgramNode:
    """Parse Lingua Universale source into an AST.

    Applies :func:`._tokenizer.tokenize` first, then drives the recursive
    descent parser.

    Args:
        source: The source text to parse.

    Returns:
        A :class:`ProgramNode` containing all top-level declarations.

    Raises:
        TokenizeError: On lexical errors (tabs, bad indent, etc.).
        ParseError: On syntax errors, always with ``line`` and ``col``.

    Example::

        from cervellaswarm_lingua_universale._parser import parse

        ast = parse('''
            protocol DelegateTask:
                roles: regina, worker, guardiana

                regina asks worker to do task
                worker returns result to regina
                regina asks guardiana to verify
                guardiana returns verdict to regina
        ''')
        print(ast.declarations[0].name)  # "DelegateTask"
    """
    tokens = tokenize(source)
    parser = Parser(tokens)
    return parser.parse_program()
