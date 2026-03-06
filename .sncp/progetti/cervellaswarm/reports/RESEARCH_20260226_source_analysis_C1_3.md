# RICERCA: Analisi Sorgente per Step C1.3 (Parser Unificato)

> **Data:** 2026-02-26
> **Ricercatrice:** Cervella Researcher
> **Scope:** Analisi completa `packages/lingua-universale/src/cervellaswarm_lingua_universale/`
> **Obiettivo:** Preparare C1.3 con dati concreti su riuso, duplicazioni, gap

---

## SEZIONE 1: INVENTARIO COMPLETO DEI FILE

Package path: `/Users/rafapra/Developer/CervellaSwarm/packages/lingua-universale/src/cervellaswarm_lingua_universale/`

| File | LOC (stimato) | Ruolo nel Linguaggio |
|------|---------------|---------------------|
| `__init__.py` | 280 | Esporta tutto il pubblico API - 13 moduli esportati |
| `intent.py` | 650 | **PARSER BASE** - sintassi naturale Python-like |
| `spec.py` | 1243 | **PARSER PROPRIETÀ** - checking statico + runtime |
| `dsl.py` | 494 | Parser/renderer Scribble-like (diventa export format) |
| `protocols.py` | 309 | AST core: Protocol, ProtocolStep, ProtocolChoice |
| `types.py` | ~471 | Enums: MessageKind (14), AgentRole (17), TaskStatus |
| `checker.py` | ~524 | SessionChecker - enforcement runtime |
| `confidence.py` | 178 | Confident[T], ConfidenceScore, CompositionStrategy |
| `trust.py` | 168 | TrustTier, TrustScore, compose_chain |
| `errors.py` | ~1784 | Messaggi errori umani EN+IT+PT |
| `codegen.py` | ~730 | Generazione Python da Protocol |
| `lean4_bridge.py` | ~672 | Generazione Lean 4 per verifica formale |
| `monitor.py` | ~473 | ProtocolMonitor, EventCollector |
| `integration.py` | ~497 | Pipeline completa + AGENT_CATALOG |

**TOTALE SORGENTE:** ~8.473 LOC in 13 moduli + 280 LOC `__init__.py`

---

## SEZIONE 2: ANALISI DEI FILE CRITICI

### 2.1 `intent.py` - IL FILE PIU IMPORTANTE

**LOC:** 650
**Pattern di parsing:** Recursive descent + pattern matching sui token

**Classi e funzioni principali:**
```python
class IntentParseError(Exception)       # Errore con numero di riga
class IntentParseResult(frozen dataclass) # protocol + source_text + warnings

_ACTION_MAP: dict[tuple[str,...], MessageKind]  # 14 entry: mapping deterministic
_KIND_TO_ACTION: dict[MessageKind, tuple]       # reverse map (per future render)

class _TokKind(Enum)      # WORD, COLON, COMMA, NEWLINE, INDENT, EOF
class _Tok(frozen dataclass)   # kind, value, line

def _tokenize_intent(source: str) -> list[_Tok]   # ~70 LOC
class _IntentParser:                               # ~300 LOC
    def parse(self) -> Protocol
    def _parse_roles(self) -> list[str]
    def _parse_elements(self, base_indent: int) -> list[ProtocolElement]
    def _parse_step(self) -> ProtocolStep
    def _resolve_step(sender, words, line) -> ProtocolStep  # CUORE: pattern matching
    def _parse_choice(self, parent_indent: int) -> ProtocolChoice
    def _parse_branch_steps(self, step_indent: int) -> list[ProtocolStep]
    # Utility: _peek, _advance, _expect_word, _expect, _skip_newlines
    # Indent: _count_indents, _peek_indent_level, _skip_indents

def _try_match_action(words, action) -> str | None  # match + estrai receiver
def _format_valid_actions() -> str                  # per error messages

def parse_intent(source: str) -> IntentParseResult  # PUBLIC API
def parse_intent_protocol(source: str) -> Protocol  # convenience
```

