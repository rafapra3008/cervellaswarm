# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Interactive REPL for Lingua Universale (C3.4 + C3.6).

Usage::

    lu repl          Start the interactive REPL.

Or programmatically::

    from cervellaswarm_lingua_universale._repl import REPLSession
    session = REPLSession()
    session.run()

For testing, inject *input_fn* and *output_fn*::

    inputs = iter(["type X = A | B", ":quit"])
    session = REPLSession(input_fn=lambda p: next(inputs))
    session.run()

Design decisions (STUDIO C3.1, S421):
    D2: stdlib REPL (readline, ZERO external deps).
    D4: REPLSession class stateful.
    Raw readline loop (not cmd.Cmd) -- better fit for a language REPL.
    Colon-prefixed commands (:help, :quit, :reset, :history, :check).
    Multiline via parse-and-check heuristics.
    NO_COLOR / FORCE_COLOR support via shared ``_colors`` module (C3.6).
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from typing import Callable

from ._colors import colors as _c, init_colors as _init_colors
from ._eval import check_source, run_source, EvalResult


# ============================================================
# Multiline heuristics
# ============================================================

_INCOMPLETE_SIGNALS = (
    "unexpected EOF",
    "expected INDENT",
    "unterminated",
    "LU-N003",
    "LU-N009",
)


def _looks_incomplete(source: str, error_text: str) -> bool:
    """Distinguish 'needs more input' from 'definitive error'.

    Returns True if the error likely means the user hasn't finished
    typing (open block, unterminated string, etc.).
    """
    stripped = source.rstrip()
    if stripped.endswith(":"):
        return True
    # Last non-empty line is indented -> block still open
    lines = [ln for ln in source.split("\n") if ln.strip()]
    if len(lines) > 1 and lines[-1].startswith("    "):
        return True
    for signal in _INCOMPLETE_SIGNALS:
        if signal in error_text:
            return True
    return False


# ============================================================
# REPL command result
# ============================================================


@dataclass
class CommandResult:
    """Outcome of a REPL meta-command (:help, :quit, etc.)."""
    should_exit: bool = False
    output: str = ""


# ============================================================
# Help text
# ============================================================

_HELP_TEXT = """\
Lingua Universale REPL commands:
  :help          Show this help
  :quit  :q  :exit   Exit the REPL
  :reset         Clear session state
  :history       Show input history
  :check <src>   Check a one-line source without executing

Keyboard:
  Ctrl+D         Exit
  Ctrl+C         Cancel current input
  Up/Down        Navigate history

Multiline:
  End a line with ':' to start a block.
  Press Enter on an empty line to execute.
  Two consecutive empty lines force a buffer reset."""


# ============================================================
# REPLSession
# ============================================================


