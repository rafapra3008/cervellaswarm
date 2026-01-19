# Semantic Search - CervellaSwarm W3

> Navigate your codebase semantically using W3 infrastructure (tree-sitter + PageRank).

## Overview

Semantic Search provides high-level API for code navigation using symbol extraction, dependency analysis, and PageRank importance scoring. Built on top of W2 infrastructure (tree-sitter parsing, dependency graph), it answers questions like:

- Where is this symbol defined?
- Who calls this function?
- What does this class use?
- How risky is it to modify this code?

**Supported Languages:** Python, TypeScript, JavaScript (via tree-sitter)

**Performance:** Fast indexing with automatic caching. Excludes `node_modules`, `.git`, `__pycache__`, `.venv` automatically.

## Quick Start

### Find a Symbol

```python
from semantic_search import SemanticSearch

search = SemanticSearch("/path/to/repo")

# Find where Symbol class is defined
location = search.find_symbol("Symbol")
if location:
    file_path, line_number = location
    print(f"Found at {file_path}:{line_number}")
```

### Analyze Impact of Changes

```python
from impact_analyzer import ImpactAnalyzer

analyzer = ImpactAnalyzer("/path/to/repo")

# Estimate risk of modifying DependencyGraph
result = analyzer.estimate_impact("DependencyGraph")
print(f"Risk: {result.risk_level} ({result.risk_score:.2f})")
print(f"Affects {result.files_affected} files, {result.callers_count} callers")

for reason in result.reasons:
    print(f"  - {reason}")
```

## API Reference

### SemanticSearch

Main class for semantic code navigation.

#### Constructor

```python
SemanticSearch(repo_root: str)
```

**Parameters:**
- `repo_root`: Path to repository root directory

**Raises:**
- `ValueError`: If repo_root doesn't exist or is not a directory

**Example:**
```python
search = SemanticSearch("/Users/rafapra/Developer/CervellaSwarm")
```

**Note:** Initialization builds symbol index (may take a few seconds for large repos).

#### find_symbol(name)

Find symbol definition location.

```python
find_symbol(name: str) -> Optional[Tuple[str, int]]
```

**Parameters:**
- `name`: Symbol name to search for (e.g., "MyClass", "login")

**Returns:**
- Tuple of `(file_path, line_number)` if found, `None` otherwise
- `file_path` is absolute path string
- `line_number` is 1-indexed

**Example:**
```python
location = search.find_symbol("SymbolExtractor")
if location:
    file, line = location
    print(f"SymbolExtractor defined at {file}:{line}")
```

**Multiple candidates:** If multiple symbols have the same name (e.g., in different files), returns the most important one based on PageRank score.

#### find_callers(symbol_name)

Find all functions that call this symbol.

```python
find_callers(symbol_name: str) -> List[Tuple[str, int, str]]
```

**Parameters:**
- `symbol_name`: Name of symbol to find callers for

**Returns:**
- List of tuples `(file_path, line_number, caller_name)`
- Returns `[]` if symbol not found or has no callers

**Example:**
```python
callers = search.find_callers("extract_symbols")
for file, line, caller in callers:
    print(f"{caller} calls it at {file}:{line}")
```

#### find_callees(symbol_name)

Find all functions this symbol calls.

```python
find_callees(symbol_name: str) -> List[str]
```

**Parameters:**
- `symbol_name`: Name of symbol to find callees for

**Returns:**
- List of symbol names that this symbol calls/uses
- Returns `[]` if symbol not found or calls nothing

**Example:**
```python
callees = search.find_callees("SemanticSearch.__init__")
print(f"SemanticSearch.__init__ calls: {', '.join(callees)}")
```

#### find_references(symbol_name)

Find all references to this symbol.

```python
find_references(symbol_name: str) -> List[Tuple[str, int]]
```

**Parameters:**
- `symbol_name`: Name of symbol to find references for

**Returns:**
- List of tuples `(file_path, line_number)` where symbol is referenced
- Returns `[]` if symbol not found or not referenced anywhere

**Example:**
```python
refs = search.find_references("DependencyGraph")
for file, line in refs:
    print(f"Used at {file}:{line}")
```

#### get_symbol_info(symbol_name)

Get detailed information about a symbol.

