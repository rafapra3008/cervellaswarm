# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for _compile_agent (C2.2.4).

Test structure:
  - Minimal agent (name only, no clauses)
  - Metadata attributes (__lu_role__, __lu_trust__, __lu_accepts__, __lu_produces__)
  - Contract guards (requires -> preconditions, ensures -> postconditions)
  - Source annotations (# [LU:line:col])
  - ContractViolation preamble import
  - Confident[T] preamble import (P2 fix)
  - Keyword escaping in agent names
  - Full program with agent + other declarations
  - Generated code is valid Python (syntax check)
  - Generated code is executable (round-trip exec)
"""

from __future__ import annotations

import pytest

from cervellaswarm_lingua_universale._ast import (
    AgentNode,
    AttrExpr,
    BinOpExpr,
    GenericType,
    GroupExpr,
    IdentExpr,
    Loc,
    MethodCallExpr,
    NotExpr,
    NumberExpr,
    ProgramNode,
    RecordTypeDecl,
    SimpleType,
    StringExpr,
    UseNode,
    VariantTypeDecl,
)
from cervellaswarm_lingua_universale._compiler import ASTCompiler, CompiledModule


@pytest.fixture()
def compiler() -> ASTCompiler:
    return ASTCompiler()


LOC = Loc(line=1, col=0)


# ===================================================================
# Minimal agent (no clauses)
# ===================================================================


class TestCompileAgentMinimal:
    """Agent with only a name -- no role, trust, accepts, produces, contracts."""

    def test_generates_class(self, compiler: ASTCompiler) -> None:
        node = AgentNode("Worker", None, None, (), (), (), (), Loc(5, 0))
        lines = compiler._compile_agent(node)
        assert lines[0] == "class Worker:  # [LU:5:0]"

    def test_docstring(self, compiler: ASTCompiler) -> None:
        node = AgentNode("Worker", None, None, (), (), (), (), LOC)
        lines = compiler._compile_agent(node)
        assert "\"\"\"Agent 'Worker' -- compiled from Lingua Universale.\"\"\"" in lines[1]

    def test_no_metadata_attrs(self, compiler: ASTCompiler) -> None:
        node = AgentNode("Worker", None, None, (), (), (), (), LOC)
        lines = compiler._compile_agent(node)
        joined = "\n".join(lines)
        assert "__lu_role__" not in joined
        assert "__lu_trust__" not in joined
        assert "__lu_accepts__" not in joined
        assert "__lu_produces__" not in joined

    def test_process_no_contracts(self, compiler: ASTCompiler) -> None:
        node = AgentNode("Worker", None, None, (), (), (), (), LOC)
        lines = compiler._compile_agent(node)
        joined = "\n".join(lines)
        assert "def process(self, **kwargs):" in joined
        assert "return self._execute(**kwargs)" in joined
        assert "ContractViolation" not in joined

    def test_execute_stub(self, compiler: ASTCompiler) -> None:
        node = AgentNode("Worker", None, None, (), (), (), (), LOC)
        lines = compiler._compile_agent(node)
        joined = "\n".join(lines)
        assert "def _execute(self, **kwargs):" in joined
        assert 'raise NotImplementedError("Worker._execute")' in joined

    def test_no_contract_import(self, compiler: ASTCompiler) -> None:
        """No contracts -> no ContractViolation preamble import."""
        node = AgentNode("Worker", None, None, (), (), (), (), LOC)
        compiler._compile_agent(node)
        assert not any("ContractViolation" in i for i in compiler._preamble_imports)


# ===================================================================
# Metadata attributes
# ===================================================================


class TestCompileAgentMetadata:
    """Agent metadata: role, trust, accepts, produces."""

    def test_role(self, compiler: ASTCompiler) -> None:
        node = AgentNode("Worker", "backend", None, (), (), (), (), LOC)
        lines = compiler._compile_agent(node)
        assert '    __lu_role__ = "backend"' in lines

    def test_trust(self, compiler: ASTCompiler) -> None:
        node = AgentNode("Worker", None, "standard", (), (), (), (), LOC)
        lines = compiler._compile_agent(node)
        assert '    __lu_trust__ = "standard"' in lines

    def test_accepts_single(self, compiler: ASTCompiler) -> None:
        node = AgentNode("Worker", None, None, ("TaskRequest",), (), (), (), LOC)
        lines = compiler._compile_agent(node)
        assert '    __lu_accepts__ = ("TaskRequest",)' in lines

    def test_accepts_multiple(self, compiler: ASTCompiler) -> None:
        node = AgentNode(
            "Worker", None, None,
            ("TaskRequest", "CodeRequest"), (), (), (), LOC,
        )
        lines = compiler._compile_agent(node)
        assert '    __lu_accepts__ = ("TaskRequest", "CodeRequest",)' in lines

    def test_produces_single(self, compiler: ASTCompiler) -> None:
        node = AgentNode("Worker", None, None, (), ("TaskResult",), (), (), LOC)
        lines = compiler._compile_agent(node)
        assert '    __lu_produces__ = ("TaskResult",)' in lines

    def test_produces_multiple(self, compiler: ASTCompiler) -> None:
        node = AgentNode(
            "Worker", None, None,
            (), ("TaskResult", "ErrorReport"), (), (), LOC,
        )
        lines = compiler._compile_agent(node)
        assert '    __lu_produces__ = ("TaskResult", "ErrorReport",)' in lines

    def test_all_metadata(self, compiler: ASTCompiler) -> None:
        """Agent with all metadata fields set."""
        node = AgentNode(
            "Guardiana", "auditor", "verified",
            ("AuditRequest",), ("AuditVerdict",), (), (), LOC,
        )
        lines = compiler._compile_agent(node)
        joined = "\n".join(lines)
        assert '__lu_role__ = "auditor"' in joined
        assert '__lu_trust__ = "verified"' in joined
        assert '__lu_accepts__ = ("AuditRequest",)' in joined
        assert '__lu_produces__ = ("AuditVerdict",)' in joined

    def test_metadata_order(self, compiler: ASTCompiler) -> None:
        """Metadata attributes appear in order: role, trust, accepts, produces."""
        node = AgentNode(
            "Worker", "backend", "standard",
            ("TaskRequest",), ("TaskResult",), (), (), LOC,
        )
        lines = compiler._compile_agent(node)
        joined = "\n".join(lines)
        role_pos = joined.index("__lu_role__")
        trust_pos = joined.index("__lu_trust__")
        accepts_pos = joined.index("__lu_accepts__")
        produces_pos = joined.index("__lu_produces__")
        assert role_pos < trust_pos < accepts_pos < produces_pos


# ===================================================================
# Contract guards (requires / ensures)
# ===================================================================


class TestCompileAgentContracts:
    """Contract enforcement: requires -> preconditions, ensures -> postconditions."""

    def test_single_requires(self, compiler: ASTCompiler) -> None:
        req = AttrExpr("task", "well_defined", Loc(5, 8))
        node = AgentNode("Worker", None, None, (), (), (req,), (), LOC)
        lines = compiler._compile_agent(node)
        joined = "\n".join(lines)
        assert "# --- requires (preconditions) ---" in joined
        # Guard uses kwargs lookup
        assert 'if not (kwargs["task"].well_defined):  # [LU:5:8]' in joined
        # Error message uses human-readable form
        assert '"task.well_defined"' in joined
        assert 'kind="requires"' in joined
        assert 'source="line 5, col 8"' in joined

    def test_multiple_requires(self, compiler: ASTCompiler) -> None:
        req1 = AttrExpr("task", "well_defined", Loc(5, 8))
        req2 = BinOpExpr(
            IdentExpr("confidence", Loc(6, 8)), ">",
            NumberExpr("0.5", Loc(6, 21)), Loc(6, 8),
        )
        node = AgentNode("Worker", None, None, (), (), (req1, req2), (), LOC)
        lines = compiler._compile_agent(node)
        joined = "\n".join(lines)
        assert 'kwargs["task"].well_defined' in joined
        assert '(kwargs["confidence"]) > (0.5)' in joined

    def test_single_ensures(self, compiler: ASTCompiler) -> None:
        ens = AttrExpr("result", "tested", Loc(8, 8))
        node = AgentNode("Worker", None, None, (), (), (), (ens,), LOC)
        lines = compiler._compile_agent(node)
        joined = "\n".join(lines)
        assert "# --- ensures (postconditions) ---" in joined
        assert 'if not (kwargs["result"].tested):  # [LU:8:8]' in joined
        # Error message uses human-readable form
        assert '"result.tested"' in joined
        assert 'kind="ensures"' in joined
        assert 'source="line 8, col 8"' in joined

    def test_multiple_ensures(self, compiler: ASTCompiler) -> None:
        ens1 = AttrExpr("result", "tested", Loc(8, 8))
        ens2 = BinOpExpr(
            AttrExpr("result", "quality", Loc(9, 8)), ">=",
            NumberExpr("0.8", Loc(9, 24)), Loc(9, 8),
        )
        node = AgentNode("Worker", None, None, (), (), (), (ens1, ens2), LOC)
        lines = compiler._compile_agent(node)
        joined = "\n".join(lines)
        assert 'kwargs["result"].tested' in joined
        assert '(kwargs["result"].quality) >= (0.8)' in joined

    def test_requires_and_ensures_order(self, compiler: ASTCompiler) -> None:
        """Requires come before _execute(), ensures come after."""
        req = IdentExpr("valid", Loc(3, 8))
        ens = IdentExpr("done", Loc(5, 8))
        node = AgentNode("Worker", None, None, (), (), (req,), (ens,), LOC)
        lines = compiler._compile_agent(node)
        joined = "\n".join(lines)
        req_pos = joined.index("requires (preconditions)")
        exec_pos = joined.index("self._execute")
        ens_pos = joined.index("ensures (postconditions)")
        assert req_pos < exec_pos < ens_pos

    def test_contract_with_method_call_no_args(self, compiler: ASTCompiler) -> None:
        """Contract using method call expression: tests.pass()."""
        req = MethodCallExpr("tests", "pass", (), Loc(4, 8))
        node = AgentNode("Worker", None, None, (), (), (req,), (), LOC)
        lines = compiler._compile_agent(node)
        joined = "\n".join(lines)
        # Guard uses kwargs lookup, "pass" is a keyword -> "pass_"
        assert 'kwargs["tests"].pass_()' in joined

    def test_contract_with_method_call_args_use_kwargs(self, compiler: ASTCompiler) -> None:
        """Regression P2-F1: method call args must resolve via kwargs.

        task.validate(threshold) -> kwargs["task"].validate(kwargs["threshold"])
        NOT -> kwargs["task"].validate(threshold)  (NameError at runtime!)
        """
        arg = IdentExpr("threshold", Loc(4, 30))
        req = MethodCallExpr("task", "validate", (arg,), Loc(4, 8))
        node = AgentNode("Worker", None, None, (), (), (req,), (), LOC)
        lines = compiler._compile_agent(node)
        joined = "\n".join(lines)
        assert 'kwargs["task"].validate(kwargs["threshold"])' in joined

    def test_contract_with_complex_expr(self, compiler: ASTCompiler) -> None:
        """Contract with nested binary expression."""
        inner = BinOpExpr(
            AttrExpr("input", "size", Loc(4, 8)), ">",
            NumberExpr("0", Loc(4, 21)), Loc(4, 8),
        )
        outer = BinOpExpr(
            inner, "and",
            AttrExpr("input", "valid", Loc(4, 28)), Loc(4, 8),
        )
        node = AgentNode("Worker", None, None, (), (), (outer,), (), LOC)
        lines = compiler._compile_agent(node)
        joined = "\n".join(lines)
        assert '((kwargs["input"].size) > (0)) and (kwargs["input"].valid)' in joined

    def test_contract_with_not_expr(self, compiler: ASTCompiler) -> None:
        """Contract with not expression: not task.blocked."""
        req = NotExpr(AttrExpr("task", "blocked", Loc(4, 12)), Loc(4, 8))
        node = AgentNode("Worker", None, None, (), (), (req,), (), LOC)
        lines = compiler._compile_agent(node)
        joined = "\n".join(lines)
        assert 'not (kwargs["task"].blocked)' in joined

    def test_contract_with_group_expr(self, compiler: ASTCompiler) -> None:
        """Contract with group expression: (valid)."""
        req = GroupExpr(IdentExpr("valid", Loc(4, 9)), Loc(4, 8))
        node = AgentNode("Worker", None, None, (), (), (req,), (), LOC)
        lines = compiler._compile_agent(node)
        joined = "\n".join(lines)
        assert '(kwargs["valid"])' in joined

    def test_contract_registers_import(self, compiler: ASTCompiler) -> None:
        """Any contract triggers ContractViolation preamble import."""
        req = IdentExpr("ok", LOC)
        node = AgentNode("Worker", None, None, (), (), (req,), (), LOC)
        compiler._compile_agent(node)
        assert any("ContractViolation" in i for i in compiler._preamble_imports)

    def test_ensures_only_registers_import(self, compiler: ASTCompiler) -> None:
        """Ensures-only agent also triggers ContractViolation import."""
        ens = IdentExpr("done", LOC)
        node = AgentNode("Worker", None, None, (), (), (), (ens,), LOC)
        compiler._compile_agent(node)
        assert any("ContractViolation" in i for i in compiler._preamble_imports)

    def test_return_result_after_ensures(self, compiler: ASTCompiler) -> None:
        """Process returns _result after postcondition checks."""
        ens = IdentExpr("done", LOC)
        node = AgentNode("Worker", None, None, (), (), (), (ens,), LOC)
        lines = compiler._compile_agent(node)
        joined = "\n".join(lines)
        assert "return _result" in joined


# ===================================================================
# _escape_contract_str -- moved to test_compiler_core.py (C2.3.1)
# Full hardened suite (8 tests) supersedes the 4 basic tests.
# ===================================================================


# ===================================================================
# Keyword escaping in agent names
# ===================================================================


class TestCompileAgentKeywordEscape:
    """Agent name that is a Python keyword gets escaped."""

    def test_keyword_name(self, compiler: ASTCompiler) -> None:
        node = AgentNode("class", None, None, (), (), (), (), LOC)
        lines = compiler._compile_agent(node)
        assert lines[0].startswith("class class_:")

    def test_keyword_name_in_execute_error(self, compiler: ASTCompiler) -> None:
        """NotImplementedError message uses original name, not escaped."""
        node = AgentNode("class", None, None, (), (), (), (), LOC)
        lines = compiler._compile_agent(node)
        joined = "\n".join(lines)
        assert 'raise NotImplementedError("class._execute")' in joined


# ===================================================================
# Confident[T] preamble import (P2 fix)
# ===================================================================


class TestConfidentPreambleImport:
    """Fix P2: Confident[T] triggers preamble import."""

    def test_confident_type_registers_import(self, compiler: ASTCompiler) -> None:
        """Using Confident generic type should register the import."""
        inner = SimpleType("Number", False, LOC)
        compiler._type_to_python(GenericType("Confident", inner, False, LOC))
        expected = (
            "from cervellaswarm_lingua_universale.confidence"
            " import Confident"
        )
        assert expected in compiler._preamble_imports

    def test_confident_in_full_program(self, compiler: ASTCompiler) -> None:
        """Program using Confident type includes the import in output."""
        from cervellaswarm_lingua_universale._ast import FieldNode
        inner = SimpleType("Number", False, LOC)
        field = FieldNode(
            "score",
            GenericType("Confident", inner, False, LOC),
            Loc(3, 4),
        )
        prog = ProgramNode(
            (RecordTypeDecl("Result", (field,), Loc(2, 0)),),
            LOC,
        )
        result = compiler.compile(prog, source_file="confident.lu")
        assert "from cervellaswarm_lingua_universale.confidence import Confident" in result.python_source

    def test_non_confident_generic_no_import(self, compiler: ASTCompiler) -> None:
        """Using List or Set does NOT register the Confident import."""
        inner = SimpleType("String", False, LOC)
        compiler._type_to_python(GenericType("List", inner, False, LOC))
        confident_imports = [i for i in compiler._preamble_imports if "Confident" in i]
        assert confident_imports == []


# ===================================================================
# Full program with agent
# ===================================================================


class TestCompileAgentFullProgram:
    """Agent compilation in a full program context."""

    def test_agent_in_program(self, compiler: ASTCompiler) -> None:
        """Agent appears in CompiledModule.agents."""
        node = AgentNode("Worker", "backend", "standard", (), (), (), (), LOC)
        prog = ProgramNode((node,), LOC)
        result = compiler.compile(prog, source_file="agent.lu")
        assert result.agents == ("Worker",)

    def test_agent_with_contracts_valid_python(self, compiler: ASTCompiler) -> None:
        """Full program with agent and contracts compiles to valid Python."""
        req = AttrExpr("task", "valid", Loc(5, 8))
        ens = AttrExpr("result", "done", Loc(7, 8))
        node = AgentNode(
            "Worker", "backend", "standard",
            ("TaskRequest",), ("TaskResult",),
            (req,), (ens,), Loc(1, 0),
        )
        prog = ProgramNode((node,), Loc(1, 0))
        result = compiler.compile(prog, source_file="contracts.lu")
        # Python builtin compile() validates syntax
        compile(result.python_source, "contracts.lu", "exec")

    def test_mixed_program_valid_python(self, compiler: ASTCompiler) -> None:
        """Program with use, types, and agent compiles to valid Python."""
        from cervellaswarm_lingua_universale._ast import FieldNode
        prog = ProgramNode(
            (
                UseNode("math", None, Loc(1, 0)),
                VariantTypeDecl("Status", ("Active", "Inactive"), Loc(3, 0)),
                RecordTypeDecl("TaskData", (
                    FieldNode("name", SimpleType("String", False, LOC), Loc(6, 4)),
                ), Loc(5, 0)),
                AgentNode(
                    "Worker", "backend", "standard",
                    ("TaskData",), ("TaskData",),
                    (AttrExpr("task", "valid", Loc(10, 8)),),
                    (AttrExpr("result", "done", Loc(12, 8)),),
                    Loc(8, 0),
                ),
            ),
            Loc(1, 0),
        )
        result = compiler.compile(prog, source_file="mixed.lu")
        # Has all expected elements
        assert "import math" in result.python_source
        assert "Literal" in result.python_source
        assert "@dataclass" in result.python_source
        assert "class Worker:" in result.python_source
        assert "ContractViolation" in result.python_source
        assert result.agents == ("Worker",)
        assert result.imports == ("math",)
        # Verify syntax
        compile(result.python_source, "mixed.lu", "exec")

    def test_multiple_agents_in_program(self, compiler: ASTCompiler) -> None:
        """Program with two agents."""
        agent1 = AgentNode("Worker", "backend", "standard", (), (), (), (), Loc(1, 0))
        agent2 = AgentNode("Guardiana", "auditor", "verified", (), (), (), (), Loc(5, 0))
        prog = ProgramNode((agent1, agent2), LOC)
        result = compiler.compile(prog, source_file="multi.lu")
        assert result.agents == ("Worker", "Guardiana")
        assert "class Worker:" in result.python_source
        assert "class Guardiana:" in result.python_source
        compile(result.python_source, "multi.lu", "exec")

    def test_agent_preamble_includes_contract_import(self, compiler: ASTCompiler) -> None:
        """Agent with contracts has ContractViolation in preamble."""
        req = IdentExpr("ok", Loc(3, 8))
        node = AgentNode("Worker", None, None, (), (), (req,), (), Loc(1, 0))
        prog = ProgramNode((node,), LOC)
        result = compiler.compile(prog, source_file="test.lu")
        assert "from cervellaswarm_lingua_universale._contracts import ContractViolation" in result.python_source

    def test_via_dispatch(self, compiler: ASTCompiler) -> None:
        """Agent compilation works through _compile_declaration dispatch."""
        node = AgentNode("Worker", "backend", "standard", (), (), (), (), LOC)
        lines = compiler._compile_declaration(node)
        assert any("class Worker:" in l for l in lines)


# ===================================================================
# Round-trip execution (generated code actually runs)
# ===================================================================


class TestCompileAgentExecution:
    """Execute generated code to verify runtime behavior."""

    def test_execute_raises_not_implemented(self, compiler: ASTCompiler) -> None:
        """Generated agent's _execute raises NotImplementedError."""
        node = AgentNode("Worker", None, None, (), (), (), (), LOC)
        prog = ProgramNode((node,), LOC)
        result = compiler.compile(prog, source_file="exec.lu")
        ns: dict = {}
        exec(result.python_source, ns)  # noqa: S102
        worker = ns["Worker"]()
        with pytest.raises(NotImplementedError, match="Worker._execute"):
            worker.process()

    def test_requires_violation_at_runtime(self, compiler: ASTCompiler) -> None:
        """Precondition check raises ContractViolation at runtime."""
        req = IdentExpr("ok", Loc(3, 8))
        node = AgentNode("Worker", None, None, (), (), (req,), (), Loc(1, 0))
        prog = ProgramNode((node,), LOC)
        result = compiler.compile(prog, source_file="requires.lu")
        ns: dict = {}
        exec(result.python_source, ns)  # noqa: S102
        worker = ns["Worker"]()
        from cervellaswarm_lingua_universale._contracts import ContractViolation
        with pytest.raises(ContractViolation, match="requires violated"):
            worker.process(ok=False)

    def test_requires_passes_when_true(self, compiler: ASTCompiler) -> None:
        """Precondition passes when condition is truthy."""
        req = IdentExpr("ok", Loc(3, 8))
        node = AgentNode("Worker", None, None, (), (), (req,), (), Loc(1, 0))
        prog = ProgramNode((node,), LOC)
        result = compiler.compile(prog, source_file="pass.lu")
        ns: dict = {}
        exec(result.python_source, ns)  # noqa: S102

        # Subclass to provide _execute
        class TestWorker(ns["Worker"]):
            def _execute(self, **kwargs):
                return "done"

        worker = TestWorker()
        assert worker.process(ok=True) == "done"

    def test_ensures_violation_at_runtime(self, compiler: ASTCompiler) -> None:
        """Postcondition check raises ContractViolation at runtime."""
        ens = IdentExpr("done", Loc(5, 8))
        node = AgentNode("Worker", None, None, (), (), (), (ens,), Loc(1, 0))
        prog = ProgramNode((node,), LOC)
        result = compiler.compile(prog, source_file="ensures.lu")
        ns: dict = {}
        exec(result.python_source, ns)  # noqa: S102

        class TestWorker(ns["Worker"]):
            def _execute(self, **kwargs):
                return "result"

        worker = TestWorker()
        from cervellaswarm_lingua_universale._contracts import ContractViolation
        with pytest.raises(ContractViolation, match="ensures violated"):
            worker.process(done=False)

    def test_metadata_attributes_at_runtime(self, compiler: ASTCompiler) -> None:
        """Generated class has correct __lu_* attributes."""
        node = AgentNode(
            "Worker", "backend", "standard",
            ("TaskRequest",), ("TaskResult",), (), (), LOC,
        )
        prog = ProgramNode((node,), LOC)
        result = compiler.compile(prog, source_file="meta.lu")
        ns: dict = {}
        exec(result.python_source, ns)  # noqa: S102
        cls = ns["Worker"]
        assert cls.__lu_role__ == "backend"
        assert cls.__lu_trust__ == "standard"
        assert cls.__lu_accepts__ == ("TaskRequest",)
        assert cls.__lu_produces__ == ("TaskResult",)
