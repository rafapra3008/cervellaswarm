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


# ============================================================
# lu demo (E.5 - T1.2)
# ============================================================


class TestParserDemo:
    """Parser structure for lu demo subcommand."""

    def test_demo_subcommand_exists(self) -> None:
        parser = _build_parser()
        args = parser.parse_args(["demo"])
        assert args.command == "demo"

    def test_demo_default_lang_is_italian(self) -> None:
        parser = _build_parser()
        args = parser.parse_args(["demo"])
        assert args.lang == "it"

    def test_demo_lang_option(self) -> None:
        parser = _build_parser()
        for lang in ["en", "it", "pt"]:
            args = parser.parse_args(["demo", "--lang", lang])
            assert args.lang == lang

    def test_demo_default_speed_is_normal(self) -> None:
        parser = _build_parser()
        args = parser.parse_args(["demo"])
        assert args.speed == "normal"

    def test_demo_speed_option(self) -> None:
        parser = _build_parser()
        for speed in ["slow", "normal", "fast"]:
            args = parser.parse_args(["demo", "--speed", speed])
            assert args.speed == speed

    def test_demo_invalid_lang_rejected(self) -> None:
        parser = _build_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["demo", "--lang", "fr"])

    def test_demo_invalid_speed_rejected(self) -> None:
        parser = _build_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["demo", "--speed", "turbo"])


