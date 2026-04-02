# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""
Architect Flow - Task routing and plan validation for multi-agent orchestration.

Integrates with the task classifier to decide whether a task should go through
an architect planning phase or directly to workers. Provides structured plan
validation and a fallback mechanism after repeated rejections.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional
import json
import re

from cervellaswarm_task_orchestration.task_classifier import (
    ClassificationResult,
    classify_task,
)


class PlanStatus(Enum):
    """Possible states of a plan."""

    DRAFT = "draft"
    WAITING_APPROVAL = "waiting_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    REVISION_1 = "revision_1"
    REVISION_2 = "revision_2"
    FALLBACK = "fallback"  # After 2 rejections


class WorkerType(Enum):
    """Available worker types for task routing."""

    BACKEND = "backend"
    FRONTEND = "frontend"
    TESTER = "tester"
    DEVOPS = "devops"
    DOCS = "docs"
    DATA = "data"
    RESEARCHER = "researcher"
    SECURITY = "security"


@dataclass
class PlanValidationResult:
    """Result of plan validation."""

    is_valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    score: float = 0.0  # 0.0 - 10.0


@dataclass
class RoutingDecision:
    """Routing decision from the orchestrator."""

    use_architect: bool
    classification: ClassificationResult
    reason: str
    suggested_workers: list[WorkerType] = field(default_factory=list)


@dataclass
class ArchitectSession:
    """Planning session with the architect agent."""

    task_id: str
    task_description: str
    status: PlanStatus = PlanStatus.DRAFT
    plan_path: Optional[Path] = None
    revision_count: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    approved_at: Optional[datetime] = None
    approved_by: Optional[str] = None
    rejection_reasons: list[str] = field(default_factory=list)


# =============================================================================
# Task Routing
# =============================================================================

# Keyword-to-worker mapping for automatic suggestion
_WORKER_KEYWORDS: dict[str, list[str]] = {
    "BACKEND": ["api", "endpoint", "database", "python", "fastapi", "backend", "server", "query", "sql"],
    "FRONTEND": ["ui", "frontend", "react", "css", "component", "button", "page", "style", "layout"],
    "TESTER": ["test", "verify", "check", "bug", "fix", "debug", "coverage", "pytest"],
    "DEVOPS": ["deploy", "docker", "ci", "cd", "infra", "nginx", "kubernetes", "pipeline"],
    "DOCS": ["doc", "readme", "guide", "tutorial", "comment", "changelog"],
    "DATA": ["data", "analytics", "report", "etl", "migration", "export"],
    "RESEARCHER": ["research", "investigate", "compare", "analyze", "study"],
    "SECURITY": ["security", "auth", "permission", "vulnerability", "audit", "encrypt"],
}


def route_task(
    task_description: str,
    task_id: Optional[str] = None,
    force_architect: bool = False,
    force_direct: bool = False,
) -> RoutingDecision:
    """
    Decide whether a task should go through architect planning or directly to workers.

    Args:
        task_description: Natural language task description.
        task_id: Unique task ID (generated if None).
        force_architect: Force architect usage.
        force_direct: Force bypass architect (go directly to workers).

    Returns:
        RoutingDecision with the decision and motivation.
    """
    if force_direct:
        return RoutingDecision(
            use_architect=False,
            classification=classify_task(task_description),
            reason="Architect bypassed (force_direct=True)",
            suggested_workers=_suggest_workers(task_description),
        )

    if force_architect:
        return RoutingDecision(
            use_architect=True,
            classification=classify_task(task_description, force_architect=True),
            reason="Architect forced (force_architect=True)",
            suggested_workers=[],
        )

    # Automatic classification
    classification = classify_task(task_description)

    if classification.should_architect:
        return RoutingDecision(
            use_architect=True,
            classification=classification,
            reason=f"Task {classification.complexity.value}: {classification.reasoning}",
            suggested_workers=[],
        )
    else:
        return RoutingDecision(
            use_architect=False,
            classification=classification,
            reason=f"Task {classification.complexity.value}: proceed directly",
            suggested_workers=_suggest_workers(task_description),
        )


