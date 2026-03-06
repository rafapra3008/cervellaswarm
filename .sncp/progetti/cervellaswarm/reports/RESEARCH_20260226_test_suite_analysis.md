# Test Suite Analysis - lingua-universale
## Analisi per C1.3 Parser Strategy

> **Data:** 2026-02-26
> **Ricercatrice:** Cervella Researcher
> **Status:** COMPLETA
> **Fonti:** 30 file test letti integralmente, src/ esaminato
> **Scope:** Pattern riutilizzabili per parser C1.3

---

## 1. INVENTARIO COMPLETO

### 1.1 File di test e conteggio

| File | Test count | Cosa testa |
|------|-----------|-----------|
| `test_intent_parse.py` | 36 | Intent parser happy paths (14 MessageKind, branching, whitespace) |
| `test_intent_edge.py` | 31 | Intent parser errors, edge cases, frozen dataclass |
| `test_spec_parse.py` | 36 | Spec parser happy paths (7 property kinds, confidence, trust) |
| `test_spec_core.py` | 50 | Spec dataclasses, PropertyReport, static checker |
| `test_spec_session.py` | 23 | Runtime checker check_session() |
| `test_dsl_parse.py` | 73 | DSL parser (tokenizer, parse, errors, roundtrip) |
| `test_dsl_render.py` | 33 | DSL renderer/render_protocol() |
| `test_checker_core.py` | 26 | SessionChecker happy paths, violations, log |
| `test_checker_flows.py` | 16 | Checker flows multi-branch |
| `test_confidence.py` | 108 | Confident[T], ConfidenceScore, compose |
| `test_trust.py` | 124 | TrustScore, TrustTier |
| `test_types_enums.py` | 11 | Enum completeness |
| `test_types_messages.py` | 46 | TaskRequest/TaskResult/etc dataclasses |
| `test_types_new_messages.py` | 42 | Nuovi tipi messaggio |
| `test_protocols_core.py` | 18 | Protocol, ProtocolStep, ProtocolChoice dataclasses |
| `test_protocols_standard.py` | 37 | Standard protocols (DelegateTask, ArchitectFlow, ecc) |
| `test_errors_core.py` | 67 | HumanError, ErrorCategory, format_error(), suggest_similar() |
| `test_errors_catalog.py` | 32 | Catalog integrity, codice LU-X### format |
| `test_errors_humanize.py` | 47 | humanize() per ProtocolViolation, DSLParseError, SpecParseError |
| `test_errors_humanize2.py` | 52 | humanize() per IntentParseError, ValueError, fallback |
| `test_codegen_core.py` | 80 | PythonGenerator, helper functions, compilabilità |
| `test_codegen_e2e.py` | 27 | End-to-end codegen |
| `test_lean4_bridge_core.py` | 151 | Lean4 bridge - generazione codice Lean |
| `test_lean4_bridge_integration.py` | 72 | Lean4 bridge - integrazione |
| `test_monitor_core.py` | 89 | ProtocolMonitor, EventCollector |
| `test_monitor_integration.py` | 45 | Monitor integration flows |
| `test_integration_core.py` | 101 | AgentInfo, AGENT_CATALOG, create_session, validate_swarm |
| `test_integration_flows.py` | 44 | Integration flow tests |
| `test_regression_s382.py` | 34 | Regression bugs S382 (12 bug fixes verificati) |
| `test_bug_hunt_9.py` | 30 | Bug hunt #9 fixes |
| **TOTALE** | **1581** | |

**Nota conteggio:** 1581 definizioni `def test_` contate da grep. La cifra 1820 del PROMPT_RIPRESA include probabilmente test parametrizzati esplosi (ogni parametro = 1 test eseguito).

### 1.2 Moduli sorgente esistenti

