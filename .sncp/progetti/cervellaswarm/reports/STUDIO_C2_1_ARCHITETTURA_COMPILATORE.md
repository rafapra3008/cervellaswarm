# STUDIO C2.1 - Architettura del Compilatore

> **Data:** 2026-02-27 - Sessione 412
> **Autore:** Cervella Regina (analisi codebase) + Cervella Researcher (ricerca esterna)
> **Status:** PROPOSTA PER GUARDIANA
> **Input:** 8 moduli letti (4330 LOC src), 18 fonti esterne, grammar EBNF (62 produzioni)
> **Zero nuove dipendenze.**

---

## 1. IL GAP: Cosa manca tra C1 e C2

### Oggi abbiamo DUE pipeline separate

```
PIPELINE A (ESISTENTE - Fase A+B):
  Python Protocol objects -> codegen.py -> Python module
  [spec.py verifica]  [checker.py enforces runtime]  [lean4_bridge.py proves]

PIPELINE B (NUOVA - Fase C):
  Source .lu -> tokenize -> parse -> ProgramNode AST -> ??? -> Python module
  [C1 DONE]                                             [C2 = QUESTO]
```

### Il compilatore C2 collega Pipeline B

```
ProgramNode AST
    |
    v
ASTCompiler (_compiler.py)    ← NUOVO
    |
    +-- UseNode        -> import statements
    +-- TypeDecl       -> Python class / type alias
    +-- AgentNode      -> Python class + contratti runtime
    +-- ProtocolNode   -> SessionChecker setup (riusa codegen.py logic)
    |
    v
Python source string + source annotations
    |
    v
CompiledModule (result type)
```

---

## 2. DECISIONI ARCHITETTURALI

### D1: String Emission + Visitor Dispatch (non ast.Module)

**Scelta:** Generare stringhe Python, come `codegen.py` gia fa.

**Perche:**
- `codegen.py` (730 LOC) gia usa string emission con successo
- Output leggibile per debug (vs `ast.unparse()` che produce one-liner)
- Cython, Coconut usano lo stesso pattern
- Zero complessita aggiuntiva rispetto a `ast.Module`

**Validazione:** `compile(source, filename, "exec")` dopo ogni compilazione.

### D2: Contratti come `raise ContractViolation` (non assert, non decoratori)

**Scelta:** `if not condition: raise ContractViolation(...)` inline.

**Perche:**
- `assert` si disabilita con `python -O` (inaccettabile per contratti di sicurezza)
- Decoratori `icontract`/`deal` aggiungono dipendenza esterna (viola zero-deps)
- `raise` inline e: non disabilitabile, tracciabile (source loc), zero-deps
- Overhead: ~0 quando il contratto passa (una branch prediction)

### D3: Source Annotations via commenti inline `# [LU:line:col]`

**Scelta:** Commenti `# [LU:15:4]` su ogni blocco generato.

**Perche:**
- Il nostro AST ha `Loc(line, col)` su OGNI nodo - zero lavoro aggiuntivo
- Coconut usa lo stesso pattern
- Leggibile, greppabile, zero-deps
- `ContractViolation` include `source="line 17, col 8"` per tracciamento errori

### D4: Non toccare `codegen.py` - il compilatore e SEPARATO

**Scelta:** File nuovo `_compiler.py`. `codegen.py` resta intatto.

**Perche:**
- `codegen.py` lavora su `Protocol` objects (Python API)
- `_compiler.py` lavora su `ProgramNode` AST (da parser C1)
- Sono pipeline diverse. Non mescolare.
- Per `ProtocolNode` AST: costruire `Protocol` object internamente, poi delegare a `codegen.py`

### D5: Testing progressivo - Golden files, poi round-trip, poi Hypothesis

**Scelta:** 3 livelli progressivi.

1. **Golden files** - output snapshot reviewable in git
2. **Round-trip exec** - 10 esempi canonici: parse -> compile -> exec -> verify
3. **Property-based** - Hypothesis per invarianti del compilatore

---

## 3. FILE NUOVI (2 file, 0 modifiche a esistenti)

### 3.1 `_contracts.py` (~30 LOC)

```python
class ContractViolation(RuntimeError):
    """Raised when a Lingua Universale contract is violated at runtime.

    Attributes:
        condition: The contract expression that failed (human readable).
        kind: "requires" or "ensures".
        source: Source location string "line N, col M" from .lu file.
    """
    condition: str
    kind: str  # "requires" | "ensures"
    source: str

    def __init__(self, condition: str, kind: str = "requires", source: str = ""):
        self.condition = condition
        self.kind = kind
        self.source = source
        msg = f"[LU Contract] {kind} violated: {condition}"
        if source:
            msg += f" (at {source})"
        super().__init__(msg)
```

### 3.2 `_compiler.py` (~400-600 LOC stimato)

