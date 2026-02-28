# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Command-line interface for Lingua Universale (C3.2 + C3.4 + C3.6 + D2).

Subcommands::

    lu run <file.lu>      Parse, compile, and execute a .lu file.
    lu check <file.lu>    Parse and compile without executing (fast).
    lu verify <file.lu>   Parse, compile, and formally verify with Lean 4.
    lu compile <file.lu>  Show the generated Python source.
    lu repl               Start the interactive REPL.
    lu lsp                Start the Language Server Protocol server (STDIO).
    lu version            Show version information.

Design decisions (STUDIO C3):
    D1: argparse stdlib -- ZERO external dependencies.
    Console script entry: ``lu = cervellaswarm_lingua_universale._cli:main``
    C3.6: Colors shared via ``_colors`` module (NO_COLOR / FORCE_COLOR).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ._colors import colors as _c, init_colors as _init_colors
from ._eval import check_file, verify_file, run_file, EvalResult


def _print_result(result: EvalResult, *, verbose: bool = False) -> None:
    """Print an EvalResult to stdout/stderr."""
    if result.ok:
        print(f"{_c.GREEN}{_c.BOLD}OK{_c.RESET} {result.source_file}")
    else:
        print(
            f"{_c.RED}{_c.BOLD}ERROR{_c.RESET} {result.source_file}",
            file=sys.stderr,
        )
        for err in result.errors:
            print(f"  {_c.RED}{err}{_c.RESET}", file=sys.stderr)


# ============================================================
# Subcommand handlers
# ============================================================


def _cmd_check(args: argparse.Namespace) -> int:
    """Handle ``lu check <file>``."""
    result = check_file(args.file)
    _print_result(result)
    if result.ok:
        decls = ""
        if result.compiled:
            parts = []
            if result.compiled.agents:
                parts.append(f"{len(result.compiled.agents)} agent(s)")
            if result.compiled.protocols:
                parts.append(f"{len(result.compiled.protocols)} protocol(s)")
            if result.compiled.types:
                parts.append(f"{len(result.compiled.types)} type(s)")
            if result.compiled.imports:
                parts.append(f"{len(result.compiled.imports)} import(s)")
            decls = ", ".join(parts)
        if decls:
            print(f"  {_c.CYAN}{decls}{_c.RESET}")
    return 0 if result.ok else 1


def _cmd_run(args: argparse.Namespace) -> int:
    """Handle ``lu run <file>``."""
    result = run_file(args.file)
    _print_result(result)
    if result.ok and result.module:
        # Show exported names from the module
        exports = [
            name
            for name in dir(result.module)
            if not name.startswith("_")
        ]
        if exports:
            print(f"  {_c.CYAN}Loaded: {', '.join(exports)}{_c.RESET}")
    return 0 if result.ok else 1


def _cmd_verify(args: argparse.Namespace) -> int:
    """Handle ``lu verify <file>``."""
    result = verify_file(args.file)
    _print_result(result)
    if result.ok:
        for line in result.verification:
            print(f"  {_c.YELLOW}{line}{_c.RESET}")
    return 0 if result.ok else 1


def _cmd_compile(args: argparse.Namespace) -> int:
    """Handle ``lu compile <file>``."""
    result = check_file(args.file)
    if not result.ok:
        _print_result(result)
        return 1

    if result.python_source:
        if args.output:
            out_path = Path(args.output)
            try:
                out_path.write_text(result.python_source, encoding="utf-8")
            except (PermissionError, OSError) as exc:
                print(f"{_c.RED}{_c.BOLD}ERROR{_c.RESET} {exc}", file=sys.stderr)
                return 1
            print(
                f"{_c.GREEN}{_c.BOLD}OK{_c.RESET} "
                f"Compiled {result.source_file} -> {out_path}"
            )
        else:
            print(result.python_source)
    return 0


def _cmd_repl(args: argparse.Namespace) -> int:
    """Handle ``lu repl``."""
    from ._repl import REPLSession

    session = REPLSession()
    session.run()
    return 0


def _cmd_lsp(args: argparse.Namespace) -> int:
    """Handle ``lu lsp``."""
    from ._lsp import start_lsp

    return start_lsp()


def _cmd_version(args: argparse.Namespace) -> int:
    """Handle ``lu version``."""
    from . import __version__

    print(f"Lingua Universale {_c.BOLD}v{__version__}{_c.RESET}")
    print("The first programming language native to AI.")
    print(f"  {_c.CYAN}Session types + Formal verification + ZERO deps{_c.RESET}")
    return 0


# ============================================================
# Argument parser
# ============================================================


def _build_parser() -> argparse.ArgumentParser:
    """Build the argparse parser with all subcommands."""
    parser = argparse.ArgumentParser(
        prog="lu",
        description="Lingua Universale - the first programming language native to AI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # lu check
    p_check = subparsers.add_parser(
        "check",
        help="Parse and compile a .lu file (no execution)",
    )
    p_check.add_argument("file", help="Path to the .lu source file")

    # lu run
    p_run = subparsers.add_parser(
        "run",
        help="Parse, compile, and execute a .lu file",
    )
    p_run.add_argument("file", help="Path to the .lu source file")

    # lu verify
    p_verify = subparsers.add_parser(
        "verify",
        help="Parse, compile, and formally verify a .lu file",
    )
    p_verify.add_argument("file", help="Path to the .lu source file")

    # lu compile
    p_compile = subparsers.add_parser(
        "compile",
        help="Show or save the generated Python source",
    )
    p_compile.add_argument("file", help="Path to the .lu source file")
    p_compile.add_argument(
        "-o", "--output",
        help="Write Python output to file instead of stdout",
    )

    # lu repl
    subparsers.add_parser("repl", help="Start the interactive REPL")

    # lu lsp
    subparsers.add_parser(
        "lsp",
        help="Start the Language Server Protocol server (requires pygls)",
    )

    # lu version
    subparsers.add_parser("version", help="Show version information")

    return parser


# ============================================================
# Main entry point
# ============================================================


_COMMAND_HANDLERS = {
    "check": _cmd_check,
    "run": _cmd_run,
    "verify": _cmd_verify,
    "compile": _cmd_compile,
    "repl": _cmd_repl,
    "lsp": _cmd_lsp,
    "version": _cmd_version,
}


def main(argv: list[str] | None = None) -> int:
    """CLI entry point.  Returns exit code (0 = success)."""
    _init_colors()

    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    handler = _COMMAND_HANDLERS.get(args.command)
    if handler is None:
        parser.print_help()
        return 1

    return handler(args)
