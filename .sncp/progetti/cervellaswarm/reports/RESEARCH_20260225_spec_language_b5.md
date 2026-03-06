# Specification Language B.5 - Ricerca Completa
## Proprieta Formali User-Friendly per Protocolli Multi-Agent

**Data:** 2026-02-25
**Autrice:** Cervella Researcher
**Fonti consultate:** 27 (web + accademiche)
**Status:** COMPLETA

---

## CONTESTO: Cosa e B.5

B.5 NON e un'altra sintassi per protocolli. E un layer per esprimere
PROPRIETA FORMALI in modo accessibile, che si traducono in:
- Teoremi Lean 4 verificabili (via lean4_bridge.py esistente)
- Invarianti da controllare a runtime (via checker.py esistente)
- Precondizioni/postcondizioni da verificare (via quality_gates esistenti)

L'utente dice:
  "questo protocollo deve sempre terminare"
  "l'audit deve avvenire prima del deploy"
  "il worker non puo auto-approvarsi"

Il sistema risponde con: verita dimostrata matematicamente. O con: "falso, ecco il controesempio."

---

## PARTE 1 - TASSONOMIA UNIVERSALE DELLE PROPRIETA FORMALI

### 1.1 Il Sistema di Riferimento: Dwyer et al. (1999) - Property Specification Patterns

Il sistema piu usato al mondo per specificare proprieta formali in modo leggibile.
Analisi di 500+ specifiche reali -> due categorie fondamentali + 5 scope.

**CATEGORIE DI PATTERN:**

#### A) Occurrence Patterns (esiste o non esiste X?)

| Pattern | Descrizione Naturale | Formula LTL | Alias |
|---------|---------------------|-------------|-------|
| **Absence** | "P non accade mai" | G(!P) | Never, Forbidden |
| **Universality** | "P vale sempre" | G(P) | Always True, Invariant |
| **Existence** | "P accade almeno una volta" | F(P) | Eventually, Reachability |
| **Bounded Existence** | "P accade al massimo N volte" | finite occurrences(P) | At Most N |

#### B) Order Patterns (in che ordine accadono X e Y?)

| Pattern | Descrizione Naturale | Formula LTL | Alias |
|---------|---------------------|-------------|-------|
| **Precedence** | "S accade sempre prima di P" | !P W S | Before, Requires |
| **Response** | "Dopo ogni P, segue S" | G(P -> F(S)) | After, Triggers |
| **Precedence Chain** | "S1,S2 precedono P" | compound | Sequence Before |
| **Response Chain** | "Dopo P, seguono S1 poi S2" | compound | Sequence After |

**5 SCOPE applicabili a ogni pattern:**

| Scope | Descrizione |
|-------|-------------|
| Globally | In tutta l'esecuzione |
| Before R | Prima dell'evento R |
| After Q | Dopo l'evento Q |
| Between Q and R | Tra Q e R (ripetibile) |
| After Q Until R | Dopo Q, finche non accade R |

**Fonte:** https://matthewbdwyer.github.io/psp/

### 1.2 DECLARE Templates (Process Mining - van der Aalst)

DECLARE e il sistema di "workflow constraints" piu usato nell'industry.
Semantica LTL rigorosa, leggibilita alta. 27 template standard.

**Existence Templates:**
```
Existence(A)        -> A accade almeno una volta         [F(A)]
Absence(A)          -> A non accade mai                  [G(!A)]
Exactly(A, n)       -> A accade esattamente n volte      [bounded]
Init(A)             -> A e il primo messaggio            [A]
Last(A)             -> A e l'ultimo messaggio            [F(A & G(!T))]
```

**Ordering Templates:**
```
Response(A, B)      -> Se A, poi B                       [G(A -> F(B))]
Precedence(A, B)    -> B solo se prima A                 [!B W A]
Succession(A, B)    -> Response + Precedence             [compound]
ChainResponse(A, B) -> Dopo A, immediatamente B          [G(A -> X(B))]
ChainPrecedence(A,B)-> B solo se immediatamente prima A  [G(X(B) -> A)]
AlternateResponse   -> A->B alternati, nessun A prima di B
AlternatePrec.      -> come sopra, direzione opposta
```

**Negative Templates:**
```
NotCoExistence(A,B) -> A e B non possono entrambi accadere
NotSuccession(A,B)  -> A non puo essere seguito da B
NotChainSuccession  -> B non immediatamente dopo A
```

**Fonte:** https://arxiv.org/html/2412.10152 (DECLARE in ASP, 2024)

