# CervellaSwarm Lingua Universale

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org)
[![Tests](https://img.shields.io/badge/tests-1273%20passed-brightgreen.svg)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-98%25-brightgreen.svg)](tests/)
[![Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen.svg)]()

Runtime-verified communication protocols for AI agents. **Zero dependencies.**

## The Problem

Every multi-agent AI framework today -- AutoGen, CrewAI, LangGraph -- uses untyped
messages. Agents send dictionaries, strings, or arbitrary JSON. Nothing guarantees
that Agent B will understand what Agent A sent. Nothing verifies the conversation
follows the protocol. When things break, nobody knows where.

```python
# How multi-agent frameworks work today
agent_b.send({"task": "fix bug", "files": ["auth.py"]})  # dict. no schema. hope for the best.
```

This package changes that.

```bash
pip install cervellaswarm-lingua-universale
```

## Quick Start

```python
from cervellaswarm_lingua_universale import (
    SessionChecker, DelegateTask, TaskRequest, TaskResult, TaskStatus,
)

# Define a typed message
request = TaskRequest(
    task_id="T001",
    description="Fix the login bug",
    target_files=("src/auth.py",),
)

# Start a protocol-checked session
checker = SessionChecker(DelegateTask)
checker.send("regina", "worker", request)  # OK: protocol expects TaskRequest here

# Worker responds with the correct type
result = TaskResult(task_id="T001", status=TaskStatus.OK, summary="Fixed null check")
checker.send("worker", "regina", result)   # OK: protocol expects TaskResult here

# Wrong message? Caught immediately.
checker.send("worker", "regina", request)
# raises ProtocolViolation: expected sender=regina, got sender=worker
```

The violation tells you **exactly** what went wrong: who sent it, who should have
sent it, what was expected at this step in the protocol.

## How It Compares

| Feature | AutoGen | CrewAI | LangGraph | **Lingua Universale** |
|---------|---------|--------|-----------|----------------------|
| Typed messages | No | No | No | **Yes** (14 message types) |
| Protocol enforcement | No | No | No | **Yes** (runtime checker) |
| Formal DSL | No | No | No | **Yes** (Scribble-inspired) |
| Protocol observability | No | No | Partial | **Yes** (6 event types) |
| Lean 4 verification | No | No | No | **Yes** (7 properties) |
| Confidence types | No | No | No | **Yes** (`Confident[T]`) |
| Trust composition | No | No | No | **Yes** (transitive) |
| External dependencies | Many | Many | Many | **Zero** |

To our knowledge, this is the first implementation of session types for AI agents
in Python. A new category, not an incremental improvement.

## Features

- **9 modules**, 84 public API symbols
- **1273 tests**, 98% coverage, runs in 0.3 seconds
- **Zero dependencies** -- pure Python standard library
- **Python 3.10+** including 3.13 free-threaded (thread-safe internals)

### Session Types and Protocols

Define who can send what to whom, and in what order:

```python
from cervellaswarm_lingua_universale import Protocol, ProtocolStep, ProtocolChoice, MessageKind

review_protocol = Protocol(
    name="CodeReview",
    roles=("developer", "reviewer", "approver"),
    elements=(
        ProtocolStep("developer", "reviewer", MessageKind.TASK_REQUEST),
        ProtocolChoice(
            decider="reviewer",
            branches={
                "approve": (
                    ProtocolStep("reviewer", "approver", MessageKind.AUDIT_REQUEST),
                    ProtocolStep("approver", "developer", MessageKind.AUDIT_VERDICT),
                ),
                "reject": (
                    ProtocolStep("reviewer", "developer", MessageKind.TASK_RESULT),
                ),
            },
        ),
    ),
)
```

### DSL Notation

Write protocols in human-readable syntax inspired by
[Scribble](https://www.scribble.org/) (Honda, Yoshida, Carbone, POPL 2008):

```python
from cervellaswarm_lingua_universale import parse_protocol, render_protocol

protocol = parse_protocol("""
protocol CodeReview {
    roles developer, reviewer;

    developer -> reviewer : TaskRequest;

    choice at reviewer {
        approve: {
            reviewer -> developer : AuditVerdict;
        }
        reject: {
            reviewer -> developer : TaskResult;
        }
    }
}
""")

# Round-trip fidelity: parse(render(P)) preserves structure
print(render_protocol(protocol))
```

### Confidence Types

Uncertainty as a first-class type -- not a string, not a comment:

```python
from cervellaswarm_lingua_universale import Confident, ConfidenceScore

# Wrap any value with its confidence
result = Confident(
    value="Authentication bug is in line 42",
    confidence=ConfidenceScore(0.85, evidence=("stack_trace", "test_failure")),
)

# Compose confidence through a pipeline
reviewed = result.and_then(lambda finding: Confident(
    value=f"Confirmed: {finding}",
    confidence=ConfidenceScore(0.95),
))

print(reviewed.confidence.value)  # 0.8075 (0.85 * 0.95 -- multiplicative)
print(reviewed.is_high)           # True (>= 0.8)
```

### Trust Composition

Model how trust propagates through delegation chains:

```python
from cervellaswarm_lingua_universale import TrustScore, TrustTier, compose_chain

coordinator = TrustScore(value=1.0, tier=TrustTier.VERIFIED)
worker = TrustScore(value=0.75, tier=TrustTier.STANDARD)

# A -> B -> C: trust composes multiplicatively
chain_trust = compose_chain((coordinator, worker))
print(chain_trust.value)  # 0.75
print(chain_trust.tier)   # TrustTier.STANDARD (lower of the two)

# Privilege attenuation: B cannot give C more authority than A gave B
attenuated = worker.attenuate(0.5)
print(attenuated.value)   # 0.375
```

### Protocol Monitor

Observe protocol execution with zero overhead when disabled:

```python
from cervellaswarm_lingua_universale import (
    SessionChecker, DelegateTask, ProtocolMonitor, EventCollector,
)

monitor = ProtocolMonitor()
collector = EventCollector()
monitor.add_listener(collector)

checker = SessionChecker(DelegateTask, monitor=monitor)
# ... send messages ...

for event in collector.events:
    print(f"{event.event_type}: {event.timestamp}")
```

### Lean 4 Bridge

Generate formal proofs that your protocols are correct:

```python
from cervellaswarm_lingua_universale import Lean4Generator, DelegateTask

generator = Lean4Generator()
lean_code = generator.generate(DelegateTask)
print(lean_code)
# Outputs Lean 4 code with theorems:
#   theorem DelegateTask_senders_valid : ...  := by decide
#   theorem DelegateTask_no_self_loop : ...   := by decide
#   theorem DelegateTask_non_empty : ...      := by decide
#   ... (5 flat properties total)
```

If [Lean 4](https://lean-lang.org/) is installed, verify automatically:

```python
from cervellaswarm_lingua_universale import Lean4Verifier

verifier = Lean4Verifier()
report = verifier.verify_protocol(DelegateTask)
print(report.all_proved)  # True -- mathematically proven
```

## FAQ

**What is a session type?**

A session type describes the sequence of messages two or more parties exchange.
Instead of "send whatever, hope the other side understands", a session type says
"first A sends X to B, then B sends Y to A." The type checker enforces this at
runtime, catching violations immediately.

**Do I need Lean 4 installed?**

No. Lean 4 verification is optional. The core library (types, protocols, checker,
DSL, monitor, confidence, trust) works with zero external tools. Install Lean 4
only if you want mathematical proofs of protocol properties.

**Can I define my own message types and protocols?**

Yes. The 14 built-in message types and 4 standard protocols cover common
multi-agent patterns, but you can create custom protocols with any roles, any
message types, and any branching logic.

**How does this relate to academic session types?**

This library implements multiparty session types (Honda, Yoshida, Carbone 2008)
adapted for AI agent systems. The DSL syntax is inspired by Scribble. The key
adaptation: our types model AI-specific concerns like confidence, trust, and
audit flows that don't exist in traditional distributed systems.

## Architecture

```
Source: Pure Python, zero dependencies

types.py            14 MessageKind, 14 message dataclasses, 17 AgentRole
    |
protocols.py        Protocol, ProtocolStep, ProtocolChoice, 4 standard protocols
    |
    +-- dsl.py              Parse/render Scribble-inspired notation
    +-- monitor.py          6 event types, ProtocolMonitor, MetricsCollector
    +-- lean4_bridge.py     Generate + verify Lean 4 proofs (7 properties)
    |
checker.py          SessionChecker: runtime protocol enforcement
    |
confidence.py       ConfidenceScore, Confident[T], 3 composition strategies
trust.py            TrustScore, TrustTier, transitive compose, attenuation
    |
integration.py      AgentInfo catalog, create_session, validate_swarm
```

9 modules, 84 public symbols, no circular dependencies.

## Limitations

- **Runtime only**: protocol violations are caught at runtime, not at type-check
  time. Static verification via mypy plugin is a future goal (Fase C).
- **No nested choices**: the DSL parser handles single-level `choice at` blocks.
  Nested branching is planned for a future release.
- **Lean 4 optional**: formal verification requires Lean 4 installed separately.
  The proofs use `by decide` (decidable properties only).
- **Python only**: no TypeScript/Go/Rust bindings yet.

## Development

```bash
git clone https://github.com/rafapra3008/cervellaswarm.git
cd cervellaswarm/packages/lingua-universale
pip install -e ".[dev]"

# Run tests (1273 tests, ~0.3s)
pytest

# Run with coverage
pytest --cov=cervellaswarm_lingua_universale --cov-report=term-missing
```

## Part of CervellaSwarm

This package is the protocol engine of [CervellaSwarm](https://github.com/rafapra3008/cervellaswarm),
a multi-agent AI coordination system with 17 specialized agents. It works
completely standalone -- no other CervellaSwarm packages required.

## References

- Honda, Yoshida, Carbone. [Multiparty Asynchronous Session Types](https://doi.org/10.1145/1328438.1328472). POPL 2008.
- Scribble Project. [scribble.org](https://www.scribble.org/). Protocol description language.
- Josang. [Subjective Logic](https://doi.org/10.1007/978-3-319-42337-1). Springer 2016. Trust composition.
- Lean 4. [lean-lang.org](https://lean-lang.org/). Theorem prover.

## License

[Apache-2.0](LICENSE)