```python
get_symbol_info(symbol_name: str) -> Optional[Symbol]
```

**Parameters:**
- `symbol_name`: Name of symbol

**Returns:**
- `Symbol` object if found, `None` otherwise
- Returns most important symbol if multiple candidates exist

**Example:**
```python
info = search.get_symbol_info("ImpactAnalyzer")
if info:
    print(f"Type: {info.type}")
    print(f"Signature: {info.signature}")
    print(f"Docstring: {info.docstring}")
    print(f"References: {len(info.references)} symbols")
```

**Symbol object fields:**
- `name`: Symbol name
- `type`: Symbol type ("class", "function", "interface", "type")
- `file`: Absolute file path
- `line`: Line number (1-indexed)
- `signature`: Function/method signature or class declaration
- `docstring`: Docstring content (if present)
- `references`: List of symbol names used by this symbol

#### get_stats()

Get statistics about indexed codebase.

```python
get_stats() -> Dict
```

**Returns:**
- Dictionary with statistics:
  - `total_symbols`: Total number of Symbol objects
  - `unique_names`: Number of unique symbol names
  - `graph_nodes`: Number of nodes in dependency graph
  - `graph_edges`: Number of edges in dependency graph
  - `cached_files`: Number of files in SymbolExtractor cache

**Example:**
```python
stats = search.get_stats()
print(f"Total symbols: {stats['total_symbols']}")
print(f"Unique names: {stats['unique_names']}")
```

#### clear_cache()

Clear SymbolExtractor cache to free memory.

```python
clear_cache() -> None
```

**Note:** Symbol index and graph remain intact. Only parser cache is cleared.

---

### ImpactAnalyzer

Estimate risk of code modifications using dependency analysis and PageRank.

#### Constructor

```python
ImpactAnalyzer(repo_root: str)
```

**Parameters:**
- `repo_root`: Path to repository root directory

**Raises:**
- `ValueError`: If repo_root doesn't exist or is not a directory

**Example:**
```python
analyzer = ImpactAnalyzer("/Users/rafapra/Developer/CervellaSwarm")
```

**Note:** Internally creates a `SemanticSearch` instance. Index is built during initialization.

#### estimate_impact(symbol_name)

Estimate impact of modifying a symbol.

```python
estimate_impact(symbol_name: str) -> Optional[ImpactResult]
```

**Parameters:**
- `symbol_name`: Name of symbol to analyze (e.g., "MyClass", "login")

**Returns:**
- `ImpactResult` object if found, `None` if symbol not found

**Example:**
```python
result = analyzer.estimate_impact("TreesitterParser")
if result:
    print(f"Risk Level: {result.risk_level.upper()}")
    print(f"Risk Score: {result.risk_score:.2f} / 1.00")
    print(f"Callers: {result.callers_count}")
    print(f"Files affected: {result.files_affected}")
    print(f"\nReasons:")
    for reason in result.reasons:
        print(f"  - {reason}")
```

**Risk Algorithm:**

Risk score is computed as: `min(base + caller_factor + type_factor, 1.0)`

- **base**: PageRank importance (0.0-0.3)
- **caller_factor**: Number of callers (0.0-0.4) - 20+ callers = max score
- **type_factor**: Symbol type weight (0.0-0.3) - classes riskier than functions

**Risk Levels:**
- `low` (0.0-0.3): Safe to modify, few dependencies
- `medium` (0.3-0.5): Moderate impact, some callers
- `high` (0.5-0.7): High impact, many callers or important
- `critical` (0.7-1.0): Critical component, widely used

#### find_dependencies(file_path)

Find all files that this file depends on.

```python
find_dependencies(file_path: str) -> List[str]
```

**Parameters:**
- `file_path`: Path to file to analyze (relative or absolute)

**Returns:**
- List of absolute file paths that this file imports/uses
- Returns `[]` if file not found or has no dependencies

**Example:**
```python
deps = analyzer.find_dependencies("scripts/utils/semantic_search.py")
for dep in deps:
    print(f"Depends on: {dep}")
```

**Use case:** Understanding what breaks if a dependency changes.

#### find_dependents(file_path)

Find all files that depend on this file.

```python
find_dependents(file_path: str) -> List[str]
```