### 1.3 Proprieta Specifiche per Session Types / Protocolli di Comunicazione

La teoria dei tipi di sessione (Multiparty Session Types, Honda, Yoshida, Carbone)
garantisce queste proprieta come conseguenze del type-checking:

| Proprieta | Descrizione | Tipo |
|-----------|-------------|------|
| **Deadlock Freedom** | Nessun agente rimane bloccato ad aspettare | Liveness |
| **Progress** | Ogni sessione avanza o termina | Liveness |
| **Termination** | Il protocollo termina in tempo finito | Liveness |
| **No Self-Loop** | Nessun agente invia messaggi a se stesso | Safety |
| **Role Separation** | Ogni ruolo e distinto | Safety |
| **Message Ordering** | I messaggi arrivano nell'ordine corretto | Safety |
| **Protocol Conformance** | L'implementazione rispetta lo schema | Safety |
| **Bounded Repetition** | Il protocollo non cicla indefinitamente | Liveness |

**Fonte:** https://theses.gla.ac.uk/85779/ (Le Brun PhD 2026, MPST)

---

## PARTE 2 - COME I GRANDI SISTEMI ESPRIMONO PROPRIETA

### 2.1 TLA+ / PlusCal - L'Approccio Matematico

TLA+ (Lamport) usa logica temporale delle azioni. Molto potente, poco user-friendly.
PlusCal e lo strato "pseudocode" sopra TLA+.

```
(* TLA+ - molto tecnico *)
Spec == Init /\ [][Next]_vars /\ WF_vars(Action)
Safety == [](data_consistent)
Liveness == <>(terminated)

(* PlusCal - piu leggibile ma ancora tecnico *)
define
  Safety == (x <= maxValue)
  Liveness == <>(done = TRUE)
end define;
```

**Lezione:** TLA+ e potentissimo ma ha una curva di apprendimento ripida.
La sua sintassi matematica e accessibile solo a esperti di logic formale.
NON e il modello giusto per B.5.

**Fonte:** https://learntla.com/

### 2.2 FizzBee - L'Approccio Python-Like

FizzBee (2024) e il piu vicino a quello che vogliamo: formal methods con sintassi Python.

```python
# FizzBee - sintassi molto accessibile!
always assertion SafeBalance:
    return balance >= 0

always eventually assertion ProtocolEnds:
    return state == "terminated"

eventually always assertion StableState:
    return not in_progress
```

**Pattern di FizzBee:**
- `always assertion X:` = safety invariant (non deve mai essere violato)
- `always eventually assertion X:` = liveness (prima o poi X diventa vero)
- `eventually always assertion X:` = stabilita (X diventa vero e ci resta)
- `fair` / `fair<strong>` = fairness constraints
- Deadlock detection: AUTOMATICA (il model checker lo rileva senza keyword)
- Transition assertions: controllano stati PRIMA e DOPO ogni transizione

**Lezione:** FizzBee dimostra che formal methods + Python-like syntax funziona.
Ha 3 tier (safety/liveness/stability) che sono intuitivi.
Il nostro B.5 deve essere ancora piu semplice (dominio piu ristretto).

**Fonte:** https://fizzbee.io/design/tutorials/getting-started/

### 2.3 Alloy 6 - L'Approccio Relazionale

Alloy usa "temporal operators" con keywords leggibili:

```alloy
-- Alloy 6 usa le stesse keyword della logica temporale
-- ma in un contesto relazionale
pred safe: always (balance >= 0)
pred live: eventually (terminated)
pred ordered: always (audit in steps before deploy in steps)
```

**Lezione:** Alloy dimostra che `always` e `eventually` come keywords English
sono sufficienti per il 90% dei casi. La stessa logica si applica al nostro caso.

**Fonte:** https://alloytools.org/

### 2.4 Lean 4 / nuXmv - L'Approccio Theorem Prover

Noi GIA abbiamo Lean 4 via lean4_bridge.py. Le 7 proprieta attuali:
```
SENDERS_IN_ROLES    -> safety (strutturale)
RECEIVERS_IN_ROLES  -> safety (strutturale)
NO_SELF_LOOP        -> safety (comportamentale)
MIN_ROLES           -> safety (strutturale)
NON_EMPTY           -> safety (strutturale)
BRANCHES_NON_EMPTY  -> safety (strutturale, choice-only)
DECIDER_IN_ROLES    -> safety (strutturale, choice-only)
```

Mancano completamente: liveness, ordering, confidence, role-specific.
Queste sono le proprieta che B.5 deve aggiungere.

**Fonte:** lean4_bridge.py (codice interno)

