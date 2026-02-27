# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Golden interop tests for the full .lu -> Python pipeline (C2.3.5).

End-to-end round-trip tests through the **interop** API:
  compile_file() -> load_module() / load_file() / save_module()

Unlike test_compiler_golden.py (C2.2.6) which tests the raw compiler,
these tests exercise the full file I/O + runtime pipeline.

10 canonical scenarios:
  I1.   Variant type via load_file
  I2.   Record type instantiation
  I3.   use python math -> math.sqrt(4)  [P1 CRITICO]
  I4.   Agent requires contract violation
  I5.   Agent ensures contract violation
  I6.   Agent contracts pass (happy path)
  I7.   Protocol session full exchange via load_file
  I8.   compile_file -> save_module -> import saved .py
  I9.   Multi-module: load same source twice independently
  I10.  __all__ filtering: mixed program exports
"""

from __future__ import annotations

import importlib.util
import sys
import textwrap
from pathlib import Path

import pytest

from cervellaswarm_lingua_universale._contracts import ContractViolation
from cervellaswarm_lingua_universale._interop import (
    compile_file,
    load_file,
    load_module,
    save_module,
)


# ============================================================
# Shared .lu sources
# ============================================================

VARIANT_SOURCE = textwrap.dedent("""\
    type Status = Active | Inactive | Pending
""")

RECORD_SOURCE = textwrap.dedent("""\
    type TaskData =
        name: str
        priority: int
        tags: List[str]
        notes: str?
""")

USE_MATH_SOURCE = textwrap.dedent("""\
    use python math
""")

AGENT_WITH_CONTRACTS = textwrap.dedent("""\
    type TaskStatus = Pending | Done

    agent Worker:
        role: executor
        accepts: task_request
        requires: priority > 0
        ensures: result.valid
""")

PROTOCOL_SOURCE = textwrap.dedent("""\
    protocol DelegateTask:
        roles: regina, worker, guardiana

        regina asks worker to do task
        worker returns result to regina
        regina asks guardiana to verify result
        guardiana returns verdict to regina
""")

MIXED_PROGRAM = textwrap.dedent("""\
    use python math

    type Color = Red | Green | Blue

    type Config =
        name: str
        value: int

    agent Painter:
        role: creator
        accepts: paint_request
        requires: color.valid
        ensures: result.done

    protocol PaintJob:
        roles: regina, painter

        regina asks painter to do paint
        painter returns result to regina
""")

MULTI_CONTRACT_AGENT = textwrap.dedent("""\
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


# ============================================================
# I1. Variant type via load_file
# ============================================================


class TestI1VariantType:
    """I1: .lu with variant type -> load_file -> access Literal alias."""

    def test_load_variant(self, tmp_path: Path) -> None:
        lu = tmp_path / "status.lu"
        lu.write_text(VARIANT_SOURCE, encoding="utf-8")

        mod = load_file(lu)
        assert hasattr(mod, "Status")

    def test_module_metadata(self, tmp_path: Path) -> None:
        lu = tmp_path / "status.lu"
        lu.write_text(VARIANT_SOURCE, encoding="utf-8")

        mod = load_file(lu)
        assert mod.__lu_version__ == "0.2"
        assert mod.__lu_source__ == "status.lu"

    def test_module_name_from_filename(self, tmp_path: Path) -> None:
        lu = tmp_path / "my_status.lu"
        lu.write_text(VARIANT_SOURCE, encoding="utf-8")

        mod = load_file(lu)
        assert mod.__name__ == "my_status"

    def test_all_contains_status(self, tmp_path: Path) -> None:
        lu = tmp_path / "status.lu"
        lu.write_text(VARIANT_SOURCE, encoding="utf-8")

        mod = load_file(lu)
        assert mod.__all__ == ["Status"]


# ============================================================
# I2. Record type instantiation
# ============================================================


