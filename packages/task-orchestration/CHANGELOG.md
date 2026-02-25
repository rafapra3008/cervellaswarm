# Changelog

All notable changes to `cervellaswarm-task-orchestration` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-02-18

### Added

- **Task Classifier** - Rule-based complexity scoring with zero LLM calls
  - Keyword scoring with configurable weights (17 complexity keywords)
  - File count estimation from natural language descriptions
  - Multi-file pattern detection via regex
  - Simple-task fast path (10 keywords bypass scoring)
  - Four complexity levels: SIMPLE, MEDIUM, COMPLEX, CRITICAL
  - Confidence score 0.0-1.0

- **Architect Flow** - Task routing and plan validation
  - `route_task()` - Deterministic routing to architect or workers
  - `validate_plan()` - Structured plan validation (4-phase format, metadata, success criteria)
  - `handle_plan_rejection()` - 3-level fallback escalation
  - `save_session_state()` - JSON session persistence
  - 8 worker types for automatic suggestion (backend, frontend, tester, devops, docs, data, researcher, security)

- **Task Manager** - File-based state management
  - Marker files (.ready, .working, .done, .ack_received, .ack_understood)
  - Atomic race condition protection via exclusive create (`open(f, 'x')`)
  - Path traversal prevention with strict ID validation
  - Configurable tasks directory
  - Git-friendly audit trail

- **Output Validator** - Reflection pattern for quality assessment
  - Cumulative scoring 0-100 with deductions per issue type
  - Error marker detection (10 patterns: Traceback, ERROR, FAILED, etc.)
  - Incomplete marker detection with code block awareness
  - Corresponding log correlation
  - Automatic retry recommendation (score < 50)

- **CLI Tools** - 6 entry points
  - `cervella-classify` - Classify task complexity
  - `cervella-route` - Route task to architect or workers
  - `cervella-validate-plan` - Validate architect plan files
  - `cervella-validate-output` - Validate worker output files
  - `cervella-task` - Manage tasks (create, list, status transitions)
  - `cervella-orchestrate` - Unified CLI dispatching to all subcommands

[0.1.0]: https://github.com/rafapra3008/cervellaswarm/releases/tag/task-orchestration-v0.1.0