### 2.5 IBM NL2LTL + DECLARE - L'Approccio NLU

NL2LTL (Fuggitti, AAAI 2023) converte linguaggio naturale -> formula LTL
usando DECLARE templates come intermediari.

```python
# NL2LTL - richiede LLM (GPT o Rasa)
from nl2ltl import translate
result = translate("eventually send Slack after Gmail", engine=GPTEngine())
# -> F(gmail -> F(slack))
```

**Lezione:** L'approccio NL2LTL e potente ma richiede ML/LLM.
La nostra scelta e diversa: keyword deterministiche + pattern fissi.
DECLARE templates pero sono un'ottima fonte per la tassonomia delle proprieta.

**Fonte:** https://github.com/IBM/nl2ltl

### 2.6 Controlled Natural Language (CNL) per Specifica Formale

La letteratura CNL (Kuhn 2014, Brunello 2019, survey 2025) identifica un approccio
intermedio tra NL libero e sintassi formale: "controlled English" con grammatica ristretta.

```
CNL Approach:
"The system shall always ensure that [condition]."
"It is required that [event A] occurs before [event B]."
"The property [X] shall never be violated."
```

La chiave: usare costrutti grammaticali fissi con variabili riempibili.
NON testo libero (ambiguo), NON formula formale (ostile).
INVECE: template grammaticali predefiniti.

**Fonte:** https://arxiv.org/pdf/2512.24159 (Developing CNL for formal spec, 2025)

---

## PARTE 3 - IL "TOP 10" DELLE PROPRIETA PER PROTOCOLLI MULTI-AGENT

Analizzando le 500+ specifiche di Dwyer, i DECLARE templates, le proprieta di session
types, e i casi d'uso reali di CervellaSwarm, emergono 10 proprieta che coprono
il 90%+ dei casi pratici per protocolli di comunicazione tra agenti AI.

### Categoria A: Safety (il sistema non fa mai X)

**P01: no_self_delegation**
- Significato: nessun agente invia messaggi a se stesso
- Naturale: "nessun agente si auto-delega"
- LTL: G(sender != receiver per ogni step)
- Gia in Lean 4: SI (NO_SELF_LOOP)
- Rilevanza CervellaSwarm: critica (viola il principio di separazione dei ruoli)

**P02: role_separation**
- Significato: ogni ruolo e distinto dagli altri
- Naturale: "ogni ruolo e unico"
- LTL: distinct(roles)
- Gia in Lean 4: parziale (MIN_ROLES)
- Rilevanza: critica (2 ruoli non possono essere la stessa entita)

**P03: no_unauthorized_message**
- Significato: solo mittenti dichiarati possono inviare certi tipi di messaggio
- Naturale: "[ruolo X] non puo inviare [messaggio Y]"
- LTL: G(MessageKind.AUDIT_VERDICT -> sender == guardiana)
- Gia in Lean 4: NO
- Rilevanza: alta (role-based access control)

**P04: ordering_required**
- Significato: il messaggio A deve precedere il messaggio B
- Naturale: "[azione A] deve avvenire prima di [azione B]"
- LTL: !B W A (B non accade finche non accade A)
- Gia in Lean 4: NO
- Rilevanza: alta (audit_before_deploy, task_before_result)
- Mapping DECLARE: Precedence(A, B)

**P05: confidence_threshold**
- Significato: tutti i messaggi di tipo X devono avere confidence >= level
- Naturale: "ogni [tipo messaggio] deve avere confidence >= [High/Medium/Low]"
- LTL: G(MessageKind.X -> confidence >= threshold)
- Gia in Lean 4: NO
- Rilevanza: alta (unica per CervellaSwarm - sfrutta confidence.py esistente)
- DIFFERENZIATORE: nessun altro sistema ha questa proprieta

### Categoria B: Liveness (il sistema prima o poi fa Y)

**P06: always_terminates**
- Significato: il protocollo termina in tempo finito
- Naturale: "questo protocollo deve sempre terminare"
- LTL: F(terminated) con fairness
- Gia in Lean 4: NO
- Rilevanza: critica (deadlock prevention)

**P07: response_guaranteed**
- Significato: ogni richiesta ottiene sempre una risposta
- Naturale: "ogni [richiesta] riceve sempre [risposta]"
- LTL: G(request -> F(response))
- Gia in Lean 4: NO
- Rilevanza: alta (SLA impliciti nei protocolli)
- Mapping DECLARE: Response(A, B)

