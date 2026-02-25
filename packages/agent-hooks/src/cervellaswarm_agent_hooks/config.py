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


def load_config() -> dict:
    """Load hooks configuration, merging with defaults."""
    config_file = find_config_file()

    if config_file is None:
        return dict(DEFAULTS)

    try:
        with open(config_file, "r", encoding="utf-8") as f:
            user_config = yaml.safe_load(f) or {}
    except (OSError, yaml.YAMLError):
        return dict(DEFAULTS)

    # Merge: user config overrides defaults (shallow per section)
    merged = dict(DEFAULTS)
    for section, values in user_config.items():
        if section in merged and isinstance(values, dict):
            merged[section] = {**merged[section], **values}
        else:
            merged[section] = values

    return merged


def get_hook_config(hook_name: str) -> dict:
    """Get configuration for a specific hook, with defaults."""
    config = load_config()
    defaults = DEFAULTS.get(hook_name, {})
    hook_config = config.get(hook_name, {})

    if isinstance(hook_config, dict) and isinstance(defaults, dict):
        return {**defaults, **hook_config}
    return hook_config if hook_config else defaults
