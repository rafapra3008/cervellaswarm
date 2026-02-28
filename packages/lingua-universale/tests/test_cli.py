# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for _cli.py -- CLI entry point (C3.2)."""

from __future__ import annotations

import pytest
from pathlib import Path

from cervellaswarm_lingua_universale._cli import main, _build_parser


# ============================================================
# Fixtures
# ============================================================

_VALID_SOURCE = """\
type TaskStatus = Pending | Running | Done

protocol DelegateTask:
    roles: regina, worker, guardiana
    regina asks worker to do task
    worker returns result to regina
    regina asks guardiana to verify
    guardiana returns verdict to regina
"""

_INVALID_SOURCE = "protocol invalid syntax here"


@pytest.fixture
def hello_lu(tmp_path: Path) -> Path:
    f = tmp_path / "hello.lu"
    f.write_text(_VALID_SOURCE, encoding="utf-8")
    return f


@pytest.fixture
def bad_lu(tmp_path: Path) -> Path:
    f = tmp_path / "bad.lu"
    f.write_text(_INVALID_SOURCE, encoding="utf-8")
    return f


# ============================================================
# Parser structure
# ============================================================


class TestParserStructure:
    """Verify argparse parser has all expected subcommands."""

    def test_parser_has_subcommands(self) -> None:
        parser = _build_parser()
        # Parse known commands without error
        for cmd in ["check", "run", "verify", "compile", "version"]:
            if cmd == "version":
                args = parser.parse_args([cmd])
            else:
                args = parser.parse_args([cmd, "dummy.lu"])
            assert args.command == cmd

    def test_compile_has_output_option(self) -> None:
        parser = _build_parser()
        args = parser.parse_args(["compile", "test.lu", "-o", "out.py"])
        assert args.output == "out.py"


# ============================================================
# lu check
# ============================================================


class TestCmdCheck:
    """lu check <file>."""

    def test_check_valid_file(self, hello_lu: Path) -> None:
        exit_code = main(["check", str(hello_lu)])
        assert exit_code == 0

    def test_check_valid_output(self, hello_lu: Path, capsys: pytest.CaptureFixture) -> None:
        main(["check", str(hello_lu)])
        captured = capsys.readouterr()
        assert "OK" in captured.out
        assert "agent" in captured.out.lower() or "protocol" in captured.out.lower()

    def test_check_invalid_file(self, bad_lu: Path) -> None:
        exit_code = main(["check", str(bad_lu)])
        assert exit_code == 1

    def test_check_nonexistent(self) -> None:
        exit_code = main(["check", "/nonexistent/file.lu"])
        assert exit_code == 1


# ============================================================
# lu run
# ============================================================


class TestCmdRun:
    """lu run <file>."""

    def test_run_valid_file(self, hello_lu: Path) -> None:
        exit_code = main(["run", str(hello_lu)])
        assert exit_code == 0

    def test_run_valid_output(self, hello_lu: Path, capsys: pytest.CaptureFixture) -> None:
        main(["run", str(hello_lu)])
        captured = capsys.readouterr()
        assert "OK" in captured.out
        assert "Loaded" in captured.out

    def test_run_invalid_file(self, bad_lu: Path) -> None:
        exit_code = main(["run", str(bad_lu)])
        assert exit_code == 1

    def test_run_nonexistent(self) -> None:
        exit_code = main(["run", "/nonexistent/file.lu"])
        assert exit_code == 1


# ============================================================
# lu verify
# ============================================================


class TestCmdVerify:
    """lu verify <file>."""

    def test_verify_valid_file(self, hello_lu: Path) -> None:
        exit_code = main(["verify", str(hello_lu)])
        assert exit_code == 0

    def test_verify_invalid_file(self, bad_lu: Path) -> None:
        exit_code = main(["verify", str(bad_lu)])
        assert exit_code == 1

    def test_verify_nonexistent(self) -> None:
        exit_code = main(["verify", "/nonexistent/file.lu"])
        assert exit_code == 1


# ============================================================
# lu compile
# ============================================================


class TestCmdCompile:
    """lu compile <file>."""

    def test_compile_to_stdout(self, hello_lu: Path, capsys: pytest.CaptureFixture) -> None:
        exit_code = main(["compile", str(hello_lu)])
        assert exit_code == 0
        captured = capsys.readouterr()
        assert "Auto-generated" in captured.out
        assert "TaskStatus" in captured.out

    def test_compile_to_file(self, hello_lu: Path, tmp_path: Path) -> None:
        out_py = tmp_path / "output.py"
        exit_code = main(["compile", str(hello_lu), "-o", str(out_py)])
        assert exit_code == 0
        assert out_py.exists()
        content = out_py.read_text()
        assert "Auto-generated" in content

    def test_compile_to_bad_path(self, hello_lu: Path) -> None:
        exit_code = main(["compile", str(hello_lu), "-o", "/nonexistent/dir/out.py"])
        assert exit_code == 1

    def test_compile_invalid(self, bad_lu: Path) -> None:
        exit_code = main(["compile", str(bad_lu)])
        assert exit_code == 1


# ============================================================
# lu version
# ============================================================


class TestCmdVersion:
    """lu version."""

    def test_version_output(self, capsys: pytest.CaptureFixture) -> None:
        exit_code = main(["version"])
        assert exit_code == 0
        captured = capsys.readouterr()
        assert "Lingua Universale" in captured.out

    def test_version_mentions_ai(self, capsys: pytest.CaptureFixture) -> None:
        exit_code = main(["version"])
        captured = capsys.readouterr()
        assert "AI" in captured.out


# ============================================================
# No command / help
# ============================================================


class TestNoCommand:
    """Running with no arguments shows help."""

    def test_no_args(self) -> None:
        exit_code = main([])
        assert exit_code == 0

    def test_unknown_command(self) -> None:
        # argparse will error on unknown subcommand
        with pytest.raises(SystemExit):
            main(["unknown_command"])


# ============================================================
# NO_COLOR / FORCE_COLOR (C3.6 -- shared _colors module)
# ============================================================


class TestCLIColors:
    """CLI respects NO_COLOR/FORCE_COLOR via shared _colors module."""

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
        assert colors.GREEN == ""

    def test_force_color_enables(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("FORCE_COLOR", "1")
        monkeypatch.delenv("NO_COLOR", raising=False)
        from cervellaswarm_lingua_universale._colors import colors, init_colors, reset_colors
        reset_colors()
        init_colors()
        assert colors.RESET == "\033[0m"
        assert colors.RED == "\033[31m"
        assert colors.GREEN == "\033[32m"

    def test_clicolor_force_enables(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("CLICOLOR_FORCE", "1")
        monkeypatch.delenv("NO_COLOR", raising=False)
        monkeypatch.delenv("FORCE_COLOR", raising=False)
        from cervellaswarm_lingua_universale._colors import colors, init_colors, reset_colors
        reset_colors()
        init_colors()
        assert colors.RESET == "\033[0m"

    def test_no_color_overrides_force(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("NO_COLOR", "1")
        monkeypatch.setenv("FORCE_COLOR", "1")
        from cervellaswarm_lingua_universale._colors import colors, init_colors, reset_colors
        reset_colors()
        init_colors()
        assert colors.RESET == ""

    def test_reset_colors(self) -> None:
        from cervellaswarm_lingua_universale._colors import colors, reset_colors
        colors.RESET = "\033[0m"
        reset_colors()
        assert colors.RESET == ""
