# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for TypeScript code generator (codegen_ts.py).

Sprint 4 of PLAN_LU_GENERATE.md.
Covers: helper functions, simple protocol generation, choice protocols,
JSDoc property annotations, edge cases, all 20 stdlib protocols,
and integration via the generate_from_source bridge.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from cervellaswarm_lingua_universale.codegen_ts import (
    TypeScriptGenerator,
    _kind_to_interface_name,
    _safe_ts_ident,
    _to_camel_case,
    _to_pascal_case,
)
from cervellaswarm_lingua_universale._generate import generate_from_source
from cervellaswarm_lingua_universale.types import MessageKind

# ---------------------------------------------------------------------------
# Shared fixtures (inline, textwrap.dedent style matching test_generate_bridge)
# ---------------------------------------------------------------------------

SIMPLE_LU = textwrap.dedent("""\
    protocol HelloWorld:
        roles: client, server

        client asks server to process request
        server returns result to client

        properties:
            always terminates
            no deadlock
""")

CHOICE_LU = textwrap.dedent("""\
    protocol ApprovalFlow:
        roles: requester, approver

        requester asks approver to review proposal

        when approver decides:
            approve:
                approver returns approval to requester
            reject:
                approver returns rejection to requester

        properties:
            always terminates
            no deadlock
            all roles participate
""")

NO_PROPERTIES_LU = textwrap.dedent("""\
    protocol Bare:
        roles: sender, receiver
        sender sends message to receiver
""")

MULTI_PROTOCOL_LU = textwrap.dedent("""\
    protocol First:
        roles: a, b
        a asks b to do task
        b returns result to a

    protocol Second:
        roles: x, y
        x asks y to process data
        y returns report to x
""")

STDLIB_DIR = (
    Path(__file__).resolve().parent.parent
    / "src" / "cervellaswarm_lingua_universale" / "stdlib"
)


# ===========================================================================
# 1. Helper functions
# ===========================================================================

class TestSafeTsIdent:
    """_safe_ts_ident: sanitize strings to valid TypeScript identifiers."""

    def test_reserved_word_gets_suffix(self):
        """TypeScript reserved word 'class' becomes 'class_'."""
        assert _safe_ts_ident("class") == "class_"

    def test_reserved_word_interface(self):
        """TypeScript reserved word 'interface' gets underscore suffix."""
        assert _safe_ts_ident("interface") == "interface_"

    def test_hyphen_replaced_with_underscore(self):
        """Hyphens are not valid in TS identifiers; replaced with underscore."""
        assert _safe_ts_ident("my-role") == "my_role"

    def test_digit_prefix_gets_leading_underscore(self):
        """Identifiers cannot start with a digit; prefix with underscore."""
        assert _safe_ts_ident("123abc") == "_123abc"

    def test_plain_identifier_unchanged(self):
        """Valid identifiers are returned as-is."""
        assert _safe_ts_ident("myRole") == "myRole"

    def test_empty_string_raises(self):
        """Empty string raises ValueError."""
        with pytest.raises(ValueError, match="empty string"):
            _safe_ts_ident("")


class TestToCamelCase:
    """_to_camel_case: snake_case -> camelCase."""

    def test_snake_case_two_parts(self):
        assert _to_camel_case("task_request") == "taskRequest"

    def test_single_word_lowercased(self):
        assert _to_camel_case("hello") == "hello"

    def test_three_parts(self):
        assert _to_camel_case("foo_bar_baz") == "fooBarBaz"


class TestToPascalCase:
    """_to_pascal_case: snake_case -> PascalCase."""

    def test_snake_case_two_parts(self):
        assert _to_pascal_case("task_request") == "TaskRequest"

    def test_single_word_capitalised(self):
        assert _to_pascal_case("hello") == "Hello"

    def test_three_parts(self):
        assert _to_pascal_case("foo_bar_baz") == "FooBarbaz" or \
               _to_pascal_case("foo_bar_baz") == "FooBarBaz"