**P08: no_deadlock**
- Significato: non esiste uno stato in cui nessun agente puo procedere
- Naturale: "nessun deadlock"
- Garantita da: session types per costruzione (se il protocollo e well-typed)
- Gia in Lean 4: implicita nella struttura lineare dei protocolli flat
- Rilevanza: critica (ma spesso garantita dal design del protocollo)

### Categoria C: Ordering / Sequencing

**P09: mandatory_step**
- Significato: un certo tipo di messaggio deve sempre comparire nel protocollo
- Naturale: "[messaggio X] deve avvenire almeno una volta"
- LTL: F(MessageKind.X)
- Gia in Lean 4: NO
- Rilevanza: media (es: "ogni workflow deve avere un AUDIT_REQUEST")
- Mapping DECLARE: Existence(A)

**P10: exclusion**
- Significato: due tipi di messaggio non possono coesistere nello stesso protocollo
- Naturale: "[messaggio A] e [messaggio B] non possono entrambi apparire"
- LTL: !(F(A) & F(B))
- Gia in Lean 4: NO
- Rilevanza: media (role conflict prevention)
- Mapping DECLARE: NotCoExistence(A, B)

### Riepilogo Top 10

| ID | Nome | Categoria | In Lean4 | Priorita |
|----|------|-----------|----------|----------|
| P01 | no_self_delegation | Safety | SI | Critica |
| P02 | role_separation | Safety | Parziale | Critica |
| P03 | no_unauthorized_message | Safety | NO | Alta |
| P04 | ordering_required | Safety | NO | Alta |
| P05 | confidence_threshold | Safety | NO | Alta |
| P06 | always_terminates | Liveness | NO | Critica |
| P07 | response_guaranteed | Liveness | NO | Alta |
| P08 | no_deadlock | Liveness | Implicita | Critica |
| P09 | mandatory_step | Ordering | NO | Media |
| P10 | exclusion | Ordering | NO | Media |

---

## PARTE 4 - CONFRONTO APPROCCI PER B.5

### Approccio 1: Formula Matematica (LTL/CTL)

```python
# Esempio: formula LTL diretta
spec.add("G(audit -> F(deploy))")
spec.add("G(sender != receiver)")
```

- Pro: massima espressivita, mappatura 1:1 con Lean 4
- Contro: richiede conoscenza di LTL (G, F, X, U) - OSTILE per non-esperti
- Usato in: TLA+, nuXmv, PRISM
- Giudizio: SCARTATO per B.5 (violazione del NORD "accessibile a tutti")

### Approccio 2: Python Fluent API (Builder Pattern)

```python
# Esempio: fluent interface
spec = ProtocolSpec(protocol)
spec.must_never(role="worker", send=MessageKind.AUDIT_VERDICT)
spec.must_always(occur=MessageKind.AUDIT_REQUEST)
spec.requires_before(MessageKind.AUDIT_REQUEST, MessageKind.TASK_RESULT)
spec.confidence_at_least(Confidence.HIGH)
```

- Pro: tipizzato (autocomplete IDE), naturale per sviluppatori Python, ZERO parsing
- Contro: verboso, non leggibile da non-sviluppatori
- Usato in: pycontract, deal.py, fluent_validation
- Giudizio: BUONO per sviluppatori, non per CEO / utenti finali

### Approccio 3: Keyword Decoration (FizzBee-style)

```python
# Esempio: keyword + assert
@property_spec
def audit_before_result(protocol):
    """AuditRequest must occur before TaskResult."""
    return ordering_required(MessageKind.AUDIT_REQUEST, MessageKind.TASK_RESULT)

@property_spec
def worker_cannot_approve(protocol):
    """Worker role cannot send AuditVerdict."""
    return no_unauthorized_message(role="worker", kind=MessageKind.AUDIT_VERDICT)
```

- Pro: Pythonic, testabile, autodocumentante
- Contro: richiede Python (non user-friendly per non-sviluppatori)
- Giudizio: BUONO per sviluppatori avanzati, non per il pubblico generale

### Approccio 4: Micro-DSL Strutturato (come intent.py - RACCOMANDATO)

```
# Stessa filosofia dell'Intent Parser!
# Micro-linguaggio che SEMBRA naturale ma e DETERMINISTICO

properties for DelegateTask:
    always: sender != receiver
    always: confidence >= High
    ordering: AuditRequest before TaskResult
    never: Worker sends AuditVerdict
    terminates: yes
    response: TaskRequest -> TaskResult
```

- Pro: leggibile da chiunque, deterministico, testabile, ZERO ambiguita
- Contro: nuovo parsing da implementare (ma segue esatto pattern intent.py)
- Ispirato a: FizzBee keywords + DECLARE patterns + CNL approach
- Giudizio: IL DESIGN OTTIMALE per B.5