**Tokenizer (70 LOC) - Come funziona:**
- `textwrap.dedent()` applicato prima (gestisce triple-quoted strings)
- Processa riga per riga: ogni riga produce INDENT tokens (1 per 4 spazi) + content tokens
- Tabs RIFIUTATI con errore esplicito
- Blank lines e commenti `#` SALTATI
- Regex `[A-Za-z_][A-Za-z0-9_]*` per WORD
- Solo `:` e `,` come simboli (non `>=`, non `[`, non `|`, non `?`)

**`_resolve_step` - il cuore della logica:**
```python
# Greedy match: prova ogni pattern in _ACTION_MAP
# L'unica parola NON nel pattern = il receiver
# words = ["asks", "backend", "to", "do", "task"]
# action = ("asks", "to", "do", "task")
# receiver = "backend"  (la parola "mancante")
```

**Dipendenze:**
- Interne: `protocols` (Protocol, ProtocolStep, ProtocolChoice, ProtocolElement), `types` (MessageKind)
- Esterne: `re`, `textwrap`, `dataclasses`, `enum` (solo stdlib)

**LIMITAZIONI ATTUALI per v0.2:**
1. Tokenizer non gestisce `>=`, `[`, `]`, `|`, `?`, `.`, `(`, `)`, `=`, `NUMBER`, `STRING`
2. Parser gestisce UN SOLO `protocol` per sorgente (no `program ::= declaration*`)
3. Non gestisce `agent`, `type`, `use`, `requires`, `ensures`
4. `_TokKind` privato - non riusabile direttamente senza refactor

---

### 2.2 `spec.py` - IL PIU MATURO (1243 LOC)

**LOC:** 1243
**Pattern di parsing:** Recursive descent, indent-aware

**Classi e funzioni principali:**
```python
class SpecParseError(Exception)   # con numero di riga

class PropertyKind(Enum)          # 7 valori: ALWAYS_TERMINATES, NO_DEADLOCK,
                                   # ORDERING, EXCLUSION, CONFIDENCE_MIN,
                                   # TRUST_MIN, ALL_ROLES_PARTICIPATE
class PropertyVerdict(Enum)       # PROVED, SATISFIED, VIOLATED, SKIPPED
class PropertySpec(frozen dataclass)  # kind + params + threshold
class ProtocolSpec(frozen dataclass)  # protocol_name + properties
class PropertyResult(frozen dataclass) # spec + verdict + evidence
class PropertyReport(frozen dataclass) # all_passed, passed_count, violated_count

# Tokenizer (quasi identico a intent.py, ma con GTE invece di COMMA)
class _TokKind(Enum)    # WORD, COLON, GTE, NEWLINE, INDENT, EOF
class _Tok(frozen dataclass)
def _tokenize_spec(source: str) -> list[_Tok]   # ~70 LOC

# Parser
class _SpecParser:
    def parse(self) -> ProtocolSpec
    def _parse_properties(self) -> list[PropertySpec]
    def _parse_property_body(self, line: int) -> PropertySpec
    def _parse_always_terminates(self) -> PropertySpec
    def _parse_no_deadlock(self) -> PropertySpec
    def _parse_all_roles_participate(self) -> PropertySpec
    def _parse_confidence_min(self) -> PropertySpec
    def _parse_trust_min(self) -> PropertySpec
    def _parse_ident_property(self) -> PropertySpec  # ORDERING o EXCLUSION
    def _parse_ordering(self, first_tok) -> PropertySpec
    def _parse_exclusion(self, role_tok) -> PropertySpec

# Static checker (5 funzioni)
def _collect_all_paths(elements) -> list[list[ProtocolStep]]
def _check_always_terminates_static(protocol) -> PropertyResult
def _check_no_deadlock_static(protocol) -> PropertyResult
def _check_ordering_static(protocol, spec) -> PropertyResult
def _check_exclusion_static(protocol, spec) -> PropertyResult
def _check_trust_min_static(protocol, spec) -> PropertyResult
def _check_all_roles_participate_static(protocol, spec) -> PropertyResult

# Runtime checker (3 funzioni)
def _check_ordering_runtime(log, spec) -> PropertyResult
def _check_exclusion_runtime(log, spec) -> PropertyResult
def _check_all_roles_participate_runtime(log, spec, protocol_roles) -> PropertyResult

# Dispatcher
def check_properties(protocol, spec) -> PropertyReport   # STATIC
def check_session(log, spec, protocol=None) -> PropertyReport  # RUNTIME

# Public API
def parse_spec(source: str) -> ProtocolSpec
```