class TestI2RecordType:
    """I2: .lu with record type -> load_file -> create instance."""

    def test_load_record(self, tmp_path: Path) -> None:
        lu = tmp_path / "task_data.lu"
        lu.write_text(RECORD_SOURCE, encoding="utf-8")

        mod = load_file(lu)
        assert hasattr(mod, "TaskData")

    def test_create_instance(self, tmp_path: Path) -> None:
        lu = tmp_path / "task_data.lu"
        lu.write_text(RECORD_SOURCE, encoding="utf-8")

        mod = load_file(lu)
        td = mod.TaskData(name="test", priority=1, tags=["a", "b"], notes=None)
        assert td.name == "test"
        assert td.priority == 1
        assert td.tags == ["a", "b"]
        assert td.notes is None

    def test_record_is_frozen(self, tmp_path: Path) -> None:
        lu = tmp_path / "task_data.lu"
        lu.write_text(RECORD_SOURCE, encoding="utf-8")

        mod = load_file(lu)
        td = mod.TaskData(name="x", priority=1, tags=[], notes=None)
        with pytest.raises(AttributeError):
            td.name = "y"  # type: ignore[misc]


# ============================================================
# I3. use python math -> math.sqrt(4)  [P1 CRITICO]
# ============================================================


class TestI3UsePythonMath:
    """I3: P1 CRITICO -- `use python math` produces a live math module."""

    def test_math_imported(self, tmp_path: Path) -> None:
        lu = tmp_path / "with_math.lu"
        lu.write_text(USE_MATH_SOURCE, encoding="utf-8")

        mod = load_file(lu)
        assert hasattr(mod, "math")

    def test_math_sqrt(self, tmp_path: Path) -> None:
        """The critical test: math.sqrt(4) == 2.0 from loaded .lu module."""
        lu = tmp_path / "with_math.lu"
        lu.write_text(USE_MATH_SOURCE, encoding="utf-8")

        mod = load_file(lu)
        assert mod.math.sqrt(4) == 2.0

    def test_math_pi(self, tmp_path: Path) -> None:
        import math

        lu = tmp_path / "with_math.lu"
        lu.write_text(USE_MATH_SOURCE, encoding="utf-8")

        mod = load_file(lu)
        assert mod.math.pi == math.pi

    def test_math_is_stdlib_module(self, tmp_path: Path) -> None:
        """The imported math is THE stdlib math, not a copy."""
        import math

        lu = tmp_path / "with_math.lu"
        lu.write_text(USE_MATH_SOURCE, encoding="utf-8")

        mod = load_file(lu)
        assert mod.math is math


# ============================================================
# I4. Agent requires contract violation
# ============================================================


class TestI4RequiresViolation:
    """I4: Agent with requires contract -- violation at runtime."""

    def test_requires_violation(self, tmp_path: Path) -> None:
        lu = tmp_path / "worker.lu"
        lu.write_text(AGENT_WITH_CONTRACTS, encoding="utf-8")

        mod = load_file(lu)
        worker = mod.Worker()
        with pytest.raises(ContractViolation, match="requires violated"):
            worker.process(priority=0, result=None)

    def test_requires_violation_negative(self, tmp_path: Path) -> None:
        lu = tmp_path / "worker.lu"
        lu.write_text(AGENT_WITH_CONTRACTS, encoding="utf-8")

        mod = load_file(lu)
        worker = mod.Worker()
        with pytest.raises(ContractViolation, match="requires violated"):
            worker.process(priority=-5, result=None)


# ============================================================
# I5. Agent ensures contract violation
# ============================================================


class TestI5EnsuresViolation:
    """I5: Agent with ensures contract -- postcondition fails."""

    def test_ensures_violation(self, tmp_path: Path) -> None:
        lu = tmp_path / "worker.lu"
        lu.write_text(AGENT_WITH_CONTRACTS, encoding="utf-8")

        mod = load_file(lu)

        class ConcreteWorker(mod.Worker):
            def _execute(self, **kwargs):
                return kwargs

        cw = ConcreteWorker()
        bad_result = type("R", (), {"valid": False})()
        with pytest.raises(ContractViolation, match="ensures violated"):
            cw.process(priority=1, result=bad_result)


# ============================================================
# I6. Agent contracts pass (happy path)
# ============================================================


