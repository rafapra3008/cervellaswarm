# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Command-line interface for Lingua Universale (C3.2 + C3.4 + C3.6 + D2 + E.3 + E.4 + T3.3 + B5 + B6).

Subcommands::

    lu run <file.lu>      Parse, compile, and execute a .lu file.
    lu check <file.lu>    Parse and compile without executing (fast).
    lu verify <file.lu>   Parse, compile, and formally verify with Lean 4.
    lu compile <file.lu>  Show the generated Python source.
    lu lint <path>        Check style, correctness, and best practices (B5).
    lu fmt <path>         Format to canonical style, zero-config (B6).
    lu init <name>        Create a new LU project with scaffolding (T3.3).
    lu repl               Start the interactive REPL.
    lu chat               Interactive guided protocol builder (E.2+E.4).
    lu demo               Run the La Nonna demo autonomously (E.5).
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
    for line in result.verification:
        if line.startswith("  All") and "PASSED" in line:
            print(f"  {_c.GREEN}{_c.BOLD}{line}{_c.RESET}")
        elif "VIOLATED." in line:
            print(f"  {_c.RED}{_c.BOLD}{line}{_c.RESET}")
        elif "PROVED" in line or "SATISFIED" in line:
            print(f"  {_c.GREEN}{line}{_c.RESET}")
        elif "VIOLATED" in line:
            print(f"  {_c.RED}{line}{_c.RESET}")
        elif "SKIPPED" in line:
            print(f"  {_c.YELLOW}{line}{_c.RESET}")
        else:
            print(f"  {_c.CYAN}{line}{_c.RESET}")
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


def _cmd_init(args: argparse.Namespace) -> int:
    """Handle ``lu init <name>``."""
    from ._init_project import init_project, list_templates

    # --list-templates: show available and exit
    if getattr(args, "list_templates", False):
        templates = list_templates()
        if not templates:
            print("No stdlib templates found.")
            return 0
        print(f"{_c.BOLD}Available templates ({len(templates)}):{_c.RESET}")
        for t in templates:
            print(f"  {_c.CYAN}{t}{_c.RESET}")
        return 0

    if not args.name:
        print(
            f"{_c.RED}{_c.BOLD}ERROR{_c.RESET} "
            "project name is required (e.g. lu init my-protocol)",
            file=sys.stderr,
        )
        return 1

    try:
        created = init_project(
            args.name,
            minimal=args.minimal,
            force=args.force,
            template=getattr(args, "template", None),
        )
    except (ValueError, OSError) as exc:
        print(f"{_c.RED}{_c.BOLD}ERROR{_c.RESET} {exc}", file=sys.stderr)
        return 1

    tmpl_info = ""
    if getattr(args, "template", None):
        tmpl_info = f" (from template {_c.CYAN}{args.template}{_c.RESET})"

    print(
        f"{_c.GREEN}{_c.BOLD}Created{_c.RESET} "
        f"LU project {_c.BOLD}{args.name}{_c.RESET}{tmpl_info}"
    )
    for path in created:
        print(f"  {_c.CYAN}{path}{_c.RESET}")
    print()
    print(f"  Next: {_c.BOLD}lu check {args.name}/{args.name}.lu{_c.RESET}")
    return 0


def _cmd_lsp(args: argparse.Namespace) -> int:
    """Handle ``lu lsp``."""
    from ._lsp import start_lsp

    return start_lsp()


def _cmd_chat(args: argparse.Namespace) -> int:
    """Handle ``lu chat``."""
    from ._intent_bridge import ChatSession

    nl_processor = None
    if getattr(args, "mode", "guided") == "nl":
        try:
            from ._nl_processor import ClaudeNLProcessor
            nl_processor = ClaudeNLProcessor()
        except ImportError as exc:
            print(
                f"{_c.RED}{_c.BOLD}ERROR{_c.RESET} {exc}",
                file=sys.stderr,
            )
            return 1

    input_fn = None
    if getattr(args, "voice", False):
        try:
            from ._voice import VoiceProcessor
            input_fn = VoiceProcessor(
                lang=args.lang,
                model_size=getattr(args, "voice_model", None),
            )
        except ImportError as exc:
            print(
                f"{_c.RED}{_c.BOLD}ERROR{_c.RESET} {exc}",
                file=sys.stderr,
            )
            return 1

    kwargs: dict[str, object] = {
        "lang": args.lang,
        "nl_processor": nl_processor,
    }
    if input_fn is not None:
        kwargs["input_fn"] = input_fn

    session = ChatSession(**kwargs)  # type: ignore[arg-type]
    result = session.run()
    if result and args.output:
        out_path = Path(args.output)
        try:
            out_path.write_text(result.generated_code, encoding="utf-8")
            print(
                f"{_c.GREEN}{_c.BOLD}OK{_c.RESET} "
                f"Saved generated code to {out_path}"
            )
        except (PermissionError, OSError) as exc:
            print(f"{_c.RED}{_c.BOLD}ERROR{_c.RESET} {exc}", file=sys.stderr)
            return 1
    return 0