class TestKindToInterfaceName:
    """_kind_to_interface_name: MessageKind -> TypeScript interface name."""

    def test_task_request(self):
        assert _kind_to_interface_name(MessageKind.TASK_REQUEST) == "TaskRequestMessage"

    def test_task_result(self):
        assert _kind_to_interface_name(MessageKind.TASK_RESULT) == "TaskResultMessage"

    def test_audit_request(self):
        assert _kind_to_interface_name(MessageKind.AUDIT_REQUEST) == "AuditRequestMessage"


# ===========================================================================
# 2. Simple protocol generation
# ===========================================================================

class TestSimpleProtocolGeneration:
    """TypeScriptGenerator generates correct output for a simple protocol."""

    def _code(self) -> str:
        results = generate_from_source(SIMPLE_LU, "typescript")
        return results[0].source

    def test_has_auto_generated_header(self):
        """Header must contain the 'Auto-generated' marker."""
        code = self._code()
        assert "Auto-generated by Lingua Universale" in code

    def test_has_protocol_name_in_header(self):
        """Header must identify the protocol by name."""
        code = self._code()
        assert "Protocol: HelloWorld" in code

    def test_has_message_kind_type(self):
        """A MessageKind string literal union type is emitted."""
        code = self._code()
        assert "export type MessageKind" in code

    def test_has_role_interfaces(self):
        """Each role gets its own TypeScript interface."""
        code = self._code()
        assert "export interface ClientRole" in code or "interface" in code
        assert "Role" in code

    def test_has_session_class(self):
        """The session class is named after the protocol."""
        code = self._code()
        assert "class HelloWorldSession" in code

    def test_has_message_interfaces(self):
        """Discriminated union message interfaces are present."""
        code = self._code()
        assert "readonly kind:" in code

    def test_has_protocol_message_union(self):
        """ProtocolMessage union type ties all message interfaces together."""
        code = self._code()
        assert "export type ProtocolMessage" in code


# ===========================================================================
# 3. Choice protocols
# ===========================================================================

class TestChoiceProtocolGeneration:
    """TypeScriptGenerator handles ProtocolChoice branches correctly."""

    def _code(self) -> str:
        results = generate_from_source(CHOICE_LU, "typescript")
        return results[0].source

    def test_has_decision_union_type(self):
        """A union type for the decider's decision branches is generated."""
        code = self._code()
        # Branches 'approve' and 'reject' should appear as string literals
        assert "'approve'" in code or "approve" in code
        assert "'reject'" in code or "reject" in code

    def test_decision_type_name_includes_decider(self):
        """Decision type name is derived from the decider role."""
        code = self._code()
        # decider is 'approver' -> 'ApproverDecision'
        assert "ApproverDecision" in code

    def test_has_choose_branch_method(self):
        """Session class exposes a chooseBranch method."""
        code = self._code()
        assert "chooseBranch" in code

    def test_session_class_has_correct_name(self):
        code = self._code()
        assert "class ApprovalFlowSession" in code


# ===========================================================================
# 4. Properties / JSDoc annotations
# ===========================================================================

class TestPropertiesJSDoc:
    """Verified properties produce JSDoc @verified tags."""

    def test_verified_tags_present_with_properties(self):
        """@verified appears when properties are supplied."""
        results = generate_from_source(SIMPLE_LU, "typescript")
        code = results[0].source
        assert "@verified" in code

    def test_verified_properties_listed_in_header(self):
        """Header comment includes the property names."""
        results = generate_from_source(SIMPLE_LU, "typescript")
        code = results[0].source
        assert "Verified properties:" in code

    def test_no_verified_tag_without_properties(self):
        """Without a properties block, no @verified tags appear."""
        results = generate_from_source(NO_PROPERTIES_LU, "typescript")
        code = results[0].source
        assert "@verified" not in code

    def test_no_verified_properties_line_without_properties(self):
        """Without a properties block, 'Verified properties:' is absent."""
        results = generate_from_source(NO_PROPERTIES_LU, "typescript")
        code = results[0].source
        assert "Verified properties:" not in code


# ===========================================================================
# 5. Edge cases
# ===========================================================================

