# B.6 Error Messages per Umani - Lingua Universale
**Data:** 2026-02-25
**Ricercatore:** Cervella Researcher
**Status:** COMPLETA
**Fonti:** 27 consultate

---

## Contesto

B.6 e il 14esimo modulo della Lingua Universale. Il suo scopo e tradurre errori
tecnici/formali in messaggi comprensibili per umani non-developer. L'obiettivo e
che un utente non tecnico che scrive:

```
properties for DelegateTask:
    worker cannot send audit_verdct   <- typo!
    trust >= mega                     <- valore sconosciuto
```

riceva non:

```
SpecParseError: line 2: unknown message kind 'audit_verdct'.
Valid (snake_case): audit_request, audit_verdict, ...
```

ma invece:

```
Errore nella specifica del protocollo "DelegateTask"
  Riga 2: "audit_verdct" non e un tipo di messaggio valido.
  Forse intendevi: audit_verdict?
  Tipi disponibili: audit_request, audit_verdict, task_request, ...
```

---

## 1. Gold Standard: Come Elm e Rust Gestiscono gli Errori

### 1.1 Elm - Il Precursore

Evan Czaplicki (2015, "Compiler Errors for Humans") ha definito i principi
che tutta l'industria ha poi adottato:

**Struttura di ogni messaggio Elm:**
1. Contesto generale (dove siamo, cosa stava succedendo)
2. Codice esatto dell'utente con evidenziazione
3. Hint specifico e actionable

**Principi chiave:**
- NON mostrare la rappresentazione interna del compilatore
- SEMPRE in plain English, leggibile da chi non conosce la teoria
- OGNI messaggio ha un hint utile (non "error: invalid")
- L'obiettivo e didattico: il messaggio INSEGNA la sintassi
- AI copilots moderni (2024-2025) apprezzano Elm perche gli errori sono
  deterministici e strutturati, facilmente processabili

### 1.2 Rust - La Struttura Industriale

Il Rust Compiler Development Guide definisce la struttura formale dei diagnostici:

**5 componenti obbligatori:**
1. **Level** - error / warning / note (severita)
2. **Code** - E0308 (link a spiegazione estesa)
3. **Message** - descrizione generale del problema (standalone intelligible)
4. **Diagnostic window** - file path + righe + codice + span labels
5. **Sub-diagnostics** - informazioni aggiuntive sequenziali

**Principio fondamentale:** "Errors should focus on the code you wrote."
Il codice dell'utente e SEMPRE al centro, tutto il resto e costruito intorno.

**Categorizzazione suggestions:**
- `MachineApplicable` - puo essere applicato automaticamente
- `HasPlaceholders` - richiede input dell'utente
- `MaybeIncorrect` - potrebbe essere sbagliato
- `Unspecified` - confidenza non determinata

**Regole stile:**
- Lowercase, senza punto finale (a meno di piu frasi)
- Breve (utente lo vede ripetutamente)
- `help:` per suggerire cosa fare
- `note:` per contesto aggiuntivo, link, fatti

### 1.3 miette - Il Pattern Python-Friendly

La libreria `miette` (Rust) formalizza il pattern in API riutilizzabile:
- `code` - codice unico del diagnostico (globalmente documentato)
- `help` - testo di aiuto aggiuntivo ("Hai provato X?")
- `url` - link a documentazione estesa
- Severity levels: Error / Warning / Advice

Questo e il pattern piu moderno e trasferibile a Python.

---

## 2. Struttura Consigliata per B.6

Basato su Elm + Rust + miette + analisi del nostro codice esistente,
la struttura ottimale per `errors.py` e:

```python
@dataclass(frozen=True)
class LinguaError:
    """Errore user-friendly della Lingua Universale."""

    # Categoria (per filtrare/gestire programmaticamente)
    category: ErrorCategory

    # Codice univoco (per documentazione e test)
    code: str  # es: "E001", "P002", "R003"

    # Messaggio principale (standalone intelligible, lowercase)
    message: str

    # Contesto (riga, posizione, nome protocollo)
    location: Optional[ErrorLocation] = None

    # Suggerimento actionable (come fixare)
    hint: Optional[str] = None

    # Note aggiuntive (fatti, link, contesto)
    notes: tuple[str, ...] = ()

    # Valore che ha causato l'errore (per "forse intendevi")
    got: Optional[str] = None

    # Valore/i attesi (per "forse intendevi")
    expected: Optional[str | tuple[str, ...]] = None
```