class TestI6ContractsPass:
    """I6: Agent contracts satisfied -- process completes."""

    def test_contracts_pass(self, tmp_path: Path) -> None:
        lu = tmp_path / "worker.lu"
        lu.write_text(AGENT_WITH_CONTRACTS, encoding="utf-8")

        mod = load_file(lu)

        class ConcreteWorker(mod.Worker):
            def _execute(self, **kwargs):
                return kwargs

        cw = ConcreteWorker()
        good_result = type("R", (), {"valid": True})()
        # Should not raise
        cw.process(priority=1, result=good_result)

    def test_agent_metadata(self, tmp_path: Path) -> None:
        lu = tmp_path / "worker.lu"
        lu.write_text(AGENT_WITH_CONTRACTS, encoding="utf-8")

        mod = load_file(lu)
        assert mod.Worker.__lu_role__ == "executor"
        assert mod.Worker.__lu_accepts__ == ("task_request",)

    def test_multi_contract_pass(self, tmp_path: Path) -> None:
        """Multi-line requires/ensures all satisfied."""
        lu = tmp_path / "analyst.lu"
        lu.write_text(MULTI_CONTRACT_AGENT, encoding="utf-8")

        mod = load_file(lu)

        class ConcreteAnalyst(mod.Analyst):
            def _execute(self, **kwargs):
                return kwargs

        ca = ConcreteAnalyst()
        good_query = type("Q", (), {"valid": True, "length": 10})()
        good_result = type("R", (), {"complete": True, "score": 8})()
        # Should not raise
        ca.process(query=good_query, result=good_result)

    def test_multi_contract_requires_violation(self, tmp_path: Path) -> None:
        """Multi-line requires: second condition fails (query.length > 0)."""
        lu = tmp_path / "analyst.lu"
        lu.write_text(MULTI_CONTRACT_AGENT, encoding="utf-8")

        mod = load_file(lu)

        class ConcreteAnalyst(mod.Analyst):
            def _execute(self, **kwargs):
                return kwargs

        ca = ConcreteAnalyst()
        bad_query = type("Q", (), {"valid": True, "length": 0})()
        good_result = type("R", (), {"complete": True, "score": 8})()
        with pytest.raises(ContractViolation, match="requires violated"):
            ca.process(query=bad_query, result=good_result)

    def test_multi_contract_ensures_violation(self, tmp_path: Path) -> None:
        """Multi-line ensures: second condition fails (result.score > 5)."""
        lu = tmp_path / "analyst.lu"
        lu.write_text(MULTI_CONTRACT_AGENT, encoding="utf-8")

        mod = load_file(lu)

        class ConcreteAnalyst(mod.Analyst):
            def _execute(self, **kwargs):
                return kwargs

        ca = ConcreteAnalyst()
        good_query = type("Q", (), {"valid": True, "length": 10})()
        bad_result = type("R", (), {"complete": True, "score": 3})()
        with pytest.raises(ContractViolation, match="ensures violated"):
            ca.process(query=good_query, result=bad_result)


# ============================================================
# I7. Protocol session full exchange via load_file
# ============================================================


class TestI7ProtocolSession:
    """I7: Protocol session -- full message exchange from loaded module."""

    def test_session_available(self, tmp_path: Path) -> None:
        lu = tmp_path / "delegate.lu"
        lu.write_text(PROTOCOL_SOURCE, encoding="utf-8")

        mod = load_file(lu)
        assert hasattr(mod, "DelegateTaskSession")
        session = mod.DelegateTaskSession()
        assert not session.is_complete

    def test_full_exchange(self, tmp_path: Path) -> None:
        from cervellaswarm_lingua_universale.types import (
            AuditRequest,
            AuditVerdict,
            AuditVerdictType,
            TaskRequest,
            TaskResult,
            TaskStatus,
        )

        lu = tmp_path / "delegate.lu"
        lu.write_text(PROTOCOL_SOURCE, encoding="utf-8")

        mod = load_file(lu)
        session = mod.DelegateTaskSession()

        session.send("regina", "worker", TaskRequest(
            task_id="T1", description="do task",
        ))
        session.send("worker", "regina", TaskResult(
            task_id="T1", status=TaskStatus.OK, summary="done",
        ))
        session.send("regina", "guardiana", AuditRequest(
            audit_id="A1", target="T1",
        ))
        session.send("guardiana", "regina", AuditVerdict(
            audit_id="A1", verdict=AuditVerdictType.APPROVED, score=9.5,
            checked=("code quality",),
        ))
        assert session.is_complete

    def test_role_accessors(self, tmp_path: Path) -> None:
        lu = tmp_path / "delegate.lu"
        lu.write_text(PROTOCOL_SOURCE, encoding="utf-8")

        mod = load_file(lu)
        session = mod.DelegateTaskSession()
        assert hasattr(session, "regina")
        assert hasattr(session, "worker")
        assert hasattr(session, "guardiana")


