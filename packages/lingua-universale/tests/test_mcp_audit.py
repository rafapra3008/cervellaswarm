# SPDX-License-Identifier: Apache-2.0
"""Tests for _mcp_audit.py -- MCP server protocol auditing."""

import json
from pathlib import Path

import pytest

from cervellaswarm_lingua_universale._mcp_audit import (
    ToolDefinition,
    InferredStep,
    load_manifest,
    infer_protocol,
    generate_lu_source,
    audit_tools,
    render_json,
    render_terminal,
    _categorize_tools,
    _infer_orderings,
    _detect_cycles,
    _extract_id_fields,
    _extract_resource_prefix,
)

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "mcp_audit"


# ---------------------------------------------------------------------------
# Manifest loader
# ---------------------------------------------------------------------------

class TestLoadManifest:
    def test_loads_sample_manifest(self):
        name, tools = load_manifest(FIXTURES_DIR / "sample_tools.json")
        assert name == "my-database-server"
        assert len(tools) == 6
        assert tools[0].name == "connect_db"

    def test_loads_minimal_manifest(self):
        name, tools = load_manifest(FIXTURES_DIR / "minimal_tools.json")
        assert name == "echo-server"
        assert len(tools) == 2

    def test_missing_file_raises(self):
        with pytest.raises(FileNotFoundError):
            load_manifest("/nonexistent/path.json")

    def test_invalid_json_raises(self, tmp_path):
        bad = tmp_path / "bad.json"
        bad.write_text("not json", encoding="utf-8")
        with pytest.raises(json.JSONDecodeError):
            load_manifest(bad)

    def test_empty_tools(self, tmp_path):
        f = tmp_path / "empty.json"
        f.write_text('{"server_name": "empty", "tools": []}', encoding="utf-8")
        name, tools = load_manifest(f)
        assert name == "empty"
        assert tools == []

    def test_missing_server_name_uses_stem(self, tmp_path):
        f = tmp_path / "myserver.json"
        f.write_text('{"tools": [{"name": "foo", "description": "", "inputSchema": {}}]}', encoding="utf-8")
        name, tools = load_manifest(f)
        assert name == "myserver"
        assert len(tools) == 1


# ---------------------------------------------------------------------------
# Tool categorization
# ---------------------------------------------------------------------------

class TestCategorizeTools:
    def test_crud_server(self):
        tools = [
            ToolDefinition("create_user", "", {}),
            ToolDefinition("get_user", "", {}),
            ToolDefinition("update_user", "", {}),
            ToolDefinition("delete_user", "", {}),
        ]
        cats = _categorize_tools(tools)
        assert "create_user" in cats["CREATE"]
        assert "get_user" in cats["READ"]
        assert "update_user" in cats["UPDATE"]
        assert "delete_user" in cats["DELETE"]

    def test_lifecycle_tools(self):
        tools = [
            ToolDefinition("connect_db", "", {}),
            ToolDefinition("disconnect_db", "", {}),
            ToolDefinition("query", "", {}),
        ]
        cats = _categorize_tools(tools)
        assert "connect_db" in cats["LIFECYCLE"]
        assert "disconnect_db" in cats["CLEANUP"]
        assert "query" in cats["READ"]

    def test_unrecognized_goes_to_other(self):
        tools = [ToolDefinition("frobnicate", "", {})]
        cats = _categorize_tools(tools)
        assert "frobnicate" in cats["OTHER"]


# ---------------------------------------------------------------------------
# Ordering inference
# ---------------------------------------------------------------------------

class TestInferOrderings:
    def test_lifecycle_before_operations(self):
        tools = [
            ToolDefinition("connect", "", {}),
            ToolDefinition("get_data", "", {}),
        ]
        cats = _categorize_tools(tools)
        orderings = _infer_orderings(tools, cats)
        assert any(o.before == "connect" and o.after == "get_data" for o in orderings)

    def test_create_before_read(self):
        tools = [
            ToolDefinition("create_item", "", {}),
            ToolDefinition("get_item", "", {}),
        ]
        cats = _categorize_tools(tools)
        orderings = _infer_orderings(tools, cats)
        assert any(o.before == "create_item" and o.after == "get_item" for o in orderings)

    def test_schema_cross_reference(self):
        # Use tool names where name-based heuristic alone wouldn't find ordering
        # but schema cross-reference does (process_payment requires user_id from create_user)
        tools = [
            ToolDefinition("create_user", "", {}),
            ToolDefinition("process_payment", "", {
                "properties": {"user_id": {"type": "string"}},
                "required": ["user_id"],
            }),
        ]
        cats = _categorize_tools(tools)
        orderings = _infer_orderings(tools, cats)
        schema_orderings = [o for o in orderings if "schema" in o.reason]
        assert len(schema_orderings) >= 1
        assert schema_orderings[0].before == "create_user"

    def test_no_self_ordering(self):
        tools = [ToolDefinition("create_user", "", {})]
        cats = _categorize_tools(tools)
        orderings = _infer_orderings(tools, cats)
        assert all(o.before != o.after for o in orderings)


