# CervellaSwarm Code Intelligence

AST-based code analysis toolkit for Python, TypeScript, and JavaScript.

## Features

- **Symbol Extraction** - Extract functions, classes, interfaces from source code
- **Dependency Graph** - Build directed graphs of symbol dependencies with PageRank scoring
- **Semantic Search** - Find symbols, callers, callees, and references across codebases
- **Impact Analysis** - Estimate risk of code modifications
- **Repository Mapping** - Generate concise repo maps within token budgets

## Installation

```bash
pip install cervellaswarm-code-intelligence
```

## Quick Start

```python
from cervellaswarm_code_intelligence import SemanticSearch

search = SemanticSearch("/path/to/repo")
location = search.find_symbol("MyClass")
callers = search.find_callers("my_function")
```

## CLI Tools

```bash
cervella-search /path/to/repo MyClass
cervella-impact /path/to/repo UserService
cervella-map /path/to/repo --budget 2000
```

## License

Apache-2.0
