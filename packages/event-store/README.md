# cervellaswarm-event-store

SQLite event database for AI agent session tracking and analytics.

Zero dependencies. Pure Python stdlib.

## Features

- **Three-table schema**: `events`, `lessons`, `error_patterns`
- **WAL mode**: concurrent reads and fast writes
- **Relevance scoring**: lessons ranked by agent, project, severity, and confidence
- **Pattern detection**: similarity clustering via `difflib.SequenceMatcher`
- **Config priority**: env var > `.cervella/event-store.yaml` > `~/.claude/event-store.yaml` > defaults
- **In-memory mode**: `EventStore(":memory:")` for fast testing
- **Type-safe**: frozen dataclasses with `__post_init__` validation throughout

## Install

```bash
pip install cervellaswarm-event-store
```

## Quick Start

```python
from cervellaswarm_event_store import EventStore, Event, Lesson

with EventStore() as store:
    # Log an event
    event = Event(
        event_type="task_completed",
        agent_name="backend",
        project="my-project",
        description="Implemented auth endpoint",
        success=True,
        duration_ms=1200,
    )
    event_id = store.log_event(event)

    # Log a lesson
    lesson = Lesson(
        context="FastAPI auth",
        problem="JWT decode failed silently",
        solution="Always validate algorithm explicitly",
        pattern="explicit-algorithm-validation",
        confidence=0.9,
    )
    store.log_lesson(lesson)

    # Query
    result = store.query_events(project="my-project", limit=10)
    stats = store.get_statistics()
    lessons = store.get_lessons(project="my-project", limit=5)
    patterns = store.detect_patterns(days=7, min_occurrences=3)
```

## CLI

```bash
# Initialize database
cervella-events init

# Log an event
cervella-events log --type task_completed --agent backend --project myproj

# Query events
cervella-events query --project myproj --limit 20 [--json]

# Statistics
cervella-events stats [--project myproj] [--json]

# Lessons
cervella-events lessons --project myproj --limit 5 [--json]

# Pattern detection
cervella-events patterns --days 7 --min-occurrences 3 [--json]
```

## Schema

### events
Tracks every agent action: task start/complete/fail, session events, custom events.

### lessons
Structured knowledge extracted from sessions, with confidence scoring and relevance ranking.

### error_patterns
Recurring error signatures detected via similarity analysis.

## Configuration

Default DB path: `.cervella/event-store.db` (project-local).

Override via:
1. `CERVELLASWARM_EVENT_STORE_DB` environment variable (explicit DB path)
2. `CERVELLASWARM_EVENT_STORE_CONFIG` environment variable (config file path)
3. `.cervella/event-store.yaml` in project root
4. `~/.claude/event-store.yaml` (user-level)

## License

Apache-2.0. See [LICENSE](LICENSE).
