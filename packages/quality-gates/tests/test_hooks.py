# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_quality_gates.hooks module."""

import os
import stat

import pytest

from cervellaswarm_quality_gates.hooks import (
    HookReport,
    HookStatus,
    _check_disabled,
    _check_shebang,
    hooks_summary,
    validate_hook,
    validate_hooks,
)
from pathlib import Path


class TestHookStatus:
    """Tests for HookStatus enum."""

    def test_all_statuses_exist(self):
        assert HookStatus.OK.value == "OK"
        assert HookStatus.BROKEN.value == "BROKEN"
        assert HookStatus.DISABLED.value == "DISABLED"
        assert HookStatus.NOT_EXEC.value == "NOT_EXEC"
        assert HookStatus.MISSING.value == "MISSING"

    def test_enum_count(self):
        assert len(HookStatus) == 5


class TestHookReport:
    """Tests for HookReport dataclass."""

    def test_frozen(self):
        r = HookReport(name="test", path="/test", status=HookStatus.OK)
        with pytest.raises(AttributeError):
            r.status = HookStatus.BROKEN

    def test_is_healthy_ok(self):
        r = HookReport(name="test", path="/test", status=HookStatus.OK)
        assert r.is_healthy is True

    def test_is_healthy_broken(self):
        r = HookReport(name="test", path="/test", status=HookStatus.BROKEN)
        assert r.is_healthy is False

    def test_is_healthy_missing(self):
        r = HookReport(name="test", path="/test", status=HookStatus.MISSING)
        assert r.is_healthy is False

    def test_default_issues_empty(self):
        r = HookReport(name="test", path="/test", status=HookStatus.OK)
        assert r.issues == ()

    def test_issues_as_tuple(self):
        r = HookReport(name="test", path="/test", status=HookStatus.BROKEN, issues=("bad shebang",))
        assert r.issues == ("bad shebang",)


class TestCheckDisabled:
    """Tests for _check_disabled helper."""

    def test_underscore_prefix(self, tmp_path):
        f = tmp_path / "_disabled.py"
        f.touch()
        assert _check_disabled(f) is True

    def test_disabled_suffix(self, tmp_path):
        f = tmp_path / "hook.py.disabled"
        f.touch()
        assert _check_disabled(f) is True

    def test_normal_file(self, tmp_path):
        f = tmp_path / "session_start.py"
        f.touch()
        assert _check_disabled(f) is False

    def test_dunder_init_not_disabled(self, tmp_path):
        """P2-2 regression: __init__.py should NOT be flagged as disabled."""
        f = tmp_path / "__init__.py"
        f.touch()
        assert _check_disabled(f) is False

    def test_dunder_main_not_disabled(self, tmp_path):
        """P2-2 regression: __main__.py should NOT be flagged as disabled."""
        f = tmp_path / "__main__.py"
        f.touch()
        assert _check_disabled(f) is False

    def test_single_underscore_still_disabled(self, tmp_path):
        f = tmp_path / "_my_hook.py"
        f.touch()
        assert _check_disabled(f) is True


class TestCheckShebang:
    """Tests for _check_shebang helper."""

    def test_valid_python3_env(self, tmp_path):
        f = tmp_path / "hook.py"
        f.write_text("#!/usr/bin/env python3\npass\n")
        ok, msg = _check_shebang(f)
        assert ok is True
        assert msg == ""

    def test_valid_bash_env(self, tmp_path):
        f = tmp_path / "hook.sh"
        f.write_text("#!/usr/bin/env bash\necho hi\n")
        ok, msg = _check_shebang(f)
        assert ok is True

    def test_valid_node_env(self, tmp_path):
        f = tmp_path / "hook.js"
        f.write_text("#!/usr/bin/env node\nconsole.log('hi')\n")
        ok, msg = _check_shebang(f)
        assert ok is True

    def test_valid_bin_bash(self, tmp_path):
        f = tmp_path / "hook.sh"
        f.write_text("#!/bin/bash\necho hi\n")
        ok, msg = _check_shebang(f)
        assert ok is True

    def test_no_shebang(self, tmp_path):
        f = tmp_path / "hook.py"
        f.write_text("print('no shebang')\n")
        ok, msg = _check_shebang(f)
        assert ok is False
        assert "No shebang" in msg

    def test_unknown_shebang(self, tmp_path):
        f = tmp_path / "hook.rb"
        f.write_text("#!/usr/bin/env ruby\nputs 'hi'\n")
        ok, msg = _check_shebang(f)
        assert ok is False
        assert "Unknown shebang" in msg

    def test_empty_file(self, tmp_path):
        f = tmp_path / "empty.py"
        f.write_text("")
        ok, msg = _check_shebang(f)
        assert ok is False
        assert "empty" in msg.lower()


