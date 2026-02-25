# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for DSL parser: valid parsing, tokenizer, and error cases."""

import pytest

from cervellaswarm_lingua_universale.dsl import (
    DSLError,
    DSLParseError,
    parse_protocol,
    parse_protocols,
    _tokenize,
    _message_kind_from_name,
    _message_kind_to_name,
    _NAME_TO_KIND,
    _KIND_TO_NAME,
)
from cervellaswarm_lingua_universale.protocols import (
    Protocol,
    ProtocolChoice,
    ProtocolStep,
)
from cervellaswarm_lingua_universale.types import MessageKind


# ============================================================
# DSL sources for testing
# ============================================================

SIMPLE_TASK_DSL = """\
protocol SimpleTask {
    roles regina, worker;

    regina -> worker : TaskRequest;
    worker -> regina : TaskResult;
}
"""

DELEGATE_TASK_DSL = """\
protocol DelegateTask {
    roles regina, worker, guardiana;

    regina    -> worker    : TaskRequest;
    worker    -> regina    : TaskResult;
    regina    -> guardiana : AuditRequest;
    guardiana -> regina    : AuditVerdict;
}
"""

RESEARCH_FLOW_DSL = """\
protocol ResearchFlow {
    roles regina, researcher, guardiana;

    regina     -> researcher : ResearchQuery;
    researcher -> regina     : ResearchReport;
    regina     -> guardiana  : AuditRequest;
    guardiana  -> regina     : AuditVerdict;
}
"""

ARCHITECT_FLOW_DSL = """\
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
"""


# ============================================================
# Tokenizer tests
# ============================================================


class TestTokenizer:
    def test_empty_source(self):
        tokens = _tokenize("")
        assert len(tokens) == 1
        assert tokens[0].value == ""  # EOF

    def test_simple_tokens(self):
        tokens = _tokenize("protocol Test { }")
        # protocol(KW), Test(IDENT), {, }
        assert len(tokens) == 5  # + EOF
        assert tokens[0].value == "protocol"
        assert tokens[1].value == "Test"

    def test_arrow_token(self):
        tokens = _tokenize("a -> b")
        assert tokens[1].value == "->"

    def test_comments_skipped(self):
        tokens = _tokenize("// this is a comment\nprotocol")
        assert tokens[0].value == "protocol"

    def test_inline_comment_skipped(self):
        tokens = _tokenize("regina -> worker : TaskRequest; // send task")
        # Should parse all tokens before the comment
        values = [t.value for t in tokens if t.value]
        assert "TaskRequest" in values
        assert "//" not in values

    def test_line_tracking(self):
        tokens = _tokenize("a\nb\nc")
        assert tokens[0].line == 1
        assert tokens[1].line == 2
        assert tokens[2].line == 3

    def test_column_tracking(self):
        tokens = _tokenize("abc def")
        assert tokens[0].col == 1
        assert tokens[1].col == 5

    def test_unexpected_character(self):
        with pytest.raises(DSLParseError, match="unexpected character.*@"):
            _tokenize("protocol @ Test")

    def test_unexpected_character_hash(self):
        with pytest.raises(DSLParseError, match="unexpected character.*#"):
            _tokenize("# comment")

    def test_keywords_detected(self):
        from cervellaswarm_lingua_universale.dsl import _TokenKind

        tokens = _tokenize("protocol roles choice at myident")
        assert tokens[0].kind == _TokenKind.KEYWORD
        assert tokens[1].kind == _TokenKind.KEYWORD
        assert tokens[2].kind == _TokenKind.KEYWORD
        assert tokens[3].kind == _TokenKind.KEYWORD
        assert tokens[4].kind == _TokenKind.IDENT


# ============================================================
# Parse valid protocols
# ============================================================


