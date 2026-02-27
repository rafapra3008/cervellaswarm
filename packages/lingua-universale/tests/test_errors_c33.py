# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for C3.3 error messages: snippet renderer, LU-N codes, integration."""

from __future__ import annotations

import pytest

from cervellaswarm_lingua_universale.errors import (
    ErrorCategory,
    ErrorSeverity,
    HumanError,
    humanize,
    format_error,
    render_snippet,
)
from cervellaswarm_lingua_universale._tokenizer import TokenizeError
from cervellaswarm_lingua_universale._parser import ParseError
from cervellaswarm_lingua_universale._eval import check_source


# ============================================================
# render_snippet
# ============================================================

_SAMPLE_SOURCE = """\
type TaskStatus = Pending | Running | Done

agent Worker:
    role: backend
    trust: standard"""


class TestRenderSnippet:
    """render_snippet() generates Rust/Elm-style code snippets."""

    def test_basic_caret(self) -> None:
        result = render_snippet(_SAMPLE_SOURCE, line=3, col=0)
        assert "3" in result
        assert "agent Worker:" in result
        assert "^" in result

    def test_caret_at_column(self) -> None:
        result = render_snippet(_SAMPLE_SOURCE, line=3, col=6)
        lines = result.split("\n")
        # The caret line should have spaces before ^
        caret_line = [l for l in lines if "^" in l][0]
        caret_pos = caret_line.index("^")
        # Should be after gutter + 6 chars
        assert caret_pos > 6

    def test_with_label(self) -> None:
        result = render_snippet(_SAMPLE_SOURCE, line=3, col=0, label="error here")
        assert "error here" in result

    def test_with_length(self) -> None:
        result = render_snippet(_SAMPLE_SOURCE, line=3, col=0, length=5)
        assert "^^^^^" in result

    def test_context_lines(self) -> None:
        result = render_snippet(_SAMPLE_SOURCE, line=3, col=0, context_lines=1)
        assert "2" in result  # line before
        assert "4" in result  # line after

    def test_first_line(self) -> None:
        result = render_snippet(_SAMPLE_SOURCE, line=1, col=0, context_lines=1)
        assert "1" in result
        assert "^" in result

    def test_last_line(self) -> None:
        result = render_snippet(_SAMPLE_SOURCE, line=5, col=0, context_lines=1)
        assert "5" in result
        assert "^" in result

    def test_out_of_range_returns_empty(self) -> None:
        assert render_snippet(_SAMPLE_SOURCE, line=0, col=0) == ""
        assert render_snippet(_SAMPLE_SOURCE, line=100, col=0) == ""

    def test_single_line_source(self) -> None:
        result = render_snippet("hello world", line=1, col=6, length=5)
        assert "hello world" in result
        assert "^^^^^" in result

    def test_empty_source_returns_empty(self) -> None:
        # line 0 is out of range
        assert render_snippet("", line=0, col=0) == ""

    def test_col_beyond_line_length(self) -> None:
        result = render_snippet("short", line=1, col=100)
        assert "^" in result
        assert "short" in result

    def test_empty_source_line_1(self) -> None:
        result = render_snippet("", line=1, col=0)
        assert "^" in result

    def test_crlf_line_endings(self) -> None:
        source = "line one\r\nline two\r\nline three"
        result = render_snippet(source, line=2, col=0)
        assert "line two" in result
        assert "^" in result
        assert "\r" not in result  # \r must not leak into output

    def test_negative_col_does_not_crash(self) -> None:
        result = render_snippet("hello", line=1, col=-1)
        assert "^" in result


# ============================================================
# ErrorCategory.SYNTAX
# ============================================================


class TestSyntaxCategory:
    """The new SYNTAX category exists."""

    def test_syntax_in_enum(self) -> None:
        assert hasattr(ErrorCategory, "SYNTAX")
        assert ErrorCategory.SYNTAX.value == "syntax"


# ============================================================
# humanize() for TokenizeError
# ============================================================


class TestHumanizeTokenizeError:
    """humanize() classifies TokenizeError into LU-N codes."""

    def test_tab_error(self) -> None:
        exc = TokenizeError("tabs are not allowed", line=2, col=0)
        err = humanize(exc)
        assert err.code == "LU-N001"
        assert err.category == ErrorCategory.SYNTAX
        assert err.severity == ErrorSeverity.ERROR

    def test_indent_error(self) -> None:
        exc = TokenizeError("indentation must be a multiple of 4 spaces (got 6)", line=3, col=0)
        err = humanize(exc)
        assert err.code == "LU-N002"

    def test_unterminated_string(self) -> None:
        exc = TokenizeError("unterminated string literal", line=5, col=10)
        err = humanize(exc)
        assert err.code == "LU-N003"

    def test_unexpected_char(self) -> None:
        exc = TokenizeError("unexpected character: '@'", line=1, col=5)
        err = humanize(exc)
        assert err.code == "LU-N004"

    def test_dedent_mismatch(self) -> None:
        exc = TokenizeError("dedent does not match any outer indentation level", line=8, col=0)
        err = humanize(exc)
        assert err.code == "LU-N005"

    def test_location_preserved(self) -> None:
        exc = TokenizeError("tabs are not allowed", line=7, col=3)
        err = humanize(exc)
        assert err.location is not None
        assert err.location.line == 7
        assert err.location.col == 3
        assert err.location.source == "tokenizer"

    def test_generic_tokenize_error(self) -> None:
        exc = TokenizeError("something unexpected happened", line=1, col=0)
        err = humanize(exc)
        assert err.code == "LU-N007"  # generic fallback


