# CervellaSwarm Lingua Universale

[![PyPI](https://img.shields.io/pypi/v/cervellaswarm-lingua-universale.svg)](https://pypi.org/project/cervellaswarm-lingua-universale/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org)
[![Tests](https://img.shields.io/badge/tests-3494%20passed-brightgreen.svg)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-98%25-brightgreen.svg)](tests/)
[![Playground](https://img.shields.io/badge/playground-try%20it%20now-blueviolet.svg)](https://rafapra3008.github.io/cervellaswarm/)
[![Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen.svg)]()

**The first programming language designed for AI. By AI.**

A complete language — grammar, compiler, REPL, LSP server, and formal verification —
built entirely on the Python standard library. **Zero external dependencies.**

```bash
pip install cervellaswarm-lingua-universale
```

> **No install needed?** [Try it in your browser](https://rafapra3008.github.io/cervellaswarm/) --
> write and run LU code in seconds, powered by Pyodide (Python in WebAssembly).

---

## What Is Lingua Universale?

Lingua Universale (LU) is a programming language where the question and the answer
live in the same language. It models AI agent communication with precision: who sends
what to whom, under what contracts, with what confidence.

It started as a session types library. It is now a full language:

- **Grammatica**: 64 production rules, formal EBNF, Lark + GBNF export
- **Compilatore**: tokenizer -> AST -> contract checker -> Python codegen
- **REPL**: interactive session with history and error recovery
- **LSP**: Language Server Protocol server for editor support
- **Verifica formale**: Lean 4 theorem generation and auto-verification
- **Errori umani**: 74 error codes in 3 languages (en/it/pt)

---

## Quick Start

### Python API

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

### .lu Files

Write protocols in the LU language and run them directly:

```
# hello.lu
agent Regina role=coordinator
agent Worker role=executor

protocol Greet {
    roles Regina, Worker;
    Regina -> Worker : TaskRequest;
    Worker -> Regina : TaskResult;
}
```

```bash
lu check hello.lu     # parse and compile, no execution
lu run   hello.lu     # parse, compile, and execute
lu repl               # interactive REPL
```

---

## CLI Reference

The `lu` command ships with 10 subcommands:

| Command | Description |
|---------|-------------|
| `lu run <file.lu>` | Parse, compile, and execute a .lu file |
| `lu check <file.lu>` | Parse and compile without executing (fast lint) |
| `lu verify <file.lu>` | Verify per-property with colored output (PROVED/VIOLATED/SKIPPED) |
| `lu compile <file.lu>` | Show (or save with `-o`) the generated Python source |
| `lu init <name>` | Scaffold a new LU project (`--template`, `--list-templates`) |
| `lu repl` | Start the interactive REPL with history |
| `lu lsp` | Start the LSP server over STDIO (requires `pygls`) |
| `lu chat` | Build protocols conversationally in natural language (3 languages) |
| `lu demo` | Run the autonomous "La Nonna" demo with typewriter effect |
| `lu version` | Show version and module count |

```bash
# Check a file and see what was declared
lu check hello.lu
# OK hello.lu
#   2 agent(s), 1 protocol(s)

# Compile to Python and save
lu compile hello.lu -o hello.py

# Chat: build protocols conversationally
lu chat --lang it          # Italian (also: en, pt)
lu chat --lang en --voice  # with voice input (requires [voice] extra)

# Demo: see the full "La Nonna" demo
lu demo --lang it --speed normal

# LSP (install optional dep first)
pip install "cervellaswarm-lingua-universale[lsp]"
lu lsp
```

---

## Editor Support (VS Code)

Install the [Lingua Universale VS Code extension](https://github.com/rafapra3008/cervellaswarm/tree/main/extensions/lingua-universale-vscode)
for a full editing experience:

| Feature | Description |
|---------|-------------|
| Syntax highlighting | Full TextMate grammar for all LU constructs |
| Diagnostics | Real-time error checking as you type (74 error codes) |
| Hover | Type info and Markdown documentation on mouse hover |
| Completion | Context-aware suggestions (7 contexts: top-level, agent body, trust, confidence, protocol body, properties, type references) |
| Go-to-definition | Click any type or agent name to jump to its definition |

The extension connects to the `lu lsp` language server automatically. Install both:

```bash
pip install "cervellaswarm-lingua-universale[lsp]"
code --install-extension lingua-universale-0.2.0.vsix
```

---

## Interactive Tutorial

Learn LU step by step with ["A Tour of Lingua Universale"](https://rafapra3008.github.io/cervellaswarm/) --
24 interactive steps across 4 chapters, running directly in your browser:

1. **Types** -- variant types, records, `Confident[T]`
2. **Agents** -- trust tiers, capabilities, contracts
3. **Protocols** -- roles, actions, choice branches, properties
4. **Verification** -- `lu check`, `lu verify`, formal proofs

Each step has editable, runnable code. No install required.

---

## Features

- **29 modules**, 137+ public API symbols
- **3494 tests**, 98% coverage, runs in under 1 second
- **Zero dependencies** -- pure Python standard library
- **Python 3.10+** including 3.13 free-threaded (thread-safe internals)
- **Grammar**: 64 production rules, GBNF + Lark export for constrained decoding
- **Errors**: 74 error codes in 3 languages (English, Italian, Portuguese)

---

## Architecture

```
Lingua Universale v0.3.1 -- 29 modules, zero dependencies

FASE A: Session Types
  types.py           14 MessageKind, 14 message dataclasses, 17 AgentRole
  protocols.py       Protocol, ProtocolStep, ProtocolChoice, 4 standard protocols
  checker.py         SessionChecker: runtime protocol enforcement
  dsl.py             Parse/render Scribble-inspired notation
  monitor.py         6 event types, ProtocolMonitor, MetricsCollector
  lean4_bridge.py    Generate + verify Lean 4 proofs (9 properties)
  integration.py     AgentInfo catalog, create_session, validate_swarm

FASE B: Advanced Types
  confidence.py      ConfidenceScore, Confident[T], 3 composition strategies
  trust.py           TrustScore, TrustTier, transitive compose, attenuation
  codegen.py         Python source generation from protocol AST
  intent.py          Natural language -> protocol intent parser
  spec.py            Property specs, formal checker, session verifier

FASE C: Il Linguaggio (compiler pipeline)
  _tokenizer.py      Lexer: 30+ token types, position tracking
  _ast.py            AST node hierarchy (agents, protocols, types, imports)
  _parser.py         Recursive descent parser, 64 production rules
  _contracts.py      Contract checker: scope, type, arity validation
  _compiler.py       ASTCompiler -> CompiledModule (Python AST)
  _interop.py        compile_file / load_file public API
  _grammar_export.py GBNF + Lark grammar export (constrained decoding)
  _eval.py           check_source / run_source / verify_source
  _repl.py           Interactive REPL with history and error recovery
  _cli.py            lu command: 10 subcommands (incl. chat, demo, init, verify)
  _init_project.py   Project scaffolding + stdlib templates (20 protocols)
  errors.py          74 error codes, 3 locales (en/it/pt), rich snippets
  _colors.py         ANSI colors respecting NO_COLOR / FORCE_COLOR

FASE D: Ecosistema
  _lsp.py            Language Server Protocol (STDIO, requires pygls)

FASE E: Per Tutti (IntentBridge)
  _intent_bridge.py  NL/guided -> IntentDraft -> verified protocol (3 languages)
  _nl_processor.py   Claude-powered NL intent extraction (optional: anthropic)
  _voice.py          Voice input via faster-whisper STT (optional: sounddevice)
```

---

## Session Types and Protocols

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

---

## Confidence Types

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

---

## Trust Composition

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

---

## Protocol Monitor

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

---

## Lean 4 Verification

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
#   ... (7 structural properties; 9 semantic PropertyKind in spec.py)
```

If [Lean 4](https://lean-lang.org/) is installed, verify automatically:

```python
from cervellaswarm_lingua_universale import Lean4Verifier

verifier = Lean4Verifier()
report = verifier.verify_protocol(DelegateTask)
print(report.all_proved)  # True -- mathematically proven
```

---

## Standard Library

20 verified protocols across 5 categories, ready to use as templates:

```bash
lu init --list-templates          # see all 20 templates
lu init my-project --template rag_pipeline  # scaffold from a template
```

| Category | Protocols |
|----------|-----------|
| **Communication** (5) | request_response, ping_pong, pub_sub, scatter_gather, pipeline |
| **Data** (3) | crud_safe, data_sync, cache_invalidation |
| **Business** (4) | two_buyer (MPST canonical), approval_workflow, auction, saga_order |
| **AI/ML** (5) | rag_pipeline, agent_delegation, tool_calling, human_in_loop, consensus |
| **Security** (3) | auth_handshake, mutual_tls, rate_limited_api |

All 9 PropertyKind covered: `always_terminates`, `no_deadlock`, `all_roles_participate`,
`ordering`, `trust_min`, `confidence_min`, `no_deletion`, `role_exclusive`, `exclusion`.

Based on research of Scribble, MPST (Honda/Yoshida POPL 2008), gRPC patterns,
and AI agent protocols. Every protocol parses and verifies to PROVED.
(Structural guarantee for finite protocols.)

---

## How It Compares

| Feature | AutoGen | CrewAI | LangGraph | **Lingua Universale** |
|---------|---------|--------|-----------|----------------------|
| Typed messages | No | No | No | **Yes** (14 message types) |
| Protocol enforcement | No | No | No | **Yes** (runtime checker) |
| Formal DSL + compiler | No | No | No | **Yes** (64 grammar rules) |
| Standard library | No | No | No | **Yes** (20 verified protocols) |
| Protocol observability | No | No | Partial | **Yes** (6 event types) |
| Lean 4 verification | No | No | No | **Yes** (9 properties) |
| Confidence types | No | No | No | **Yes** (`Confident[T]`) |
| Trust composition | No | No | No | **Yes** (transitive) |
| REPL + LSP (hover, completion, goto-def) | No | No | No | **Yes** |
| NL protocol building (chat) | No | No | No | **Yes** (3 languages) |
| Voice input | No | No | No | **Yes** (local STT) |
| Browser playground | No | No | No | **Yes** (Pyodide, $0) |
| Interactive tutorial | No | No | No | **Yes** (24 steps) |
| Constrained decoding export | No | No | No | **Yes** (GBNF + Lark) |
| External dependencies | Many | Many | Many | **Zero** |

---

## FAQ

**What is a session type?**

A session type describes the sequence of messages two or more parties exchange.
Instead of "send whatever, hope the other side understands", a session type says
"first A sends X to B, then B sends Y to A." The checker enforces this at
runtime, catching violations immediately with a precise error message.

**What is a .lu file?**

A `.lu` source file written in the Lingua Universale language. It can declare agents,
protocols, types, and imports. The `lu` CLI compiles it to Python and can run or
formally verify it.

**Do I need Lean 4 installed?**

No. Lean 4 verification is optional. The core library (types, protocols, checker,
DSL, compiler, REPL, confidence, trust) works with zero external tools. Install
Lean 4 only if you want mathematical proofs of protocol properties.

**Do I need pygls for the LSP?**

The LSP server (`lu lsp`) requires `pygls`. Install it with:
`pip install "cervellaswarm-lingua-universale[lsp]"`
Everything else works without it.

**Can I define my own message types and protocols?**

Yes. The 14 built-in message types and 4 standard protocols cover common
multi-agent patterns, but you can create custom protocols with any roles, any
message types, and any branching logic -- both in Python and in `.lu` files.

**How does this relate to academic session types?**

This library implements multiparty session types (Honda, Yoshida, Carbone 2008)
adapted for AI agent systems. The DSL syntax is inspired by Scribble. The key
adaptation: our types model AI-specific concerns like confidence, trust, and
audit flows that don't exist in traditional distributed systems.

---

## Development

```bash
git clone https://github.com/rafapra3008/cervellaswarm.git
cd cervellaswarm/packages/lingua-universale
pip install -e ".[dev]"

# Run tests (3494 tests, < 2s)
pytest

# Run with coverage
pytest --cov=cervellaswarm_lingua_universale --cov-report=term-missing
```

---

## Part of CervellaSwarm

This package is the language engine of [CervellaSwarm](https://github.com/rafapra3008/cervellaswarm),
a multi-agent AI coordination system with 17 specialized agents. It works
completely standalone -- no other CervellaSwarm packages required.

---

## References

- Honda, Yoshida, Carbone. [Multiparty Asynchronous Session Types](https://doi.org/10.1145/1328438.1328472). POPL 2008.
- Scribble Project. [scribble.org](https://www.scribble.org/). Protocol description language.
- Josang. [Subjective Logic](https://doi.org/10.1007/978-3-319-42337-1). Springer 2016. Trust composition.
- Lean 4. [lean-lang.org](https://lean-lang.org/). Theorem prover.

---

## License

[Apache-2.0](LICENSE)