**Costanti chiave (riusabili):**
```python
_CONFIDENCE_LEVELS = MappingProxyType({
    "certain": 1.0, "high": 0.8, "medium": 0.5, "low": 0.2, "speculative": 0.1,
})
_TRUST_TIER_MAP = MappingProxyType({...})
_TRUST_TIER_ORDER = MappingProxyType({...})
_VALUE_TO_KIND = MappingProxyType({k.value: k for k in MessageKind})
_VALUE_TO_ROLE = MappingProxyType({r.value: r for r in AgentRole})
```

**Dipendenze:**
- Interne: `protocols`, `types` (AgentRole, MessageKind), `checker` (MessageRecord), `trust` (TrustTier, trust_tier_for_role)
- Esterne: `re`, `textwrap`, `dataclasses`, `enum`, `types.MappingProxyType` (solo stdlib)

---

### 2.3 `dsl.py` - IL FORMATO EXPORT (494 LOC)

**LOC:** 494
**Pattern:** Regex-based tokenizer + recursive descent parser + renderer

**Differenza chiave dal tokenizer di intent.py/spec.py:**
- USA `re.compile("|".join(...))` - master regex su tutto il sorgente
- NON è line-oriented (non ha logica indent)
- Gestisce `->`, `{`, `}`, `;`, `,`, `:` e NUMBER
- Più simile a un tokenizer classico (line/col tracking)

```python
class DSLParseError(DSLError)  # con line + col (NON solo line come gli altri!)

_TOKEN_SPEC = [...]  # lista di (name, regex)
_MASTER_RE = re.compile(...)  # una regex per tutto

def _tokenize(source: str) -> list[_Token]   # regex-based, non line-oriented

class _Parser:
    def parse_protocol(self) -> Protocol
    def _parse_max_repetitions(self) -> int | None
    def _parse_roles(self) -> list[str]
    def _parse_elements(self) -> list[ProtocolElement]
    def _parse_step(self) -> ProtocolStep
    def _parse_choice(self) -> ProtocolChoice
    def _parse_branch(self) -> tuple[str, list[ProtocolStep]]

# MessageKind <-> PascalCase
_NAME_TO_KIND: dict[str, MessageKind]   # "TaskRequest" -> TASK_REQUEST
_KIND_TO_NAME: dict[MessageKind, str]   # TASK_REQUEST -> "TaskRequest"
def _message_kind_from_name(name, line, col) -> MessageKind
def _message_kind_to_name(kind) -> str

# Renderer (UNICO tra i parser!)
def render_protocol(protocol: Protocol) -> str
def render_protocols(protocols) -> str
def _render_element(elem, lines, indent) -> None
def _render_step(step, lines, prefix) -> None
def _render_choice(choice, lines, indent) -> None

# Public API
def parse_protocol(source: str) -> Protocol
def parse_protocols(source: str) -> list[Protocol]
```

**Nota IMPORTANTE per C1.3:** dsl.py è il SOLO modulo con un **renderer** (Protocol -> testo). Il parser unificato avrà bisogno di un renderer per Scribble export - questo codice è riusabile.

---

