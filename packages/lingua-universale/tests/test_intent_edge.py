# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Edge case and error tests for the intent parser (B.4).

Tests error handling, invalid input, edge cases, and boundary conditions.
"""

import pytest

from cervellaswarm_lingua_universale.intent import (
    IntentParseError,
    IntentParseResult,
    parse_intent,
    parse_intent_protocol,
)
from cervellaswarm_lingua_universale.protocols import (
    Protocol,
    ProtocolChoice,
    ProtocolStep,
)


# ============================================================
# Syntax errors
# ============================================================


class TestSyntaxErrors:
    """Test that syntax errors produce clear IntentParseError."""

    def test_missing_protocol_keyword(self):
        with pytest.raises(IntentParseError, match="expected 'protocol'"):
            parse_intent_protocol("""
                NotAProtocol:
                    roles: a, b
                    a asks b to do task
                    b returns result to a
            """)

    def test_missing_colon_after_name(self):
        with pytest.raises(IntentParseError, match="expected.*COLON"):
            parse_intent_protocol("""
                protocol Test
                    roles: a, b
                    a asks b to do task
                    b returns result to a
            """)

    def test_missing_roles_declaration(self):
        with pytest.raises(IntentParseError, match="expected 'roles'"):
            parse_intent_protocol("""
                protocol Test:
                    a asks b to do task
                    b returns result to a
            """)

    def test_missing_colon_after_roles(self):
        with pytest.raises(IntentParseError, match="expected.*COLON"):
            parse_intent_protocol("""
                protocol Test:
                    roles a, b
                    a asks b to do task
                    b returns result to a
            """)

    def test_unknown_action(self):
        with pytest.raises(IntentParseError, match="cannot parse action"):
            parse_intent_protocol("""
                protocol Test:
                    roles: a, b

                    a flies b to moon
                    b returns result to a
            """)

    def test_tabs_rejected(self):
        with pytest.raises(IntentParseError, match="tabs are not allowed"):
            parse_intent_protocol("protocol Test:\n\troles: a, b\n")

    def test_bad_indentation(self):
        with pytest.raises(IntentParseError, match="multiple of 4"):
            parse_intent_protocol("""
                protocol Test:
                  roles: a, b
                  a asks b to do task
                  b returns result to a
            """)

    def test_unexpected_character(self):
        with pytest.raises(IntentParseError, match="unexpected character"):
            parse_intent_protocol("""
                protocol Test:
                    roles: a, b

                    a asks b to do task!
                    b returns result to a
            """)

    def test_trailing_content(self):
        with pytest.raises(IntentParseError, match="unexpected content"):
            parse_intent_protocol("""
                protocol Test:
                    roles: a, b

                    a asks b to do task
                    b returns result to a
                protocol Extra:
                    roles: c, d

                    c asks d to do task
                    d returns result to c
            """)


# ============================================================
# Protocol validation (delegated to Protocol.__post_init__)
# ============================================================


class TestProtocolValidation:
    """Test that Protocol validation catches structural errors."""

    def test_single_role_rejected(self):
        """Single role is rejected - either at step level (self-send) or Protocol level."""
        with pytest.raises(ValueError):
            parse_intent_protocol("""
                protocol Test:
                    roles: only_one

                    only_one asks only_one to do task
            """)

    def test_duplicate_roles_rejected(self):
        """Duplicate roles - error caught at step level (self-send) or Protocol level."""
        with pytest.raises(ValueError):
            parse_intent_protocol("""
                protocol Test:
                    roles: a, a

                    a asks a to do task
            """)

    def test_undeclared_sender_rejected(self):
        with pytest.raises(ValueError, match="sender.*not in protocol roles"):
            parse_intent_protocol("""
                protocol Test:
                    roles: a, b

                    c asks b to do task
                    b returns result to a
            """)

    def test_undeclared_receiver_rejected(self):
        with pytest.raises(ValueError, match="receiver.*not in protocol roles"):
            parse_intent_protocol("""
                protocol Test:
                    roles: a, b

                    a asks c to do task
                    b returns result to a
            """)

    def test_self_send_rejected(self):
        with pytest.raises(ValueError, match="cannot be the same"):
            parse_intent_protocol("""
                protocol Test:
                    roles: a, b

                    a asks a to do task
                    b returns result to a
            """)


# ============================================================
# Choice edge cases
# ============================================================


class TestChoiceEdgeCases:
    """Test edge cases in branching."""

    def test_empty_branch_rejected(self):
        with pytest.raises(IntentParseError, match="at least one step"):
            parse_intent_protocol("""
                protocol Test:
                    roles: a, b

                    when a decides:
                        go:
                        stop:
                            a sends shutdown to b
                            b sends ack to a
            """)

    def test_duplicate_branch_label_rejected(self):
        with pytest.raises(IntentParseError, match="duplicate branch label"):
            parse_intent_protocol("""
                protocol Test:
                    roles: a, b

                    when a decides:
                        go:
                            a asks b to do task
                            b returns result to a
                        go:
                            a sends shutdown to b
                            b sends ack to a
            """)

    def test_choice_with_no_branches_rejected(self):
        with pytest.raises(IntentParseError, match="at least one branch"):
            parse_intent_protocol("""
                protocol Test:
                    roles: a, b

                    a asks b to do task
                    b returns result to a
                    when a decides:
            """)

    def test_undeclared_decider_rejected(self):
        with pytest.raises(ValueError, match="decider.*not in protocol roles"):
            parse_intent_protocol("""
                protocol Test:
                    roles: a, b

                    when c decides:
                        go:
                            a asks b to do task
                            b returns result to a
            """)


# ============================================================
# Edge cases in input
# ============================================================


class TestInputEdgeCases:
    """Test unusual but valid inputs."""

    def test_empty_string_raises(self):
        with pytest.raises(IntentParseError, match="expected 'protocol'"):
            parse_intent_protocol("")

    def test_whitespace_only_raises(self):
        with pytest.raises(IntentParseError, match="expected 'protocol'"):
            parse_intent_protocol("   \n  \n  ")

    def test_comments_only_raises(self):
        with pytest.raises(IntentParseError, match="expected 'protocol'"):
            parse_intent_protocol("# only comments\n# nothing else\n")

    def test_many_roles(self):
        p = parse_intent_protocol("""
            protocol BigTeam:
                roles: a, b, c, d, e

                a asks b to do task
                b returns result to a
                a asks c to verify
                c returns verdict to a
        """)
        assert len(p.roles) == 5

    def test_long_role_names(self):
        p = parse_intent_protocol("""
            protocol Test:
                roles: team_leader_alpha, backend_developer_beta

                team_leader_alpha asks backend_developer_beta to do task
                backend_developer_beta returns result to team_leader_alpha
        """)
        assert "team_leader_alpha" in p.roles
        assert "backend_developer_beta" in p.roles

    def test_underscore_in_names(self):
        p = parse_intent_protocol("""
            protocol my_protocol:
                roles: role_one, role_two

                role_one asks role_two to do task
                role_two returns result to role_one
        """)
        assert p.name == "my_protocol"

    def test_mixed_actions_in_one_protocol(self):
        p = parse_intent_protocol("""
            protocol MixedFlow:
                roles: boss, dev, qa, researcher

                boss asks dev to do task
                dev returns result to boss
                boss asks qa to verify
                qa returns verdict to boss
                boss asks researcher to research
                researcher returns report to boss
        """)
        assert len(p.elements) == 6
        kinds = [e.message_kind for e in p.elements]
        from cervellaswarm_lingua_universale.types import MessageKind
        assert kinds == [
            MessageKind.TASK_REQUEST,
            MessageKind.TASK_RESULT,
            MessageKind.AUDIT_REQUEST,
            MessageKind.AUDIT_VERDICT,
            MessageKind.RESEARCH_QUERY,
            MessageKind.RESEARCH_REPORT,
        ]

    def test_steps_then_choice_then_steps(self):
        p = parse_intent_protocol("""
            protocol ComplexFlow:
                roles: a, b, c

                a asks b to plan
                b proposes plan to a

                when a decides:
                    yes:
                        a tells b decision
                        a asks c to do task
                        c returns result to a
                    no:
                        a tells b decision
                        b proposes plan to a
        """)
        assert len(p.elements) == 3
        assert isinstance(p.elements[0], ProtocolStep)
        assert isinstance(p.elements[2], ProtocolChoice)


# ============================================================
# IntentParseResult frozen
# ============================================================


class TestIntentParseResult:
    """Test the IntentParseResult dataclass."""

    def test_is_frozen(self):
        result = parse_intent("""
            protocol Test:
                roles: a, b

                a asks b to do task
                b returns result to a
        """)
        with pytest.raises(AttributeError):
            result.protocol = None  # type: ignore[misc]

    def test_contains_source_text(self):
        src = """
            protocol Test:
                roles: a, b

                a asks b to do task
                b returns result to a
        """
        result = parse_intent(src)
        assert result.source_text == src

    def test_warnings_empty_by_default(self):
        result = parse_intent("""
            protocol Test:
                roles: a, b

                a asks b to do task
                b returns result to a
        """)
        assert result.warnings == ()


# ============================================================
# IntentParseError details
# ============================================================


class TestIntentParseErrorDetails:
    """Test that errors include line numbers."""

    def test_error_has_line_number(self):
        try:
            parse_intent_protocol("""
                protocol Test:
                    roles: a, b

                    a flies b to moon
                    b returns result to a
            """)
            pytest.fail("Expected IntentParseError")
        except IntentParseError as e:
            assert e.line > 0
            assert "line" in str(e)

    def test_tab_error_has_line_number(self):
        try:
            parse_intent_protocol("protocol T:\n\troles: a, b")
            pytest.fail("Expected IntentParseError")
        except IntentParseError as e:
            assert e.line == 2
