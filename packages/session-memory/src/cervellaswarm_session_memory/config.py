# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
Configuration loader for CervellaSwarm Session Memory.

Config is searched in this order:
1. CERVELLASWARM_SESSION_MEMORY_CONFIG environment variable (explicit path)
2. .cervella/session-memory.yaml in the current project root
3. ~/.claude/session-memory.yaml (user-level default)

If no config file is found, sensible defaults are used.
"""

import os
from pathlib import Path

import yaml

DEFAULTS = {
    "memory_dir": ".session-memory",
    "state_file": "SESSION_STATE.md",
    "compass_file": "PROJECT_COMPASS.md",
    "max_lines": 300,
    "warning_lines": 200,
    "quality": {
        "weights": {
            "actionability": 0.30,
            "specificity": 0.30,
            "freshness": 0.20,
            "conciseness": 0.20,
        },
        "target_score": 8.0,
    },
    "secrets": {
        "extra_patterns": [],
        "skip_files": [],
    },
    "projects": {},
}


def find_config_file() -> Path | None:
    """Find the session-memory config file in priority order."""
    # 1. Environment variable
    env_path = os.environ.get("CERVELLASWARM_SESSION_MEMORY_CONFIG")
    if env_path:
        p = Path(env_path)
        if p.exists():
            return p

    # 2. Project-level: .cervella/session-memory.yaml (walk up from CWD)
    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        candidate = parent / ".cervella" / "session-memory.yaml"
        if candidate.exists():
            return candidate
        # Stop at git root
        if (parent / ".git").exists():
            break

    # 3. User-level: ~/.claude/session-memory.yaml
    user_config = Path.home() / ".claude" / "session-memory.yaml"
    if user_config.exists():
        return user_config

    return None


def load_config(config_path: Path | None = None) -> dict:
    """Load session-memory configuration, merging with defaults.

    Args:
        config_path: Explicit path to config file. If None, auto-discover.

    Returns:
        Merged configuration dictionary.
    """
    config_file = config_path if config_path else find_config_file()

    if config_file is None:
        return _deep_copy_defaults()

    try:
        with open(config_file, "r", encoding="utf-8") as f:
            user_config = yaml.safe_load(f) or {}
    except Exception:
        return _deep_copy_defaults()

    return _merge_config(user_config)


def get_section(section: str, config: dict | None = None) -> dict:
    """Get a specific config section with defaults.

    Args:
        section: Section name (e.g., "quality", "secrets").
        config: Pre-loaded config. If None, loads automatically.

    Returns:
        Section config dict.
    """
    if config is None:
        config = load_config()

    defaults = DEFAULTS.get(section, {})
    section_config = config.get(section, {})

    if isinstance(section_config, dict) and isinstance(defaults, dict):
        return {**defaults, **section_config}
    return section_config if section_config else defaults


def get_memory_dir(project_root: Path | None = None, config: dict | None = None) -> Path:
    """Get the memory directory path.

    Args:
        project_root: Project root directory. If None, uses CWD.
        config: Pre-loaded config. If None, loads automatically.

    Returns:
        Absolute path to memory directory.
    """
    if config is None:
        config = load_config()

    memory_dir_name = config.get("memory_dir", DEFAULTS["memory_dir"])
    root = project_root if project_root else Path.cwd()
    return root / memory_dir_name


def _deep_copy_defaults() -> dict:
    """Create a deep copy of DEFAULTS to prevent mutation."""
    import copy
    return copy.deepcopy(DEFAULTS)


def _merge_config(user_config: dict) -> dict:
    """Merge user config with defaults (shallow per section)."""
    merged = _deep_copy_defaults()
    for section, values in user_config.items():
        if section in merged and isinstance(values, dict) and isinstance(merged[section], dict):
            merged[section] = {**merged[section], **values}
        else:
            merged[section] = values
    return merged
