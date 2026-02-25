# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""CervellaSwarm Event Store - SQLite event database for AI agent session tracking."""

from importlib.metadata import version as _version

__version__ = _version("cervellaswarm-event-store")

from cervellaswarm_event_store.config import (
    find_config_file,
    get_db_path,
    get_section,
    load_config,
)
from cervellaswarm_event_store.database import EventStore
from cervellaswarm_event_store.writer import (
    Event,
    Lesson,
)
from cervellaswarm_event_store.reader import (
    AgentSummary,
    EventRecord,
    QueryResult,
    Statistics,
)
from cervellaswarm_event_store.analytics import (
    DetectedPattern,
    ScoredLesson,
    get_relevant_lessons,
)

__all__ = [
    # Config
    "find_config_file",
    "get_db_path",
    "get_section",
    "load_config",
    # Core store
    "EventStore",
    # Write types
    "Event",
    "Lesson",
    # Read types
    "AgentSummary",
    "EventRecord",
    "QueryResult",
    "Statistics",
    # Analytics types
    "DetectedPattern",
    "ScoredLesson",
    "get_relevant_lessons",
]
