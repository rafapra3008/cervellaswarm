# Python Standalone Package - Packaging Best Practices 2026

**Status**: COMPLETA
**Fonti**: 12 consultate (PyPA docs, PEP 639, uv docs, pyopensci, Real Python, inventivehq, astral.sh, medium, packaging.python.org)
**Data**: 2026-02-18
**Target**: `cervellaswarm-code-intelligence` - PyPI standalone package

---

## Sintesi Executive

- **Build backend**: Hatchling (non setuptools, non uv_build per ora)
- **Layout**: src/ layout - standard de facto 2026 per packages pubblicati
- **License**: PEP 639 in vigore - `license = "Apache-2.0"` + `license-files`
- **Publish**: `python -m build` + Trusted Publishing OIDC (non twine + token)
- **Tests**: conftest.py gerarchico, pytest config in pyproject.toml, NO `__init__.py` in tests/

---

## 1. Build Backend: Hatchling (Raccomandato)

### Confronto 2025-2026

| Backend | Caso d'uso | Popolarita | Note |
|---------|-----------|------------|------|
| **hatchling** | Pure Python, CLI tools | 8.1k packages | Default PyPA guide, PyPA umbrella |
| uv_build | Pure Python, zero-config | Stabile da Jul 2025 | 10-35x piu veloce ma nuovissimo |
| setuptools>=77 | C extensions, legacy | 50k packages | Richiesto solo per extensions |
| flit | Librerie semplici | 3.8% market | No versioning, no env mgmt |

**Decisione per cervellaswarm-code-intelligence**: **Hatchling**

Motivi:
- tree-sitter usa bindings C -> potremmo avere future C extensions
- Hatchling supporta build hooks (utile se aggiungiamo extensions)
- E' il backend raccomandato dalla PyPA documentation ufficiale
- uv_build e stabilissimo ma ancora giovane (luglio 2025), meglio hatchling per il first public package
- Setuptools: troppo verboso, richiede `[tool.setuptools]` config extra

```toml
[build-system]
requires = ["hatchling>=1.26"]
build-backend = "hatchling.build"
```

---

## 2. Layout: src/ (Standard 2026)

### Struttura Raccomandata

```
cervellaswarm-code-intelligence/
├── src/
│   └── cervellaswarm_code_intelligence/     # underscore per Python module
│       ├── __init__.py                       # public API exports
│       ├── parser/
│       │   ├── __init__.py
│       │   └── treesitter_parser.py
│       ├── extractors/
│       │   ├── __init__.py
│       │   ├── symbol_extractor.py
│       │   ├── python_extractor.py
│       │   └── typescript_extractor.py
│       ├── graph/
│       │   ├── __init__.py
│       │   ├── dependency_graph.py
│       │   └── symbol_cache.py
│       ├── search/
│       │   ├── __init__.py
│       │   └── semantic_search.py
│       ├── analysis/
│       │   ├── __init__.py
│       │   └── impact_analyzer.py
│       ├── mapping/
│       │   ├── __init__.py
│       │   └── repo_mapper.py
│       ├── cli/
│       │   ├── __init__.py
│       │   ├── search_cmd.py      # cervella-search
│       │   ├── impact_cmd.py      # cervella-impact
│       │   └── map_cmd.py         # cervella-map
│       └── _types.py              # shared types
├── tests/
│   ├── conftest.py                # root fixtures
│   ├── parser/
│   │   ├── conftest.py            # parser-specific fixtures
│   │   └── test_treesitter_parser.py
│   ├── extractors/
│   │   ├── conftest.py
│   │   └── test_symbol_extractor.py
│   ├── graph/
│   │   └── test_dependency_graph.py
│   ├── search/
│   │   └── test_semantic_search.py
│   ├── analysis/
│   │   └── test_impact_analyzer.py
│   └── mapping/
│       └── test_repo_mapper.py
├── docs/
│   └── index.md
├── LICENSE                        # Apache 2.0 full text
├── NOTICE                         # Attribution notices (REQUIRED per Apache 2.0)
├── README.md
├── CHANGELOG.md
└── pyproject.toml
```

### Perche src/ e non flat?

- **Previene import accidentali**: senza src/, `import cervellaswarm_code_intelligence` in tests usa i file locali invece del package installato
- **Forza installazione corretta**: `pip install -e .` garantisce che tests usino il package reale
- **Standard PyPA 2026**: tutte le guide ufficiali lo raccomandano
- **Tests NON inclusi nel wheel**: riduce dimensione package distribuito

### __init__.py con Public API