```
src/cervellaswarm_lingua_universale/
  intent.py      <- RIUSO DIRETTO per C1.3 (parser intent esistente)
  spec.py        <- RIUSO DIRETTO per C1.3 (parser spec esistente)
  dsl.py         <- Pattern tokenizer riutilizzabile
  checker.py     <- Downstream consumer dei parser
  protocols.py   <- AST target (Protocol, ProtocolStep, ProtocolChoice)
  types.py       <- MessageKind e tipi base
  confidence.py  <- Confident[T], ConfidenceScore (nuovi per C1.3)
  trust.py       <- TrustScore (nuovo per C1.3)
  errors.py      <- HumanError, humanize() - pattern di errore matura
  codegen.py     <- Downstream consumer
  lean4_bridge.py
  integration.py
  monitor.py
```

---

## 2. PATTERN DI TESTING RIUTILIZZABILI

### 2.1 Pattern A: Test per classi (organizzazione in classi tematiche)

Tutti i file esistenti usano classi pytest. Struttura canonica:

```python
class TestHappyPath:
    """Descrizione chiara dello scope."""
    def test_caso_base(self): ...
    def test_caso_variante(self): ...

class TestErrorCases:
    """Error handling."""
    def test_errore_specifico_con_match(self): ...

class TestEdgeCases:
    """Boundary e casi limite."""
    def test_stringa_vuota(self): ...
    def test_input_massimo(self): ...
```

**Applicazione per C1.3:** Usare la stessa struttura. Classi suggerite:
- `TestTokenizerBasic`, `TestTokenizerIndent`, `TestTokenizerErrors`
- `TestParserProgram`, `TestParserProtocol`, `TestParserAgent`, `TestParserType`
- `TestParserStep`, `TestParserChoice`, `TestParserProperties`
- `TestParserErrors`, `TestParserEdgeCases`
- `TestASTOutput`, `TestBackwardCompat`

### 2.2 Pattern B: Test inline di stringhe multi-riga (pattern killer per parser)

Usato estensivamente in `test_intent_parse.py` e `test_intent_edge.py`:

```python
def test_simple_two_step(self):
    p = parse_intent_protocol("""
        protocol SimpleTask:
            roles: regina, worker

            regina asks worker to do task
            worker returns result to regina
    """)
    assert p.name == "SimpleTask"
    assert p.roles == ("regina", "worker")
    assert len(p.elements) == 2
```

**Valore:** Zero file esterni, test completamente self-contained, leggibilità massima. ADOTTARE per C1.3.

### 2.3 Pattern C: pytest.raises con match preciso

Standard in tutti i file di error testing:

```python
def test_missing_protocol_keyword(self):
    with pytest.raises(IntentParseError, match="expected 'protocol'"):
        parse_intent_protocol("NotAProtocol: ...")

def test_error_has_line_number(self):
    try:
        parse_intent_protocol("...")
        pytest.fail("Expected IntentParseError")
    except IntentParseError as e:
        assert e.line > 0
        assert "line" in str(e)
```

**Pattern C.2:** Verificare non solo il tipo di eccezione ma anche il line number e il contenuto del messaggio. CRITICO per C1.3 (parser deve sempre esporre riga di errore).

### 2.4 Pattern D: parametrize per enumerazioni complete

Usato in `test_spec_parse.py` e `test_integration_core.py`:

```python
@pytest.mark.parametrize("level,expected_threshold", [
    ("high", 0.8), ("medium", 0.5), ("low", 0.2),
    ("certain", 1.0), ("speculative", 0.1),
])
def test_parse_confidence_level(self, level, expected_threshold):
    spec = parse_spec(f"""
        properties for DelegateTask:
            confidence >= {level}
    """)
    assert spec.properties[0].threshold == expected_threshold

@pytest.mark.parametrize("role", list(AgentRole))
def test_agent_by_role_parametrized(self, role):
    info = agent_by_role(role)
    assert info is not None
```

**Applicazione per C1.3:** Parametrize sui nuovi costrutti (`agent`, `type`, `use`, `Confident[T]`, `requires`, `ensures`).

### 2.5 Pattern E: Helper factories per dati di test (no conftest eccessivo)

In `test_checker_core.py` e `test_spec_session.py`:

