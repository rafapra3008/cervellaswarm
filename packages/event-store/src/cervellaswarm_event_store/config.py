# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
Configuration loader for cervellaswarm-event-store.

DB path resolution order:
1. CERVELLASWARM_EVENT_STORE_DB env var (explicit db path)
2. db_path key in config file
3. .cervella/event-store.db in project root (walk up from CWD)

Config file search order:
1. CERVELLASWARM_EVENT_STORE_CONFIG env var (explicit config path)
2. .cervella/event-store.yaml in project root
3. ~/.claude/event-store.yaml (user-level)

If no config is found, defaults are used.
"""

import copy
import os
from pathlib import Path

try:
    import yaml as _yaml  # optional

    _YAML_AVAILABLE = True
except ImportError:  # pragma: no cover
    _YAML_AVAILABLE = False

DEFAULTS: dict = {
    "db_path": ".cervella/event-store.db",
    "pattern_detection": {
        "similarity_threshold": 0.7,
        "min_occurrences": 3,
        "default_days": 7,
    },
    "lessons": {
        "default_limit": 10,
        "min_confidence": 0.5,
    },
    "query": {
        "default_limit": 50,
    },
}


def find_config_file() -> "Path | None":
    """Find the event-store config file in priority order."""
    # 1. Explicit env var
    env_path = os.environ.get("CERVELLASWARM_EVENT_STORE_CONFIG")
    if env_path:
        p = Path(env_path)
        if p.exists():
            return p

    # 2. Project-level: walk up from CWD
    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        candidate = parent / ".cervella" / "event-store.yaml"
        if candidate.exists():
            return candidate
        if (parent / ".git").exists():
            break

    # 3. User-level
    user_config = Path.home() / ".claude" / "event-store.yaml"
    if user_config.exists():
        return user_config

    return None


def _deep_copy_defaults() -> dict:
    """Return a deep copy of DEFAULTS to prevent mutation."""
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


def load_config(config_path: "Path | None" = None) -> dict:
    """Load event-store configuration, merging with defaults.

    Args:
        config_path: Explicit path to config file. If None, auto-discover.

    Returns:
        Merged configuration dictionary.
    """
    config_file = config_path if config_path else find_config_file()

    if config_file is None:
        return _deep_copy_defaults()

    if not _YAML_AVAILABLE:
        return _deep_copy_defaults()

    try:
        with open(config_file, "r", encoding="utf-8") as f:
            user_config = _yaml.safe_load(f) or {}
    except (OSError, Exception):
        return _deep_copy_defaults()

    return _merge_config(user_config)


def get_db_path(config: "dict | None" = None) -> Path:
    """Resolve the SQLite database path.

    Resolution order:
    1. CERVELLASWARM_EVENT_STORE_DB env var
    2. config["db_path"]
    3. Default: .cervella/event-store.db (relative to CWD)

    Args:
        config: Pre-loaded config. If None, loads automatically.

    Returns:
        Absolute Path to the SQLite database file.
    """
    # 1. Env var override (explicit DB path)
    env_db = os.environ.get("CERVELLASWARM_EVENT_STORE_DB")
    if env_db:
        return Path(env_db)

    # 2. Config file
    if config is None:
        config = load_config()

    db_path_str = config.get("db_path", DEFAULTS["db_path"])
    db_path = Path(db_path_str)

    # Resolve relative to CWD if not absolute
    if not db_path.is_absolute():
        db_path = Path.cwd() / db_path

    return db_path


def get_section(section: str, config: "dict | None" = None) -> dict:
    """Get a specific config section with defaults applied.

    Args:
        section: Section name (e.g. "pattern_detection", "lessons").
        config: Pre-loaded config. If None, loads automatically.

    Returns:
        Section config dict with defaults merged in.
    """
    if config is None:
        config = load_config()

    defaults = DEFAULTS.get(section, {})
    section_config = config.get(section, {})

    if isinstance(section_config, dict) and isinstance(defaults, dict):
        return {**defaults, **section_config}
    return section_config if section_config else copy.deepcopy(defaults) if isinstance(defaults, dict) else defaults