```python
# src/cervellaswarm_code_intelligence/__init__.py
"""CervellaSwarm Code Intelligence - AST-based code analysis toolkit."""

__version__ = "0.1.0"
__all__ = [
    # Core classes
    "TreesitterParser",
    "SymbolExtractor",
    "DependencyGraph",
    "SemanticSearch",
    "ImpactAnalyzer",
    "RepoMapper",
    # Types
    "Symbol",
    "SymbolType",
]

# Lazy imports to avoid loading heavy tree-sitter deps unless needed
from cervellaswarm_code_intelligence.parser.treesitter_parser import TreesitterParser
from cervellaswarm_code_intelligence.extractors.symbol_extractor import SymbolExtractor
from cervellaswarm_code_intelligence.graph.dependency_graph import DependencyGraph
from cervellaswarm_code_intelligence.search.semantic_search import SemanticSearch
from cervellaswarm_code_intelligence.analysis.impact_analyzer import ImpactAnalyzer
from cervellaswarm_code_intelligence.mapping.repo_mapper import RepoMapper
from cervellaswarm_code_intelligence._types import Symbol, SymbolType
```

---

## 3. pyproject.toml Completo (PEP 639 + 2026 Standards)

```toml
# =============================================================================
# CervellaSwarm Code Intelligence
# SPDX-License-Identifier: Apache-2.0
# =============================================================================

[build-system]
requires = ["hatchling>=1.26"]
build-backend = "hatchling.build"

# -----------------------------------------------------------------------------
# Project Metadata (PEP 621 + PEP 639)
# -----------------------------------------------------------------------------
[project]
name = "cervellaswarm-code-intelligence"
version = "0.1.0"
description = "AST-based code analysis toolkit: symbol extraction, dependency graphs, semantic search"
readme = "README.md"

# PEP 639: SPDX string (NOT table format - that's deprecated since setuptools 77)
license = "Apache-2.0"
license-files = ["LICENSE", "NOTICE"]

requires-python = ">=3.10"
authors = [
    {name = "CervellaSwarm Contributors"},
]
keywords = [
    "ast",
    "code-analysis",
    "tree-sitter",
    "symbol-extraction",
    "dependency-graph",
    "semantic-search",
    "impact-analysis",
]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Software Development :: Quality Assurance",
    "Typing :: Typed",
]

# Core runtime dependencies (minimal - no anthropic, no click bloat)
dependencies = [
    "tree-sitter>=0.23.0",
    "tree-sitter-language-pack>=0.3.0",
    "networkx>=3.0",        # dependency graphs
    "pyyaml>=6.0",
]

# -----------------------------------------------------------------------------
# Entry Points (CLI commands)
# -----------------------------------------------------------------------------
[project.scripts]
cervella-search = "cervellaswarm_code_intelligence.cli.search_cmd:main"
cervella-impact = "cervellaswarm_code_intelligence.cli.impact_cmd:main"
cervella-map    = "cervellaswarm_code_intelligence.cli.map_cmd:main"

# -----------------------------------------------------------------------------
# Project URLs
# -----------------------------------------------------------------------------
[project.urls]
Homepage      = "https://github.com/rafapra3008/cervellaswarm"
Repository    = "https://github.com/rafapra3008/cervellaswarm"
Documentation = "https://github.com/rafapra3008/cervellaswarm/tree/main/docs"
"Bug Tracker" = "https://github.com/rafapra3008/cervellaswarm/issues"
Changelog     = "https://github.com/rafapra3008/cervellaswarm/blob/main/CHANGELOG.md"

# -----------------------------------------------------------------------------
# Optional Dependencies Groups
# -----------------------------------------------------------------------------
[project.optional-dependencies]
# Developer tools
dev = [
    "pytest>=8.0",
    "pytest-cov>=5.0",
    "ruff>=0.9.0",
    "mypy>=1.0",
]
# Testing only (subset of dev, useful for CI)
test = [
    "pytest>=8.0",
    "pytest-cov>=5.0",
]
# Type stubs
typing = [
    "types-PyYAML",
    "types-networkx",
]
# Everything
all = [
    "cervellaswarm-code-intelligence[dev,typing]",
]

# -----------------------------------------------------------------------------
# Hatchling Build Config
# -----------------------------------------------------------------------------
[tool.hatch.build.targets.wheel]
packages = ["src/cervellaswarm_code_intelligence"]

[tool.hatch.build.targets.sdist]
include = [
    "src/",
    "tests/",
    "LICENSE",
    "NOTICE",
    "README.md",
    "CHANGELOG.md",
    "pyproject.toml",
]

# -----------------------------------------------------------------------------
# Pytest Configuration
# -----------------------------------------------------------------------------
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]         # KEY: src layout requires this!
addopts = [
    "--tb=short",
    "-q",
]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests requiring real files",
    "unit: marks tests as pure unit tests",
]

# -----------------------------------------------------------------------------
# Coverage
# -----------------------------------------------------------------------------
[tool.coverage.run]
source = ["cervellaswarm_code_intelligence"]
omit = [
    "*/tests/*",
    "*/__main__.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
]
precision = 2
show_missing = true

# -----------------------------------------------------------------------------
# Ruff (linter + formatter)
# -----------------------------------------------------------------------------
[tool.ruff]
line-length = 100
target-version = "py310"
src = ["src"]           # tells ruff where packages live

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "C4", "ANN"]
ignore = ["ANN101", "ANN102"]  # self/cls annotations

# -----------------------------------------------------------------------------
# Mypy
# -----------------------------------------------------------------------------
[tool.mypy]
python_version = "3.10"
strict = true
mypy_path = "src"
```