### 2.4 `protocols.py` - L'AST CORE (309 LOC)

```python
@dataclass(frozen=True)
class ProtocolStep:
    sender: str
    receiver: str
    message_kind: MessageKind
    description: str = ""
    # __post_init__: valida sender != receiver, entrambi non vuoti

@dataclass(frozen=True)
class ProtocolChoice:
    decider: str
    branches: Mapping[str, tuple[ProtocolStep, ...]]
    description: str = ""
    # __post_init__: rende branches immutable via MappingProxyType

ProtocolElement = ProtocolStep | ProtocolChoice

@dataclass(frozen=True)
class Protocol:
    name: str
    roles: tuple[str, ...]
    elements: tuple[ProtocolElement, ...]
    max_repetitions: int = 1
    description: str = ""
    # __post_init__: valida ruoli, max_rep >= 1, sender/receiver in roles

# 4 protocolli standard hardcoded: DelegateTask, ArchitectFlow, ResearchFlow, SimpleTask
STANDARD_PROTOCOLS: Mapping[str, Protocol] = MappingProxyType({...})
```

**Nota per C1.3:** `protocols.py` è l'**AST attuale** - ma è incompleto per v0.2. Il parser unificato produrrà nodi AST NUOVI: `AgentDecl`, `TypeDecl`, `UseDecl`, `RequiresClause`, `EnsuresClause`, `Condition`, `Expr`. Questi NON esistono ancora.

---

### 2.5 `__init__.py` - COSA ESPORTA (280 LOC)

Esporta **tutto** il pubblico API in un unico namespace:
- `types`: AgentRole, MessageKind, TaskStatus, AuditVerdictType, PlanComplexity + 14 message dataclasses
- `protocols`: Protocol, ProtocolStep, ProtocolChoice, ProtocolElement, 4 standard protocols
- `checker`: MessageRecord, ProtocolViolation, SessionChecker, SessionComplete, SessionState
- `dsl`: parse_protocol, parse_protocols, render_protocol, render_protocols
- `monitor`: 10 classi/funzioni monitor
- `lean4_bridge`: Lean4Generator, Lean4Verifier, generate_lean4
- `integration`: AgentInfo, AGENT_CATALOG, create_session, validate_swarm
- `confidence`: ConfidenceScore, Confident, CompositionStrategy, compose_scores
- `trust`: TrustTier, TrustScore, trust_tier_for_role, compose_chain
- `codegen`: GeneratedCode, PythonGenerator, generate_python
- `intent`: parse_intent, parse_intent_protocol, IntentParseResult, IntentParseError
- `spec`: PropertyKind, PropertySpec, ProtocolSpec, parse_spec, check_properties, check_session
- `errors`: HumanError, humanize, format_error

**__all__** esplicito con ~80 nomi. Zero simboli privati esportati.

---

### 2.6 `confidence.py` (178 LOC) e `trust.py` (168 LOC)

Già descritti nel C1.1 STUDIO. Punti chiave per C1.3:
- `Confident[T]`: Generic Python class, non keyword. Il parser unificato dovrà riconoscere `Confident` come tipo speciale nella grammatica `type_expr`.
- `TrustTier`: enum con 4 valori ("verified", "trusted", "standard", "untrusted") - già usati come terminali nella grammatica EBNF v0.2.
- `_CONFIDENCE_LEVELS` in spec.py è già il mapping corretto per il parser unificato.

---

## SEZIONE 3: CODICE DUPLICATO

Questo è il punto più critico per C1.3.

### Duplicazione IDENTICA tra `intent.py` e `spec.py`

