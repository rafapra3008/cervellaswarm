# CervellaSwarm Code Intelligence

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org)
[![Tests](https://img.shields.io/badge/tests-395%20passed-brightgreen.svg)](tests/)

Find any symbol, trace any dependency, map any repository. Built on [tree-sitter](https://tree-sitter.github.io/).

```bash
pip install cervellaswarm-code-intelligence
```

## What It Does

Extract symbols from source code, build dependency graphs with PageRank scoring,
and answer questions like:

- Where is `UserService` defined?
- What calls `authenticate()`? What does it call?
- How risky is it to refactor `DatabasePool`?
- What are the most important symbols in this repo?

## Quick Start

### Find symbols across your codebase

```python
from cervellaswarm_code_intelligence import SemanticSearch

search = SemanticSearch("/path/to/your/repo")

# Where is this symbol defined?
location = search.find_symbol("UserService")
# => ("/path/to/your/repo/app/services.py", 42)

# Who calls this function?
callers = search.find_callers("authenticate")
# => [("app/auth.py", 15, "login"), ("app/api.py", 88, "verify_token")]

# What does this function call?
callees = search.find_callees("login")
# => ["authenticate", "generate_token", "log_attempt"]
```

### Estimate impact of code changes

```python
from cervellaswarm_code_intelligence import ImpactAnalyzer

analyzer = ImpactAnalyzer("/path/to/your/repo")
result = analyzer.estimate_impact("DatabasePool")

print(result.risk_level)      # => "high"
print(result.risk_score)       # => 0.62
print(result.callers_count)    # => 14
print(result.files_affected)   # => 7
print(result.reasons)
# => ["14 callers - high impact",
#     "Used in 7 files - moderate scope",
#     "Class type - changes may affect multiple methods"]
```

### Generate repository maps within token budgets

```python
from cervellaswarm_code_intelligence import RepoMapper

mapper = RepoMapper("/path/to/your/repo")
repo_map = mapper.build_map(token_budget=2000)
print(repo_map)
# => # REPOSITORY MAP
#
#    ## app/auth.py
#
#    def login(username: str, password: str) -> Token
#    def verify_token(token: str) -> bool
#    class AuthMiddleware
#    ...
```

### Extract symbols from a single file

```python
from cervellaswarm_code_intelligence import SymbolExtractor, TreesitterParser

parser = TreesitterParser()
extractor = SymbolExtractor(parser)

symbols = extractor.extract_symbols("app/models.py")
for symbol in symbols:
    print(f"{symbol.type:10} {symbol.name:20} line {symbol.line}")
# => class      User                 line 5
#    function   create_user          line 28
#    function   get_user_by_email    line 45
```

### Build and analyze dependency graphs

```python
from cervellaswarm_code_intelligence import DependencyGraph, Symbol

graph = DependencyGraph()

# Add symbols and references
graph.add_symbol(login_symbol)
graph.add_symbol(auth_symbol)
graph.add_reference("auth.py:login", "auth.py:verify_credentials")

# Compute importance via PageRank
scores = graph.compute_importance()

# Get the most important symbols
top_10 = graph.get_top_symbols(n=10)
```

## CLI Tools

Three command-line tools are included:

```bash
# Find where a symbol is defined, who calls it, what it calls
cervella-search /path/to/repo UserService
cervella-search /path/to/repo authenticate callers
cervella-search /path/to/repo login callees

# Estimate impact of modifying a symbol
cervella-impact /path/to/repo DatabasePool
# Risk: HIGH (0.62) - 14 callers, 7 files affected

# Generate a repository map within a token budget
cervella-map --repo-path /path/to/repo --budget 2000 --output repo_map.md
cervella-map --repo-path /path/to/repo --filter "**/*.py" --stats
```

## Architecture

```
Source Files (.py, .ts, .tsx, .js, .jsx)
         |
    TreesitterParser        -- Parse into AST
         |
    SymbolExtractor         -- Extract functions, classes, interfaces
    |              |
    PythonExtractor    TypeScriptExtractor
         |
    DependencyGraph         -- Build edges, compute PageRank
         |
    +-----------+-----------+
    |           |           |
SemanticSearch  RepoMapper  ImpactAnalyzer
```

**5 layers, 14 modules, 3 external dependencies.**

## Supported Languages

| Language   | Extensions          | Functions | Classes | Interfaces | Types | References |
|------------|---------------------|-----------|---------|------------|-------|------------|
| Python     | `.py`               | Yes       | Yes     | --         | --    | Yes        |
| TypeScript | `.ts`, `.tsx`       | Yes       | Yes     | Yes        | Yes   | Yes        |
| JavaScript | `.js`, `.jsx`       | Yes       | Yes     | --         | --    | Yes        |

Other languages: contributions welcome. The extractor architecture is designed for
easy addition of new language backends.

## API Reference

### Core Classes

| Class | Purpose | Key Methods |
|-------|---------|-------------|
| `Symbol` | Data class for extracted symbols | `.name`, `.type`, `.file`, `.line`, `.signature`, `.references` |
| `TreesitterParser` | Parse source files into ASTs | `.parse_file(path)`, `.detect_language(path)` |
| `SymbolExtractor` | Extract symbols from parsed files | `.extract_symbols(path)`, `.clear_cache()` |
| `DependencyGraph` | Build and analyze dependency graphs | `.add_symbol()`, `.compute_importance()`, `.get_top_symbols(n)` |
| `SemanticSearch` | High-level code navigation | `.find_symbol()`, `.find_callers()`, `.find_callees()`, `.find_references()` |
| `ImpactAnalyzer` | Risk assessment for code changes | `.estimate_impact(name)`, `.find_dependencies(path)`, `.find_dependents(path)` |
| `RepoMapper` | Generate token-budgeted repo maps | `.build_map(budget)`, `.get_stats()` |

### Risk Score Algorithm

Impact analysis computes risk as: `min(base + caller_factor + type_factor, 1.0)`

| Factor | Range | Source |
|--------|-------|--------|
| `base` | 0.0 - 0.3 | PageRank importance score |
| `caller_factor` | 0.0 - 0.4 | `min(callers / 20, 0.4)` |
| `type_factor` | 0.0 - 0.3 | Symbol type (class=0.3, interface=0.25, function=0.2) |

Risk levels: **low** (< 0.3), **medium** (0.3-0.5), **high** (0.5-0.7), **critical** (> 0.7).

## Limitations

- **Language support**: Python, TypeScript, and JavaScript only. No Go, Rust, Java, C++.
- **Reference extraction**: Based on name matching within AST, not full type resolution.
  This means it can produce false positives for common names.
- **Performance**: Builds a full in-memory index on initialization. For very large
  repositories (10k+ files), the initial scan may take several seconds.
- **Token estimation**: Uses a 4-chars-per-token heuristic, which is approximate.

## Development

```bash
# Clone and install in development mode
git clone https://github.com/rafapra3008/cervellaswarm.git
cd cervellaswarm/packages/code-intelligence
pip install -e ".[dev]"

# Run tests (395 tests, ~0.5s)
pytest

# Run with coverage
pytest --cov=cervellaswarm_code_intelligence --cov-report=term-missing
```

## Part of CervellaSwarm

This package is the code intelligence engine of [CervellaSwarm](https://github.com/rafapra3008/cervellaswarm),
a multi-agent AI coordination system. It works standalone -- no other CervellaSwarm
packages are required.

## License

[Apache-2.0](LICENSE)
