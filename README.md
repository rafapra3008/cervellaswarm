<div align="center">

# Lingua Universale

**A language for verified AI agent protocols.**

[![PyPI](https://img.shields.io/pypi/v/cervellaswarm-lingua-universale.svg)](https://pypi.org/project/cervellaswarm-lingua-universale/)
[![Tests](https://img.shields.io/badge/tests-3920_passing-brightgreen.svg)](packages/lingua-universale/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-blue.svg)](packages/lingua-universale/)
[![VS Code](https://img.shields.io/badge/VS_Code-Marketplace-blue.svg)](https://marketplace.visualstudio.com/items?itemName=cervellaswarm.lingua-universale)
[![Discord](https://img.shields.io/badge/Discord-community-5865F2.svg)](https://discord.gg/bvUBuejXxV)

[**Try it in your browser**](https://rafapra3008.github.io/cervellaswarm/) -- no install needed.
[**Watch AI agents live**](https://lu-debugger.fly.dev/) -- 3 agents on a verified protocol.

</div>

---

## The Problem

Your AI agents talk to each other, but nothing guarantees they follow the rules. Wrong sender, wrong message order, missing steps -- and you only find out in production.

Lingua Universale (LU) is a type checker for AI agent conversations. You define the protocol, LU proves it's correct, and the runtime enforces it.

```python
from cervellaswarm_lingua_universale import Protocol, ProtocolStep, MessageKind, SessionChecker, TaskRequest

# Define: who sends what, to whom, in what order
review = Protocol(name="Review", roles=("dev", "reviewer"), elements=(
    ProtocolStep(sender="dev", receiver="reviewer", message_kind=MessageKind.TASK_REQUEST),
    ProtocolStep(sender="reviewer", receiver="dev", message_kind=MessageKind.TASK_RESULT),
))

checker = SessionChecker(review)
checker.send("dev", "reviewer", TaskRequest(task_id="1", description="Review auth"))  # OK
checker.send("dev", "reviewer", TaskRequest(task_id="2", description="Oops"))         # ProtocolViolation!
#                                                                                      ^^^ wrong turn: reviewer must send next
```

The protocol says reviewer goes next. The runtime blocks it. Not because you trust the code -- because the session type makes it impossible.

---

## Install

```bash
pip install cervellaswarm-lingua-universale
```

Or try it first: [**Playground**](https://rafapra3008.github.io/cervellaswarm/) (runs in your browser via Pyodide).

---

## Write a Protocol

```
protocol DelegateTask:
    roles: supervisor, worker, validator

    supervisor asks worker to execute analysis
    worker returns result to supervisor
    supervisor asks validator to verify result

    when validator decides:
        pass:
            validator returns approval to supervisor
        fail:
            validator sends feedback to supervisor

    properties:
        always terminates
        no deadlock
        no deletion
        all roles participate
```

Then verify it:

```bash
lu verify delegate_task.lu
```

```
  [1/4] always_terminates  ... PROVED
  [2/4] no_deadlock        ... PROVED
  [3/4] no_deletion        ... PROVED
  [4/4] all_roles_participate ... PROVED

  All 4 properties PASSED.
```

Mathematical proof. Not a test that passes today and fails tomorrow.

---

## What You Get

| Feature | Description |
|---------|-------------|
| **Full compiler** | Tokenizer, parser (64 rules), AST, contract checker, Python codegen |
| **9 verified properties** | `always_terminates`, `no_deadlock`, `no_deletion`, `role_exclusive`, and more |
| **20 stdlib protocols** | AI/ML, Business, Communication, Data, Security -- ready to use |
| **Linter + Formatter** | `lu lint` (10 rules) + `lu fmt` (zero-config, like gofmt) |
| **LSP server** | Diagnostics, hover, completion, go-to-definition, formatting |
| **VS Code extension** | [Install from Marketplace](https://marketplace.visualstudio.com/items?itemName=cervellaswarm.lingua-universale) |
| **Interactive chat** | `lu chat` -- build protocols conversationally (English, Italian, Portuguese) |
| **Browser playground** | [Try it now](https://rafapra3008.github.io/cervellaswarm/) -- Check, Lint, Run, Chat |
| **Lean 4 bridge** | Generate and verify mathematical proofs |
| **REPL** | `lu repl` for interactive exploration |
| **Project scaffolding** | `lu init --template rag_pipeline` from 20 verified templates |

36 modules. 3920 tests. Zero external dependencies. Pure Python stdlib.

---

## CLI

```bash
lu check file.lu          # Parse and compile
lu verify file.lu         # Formal property verification
lu run file.lu            # Execute
lu lint file.lu           # 10 style and correctness rules
lu fmt file.lu            # Zero-config auto-formatter
lu chat --lang en         # Build a protocol conversationally
lu demo --lang it         # See the La Nonna demo
lu init --template NAME   # Scaffold from stdlib templates
lu mcp-audit --manifest t.json  # Audit MCP server protocols
lu repl                   # Interactive REPL
lu lsp                    # Start LSP server
```

---

## CI Integration

Add protocol verification to your GitHub Actions workflow:

```yaml
# .github/workflows/lu-check.yml
on:
  push:
    paths: ["**/*.lu"]

jobs:
  lu-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v6
        with:
          python-version: "3.11"
      - run: pip install cervellaswarm-lingua-universale
      - run: lu lint protocols/
      - run: lu verify protocols/
```

Exit code is non-zero on violations -- works with any CI system.

---

## How It Works

LU is built on [multiparty session types](https://en.wikipedia.org/wiki/Session_type) (Honda, Yoshida, Carbone -- POPL 2008). Session types describe communication protocols as types: if two processes follow the same session type, they cannot deadlock, messages cannot arrive in the wrong order, and the conversation always terminates.

The pipeline:

```
.lu source → Tokenizer → Parser → AST → Spec Checker → Lean 4 Proofs → Python Codegen
                                           ↓
                                    PROVED or VIOLATED
```

LU doesn't replace your AI agent framework. It makes it safe. Like TypeScript for JavaScript -- you keep your tools, you add guarantees.

---

## Examples

**[LU Debugger](https://lu-debugger.fly.dev/)** -- Live web app: 3 AI agents (Customer, Warehouse, Payment) communicate on a verified OrderProcessing protocol. Click "Break" to see a protocol violation blocked in real time. [Source code](lu-debugger/).

See the [`examples/`](packages/lingua-universale/examples/) directory:

- **[Agent Orchestration](packages/lingua-universale/examples/dogfood_agent_orchestration.lu)** -- 3 AI agents with nested choice, 8/8 properties proved
- **[Live Runner](packages/lingua-universale/examples/dogfood_runner_live.py)** -- Real Claude API agents on a verified protocol
- **[Standard Library](packages/lingua-universale/src/cervellaswarm_lingua_universale/stdlib/)** -- 20 verified protocols across 5 categories

Or try the [interactive Colab notebook](https://colab.research.google.com/github/rafapra3008/cervellaswarm/blob/main/docs/blog/from-vibecoding-to-vericoding-demo.ipynb) -- 2 minutes, zero setup.

---

## More from CervellaSwarm

Lingua Universale is the core project by [CervellaSwarm](https://github.com/rafapra3008/cervellaswarm). We also publish these Python packages:

| Package | What it does |
|---------|-------------|
| [code-intelligence](packages/code-intelligence/) | AST-powered code understanding (tree-sitter, PageRank) |
| [agent-hooks](packages/agent-hooks/) | Lifecycle hooks for Claude Code agents |
| [agent-templates](packages/agent-templates/) | Agent definition templates & team configuration |
| [task-orchestration](packages/task-orchestration/) | Deterministic task routing & validation |
| [spawn-workers](packages/spawn-workers/) | Multi-agent process management |
| [session-memory](packages/session-memory/) | Persistent session context across conversations |
| [event-store](packages/event-store/) | Immutable event logging & audit trail |
| [quality-gates](packages/quality-gates/) | Automated quality checks & scoring |

All Apache 2.0, Python 3.10+, tested, documented.

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

- **Bug reports:** [GitHub Issues](https://github.com/rafapra3008/cervellaswarm/issues)
- **Security:** See [SECURITY.md](SECURITY.md) for responsible disclosure

---

## License

Apache License 2.0 -- see [LICENSE](LICENSE).

Copyright 2025-2026 CervellaSwarm Contributors.

---

<div align="center">

**Lingua Universale** -- *Verified protocols for AI agents.*

[Playground](https://rafapra3008.github.io/cervellaswarm/) | [LU Debugger](https://lu-debugger.fly.dev/) | [PyPI](https://pypi.org/project/cervellaswarm-lingua-universale/) | [VS Code](https://marketplace.visualstudio.com/items?itemName=cervellaswarm.lingua-universale) | [Blog](docs/blog/from-vibecoding-to-vericoding.md) | [Colab Demo](https://colab.research.google.com/github/rafapra3008/cervellaswarm/blob/main/docs/blog/from-vibecoding-to-vericoding-demo.ipynb)

</div>

## Hosted deployment

A hosted deployment is available on [Fronteir AI](https://fronteir.ai/mcp/rafapra3008-cervellaswarm).

