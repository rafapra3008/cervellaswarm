# STEP C1.1 - STUDIO: Analisi dei Moduli Esistenti

> **Sessione:** 408
> **Data:** 26 Febbraio 2026
> **Analista:** Cervella Regina
> **Codice analizzato:** 8.466 LOC (14 file: 13 moduli + `__init__.py` 279 LOC) + showcase (492 LOC)

---

## DELIVERABLE 1: Tabella "Modulo -> Feature del Linguaggio -> Gap"

| Modulo | LOC | Feature del Linguaggio che GIA contiene | Gap (cosa MANCA per il linguaggio) |
|--------|-----|----------------------------------------|-------------------------------------|
| **spec.py** | 1242 | EBNF formale documentata, tokenizer indent-aware, recursive descent parser, property system (`always terminates`, `no deadlock`, `A before B`, `confidence >=`, `trust >=`), verifica statica + runtime | Sintassi legata a "properties for X:" - serve integrazione nella grammatica unificata. Nessun tipo `requires`/`ensures` generico. |
| **dsl.py** | 493 | EBNF formale documentata, tokenizer regex-based, recursive descent parser, Scribble-inspired (`protocol X { roles...; step -> step : Msg; choice at X { branch: {...} } }`), renderer bidirezionale (round-trip) | Grammatica fissa su protocolli agent. Non estensibile a domini generici. Keyword C-style (`{`, `}`, `;`) non Python-like. |
| **intent.py** | 649 | Sintassi naturale Python-like (`protocol X:`, indent-based, `regina asks worker to do task`), tokenizer indent-aware, recursive descent parser, action verb mapping deterministico | Solo input (no renderer/round-trip). Grammatica limitata a 14 verbi d'azione. Non supporta `requires`/`ensures`/`confidence`. |
| **codegen.py** | 730 | Pipeline Protocol -> Python completa, generazione role classes tipizzate, SessionChecker enforcement, template-based (zero eval/exec) | Genera Python "boilerplate", non un linguaggio intermedio. Nessun contratto `requires`/`ensures` nel codice generato. Nessun `Confident[T]` nel output. |
| **showcase.py** | 492 | Demo end-to-end funzionante: intent -> DSL -> spec -> static verify -> Lean4 -> codegen -> runtime -> confidence & trust | Flusso manuale (8 funzioni chiamate in sequenza). Non c'e un unico linguaggio che unifica tutto. |
| **protocols.py** | 308 | Tipi core: `Protocol`, `ProtocolStep`, `ProtocolChoice`, `ProtocolElement`. Immutabili (frozen dataclass). | Solo struttura dati, nessuna sintassi. |
| **types.py** | 471 | `MessageKind` (14 tipi), `AgentRole` (17 ruoli), `TaskStatus`, `AuditVerdictType`, `PlanComplexity`. Message dataclasses tipizzate. | Enums hardcoded. Il linguaggio dovrebbe permettere tipi custom. |
| **checker.py** | 524 | `SessionChecker`: state machine runtime, enforcement protocolli, session log, role bindings. | Enforcement runtime-only. Il linguaggio dovrebbe poter esprimere questi vincoli staticamente. |
| **confidence.py** | 177 | `ConfidenceScore`, `Confident[T]`, `CompositionStrategy`, `compose_scores`. Incertezza come tipo NATIVO. | Esiste come libreria Python, non come keyword del linguaggio. `confidence >= high` e in spec.py ma disconnesso da `Confident[T]`. |
| **trust.py** | 167 | `TrustTier` (4 livelli), `TrustScore`, `trust_tier_for_role`, `compose_chain`. Fiducia componibile. | Stessa cosa: libreria Python, non parte della grammatica. `trust >= trusted` in spec.py ma come property, non come vincolo nel codice. |
| **errors.py** | 1784 | Sistema errori umani multilingue (EN+IT), `humanize()`, `format_error()`, rich formatting. 257 test. | Pronto per il linguaggio! Solo da estendere con errori syntax/semantic del nuovo parser. |
| **lean4_bridge.py** | 672 | Genera codice Lean 4 per verifica formale: theorems per terminazione, deadlock, ordering. | Template-based per protocolli. Il linguaggio dovrebbe avere `proof` keyword nativa che compila a Lean 4. |
| **monitor.py** | 473 | `ProtocolMonitor`, `EventCollector`, listener pattern per eventi runtime. | Monitoring runtime. Il linguaggio potrebbe avere `observe` keyword. |
| **integration.py** | 497 | Pipeline completa: intent -> DSL -> spec -> verify -> codegen. `VerificationPipeline` class. | Orchestrazione via Python API. Il linguaggio dovrebbe ESSERE la pipeline. |