### 2.1 ErrorCategory - Tassonomia Standard

Da analisi di compilatori, DSL, e model checkers:

```python
class ErrorCategory(Enum):
    # Errori di SINTASSI - il testo non rispetta la grammatica
    SYNTAX = "syntax"
    # Errori di TIPO/NOME - identificatore non riconosciuto
    UNKNOWN_IDENTIFIER = "unknown_identifier"
    # Errori SEMANTICI - sintassi corretta ma senso sbagliato
    SEMANTIC = "semantic"
    # Violazioni di PROPRIETA - la proprieta e falsa
    PROPERTY_VIOLATION = "property_violation"
    # Errori di RUNTIME - violazione durante l'esecuzione
    PROTOCOL_VIOLATION = "protocol_violation"
    # Errori di VERIFICA FORMALE - Lean 4 non riesce a provare
    VERIFICATION_FAILURE = "verification_failure"
    # Errori di CONFIGURAZIONE - parametri invalidi
    CONFIGURATION = "configuration"
```

---

## 3. Errori Lean 4: Come Gestirli

### 3.1 Tipi di errore piu comuni da Lean 4 --json

Dal JSON output di `lean --json`, i messaggi con `severity: "error"` contengono:
- `type mismatch` - tipo atteso vs tipo trovato
- `unknown identifier` - identificatore non in scope
- `failed to synthesize instance` - classe mancante
- `application type mismatch` - argomenti errati
- `declaration uses sorry` - proof incompleta

### 3.2 Traduzione per Non-Developer

Per il nostro caso (teoremi `by decide`), gli errori sono quasi sempre uno di:

1. **Teorema non provabile** - la proprieta e FALSA
   - Lean dice: `type mismatch` o `decide tactic failed`
   - Noi diciamo: "La proprieta '{nome}' e VIOLATA nel protocollo '{proto}'."

2. **Identificatore sconosciuto** - bug nel codice generato
   - Lean dice: `unknown identifier 'DelegatTask_roles'`
   - Noi diciamo: "Errore interno nella generazione Lean 4 [codice E_L001]."

3. **Timeout**
   - Noi diciamo: "Verifica troppo lenta (>{N}s). Il protocollo potrebbe
     essere troppo complesso per la verifica automatica."

### 3.3 Pattern Wrapper

```python
def translate_lean_error(lean_message: str, property_name: str) -> LinguaError:
    """Traduce un messaggio di errore Lean 4 in LinguaError user-friendly."""
    msg_lower = lean_message.lower()

    if "decide tactic failed" in msg_lower or "type mismatch" in msg_lower:
        return LinguaError(
            category=ErrorCategory.PROPERTY_VIOLATION,
            code="V001",
            message=f"la proprieta '{property_name}' e violata",
            hint="controlla la definizione del protocollo",
            notes=(f"dettaglio tecnico: {lean_message[:100]}",),
        )

    if "unknown identifier" in msg_lower:
        return LinguaError(
            category=ErrorCategory.VERIFICATION_FAILURE,
            code="L001",
            message="errore interno nella generazione del codice Lean 4",
            hint="segnala questo errore come bug",
            notes=(f"lean output: {lean_message[:200]}",),
        )

    # Default: errore generico
    return LinguaError(
        category=ErrorCategory.VERIFICATION_FAILURE,
        code="L999",
        message="verifica formale fallita",
        notes=(lean_message[:300],),
    )
```

---

## 4. "Forse Intendevi?" - Fuzzy Matching

Il pattern piu apprezzato dagli utenti (Elm, Lean 4, Rust) e il suggerimento
"forse intendevi X?". Per ZERO deps esterne, `difflib` stdlib e sufficiente:

```python
import difflib

def suggest_similar(got: str, valid: list[str], n: int = 3) -> list[str]:
    """Suggerisci i valori validi piu simili a 'got' (stdlib difflib)."""
    return difflib.get_close_matches(got, valid, n=n, cutoff=0.6)
```

Lean 4 stesso (2024) ha aggiunto questo pattern per `unknown identifier`:
code action che suggerisce nomi simili nell'environment.