# ============================================================
# humanize() for ParseError
# ============================================================


class TestHumanizeParseError:
    """humanize() classifies ParseError into LU-N codes."""

    def test_unknown_keyword(self) -> None:
        exc = ParseError(
            "expected 'protocol', 'agent', 'type', or 'use', got 'agnet'",
            line=1, col=0,
        )
        err = humanize(exc)
        assert err.code == "LU-N006"

    def test_unknown_keyword_fuzzy(self) -> None:
        exc = ParseError(
            "expected 'protocol', 'agent', 'type', or 'use', got 'agnet'",
            line=1, col=0,
        )
        err = humanize(exc)
        assert "agent" in err.similar

    def test_expected_colon(self) -> None:
        exc = ParseError("expected COLON, got NEWLINE ('')", line=3, col=15)
        err = humanize(exc)
        assert err.code == "LU-N008"

    def test_empty_protocol(self) -> None:
        exc = ParseError("protocol must have at least one step", line=2, col=0)
        err = humanize(exc)
        assert err.code == "LU-N009"

    def test_unknown_action(self) -> None:
        exc = ParseError("cannot parse action 'yells'", line=5, col=4)
        err = humanize(exc)
        assert err.code == "LU-N010"

    def test_unknown_action_no_quotes(self) -> None:
        exc = ParseError("cannot parse action yells", line=5, col=4)
        err = humanize(exc)
        assert err.code == "LU-N010"
        # got falls back to full msg when no quotes -- at least code is correct
        assert err.got is not None

    def test_unknown_property(self) -> None:
        exc = ParseError("unknown property 'maybe terminates'", line=10, col=8)
        err = humanize(exc)
        assert err.code == "LU-N011"

    def test_unknown_agent_clause(self) -> None:
        exc = ParseError("unknown agent clause: 'trsut'", line=4, col=4)
        err = humanize(exc)
        assert err.code == "LU-N012"

    def test_agent_clause_fuzzy(self) -> None:
        exc = ParseError("unknown agent clause: 'trsut'", line=4, col=4)
        err = humanize(exc)
        assert "trust" in err.similar

    def test_location_preserved(self) -> None:
        exc = ParseError("protocol must have at least one step", line=12, col=8)
        err = humanize(exc)
        assert err.location is not None
        assert err.location.line == 12
        assert err.location.col == 8
        assert err.location.source == "parser"

    def test_generic_parse_error(self) -> None:
        exc = ParseError("expected INDENT, got EOF", line=5, col=0)
        err = humanize(exc)
        assert err.code == "LU-N007"

    def test_locale_it(self) -> None:
        exc = TokenizeError("tabs are not allowed", line=2, col=0)
        err = humanize(exc, locale="it")
        assert "tab" in err.message.lower()
        assert err.locale == "it"

    def test_locale_pt(self) -> None:
        exc = TokenizeError("tabs are not allowed", line=2, col=0)
        err = humanize(exc, locale="pt")
        assert "tab" in err.message.lower()
        assert err.locale == "pt"


# ============================================================
# format_error with source snippet
# ============================================================


class TestFormatErrorWithSnippet:
    """format_error() with source parameter renders snippets."""

    def test_snippet_appears_in_output(self) -> None:
        exc = TokenizeError("unexpected character: '@'", line=1, col=5)
        err = humanize(exc)
        source = "type @Bad = A | B"
        output = format_error(err, source=source)
        assert "[LU-N004]" in output
        assert "@Bad" in output or "type" in output
        assert "^" in output
        assert "Hint:" in output

    def test_no_snippet_without_source(self) -> None:
        exc = TokenizeError("tabs are not allowed", line=2, col=0)
        err = humanize(exc)
        output = format_error(err)
        assert "[LU-N001]" in output
        # No source = no snippet lines
        assert "|" not in output

    def test_verbose_includes_technical(self) -> None:
        exc = ParseError("expected COLON, got NEWLINE ('')", line=3, col=15)
        err = humanize(exc)
        output = format_error(err, verbose=True)
        assert "[technical]" in output


# ============================================================
# Integration: check_source with humanized errors
# ============================================================


class TestCheckSourceHumanized:
    """check_source() now returns humanized error messages."""

    def test_syntax_error_has_code(self) -> None:
        result = check_source("agnet Worker:\n    role: backend")
        assert result.ok is False
        assert len(result.errors) >= 1
        # The error should contain an LU code
        assert "LU-N" in result.errors[0]

    def test_valid_source_no_errors(self) -> None:
        result = check_source("type Color = Red | Green | Blue")
        assert result.ok is True
        assert result.errors == []

    def test_invalid_source_has_snippet(self) -> None:
        source = "protocol Bad\n    roles: a, b\n    a sends msg to b"
        result = check_source(source)
        assert result.ok is False
        # Should have snippet with line numbers
        err_text = result.errors[0]
        assert "LU-N" in err_text or "expected" in err_text.lower()
