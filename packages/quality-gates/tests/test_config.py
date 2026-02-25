# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_quality_gates.config module."""

import copy
from pathlib import Path
from unittest.mock import patch

import pytest

from cervellaswarm_quality_gates.config import (
    DEFAULTS,
    _DEFAULTS_RAW,
    _deep_merge,
    _load_yaml,
    find_config_file,
    get_section,
    load_config,
)


class TestDefaults:
    """Tests for DEFAULTS structure."""

    def test_defaults_has_quality_section(self):
        assert "quality" in DEFAULTS

    def test_defaults_has_hooks_section(self):
        assert "hooks" in DEFAULTS

    def test_defaults_has_sync_section(self):
        assert "sync" in DEFAULTS

    def test_quality_weights_sum_to_one(self):
        weights = DEFAULTS["quality"]["weights"]
        total = sum(weights.values())
        assert abs(total - 1.0) < 0.001

    def test_quality_has_min_score(self):
        assert DEFAULTS["quality"]["min_score"] == 7.0

    def test_hooks_has_directory(self):
        assert "directory" in DEFAULTS["hooks"]

    def test_sync_has_ignore_patterns(self):
        patterns = DEFAULTS["sync"]["ignore_patterns"]
        assert "*.pyc" in patterns
        assert "__pycache__" in patterns

    def test_defaults_is_immutable(self):
        """P2-1 regression: DEFAULTS should be MappingProxyType."""
        with pytest.raises(TypeError):
            DEFAULTS["quality"] = "corrupted"

    def test_defaults_nested_is_immutable(self):
        """P2-1 regression: nested dicts in DEFAULTS also immutable."""
        with pytest.raises(TypeError):
            DEFAULTS["quality"]["min_score"] = 99