```python
def make_task_request(task_id="T001"):
    return TaskRequest(task_id=task_id, description="Do the work")

def run_delegate_task_session():
    """Run a complete DelegateTask session and return the log."""
    checker = SessionChecker(DelegateTask, session_id="spec-session-test")
    checker.send("regina", "worker", make_task_request())
    ...
    return checker.log
```

**Vantaggio:** Funzioni helper locali al file, non fixtures globali. Riduce dipendenza da conftest. PREFERIRE per C1.3.

### 2.6 Pattern F: Test di downstream integration (roundtrip)

In `test_intent_parse.py`:

```python
def test_full_roundtrip_intent_to_dsl(self):
    """Intent -> Protocol -> DSL -> Protocol (roundtrip via DSL)."""
    p1 = parse_intent_protocol("...")
    dsl_text = render_protocol(p1)
    p2 = parse_protocol(dsl_text)
    assert p1.name == p2.name
    assert len(p1.elements) == len(p2.elements)
```

**Applicazione per C1.3:** Test roundtrip critici:
- `parse_unified("protocol X: ...") -> Protocol -> intent.py existing AST`
- `parse_unified("agent A: ...") -> AgentDecl`
- `parse_unified compliant with intent backward compat`

### 2.7 Pattern G: Test di frozen dataclass

Usato sistematicamente ovunque:

```python
def test_is_frozen(self):
    result = parse_intent(...)
    with pytest.raises(AttributeError):
        result.protocol = None

def test_frozen(self):
    cs = ConfidenceScore(value=0.5)
    with pytest.raises((AttributeError, TypeError)):
        cs.value = 0.9
```

**Applicazione per C1.3:** Tutti i nodi AST del parser devono essere frozen. Testare immutabilità per ogni nuovo nodo (`AgentDecl`, `TypeDecl`, `UseDecl`, `ProtocolUnified`).

### 2.8 Pattern H: Test interni su moduli (accesso a `_privates`)

In `test_dsl_parse.py` e `test_errors_catalog.py`:

```python
from cervellaswarm_lingua_universale.dsl import (
    _tokenize,
    _message_kind_from_name,
    _NAME_TO_KIND,
)

import cervellaswarm_lingua_universale.errors as _errors_mod
cat = _errors_mod._CATALOG
```

**Applicazione per C1.3:** Testare il tokenizer unificato direttamente (`_tokenize_unified`, `_Token`, `_TokenKind`). Il tokenizer e il componente con piu edge cases: tab vs space, indent stack, linee vuote.

### 2.9 Pattern I: Test di literal DSL sources come costanti modulo

In `test_dsl_parse.py`:

```python
SIMPLE_TASK_DSL = """\
protocol SimpleTask {
    roles regina, worker;
    regina -> worker : TaskRequest;
    ...
}
"""

class TestParseSimpleTask:
    def test_name(self):
        p = parse_protocol(SIMPLE_TASK_DSL)
        assert p.name == "SimpleTask"
```

**Applicazione per C1.3:** Definire i 10 esempi canonici dal DESIGN_C1_2_SYNTAX_GRAMMAR.md come costanti modulo. Ogni esempio = 1 set di test `TestExampleN`.

---

## 3. CONFTEST.PY - ANALISI

Il conftest.py attuale contiene solo fixtures per i tipi di messaggi:
- `task_request`, `task_result_ok`, `task_result_blocked`
- `audit_request`, `audit_verdict_approved`
- `plan_request`, `plan_proposal`, `plan_decision_approved/rejected`
- `research_query`, `research_report`

**Osservazione critica:** Queste fixtures NON sono usate nei file di test piu recenti. I file moderni (test_intent_parse.py, test_spec_parse.py, test_dsl_parse.py) usano helper locali. Il conftest e diventato quasi decorativo.

**Raccomandazione per C1.3:** NON estendere il conftest. Usare helper locali per file.

---

## 4. QUALITA DELLA TEST SUITE ESISTENTE

### 4.1 Punti di forza