def _cmd_demo(args: argparse.Namespace) -> int:
    """Handle ``lu demo``: run a scripted La Nonna demo autonomously."""
    import time
    from ._intent_bridge import ChatSession

    lang = args.lang
    speed = getattr(args, "speed", "normal")
    delay_map = {"slow": 0.06, "normal": 0.03, "fast": 0.01}
    char_delay = delay_map.get(speed, 0.03)

    # Scripted inputs for the La Nonna demo
    demo_inputs = {
        "it": [
            "GestioneRicette",
            "Cuoco, Dispensa",
            "Cuoco", "Dispensa", "1",        # asks_task
            "Dispensa", "Cuoco", "2",        # return_result
            "fatto",
            "si",                            # has choices
            "Cuoco",                         # decider
            "cucinare, aggiungere",          # branches
            "3",                             # add no_deletion
            "4",                             # add all_roles_participate
            "fatto",
            "si",                            # confirm
        ],
        "en": [
            "RecipeManager",
            "Cook, Pantry",
            "Cook", "Pantry", "1",
            "Pantry", "Cook", "2",
            "done",
            "yes",
            "Cook",
            "cook, add_recipe",
            "3",                             # no_deletion
            "4",                             # all_roles_participate
            "done",
            "yes",
        ],
        "pt": [
            "GerenciamentoReceitas",
            "Cozinheiro, Despensa",
            "Cozinheiro", "Despensa", "1",
            "Despensa", "Cozinheiro", "2",
            "pronto",
            "sim",
            "Cozinheiro",
            "cozinhar, adicionar",
            "3",
            "4",
            "pronto",
            "sim",
        ],
    }

    inputs = demo_inputs.get(lang, demo_inputs["en"])
    input_idx = 0

    def _typewrite(text: str) -> None:
        """Print text with typewriter effect."""
        for ch in text:
            sys.stdout.write(ch)
            sys.stdout.flush()
            if ch not in ("\n", " "):
                time.sleep(char_delay)
        sys.stdout.write("\n")
        sys.stdout.flush()

    def _demo_input(prompt: str) -> str:
        nonlocal input_idx
        if input_idx >= len(inputs):
            raise EOFError
        val = inputs[input_idx]
        input_idx += 1
        # Show the prompt + typed response with delay
        sys.stdout.write(prompt)
        sys.stdout.flush()
        time.sleep(0.3)
        _typewrite(val)
        time.sleep(0.5)
        return val

    def _demo_output(*args: object) -> None:
        text = " ".join(str(a) for a in args)
        for line in text.split("\n"):
            time.sleep(0.15)
            print(line)
        time.sleep(0.3)

    session = ChatSession(
        lang=lang,
        input_fn=_demo_input,
        output_fn=_demo_output,
    )
    session.run()
    return 0


def _discover_lu_files(path: str) -> list[Path]:
    """Discover .lu files from a path (file or directory).

    If path is a .lu file, return [path].
    If path is a directory, return all .lu files recursively, sorted.
    Non-.lu files and nonexistent paths return [].
    """
    p = Path(path)
    if p.is_file():
        if p.suffix != ".lu":
            return []
        return [p]
    if p.is_dir():
        # Collect without following symlinks to avoid loops
        result = []
        for f in sorted(p.rglob("*.lu")):
            if not f.is_symlink():
                result.append(f)
        return result
    # Not found -- let caller handle the error
    return []