**Applicazioni nel nostro codice:**
- `audit_verdct` -> suggerisce `audit_verdict`
- `turst` -> suggerisce `trust`
- `mega` (trust tier sconosciuto) -> suggerisce `trusted`, `standard`

---

## 5. Multi-Lingua: Approccio ZERO Deps

### 5.1 Opzioni Analizzate

| Approccio | Deps | Flessibilita | Raccomandazione |
|-----------|------|--------------|-----------------|
| `gettext` (stdlib) | 0 (ma tool esterni per .po) | Media | Troppo pesante per uso interno |
| ICU MessageFormat | Dipendenza esterna | Alta | VIETATO (nostro requisito) |
| Template string semplici | 0 | Media | RACCOMANDATO |
| Dict[lang, Dict[code, str]] | 0 | Alta | RACCOMANDATO |

### 5.2 Pattern Raccomandato: Template Lookup

```python
# Messaggi per lingua (MappingProxyType, immutabile, P04 compliant)
_MESSAGES: MappingProxyType[str, MappingProxyType[str, str]] = MappingProxyType({
    "it": MappingProxyType({
        "E001": "tipo di messaggio sconosciuto '{got}'",
        "E002": "livello di confidenza sconosciuto '{got}'",
        "P001": "la proprieta '{property}' e violata",
    }),
    "en": MappingProxyType({
        "E001": "unknown message kind '{got}'",
        "E002": "unknown confidence level '{got}'",
        "P001": "property '{property}' is violated",
    }),
})

def format_message(code: str, lang: str = "en", **kwargs: str) -> str:
    """Formatta un messaggio localizzato con i parametri."""
    template = _MESSAGES.get(lang, _MESSAGES["en"]).get(code, code)
    return template.format(**kwargs)
```

Questo approccio:
- ZERO deps (solo stdlib)
- Estendibile a nuove lingue senza refactor
- Testabile (ogni codice ha un template)
- P04 compliant (MappingProxyType)

**Nota:** Per la missione NORD (accessibile a tutti), supportare almeno
`it` e `en` e strategicamente importante.

---

## 6. Pattern da Model Checkers per Property Violations

### 6.1 Alloy - Counterexample Visualization

Alloy mostra violazioni come **counterexample cliccabili** che aprono
il visualizzatore. Principio chiave: mostra la TRACCIA che viola la proprieta.

Trasferibile a noi: quando `ORDERING` e violata, mostrare i passi
nella sequenza che dimostrano la violazione.

### 6.2 TLA+ / FizzBee - Witness

TLA+ e FizzBee mostrano la **sequenza di azioni** che porta alla violazione.
FizzBee usa Python-like syntax e state transition graph per la debug experience.

### 6.3 Dafny - "Constant Watch"

Dafny guarda continuamente il codice e mostra counterexamples inline.
Principio: la violazione deve mostrare un esempio concreto di PERCHE.

### 6.4 Nostro Pattern per Property Violations

```python
@dataclass(frozen=True)
class PropertyViolationDetails:
    """Dettagli specifici per violazioni di proprieta."""
    property_kind: str          # "ORDERING", "EXCLUSION", etc.
    witness: str                # La prova/esempio della violazione
    counterexample_path: Optional[tuple[str, ...]] = None  # Passi della traccia
```

Esempio output per violazione ORDERING:

```
VIOLAZIONE: task_result appare prima di task_request
  Prova: nel percorso di esecuzione 2 (branch "fast_path"):
    Passo 3: worker -> regina : task_result
    Passo 5: regina -> worker : task_request
  Suggerimento: sposta task_request prima di task_result nella definizione
  del protocollo DelegateTask.
```

---

## 7. Analisi del Codice Esistente

Ho letto tutti i 5 moduli indicati. Stato attuale degli errori:

### 7.1 checker.py
- `ProtocolViolation`: messaggio tecnico: "expected {expected}, got {got}"
- `SessionComplete`: messaggio corto, non user-friendly
- **Gap:** nessun hint, nessuna categoria, nessun "forse intendevi"

### 7.2 spec.py
- `SpecParseError`: ha numero di riga - OTTIMO
- Messaggi tipo: `"unknown confidence level 'xxx'. Valid: certain, high, ..."`
- **Gap:** inglese tecnico, nessun fuzzy matching, nessun hint di fix

### 7.3 intent.py
- `IntentParseError`: ha numero di riga - OTTIMO
- `_format_valid_actions()`: lista tutte le azioni valide - BUONO
- **Gap:** non suggerisce l'azione piu simile a quella sbagliata