**Parameters:**
- `file_path`: Path to file to analyze (relative or absolute)

**Returns:**
- List of absolute file paths that import/use this file
- Returns `[]` if file not found or has no dependents

**Example:**
```python
dependents = analyzer.find_dependents("scripts/utils/symbol_extractor.py")
for dep in dependents:
    print(f"Used by: {dep}")
```

**Use case:** Understanding blast radius of changes.

#### get_stats()

Get statistics about analyzed codebase.

```python
get_stats() -> Dict
```

**Returns:**
- Same as `SemanticSearch.get_stats()` (uses internal `search` instance)

---

### ImpactResult

Dataclass containing impact analysis results.

**Fields:**

```python
@dataclass
class ImpactResult:
    symbol_name: str           # Name of analyzed symbol
    risk_score: float          # Overall risk score (0.0-1.0)
    risk_level: str            # "low", "medium", "high", "critical"
    files_affected: int        # Number of files affected by changes
    callers_count: int         # Number of symbols that call this symbol
    importance_score: float    # PageRank importance (0.0-1.0)
    reasons: List[str]         # List of reasons explaining risk score
```

**Example:**
```python
result = analyzer.estimate_impact("DependencyGraph")
print(result)  # <ImpactResult 'DependencyGraph': HIGH (0.65) - 8 callers, 3 files>

if result.risk_level in ["high", "critical"]:
    print("⚠️  CAUTION: Review carefully before modifying!")
    print("\n".join(result.reasons))
```

## Examples

### Example 1: Find Symbol and Analyze Impact

```python
from semantic_search import SemanticSearch
from impact_analyzer import ImpactAnalyzer

# Initialize
repo_root = "/Users/rafapra/Developer/CervellaSwarm"
search = SemanticSearch(repo_root)
analyzer = ImpactAnalyzer(repo_root)

# Find Symbol class
location = search.find_symbol("Symbol")
if location:
    file, line = location
    print(f"✅ Symbol defined at {file}:{line}")

    # Analyze impact
    result = analyzer.estimate_impact("Symbol")
    if result:
        print(f"\n🎯 Risk Level: {result.risk_level.upper()}")
        print(f"📊 Risk Score: {result.risk_score:.2f}")
        print(f"📞 Callers: {result.callers_count}")
        print(f"📁 Files affected: {result.files_affected}")
        print(f"\n💡 Assessment:")
        for reason in result.reasons:
            print(f"   {reason}")
```

### Example 2: Find All Callers of a Function

```python
from semantic_search import SemanticSearch

search = SemanticSearch("/Users/rafapra/Developer/CervellaSwarm")

# Find who calls extract_symbols()
callers = search.find_callers("extract_symbols")
print(f"📞 extract_symbols() is called by {len(callers)} symbols:\n")

for file, line, caller in callers:
    print(f"   {caller}")
    print(f"      at {file}:{line}")
    print()
```

### Example 3: Analyze File Dependencies

```python
from impact_analyzer import ImpactAnalyzer

analyzer = ImpactAnalyzer("/Users/rafapra/Developer/CervellaSwarm")

file = "scripts/utils/semantic_search.py"

# What does this file depend on?
deps = analyzer.find_dependencies(file)
print(f"📦 {file} depends on:")
for dep in deps:
    print(f"   - {dep}")

print()

# What depends on this file?
dependents = analyzer.find_dependents(file)
print(f"🔗 {file} is used by:")
for dep in dependents:
    print(f"   - {dep}")
```

### Example 4: Pre-modification Safety Check