**Tokenizer base (~65 LOC identiche):**
```python
# DUPLICATO in intent.py e spec.py (quasi identico):
class _TokKind(Enum):  # diversi solo nei valori: intent ha COMMA, spec ha GTE
class _Tok(frozen dataclass):
    kind: _TokKind
    value: str
    line: int

_WORD_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")

def _tokenize_XYZ(source: str) -> list[_Tok]:
    tokens = []
    source = textwrap.dedent(source)
    lines = source.split("\n")
    for line_no, raw_line in enumerate(lines, start=1):
        if "\t" in raw_line: raise ...
        stripped = raw_line.rstrip()
        if not stripped or stripped.lstrip().startswith("#"): continue
        leading = len(stripped) - len(stripped.lstrip())
        indent_level = leading // 4
        if leading % 4 != 0 and leading > 0: raise ...
        for _ in range(indent_level):
            tokens.append(_Tok(_TokKind.INDENT, "    ", line_no))
        # tokenize content...
    tokens.append(_Tok(_TokKind.EOF, "", len(lines)))
    return tokens
```

**Parser utility (~40 LOC identiche):**
```python
# DUPLICATO in _IntentParser e _SpecParser:
def _peek(self) -> _Tok
def _advance(self) -> _Tok
def _expect_word(self, value=None) -> _Tok
def _expect(self, kind, value=None) -> _Tok
def _skip_newlines(self) -> None
def _count_indents(self) -> int
def _peek_indent_level(self) -> int
```

**Stima duplicazione:**
- ~105 LOC identiche tra intent.py e spec.py (tokenizer + parser utilities)
- Pari a circa 16% del codice di intent.py e 8% di spec.py

### Differenze tra i tokenizer (da unificare)

| Token | intent.py | spec.py | dsl.py | Serve in v0.2 |
|-------|-----------|---------|--------|---------------|
| WORD | YES | YES | YES (IDENT) | YES |
| COLON | YES | YES | YES | YES |
| COMMA | YES | NO | YES | YES |
| GTE | NO | YES | NO | YES |
| INDENT | YES | YES | NO | YES |
| NEWLINE | YES | YES | NO (skipped) | YES |
| ARROW | NO | NO | YES | NO (no `->` in v0.2) |
| LBRACE/RBRACE | NO | NO | YES | NO |
| SEMICOLON | NO | NO | YES | NO |
| NUMBER | NO | NO | YES | YES (per `tests.pass(80)`) |
| STRING | NO | NO | NO | YES (per `"2.0"`) |
| LBRACKET/RBRACKET | NO | NO | NO | YES (per `List[T]`) |
| PIPE | NO | NO | NO | YES (per `a \| b`) |
| QUESTION | NO | NO | NO | YES (per `String?`) |
| DOT | NO | NO | NO | YES (per `task.well_defined`) |
| LPAREN/RPAREN | NO | NO | NO | YES (per `tests.pass(80)`) |
| EQUALS | NO | NO | NO | YES (per `type X =`) |
| LTE, EQ, NEQ, GT, LT | NO | NO | NO | YES (per expressions) |

---

## SEZIONE 4: PATTERN COMUNI (RIUSABILI)

### Pattern P1: Tokenizer Indent-Aware (RIUSABILE, ~70 LOC)
Presente in intent.py e spec.py. Da estrarre in `_tokenize_unified()`:
- `textwrap.dedent()` first
- Line-by-line processing
- Tab rejection
- 4-space indent level counting -> INDENT tokens
- Comment `#` skipping
- Blank line skipping
- NEWLINE token per ogni riga non vuota
- EOF finale

**Estensione necessaria:** aggiungere lexer per `>=`, `<=`, `==`, `!=`, `>`, `<`, `[`, `]`, `|`, `?`, `.`, `(`, `)`, `=`, NUMBER, STRING

### Pattern P2: Parser Base Class (RIUSABILE, ~40 LOC)
```python
class _BaseParser:
    def __init__(self, tokens): self._tokens = tokens; self._pos = 0
    def _peek(self) -> _Tok
    def _advance(self) -> _Tok
    def _expect_word(self, value=None) -> _Tok
    def _expect(self, kind, value=None) -> _Tok
    def _skip_newlines(self) -> None
    def _count_indents(self) -> int
    def _peek_indent_level(self) -> int
    def _skip_indents(self) -> None
```