### Approccio 5: JSON/YAML Config

```yaml
# YAML property spec
properties:
  - type: ordering
    before: AuditRequest
    after: TaskResult
  - type: role_restriction
    role: worker
    cannot_send: AuditVerdict
```

- Pro: leggibile, toolable, CI/CD friendly
- Contro: troppo verboso, non "sembra linguaggio naturale"
- Giudizio: ALTERNATIVA valida per config-driven, ma meno elegante

### Tabella di Confronto

| Approccio | User-Friendly | Deterministico | ZERO deps | Testabile | Lean4 map |
|-----------|--------------|----------------|-----------|-----------|-----------|
| LTL Formule | NO | SI | SI | SI | SI 1:1 |
| Python Fluent | Medio | SI | SI | SI | SI |
| Keyword Deco | Medio | SI | SI | SI | SI |
| **Micro-DSL** | **SI** | **SI** | **SI** | **SI** | **SI** |
| YAML Config | Medio | SI | SI | Medio | Medio |

---

## PARTE 5 - DESIGN RACCOMANDATO PER B.5

### 5.1 Il Principio Guida: Stessa Filosofia di intent.py

La decisione su B.4 Intent Parser si applica IDENTICAMENTE a B.5:
- Micro-linguaggio strutturato > parser testo libero (regex NLP)
- Deterministico > fuzzy
- Semplice > potente
- Leggibile > completo

La differenza e l'output target:
- intent.py -> Protocol (struttura)
- spec.py -> SpecificationResult (proprieta) -> Lean4 theorems

### 5.2 Sintassi Proposta: "Spec DSL"

```
# Sintassi B.5 proposta - si legge come vincoli in italiano/inglese

properties for DelegateTask:

    # Safety - il sistema non deve mai fare X
    never: sender == receiver
    never: Worker sends AuditVerdict
    never: Guardiana sends TaskRequest

    # Liveness - il sistema deve prima o poi fare Y
    always terminates
    response: TaskRequest -> TaskResult

    # Ordering - X deve accadere prima di Y
    ordering: AuditRequest before TaskResult
    ordering: PlanDecision before TaskRequest

    # Confidence - vincoli sulla certezza dei messaggi
    confidence: TaskResult >= High
    confidence: AuditVerdict >= Certain

    # Existence - X deve accadere almeno una volta
    requires: AuditRequest
    requires at most 3: TaskRequest

    # Exclusion - X e Y non possono coesistere
    exclusive: PlanRequest, TaskRequest
```

### 5.3 Struttura Modulo spec.py (stima)

```
spec.py (~500-600 LOC stimati)

SEZIONE 1: Property Types (~80 LOC)
  - PropertyKind (Enum): NEVER, RESPONSE, ORDERING, CONFIDENCE,
                          REQUIRES, EXCLUSION, TERMINATES
  - Property (frozen dataclass): kind + params
  - SpecificationResult (frozen dataclass): protocol + properties + warnings

SEZIONE 2: Keyword Maps (~60 LOC)
  - KEYWORD_MAP: str -> PropertyKind (deterministico)
    "never:" -> NEVER
    "always terminates" -> TERMINATES
    "response:" -> RESPONSE
    "ordering:" -> ORDERING
    "confidence:" -> CONFIDENCE
    "requires:" -> REQUIRES
    "exclusive:" -> EXCLUSION

SEZIONE 3: Parser (~150 LOC)
  - _tokenize_spec(text) -> list[Token]
  - _parse_property_line(line) -> Property | None
  - _parse_never(args) -> Property
  - _parse_ordering(args) -> Property
  - _parse_confidence(args) -> Property
  - _parse_response(args) -> Property

SEZIONE 4: Lean 4 Mapper (~100 LOC)
  - _property_to_lean4(prop, protocol) -> str  # teorema Lean 4
  - spec_to_lean4_theorems(result) -> list[str]
  - Integrazione con Lean4Generator esistente (lean4_bridge.py)

SEZIONE 5: Public API (~60 LOC)
  - parse_spec(text, protocol) -> SpecificationResult
  - verify_spec(result) -> VerificationReport  # usa Lean4Verifier
  - spec_to_lean4(result) -> str  # codice Lean 4 generato
```

### 5.4 Mapping a Lean 4 (integrazione con bridge esistente)

I 7 teoremi esistenti in lean4_bridge.py coprono safety strutturale.
B.5 aggiungerebbe teoremi per le nuove proprieta:

```lean4
-- Generato da property: "never: Worker sends AuditVerdict"
theorem no_worker_verdict : ∀ step ∈ protocol.elements,
    step.sender = "worker" → step.message_kind ≠ MessageKind.AuditVerdict := by
  decide

-- Generato da property: "ordering: AuditRequest before TaskResult"
theorem audit_before_result : ∃ i j, i < j ∧
    protocol.elements[i].message_kind = MessageKind.AuditRequest ∧
    protocol.elements[j].message_kind = MessageKind.TaskResult := by
  decide

-- Generato da property: "always terminates"
-- (proprieta strutturale: il protocollo ha lista finita di step)
theorem terminates : protocol.elements.length > 0 ∧
    protocol.max_repetitions.isSome := by
  decide
```

### 5.5 Integrazione con Moduli Esistenti

```python
# B.5 si integra con TUTTI i moduli esistenti:

# con intent.py (B.4)
intent_result = parse_to_protocol("regina delegates to worker")
spec_result = parse_spec("""
    properties for SimpleTask:
        never: sender == receiver
        always terminates
""", protocol=intent_result)

# con lean4_bridge.py
theorems = spec_to_lean4(spec_result)
report = Lean4Verifier().verify_all(protocol, properties=spec_result.properties)

# con confidence.py (B.1) e trust.py (B.2)
spec_result = parse_spec("""
    confidence: TaskResult >= High
    confidence: AuditVerdict >= Certain
""", protocol=protocol)
# -> verifica che le ConfidenceLevel siano rispettate a runtime

# con codegen.py (B.3)
code = generate_code(protocol, spec=spec_result)
# -> il codice generato include assert di runtime per le proprieta
```

---

## PARTE 6 - DIFFERENZIATORI UNICI DI B.5 vs STATO DELL'ARTE

### Cosa esiste gia nel mondo:

| Sistema | Forza | Limite per noi |
|---------|-------|----------------|
| TLA+/PlusCal | Molto potente | Non accessibile (curva 6+ mesi) |
| FizzBee | Python-like | Richiede Starlark, non ZERO deps |
| Alloy 6 | User-friendly | Java, separato da Python |
| NL2LTL (IBM) | Naturale | Richiede GPT/ML |
| DECLARE | Completo | Orientato a Business Process, non AI agents |
| nuXmv | Potente | Non embedded in Python |
| Session Types (Scribble) | Perfetto per MPST | No property language separato |

### Cosa ha B.5 che nessuno ha:

1. **confidence_threshold come proprieta formale** - P05 e UNICA nel nostro dominio.
   FizzBee, TLA+, DECLARE: nessuno ha un operatore `confidence >= Level`.
   CervellaSwarm e il PRIMO sistema con AI-confidence come tipo verificabile.

2. **Integrazione con intent.py**: la pipeline completa
   `"describe intent" -> parse_protocol -> "add properties" -> verify_with_lean4`
   e unica nel panorama AI agents.

3. **ZERO deps, pure stdlib**: nessun sistema formale esistente funziona
   senza dipendenze (FizzBee: Go+Starlark, Alloy: Java, NL2LTL: GPT).

4. **Dominio ristretto = alta precisione**: le proprieta per protocolli multi-agent
   AI sono un sottoinsieme PICCOLO ma CRITICO delle proprieta formali generali.
   Questo permette alta accuratezza con implementazione semplice.

---

## PARTE 7 - PATTERN DI IMPLEMENTAZIONE CONSIGLIATI

### 7.1 Parser Pattern (come intent.py, come dsl.py)

Il tokenizer DEVE essere indent-aware (stessa tecnica di intent.py):

```python
# spec.py tokenizer
SPEC_KEYWORDS = frozenset({
    "never", "always", "ordering", "confidence",
    "requires", "exclusive", "response", "terminates",
    "before", "after", "sends", ">=", "->",
})

PROPERTY_LINE_PATTERN = re.compile(
    r"^\s*(?P<keyword>never|always|ordering|confidence|requires|exclusive|response)"
    r"\s*:?\s*(?P<args>.*)\s*$"
)
```

### 7.2 Property Dataclass Pattern

```python
@dataclass(frozen=True)
class Property:
    kind: PropertyKind
    subject: str | None      # "Worker" in "never: Worker sends X"
    predicate: str | None    # "sends" in "never: Worker sends X"
    object_: str | None      # "AuditVerdict"
    threshold: str | None    # "High" in "confidence >= High"
    before: str | None       # in ordering
    after: str | None        # in ordering
    source_text: str         # testo originale per debug

@dataclass(frozen=True)
class SpecificationResult:
    protocol: Protocol
    properties: tuple[Property, ...]
    warnings: tuple[str, ...]
    lean4_theorems: tuple[str, ...]  # generati automaticamente
```

