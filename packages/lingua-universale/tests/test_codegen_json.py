# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for JSON Schema code generator (Sprint 6 of PLAN_LU_GENERATE.md).

Covers:
- Valid JSON output (simple and choice protocols)
- Schema structure ($schema, title, $defs, required)
- Roles array (enum values, minItems/maxItems)
- Steps and choices ($defs shapes, oneOf discrimination)
- Verified properties (x-lu-properties present/absent)
- Helper functions (_step_to_dict, _choice_to_dict, _elements_to_list)
- All 20 stdlib protocols generate valid JSON
- Integration via generate_from_source bridge (json-schema + json alias)
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

import pytest

from cervellaswarm_lingua_universale._generate import generate_from_source
from cervellaswarm_lingua_universale.codegen_json import (
    JSONSchemaGenerator,
    _choice_to_dict,
    _elements_to_list,
    _step_to_dict,
    generate_json_schema,
)
from cervellaswarm_lingua_universale.protocols import Protocol, ProtocolChoice, ProtocolStep
from cervellaswarm_lingua_universale.types import MessageKind

# ---------------------------------------------------------------------------
# Shared LU fixtures (same as test_generate_bridge.py for consistency)
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

STDLIB_DIR = (
    Path(__file__).resolve().parent.parent
    / "src" / "cervellaswarm_lingua_universale" / "stdlib"
)

# ---------------------------------------------------------------------------
# Helper: build a minimal Protocol + ProtocolStep by hand for unit tests
# ---------------------------------------------------------------------------

def _make_simple_protocol() -> Protocol:
    """Build a simple 2-role protocol with two steps (no choice)."""
    return Protocol(
        name="PingPong",
        roles=("client", "server"),
        elements=(
            ProtocolStep(
                sender="client",
                receiver="server",
                message_kind=MessageKind.TASK_REQUEST,
                description="client pings server",
            ),
            ProtocolStep(
                sender="server",
                receiver="client",
                message_kind=MessageKind.TASK_RESULT,
                description="server pongs client",
            ),
        ),
    )


def _make_choice_protocol() -> Protocol:
    """Build a 2-role protocol with one branching choice."""
    return Protocol(
        name="Branching",
        roles=("decider", "worker"),
        elements=(
            ProtocolChoice(
                decider="decider",
                description="decider picks a path",
                branches={
                    "yes": (
                        ProtocolStep(
                            sender="decider",
                            receiver="worker",
                            message_kind=MessageKind.TASK_REQUEST,
                        ),
                    ),
                    "no": (
                        ProtocolStep(
                            sender="decider",
                            receiver="worker",
                            message_kind=MessageKind.SHUTDOWN_REQUEST,
                        ),
                    ),
                },
            ),
        ),
    )


# ===========================================================================
# 1. Valid JSON output
# ===========================================================================

class TestValidJsonOutput:
    """generate_json_schema() / JSONSchemaGenerator.generate() must always
    produce strings that json.loads() can parse without error."""

    def test_simple_protocol_is_valid_json(self):
        """A plain step-only protocol produces parseable JSON."""
        protocol = _make_simple_protocol()
        output = generate_json_schema(protocol)
        # Must not raise
        parsed = json.loads(output)
        assert isinstance(parsed, dict)

    def test_choice_protocol_is_valid_json(self):
        """A protocol with a branching ProtocolChoice produces parseable JSON."""
        protocol = _make_choice_protocol()
        output = generate_json_schema(protocol)
        parsed = json.loads(output)
        assert isinstance(parsed, dict)


# ===========================================================================
# 2. Schema structure
# ===========================================================================

class TestSchemaStructure:
    """The top-level schema object must have the mandated fields."""

    @pytest.fixture(autouse=True)
    def schema(self):
        self._schema = json.loads(generate_json_schema(_make_simple_protocol()))

    def test_has_dollar_schema_2020_12(self):
        """$schema field must be the JSON Schema 2020-12 URL."""
        assert self._schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"

    def test_title_matches_protocol_name(self):
        """title must equal the protocol name."""
        assert self._schema["title"] == "PingPong"

    def test_has_all_required_defs(self):
        """$defs must contain ProtocolStep, ProtocolChoice, ProtocolElement, MessageKind."""
        defs = self._schema["$defs"]
        for key in ("ProtocolStep", "ProtocolChoice", "ProtocolElement", "MessageKind"):
            assert key in defs, f"Missing $defs key: {key}"

    def test_required_fields(self):
        """Top-level required array must be exactly [protocol, roles, steps]."""
        assert set(self._schema["required"]) == {"protocol", "roles", "steps"}

    def test_has_x_lu_version(self):
        """x-lu-version extension field must be present."""
        assert "x-lu-version" in self._schema
        assert isinstance(self._schema["x-lu-version"], str)
        assert self._schema["x-lu-version"]  # non-empty

    def test_type_is_object(self):
        """Top-level type must be 'object'."""
        assert self._schema.get("type") == "object"


# ===========================================================================
# 3. Roles
# ===========================================================================