# ---------------------------------------------------------------------------
# Cycle detection
# ---------------------------------------------------------------------------

class TestDetectCycles:
    def test_no_cycles(self):
        orderings = [InferredStep("a", "b", "", "high"), InferredStep("b", "c", "", "high")]
        assert _detect_cycles(orderings) == []

    def test_simple_cycle(self):
        orderings = [InferredStep("a", "b", "", "high"), InferredStep("b", "a", "", "high")]
        warnings = _detect_cycles(orderings)
        assert len(warnings) >= 1
        assert "Circular" in warnings[0]


# ---------------------------------------------------------------------------
# LU source generation
# ---------------------------------------------------------------------------

class TestGenerateLuSource:
    def test_generated_source_is_valid_lu(self):
        """The generated .lu text must parse successfully."""
        from cervellaswarm_lingua_universale import check_source

        _, tools = load_manifest(FIXTURES_DIR / "sample_tools.json")
        protocol = infer_protocol("test-server", tools)
        source = generate_lu_source(protocol)

        result = check_source(source, source_file="<test>")
        assert result.ok, f"Generated .lu failed to parse: {result.errors}"

    def test_minimal_server_generates_valid_lu(self):
        from cervellaswarm_lingua_universale import check_source

        _, tools = load_manifest(FIXTURES_DIR / "minimal_tools.json")
        protocol = infer_protocol("echo", tools)
        source = generate_lu_source(protocol)

        result = check_source(source, source_file="<test>")
        assert result.ok, f"Generated .lu failed to parse: {result.errors}"

    def test_contains_protocol_name(self):
        _, tools = load_manifest(FIXTURES_DIR / "sample_tools.json")
        protocol = infer_protocol("my-db", tools)
        source = generate_lu_source(protocol)
        assert "protocol MyDb:" in source

    def test_contains_all_tools_as_steps(self):
        _, tools = load_manifest(FIXTURES_DIR / "sample_tools.json")
        protocol = infer_protocol("test", tools)
        source = generate_lu_source(protocol)
        for tool in tools:
            assert tool.name in source


# ---------------------------------------------------------------------------
# Full audit pipeline
# ---------------------------------------------------------------------------

class TestAuditTools:
    def test_sample_server_all_proved(self):
        _, tools = load_manifest(FIXTURES_DIR / "sample_tools.json")
        report = audit_tools("test-server", tools)
        assert report.violated == 0
        assert report.passed >= 3  # at least terminates + deadlock + roles

    def test_minimal_server_all_proved(self):
        _, tools = load_manifest(FIXTURES_DIR / "minimal_tools.json")
        report = audit_tools("echo", tools)
        assert report.violated == 0
        assert report.passed >= 3

    def test_report_has_correct_tool_count(self):
        _, tools = load_manifest(FIXTURES_DIR / "sample_tools.json")
        report = audit_tools("test", tools)
        assert report.tool_count == 6

    def test_json_output_is_serializable(self):
        _, tools = load_manifest(FIXTURES_DIR / "sample_tools.json")
        report = audit_tools("test", tools)
        result = render_json(report)
        # Must be JSON-serializable
        json_str = json.dumps(result)
        assert '"passed"' in json_str

    def test_delete_tools_produce_no_deletion_property(self):
        _, tools = load_manifest(FIXTURES_DIR / "sample_tools.json")
        report = audit_tools("test", tools)
        kinds = [pr["kind"] for pr in report.property_results]
        assert "no_deletion" in kinds


# ---------------------------------------------------------------------------
# Showcase fixtures (demo-ready servers)
# ---------------------------------------------------------------------------

