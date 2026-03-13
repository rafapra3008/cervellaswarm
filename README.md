<div align="center">

# CervellaSwarm

**Build AI agent teams that remember.**

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![PyPI Packages](https://img.shields.io/badge/PyPI-9_packages-orange.svg)](https://pypi.org/search/?q=cervellaswarm)
[![Tests: 6612 passing](https://img.shields.io/badge/tests-6612_passing-brightgreen.svg)](packages/)
[![Coverage: 95%](https://img.shields.io/badge/coverage-95%25-brightgreen.svg)](packages/)
[![Claude Code](https://img.shields.io/badge/Claude_Code-native-blueviolet.svg)](https://claude.ai/code)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rafapra3008/cervellaswarm/blob/main/docs/blog/from-vibecoding-to-vericoding-demo.ipynb)

```
   You ──> Queen ──> Architect ──> Workers ──> Guardians ──> Done
                                     |            |
                                  Frontend    Quality ✓
                                  Backend     Security ✓
                                  Tester      Standards ✓
```

*17 specialized AI agents. Persistent memory across sessions. Quality gates built in.*

</div>

---

## The Problem

Your AI coding sessions forget everything when you close the terminal. Context is lost, decisions vanish, and the next session starts from zero.

Single AI assistants also can't specialize. They try to be frontend engineers, security auditors, and architects all at once -- and do none of it well.

**CervellaSwarm fixes both.**

## How It Works

CervellaSwarm is a multi-agent orchestration system for [Claude Code](https://claude.ai/code). Instead of one AI assistant, you get a coordinated team of 17 specialized agents:

```
You: "Refactor the authentication module"

   Queen (orchestrator)
     |
     +-- Architect: creates a 4-phase plan
     +-- Backend: implements the refactored code
     +-- Tester: writes and runs tests
     +-- Guardian: reviews quality before merge
     +-- SNCP: saves everything for next session
```

Three things no other framework does:

| Capability | What it means |
|---|---|
| **Session Continuity** (SNCP) | Your team remembers project state, decisions, and context across sessions. Plain text, git-native, auditable. |
| **Hierarchical Orchestration** | Queen coordinates Guardians who oversee Workers. 3+ levels, not flat. |
| **Hook System** | 16 lifecycle hooks (pre-session, post-commit, file guards, observability). Quality gates are automatic, not optional. |

## Quick Start

```bash
# Clone and install
git clone https://github.com/rafapra3008/cervellaswarm.git
cd cervellaswarm/packages/cli && npm install && npm link

# Initialize in your project
cd ~/your-project
cervellaswarm init

# Give a task to your AI team
cervellaswarm task "add user authentication with OAuth"
```

The Queen automatically routes your task to the right agents, coordinates their work, and has Guardians review the output.

> **Requirements:** macOS or Linux, Node.js >= 18, [Claude Code CLI](https://claude.ai/code), Claude API key

For detailed setup, see the [Getting Started guide](docs/GETTING_STARTED.md).

## The Team

| Role | Agent | What they do |
|---|---|---|
| **Queen** | `cervella-orchestrator` | Coordinates all agents, delegates, decides |
| **Architect** | `cervella-architect` | Plans complex tasks before implementation |
| **Guardian** | `cervella-guardiana-qualita` | Code quality, standards, test coverage |
| **Guardian** | `cervella-guardiana-ops` | Infrastructure, deploy safety, security |
| **Guardian** | `cervella-guardiana-ricerca` | Validates research quality and sources |
| **Worker** | `cervella-frontend` | React, CSS, Tailwind, UI/UX |
| **Worker** | `cervella-backend` | Python, FastAPI, REST APIs |
| **Worker** | `cervella-tester` | Testing, QA, debugging |
| **Worker** | `cervella-data` | SQL, analytics, database design |
| **Worker** | `cervella-security` | Security audits, vulnerability scanning |
| **Worker** | `cervella-devops` | CI/CD, Docker, deployment |
| **Worker** | `cervella-researcher` | Technical research, best practices |
| **Worker** | `cervella-docs` | Documentation, guides, tutorials |
| **Worker** | `cervella-marketing` | UX strategy, copywriting |
| **Worker** | `cervella-ingegnera` | Architecture analysis, refactoring |
| **Worker** | `cervella-scienziata` | Market research, competitor analysis |
| **Worker** | `cervella-reviewer` | Code review, best practices |

Guardians and critical analysts run on Claude Opus for deeper reasoning. Most Workers run on Claude Sonnet for speed. The Queen decides who works on what.

See [Agents Reference](docs/AGENTS_REFERENCE.md) for detailed capabilities and examples.

## Packages

All packages are on [PyPI](https://pypi.org/search/?q=cervellaswarm) -- install what you need:

| Package | What it does | Install |
|---|---|---|
| **[lingua-universale](packages/lingua-universale/)** | Session types & formal verification for AI agents. The core. | `pip install cervellaswarm-lingua-universale` |
| **[code-intelligence](packages/code-intelligence/)** | AST-powered code understanding (tree-sitter, PageRank) | `pip install cervellaswarm-code-intelligence` |
| **[agent-hooks](packages/agent-hooks/)** | Lifecycle hooks for Claude Code agents | `pip install cervellaswarm-agent-hooks` |
| **[agent-templates](packages/agent-templates/)** | Agent definition templates & team configuration | `pip install cervellaswarm-agent-templates` |
| **[task-orchestration](packages/task-orchestration/)** | Deterministic task routing & validation | `pip install cervellaswarm-task-orchestration` |
| **[spawn-workers](packages/spawn-workers/)** | Multi-agent process management (tmux/nohup) | `pip install cervellaswarm-spawn-workers` |
| **[session-memory](packages/session-memory/)** | Persistent session context across conversations | `pip install cervellaswarm-session-memory` |
| **[event-store](packages/event-store/)** | Immutable event logging & audit trail | `pip install cervellaswarm-event-store` |
| **[quality-gates](packages/quality-gates/)** | Automated quality checks & scoring | `pip install cervellaswarm-quality-gates` |

Every package: Apache 2.0, Python 3.10+, tested, documented, zero or minimal dependencies.

> **The crown jewel:** To our knowledge, `lingua-universale` is the first session type system for AI agent communication in Python. 29 modules, 3436 tests, ZERO external dependencies. [Try it in your browser](https://rafapra3008.github.io/cervellaswarm/) or [read the vision](packages/lingua-universale/NORD.md).

## Try It Now

```bash
pip install cervellaswarm-lingua-universale
```

```python
from cervellaswarm_lingua_universale import (
    Protocol, ProtocolStep, MessageKind, SessionChecker, TaskResult, TaskStatus,
)

# Define a protocol: who sends what, to whom, in what order
review = Protocol(name="Review", roles=("dev", "reviewer"), elements=(
    ProtocolStep(sender="dev", receiver="reviewer", message_kind=MessageKind.TASK_RESULT),
))

# The checker enforces it at runtime
checker = SessionChecker(review)
checker.send("dev", "reviewer", TaskResult(task_id="1", status=TaskStatus.OK, summary="Done"))
# Wrong sender/receiver/order? -> ProtocolViolation raised immediately
```

**[Try it in your browser](https://rafapra3008.github.io/cervellaswarm/)** -- no install needed, runs via Pyodide (Python in WebAssembly).

Or try the **[interactive Colab notebook](https://colab.research.google.com/github/rafapra3008/cervellaswarm/blob/main/docs/blog/from-vibecoding-to-vericoding-demo.ipynb)** -- 2 minutes, zero setup, 9 features demoed live.

## Key Features

### SNCP -- Persistent Memory

Your AI team remembers across sessions. No more re-explaining your project.

```
Session 1: "We decided to use JWT for auth because..."
  [session ends]
Session 2: Queen loads context -> knows the JWT decision -> continues from there
```

SNCP stores project state as plain markdown files in your repo. Git-native, human-readable, auditable. No databases, no cloud services, no vendor lock-in.

### Automatic Quality Gates

Three Guardian agents review every significant change:

- **Quality Guardian** -- checks code standards, test coverage, architectural consistency
- **Ops Guardian** -- validates infrastructure, security, deploy safety
- **Research Guardian** -- verifies sources and methodology for research tasks

Work doesn't ship until Guardians approve. Like having senior reviewers on every PR, but AI.

### Parallel Execution

Multiple agents work simultaneously:

```bash
cervellaswarm task "Build a dashboard with user analytics"

# Queen spawns in parallel:
#   Frontend: React components + Tailwind styling
#   Backend: FastAPI endpoints + SQL queries
#   Tester: writes tests as code is produced
#   Guardian: reviews completed modules
```

### Intelligent Task Routing

The Architect agent classifies task complexity and routes automatically:

- **Simple tasks** (typo fix, small change) -> direct to Worker
- **Medium tasks** (new endpoint, component) -> Worker + Guardian review
- **Complex tasks** (new feature, refactor) -> Architect plan -> Workers -> Guardian audit

### Code Intelligence (AST Pipeline)

Built-in tree-sitter powered code understanding:

- `find_symbol("UserAuth")` -- locate any symbol across languages
- `find_callers("validate_token")` -- who calls this function?
- `estimate_impact("auth.py")` -- risk score before you refactor
- Supports Python, TypeScript, JavaScript

## Why CervellaSwarm?

| Feature | CervellaSwarm | AutoGen | CrewAI | LangGraph |
|---|:---:|:---:|:---:|:---:|
| Session memory (native) | **SNCP 4.0** | -- | -- | -- |
| Agent hierarchy (3+ levels) | **Queen/Guardian/Worker** | Basic | Basic | Manual |
| Hook system (lifecycle events) | **16 hooks** | -- | -- | -- |
| Quality gates (built-in review) | **3 Guardians** | -- | -- | -- |
| Claude Code native | **Yes** | -- | -- | -- |
| Code intelligence (AST) | **Tree-sitter** | -- | -- | -- |
| Multi-LLM support | Claude only* | Multi | Multi | Multi |
| Ecosystem size | Growing | Large | Large | Large |

*Multi-LLM adapter is planned. CervellaSwarm is Claude-first, not Claude-only.

> **Honest note:** AutoGen, CrewAI, and LangGraph have larger ecosystems and multi-LLM support today. CervellaSwarm's edge is session continuity, hierarchical quality control, and deep Claude Code integration. Choose what fits your workflow.

## Documentation

| Guide | Description |
|---|---|
| [Getting Started](docs/GETTING_STARTED.md) | Full setup tutorial (prerequisites to first task) |
| [Agents Reference](docs/AGENTS_REFERENCE.md) | All 17 agents: capabilities, when to use, examples |
| [SNCP Guide](docs/SNCP_GUIDE.md) | Session memory system explained |
| [Architecture](docs/ARCHITECTURE.md) | System design, task flow, integrations |
| [Semantic Search](docs/SEMANTIC_SEARCH.md) | Code intelligence API reference |
| [Architect Pattern](docs/ARCHITECT_PATTERN.md) | AI planning before implementation |
| [Git Attribution](docs/GIT_ATTRIBUTION.md) | Multi-agent commit tracking |

## Battle-Tested

```
442+ sessions of daily use since December 2025
6,612 tests passing across 9 packages (95%+ coverage)
17 agents used daily across real production codebases
9 packages published on PyPI, all Apache 2.0
Built before multi-agent was a buzzword
```

This isn't a demo project. CervellaSwarm has been our daily development tool since December 2025, managing real codebases with real deadlines.

## Project Structure

```
packages/
  lingua-universale/   # Session types & formal verification (Python, PyPI)
  code-intelligence/   # AST pipeline & semantic search (Python, PyPI)
  agent-hooks/         # Lifecycle hook system (Python, PyPI)
  agent-templates/     # Agent & team definitions (Python, PyPI)
  task-orchestration/  # Task routing & validation (Python, PyPI)
  spawn-workers/       # Process management (Python, PyPI)
  session-memory/      # Persistent context (Python, PyPI)
  event-store/         # Event logging (Python, PyPI)
  quality-gates/       # Quality scoring (Python, PyPI)
  core/                # Core library (Node.js)
  cli/                 # CLI tool (Node.js)
  mcp-server/          # MCP integration (Node.js)
scripts/
  swarm/               # Agent orchestration
  utils/               # Internal utilities
tests/                 # Integration tests (pytest)
docs/                  # Documentation
```

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

- **Bug reports:** [GitHub Issues](https://github.com/rafapra3008/cervellaswarm/issues)
- **Security:** See [SECURITY.md](SECURITY.md) for responsible disclosure
- **Code of Conduct:** [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

## License

Apache License 2.0 -- see [LICENSE](LICENSE) for full text.

Copyright 2025-2026 CervellaSwarm Contributors.

---

<div align="center">

**CervellaSwarm** -- *17 brains are better than one.*

[Getting Started](docs/GETTING_STARTED.md) | [Documentation](docs/) | [Playground](https://rafapra3008.github.io/cervellaswarm/) | [Blog: From Vibecoding to Vericoding](docs/blog/from-vibecoding-to-vericoding.md) | [Colab Demo](https://colab.research.google.com/github/rafapra3008/cervellaswarm/blob/main/docs/blog/from-vibecoding-to-vericoding-demo.ipynb) | [Contributing](CONTRIBUTING.md)

</div>
