# CHANGELOG - CervellaSwarm

All notable changes to CervellaSwarm.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
adhering to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Changed
- **Config alignment**: All 4 Python config packages (quality-gates, session-memory, event-store, agent-hooks) aligned on deep merge, consistent API (`config_path` param, `_deep_merge`). `dict(DEFAULTS)` bug fixed in agent-hooks (S509).
- **Dep version align**: CLI `@anthropic-ai/sdk` ^0.39->^0.81 (match Core). `conf` dep removed from CLI (comes via Core) (S509).
- **loader.py exception handling**: `except Exception` -> specific exceptions + `logging.warning`. Dict guard for empty/scalar YAML (S509).
- **event-store broad except**: `(OSError, Exception)` -> `(OSError, ValueError, YAMLError)` with proper `_YAML_ERRORS` tuple (S509).
- **Ruff codebase-wide**: 861 lint violations fixed (import sort, whitespace, f-strings, unused vars). Root config in pyproject.toml. 2 structural residuals.
- **UTC datetime standardization**: ~28 source files migrated from `datetime.now()` to `datetime.now(tz=timezone.utc)`. DST risk eliminated.
- **B904 raise-from**: 10 fix across cervella/cli + LU. Proper exception chaining.
- **CI Node.js matrix**: 18.x/20.x -> 20.x/22.x (Node 18 EOL). `fail-fast: false` added (S508).
- **DRY config CLI->Core**: CLI imports shared config from `@cervellaswarm/core/config` instead of local duplicates (-329 LOC) (S508).

