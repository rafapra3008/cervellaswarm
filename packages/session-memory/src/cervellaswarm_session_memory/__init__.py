# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""CervellaSwarm Session Memory - Git-native, human-readable session continuity for AI agents."""

from importlib.metadata import version as _version

__version__ = _version("cervellaswarm-session-memory")

from cervellaswarm_session_memory.config import (
    get_memory_dir,
    get_section,
    load_config,
)
from cervellaswarm_session_memory.project_manager import (
    ProjectInfo,
    archive_state,
    discover_projects,
    get_project,
    init_project,
    normalize_name,
)
from cervellaswarm_session_memory.quality_checker import (
    QualityResult,
    check_actionability,
    check_all_projects,
    check_conciseness,
    check_freshness,
    check_quality,
    check_specificity,
)
from cervellaswarm_session_memory.secret_auditor import (
    AuditResult,
    Finding,
    Severity,
    audit_directory,
    audit_file,
)
from cervellaswarm_session_memory.sync_checker import (
    CheckStatus,
    SyncResult,
    verify_all,
    verify_project,
)

__all__ = [
    # Config
    "load_config",
    "get_section",
    "get_memory_dir",
    # Project management
    "ProjectInfo",
    "init_project",
    "discover_projects",
    "get_project",
    "normalize_name",
    "archive_state",
    # Quality checking
    "QualityResult",
    "check_quality",
    "check_all_projects",
    "check_actionability",
    "check_specificity",
    "check_freshness",
    "check_conciseness",
    # Secret auditing
    "AuditResult",
    "Finding",
    "Severity",
    "audit_directory",
    "audit_file",
    # Sync checking
    "SyncResult",
    "CheckStatus",
    "verify_project",
    "verify_all",
]
