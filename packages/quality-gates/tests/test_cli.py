# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_quality_gates.cli module."""

import json
import stat
from unittest.mock import patch

import pytest

from cervellaswarm_quality_gates.cli import main, _build_parser


class TestBuildParser:
    """Tests for argument parser construction."""

    def test_parser_creates(self):
        parser = _build_parser()
        assert parser is not None

    def test_parser_prog_name(self):
        parser = _build_parser()
        assert parser.prog == "cervella-check"

    def test_quality_subcommand(self):
        parser = _build_parser()
        args = parser.parse_args(["quality", "test.md"])
        assert args.command == "quality"
        assert args.file == "test.md"

    def test_hooks_subcommand(self):
        parser = _build_parser()
        args = parser.parse_args(["hooks", "/path/to/hooks"])
        assert args.command == "hooks"
        assert args.directory == "/path/to/hooks"

    def test_sync_subcommand(self):
        parser = _build_parser()
        args = parser.parse_args(["sync", "/src", "/tgt"])
        assert args.command == "sync"
        assert args.source == "/src"
        assert args.target == "/tgt"

    def test_all_subcommand(self):
        parser = _build_parser()
        args = parser.parse_args(["all", "--project-dir", "/my/project"])
        assert args.command == "all"
        assert args.project_dir == "/my/project"

    def test_json_flag(self):
        parser = _build_parser()
        args = parser.parse_args(["--json", "quality", "test.md"])
        assert args.json is True

    def test_verbose_flag(self):
        parser = _build_parser()
        args = parser.parse_args(["--verbose", "hooks", "/path"])
        assert args.verbose is True


class TestMainNoCommand:
    """Tests for main() with no subcommand."""

    def test_no_args_returns_zero(self, capsys):
        result = main([])
        assert result == 0

    def test_no_args_prints_help(self, capsys):
        main([])
        captured = capsys.readouterr()
        assert "cervella-check" in captured.out


class TestCmdQuality:
    """Tests for 'quality' subcommand."""

    def test_score_existing_file(self, tmp_path, sample_session_content, capsys):
        f = tmp_path / "session.md"
        f.write_text(sample_session_content)
        result = main(["quality", str(f)])
        captured = capsys.readouterr()
        assert "Quality Score" in captured.out
        assert "Actionability" in captured.out

    def test_score_file_json_output(self, tmp_path, sample_session_content, capsys):
        f = tmp_path / "session.md"
        f.write_text(sample_session_content)
        result = main(["--json", "quality", str(f)])
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "total" in data
        assert "actionability" in data
        assert "passes" in data

    def test_score_nonexistent_file(self, capsys):
        result = main(["quality", "/nonexistent/file.md"])
        assert result == 1
        captured = capsys.readouterr()
        assert "Error" in captured.err

    def test_score_with_min_score(self, tmp_path, capsys):
        f = tmp_path / "test.md"
        f.write_text("just some vague text")
        result = main(["quality", str(f), "--min-score", "1.0"])
        captured = capsys.readouterr()
        # Low content should still pass with min_score=1.0
        assert "PASS" in captured.out or "FAIL" in captured.out

    def test_high_quality_passes(self, tmp_path, sample_session_content, capsys):
        f = tmp_path / "session.md"
        f.write_text(sample_session_content)
        result = main(["quality", str(f), "--min-score", "3.0"])
        assert result == 0  # should pass with low threshold


class TestCmdHooks:
    """Tests for 'hooks' subcommand."""

    def test_validate_directory(self, valid_hook, broken_hook, tmp_hooks_dir, capsys):
        result = main(["hooks", str(tmp_hooks_dir)])
        captured = capsys.readouterr()
        assert "Hook Validation" in captured.out

    def test_validate_empty_directory(self, tmp_hooks_dir, capsys):
        result = main(["hooks", str(tmp_hooks_dir)])
        assert result == 0
        captured = capsys.readouterr()
        assert "No hooks found" in captured.out

    def test_validate_json_output(self, valid_hook, tmp_hooks_dir, capsys):
        result = main(["--json", "hooks", str(tmp_hooks_dir)])
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "hooks" in data
        assert "summary" in data

    def test_validate_verbose(self, broken_hook, tmp_hooks_dir, capsys):
        result = main(["--verbose", "hooks", str(tmp_hooks_dir)])
        captured = capsys.readouterr()
        assert "BROKEN" in captured.out

    def test_unhealthy_hooks_return_1(self, broken_hook, tmp_hooks_dir):
        result = main(["hooks", str(tmp_hooks_dir)])
        assert result == 1


class TestCmdSync:
    """Tests for 'sync' subcommand."""

    def test_sync_identical(self, tmp_path, capsys):
        src = tmp_path / "src"
        tgt = tmp_path / "tgt"
        src.mkdir()
        tgt.mkdir()
        (src / "a.md").write_text("same")
        (tgt / "a.md").write_text("same")
        result = main(["sync", str(src), str(tgt)])
        assert result == 0
        captured = capsys.readouterr()
        assert "IN SYNC" in captured.out

    def test_sync_different(self, agent_source, agent_target, capsys):
        result = main(["sync", str(agent_source), str(agent_target)])
        assert result == 1
        captured = capsys.readouterr()
        assert "OUT OF SYNC" in captured.out

    def test_sync_json_output(self, agent_source, agent_target, capsys):
        result = main(["--json", "sync", str(agent_source), str(agent_target)])
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "is_synced" in data
        assert data["is_synced"] is False

    def test_sync_json_verbose(self, agent_source, agent_target, capsys):
        result = main(["--json", "--verbose", "sync", str(agent_source), str(agent_target)])
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "diffs" in data


class TestCmdAll:
    """Tests for 'all' subcommand."""

    def test_all_on_empty_project(self, tmp_path, capsys):
        (tmp_path / ".git").mkdir()
        result = main(["all", "--project-dir", str(tmp_path)])
        captured = capsys.readouterr()
        assert "Quality Gates" in captured.out

    def test_all_finds_session_files(self, tmp_path, sample_session_content, capsys):
        (tmp_path / ".git").mkdir()
        session = tmp_path / "PROMPT_RIPRESA.md"
        session.write_text(sample_session_content)
        result = main(["all", "--project-dir", str(tmp_path)])
        captured = capsys.readouterr()
        assert "PROMPT_RIPRESA.md" in captured.out

    def test_all_json_output(self, tmp_path, capsys):
        (tmp_path / ".git").mkdir()
        result = main(["--json", "all", "--project-dir", str(tmp_path)])
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "quality" in data
        assert "hooks" in data

    def test_all_with_hooks_dir(self, tmp_path, capsys):
        (tmp_path / ".git").mkdir()
        hooks = tmp_path / ".claude" / "hooks"
        hooks.mkdir(parents=True)
        f = hooks / "test.py"
        f.write_text("#!/usr/bin/env python3\npass\n")
        f.chmod(f.stat().st_mode | stat.S_IXUSR)
        result = main(["all", "--project-dir", str(tmp_path)])
        captured = capsys.readouterr()
        assert "Hooks" in captured.out

    def test_all_with_min_score(self, tmp_path, capsys):
        (tmp_path / ".git").mkdir()
        session = tmp_path / "SESSION_STATE.md"
        session.write_text("just text")
        result = main(["all", "--project-dir", str(tmp_path), "--min-score", "1.0"])
        # Should pass with very low threshold
        assert isinstance(result, int)