class TestParseSimpleTask:
    def test_name(self):
        p = parse_protocol(SIMPLE_TASK_DSL)
        assert p.name == "SimpleTask"

    def test_roles(self):
        p = parse_protocol(SIMPLE_TASK_DSL)
        assert p.roles == ("regina", "worker")

    def test_element_count(self):
        p = parse_protocol(SIMPLE_TASK_DSL)
        assert len(p.elements) == 2

    def test_first_step(self):
        p = parse_protocol(SIMPLE_TASK_DSL)
        step = p.elements[0]
        assert isinstance(step, ProtocolStep)
        assert step.sender == "regina"
        assert step.receiver == "worker"
        assert step.message_kind == MessageKind.TASK_REQUEST

    def test_second_step(self):
        p = parse_protocol(SIMPLE_TASK_DSL)
        step = p.elements[1]
        assert isinstance(step, ProtocolStep)
        assert step.sender == "worker"
        assert step.receiver == "regina"
        assert step.message_kind == MessageKind.TASK_RESULT

    def test_default_max_repetitions(self):
        p = parse_protocol(SIMPLE_TASK_DSL)
        assert p.max_repetitions == 1

    def test_description_empty(self):
        p = parse_protocol(SIMPLE_TASK_DSL)
        assert p.description == ""


class TestParseDelegateTask:
    def test_name(self):
        p = parse_protocol(DELEGATE_TASK_DSL)
        assert p.name == "DelegateTask"

    def test_roles(self):
        p = parse_protocol(DELEGATE_TASK_DSL)
        assert p.roles == ("regina", "worker", "guardiana")

    def test_element_count(self):
        p = parse_protocol(DELEGATE_TASK_DSL)
        assert len(p.elements) == 4

    def test_all_steps_are_protocol_steps(self):
        p = parse_protocol(DELEGATE_TASK_DSL)
        for elem in p.elements:
            assert isinstance(elem, ProtocolStep)

    def test_message_kinds_sequence(self):
        p = parse_protocol(DELEGATE_TASK_DSL)
        kinds = [e.message_kind for e in p.elements]
        assert kinds == [
            MessageKind.TASK_REQUEST,
            MessageKind.TASK_RESULT,
            MessageKind.AUDIT_REQUEST,
            MessageKind.AUDIT_VERDICT,
        ]


class TestParseResearchFlow:
    def test_name(self):
        p = parse_protocol(RESEARCH_FLOW_DSL)
        assert p.name == "ResearchFlow"

    def test_roles(self):
        p = parse_protocol(RESEARCH_FLOW_DSL)
        assert p.roles == ("regina", "researcher", "guardiana")

    def test_research_message_kinds(self):
        p = parse_protocol(RESEARCH_FLOW_DSL)
        assert p.elements[0].message_kind == MessageKind.RESEARCH_QUERY
        assert p.elements[1].message_kind == MessageKind.RESEARCH_REPORT


class TestParseArchitectFlow:
    def test_name(self):
        p = parse_protocol(ARCHITECT_FLOW_DSL)
        assert p.name == "ArchitectFlow"

    def test_roles(self):
        p = parse_protocol(ARCHITECT_FLOW_DSL)
        assert p.roles == ("regina", "architect", "worker", "guardiana")

    def test_element_count(self):
        p = parse_protocol(ARCHITECT_FLOW_DSL)
        # PlanRequest, PlanProposal, choice
        assert len(p.elements) == 3

    def test_first_two_are_steps(self):
        p = parse_protocol(ARCHITECT_FLOW_DSL)
        assert isinstance(p.elements[0], ProtocolStep)
        assert isinstance(p.elements[1], ProtocolStep)
        assert p.elements[0].message_kind == MessageKind.PLAN_REQUEST
        assert p.elements[1].message_kind == MessageKind.PLAN_PROPOSAL

    def test_choice_element(self):
        p = parse_protocol(ARCHITECT_FLOW_DSL)
        choice = p.elements[2]
        assert isinstance(choice, ProtocolChoice)
        assert choice.decider == "regina"

    def test_choice_branch_count(self):
        p = parse_protocol(ARCHITECT_FLOW_DSL)
        choice = p.elements[2]
        assert len(choice.branches) == 2
        assert "approve" in choice.branches
        assert "reject" in choice.branches

    def test_approve_branch_steps(self):
        p = parse_protocol(ARCHITECT_FLOW_DSL)
        choice = p.elements[2]
        approve = choice.branches["approve"]
        assert len(approve) == 5
        kinds = [s.message_kind for s in approve]
        assert kinds == [
            MessageKind.PLAN_DECISION,
            MessageKind.TASK_REQUEST,
            MessageKind.TASK_RESULT,
            MessageKind.AUDIT_REQUEST,
            MessageKind.AUDIT_VERDICT,
        ]

    def test_reject_branch_steps(self):
        p = parse_protocol(ARCHITECT_FLOW_DSL)
        choice = p.elements[2]
        reject = choice.branches["reject"]
        assert len(reject) == 2
        assert reject[0].message_kind == MessageKind.PLAN_DECISION
        assert reject[1].message_kind == MessageKind.PLAN_PROPOSAL