class TestCmdDemo:
    """lu demo -- scripted autonomous demo."""

    def test_demo_italian_returns_zero(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Demo in Italian runs to completion."""
        import time
        monkeypatch.setattr(time, "sleep", lambda _: None)
        exit_code = main(["demo", "--lang", "it", "--speed", "fast"])
        assert exit_code == 0

    def test_demo_english_returns_zero(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Demo in English runs to completion."""
        import time
        monkeypatch.setattr(time, "sleep", lambda _: None)
        exit_code = main(["demo", "--lang", "en", "--speed", "fast"])
        assert exit_code == 0

    def test_demo_portuguese_returns_zero(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Demo in Portuguese runs to completion."""
        import time
        monkeypatch.setattr(time, "sleep", lambda _: None)
        exit_code = main(["demo", "--lang", "pt", "--speed", "fast"])
        assert exit_code == 0

    def test_demo_italian_output_contains_protocol(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture,
    ) -> None:
        """Italian demo mentions GestioneRicette (the protocol name)."""
        import time
        monkeypatch.setattr(time, "sleep", lambda _: None)
        main(["demo", "--lang", "it", "--speed", "fast"])
        captured = capsys.readouterr()
        assert "GestioneRicette" in captured.out

    def test_demo_english_output_contains_protocol(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture,
    ) -> None:
        """English demo mentions RecipeManager (the protocol name)."""
        import time
        monkeypatch.setattr(time, "sleep", lambda _: None)
        main(["demo", "--lang", "en", "--speed", "fast"])
        captured = capsys.readouterr()
        assert "RecipeManager" in captured.out

    def test_demo_output_contains_roles(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture,
    ) -> None:
        """Demo output mentions the agent roles."""
        import time
        monkeypatch.setattr(time, "sleep", lambda _: None)
        main(["demo", "--lang", "it", "--speed", "fast"])
        captured = capsys.readouterr()
        assert "Cuoco" in captured.out
        assert "Dispensa" in captured.out

    def test_demo_portuguese_output_contains_protocol(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture,
    ) -> None:
        """Portuguese demo mentions GerenciamentoReceitas (the protocol name)."""
        import time
        monkeypatch.setattr(time, "sleep", lambda _: None)
        main(["demo", "--lang", "pt", "--speed", "fast"])
        captured = capsys.readouterr()
        assert "GerenciamentoReceitas" in captured.out

    def test_demo_truncated_inputs_graceful(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Demo handles EOFError gracefully if inputs run out early."""
        import time
        monkeypatch.setattr(time, "sleep", lambda _: None)
        # Should not crash -- ChatSession catches EOFError
        exit_code = main(["demo", "--lang", "it", "--speed", "fast"])
        assert exit_code == 0

    def test_demo_pipeline_generates_code(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture,
    ) -> None:
        """Demo runs the full pipeline and produces generated Python code."""
        import time
        monkeypatch.setattr(time, "sleep", lambda _: None)
        main(["demo", "--lang", "en", "--speed", "fast"])
        captured = capsys.readouterr()
        # Pipeline should generate Python class with protocol name
        assert "class" in captured.out.lower() or "protocol" in captured.out.lower()

    def test_demo_handler_registered(self) -> None:
        """Demo handler is in the command dispatch table."""
        from cervellaswarm_lingua_universale._cli import _COMMAND_HANDLERS
        assert "demo" in _COMMAND_HANDLERS


# ============================================================
# lu lint / lu fmt -- multi-file support
# ============================================================

# LU source that is already in canonical format (no changes expected from fmt).
_CLEAN_SOURCE = """\
protocol Clean:
    roles: alice, bob

    alice asks bob to do task
    bob returns result to alice

    properties:
        always terminates
        no deadlock
"""

# Valid LU source that is NOT in canonical format (fmt will change it).
_MESSY_SOURCE = """\
protocol Messy:
    roles: alice, bob
    alice asks bob to do task
    bob returns result to alice
    properties:
        no deadlock
        always terminates
"""

# Valid LU source that triggers LU-W012 (self-send, severity ERROR).
_BAD_SOURCE = """\
protocol Bad:
    roles: alice, bob
    alice asks alice to do task
    bob returns result to alice
    properties:
        always terminates
"""


class TestMultiFile:
    """Multi-file support for lu lint and lu fmt (directory traversal)."""

    # ----------------------------------------------------------
    # _discover_lu_files
    # ----------------------------------------------------------

    def test_discover_single_file_returns_that_file(self, tmp_path: Path) -> None:
        """_discover_lu_files on a single .lu file returns [that file]."""
        from cervellaswarm_lingua_universale._cli import _discover_lu_files

        f = tmp_path / "proto.lu"
        f.write_text(_CLEAN_SOURCE, encoding="utf-8")

        result = _discover_lu_files(str(f))
        assert result == [f]

    def test_discover_directory_returns_all_lu_files_recursively(self, tmp_path: Path) -> None:
        """_discover_lu_files on a directory returns all .lu files, including nested."""
        from cervellaswarm_lingua_universale._cli import _discover_lu_files

        (tmp_path / "a.lu").write_text(_CLEAN_SOURCE, encoding="utf-8")
        (tmp_path / "sub").mkdir()
        (tmp_path / "sub" / "b.lu").write_text(_CLEAN_SOURCE, encoding="utf-8")
        (tmp_path / "sub" / "notes.txt").write_text("not a lu file", encoding="utf-8")

        result = _discover_lu_files(str(tmp_path))
        names = {p.name for p in result}
        assert names == {"a.lu", "b.lu"}
        assert (tmp_path / "notes.txt") not in result

    def test_discover_directory_returns_sorted_paths(self, tmp_path: Path) -> None:
        """_discover_lu_files returns paths in sorted order."""
        from cervellaswarm_lingua_universale._cli import _discover_lu_files

        (tmp_path / "z.lu").write_text(_CLEAN_SOURCE, encoding="utf-8")
        (tmp_path / "a.lu").write_text(_CLEAN_SOURCE, encoding="utf-8")
        (tmp_path / "m.lu").write_text(_CLEAN_SOURCE, encoding="utf-8")

        result = _discover_lu_files(str(tmp_path))
        assert result == sorted(result)

    def test_discover_empty_directory_returns_empty_list(self, tmp_path: Path) -> None:
        """_discover_lu_files on a directory with no .lu files returns []."""
        from cervellaswarm_lingua_universale._cli import _discover_lu_files

        result = _discover_lu_files(str(tmp_path))
        assert result == []

    def test_discover_nonexistent_path_returns_empty_list(self) -> None:
        """_discover_lu_files on a nonexistent path returns [] (no crash)."""
        from cervellaswarm_lingua_universale._cli import _discover_lu_files

        result = _discover_lu_files("/nonexistent/path/that/does/not/exist")
        assert result == []

    # ----------------------------------------------------------
    # lu lint <directory>
    # ----------------------------------------------------------

    def test_lint_directory_clean_files_exits_zero(self, tmp_path: Path) -> None:
        """lu lint <dir> with all clean files exits 0."""
        (tmp_path / "a.lu").write_text(_CLEAN_SOURCE, encoding="utf-8")
        (tmp_path / "b.lu").write_text(_CLEAN_SOURCE, encoding="utf-8")

        exit_code = main(["lint", str(tmp_path)])
        assert exit_code == 0

    def test_lint_directory_clean_files_shows_summary(
        self, tmp_path: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """lu lint <dir> with clean files shows a summary line."""
        (tmp_path / "a.lu").write_text(_CLEAN_SOURCE, encoding="utf-8")
        (tmp_path / "b.lu").write_text(_CLEAN_SOURCE, encoding="utf-8")

        main(["lint", str(tmp_path)])
        captured = capsys.readouterr()
        assert "2 files" in captured.out
        assert "OK" in captured.out

    def test_lint_directory_dirty_files_exits_one(self, tmp_path: Path) -> None:
        """lu lint <dir> with files containing errors exits 1."""
        (tmp_path / "clean.lu").write_text(_CLEAN_SOURCE, encoding="utf-8")
        (tmp_path / "bad.lu").write_text(_BAD_SOURCE, encoding="utf-8")

        exit_code = main(["lint", str(tmp_path)])
        assert exit_code == 1

    def test_lint_directory_dirty_files_shows_findings(
        self, tmp_path: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """lu lint <dir> with errors shows the finding code and file path."""
        (tmp_path / "bad.lu").write_text(_BAD_SOURCE, encoding="utf-8")
        (tmp_path / "clean.lu").write_text(_CLEAN_SOURCE, encoding="utf-8")

        main(["lint", str(tmp_path)])
        captured = capsys.readouterr()
        combined = captured.out + captured.err
        assert "LU-W012" in combined
        assert "bad.lu" in combined

    def test_lint_empty_directory_exits_one(self, tmp_path: Path) -> None:
        """lu lint <dir> with no .lu files exits 1 and reports the error."""
        exit_code = main(["lint", str(tmp_path)])
        assert exit_code == 1

    def test_lint_empty_directory_error_message(
        self, tmp_path: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """lu lint <dir> with no .lu files prints an error to stderr."""
        main(["lint", str(tmp_path)])
        captured = capsys.readouterr()
        assert "no .lu files" in captured.err.lower() or "no .lu" in captured.err

    # ----------------------------------------------------------
    # lu fmt --check <directory>
    # ----------------------------------------------------------

    def test_fmt_check_directory_all_formatted_exits_zero(self, tmp_path: Path) -> None:
        """lu fmt --check <dir> with all already-formatted files exits 0."""
        (tmp_path / "a.lu").write_text(_CLEAN_SOURCE, encoding="utf-8")
        (tmp_path / "b.lu").write_text(_CLEAN_SOURCE, encoding="utf-8")

        exit_code = main(["fmt", "--check", str(tmp_path)])
        assert exit_code == 0

    def test_fmt_check_directory_all_formatted_shows_ok(
        self, tmp_path: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """lu fmt --check <dir> all-clean shows OK summary."""
        (tmp_path / "a.lu").write_text(_CLEAN_SOURCE, encoding="utf-8")
        (tmp_path / "b.lu").write_text(_CLEAN_SOURCE, encoding="utf-8")

        main(["fmt", "--check", str(tmp_path)])
        captured = capsys.readouterr()
        assert "OK" in captured.out

    def test_fmt_check_directory_some_unformatted_exits_one(self, tmp_path: Path) -> None:
        """lu fmt --check <dir> with at least one unformatted file exits 1."""
        (tmp_path / "clean.lu").write_text(_CLEAN_SOURCE, encoding="utf-8")
        (tmp_path / "messy.lu").write_text(_MESSY_SOURCE, encoding="utf-8")

        exit_code = main(["fmt", "--check", str(tmp_path)])
        assert exit_code == 1

    def test_fmt_check_directory_unformatted_reports_file(
        self, tmp_path: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """lu fmt --check <dir> names the files that would be reformatted."""
        (tmp_path / "messy.lu").write_text(_MESSY_SOURCE, encoding="utf-8")
        (tmp_path / "clean.lu").write_text(_CLEAN_SOURCE, encoding="utf-8")

        main(["fmt", "--check", str(tmp_path)])
        captured = capsys.readouterr()
        combined = captured.out + captured.err
        assert "messy.lu" in combined

    # ----------------------------------------------------------
    # lu fmt <directory> (in-place)
    # ----------------------------------------------------------

    def test_fmt_directory_rewrites_unformatted_files(self, tmp_path: Path) -> None:
        """lu fmt <dir> rewrites unformatted files in place."""
        messy = tmp_path / "messy.lu"
        messy.write_text(_MESSY_SOURCE, encoding="utf-8")

        exit_code = main(["fmt", str(tmp_path)])
        assert exit_code == 0
        # File must have been changed (formatted != original messy source)
        assert messy.read_text(encoding="utf-8") != _MESSY_SOURCE

    def test_fmt_directory_leaves_clean_files_unchanged(self, tmp_path: Path) -> None:
        """lu fmt <dir> does not modify already-formatted files."""
        clean = tmp_path / "clean.lu"
        clean.write_text(_CLEAN_SOURCE, encoding="utf-8")
        original_mtime = clean.stat().st_mtime

        main(["fmt", str(tmp_path)])
        # Content must be identical (formatter is idempotent)
        assert clean.read_text(encoding="utf-8") == _CLEAN_SOURCE

    def test_fmt_directory_reports_reformatted_files(
        self, tmp_path: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """lu fmt <dir> prints the name of each file it reformats."""
        (tmp_path / "messy.lu").write_text(_MESSY_SOURCE, encoding="utf-8")

        main(["fmt", str(tmp_path)])
        captured = capsys.readouterr()
        combined = captured.out + captured.err
        assert "messy.lu" in combined

    def test_fmt_directory_multiple_files_reformatted_summary(
        self, tmp_path: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """lu fmt <dir> shows a summary when multiple files are processed."""
        (tmp_path / "a.lu").write_text(_MESSY_SOURCE, encoding="utf-8")
        (tmp_path / "b.lu").write_text(_MESSY_SOURCE, encoding="utf-8")
        (tmp_path / "c.lu").write_text(_CLEAN_SOURCE, encoding="utf-8")

        main(["fmt", str(tmp_path)])
        captured = capsys.readouterr()
        # 3 files processed -> summary line expected
        assert "3 files" in captured.out

    # ----------------------------------------------------------
    # lu fmt --stdout <directory> (error case)
    # ----------------------------------------------------------

    def test_fmt_stdout_with_multiple_files_exits_one(self, tmp_path: Path) -> None:
        """lu fmt --stdout with a directory containing multiple files exits 1."""
        (tmp_path / "a.lu").write_text(_CLEAN_SOURCE, encoding="utf-8")
        (tmp_path / "b.lu").write_text(_CLEAN_SOURCE, encoding="utf-8")

        exit_code = main(["fmt", "--stdout", str(tmp_path)])
        assert exit_code == 1

    def test_fmt_stdout_with_multiple_files_error_message(
        self, tmp_path: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """lu fmt --stdout with multiple files prints an informative error."""
        (tmp_path / "a.lu").write_text(_CLEAN_SOURCE, encoding="utf-8")
        (tmp_path / "b.lu").write_text(_CLEAN_SOURCE, encoding="utf-8")

        main(["fmt", "--stdout", str(tmp_path)])
        captured = capsys.readouterr()
        assert "single file" in captured.err.lower() or "--stdout" in captured.err

    def test_fmt_stdout_with_single_file_exits_zero(self, tmp_path: Path) -> None:
        """lu fmt --stdout with a single .lu file exits 0 and prints to stdout."""
        f = tmp_path / "clean.lu"
        f.write_text(_CLEAN_SOURCE, encoding="utf-8")

        exit_code = main(["fmt", "--stdout", str(f)])
        assert exit_code == 0

    def test_fmt_stdout_with_single_file_prints_formatted_source(
        self, tmp_path: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """lu fmt --stdout with a single file prints formatted LU source."""
        f = tmp_path / "clean.lu"
        f.write_text(_CLEAN_SOURCE, encoding="utf-8")

        main(["fmt", "--stdout", str(f)])
        captured = capsys.readouterr()
        assert "protocol" in captured.out
        assert "roles:" in captured.out
