# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for the code generation layer (codegen.py) - Core functionality.

Tests cover:
- PythonGenerator individual methods
- generate_python() convenience function
- GeneratedCode result type
- Helper functions (_safe_python_ident, _to_class_name, etc.)
"""

import pytest

from cervellaswarm_lingua_universale.codegen import (
    GeneratedCode,
    PythonGenerator,
    generate_python,
    generate_python_multi,
    _safe_python_ident,
    _to_class_name,
    _to_method_name,
    _collect_role_steps,
    _used_message_kinds,
    _has_choices,
    _kind_to_message_class,
    _escape_string,
    _validate_protocol_name,
)
from cervellaswarm_lingua_universale.protocols import (
    ArchitectFlow,
    DelegateTask,
    Protocol,
    ProtocolChoice,
    ProtocolStep,
    ResearchFlow,
    SimpleTask,
)
from cervellaswarm_lingua_universale.types import MessageKind


# ============================================================
# GeneratedCode result type
# ============================================================


class TestGeneratedCode:
    """Tests for the GeneratedCode frozen dataclass."""

    def test_basic_creation(self):
        gc = GeneratedCode(
            protocol_name="Test",
            source="print('hello')",
            roles_generated=("a", "b"),
            methods_generated=("send_task_request",),
        )
        assert gc.protocol_name == "Test"
        assert gc.source == "print('hello')"
        assert gc.roles_generated == ("a", "b")
        assert gc.methods_generated == ("send_task_request",)
        assert gc.generated_at  # not empty

    def test_empty_protocol_name_raises(self):
        with pytest.raises(ValueError, match="protocol_name cannot be empty"):
            GeneratedCode(
                protocol_name="",
                source="x",
                roles_generated=(),
                methods_generated=(),
            )

    def test_empty_source_raises(self):
        with pytest.raises(ValueError, match="source cannot be empty"):
            GeneratedCode(
                protocol_name="Test",
                source="",
                roles_generated=(),
                methods_generated=(),
            )

    def test_frozen(self):
        gc = GeneratedCode(
            protocol_name="Test",
            source="x = 1",
            roles_generated=(),
            methods_generated=(),
        )
        with pytest.raises(AttributeError):
            gc.protocol_name = "Other"  # type: ignore[misc]

    def test_line_count(self):
        gc = GeneratedCode(
            protocol_name="Test",
            source="line1\nline2\nline3",
            roles_generated=(),
            methods_generated=(),
        )
        assert gc.line_count == 3

    def test_line_count_single_line(self):
        gc = GeneratedCode(
            protocol_name="Test",
            source="single",
            roles_generated=(),
            methods_generated=(),
        )
        assert gc.line_count == 1


# ============================================================
# Helper functions
# ============================================================


class TestSafePythonIdent:
    """Tests for _safe_python_ident."""

    def test_simple_name(self):
        assert _safe_python_ident("regina") == "regina"

    def test_hyphenated_name(self):
        assert _safe_python_ident("guardiana-qualita") == "guardiana_qualita"

    def test_digit_prefix(self):
        assert _safe_python_ident("3agents") == "_3agents"

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="empty string"):
            _safe_python_ident("")

    def test_python_keyword(self):
        result = _safe_python_ident("class")
        assert result == "class_"
        assert result.isidentifier()

    def test_spaces(self):
        assert _safe_python_ident("my role") == "my_role"

    def test_special_chars(self):
        assert _safe_python_ident("role@#$") == "role___"


class TestToClassName:
    """Tests for _to_class_name."""

    def test_simple(self):
        assert _to_class_name("regina") == "Regina"

    def test_underscore(self):
        assert _to_class_name("my_role") == "MyRole"

    def test_hyphenated(self):
        assert _to_class_name("guardiana-qualita") == "GuardianaQualita"

    def test_all_caps(self):
        assert _to_class_name("WORKER") == "Worker"


class TestToMethodName:
    """Tests for _to_method_name."""

    def test_task_request(self):
        assert _to_method_name(MessageKind.TASK_REQUEST) == "send_task_request"

    def test_audit_verdict(self):
        assert _to_method_name(MessageKind.AUDIT_VERDICT) == "send_audit_verdict"

    def test_all_kinds_valid_identifiers(self):
        for kind in MessageKind:
            method = _to_method_name(kind)
            assert method.startswith("send_")
            assert method.isidentifier()


class TestCollectRoleSteps:
    """Tests for _collect_role_steps."""

    def test_delegate_task_roles(self):
        role_steps = _collect_role_steps(DelegateTask)
        assert "regina" in role_steps
        assert "worker" in role_steps
        assert "guardiana" in role_steps
        # Regina sends task_request and audit_request
        regina_kinds = [s.message_kind for s, _ in role_steps["regina"]]
        assert MessageKind.TASK_REQUEST in regina_kinds
        assert MessageKind.AUDIT_REQUEST in regina_kinds

    def test_simple_task_no_guardiana(self):
        role_steps = _collect_role_steps(SimpleTask)
        assert "regina" in role_steps
        assert "worker" in role_steps
        assert "guardiana" not in role_steps

    def test_architect_flow_includes_branch_steps(self):
        role_steps = _collect_role_steps(ArchitectFlow)
        # Architect has steps in both flat and branched elements
        architect_kinds = [s.message_kind for s, _ in role_steps["architect"]]
        assert MessageKind.PLAN_PROPOSAL in architect_kinds

    def test_branch_name_annotation(self):
        role_steps = _collect_role_steps(ArchitectFlow)
        # Steps inside branches should have branch_name set
        for step, branch_name in role_steps["worker"]:
            assert branch_name == "approve"  # worker only appears in approve branch


class TestUsedMessageKinds:
    """Tests for _used_message_kinds."""

    def test_delegate_task(self):
        kinds = _used_message_kinds(DelegateTask)
        assert MessageKind.TASK_REQUEST in kinds
        assert MessageKind.TASK_RESULT in kinds
        assert MessageKind.AUDIT_REQUEST in kinds
        assert MessageKind.AUDIT_VERDICT in kinds
        assert MessageKind.DM not in kinds

    def test_preserves_enum_order(self):
        kinds = _used_message_kinds(DelegateTask)
        # Should be in MessageKind enum order
        indices = [list(MessageKind).index(k) for k in kinds]
        assert indices == sorted(indices)

    def test_simple_task_minimal(self):
        kinds = _used_message_kinds(SimpleTask)
        assert len(kinds) == 2
        assert MessageKind.TASK_REQUEST in kinds
        assert MessageKind.TASK_RESULT in kinds


class TestHasChoices:
    """Tests for _has_choices."""

    def test_delegate_task_no_choices(self):
        assert not _has_choices(DelegateTask)

    def test_architect_flow_has_choices(self):
        assert _has_choices(ArchitectFlow)

    def test_simple_task_no_choices(self):
        assert not _has_choices(SimpleTask)


class TestKindToMessageClass:
    """Tests for _kind_to_message_class."""

    def test_all_kinds_mapped(self):
        mapping = _kind_to_message_class()
        for kind in MessageKind:
            assert kind in mapping, f"{kind} not in mapping"

    def test_correct_class_names(self):
        mapping = _kind_to_message_class()
        assert mapping[MessageKind.TASK_REQUEST] == "TaskRequest"
        assert mapping[MessageKind.AUDIT_VERDICT] == "AuditVerdict"
        assert mapping[MessageKind.DM] == "DirectMessage"


# ============================================================
# PythonGenerator methods
# ============================================================


class TestPythonGeneratorHeader:
    """Tests for generate_header."""

    def test_contains_protocol_name(self):
        gen = PythonGenerator()
        header = gen.generate_header(DelegateTask)
        assert "DelegateTask" in header

    def test_contains_docstring_markers(self):
        gen = PythonGenerator()
        header = gen.generate_header(DelegateTask)
        assert '"""' in header

    def test_contains_timestamp(self):
        gen = PythonGenerator()
        header = gen.generate_header(DelegateTask)
        assert "UTC" in header

    def test_contains_do_not_edit(self):
        gen = PythonGenerator()
        header = gen.generate_header(DelegateTask)
        assert "DO NOT EDIT" in header


