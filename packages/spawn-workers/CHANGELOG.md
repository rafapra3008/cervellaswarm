# Changelog

All notable changes to `cervellaswarm-spawn-workers` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-02-18

### Added

- `SpawnManager` class for worker lifecycle management (spawn, monitor, kill, cleanup)
- tmux backend with detached sessions and remain-on-exit
- nohup backend as universal fallback
- Auto-detection of best available backend via `shutil.which("tmux")`
- `team.yaml` config loader compatible with cervellaswarm-agent-templates
- Worker prompt generation with 10 specialties
- Signal handling (SIGINT/SIGTERM) with graceful shutdown
- `cervella-spawn` CLI with --team, --worker, --status, --kill, --list commands
- File-based state tracking (.ready/.working/.done markers)
- Worker health checks with uptime monitoring
- PID/session tracking files in status directory

[0.1.0]: https://github.com/rafapra3008/cervellaswarm/releases/tag/spawn-workers-v0.1.0
