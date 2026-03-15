# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for lu generate bridge + Python target + CLI.

Sprint 2 of PLAN_LU_GENERATE.md.
Covers: bridge parsing, Python generation, CLI integration, edge cases,
end-to-end round-trip (Guardiana F4 requirement).
"""

from __future__ import annotations

import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

from cervellaswarm_lingua_universale._generate import (
    GenerateResult,
    _parse_to_protocols,
    _resolve_target,
    generate_from_file,
    generate_from_source,
)

# -- Fixtures ----------------------------------------------------------------

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

NO_PROPERTIES_LU = textwrap.dedent("""\
    protocol Bare:
        roles: sender, receiver
        sender sends message to receiver
""")

STDLIB_DIR = (
    Path(__file__).resolve().parent.parent
    / "src" / "cervellaswarm_lingua_universale" / "stdlib"
)


# -- Bridge tests ------------------------------------------------------------

class TestParseToProtocols:
    """Tests for _parse_to_protocols bridge."""

    def test_simple_protocol(self):
        results = _parse_to_protocols(SIMPLE_LU)
        assert len(results) == 1
        protocol, spec = results[0]
        assert protocol.name == "HelloWorld"
        assert set(protocol.roles) == {"client", "server"}
        assert len(protocol.elements) == 2

    def test_protocol_with_choice(self):
        results = _parse_to_protocols(CHOICE_LU)
        assert len(results) == 1
        protocol, spec = results[0]
        assert protocol.name == "ApprovalFlow"
        # 1 step + 1 choice = 2 elements
        assert len(protocol.elements) == 2

    def test_properties_extracted(self):
        results = _parse_to_protocols(SIMPLE_LU)
        _, spec = results[0]
        assert spec is not None
        assert len(spec.properties) == 2  # always_terminates + no_deadlock

    def test_no_properties(self):
        results = _parse_to_protocols(NO_PROPERTIES_LU)
        _, spec = results[0]
        assert spec is None

    def test_multi_protocol(self):
        results = _parse_to_protocols(MULTI_PROTOCOL_LU)
        assert len(results) == 2
        names = {r[0].name for r in results}
        assert names == {"First", "Second"}

    def test_empty_source_raises(self):
        with pytest.raises(ValueError, match="No protocol declarations"):
            _parse_to_protocols("")

    def test_no_protocol_source_raises(self):
        # Source with no valid declarations at all
        with pytest.raises((ValueError, Exception)):
            _parse_to_protocols("this is not valid LU syntax at all")

    def test_choice_has_branches(self):
        from cervellaswarm_lingua_universale.protocols import ProtocolChoice

        results = _parse_to_protocols(CHOICE_LU)
        protocol, _ = results[0]
        choices = [e for e in protocol.elements if isinstance(e, ProtocolChoice)]
        assert len(choices) == 1
        assert "approve" in choices[0].branches
        assert "reject" in choices[0].branches


# -- Target resolution -------------------------------------------------------

class TestResolveTarget:
    """Tests for target name resolution and aliases."""

    def test_python(self):
        assert _resolve_target("python") == "python"

    def test_typescript(self):
        assert _resolve_target("typescript") == "typescript"

    def test_ts_alias(self):
        assert _resolve_target("ts") == "typescript"

    def test_json_schema(self):
        assert _resolve_target("json-schema") == "json-schema"

    def test_json_alias(self):
        assert _resolve_target("json") == "json-schema"

    def test_unknown_raises(self):
        with pytest.raises(ValueError, match="Unknown target.*rust"):
            _resolve_target("rust")

    def test_error_shows_supported(self):
        with pytest.raises(ValueError, match="python"):
            _resolve_target("cobol")


# -- Python generation -------------------------------------------------------

class TestGeneratePython:
    """Tests for Python code generation via bridge."""

    def test_generate_from_source_simple(self):
        results = generate_from_source(SIMPLE_LU, "python")
        assert len(results) == 1
        result = results[0]
        assert isinstance(result, GenerateResult)
        assert result.protocol_name == "HelloWorld"
        assert result.target == "python"
        assert result.file_extension == ".py"
        assert result.properties_included is True

    def test_generated_python_compiles(self):
        """Generated Python source is valid Python (compile check)."""
        results = generate_from_source(SIMPLE_LU, "python")
        code = results[0].source
        compile(code, "<generated>", "exec")  # raises SyntaxError if invalid

    def test_generated_python_has_imports(self):
        results = generate_from_source(SIMPLE_LU, "python")
        code = results[0].source
        assert "from cervellaswarm_lingua_universale" in code
        assert "SessionChecker" in code

    def test_generated_python_has_protocol(self):
        results = generate_from_source(SIMPLE_LU, "python")
        code = results[0].source
        assert "HELLOWORLD" in code or "HelloWorld" in code
        assert "Protocol(" in code

    def test_generated_python_has_session_class(self):
        results = generate_from_source(SIMPLE_LU, "python")
        code = results[0].source
        assert "class ProtocolSession" in code or "Session" in code

    def test_multi_protocol_generates_both(self):
        results = generate_from_source(MULTI_PROTOCOL_LU, "python")
        assert len(results) == 2
        names = {r.protocol_name for r in results}
        assert names == {"First", "Second"}

    def test_choice_protocol_generates(self):
        results = generate_from_source(CHOICE_LU, "python")
        code = results[0].source
        compile(code, "<generated>", "exec")
        assert "ApprovalFlow" in code

    def test_no_properties_still_generates(self):
        results = generate_from_source(NO_PROPERTIES_LU, "python")
        assert len(results) == 1
        assert results[0].properties_included is False
        compile(results[0].source, "<generated>", "exec")


# -- End-to-end round-trip (Guardiana F4 requirement) ------------------------

class TestEndToEndRoundTrip:
    """The gold standard: .lu -> generate python -> exec -> send -> complete."""

    def test_simple_protocol_round_trip(self):
        """Full round-trip: generate, exec, create session, send, complete."""
        results = generate_from_source(SIMPLE_LU, "python")
        code = results[0].source

        # Execute the generated code
        namespace = {}
        exec(code, namespace)

        # Find the session class (codegen names it ProtocolSession)
        session_cls = namespace.get("ProtocolSession") or namespace.get("HelloWorldSession")
        assert session_cls is not None, f"No session class found in: {list(namespace.keys())}"
        session = session_cls()

        # Step 1: client asks server
        from cervellaswarm_lingua_universale.types import TaskRequest
        session.send("client", "server", TaskRequest(
            task_id="1", description="process request",
        ))

        # Step 2: server returns result
        from cervellaswarm_lingua_universale.types import TaskResult
        session.send("server", "client", TaskResult(
            task_id="1", status="completed", summary="done",
        ))

        # Protocol should be complete
        assert session.is_complete

    def test_choice_protocol_round_trip(self):
        """Round-trip with choice: approve branch."""
        results = generate_from_source(CHOICE_LU, "python")
        code = results[0].source

        namespace = {}
        exec(code, namespace)

        # Find session class
        session_cls = namespace.get("ProtocolSession") or namespace.get("ApprovalFlowSession")
        assert session_cls is not None
        session = session_cls()

        from cervellaswarm_lingua_universale.types import TaskRequest, TaskResult
        # Step 1: requester asks
        session.send("requester", "approver", TaskRequest(
            task_id="1", description="review proposal",
        ))

        # Choose approve branch and send approval
        session.choose_branch("approve")

        # Step 2: approver returns approval
        session.send("approver", "requester", TaskResult(
            task_id="1", status="approved", summary="approved",
        ))

        assert session.is_complete


# -- File-based generation ---------------------------------------------------

class TestGenerateFromFile:
    """Tests for generate_from_file."""

    def test_nonexistent_file_raises(self):
        with pytest.raises(FileNotFoundError, match="not_real.lu"):
            generate_from_file("not_real.lu", "python")

    def test_stdlib_ping_pong(self):
        lu_file = STDLIB_DIR / "communication" / "ping_pong.lu"
        if not lu_file.exists():
            pytest.skip("stdlib not found")
        results = generate_from_file(lu_file, "python")
        assert len(results) >= 1
        assert results[0].protocol_name == "PingPong"
        compile(results[0].source, "<generated>", "exec")

    def test_stdlib_saga_order_nested_choice(self):
        """saga_order.lu has nested choice -- must handle correctly."""
        lu_file = STDLIB_DIR / "business" / "saga_order.lu"
        if not lu_file.exists():
            pytest.skip("stdlib not found")
        results = generate_from_file(lu_file, "python")
        assert len(results) >= 1
        compile(results[0].source, "<generated>", "exec")


# -- All 20 stdlib protocols -------------------------------------------------

class TestAllStdlibProtocols:
    """Every stdlib .lu file must generate valid Python."""

    @pytest.fixture(params=sorted(STDLIB_DIR.rglob("*.lu")) if STDLIB_DIR.exists() else [])
    def lu_file(self, request):
        return request.param

    def test_stdlib_generates_valid_python(self, lu_file):
        results = generate_from_file(lu_file, "python")
        assert len(results) >= 1
        for result in results:
            compile(result.source, f"<{lu_file.name}>", "exec")


# -- Not-yet-available targets -----------------------------------------------

class TestAllTargetsAvailable:
    """All three targets are implemented and working."""

    def test_python_available(self):
        results = generate_from_source(SIMPLE_LU, "python")
        assert len(results) == 1
        assert results[0].target == "python"

    def test_typescript_available(self):
        results = generate_from_source(SIMPLE_LU, "typescript")
        assert len(results) == 1
        assert results[0].target == "typescript"

    def test_json_schema_available(self):
        results = generate_from_source(SIMPLE_LU, "json-schema")
        assert len(results) == 1
        assert results[0].target == "json-schema"
        assert results[0].file_extension == ".json"

    def test_json_alias(self):
        results = generate_from_source(SIMPLE_LU, "json")
        assert results[0].target == "json-schema"

    def test_unknown_target_still_raises(self):
        with pytest.raises(ValueError, match="Unknown target.*rust"):
            generate_from_source(SIMPLE_LU, "rust")


class TestTypeScriptViabridge:
    """TypeScript generation works through the bridge (Sprint 3)."""

    def test_typescript_generates_from_source(self):
        results = generate_from_source(SIMPLE_LU, "typescript")
        assert len(results) == 1
        result = results[0]
        assert result.protocol_name == "HelloWorld"
        assert result.target == "typescript"
        assert result.file_extension == ".ts"

    def test_typescript_has_message_kind(self):
        results = generate_from_source(SIMPLE_LU, "typescript")
        code = results[0].source
        assert "MessageKind" in code

    def test_typescript_has_interfaces(self):
        results = generate_from_source(SIMPLE_LU, "typescript")
        code = results[0].source
        assert "interface" in code
        assert "Role" in code

    def test_typescript_has_session_class(self):
        results = generate_from_source(SIMPLE_LU, "typescript")
        code = results[0].source
        assert "class HelloWorldSession" in code

    def test_typescript_choice_protocol(self):
        results = generate_from_source(CHOICE_LU, "typescript")
        code = results[0].source
        assert "ApprovalFlowSession" in code
        assert "chooseBranch" in code

    def test_typescript_ts_alias(self):
        results = generate_from_source(SIMPLE_LU, "ts")
        assert results[0].target == "typescript"


# -- CLI integration ---------------------------------------------------------

class TestCLIGenerate:
    """Tests for `lu generate` CLI command."""

    def test_cli_help(self):
        result = subprocess.run(
            ["lu",
             "generate", "--help"],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0
        assert "python" in result.stdout  # target choice visible in help

    def test_cli_generate_python_stdout(self):
        lu_file = STDLIB_DIR / "communication" / "ping_pong.lu"
        if not lu_file.exists():
            pytest.skip("stdlib not found")
        result = subprocess.run(
            ["lu",
             "generate", "python", str(lu_file)],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0
        assert "Protocol" in result.stdout
        assert "PingPong" in result.stdout

    def test_cli_generate_dry_run(self):
        lu_file = STDLIB_DIR / "communication" / "ping_pong.lu"
        if not lu_file.exists():
            pytest.skip("stdlib not found")
        result = subprocess.run(
            ["lu",
             "generate", "python", str(lu_file), "--dry-run"],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0
        assert "Would generate" in result.stdout

    def test_cli_generate_output_file(self, tmp_path):
        lu_file = STDLIB_DIR / "communication" / "ping_pong.lu"
        if not lu_file.exists():
            pytest.skip("stdlib not found")
        out_file = tmp_path / "output.py"
        result = subprocess.run(
            ["lu",
             "generate", "python", str(lu_file), "-o", str(out_file)],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0
        assert out_file.exists()
        content = out_file.read_text()
        assert "PingPong" in content
        compile(content, "<output>", "exec")

    def test_cli_generate_output_dir(self, tmp_path):
        lu_file = STDLIB_DIR / "communication" / "ping_pong.lu"
        if not lu_file.exists():
            pytest.skip("stdlib not found")
        result = subprocess.run(
            ["lu",
             "generate", "python", str(lu_file), "-o", str(tmp_path)],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0
        generated = list(tmp_path.glob("*.py"))
        assert len(generated) == 1

    def test_cli_nonexistent_file(self):
        result = subprocess.run(
            ["lu",
             "generate", "python", "nonexistent.lu"],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 1
        assert "Error" in result.stderr

    def test_cli_typescript_generates(self):
        lu_file = STDLIB_DIR / "communication" / "ping_pong.lu"
        if not lu_file.exists():
            pytest.skip("stdlib not found")
        result = subprocess.run(
            ["lu",
             "generate", "ts", str(lu_file)],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0
        assert "MessageKind" in result.stdout
        assert "PingPong" in result.stdout
