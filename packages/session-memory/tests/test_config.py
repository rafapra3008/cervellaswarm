# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_session_memory.config module."""

import copy
import pytest
from pathlib import Path

from cervellaswarm_session_memory.config import (
    DEFAULTS,
    load_config,
    get_section,
    get_memory_dir,
    find_config_file,
)


# ---------------------------------------------------------------------------
# DEFAULTS structure
# ---------------------------------------------------------------------------

def test_defaults_structure():
    """DEFAULTS contains all expected top-level keys."""
    expected_keys = {
        "memory_dir",
        "state_file",
        "compass_file",
        "max_lines",
        "warning_lines",
        "quality",
        "secrets",
        "projects",
    }
    assert set(DEFAULTS.keys()) == expected_keys


def test_defaults_weights_sum_to_one():
    """Quality weights in DEFAULTS sum exactly to 1.0."""
    weights = DEFAULTS["quality"]["weights"]
    total = sum(weights.values())
    assert abs(total - 1.0) < 1e-9


# ---------------------------------------------------------------------------
# load_config - no file
# ---------------------------------------------------------------------------

def test_load_config_no_file(monkeypatch, tmp_path):
    """Returns defaults when no config file exists."""
    monkeypatch.delenv("CERVELLASWARM_SESSION_MEMORY_CONFIG", raising=False)
    monkeypatch.chdir(tmp_path)
    # tmp_path has no .git, no .cervella/ -> no user config in ~/ assumed absent
    config = load_config()
    assert config["memory_dir"] == DEFAULTS["memory_dir"]
    assert config["max_lines"] == DEFAULTS["max_lines"]


# ---------------------------------------------------------------------------
# load_config - env var
# ---------------------------------------------------------------------------

def test_load_config_from_env(tmp_path, monkeypatch):
    """Loads config from CERVELLASWARM_SESSION_MEMORY_CONFIG env var."""
    cfg = tmp_path / "custom.yaml"
    cfg.write_text("max_lines: 999\n", encoding="utf-8")
    monkeypatch.setenv("CERVELLASWARM_SESSION_MEMORY_CONFIG", str(cfg))
    config = load_config()
    assert config["max_lines"] == 999


# ---------------------------------------------------------------------------
# load_config - project level
# ---------------------------------------------------------------------------

