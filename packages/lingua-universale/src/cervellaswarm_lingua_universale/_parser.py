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
- ``_parse_agent``, ``_parse_type_decl``, ``_parse_use_decl`` are fully
  implemented (C1.3.4), including expression parsing for requires/ensures.

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
# Shared constants
# ---------------------------------------------------------------------------

_VALID_CONFIDENCE = ("certain", "high", "medium", "low", "speculative")

_VALID_TRUST = ("verified", "trusted", "standard", "untrusted")

_AGENT_CLAUSES = ("role", "trust", "accepts", "produces", "requires", "ensures")

_CMP_OPS: dict[TokKind, str] = {
    TokKind.EQ: "==",
    TokKind.NEQ: "!=",
    TokKind.LT: "<",
    TokKind.GT: ">",
    TokKind.LTE: "<=",
    TokKind.GTE: ">=",
}


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
    # expressions (C1.3.4)
    # ------------------------------------------------------------------

    def _parse_expr(self) -> Expr:
        """Parse: expr ::= or_expr"""
        return self._parse_or_expr()

    def _parse_or_expr(self) -> Expr:
        """Parse: or_expr ::= and_expr ('or' and_expr)*"""
        left = self._parse_and_expr()
        while self._at_ident("or"):
            loc = self._loc()
            self._advance()
            right = self._parse_and_expr()
            left = BinOpExpr(left=left, op="or", right=right, loc=loc)
        return left

    def _parse_and_expr(self) -> Expr:
        """Parse: and_expr ::= not_expr ('and' not_expr)*"""
        left = self._parse_not_expr()
        while self._at_ident("and"):
            loc = self._loc()
            self._advance()
            right = self._parse_not_expr()
            left = BinOpExpr(left=left, op="and", right=right, loc=loc)
        return left

    def _parse_not_expr(self) -> Expr:
        """Parse: not_expr ::= 'not' not_expr | comparison"""
        if self._at_ident("not"):
            loc = self._loc()
            self._advance()
            operand = self._parse_not_expr()
            return NotExpr(operand=operand, loc=loc)
        return self._parse_comparison()

    def _parse_comparison(self) -> Expr:
        """Parse: comparison ::= primary (comparison_op primary)?"""
        left = self._parse_primary()
        tok = self._peek()
        if tok.kind in _CMP_OPS:
            loc = self._loc()
            op = _CMP_OPS[tok.kind]
            self._advance()
            right = self._parse_primary()
            return BinOpExpr(left=left, op=op, right=right, loc=loc)
        return left

    def _parse_primary(self) -> Expr:
        """Parse: primary ::= IDENT '.' IDENT '(' args? ')' (LL(3) method call)
                            | IDENT '.' IDENT              (attribute access)
                            | IDENT                         (bare identifier)
                            | NUMBER
                            | STRING
                            | '(' expr ')'                  (grouped expression)
        """
        tok = self._peek()
        loc = self._loc()

        if tok.kind == TokKind.NUMBER:
            self._advance()
            return NumberExpr(value=tok.value, loc=loc)

        if tok.kind == TokKind.STRING:
            self._advance()
            return StringExpr(value=tok.value, loc=loc)

        if tok.kind == TokKind.LPAREN:
            self._advance()
            inner = self._parse_expr()
            self._expect(TokKind.RPAREN)
            return GroupExpr(inner=inner, loc=loc)

        if tok.kind == TokKind.IDENT:
            # LL(3) lookahead for IDENT.IDENT( vs IDENT.IDENT vs bare IDENT
            if (
                self._peek_at(1).kind == TokKind.DOT
                and self._peek_at(2).kind == TokKind.IDENT
            ):
                if self._peek_at(3).kind == TokKind.LPAREN:
                    # Method call: obj.method(args)
                    obj_tok = self._advance()    # IDENT
                    self._advance()              # DOT
                    method_tok = self._advance() # IDENT
                    self._advance()              # LPAREN
                    args: list[Expr] = []
                    if not self._at(TokKind.RPAREN):
                        args.append(self._parse_expr())
                        while self._at(TokKind.COMMA):
                            self._advance()
                            args.append(self._parse_expr())
                    self._expect(TokKind.RPAREN)
                    return MethodCallExpr(
                        obj=obj_tok.value, method=method_tok.value,
                        args=tuple(args), loc=loc,
                    )
                else:
                    # Attribute access: obj.attr
                    obj_tok = self._advance()   # IDENT
                    self._advance()             # DOT
                    attr_tok = self._advance()  # IDENT
                    return AttrExpr(obj=obj_tok.value, attr=attr_tok.value, loc=loc)
            else:
                # Bare identifier
                return IdentExpr(name=self._advance().value, loc=loc)

        raise ParseError(
            f"expected expression, got {tok.kind.name} ({tok.value!r})",
            line=tok.line,
            col=tok.col,
        )

    # ------------------------------------------------------------------
    # use_decl (C1.3.4)
    # ------------------------------------------------------------------

    def _parse_use_decl(self) -> UseNode:
        """Parse: use_decl ::= 'use' 'python' dotted_name ('as' IDENT)? NEWLINE"""
        loc = self._loc()
        self._expect_ident("use")
        self._expect_ident("python")

        # dotted_name ::= IDENT ('.' IDENT)*
        parts = [self._expect_ident().value]
        while self._at(TokKind.DOT):
            self._advance()
            parts.append(self._expect_ident().value)
        module = ".".join(parts)

        # optional alias: 'as' IDENT
        alias: str | None = None
        if self._at_ident("as"):
            self._advance()
            alias = self._expect_ident().value

        self._expect(TokKind.NEWLINE)
        return UseNode(module=module, alias=alias, loc=loc)

    # ------------------------------------------------------------------
    # type_decl (C1.3.4)
    # ------------------------------------------------------------------

    def _parse_type_decl(self) -> VariantTypeDecl | RecordTypeDecl:
        """Parse: type_decl ::= 'type' IDENT '=' variant_type NEWLINE
                              | 'type' IDENT '=' NEWLINE INDENT field+ DEDENT

        Discriminant LL(1): after '=' -> IDENT means variant, NEWLINE means record.
        """
        loc = self._loc()
        self._expect_ident("type")
        name_tok = self._expect_ident()
        self._expect(TokKind.EQUALS)

        if self._at(TokKind.NEWLINE):
            # Record type
            self._advance()  # NEWLINE
            self._expect(TokKind.INDENT)

            fields: list[FieldNode] = []
            while not self._at(TokKind.DEDENT) and not self._at(TokKind.EOF):
                self._skip_newlines()
                if self._at(TokKind.DEDENT) or self._at(TokKind.EOF):
                    break
                fields.append(self._parse_field())

            self._expect(TokKind.DEDENT)

            if not fields:
                raise ParseError(
                    f"record type '{name_tok.value}' must have at least one field",
                    line=name_tok.line,
                    col=name_tok.col,
                )
            return RecordTypeDecl(
                name=name_tok.value, fields=tuple(fields), loc=loc,
            )
        else:
            # Variant type: IDENT ('|' IDENT)+
            variants = [self._expect_ident().value]
            while self._at(TokKind.PIPE):
                self._advance()
                variants.append(self._expect_ident().value)

            self._expect(TokKind.NEWLINE)

            if len(variants) < 2:
                raise ParseError(
                    f"variant type '{name_tok.value}' must have at least 2 variants "
                    f"(got {len(variants)})",
                    line=name_tok.line,
                    col=name_tok.col,
                )
            return VariantTypeDecl(
                name=name_tok.value, variants=tuple(variants), loc=loc,
            )

    def _parse_type_expr(self) -> SimpleType | GenericType:
        """Parse: type_expr ::= base_type '?'?
                  base_type ::= IDENT '[' type_expr ']' | IDENT
        """
        name_tok = self._expect_ident()
        loc = self._tok_loc(name_tok)

        if self._at(TokKind.LBRACKET):
            self._advance()  # [
            arg = self._parse_type_expr()
            self._expect(TokKind.RBRACKET)  # ]
            optional = self._at(TokKind.QUESTION)
            if optional:
                self._advance()
            return GenericType(
                name=name_tok.value, arg=arg, optional=optional, loc=loc,
            )

        optional = self._at(TokKind.QUESTION)
        if optional:
            self._advance()
        return SimpleType(name=name_tok.value, optional=optional, loc=loc)

    def _parse_field(self) -> FieldNode:
        """Parse: field ::= IDENT ':' type_expr NEWLINE"""
        loc = self._loc()
        name_tok = self._expect_ident()
        self._expect(TokKind.COLON)
        type_expr = self._parse_type_expr()
        self._expect(TokKind.NEWLINE)
        return FieldNode(name=name_tok.value, type_expr=type_expr, loc=loc)

    # ------------------------------------------------------------------
    # agent_decl (C1.3.4)
    # ------------------------------------------------------------------

    def _parse_agent(self) -> AgentNode:
        """Parse: agent_decl ::= 'agent' IDENT ':' NEWLINE INDENT agent_body DEDENT"""
        loc = self._loc()
        self._expect_ident("agent")
        name_tok = self._expect_ident()
        self._expect(TokKind.COLON)
        self._expect(TokKind.NEWLINE)
        self._expect(TokKind.INDENT)

        role: str | None = None
        trust: str | None = None
        accepts: tuple[str, ...] = ()
        produces: tuple[str, ...] = ()
        requires: tuple[Expr, ...] = ()
        ensures: tuple[Expr, ...] = ()
        _seen: set[str] = set()

        while not self._at(TokKind.DEDENT) and not self._at(TokKind.EOF):
            self._skip_newlines()
            if self._at(TokKind.DEDENT) or self._at(TokKind.EOF):
                break

            tok = self._peek()
            if tok.kind != TokKind.IDENT:
                raise ParseError(
                    f"expected agent clause keyword (role, trust, accepts, "
                    f"produces, requires, ensures), got {tok.kind.name} ({tok.value!r})",
                    line=tok.line,
                    col=tok.col,
                )

            # Detect duplicate clauses
            if tok.value in _AGENT_CLAUSES:
                if tok.value in _seen:
                    raise ParseError(
                        f"duplicate agent clause '{tok.value}' "
                        f"(already defined earlier in this agent)",
                        line=tok.line,
                        col=tok.col,
                    )
                _seen.add(tok.value)

            if tok.value == "role":
                self._advance()
                self._expect(TokKind.COLON)
                role = self._expect_ident().value
                self._expect(TokKind.NEWLINE)

            elif tok.value == "trust":
                self._advance()
                self._expect(TokKind.COLON)
                trust_tok = self._expect_ident()
                if trust_tok.value not in _VALID_TRUST:
                    raise ParseError(
                        f"invalid trust tier: '{trust_tok.value}'. "
                        f"Valid: {', '.join(_VALID_TRUST)}",
                        line=trust_tok.line,
                        col=trust_tok.col,
                    )
                trust = trust_tok.value
                self._expect(TokKind.NEWLINE)

            elif tok.value == "accepts":
                accepts = self._parse_message_list()

            elif tok.value == "produces":
                produces = self._parse_message_list()

            elif tok.value == "requires":
                requires = self._parse_condition_list("requires")

            elif tok.value == "ensures":
                ensures = self._parse_condition_list("ensures")

            else:
                raise ParseError(
                    f"unknown agent clause: '{tok.value}'. "
                    f"Expected: role, trust, accepts, produces, requires, ensures",
                    line=tok.line,
                    col=tok.col,
                )

        self._expect(TokKind.DEDENT)
        return AgentNode(
            name=name_tok.value,
            role=role,
            trust=trust,
            accepts=accepts,
            produces=produces,
            requires=requires,
            ensures=ensures,
            loc=loc,
        )

    def _parse_message_list(self) -> tuple[str, ...]:
        """Parse: ``keyword ':' IDENT (',' IDENT)* NEWLINE`` for accepts/produces."""
        self._advance()
        self._expect(TokKind.COLON)
        msgs = [self._expect_ident().value]
        while self._at(TokKind.COMMA):
            self._advance()
            msgs.append(self._expect_ident().value)
        self._expect(TokKind.NEWLINE)
        return tuple(msgs)

    def _parse_condition_list(self, keyword: str) -> tuple[Expr, ...]:
        """Parse: requires/ensures clause, block or inline.

        Block form:  keyword ':' NEWLINE INDENT condition+ DEDENT
        Inline form: keyword ':' expr NEWLINE
        """
        self._expect_ident(keyword)
        self._expect(TokKind.COLON)

        if self._at(TokKind.NEWLINE):
            # Block form
            self._advance()
            self._expect(TokKind.INDENT)
            conditions: list[Expr] = []
            while not self._at(TokKind.DEDENT) and not self._at(TokKind.EOF):
                self._skip_newlines()
                if self._at(TokKind.DEDENT) or self._at(TokKind.EOF):
                    break
                expr = self._parse_expr()
                self._expect(TokKind.NEWLINE)
                conditions.append(expr)
            self._expect(TokKind.DEDENT)
            return tuple(conditions)
        else:
            # Inline form
            expr = self._parse_expr()
            self._expect(TokKind.NEWLINE)
            return (expr,)


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