def _cmd_lint(args: argparse.Namespace) -> int:
    """Handle ``lu lint <path>`` (file or directory)."""
    from ._lint import lint_file, LintSeverity

    ignore = frozenset(c.strip() for c in args.ignore.split(",") if c.strip()) if args.ignore else frozenset()

    files: list[Path] = []
    for p in args.path:
        found = _discover_lu_files(p)
        if not found:
            print(
                f"{_c.RED}Error: no .lu files found at: {p}{_c.RESET}",
                file=sys.stderr,
            )
            return 1
        files.extend(found)

    total_errors = 0
    total_warnings = 0
    files_with_findings = 0

    for lu_file in files:
        try:
            findings = lint_file(str(lu_file), ignore=ignore)
        except Exception as exc:
            print(
                f"{_c.RED}Error: {lu_file}: {exc}{_c.RESET}",
                file=sys.stderr,
            )
            total_errors += 1
            files_with_findings += 1
            continue

        if not findings:
            if len(files) == 1:
                print(f"{_c.GREEN}{_c.BOLD}OK{_c.RESET} {lu_file} -- no lint findings")
            continue

        files_with_findings += 1
        for f in findings:
            if f.severity == LintSeverity.ERROR:
                prefix = f"{_c.RED}{f.severity.value}{_c.RESET}"
                total_errors += 1
            else:
                prefix = f"{_c.YELLOW}{f.severity.value}{_c.RESET}"
                total_warnings += 1
            print(f"  {lu_file}:{f.line}: {prefix} {f.code} [{f.category.value}] {f.message}")

    # Summary for multi-file
    if len(files) > 1:
        if total_errors == 0 and total_warnings == 0:
            print(f"\n{_c.GREEN}{_c.BOLD}OK{_c.RESET} {len(files)} files checked, no findings")
        else:
            parts = []
            if total_errors:
                parts.append(f"{_c.RED}{total_errors} error(s){_c.RESET}")
            if total_warnings:
                parts.append(f"{_c.YELLOW}{total_warnings} warning(s){_c.RESET}")
            print(f"\n{len(files)} files checked, {files_with_findings} with findings: {', '.join(parts)}")

    return 1 if total_errors > 0 else 0


