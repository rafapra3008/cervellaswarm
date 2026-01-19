# CHANGELOG - CervellaSwarm

All notable changes to CervellaSwarm.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
adhering to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

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

- Tree-sitter queries for 5 languages (Python, TypeScript, JavaScript, Go, Rust)
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

*Last updated: 2026-01-19*
*Format: Keep a Changelog 1.0.0*