```python
@dataclass(frozen=True)
class CompiledModule:
    """Result of compiling a ProgramNode to Python."""
    source_file: str           # nome .lu originale
    python_source: str         # codice Python generato
    agents: tuple[str, ...]    # nomi agenti compilati
    protocols: tuple[str, ...] # nomi protocolli compilati
    imports: tuple[str, ...]   # moduli importati

class ASTCompiler:
    """Compiles ProgramNode AST -> Python source string.

    Architecture: isinstance-based visitor dispatch, string emission.
    Each declaration type has a dedicated _compile_X method.
    """

    def compile(self, program: ProgramNode, source_file: str = "<input>") -> CompiledModule:
        """Main entry point. Compiles entire program."""
        ...

    # --- Declaration dispatch ---
    def _compile_declaration(self, decl: Declaration) -> list[str]: ...

    # --- UseNode -> import statement ---
    def _compile_use(self, node: UseNode) -> list[str]:
        # use math -> import math
        # use datetime as dt -> import datetime as dt
        ...

    # --- TypeDecl -> Python types ---
    def _compile_variant_type(self, node: VariantTypeDecl) -> list[str]:
        # type Status = Active | Inactive
        # -> Status = Literal["Active", "Inactive"]  (o Enum)
        ...

    def _compile_record_type(self, node: RecordTypeDecl) -> list[str]:
        # type TaskData:
        #     name: String
        #     priority: Number
        # -> @dataclass(frozen=True) class TaskData: ...
        ...

    # --- AgentNode -> Python class + contratti ---
    def _compile_agent(self, node: AgentNode) -> list[str]:
        # agent Worker:
        #     role: backend
        #     trust: standard
        #     requires: input.is_valid
        #     ensures: result.quality > 0
        # -> class Worker: ... with ContractViolation checks
        ...

    # --- ProtocolNode -> SessionChecker setup ---
    def _compile_protocol(self, node: ProtocolNode) -> list[str]:
        # Internamente: costruisce Protocol object, poi genera setup code
        # Riusa la logica di codegen.py dove possibile
        ...

    # --- Expr -> Python string ---
    def _expr_to_python(self, expr: Expr) -> str:
        """Convert any Expr AST node to a Python expression string."""
        # IdentExpr("x") -> "x"
        # AttrExpr("input", "valid") -> "input.valid"
        # BinOpExpr(l, "and", r) -> "(l) and (r)"
        # NotExpr(e) -> "not (e)"
        # MethodCallExpr("tests", "pass", []) -> "tests.pass_()"
        # NumberExpr("42") -> "42"
        # StringExpr('"hello"') -> '"hello"'
        # GroupExpr(e) -> "(e)"
        ...

    # --- TypeExpr -> Python type hint ---
    def _type_to_python(self, tex: TypeExpr) -> str:
        # SimpleType("String", optional=False) -> "str"
        # SimpleType("Number", optional=True) -> "Optional[float]"
        # GenericType("List", arg, optional=False) -> "list[str]"
        # GenericType("Confident", arg) -> "Confident[str]"
        ...

    # --- Source annotation ---
    def _loc_comment(self, loc: Loc) -> str:
        return f"# [LU:{loc.line}:{loc.col}]"
```

---

## 4. MAPPING COMPLETO AST -> Python

### 4.1 Dichiarazioni

| AST Node | Python Generato |
|----------|----------------|
| `UseNode("math", None)` | `import math` |
| `UseNode("datetime", "dt")` | `import datetime as dt` |
| `VariantTypeDecl("Status", ("Active","Inactive"))` | `Status = Literal["Active", "Inactive"]` |
| `RecordTypeDecl("TaskData", fields)` | `@dataclass(frozen=True) class TaskData: ...` |
| `AgentNode("Worker", ...)` | `class Worker: ...` + contratti |
| `ProtocolNode("DelegateTask", ...)` | Protocol + SessionChecker setup |

### 4.2 Espressioni

| Expr AST | Python |
|----------|--------|
| `IdentExpr("x")` | `x` |
| `NumberExpr("42")` | `42` |
| `StringExpr('"hello"')` | `"hello"` |
| `AttrExpr("input", "valid")` | `input.valid` |
| `MethodCallExpr("tests", "pass", [x])` | `tests.pass_(x)` |
| `BinOpExpr(a, "and", b)` | `(a) and (b)` |
| `BinOpExpr(a, ">=", b)` | `(a) >= (b)` |
| `NotExpr(e)` | `not (e)` |
| `GroupExpr(e)` | `(e)` |

### 4.3 Type expressions

| TypeExpr AST | Python |
|-------------|--------|
| `SimpleType("String", False)` | `str` |
| `SimpleType("Number", False)` | `float` |
| `SimpleType("Boolean", False)` | `bool` |
| `SimpleType("String", True)` | `Optional[str]` |
| `GenericType("List", SimpleType("String"), False)` | `list[str]` |
| `GenericType("Confident", SimpleType("Number"), False)` | `Confident[float]` |

