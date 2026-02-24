# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_event_store.config module."""

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from cervellaswarm_event_store.config import (
    DEFAULTS,
    _deep_copy_defaults,
    _merge_config,
    find_config_file,
    get_db_path,
    get_section,
    load_config,
)


class TestDefaults:
    def test_defaults_has_db_path(self):
        assert "db_path" in DEFAULTS

    def test_defaults_has_pattern_detection(self):
        assert "pattern_detection" in DEFAULTS

    def test_defaults_has_lessons(self):
        assert "lessons" in DEFAULTS

    def test_defaults_has_query(self):
        assert "query" in DEFAULTS

    def test_defaults_similarity_threshold(self):
        assert DEFAULTS["pattern_detection"]["similarity_threshold"] == 0.7

    def test_defaults_min_occurrences(self):
        assert DEFAULTS["pattern_detection"]["min_occurrences"] == 3

    def test_deep_copy_prevents_mutation(self):
        copy1 = _deep_copy_defaults()
        copy2 = _deep_copy_defaults()
        copy1["db_path"] = "changed"
        assert copy2["db_path"] == DEFAULTS["db_path"]


class TestFindConfigFile:
    def test_returns_none_when_nothing_found(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        monkeypatch.delenv("CERVELLASWARM_EVENT_STORE_CONFIG", raising=False)
        result = find_config_file()
        assert result is None

    def test_env_var_takes_priority(self, tmp_path, monkeypatch):
        cfg = tmp_path / "my_config.yaml"
        cfg.write_text("db_path: /tmp/test.db\n")
        monkeypatch.setenv("CERVELLASWARM_EVENT_STORE_CONFIG", str(cfg))
        result = find_config_file()
        assert result == cfg

    def test_env_var_nonexistent_is_ignored(self, tmp_path, monkeypatch):
        monkeypatch.setenv("CERVELLASWARM_EVENT_STORE_CONFIG", str(tmp_path / "nope.yaml"))
        monkeypatch.chdir(tmp_path)
        result = find_config_file()
        assert result is None

    def test_project_level_config_found(self, tmp_path, monkeypatch):
        monkeypatch.delenv("CERVELLASWARM_EVENT_STORE_CONFIG", raising=False)
        cervella_dir = tmp_path / ".cervella"
        cervella_dir.mkdir()
        cfg = cervella_dir / "event-store.yaml"
        cfg.write_text("db_path: .cervella/test.db\n")
        monkeypatch.chdir(tmp_path)
        result = find_config_file()
        assert result == cfg

    def test_stops_at_git_root(self, tmp_path, monkeypatch):
        monkeypatch.delenv("CERVELLASWARM_EVENT_STORE_CONFIG", raising=False)
        git_root = tmp_path / "repo"
        git_root.mkdir()
        (git_root / ".git").mkdir()
        subdir = git_root / "src" / "module"
        subdir.mkdir(parents=True)
        monkeypatch.chdir(subdir)
        result = find_config_file()
        assert result is None


class TestLoadConfig:
    def test_returns_defaults_when_no_file(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        monkeypatch.delenv("CERVELLASWARM_EVENT_STORE_CONFIG", raising=False)
        cfg = load_config()
        assert cfg["db_path"] == DEFAULTS["db_path"]

    def test_loads_explicit_file(self, tmp_path):
        cfg_file = tmp_path / "event-store.yaml"
        cfg_file.write_text("db_path: /custom/path.db\n")
        cfg = load_config(config_path=cfg_file)
        assert cfg["db_path"] == "/custom/path.db"

    def test_merges_with_defaults(self, tmp_path):
        cfg_file = tmp_path / "event-store.yaml"
        cfg_file.write_text("db_path: custom.db\n")
        cfg = load_config(config_path=cfg_file)
        # Custom key present
        assert cfg["db_path"] == "custom.db"
        # Default section still present
        assert "pattern_detection" in cfg

    def test_returns_defaults_on_invalid_yaml(self, tmp_path):
        cfg_file = tmp_path / "event-store.yaml"
        cfg_file.write_text(": invalid: yaml: [[\n")
        cfg = load_config(config_path=cfg_file)
        assert cfg["db_path"] == DEFAULTS["db_path"]

    def test_returns_defaults_on_missing_file(self, tmp_path):
        cfg = load_config(config_path=tmp_path / "nonexistent.yaml")
        assert cfg["db_path"] == DEFAULTS["db_path"]


class TestMergeConfig:
    def test_overrides_simple_key(self):
        merged = _merge_config({"db_path": "custom.db"})
        assert merged["db_path"] == "custom.db"

    def test_merges_nested_section(self):
        merged = _merge_config({"pattern_detection": {"min_occurrences": 5}})
        assert merged["pattern_detection"]["min_occurrences"] == 5
        assert merged["pattern_detection"]["similarity_threshold"] == 0.7

    def test_unknown_key_passthrough(self):
        merged = _merge_config({"custom_key": "hello"})
        assert merged["custom_key"] == "hello"

    def test_does_not_mutate_defaults(self):
        original_db = DEFAULTS["db_path"]
        _merge_config({"db_path": "mutated.db"})
        assert DEFAULTS["db_path"] == original_db


class TestGetDbPath:
    def test_returns_path_object(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        monkeypatch.delenv("CERVELLASWARM_EVENT_STORE_DB", raising=False)
        monkeypatch.delenv("CERVELLASWARM_EVENT_STORE_CONFIG", raising=False)
        p = get_db_path()
        assert isinstance(p, Path)

    def test_env_var_overrides_all(self, monkeypatch, tmp_path):
        expected = str(tmp_path / "override.db")
        monkeypatch.setenv("CERVELLASWARM_EVENT_STORE_DB", expected)
        p = get_db_path()
        assert str(p) == expected

    def test_default_is_project_local(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        monkeypatch.delenv("CERVELLASWARM_EVENT_STORE_DB", raising=False)
        monkeypatch.delenv("CERVELLASWARM_EVENT_STORE_CONFIG", raising=False)
        p = get_db_path()
        assert ".cervella" in str(p)
        assert "event-store.db" in str(p)

    def test_relative_path_resolved_to_absolute(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        monkeypatch.delenv("CERVELLASWARM_EVENT_STORE_DB", raising=False)
        cfg = {"db_path": "relative/path.db"}
        p = get_db_path(config=cfg)
        assert p.is_absolute()


class TestGetSection:
    def test_returns_section_with_defaults(self):
        section = get_section("pattern_detection")
        assert "similarity_threshold" in section
        assert "min_occurrences" in section

    def test_merges_user_section(self):
        config = {"pattern_detection": {"min_occurrences": 10}}
        section = get_section("pattern_detection", config=config)
        assert section["min_occurrences"] == 10
        assert "similarity_threshold" in section  # default preserved

    def test_unknown_section_returns_empty(self):
        section = get_section("nonexistent")
        assert section == {}