class TestPythonGeneratorImports:
    """Tests for generate_imports."""

    def test_includes_message_kind(self):
        gen = PythonGenerator()
        imports = gen.generate_imports(DelegateTask)
        assert "MessageKind" in imports

    def test_includes_session_checker(self):
        gen = PythonGenerator()
        imports = gen.generate_imports(DelegateTask)
        assert "SessionChecker" in imports

    def test_includes_protocol_violation(self):
        gen = PythonGenerator()
        imports = gen.generate_imports(DelegateTask)
        assert "ProtocolViolation" in imports

    def test_includes_used_message_classes(self):
        gen = PythonGenerator()
        imports = gen.generate_imports(DelegateTask)
        assert "TaskRequest" in imports
        assert "TaskResult" in imports
        assert "AuditRequest" in imports
        assert "AuditVerdict" in imports

    def test_excludes_unused_message_classes(self):
        gen = PythonGenerator()
        imports = gen.generate_imports(SimpleTask)
        # SimpleTask only uses TaskRequest and TaskResult
        assert "AuditRequest" not in imports
        assert "PlanRequest" not in imports

    def test_includes_future_annotations(self):
        gen = PythonGenerator()
        imports = gen.generate_imports(DelegateTask)
        assert "from __future__ import annotations" in imports