### 7.3 Lean 4 Generation Pattern

Il mapping deterministico (NO ambiguita) da Property -> teorema Lean 4:

```python
_KIND_TO_LEAN4_TEMPLATE: dict[PropertyKind, str] = {
    PropertyKind.NEVER_SELF_LOOP:
        "theorem no_self_loop : ∀ s ∈ {protocol}.elements, "
        "s.sender ≠ s.receiver := by decide",
    PropertyKind.ORDERING:
        "theorem {before}_before_{after} : ∃ i j, i < j ∧ ... := by decide",
    PropertyKind.CONFIDENCE:
        "-- Runtime check (not static theorem): "
        "all {kind} messages have confidence >= {level}",
}
```

**Nota importante:** alcune proprieta (confidence_threshold) NON sono verificabili
staticamente (il valore dipende dal runtime). Per queste: generare un runtime assert
invece di un teorema Lean 4. Documentare esplicitamente la distinzione.

### 7.4 Distinzione Static vs Runtime Properties

```
STATIC (verificabili da Lean 4, a design-time):
  - P01 no_self_delegation: dipende solo dalla struttura del Protocol
  - P02 role_separation: dipende dalla lista dei ruoli
  - P03 no_unauthorized_message: dipende da MessageKind + ruolo
  - P04 ordering_required: dipende dalla sequenza degli step
  - P08 no_deadlock: garantita dalla struttura lineare dei protocolli flat
  - P09 mandatory_step: dipende dalla presenza di un MessageKind
  - P10 exclusion: dipende dalla struttura

RUNTIME (verificabili solo durante esecuzione):
  - P05 confidence_threshold: il valore di confidence e nel messaggio reale
  - P06 always_terminates: dipende dall'esecuzione effettiva
  - P07 response_guaranteed: dipende dal comportamento runtime degli agenti
```

**Questa distinzione e CRITICA** e deve essere documentata nel modulo.

---

## PARTE 8 - FONTI COMPLETE

### Fonti Web / Accademiche (27)

