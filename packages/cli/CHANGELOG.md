# Changelog

All notable changes to CervellaSwarm CLI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0-beta.1] - 2026-01-21

### Fixed
- Removed non-existent "main" field from package.json
- Updated tests to reflect 17 agents (was 16)

### Verified
- All 17 agents correctly referenced
- 134/134 tests passing

## [2.0.0-beta] - 2026-01-19

### Added
- Initial beta release
- 8 specialized worker types (backend, frontend, tester, docs, devops, data, security, researcher)
- Full swarm: 17 agents including 3 Guardians (Opus) and Architect
- Task routing system with intelligent agent selection
- SNCP (Sistema Nervoso Centrale Progetto) for project memory
- Session management with resume capability
- MCP server integration

### Features
- `cervellaswarm init` - Initialize project with guided wizard
- `cervellaswarm task` - Execute tasks with automatic agent routing
- `cervellaswarm status` - View project status
- `cervellaswarm resume` - Resume previous sessions
