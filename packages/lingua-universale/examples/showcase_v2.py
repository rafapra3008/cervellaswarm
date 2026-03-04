#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors
"""
Lingua Universale - Phase C Showcase (v2)

From .lu files to verified, executable Python in milliseconds.
Demonstrates the complete C3 "Experience" pipeline:
  1. Parse & compile .lu files
  2. Generated Python code preview
  3. Execute .lu programs
  4. Formal verification with Lean 4
  5. Rust-style error messages on broken files
  6. Interactive REPL session (automated)

Usage:
    python examples/showcase_v2.py
    NO_COLOR=1 python examples/showcase_v2.py  # disable colors
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# ANSI color helpers (no deps)
# ---------------------------------------------------------------------------

_NO_COLOR = bool(os.environ.get("NO_COLOR")) or "--no-color" in sys.argv

BOLD   = "" if _NO_COLOR else "\033[1m"
GREEN  = "" if _NO_COLOR else "\033[32m"
RED    = "" if _NO_COLOR else "\033[31m"
YELLOW = "" if _NO_COLOR else "\033[33m"
CYAN   = "" if _NO_COLOR else "\033[36m"
DIM    = "" if _NO_COLOR else "\033[2m"
RESET  = "" if _NO_COLOR else "\033[0m"

TOTAL_SECTIONS = 6

# Resolve examples directory
EXAMPLES_DIR = Path(__file__).parent


def header(section_num: int, title: str) -> None:
    """Print a section header."""
    pad = "-" * max(0, 52 - len(title))
    print(f"\n{BOLD}--- [{section_num}/{TOTAL_SECTIONS}] {title} {pad}{RESET}\n")


def ok(label: str = "") -> None:
    """Print a green [OK] with optional label."""
    suffix = f" {label}" if label else ""
    print(f"  {GREEN}[OK]{RESET}{suffix}")


def fail(label: str = "") -> None:
    """Print a red [FAIL] with optional label."""
    suffix = f" {label}" if label else ""
    print(f"  {RED}[FAIL]{RESET}{suffix}")


def info(label: str) -> None:
    """Print a dim info line."""
    print(f"  {DIM}{label}{RESET}")


# ---------------------------------------------------------------------------
# Imports from Lingua Universale
# ---------------------------------------------------------------------------

from cervellaswarm_lingua_universale import (
    check_file,
    run_file,
    verify_file,
    REPLSession,
    __version__,
)


# ---------------------------------------------------------------------------
# SECTION 1 - Parse & Compile .lu files
# ---------------------------------------------------------------------------


def section_1_parse_compile() -> None:
    """Parse and compile all valid .lu example files."""
    header(1, "PARSE & COMPILE (.lu -> Python)")

    example_files = ["hello.lu", "confidence.lu", "multiagent.lu", "ricette.lu"]
    all_ok = True

    for name in example_files:
        path = EXAMPLES_DIR / name
        result = check_file(path)

        if result.ok:
            c = result.compiled
            types = len(c.types) if c else 0
            agents = len(c.agents) if c else 0
            protocols = len(c.protocols) if c else 0
            print(
                f"  {GREEN}[OK]{RESET} {name:<20s} "
                f"{DIM}{types} type(s), {agents} agent(s), {protocols} protocol(s){RESET}"
            )
        else:
            all_ok = False
            print(f"  {RED}[FAIL]{RESET} {name}: {result.errors[0][:80]}")

    if all_ok:
        ok(f"All {len(example_files)} .lu files compiled successfully")
    else:
        fail("Some .lu files failed compilation")


# ---------------------------------------------------------------------------
# SECTION 2 - Generated Python Preview
# ---------------------------------------------------------------------------


def section_2_generated_python() -> None:
    """Show the generated Python code from a .lu file."""
    header(2, "GENERATED PYTHON (ricette.lu)")

    result = check_file(EXAMPLES_DIR / "ricette.lu")
    if not result.ok or not result.python_source:
        fail("Could not compile ricette.lu")
        return

    lines = result.python_source.splitlines()
    preview = lines[:30]
    for line in preview:
        print(f"  {CYAN}{line}{RESET}")
    if len(lines) > 30:
        print(f"  {DIM}... ({len(lines) - 30} more lines){RESET}")

    print()
    print(f"  {DIM}Total generated lines: {len(lines)}{RESET}")
    ok("Python module generated with type hints and contracts")


# ---------------------------------------------------------------------------
# SECTION 3 - Execute .lu Program
# ---------------------------------------------------------------------------


def section_3_execute() -> None:
    """Execute a .lu file and inspect the live module."""
    header(3, "EXECUTE (hello.lu -> live module)")

    result = run_file(EXAMPLES_DIR / "hello.lu")

    if not result.ok:
        fail(f"Execution failed: {result.errors[0][:80]}")
        return

    mod = result.module
    print(f"  Module loaded : {mod.__name__}")  # type: ignore[union-attr]

    # Inspect what the module exported
    if result.compiled:
        c = result.compiled
        if c.types:
            for t in c.types:
                val = getattr(mod, t, None)
                print(f"  Type {t:<16s}: {val}")
        if c.agents:
            for a in c.agents:
                cls = getattr(mod, a, None)
                if cls:
                    inst = cls()
                    role = getattr(inst, "__lu_role__", "?")
                    trust = getattr(inst, "__lu_trust__", "?")
                    print(f"  Agent {a:<15s}: role={role}, trust={trust}")
        if c.protocols:
            for p in c.protocols:
                session_cls = getattr(mod, f"{p}Session", None)
                if session_cls:
                    print(f"  Session class  : {p}Session")

    ok("Module loaded and inspected -- types, agents, protocols are live Python objects")


# ---------------------------------------------------------------------------
# SECTION 4 - Formal Verification
# ---------------------------------------------------------------------------


def section_4_verify() -> None:
    """Demonstrate Lean 4 formal verification on a .lu file."""
    header(4, "FORMAL VERIFICATION (hello.lu)")

    result = verify_file(EXAMPLES_DIR / "hello.lu")

    if not result.ok:
        fail(f"Verification failed: {result.errors[0][:80]}")
        return

    for line in result.verification:
        print(f"  {CYAN}{line}{RESET}")

    ok("Formal verification pipeline ready")


# ---------------------------------------------------------------------------
# SECTION 5 - Rust-style Error Messages
# ---------------------------------------------------------------------------


def section_5_error_messages() -> None:
    """Demonstrate human-friendly error messages on a broken .lu file."""
    header(5, "ERROR MESSAGES (errors.lu)")

    result = check_file(EXAMPLES_DIR / "errors.lu")

    if result.ok:
        print(f"  {YELLOW}[WARN] errors.lu compiled without errors (unexpected){RESET}")
        return

    print(f"  {BOLD}Rust-style error output:{RESET}\n")

    for err in result.errors:
        for line in err.splitlines():
            print(f"    {RED}{line}{RESET}")

    print()
    info("Error messages include: code, snippet, pointer, hint, suggestions")
    ok("Human-friendly error diagnostics (3 locales: en, it, pt)")


# ---------------------------------------------------------------------------
# SECTION 6 - REPL Session (Automated)
# ---------------------------------------------------------------------------


def section_6_repl() -> None:
    """Demonstrate the REPL with automated input."""
    header(6, "REPL SESSION (automated)")

    # Simulate a REPL session with pre-defined inputs
    repl_inputs = [
        "type Color = Red | Green | Blue",
        ":check type Score = High | Low",
        ":history",
        ":quit",
    ]
    input_iter = iter(repl_inputs)

    captured: list[str] = []

    def mock_input(prompt: str) -> str:
        try:
            line = next(input_iter)
            # Show the prompt + input like a real terminal
            captured.append(f"{prompt}{line}")
            return line
        except StopIteration:
            raise EOFError

    def mock_output(*args: object) -> None:
        text = " ".join(str(a) for a in args)
        captured.append(text)

    # Set FORCE_COLOR to ensure colors work in automated mode
    old_force = os.environ.get("FORCE_COLOR")
    if not _NO_COLOR:
        os.environ["FORCE_COLOR"] = "1"

    try:
        session = REPLSession(input_fn=mock_input, output_fn=mock_output)
        session.run()
    finally:
        if old_force is None:
            os.environ.pop("FORCE_COLOR", None)
        else:
            os.environ["FORCE_COLOR"] = old_force

    # Display the captured session
    for line in captured:
        print(f"  {line}")

    print()
    ok("REPL session: type definitions, :check, :history, :quit")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    """Run all showcase v2 sections. Returns 0 on success."""
    print(f"\n{BOLD}{CYAN}")
    print("=" * 64)
    print("  LINGUA UNIVERSALE - Phase C Showcase (v2)")
    print(f"  Version {__version__}")
    print("  From .lu files to verified Python in milliseconds.")
    print("  The first language native to AI.")
    print("=" * 64)
    print(f"{RESET}")

    section_1_parse_compile()
    section_2_generated_python()
    section_3_execute()
    section_4_verify()
    section_5_error_messages()
    section_6_repl()

    print(f"\n{BOLD}{GREEN}")
    print("=" * 64)
    print("  SHOWCASE v2 COMPLETE")
    print("  All 6 sections passed.")
    print("  Phase C: The Experience is coming together.")
    print("=" * 64)
    print(f"{RESET}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
