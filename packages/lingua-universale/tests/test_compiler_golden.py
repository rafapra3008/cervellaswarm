# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Golden file tests for the full compilation pipeline (C2.2.6).

Round-trip tests: source text -> parse() -> compile() -> exec().
Each test starts from Lingua Universale source text, not hand-built AST.

10 canonical examples covering:
  G1.  Simple variant type
  G2.  Record type with optional/generic fields
  G3.  Use statement (with and without alias)
  G4.  Agent with contracts (requires + ensures)
  G5.  Simple protocol (DelegateTask)
  G6.  Protocol with properties
  G7.  Mixed program: use + type + agent + protocol
  G8.  Agent with block-form contracts (multi-line requires/ensures)
  G9.  Protocol with choice (when ... decides)
  G10. Two protocols -- no class name collision
"""

from __future__ import annotations

import textwrap

import pytest

from cervellaswarm_lingua_universale._compiler import ASTCompiler, CompiledModule
from cervellaswarm_lingua_universale._parser import parse


def _roundtrip(source: str, filename: str = "golden.lu") -> CompiledModule:
    """Parse source text and compile to Python."""
    program = parse(source)
    compiler = ASTCompiler()
    return compiler.compile(program, source_file=filename)


def _exec_source(result: CompiledModule) -> dict:
    """Execute compiled Python and return the namespace."""
    ns: dict = {}
    exec(compile(result.python_source, result.source_file, "exec"), ns)  # noqa: S102
    return ns


# ============================================================
# G1. Simple variant type
# ============================================================


class TestGoldenVariantType:
    """Variant type: type Status = Active | Inactive | Pending."""

    SOURCE = textwrap.dedent("""\
        type Status = Active | Inactive | Pending
    """)

    def test_compiles(self) -> None:
        result = _roundtrip(self.SOURCE, "variant.lu")
        assert result.source_file == "variant.lu"
        assert result.agents == ()
        assert result.protocols == ()
        assert result.types == ("Status",)
        assert result.exports == ("Status",)

    def test_generates_literal(self) -> None:
        result = _roundtrip(self.SOURCE)
        assert 'Status = Literal["Active", "Inactive", "Pending"]' in result.python_source

    def test_loc_annotation(self) -> None:
        result = _roundtrip(self.SOURCE)
        assert "# [LU:1:0]" in result.python_source

    def test_metadata(self) -> None:
        result = _roundtrip(self.SOURCE, "variant.lu")
        assert '__lu_version__' in result.python_source
        assert '__lu_source__ = "variant.lu"' in result.python_source
        assert '__all__ = ["Status"]' in result.python_source

    def test_exec_roundtrip(self) -> None:
        result = _roundtrip(self.SOURCE)
        ns = _exec_source(result)
        # Literal type alias is accessible in the namespace
        assert "Status" in ns
        assert ns["__lu_version__"] == "0.2"


# ============================================================
# G2. Record type with optional/generic fields
# ============================================================


class TestGoldenRecordType:
    """Record type with various field types."""

    SOURCE = textwrap.dedent("""\
        type TaskData =
            name: str
            priority: int
            tags: List[str]
            notes: str?
            confidence: Confident[str]
    """)

    def test_compiles(self) -> None:
        result = _roundtrip(self.SOURCE, "record.lu")
        assert result.agents == ()
        assert result.protocols == ()
        assert result.types == ("TaskData",)
        assert result.exports == ("TaskData",)

    def test_generates_dataclass(self) -> None:
        result = _roundtrip(self.SOURCE)
        src = result.python_source
        assert "@dataclass(frozen=True)" in src
        assert "class TaskData:" in src
        assert "name: str" in src
        assert "priority: int" in src
        assert "tags: list[str]" in src
        assert "notes: str | None" in src

    def test_confident_field(self) -> None:
        result = _roundtrip(self.SOURCE)
        assert 'confidence: Confident[str]' in result.python_source

    def test_preamble_imports(self) -> None:
        result = _roundtrip(self.SOURCE)
        src = result.python_source
        assert "from dataclasses import dataclass" in src
        assert "from cervellaswarm_lingua_universale.confidence import Confident" in src

    def test_exec_roundtrip(self) -> None:
        result = _roundtrip(self.SOURCE)
        ns = _exec_source(result)
        # Create an instance of the record
        td = ns["TaskData"](
            name="test", priority=1, tags=["a"], notes=None, confidence="high",
        )
        assert td.name == "test"
        assert td.priority == 1
        assert td.tags == ["a"]
        assert td.notes is None
        assert td.confidence == "high"


# ============================================================
# G3. Use statement (with and without alias)
# ============================================================


class TestGoldenUseStatement:
    """Use statements compile to Python imports."""

    SOURCE = textwrap.dedent("""\
        use python os.path
        use python json as json_lib
    """)

    def test_compiles(self) -> None:
        result = _roundtrip(self.SOURCE, "use.lu")
        assert result.imports == ("os.path", "json")

    def test_generates_imports(self) -> None:
        result = _roundtrip(self.SOURCE)
        src = result.python_source
        assert "import os.path" in src
        assert "import json as json_lib" in src

    def test_loc_annotations(self) -> None:
        result = _roundtrip(self.SOURCE)
        src = result.python_source
        assert "# [LU:1:0]" in src
        assert "# [LU:2:0]" in src

    def test_exec_roundtrip(self) -> None:
        result = _roundtrip(self.SOURCE)
        ns = _exec_source(result)
        import os.path
        assert ns["os"].path is os.path


# ============================================================
# G4. Agent with contracts (inline requires/ensures)
# ============================================================


class TestGoldenAgentContracts:
    """Agent with role, trust, accepts, produces, requires, ensures."""

    SOURCE = textwrap.dedent("""\
        agent Worker:
            role: backend
            trust: standard
            accepts: TaskRequest
            produces: TaskResult
            requires: task.well_defined
            ensures: result.done
    """)

    def test_compiles(self) -> None:
        result = _roundtrip(self.SOURCE, "agent.lu")
        assert result.agents == ("Worker",)
        assert result.protocols == ()

    def test_generates_class(self) -> None:
        result = _roundtrip(self.SOURCE)
        src = result.python_source
        assert "class Worker:" in src
        assert '__lu_role__ = "backend"' in src
        assert '__lu_trust__ = "standard"' in src
        assert '__lu_accepts__ = ("TaskRequest",)' in src
        assert '__lu_produces__ = ("TaskResult",)' in src

    def test_contract_guards(self) -> None:
        result = _roundtrip(self.SOURCE)
        src = result.python_source
        assert 'kwargs["task"].well_defined' in src
        assert 'kwargs["result"].done' in src
        assert "ContractViolation" in src

    def test_loc_from_real_source(self) -> None:
        """Loc annotations reflect real line numbers from parser."""
        result = _roundtrip(self.SOURCE)
        src = result.python_source
        # Agent is at line 1 in the source
        assert "# [LU:1:0]" in src

    def test_exec_roundtrip(self) -> None:
        result = _roundtrip(self.SOURCE)
        ns = _exec_source(result)
        worker_cls = ns["Worker"]
        assert worker_cls.__lu_role__ == "backend"
        assert worker_cls.__lu_trust__ == "standard"
        assert worker_cls.__lu_accepts__ == ("TaskRequest",)
        assert worker_cls.__lu_produces__ == ("TaskResult",)

    def test_contract_violation_at_runtime(self) -> None:
        """Requires contract raises ContractViolation at runtime."""
        from cervellaswarm_lingua_universale._contracts import ContractViolation

        result = _roundtrip(self.SOURCE)
        ns = _exec_source(result)

        # Subclass to provide _execute implementation
        class ConcreteWorker(ns["Worker"]):
            def _execute(self, **kwargs):
                return {"done": True}

        cw = ConcreteWorker()
        # requires: task.well_defined -- fails when False
        bad_task = type("Task", (), {"well_defined": False})()
        with pytest.raises(ContractViolation, match="task.well_defined"):
            cw.process(task=bad_task, result=type("R", (), {"done": True})())

    def test_ensures_violation_at_runtime(self) -> None:
        """Ensures contract raises ContractViolation at runtime."""
        from cervellaswarm_lingua_universale._contracts import ContractViolation

        result = _roundtrip(self.SOURCE)
        ns = _exec_source(result)

        class ConcreteWorker(ns["Worker"]):
            def _execute(self, **kwargs):
                return kwargs

        cw = ConcreteWorker()
        good_task = type("Task", (), {"well_defined": True})()
        # ensures: result.done -- fails when False
        bad_result = type("Result", (), {"done": False})()
        with pytest.raises(ContractViolation, match="result.done"):
            cw.process(task=good_task, result=bad_result)

    def test_contract_passes_at_runtime(self) -> None:
        """When contracts are satisfied, process() completes."""
        result = _roundtrip(self.SOURCE)
        ns = _exec_source(result)

        class ConcreteWorker(ns["Worker"]):
            def _execute(self, **kwargs):
                return kwargs

        cw = ConcreteWorker()
        good_task = type("Task", (), {"well_defined": True})()
        good_result = type("Result", (), {"done": True})()
        # Should not raise
        cw.process(task=good_task, result=good_result)


# ============================================================
# G5. Simple protocol (DelegateTask)
# ============================================================


class TestGoldenSimpleProtocol:
    """Standard DelegateTask protocol -- the canonical example."""

    SOURCE = textwrap.dedent("""\
        protocol DelegateTask:
            roles: regina, worker, guardiana

            regina asks worker to do task
            worker returns result to regina
            regina asks guardiana to verify result
            guardiana returns verdict to regina
    """)

    def test_compiles(self) -> None:
        result = _roundtrip(self.SOURCE, "delegate.lu")
        assert result.protocols == ("DelegateTask",)
        assert result.agents == ()

    def test_generates_protocol_constant(self) -> None:
        result = _roundtrip(self.SOURCE)
        src = result.python_source
        assert "DELEGATETASK = Protocol(" in src

    def test_generates_prefixed_role_classes(self) -> None:
        result = _roundtrip(self.SOURCE)
        src = result.python_source
        assert "class DelegateTaskReginaRole:" in src
        assert "class DelegateTaskWorkerRole:" in src
        assert "class DelegateTaskGuardianaRole:" in src

    def test_generates_session_class(self) -> None:
        result = _roundtrip(self.SOURCE)
        src = result.python_source
        assert "class DelegateTaskSession:" in src

    def test_preamble_imports(self) -> None:
        result = _roundtrip(self.SOURCE)
        src = result.python_source
        assert "from cervellaswarm_lingua_universale.types import MessageKind" in src
        assert "from cervellaswarm_lingua_universale.protocols import (" in src
        assert "from cervellaswarm_lingua_universale.checker import (" in src

    def test_exec_roundtrip(self) -> None:
        result = _roundtrip(self.SOURCE)
        ns = _exec_source(result)
        assert "DELEGATETASK" in ns
        assert "DelegateTaskSession" in ns
        assert "DelegateTaskReginaRole" in ns

    def test_session_runtime(self) -> None:
        """Session can be instantiated and has role accessors."""
        result = _roundtrip(self.SOURCE)
        ns = _exec_source(result)
        session = ns["DelegateTaskSession"]()
        assert hasattr(session, "regina")
        assert hasattr(session, "worker")
        assert hasattr(session, "guardiana")
        assert not session.is_complete

    def test_session_full_exchange(self) -> None:
        """Full message exchange completes the protocol session."""
        from cervellaswarm_lingua_universale.types import (
            AuditRequest,
            AuditVerdict,
            AuditVerdictType,
            TaskRequest,
            TaskResult,
            TaskStatus,
        )

        result = _roundtrip(self.SOURCE)
        ns = _exec_source(result)
        session = ns["DelegateTaskSession"]()

        # Step 1: regina asks worker to do task
        session.send("regina", "worker", TaskRequest(
            task_id="T1", description="do task",
        ))
        # Step 2: worker returns result to regina
        session.send("worker", "regina", TaskResult(
            task_id="T1", status=TaskStatus.OK, summary="done",
        ))
        # Step 3: regina asks guardiana to verify
        session.send("regina", "guardiana", AuditRequest(
            audit_id="A1", target="T1",
        ))
        # Step 4: guardiana returns verdict to regina
        session.send("guardiana", "regina", AuditVerdict(
            audit_id="A1", verdict=AuditVerdictType.APPROVED, score=9.5,
            checked=("code quality",),
        ))
        assert session.is_complete


# ============================================================
# G6. Protocol with properties
# ============================================================


class TestGoldenProtocolProperties:
    """Protocol with declared properties (always terminates, no deadlock)."""

    SOURCE = textwrap.dedent("""\
        protocol SafeHandoff:
            roles: regina, worker

            regina asks worker to do task
            worker returns result to regina

            properties:
                always terminates
                no deadlock
    """)

    def test_compiles(self) -> None:
        result = _roundtrip(self.SOURCE, "safe.lu")
        assert result.protocols == ("SafeHandoff",)

    def test_properties_as_comments(self) -> None:
        result = _roundtrip(self.SOURCE)
        src = result.python_source
        assert "Declared properties (2):" in src
        assert "AlwaysTerminates" in src
        assert "NoDeadlock" in src

    def test_exec_roundtrip(self) -> None:
        result = _roundtrip(self.SOURCE)
        ns = _exec_source(result)
        session = ns["SafeHandoffSession"]()
        assert not session.is_complete


# ============================================================
# G7. Mixed program: use + type + agent + protocol
# ============================================================


class TestGoldenMixedProgram:
    """Full program with all declaration types."""

    SOURCE = textwrap.dedent("""\
        use python math

        type TaskStatus = Pending | Running | Done

        type TaskInfo =
            name: str
            priority: int

        agent Worker:
            role: backend
            trust: standard
            accepts: TaskRequest
            produces: TaskResult
            requires: task.valid
            ensures: result.ok

        protocol SimpleTask:
            roles: regina, worker

            regina asks worker to do task
            worker returns result to regina
    """)

    def test_compiles(self) -> None:
        result = _roundtrip(self.SOURCE, "mixed.lu")
        assert result.imports == ("math",)
        assert result.agents == ("Worker",)
        assert result.protocols == ("SimpleTask",)
        assert result.types == ("TaskStatus", "TaskInfo")
        assert result.exports == ("TaskStatus", "TaskInfo", "Worker", "SimpleTaskSession")

    def test_all_declarations_present(self) -> None:
        result = _roundtrip(self.SOURCE)
        src = result.python_source
        # Use
        assert "import math" in src
        # Variant type
        assert 'TaskStatus = Literal["Pending", "Running", "Done"]' in src
        # Record type
        assert "class TaskInfo:" in src
        assert "name: str" in src
        # Agent
        assert "class Worker:" in src
        assert '__lu_role__ = "backend"' in src
        # Protocol
        assert "SIMPLETASK = Protocol(" in src
        assert "class SimpleTaskSession:" in src

    def test_exec_roundtrip(self) -> None:
        result = _roundtrip(self.SOURCE)
        ns = _exec_source(result)
        assert "TaskStatus" in ns
        assert "TaskInfo" in ns
        assert "Worker" in ns
        assert "SIMPLETASK" in ns
        assert "SimpleTaskSession" in ns
        # math module imported
        import math
        assert ns["math"] is math

    def test_order_preserved(self) -> None:
        """Declarations appear in source order in the generated Python."""
        result = _roundtrip(self.SOURCE)
        src = result.python_source
        # Find positions to verify order
        pos_import = src.index("import math")
        pos_status = src.index("TaskStatus = Literal")
        pos_info = src.index("class TaskInfo:")
        pos_worker = src.index("class Worker:")
        pos_proto = src.index("SIMPLETASK = Protocol(")
        assert pos_import < pos_status < pos_info < pos_worker < pos_proto


# ============================================================
# G8. Agent with block-form contracts
# ============================================================


class TestGoldenAgentBlockContracts:
    """Agent with multi-line requires/ensures blocks."""

    SOURCE = textwrap.dedent("""\
        agent Analyst:
            role: researcher
            trust: trusted
            accepts: ResearchQuery
            produces: ResearchReport
            requires:
                query.valid
                query.length > 0
            ensures:
                result.complete
                result.score > 5
    """)

    def test_compiles(self) -> None:
        result = _roundtrip(self.SOURCE, "analyst.lu")
        assert result.agents == ("Analyst",)

    def test_multiple_preconditions(self) -> None:
        result = _roundtrip(self.SOURCE)
        src = result.python_source
        assert 'kwargs["query"].valid' in src
        assert '(kwargs["query"].length) > (0)' in src

    def test_multiple_postconditions(self) -> None:
        result = _roundtrip(self.SOURCE)
        src = result.python_source
        assert 'kwargs["result"].complete' in src
        assert '(kwargs["result"].score) > (5)' in src

    def test_exec_roundtrip(self) -> None:
        result = _roundtrip(self.SOURCE)
        ns = _exec_source(result)
        analyst = ns["Analyst"]
        assert analyst.__lu_role__ == "researcher"
        assert analyst.__lu_trust__ == "trusted"

    def test_multi_contract_violation(self) -> None:
        """First failing precondition raises ContractViolation."""
        from cervellaswarm_lingua_universale._contracts import ContractViolation

        result = _roundtrip(self.SOURCE)
        ns = _exec_source(result)

        class ConcreteAnalyst(ns["Analyst"]):
            def _execute(self, **kwargs):
                return kwargs

        ca = ConcreteAnalyst()
        # query.valid = False -> first precondition fails
        bad_query = type("Q", (), {"valid": False, "length": 10})()
        with pytest.raises(ContractViolation, match="query.valid"):
            ca.process(
                query=bad_query,
                result=type("R", (), {"complete": True, "score": 8})(),
            )


# ============================================================
# G9. Protocol with choice (when ... decides)
# ============================================================


class TestGoldenProtocolChoice:
    """Protocol with choice branching."""

    SOURCE = textwrap.dedent("""\
        protocol ReviewTask:
            roles: regina, worker, guardiana

            regina asks worker to do task
            worker returns result to regina
            regina asks guardiana to verify result

            when guardiana decides:
                approve:
                    guardiana returns verdict to regina
                reject:
                    guardiana returns verdict to regina
                    regina asks worker to redo task
                    worker returns result to regina
    """)

    def test_compiles(self) -> None:
        result = _roundtrip(self.SOURCE, "review.lu")
        assert result.protocols == ("ReviewTask",)

    def test_generates_choice_structure(self) -> None:
        result = _roundtrip(self.SOURCE)
        src = result.python_source
        assert "REVIEWTASK = Protocol(" in src
        assert "class ReviewTaskSession:" in src

    def test_exec_roundtrip(self) -> None:
        result = _roundtrip(self.SOURCE)
        ns = _exec_source(result)
        assert "ReviewTaskSession" in ns
        assert "REVIEWTASK" in ns

    def test_session_with_choice(self) -> None:
        """Session handles choice branching at runtime."""
        from cervellaswarm_lingua_universale.types import (
            AuditRequest,
            AuditVerdict,
            AuditVerdictType,
            TaskRequest,
            TaskResult,
            TaskStatus,
        )

        result = _roundtrip(self.SOURCE)
        ns = _exec_source(result)
        session = ns["ReviewTaskSession"]()

        # Steps before choice
        session.send("regina", "worker", TaskRequest(
            task_id="T1", description="do task",
        ))
        session.send("worker", "regina", TaskResult(
            task_id="T1", status=TaskStatus.OK, summary="done",
        ))
        session.send("regina", "guardiana", AuditRequest(
            audit_id="A1", target="T1",
        ))

        # Choose "approve" branch
        session.choose_branch("approve")
        session.send("guardiana", "regina", AuditVerdict(
            audit_id="A1", verdict=AuditVerdictType.APPROVED, score=9.5,
            checked=("quality",),
        ))
        assert session.is_complete

    def test_session_reject_branch(self) -> None:
        """Reject branch exercises the longer path (3 extra steps)."""
        from cervellaswarm_lingua_universale.types import (
            AuditRequest,
            AuditVerdict,
            AuditVerdictType,
            TaskRequest,
            TaskResult,
            TaskStatus,
        )

        result = _roundtrip(self.SOURCE)
        ns = _exec_source(result)
        session = ns["ReviewTaskSession"]()

        # Steps before choice
        session.send("regina", "worker", TaskRequest(
            task_id="T1", description="do task",
        ))
        session.send("worker", "regina", TaskResult(
            task_id="T1", status=TaskStatus.OK, summary="done",
        ))
        session.send("regina", "guardiana", AuditRequest(
            audit_id="A1", target="T1",
        ))

        # Choose "reject" branch -- 3 steps: verdict + redo + result
        session.choose_branch("reject")
        session.send("guardiana", "regina", AuditVerdict(
            audit_id="A1", verdict=AuditVerdictType.NEEDS_REVISION, score=4.0,
            checked=("quality",), issues=("needs work",),
        ))
        session.send("regina", "worker", TaskRequest(
            task_id="T1-redo", description="redo task",
        ))
        session.send("worker", "regina", TaskResult(
            task_id="T1-redo", status=TaskStatus.OK, summary="redone",
        ))
        assert session.is_complete


# ============================================================
# G10. Two protocols -- no class name collision
# ============================================================


class TestGoldenTwoProtocols:
    """Two protocols sharing a role name -- prefixed classes avoid collision."""

    SOURCE = textwrap.dedent("""\
        protocol TaskFlow:
            roles: regina, worker

            regina asks worker to do task
            worker returns result to regina

        protocol AuditFlow:
            roles: regina, guardiana

            regina asks guardiana to verify code
            guardiana returns verdict to regina
    """)

    def test_compiles(self) -> None:
        result = _roundtrip(self.SOURCE, "two_protos.lu")
        assert result.protocols == ("TaskFlow", "AuditFlow")

    def test_no_collision(self) -> None:
        """Both protocols have uniquely prefixed role classes."""
        result = _roundtrip(self.SOURCE)
        src = result.python_source
        # TaskFlow roles
        assert "class TaskFlowReginaRole:" in src
        assert "class TaskFlowWorkerRole:" in src
        assert "class TaskFlowSession:" in src
        # AuditFlow roles
        assert "class AuditFlowReginaRole:" in src
        assert "class AuditFlowGuardianaRole:" in src
        assert "class AuditFlowSession:" in src

    def test_exec_roundtrip(self) -> None:
        """Both protocols compile and execute without namespace collision."""
        result = _roundtrip(self.SOURCE)
        ns = _exec_source(result)
        # Both protocol constants exist
        assert "TASKFLOW" in ns
        assert "AUDITFLOW" in ns
        # Both session classes exist
        assert "TaskFlowSession" in ns
        assert "AuditFlowSession" in ns
        # Both are instantiable
        s1 = ns["TaskFlowSession"]()
        s2 = ns["AuditFlowSession"]()
        assert not s1.is_complete
        assert not s2.is_complete

    def test_independent_sessions(self) -> None:
        """Two protocol sessions operate independently at runtime."""
        from cervellaswarm_lingua_universale.types import (
            AuditRequest,
            AuditVerdict,
            AuditVerdictType,
            TaskRequest,
            TaskResult,
            TaskStatus,
        )

        result = _roundtrip(self.SOURCE)
        ns = _exec_source(result)

        # Complete TaskFlow
        s1 = ns["TaskFlowSession"]()
        s1.send("regina", "worker", TaskRequest(
            task_id="T1", description="do task",
        ))
        s1.send("worker", "regina", TaskResult(
            task_id="T1", status=TaskStatus.OK, summary="done",
        ))
        assert s1.is_complete

        # Complete AuditFlow
        s2 = ns["AuditFlowSession"]()
        s2.send("regina", "guardiana", AuditRequest(
            audit_id="A1", target="code",
        ))
        s2.send("guardiana", "regina", AuditVerdict(
            audit_id="A1", verdict=AuditVerdictType.APPROVED, score=9.8,
            checked=("style",),
        ))
        assert s2.is_complete
