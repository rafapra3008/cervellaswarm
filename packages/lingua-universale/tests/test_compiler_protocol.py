# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for _compile_protocol (C2.2.5).

Test structure:
  - _step_to_message_kind: action+payload -> MessageKind mapping
  - _ast_to_protocol: ProtocolNode AST -> Protocol runtime object
  - _compile_protocol: full protocol compilation
  - Preamble imports: protocol-specific imports registered
  - Choice protocols: ChoiceNode -> ProtocolChoice
  - Full program: protocol + agent + types in same module
  - Generated code is valid Python (syntax check)
"""

from __future__ import annotations

import pytest

from cervellaswarm_lingua_universale._ast import (
    AgentNode,
    BranchNode,
    ChoiceNode,
    Loc,
    ProgramNode,
    ProtocolNode,
    StepNode,
    UseNode,
    VariantTypeDecl,
)
from cervellaswarm_lingua_universale._compiler import ASTCompiler, CompiledModule


@pytest.fixture()
def compiler() -> ASTCompiler:
    return ASTCompiler()


LOC = Loc(line=1, col=0)


def _delegate_task_node(loc: Loc = LOC) -> ProtocolNode:
    """Helper: a standard DelegateTask protocol AST node."""
    return ProtocolNode(
        name="DelegateTask",
        roles=("regina", "worker", "guardiana"),
        steps=(
            StepNode("regina", "asks", "worker", "do task", Loc(4, 4)),
            StepNode("worker", "returns", "regina", "result", Loc(5, 4)),
            StepNode("regina", "asks", "guardiana", "verify", Loc(6, 4)),
            StepNode("guardiana", "returns", "regina", "verdict", Loc(7, 4)),
        ),
        properties=(),
        loc=loc,
    )


# ===================================================================
# _step_to_message_kind
# ===================================================================


class TestStepToMessageKind:
    """Tests for action+payload -> MessageKind heuristic mapping."""

    def test_asks_default_task_request(self, compiler: ASTCompiler) -> None:
        from cervellaswarm_lingua_universale.types import MessageKind
        step = StepNode("regina", "asks", "worker", "do task", LOC)
        assert compiler._step_to_message_kind(step) == MessageKind.TASK_REQUEST

    def test_asks_verify_audit_request(self, compiler: ASTCompiler) -> None:
        from cervellaswarm_lingua_universale.types import MessageKind
        step = StepNode("regina", "asks", "guardiana", "verify result", LOC)
        assert compiler._step_to_message_kind(step) == MessageKind.AUDIT_REQUEST

    def test_asks_audit_audit_request(self, compiler: ASTCompiler) -> None:
        from cervellaswarm_lingua_universale.types import MessageKind
        step = StepNode("regina", "asks", "guardiana", "audit code", LOC)
        assert compiler._step_to_message_kind(step) == MessageKind.AUDIT_REQUEST

    def test_asks_check_audit_request(self, compiler: ASTCompiler) -> None:
        from cervellaswarm_lingua_universale.types import MessageKind
        step = StepNode("regina", "asks", "guardiana", "check quality", LOC)
        assert compiler._step_to_message_kind(step) == MessageKind.AUDIT_REQUEST

    def test_asks_plan_plan_request(self, compiler: ASTCompiler) -> None:
        from cervellaswarm_lingua_universale.types import MessageKind
        step = StepNode("regina", "asks", "architect", "plan feature", LOC)
        assert compiler._step_to_message_kind(step) == MessageKind.PLAN_REQUEST

    def test_asks_research_research_query(self, compiler: ASTCompiler) -> None:
        from cervellaswarm_lingua_universale.types import MessageKind
        step = StepNode("regina", "asks", "researcher", "research topic", LOC)
        assert compiler._step_to_message_kind(step) == MessageKind.RESEARCH_QUERY

    def test_returns_default_task_result(self, compiler: ASTCompiler) -> None:
        from cervellaswarm_lingua_universale.types import MessageKind
        step = StepNode("worker", "returns", "regina", "result", LOC)
        assert compiler._step_to_message_kind(step) == MessageKind.TASK_RESULT

    def test_returns_verdict_audit_verdict(self, compiler: ASTCompiler) -> None:
        from cervellaswarm_lingua_universale.types import MessageKind
        step = StepNode("guardiana", "returns", "regina", "verdict", LOC)
        assert compiler._step_to_message_kind(step) == MessageKind.AUDIT_VERDICT

    def test_returns_plan_plan_proposal(self, compiler: ASTCompiler) -> None:
        from cervellaswarm_lingua_universale.types import MessageKind
        step = StepNode("architect", "returns", "regina", "plan", LOC)
        assert compiler._step_to_message_kind(step) == MessageKind.PLAN_PROPOSAL

    def test_returns_report_research_report(self, compiler: ASTCompiler) -> None:
        from cervellaswarm_lingua_universale.types import MessageKind
        step = StepNode("researcher", "returns", "regina", "research report", LOC)
        assert compiler._step_to_message_kind(step) == MessageKind.RESEARCH_REPORT

    def test_tells_decision_plan_decision(self, compiler: ASTCompiler) -> None:
        from cervellaswarm_lingua_universale.types import MessageKind
        step = StepNode("regina", "tells", "architect", "decision", LOC)
        assert compiler._step_to_message_kind(step) == MessageKind.PLAN_DECISION

    def test_tells_default_dm(self, compiler: ASTCompiler) -> None:
        from cervellaswarm_lingua_universale.types import MessageKind
        step = StepNode("regina", "tells", "worker", "update", LOC)
        assert compiler._step_to_message_kind(step) == MessageKind.DM

    def test_proposes_plan_proposal(self, compiler: ASTCompiler) -> None:
        from cervellaswarm_lingua_universale.types import MessageKind
        step = StepNode("architect", "proposes", "regina", "architecture", LOC)
        assert compiler._step_to_message_kind(step) == MessageKind.PLAN_PROPOSAL

    def test_sends_shutdown(self, compiler: ASTCompiler) -> None:
        from cervellaswarm_lingua_universale.types import MessageKind
        step = StepNode("regina", "sends", "worker", "shutdown signal", LOC)
        assert compiler._step_to_message_kind(step) == MessageKind.SHUTDOWN_REQUEST

    def test_sends_broadcast(self, compiler: ASTCompiler) -> None:
        from cervellaswarm_lingua_universale.types import MessageKind
        step = StepNode("regina", "sends", "worker", "broadcast update", LOC)
        assert compiler._step_to_message_kind(step) == MessageKind.BROADCAST

    def test_sends_context(self, compiler: ASTCompiler) -> None:
        from cervellaswarm_lingua_universale.types import MessageKind
        step = StepNode("regina", "sends", "worker", "context info", LOC)
        assert compiler._step_to_message_kind(step) == MessageKind.CONTEXT_INJECT

    def test_sends_default_dm(self, compiler: ASTCompiler) -> None:
        from cervellaswarm_lingua_universale.types import MessageKind
        step = StepNode("regina", "sends", "worker", "message", LOC)
        assert compiler._step_to_message_kind(step) == MessageKind.DM

    def test_unknown_action_dm(self, compiler: ASTCompiler) -> None:
        from cervellaswarm_lingua_universale.types import MessageKind
        step = StepNode("regina", "unknown_verb", "worker", "payload", LOC)
        assert compiler._step_to_message_kind(step) == MessageKind.DM

    def test_payload_case_insensitive(self, compiler: ASTCompiler) -> None:
        """Payload matching is case-insensitive."""
        from cervellaswarm_lingua_universale.types import MessageKind
        step = StepNode("regina", "asks", "guardiana", "VERIFY CODE", LOC)
        assert compiler._step_to_message_kind(step) == MessageKind.AUDIT_REQUEST


# ===================================================================
# _ast_to_protocol
# ===================================================================


class TestAstToProtocol:
    """Tests for ProtocolNode AST -> Protocol runtime object transformation."""

    def test_basic_protocol(self, compiler: ASTCompiler) -> None:
        from cervellaswarm_lingua_universale.protocols import Protocol
        node = _delegate_task_node()
        proto = compiler._ast_to_protocol(node)
        assert isinstance(proto, Protocol)
        assert proto.name == "DelegateTask"
        assert proto.roles == ("regina", "worker", "guardiana")
        assert len(proto.elements) == 4

    def test_step_sender_receiver(self, compiler: ASTCompiler) -> None:
        from cervellaswarm_lingua_universale.protocols import ProtocolStep
        node = _delegate_task_node()
        proto = compiler._ast_to_protocol(node)
        first = proto.elements[0]
        assert isinstance(first, ProtocolStep)
        assert first.sender == "regina"
        assert first.receiver == "worker"

    def test_step_description(self, compiler: ASTCompiler) -> None:
        node = _delegate_task_node()
        proto = compiler._ast_to_protocol(node)
        assert proto.elements[0].description == "do task"
        assert proto.elements[1].description == "result"

    def test_protocol_with_choice(self, compiler: ASTCompiler) -> None:
        from cervellaswarm_lingua_universale.protocols import ProtocolChoice
        node = ProtocolNode(
            name="WithChoice",
            roles=("regina", "worker"),
            steps=(
                StepNode("regina", "asks", "worker", "do task", LOC),
                ChoiceNode(
                    decider="regina",
                    branches=(
                        BranchNode("accept", (
                            StepNode("regina", "tells", "worker", "decision", LOC),
                        ), LOC),
                        BranchNode("reject", (
                            StepNode("regina", "tells", "worker", "decision", LOC),
                        ), LOC),
                    ),
                    loc=LOC,
                ),
            ),
            properties=(),
            loc=LOC,
        )
        proto = compiler._ast_to_protocol(node)
        assert len(proto.elements) == 2
        choice = proto.elements[1]
        assert isinstance(choice, ProtocolChoice)
        assert choice.decider == "regina"
        assert "accept" in choice.branches
        assert "reject" in choice.branches
        assert len(choice.branches["accept"]) == 1


# ===================================================================
# _compile_protocol
# ===================================================================


class TestCompileProtocol:
    """Tests for full protocol compilation."""

    def test_generates_protocol_constant(self, compiler: ASTCompiler) -> None:
        node = _delegate_task_node()
        lines = compiler._compile_protocol(node)
        joined = "\n".join(lines)
        assert "DELEGATETASK = Protocol(" in joined

    def test_generates_role_classes(self, compiler: ASTCompiler) -> None:
        node = _delegate_task_node()
        lines = compiler._compile_protocol(node)
        joined = "\n".join(lines)
        # Role classes are prefixed with protocol name to avoid collision
        assert "class DelegateTaskReginaRole:" in joined
        assert "class DelegateTaskWorkerRole:" in joined
        assert "class DelegateTaskGuardianaRole:" in joined

    def test_generates_session_class(self, compiler: ASTCompiler) -> None:
        node = _delegate_task_node()
        lines = compiler._compile_protocol(node)
        joined = "\n".join(lines)
        # Session class prefixed with protocol name
        assert "class DelegateTaskSession:" in joined

    def test_source_annotation(self, compiler: ASTCompiler) -> None:
        node = _delegate_task_node(loc=Loc(10, 0))
        lines = compiler._compile_protocol(node)
        assert "# [LU:10:0]" in lines[0]

    def test_via_dispatch(self, compiler: ASTCompiler) -> None:
        node = _delegate_task_node()
        lines = compiler._compile_declaration(node)
        joined = "\n".join(lines)
        assert "DELEGATETASK = Protocol(" in joined

    def test_message_kind_mapping_in_output(self, compiler: ASTCompiler) -> None:
        node = _delegate_task_node()
        lines = compiler._compile_protocol(node)
        joined = "\n".join(lines)
        assert "MessageKind.TASK_REQUEST" in joined
        assert "MessageKind.TASK_RESULT" in joined
        assert "MessageKind.AUDIT_REQUEST" in joined
        assert "MessageKind.AUDIT_VERDICT" in joined


# ===================================================================
# Preamble imports
# ===================================================================


class TestProtocolPreambleImports:
    """Protocol compilation registers correct preamble imports."""

    def test_registers_protocol_imports(self, compiler: ASTCompiler) -> None:
        node = _delegate_task_node()
        compiler._compile_protocol(node)
        preamble = "\n".join(compiler._preamble_imports)
        assert "Protocol" in preamble
        assert "ProtocolStep" in preamble
        assert "MessageKind" in preamble
        assert "SessionChecker" in preamble

    def test_registers_message_dataclass_imports(self, compiler: ASTCompiler) -> None:
        """Used message dataclasses are imported."""
        node = _delegate_task_node()
        compiler._compile_protocol(node)
        preamble = "\n".join(compiler._preamble_imports)
        assert "TaskRequest" in preamble
        assert "TaskResult" in preamble
        assert "AuditRequest" in preamble
        assert "AuditVerdict" in preamble

    def test_registers_optional_import(self, compiler: ASTCompiler) -> None:
        node = _delegate_task_node()
        compiler._compile_protocol(node)
        preamble = "\n".join(compiler._preamble_imports)
        assert "Optional" in preamble


# ===================================================================
# Choice protocol
# ===================================================================


class TestCompileProtocolChoice:
    """Protocol with ChoiceNode generates ProtocolChoice in output."""

    def _choice_node(self) -> ProtocolNode:
        return ProtocolNode(
            name="PlanReview",
            roles=("regina", "architect"),
            steps=(
                StepNode("regina", "asks", "architect", "plan", Loc(3, 4)),
                StepNode("architect", "returns", "regina", "proposal", Loc(4, 4)),
                ChoiceNode(
                    decider="regina",
                    branches=(
                        BranchNode("approve", (
                            StepNode("regina", "tells", "architect", "decision approved", Loc(7, 8)),
                        ), Loc(6, 8)),
                        BranchNode("revise", (
                            StepNode("regina", "tells", "architect", "decision revise", Loc(9, 8)),
                        ), Loc(8, 8)),
                    ),
                    loc=Loc(5, 4),
                ),
            ),
            properties=(),
            loc=Loc(1, 0),
        )

    def test_choice_in_output(self, compiler: ASTCompiler) -> None:
        lines = compiler._compile_protocol(self._choice_node())
        joined = "\n".join(lines)
        assert "ProtocolChoice(" in joined

    def test_branch_names_in_output(self, compiler: ASTCompiler) -> None:
        lines = compiler._compile_protocol(self._choice_node())
        joined = "\n".join(lines)
        assert '"approve"' in joined
        assert '"revise"' in joined

    def test_choose_branch_method(self, compiler: ASTCompiler) -> None:
        lines = compiler._compile_protocol(self._choice_node())
        joined = "\n".join(lines)
        assert "choose_branch" in joined

    def test_valid_python(self, compiler: ASTCompiler) -> None:
        prog = ProgramNode((self._choice_node(),), LOC)
        result = compiler.compile(prog, source_file="choice.lu")
        compile(result.python_source, "choice.lu", "exec")


# ===================================================================
# Full program with protocol
# ===================================================================


class TestCompileProtocolFullProgram:
    """Protocol compilation in a full program context."""

    def test_protocol_in_compiled_module(self, compiler: ASTCompiler) -> None:
        prog = ProgramNode((_delegate_task_node(),), LOC)
        result = compiler.compile(prog, source_file="proto.lu")
        assert result.protocols == ("DelegateTask",)

    def test_valid_python(self, compiler: ASTCompiler) -> None:
        prog = ProgramNode((_delegate_task_node(),), LOC)
        result = compiler.compile(prog, source_file="proto.lu")
        compile(result.python_source, "proto.lu", "exec")

    def test_mixed_program_valid_python(self, compiler: ASTCompiler) -> None:
        """Program with use, types, agent, and protocol."""
        prog = ProgramNode(
            (
                UseNode("math", None, Loc(1, 0)),
                VariantTypeDecl("Status", ("Active", "Inactive"), Loc(3, 0)),
                AgentNode("Worker", "backend", "standard", (), (), (), (), Loc(5, 0)),
                _delegate_task_node(loc=Loc(10, 0)),
            ),
            LOC,
        )
        result = compiler.compile(prog, source_file="mixed.lu")
        assert result.agents == ("Worker",)
        assert result.protocols == ("DelegateTask",)
        assert result.imports == ("math",)
        assert "import math" in result.python_source
        assert "class Worker:" in result.python_source
        assert "DELEGATETASK = Protocol(" in result.python_source
        compile(result.python_source, "mixed.lu", "exec")

    def test_two_protocols_in_program(self, compiler: ASTCompiler) -> None:
        proto1 = _delegate_task_node(loc=Loc(1, 0))
        proto2 = ProtocolNode(
            name="PeerChat",
            roles=("alice", "bob"),
            steps=(
                StepNode("alice", "sends", "bob", "message", Loc(10, 4)),
                StepNode("bob", "sends", "alice", "message", Loc(11, 4)),
            ),
            properties=(),
            loc=Loc(8, 0),
        )
        prog = ProgramNode((proto1, proto2), LOC)
        result = compiler.compile(prog, source_file="multi.lu")
        assert result.protocols == ("DelegateTask", "PeerChat")
        compile(result.python_source, "multi.lu", "exec")

    def test_two_protocols_no_class_collision(self, compiler: ASTCompiler) -> None:
        """Regression F1: two protocols with shared role must not collide."""
        proto1 = ProtocolNode(
            name="TaskFlow",
            roles=("regina", "worker"),
            steps=(
                StepNode("regina", "asks", "worker", "do task", Loc(2, 4)),
                StepNode("worker", "returns", "regina", "result", Loc(3, 4)),
            ),
            properties=(),
            loc=Loc(1, 0),
        )
        proto2 = ProtocolNode(
            name="AuditFlow",
            roles=("regina", "guardiana"),
            steps=(
                StepNode("regina", "asks", "guardiana", "audit code", Loc(6, 4)),
                StepNode("guardiana", "returns", "regina", "verdict", Loc(7, 4)),
            ),
            properties=(),
            loc=Loc(5, 0),
        )
        prog = ProgramNode((proto1, proto2), LOC)
        result = compiler.compile(prog, source_file="collision.lu")
        src = result.python_source
        # Both "regina" roles exist with unique prefixed class names
        assert "class TaskFlowReginaRole:" in src
        assert "class AuditFlowReginaRole:" in src
        assert "class TaskFlowSession:" in src
        assert "class AuditFlowSession:" in src
        compile(src, "collision.lu", "exec")

    def test_properties_emitted_as_comments(self, compiler: ASTCompiler) -> None:
        """Declared properties appear as comments in generated code."""
        from cervellaswarm_lingua_universale._ast import AlwaysTerminates, NoDeadlock
        node = ProtocolNode(
            name="SafeTask",
            roles=("regina", "worker"),
            steps=(
                StepNode("regina", "asks", "worker", "do task", Loc(3, 4)),
                StepNode("worker", "returns", "regina", "result", Loc(4, 4)),
            ),
            properties=(AlwaysTerminates(LOC), NoDeadlock(LOC)),
            loc=Loc(1, 0),
        )
        lines = compiler._compile_protocol(node)
        joined = "\n".join(lines)
        assert "Declared properties (2):" in joined
        assert "AlwaysTerminates" in joined
        assert "NoDeadlock" in joined

    def test_preamble_imports_in_output(self, compiler: ASTCompiler) -> None:
        prog = ProgramNode((_delegate_task_node(),), LOC)
        result = compiler.compile(prog, source_file="test.lu")
        src = result.python_source
        assert "from cervellaswarm_lingua_universale.types import MessageKind" in src
        assert "from cervellaswarm_lingua_universale.protocols import" in src
        assert "from cervellaswarm_lingua_universale.checker import" in src
