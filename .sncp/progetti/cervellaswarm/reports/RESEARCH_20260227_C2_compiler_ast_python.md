# Ricerca C2: Best Practices Compilatore AST -> Python

> **Data:** 2026-02-27
> **Autore:** Cervella Researcher
> **Status:** COMPLETA
> **Fonti consultate:** 18 web sources + codebase analysis
> **Contesto:** Preparazione FASE C2 - Il Compilatore (step C2.1 STUDIO)

---

## Premessa: Stato dell'arte in casa nostra

Prima della ricerca esterna, analisi del `codegen.py` esistente (730 LOC):

**Cosa gia abbiamo:**
- `PythonGenerator` class con metodi `generate_header/imports/protocol_definition/role_classes/session_class`
- String emission pura: costruisce liste di stringhe, poi `"\n".join()`
- Helper `_safe_python_ident`, `_escape_string`, `_to_class_name`
- `GeneratedCode` frozen dataclass come result type
- Zero dipendenze esterne (pattern della famiglia)

**Il gap critico:** `codegen.py` prende `Protocol` objects (Python objects, non AST).
C2 deve prendere `ProgramNode` (AST dalla C1) e generare Python.

---

## Domanda 1: Pattern di Compilazione AST -> Python

### 1.1 Come fanno i grandi

**Cython** (il piu rilevante):
- Pipeline: sorgente Cython -> parse tree -> trasformazioni via Visitor pattern -> C code string
- Usa `Visitor.py` con `visit_NomeNodo()` dispatch automatico per ogni tipo di nodo
- Trasformazioni multiple pass: analisi dichiarazioni -> analisi espressioni -> code gen
- Per il code gen finale: string emission con template Tempita per parti complesse
- Conclusione: **Visitor pattern + string emission per la fase finale**

**Hy (Lisp -> Python AST)**:
- Compila direttamente a `ast.Module` Python (non stringhe)
- Usa `ast.fix_missing_locations()` per propagare lineno/col_offset
- Poi usa `compile(ast_module, filename, "exec")` per ottenere bytecode
- Conclusione: **Genera Python AST nativo, poi compile() -> bytecode**

**Coconut (Python superset -> Python)**:
- String emission con commenti inline per source mapping
- `# line N "file.coco"` su ogni riga generata
- Non genera ast.Module, genera sorgente Python leggibile

### 1.2 String Emission vs Python ast.Module

| Criterio | String Emission | ast.Module |
|----------|----------------|------------|
| Semplicita | Alta (gia lo facciamo) | Bassa (node types, fix_missing_locations) |
| Leggibilita output | Alta (debug facile) | Bassa (bisogna fare unparse) |
| Validazione | Solo via compile() dopo | Strutturale durante costruzione |
| Source maps | Commenti inline | ast.copy_location() nativo |
| Performance | Leggermente piu veloce | Overhead minimo ast construction |
| Optimizations | Difficile fare pass multipli | Possibile NodeTransformer |
| Zero-deps | SI | SI (ast stdlib) |
| Gia nel nostro codebase | SI (codegen.py) | NO |

### 1.3 Raccomandazione per Lingua Universale

**USARE STRING EMISSION** - motivazioni:

1. `codegen.py` gia usa string emission e funziona bene (1826 test, 9.5+/10)
2. Il linguaggio e dichiarativo: non ci sono ottimizzazioni multi-pass che giustificano ast.Module
3. Output leggibile e critico: il codice generato deve potersi leggere per debug
4. Zero-deps e un valore della famiglia - ast stdlib e ok ma aggiunge complessita
5. Cython stesso usa string emission per la fase finale

**Pattern concreto da adottare:**

```python
class ASTCompiler:
    """Visitor-based AST -> Python string compiler."""

    def compile(self, node: ProgramNode) -> str:
        lines = []
        for decl in node.declarations:
            lines.extend(self._compile_declaration(decl))
        return "\n".join(lines)

    def _compile_declaration(self, node):
        if isinstance(node, AgentNode):
            return self._compile_agent(node)
        elif isinstance(node, ProtocolNode):
            return self._compile_protocol(node)
        # ... dispatch per tipo
```

**Rischio:** String emission non valida la struttura Python prima di scrivere.
**Mitigazione:** Fare `compile(generated_source, "generated", "exec")` come test post-generation.

---

## Domanda 2: Source Maps / Error Tracing

### 2.1 Come fanno i grandi

**TypeScript -> JavaScript:**
- File `.js.map` separato con mappings base64-encoded
- Ogni posizione JS mappa a posizione TS (linea, colonna, file)
- Oppure inline: `//# sourceMappingURL=data:application/json;base64,...`
- Framework pesante, non adatto a DSL puri