### 4.4 Agent compilation (il cuore)

**Input Lingua Universale:**
```
agent Worker:
    role: backend
    trust: standard
    accepts: TaskRequest
    produces: TaskResult
    requires:
        input.is_valid
        input.size > 0
    ensures:
        result.quality >= 0.8
```

**Output Python generato:**
```python
# [LU:1:0] agent Worker
class Worker:
    """Agent 'Worker' - compiled from Lingua Universale."""
    __lu_role__ = "backend"
    __lu_trust__ = "standard"
    __lu_accepts__ = ("TaskRequest",)
    __lu_produces__ = ("TaskResult",)

    def process(self, input):
        # [LU:6:8] requires: input.is_valid
        if not (input.is_valid):
            raise ContractViolation("input.is_valid", kind="requires", source="line 6, col 8")
        # [LU:7:8] requires: input.size > 0
        if not ((input.size) > (0)):
            raise ContractViolation("input.size > 0", kind="requires", source="line 7, col 8")
        _result = self._execute(input)
        # [LU:9:8] ensures: result.quality >= 0.8
        if not ((_result.quality) >= (0.8)):
            raise ContractViolation("result.quality >= 0.8", kind="ensures", source="line 9, col 8")
        return _result

    def _execute(self, input):
        """Override this method to implement agent logic."""
        raise NotImplementedError("Worker._execute must be implemented")
```

---

## 5. PIANO DI IMPLEMENTAZIONE (Sub-step C2.2)

| Sub-step | Cosa | Effort | Dipende da |
|----------|------|--------|------------|
| C2.2.1 | `_contracts.py` + test | 0.5 sess | nulla |
| C2.2.2 | `_compiler.py` core: `_expr_to_python`, `_type_to_python`, `_compile_use` | 1 sess | C2.2.1 |
| C2.2.3 | `_compile_variant_type`, `_compile_record_type` | 0.5 sess | C2.2.2 |
| C2.2.4 | `_compile_agent` (il cuore: contratti + metadata) | 1-2 sess | C2.2.2 |
| C2.2.5 | `_compile_protocol` (bridge a codegen.py) | 1 sess | C2.2.3, C2.2.4 |
| C2.2.6 | Golden file tests + round-trip exec per 10 esempi canonici | 1 sess | C2.2.5 |
| C2.2.7 | Guardiana audit finale C2.2 | 0.5 sess | C2.2.6 |

**Effort totale C2.2:** ~5-7 sessioni
**Guardiana dopo ogni sub-step** (pattern confermato x11)

---

## 6. RISCHI E MITIGAZIONI

| Rischio | Impatto | Mitigazione |
|---------|---------|-------------|
| Precedenza operatori sbagliata in `_expr_to_python` | Codice generato semanticamente diverso | Parentesizzare SEMPRE: `(left) op (right)` |
| `ProtocolNode` duplica codegen.py | Maintenance burden | Costruire `Protocol` object dal `ProtocolNode`, poi delegare |
| `MethodCallExpr` con keyword Python (`pass`, `class`) | SyntaxError nel generato | Usare `_safe_python_ident` da codegen.py (suffisso `_`) |
| `ensures` deve accedere al risultato | Pattern diverso da requires | Variabile `_result = self._execute(input)` prima di verificare |
| File generati non importabili | Errori runtime | `compile(source, "test", "exec")` come test post-generation |

---

## 7. COME SI COLLEGA AL RESTO

```
FASE A+B (13 moduli, 1820 test):
  types.py ──────────────────────────────┐
  protocols.py ──────────────────────────┤
  checker.py ────────────────────────────┤
  codegen.py ───── PythonGenerator ──────┤
  spec.py ───── check_properties ────────┤
  lean4_bridge.py ── VerificationResult ─┤
  integration.py ── agent catalog ───────┤
  ...                                    │
                                         v
FASE C1 (parser):                    FASE C2 (compilatore):
  _tokenizer.py                        _contracts.py (ContractViolation)
  _ast.py ────── ProgramNode ───────>  _compiler.py (ASTCompiler)
  _parser.py                               |
                                           v
                                       CompiledModule
                                           |
                                       Python source con:
                                       - import statements
                                       - typed classes
                                       - contratti runtime
                                       - SessionChecker setup
                                       - source annotations [LU:N:M]
```

**Il compilatore CONNETTE C1 (parser) con A+B (runtime). Non rimpiazza nulla.**

---

*"La domanda e la risposta nello STESSO linguaggio." - Rafa*
*Report basato su: 8 moduli (4330 LOC), 18 fonti esterne, grammar EBNF (62 produzioni)*