class TestFindConfigFile:
    """Tests for find_config_file."""

    def test_returns_none_when_no_config(self, clean_env, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        (tmp_path / ".git").mkdir()
        result = find_config_file()
        assert result is None

    def test_finds_env_var_config(self, tmp_path, monkeypatch):
        cfg = tmp_path / "custom.yaml"
        cfg.write_text("quality:\n  min_score: 8.0\n")
        monkeypatch.setenv("CERVELLASWARM_QUALITY_GATES_CONFIG", str(cfg))
        result = find_config_file()
        assert result == cfg

    def test_env_var_nonexistent_file_skipped(self, tmp_path, monkeypatch):
        monkeypatch.setenv("CERVELLASWARM_QUALITY_GATES_CONFIG", "/nonexistent.yaml")
        monkeypatch.chdir(tmp_path)
        (tmp_path / ".git").mkdir()
        result = find_config_file()
        assert result is None

    def test_finds_project_config(self, tmp_path, monkeypatch, clean_env):
        monkeypatch.chdir(tmp_path)
        (tmp_path / ".git").mkdir()
        cfg_dir = tmp_path / ".cervella"
        cfg_dir.mkdir()
        cfg = cfg_dir / "quality-gates.yaml"
        cfg.write_text("quality:\n  min_score: 9.0\n")
        result = find_config_file()
        assert result == cfg

    def test_finds_user_config(self, tmp_path, monkeypatch, clean_env):
        monkeypatch.chdir(tmp_path)
        (tmp_path / ".git").mkdir()
        user_cfg = tmp_path / ".claude" / "quality-gates.yaml"
        user_cfg.parent.mkdir(parents=True)
        user_cfg.write_text("quality:\n  min_score: 6.0\n")
        with patch("cervellaswarm_quality_gates.config.Path.home", return_value=tmp_path):
            result = find_config_file()
        assert result == user_cfg

    def test_project_config_takes_priority_over_user(self, tmp_path, monkeypatch, clean_env):
        monkeypatch.chdir(tmp_path)
        (tmp_path / ".git").mkdir()
        # Project config
        proj_cfg = tmp_path / ".cervella" / "quality-gates.yaml"
        proj_cfg.parent.mkdir()
        proj_cfg.write_text("quality:\n  min_score: 9.0\n")
        # User config
        user_cfg = tmp_path / ".claude" / "quality-gates.yaml"
        user_cfg.parent.mkdir(parents=True)
        user_cfg.write_text("quality:\n  min_score: 6.0\n")
        result = find_config_file()
        assert result == proj_cfg


class TestLoadYaml:
    """Tests for _load_yaml helper."""

    def test_load_valid_yaml(self, tmp_path):
        f = tmp_path / "test.yaml"
        f.write_text("key: value\n")
        result = _load_yaml(f)
        assert result == {"key": "value"}

    def test_load_empty_yaml(self, tmp_path):
        f = tmp_path / "empty.yaml"
        f.write_text("")
        result = _load_yaml(f)
        assert result == {}

    def test_load_nonexistent_file(self, tmp_path):
        result = _load_yaml(tmp_path / "nope.yaml")
        assert result == {}

    def test_load_yaml_without_yaml_module(self, tmp_path):
        f = tmp_path / "test.yaml"
        f.write_text("key: value\n")
        with patch("cervellaswarm_quality_gates.config._YAML_AVAILABLE", False):
            result = _load_yaml(f)
        assert result == {}

    def test_load_corrupted_yaml(self, tmp_path):
        """P3-8 regression: corrupted YAML should return {} not crash."""
        f = tmp_path / "bad.yaml"
        f.write_text("{{invalid:\n  !!broken\n  garbage: [[[")
        result = _load_yaml(f)
        assert result == {}


class TestDeepMerge:
    """Tests for _deep_merge helper."""

    def test_simple_merge(self):
        base = {"a": 1, "b": 2}
        override = {"b": 3, "c": 4}
        result = _deep_merge(base, override)
        assert result == {"a": 1, "b": 3, "c": 4}

    def test_nested_merge(self):
        base = {"section": {"a": 1, "b": 2}}
        override = {"section": {"b": 3, "c": 4}}
        result = _deep_merge(base, override)
        assert result == {"section": {"a": 1, "b": 3, "c": 4}}

    def test_does_not_mutate_base(self):
        base = {"section": {"a": 1}}
        original = copy.deepcopy(base)
        _deep_merge(base, {"section": {"b": 2}})
        assert base == original

    def test_override_non_dict_with_dict(self):
        base = {"key": "string_value"}
        override = {"key": {"nested": True}}
        result = _deep_merge(base, override)
        assert result == {"key": {"nested": True}}

    def test_empty_override(self):
        base = {"a": 1}
        result = _deep_merge(base, {})
        assert result == {"a": 1}

    def test_empty_base(self):
        result = _deep_merge({}, {"a": 1})
        assert result == {"a": 1}


class TestLoadConfig:
    """Tests for load_config."""

    def test_returns_defaults_when_no_config(self, clean_env):
        with patch("cervellaswarm_quality_gates.config.find_config_file", return_value=None):
            config = load_config()
        assert config == DEFAULTS
        # Ensure it's a copy, not the original
        config["quality"]["min_score"] = 99
        assert DEFAULTS["quality"]["min_score"] == 7.0

    def test_loads_from_explicit_path(self, tmp_path):
        cfg = tmp_path / "test.yaml"
        cfg.write_text("quality:\n  min_score: 9.0\n")
        config = load_config(cfg)
        assert config["quality"]["min_score"] == 9.0
        # Defaults preserved for keys not in file
        assert "weights" in config["quality"]

    def test_merges_user_config_with_defaults(self, tmp_path):
        cfg = tmp_path / "test.yaml"
        cfg.write_text("quality:\n  weights:\n    actionability: 0.50\n")
        config = load_config(cfg)
        assert config["quality"]["weights"]["actionability"] == 0.50
        assert config["quality"]["weights"]["specificity"] == 0.30  # default preserved

    def test_returns_defaults_for_empty_yaml(self, tmp_path):
        cfg = tmp_path / "empty.yaml"
        cfg.write_text("")
        config = load_config(cfg)
        assert config == DEFAULTS

    def test_returns_defaults_for_unreadable_file(self, tmp_path):
        with patch("cervellaswarm_quality_gates.config._load_yaml", return_value={}):
            config = load_config(tmp_path / "bad.yaml")
        assert config == DEFAULTS


class TestGetSection:
    """Tests for get_section."""

    def test_get_quality_section(self):
        config = copy.deepcopy(_DEFAULTS_RAW)
        section = get_section("quality", config)
        assert "weights" in section
        assert "min_score" in section

    def test_get_hooks_section(self):
        config = copy.deepcopy(_DEFAULTS_RAW)
        section = get_section("hooks", config)
        assert "directory" in section

    def test_get_nonexistent_section(self):
        config = copy.deepcopy(_DEFAULTS_RAW)
        section = get_section("nonexistent", config)
        assert section == {}

    def test_section_merges_with_defaults(self):
        config = copy.deepcopy(_DEFAULTS_RAW)
        config["quality"]["min_score"] = 9.5
        section = get_section("quality", config)
        assert section["min_score"] == 9.5
        assert "weights" in section  # default preserved

    def test_auto_loads_config_when_none(self, clean_env):
        with patch("cervellaswarm_quality_gates.config.load_config", return_value=copy.deepcopy(_DEFAULTS_RAW)):
            section = get_section("quality")
        assert "weights" in section