- **Copertura degli errori:** Ogni parser ha una classe `TestSyntaxErrors` / `TestParseErrors` con tutti i messaggi di errore verificati con `match=`. Standard molto alto.
- **Line numbers negli errori:** Ogni errore di parsing espone `.line`. I test verificano che `e.line > 0`. Standard da replicare.
- **Test di immutabilita sistematici:** Ogni dataclass e verificata come frozen.
- **Test di integrazione downstream:** intent_parse testa che il risultato funzioni con SessionChecker, Lean4, CodeGen, DSL. Pattern eccellente.
- **Regression tests dedicati:** `test_regression_s382.py` e `test_bug_hunt_9.py` - ogni bug fixato ha il suo test che rimane permanentemente.

### 4.2 Gap attuali (rilevanti per C1.3)

| Gap | Impatto su C1.3 |
|-----|-----------------|
| Nessun test su indent stack / DEDENT | Il tokenizer C1.3 DEVE gestire indent stack come Python. Gap critico. |
| Nessun test su nuovi costrutti (`agent`, `type`, `use`) | Tutto da creare. |
| Nessun test su `Confident[T]` come tipo inline nel protocol | Tutto da creare. |
| Nessun test su `requires:` / `ensures:` inline | Tutto da creare. |
| Nessun test di backward compat intent.py -> parser unificato | Critico: "intent esistenti devono rimanere validi". |
| Nessun test su `use python: ...` | Nuovo costrutto C1.3. |
| Nessun performance test | Non urgente per C1.3 ma gap futuro. |

---

## 5. STRUTTURA SUGGERITA PER I TEST C1.3

Basata sull'analisi della suite esistente e sulla grammatica EBNF (62 produzioni):

### File suggeriti (~700 LOC test, stima Ingegnera confermata)

```
tests/
  test_parser_tokenizer.py    # Tokenizer: indent stack, INDENT/DEDENT, keywords (~120 LOC)
  test_parser_core.py         # program, protocol, roles, step, choice (~180 LOC)
  test_parser_new_constructs.py  # agent, type, use python (~120 LOC)
  test_parser_properties.py   # requires/ensures inline, confidence, trust (~80 LOC)
  test_parser_errors.py       # Tutti gli errori con match e line number (~120 LOC)
  test_parser_backward_compat.py  # Intent esistenti validi nel nuovo parser (~80 LOC)
```

### Template per test_parser_tokenizer.py

```python
"""Tests for unified tokenizer: indent stack, INDENT/DEDENT, keywords."""
import pytest
from cervellaswarm_lingua_universale.parser import (
    _tokenize, _TokenKind, ParseError
)

class TestTokenizerBasic:
    """Basic token recognition."""
    def test_keywords_recognized(self): ...
    def test_identifiers_vs_keywords(self): ...
    def test_colon_newline_indent(self): ...
    def test_comments_ignored(self): ...
    def test_line_tracking(self): ...

class TestIndentStack:
    """INDENT/DEDENT generation (Python-like)."""
    def test_single_indent(self): ...
    def test_nested_indent(self): ...
    def test_dedent_to_zero(self): ...
    def test_tabs_rejected(self):
        with pytest.raises(ParseError, match="tabs are not allowed"):
            _tokenize("protocol X:\n\troles: a, b")
    def test_non_multiple_of_4_rejected(self):
        with pytest.raises(ParseError, match="multiple of 4"):
            _tokenize("protocol X:\n  roles: a, b")
    def test_indent_mismatch_rejected(self): ...
    def test_empty_lines_ignored_in_indent_count(self): ...

class TestTokenizerNewTokenTypes:
    """Tokens new in v0.2: Confident[T], String?, TrustScore."""
    def test_generic_type_bracket(self): ...
    def test_optional_type_question_mark(self): ...
```

### Template per test_parser_backward_compat.py

