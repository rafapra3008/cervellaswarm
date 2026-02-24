# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
Configuration loader for cervellaswarm-quality-gates.

Config file search order:
1. CERVELLASWARM_QUALITY_GATES_CONFIG env var (explicit path)
2. .cervella/quality-gates.yaml in project root (walk up from CWD)
3. ~/.claude/quality-gates.yaml (user-level)

If no config is found, defaults are used.
"""

from __future__ import annotations

import copy
import os
from pathlib import Path
from types import MappingProxyType
from typing import Any

_YAML_AVAILABLE = False
_YAML_ERRORS: tuple[type[Exception], ...] = ()
try:
    import yaml as _yaml

    _YAML_AVAILABLE = True
    _YAML_ERRORS = (_yaml.YAMLError,)
except ImportError:  # pragma: no cover
    pass

_DEFAULTS_RAW: dict[str, Any] = {
    "quality": {
        "weights": {
            "actionability": 0.30,
            "specificity": 0.30,
            "freshness": 0.20,
            "conciseness": 0.20,
        },
        "min_score": 7.0,
    },
    "hooks": {
        "directory": ".claude/hooks/",
        "required_hooks": [],
    },
    "sync": {
        "ignore_patterns": ["*.pyc", "__pycache__", ".DS_Store"],
    },
}

# P04: Immutable global with MappingProxyType
DEFAULTS: MappingProxyType = MappingProxyType({
    k: MappingProxyType(v) if isinstance(v, dict) else v
    for k, v in _DEFAULTS_RAW.items()
})


def find_config_file() -> Path | None:
    """Find the quality-gates config file in priority order."""
    env_path = os.environ.get("CERVELLASWARM_QUALITY_GATES_CONFIG")
    if env_path:
        p = Path(env_path)
        if p.exists():
            return p

    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        candidate = parent / ".cervella" / "quality-gates.yaml"
        if candidate.exists():
            return candidate
        if (parent / ".git").exists():
            break

    user_config = Path.home() / ".claude" / "quality-gates.yaml"
    if user_config.exists():
        return user_config

    return None


def _load_yaml(path: Path) -> dict:
    """Load a YAML file safely. Returns empty dict on error."""
    if not _YAML_AVAILABLE:
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return _yaml.safe_load(f) or {}
    except (OSError, ValueError, *_YAML_ERRORS):
        return {}


def _deep_merge(base: dict, override: dict) -> dict:
    """Deep merge override into base (recursive for nested dicts)."""
    result = copy.deepcopy(base)
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def load_config(config_path: Path | None = None) -> dict[str, Any]:
    """Load quality-gates configuration, merging with defaults.

    Args:
        config_path: Explicit path to config file. If None, auto-discover.

    Returns:
        Merged configuration dictionary.
    """
    config_file = config_path if config_path else find_config_file()

    if config_file is None:
        return copy.deepcopy(_DEFAULTS_RAW)

    user_config = _load_yaml(config_file)
    if not user_config:
        return copy.deepcopy(_DEFAULTS_RAW)

    return _deep_merge(_DEFAULTS_RAW, user_config)


def get_section(section: str, config: dict | None = None) -> dict:
    """Get a specific config section with defaults applied.

    Args:
        section: Section name (e.g. "quality", "hooks", "sync").
        config: Pre-loaded config. If None, loads automatically.

    Returns:
        Section config dict with defaults merged in.
    """
    if config is None:
        config = load_config()

    defaults = _DEFAULTS_RAW.get(section, {})
    section_data = config.get(section, {})

    if isinstance(section_data, dict) and isinstance(defaults, dict):
        return _deep_merge(defaults, section_data)
    return section_data if section_data else copy.deepcopy(defaults)
