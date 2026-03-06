# STUDIO C2.3 -- Python Interop

> **Creato:** 2026-02-27 - Sessione 415
> **Audit Guardiana Piano:** 9.0/10 APPROVED con riserve (2 P1, 3 P2, 5 P3 incorporati)
> **Prerequisiti:** C2.2 COMPLETO (7/7 sub-step, 9.5/10, 228 compiler tests, 100% coverage)

---

## L'INSIGHT

> "ABC mori perche era chiuso. Python vinse perche importava C."
> -- SUBROADMAP Fase C, Step C2.3

Il compilatore C2.2 genera Python valido e eseguibile. Ma il codice generato non e
ancora un "first-class Python citizen". C2.3 colma questo gap: il codice .lu diventa
un modulo Python importabile, salvabile, caricabile a runtime.

---

## SCOPE ESATTO

### IN C2.3

| Feature | Descrizione |
|---------|-------------|
| `__all__` generation | Il codice generato espone agents + protocols + types |
| Module metadata | `__lu_version__`, `__lu_source__` nel modulo generato |
| `compile_file()` | .lu file -> CompiledModule |
| `save_module()` | CompiledModule -> .py file su disco |
| `load_module()` | CompiledModule -> types.ModuleType a runtime |
| `load_file()` | Convenience: .lu -> ModuleType |
| Hardening | `_escape_contract_str` + pickle test ContractViolation |
| Types tracking | `CompiledModule.types` per variant + record names |

### DEFERRED (con motivazione)

| Feature | Perche | Quando |
|---------|--------|--------|
| `export` keyword | Richiede estensione grammatica EBNF completa | C2.4 |
| `@cervellaswarm.protocol` | API Python-side, non compiler | C3 |
| Inline .lu in Python | Richiede preprocessor/import hook | C3 |
| Type stubs .pyi | Nice-to-have, non critical path | C3 |
| GenericType Map[K,V] | Dipende da estensione grammatica C1 | Quando grammatica lo supporta |

---

## ARCHITETTURA

### Nuovo file: `_interop.py`

Separazione delle responsabilita:
- `_compiler.py` = pure string generation (no I/O, no importlib, no side effects)
- `_interop.py` = I/O e runtime module management

```
Pipeline:

  .lu file ──> compile_file() ──> CompiledModule ──> load_module() ──> ModuleType
                                       │
                                       └──> save_module() ──> .py file ──> import
```

### CompiledModule esteso

```python
@dataclass(frozen=True)
class CompiledModule:
    source_file: str
    python_source: str
    agents: tuple[str, ...]
    protocols: tuple[str, ...]
    imports: tuple[str, ...]
    types: tuple[str, ...]      # NEW: variant + record names
    exports: tuple[str, ...]    # NEW: names in __all__
```

### Codice generato -- nuova struttura

```python
"""Auto-generated from example.lu by Lingua Universale compiler."""

__lu_version__ = "0.2"
__lu_source__ = "example.lu"

from typing import Literal
# ... preamble imports ...

# ... declarations (types, agents, protocols) ...

__all__ = ["Worker", "DelegateTaskSession", "TaskStatus"]
```

### API `_interop.py`

```python
class InteropError(RuntimeError): ...

def compile_file(path, *, encoding="utf-8", source_name=None) -> CompiledModule: ...
def save_module(compiled, output_path, *, overwrite=False) -> Path: ...
def load_module(compiled, *, module_name=None) -> types.ModuleType: ...
def load_file(path, *, encoding="utf-8", module_name=None) -> types.ModuleType: ...
```

**Security note:** `load_module` e `load_file` eseguono `exec()` internamente.
Docstring deve dichiarare: "do not load untrusted .lu files without review."

---

## SUB-STEPS (6)

### C2.3.1 -- Hardening + types tracking
- `_escape_contract_str`: allineare con `codegen._escape_string` (gestisce `\n`, `\r`)
- Pickle round-trip test per `ContractViolation`
- `CompiledModule.types` per variant + record names
- ~10-12 test nuovi
- **Effort:** 0.5 sessione | **Rischio:** BASSO

### C2.3.2 -- `__all__` + module metadata
- `__all__` alla fine del modulo generato
- `__lu_version__` + `__lu_source__` dopo docstring
- `CompiledModule.exports`
- ~15-20 test nuovi
- **Effort:** 0.5 sessione | **Rischio:** BASSO

### C2.3.3 -- compile_file + save_module
- Nuovo file `_interop.py`
- `compile_file(path, *, encoding, source_name)`
- `save_module(compiled, output_path, *, overwrite)`
- `InteropError`
- ~15-20 test in `test_interop.py`
- **Effort:** 0.5 sessione | **Rischio:** BASSO

### C2.3.4 -- load_module + load_file
- `load_module(compiled, *, module_name) -> types.ModuleType`
- `load_file(path) -> types.ModuleType`
- Test per `__file__`, `__spec__`, GC edge cases
- Security warning nei docstring
- ~25-30 test
- **Effort:** 1 sessione | **Rischio:** MEDIO

### C2.3.5 -- Golden interop tests
- 10 round-trip (I1-I10) in `test_interop_golden.py`
- Include: `use python math` -> load_module -> `math.sqrt(4)` (P1 finding)
- Test runtime: contracts, sessions, multi-module
- ~20-30 test
- **Effort:** 0.5 sessione | **Rischio:** BASSO

### C2.3.6 -- Guardiana audit finale
- Update `__init__.py` con nuove API
- Target: 9.5/10
- **Effort:** 0.5 sessione

---

## RISCHI E MITIGAZIONI

| Rischio | Probabilita | Impatto | Mitigazione |
|---------|-------------|---------|-------------|
| importlib edge cases | MEDIO | MEDIO | Test dedicati per __file__, __spec__, GC |
| exec() security | BASSO | ALTO | Docstring warning, no untrusted files |
| test_compiler_core.py > 500 righe | MEDIO | BASSO | Split in file separato se necessario |
| File I/O flaky tests | BASSO | BASSO | tmp_path fixture esclusivamente |

---

## STIMA TOTALE

- **Test nuovi:** ~80-100
- **LOC nuovi:** ~400-500 (source) + ~800-1000 (test)
- **Effort:** ~3 sessioni (allineato con roadmap "2-3 sessioni")
- **File nuovi:** 3 (`_interop.py`, `test_interop.py`, `test_interop_golden.py`)
- **File modificati:** 2 (`_compiler.py`, `__init__.py`)

---

## FINDING GUARDIANA INCORPORATI

| ID | Severity | Descrizione | Azione |
|----|----------|-------------|--------|
| F1 | P1 | Manca test `use python X` round-trip via load_module | Aggiunto in C2.3.5 |
| F6 | P1 | exec() warning in docstring load_module/load_file | Aggiunto in C2.3.4 |
| F3 | P2 | source_name param per compile_file | Aggiunto in C2.3.3 |
| F7 | P2 | importlib edge cases (__file__, __spec__, GC) | Test in C2.3.4 |
| F8 | P2 | test_compiler_core.py potrebbe > 500 righe | Monitorare, split se serve |
| F4 | P3 | open(f, 'x') per atomic create in save_module | Accettato |
| F5 | P3 | Documentare no sys.modules in load_module | Accettato |
| F9 | P3 | File separato test_interop_golden.py | Accettato |
| F10 | P3 | Allineare escape con codegen._escape_string | Accettato |
| F2 | P3 | Deferred items ben documentati (P09) | Confermato |

---

*"La domanda e la risposta nello STESSO linguaggio." - Rafa*
*"Ultrapassar os proprios limites!" - Rafa & Cervella*