### 7.4 lean4_bridge.py
- Errori: `ValueError` e `RuntimeError` grezzi
- Output Lean: stringa grezza passata come `error` field
- **Gap totale:** nessuna traduzione per non-developer

### 7.5 codegen.py
- `ValueError`: messaggi tecnici generici
- **Gap:** non indica cosa l'utente deve correggere

### 7.6 Errori Gia Buoni (da preservare)
- Line numbers in `SpecParseError` e `IntentParseError`
- Lista valori validi in spec.py (buon pattern)
- Struttura `expected` vs `got` in `ProtocolViolation`

---

## 8. Architettura Raccomandata per errors.py

### 8.1 Cosa NON fare

- NON sostituire le eccezioni esistenti (breaking change)
- NON aggiungere deps esterne
- NON duplicare la logica di validazione

### 8.2 Cosa FARE: Translator Layer

`errors.py` e un **layer di traduzione**, non un sostituto. Pattern:

```
Exception tecnica (SpecParseError, ProtocolViolation, ValueError)
    |
errors.py translator
    |
LinguaError (user-friendly, multi-lingua, con hint)
    |
format_error() -> stringa per l'utente
```

### 8.3 Componenti di errors.py

1. **`ErrorCategory`** (enum) - tassonomia 7 categorie
2. **`ErrorLocation`** (frozen dataclass) - riga, colonna, nome file
3. **`LinguaError`** (frozen dataclass) - messaggio strutturato completo
4. **`ErrorCode`** (costanti stringa) - E001..Exxx, V001..Vxxx, L001..Lxxx
5. **`_MESSAGE_TEMPLATES`** (MappingProxyType) - it/en per ogni codice
6. **`suggest_similar()`** - fuzzy matching via difflib
7. **`format_error()`** - rendering human-readable
8. **`translate_*()`** - da eccezione tecnica a LinguaError
   - `translate_spec_error(SpecParseError)`
   - `translate_intent_error(IntentParseError)`
   - `translate_protocol_violation(ProtocolViolation)`
   - `translate_lean_error(str, property_name)`
   - `translate_property_violation(PropertyResult)`
9. **`explain(error_code)`** - spiegazione estesa (ispirata a `rustc --explain`)

### 8.4 Codici Errore

```
E = syntax/parse Error
P = Property violation
V = Verification (Lean 4)
R = Runtime (protocol)
C = Configuration
```

Esempi:
- `E001` - unknown message kind
- `E002` - unknown confidence level
- `E003` - unknown trust tier
- `E004` - indentation error
- `E005` - unexpected character
- `P001` - ordering violated
- `P002` - exclusion violated
- `P003` - roles not participating
- `R001` - wrong sender
- `R002` - wrong receiver
- `R003` - wrong message kind
- `R004` - session already complete
- `V001` - lean proof failed (property false)
- `V002` - lean timeout
- `V003` - lean not installed

---

## 9. Differenziatori vs Competizione

### 9.1 Cosa nessuno ha

1. **`confidence >= high` come proprieta formale** - unico al mondo (B.5)
2. **Errori multi-lingua per session type violations** - campo vergine
3. **"Forse intendevi X?" per MessageKind** - applicazione nuova
4. **Traduzione errori Lean 4 in linguaggio naturale per AI protocols** - primo al mondo

### 9.2 Best Practice Adottate

- Elm: hint didattico in ogni messaggio
- Rust: struttura Level+Code+Message+Location+Sub-diagnostics
- miette: codice unico + url + help separato da note
- Lean 4 (2024): code action "simile a X?" per unknown identifier
- Alloy/FizzBee: witness/counterexample con traccia di esecuzione
- difflib stdlib: fuzzy matching zero-deps

---

## 10. Stima Modulo

Basato sui moduli precedenti (spec.py: 1242 LOC, intent.py: ~650 LOC):

- errors.py: ~600-800 LOC (piu template messaggi)
- Test: ~80-120 test (ogni codice errore + ogni translator + ogni formatter)
- Zero deps esterne (solo `difflib` stdlib)
- Pattern: frozen dataclasses, MappingProxyType, ZERO side effects

---

## Raccomandazione Finale

**Approccio:** Translator Layer su eccezioni esistenti.