### Pattern P3: Error con Line Info (RIUSABILE)
```python
class ParseError(Exception):
    def __init__(self, message: str, line: int = 0) -> None:
        self.line = line
        loc = f"line {line}" if line else "unknown location"
        super().__init__(f"{loc}: {message}")
```
Identico in intent.py (`IntentParseError`) e spec.py (`SpecParseError`). Da unificare.

### Pattern P4: Result Dataclass (RIUSABILE)
```python
@dataclass(frozen=True)
class ParseResult:
    # Il pattern IntentParseResult è buono:
    ast: SomeNode
    source_text: str
    warnings: tuple[str, ...] = ()
```

### Pattern P5: _resolve_step con greedy pattern matching (RIUSABILE IN PARTE)
Il meccanismo di `_try_match_action` è elegante: prova ogni pattern, trova il receiver come "parola mancante". Va mantenuto per i passi del protocol. **Ma non serve per i nuovi costrutti** (agent, type, use, requires/ensures usano struttura deterministica LL(1)).

### Pattern P6: Lookup tables immutabili (RIUSABILE)
```python
_CONFIDENCE_LEVELS = MappingProxyType({...})  # spec.py
_TRUST_TIER_MAP = MappingProxyType({...})      # spec.py
_VALUE_TO_KIND = MappingProxyType({...})       # spec.py
_ACTION_MAP = {...}                             # intent.py
```
Tutte queste costanti vanno nel parser unificato.

### Pattern P7: Renderer (dsl.py, DA ADATTARE)
```python
def render_protocol(protocol: Protocol) -> str  # DSL brace-style
```
Serve un `render_intent(protocol: Protocol) -> str` in stile intent.py (indent, verbi naturali). Attualmente NON esiste (`# Reserved for future render_intent()` - commento in intent.py riga 129).

---

## SEZIONE 5: IDENTIFICAZIONE GAP

Questi elementi NON esistono nel codice attuale e devono essere CREATI da zero per C1.3.

### Gap G1: Tokenizer esteso per v0.2 (CRITICO)
I tokenizer attuali gestiscono solo: WORD, COLON, COMMA/GTE, INDENT, NEWLINE, EOF.
Mancano: NUMBER, STRING, LBRACKET, RBRACKET, PIPE, QUESTION, DOT, LPAREN, RPAREN, EQUALS, LTE, EQ, NEQ, GT, LT.
**Stima:** ~50 LOC aggiuntivi nel tokenizer unificato.

### Gap G2: Parser per top-level `program` (CRITICO)
Nessun parser attuale gestisce `program ::= declaration*`.
intent.py parsifica UN SOLO protocol.
spec.py parsifica UN SOLO spec block.
dsl.py parsifica protocolli multipli ma con sintassi diversa.
**Serve:** `parse_program(source: str) -> ProgramAST` - il nuovo entry point.
**Stima:** ~80 LOC per il dispatcher top-level.

### Gap G3: Nodi AST nuovi (CRITICO)
```python
# NON ESISTONO - da creare in un nuovo file `ast_nodes.py`:
@dataclass(frozen=True)
class AgentDecl:
    name: str
    clauses: tuple[AgentClause, ...]

@dataclass(frozen=True)
class TypeDecl:
    name: str
    variants: tuple[str, ...] | None       # per variant type
    fields: tuple[FieldDecl, ...] | None   # per record type

@dataclass(frozen=True)
class UseDecl:
    module: str        # dotted name
    alias: str | None

@dataclass(frozen=True)
class RequiresClause:
    conditions: tuple[Condition, ...]

@dataclass(frozen=True)
class EnsuresClause:
    conditions: tuple[Condition, ...]

@dataclass(frozen=True)
class Condition:
    expr: Expr    # arbitrario

# Expr gerarchia (or_expr, and_expr, not_expr, comparison, primary)
# Nessun nodo Expr esiste attualmente
```
**Stima:** ~100-120 LOC per i nodi AST + validation.