def _cmd_fmt(args: argparse.Namespace) -> int:
    """Handle ``lu fmt <path>`` (file or directory)."""
    import difflib

    from ._fmt import format_file

    files: list[Path] = []
    for p in args.path:
        found = _discover_lu_files(p)
        if not found:
            print(
                f"{_c.RED}Error: no .lu files found at: {p}{_c.RESET}",
                file=sys.stderr,
            )
            return 1
        files.extend(found)

    # --stdout only makes sense for a single file
    if args.stdout and len(files) > 1:
        print(
            f"{_c.RED}Error: --stdout only works with a single file{_c.RESET}",
            file=sys.stderr,
        )
        return 1

    would_reformat = 0
    reformatted = 0
    error_count = 0

    for lu_file in files:
        try:
            formatted, changed = format_file(str(lu_file))
        except Exception as exc:
            print(
                f"{_c.RED}Error: {lu_file}: {exc}{_c.RESET}",
                file=sys.stderr,
            )
            error_count += 1
            continue

        if args.check:
            if changed:
                print(f"{_c.YELLOW}Would reformat{_c.RESET} {lu_file}")
                would_reformat += 1
            elif len(files) == 1:
                print(f"{_c.GREEN}{_c.BOLD}OK{_c.RESET} {lu_file}")
            continue

        if args.diff:
            if not changed:
                if len(files) == 1:
                    print(f"{_c.GREEN}{_c.BOLD}OK{_c.RESET} {lu_file} -- already formatted")
                continue
            original = lu_file.read_text(encoding="utf-8")
            diff = difflib.unified_diff(
                original.splitlines(keepends=True),
                formatted.splitlines(keepends=True),
                fromfile=f"a/{lu_file}",
                tofile=f"b/{lu_file}",
            )
            sys.stdout.writelines(diff)
            would_reformat += 1
            continue

        if args.stdout:
            sys.stdout.write(formatted)
            return 0

        # Default: in-place write
        if not changed:
            if len(files) == 1:
                print(f"{_c.GREEN}{_c.BOLD}OK{_c.RESET} {lu_file} -- already formatted")
            continue

        lu_file.write_text(formatted, encoding="utf-8")
        print(f"{_c.GREEN}Formatted{_c.RESET} {lu_file}")
        reformatted += 1

    # Summary for multi-file
    if len(files) > 1:
        if args.check or args.diff:
            if would_reformat == 0 and error_count == 0:
                print(f"\n{_c.GREEN}{_c.BOLD}OK{_c.RESET} {len(files)} files checked, all formatted")
            else:
                print(f"\n{len(files)} files checked, {would_reformat} would be reformatted")
        else:
            if reformatted == 0 and error_count == 0:
                print(f"\n{_c.GREEN}{_c.BOLD}OK{_c.RESET} {len(files)} files checked, all formatted")
            elif reformatted > 0:
                print(f"\n{len(files)} files checked, {reformatted} reformatted")

    # Exit code: 1 if any files need reformatting or had errors
    if args.check or args.diff:
        return 1 if (would_reformat > 0 or error_count > 0) else 0
    return 1 if error_count > 0 else 0


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

    # lu init
    p_init = subparsers.add_parser(
        "init",
        help="Create a new LU project with scaffolding",
    )
    p_init.add_argument("name", nargs="?", default=None, help="Project name (e.g. my-protocol)")
    p_init.add_argument(
        "--minimal",
        action="store_true",
        help="Only create the .lu file (no README/test)",
    )
    p_init.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing non-empty directory",
    )
    p_init.add_argument(
        "--template",
        help="Use a stdlib template (e.g. rag_pipeline, two_buyer)",
    )
    p_init.add_argument(
        "--list-templates",
        action="store_true",
        help="List available stdlib templates and exit",
    )

    # lu repl
    subparsers.add_parser("repl", help="Start the interactive REPL")

    # lu lsp
    subparsers.add_parser(
        "lsp",
        help="Start the Language Server Protocol server (requires pygls)",
    )

    # lu chat
    p_chat = subparsers.add_parser(
        "chat",
        help="Interactive guided protocol builder",
    )
    p_chat.add_argument(
        "--lang",
        choices=["en", "it", "pt"],
        default="en",
        help="Interface language (default: en)",
    )
    p_chat.add_argument(
        "--mode",
        choices=["guided", "nl"],
        default="guided",
        help="Chat mode: guided (step-by-step) or nl (natural language, requires anthropic)",
    )
    p_chat.add_argument(
        "--voice",
        action="store_true",
        help="Use voice input via microphone (requires [voice] extra)",
    )
    p_chat.add_argument(
        "--voice-model",
        choices=["tiny", "base", "small", "medium", "turbo", "large-v3"],
        default=None,
        help="Whisper model size for voice (default: small)",
    )
    p_chat.add_argument(
        "-o", "--output",
        help="Save generated Python to file",
    )

    # lu demo
    p_demo = subparsers.add_parser(
        "demo",
        help="Run the La Nonna demo autonomously (scripted)",
    )
    p_demo.add_argument(
        "--lang",
        choices=["en", "it", "pt"],
        default="it",
        help="Demo language (default: it)",
    )
    p_demo.add_argument(
        "--speed",
        choices=["slow", "normal", "fast"],
        default="normal",
        help="Typing speed (default: normal)",
    )

    # lu lint
    p_lint = subparsers.add_parser(
        "lint", help="Check style, correctness, and best practices",
    )
    p_lint.add_argument("path", nargs="+", help="Path(s) to .lu file(s) or director(ies)")
    p_lint.add_argument(
        "--ignore",
        default="",
        help="Comma-separated rule codes to ignore (e.g. LU-W002,LU-W020)",
    )

    # lu fmt
    p_fmt = subparsers.add_parser(
        "fmt", help="Format .lu files to canonical style (zero-config)",
    )
    p_fmt.add_argument("path", nargs="+", help="Path(s) to .lu file(s) or director(ies)")
    fmt_mode = p_fmt.add_mutually_exclusive_group()
    fmt_mode.add_argument(
        "--check",
        action="store_true",
        help="Check if file is formatted; exit 1 if not (CI mode)",
    )
    fmt_mode.add_argument(
        "--diff",
        action="store_true",
        help="Show diff without writing (preview mode)",
    )
    fmt_mode.add_argument(
        "--stdout",
        action="store_true",
        help="Print formatted output to stdout instead of writing file",
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
    "init": _cmd_init,
    "repl": _cmd_repl,
    "lsp": _cmd_lsp,
    "chat": _cmd_chat,
    "demo": _cmd_demo,
    "lint": _cmd_lint,
    "fmt": _cmd_fmt,
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
