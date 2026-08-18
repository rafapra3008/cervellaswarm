# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
Configuration loader for CervellaSwarm Agent Hooks.

Hooks look for configuration in this order:
1. CERVELLA_HOOKS_CONFIG environment variable (explicit path)
2. .cervella/hooks.yaml in the current project root
3. ~/.claude/hooks.yaml (user-level default)

If no config file is found, hooks use sensible defaults.
"""

import copy
import os
from pathlib import Path

import yaml

__version__ = "1.0.0"

# Default config values
DEFAULTS = {
    "file_limits": {
        "checks": [
            {
                "pattern": "*.md",
                "name": "Large markdown files",
                "max_lines": 300,
                "action": "Consider splitting or archiving old content",
            }
        ],
    },
    "context_inject": {
        "facts_file": "docs/FACTS.md",
        "state_file": "SESSION_STATE.md",
        "facts_max_lines": 100,
        "state_max_lines": 50,
    },
    "session_checkpoint": {
        "state_file": "SESSION_STATE.md",
        "include_git_status": True,
        "include_recent_commits": True,
        "max_lines": 200,
    },
    "git_reminder": {
        "interval_minutes": 30,
    },
    "bash_validator": {
        "extra_blocked": [],
        "extra_risky": [],
        "extra_safe_rm": [],
    },
    "quality_validator": {
        # SNCP 5.1 quality metrics thresholds (warning only, mai blocco)
        "density_min": 0.30,
        "density_max": 0.55,
        "recency_max_old_pct": 0.30,   # max 30% entries >90gg in DOVE SIAMO + ProxStep
        "recency_min_recent_h2": 2,    # min 2 H2 <=14gg in DOVE SIAMO
        "recency_status_fallback": True,  # P1.2.A: fallback to status header date
        "coverage_hard": ["status", "dove siamo", "puntator"],
        "coverage_warn": ["prossim", "lezion"],
        "actionability_min": 3,         # >=3 step con owner+effort in ProxStep
        "anti_rot_min_pct": 0.80,       # >=80% path navigabili come markdown link
        "anti_rot_min_pct_state_a": 0.20,  # P1.2.C: lenient for legacy state A
        "self_sufficiency_lines": 50,   # prime 50 righe rispondono 3 boolean Q
        "split_threshold_lines": 150,   # soglia minima per split 3-tier
        "evergreen_scope_lookback_lines": 5,  # F2 (P4.6 R2): scope-marker lookback distance
        "report_dir": ".sncp/reports/daily",
    },
}


def find_config_file() -> Path | None:
    """Find the hooks config file in priority order."""
    # 1. Environment variable
    env_path = os.environ.get("CERVELLA_HOOKS_CONFIG")
    if env_path:
        p = Path(env_path)
        if p.exists():
            return p

    # 2. Project-level: .cervella/hooks.yaml (walk up from CWD)
    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        candidate = parent / ".cervella" / "hooks.yaml"
        if candidate.exists():
            return candidate
        # Stop at git root
        if (parent / ".git").exists():
            break

    # 3. User-level: ~/.claude/hooks.yaml
    user_config = Path.home() / ".claude" / "hooks.yaml"
    if user_config.exists():
        return user_config

    return None


def _deep_merge(base: dict, override: dict) -> dict:
    """Deep merge override into base (recursive for nested dicts)."""
    result = copy.deepcopy(base)
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def load_config(config_path: Path | None = None) -> dict:
    """Load hooks configuration, merging with defaults.

    Args:
        config_path: Explicit path to config file. If None, auto-discover.

    Returns:
        Merged configuration dictionary.
    """
    config_file = config_path if config_path else find_config_file()

    if config_file is None:
        return copy.deepcopy(DEFAULTS)

    try:
        with open(config_file, "r", encoding="utf-8") as f:
            user_config = yaml.safe_load(f) or {}
    except (OSError, yaml.YAMLError):
        return copy.deepcopy(DEFAULTS)

    if not isinstance(user_config, dict):
        return copy.deepcopy(DEFAULTS)

    return _deep_merge(DEFAULTS, user_config)


def get_hook_config(hook_name: str, config: dict | None = None) -> dict:
    """Get configuration for a specific hook, with defaults.

    Args:
        hook_name: Hook name (e.g. "file_limits", "git_reminder").
        config: Pre-loaded config. If None, loads automatically.

    Returns:
        Hook config dict with defaults merged in.
    """
    if config is None:
        config = load_config()
    defaults = DEFAULTS.get(hook_name, {})
    hook_config = config.get(hook_name, {})

    if isinstance(hook_config, dict) and isinstance(defaults, dict):
        return _deep_merge(defaults, hook_config)
    return hook_config if hook_config else copy.deepcopy(defaults)
