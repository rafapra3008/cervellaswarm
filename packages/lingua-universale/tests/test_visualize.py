# SPDX-License-Identifier: Apache-2.0
"""Tests for _visualize.py -- diagram generation from .lu protocols."""

from pathlib import Path

import pytest

from cervellaswarm_lingua_universale._visualize import (
    generate_mermaid,
    generate_mermaid_fenced,
    visualize_source,
    visualize_file,
)

EXAMPLES_DIR = Path(__file__).parent.parent / "examples"
STDLIB_DIR = (
    Path(__file__).parent.parent
    / "src"
    / "cervellaswarm_lingua_universale"
    / "stdlib"
)


# ---------------------------------------------------------------------------
# Mermaid generation from AST
# ---------------------------------------------------------------------------

class TestGenerateMermaid:
    def test_hello_world(self):
        from cervellaswarm_lingua_universale._parser import parse
        from cervellaswarm_lingua_universale._ast import ProtocolNode

        source = (EXAMPLES_DIR / "hello.lu").read_text(encoding="utf-8")
        program = parse(source)
        protocols = [d for d in program.declarations if isinstance(d, ProtocolNode)]
        diagram = generate_mermaid(protocols[0])

        assert "sequenceDiagram" in diagram
        assert "participant regina" in diagram
        assert "participant worker" in diagram
        assert "regina->>+worker:" in diagram
        assert "worker->>+regina:" in diagram

    def test_choice_branching(self):
        from cervellaswarm_lingua_universale._parser import parse
        from cervellaswarm_lingua_universale._ast import ProtocolNode

        source = (STDLIB_DIR / "business" / "approval_workflow.lu").read_text(encoding="utf-8")
        program = parse(source)
        protocols = [d for d in program.declarations if isinstance(d, ProtocolNode)]
        diagram = generate_mermaid(protocols[0])

        assert "alt approve" in diagram
        assert "else reject" in diagram
        assert "end" in diagram

    def test_fenced_wraps_in_backticks(self):
        from cervellaswarm_lingua_universale._parser import parse
        from cervellaswarm_lingua_universale._ast import ProtocolNode

        source = (EXAMPLES_DIR / "hello.lu").read_text(encoding="utf-8")
        program = parse(source)
        protocols = [d for d in program.declarations if isinstance(d, ProtocolNode)]
        fenced = generate_mermaid_fenced(protocols[0])

        assert fenced.startswith("```mermaid\n")
        assert fenced.endswith("\n```")


# ---------------------------------------------------------------------------
# High-level API
# ---------------------------------------------------------------------------

class TestVisualizeSource:
    def test_simple_protocol(self):
        source = """\
protocol Ping:
    roles: client, server
    client asks server to do ping
    server returns pong to client
"""
        result = visualize_source(source)
        assert "sequenceDiagram" in result
        assert "client->>+server:" in result

    def test_fenced_output(self):
        source = """\
protocol Ping:
    roles: client, server
    client asks server to do ping
    server returns pong to client
"""
        result = visualize_source(source, fenced=True)
        assert result.startswith("```mermaid\n")

    def test_no_protocol_raises(self):
        source = "type Foo = Bar | Baz\n"
        with pytest.raises(ValueError, match="No protocol"):
            visualize_source(source)

    def test_unsupported_format_raises(self):
        source = """\
protocol P:
    roles: a, b
    a asks b to do x
    b returns y to a
"""
        with pytest.raises(ValueError, match="Unsupported format"):
            visualize_source(source, fmt="dot")


class TestVisualizeFile:
    def test_hello_lu(self):
        result = visualize_file(EXAMPLES_DIR / "hello.lu")
        assert "sequenceDiagram" in result
        assert "participant regina" in result

    def test_payment_auth(self):
        result = visualize_file(EXAMPLES_DIR / "payment_auth.lu")
        assert "participant merchant" in result
        assert "participant auth" in result
        assert "participant gateway" in result
        assert "asks verify identity" in result

    def test_nonexistent_file_raises(self):
        with pytest.raises(OSError):
            visualize_file("/nonexistent/file.lu")


# ---------------------------------------------------------------------------
# Stdlib regression: all 20 protocols must visualize without error
# ---------------------------------------------------------------------------

class TestStdlibVisualize:
    @pytest.fixture(params=sorted(STDLIB_DIR.rglob("*.lu")))
    def stdlib_file(self, request):
        return request.param

    def test_stdlib_protocol_visualizes(self, stdlib_file):
        """Every stdlib .lu file must produce a valid Mermaid diagram."""
        result = visualize_file(stdlib_file)
        assert "sequenceDiagram" in result
        assert "participant" in result