def _suggest_workers(task_description: str) -> list[WorkerType]:
    """
    Suggest appropriate workers based on the task description.

    Returns:
        List of WorkerType in priority order.
    """
    desc_lower = task_description.lower()
    workers: list[WorkerType] = []

    for worker_name, keywords in _WORKER_KEYWORDS.items():
        if any(kw in desc_lower for kw in keywords):
            workers.append(WorkerType[worker_name])

    # Default: backend if no match
    if not workers:
        workers.append(WorkerType.BACKEND)

    return workers


# =============================================================================
# Plan Validation
# =============================================================================

# Required sections in the plan
REQUIRED_PLAN_SECTIONS: list[str] = [
    "## Metadata",
    "## Phase 1: Understanding",
    "## Phase 2: Design",
    "## Phase 3: Review",
    "## Phase 4: Final Plan",
]

# Required metadata fields
REQUIRED_METADATA_FIELDS: list[str] = [
    "Task ID",
    "Complexity",
    "Files Affected",
]

# Pattern for success criteria
SUCCESS_CRITERIA_PATTERN = r"###\s*Success Criteria"


def validate_plan(plan_content: str) -> PlanValidationResult:
    """
    Validate the content of an architect-generated plan.

    Checks for required sections, metadata fields, success criteria,
    execution order, file references, and plan length.

    Args:
        plan_content: Markdown content of the plan.

    Returns:
        PlanValidationResult with validity, errors, and score.
    """
    errors: list[str] = []
    warnings: list[str] = []
    score = 10.0

    # Check required sections
    for section in REQUIRED_PLAN_SECTIONS:
        if section not in plan_content:
            errors.append(f"Missing section: {section}")
            score -= 1.5

    # Check metadata fields
    metadata_section = _extract_section(plan_content, "## Metadata", "## Phase 1")
    if metadata_section:
        for fld in REQUIRED_METADATA_FIELDS:
            if fld not in metadata_section:
                errors.append(f"Missing metadata field: {fld}")
                score -= 0.5
    else:
        errors.append("Metadata section not found or malformed")
        score -= 2.0

    # Check success criteria
    if not re.search(SUCCESS_CRITERIA_PATTERN, plan_content, re.IGNORECASE):
        errors.append("Success Criteria not defined")
        score -= 1.0

    # Check execution order
    if "### Execution Order" not in plan_content and "Execution Order" not in plan_content:
        warnings.append("Execution Order not explicit")
        score -= 0.5

    # Check file references
    if not re.search(r"`[^`]+\.(py|ts|js|md|json|yaml)`", plan_content):
        warnings.append("No specific files mentioned in plan")
        score -= 0.5

    # Check plan length
    if len(plan_content) < 500:
        warnings.append("Plan too short (< 500 chars)")
        score -= 1.0

    if len(plan_content) > 10000:
        warnings.append("Plan too long (> 10000 chars)")
        score -= 0.5

    score = max(0.0, min(10.0, score))

    return PlanValidationResult(
        is_valid=len(errors) == 0 and score >= 7.0,
        errors=errors,
        warnings=warnings,
        score=score,
    )


def validate_plan_file(plan_path: Path) -> PlanValidationResult:
    """
    Validate a plan file from disk.

    Args:
        plan_path: Path to the plan markdown file.

    Returns:
        PlanValidationResult.
    """
    if not plan_path.exists():
        return PlanValidationResult(
            is_valid=False,
            errors=[f"File not found: {plan_path}"],
            score=0.0,
        )

    content = plan_path.read_text()
    return validate_plan(content)


def _extract_section(content: str, start_marker: str, end_marker: str) -> Optional[str]:
    """Extract a section between two markers."""
    start_idx = content.find(start_marker)
    if start_idx == -1:
        return None

    end_idx = content.find(end_marker, start_idx + len(start_marker))
    if end_idx == -1:
        end_idx = len(content)

    return content[start_idx:end_idx]