class REPLSession:
    """Stateful interactive session for Lingua Universale.

    Parameters:
        input_fn:  Replaces ``input()`` -- inject for testing.
        output_fn: Replaces ``print()`` -- inject for testing.
    """

    PROMPT = "lu>  "
    PROMPT_CONT = "...  "
    HISTORY_FILE = os.path.expanduser("~/.lu_history")
    HISTORY_LENGTH = 1000

    def __init__(
        self,
        *,
        input_fn: Callable[[str], str] = input,
        output_fn: Callable[..., None] | None = None,
    ) -> None:
        self._input_fn = input_fn
        self._output_fn: Callable[..., None] = output_fn or print
        self._source_history: list[str] = []
        self._last_result: EvalResult | None = None
        self._last_error: str | None = None

    # --------------------------------------------------------
    # Public API
    # --------------------------------------------------------

    def run(self) -> None:
        """Main REPL loop.  Blocks until ``:quit`` or ``Ctrl+D``."""
        _init_colors()
        self._setup_readline()
        self._print_banner()

        buffer: list[str] = []

        while True:
            prompt = self.PROMPT_CONT if buffer else self.PROMPT
            colored_prompt = f"{_c.CYAN}{_c.BOLD}{prompt}{_c.RESET}" if _c.CYAN else prompt

            try:
                line = self._input_fn(colored_prompt)
            except EOFError:
                self._output_fn("")  # trailing newline
                break
            except KeyboardInterrupt:
                self._output_fn("")
                buffer.clear()
                continue

            stripped = line.strip()

            # Meta-commands -- only when buffer is empty
            if not buffer and stripped.startswith(":"):
                result = self.handle_command(stripped)
                if result.should_exit:
                    break
                if result.output:
                    self._output_fn(result.output)
                continue

            buffer.append(line)

            # Empty line -> attempt execution if buffer has content
            if not stripped:
                if len(buffer) <= 1:
                    buffer.clear()
                    continue
                # Check for double-empty (force reset)
                if len(buffer) >= 2 and buffer[-2].strip() == "":
                    source = "\n".join(buffer[:-2]).strip()
                    if source:
                        self._execute(source)
                    buffer.clear()
                    continue
                source = "\n".join(buffer).strip()
                if source:
                    self._execute(source)
                buffer.clear()
                continue

            # Check completeness
            source = "\n".join(buffer)
            complete, has_error = self._is_complete(source)
            if complete:
                if has_error:
                    self._execute(source)
                    buffer.clear()
                elif not source.rstrip().endswith(":"):
                    self._execute(source)
                    buffer.clear()
                # else: block still open, keep accumulating

        self._save_readline()

    def eval(self, source: str) -> EvalResult:
        """Evaluate LU source and track history.  For programmatic use."""
        result = run_source(source)
        if result.ok:
            self._source_history.append(source)
            self._last_result = result
            self._last_error = None
        else:
            self._last_error = result.errors[0] if result.errors else None
        return result

    def handle_command(self, cmd: str) -> CommandResult:
        """Process a colon-prefixed meta-command."""
        parts = cmd.split(None, 1)
        name = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if name in (":quit", ":q", ":exit"):
            return CommandResult(should_exit=True)

        if name == ":help":
            return CommandResult(output=f"{_c.YELLOW}{_HELP_TEXT}{_c.RESET}")

        if name == ":history":
            if not self._source_history:
                return CommandResult(output=f"  {_c.YELLOW}(empty){_c.RESET}")
            lines = [
                f"  {_c.CYAN}{i + 1}{_c.RESET}: {s[:72]}"
                for i, s in enumerate(self._source_history)
            ]
            return CommandResult(output="\n".join(lines))

        if name == ":reset":
            self._source_history.clear()
            self._last_result = None
            self._last_error = None
            return CommandResult(output=f"{_c.GREEN}Session reset.{_c.RESET}")

        if name == ":check":
            if not arg:
                return CommandResult(
                    output=f"{_c.RED}Usage: :check <source>{_c.RESET}",
                )
            result = check_source(arg)
            if result.ok:
                summary = self._compiled_summary(result)
                msg = f"{_c.GREEN}{_c.BOLD}OK{_c.RESET}"
                if summary:
                    msg += f"  {_c.CYAN}{summary}{_c.RESET}"
                return CommandResult(output=msg)
            return CommandResult(
                output=f"{_c.RED}{result.errors[0]}{_c.RESET}",
            )

        return CommandResult(
            output=f"{_c.RED}Unknown command: {name}{_c.RESET}  Type :help for commands.",
        )

    # --------------------------------------------------------
    # Internal helpers
    # --------------------------------------------------------

    @staticmethod
    def _compiled_summary(result: EvalResult) -> str:
        """Build a short summary of compiled declarations."""
        parts: list[str] = []
        if result.compiled:
            if result.compiled.agents:
                parts.append(f"{len(result.compiled.agents)} agent(s)")
            if result.compiled.protocols:
                parts.append(f"{len(result.compiled.protocols)} protocol(s)")
            if result.compiled.types:
                parts.append(f"{len(result.compiled.types)} type(s)")
        return ", ".join(parts)

    def _execute(self, source: str) -> None:
        """Run source and print result."""
        result = self.eval(source)
        if result.ok:
            summary = self._compiled_summary(result)
            tail = f"  {summary}" if summary else ""
            self._output_fn(f"{_c.GREEN}{_c.BOLD}OK{_c.RESET}{tail}")
        else:
            for err in result.errors:
                self._output_fn(f"{_c.RED}{err}{_c.RESET}")

    def _is_complete(self, source: str) -> tuple[bool, bool]:
        """Check whether accumulated source is complete.

        Returns:
            (is_complete, has_error):
              - (True, False)  -- valid and complete, ready to eval.
              - (True, True)   -- definitive error, show it now.
              - (False, False) -- incomplete, ask for more input.
        """
        result = check_source(source)
        if result.ok:
            return True, False
        error_text = result.errors[0] if result.errors else ""
        if _looks_incomplete(source, error_text):
            return False, False
        return True, True

    def _print_banner(self) -> None:
        from . import __version__
        self._output_fn(
            f"{_c.CYAN}{_c.BOLD}Lingua Universale v{__version__}{_c.RESET}  "
            f"-- the first language native to AI",
        )
        self._output_fn(
            f"Type {_c.BOLD}:help{_c.RESET} for commands, "
            f"{_c.BOLD}Ctrl+D{_c.RESET} to exit.",
        )

    def _setup_readline(self) -> None:
        """Load readline history.  Graceful no-op if unavailable."""
        try:
            import readline as _rl
            if os.path.exists(self.HISTORY_FILE):
                _rl.read_history_file(self.HISTORY_FILE)
            _rl.set_history_length(self.HISTORY_LENGTH)
        except (ImportError, OSError):
            pass

    def _save_readline(self) -> None:
        """Persist readline history.  Graceful no-op if unavailable."""
        try:
            import readline as _rl
            _rl.write_history_file(self.HISTORY_FILE)
        except (ImportError, OSError):
            pass
