# Changelog

All notable changes to `cervellaswarm-quality-gates` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-02-24

### Added
- Initial release
- `score_content` with 4-dimension quality scoring (actionability, specificity, freshness, conciseness)
- Configurable weights via YAML config (project `.cervella/` > user `~/.claude/` > env var)
- `validate_hooks` with 5 hook statuses (OK, BROKEN, DISABLED, NOT_EXEC, MISSING)
- Shebang validation and executable permission checks
- `compare_agents` for directory diff between agent definition dirs
- `SyncReport` with only_in_source, only_in_target, differing, identical sets
- `cervella-check` CLI: quality, hooks, sync, all subcommands
- `--json` flag on all commands for machine-readable output
- `--project-dir` option for all-in-one validation
- ZERO runtime dependencies (stdlib only: pathlib, json, argparse, configparser)
- 200+ tests with comprehensive edge case coverage

[0.1.0]: https://github.com/rafapra3008/cervellaswarm/releases/tag/quality-gates-v0.1.0
