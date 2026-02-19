# cervellaswarm-lingua-universale

Session types and formal protocols for AI agent communication.

**The first typed protocol system for multi-agent AI frameworks.**

## What This Solves

AI agent frameworks (AutoGen, CrewAI, LangGraph) use untyped string messages.
No guarantees that agents follow the protocol. No verification. No formal safety.

This package provides:
- **Typed messages**: every agent message has a schema
- **Session protocols**: communication sequences are formally defined
- **Runtime checking**: protocol violations detected at runtime
- **Protocol monitor**: track state of all active conversations

## Quick Start

```python
from cervellaswarm_lingua_universale.types import TaskRequest, TaskResult, TaskStatus
from cervellaswarm_lingua_universale.protocols import DelegateTask
from cervellaswarm_lingua_universale.checker import SessionChecker

# Create a typed message
request = TaskRequest(
    task_id="T001",
    description="Fix the login bug",
    target_files=["src/auth.py"],
    constraints=["No breaking changes"],
)

# Start a protocol session
checker = SessionChecker(DelegateTask)
checker.send("regina", "backend", request)  # OK

# Worker responds
result = TaskResult(
    task_id="T001",
    status=TaskStatus.OK,
    summary="Fixed null check in auth handler",
    files_modified=["src/auth.py"],
)
checker.send("backend", "regina", result)  # OK

# Trying to send wrong message type = ProtocolViolation
# checker.send("backend", "regina", request)  # RAISES!
```

## License

Apache-2.0
