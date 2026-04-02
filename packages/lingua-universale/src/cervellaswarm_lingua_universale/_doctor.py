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
import subprocess
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


def _check_pypi_version(current: str) -> str | None:
    """Check latest version on PyPI.  Returns None on network error."""
    try:
        import json
        from urllib.request import urlopen

        url = "https://pypi.org/pypi/cervellaswarm-lingua-universale/json"
        with urlopen(url, timeout=3) as resp:
            data = json.loads(resp.read())
            return data.get("info", {}).get("version")
    except Exception as e:
        print(f"lu doctor: PyPI version check failed: {e}", file=sys.stderr)
        return None


def _get_tool_version(cmd: str, flag: str = "--version") -> str:
    """Run a tool with --version and return the first line."""
    try:
        result = subprocess.run(
            [cmd, flag], capture_output=True, text=True, timeout=5,
        )
        return result.stdout.strip().split("\n")[0] if result.stdout else ""
    except Exception as e:
        print(f"lu doctor: {cmd} version check failed: {e}", file=sys.stderr)
        return ""


def _has_vscode_extension(extension_id: str) -> bool:
    """Check if a VS Code extension is installed."""
    try:
        result = subprocess.run(
            ["code", "--list-extensions"], capture_output=True, text=True, timeout=5,
        )
        return extension_id in result.stdout
    except Exception as e:
        print(f"lu doctor: VS Code extension check failed: {e}", file=sys.stderr)
        return False


def _check_test_suite() -> None:
    """Try to discover tests via pytest, fall back to static count."""
    # Try to find tests/ directory relative to package source
    pkg_dir = os.path.dirname(os.path.abspath(__file__))
    # Source layout: src/cervellaswarm_lingua_universale/ -> ../../tests/
    tests_dir = os.path.normpath(os.path.join(pkg_dir, "..", "..", "tests"))

    if os.path.isdir(tests_dir):
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "--co", "-q", tests_dir],
                capture_output=True, text=True, timeout=30,
            )
            if result.returncode == 0:
                # Parse test count from pytest --co -q output
                total = 0
                for line in result.stdout.strip().split("\n"):
                    line = line.strip()
                    # Format: "tests/test_foo.py: 42"
                    if ": " in line and line.split(": ")[-1].isdigit():
                        total += int(line.split(": ")[-1])
                    # Format: "N tests/no tests collected" (older pytest)
                    elif "test" in line:
                        parts = line.split()
                        if parts and parts[0].isdigit():
                            total = int(parts[0])
                            break
                if total > 0:
                    _ok("Test suite", f"{total} tests discovered")
                    return
        except Exception as e:
            print(f"lu doctor: pytest discovery failed: {e}", file=sys.stderr)

    _warn("Test suite", "pytest not available -- run `pytest` in source tree to verify")


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

    # ── LU core + version freshness ──────────────────────────────
    latest = _check_pypi_version(__version__)
    if latest and latest != __version__:
        _warn("Lingua Universale", f"v{__version__} -- update available: v{latest}")
    else:
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

    # ── Test suite ─────────────────────────────────────────────
    _check_test_suite()

    # ── Optional: anthropic (for lu chat) ───────────────────────
    print(f"\n{_c.BOLD}Optional dependencies:{_c.RESET}\n")

    try:
        import anthropic  # noqa: F401

        _ok("anthropic SDK", "lu chat available")
        if os.environ.get("ANTHROPIC_API_KEY"):
            _ok("ANTHROPIC_API_KEY", "set")
        else:
            _warn("ANTHROPIC_API_KEY", "not set -- lu chat --mode nl will not work (guided mode works fine)")
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

    lean_path = shutil.which("lean")
    if lean_path:
        lean_ver = _get_tool_version("lean", "--version")
        _ok("Lean 4", lean_ver or "installed")
    else:
        _warn("Lean 4", "not installed -- optional, for theorem proving")

    # ── VS Code + LU extension ────────────────────────────────
    if shutil.which("code"):
        if _has_vscode_extension("cervellaswarm.lingua-universale"):
            _ok("VS Code extension", "cervellaswarm.lingua-universale installed")
        else:
            _warn("VS Code extension", "not installed -- search 'Lingua Universale' in Extensions")
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
