# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_quality_gates.sync module."""

import pytest

from cervellaswarm_quality_gates.sync import (
    FileDiff,
    SyncAction,
    SyncResult,
    _file_hash,
    _list_files,
    _should_ignore,
    compare_agents,
)
from pathlib import Path


class TestSyncAction:
    """Tests for SyncAction enum."""

    def test_all_actions(self):
        assert SyncAction.COPY.value == "copy"
        assert SyncAction.UPDATE.value == "update"
        assert SyncAction.DELETE.value == "delete"
        assert SyncAction.SKIP.value == "skip"


class TestFileDiff:
    """Tests for FileDiff dataclass."""

    def test_frozen(self):
        d = FileDiff(name="a.md", source_path="/a", target_path=None, action=SyncAction.COPY, reason="test")
        with pytest.raises(AttributeError):
            d.action = SyncAction.DELETE

    def test_copy_action(self):
        d = FileDiff(name="a.md", source_path="/a", target_path=None, action=SyncAction.COPY, reason="Only in source")
        assert d.target_path is None
        assert d.action == SyncAction.COPY


class TestSyncResult:
    """Tests for SyncResult dataclass."""

    def test_is_synced_when_identical(self):
        r = SyncResult(
            source_dir="/src", target_dir="/tgt",
            only_in_source=(), only_in_target=(), different=(), identical=("a.md",),
        )
        assert r.is_synced is True

    def test_not_synced_when_only_in_source(self):
        r = SyncResult(
            source_dir="/src", target_dir="/tgt",
            only_in_source=("extra.md",), only_in_target=(), different=(), identical=(),
        )
        assert r.is_synced is False

    def test_not_synced_when_different(self):
        r = SyncResult(
            source_dir="/src", target_dir="/tgt",
            only_in_source=(), only_in_target=(), different=("changed.md",), identical=(),
        )
        assert r.is_synced is False

    def test_total_files(self):
        r = SyncResult(
            source_dir="/src", target_dir="/tgt",
            only_in_source=("a",), only_in_target=("b",), different=("c",), identical=("d", "e"),
        )
        assert r.total_files == 5

    def test_frozen(self):
        r = SyncResult(
            source_dir="/src", target_dir="/tgt",
            only_in_source=(), only_in_target=(), different=(), identical=(),
        )
        with pytest.raises(AttributeError):
            r.source_dir = "/other"


class TestFileHash:
    """Tests for _file_hash helper."""

    def test_same_content_same_hash(self, tmp_path):
        f1 = tmp_path / "a.txt"
        f2 = tmp_path / "b.txt"
        f1.write_text("hello world")
        f2.write_text("hello world")
        assert _file_hash(f1) == _file_hash(f2)

    def test_different_content_different_hash(self, tmp_path):
        f1 = tmp_path / "a.txt"
        f2 = tmp_path / "b.txt"
        f1.write_text("hello")
        f2.write_text("world")
        assert _file_hash(f1) != _file_hash(f2)

    def test_empty_file(self, tmp_path):
        f = tmp_path / "empty.txt"
        f.write_text("")
        h = _file_hash(f)
        assert isinstance(h, str)
        assert len(h) == 64  # SHA-256 hex


class TestShouldIgnore:
    """Tests for _should_ignore helper."""

    def test_pyc_ignored(self):
        assert _should_ignore("module.pyc", ["*.pyc"])

    def test_pycache_ignored(self):
        assert _should_ignore("__pycache__", ["__pycache__"])

    def test_normal_file_not_ignored(self):
        assert _should_ignore("agent.md", ["*.pyc"]) is False

    def test_ds_store_ignored(self):
        assert _should_ignore(".DS_Store", [".DS_Store"])

    def test_multiple_patterns(self):
        assert _should_ignore("test.pyc", ["*.pyc", "*.pyo", "__pycache__"])

    def test_empty_patterns(self):
        assert _should_ignore("anything.txt", []) is False


