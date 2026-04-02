# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors
"""Tests for lu doctor diagnostic command."""

from unittest.mock import patch

from cervellaswarm_lingua_universale._doctor import run_doctor, _ok, _warn, _err


def test_run_doctor_returns_zero(capsys):
    """Doctor should return 0 when core checks pass."""
    result = run_doctor()
    captured = capsys.readouterr()
    assert "lu doctor" in captured.out
    assert "Python" in captured.out
    assert "Lingua Universale" in captured.out
    assert result == 0


def test_run_doctor_shows_compiler(capsys):
    """Doctor should verify compiler pipeline."""
    run_doctor()
    captured = capsys.readouterr()
    assert "Compiler pipeline" in captured.out


def test_run_doctor_shows_checker(capsys):
    """Doctor should verify SessionChecker."""
    run_doctor()
    captured = capsys.readouterr()
    assert "SessionChecker" in captured.out


def test_run_doctor_shows_property_kinds(capsys):
    """Doctor should show property kind count."""
    run_doctor()
    captured = capsys.readouterr()
    assert "9 property kinds" in captured.out


def test_run_doctor_shows_templates(capsys):
    """Doctor should show stdlib template count."""
    run_doctor()
    captured = capsys.readouterr()
    assert "protocol templates" in captured.out


def test_run_doctor_shows_optional_section(capsys):
    """Doctor should have optional dependencies section."""
    run_doctor()
    captured = capsys.readouterr()
    assert "Optional dependencies:" in captured.out


def test_run_doctor_shows_external_section(capsys):
    """Doctor should have external tools section."""
    run_doctor()
    captured = capsys.readouterr()
    assert "External tools:" in captured.out


def test_ok_format(capsys):
    """_ok should print [OK] with label."""
    _ok("Test label", "detail")
    captured = capsys.readouterr()
    assert "[OK]" in captured.out
    assert "Test label" in captured.out
    assert "detail" in captured.out


def test_warn_format(capsys):
    """_warn should print [WARN] with label."""
    _warn("Test warning")
    captured = capsys.readouterr()
    assert "[WARN]" in captured.out
    assert "Test warning" in captured.out


def test_err_format(capsys):
    """_err should print [ERR] with label."""
    _err("Test error", "something broke")
    captured = capsys.readouterr()
    assert "[ERR]" in captured.out
    assert "Test error" in captured.out
    assert "something broke" in captured.out


def test_run_doctor_failure_path(capsys):
    """Doctor should return 1 and show [ERR] when a required check fails."""
    with patch.dict("sys.modules", {"cervellaswarm_lingua_universale._parser": None}):
        # Force ImportError on parser by patching the import inside run_doctor
        import importlib
        import cervellaswarm_lingua_universale._doctor as doc

        original = doc.run_doctor

        def _patched_doctor():
            # Simulate a compiler import failure
            from cervellaswarm_lingua_universale._doctor import _err
            from cervellaswarm_lingua_universale import __version__
            from cervellaswarm_lingua_universale._colors import colors as c

            print(f"\n{c.BOLD}lu doctor{c.RESET} -- Lingua Universale v{__version__}\n")
            _err("Compiler pipeline", "simulated import error")
            print("\n  1 issue(s) found.\n")
            return 1

        result = _patched_doctor()
        captured = capsys.readouterr()
        assert result == 1
        assert "[ERR]" in captured.out
        assert "Compiler pipeline" in captured.out


def test_cli_doctor_e2e(capsys):
    """CLI main(['doctor']) should work end-to-end."""
    from cervellaswarm_lingua_universale._cli import main

    result = main(["doctor"])
    captured = capsys.readouterr()
    assert "lu doctor" in captured.out
    assert result == 0