class TestRoles:
    """The roles property must reflect the protocol's role list exactly."""

    def test_roles_enum_contains_all_roles(self):
        """roles.items.enum must list every role declared in the protocol."""
        protocol = _make_simple_protocol()
        schema = json.loads(generate_json_schema(protocol))
        enum_values = schema["properties"]["roles"]["items"]["enum"]
        assert set(enum_values) == {"client", "server"}

    def test_roles_min_max_items_match_count(self):
        """minItems and maxItems must equal len(protocol.roles)."""
        protocol = Protocol(
            name="ThreeRole",
            roles=("a", "b", "c"),
            elements=(
                ProtocolStep(sender="a", receiver="b", message_kind=MessageKind.TASK_REQUEST),
                ProtocolStep(sender="b", receiver="c", message_kind=MessageKind.TASK_RESULT),
                ProtocolStep(sender="c", receiver="a", message_kind=MessageKind.AUDIT_VERDICT),
            ),
        )
        schema = json.loads(generate_json_schema(protocol))
        roles_prop = schema["properties"]["roles"]
        assert roles_prop["minItems"] == 3
        assert roles_prop["maxItems"] == 3


# ===========================================================================
# 4. Steps and choices ($defs shapes)
# ===========================================================================

class TestDefsShapes:
    """The ProtocolStep, ProtocolChoice, ProtocolElement $defs must have
    the correct required fields and discriminator structure."""

    @pytest.fixture(autouse=True)
    def defs(self):
        schema = json.loads(generate_json_schema(_make_simple_protocol()))
        self._defs = schema["$defs"]

    def test_protocol_step_required_fields(self):
        """ProtocolStep.required must include type, sender, receiver, message_kind."""
        required = self._defs["ProtocolStep"]["required"]
        assert "type" in required
        assert "sender" in required
        assert "receiver" in required
        assert "message_kind" in required

    def test_protocol_choice_required_fields(self):
        """ProtocolChoice.required must include type, decider, branches."""
        # Use a protocol with a choice to ensure ProtocolChoice is in $defs
        schema = json.loads(generate_json_schema(_make_choice_protocol()))
        required = schema["$defs"]["ProtocolChoice"]["required"]
        assert "type" in required
        assert "decider" in required
        assert "branches" in required

    def test_protocol_element_is_one_of(self):
        """ProtocolElement must use oneOf to discriminate step vs choice."""
        element_def = self._defs["ProtocolElement"]
        assert "oneOf" in element_def
        refs = [item.get("$ref") for item in element_def["oneOf"]]
        assert "#/$defs/ProtocolStep" in refs
        assert "#/$defs/ProtocolChoice" in refs

    def test_protocol_step_type_const_is_step(self):
        """ProtocolStep.properties.type must be const 'step'."""
        step_def = self._defs["ProtocolStep"]
        type_prop = step_def["properties"]["type"]
        assert type_prop.get("const") == "step"

    def test_protocol_choice_type_const_is_choice(self):
        """ProtocolChoice.properties.type must be const 'choice'."""
        schema = json.loads(generate_json_schema(_make_choice_protocol()))
        choice_def = schema["$defs"]["ProtocolChoice"]
        type_prop = choice_def["properties"]["type"]
        assert type_prop.get("const") == "choice"


# ===========================================================================
# 5. x-lu-properties extension
# ===========================================================================

class TestXLuProperties:
    """x-lu-properties must be included when properties are given and
    absent when no ProtocolSpec is provided."""

    def test_x_lu_properties_present_when_spec_provided(self):
        """Schemas derived from LU source with properties block include
        x-lu-properties as a non-empty list."""
        results = generate_from_source(SIMPLE_LU, "json-schema")
        schema = json.loads(results[0].source)
        assert "x-lu-properties" in schema
        assert isinstance(schema["x-lu-properties"], list)
        assert len(schema["x-lu-properties"]) > 0

    def test_x_lu_properties_absent_when_no_spec(self):
        """Schemas with no properties block must not include x-lu-properties."""
        protocol = _make_simple_protocol()
        schema = json.loads(generate_json_schema(protocol, properties=None))
        assert "x-lu-properties" not in schema

    def test_x_lu_properties_values_are_strings(self):
        """Every entry in x-lu-properties must be a non-empty string."""
        results = generate_from_source(SIMPLE_LU, "json-schema")
        schema = json.loads(results[0].source)
        for entry in schema.get("x-lu-properties", []):
            assert isinstance(entry, str)
            assert entry  # non-empty


# ===========================================================================
# 6. Helper functions (unit tests)
# ===========================================================================