class TestFilesystemServer:
    """Tests for the Anthropic filesystem server fixture (Show HN demo)."""

    def test_loads_filesystem_manifest(self):
        name, tools = load_manifest(FIXTURES_DIR / "filesystem_server.json")
        assert name == "server-filesystem"
        assert len(tools) == 11

    def test_categorizes_filesystem_tools(self):
        _, tools = load_manifest(FIXTURES_DIR / "filesystem_server.json")
        cats = _categorize_tools(tools)
        assert "read_file" in cats["READ"]
        assert "write_file" in cats["CREATE"]
        assert "edit_file" in cats["UPDATE"]
        assert "create_directory" in cats["CREATE"]
        assert "directory_tree" in cats["OTHER"]
        assert "move_file" in cats["OTHER"]

    def test_filesystem_all_proved(self):
        _, tools = load_manifest(FIXTURES_DIR / "filesystem_server.json")
        report = audit_tools("server-filesystem", tools)
        assert report.violated == 0
        assert report.passed >= 3
        assert report.tool_count == 11

    def test_filesystem_infers_ordering(self):
        _, tools = load_manifest(FIXTURES_DIR / "filesystem_server.json")
        protocol = infer_protocol("server-filesystem", tools)
        # write_file (CREATE) before read_file (READ)
        assert any(
            o.before == "write_file" and o.after == "read_file"
            for o in protocol.orderings
        )
        # create_directory (CREATE) before list_directory (READ)
        assert any(
            o.before == "create_directory" and o.after == "list_directory"
            for o in protocol.orderings
        )

    def test_filesystem_generates_valid_lu(self):
        from cervellaswarm_lingua_universale import check_source

        _, tools = load_manifest(FIXTURES_DIR / "filesystem_server.json")
        protocol = infer_protocol("server-filesystem", tools)
        source = generate_lu_source(protocol)
        result = check_source(source, source_file="<test>")
        assert result.ok, f"Filesystem .lu failed: {result.errors}"


class TestLuMcpServer:
    """Tests for the lu-mcp-server fixture (dog-fooding)."""

    def test_loads_lu_mcp_manifest(self):
        name, tools = load_manifest(FIXTURES_DIR / "lu_mcp_server.json")
        assert name == "lu-mcp-server"
        assert len(tools) == 4

    def test_lu_mcp_all_proved(self):
        _, tools = load_manifest(FIXTURES_DIR / "lu_mcp_server.json")
        report = audit_tools("lu-mcp-server", tools)
        assert report.violated == 0
        assert report.passed >= 3

    def test_lu_mcp_infers_load_before_verify(self):
        """lu_load_protocol description says 'Must be called before verify_message'."""
        _, tools = load_manifest(FIXTURES_DIR / "lu_mcp_server.json")
        protocol = infer_protocol("lu-mcp-server", tools)
        assert any(
            o.before == "lu_load_protocol" and o.after == "lu_verify_message"
            for o in protocol.orderings
        )

    def test_lu_mcp_generates_valid_lu(self):
        from cervellaswarm_lingua_universale import check_source

        _, tools = load_manifest(FIXTURES_DIR / "lu_mcp_server.json")
        protocol = infer_protocol("lu-mcp-server", tools)
        source = generate_lu_source(protocol)
        result = check_source(source, source_file="<test>")
        assert result.ok, f"LU MCP .lu failed: {result.errors}"


# ---------------------------------------------------------------------------
# Render output
# ---------------------------------------------------------------------------

class TestRender:
    def test_render_terminal_smoke(self):
        _, tools = load_manifest(FIXTURES_DIR / "sample_tools.json")
        report = audit_tools("test", tools)
        output = render_terminal(report)
        assert "MCP Audit Report" in output
        assert "PROVED" in output

    def test_render_terminal_with_warnings(self):
        """Servers with DELETE tools produce warnings."""
        _, tools = load_manifest(FIXTURES_DIR / "sample_tools.json")
        report = audit_tools("test", tools)
        output = render_terminal(report)
        assert "delete_user" in output


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_numeric_server_name(self):
        """Server names starting with digit get 'Mcp' prefix."""
        protocol = infer_protocol("3rd-party-api", [
            ToolDefinition("get_data", "Fetch data", {}),
        ])
        assert protocol.name == "Mcp3RdPartyApi"

    def test_short_tool_name_no_false_positive(self):
        """Short tool names like 'get' should not match inside longer words."""
        tools = [
            ToolDefinition("get", "Get something", {}),
            ToolDefinition("process_data", "Requires getting the data first after setup", {}),
        ]
        cats = _categorize_tools(tools)
        orderings = _infer_orderings(tools, cats)
        # "get" should NOT match inside "getting" with word boundary
        desc_orderings = [o for o in orderings if "description" in o.reason]
        assert len(desc_orderings) == 0


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

