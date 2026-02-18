# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_agent_hooks.cli."""

import json
import sys
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pytest

from cervellaswarm_agent_hooks import __version__
from cervellaswarm_agent_hooks.cli import (
    HOOKS_INFO,
    _get_example_config,
    cmd_list,
    cmd_setup,
    cmd_version,
    main,
)


# ---------------------------------------------------------------------------
# cmd_list
# ---------------------------------------------------------------------------


class TestCmdList:
    def test_shows_version(self, capsys):
        cmd_list()
        captured = capsys.readouterr()
        assert __version__ in captured.out

    def test_shows_all_hooks(self, capsys):
        cmd_list()
        captured = capsys.readouterr()
        for hook in HOOKS_INFO:
            assert hook["name"] in captured.out

    def test_shows_commands(self, capsys):
        cmd_list()
        captured = capsys.readouterr()
        for hook in HOOKS_INFO:
            assert hook["command"] in captured.out

    def test_shows_events(self, capsys):
        cmd_list()
        captured = capsys.readouterr()
        # Check that hook events are displayed
        events = {h["event"] for h in HOOKS_INFO}
        for event in events:
            assert event in captured.out


# ---------------------------------------------------------------------------
# cmd_setup
# ---------------------------------------------------------------------------


class TestCmdSetup:
    def test_creates_config_file(self, capsys, tmp_path):
        with patch("cervellaswarm_agent_hooks.cli.Path.cwd", return_value=tmp_path):
            cmd_setup()
        config_file = tmp_path / ".cervella" / "hooks.yaml"
        assert config_file.exists()

    def test_shows_settings_json_snippet(self, capsys, tmp_path):
        with patch("cervellaswarm_agent_hooks.cli.Path.cwd", return_value=tmp_path):
            cmd_setup()
        captured = capsys.readouterr()
        # settings.json snippet contains JSON with hook events
        assert "PreToolUse" in captured.out or "SessionEnd" in captured.out

    def test_skips_creation_if_config_exists(self, capsys, tmp_path):
        cervella_dir = tmp_path / ".cervella"
        cervella_dir.mkdir()
        existing = cervella_dir / "hooks.yaml"
        existing.write_text("# my existing config")

        with patch("cervellaswarm_agent_hooks.cli.Path.cwd", return_value=tmp_path):
            cmd_setup()

        captured = capsys.readouterr()
        assert "already exists" in captured.out
        # File unchanged
        assert existing.read_text() == "# my existing config"

    def test_shows_version_in_setup(self, capsys, tmp_path):
        with patch("cervellaswarm_agent_hooks.cli.Path.cwd", return_value=tmp_path):
            cmd_setup()
        captured = capsys.readouterr()
        assert __version__ in captured.out


# ---------------------------------------------------------------------------
# cmd_version
# ---------------------------------------------------------------------------


class TestCmdVersion:
    def test_shows_version(self, capsys):
        cmd_version()
        captured = capsys.readouterr()
        assert __version__ in captured.out

    def test_output_contains_package_name(self, capsys):
        cmd_version()
        captured = capsys.readouterr()
        assert "cervellaswarm-agent-hooks" in captured.out


# ---------------------------------------------------------------------------
# _get_example_config
# ---------------------------------------------------------------------------


class TestGetExampleConfig:
    def test_returns_string(self):
        result = _get_example_config()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_contains_yaml_keys(self):
        result = _get_example_config()
        # Either from package or fallback, should contain hook sections
        assert "context_inject" in result or "file_limits" in result or "session_checkpoint" in result


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


class TestMain:
    def test_list_command(self, capsys):
        with patch("sys.argv", ["cervella-hooks", "list"]):
            result = main()
        assert result == 0
        captured = capsys.readouterr()
        assert "bash-validator" in captured.out

    def test_version_command(self, capsys):
        with patch("sys.argv", ["cervella-hooks", "version"]):
            result = main()
        assert result == 0
        captured = capsys.readouterr()
        assert __version__ in captured.out

    def test_version_flag_long(self, capsys):
        with patch("sys.argv", ["cervella-hooks", "--version"]):
            result = main()
        assert result == 0

    def test_version_flag_short(self, capsys):
        with patch("sys.argv", ["cervella-hooks", "-V"]):
            result = main()
        assert result == 0

    def test_help_command(self, capsys):
        with patch("sys.argv", ["cervella-hooks", "help"]):
            result = main()
        assert result == 0
        captured = capsys.readouterr()
        assert "Usage" in captured.out

    def test_help_flag(self, capsys):
        with patch("sys.argv", ["cervella-hooks", "--help"]):
            result = main()
        assert result == 0

    def test_no_args_shows_help(self, capsys):
        with patch("sys.argv", ["cervella-hooks"]):
            result = main()
        assert result == 0
        captured = capsys.readouterr()
        assert "Usage" in captured.out

    def test_unknown_command_returns_1(self, capsys):
        with patch("sys.argv", ["cervella-hooks", "unknown-xyz"]):
            result = main()
        assert result == 1
        captured = capsys.readouterr()
        assert "Unknown command" in captured.err

    def test_setup_command(self, capsys, tmp_path):
        with patch("sys.argv", ["cervella-hooks", "setup"]):
            with patch("cervellaswarm_agent_hooks.cli.Path.cwd", return_value=tmp_path):
                result = main()
        assert result == 0

    def test_hooks_info_has_5_hooks(self):
        assert len(HOOKS_INFO) == 5

    def test_hooks_info_required_fields(self):
        required = {"name", "command", "event", "matcher", "description", "timeout"}
        for hook in HOOKS_INFO:
            assert required.issubset(hook.keys()), f"Hook {hook.get('name')} missing fields"