**Coconut -> Python:**
- Approccio elegante e minimale: commento su ogni riga generata
- `# line N "source.coco"` decorates every emitted Python line
- Leggibile, senza dipendenze, funziona con qualsiasi debugger

**Cython -> C:**
- Ogni nodo AST ha `pos` attribute con (file, line, col)
- Il generatore di C emette `/* "file.pyx":42 */` prima di ogni blocco

**Python ast.copy_location:**
- Se si genera ast.Module: `ast.copy_location(new_node, source_node)`
- Copia lineno, col_offset, end_lineno, end_col_offset
- Python traceback usa questi per mostrare la riga corretta

### 2.2 Approccio pratico per Lingua Universale

Il nostro AST gia ha `Loc` su ogni nodo: `@dataclass(frozen=True) class Loc: line: int; col: int`

**Strategia raccomandata: Commenti inline + `__source_location__` attribute**

```python
# Ogni blocco generato inizia con commento source location
# [LU:15:4] agent Worker
class Worker:
    """Agent 'Worker' - compiled from Lingua Universale line 15."""
    __source_location__ = "line 15, col 4"

    def process(self, input):
        # [LU:17:8] requires: input.is_valid
        if not input.is_valid:
            raise ContractViolation(
                "requires: input.is_valid",
                source="line 17, col 8"
            )
```

**Per errori runtime**, wrappare con try/except che aggiunge source location:

```python
class ContractViolation(Exception):
    def __init__(self, condition: str, source: str):
        super().__init__(f"Contract violated at {source}: {condition}")
```

### 2.3 Rischi e tradeoff

- **Approccio commenti inline:** Semplice, leggibile, zero-deps. Limite: non funziona con debugger interattivo (pdb non sa dove andare nel sorgente .lu).
- **Approccio ast.Module con copy_location:** Python traceback punta al file .lu correttamente. Costo: complessita aggiuntiva.
- **Raccomandazione:** Commenti inline per C2 (MVP). Se in C3 si vuole il debugger REPL, aggiungere ast.Module con copy_location.

---

## Domanda 3: Contratti Runtime

### 3.1 Librerie disponibili

**icontract** (v2.7.3):
- `@require(lambda arg: condition)` per precondizioni
- `@ensure(lambda result: condition)` per postcondizioni
- Supporta ereditarieta dei contratti (unico in Python)
- Overhead: 3.91 μs per precondizione, 4.39 μs per postcondizione
- Violation messages dettagliati con valori delle variabili
- Integrazione con CrossHair (verifica formale) e Hypothesis (PBT)

**deal** (life4/deal):
- `@deal.pre(lambda arg: condition)` / `@deal.post(lambda result: condition)`
- Zero-dependency runtime
- `deal lint` per analisi statica
- `deal.cases()` per test generation automatico
- Overhead simile a icontract: ~4 μs per precondizione

**dpcontracts:**
- Overhead molto alto: 53.92 μs per precondizione (da evitare)
- Non supporta ricorsione/ereditarieta

### 3.2 Generazione assert vs decoratori vs raise

**Opzione A: assert inline (piu semplice)**
```python
def process(self, data):
    assert data.is_valid, "requires: data.is_valid"
    result = self._do_work(data)
    assert result is not None, "ensures: result is not None"
    return result
```
Pro: zero-deps, veloce (ottimizzato via -O), familiare
Contro: `python -O` disabilita gli assert! NON usare per contratti di sicurezza.

**Opzione B: raise inline (raccomandato per noi)**
```python
def process(self, data):
    if not data.is_valid:
        raise ContractViolation("requires: data.is_valid", loc="LU:17:4")
    result = self._do_work(data)
    if result is None:
        raise ContractViolation("ensures: result is not None", loc="LU:19:4")
    return result
```
Pro: non disabilitabile, source location tracciabile, zero-deps
Contro: verboso nel codice generato

**Opzione C: decoratori icontract (piu espressivo)**
```python
@require(lambda data: data.is_valid)
@ensure(lambda result: result is not None)
def process(self, data):
    return self._do_work(data)
```
Pro: separazione contratti/logica, violation messages ricchi
Contro: dipendenza esterna (rompe il principio zero-deps della famiglia)

### 3.3 Raccomandazione per Lingua Universale

**USARE `raise ContractViolation` inline** - motivazioni:

1. Zero-deps (famiglia value)
2. Non disabilitabile (assert si disabilita con python -O)
3. Possiamo incorporare source location
4. Il codice generato e self-contained

Definire `ContractViolation(Exception)` nel package lingua-universale e importarla.

```python
# Nel package: cervellaswarm_lingua_universale/contracts.py
class ContractViolation(RuntimeError):
    """Raised when a Lingua Universale contract is violated at runtime."""
    def __init__(self, condition: str, kind: str = "requires", source: str = ""):
        msg = f"[LU Contract] {kind} violated: {condition}"
        if source:
            msg += f" (at {source})"
        super().__init__(msg)
```

