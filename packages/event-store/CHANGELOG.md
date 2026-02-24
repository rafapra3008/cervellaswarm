# Changelog

All notable changes to `cervellaswarm-event-store` will be documented in this file.

## [0.1.0] - 2026-02-24

### Added
- Initial release
- `EventStore` class with SQLite backend (WAL mode, :memory: support)
- Three-table schema: `events`, `lessons`, `error_patterns`
- `Event` and `Lesson` frozen dataclasses with `__post_init__` validation
- `log_event` / `log_lesson` writer functions
- `query_events` with flexible filters (agent, project, event_type, session, limit, days)
- `get_statistics` returning `Statistics` frozen dataclass
- `get_lessons` with relevance scoring (`ScoredLesson`)
- `detect_patterns` via `SequenceMatcher` similarity clustering
- `agent_stats` per-agent aggregated view
- `get_relevant_lessons` context-aware scoring
- `config.py` with env var > project `.cervella/` > user `~/.claude/` priority
- `cervella-events` CLI: init, log, query, stats, lessons, patterns subcommands
- `--json` flag on all commands
- ZERO runtime dependencies (stdlib only: sqlite3, uuid, json, difflib, argparse)
- 180+ tests with `:memory:` database fixtures