# =============================================================================
# Fallback Logic
# =============================================================================

MAX_REVISIONS = 2  # After 2 rejections -> fallback


def handle_plan_rejection(
    session: ArchitectSession,
    rejection_reason: str,
) -> tuple[ArchitectSession, str]:
    """
    Handle rejection of a plan.

    Tracks rejection count and transitions to fallback after MAX_REVISIONS.

    Args:
        session: Current architect session.
        rejection_reason: Reason for rejection.

    Returns:
        Tuple of (updated session, action string).
    """
    session.rejection_reasons.append(rejection_reason)
    session.revision_count += 1

    if session.revision_count == 1:
        session.status = PlanStatus.REVISION_1
        action = "REQUEST_REVISION"
    elif session.revision_count == 2:
        session.status = PlanStatus.REVISION_2
        action = "REQUEST_REVISION"
    else:
        session.status = PlanStatus.FALLBACK
        action = "FALLBACK_TO_WORKER"

    return session, action


def should_fallback(session: ArchitectSession) -> bool:
    """Check whether the session should fall back (too many rejections)."""
    return session.revision_count > MAX_REVISIONS


def create_fallback_instruction(session: ArchitectSession) -> str:
    """
    Create instructions for a worker when falling back from architect mode.

    Args:
        session: Session with task details.

    Returns:
        Markdown instructions for the worker.
    """
    reasons = "\n".join(f"- {r}" for r in session.rejection_reasons)

    return f"""# Fallback Mode - Task {session.task_id}

> **WARNING:** Plan not approved after {session.revision_count} attempts.
> Proceed with caution, one step at a time.

## Task
{session.task_description}

## Rejection History
{reasons}

## Fallback Instructions
1. **Start SMALL** - smallest possible change
2. **Ask for confirmation** - after every significant step
3. **Test immediately** - verify before continuing
4. **Document** - write what you did and why

## Warning
The plan was rejected. Proceed with:
- Incremental changes
- Frequent checkpoints
- No broad refactoring without approval
"""


# =============================================================================
# Session Management
# =============================================================================


def create_session(task_id: str, task_description: str) -> ArchitectSession:
    """Create a new architect session."""
    return ArchitectSession(
        task_id=task_id,
        task_description=task_description,
        status=PlanStatus.DRAFT,
    )


def approve_plan(session: ArchitectSession, approved_by: str = "coordinator") -> ArchitectSession:
    """Approve a plan."""
    session.status = PlanStatus.APPROVED
    session.approved_at = datetime.now()
    session.approved_by = approved_by
    return session


def get_plan_path(task_id: str, base_dir: Optional[Path] = None) -> Path:
    """Return the standard path for a plan file."""
    base = base_dir or Path(".swarm/plans")
    return base / f"PLAN_{task_id}.md"


def save_session_state(
    session: ArchitectSession,
    output_dir: Optional[Path] = None,
) -> Path:
    """
    Save session state to disk as JSON.

    Args:
        session: The architect session to save.
        output_dir: Directory for session files (default: .swarm/sessions).

    Returns:
        Path of the saved file.
    """
    out = output_dir or Path(".swarm/sessions")
    out.mkdir(parents=True, exist_ok=True)
    output_path = out / f"session_{session.task_id}.json"

    state = {
        "task_id": session.task_id,
        "task_description": session.task_description,
        "status": session.status.value,
        "plan_path": str(session.plan_path) if session.plan_path else None,
        "revision_count": session.revision_count,
        "created_at": session.created_at.isoformat(),
        "approved_at": session.approved_at.isoformat() if session.approved_at else None,
        "approved_by": session.approved_by,
        "rejection_reasons": session.rejection_reasons,
    }

    output_path.write_text(json.dumps(state, indent=2))
    return output_path