**NON rompere le eccezioni tecniche esistenti** (SpecParseError,
IntentParseError, ProtocolViolation). Sono utili per i developer.

**AGGIUNGERE** errors.py come layer di traduzione opzionale per:
1. CLI output (l'utente finale vede messaggi user-friendly)
2. API response (quando il caller e non-developer)
3. Test di leggibilita (assicurare che ogni errore sia comprensibile)

**Priorita di implementazione:**
1. `ErrorCategory` + `LinguaError` + `ErrorLocation` (struttura base)
2. `translate_spec_error()` + `translate_intent_error()` (DSL errors)
3. `translate_protocol_violation()` (runtime errors)
4. `suggest_similar()` con difflib (fuzzy matching)
5. Message templates it/en (multi-lingua)
6. `translate_lean_error()` (Lean 4 errors)
7. `explain()` (spiegazioni estese stile rustc --explain)

**Il differenziatore:** errori per umani in italiano e inglese per un
sistema di session types formali con verifica Lean 4. Nessuno lo ha.

---

## Fonti

1. [Elm - Compiler Errors for Humans](https://elm-lang.org/news/compiler-errors-for-humans) - Evan Czaplicki, 2015
2. [Rust Compiler Dev Guide - Diagnostics](https://rustc-dev-guide.rust-lang.org/diagnostics.html)
3. [Shape of Errors to Come - Rust Blog](https://blog.rust-lang.org/2016/08/10/Shape-of-errors-to-come/)
4. [miette - Rust diagnostic library](https://github.com/zkat/miette)
5. [miette docs](https://docs.rs/miette/latest/miette/)
6. [Elm Error Message Design - Jamalambda](https://jamalambda.com/posts/2021-06-13-elm-errors.html)
7. [Elm DeepWiki - Syntax Error Reporting](https://deepwiki.com/elm/compiler/4.1-syntax-error-reporting)
8. [Writing Good Compiler Error Messages - Caleb Mer](https://calebmer.com/2019/07/01/writing-good-compiler-error-messages.html)
9. [Lean 4 - unknown identifier errors](https://lean-lang.org/doc/reference/latest/Error-Explanations/About___--unknownIdentifier/)
10. [Lean 4 Exception types](https://leanprover-community.github.io/mathlib4_docs/Lean/Exception.html)
11. [Lean 4 Interacting - errors](https://lean-lang.org/theorem_proving_in_lean4/Interacting-with-Lean/)
12. [FizzBee - formal methods accessible](https://fizzbee.io/)
13. [FizzBee GitHub](https://github.com/fizzbee-io/fizzbee)
14. [FizzBee vs TLA+ article](https://materializedview.io/p/fizzbee-tla-and-formal-software-verification)
15. [Alloy Analyzer GUI](https://alloytools.org/quickguide/gui.html)
16. [TLA+ Wikipedia](https://en.wikipedia.org/wiki/TLA+)
17. [Dafny verifier error messages](https://github.com/dafny-lang/dafny)
18. [Dafny IDE paper](https://arxiv.org/pdf/1404.6602)
19. [Python gettext stdlib](https://docs.python.org/3/library/gettext.html)
20. [Python i18n guide](https://internationalization-guide.readthedocs.io/en/latest/i18n-of-python-application.html)
21. [PEP style guide for error messages (discussion)](https://discuss.python.org/t/a-pep-style-guide-for-error-messages/30842)
22. [Counterexample Simplification for Liveness Properties](https://link.springer.com/chapter/10.1007/978-3-319-92970-5_11)
23. [Witness and Counterexample Automata](https://www.researchgate.net/publication/220703347_Witness_and_Counterexample_Automata_for_ACTL)
24. [Explaining counterexamples using causality](https://link.springer.com/article/10.1007/s10703-011-0132-2)
25. [Rust Borrow Checker Deep Dive - InfoQ](https://www.infoq.com/presentations/rust-borrow-checker/)
26. [DSL Design Patterns - Fowler](https://martinfowler.com/dsl.html)
27. [AI Coding Agents and DSLs](https://devblogs.microsoft.com/all-things-azure/ai-coding-agents-domain-specific-languages/)

---
COSTITUZIONE-APPLIED: SI
Principio usato: "Ricerca PRIMA di implementare" (Formula Magica) + "Fatto BENE > Fatto VELOCE"