# ============================================================
# I8. compile_file -> save_module -> import saved .py
# ============================================================


class TestI8SaveAndImport:
    """I8: Full pipeline -- .lu -> compile -> save .py -> import as Python."""

    def test_save_and_read(self, tmp_path: Path) -> None:
        lu = tmp_path / "mixed.lu"
        lu.write_text(MIXED_PROGRAM, encoding="utf-8")

        compiled = compile_file(lu)
        py_file = tmp_path / "mixed.py"
        save_module(compiled, py_file)

        saved = py_file.read_text(encoding="utf-8")
        assert saved == compiled.python_source

    def test_save_and_import(self, tmp_path: Path) -> None:
        """Import the saved .py file via importlib -- true Python interop.

        Uses a source *without* protocols because protocol-generated code
        imports from cervellaswarm_lingua_universale.checker/protocols/types
        which are only available when the package is installed and on the
        import path.  Types, agents, and use-statements are self-contained.
        """
        source = textwrap.dedent("""\
            use python math

            type Color = Red | Green | Blue

            type Config =
                name: str
                value: int
        """)
        lu = tmp_path / "importable.lu"
        lu.write_text(source, encoding="utf-8")

        compiled = compile_file(lu)
        py_file = tmp_path / "importable_gen.py"
        save_module(compiled, py_file)

        # Import via importlib (not exec)
        spec = importlib.util.spec_from_file_location("importable_gen", py_file)
        assert spec is not None
        assert spec.loader is not None
        imported = importlib.util.module_from_spec(spec)
        sys.modules["importable_gen"] = imported  # needed for @dataclass
        try:
            spec.loader.exec_module(imported)
        finally:
            sys.modules.pop("importable_gen", None)

        # Verify declarations accessible
        assert hasattr(imported, "Color")
        assert hasattr(imported, "Config")
        assert hasattr(imported, "math")
        assert imported.math.sqrt(16) == 4.0

        # Verify Config is a working dataclass
        cfg = imported.Config(name="test", value=42)
        assert cfg.name == "test"
        assert cfg.value == 42

    def test_save_overwrite(self, tmp_path: Path) -> None:
        """Save with overwrite=True replaces existing file."""
        lu = tmp_path / "variant.lu"
        lu.write_text(VARIANT_SOURCE, encoding="utf-8")

        compiled = compile_file(lu)
        py_file = tmp_path / "output.py"
        py_file.write_text("# old\n")

        save_module(compiled, py_file, overwrite=True)
        assert py_file.read_text(encoding="utf-8") == compiled.python_source

    def test_save_not_in_sys_modules(self, tmp_path: Path) -> None:
        """Imported module can be cleaned up from sys.modules."""
        lu = tmp_path / "variant.lu"
        lu.write_text(VARIANT_SOURCE, encoding="utf-8")

        compiled = compile_file(lu)
        py_file = tmp_path / "variant_gen_sys_test.py"
        save_module(compiled, py_file)

        mod_name = "variant_gen_sys_test_unique"
        spec = importlib.util.spec_from_file_location(mod_name, py_file)
        assert spec is not None
        assert spec.loader is not None
        imported = importlib.util.module_from_spec(spec)
        # Verify it's not auto-registered before exec
        assert mod_name not in sys.modules
        spec.loader.exec_module(imported)
        # Clean up if it was added
        sys.modules.pop(mod_name, None)


# ============================================================
# I9. Multi-module: load same source twice independently
# ============================================================