**Performance:** raise con `if not condition` e praticamente 0 overhead quando il contratto passa (una branch prediction). Non serve benchmark.

**Overhead totale stimato per agent con 3 requires + 2 ensures:** ~5-10 microsecond per chiamata. Accettabile per protocolli multi-agent.

---

## Domanda 4: Python Interop

### 4.1 `use python math` - Come implementarlo

Il nodo `UseNode` nell'AST ha gia: `module: str`, `alias: str | None`.

```
# Lingua Universale
use python math
use python datetime as dt
```

**Generazione Python:**
```python
# Generato da: use python math
import math  # [LU:1:0] use python math

# Generato da: use python datetime as dt
import datetime as dt  # [LU:2:0] use python datetime as dt
```

**Meccanismo:** Pattern diretto. `UseNode.module` -> `import {module}` o `import {module} as {alias}`.

**Namespace isolation:** Ogni agente compilato diventa una classe. Gli import sono a livello modulo del file generato. Non ci sono collisioni perche ogni file .lu compila in un modulo Python separato.

### 4.2 Esportare per importazione da Python

Il codice generato deve essere importabile come modulo Python normale:

```python
# Generato da my_protocol.lu:
"""Auto-generated from my_protocol.lu by Lingua Universale compiler."""

from cervellaswarm_lingua_universale.contracts import ContractViolation

class WorkerAgent:
    """..."""
    def process(self, data): ...

# Alla fine del file generato:
__all__ = ["WorkerAgent", "ProtocolSession"]
```

Poi da Python: `from my_protocol import WorkerAgent`.

**Importazione dinamica del generato:** usare `importlib.util.spec_from_file_location` per caricare a runtime:

```python
import importlib.util
spec = importlib.util.spec_from_file_location("my_protocol", "/path/to/generated.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
Worker = mod.WorkerAgent
```

### 4.3 Rischi e tradeoff

- **Collisioni nomi:** Se due .lu files definiscono `WorkerAgent`, l'import dell'uno sovrascrive l'altro. Mitigazione: namespace basato sul nome file (`my_protocol.WorkerAgent`).
- **Circular imports:** Se .lu A usa .lu B che usa .lu A. Mitigazione: detection al compile time (analisi del grafo delle dipendenze).
- **Versioning:** Se il formato generato cambia, i file vecchi rompono. Mitigazione: aggiungere `__lu_version__ = "0.2"` nei file generati.

---

## Domanda 5: Testing del Compilatore

### 5.1 Snapshot Testing (Golden Files)

**Strumenti disponibili:**
- `pytest-golden`: `--update-goldens` per aggiornare, file YAML
- `pytest-snapshot`: `--snapshot-update`, file `.txt` semplici
- `syrupy`: integra con pytest fixtures, readable serialization, git-friendly
- `inline-snapshot`: snapshots nel codice test stesso

**Pattern per il compilatore:**
```python
# test_compiler_golden.py
def test_agent_with_requires(snapshot):
    source = """
    agent Worker:
        requires: input.is_valid
        ensures: result is not None
    """
    ast = parse(source)
    generated = compile_to_python(ast)
    snapshot.assert_match(generated, "agent_with_requires.py.golden")
```

**File golden:** `.sncp/progetti/cervellaswarm/golden/` (NON nella test dir per evitare shadowing)

### 5.2 Round-Trip Testing

**Pipeline:**
1. Source LU -> parse() -> ProgramNode
2. ProgramNode -> compile() -> Python string
3. Python string -> exec() in sandbox namespace
4. Verify behavior matches spec

```python
def test_round_trip_contract():
    source = "agent Worker:\n    requires: x > 0\n    ensures: result > x"
    ast = parse(source)
    py_code = compile_to_python(ast)
    namespace = {}
    exec(py_code, namespace)
    Worker = namespace["Worker"]
    with pytest.raises(ContractViolation):
        Worker().process(x=-1)  # violates requires: x > 0
```

### 5.3 Property-Based Testing con Hypothesis

Per testare proprieta del compilatore, non casi specifici:

```python
from hypothesis import given, strategies as st

@given(st.integers(min_value=1, max_value=100))
def test_confidence_level_always_valid(n):
    """Any valid confidence level compiles to valid Python."""
    source = f"agent A:\n    confidence: {['Low','Medium','High'][n % 3]}"
    ast = parse(source)
    py = compile_to_python(ast)
    assert py  # never empty
    compile(py, "generated", "exec")  # always valid Python
```

