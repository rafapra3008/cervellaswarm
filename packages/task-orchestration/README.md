# cervellaswarm-task-orchestration

**Deterministic task classification, routing, and validation for multi-agent systems.**

Zero LLM calls. File-based state. Git-friendly audit trail.

```
Task Description ──> Classifier ──> Router ──> Workers
                     (rule-based)   (deterministic)  │
                                                     ▼
                                              Output Validator
                                              (score 0-100)
```

## Why This Exists

Every multi-agent framework routes tasks using LLM calls. That means:
- Non-deterministic results (same input, different routing)
- API costs for every routing decision
- Latency before any real work starts
- No way to unit-test routing logic

This package takes a different approach: **rule-based classification with zero LLM calls**.
The classifier uses keyword scoring, file count estimation, and pattern matching to produce
a deterministic complexity score. Same input always produces the same routing decision.

## Installation

```bash
pip install cervellaswarm-task-orchestration
```

**Requirements:** Python 3.10+ | **Dependencies:** None (zero external deps!)

## Quick Start

### Classify a Task

```python
from cervellaswarm_task_orchestration import classify_task, TaskComplexity

result = classify_task("refactor the authentication module across 5 files")
print(result.complexity)       # TaskComplexity.CRITICAL
print(result.should_architect)  # True
print(result.confidence)        # 1.0
print(result.triggers)          # ['refactor', 'files>5 (5)']
```

### Route to Architect or Workers

```python
from cervellaswarm_task_orchestration import route_task

decision = route_task("fix typo in README")
print(decision.use_architect)      # False
print(decision.suggested_workers)  # [WorkerType.DOCS]

decision = route_task("redesign the entire API layer")
print(decision.use_architect)      # True
print(decision.reason)             # "Task critical: Detailed planning required"
```

### Validate an Architect Plan

```python
from cervellaswarm_task_orchestration import validate_plan

result = validate_plan(plan_markdown)
print(result.is_valid)   # True/False
print(result.score)      # 0.0 - 10.0
print(result.errors)     # ['Missing section: ## Phase 2: Design']
print(result.warnings)   # ['Plan too short (< 500 chars)']
```

### Manage Task State (File-Based)

```python
from cervellaswarm_task_orchestration import (
    create_task, mark_ready, mark_working, mark_done, get_task_status
)

# Create a task (writes .swarm/tasks/TASK_001.md)
create_task("TASK_001", "backend-worker", "Implement user auth endpoint", risk_level=2)

# State machine: created -> ready -> working -> done
mark_ready("TASK_001")
mark_working("TASK_001")   # ATOMIC: only one worker can claim!
mark_done("TASK_001")

print(get_task_status("TASK_001"))  # "done"
```

### Validate Worker Output

```python
from cervellaswarm_task_orchestration import validate_output
from pathlib import Path

result = validate_output(Path(".swarm/tasks/TASK_001_output.md"))
print(result.valid)         # True/False
print(result.score)         # 0-100
print(result.retry_needed)  # True if score < 50
print(result.errors)        # ['Error markers found: Traceback, ERROR:']
```

## CLI Tools

```bash
# Classify task complexity
cervella-classify "refactor the database layer"

# Route task to architect or workers
cervella-route "add pagination to the API" --json

# Validate an architect plan
cervella-validate-plan .swarm/plans/PLAN_001.md

# Validate worker output
cervella-validate-output --file output.md

# Manage tasks
cervella-task create TASK_001 backend-worker "Implement auth" --risk 2
cervella-task list
cervella-task status TASK_001

# Unified CLI
cervella-orchestrate classify "migrate to PostgreSQL"
cervella-orchestrate route "fix typo in docs"
cervella-orchestrate task list
```

## Architecture

### Task Classifier (`task_classifier.py`)

Rule-based complexity scoring with zero LLM calls:

| Input | Method | Output |
|-------|--------|--------|
| "fix typo" | Simple keyword fast-path | SIMPLE (confidence: 0.9) |
| "add new endpoint" | Keyword scoring | MEDIUM (confidence: 0.27) |
| "refactor auth module" | Keyword scoring | COMPLEX (confidence: 0.53) |
| "redesign entire API across 10 files" | Keyword + file count | CRITICAL (confidence: 1.0) |

Complexity levels: `SIMPLE` < `MEDIUM` < `COMPLEX` < `CRITICAL`

### Architect Flow (`architect_flow.py`)

Routing + plan validation + fallback logic:

```
classify_task() ──> should_architect?
                    │
              ┌─────┴─────┐
              No           Yes
              │            │
         Direct to     Architect
         Workers       Planning
              │            │
              │      validate_plan()
              │            │
              │      ┌─────┴─────┐
              │      Valid       Invalid
              │      │           │
              │      Approve     Reject (max 2x)
              │                  │
              │            FALLBACK_TO_WORKER
              ▼                  │
         Output Validator  <─────┘
```

### Task Manager (`task_manager.py`)

File-based state machine with atomic operations:

```
created ──> ready ──> working ──> done
                        │
                  ATOMIC CLAIM
                 (exclusive create)
```