class TestListFiles:
    """Tests for _list_files helper."""

    def test_lists_files(self, agent_source):
        files = _list_files(agent_source, [])
        assert "agent_a.md" in files
        assert "agent_b.md" in files
        assert "shared.md" in files

    def test_ignores_patterns(self, agent_source):
        (agent_source / "test.pyc").write_text("")
        files = _list_files(agent_source, ["*.pyc"])
        assert "test.pyc" not in files
        assert "agent_a.md" in files

    def test_nonexistent_directory(self, tmp_path):
        files = _list_files(tmp_path / "nonexistent", [])
        assert files == {}

    def test_empty_directory(self, tmp_path):
        d = tmp_path / "empty"
        d.mkdir()
        files = _list_files(d, [])
        assert files == {}

    def test_skips_directories(self, tmp_path):
        d = tmp_path / "agents"
        d.mkdir()
        (d / "subdir").mkdir()
        (d / "file.md").write_text("content")
        files = _list_files(d, [])
        assert "file.md" in files
        assert "subdir" not in files


class TestCompareAgents:
    """Tests for compare_agents."""

    def test_identical_directories(self, tmp_path):
        src = tmp_path / "src"
        tgt = tmp_path / "tgt"
        src.mkdir()
        tgt.mkdir()
        (src / "a.md").write_text("same")
        (tgt / "a.md").write_text("same")
        result = compare_agents(src, tgt)
        assert result.is_synced is True
        assert result.identical == ("a.md",)

    def test_only_in_source(self, agent_source, agent_target):
        result = compare_agents(agent_source, agent_target)
        assert "shared.md" in result.only_in_source

    def test_only_in_target(self, agent_source, agent_target):
        result = compare_agents(agent_source, agent_target)
        assert "agent_c.md" in result.only_in_target

    def test_different_content(self, agent_source, agent_target):
        result = compare_agents(agent_source, agent_target)
        assert "agent_b.md" in result.different

    def test_identical_files(self, agent_source, agent_target):
        result = compare_agents(agent_source, agent_target)
        assert "agent_a.md" in result.identical

    def test_diffs_generated(self, agent_source, agent_target):
        result = compare_agents(agent_source, agent_target)
        assert len(result.diffs) > 0
        actions = {d.name: d.action for d in result.diffs}
        assert actions["shared.md"] == SyncAction.COPY
        assert actions["agent_b.md"] == SyncAction.UPDATE
        assert actions["agent_c.md"] == SyncAction.DELETE

    def test_custom_ignore_patterns(self, agent_source, agent_target):
        (agent_source / "temp.bak").write_text("ignore me")
        result = compare_agents(agent_source, agent_target, ignore_patterns=["*.bak"])
        all_names = (
            list(result.only_in_source)
            + list(result.only_in_target)
            + list(result.different)
            + list(result.identical)
        )
        assert "temp.bak" not in all_names

    def test_empty_source(self, tmp_path, agent_target):
        src = tmp_path / "empty_src"
        src.mkdir()
        result = compare_agents(src, agent_target)
        assert len(result.only_in_target) > 0
        assert len(result.only_in_source) == 0

    def test_empty_target(self, agent_source, tmp_path):
        tgt = tmp_path / "empty_tgt"
        tgt.mkdir()
        result = compare_agents(agent_source, tgt)
        assert len(result.only_in_source) > 0
        assert len(result.only_in_target) == 0

    def test_both_empty(self, tmp_path):
        src = tmp_path / "src"
        tgt = tmp_path / "tgt"
        src.mkdir()
        tgt.mkdir()
        result = compare_agents(src, tgt)
        assert result.is_synced is True
        assert result.total_files == 0

    def test_nonexistent_source(self, tmp_path):
        tgt = tmp_path / "tgt"
        tgt.mkdir()
        (tgt / "a.md").write_text("content")
        result = compare_agents(tmp_path / "nonexistent", tgt)
        assert "a.md" in result.only_in_target

    def test_result_paths_are_strings(self, agent_source, agent_target):
        result = compare_agents(agent_source, agent_target)
        assert isinstance(result.source_dir, str)
        assert isinstance(result.target_dir, str)
