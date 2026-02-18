# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_agent_hooks.file_limits - core utilities."""

import json
import os
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pytest

from cervellaswarm_agent_hooks.file_limits import (
    count_lines,
    find_project_root,
    format_output,
)


# ---------------------------------------------------------------------------
# count_lines
# ---------------------------------------------------------------------------


class TestCountLines:
    def test_empty_file(self, tmp_path):
        f = tmp_path / "empty.md"
        f.write_text("")
        assert count_lines(f) == 0

    def test_single_line(self, tmp_path):
        f = tmp_path / "single.md"
        f.write_text("hello\n")
        assert count_lines(f) == 1

    def test_multiple_lines(self, tmp_path):
        f = tmp_path / "multi.md"
        f.write_text("line1\nline2\nline3\n")
        assert count_lines(f) == 3

    def test_no_trailing_newline(self, tmp_path):
        f = tmp_path / "no_newline.md"
        f.write_text("line1\nline2")
        assert count_lines(f) == 2

    def test_nonexistent_file_returns_zero(self, tmp_path):
        f = tmp_path / "nonexistent.md"
        assert count_lines(f) == 0

    def test_binary_file_returns_zero(self, tmp_path):
        f = tmp_path / "binary.bin"
        f.write_bytes(b"\xff\xfe\x00\x01")
        result = count_lines(f)
        assert isinstance(result, int)


# ---------------------------------------------------------------------------
# find_project_root
# ---------------------------------------------------------------------------


class TestFindProjectRoot:
    def test_finds_git_root_current(self, tmp_path):
        (tmp_path / ".git").mkdir()
        root = find_project_root(str(tmp_path))
        assert root == tmp_path

    def test_finds_git_root_parent(self, tmp_path):
        (tmp_path / ".git").mkdir()
        subdir = tmp_path / "src" / "module"
        subdir.mkdir(parents=True)
        root = find_project_root(str(subdir))
        assert root == tmp_path

    def test_no_git_returns_cwd(self, tmp_path):
        root = find_project_root(str(tmp_path))
        assert root == tmp_path


# ---------------------------------------------------------------------------
# format_output
# ---------------------------------------------------------------------------


class TestFormatOutput:
    def test_empty_violations_returns_empty_string(self):
        assert format_output([]) == ""

    def test_lines_violation_format(self):
        v = [
            {
                "file": "README.md",
                "name": "Markdown files",
                "current": 250,
                "limit": 150,
                "type": "lines",
                "action": "Archive old content",
                "severity": "WARNING",
            }
        ]
        output = format_output(v)
        assert "README.md" in output
        assert "250" in output
        assert "150" in output
        assert "WARNING" in output
        assert "Archive old content" in output
        assert "lines" in output

    def test_count_violation_format(self):
        v = [
            {
                "file": "reports/*.json",
                "name": "Reports",
                "current": 60,
                "limit": 50,
                "type": "count",
                "action": "Clean up",
                "severity": "CRITICAL",
            }
        ]
        output = format_output(v)
        assert "CRITICAL" in output
        assert "[!]" in output
        assert "files" in output

    def test_warning_uses_star_icon(self):
        v = [
            {
                "file": "notes.md",
                "name": "Notes",
                "current": 10,
                "limit": 5,
                "type": "lines",
                "action": "Trim",
                "severity": "WARNING",
            }
        ]
        output = format_output(v)
        assert "[*]" in output

    def test_multiple_violations(self):
        v = [
            {
                "file": "file1.md",
                "name": "N1",
                "current": 10,
                "limit": 5,
                "type": "lines",
                "action": "A1",
                "severity": "WARNING",
            },
            {
                "file": "file2.md",
                "name": "N2",
                "current": 20,
                "limit": 5,
                "type": "lines",
                "action": "A2",
                "severity": "CRITICAL",
            },
        ]
        output = format_output(v)
        assert "file1.md" in output
        assert "file2.md" in output

    def test_header_and_footer_present(self):
        v = [
            {
                "file": "x.md",
                "name": "X",
                "current": 10,
                "limit": 5,
                "type": "lines",
                "action": "Fix it",
                "severity": "WARNING",
            }
        ]
        output = format_output(v)
        assert "FILE LIMITS GUARD" in output
        assert "Clean up" in output
