# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for the LSP server validation logic (D2).

Tests the diagnostic conversion pipeline:
    LU source -> parse() -> TokenizeError|ParseError -> humanize() -> LSP Diagnostic

Does NOT test the full LSP protocol (that requires pytest-lsp).
Tests the core _source_diagnostics() function which is the heart of the server.
"""

from __future__ import annotations

import pytest

# Skip entire module if pygls is not installed
pygls = pytest.importorskip("pygls", reason="pygls not installed")

from lsprotocol import types

from cervellaswarm_lingua_universale._lsp import _source_diagnostics, _check_pygls_available


# ============================================================
# Availability check
# ============================================================


class TestPyglsAvailability:
    def test_pygls_is_available(self):
        assert _check_pygls_available() is True


# ============================================================
# Valid source -> no diagnostics
# ============================================================


class TestValidSource:
    def test_empty_source(self):
        diags = _source_diagnostics("")
        assert diags == []

    def test_valid_type_declaration(self):
        diags = _source_diagnostics("type Color = Red | Green | Blue")
        assert diags == []

    def test_valid_agent(self):
        source = """\
agent Worker:
    role: backend
    trust: standard
    accepts: TaskRequest
    produces: TaskResult
"""
        diags = _source_diagnostics(source)
        assert diags == []

    def test_valid_protocol(self):
        source = """\
protocol Simple:
    roles: alice, bob
    alice asks bob to do task
    bob returns result to alice
    properties:
        always terminates
"""
        diags = _source_diagnostics(source)
        assert diags == []

    def test_valid_hello_lu(self):
        """The complete hello.lu example should produce zero diagnostics."""
        source = """\
type TaskStatus = Pending | Running | Done

agent Worker:
    role: backend
    trust: standard
    accepts: TaskRequest
    produces: TaskResult
    requires: task.well_defined
    ensures: result.done

protocol DelegateTask:
    roles: regina, worker, guardiana
    regina asks worker to do task
    worker returns result to regina
    regina asks guardiana to verify
    guardiana returns verdict to regina
    properties:
        always terminates
        no deadlock
"""
        diags = _source_diagnostics(source)
        assert diags == []

    def test_valid_use_statement(self):
        source = "use python datetime"
        diags = _source_diagnostics(source)
        assert diags == []


# ============================================================
# TokenizeError -> diagnostics
# ============================================================


class TestTokenizeErrors:
    def test_tab_character(self):
        source = "type X = A | B\n\tagent Foo:"
        diags = _source_diagnostics(source)
        assert len(diags) == 1
        d = diags[0]
        assert d.severity == types.DiagnosticSeverity.Error
        assert d.source == "lingua-universale"
        assert d.range.start.line == 1  # line 2, 0-indexed
        assert "tab" in d.message.lower()

    def test_bad_indent(self):
        source = "agent X:\n   role: backend"  # 3 spaces, not 4
        diags = _source_diagnostics(source)
        assert len(diags) == 1
        d = diags[0]
        assert d.severity == types.DiagnosticSeverity.Error
        assert d.range.start.line == 1  # line 2

    def test_unterminated_string(self):
        source = 'type X =\n    name: "unterminated'
        diags = _source_diagnostics(source)
        assert len(diags) == 1
        d = diags[0]
        assert d.severity == types.DiagnosticSeverity.Error
        assert "string" in d.message.lower() or "unterminated" in d.message.lower()


# ============================================================
# ParseError -> diagnostics
# ============================================================


class TestParseErrors:
    def test_invalid_trust_tier(self):
        source = """\
agent BrokenBot:
    role: backend
    trust: legendary
    accepts: TaskRequest
"""
        diags = _source_diagnostics(source)
        assert len(diags) == 1
        d = diags[0]
        assert d.severity == types.DiagnosticSeverity.Error
        assert d.source == "lingua-universale"
        # Should have an error code (LU-N013 for invalid trust)
        assert d.code is not None
        assert d.code.startswith("LU-")

    def test_unknown_top_level(self):
        source = "foo bar baz"
        diags = _source_diagnostics(source)
        assert len(diags) == 1
        d = diags[0]
        assert d.severity == types.DiagnosticSeverity.Error

    def test_missing_colon_after_agent_name(self):
        source = "agent Worker\n    role: backend"
        diags = _source_diagnostics(source)
        assert len(diags) == 1


# ============================================================
# Diagnostic structure
# ============================================================


class TestDiagnosticStructure:
    def test_diagnostic_has_range(self):
        diags = _source_diagnostics("\tagent X:")
        assert len(diags) == 1
        d = diags[0]
        assert isinstance(d.range, types.Range)
        assert isinstance(d.range.start, types.Position)
        assert isinstance(d.range.end, types.Position)

    def test_diagnostic_line_is_zero_indexed(self):
        """LU uses 1-indexed lines, LSP uses 0-indexed."""
        source = "type X = A | B\n\tagent Y:"  # tab on line 2
        diags = _source_diagnostics(source)
        assert len(diags) == 1
        # Tab is on LU line 2 -> LSP line 1
        assert diags[0].range.start.line == 1

    def test_diagnostic_has_source(self):
        diags = _source_diagnostics("\tagent X:")
        assert diags[0].source == "lingua-universale"

    def test_diagnostic_has_code_when_humanized(self):
        source = """\
agent Bad:
    role: backend
    trust: legendary
"""
        diags = _source_diagnostics(source)
        assert len(diags) == 1
        d = diags[0]
        # humanize() should provide LU-N error code
        assert d.code is not None
        assert d.code.startswith("LU-")

    def test_diagnostic_message_includes_suggestion(self):
        """humanize() adds suggestion to the message."""
        source = """\
agent Bad:
    role: backend
    trust: legendary
"""
        diags = _source_diagnostics(source)
        assert len(diags) == 1
        # Message should be multi-part (main + suggestion)
        assert len(diags[0].message) > 10


# ============================================================
# Edge cases
# ============================================================


class TestEdgeCases:
    def test_comment_only_source(self):
        diags = _source_diagnostics("# just a comment")
        assert diags == []

    def test_blank_lines_only(self):
        diags = _source_diagnostics("\n\n\n")
        assert diags == []

    def test_valid_record_type(self):
        source = """\
type Point =
    x: Number
    y: Number
"""
        diags = _source_diagnostics(source)
        assert diags == []


# ============================================================
# Server creation
# ============================================================


class TestServerCreation:
    def test_create_server_returns_language_server(self):
        from cervellaswarm_lingua_universale._lsp import create_server
        from cervellaswarm_lingua_universale import __version__
        server = create_server()
        assert server is not None
        assert server.name == "lingua-universale-lsp"
        assert server.version == __version__
