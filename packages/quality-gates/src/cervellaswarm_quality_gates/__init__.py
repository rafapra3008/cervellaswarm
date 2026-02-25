# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""CervellaSwarm Quality Gates - Quality gates for AI agent swarms."""

from importlib.metadata import version as _version

__version__ = _version("cervellaswarm-quality-gates")

from cervellaswarm_quality_gates.config import (
    find_config_file,
    get_section,
    load_config,
)
from cervellaswarm_quality_gates.hooks import (
    HookReport,
    HookStatus,
    hooks_summary,
    validate_hook,
    validate_hooks,
)
from cervellaswarm_quality_gates.quality import (
    QualityScore,
    score_content,
    score_file,
)
from cervellaswarm_quality_gates.sync import (
    FileDiff,
    SyncAction,
    SyncResult,
    compare_agents,
)

__all__ = [
    # Config
    "find_config_file",
    "get_section",
    "load_config",
    # Quality scoring
    "QualityScore",
    "score_content",
    "score_file",
    # Hook validation
    "HookReport",
    "HookStatus",
    "hooks_summary",
    "validate_hook",
    "validate_hooks",
    # Agent sync
    "FileDiff",
    "SyncAction",
    "SyncResult",
    "compare_agents",
]
