# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Coverage gap tests for the Lingua Universale v0.2 parser (_parser.py).

Targets the 19 uncovered lines identified after C1.3.5 (96% coverage):

Groups:
    1. TestSkipNewlines      - line 192: _skip_newlines advance body
    2. TestEOFGuards         - lines 263, 426, 456, 485, 761, 851, 957:
                               break-after-skip_newlines guards in all loops
    3. TestErrorPaths        - lines 273, 345, 432, 462, 508, 589, 705, 767, 855:
                               error raises in protocol body, step, choice,
                               branch, property, expression, record type, agent
    4. TestFunctionalGaps    - lines 909-910: produces with comma-separated list

NOTE: No __init__.py in this directory (Package Shadowing Fix, S340).
"""

from __future__ import annotations

import textwrap

import pytest

from cervellaswarm_lingua_universale._parser import ParseError, Parser, parse
from cervellaswarm_lingua_universale._tokenizer import Tok, TokKind
from cervellaswarm_lingua_universale._ast import (
    AgentNode,
    AttrExpr,
    BranchNode,
    ChoiceNode,
    IdentExpr,
    ProtocolNode,
    RecordTypeDecl,
    StepNode,
)


# ===========================================================================
# Helpers
# ===========================================================================


def _parse(src: str):
    """Parse Lingua Universale source, applying textwrap.dedent first."""
    return parse(textwrap.dedent(src))


def _parse_agent(src: str) -> AgentNode:
    """Parse a single agent declaration (dedented)."""
    tree = _parse(src)
    assert len(tree.declarations) == 1
    node = tree.declarations[0]
    assert isinstance(node, AgentNode)
    return node


def _parse_protocol(src: str) -> ProtocolNode:
    """Parse a single protocol declaration (dedented)."""
    tree = _parse(src)
    assert len(tree.declarations) == 1
    node = tree.declarations[0]
    assert isinstance(node, ProtocolNode)
    return node


# ===========================================================================
# 1. TestSkipNewlines - line 192
# ===========================================================================


class TestSkipNewlines:
    """Line 192: the self._advance() body of _skip_newlines.

    This is hit whenever multiple consecutive NEWLINE tokens appear in
    the token stream. The parse_program and all block parsers call
    _skip_newlines, so any blank line inside a block exercises line 192.
    """

    def test_blank_lines_between_declarations_hit_skip_newlines(self) -> None:
        """Line 192: blank lines at top level between two declarations."""
        src = """\
            use python math


            use python os
        """
        tree = _parse(src)
        # Two blank lines in between -> _skip_newlines advances twice
        assert len(tree.declarations) == 2

    def test_blank_line_inside_protocol_body_hit_skip_newlines(self) -> None:
        """Line 192: blank line inside protocol body between two steps."""
        src = """\
            protocol T:
                roles: a, b

                a asks b to do task

                b returns result to a
        """
        proto = _parse_protocol(src)
        # Two blank lines inside the protocol body exercise _skip_newlines
        assert len(proto.steps) == 2

    def test_multiple_blank_lines_before_property_block(self) -> None:
        """Line 192: multiple blank lines before properties: block."""
        src = """\
            protocol T:
                roles: a, b

                a asks b to do task
                b returns result to a


                properties:
                    always terminates
        """
        proto = _parse_protocol(src)
        assert len(proto.properties) == 1

    def test_blank_lines_in_agent_body_hit_skip_newlines(self) -> None:
        """Line 192: blank line between agent clauses exercises _skip_newlines."""
        src = """\
            agent W:
                role: backend

                trust: standard
        """
        agent = _parse_agent(src)
        assert agent.role == "backend"
        assert agent.trust == "standard"


# ===========================================================================
# 2. TestEOFGuards - lines 263, 426, 456, 485, 761, 851, 957
# ===========================================================================


class TestEOFGuards:
    """Break-after-skip_newlines guards in loop bodies.

    Each guard has the pattern:
        self._skip_newlines()
        if self._at(TokKind.DEDENT) or self._at(TokKind.EOF):
            break

    They are hit when a blank line (NEWLINE) immediately precedes the
    DEDENT that closes the block. The _skip_newlines call consumes the
    NEWLINE, then the guard sees DEDENT and breaks.
    """

    def test_protocol_body_eof_guard_line_263(self) -> None:
        """Line 263: blank line (NEWLINE token) before closing DEDENT in protocol body.

        The protocol body loop (lines 260-278) calls _skip_newlines then
        checks for DEDENT/EOF at line 263.

        The tokenizer strips blank lines before DEDENT, so we bypass it
        and feed a hand-crafted token list: after the last step NEWLINE
        we inject an extra NEWLINE, then DEDENT. _skip_newlines eats the
        extra NEWLINE, then line 263 fires.
        """

        def T(kind: TokKind, value: str = "", line: int = 1, col: int = 0) -> Tok:
            return Tok(kind=kind, value=value, line=line, col=col)

        tokens = [
            T(TokKind.IDENT, "protocol"),
            T(TokKind.IDENT, "T"),
            T(TokKind.COLON, ":"),
            T(TokKind.NEWLINE),
            T(TokKind.INDENT),
            T(TokKind.IDENT, "roles"),
            T(TokKind.COLON, ":"),
            T(TokKind.IDENT, "a"),
            T(TokKind.COMMA, ","),
            T(TokKind.IDENT, "b"),
            T(TokKind.NEWLINE),
            T(TokKind.IDENT, "a"),
            T(TokKind.IDENT, "asks"),
            T(TokKind.IDENT, "b"),
            T(TokKind.IDENT, "to"),
            T(TokKind.IDENT, "do"),
            T(TokKind.IDENT, "task"),
            T(TokKind.NEWLINE),
            T(TokKind.NEWLINE),    # extra blank line -> _skip_newlines eats it
            T(TokKind.DEDENT),     # line 263 break fires here
            T(TokKind.EOF),
        ]
        program = Parser(tokens).parse_program()
        proto = program.declarations[0]
        assert isinstance(proto, ProtocolNode)
        assert len(proto.steps) == 1

    def test_choice_body_eof_guard_line_426(self) -> None:
        """Line 426: blank line before closing DEDENT in choice loop.

        The choice branch-collection loop (lines 423-427) calls
        _skip_newlines then checks DEDENT/EOF at line 426.
        """
        src = """\
            protocol T:
                roles: a, b

                when a decides:
                    yes:
                        a asks b to do task
                        b returns result to a

        """
        # Blank line after the last branch, before DEDENT of choice block
        proto = _parse_protocol(src)
        choice = proto.steps[0]
        assert isinstance(choice, ChoiceNode)
        assert len(choice.branches) == 1

    def test_branch_body_eof_guard_line_456(self) -> None:
        """Line 456: blank line before closing DEDENT in branch step loop.

        The branch step-collection loop (lines 453-457) calls
        _skip_newlines then checks DEDENT/EOF at line 456.
        """
        src = """\
            protocol T:
                roles: a, b

                when a decides:
                    yes:
                        a asks b to do task

        """
        # Trailing blank line inside the branch body
        proto = _parse_protocol(src)
        choice = proto.steps[0]
        assert isinstance(choice, ChoiceNode)
        branch = choice.branches[0]
        assert isinstance(branch, BranchNode)
        assert len(branch.steps) == 1
        assert isinstance(branch.steps[0], StepNode)

    def test_properties_body_eof_guard_line_485(self) -> None:
        """Line 485: NEWLINE before closing DEDENT in properties loop.

        The properties-collection loop (lines 482-486) calls
        _skip_newlines then checks DEDENT/EOF at line 485.

        The tokenizer strips blank lines before DEDENT, so we bypass it
        and inject an extra NEWLINE after the last property line.
        """

        def T(kind: TokKind, value: str = "", line: int = 1, col: int = 0) -> Tok:
            return Tok(kind=kind, value=value, line=line, col=col)

        tokens = [
            T(TokKind.IDENT, "protocol"),
            T(TokKind.IDENT, "T"),
            T(TokKind.COLON, ":"),
            T(TokKind.NEWLINE),
            T(TokKind.INDENT),
            T(TokKind.IDENT, "roles"),
            T(TokKind.COLON, ":"),
            T(TokKind.IDENT, "a"),
            T(TokKind.COMMA, ","),
            T(TokKind.IDENT, "b"),
            T(TokKind.NEWLINE),
            T(TokKind.IDENT, "a"),
            T(TokKind.IDENT, "asks"),
            T(TokKind.IDENT, "b"),
            T(TokKind.IDENT, "to"),
            T(TokKind.IDENT, "do"),
            T(TokKind.IDENT, "task"),
            T(TokKind.NEWLINE),
            T(TokKind.IDENT, "properties"),
            T(TokKind.COLON, ":"),
            T(TokKind.NEWLINE),
            T(TokKind.INDENT),           # open properties body
            T(TokKind.IDENT, "always"),
            T(TokKind.IDENT, "terminates"),
            T(TokKind.NEWLINE),
            T(TokKind.NEWLINE),          # extra blank line -> _skip_newlines
            T(TokKind.DEDENT),           # line 485 break fires here
            T(TokKind.DEDENT),           # close protocol body
            T(TokKind.EOF),
        ]
        program = Parser(tokens).parse_program()
        proto = program.declarations[0]
        assert isinstance(proto, ProtocolNode)
        assert len(proto.properties) == 1

    def test_record_body_eof_guard_line_761(self) -> None:
        """Line 761: blank line before closing DEDENT in record type loop.

        The record field-collection loop (lines 758-762) calls
        _skip_newlines then checks DEDENT/EOF at line 761.
        """
        src = """\
            type Result =
                value: String

        """
        # Trailing blank line inside record body
        tree = _parse(src)
        node = tree.declarations[0]
        assert isinstance(node, RecordTypeDecl)
        assert len(node.fields) == 1

    def test_agent_body_eof_guard_line_851(self) -> None:
        """Line 851: NEWLINE before closing DEDENT in agent body loop.

        The agent clause loop (lines 848-926) calls _skip_newlines then
        checks DEDENT/EOF at line 851.

        The tokenizer strips blank lines before DEDENT, so we bypass it
        and inject an extra NEWLINE after the last clause line.
        """

        def T(kind: TokKind, value: str = "", line: int = 1, col: int = 0) -> Tok:
            return Tok(kind=kind, value=value, line=line, col=col)

        tokens = [
            T(TokKind.IDENT, "agent"),
            T(TokKind.IDENT, "W"),
            T(TokKind.COLON, ":"),
            T(TokKind.NEWLINE),
            T(TokKind.INDENT),           # open agent body
            T(TokKind.IDENT, "role"),
            T(TokKind.COLON, ":"),
            T(TokKind.IDENT, "backend"),
            T(TokKind.NEWLINE),
            T(TokKind.NEWLINE),          # extra blank line -> _skip_newlines
            T(TokKind.DEDENT),           # line 851 break fires here
            T(TokKind.EOF),
        ]
        program = Parser(tokens).parse_program()
        agent = program.declarations[0]
        assert isinstance(agent, AgentNode)
        assert agent.role == "backend"

    def test_condition_list_body_eof_guard_line_957(self) -> None:
        """Line 957: NEWLINE before closing DEDENT in condition_list loop.

        The condition-list loop (lines 954-960) calls _skip_newlines
        then checks DEDENT/EOF at line 957.

        The tokenizer strips blank lines before DEDENT, so we bypass it
        and inject an extra NEWLINE after the last condition line.
        """

        def T(kind: TokKind, value: str = "", line: int = 1, col: int = 0) -> Tok:
            return Tok(kind=kind, value=value, line=line, col=col)

        tokens = [
            T(TokKind.IDENT, "agent"),
            T(TokKind.IDENT, "W"),
            T(TokKind.COLON, ":"),
            T(TokKind.NEWLINE),
            T(TokKind.INDENT),           # open agent body
            T(TokKind.IDENT, "requires"),
            T(TokKind.COLON, ":"),
            T(TokKind.NEWLINE),
            T(TokKind.INDENT),           # open requires block
            T(TokKind.IDENT, "x"),       # condition expr: x.valid
            T(TokKind.DOT, "."),
            T(TokKind.IDENT, "valid"),
            T(TokKind.NEWLINE),
            T(TokKind.NEWLINE),          # extra blank line -> _skip_newlines
            T(TokKind.DEDENT),           # line 957 break fires here
            T(TokKind.DEDENT),           # close agent body
            T(TokKind.EOF),
        ]
        program = Parser(tokens).parse_program()
        agent = program.declarations[0]
        assert isinstance(agent, AgentNode)
        assert len(agent.requires) == 1
        assert isinstance(agent.requires[0], AttrExpr)


# ===========================================================================
# 3. TestErrorPaths - lines 273, 345, 432, 462, 508, 589, 705, 767, 855
# ===========================================================================


class TestErrorPaths:
    """Error raises in parser branches that were not previously covered."""

    # --- Line 273: non-IDENT token in protocol body ---

    def test_non_ident_in_protocol_body_line_273(self) -> None:
        """Line 273: a non-IDENT token where step/when/properties is expected.

        After roles: and a step the protocol body loop hits tok.kind != IDENT,
        which triggers the ParseError at line 273.
        We inject a NUMBER token (e.g. '42') in the protocol body.
        """
        src = """\
            protocol T:
                roles: a, b

                a asks b to do task
                b returns result to a
                42
        """
        with pytest.raises(ParseError, match="expected step"):
            _parse(src)

    # --- Line 345: empty words list in _resolve_step ---

    def test_empty_action_after_sender_line_345(self) -> None:
        """Line 345: _resolve_step called with empty words list.

        This happens when a sender IDENT is followed immediately by NEWLINE
        with no action words. The step 'a' on its own line triggers this.
        """
        src = """\
            protocol T:
                roles: a, b

                a
        """
        with pytest.raises(ParseError, match="expected action after"):
            _parse(src)

    # --- Line 432: choice with no branches ---

    def test_choice_no_branches_line_432(self) -> None:
        """Line 432: ChoiceNode with zero branches raises ParseError.

        Like the branch test, we bypass the tokenizer to inject INDENT +
        NEWLINE + DEDENT as the choice body, making the loop consume the
        blank line via _skip_newlines, then break with branches=[] which
        triggers the guard at line 432.
        """

        def T(kind: TokKind, value: str = "", line: int = 1, col: int = 0) -> Tok:
            return Tok(kind=kind, value=value, line=line, col=col)

        tokens = [
            T(TokKind.IDENT, "protocol"),
            T(TokKind.IDENT, "T"),
            T(TokKind.COLON, ":"),
            T(TokKind.NEWLINE),
            T(TokKind.INDENT),
            T(TokKind.IDENT, "roles"),
            T(TokKind.COLON, ":"),
            T(TokKind.IDENT, "a"),
            T(TokKind.COMMA, ","),
            T(TokKind.IDENT, "b"),
            T(TokKind.NEWLINE),
            T(TokKind.IDENT, "a"),
            T(TokKind.IDENT, "asks"),
            T(TokKind.IDENT, "b"),
            T(TokKind.IDENT, "to"),
            T(TokKind.IDENT, "do"),
            T(TokKind.IDENT, "task"),
            T(TokKind.NEWLINE),
            T(TokKind.IDENT, "when"),
            T(TokKind.IDENT, "a"),
            T(TokKind.IDENT, "decides"),
            T(TokKind.COLON, ":"),
            T(TokKind.NEWLINE),
            T(TokKind.INDENT),      # open choice body
            T(TokKind.NEWLINE),     # blank line consumed by _skip_newlines
            T(TokKind.DEDENT),      # close choice body with branches=[]
            T(TokKind.DEDENT),      # close protocol body
            T(TokKind.EOF),
        ]
        with pytest.raises(ParseError, match="at least one branch"):
            Parser(tokens).parse_program()

    # --- Line 462: branch with no steps ---

    def test_branch_no_steps_line_462(self) -> None:
        """Line 462: BranchNode with zero steps raises ParseError.

        To reach line 462 we must get _parse_branch to succeed on
        _expect(INDENT) but collect zero steps. The tokenizer never emits
        INDENT for a whitespace-only branch body, so we bypass the tokenizer
        and feed a hand-crafted token list to Parser directly.

        Token stream: protocol header + choice header + branch 'yes:' INDENT
        NEWLINE DEDENT -> _skip_newlines eats NEWLINE, EOF guard breaks with
        steps=[] -> line 462 fires.
        """

        def T(kind: TokKind, value: str = "", line: int = 1, col: int = 0) -> Tok:
            return Tok(kind=kind, value=value, line=line, col=col)

        tokens = [
            T(TokKind.IDENT, "protocol"),
            T(TokKind.IDENT, "T"),
            T(TokKind.COLON, ":"),
            T(TokKind.NEWLINE),
            T(TokKind.INDENT),
            T(TokKind.IDENT, "roles"),
            T(TokKind.COLON, ":"),
            T(TokKind.IDENT, "a"),
            T(TokKind.COMMA, ","),
            T(TokKind.IDENT, "b"),
            T(TokKind.NEWLINE),
            T(TokKind.IDENT, "when"),
            T(TokKind.IDENT, "a"),
            T(TokKind.IDENT, "decides"),
            T(TokKind.COLON, ":"),
            T(TokKind.NEWLINE),
            T(TokKind.INDENT),      # open choice body
            T(TokKind.IDENT, "yes"),
            T(TokKind.COLON, ":"),
            T(TokKind.NEWLINE),
            T(TokKind.INDENT),      # open branch body (only blank lines inside)
            T(TokKind.NEWLINE),     # blank line consumed by _skip_newlines
            T(TokKind.DEDENT),      # close branch body with steps=[]
            T(TokKind.DEDENT),      # close choice body
            T(TokKind.DEDENT),      # close protocol body
            T(TokKind.EOF),
        ]
        with pytest.raises(ParseError, match="at least one step"):
            Parser(tokens).parse_program()

    # --- Line 508: non-IDENT token in properties block ---

    def test_non_ident_in_properties_block_line_508(self) -> None:
        """Line 508: non-IDENT token where a property keyword is expected.

        The properties block parser checks tok.kind != IDENT at line 507
        and raises ParseError at line 508-511.
        We inject a NUMBER token (e.g. '42') as a property line.
        """
        src = """\
            protocol T:
                roles: a, b

                a asks b to do task
                b returns result to a

                properties:
                    42
        """
        with pytest.raises(ParseError, match="expected property keyword"):
            _parse(src)

    # --- Line 589: unknown property keyword ---

    def test_unknown_property_keyword_line_589(self) -> None:
        """Line 589: an IDENT that is not a known property keyword.

        When an identifier doesn't match any of the known property starters
        (always/no/all/confidence/trust/X before/X cannot) and has no
        recognised second word, the fall-through ParseError at line 589
        is raised.
        """
        src = """\
            protocol T:
                roles: a, b

                a asks b to do task
                b returns result to a

                properties:
                    magic foo bar
        """
        with pytest.raises(ParseError, match="unknown property"):
            _parse(src)

    # --- Line 705: invalid primary expression token ---

    def test_invalid_primary_token_line_705(self) -> None:
        """Line 705: _parse_primary called with a token that is not a valid expr start.

        A COLON token where an expression is expected triggers the
        ParseError at line 705.
        """
        src = """\
            agent W:
                requires: :
        """
        with pytest.raises(ParseError, match="expected expression"):
            _parse(src)

    # --- Line 767: record type with no fields ---

    def test_record_type_empty_body_line_767(self) -> None:
        """Line 767: RecordTypeDecl with zero fields raises ParseError.

        Like the branch/choice tests, we bypass the tokenizer to inject
        INDENT + NEWLINE + DEDENT as the record body. After _skip_newlines
        eats the NEWLINE, the loop finds DEDENT and breaks with fields=[],
        triggering the guard at lines 766-770.
        """

        def T(kind: TokKind, value: str = "", line: int = 1, col: int = 0) -> Tok:
            return Tok(kind=kind, value=value, line=line, col=col)

        tokens = [
            T(TokKind.IDENT, "type"),
            T(TokKind.IDENT, "Empty"),
            T(TokKind.EQUALS, "="),
            T(TokKind.NEWLINE),
            T(TokKind.INDENT),      # open record body
            T(TokKind.NEWLINE),     # blank line consumed by _skip_newlines
            T(TokKind.DEDENT),      # close record body with fields=[]
            T(TokKind.EOF),
        ]
        with pytest.raises(ParseError, match="at least one field"):
            Parser(tokens).parse_program()

    # --- Line 855: non-IDENT token in agent body ---

    def test_non_ident_in_agent_body_line_855(self) -> None:
        """Line 855: non-IDENT token where an agent clause keyword is expected.

        The agent body loop at line 854 checks tok.kind != IDENT and raises
        ParseError at line 855.
        We inject a NUMBER token (e.g. '42') as an agent clause.
        """
        src = """\
            agent W:
                42
        """
        with pytest.raises(ParseError, match="expected agent clause keyword"):
            _parse(src)


# ===========================================================================
# 4. TestFunctionalGaps - lines 909-910
# ===========================================================================


class TestFunctionalGaps:
    """Lines 909-910: produces with comma-separated list of messages.

    The while loop at lines 908-910 handles multiple comma-separated
    identifiers after 'produces:'. A single-item produces list does NOT
    exercise the loop body (lines 909-910). We need 2+ items.
    """

    def test_produces_two_messages(self) -> None:
        """Lines 909-910: produces: with exactly two comma-separated messages."""
        src = """\
            agent W:
                produces: Msg1, Msg2
        """
        agent = _parse_agent(src)
        assert agent.produces == ("Msg1", "Msg2")

    def test_produces_three_messages(self) -> None:
        """Lines 909-910: produces: with three comma-separated messages."""
        src = """\
            agent W:
                produces: Alpha, Beta, Gamma
        """
        agent = _parse_agent(src)
        assert agent.produces == ("Alpha", "Beta", "Gamma")

    def test_produces_multiple_messages_preserved_order(self) -> None:
        """Lines 909-910: order of produces items is preserved."""
        src = """\
            agent W:
                produces: First, Second, Third, Fourth
        """
        agent = _parse_agent(src)
        assert agent.produces == ("First", "Second", "Third", "Fourth")

    def test_produces_multi_with_other_clauses(self) -> None:
        """Lines 909-910: produces comma list works alongside other clauses."""
        src = """\
            agent W:
                role: backend
                accepts: Request
                produces: ResultA, ResultB
        """
        agent = _parse_agent(src)
        assert agent.role == "backend"
        assert agent.accepts == ("Request",)
        assert agent.produces == ("ResultA", "ResultB")