- Race condition protection via `open(file, 'x')` exclusive create
- Path traversal prevention with strict ID validation
- All state visible in the filesystem (git-friendly audit trail)

### Output Validator (`output_validator.py`)

Reflection pattern with cumulative scoring:

| Check | Impact | Example |
|-------|--------|---------|
| File missing | score = 0 | Output file not created |
| Empty file | score = 0 | Worker created but didn't write |
| Error markers | -40 points | `Traceback`, `ERROR:`, `FAILED` |
| Incomplete markers | -15 points | `TODO:`, `FIXME:` (outside code blocks) |
| Too short | -10 points | Less than 100 characters |
| Log errors | -10 points | Corresponding worker log has errors |
| Success indicators | +5 points | `DONE`, `Completed`, `PASSED` |

**Score < 50 triggers `retry_needed = True`**

## Comparison with Other Frameworks

| Feature | CervellaSwarm | CrewAI | AutoGen | LangGraph | OpenAI SDK |
|---------|:---:|:---:|:---:|:---:|:---:|
| Task Classification | Rule-based | LLM | LLM | Manual | LLM |
| Complexity Scoring | 0.0-1.0 | No | No | No | No |
| Deterministic Routing | Yes | No | No | Partial | No |
| Output Validation | Score 0-100 | Guardrails | Manual | Manual | Tripwire |
| Fallback Escalation | 3-level | Same agent | max_turns | Checkpoint | Exception |
| File-based State | Yes | No | No | No | No |
| Atomic Race Protection | Yes | No | No | No | No |
| Zero LLM Calls | Yes | No | No | No | No |
| Zero Dependencies | Yes | No | No | No | No |

> **Honest note:** CrewAI and AutoGen have larger ecosystems and multi-LLM support.
> LangGraph offers more flexible graph-based workflows. This package focuses on
> deterministic, testable orchestration with zero external dependencies.

## Customization

### Custom Tasks Directory

```python
from cervellaswarm_task_orchestration.task_manager import create_task

create_task("TASK_001", "worker", "My task", tasks_dir="my_project/.tasks")
```

### Plan Validation Sections

The plan validator checks for these required sections:
- `## Metadata` (with Task ID, Complexity, Files Affected)
- `## Phase 1: Understanding`
- `## Phase 2: Design`
- `## Phase 3: Review`
- `## Phase 4: Final Plan` (with `### Success Criteria`)

### Worker Type Routing

The router maps keywords to worker types:

| Keywords | Worker Type |
|----------|------------|
| api, endpoint, database, python, fastapi | BACKEND |
| ui, frontend, react, css, component | FRONTEND |
| test, verify, bug, fix, debug | TESTER |
| deploy, docker, ci, cd, infra | DEVOPS |
| doc, readme, guide, tutorial | DOCS |
| data, analytics, report, etl | DATA |
| research, investigate, compare | RESEARCHER |
| security, auth, vulnerability | SECURITY |

## API Reference

### task_classifier

- `classify_task(description, estimated_files?, has_breaking_changes?, force_architect?) -> ClassificationResult`
- `should_use_architect(description) -> bool`
- `estimate_files_affected(description) -> int`
- `calculate_keyword_score(description) -> tuple[float, list[str]]`
- `is_simple_task(description) -> bool`
- `has_multifile_pattern(description) -> bool`

### architect_flow

- `route_task(description, task_id?, force_architect?, force_direct?) -> RoutingDecision`
- `validate_plan(content) -> PlanValidationResult`
- `validate_plan_file(path) -> PlanValidationResult`
- `create_session(task_id, description) -> ArchitectSession`
- `approve_plan(session, approved_by?) -> ArchitectSession`
- `handle_plan_rejection(session, reason) -> tuple[ArchitectSession, str]`
- `should_fallback(session) -> bool`
- `create_fallback_instruction(session) -> str`
- `save_session_state(session, output_dir?) -> Path`

### task_manager

- `create_task(task_id, agent, description, risk_level?, tasks_dir?) -> str`
- `list_tasks(tasks_dir?) -> list[dict]`
- `mark_ready(task_id, tasks_dir?) -> bool`
- `mark_working(task_id, tasks_dir?) -> bool` (atomic!)
- `mark_done(task_id, tasks_dir?) -> bool`
- `ack_received(task_id, tasks_dir?) -> bool`
- `ack_understood(task_id, tasks_dir?) -> bool`
- `get_task_status(task_id, tasks_dir?) -> str`
- `get_ack_status(task_id, tasks_dir?) -> str`
- `cleanup_task(task_id, tasks_dir?) -> bool`
- `validate_task_id(task_id) -> bool`

### output_validator

- `validate_output(output_file, logs_dir?) -> ValidationResult`
- `find_last_output(tasks_dir?) -> Path | None`
- `find_task_output(task_id, tasks_dir?) -> Path | None`

## Development

```bash
git clone https://github.com/rafapra3008/cervellaswarm.git
cd cervellaswarm/packages/task-orchestration
pip install -e ".[dev]"
pytest
```

## License

Apache-2.0 - see [LICENSE](LICENSE) for details.

---

Part of [CervellaSwarm](https://github.com/rafapra3008/cervellaswarm) - Build AI agent teams that remember.