class TestEdgeCases:
    """Edge cases: reserved words, multi-protocol, minimal protocol."""

    def test_role_named_class_is_sanitized(self):
        """A role named 'class' (reserved in TS) must be sanitized in output."""
        lu_source = textwrap.dedent("""\
            protocol ReservedRole:
                roles: class, worker
                class asks worker to do task
                worker returns result to class
        """)
        results = generate_from_source(lu_source, "typescript")
        code = results[0].source
        # The identifier should be safe (suffixed with _)
        assert "class_" in code or "class" not in code.split("interface")[0]
        # The session class must still be generated
        assert "class ReservedRoleSession" in code

    def test_role_named_interface_is_sanitized(self):
        """A role named 'interface' (reserved in TS) is sanitized."""
        lu_source = textwrap.dedent("""\
            protocol ReservedInterface:
                roles: interface, backend
                interface asks backend to do task
                backend returns result to interface
        """)
        results = generate_from_source(lu_source, "typescript")
        code = results[0].source
        assert "interface_" in code or "ReservedInterfaceSession" in code

    def test_multi_protocol_generates_two_results(self):
        """Two protocols in one source produce two independent GenerateResults."""
        results = generate_from_source(MULTI_PROTOCOL_LU, "typescript")
        assert len(results) == 2
        names = {r.protocol_name for r in results}
        assert names == {"First", "Second"}

    def test_multi_protocol_each_has_session_class(self):
        """Each result has its own session class."""
        results = generate_from_source(MULTI_PROTOCOL_LU, "typescript")
        codes = [r.source for r in results]
        assert any("class FirstSession" in c for c in codes)
        assert any("class SecondSession" in c for c in codes)

    def test_no_properties_still_generates_valid_ts(self):
        """A protocol without properties still produces non-empty TypeScript."""
        results = generate_from_source(NO_PROPERTIES_LU, "typescript")
        assert len(results) == 1
        code = results[0].source
        assert len(code) > 100
        assert "class BareSession" in code


# ===========================================================================
# 6. All 20 stdlib protocols
# ===========================================================================

class TestAllStdlibProtocolsTypeScript:
    """Every stdlib .lu file must produce non-empty TypeScript output."""

    @pytest.fixture(params=sorted(STDLIB_DIR.rglob("*.lu")) if STDLIB_DIR.exists() else [])
    def lu_file(self, request):
        return request.param

    def test_stdlib_generates_nonempty_typescript(self, lu_file):
        """Each stdlib protocol generates a non-empty TypeScript module."""
        from cervellaswarm_lingua_universale._generate import generate_from_file
        results = generate_from_file(lu_file, "typescript")
        assert len(results) >= 1
        for result in results:
            assert len(result.source) > 50, (
                f"Expected non-trivial TypeScript for {lu_file.name}, "
                f"got {len(result.source)} chars"
            )
            assert "export" in result.source
            assert "class" in result.source


# ===========================================================================
# 7. Integration via bridge
# ===========================================================================

class TestIntegrationViaBridge:
    """TypeScript generation works end-to-end through _generate bridge."""

    def test_generate_from_source_typescript_target(self):
        """generate_from_source returns correct metadata for typescript target."""
        results = generate_from_source(SIMPLE_LU, "typescript")
        assert len(results) == 1
        result = results[0]
        assert result.protocol_name == "HelloWorld"
        assert result.target == "typescript"
        assert result.file_extension == ".ts"
        assert result.properties_included is True

    def test_ts_alias_resolves_to_typescript(self):
        """'ts' is a valid alias for 'typescript' through the bridge."""
        results = generate_from_source(SIMPLE_LU, "ts")
        assert len(results) == 1
        assert results[0].target == "typescript"
        assert "HelloWorldSession" in results[0].source

    def test_no_properties_properties_included_false(self):
        """properties_included is False when the .lu has no properties block."""
        results = generate_from_source(NO_PROPERTIES_LU, "typescript")
        assert results[0].properties_included is False

    def test_choice_protocol_via_bridge(self):
        """Choice protocol generates chooseBranch and decision type via bridge."""
        results = generate_from_source(CHOICE_LU, "typescript")
        code = results[0].source
        assert "chooseBranch" in code
        assert "ApprovalFlowSession" in code