```python
from impact_analyzer import ImpactAnalyzer

def check_before_modifying(symbol_name: str, repo_root: str):
    """Check if it's safe to modify a symbol."""
    analyzer = ImpactAnalyzer(repo_root)
    result = analyzer.estimate_impact(symbol_name)

    if not result:
        print(f"❌ Symbol '{symbol_name}' not found")
        return False

    print(f"🔍 Analyzing '{symbol_name}'...")
    print(f"Risk Level: {result.risk_level.upper()}")
    print(f"Risk Score: {result.risk_score:.2f}")
    print(f"Callers: {result.callers_count}")
    print(f"Files affected: {result.files_affected}")
    print()

    if result.risk_level in ["high", "critical"]:
        print("⚠️  HIGH RISK! Recommendations:")
        for reason in result.reasons:
            print(f"   - {reason}")
        print("\nSuggested actions:")
        print("   1. Review all callers")
        print("   2. Write comprehensive tests")
        print("   3. Consider backward compatibility")
        print("   4. Notify team before modifying")
        return False
    elif result.risk_level == "medium":
        print("✅ MODERATE RISK - Proceed with caution")
        print("   - Review callers")
        print("   - Add tests for affected code")
        return True
    else:
        print("✅ LOW RISK - Safe to modify with standard testing")
        return True

# Example usage
check_before_modifying("DependencyGraph", "/Users/rafapra/Developer/CervellaSwarm")
```

## CLI Usage

Both modules provide CLI for quick analysis.

### SemanticSearch CLI

```bash
cd scripts/utils
python semantic_search.py <repo_root> <symbol_name> [command]
```

**Commands:**
- `find` - Find symbol definition (default)
- `callers` - Find all callers
- `callees` - Find all callees
- `refs` - Find all references
- `info` - Show detailed symbol info
- `stats` - Show repository statistics

**Examples:**

```bash
# Find where Symbol class is defined
python semantic_search.py ~/Developer/CervellaSwarm Symbol

# Find who calls extract_symbols
python semantic_search.py ~/Developer/CervellaSwarm extract_symbols callers

# Find what DependencyGraph uses
python semantic_search.py ~/Developer/CervellaSwarm DependencyGraph callees

# Show detailed info about TreesitterParser
python semantic_search.py ~/Developer/CervellaSwarm TreesitterParser info

# Show repository stats
python semantic_search.py ~/Developer/CervellaSwarm Symbol stats
```

### ImpactAnalyzer CLI

```bash
cd scripts/utils
python impact_analyzer.py <repo_root> <symbol_name>
```

**Example:**

```bash
# Analyze impact of modifying SemanticSearch
python impact_analyzer.py ~/Developer/CervellaSwarm SemanticSearch
```

**Output:**
```
🔍 Initializing impact analyzer for: /Users/rafapra/Developer/CervellaSwarm

📊 Repository Statistics:
   Total symbols: 156
   Unique names: 142
   Graph nodes: 156
   Graph edges: 312

⚡ Analyzing impact: SemanticSearch

============================================================
IMPACT ANALYSIS: SemanticSearch
============================================================

🎯 Risk Level: HIGH
📊 Risk Score: 0.62 / 1.00

📈 Impact Metrics:
   Callers: 8
   Files affected: 3
   PageRank importance: 0.042156

💡 Reasons:
   1. 8 callers - moderate impact
   2. Used in 3 files - limited scope
   3. High PageRank importance (0.0422) - central to codebase
   4. Class type - changes may affect multiple methods
   5. HIGH RISK: Review callers and add tests before modifying

============================================================

📞 Callers (8):
   ImpactAnalyzer.__init__ at .../impact_analyzer.py:145
   ...
```

## Performance

### Indexing Performance

- **Small repos** (< 100 files): ~1-2 seconds
- **Medium repos** (100-1000 files): ~5-10 seconds
- **Large repos** (1000+ files): ~20-30 seconds

### Automatic Exclusions

The following directories are automatically excluded from scanning:
- `node_modules/`
- `.git/`
- `__pycache__/`
- `.venv/`, `venv/`
- `dist/`, `build/`
- `.next/`, `.nuxt/`
- `coverage/`
- `.pytest_cache/`, `.mypy_cache/`, `.tox/`
- `*.egg-info/`, `.eggs/`

### Caching

- **SymbolExtractor cache**: Parsed results cached per file
- **No re-parsing** unless file changes
- Use `search.clear_cache()` to free memory after analysis

### Query Performance

After index is built:
- `find_symbol()`: O(1) lookup
- `find_callers()`: O(1) graph lookup
- `find_callees()`: O(1) lookup
- `find_references()`: O(1) graph lookup
- `estimate_impact()`: O(1) + PageRank computation (cached)

## Integration with CervellaSwarm

### spawn-workers Integration

Use Semantic Search in worker prompts to provide context:

```python
from semantic_search import SemanticSearch

# Before delegating to backend worker
search = SemanticSearch("/Users/rafapra/Developer/CervellaSwarm")
location = search.find_symbol("extract_symbols")

if location:
    file, line = location
    # Include in worker prompt
    context = f"Symbol defined at {file}:{line}"
```

### Pre-Modification Checks

Before modifying critical code:

```python
from impact_analyzer import ImpactAnalyzer

analyzer = ImpactAnalyzer(repo_root)
result = analyzer.estimate_impact(symbol_name)

if result and result.risk_level in ["high", "critical"]:
    # Delegate to cervella-guardiana-qualita for review
    spawn_workers(
        "--guardiana-qualita",
        task=f"Review modification to {symbol_name}",
        context=result.reasons
    )
```

### Worker Prompt Templates

**Example: cervella-backend prompt enhancement**

```markdown
## Code Navigation Tools

You have access to SemanticSearch and ImpactAnalyzer:

- Find symbol definitions: `search.find_symbol("MyClass")`
- Find callers: `search.find_callers("my_function")`
- Estimate impact: `analyzer.estimate_impact("MyClass")`

BEFORE modifying any symbol:
1. Run `estimate_impact(symbol_name)`
2. If risk_level is "high" or "critical": consult Regina
3. Document impact in output
```

## Troubleshooting

### Symbol Not Found

**Issue:** `find_symbol()` returns `None`

**Solutions:**
1. Check symbol name spelling (case-sensitive)
2. Verify file is not excluded (check `should_exclude()` logic)
3. Ensure file extension is supported (.py, .ts, .tsx, .js, .jsx)
4. Check symbol is actually defined (not just imported)

### Incomplete Callers

**Issue:** `find_callers()` returns fewer results than expected

**Possible causes:**
1. Dynamic calls (e.g., `getattr()`) not detected
2. Indirect calls through abstractions
3. Cross-language calls (Python calling TypeScript via API)

**Note:** tree-sitter parses source code statically. Runtime-only references won't be detected.

### Performance Issues

**Issue:** Index building takes too long

**Solutions:**
1. Check excluded directories are working (should see ~100 files, not 17k+)
2. Use `search.get_stats()` to verify file count
3. Consider excluding more directories for your specific repo

### Memory Usage

**Issue:** High memory usage

**Solutions:**
1. Call `search.clear_cache()` after analysis
2. Avoid creating multiple `SemanticSearch` instances
3. Reuse existing instance for multiple queries

## Requirements

- Python 3.10+
- tree-sitter bindings (`tree-sitter`, `tree-sitter-python`, `tree-sitter-typescript`)
- NetworkX (for PageRank)

**Installation:**
```bash
pip install tree-sitter tree-sitter-python tree-sitter-typescript networkx
```

## Architecture

```
SemanticSearch
├── SymbolExtractor (parse symbols from files)
│   └── TreesitterParser (tree-sitter parsing)
└── DependencyGraph (analyze relationships)
    └── PageRank (compute importance)

ImpactAnalyzer
└── SemanticSearch (reuses existing infrastructure)
```

**Data Flow:**

1. **Indexing**: `SemanticSearch.__init__()` scans repo
2. **Parsing**: `SymbolExtractor.extract_symbols()` parses each file
3. **Graph Building**: Symbols and references added to `DependencyGraph`
4. **PageRank**: `graph.compute_importance()` calculates scores
5. **Queries**: API methods use pre-built index for fast lookups

## Version History

- **v1.1.0** (2026-01-19): W3 Day 3 - Bug fix: Exclude node_modules, .git, etc.
- **v1.0.0** (2026-01-19): W3 Day 1-2 - Initial implementation (REQ-01 to REQ-08)

## Related Documentation

- [Tree-sitter Integration](README_TREESITTER.md) - W2 infrastructure details
- [Symbol Extractor Tests](../tests/README_SYMBOL_EXTRACTOR_TESTS.md) - Test suite documentation
- [W3 Research Output](.swarm/tasks/TASK_W3_RESEARCH_OUTPUT.md) - Research and requirements

---

**Author:** Cervella Backend
**Version:** 1.1.0
**Date:** 2026-01-19

*Part of CervellaSwarm W3 Semantic Search Initiative*