# ============================================================
# Parse edge cases
# ============================================================


class TestParseEdgeCases:
    def test_with_comments(self):
        source = """\
// Protocol for simple task delegation
protocol Simple {
    roles a, b; // two roles
    // First interaction
    a -> b : TaskRequest;
    b -> a : TaskResult; // reply
}
"""
        p = parse_protocol(source)
        assert p.name == "Simple"
        assert len(p.elements) == 2

    def test_minimal_whitespace(self):
        source = "protocol X{roles a,b;a->b:TaskRequest;b->a:TaskResult;}"
        p = parse_protocol(source)
        assert p.name == "X"
        assert len(p.elements) == 2

    def test_extra_whitespace(self):
        source = """
            protocol    Spacey   {
                roles    a  ,   b  ;

                a   ->   b   :   TaskRequest  ;
                b   ->   a   :   TaskResult   ;
            }
        """
        p = parse_protocol(source)
        assert p.name == "Spacey"
        assert len(p.elements) == 2

    def test_multiple_protocols(self):
        source = SIMPLE_TASK_DSL + "\n" + DELEGATE_TASK_DSL
        protocols = parse_protocols(source)
        assert len(protocols) == 2
        assert protocols[0].name == "SimpleTask"
        assert protocols[1].name == "DelegateTask"

    def test_protocol_no_elements(self):
        source = "protocol Empty { roles a, b; }"
        p = parse_protocol(source)
        assert p.name == "Empty"
        assert len(p.elements) == 0

    def test_underscore_in_names(self):
        source = "protocol My_Proto { roles role_a, role_b; role_a -> role_b : Dm; }"
        p = parse_protocol(source)
        assert p.name == "My_Proto"
        assert p.roles == ("role_a", "role_b")

    def test_all_message_kinds_parseable(self):
        """Every MessageKind can appear in DSL notation."""
        for kind in MessageKind:
            name = _message_kind_to_name(kind)
            source = f"protocol Test {{ roles a, b; a -> b : {name}; }}"
            p = parse_protocol(source)
            assert p.elements[0].message_kind == kind


# ============================================================
# Parse error cases
# ============================================================