def test_load_config_from_project(tmp_path, monkeypatch):
    """Loads config from .cervella/session-memory.yaml in project root."""
    monkeypatch.delenv("CERVELLASWARM_SESSION_MEMORY_CONFIG", raising=False)
    (tmp_path / ".git").mkdir()
    cervella_dir = tmp_path / ".cervella"
    cervella_dir.mkdir()
    cfg = cervella_dir / "session-memory.yaml"
    cfg.write_text("max_lines: 555\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    config = load_config()
    assert config["max_lines"] == 555


# ---------------------------------------------------------------------------
# load_config - user level
# ---------------------------------------------------------------------------

def test_load_config_from_user(tmp_path, monkeypatch):
    """Loads config from ~/.claude/session-memory.yaml user level."""
    monkeypatch.delenv("CERVELLASWARM_SESSION_MEMORY_CONFIG", raising=False)
    # Use tmp_path as home to avoid touching real home
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    claude_dir = fake_home / ".claude"
    claude_dir.mkdir()
    cfg = claude_dir / "session-memory.yaml"
    cfg.write_text("max_lines: 777\n", encoding="utf-8")
    monkeypatch.setattr(Path, "home", staticmethod(lambda: fake_home))
    # CWD has no .cervella/ and no .git -> falls through to user config
    monkeypatch.chdir(tmp_path)
    config = load_config()
    assert config["max_lines"] == 777


# ---------------------------------------------------------------------------
# load_config - priority
# ---------------------------------------------------------------------------

def test_load_config_priority(tmp_path, monkeypatch):
    """Env var config wins over project-level config."""
    # Create project-level config
    (tmp_path / ".git").mkdir()
    cervella_dir = tmp_path / ".cervella"
    cervella_dir.mkdir()
    project_cfg = cervella_dir / "session-memory.yaml"
    project_cfg.write_text("max_lines: 111\n", encoding="utf-8")

    # Create env var config
    env_cfg = tmp_path / "override.yaml"
    env_cfg.write_text("max_lines: 999\n", encoding="utf-8")
    monkeypatch.setenv("CERVELLASWARM_SESSION_MEMORY_CONFIG", str(env_cfg))
    monkeypatch.chdir(tmp_path)

    config = load_config()
    assert config["max_lines"] == 999


# ---------------------------------------------------------------------------
# load_config - explicit path
# ---------------------------------------------------------------------------

def test_load_config_explicit_path(tmp_path):
    """load_config(config_path=...) uses the given path directly."""
    cfg = tmp_path / "explicit.yaml"
    cfg.write_text("max_lines: 42\n", encoding="utf-8")
    config = load_config(config_path=cfg)
    assert config["max_lines"] == 42


# ---------------------------------------------------------------------------
# load_config - invalid / empty YAML
# ---------------------------------------------------------------------------

def test_load_config_invalid_yaml(tmp_path):
    """Invalid YAML in config file falls back to defaults."""
    cfg = tmp_path / "bad.yaml"
    cfg.write_text("key: [unclosed\n", encoding="utf-8")
    config = load_config(config_path=cfg)
    assert config["max_lines"] == DEFAULTS["max_lines"]


def test_load_config_empty_yaml(tmp_path):
    """Empty YAML config file returns defaults."""
    cfg = tmp_path / "empty.yaml"
    cfg.write_text("", encoding="utf-8")
    config = load_config(config_path=cfg)
    assert config["max_lines"] == DEFAULTS["max_lines"]
    assert config["memory_dir"] == DEFAULTS["memory_dir"]


# ---------------------------------------------------------------------------
# merge_config behaviour (via load_config with explicit path)
# ---------------------------------------------------------------------------

def test_merge_config_shallow(tmp_path):
    """User config section values overwrite defaults for that section."""
    cfg = tmp_path / "merge.yaml"
    cfg.write_text("quality:\n  target_score: 9.5\n", encoding="utf-8")
    config = load_config(config_path=cfg)
    assert config["quality"]["target_score"] == 9.5
    # Other quality sub-keys inherited from defaults
    assert "weights" in config["quality"]


def test_merge_config_new_section(tmp_path):
    """User config can add sections not in DEFAULTS."""
    cfg = tmp_path / "new_section.yaml"
    cfg.write_text("custom_section:\n  key: value\n", encoding="utf-8")
    config = load_config(config_path=cfg)
    assert config.get("custom_section") == {"key": "value"}


# ---------------------------------------------------------------------------
# get_section
# ---------------------------------------------------------------------------

def test_get_section_existing():
    """get_section returns section dict merged with defaults."""
    config = {"quality": {"target_score": 9.0}}
    result = get_section("quality", config=config)
    assert result["target_score"] == 9.0
    assert "weights" in result  # from DEFAULTS


def test_get_section_missing():
    """get_section returns defaults for section not in config."""
    config = {}
    result = get_section("quality", config=config)
    assert result == DEFAULTS["quality"]


def test_get_section_with_preloaded_config():
    """get_section uses the passed config without re-loading."""
    pre_config = {"secrets": {"extra_patterns": ["my-pattern"], "skip_files": []}}
    result = get_section("secrets", config=pre_config)
    assert "my-pattern" in result["extra_patterns"]


# ---------------------------------------------------------------------------
# get_memory_dir
# ---------------------------------------------------------------------------

def test_get_memory_dir_default(tmp_path):
    """get_memory_dir returns CWD/.session-memory when no root given."""
    config = {"memory_dir": ".session-memory"}
    result = get_memory_dir(project_root=tmp_path, config=config)
    assert result == tmp_path / ".session-memory"


def test_get_memory_dir_custom_root(tmp_path):
    """get_memory_dir uses provided project_root."""
    custom_root = tmp_path / "custom"
    custom_root.mkdir()
    config = {"memory_dir": ".session-memory"}
    result = get_memory_dir(project_root=custom_root, config=config)
    assert result == custom_root / ".session-memory"


def test_get_memory_dir_custom_name(tmp_path):
    """get_memory_dir uses memory_dir from config when set."""
    config = {"memory_dir": ".my-mem"}
    result = get_memory_dir(project_root=tmp_path, config=config)
    assert result == tmp_path / ".my-mem"


# ---------------------------------------------------------------------------
# find_config_file
# ---------------------------------------------------------------------------

def test_find_config_file_none(monkeypatch, tmp_path):
    """find_config_file returns None when no config exists."""
    monkeypatch.delenv("CERVELLASWARM_SESSION_MEMORY_CONFIG", raising=False)
    (tmp_path / ".git").mkdir()  # stop walking at git root
    monkeypatch.chdir(tmp_path)
    fake_home = tmp_path / "fakehome"
    fake_home.mkdir()
    monkeypatch.setattr(Path, "home", staticmethod(lambda: fake_home))
    result = find_config_file()
    assert result is None


def test_find_config_file_env(monkeypatch, tmp_path):
    """find_config_file returns path from env var when it exists."""
    cfg = tmp_path / "env.yaml"
    cfg.write_text("max_lines: 1\n", encoding="utf-8")
    monkeypatch.setenv("CERVELLASWARM_SESSION_MEMORY_CONFIG", str(cfg))
    result = find_config_file()
    assert result == cfg


def test_find_config_file_project(monkeypatch, tmp_path):
    """find_config_file finds .cervella/session-memory.yaml in project dir."""
    monkeypatch.delenv("CERVELLASWARM_SESSION_MEMORY_CONFIG", raising=False)
    (tmp_path / ".git").mkdir()
    cervella = tmp_path / ".cervella"
    cervella.mkdir()
    cfg = cervella / "session-memory.yaml"
    cfg.write_text("max_lines: 1\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    result = find_config_file()
    assert result == cfg


# ---------------------------------------------------------------------------
# Deep copy - mutation protection
# ---------------------------------------------------------------------------

def test_deep_copy_prevents_mutation(tmp_path):
    """Mutating load_config() return value does not change DEFAULTS."""
    original_max = DEFAULTS["max_lines"]
    config = load_config(config_path=None)
    config["max_lines"] = 99999
    config["quality"]["target_score"] = 0.0
    assert DEFAULTS["max_lines"] == original_max
    assert DEFAULTS["quality"]["target_score"] == 8.0