### Added
- **+131 tests scripts/common/**: colors (33), paths (37), db (61) -- test coverage for most-imported shared modules (S509).
- **+10 config tests**: deep merge, config_path param tests across 3 packages (S509).
- **14 hardtest failures fixed**: S504 (10) + S498 (4) updated for monkeypatch, UTC, allowlist API (S509).
- **+202 tests** across packages (S505 +155, S506 +47). Total: 9744.
- **+194 JS tests** for packages/cli + packages/core (S508). CLI: 134->291, Core: 82->119. Total: 10,213.
- `create_auto_pr.py`: 47 tests (was 0 for 360 LOC).
- `memory_validator`: O(1) file index with PermissionError guard.
- Il Sogno v2.5.0: atomic lock eviction via `os.rename`.
- `patch-claude-sandbox-tls.py`: fix for gh CLI TLS in Claude Code sandbox.
- Subprocess timeout on all 20 `subprocess.run()` calls (S507).
- DRY `_utils.py` for agent-hooks: `find_project_root` shared across 3 modules (S507).
- Pre-commit ruff lint check (warning, non-blocking) (S507).
- `pytest-rerunfailures` for flaky test detection in CI (S507).
- Bandit SAST security scan in CI (continue-on-error) (S507).
- 3 new hook events: TaskCreated, TaskCompleted, StopFailure (S508).
- DRY `findSncpDir` JS: 2 copies -> 1 in `sncp/utils.js` (S508).
- DRY `extractFilesFromOutput`: CLI uses `@cervellaswarm/core/workers` (S508).
- `test:coverage` script for packages/core (S508).

### Fixed
- 2 HIGH security fixes (S505): connection leak, unvalidated input.
- 5 P1 fixes (S505): 0 warnings achieved.
- Il Sogno lock race condition (S506): atomic rename replaces unlink+retry.
- CI `--ignore=E501,E402` redundancy removed (S507).
- Bandit SAST: 2 TRUE POSITIVE fixed (SQL f-string -> allowlist dict), 52->0 MEDIUM (S508).
- `billing.js` falsy check: `if (data.tier)` -> `if (data.tier !== undefined)` (S508).

### Removed
- **SubagentStop double firing**: removed duplicate project-level hook wiring. Global hook updated with UTC (S509).
- **Dead `_merge_config`**: removed from session-memory config (replaced by `_deep_merge`) (S509).
- **Stale `config/claude-hooks/`**: 812 LOC dead archived code eliminated from disk (S509).
- 395 LOC dead code (S505): unused imports, unreachable branches, stale utilities.
- 12 LOC duplicate `find_project_root` across 3 files (S507).
- 375 LOC duplicated code (S508): config CLI->Core dedup (-329), findSncpDir (-20), extractFiles (-26).

---

## [0.1.0] - 2026-02-25

First open source release of the CervellaSwarm Python package suite. 9 packages on PyPI.

### Added

**Lingua Universale** -- Session types & formal verification for AI agents
- 14 modules: types, protocols, checker, dsl, monitor, lean4_bridge, integration, confidence, trust, codegen, intent, spec, errors (+ showcase example)
- Session type system: typed protocols with runtime checking (first in Python for AI)
- DSL notation: Scribble-inspired `sender -> receiver : MessageKind;` syntax with parser + renderer
- Lean 4 bridge: Python protocols to Lean 4 formal proofs (7 verification properties)
- Confidence types: `Confident[T]` with composition strategies (min, product, average)
- Trust composition: 4-tier trust model with transitive composition (Subjective Logic)
- Code generation: Protocol -> typed Python classes with runtime enforcement
- Intent parser: structured micro-language for protocol definitions
- Specification language: 7 formal properties (always_terminates, no_deadlock, confidence_min, etc.)
- Error messages: Elm/Rust-style user-friendly errors, 35 codes, 3 locales (en, it, pt)
- 1,820 tests, 98% coverage, ZERO external dependencies

**Code Intelligence** -- AST-powered code understanding
- Tree-sitter parser for Python, TypeScript, JavaScript
- Symbol extraction, dependency graph (PageRank), semantic search
- Impact analysis with risk scoring
- 399 tests, 3 CLI tools (`cervella-search`, `cervella-impact`, `cervella-map`)

**Agent Hooks** -- Lifecycle hooks for Claude Code agents
- Bash validator, git reminder, file limits guard, context injector, session checkpoint
- YAML configuration with project/user/env override
- 236 tests, 5 CLI tools

**Agent Templates** -- Agent definition templates & team configuration
- 4 base templates + 7 worker specialties + team.yaml format
- Enhanced frontmatter: role, permissionMode, maxTurns, disallowedTools
- 192 tests, 1 CLI tool (`cervella-agent`)

**Task Orchestration** -- Deterministic task routing & validation
- Rule-based task classification (unique: 0/5 competitors have deterministic routing)
- Plan validation, output validation, atomic race protection
- 305 tests, 6 CLI tools, ZERO dependencies

**Spawn Workers** -- Multi-agent process management
- tmux/nohup backend auto-detection
- Signal handling (SIGINT/SIGTERM), cross-invocation tracking
- team.yaml integration for team-level spawning
- 191 tests, 1 CLI tool (`cervella-spawn`)

**Session Memory** -- Persistent session context
- Template-based session snapshots with rotation
- Project detection and auto-save
- 193 tests

**Event Store** -- Immutable event logging & audit trail
- Schema-validated events with freezing
- Query API with filtering and aggregation
- 249 tests, ZERO runtime dependencies

**Quality Gates** -- Automated quality checks & scoring
- Multi-gate validation with configurable thresholds
- Score composition and reporting
- 206 tests

**Open Source Infrastructure**
- CI/CD: GitHub Actions per-package workflows with reusable build template
- PyPI: Trusted Publishers (OIDC) -- zero secrets, zero API tokens
- Dual repo strategy: private development + public releases with content scanning
- Security: 6-layer content scanner (v3.2.0) blocks private paths, emails, project names
- .github/: issue templates, PR template, dependabot, CODEOWNERS, FUNDING

---

## Node.js CLI/MCP Releases (legacy)

The following releases predate the Python package suite and refer to the Node.js CLI and MCP server components.

## [2.0.0-beta] - 2026-01-19

Major release with semantic code understanding, intelligent planning, and improved reliability.

### Added

**W1: Git Flow 2.0** - Worker Attribution System
- `git_worker_commit.sh` v1.2.2 (720 lines) - Automated commit attribution
- Worker attribution for all 16 agents with signature tracking
- Auto-commit support in spawn-workers.sh v3.6.0
- `auto_detect_type()` - Intelligent commit type suggestion from file changes
- 13 scope patterns for conventional commits
- Dual remote setup (private development + public releases)
- `docs/GIT_ATTRIBUTION.md` - Complete documentation

**W2: Tree-sitter Integration** - AST-based Code Understanding
- `treesitter_parser.py` (365 lines) - Multi-language AST parsing
- `symbol_extractor.py` (486 lines) - Symbol extraction with type info
- `dependency_graph.py` (451 lines) - PageRank-based importance ranking
- `repo_mapper.py` (571 lines) - Repository-wide mapping
- `generate_worker_context.py` (147 lines) - Smart context generation
- Reference extraction for Python and TypeScript
- spawn-workers.sh v3.7.0 with `--with-context` flag
- 142 tests in test suite for tree-sitter components

**W3-A: Semantic Search API** - Intelligent Code Navigation
- `semantic_search.py` - Core semantic API with:
  - `find_symbol(name)` - Locate symbol definitions
  - `find_callers(symbol)` - Find all callers of a function/class
  - `find_callees(symbol)` - Find all functions called by a symbol
  - `find_references(symbol)` - Find all usages
- `impact_analyzer.py` - Risk assessment with:
  - `estimate_impact(symbol)` - Risk score for modifications
  - `find_dependencies(file)` - File dependency tracking
  - `find_dependents(file)` - Reverse dependency tracking
- 25 semantic search tests passing
- `docs/SEMANTIC_SEARCH.md` (778 lines) - Complete API documentation

**W3-B: Architect Pattern** - AI Planning Before Implementation
- `cervella-architect.md` (259 lines) - Opus-powered planning agent
- `PLAN_TEMPLATE.md` (150 lines) - Structured 4-phase planning template
- `task_classifier.py` (280 lines) - Intelligent task complexity detection
- `architect_flow.py` (525 lines) - Planning workflow orchestration
- Automatic routing: complex tasks -> architect, simple tasks -> direct
- Fallback logic after 2 rejected plans
- 85 hardtests passing
- `docs/ARCHITECT_PATTERN.md` (282 lines) - Pattern documentation

**W4: Polish & Reliability**
- Centralized database connection (`scripts/common/db.py`)
- Centralized ANSI colors (`scripts/common/colors.py`)
- Centralized config constants (`scripts/common/config.py`)
- pytest-cov integration with 41% baseline coverage
- GitHub Actions CI for Python (matrix: 3.10, 3.11, 3.12)
- 241 tests passing across the codebase

### Breaking Changes

- `spawn-workers.sh` API changed: new `--with-context` flag required for auto-context
- Git commit workflow now requires `worker_attribution.json` configuration
- Minimum Node.js version: 18.0.0

### Changed

- spawn-workers.sh upgraded to v3.7.0 with auto-context
- Worker prompts updated with semantic search commands
- Test infrastructure migrated to pytest with coverage reporting
- Code deduplication: connect_db() centralized (was in 4 files)
- ANSI color definitions centralized (was in 3 files)

### Fixed

- PageRank now orders files by actual importance (was alphabetical)
- Reference extraction for Python builtins filtering
- Staged changes preservation in git operations (--soft vs --hard)

### Technical

- Tree-sitter queries for 3 languages (Python, TypeScript, JavaScript)
- 152x speedup with reference caching
- Risk score algorithm based on dependent count and change frequency

---

## [0.2.3] - 2026-01-19

### Fixed
- npm package homepage and repository URLs corrected
- Show HN commands verified (`npx cervellaswarm init/task`)

---

## [0.1.2] - 2026-01-18

### Added
- Initial public release on npm
- CLI: `cervellaswarm` and `cs` commands
- MCP Server: `@cervellaswarm/mcp-server`
- 16 specialized AI agents
- spawn-workers command
- swarm-status health checks

---

## Schema Versioning

```
MAJOR.MINOR.PATCH

MAJOR: Breaking changes (e.g., API changes)
MINOR: New backward-compatible features
PATCH: Backward-compatible bug fixes
```

---

**Legend:**
- `Added`: New features
- `Changed`: Changes to existing features
- `Deprecated`: Features to be removed
- `Removed`: Removed features
- `Fixed`: Bug fixes
- `Security`: Security fixes
- `Technical`: Implementation details

---

*Last updated: 2026-02-25*
*Format: Keep a Changelog 1.0.0*
