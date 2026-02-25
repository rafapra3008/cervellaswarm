# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Tests for cervellaswarm_agent_hooks.bash_validator - patterns and primitives."""

import pytest

from cervellaswarm_agent_hooks.bash_validator import (
    check_autofix,
    check_blocked,
    check_risky,
    is_safe_rm_target,
)


# ---------------------------------------------------------------------------
# BLOCKED patterns
# ---------------------------------------------------------------------------


class TestBlocked:
    def test_rm_root(self):
        assert check_blocked("rm -rf /") is not None

    def test_rm_root_no_flags(self):
        assert check_blocked("rm /") is not None

    def test_rm_home(self):
        assert check_blocked("rm -rf ~/important") is not None

    def test_rm_dot_current(self):
        assert check_blocked("rm -rf .") is not None

    def test_rm_dot_parent(self):
        assert check_blocked("rm -rf ..") is not None

    def test_force_push_main(self):
        assert check_blocked("git push origin --force main") is not None

    def test_force_push_master(self):
        assert check_blocked("git push origin --force master") is not None

    def test_force_push_f_main(self):
        assert check_blocked("git push origin -f main") is not None

    def test_force_push_f_master(self):
        assert check_blocked("git push -f origin master") is not None

    def test_drop_table(self):
        assert check_blocked("DROP TABLE users") is not None

    def test_drop_table_case_insensitive(self):
        assert check_blocked("drop table users") is not None

    def test_drop_database(self):
        assert check_blocked("DROP DATABASE mydb") is not None

    def test_truncate_table(self):
        assert check_blocked("TRUNCATE TABLE logs") is not None

    def test_mkfs(self):
        assert check_blocked("mkfs.ext4 /dev/sda") is not None

    def test_dd_to_device(self):
        assert check_blocked("dd if=/dev/zero of=/dev/sda") is not None

    def test_fork_bomb(self):
        assert check_blocked(":(){ :|:& };:") is not None

    def test_device_overwrite(self):
        assert check_blocked("> /dev/sda") is not None

    def test_safe_command_not_blocked(self):
        assert check_blocked("ls -la") is None

    def test_git_push_feature_not_blocked(self):
        assert check_blocked("git push origin --force feature-branch") is None

    def test_empty_not_blocked(self):
        assert check_blocked("") is None

    def test_normal_rm_not_blocked(self):
        assert check_blocked("rm myfile.txt") is None


# ---------------------------------------------------------------------------
# RISKY patterns
# ---------------------------------------------------------------------------


class TestRisky:
    def test_git_reset_hard(self):
        assert check_risky("git reset --hard HEAD~1") is not None

    def test_git_clean_f(self):
        assert check_risky("git clean -f") is not None

    def test_git_clean_fd(self):
        assert check_risky("git clean -fd") is not None

    def test_git_checkout_dot(self):
        assert check_risky("git checkout .") is not None

    def test_git_restore_dot(self):
        assert check_risky("git restore .") is not None

    def test_git_branch_delete_force(self):
        assert check_risky("git branch -D old-feature") is not None

    def test_git_stash_drop(self):
        assert check_risky("git stash drop") is not None

    def test_chmod_777(self):
        assert check_risky("chmod 777 /some/path") is not None

    def test_kill_9(self):
        assert check_risky("kill -9 1234") is not None

    def test_docker_system_prune(self):
        assert check_risky("docker system prune") is not None

    def test_rm_rf_unknown(self):
        assert check_risky("rm -rf /some/random/path") is not None

    def test_safe_command_not_risky(self):
        assert check_risky("git status") is None

    def test_git_push_main_not_risky(self):
        assert check_risky("git push origin main") is None


# ---------------------------------------------------------------------------
# SAFE rm targets
# ---------------------------------------------------------------------------


class TestSafeRmTargets:
    def test_node_modules(self):
        assert is_safe_rm_target("rm -rf node_modules") is True

    def test_dist(self):
        assert is_safe_rm_target("rm -rf dist") is True

    def test_build(self):
        assert is_safe_rm_target("rm -rf build") is True

    def test_cache(self):
        assert is_safe_rm_target("rm -rf .cache") is True

    def test_pycache(self):
        assert is_safe_rm_target("rm -rf __pycache__") is True

    def test_next(self):
        assert is_safe_rm_target("rm -rf .next") is True

    def test_turbo(self):
        assert is_safe_rm_target("rm -rf .turbo") is True

    def test_coverage(self):
        assert is_safe_rm_target("rm -rf coverage") is True

    def test_pytest_cache(self):
        assert is_safe_rm_target("rm -rf .pytest_cache") is True

    def test_mypy_cache(self):
        assert is_safe_rm_target("rm -rf .mypy_cache") is True

    def test_tmp(self):
        assert is_safe_rm_target("rm -rf tmp") is True

    def test_slash_tmp(self):
        assert is_safe_rm_target("rm -rf /tmp/myfile") is True

    def test_venv(self):
        assert is_safe_rm_target("rm -rf venv") is True

    def test_dot_venv(self):
        assert is_safe_rm_target("rm -rf .venv") is True

    def test_eggs(self):
        assert is_safe_rm_target("rm -rf .eggs") is True

    def test_pyc_glob(self):
        assert is_safe_rm_target("rm -rf *.pyc") is True

    def test_random_path_not_safe(self):
        assert is_safe_rm_target("rm -rf /some/random/path") is False

    def test_no_rf_flag_returns_false(self):
        assert is_safe_rm_target("rm node_modules") is False


# ---------------------------------------------------------------------------
# AUTO-FIX
# ---------------------------------------------------------------------------


class TestAutofix:
    def test_force_to_force_with_lease(self):
        fixed, reason = check_autofix("git push origin --force feature")
        assert fixed is not None
        assert "--force-with-lease" in fixed
        assert "auto-fix" in reason

    def test_dash_f_to_force_with_lease(self):
        fixed, reason = check_autofix("git push -f origin feature")
        assert fixed is not None
        assert "--force-with-lease" in fixed

    def test_no_fix_for_main(self):
        fixed, reason = check_autofix("git push origin --force main")
        assert fixed is None

    def test_no_fix_for_master(self):
        fixed, reason = check_autofix("git push origin --force master")
        assert fixed is None

    def test_no_fix_when_already_with_lease(self):
        cmd = "git push origin --force-with-lease feature"
        fixed, reason = check_autofix(cmd)
        assert fixed is None

    def test_no_fix_for_safe_command(self):
        fixed, reason = check_autofix("ls -la")
        assert fixed is None
        assert reason is None

    def test_no_fix_for_empty(self):
        fixed, reason = check_autofix("")
        assert fixed is None