class TestParseErrors:
    def test_empty_source(self):
        with pytest.raises(DSLParseError, match="no protocols found"):
            parse_protocols("")

    def test_empty_source_single(self):
        with pytest.raises(DSLParseError, match="expected 'protocol'"):
            parse_protocol("")

    def test_missing_protocol_keyword(self):
        with pytest.raises(DSLParseError, match="expected 'protocol'"):
            parse_protocol("notprotocol Test { roles a, b; }")

    def test_missing_protocol_name(self):
        with pytest.raises(DSLParseError, match="expected IDENT"):
            parse_protocol("protocol { roles a, b; }")

    def test_missing_opening_brace(self):
        with pytest.raises(DSLParseError, match="expected.*LBRACE"):
            parse_protocol("protocol Test roles a, b; }")

    def test_missing_roles_keyword(self):
        with pytest.raises(DSLParseError, match="expected 'roles'"):
            parse_protocol("protocol Test { a, b; }")

    def test_missing_roles_semicolon(self):
        with pytest.raises(DSLParseError, match="expected.*SEMICOLON"):
            parse_protocol("protocol Test { roles a, b }")

    def test_missing_step_arrow(self):
        with pytest.raises(DSLParseError, match="expected.*ARROW"):
            parse_protocol("protocol T { roles a, b; a b : TaskRequest; }")

    def test_missing_step_colon(self):
        with pytest.raises(DSLParseError, match="expected.*COLON"):
            parse_protocol("protocol T { roles a, b; a -> b TaskRequest; }")

    def test_missing_step_semicolon(self):
        with pytest.raises(DSLParseError, match="expected.*SEMICOLON"):
            parse_protocol("protocol T { roles a, b; a -> b : TaskRequest }")

    def test_unknown_message_type(self):
        with pytest.raises(DSLParseError, match="unknown message type 'FakeMsg'"):
            parse_protocol("protocol T { roles a, b; a -> b : FakeMsg; }")

    def test_unexpected_character(self):
        with pytest.raises(DSLParseError, match="unexpected character"):
            parse_protocol("protocol T { roles a, b; a -> b @ TaskRequest; }")

    def test_unclosed_brace(self):
        with pytest.raises(DSLParseError, match="unexpected end of input"):
            parse_protocol("protocol T { roles a, b; a -> b : TaskRequest;")

    def test_duplicate_branch_label(self):
        source = """\
protocol T {
    roles a, b;
    choice at a {
        same: { a -> b : TaskRequest; }
        same: { a -> b : TaskResult; }
    }
}
"""
        with pytest.raises(DSLParseError, match="duplicate branch label.*same"):
            parse_protocol(source)

    def test_trailing_content(self):
        source = SIMPLE_TASK_DSL + "extra"
        with pytest.raises(DSLParseError, match="unexpected token after protocol"):
            parse_protocol(source)

    def test_single_role(self):
        """Protocol with 1 role: step has sender == receiver -> rejected."""
        with pytest.raises(ValueError, match="sender and receiver cannot be the same"):
            parse_protocol("protocol T { roles a; a -> a : Dm; }")

    def test_single_role_different_step_targets(self):
        """Protocol with 1 role but step targets another -> role check fails."""
        with pytest.raises(ValueError, match="at least 2 roles"):
            parse_protocol("protocol T { roles a; a -> b : Dm; }")

    def test_role_not_in_protocol(self):
        """Sender/receiver not in roles (enforced by Protocol.__post_init__)."""
        with pytest.raises(ValueError, match="not in protocol roles"):
            parse_protocol("protocol T { roles a, b; a -> c : Dm; }")

    def test_unexpected_token_in_elements(self):
        with pytest.raises(DSLParseError, match="expected step or 'choice'"):
            parse_protocol("protocol T { roles a, b; ; }")

    def test_empty_branch(self):
        source = "protocol T { roles a, b; choice at a { go: { } } }"
        with pytest.raises(DSLParseError, match="must have at least one step"):
            parse_protocol(source)

    def test_unclosed_branch(self):
        source = """\
protocol T {
    roles a, b;
    choice at a {
        go: { a -> b : TaskRequest;
    }
}
"""
        # The missing } for the branch means the parser tries to parse more steps
        # and eventually hits EOF
        with pytest.raises(DSLParseError):
            parse_protocol(source)


# ============================================================
# MessageKind name conversion
# ============================================================


class TestMessageKindConversion:
    def test_all_kinds_have_names(self):
        assert len(_NAME_TO_KIND) == len(MessageKind)
        assert len(_KIND_TO_NAME) == len(MessageKind)

    def test_roundtrip_all_kinds(self):
        for kind in MessageKind:
            name = _message_kind_to_name(kind)
            assert _message_kind_from_name(name) == kind

    def test_task_request_name(self):
        assert _message_kind_to_name(MessageKind.TASK_REQUEST) == "TaskRequest"

    def test_audit_verdict_name(self):
        assert _message_kind_to_name(MessageKind.AUDIT_VERDICT) == "AuditVerdict"

    def test_plan_proposal_name(self):
        assert _message_kind_to_name(MessageKind.PLAN_PROPOSAL) == "PlanProposal"

    def test_dm_name(self):
        assert _message_kind_to_name(MessageKind.DM) == "Dm"

    def test_context_inject_name(self):
        assert _message_kind_to_name(MessageKind.CONTEXT_INJECT) == "ContextInject"

    def test_unknown_name_error(self):
        with pytest.raises(DSLParseError, match="unknown message type 'Bogus'"):
            _message_kind_from_name("Bogus")

    def test_unknown_name_shows_valid_types(self):
        with pytest.raises(DSLParseError, match="Valid types:.*TaskRequest"):
            _message_kind_from_name("Bogus")

    def test_dsl_error_hierarchy(self):
        assert issubclass(DSLParseError, DSLError)
        assert issubclass(DSLError, Exception)

    def test_parse_error_has_line_col(self):
        err = DSLParseError("test", line=5, col=10)
        assert err.line == 5
        assert err.col == 10
        assert "line 5" in str(err)
        assert "col 10" in str(err)

    def test_parse_error_no_location(self):
        err = DSLParseError("test")
        assert "unknown location" in str(err)
