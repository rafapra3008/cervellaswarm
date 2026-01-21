# Changelog

All notable changes to CervellaSwarm MCP Server will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0-beta.1] - 2026-01-21

### Fixed
- Rebuilt dist/ to sync with source code
- All 17 agents now correctly available

### Verified
- Server starts correctly
- All workers respond properly

## [2.0.0-beta] - 2026-01-19

### Added
- Initial beta release
- MCP server for Claude Code integration
- 8 specialized workers accessible via MCP tools:
  - `spawn_worker` - Spawn a specialized agent
  - `list_workers` - List available workers
  - `check_status` - Check server configuration
  - `check_usage` - Check API usage and quotas

### Features
- Seamless integration with Claude Code
- API key configuration support
- Usage tracking and quota management