class TestHelperFunctions:
    """Unit tests for the three helper functions exported from codegen_json."""

    def test_step_to_dict_basic_fields(self):
        """_step_to_dict must return type, sender, receiver, message_kind."""
        step = ProtocolStep(
            sender="alice",
            receiver="bob",
            message_kind=MessageKind.TASK_REQUEST,
            description="hello",
        )
        d = _step_to_dict(step)
        assert d["type"] == "step"
        assert d["sender"] == "alice"
        assert d["receiver"] == "bob"
        assert d["message_kind"] == MessageKind.TASK_REQUEST.value
        assert d["description"] == "hello"

    def test_step_to_dict_omits_empty_description(self):
        """_step_to_dict must omit the description key when it is empty."""
        step = ProtocolStep(
            sender="alice",
            receiver="bob",
            message_kind=MessageKind.TASK_RESULT,
        )
        d = _step_to_dict(step)
        assert "description" not in d

    def test_choice_to_dict_structure(self):
        """_choice_to_dict must return type, decider, branches dict."""
        choice = ProtocolChoice(
            decider="manager",
            description="pick path",
            branches={
                "left": (
                    ProtocolStep(
                        sender="manager",
                        receiver="worker",
                        message_kind=MessageKind.TASK_REQUEST,
                    ),
                ),
                "right": (
                    ProtocolStep(
                        sender="manager",
                        receiver="worker",
                        message_kind=MessageKind.SHUTDOWN_REQUEST,
                    ),
                ),
            },
        )
        # We need a valid Protocol context to build the choice, but _choice_to_dict
        # works directly on the ProtocolChoice object without a Protocol.
        d = _choice_to_dict(choice)
        assert d["type"] == "choice"
        assert d["decider"] == "manager"
        assert "branches" in d
        assert set(d["branches"].keys()) == {"left", "right"}
        # Each branch should be a list with one step dict
        left_branch = d["branches"]["left"]
        assert isinstance(left_branch, list)
        assert len(left_branch) == 1
        assert left_branch[0]["type"] == "step"

    def test_elements_to_list_mixed_step_and_choice(self):
        """_elements_to_list must handle a sequence with both steps and choices."""
        step = ProtocolStep(
            sender="a",
            receiver="b",
            message_kind=MessageKind.TASK_REQUEST,
        )
        choice = ProtocolChoice(
            decider="a",
            branches={
                "ok": (
                    ProtocolStep(
                        sender="a",
                        receiver="b",
                        message_kind=MessageKind.TASK_RESULT,
                    ),
                ),
            },
        )
        result = _elements_to_list([step, choice])
        assert len(result) == 2
        assert result[0]["type"] == "step"
        assert result[1]["type"] == "choice"
        # The choice's branch element is also serialised correctly
        assert result[1]["branches"]["ok"][0]["type"] == "step"


# ===========================================================================
# 7. All 20 stdlib protocols
# ===========================================================================

class TestAllStdlibProtocols:
    """Every .lu file in the stdlib must generate valid, title-matching JSON."""

    @pytest.fixture(
        params=sorted(STDLIB_DIR.rglob("*.lu")) if STDLIB_DIR.exists() else [],
        ids=lambda p: p.stem,
    )
    def lu_file(self, request):
        return request.param

    def test_stdlib_generates_valid_json(self, lu_file):
        """json.loads() must not raise, and title must be non-empty."""
        from cervellaswarm_lingua_universale._generate import generate_from_file

        results = generate_from_file(lu_file, "json-schema")
        assert len(results) >= 1, f"No results for {lu_file.name}"
        for result in results:
            schema = json.loads(result.source)  # raises on invalid JSON
            assert schema.get("title") == result.protocol_name, (
                f"title mismatch in {lu_file.name}: "
                f"expected {result.protocol_name!r}, got {schema.get('title')!r}"
            )


# ===========================================================================
# 8. Integration via _generate bridge
# ===========================================================================

class TestIntegrationViaBridge:
    """generate_from_source with json-schema / json targets must work end-to-end."""

    def test_json_schema_target_via_bridge(self):
        """generate_from_source(lu, 'json-schema') produces valid JSON with correct title."""
        results = generate_from_source(SIMPLE_LU, "json-schema")
        assert len(results) == 1
        result = results[0]
        assert result.target == "json-schema"
        assert result.file_extension == ".json"
        assert result.protocol_name == "HelloWorld"
        schema = json.loads(result.source)
        assert schema["title"] == "HelloWorld"

    def test_json_alias_via_bridge(self):
        """generate_from_source(lu, 'json') must resolve to json-schema target."""
        results = generate_from_source(SIMPLE_LU, "json")
        assert len(results) == 1
        assert results[0].target == "json-schema"
        assert results[0].file_extension == ".json"
        # Still valid JSON
        json.loads(results[0].source)

    def test_choice_protocol_via_bridge(self):
        """A choice protocol through the bridge produces valid JSON with all branch names."""
        results = generate_from_source(CHOICE_LU, "json-schema")
        assert len(results) == 1
        schema = json.loads(results[0].source)
        assert schema["title"] == "ApprovalFlow"
        # roles must include both participants
        enum_values = schema["properties"]["roles"]["items"]["enum"]
        assert set(enum_values) == {"requester", "approver"}

    def test_no_properties_protocol_via_bridge(self):
        """A protocol with no properties block produces valid JSON without x-lu-properties."""
        results = generate_from_source(NO_PROPERTIES_LU, "json-schema")
        assert len(results) == 1
        schema = json.loads(results[0].source)
        assert "x-lu-properties" not in schema
        assert schema["title"] == "Bare"