```python
"""Backward compat: tutti i programmi intent.py validi devono parsare."""
from cervellaswarm_lingua_universale.parser import parse_program
from cervellaswarm_lingua_universale.intent import parse_intent_protocol

# I 10 esempi canonici del DESIGN_C1_2_SYNTAX_GRAMMAR.md
CANONICAL_EXAMPLES = [
    ("delegate_task_base", """
protocol DelegateTask:
    roles: regina, worker, guardiana

    regina asks worker to do task
    worker returns result to regina
    regina asks guardiana to verify
    guardiana returns verdict to regina
"""),
    # ... altri 9 esempi
]

class TestBackwardCompatWithIntentPy:
    """Ogni programma valido per intent.py deve essere valido per il parser unificato."""

    @pytest.mark.parametrize("name,source", CANONICAL_EXAMPLES)
    def test_canonical_example_parses(self, name, source):
        # intent.py parse
        old_result = parse_intent_protocol(source)
        # nuovo parser
        new_result = parse_program(source)
        assert len(new_result.declarations) == 1
        new_proto = new_result.declarations[0]
        assert new_proto.name == old_result.name
        assert new_proto.roles == old_result.roles
        assert len(new_proto.elements) == len(old_result.elements)
```

---

## 6. PATTERN DA ERRORI PER C1.3

Dai test esistenti emerge uno standard chiaro. Ogni `ParseError` deve:

1. Avere `.line` (intero > 0)
2. Avere un messaggio testabile con `match=` preciso
3. Identificare il token inaspettato (cosa "got") vs cosa era atteso

Pattern da `test_intent_edge.py`:
```python
# Standard per ogni errore di parsing:
with pytest.raises(ParseError, match="expected 'protocol'"):  # atteso
with pytest.raises(ParseError, match="expected.*COLON"):      # atteso pattern
with pytest.raises(ParseError, match="cannot parse action"):  # azione sconosciuta
with pytest.raises(ParseError, match="tabs are not allowed"): # whitespace
with pytest.raises(ParseError, match="multiple of 4"):        # indentazione
with pytest.raises(ParseError, match="unexpected character"): # carattere invalido
```

Per C1.3 aggiungere:
```python
with pytest.raises(ParseError, match="expected 'agent'"):
with pytest.raises(ParseError, match="expected 'type'"):
with pytest.raises(ParseError, match="expected 'use'"):
with pytest.raises(ParseError, match="unknown type"):        # Confident[Unknown]
with pytest.raises(ParseError, match="expected DEDENT"):     # indent mismatch
```

---

## 7. RACCOMANDAZIONI FINALI

### Per C1.3 - Test Strategy

1. **Adottare tutti i pattern A-I senza eccezioni.** Sono stati validati su 1581 test esistenti.

2. **Priorita test:** In questo ordine:
   - Tokenizer prima (base di tutto)
   - Backward compat con intent.py (DECISIONE FONDAMENTALE del design)
   - Costrutti base protocol (piu riuso da test esistenti)
   - Nuovi costrutti (`agent`, `type`, `use`)
   - Properties inline (`requires`, `ensures`)
   - Nuovi tipi AI nativi (`Confident[T]`, `TrustScore`, `String?`)

3. **Target:** 700 LOC test per ~350 LOC parser. Rapporto 2:1. Standard del progetto.

4. **File naming:** Seguire la convenzione esistente: `test_parser_[area].py`. NON `test_unified_parser.py` (troppo generico).

5. **Error codes:** Il sistema LU-X### esiste e funziona. Per C1.3 aggiungere codici `LU-I00X` (gia namespace intent) per i nuovi costrutti. Verificare con `test_errors_catalog.py` che il catalog sia aggiornato.

6. **Regression file:** Creare `test_regression_c1_3.py` subito quando troviamo il primo bug durante sviluppo. Pattern gia stabilito in `test_regression_s382.py`.

7. **Downstream integration tests:** Dopo ogni parser che produce AST, aggiungere 2-3 test che verificano che il downstream (SessionChecker, CodeGen) accetti il risultato. Pattern da `TestDownstreamIntegration` in `test_intent_parse.py`.

---

*Report generato da Cervella Researcher - Sessione 409*
*Prossimo step: C1.3 Parser Unificato - la Regina usa questo report per la strategia.*
