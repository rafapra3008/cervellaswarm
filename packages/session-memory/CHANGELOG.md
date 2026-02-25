# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-02-19

### Added

- **Project Manager** (`project_manager.py`): Initialize, discover, and manage session memory projects
  - `init_project()`: Create project structure from templates
  - `discover_projects()`: Auto-discover projects in a directory
  - `archive_state()`: Archive old session states with timestamps
  - Template rendering with `{{ placeholder }}` substitution
- **Quality Checker** (`quality_checker.py`): 4-criteria scoring engine for session state files
  - Actionability (30%): TODOs, next steps, action items
  - Specificity (30%): Dates, versions, numbers vs vague terms
  - Freshness (20%): How recently the file was updated
  - Conciseness (20%): Respects configurable line limits
  - All weights and thresholds configurable via YAML
- **Secret Auditor** (`secret_auditor.py`): Regex-based secret detection
  - CRITICAL patterns: API keys (OpenAI, GitHub, Google, Stripe, AWS), private keys
  - HIGH patterns: Password, secret, and token assignments
  - Skip logic for test/mock files, sanitization detection
  - Extensible via config with custom patterns
- **Sync Checker** (`sync_checker.py`): Freshness and coherence verification
  - State file freshness check (configurable thresholds)
  - File size limit enforcement
  - Git uncommitted changes detection
  - Git tracking verification
- **CLI** (`cli.py`): Unified command-line interface
  - `cervella-session init <project>`: Create project structure
  - `cervella-session check [project]`: Quality scoring
  - `cervella-session audit [path]`: Secret scanning
  - `cervella-session sync [project]`: Sync verification
  - `cervella-session list`: List discovered projects
  - All commands support `--json` for machine-readable output
- **Config System** (`config.py`): YAML-based configuration
  - Priority: env var > project `.cervella/session-memory.yaml` > user `~/.claude/session-memory.yaml` > defaults
  - Project registry for multi-project support
  - Configurable quality weights, line limits, secret patterns
- **Templates**: Markdown templates for session state and project compass
  - `session_state.md`: Generalized session state template
  - `project_compass.md`: Project direction and decision tracking

[0.1.0]: https://github.com/rafapra3008/cervellaswarm/releases/tag/session-memory-v0.1.0
