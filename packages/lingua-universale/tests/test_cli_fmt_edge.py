# SPDX-License-Identifier: Apache-2.0
"""Edge-case tests for _cli.py -- _fmt_check_file, _fmt_diff_file,
_fmt_inplace_file, _fmt_print_summary, and _cmd_fmt integration.

S486 HARDTEST: empty .lu files, comment-only files, already-formatted files,
format_file exceptions.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from cervellaswarm_lingua_universale._cli import (
    _fmt_check_file,
    _fmt_diff_file,
    _fmt_inplace_file,
    _fmt_print_summary,
    _cmd_fmt,
)


# ---------------------------------------------------------------------------
# _fmt_check_file
# ---------------------------------------------------------------------------


class TestFmtCheckFile:
    """Edge cases for --check mode reporting."""

    def test_unchanged_single_file_prints_ok(self, capsys):
        """Single file already formatted prints OK."""
        result = _fmt_check_file(Path("test.lu"), changed=False, single=True)
        assert result is False
        out = capsys.readouterr().out
        assert "OK" in out

    def test_unchanged_multi_file_silent(self, capsys):
        """Multi-file mode: unchanged files print nothing."""
        result = _fmt_check_file(Path("test.lu"), changed=False, single=False)
        assert result is False
        out = capsys.readouterr().out
        assert out == ""

    def test_changed_reports_would_reformat(self, capsys):
        """Changed file reports 'Would reformat'."""
        result = _fmt_check_file(Path("test.lu"), changed=True, single=True)
        assert result is True
        out = capsys.readouterr().out
        assert "Would reformat" in out

    def test_changed_multi_file(self, capsys):
        """Changed file in multi-file mode also reports."""
        result = _fmt_check_file(Path("a.lu"), changed=True, single=False)
        assert result is True
        out = capsys.readouterr().out
        assert "Would reformat" in out


# ---------------------------------------------------------------------------
# _fmt_diff_file
# ---------------------------------------------------------------------------


class TestFmtDiffFile:
    """Edge cases for --diff mode."""

    def test_unchanged_single_prints_ok(self, capsys):
        """Unchanged single file prints OK message."""
        result = _fmt_diff_file(Path("test.lu"), "content", changed=False, single=True)
        assert result is False
        out = capsys.readouterr().out
        assert "already formatted" in out

    def test_unchanged_multi_silent(self, capsys):
        """Unchanged file in multi-mode prints nothing."""
        result = _fmt_diff_file(Path("test.lu"), "content", changed=False, single=False)
        assert result is False
        out = capsys.readouterr().out
        assert out == ""

    def test_changed_shows_diff(self, tmp_path, capsys):
        """Changed file outputs unified diff."""
        lu_file = tmp_path / "test.lu"
        lu_file.write_text("type X = A | B\n", encoding="utf-8")
        formatted = "type X = A | B | C\n"
        result = _fmt_diff_file(lu_file, formatted, changed=True, single=True)
        assert result is True
        out = capsys.readouterr().out
        assert "---" in out  # unified diff header
        assert "+++" in out


# ---------------------------------------------------------------------------
# _fmt_inplace_file
# ---------------------------------------------------------------------------


class TestFmtInplaceFile:
    """Edge cases for default in-place formatting mode."""

    def test_unchanged_single_prints_ok(self, capsys):
        result = _fmt_inplace_file(Path("test.lu"), "content", changed=False, single=True)
        assert result is False
        out = capsys.readouterr().out
        assert "already formatted" in out

    def test_unchanged_multi_silent(self, capsys):
        result = _fmt_inplace_file(Path("test.lu"), "content", changed=False, single=False)
        assert result is False
        out = capsys.readouterr().out
        assert out == ""

    def test_changed_writes_file(self, tmp_path, capsys):
        """Changed file is written in-place."""
        lu_file = tmp_path / "test.lu"
        lu_file.write_text("old content", encoding="utf-8")
        result = _fmt_inplace_file(lu_file, "new content", changed=True, single=True)
        assert result is True
        assert lu_file.read_text(encoding="utf-8") == "new content"
        out = capsys.readouterr().out
        assert "Formatted" in out


# ---------------------------------------------------------------------------
# _fmt_print_summary
# ---------------------------------------------------------------------------


class TestFmtPrintSummary:
    """Edge cases for multi-file summary."""

    def test_single_file_no_output(self, capsys):
        """Single file never prints summary."""
        _fmt_print_summary(1, 0, 0, 0, False)
        out = capsys.readouterr().out
        assert out == ""

    def test_multi_all_clean_check_mode(self, capsys):
        """All files clean in --check mode."""
        _fmt_print_summary(5, 0, 0, 0, True)
        out = capsys.readouterr().out
        assert "5 files checked" in out
        assert "all formatted" in out

    def test_multi_some_would_reformat(self, capsys):
        _fmt_print_summary(5, 2, 0, 0, True)
        out = capsys.readouterr().out
        assert "2 would be reformatted" in out

    def test_multi_all_clean_inplace_mode(self, capsys):
        _fmt_print_summary(3, 0, 0, 0, False)
        out = capsys.readouterr().out
        assert "3 files checked" in out
        assert "all formatted" in out

    def test_multi_some_reformatted(self, capsys):
        _fmt_print_summary(4, 0, 2, 0, False)
        out = capsys.readouterr().out
        assert "2 reformatted" in out


# ---------------------------------------------------------------------------
# _cmd_fmt integration -- real .lu files
# ---------------------------------------------------------------------------


class TestCmdFmtIntegration:
    """Integration tests for _cmd_fmt with real .lu content."""

    def _make_args(self, paths, check=False, diff=False, stdout=False):
        import argparse
        return argparse.Namespace(
            path=paths,
            check=check,
            diff=diff,
            stdout=stdout,
        )

    def test_empty_lu_file(self, tmp_path, capsys):
        """Empty .lu file should not crash the formatter."""
        lu = tmp_path / "empty.lu"
        lu.write_text("", encoding="utf-8")
        args = self._make_args([str(lu)], check=True)
        rc = _cmd_fmt(args)
        # Should not crash -- exit code 0 means already formatted
        assert rc in (0, 1)

    def test_comment_only_lu_file(self, tmp_path, capsys):
        """File with only comments should not crash."""
        lu = tmp_path / "comments.lu"
        lu.write_text("# This is a comment\n# Another comment\n", encoding="utf-8")
        args = self._make_args([str(lu)], check=True)
        rc = _cmd_fmt(args)
        assert rc in (0, 1)

    def test_check_already_formatted_single(self, tmp_path, capsys):
        """--check on single already-formatted file returns 0."""
        from cervellaswarm_lingua_universale._fmt import format_source

        lu = tmp_path / "formatted.lu"
        source = "type Result = Success | Error\n"
        formatted = format_source(source)
        lu.write_text(formatted, encoding="utf-8")
        args = self._make_args([str(lu)], check=True)
        rc = _cmd_fmt(args)
        assert rc == 0
        out = capsys.readouterr().out
        assert "OK" in out

    def test_check_already_formatted_multi(self, tmp_path, capsys):
        """--check on multiple already-formatted files returns 0."""
        from cervellaswarm_lingua_universale._fmt import format_source

        for name in ("a.lu", "b.lu"):
            lu = tmp_path / name
            source = "type Result = Success | Error\n"
            lu.write_text(format_source(source), encoding="utf-8")
        args = self._make_args([str(tmp_path)], check=True)
        rc = _cmd_fmt(args)
        assert rc == 0
        out = capsys.readouterr().out
        assert "all formatted" in out

    def test_diff_already_formatted(self, tmp_path, capsys):
        """--diff on already-formatted single file shows OK message."""
        from cervellaswarm_lingua_universale._fmt import format_source

        lu = tmp_path / "ok.lu"
        source = "type Result = Success | Error\n"
        lu.write_text(format_source(source), encoding="utf-8")
        args = self._make_args([str(lu)], diff=True)
        rc = _cmd_fmt(args)
        assert rc == 0
        out = capsys.readouterr().out
        assert "already formatted" in out

    def test_format_file_exception_handled(self, tmp_path, capsys):
        """format_file raising exception is caught gracefully."""
        lu = tmp_path / "bad.lu"
        lu.write_text("this is not valid LU syntax }{}{", encoding="utf-8")
        args = self._make_args([str(lu)])
        rc = _cmd_fmt(args)
        # Should return error (1) but not crash
        assert rc == 1
        err = capsys.readouterr().err
        assert "Error" in err

    def test_nonexistent_path_returns_error(self, tmp_path, capsys):
        """Path to nonexistent file returns error."""
        args = self._make_args([str(tmp_path / "ghost.lu")])
        rc = _cmd_fmt(args)
        assert rc == 1
        err = capsys.readouterr().err
        assert "no .lu files" in err

    def test_non_lu_file_returns_error(self, tmp_path, capsys):
        """Non-.lu file returns error."""
        txt = tmp_path / "readme.txt"
        txt.write_text("not a lu file", encoding="utf-8")
        args = self._make_args([str(txt)])
        rc = _cmd_fmt(args)
        assert rc == 1
