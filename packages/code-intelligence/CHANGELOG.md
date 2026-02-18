# Changelog

All notable changes to `cervellaswarm-code-intelligence` will be documented in this file.

This project follows [Semantic Versioning](https://semver.org/).

## [0.1.0] - 2026-02-18

### Added

- Initial release as standalone package (extracted from CervellaSwarm monorepo)
- **Symbol Extraction**: Extract functions, classes, interfaces, and type aliases from Python, TypeScript, and JavaScript
- **Dependency Graph**: Build directed graphs of symbol references with PageRank importance scoring
- **Semantic Search**: Find symbol definitions, callers, callees, and references across codebases
- **Impact Analysis**: Estimate risk of code modifications using PageRank + caller count + type weight
- **Repository Mapping**: Generate concise repository maps within configurable token budgets
- **CLI Tools**: `cervella-search`, `cervella-impact`, `cervella-map`
- 395 tests passing, Apache-2.0 license
