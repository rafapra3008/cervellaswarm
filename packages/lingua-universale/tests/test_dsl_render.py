# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for DSL renderer and round-trip fidelity."""

import pytest

from cervellaswarm_lingua_universale.dsl import (
    parse_protocol,
    parse_protocols,
    render_protocol,
    render_protocols,
    _message_kind_to_name,
)
from cervellaswarm_lingua_universale.protocols import (
    Protocol,
    ProtocolChoice,
    ProtocolStep,
    DelegateTask,
    ArchitectFlow,
    ResearchFlow,
    SimpleTask,
    STANDARD_PROTOCOLS,
)
from cervellaswarm_lingua_universale.types import MessageKind


# ============================================================
# Renderer output tests
# ============================================================


class TestRenderSimpleTask:
    def test_contains_protocol_keyword(self):
        dsl = render_protocol(SimpleTask)
        assert dsl.startswith("protocol SimpleTask {")

    def test_contains_roles(self):
        dsl = render_protocol(SimpleTask)
        assert "roles regina, worker;" in dsl

    def test_contains_steps(self):
        dsl = render_protocol(SimpleTask)
        assert "regina -> worker : TaskRequest;" in dsl
        assert "worker -> regina : TaskResult;" in dsl

    def test_ends_with_closing_brace(self):
        dsl = render_protocol(SimpleTask)
        assert dsl.strip().endswith("}")

    def test_ends_with_newline(self):
        dsl = render_protocol(SimpleTask)
        assert dsl.endswith("\n")


class TestRenderDelegateTask:
    def test_four_steps(self):
        dsl = render_protocol(DelegateTask)
        assert "TaskRequest" in dsl
        assert "TaskResult" in dsl
        assert "AuditRequest" in dsl
        assert "AuditVerdict" in dsl

    def test_three_roles(self):
        dsl = render_protocol(DelegateTask)
        assert "roles regina, worker, guardiana;" in dsl


class TestRenderResearchFlow:
    def test_research_message_kinds(self):
        dsl = render_protocol(ResearchFlow)
        assert "ResearchQuery" in dsl
        assert "ResearchReport" in dsl

    def test_researcher_role(self):
        dsl = render_protocol(ResearchFlow)
        assert "researcher" in dsl


class TestRenderArchitectFlow:
    def test_choice_block(self):
        dsl = render_protocol(ArchitectFlow)
        assert "choice at regina {" in dsl

    def test_approve_branch(self):
        dsl = render_protocol(ArchitectFlow)
        assert "approve: {" in dsl

    def test_reject_branch(self):
        dsl = render_protocol(ArchitectFlow)
        assert "reject: {" in dsl

    def test_plan_message_kinds(self):
        dsl = render_protocol(ArchitectFlow)
        assert "PlanRequest" in dsl
        assert "PlanProposal" in dsl
        assert "PlanDecision" in dsl

    def test_indentation_choice(self):
        dsl = render_protocol(ArchitectFlow)
        lines = dsl.split("\n")
        choice_lines = [l for l in lines if "choice" in l]
        assert any(l.startswith("    choice") for l in choice_lines)

    def test_indentation_branch(self):
        dsl = render_protocol(ArchitectFlow)
        lines = dsl.split("\n")
        branch_lines = [l for l in lines if "approve:" in l]
        assert any(l.startswith("        approve:") for l in branch_lines)


class TestRenderEdgeCases:
    def test_empty_elements(self):
        proto = Protocol(name="Empty", roles=("a", "b"), elements=())
        dsl = render_protocol(proto)
        assert "protocol Empty {" in dsl
        assert "roles a, b;" in dsl
        # No blank line when no elements
        lines = dsl.strip().split("\n")
        assert len(lines) == 3  # protocol, roles, closing brace

    def test_single_step(self):
        proto = Protocol(
            name="Minimal",
            roles=("a", "b"),
            elements=(
                ProtocolStep(
                    sender="a", receiver="b", message_kind=MessageKind.DM
                ),
            ),
        )
        dsl = render_protocol(proto)
        assert "a -> b : Dm;" in dsl

    def test_render_multiple_protocols(self):
        dsl = render_protocols([SimpleTask, DelegateTask])
        assert "protocol SimpleTask" in dsl
        assert "protocol DelegateTask" in dsl


# ============================================================
# Round-trip tests: DSL -> Protocol -> DSL
# ============================================================


