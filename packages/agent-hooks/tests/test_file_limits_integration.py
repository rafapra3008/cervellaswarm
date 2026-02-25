# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_agent_hooks.file_limits - check_limits() and main()."""

import json
import os
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pytest

from cervellaswarm_agent_hooks.file_limits import check_limits, main


# ---------------------------------------------------------------------------
# check_limits
# ---------------------------------------------------------------------------


class TestCheckLimits:
    def test_no_violations_when_under_limit(self, tmp_project):
        md = tmp_project / "small.md"
        md.write_text("line1\nline2\n")

        config = {
            "checks": [
                {
                    "pattern": "*.md",
                    "name": "Markdown files",
                    "max_lines": 100,
                    "action": "Clean up",
                }
            ]
        }
        with patch("cervellaswarm_agent_hooks.file_limits.get_hook_config", return_value=config):
            violations = check_limits(str(tmp_project))
        assert violations == []

    def test_violation_when_over_line_limit(self, tmp_project):
        md = tmp_project / "big.md"
        md.write_text("\n".join(f"line{i}" for i in range(20)))

        config = {
            "checks": [
                {
                    "pattern": "*.md",
                    "name": "Markdown files",
                    "max_lines": 5,
                    "action": "Trim it",
                }
            ]
        }
        with patch("cervellaswarm_agent_hooks.file_limits.get_hook_config", return_value=config):
            violations = check_limits(str(tmp_project))
        assert len(violations) == 1
        assert violations[0]["type"] == "lines"
        assert violations[0]["current"] == 20

    def test_violation_critical_severity(self, tmp_project):
        md = tmp_project / "huge.md"
        md.write_text("\n".join(f"line{i}" for i in range(100)))

        config = {
            "checks": [
                {
                    "pattern": "*.md",
                    "name": "Markdown files",
                    "max_lines": 5,
                }
            ]
        }
        with patch("cervellaswarm_agent_hooks.file_limits.get_hook_config", return_value=config):
            violations = check_limits(str(tmp_project))
        assert violations[0]["severity"] == "CRITICAL"

    def test_violation_warning_severity(self, tmp_project):
        md = tmp_project / "medium.md"
        md.write_text("\n".join(f"line{i}" for i in range(8)))

        config = {
            "checks": [
                {
                    "pattern": "*.md",
                    "name": "Markdown files",
                    "max_lines": 5,
                }
            ]
        }
        with patch("cervellaswarm_agent_hooks.file_limits.get_hook_config", return_value=config):
            violations = check_limits(str(tmp_project))
        assert violations[0]["severity"] == "WARNING"

    def test_count_violation(self, tmp_project):
        for i in range(5):
            (tmp_project / f"report_{i}.json").write_text("{}")

        config = {
            "checks": [
                {
                    "pattern": "*.json",
                    "name": "Report files",
                    "max_count": 3,
                    "action": "Archive old reports",
                }
            ]
        }
        with patch("cervellaswarm_agent_hooks.file_limits.get_hook_config", return_value=config):
            violations = check_limits(str(tmp_project))
        count_violations = [v for v in violations if v["type"] == "count"]
        assert len(count_violations) == 1
        assert count_violations[0]["current"] == 5

    def test_empty_checks_no_violations(self, tmp_project):
        config = {"checks": []}
        with patch("cervellaswarm_agent_hooks.file_limits.get_hook_config", return_value=config):
            violations = check_limits(str(tmp_project))
        assert violations == []

    def test_no_matching_files_no_violations(self, tmp_project):
        config = {
            "checks": [
                {
                    "pattern": "*.nonexistent",
                    "name": "Fake",
                    "max_lines": 5,
                }
            ]
        }
        with patch("cervellaswarm_agent_hooks.file_limits.get_hook_config", return_value=config):
            violations = check_limits(str(tmp_project))
        assert violations == []

    def test_violation_includes_file_path(self, tmp_project):
        md = tmp_project / "myfile.md"
        md.write_text("\n".join(f"line{i}" for i in range(20)))

        config = {
            "checks": [
                {
                    "pattern": "*.md",
                    "name": "Docs",
                    "max_lines": 5,
                }
            ]
        }
        with patch("cervellaswarm_agent_hooks.file_limits.get_hook_config", return_value=config):
            violations = check_limits(str(tmp_project))
        assert "myfile.md" in violations[0]["file"]

    def test_count_critical_when_over_2x(self, tmp_project):
        for i in range(10):
            (tmp_project / f"f_{i}.json").write_text("{}")

        config = {
            "checks": [
                {
                    "pattern": "*.json",
                    "name": "JSONs",
                    "max_count": 3,
                }
            ]
        }
        with patch("cervellaswarm_agent_hooks.file_limits.get_hook_config", return_value=config):
            violations = check_limits(str(tmp_project))
        count_v = [v for v in violations if v["type"] == "count"]
        assert count_v[0]["severity"] == "CRITICAL"


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


class TestMain:
    def test_main_no_violations(self, monkeypatch, capsys, tmp_project):
        payload = {"cwd": str(tmp_project)}
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(payload)))

        with patch(
            "cervellaswarm_agent_hooks.file_limits.check_limits", return_value=[]
        ):
            result = main()

        assert result == 0
        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert "result" in output

    def test_main_with_violations_prints_to_stderr(self, monkeypatch, capsys, tmp_project):
        payload = {"cwd": str(tmp_project)}
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(payload)))

        violations = [
            {
                "file": "big.md",
                "name": "Markdown",
                "current": 500,
                "limit": 200,
                "type": "lines",
                "action": "Trim",
                "severity": "CRITICAL",
            }
        ]
        with patch(
            "cervellaswarm_agent_hooks.file_limits.check_limits", return_value=violations
        ):
            result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "CRITICAL" in captured.err
        output = json.loads(captured.out)
        assert "result" in output

    def test_main_invalid_json_still_runs(self, monkeypatch, capsys):
        monkeypatch.setattr("sys.stdin", StringIO("not json"))
        with patch(
            "cervellaswarm_agent_hooks.file_limits.check_limits", return_value=[]
        ):
            result = main()
        assert result == 0

    def test_main_never_blocks(self, monkeypatch, capsys, tmp_project):
        # Even with violations, main always returns 0
        payload = {"cwd": str(tmp_project)}
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps(payload)))

        big_violations = [
            {
                "file": f"f{i}.md",
                "name": "Docs",
                "current": 1000,
                "limit": 10,
                "type": "lines",
                "action": "Fix",
                "severity": "CRITICAL",
            }
            for i in range(5)
        ]
        with patch(
            "cervellaswarm_agent_hooks.file_limits.check_limits", return_value=big_violations
        ):
            result = main()
        assert result == 0