---

## DELIVERABLE 2: Inventario Keyword/Strutture GIA usate nel DSL

### Grammatica spec.py (Proprieties)
```
KEYWORD: properties, for, always, terminates, no, deadlock, before, cannot, send,
         confidence, trust, all, roles, participate
OPERATORI: >= :
STRUTTURA: indent-based (4 spaces), line-oriented
```

### Grammatica dsl.py (Protocol)
```
KEYWORD: protocol, roles, choice, at, max_repetitions
OPERATORI: -> : ; , { }
STRUTTURA: brace-based (C-style)
```

### Grammatica intent.py (Natural Language)
```
KEYWORD: protocol, roles, when, decides
VERBI: asks, to, do, task, returns, result, verify, verdict, tells, decision,
       proposes, plan, sends, message, broadcast, shutdown, ack, context,
       research, report
OPERATORI: : ,
STRUTTURA: indent-based (Python-like, 4 spaces)
```

### Tipi nativi gia esistenti come concetti
```
TIPI CONFIDENZA: certain (1.0), high (0.8), medium (0.5), low (0.2), speculative (0.1)
TIPI TRUST:      verified, trusted, standard, untrusted
TIPI MESSAGGIO:  14 MessageKind (task_request, task_result, audit_request, ...)
TIPI STATUS:     ok, fail, blocked
TIPI AUDIT:      approved, blocked, needs_revision
TIPI RUOLO:      17 AgentRole (regina, guardiana-qualita, backend, ...)
```

### Pattern ricorrenti (proto-linguaggio implicito)
```
1. sender -> receiver : MessageType;     (dsl.py)
2. sender verb receiver prep object      (intent.py)
3. properties for Protocol:              (spec.py)
4.     property_assertion                (spec.py)
5. choice at decider { branches }        (dsl.py)
6. when decider decides:                 (intent.py)
7. Confident[T]                          (confidence.py - Python, non DSL)
8. compose_scores(..., strategy=MIN)     (confidence.py - Python API)
9. trust_tier_for_role(role)             (trust.py - Python API)
```

---

## DELIVERABLE 3: Proposta - "Il Linguaggio Nasce da QUI"

### La Risposta Chiara

**Il linguaggio nasce dalla FUSIONE di 3 moduli: intent.py (sintassi) + spec.py (proprieta) + confidence/trust (tipi nativi).**

### Perche

| Modulo | Contributo al Linguaggio | Ruolo |
|--------|--------------------------|-------|
| **intent.py** | SINTASSI BASE | La sua grammatica indent-based, Python-like, e gia la piu vicina a come vogliamo il linguaggio. "regina asks worker to do task" e leggibile sia dall'AI che dall'umano. |
| **spec.py** | SISTEMA DI PROPRIETA | `always terminates`, `no deadlock`, `confidence >= high` sono GIA keyword native. Il tokenizer e parser sono i piu maturi (1242 LOC). |
| **confidence.py + trust.py** | TIPI NATIVI AI | `Confident[T]`, `ConfidenceScore`, `TrustTier` sono i tipi che nessun altro linguaggio ha. Devono diventare keyword. |

### Cosa gia "sembra un linguaggio" (senza toccare nulla)

Se prendiamo intent.py + spec.py e li mettiamo insieme, OGGI possiamo scrivere:

```
protocol RecipeApp:
    roles: regina, backend, guardiana

    regina asks backend to do task
    backend returns result to regina
    regina asks guardiana to verify
    guardiana returns verdict to regina

properties for RecipeApp:
    always terminates
    no deadlock
    task_request before task_result
    confidence >= high
    all roles participate
```

Questo **GIA funziona** - ma in DUE parser separati. Il linguaggio unificato li fonde in UNO.

### Cosa MANCA (i gap critici per Fase C1.2)

1. **`requires` / `ensures`** - contratti pre/post non esistono in nessun modulo
2. **`confidence` come tipo nel corpo** - esiste solo come property in spec.py, non come annotazione inline
3. **`proof` keyword** - il bridge Lean 4 e nascosto, dovrebbe essere esplicito
4. **Tipi custom** - gli enum sono hardcoded, il linguaggio deve permettere `type Status = ok | fail | blocked`
5. **Import/export Python** - nessun modulo ha interop bidirezionale
6. **Grammatica unificata** - tre parser separati (dsl.py, spec.py, intent.py) devono diventare UNO

### Architettura proposta per il nuovo parser

```
+================================================================+
|                                                                  |
|  IL LINGUAGGIO UNIFICATO (proposta)                             |
|                                                                  |
|  BASE SINTATTICA:  intent.py (indent-based, Python-like)        |
|  SISTEMA PROPRIETA: spec.py (keyword native)                     |
|  TIPI AI:          confidence.py + trust.py (Confident[T])      |
|  CODEGEN:          codegen.py (Python output con contratti)      |
|  VERIFICA:         lean4_bridge.py (proof automatiche)           |
|  ERRORI:           errors.py (messaggi umani multilingue)        |
|                                                                  |
|  NUOVO:                                                          |
|    - requires/ensures come keyword                               |
|    - confidence come annotazione inline                          |
|    - proof come keyword (compila a Lean 4)                       |
|    - type declarations (enum-like, user-defined)                 |
|    - use python X (import bidirezionale)                         |
|                                                                  |
+================================================================+
```

### Il Core Diventa: intent.py evoluto

intent.py e il modulo che piu "sembra" il linguaggio che vogliamo:
- Sintassi Python-like (indent, `:`, no `;` no `{}`)
- Leggibile da non-sviluppatori ("regina asks worker to do task")
- Tokenizer + parser indent-aware gia robusto (649 LOC totali, ~70 LOC tokenizer)
- Recursive descent parser gia funzionante

**dsl.py rimane** come formato di interscambio/export (Scribble-compatibile).
**spec.py si fonde** nel linguaggio unificato (le keyword properties entrano nella grammatica).

---

## RIEPILOGO QUANTITATIVO

```
CODICE ANALIZZATO:     8.466 LOC (14 file: 13 moduli + __init__.py) + 492 LOC (showcase) = 8.958 LOC totali
PARSER ESISTENTI:      3 (dsl.py, spec.py, intent.py) - tutti recursive descent
GRAMMATICHE EBNF:      3 (tutte documentate nel docstring)
KEYWORD GIA DEFINITE:  ~40 keyword uniche tra i 3 parser
TIPI NATIVI AI:        2 (Confident[T], TrustScore) + 5 livelli confidence + 4 tier trust
TEST ESISTENTI:        1.820 test, 98% coverage
GAP PRINCIPALI:        6 (requires/ensures, confidence inline, proof keyword,
                           tipi custom, Python interop, grammatica unificata)
```

---

## DECISIONE CHIAVE PER C1.2

**Il linguaggio nasce da intent.py** (sintassi base) **arricchito con le keyword di spec.py** (proprieta formali) **e i tipi di confidence.py/trust.py** (tipi AI nativi).

Questo rispetta l'insight di Rafa: **dual-readable** - facile per l'AI (intent.py e gia parsabile) + facile per gli umani (leggibile come inglese).

---

*Cervella Regina - CervellaSwarm S408*
*"Ogni punto alla volta, mirato, con calma."*