class TestRoundtripFromDSL:
    """Parse DSL, render back, parse again: structures must match."""

    def _roundtrip(self, source: str) -> None:
        proto1 = parse_protocol(source)
        dsl = render_protocol(proto1)
        proto2 = parse_protocol(dsl)
        assert proto1 == proto2

    def test_simple_task(self):
        source = """\
protocol SimpleTask {
    roles regina, worker;

    regina -> worker : TaskRequest;
    worker -> regina : TaskResult;
}
"""
        self._roundtrip(source)

    def test_delegate_task(self):
        source = """\
protocol DelegateTask {
    roles regina, worker, guardiana;

    regina -> worker : TaskRequest;
    worker -> regina : TaskResult;
    regina -> guardiana : AuditRequest;
    guardiana -> regina : AuditVerdict;
}
"""
        self._roundtrip(source)

    def test_research_flow(self):
        source = """\
protocol ResearchFlow {
    roles regina, researcher, guardiana;

    regina -> researcher : ResearchQuery;
    researcher -> regina : ResearchReport;
    regina -> guardiana : AuditRequest;
    guardiana -> regina : AuditVerdict;
}
"""
        self._roundtrip(source)

    def test_architect_flow_with_choice(self):
        source = """\
protocol ArchitectFlow {
    roles regina, architect, worker, guardiana;

    regina -> architect : PlanRequest;
    architect -> regina : PlanProposal;
    choice at regina {
        approve: {
            regina -> architect : PlanDecision;
            regina -> worker : TaskRequest;
            worker -> regina : TaskResult;
            regina -> guardiana : AuditRequest;
            guardiana -> regina : AuditVerdict;
        }
        reject: {
            regina -> architect : PlanDecision;
            architect -> regina : PlanProposal;
        }
    }
}
"""
        self._roundtrip(source)

    def test_with_comments_stripped(self):
        source = """\
// A protocol with comments
protocol Commented {
    roles a, b; // roles declared here
    // First step
    a -> b : TaskRequest;
    b -> a : TaskResult;
}
"""
        proto1 = parse_protocol(source)
        dsl = render_protocol(proto1)
        proto2 = parse_protocol(dsl)
        assert proto1 == proto2
        # Comments are stripped
        assert "//" not in dsl

    def test_whitespace_normalised(self):
        source = "protocol X{roles a,b;a->b:TaskRequest;b->a:TaskResult;}"
        proto1 = parse_protocol(source)
        dsl = render_protocol(proto1)
        proto2 = parse_protocol(dsl)
        assert proto1 == proto2
        # Rendered output has proper indentation
        assert "    roles a, b;" in dsl

    def test_multiple_protocols_roundtrip(self):
        source = """\
protocol A {
    roles x, y;

    x -> y : Dm;
}

protocol B {
    roles p, q;

    p -> q : Broadcast;
}
"""
        protos1 = parse_protocols(source)
        dsl = render_protocols(protos1)
        protos2 = parse_protocols(dsl)
        assert len(protos1) == len(protos2)
        assert protos1[0] == protos2[0]
        assert protos1[1] == protos2[1]


# ============================================================
# Round-trip from Protocol objects (loses descriptions)
# ============================================================


class TestRoundtripFromProtocol:
    """Render Protocol -> DSL -> Protocol.

    Note: ``description`` fields are lost (not in DSL notation).
    Structural equality is checked on elements.
    """

    def _structural_match(self, original: Protocol, parsed: Protocol) -> None:
        assert original.name == parsed.name
        assert original.roles == parsed.roles
        assert len(original.elements) == len(parsed.elements)
        for orig_elem, parsed_elem in zip(original.elements, parsed.elements):
            if isinstance(orig_elem, ProtocolStep):
                assert isinstance(parsed_elem, ProtocolStep)
                assert orig_elem.sender == parsed_elem.sender
                assert orig_elem.receiver == parsed_elem.receiver
                assert orig_elem.message_kind == parsed_elem.message_kind
            elif isinstance(orig_elem, ProtocolChoice):
                assert isinstance(parsed_elem, ProtocolChoice)
                assert orig_elem.decider == parsed_elem.decider
                assert orig_elem.branches.keys() == parsed_elem.branches.keys()
                for key in orig_elem.branches:
                    orig_steps = orig_elem.branches[key]
                    parsed_steps = parsed_elem.branches[key]
                    assert len(orig_steps) == len(parsed_steps)
                    for os, ps in zip(orig_steps, parsed_steps):
                        assert os.sender == ps.sender
                        assert os.receiver == ps.receiver
                        assert os.message_kind == ps.message_kind

    def test_simple_task(self):
        dsl = render_protocol(SimpleTask)
        parsed = parse_protocol(dsl)
        self._structural_match(SimpleTask, parsed)

    def test_delegate_task(self):
        dsl = render_protocol(DelegateTask)
        parsed = parse_protocol(dsl)
        self._structural_match(DelegateTask, parsed)

    def test_research_flow(self):
        dsl = render_protocol(ResearchFlow)
        parsed = parse_protocol(dsl)
        self._structural_match(ResearchFlow, parsed)

    def test_architect_flow(self):
        dsl = render_protocol(ArchitectFlow)
        parsed = parse_protocol(dsl)
        self._structural_match(ArchitectFlow, parsed)

    def test_all_standard_protocols(self):
        """Every standard protocol survives render -> parse."""
        for name, proto in STANDARD_PROTOCOLS.items():
            dsl = render_protocol(proto)
            parsed = parse_protocol(dsl)
            self._structural_match(proto, parsed)

    def test_render_stable(self):
        """render(parse(render(P))) == render(P) -- idempotent rendering."""
        for proto in STANDARD_PROTOCOLS.values():
            dsl1 = render_protocol(proto)
            parsed = parse_protocol(dsl1)
            dsl2 = render_protocol(parsed)
            assert dsl1 == dsl2


# ============================================================
# MessageKind name coverage
# ============================================================


class TestAllMessageKindNames:
    """Every MessageKind has a valid PascalCase name for the DSL."""

    @pytest.mark.parametrize("kind", list(MessageKind))
    def test_kind_name_is_pascal_case(self, kind):
        name = _message_kind_to_name(kind)
        # PascalCase: first char uppercase, no underscores
        assert name[0].isupper()
        assert "_" not in name

    @pytest.mark.parametrize("kind", list(MessageKind))
    def test_kind_parseable_in_dsl(self, kind):
        name = _message_kind_to_name(kind)
        source = f"protocol T {{ roles a, b; a -> b : {name}; }}"
        p = parse_protocol(source)
        assert p.elements[0].message_kind == kind
