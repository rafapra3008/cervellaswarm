# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""CervellaSwarm Task Orchestration - Deterministic task classification, routing, and validation."""

__version__ = "0.1.0"

from cervellaswarm_task_orchestration.task_classifier import (
    ClassificationResult,
    TaskComplexity,
    classify_task,
    should_use_architect,
)
from cervellaswarm_task_orchestration.architect_flow import (
    ArchitectSession,
    PlanStatus,
    PlanValidationResult,
    RoutingDecision,
    WorkerType,
    route_task,
    validate_plan,
)
from cervellaswarm_task_orchestration.task_manager import (
    create_task,
    list_tasks,
    mark_ready,
    mark_working,
    mark_done,
    get_task_status,
    cleanup_task,
)
from cervellaswarm_task_orchestration.output_validator import (
    validate_output,
)

__all__ = [
    # task_classifier
    "ClassificationResult",
    "TaskComplexity",
    "classify_task",
    "should_use_architect",
    # architect_flow
    "ArchitectSession",
    "PlanStatus",
    "PlanValidationResult",
    "RoutingDecision",
    "WorkerType",
    "route_task",
    "validate_plan",
    # task_manager
    "create_task",
    "list_tasks",
    "mark_ready",
    "mark_working",
    "mark_done",
    "get_task_status",
    "cleanup_task",
    # output_validator
    "validate_output",
]
