# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_agent_hooks.config."""

import os
from pathlib import Path
from unittest.mock import patch

import pytest
from cervellaswarm_agent_hooks.config import (
    DEFAULTS,
    _deep_merge,
    find_config_file,
    get_hook_config,
    load_config,
)

# ---------------------------------------------------------------------------
# find_config_file
# ---------------------------------------------------------------------------


class TestFindConfigFile:
    def test_env_variable_takes_priority(self, tmp_path, monkeypatch):
        config_file = tmp_path / "custom_hooks.yaml"
        config_file.write_text("# custom")
        monkeypatch.setenv("CERVELLA_HOOKS_CONFIG", str(config_file))
        result = find_config_file()
        assert result == config_file

    def test_env_variable_missing_file_skips(self, tmp_path, monkeypatch):
        monkeypatch.setenv("CERVELLA_HOOKS_CONFIG", str(tmp_path / "nonexistent.yaml"))
        # Should fall through to project or user config
        # We make sure project config doesn't exist either
        with patch("cervellaswarm_agent_hooks.config.Path.cwd", return_value=tmp_path):
            result = find_config_file()
        # Could return user config or None - just ensure it doesn't return the nonexistent path
        if result is not None:
            assert result.exists()

    def test_project_config_found(self, tmp_path, monkeypatch):
        monkeypatch.delenv("CERVELLA_HOOKS_CONFIG", raising=False)
        # Create .cervella/hooks.yaml and .git in tmp_path
        (tmp_path / ".git").mkdir()
        cervella_dir = tmp_path / ".cervella"
        cervella_dir.mkdir()
        config_file = cervella_dir / "hooks.yaml"
        config_file.write_text("# project config")

        with patch("cervellaswarm_agent_hooks.config.Path.cwd", return_value=tmp_path):
            result = find_config_file()

        assert result == config_file

    def test_user_config_fallback(self, tmp_path, monkeypatch):
        monkeypatch.delenv("CERVELLA_HOOKS_CONFIG", raising=False)
        user_config = tmp_path / ".claude" / "hooks.yaml"
        user_config.parent.mkdir(parents=True)
        user_config.write_text("# user config")

        # No project config exists
        project_dir = tmp_path / "project"
        project_dir.mkdir()

        with patch("cervellaswarm_agent_hooks.config.Path.cwd", return_value=project_dir):
            with patch("cervellaswarm_agent_hooks.config.Path.home", return_value=tmp_path):
                result = find_config_file()

        assert result == user_config

    def test_no_config_returns_none(self, tmp_path, monkeypatch):
        monkeypatch.delenv("CERVELLA_HOOKS_CONFIG", raising=False)
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        # No .cervella/hooks.yaml, no ~/.claude/hooks.yaml

        with patch("cervellaswarm_agent_hooks.config.Path.cwd", return_value=project_dir):
            with patch("cervellaswarm_agent_hooks.config.Path.home", return_value=tmp_path):
                result = find_config_file()

        assert result is None


# ---------------------------------------------------------------------------
# load_config
# ---------------------------------------------------------------------------


class TestLoadConfig:
    def test_no_config_file_returns_defaults(self):
        with patch(
            "cervellaswarm_agent_hooks.config.find_config_file", return_value=None
        ):
            config = load_config()
        assert config == dict(DEFAULTS)

    def test_loads_yaml_file(self, tmp_path):
        config_file = tmp_path / "hooks.yaml"
        config_file.write_text(
            """
file_limits:
  checks:
    - pattern: "*.log"
      name: "Log files"
      max_lines: 1000
""",
            encoding="utf-8",
        )
        with patch(
            "cervellaswarm_agent_hooks.config.find_config_file", return_value=config_file
        ):
            config = load_config()

        assert "file_limits" in config
        checks = config["file_limits"]["checks"]
        assert len(checks) == 1
        assert checks[0]["pattern"] == "*.log"

    def test_merges_with_defaults(self, tmp_path):
        config_file = tmp_path / "hooks.yaml"
        config_file.write_text(
            """
context_inject:
  facts_max_lines: 200
""",
            encoding="utf-8",
        )
        with patch(
            "cervellaswarm_agent_hooks.config.find_config_file", return_value=config_file
        ):
            config = load_config()

        # facts_max_lines overridden
        assert config["context_inject"]["facts_max_lines"] == 200
        # state_max_lines kept from defaults
        assert config["context_inject"]["state_max_lines"] == DEFAULTS["context_inject"]["state_max_lines"]

    def test_invalid_yaml_returns_defaults(self, tmp_path):
        config_file = tmp_path / "hooks.yaml"
        config_file.write_text("{{{invalid yaml{{", encoding="utf-8")
        with patch(
            "cervellaswarm_agent_hooks.config.find_config_file", return_value=config_file
        ):
            config = load_config()
        assert config == dict(DEFAULTS)

    def test_empty_yaml_returns_defaults(self, tmp_path):
        config_file = tmp_path / "hooks.yaml"
        config_file.write_text("", encoding="utf-8")
        with patch(
            "cervellaswarm_agent_hooks.config.find_config_file", return_value=config_file
        ):
            config = load_config()
        assert config == dict(DEFAULTS)

    def test_custom_section_added(self, tmp_path):
        config_file = tmp_path / "hooks.yaml"
        config_file.write_text(
            """
my_custom_hook:
  enabled: true
  threshold: 42
""",
            encoding="utf-8",
        )
        with patch(
            "cervellaswarm_agent_hooks.config.find_config_file", return_value=config_file
        ):
            config = load_config()

        assert "my_custom_hook" in config
        assert config["my_custom_hook"]["enabled"] is True