class TestHelpers:
    def test_extract_id_fields(self):
        schema = {"properties": {"user_id": {"type": "string"}}, "required": ["user_id"]}
        assert "user_id" in _extract_id_fields(schema)

    def test_extract_id_fields_empty(self):
        assert _extract_id_fields({}) == []

    def test_extract_resource_prefix(self):
        assert _extract_resource_prefix("create_user") == "user"
        assert _extract_resource_prefix("get_user_profile") == "user_profile"

    def test_dotted_tool_names_generate_valid_lu(self):
        """MCP tools often use dotted names like resources.list -- must sanitize."""
        from cervellaswarm_lingua_universale import check_source

        tools = [
            ToolDefinition("resources.list", "List resources", {}),
            ToolDefinition("tools.call", "Call a tool", {}),
            ToolDefinition("name with spaces", "Has spaces", {}),
        ]
        protocol = infer_protocol("dotted-server", tools)
        source = generate_lu_source(protocol)
        result = check_source(source, source_file="<test>")
        assert result.ok, f"Dotted names broke .lu: {result.errors}"

    def test_e2e_dotted_names_audit(self):
        """Full audit with dotted MCP tool names."""
        tools = [
            ToolDefinition("fs.read_file", "Read a file", {}),
            ToolDefinition("fs.write_file", "Write a file", {}),
        ]
        report = audit_tools("fs-server", tools)
        assert report.violated == 0


# ---------------------------------------------------------------------------
# Bug hunt S480 -- edge cases found / regressions
# ---------------------------------------------------------------------------


class TestDigitPrefixedToolNames:
    """Bug: tool names starting with a digit produced invalid LU (NUMBER token).

    Fix: generate_lu_source() prefixes safe_name with '_' when it starts with a digit.
    """

    def test_digit_prefixed_name_generates_valid_lu(self):
        """'2fast' -> '_2fast' in generated .lu so parser sees IDENTIFIER."""
        from cervellaswarm_lingua_universale import check_source

        tools = [
            ToolDefinition("2fast", "Go fast", {}),
            ToolDefinition("go_slow", "Go slow", {}),
        ]
        protocol = infer_protocol("test", tools)
        source = generate_lu_source(protocol)
        result = check_source(source)
        assert result.ok, f"Digit-prefixed tool broke .lu: {result.errors}"

    def test_digit_prefixed_name_step_content(self):
        """Sanitized step name is '_2fast', not '2fast'."""
        tools = [ToolDefinition("2fast", "Go fast", {}), ToolDefinition("normal", "Normal", {})]
        protocol = infer_protocol("test", tools)
        source = generate_lu_source(protocol)
        assert "_2fast" in source
        assert "do 2fast" not in source  # no bare digit-prefixed identifier

    def test_all_digit_tool_name_audit_succeeds(self):
        """Full audit pipeline works when tool names begin with digits."""
        tools = [
            ToolDefinition("123_check", "Check something", {}),
            ToolDefinition("9lives_api", "Nine lives", {}),
            ToolDefinition("normal_tool", "Normal", {}),
        ]
        report = audit_tools("digit-server", tools)
        assert report.violated == 0

    def test_numeric_only_tool_name(self):
        """Tool name '42' -> '_42', parses correctly."""
        from cervellaswarm_lingua_universale import check_source

        tools = [ToolDefinition("42", "The answer", {}), ToolDefinition("query", "Query", {})]
        protocol = infer_protocol("test", tools)
        source = generate_lu_source(protocol)
        result = check_source(source)
        assert result.ok, f"Numeric-only tool name broke .lu: {result.errors}"