class TestPythonGeneratorProtocolDef:
    """Tests for generate_protocol_definition."""

    def test_contains_protocol_name(self):
        gen = PythonGenerator()
        code = gen.generate_protocol_definition(DelegateTask)
        assert "DELEGATETASK" in code  # uppercase constant

    def test_contains_roles(self):
        gen = PythonGenerator()
        code = gen.generate_protocol_definition(DelegateTask)
        assert '"regina"' in code
        assert '"worker"' in code
        assert '"guardiana"' in code

    def test_contains_steps(self):
        gen = PythonGenerator()
        code = gen.generate_protocol_definition(DelegateTask)
        assert "ProtocolStep(" in code
        assert "TASK_REQUEST" in code

    def test_branched_protocol_contains_choice(self):
        gen = PythonGenerator()
        code = gen.generate_protocol_definition(ArchitectFlow)
        assert "ProtocolChoice(" in code
        assert '"approve"' in code
        assert '"reject"' in code

    def test_compiles(self):
        gen = PythonGenerator()
        # The protocol definition alone won't compile (needs imports)
        # But we can check it's valid Python syntax within a module
        imports = gen.generate_imports(DelegateTask)
        code = gen.generate_protocol_definition(DelegateTask)
        full = imports + "\n" + code
        compile(full, "test.py", "exec")


class TestPythonGeneratorRoleClasses:
    """Tests for generate_role_classes."""

    def test_delegate_task_creates_three_classes(self):
        gen = PythonGenerator()
        code = gen.generate_role_classes(DelegateTask)
        assert "class ReginaRole:" in code
        assert "class WorkerRole:" in code
        assert "class GuardianaRole:" in code

    def test_simple_task_creates_two_classes(self):
        gen = PythonGenerator()
        code = gen.generate_role_classes(SimpleTask)
        assert "class ReginaRole:" in code
        assert "class WorkerRole:" in code
        assert "Guardiana" not in code

    def test_regina_has_send_methods(self):
        gen = PythonGenerator()
        code = gen.generate_role_classes(DelegateTask)
        assert "send_task_request" in code
        assert "send_audit_request" in code

    def test_worker_has_send_task_result(self):
        gen = PythonGenerator()
        code = gen.generate_role_classes(DelegateTask)
        # Check worker section specifically
        assert "send_task_result" in code

    def test_contains_type_hints(self):
        gen = PythonGenerator()
        code = gen.generate_role_classes(DelegateTask)
        assert "TaskRequest" in code
        assert "TaskResult" in code

    def test_contains_docstrings(self):
        gen = PythonGenerator()
        code = gen.generate_role_classes(DelegateTask)
        assert '"""Send task_request to worker."""' in code

    def test_deduplicates_methods(self):
        gen = PythonGenerator()
        code = gen.generate_role_classes(ArchitectFlow)
        # Regina sends plan_decision in both approve and reject branches
        # Should only generate one send_plan_decision method
        count = code.count("def send_plan_decision(")
        assert count == 1


