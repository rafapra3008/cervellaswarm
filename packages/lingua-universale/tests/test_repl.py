# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for _repl.py -- Interactive REPL (C3.4).

Pattern: dependency injection of input_fn for deterministic testing.
No stdin mocking, no readline dependency.
"""

from __future__ import annotations

import pytest

from cervellaswarm_lingua_universale._repl import (
    CommandResult,
    REPLSession,
    _looks_incomplete,
)


# ============================================================
# Helper: build a session fed by a list of input lines
# ============================================================


def _make_session(lines: list[str]) -> REPLSession:
    """Create a REPLSession that reads from *lines* then raises EOFError."""
    it = iter(lines)

    def _input_fn(prompt: str) -> str:
        try:
            return next(it)
        except StopIteration:
            raise EOFError

    return REPLSession(input_fn=_input_fn)


# ============================================================
# eval() direct -- no loop
# ============================================================


class TestREPLEval:
    """Test eval() method directly (no run loop)."""

    def test_valid_type_decl(self) -> None:
        session = REPLSession()
        r = session.eval("type Color = Red | Green | Blue")
        assert r.ok

    def test_invalid_source_returns_error(self) -> None:
        session = REPLSession()
        r = session.eval("this is not valid LU !!!!")
        assert not r.ok
        assert r.errors

    def test_history_accumulates_on_success(self) -> None:
        session = REPLSession()
        session.eval("type X = A | B")
        session.eval("type Y = C | D")
        assert len(session._source_history) == 2

    def test_history_not_added_on_error(self) -> None:
        session = REPLSession()
        session.eval("type X = A | B")
        session.eval("broken broken broken")
        assert len(session._source_history) == 1

    def test_error_preserves_history(self) -> None:
        session = REPLSession()
        session.eval("type Color = Red | Green | Blue")
        session.eval("this is garbage !!!")
        assert not session.eval("this is garbage !!!").ok
        assert session._source_history == ["type Color = Red | Green | Blue"]

    def test_last_result_tracked(self) -> None:
        session = REPLSession()
        session.eval("type X = A | B")
        assert session._last_result is not None
        assert session._last_result.ok

    def test_last_error_tracked(self) -> None:
        session = REPLSession()
        session.eval("broken broken broken")
        assert session._last_error is not None


# ============================================================
# handle_command()
# ============================================================


class TestREPLCommands:
    """Test meta-commands (:help, :quit, etc.)."""

    def test_quit(self) -> None:
        session = REPLSession()
        r = session.handle_command(":quit")
        assert r.should_exit is True

    def test_q_alias(self) -> None:
        session = REPLSession()
        r = session.handle_command(":q")
        assert r.should_exit is True

    def test_exit_alias(self) -> None:
        session = REPLSession()
        r = session.handle_command(":exit")
        assert r.should_exit is True

    def test_help(self) -> None:
        session = REPLSession()
        r = session.handle_command(":help")
        assert not r.should_exit
        assert ":quit" in r.output
        assert ":help" in r.output

    def test_history_empty(self) -> None:
        session = REPLSession()
        r = session.handle_command(":history")
        assert "empty" in r.output.lower()

    def test_history_with_entries(self) -> None:
        session = REPLSession()
        session.eval("type X = A | B")
        r = session.handle_command(":history")
        assert "type X" in r.output

    def test_reset_clears_state(self) -> None:
        session = REPLSession()
        session.eval("type X = A | B")
        r = session.handle_command(":reset")
        assert "reset" in r.output.lower()
        assert session._source_history == []
        assert session._last_result is None

    def test_check_valid(self) -> None:
        session = REPLSession()
        r = session.handle_command(":check type X = A | B")
        assert "OK" in r.output

    def test_check_invalid(self) -> None:
        session = REPLSession()
        r = session.handle_command(":check broken broken")
        assert r.output  # error message present

    def test_check_no_arg_shows_usage(self) -> None:
        session = REPLSession()
        r = session.handle_command(":check")
        assert "Usage" in r.output
        assert not r.should_exit

    def test_unknown_command(self) -> None:
        session = REPLSession()
        r = session.handle_command(":foobar")
        assert "Unknown command" in r.output


# ============================================================
# _is_complete() -- multiline detection
# ============================================================


class TestIsComplete:
    """Test multiline completeness heuristics."""

    def test_valid_oneliner_is_complete(self) -> None:
        session = REPLSession()
        complete, has_error = session._is_complete("type X = A | B")
        assert complete is True
        assert has_error is False

    def test_colon_ending_is_incomplete(self) -> None:
        session = REPLSession()
        complete, has_error = session._is_complete("protocol Ping:")
        assert complete is False

    def test_indented_continuation_is_incomplete(self) -> None:
        session = REPLSession()
        source = "protocol Ping:\n    roles: a, b"
        complete, has_error = session._is_complete(source)
        assert complete is False

    def test_definitive_error_is_complete_with_error(self) -> None:
        session = REPLSession()
        complete, has_error = session._is_complete("broken broken broken")
        assert complete is True
        assert has_error is True


# ============================================================
# _looks_incomplete() unit tests
# ============================================================


class TestLooksIncomplete:
    """Unit tests for the multiline heuristic function."""

    def test_colon_ending(self) -> None:
        assert _looks_incomplete("protocol Ping:", "") is True

    def test_eof_signal(self) -> None:
        assert _looks_incomplete("x", "unexpected EOF") is True

    def test_indent_signal(self) -> None:
        assert _looks_incomplete("x", "expected INDENT") is True

    def test_unterminated_signal(self) -> None:
        assert _looks_incomplete("x", "unterminated string literal") is True

    def test_definitive_error(self) -> None:
        assert _looks_incomplete("broken", "some definitive error") is False

    def test_indented_last_line(self) -> None:
        assert _looks_incomplete("protocol P:\n    roles: a", "") is True

    def test_single_flat_line(self) -> None:
        assert _looks_incomplete("type X = A", "some error") is False


# ============================================================
# run() loop -- integration with input_fn
# ============================================================


class TestREPLLoop:
    """Test the full run() loop with injected input."""

    def test_quit_exits(self, capsys: pytest.CaptureFixture[str]) -> None:
        session = _make_session([":quit"])
        session.run()
        captured = capsys.readouterr()
        assert "Lingua Universale" in captured.out  # banner printed

    def test_eof_exits_gracefully(self, capsys: pytest.CaptureFixture[str]) -> None:
        session = _make_session([])  # immediate EOF
        session.run()
        # Should not raise

    def test_single_type_decl(self, capsys: pytest.CaptureFixture[str]) -> None:
        session = _make_session([
            "type Color = Red | Green | Blue",
            "",       # empty line triggers execution
            ":quit",
        ])
        session.run()
        captured = capsys.readouterr()
        assert "OK" in captured.out

    def test_help_command_in_loop(self, capsys: pytest.CaptureFixture[str]) -> None:
        session = _make_session([":help", ":quit"])
        session.run()
        captured = capsys.readouterr()
        assert ":quit" in captured.out
        assert ":help" in captured.out

    def test_error_displayed(self, capsys: pytest.CaptureFixture[str]) -> None:
        session = _make_session([
            "broken broken broken",
            "",  # triggers execution
            ":quit",
        ])
        session.run()
        captured = capsys.readouterr()
        # Error output goes through output_fn (which is print -> stdout)
        assert captured.out  # something was printed

    def test_reset_in_loop(self, capsys: pytest.CaptureFixture[str]) -> None:
        session = _make_session([
            "type X = A | B",
            "",
            ":reset",
            ":history",
            ":quit",
        ])
        session.run()
        captured = capsys.readouterr()
        assert "reset" in captured.out.lower()
        assert "empty" in captured.out.lower()

    def test_keyboard_interrupt_resets_buffer(
        self, capsys: pytest.CaptureFixture[str],
    ) -> None:
        call_count = 0

        def _input_fn(prompt: str) -> str:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return "protocol Ping:"
            if call_count == 2:
                raise KeyboardInterrupt
            if call_count == 3:
                return ":quit"
            raise EOFError

        session = REPLSession(input_fn=_input_fn)
        session.run()
        # Should not crash, should exit via :quit

    def test_double_empty_resets_buffer(
        self, capsys: pytest.CaptureFixture[str],
    ) -> None:
        session = _make_session([
            "protocol P:",
            "    roles: a, b",
            "",   # first empty -> tries execution (incomplete)
            "",   # second empty -> forces reset
            ":quit",
        ])
        session.run()
        # Should not crash; buffer was reset, no OK expected

    def test_multiline_block(self, capsys: pytest.CaptureFixture[str]) -> None:
        session = _make_session([
            "protocol Ping:",
            "    roles: sender, receiver",
            "    sender sends ping to receiver",
            "",       # empty line -> execute
            ":quit",
        ])
        session.run()
        captured = capsys.readouterr()
        assert "OK" in captured.out


# ============================================================
# NO_COLOR / FORCE_COLOR
# ============================================================


class TestREPLColors:
    """Test color initialization respects env vars."""

    @pytest.fixture(autouse=True)
    def _clean_colors(self) -> None:  # noqa: PT004
        """Reset color singleton after each test to avoid pollution."""
        yield
        from cervellaswarm_lingua_universale._colors import reset_colors
        reset_colors()

    def test_no_color_disables(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("NO_COLOR", "1")
        from cervellaswarm_lingua_universale._colors import colors, init_colors, reset_colors
        reset_colors()
        init_colors()
        assert colors.RESET == ""
        assert colors.RED == ""

    def test_force_color_enables(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("FORCE_COLOR", "1")
        monkeypatch.delenv("NO_COLOR", raising=False)
        from cervellaswarm_lingua_universale._colors import colors, init_colors, reset_colors
        reset_colors()
        init_colors()
        assert colors.RESET == "\033[0m"
        assert colors.RED == "\033[31m"


# ============================================================
# CLI integration: lu repl subcommand
# ============================================================


class TestCLIReplSubcommand:
    """Test that 'repl' subcommand is registered in CLI."""

    def test_repl_in_parser(self) -> None:
        from cervellaswarm_lingua_universale._cli import _build_parser
        parser = _build_parser()
        # The repl subcommand should parse without error
        args = parser.parse_args(["repl"])
        assert args.command == "repl"

    def test_repl_in_handlers(self) -> None:
        from cervellaswarm_lingua_universale._cli import _COMMAND_HANDLERS
        assert "repl" in _COMMAND_HANDLERS