**Round-trip property:**
```python
@given(st.from_regex(r"agent [a-z]+:\n    requires: [a-z]+ > 0"))
def test_parse_compile_always_valid_python(source):
    try:
        ast = parse(source)
        py = compile_to_python(ast)
        compile(py, "test", "exec")  # must be valid Python
    except ParseError:
        pass  # invalid input is ok, as long as no crash
```

### 5.4 Raccomandazione Testing Strategy

Per C2, in ordine di priorita:

1. **Golden files** (syrupy, gia usato nella community) - per output leggibile e reviewable
2. **Round-trip exec tests** - 10 esempi canonici gia in `test_parser_integration.py`, estenderli con exec+verify
3. **Property-based (Hypothesis)** - aggiungere DOPO che i golden sono stabili

**Non usare pytest-golden** (YAML files, meno readable). **Usare syrupy** o file .golden semplici con diff esplicito.

---

## Architettura Proposta: C2.2

Basata su tutto quanto sopra, la struttura raccomandata per il compilatore:

```
packages/lingua-universale/src/cervellaswarm_lingua_universale/
  _compiler.py          # nuovo: ASTCompiler class (Visitor-based)
  _contracts.py         # nuovo: ContractViolation, SourceLocation
  codegen.py            # esistente: PythonGenerator (Protocol objects, NON toccare)
```

### `_compiler.py` - Struttura

```python
@dataclass(frozen=True)
class CompiledModule:
    source_file: str      # nome .lu originale
    python_source: str    # codice Python generato
    agents: tuple[str, ...]
    protocols: tuple[str, ...]
    imports: tuple[str, ...]

class ASTCompiler:
    """Compila ProgramNode -> Python source string.

    Architecture: Visitor-based dispatch, string emission, source annotations.
    """

    def compile(self, program: ProgramNode, source_file: str = "<input>") -> CompiledModule:
        ...

    def _compile_agent(self, node: AgentNode) -> list[str]:
        ...

    def _compile_requires(self, exprs: tuple[Expr, ...], loc: Loc) -> list[str]:
        ...

    def _compile_ensures(self, exprs: tuple[Expr, ...], loc: Loc) -> list[str]:
        ...

    def _compile_protocol(self, node: ProtocolNode) -> list[str]:
        ...

    def _compile_use(self, node: UseNode) -> list[str]:
        ...

    def _expr_to_python(self, expr: Expr) -> str:
        """Converte Expr AST -> stringa Python inline."""
        ...
```

### Mapping Expr -> Python

| Expr AST | Python generato |
|----------|----------------|
| `IdentExpr("input")` | `input` |
| `AttrExpr("input", "is_valid")` | `input.is_valid` |
| `BinOpExpr(left, "and", right)` | `(left) and (right)` |
| `BinOpExpr(left, ">", right)` | `(left) > (right)` |
| `NotExpr(operand)` | `not (operand)` |
| `NumberExpr("42")` | `42` |
| `StringExpr('"hello"')` | `"hello"` |
| `MethodCallExpr("tests", "pass", args)` | `tests.pass_(...)` (keyword safe) |

---

## Sintesi Raccomandata

| Decisione | Scelta | Motivo |
|-----------|--------|--------|
| Pattern compilazione | String Emission + Visitor dispatch | Gia nel codebase, semplice, zero-deps |
| Source maps | Commenti inline `# [LU:N:M]` + ContractViolation source param | Zero-deps, leggibile |
| Contratti runtime | `raise ContractViolation(condition, source)` inline | Zero-deps, non disabilitabile |
| Python interop | `import {module}` diretto, `importlib` per load dinamico | Standard Python |
| Testing | Golden files (syrupy) + round-trip exec + Hypothesis | Progressivo, da golden a PBT |
| Dipendenze aggiunte | 0 (ContractViolation nel nostro package) | Principio zero-deps della famiglia |

---

## Rischi Critici per C2

1. **`ensures` su funzioni che restituiscono valori:** La postcondizione deve poter accedere al risultato. Pattern: variabile temporanea `_result = f(); if not condition(_result): raise`.
2. **Espressioni complesse nel compilatore:** `BinOpExpr` annidati devono generare parentesi corrette. Risk: precedenza operatori sbagliata -> comportamento diverso.
3. **ProtocolNode vs AgentNode accoppiamento:** Un `ProtocolNode` si usa per generare `SessionChecker` (gia in codegen.py). Non duplicare - chiamare codegen.py esistente per la parte protocol.
4. **Naming clashes:** `AgentNode.name = "Worker"` + un modulo Python che si chiama `Worker` -> collisione. Mitigazione: prefissare classi generate con convenzione (es: `_LU_Worker`).

---

*Report generato: 2026-02-27*
*Prossimo step: C2.1 STUDIO completo con proposta architettura per Guardiana*