class TestPythonGeneratorSessionClass:
    """Tests for generate_session_class."""

    def test_creates_protocol_session(self):
        gen = PythonGenerator()
        code = gen.generate_session_class(DelegateTask)
        assert "class ProtocolSession:" in code

    def test_has_is_complete_property(self):
        gen = PythonGenerator()
        code = gen.generate_session_class(DelegateTask)
        assert "def is_complete(self)" in code

    def test_has_session_id_property(self):
        gen = PythonGenerator()
        code = gen.generate_session_class(DelegateTask)
        assert "def session_id(self)" in code

    def test_has_role_properties(self):
        gen = PythonGenerator()
        code = gen.generate_session_class(DelegateTask)
        assert "def regina(self)" in code
        assert "def worker(self)" in code
        assert "def guardiana(self)" in code

    def test_has_send_method(self):
        gen = PythonGenerator()
        code = gen.generate_session_class(DelegateTask)
        assert "def send(self, sender: str, receiver: str, msg: object)" in code

    def test_choice_protocol_has_choose_branch(self):
        gen = PythonGenerator()
        code = gen.generate_session_class(ArchitectFlow)
        assert "def choose_branch(self, branch_name: str)" in code

    def test_flat_protocol_no_choose_branch(self):
        gen = PythonGenerator()
        code = gen.generate_session_class(DelegateTask)
        assert "choose_branch" not in code

    def test_has_checker_property(self):
        gen = PythonGenerator()
        code = gen.generate_session_class(DelegateTask)
        assert "def checker(self)" in code


class TestPythonGeneratorGenerate:
    """Tests for the full generate() method."""

    def test_delegate_task_compiles(self):
        gen = PythonGenerator()
        code = gen.generate(DelegateTask)
        compile(code, "DelegateTask.py", "exec")

    def test_architect_flow_compiles(self):
        gen = PythonGenerator()
        code = gen.generate(ArchitectFlow)
        compile(code, "ArchitectFlow.py", "exec")

    def test_simple_task_compiles(self):
        gen = PythonGenerator()
        code = gen.generate(SimpleTask)
        compile(code, "SimpleTask.py", "exec")

    def test_research_flow_compiles(self):
        gen = PythonGenerator()
        code = gen.generate(ResearchFlow)
        compile(code, "ResearchFlow.py", "exec")


# ============================================================
# Guardiana P2 fix regression tests (S395)
# ============================================================


class TestEscapeString:
    """Tests for _escape_string (P2-F1 fix)."""

    def test_double_quotes(self):
        assert _escape_string('say "hello"') == 'say \\"hello\\"'

    def test_newlines(self):
        assert _escape_string("line1\nline2") == "line1\\nline2"

    def test_carriage_return(self):
        assert _escape_string("line1\rline2") == "line1\\rline2"

    def test_backslash(self):
        assert _escape_string("path\\to\\file") == "path\\\\to\\\\file"

    def test_combined(self):
        result = _escape_string('say "hi"\nnew line')
        assert result == 'say \\"hi\\"\\nnew line'

    def test_empty_string(self):
        assert _escape_string("") == ""

    def test_no_special_chars(self):
        assert _escape_string("simple text") == "simple text"


class TestValidateProtocolName:
    """Tests for _validate_protocol_name (P2-F2 fix)."""

    def test_valid_name(self):
        _validate_protocol_name("DelegateTask")  # Should not raise

    def test_valid_name_with_underscore(self):
        _validate_protocol_name("My_Protocol")  # Should not raise

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            _validate_protocol_name("")

    def test_digit_only_name_still_works(self):
        # "123" -> "_123" (sanitized) -> valid
        _validate_protocol_name("123")  # Should not raise


class TestDescriptionEscapingInGeneration:
    """Regression tests for description escaping in generated code (P2-F1)."""

    def test_description_with_newlines_compiles(self):
        proto = Protocol(
            name="NewlineProto",
            roles=("a", "b"),
            description="Line 1\nLine 2",
            elements=(
                ProtocolStep(
                    sender="a", receiver="b",
                    message_kind=MessageKind.DM,
                    description="Step\nwith\nnewlines",
                ),
            ),
        )
        code = generate_python(proto)
        compile(code, "NewlineProto.py", "exec")

    def test_description_with_backslashes_compiles(self):
        proto = Protocol(
            name="BackslashProto",
            roles=("a", "b"),
            description="path\\to\\file",
            elements=(
                ProtocolStep(
                    sender="a", receiver="b",
                    message_kind=MessageKind.DM,
                ),
            ),
        )
        code = generate_python(proto)
        compile(code, "BackslashProto.py", "exec")

    def test_description_with_quotes_compiles(self):
        proto = Protocol(
            name="QuoteProto",
            roles=("a", "b"),
            description='He said "hello"',
            elements=(
                ProtocolStep(
                    sender="a", receiver="b",
                    message_kind=MessageKind.DM,
                    description='Step "desc"',
                ),
            ),
        )
        code = generate_python(proto)
        compile(code, "QuoteProto.py", "exec")