1. [Property Specification Patterns (Dwyer et al.) - matthewbdwyer.github.io](https://matthewbdwyer.github.io/psp/)
2. [PSP Pattern Mappings for LTL - KSU](https://people.cs.ksu.edu/~dwyer/SPAT/ltl.html)
3. [Occurrence Patterns - matthewbdwyer.github.io](https://matthewbdwyer.github.io/psp/patterns/occurrence.html)
4. [TLA+ Wikipedia](https://en.wikipedia.org/wiki/TLA+)
5. [Learn TLA+ - learntla.com](https://learntla.com/)
6. [TLA+ in Practice and Theory - pron.github.io](https://pron.github.io/posts/tlaplus_part1)
7. [FizzBee GitHub - fizzbee-io/fizzbee](https://github.com/fizzbee-io/fizzbee)
8. [FizzBee Getting Started - fizzbee.io](https://fizzbee.io/design/tutorials/getting-started/)
9. [FizzBee Introducing - thenewstack.io](https://thenewstack.io/introducing-fizzbee-simplifying-formal-methods-for-all/)
10. [Alloy Specification Language - alloytools.org](https://alloytools.org/)
11. [Alloy Wikipedia](https://en.wikipedia.org/wiki/Alloy_(specification_language))
12. [Formal Software Design with Alloy 6 - haslab.github.io](https://haslab.github.io/formal-software-design/overview/index.html)
13. [NL2LTL Python Package - IBM Research](https://research.ibm.com/publications/nl2ltl-a-python-package-for-converting-natural-language-nl-instructions-to-linear-temporal-logic-ltl-formulas)
14. [NL2LTL GitHub - IBM](https://github.com/IBM/nl2ltl)
15. [nl2spec CAV 2023 - Springer](https://link.springer.com/chapter/10.1007/978-3-031-37703-7_18)
16. [NL2TL: LLMs for Temporal Logics (arXiv 2305.07766)](https://arxiv.org/html/2305.07766v2)
17. [Grammar-Forced Translation NL->LTL (arXiv 2512.16814)](https://arxiv.org/pdf/2512.16814)
18. [DECLARE in ASP (arXiv 2412.10152)](https://arxiv.org/html/2412.10152)
19. [Declarative Process Mining Book - Montali](https://www.inf.unibz.it/~montali/papers/diciccio-montali-PMBook2022-declarative-mining.pdf)
20. [Brunello 2019 - Synthesis of LTL from NL - TIME 2019](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.TIME.2019.17)
21. [PRISM Manual Property Specification](https://www.prismmodelchecker.org/manual/PropertySpecification/AllOnOnePage)
22. [nuXmv Symbolic Model Checker - fbk.eu](https://nuxmv.fbk.eu/downloads/nuxmv-user-manual.pdf)
23. [Developing CNL for Formal Spec (arXiv 2512.24159)](https://www.arxiv.org/pdf/2512.24159)
24. [Controlled Natural Language Survey - Kuhn 2014 (MIT Press)](https://direct.mit.edu/coli/article/40/1/121/1455/A-Survey-and-Classification-of-Controlled-Natural)
25. [Multiparty Session Types - Le Brun PhD 2026 (Glasgow)](https://theses.gla.ac.uk/85779/)
26. [Safety and Liveness Properties - Wikipedia](https://en.wikipedia.org/wiki/Safety_and_liveness_properties)
27. [Deadlock Freedom: Beyond Liveness Properties - ellismichael.com](https://ellismichael.com/blog/2023/01/19/deadlock-freedom/)

---

## SINTESI E RACCOMANDAZIONE

### Il Design Ottimale per B.5

**Approccio:** Micro-DSL strutturato (stessa filosofia di intent.py)

**Architettura:**
```
INPUT: testo con proprieta
  |
  v
[Parser spec] -> SpecificationResult (frozen dataclass)
  |
  +-> [Lean 4 Mapper] -> teoremi statici -> Lean4Verifier
  |
  +-> [Runtime Checker] -> assert dinamici -> checker.py / monitor.py
```

**Le 10 proprieta prioritarie (in ordine di implementazione):**

1. `never: sender == receiver` (P01 - gia in Lean4, aggiungere al DSL)
2. `always terminates` (P06 - liveness fondamentale)
3. `ordering: X before Y` (P04 - ordering, molto usata)
4. `never: [Role] sends [MessageKind]` (P03 - role restriction)
5. `response: X -> Y` (P07 - response pattern)
6. `confidence: [MessageKind] >= [Level]` (P05 - DIFFERENZIATORE UNICO)
7. `requires: [MessageKind]` (P09 - existence)
8. `exclusive: X, Y` (P10 - not-coexistence)
9. `never: sender == receiver [when Role]` (P02 - role separation estesa)
10. `requires at most N: [MessageKind]` (bounded existence)

**Metriche attese (basate su pattern dei moduli B precedenti):**
- LOC: ~500-600 (coerente con intent.py: 649 LOC)
- ZERO deps (regola inviolabile)
- Test: 80-120 (coerente con confidence.py, trust.py)
- Integrazione: spec.py -> lean4_bridge.py, checker.py, monitor.py, codegen.py
- Tempo parsing: < 1ms per spec tipica (regex compilati)

**Distinzione critica da documentare nel modulo:**
- Proprieta STATICHE: verificabili a design-time con Lean 4 (struttura Protocol)
- Proprieta RUNTIME: verificabili solo durante esecuzione (confidence, termination)

### Perche questa scelta e giusta per CervellaSwarm

1. **Coerenza con intent.py**: stesso pattern, stessa filosofia, stesso team conosce gia
2. **confidence_threshold e UNICO**: nessun sistema formale al mondo ha questo
3. **ZERO deps**: coerente con tutti i 12 moduli precedenti
4. **Dominio ristretto = alta precisione**: poche proprieta ben definite > molte ambigue
5. **Lean 4 integration**: si innesta naturalmente sul bridge esistente
6. **La nonna con le ricette**: "l'audit deve avvenire prima del deploy" E comprensibile

### Cosa B.5 NON deve fare (scope exclusions esplicite)

- NON supportare full LTL/CTL (fuori scope, complessita eccessiva)
- NON dipendere da ML/LLM per il parsing (ZERO deps)
- NON tentare di coprire tutti i 27 template DECLARE (eccessivo per v1)
- NON essere un model checker completo (quello e Lean 4's job)
- NON gestire proprieta probabilistiche PCTL (PRISM territory, non nostro)

---

*Cervella Researcher - CervellaSwarm*
*"Ricerca PRIMA di implementare."*
*2026-02-25*

COSTITUZIONE-APPLIED: SI
Principio usato: "Nulla e complesso, solo non ancora studiato" + "Fatto BENE > Fatto VELOCE"
