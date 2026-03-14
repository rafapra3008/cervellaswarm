# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""lu doctor -- environment diagnostics.

Checks Python version, LU installation, optional dependencies,
and external tools.  Inspired by flutter doctor / homebrew doctor.
"""

from __future__ import annotations

import importlib
import os
import shutil
import sys

from ._colors import colors as _c


def _ok(label: str, detail: str = "") -> None:
    suffix = f" ({detail})" if detail else ""
    print(f"  {_c.GREEN}[OK]{_c.RESET}  {label}{suffix}")


def _warn(label: str, detail: str = "") -> None:
    suffix = f" ({detail})" if detail else ""
    print(f"  {_c.YELLOW}[WARN]{_c.RESET} {label}{suffix}")


def _err(label: str, detail: str = "") -> None:
    suffix = f" ({detail})" if detail else ""
    print(f"  {_c.RED}[ERR]{_c.RESET}  {label}{suffix}")


def run_doctor() -> int:
    """Run all diagnostic checks.  Returns 0 if all required checks pass."""
    from . import __version__

    print(f"\n{_c.BOLD}lu doctor{_c.RESET} -- Lingua Universale v{__version__}\n")

    issues = 0

    # ── Python version ──────────────────────────────────────────
    py = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    if sys.version_info >= (3, 10):
        _ok("Python", py)
    else:
        _err("Python", f"{py} -- requires 3.10+")
        issues += 1

    # ── LU core ─────────────────────────────────────────────────
    _ok("Lingua Universale", f"v{__version__}")

    # ── Parser / compiler ───────────────────────────────────────
    try:
        from ._parser import parse  # noqa: F401
        from ._compiler import ASTCompiler  # noqa: F401

        _ok("Compiler pipeline", "parser + compiler")
    except ImportError as exc:
        _err("Compiler pipeline", str(exc))
        issues += 1

    # ── SessionChecker ──────────────────────────────────────────
    try:
        from .checker import SessionChecker  # noqa: F401

        _ok("SessionChecker", "runtime verification")
    except ImportError as exc:
        _err("SessionChecker", str(exc))
        issues += 1

    # ── Spec / PropertyKind ─────────────────────────────────────
    try:
        from .spec import PropertyKind

        _ok("Formal verification", f"{len(PropertyKind)} property kinds")
    except ImportError as exc:
        _err("Formal verification", str(exc))
        issues += 1

    # ── LSP ─────────────────────────────────────────────────────
    try:
        importlib.import_module("pygls")
        _ok("LSP server", "pygls available")
    except ImportError:
        _warn("LSP server", "pygls not installed -- pip install pygls")

    # ── Standard library ────────────────────────────────────────
    try:
        from ._init_project import list_templates

        templates = list_templates()
        if templates:
            _ok("Standard library", f"{len(templates)} protocol templates")
        else:
            _warn("Standard library", "no templates found in stdlib/")
    except ImportError:
        _warn("Standard library", "init_project module not found")

    # ── Optional: anthropic (for lu chat) ───────────────────────
    print(f"\n{_c.BOLD}Optional dependencies:{_c.RESET}\n")

    try:
        import anthropic  # noqa: F401

        _ok("anthropic SDK", "lu chat available")
        if os.environ.get("ANTHROPIC_API_KEY"):
            _ok("ANTHROPIC_API_KEY", "set")
        else:
            _warn("ANTHROPIC_API_KEY", "not set -- lu chat will not work")
    except ImportError:
        _warn("anthropic SDK", "not installed -- pip install cervellaswarm-lingua-universale[nl]")

    # ── Optional: faster-whisper (for lu chat --voice) ──────────
    try:
        importlib.import_module("faster_whisper")
        _ok("faster-whisper", "voice input available")
    except ImportError:
        _warn("faster-whisper", "not installed -- pip install cervellaswarm-lingua-universale[voice]")

    # ── Optional: Lean 4 ────────────────────────────────────────
    print(f"\n{_c.BOLD}External tools:{_c.RESET}\n")

    if shutil.which("lean"):
        _ok("Lean 4", "formal proofs available")
    else:
        _warn("Lean 4", "not installed -- optional, for theorem proving")

    # ── VS Code extension ───────────────────────────────────────
    if shutil.which("code"):
        _ok("VS Code", "detected")
    else:
        _warn("VS Code", "not detected")

    # ── Summary ─────────────────────────────────────────────────
    print()
    if issues == 0:
        print(f"  {_c.GREEN}{_c.BOLD}All checks passed.{_c.RESET} LU is ready to use.\n")
        return 0
    else:
        print(
            f"  {_c.RED}{_c.BOLD}{issues} issue(s) found.{_c.RESET} "
            f"Fix the errors above.\n"
        )
        return 1
