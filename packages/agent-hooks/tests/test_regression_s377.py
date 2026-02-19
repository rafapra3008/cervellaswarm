# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
Regression tests for S377 bug fixes in cervellaswarm-agent-hooks.

Fix 1: config.py - except Exception narrowed to except (OSError, yaml.YAMLError)
Fix 2: bash_validator.py - invalid regex in extra patterns validated with re.compile()
"""

import re
from unittest.mock import patch

import pytest
import yaml

from cervellaswarm_agent_hooks.config import load_config, DEFAULTS
from cervellaswarm_agent_hooks.bash_validator import _load_extra_patterns


# ---------------------------------------------------------------------------
# Fix 1: config.py - narrowed except clause
# ---------------------------------------------------------------------------


class TestConfigNarrowedExcept:
    """Verify load_config() only silently catches OSError and yaml.YAMLError."""

    def test_oserror_returns_defaults(self, tmp_path, monkeypatch):
        """OSError (e.g. permission denied) is caught and defaults returned."""
        config_file = tmp_path / "hooks.yaml"
        config_file.write_text("bash_validator:\n  extra_blocked: []\n")
        monkeypatch.setenv("CERVELLA_HOOKS_CONFIG", str(config_file))

        with patch(
            "cervellaswarm_agent_hooks.config.open",
            side_effect=OSError("permission denied"),
        ):
            result = load_config()

        assert result == dict(DEFAULTS)

    def test_yaml_error_returns_defaults(self, tmp_path, monkeypatch):
        """yaml.YAMLError (malformed YAML) is caught and defaults returned."""
        config_file = tmp_path / "hooks.yaml"
        # Write content that triggers a YAMLError via mocked yaml.safe_load
        config_file.write_text("key: value\n")
        monkeypatch.setenv("CERVELLA_HOOKS_CONFIG", str(config_file))

        with patch(
            "cervellaswarm_agent_hooks.config.yaml.safe_load",
            side_effect=yaml.YAMLError("bad yaml"),
        ):
            result = load_config()

        assert result == dict(DEFAULTS)

    def test_type_error_propagates(self, tmp_path, monkeypatch):
        """TypeError is NOT caught - it propagates (was silently swallowed before fix)."""
        config_file = tmp_path / "hooks.yaml"
        config_file.write_text("key: value\n")
        monkeypatch.setenv("CERVELLA_HOOKS_CONFIG", str(config_file))

        with patch(
            "cervellaswarm_agent_hooks.config.yaml.safe_load",
            side_effect=TypeError("unexpected type"),
        ):
            with pytest.raises(TypeError, match="unexpected type"):
                load_config()

    def test_attribute_error_propagates(self, tmp_path, monkeypatch):
        """AttributeError is NOT caught - it propagates (was silently swallowed before fix)."""
        config_file = tmp_path / "hooks.yaml"
        config_file.write_text("key: value\n")
        monkeypatch.setenv("CERVELLA_HOOKS_CONFIG", str(config_file))

        with patch(
            "cervellaswarm_agent_hooks.config.yaml.safe_load",
            side_effect=AttributeError("unexpected attr"),
        ):
            with pytest.raises(AttributeError, match="unexpected attr"):
                load_config()


# ---------------------------------------------------------------------------
# Fix 2: bash_validator.py - invalid regex patterns skipped silently
# ---------------------------------------------------------------------------


class TestLoadExtraPatternsValidation:
    """Verify _load_extra_patterns() validates regex and skips invalid ones."""

    def _make_config(self, extra_blocked=None, extra_risky=None):
        """Build a bash_validator config dict."""
        return {
            "extra_blocked": extra_blocked or [],
            "extra_risky": extra_risky or [],
            "extra_safe_rm": [],
        }

    def test_valid_extra_blocked_pattern_works(self):
        """A valid extra_blocked pattern is loaded and detects the command."""
        cfg = self._make_config(
            extra_blocked=[{"pattern": r"dangerous-cmd", "reason": "test block"}]
        )
        with patch(
            "cervellaswarm_agent_hooks.config.get_hook_config",
            return_value=cfg,
        ):
            extra_blocked, extra_risky, extra_safe = _load_extra_patterns()

        assert len(extra_blocked) == 1
        pattern, reason = extra_blocked[0]
        assert re.search(pattern, "dangerous-cmd --flag") is not None
        assert reason == "test block"

    def test_valid_extra_risky_pattern_works(self):
        """A valid extra_risky pattern is loaded and detects the command."""
        cfg = self._make_config(
            extra_risky=[{"pattern": r"risky-cmd", "reason": "test risky"}]
        )
        with patch(
            "cervellaswarm_agent_hooks.config.get_hook_config",
            return_value=cfg,
        ):
            extra_blocked, extra_risky, extra_safe = _load_extra_patterns()

        assert len(extra_risky) == 1
        pattern, reason = extra_risky[0]
        assert re.search(pattern, "risky-cmd --arg") is not None
        assert reason == "test risky"

    def test_invalid_regex_in_extra_blocked_skipped(self):
        """An invalid regex in extra_blocked is silently skipped (no crash)."""
        cfg = self._make_config(
            extra_blocked=[{"pattern": "[unclosed", "reason": "bad regex"}]
        )
        with patch(
            "cervellaswarm_agent_hooks.config.get_hook_config",
            return_value=cfg,
        ):
            extra_blocked, extra_risky, extra_safe = _load_extra_patterns()

        assert extra_blocked == []

    def test_invalid_regex_in_extra_risky_skipped(self):
        """An invalid regex in extra_risky is silently skipped (no crash)."""
        cfg = self._make_config(
            extra_risky=[{"pattern": "(*invalid", "reason": "bad risky regex"}]
        )
        with patch(
            "cervellaswarm_agent_hooks.config.get_hook_config",
            return_value=cfg,
        ):
            extra_blocked, extra_risky, extra_safe = _load_extra_patterns()

        assert extra_risky == []

    def test_valid_and_invalid_patterns_mixed(self):
        """Valid patterns survive alongside invalid ones in the same list."""
        cfg = self._make_config(
            extra_blocked=[
                {"pattern": "[bad-regex", "reason": "invalid"},
                {"pattern": r"good-pattern", "reason": "valid block"},
                {"pattern": "(?P<x>a)(?P<x>b)", "reason": "also invalid"},
                {"pattern": r"another-good", "reason": "valid block 2"},
            ]
        )

        # Verify both "invalid" patterns are genuinely bad regex (pre-check)
        with pytest.raises(re.error):
            re.compile("[bad-regex")
        with pytest.raises(re.error):
            re.compile("(?P<x>a)(?P<x>b)")

        with patch(
            "cervellaswarm_agent_hooks.config.get_hook_config",
            return_value=cfg,
        ):
            extra_blocked, extra_risky, extra_safe = _load_extra_patterns()

        # Only the two valid patterns survive
        assert len(extra_blocked) == 2
        patterns = [p for p, _ in extra_blocked]
        assert r"good-pattern" in patterns
        assert r"another-good" in patterns