class TestValidateHook:
    """Tests for validate_hook."""

    def test_valid_hook(self, valid_hook):
        report = validate_hook(valid_hook)
        assert report.status == HookStatus.OK
        assert report.is_healthy is True
        assert report.name == "session_start.py"

    def test_broken_hook(self, broken_hook):
        report = validate_hook(broken_hook)
        assert report.status == HookStatus.BROKEN
        assert len(report.issues) > 0

    def test_not_executable_hook(self, not_exec_hook):
        report = validate_hook(not_exec_hook)
        assert report.status == HookStatus.NOT_EXEC

    def test_disabled_hook(self, disabled_hook):
        report = validate_hook(disabled_hook)
        assert report.status == HookStatus.DISABLED

    def test_missing_hook(self, tmp_path):
        report = validate_hook(tmp_path / "nonexistent.py")
        assert report.status == HookStatus.MISSING

    def test_empty_executable_file(self, tmp_path):
        f = tmp_path / "empty_hook.py"
        f.write_text("")
        f.chmod(f.stat().st_mode | stat.S_IXUSR)
        report = validate_hook(f)
        assert report.status == HookStatus.BROKEN
        assert any("empty" in i.lower() for i in report.issues)

    def test_disabled_suffix_hook(self, tmp_path):
        f = tmp_path / "my_hook.py.disabled"
        f.write_text("#!/usr/bin/env python3\n")
        f.chmod(f.stat().st_mode | stat.S_IXUSR)
        report = validate_hook(f)
        assert report.status == HookStatus.DISABLED

    def test_valid_sh_hook(self, tmp_path):
        f = tmp_path / "deploy.sh"
        f.write_text("#!/bin/sh\necho deploy\n")
        f.chmod(f.stat().st_mode | stat.S_IXUSR)
        report = validate_hook(f)
        assert report.status == HookStatus.OK


class TestValidateHooks:
    """Tests for validate_hooks (directory-level)."""

    def test_empty_directory(self, tmp_hooks_dir):
        reports = validate_hooks(tmp_hooks_dir)
        assert reports == []

    def test_nonexistent_directory(self, tmp_path):
        reports = validate_hooks(tmp_path / "nonexistent")
        assert reports == []

    def test_nonexistent_dir_with_required(self, tmp_path):
        reports = validate_hooks(tmp_path / "nonexistent", required_hooks=["startup"])
        assert len(reports) == 1
        assert reports[0].status == HookStatus.MISSING
        assert reports[0].name == "startup"

    def test_directory_with_mixed_hooks(self, valid_hook, broken_hook, not_exec_hook, tmp_hooks_dir):
        reports = validate_hooks(tmp_hooks_dir)
        statuses = {r.name: r.status for r in reports}
        assert statuses["session_start.py"] == HookStatus.OK
        assert statuses["broken_hook.py"] == HookStatus.BROKEN
        assert statuses["no_exec.py"] == HookStatus.NOT_EXEC

    def test_required_hooks_missing(self, valid_hook, tmp_hooks_dir):
        reports = validate_hooks(tmp_hooks_dir, required_hooks=["session_start.py", "file_limits.py"])
        names = {r.name for r in reports}
        assert "file_limits.py" in names
        missing = [r for r in reports if r.name == "file_limits.py"]
        assert missing[0].status == HookStatus.MISSING

    def test_required_hook_already_exists(self, valid_hook, tmp_hooks_dir):
        reports = validate_hooks(tmp_hooks_dir, required_hooks=["session_start.py"])
        session_reports = [r for r in reports if r.name == "session_start.py"]
        assert len(session_reports) == 1  # no duplicate
        assert session_reports[0].status == HookStatus.OK

    def test_reports_sorted_by_name(self, tmp_hooks_dir):
        for name in ["z_hook.py", "a_hook.py", "m_hook.py"]:
            f = tmp_hooks_dir / name
            f.write_text("#!/usr/bin/env python3\n")
            f.chmod(f.stat().st_mode | stat.S_IXUSR)
        reports = validate_hooks(tmp_hooks_dir)
        file_reports = [r for r in reports if not r.name.startswith("_")]
        names = [r.name for r in file_reports]
        assert names == sorted(names)


class TestHooksSummary:
    """Tests for hooks_summary."""

    def test_empty_reports(self):
        assert hooks_summary([]) == {}

    def test_all_ok(self):
        reports = [
            HookReport(name="a", path="/a", status=HookStatus.OK),
            HookReport(name="b", path="/b", status=HookStatus.OK),
        ]
        summary = hooks_summary(reports)
        assert summary == {"OK": 2}

    def test_mixed_statuses(self):
        reports = [
            HookReport(name="a", path="/a", status=HookStatus.OK),
            HookReport(name="b", path="/b", status=HookStatus.BROKEN),
            HookReport(name="c", path="/c", status=HookStatus.MISSING),
            HookReport(name="d", path="/d", status=HookStatus.OK),
        ]
        summary = hooks_summary(reports)
        assert summary == {"OK": 2, "BROKEN": 1, "MISSING": 1}

    def test_all_broken(self):
        reports = [
            HookReport(name="a", path="/a", status=HookStatus.BROKEN, issues=("bad",)),
        ]
        summary = hooks_summary(reports)
        assert summary == {"BROKEN": 1}