### Gap G4: Parser per `requires`/`ensures`/`agent`/`type`/`use` (CRITICO)
I metodi di parsing per questi costrutti non esistono in nessun file.
**Stima:** ~200-250 LOC.

### Gap G5: Parser per espressioni (CRITICO)
La grammatica v0.2 definisce `expr -> or_expr -> and_expr -> not_expr -> comparison -> primary`.
Nessun modulo parsifica espressioni. spec.py parsifica solo property keywords fissi.
**Stima:** ~120 LOC per il parser di espressioni.

### Gap G6: Properties inline nel protocol (MEDIO)
spec.py parsifica `properties for X:` come blocco separato.
v0.2 vuole `properties:` DENTRO `protocol_body`.
Il check attuale richiede che la spec abbia un `protocol_name` - con properties inline non serve più.
**Stima:** ~30 LOC di adattamento.

### Gap G7: Renderer intent-style (MEDIO)
Non esiste `render_intent()` (solo `render_protocol()` in stile DSL brace).
`_KIND_TO_ACTION` esiste in intent.py (riga 130) ma è commentato "Reserved for future".
**Stima:** ~60 LOC per renderer intent-style.

### Gap G8: Error system esteso (BASSO)
errors.py già gestisce `IntentParseError` (LU-I) e `SpecParseError` (LU-S) e `DSLParseError` (LU-D).
Il parser unificato produrrà un nuovo tipo `UnifiedParseError` (nuovo codice LU-U?).
**Stima:** ~40 LOC in errors.py.

---

## SEZIONE 6: STIMA RIUSO

### Codice DIRETTAMENTE RIUSABILE (stima ~55%)

| Componente | Da dove | LOC stimati | Note |
|------------|---------|-------------|------|
| Pattern tokenizer base | intent.py + spec.py | ~70 | Da unificare in 1 |
| Parser base class (_peek, _advance, _expect, etc.) | intent.py + spec.py | ~40 | Da estrarre |
| `_parse_roles()` | intent.py | ~15 | Identico |
| `_parse_elements()` / `_parse_choice()` | intent.py | ~100 | Con piccoli adattamenti |
| `_parse_step()` + `_resolve_step()` + `_try_match_action()` | intent.py | ~80 | Con `action` esteso (EBNF) |
| `_ACTION_MAP` + 14 verbi | intent.py | ~20 | Aggiungere `proposes` (già fixato v0.2) |
| Parsing properties (tutti e 7 tipi) | spec.py | ~200 | Con adattamento inline |
| `_collect_all_paths()` | spec.py | ~30 | Invariato |
| Static/runtime checkers (5+3 funzioni) | spec.py | ~200 | Invariati |
| `_CONFIDENCE_LEVELS`, `_TRUST_TIER_MAP`, lookup tables | spec.py | ~20 | Invariate |
| Renderer DSL (per Scribble export) | dsl.py | ~80 | Invariato |
| `_NAME_TO_KIND`, `_KIND_TO_NAME` | dsl.py | ~10 | Invariati |
| Error classes base | intent.py + spec.py + dsl.py | ~30 | Da unificare |
| `ParseError` base | tutti | ~10 | |

**TOTALE RIUSABILE:** ~905 LOC (su ~1200 LOC target del parser unificato) = **~55-60% riuso**

### Codice DA CREARE EX NOVO (~45%)

| Componente | Gap # | LOC stimati |
|------------|--------|-------------|
| Tokenizer esteso (nuovi token) | G1 | ~50 |
| Parser `program` top-level | G2 | ~80 |
| Nodi AST nuovi | G3 | ~120 |
| Parser agent/type/use/requires/ensures | G4 | ~250 |
| Parser espressioni | G5 | ~120 |
| Properties inline adattamento | G6 | ~30 |
| Renderer intent-style | G7 | ~60 |
| Error system esteso | G8 | ~40 |