---

## 4. Apache 2.0 - File Richiesti

### File Obbligatori

| File | Contenuto | Obbligatorio? |
|------|-----------|---------------|
| `LICENSE` | Full Apache 2.0 text | SI - sempre |
| `NOTICE` | Attribution notices | SI - se distribuisci derivative work |
| Header SPDX nei file | `# SPDX-License-Identifier: Apache-2.0` | Raccomandato (REUSE standard) |

### NOTICE File (Template)

```
CervellaSwarm Code Intelligence
Copyright 2026 CervellaSwarm Contributors

This product includes software developed at:
https://github.com/rafapra3008/cervellaswarm

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at:

    http://www.apache.org/licenses/LICENSE-2.0
```

### Header SPDX nei File Sorgenti

```python
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors
"""Module docstring here..."""
```

Nota: SPDX header non e' legalmente obbligatorio, ma e' lo standard de facto
nel 2026 (adottato da Apache, Google, Linux Foundation). Facilita license scanning
automatico (REUSE initiative, FOSSA, Snyk).

---

## 5. Tests - Struttura Standalone

### Problemi da Monorepo che SPARISCONO con src/ layout

Nel monorepo attuale, tests/ vivono accanto a scripts/ e ci sono problemi di
shadowing degli imports (documentato in MEMORY.md). Con il package standalone:

- **src/ layout risolve il shadowing**: `import cervellaswarm_code_intelligence` e' inequivocabile
- **NO `__init__.py` in tests/**: pytest usa importmode=importlib di default ora
- **Ogni subdirectory tests/ ha il suo conftest.py** per fixtures locali

### conftest.py Pattern

```python
# tests/conftest.py (root - fixtures globali)
"""Shared test fixtures for cervellaswarm-code-intelligence."""

import pytest
from pathlib import Path


@pytest.fixture(scope="session")
def repo_root(tmp_path_factory):
    """Session-scoped temp repo for integration tests."""
    root = tmp_path_factory.mktemp("test_repo")
    # Create minimal realistic repo structure
    (root / "main.py").write_text("class Main:\n    pass\n")
    (root / "utils.py").write_text("def helper():\n    pass\n")
    subpkg = root / "subpkg"
    subpkg.mkdir()
    (subpkg / "__init__.py").write_text("")
    (subpkg / "models.py").write_text("class User:\n    pass\n")
    return root


@pytest.fixture
def temp_py_file(tmp_path):
    """Single Python file for unit tests."""
    f = tmp_path / "sample.py"
    f.write_text("def foo():\n    pass\n\nclass Bar:\n    pass\n")
    return f
```

```python
# tests/parser/conftest.py (fixtures specifiche del parser)
"""Parser-specific fixtures."""

import pytest
from cervellaswarm_code_intelligence.parser.treesitter_parser import TreesitterParser


@pytest.fixture
def parser():
    """Fresh TreesitterParser instance."""
    return TreesitterParser()
```

### Import Pattern nei Tests

```python
# tests/parser/test_treesitter_parser.py
# CORRETTO con src/ layout:
from cervellaswarm_code_intelligence.parser.treesitter_parser import TreesitterParser
from cervellaswarm_code_intelligence._types import Symbol

# Non serve sys.path hacking - pip install -e . risolve tutto
```

### Eseguire Tests in Isolamento

```bash
# Installa in modalita editable prima di runnare i tests
pip install -e ".[test]"

# Run tests
pytest tests/ -q
pytest tests/ -m "not slow"    # skip integration
pytest tests/parser/ -v        # solo parser tests

# Con coverage
pytest tests/ --cov=cervellaswarm_code_intelligence --cov-report=term-missing
```

---

## 6. Publishing a PyPI

### Workflow Moderno (Trusted Publishing - SENZA TOKEN)

Trusted Publishing usa OIDC per autenticarsi a PyPI da GitHub Actions.
Non servono API tokens o passwords nel repository. E' il metodo raccomandato dal 2024.

#### Setup una tantum su PyPI

1. Vai su https://pypi.org/manage/account/publishing/
2. Aggiungi "Trusted Publisher":
   - Owner: `rafapra3008`
   - Repository: `cervellaswarm`
   - Workflow: `release.yml`
   - Environment: `pypi` (opzionale ma raccomandato)

#### GitHub Actions Workflow

```yaml
# .github/workflows/release.yml
name: Release to PyPI

on:
  push:
    tags:
      - "ci/v*"   # cervellaswarm-code-intelligence versioned tags

jobs:
  build:
    name: Build distribution
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install build
        run: pip install build

      - name: Build package
        run: python -m build
        working-directory: packages/code-intelligence   # adjust path

      - uses: actions/upload-artifact@v4
        with:
          name: dist-packages
          path: packages/code-intelligence/dist/

  publish-testpypi:
    name: Publish to TestPyPI
    needs: build
    runs-on: ubuntu-latest
    environment: testpypi
    permissions:
      id-token: write    # REQUIRED for Trusted Publishing
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: dist-packages
          path: dist/
      - uses: pypa/gh-action-pypi-publish@release/v1
        with:
          repository-url: https://test.pypi.org/legacy/

  publish-pypi:
    name: Publish to PyPI
    needs: publish-testpypi
    runs-on: ubuntu-latest
    environment: pypi
    permissions:
      id-token: write    # REQUIRED for Trusted Publishing
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: dist-packages
          path: dist/
      - uses: pypa/gh-action-pypi-publish@release/v1
```

### Workflow Manuale (per prima pubblicazione)

```bash
# 1. Installa tools
pip install build twine

# 2. Build
cd packages/code-intelligence
python -m build
# Produce: dist/cervellaswarm_code_intelligence-0.1.0.tar.gz
#          dist/cervellaswarm_code_intelligence-0.1.0-py3-none-any.whl

# 3. Check prima di pubblicare
twine check dist/*

# 4. Test su TestPyPI prima
twine upload --repository testpypi dist/*
# Installa e testa:
pip install --index-url https://test.pypi.org/simple/ cervellaswarm-code-intelligence

# 5. Pubblica su PyPI reale
twine upload dist/*
```

### Versioning

Usa semantic versioning. Aggiorna `version` in pyproject.toml e crea git tag:
```bash
git tag ci/v0.1.0
git push origin ci/v0.1.0
```

---

## 7. Delta rispetto all'attuale cervella/pyproject.toml

| Cosa | Attuale (cervella) | Nuovo (code-intelligence) |
|------|--------------------|--------------------------|
| Build backend | setuptools>=61 | hatchling>=1.26 |
| Layout | flat (.) | src/ layout |
| License field | `{text = "Apache-2.0"}` | `"Apache-2.0"` (PEP 639) |
| license-files | assente | `["LICENSE", "NOTICE"]` |
| pythonpath in pytest | `["."]` | `["src"]` |
| Entry point ref | `cli:main` | `cervellaswarm_code_intelligence.cli.search_cmd:main` |
| Publishing | non configurato | Trusted Publishing OIDC |

---

## Raccomandazione

**Implementare in questo ordine per FASE 1:**

1. Creare directory `packages/code-intelligence/` con struttura src/
2. Copiare i moduli da `scripts/utils/` nella struttura package
3. Aggiornare import relativi (da `from treesitter_parser import` a `from cervellaswarm_code_intelligence.parser.treesitter_parser import`)
4. Scrivere pyproject.toml con hatchling + PEP 639
5. `pip install -e ".[test]"` e verificare che tutti i 400+ test passino
6. Build e check con `python -m build && twine check dist/*`
7. Prima pubblicazione su TestPyPI, poi PyPI

**Il task critico** e' la migrazione degli import: tutti i `sys.path.insert(0, str(_dir))` nei CLI files vanno rimossi - con src/ layout e `pip install -e .` non servono piu.

---

*Report generato da Cervella Researcher - Sessione 367 (2026-02-18)*