class TestCliMcpAuditErrorHandling:
    """Bug: _cmd_mcp_audit used json.JSONDecodeError before importing json (NameError).

    Fix: import json as _json_mod at the top of _cmd_mcp_audit, use _json_mod.JSONDecodeError.
    """

    def test_nonexistent_manifest_returns_clean_error(self, capsys):
        """CLI prints 'Error loading manifest' instead of crashing with NameError."""
        import argparse
        from cervellaswarm_lingua_universale._cli import _cmd_mcp_audit

        args = argparse.Namespace(
            manifest="/nonexistent/path/tools.json",
            json_output=False,
            save_lu=None,
        )
        rc = _cmd_mcp_audit(args)
        assert rc == 1
        captured = capsys.readouterr()
        assert "Error loading manifest" in captured.err

    def test_invalid_json_manifest_returns_clean_error(self, tmp_path, capsys):
        """CLI prints 'Error loading manifest' for malformed JSON, not NameError."""
        import argparse
        from cervellaswarm_lingua_universale._cli import _cmd_mcp_audit

        bad = tmp_path / "bad.json"
        bad.write_text("not valid json", encoding="utf-8")

        args = argparse.Namespace(
            manifest=str(bad),
            json_output=False,
            save_lu=None,
        )
        rc = _cmd_mcp_audit(args)
        assert rc == 1
        captured = capsys.readouterr()
        assert "Error loading manifest" in captured.err

    def test_empty_tools_manifest_returns_error(self, tmp_path, capsys):
        """CLI prints 'No tools found' for manifests with zero tools."""
        import argparse, json
        from cervellaswarm_lingua_universale._cli import _cmd_mcp_audit

        empty = tmp_path / "empty.json"
        empty.write_text(json.dumps({"server_name": "empty", "tools": []}), encoding="utf-8")

        args = argparse.Namespace(
            manifest=str(empty),
            json_output=False,
            save_lu=None,
        )
        rc = _cmd_mcp_audit(args)
        assert rc == 1
        captured = capsys.readouterr()
        assert "No tools found" in captured.err

    def test_valid_manifest_json_output_is_serializable(self, tmp_path, capsys):
        """--json output round-trips through JSON without error."""
        import argparse, json
        from cervellaswarm_lingua_universale._cli import _cmd_mcp_audit

        manifest = tmp_path / "ok.json"
        manifest.write_text(json.dumps({
            "server_name": "test",
            "tools": [
                {"name": "get_item", "description": "Get", "inputSchema": {}},
                {"name": "list_items", "description": "List", "inputSchema": {}},
            ],
        }), encoding="utf-8")

        args = argparse.Namespace(
            manifest=str(manifest),
            json_output=True,
            save_lu=None,
        )
        rc = _cmd_mcp_audit(args)
        assert rc == 0
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["violated"] == 0


class TestDuplicateToolNames:
    """Duplicate tool names cause silently missing protocol steps (tool_count > actual steps).

    This is a known limitation, not a crash -- documenting the behavior.
    """

    def test_duplicate_names_do_not_crash(self):
        """Duplicates are tolerated; only unique names appear in generated steps."""
        tools = [
            ToolDefinition("create_user", "Create", {}),
            ToolDefinition("create_user", "Duplicate", {}),
            ToolDefinition("get_user", "Read", {}),
        ]
        protocol = infer_protocol("test", tools)
        source = generate_lu_source(protocol)
        # Should not crash and should produce valid output
        assert "protocol Test:" in source

    def test_duplicate_names_step_count_is_unique(self):
        """Only unique tool names produce steps; tool_count may exceed step count."""
        from cervellaswarm_lingua_universale import check_source

        tools = [
            ToolDefinition("create_item", "Create", {}),
            ToolDefinition("create_item", "Duplicate create", {}),
            ToolDefinition("delete_item", "Delete", {}),
        ]
        protocol = infer_protocol("test", tools)
        source = generate_lu_source(protocol)
        result = check_source(source)
        assert result.ok, f"Duplicate tool names broke .lu: {result.errors}"
        # Unique steps: create_item + delete_item = 2 (not 3)
        assert source.count("client asks server") == 2


class TestSameResourceFalsePositives:
    """P3: _same_resource uses substring matching; 'file' in 'profile' is True.

    This is a known heuristic limitation -- documenting behavior so regressions
    are caught if the heuristic is tightened.
    """

    def test_file_substring_in_profile_produces_ordering(self):
        """'file' substring matches inside 'profile' -- spurious ordering is inferred."""
        tools = [
            ToolDefinition("create_file", "Create a file", {}),
            ToolDefinition("get_user_profile", "Get user profile", {}),
        ]
        cats = _categorize_tools(tools)
        orderings = _infer_orderings(tools, cats)
        # Heuristic limitation: 'file' appears as substring in 'get_user_profile'
        spurious = [
            o for o in orderings
            if o.before == "create_file" and o.after == "get_user_profile"
        ]
        # Document current behavior (spurious ordering exists) --
        # if this fails in future, the heuristic was improved (update test accordingly)
        assert len(spurious) >= 1, (
            "Heuristic improved! Update test: spurious 'file in profile' ordering no longer inferred."
        )