**TOTALE NUOVO:** ~750 LOC

**Stima totale parser unificato:** ~1200-1300 LOC (coerente con stima Ingegnera ~1200 LOC).

---

## SEZIONE 7: ARCHITETTURA RACCOMANDATA PER C1.3

Sulla base dell'analisi, raccomando questa struttura:

### File da CREARE

```
packages/lingua-universale/src/cervellaswarm_lingua_universale/
    parser/                          # nuovo sotto-package
        __init__.py                  # pubblica UnifiedParser, parse_program
        _tokens.py                   # TokenKind enum + Token dataclass (unificato)
        _lexer.py                    # Tokenizer unificato (~120 LOC)
        _ast.py                      # Nodi AST nuovi: AgentDecl, TypeDecl, etc. (~120 LOC)
        _parser.py                   # Parser unificato (~700 LOC)
        _checker.py                  # Verifica statica sul nuovo AST (~100 LOC)
        _renderer.py                 # render_intent() + render_scribble() (~120 LOC)
```

**ALTERNATIVA:** un singolo `parser.py` (~1200 LOC) - più semplice, meno overhead.
Raccomando il singolo file per ora (coerente con le convenzioni attuali del codebase).

### Sequenza di implementazione raccomandata

1. `_tokens.py`: `TokenKind` unificato (tutti i 20+ token) + `Token` dataclass
2. `_lexer.py`: Tokenizer unificato da intent.py + spec.py + nuovi token
3. `_ast.py`: Nodi AST nuovi (aggiunge a protocols.py esistente)
4. `_parser.py` - BASE: `program`, `protocol_decl`, `agent_decl` (usa codice intent.py)
5. `_parser.py` - PROPERTIES: properties inline (usa codice spec.py)
6. `_parser.py` - NUOVI: `type_decl`, `use_decl`, `requires`/`ensures`
7. `_parser.py` - EXPR: parser espressioni (completamente nuovo)
8. Test: ~700 LOC (stima Ingegnera)

---

## SINTESI ESECUTIVA

**Status:** RICERCA COMPLETA
**Fonti:** 13 file sorgente letti, 2 report precedenti (C1.1 STUDIO + C1.2 DESIGN)

**5 punti chiave:**

1. **Il tokenizer è duplicato 2 volte** (intent.py + spec.py ~105 LOC identiche) - da unificare in C1.3 come prima azione.

2. **intent.py è il 55-60% del nuovo parser** - il tokenizer, il parser base, `_parse_elements`, `_parse_choice`, `_resolve_step` sono tutti riusabili quasi verbatim con piccoli adattamenti.

3. **spec.py contribuisce il check statico** - `_collect_all_paths` e tutte le funzioni di verifica proprietà sono riusabili as-is. Il solo adattamento: properties diventano inline nel protocol (tolto il `properties for X:` header).

4. **I nodi AST nuovi sono il vero lavoro nuovo** - `AgentDecl`, `TypeDecl`, `UseDecl`, `Condition`, `Expr` non esistono. Questo è ~120 LOC di design + ~250 LOC di parsing.

5. **Il parser di espressioni è il sottosistema più complesso** - nessun precedente nel codebase. La grammatica EBNF v0.2 ha 8 produzioni per expr (or_expr, and_expr, not_expr, comparison, primary, args). Stima ~120 LOC.

**Raccomandazione:** Iniziare C1.3 con il tokenizer unificato (step 1 e 2 della sequenza sopra) - è il fondamento di tutto e risolve la duplicazione esistente. Test-driven: scrivere i test del tokenizer prima del codice.

---

*Cervella Researcher - CervellaSwarm S409*
*"Ricerca PRIMA di implementare."*