class TestI9MultiModule:
    """I9: Load the same .lu source twice -- modules are independent."""

    def test_independent_modules(self, tmp_path: Path) -> None:
        lu = tmp_path / "variant.lu"
        lu.write_text(VARIANT_SOURCE, encoding="utf-8")

        compiled = compile_file(lu)
        mod1 = load_module(compiled, module_name="mod_a")
        mod2 = load_module(compiled, module_name="mod_b")

        assert mod1 is not mod2
        assert mod1.__name__ == "mod_a"
        assert mod2.__name__ == "mod_b"

    def test_independent_namespaces(self, tmp_path: Path) -> None:
        """Modifying one module's namespace does not affect the other."""
        lu = tmp_path / "variant.lu"
        lu.write_text(VARIANT_SOURCE, encoding="utf-8")

        compiled = compile_file(lu)
        mod1 = load_module(compiled, module_name="ns_a")
        mod2 = load_module(compiled, module_name="ns_b")

        # Add an attribute to mod1 only
        mod1.extra = "only_in_mod1"
        assert not hasattr(mod2, "extra")

    def test_load_file_twice(self, tmp_path: Path) -> None:
        """load_file called twice returns independent modules."""
        lu = tmp_path / "variant.lu"
        lu.write_text(VARIANT_SOURCE, encoding="utf-8")

        mod1 = load_file(lu, module_name="lf_a")
        mod2 = load_file(lu, module_name="lf_b")

        assert mod1 is not mod2
        assert mod1.__name__ == "lf_a"
        assert mod2.__name__ == "lf_b"
        assert hasattr(mod1, "Status")
        assert hasattr(mod2, "Status")

    def test_sentinel_restore_existing_module(self, tmp_path: Path) -> None:
        """When module_name collides with sys.modules, the original is restored.

        P2 F1: Tests the sentinel restore path in load_module -- if a module
        with the same name already exists in sys.modules, it must be restored
        after exec() completes.
        """
        import types as stdlib_types

        lu = tmp_path / "record.lu"
        lu.write_text(RECORD_SOURCE, encoding="utf-8")

        compiled = compile_file(lu)

        # Pre-register a fake module with the target name
        fake = stdlib_types.ModuleType("_lu_sentinel_test")
        fake.marker = "original"
        sys.modules["_lu_sentinel_test"] = fake
        try:
            mod = load_module(compiled, module_name="_lu_sentinel_test")
            # Loaded module works (has record type)
            assert hasattr(mod, "TaskData")
            td = mod.TaskData(name="x", priority=1, tags=[], notes=None)
            assert td.name == "x"
            # Original module restored in sys.modules
            assert sys.modules["_lu_sentinel_test"] is fake
            assert sys.modules["_lu_sentinel_test"].marker == "original"
        finally:
            sys.modules.pop("_lu_sentinel_test", None)


# ============================================================
# I10. __all__ filtering: mixed program exports
# ============================================================


class TestI10AllExports:
    """I10: __all__ in loaded module matches expected exports."""

    def test_all_contains_user_types(self, tmp_path: Path) -> None:
        lu = tmp_path / "mixed.lu"
        lu.write_text(MIXED_PROGRAM, encoding="utf-8")

        mod = load_file(lu)
        # Types + agents + session (but NOT imports like math)
        assert "Color" in mod.__all__
        assert "Config" in mod.__all__
        assert "Painter" in mod.__all__
        assert "PaintJobSession" in mod.__all__

    def test_all_excludes_imports(self, tmp_path: Path) -> None:
        """Imports (use python math) should NOT be in __all__."""
        lu = tmp_path / "mixed.lu"
        lu.write_text(MIXED_PROGRAM, encoding="utf-8")

        mod = load_file(lu)
        assert "math" not in mod.__all__

    def test_all_matches_compiled_exports(self, tmp_path: Path) -> None:
        """Module __all__ matches CompiledModule.exports exactly."""
        lu = tmp_path / "mixed.lu"
        lu.write_text(MIXED_PROGRAM, encoding="utf-8")

        compiled = compile_file(lu)
        mod = load_module(compiled)
        assert list(mod.__all__) == list(compiled.exports)

    def test_variant_only_exports(self, tmp_path: Path) -> None:
        """Simple variant: __all__ has exactly the type name."""
        lu = tmp_path / "variant.lu"
        lu.write_text(VARIANT_SOURCE, encoding="utf-8")

        mod = load_file(lu)
        assert mod.__all__ == ["Status"]

    def test_agent_exports_include_type_and_agent(self, tmp_path: Path) -> None:
        """Agent source: __all__ includes both types and agents."""
        lu = tmp_path / "worker.lu"
        lu.write_text(AGENT_WITH_CONTRACTS, encoding="utf-8")

        mod = load_file(lu)
        assert "TaskStatus" in mod.__all__
        assert "Worker" in mod.__all__