# ---------------------------------------------------------------------------
# get_hook_config
# ---------------------------------------------------------------------------


class TestGetHookConfig:
    def test_returns_defaults_when_no_file(self):
        with patch(
            "cervellaswarm_agent_hooks.config.find_config_file", return_value=None
        ):
            config = get_hook_config("context_inject")
        expected = DEFAULTS["context_inject"]
        assert config == expected

    def test_merges_user_overrides_with_defaults(self, tmp_path):
        config_file = tmp_path / "hooks.yaml"
        config_file.write_text(
            """
context_inject:
  facts_max_lines: 999
""",
            encoding="utf-8",
        )
        with patch(
            "cervellaswarm_agent_hooks.config.find_config_file", return_value=config_file
        ):
            config = get_hook_config("context_inject")

        assert config["facts_max_lines"] == 999
        # Other defaults still present
        assert "state_file" in config

    def test_unknown_hook_returns_empty(self):
        with patch(
            "cervellaswarm_agent_hooks.config.find_config_file", return_value=None
        ):
            config = get_hook_config("nonexistent_hook")
        assert config == {}

    def test_all_known_hooks_have_defaults(self):
        known_hooks = [
            "file_limits",
            "context_inject",
            "session_checkpoint",
            "git_reminder",
            "bash_validator",
        ]
        with patch(
            "cervellaswarm_agent_hooks.config.find_config_file", return_value=None
        ):
            for hook in known_hooks:
                config = get_hook_config(hook)
                assert isinstance(config, dict), f"Expected dict for {hook}"
                assert len(config) > 0, f"Expected non-empty defaults for {hook}"

    def test_file_limits_default_has_checks(self):
        with patch(
            "cervellaswarm_agent_hooks.config.find_config_file", return_value=None
        ):
            config = get_hook_config("file_limits")
        assert "checks" in config
        assert isinstance(config["checks"], list)
        assert len(config["checks"]) > 0

    def test_session_checkpoint_default_includes_git_status(self):
        with patch(
            "cervellaswarm_agent_hooks.config.find_config_file", return_value=None
        ):
            config = get_hook_config("session_checkpoint")
        assert config["include_git_status"] is True
        assert config["include_recent_commits"] is True

    def test_git_reminder_default_interval(self):
        with patch(
            "cervellaswarm_agent_hooks.config.find_config_file", return_value=None
        ):
            config = get_hook_config("git_reminder")
        assert config["interval_minutes"] == 30


# ---------------------------------------------------------------------------
# load_config with config_path parameter (S509 alignment)
# ---------------------------------------------------------------------------


class TestLoadConfigPath:
    def test_explicit_path(self, tmp_path):
        cfg = tmp_path / "hooks.yaml"
        cfg.write_text("git_reminder:\n  interval_minutes: 60\n", encoding="utf-8")
        config = load_config(config_path=cfg)
        assert config["git_reminder"]["interval_minutes"] == 60
        # Defaults preserved
        assert "file_limits" in config

    def test_explicit_path_invalid_yaml(self, tmp_path):
        cfg = tmp_path / "bad.yaml"
        cfg.write_text("{{{bad yaml{", encoding="utf-8")
        config = load_config(config_path=cfg)
        assert config == DEFAULTS

    def test_explicit_path_none_uses_discovery(self):
        with patch("cervellaswarm_agent_hooks.config.find_config_file", return_value=None):
            config = load_config(config_path=None)
        assert config == DEFAULTS


# ---------------------------------------------------------------------------
# _deep_merge (S509 alignment)
# ---------------------------------------------------------------------------


class TestDeepMerge:
    def test_simple_merge(self):
        result = _deep_merge({"a": 1, "b": 2}, {"b": 3, "c": 4})
        assert result == {"a": 1, "b": 3, "c": 4}

    def test_nested_merge(self):
        base = {"section": {"a": 1, "b": 2}}
        override = {"section": {"b": 3, "c": 4}}
        result = _deep_merge(base, override)
        assert result == {"section": {"a": 1, "b": 3, "c": 4}}

    def test_does_not_mutate_base(self):
        base = {"section": {"a": 1}}
        _deep_merge(base, {"section": {"b": 2}})
        assert base == {"section": {"a": 1}}

    def test_empty_override(self):
        result = _deep_merge({"a": 1}, {})
        assert result == {"a": 1}

    def test_override_non_dict_with_dict(self):
        result = _deep_merge({"key": "string"}, {"key": {"nested": True}})
        assert result == {"key": {"nested": True}}
