# Changelog

All notable changes to `cervellaswarm-agent-hooks` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-02-18

### Added

- **bash-validator**: PreToolUse hook that blocks destructive commands (rm -rf /, DROP TABLE, fork bombs), asks for confirmation on risky commands (git reset --hard, chmod 777), and auto-fixes `--force` to `--force-with-lease`. 15+ blocked patterns, 10 risky patterns, 19 safe rm targets. Zero dependencies.
- **git-reminder**: Stop hook that sends discreet desktop notifications about uncommitted files. 30-minute cooldown to avoid noise. Cross-platform: macOS (osascript) + Linux (notify-send).
- **file-limits**: SessionEnd hook that warns when files exceed configured line count or file count limits. Configurable via hooks.yaml.
- **context-inject**: SubagentStart hook that automatically injects project facts and session state into all subagents. Config-driven with sensible defaults.
- **session-checkpoint**: SessionEnd/PreCompact hook that auto-saves git status, recent commits, and branch info to a state file.
- **cervella-hooks CLI**: Setup command generates `.cervella/hooks.yaml` config and prints `settings.json` snippet for Claude Code.
- **YAML configuration**: All hooks configurable via `.cervella/hooks.yaml` (project) or `~/.claude/hooks.yaml` (user). Environment variable `CERVELLA_HOOKS_CONFIG` for explicit path.
- **227 tests**, 98% code coverage, runs in 0.12s.

[0.1.0]: https://github.com/rafapra3008/cervellaswarm/releases/tag/agent-hooks-v0.1.0
