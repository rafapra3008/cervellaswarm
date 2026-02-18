# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""CervellaSwarm Session Memory - Git-native, human-readable session continuity for AI agents."""

from cervellaswarm_session_memory.config import (
    load_config,
    get_section,
    get_memory_dir,
)
from cervellaswarm_session_memory.project_manager import (
    ProjectInfo,
    init_project,
    discover_projects,
    get_project,
    normalize_name,
    archive_state,
)
from cervellaswarm_session_memory.quality_checker import (
    QualityResult,
    check_quality,
    check_all_projects,
    check_actionability,
    check_specificity,
    check_freshness,
    check_conciseness,
)
from cervellaswarm_session_memory.secret_auditor import (
    AuditResult,
    Finding,
    Severity,
    audit_directory,
    audit_file,
)
from cervellaswarm_session_memory.sync_checker import (
    SyncResult,
    CheckStatus,
    verify_project,
    verify_all,
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
