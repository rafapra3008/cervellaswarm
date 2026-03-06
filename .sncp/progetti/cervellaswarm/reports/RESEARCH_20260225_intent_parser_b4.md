# Intent Parser B.4 - Ricerca Completa
## Da Linguaggio Naturale a Specifica Formale

**Data:** 2026-02-25
**Autrice:** Cervella Researcher
**Fonti consultate:** 28 (20 web + 8 interne/accademiche)
**Status:** COMPLETA

---

## CONTESTO: Cosa Deve Produrre Intent Parser

L'output di B.4 e un oggetto `Protocol` della Lingua Universale:

```python
# La struttura target (da protocols.py)
Protocol(
    name="MyWorkflow",
    roles=("regina", "worker", "guardiana"),
    elements=(
        ProtocolStep(sender="regina", receiver="worker",
                     message_kind=MessageKind.TASK_REQUEST),
        ProtocolStep(sender="worker", receiver="regina",
                     message_kind=MessageKind.TASK_RESULT),
    ),
    max_repetitions=1,
    description="Extracted from: 'regina asks worker to do X, worker responds'"
)
```

L'input e testo libero in linguaggio naturale come:
- "La Regina manda un task al Worker, il Worker risponde con il risultato, poi la Guardiana verifica"
- "coordinator asks researcher for a report, researcher returns findings, coordinator reviews"
- "agent A delegates to agent B, B completes and notifies A"

---

## PARTE 1 - PANORAMICA APPROCCI ESISTENTI

### 1.1 Intent Recognition Senza LLM: Lo Stato dell'Arte

La letteratura e il software esistente identificano tre famiglie principali:

#### A) Keyword-Based Matching (piu leggero)

**Adapt Intent Parser** (Mycroft AI, open source)
- Architettura: keyword registration + IntentBuilder con require/optionally
- Funzionamento: `IntentBuilder('PlayMusic').require('PlayVerb').require('Artist').build()`
- Entita: dizionari di sinonimi per ogni concetto
- Forza: ZERO ML, deterministico, funziona su embedded devices
- Limite: vocabolario fisso, nessuna gestione di frasi non previste
- Fonte: https://github.com/MycroftAI/adapt

**Padatious** (Mycroft AI)
- Architettura: template con slot variables, `"ask {Role} to {Action}"`
- Forza: piu flessibile di Adapt, gestisce variazioni naturali
- Limite: richiede neural network training (non stdlib)
- Fonte: https://mycroft-ai.gitbook.io/docs/mycroft-technologies/padatious

**Python `re` module con named groups**
- Il metodo piu leggero possibile: ZERO deps, stdlib puro
- Pattern: `(?P<sender>\w+)\s+(?:sends?|asks?|delegates?)\s+(?P<receiver>\w+)`
- `re.match(pattern, text).groupdict()` -> dict con slot estratti
- Limite: fragile su variazioni sintattiche non previste
- Fonte: https://timothygebhard.de/posts/named-groups-in-regex-in-python/

#### B) Template-Based / Semi-Formale

**Pseudocode DSL approach** (ricerca accademica)
- Input: requirements in linguaggio naturale
- Stage 1: dependency parsing + conditional keyword extraction
- Stage 2: mapping a intermediate representation (pseudocode)
- Stage 3: rule-based translation al formato formale
- Keyword mapping: "if/when/while" -> if-block, "until" -> until-block
- Questo e esattamente il pattern REQ2LTL (vedi sotto)
- Fonte: https://arxiv.org/html/2309.13272

**Req2LTL / OnionL Framework**
- Intermediate Representation: OnionL - albero compositivo
- 3 elementi: Atomic Propositions (Com/Var/Rel/Formula), Scopes, Relations
- Keyword mapping formalizzato:
  - "always" -> Globally (G)
  - "eventually" -> Eventually (F)
  - "next" -> Next (X)
  - "if...then" -> Implication (->)
  - "and/or" -> Conjunction/Disjunction
  - "unless/until" -> Until operator
- Risultati: 88.4% semantic accuracy, 100% syntactic correctness
- Fonte: https://arxiv.org/html/2512.17334v1

#### C) Hybrid: Rule-based Core + Optional ML

**Rasa NLU RulePolicy**
- ML per classificazione intent, ma `RulePolicy` per enforcement deterministico
- RegexFeaturizer: regex come features (non regole)
- Rule-based component sovrascrive ML se applicabile
- Lesson: "use rule-based as a fast filter for obvious cases"
- Fonte: https://rasa.com/blog/rasa-nlu-in-depth-part-1-intent-classification/

**Dialogflow / LUIS**
- LUIS: pattern utterances con `{entity}` slots, machine-learning + text-matching
- Dialogflow: training phrases + ML expansion automatica
- Lezione chiave: tutti i sistemi produzione COMBINANO keyword/regex con ML
- Fonte: https://learn.microsoft.com/en-us/azure/ai-services/LUIS/luis-how-to-model-intent-pattern

---

## PARTE 2 - NL A SPECIFICA FORMALE: RICERCA ACCADEMICA

### 2.1 Il Problema Fondamentale

La letteratura 2024-2025 (Frontiers in Computer Science, ScienceDirect, arXiv) identifica
tre sfide principali nella traduzione NL -> specifica formale:

1. **Ambiguita**: stessa frase, significati diversi a seconda del contesto
2. **Variabilita**: "A asks B", "A delegates to B", "A sends request to B" = stessa cosa
3. **Incomplezza**: il testo naturale spesso omette il ovvio

### 2.2 Pipeline a 3 Stage: Il Pattern Piu Diffuso

Tutti i sistemi accademici recenti usano la stessa architettura:

```
TESTO NATURALE
     |
     v
[Stage 1: PARSING] -- keyword extraction, entity detection, role identification
     |
     v
[Stage 2: INTERMEDIATE REPRESENTATION] -- semi-formale, verificabile da umano
     |
     v
[Stage 3: FORMAL TRANSLATION] -- regole deterministiche IR -> formato target
```

Questo pattern appare in:
- REQ2LTL (OnionL IR -> LTL formula)
- NLP-Based Requirements Formalization (dep-parsing -> tabular IR -> pseudocode)
- VERIFAI (NLP + ontology -> semi-automated formal spec)

**Fonte principale pipeline:** https://ceur-ws.org/Vol-1564/paper20.pdf

### 2.3 Specification Mining: Il Caso Caruca

Caruca (2025) risolve un problema contiguo: estrarre specifiche da documentazione.
Approccio: LLM per convertire doc -> structured invocation syntax, poi esecuzione
concreta per verificare proprieta.

**Lezione per noi:** anche senza LLM, la stessa idea funziona con regex su testo
strutturato. Il testo dell'utente e piu strutturato della documentazione raw.
Fonte: https://arxiv.org/abs/2510.14279

### 2.4 Formal Methods + NL: Survey 2025

La review su Frontiers (Marzo 2025) identifica le direzioni future:
- Human-in-the-loop per casi ambigui
- Intermediate representation verificabile
- Multi-stage prompting per LLM (ma anche regex!)

La LLM non serve per la classificazione deterministica; serve solo per
i casi ambigui/non previsti. Il 70-80% dei casi tipici e coperto da
regex + keyword matching.

Fonte: https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2025.1519437/full

### 2.5 Property Extraction: Safety vs Liveness

La distinzione classica di Lamport/Alpern-Schneider applicata al nostro caso:

**Safety properties** (il sistema non fa mai X):
- Keywords trigger: "never", "must not", "forbidden", "no X allowed"
- Esempio: "nessun dato perso" -> safety property `no_data_loss`
- Pattern: negazione + substantivo/verbo d'azione

**Liveness properties** (il sistema fa eventualmente Y):
- Keywords trigger: "always responds", "eventually", "guaranteed", "must eventually"
- Esempio: "sempre risponde" -> liveness property `always_responds`
- Pattern: avverbio di certezza + verbo di completamento

**Proprieta composte** (auth_required, max_retries):
- "requires authentication" / "auth needed" -> `auth_required`
- "retries up to N times" / "at most N attempts" -> `max_retries(N)`

Fonte: https://www.hillelwayne.com/post/safety-and-liveness/
Fonte accademica: https://www.cs.cornell.edu/fbs/publications/RecSafeLive.pdf

---

## PARTE 3 - ANALISI PER IL NOSTRO CASO SPECIFICO

### 3.1 Vincoli Architetturali

La Lingua Universale ha questi vincoli ferrei:
- ZERO deps esterne (tutto stdlib Python)
- Pattern frozen dataclasses + template-based come lean4_bridge.py e codegen.py
- Output: oggetto `Protocol` valido o errore esplicito
- Deve funzionare con i MessageKind esistenti (14 valori)
- Deve riconoscere i ruoli AgentRole (17 valori + nomi custom)

### 3.2 I Vocabulary da Mappare

#### Ruoli (riconoscimento fuzzy):

```python
ROLE_ALIASES = {
    # Standard CervellaSwarm roles
    "regina": "regina", "queen": "regina", "coordinator": "regina",
    "orchestrator": "regina", "hub": "regina",
    "worker": "worker", "agent": "worker", "executor": "worker",
    "guardiana": "guardiana", "guardian": "guardiana",
    "auditor": "guardiana", "reviewer": "guardiana",
    "architect": "architect", "planner": "architect",
    "researcher": "researcher", "researcher": "researcher",
    # Generic
    "a": None,  # placeholder, needs disambiguation
    "b": None,
}
```

#### Azioni -> MessageKind:

```python
ACTION_TO_MESSAGEKIND = {
    # Task delegation
    "delegates": MessageKind.TASK_REQUEST,
    "assigns": MessageKind.TASK_REQUEST,
    "asks to do": MessageKind.TASK_REQUEST,
    "sends task": MessageKind.TASK_REQUEST,
    "requests work": MessageKind.TASK_REQUEST,
    # Task result
    "responds with result": MessageKind.TASK_RESULT,
    "returns result": MessageKind.TASK_RESULT,
    "completes and notifies": MessageKind.TASK_RESULT,
    "sends result": MessageKind.TASK_RESULT,
    # Audit
    "requests audit": MessageKind.AUDIT_REQUEST,
    "asks to verify": MessageKind.AUDIT_REQUEST,
    "sends for review": MessageKind.AUDIT_REQUEST,
    "verifies": MessageKind.AUDIT_VERDICT,
    "approves": MessageKind.AUDIT_VERDICT,
    "rejects": MessageKind.AUDIT_VERDICT,
    # Plan
    "asks for plan": MessageKind.PLAN_REQUEST,
    "proposes plan": MessageKind.PLAN_PROPOSAL,
    "decides on plan": MessageKind.PLAN_DECISION,
    # Research
    "queries": MessageKind.RESEARCH_QUERY,
    "asks for research": MessageKind.RESEARCH_QUERY,
    "reports findings": MessageKind.RESEARCH_REPORT,
}
```

#### Structural keywords (protocol structure):

```python
STEP_SEPARATORS = [
    r",\s*then\s+",          # "A asks B, then B responds"
    r";\s*",                  # "A asks B; B responds"
    r"\.\s+",                 # "A asks B. B responds."
    r"\s+and\s+then\s+",     # "A asks B and then B responds"
    r"\s+after\s+that\s+",   # "A asks B. After that B responds."
    r"\s+next[,\s]+",        # "A asks B. Next, B responds"
    r"\s+subsequently\s+",   # technical writing
]

BRANCH_INDICATORS = [
    r"(?:if|when)\s+(?:approved|accepted)",   # "if approved, A sends X"
    r"(?:if|when)\s+(?:rejected|refused)",    # "if rejected, A sends Y"
    r"either\s+.+\s+or\s+",                  # "either approve or reject"
    r"(?:approve|reject)\s+(?:branch|case)",  # "approve branch: ..."
]
```

### 3.3 Pipeline Raccomandata per B.4

Basandosi su TUTTI gli approcci studiati, la pipeline ottimale per il nostro
vincolo (ZERO deps, stdlib) e:

```
INPUT: testo naturale
  |
  v
[STAGE 1: SENTENCE TOKENIZER]
  - Splitta su STEP_SEPARATORS
  - Output: lista di "step sentences"
  - Tools: re.split(), str.split() - STDLIB
  |
  v
[STAGE 2: ROLE + ACTION EXTRACTOR per ogni sentence]
  - Pattern: "ROLE VERB ROLE" (Subject-Verb-Object)
  - Named groups regex: (?P<sender>...)\s+(?P<verb>...)\s+(?P<receiver>...)
  - Fuzzy lookup in ROLE_ALIASES (lowercase, strip)
  - Verb -> MessageKind lookup in ACTION_TO_MESSAGEKIND
  - Tools: re module - STDLIB
  |
  v
[STAGE 3: BRANCH DETECTOR]
  - Cerca BRANCH_INDICATORS nel testo originale
  - Se trovati: raggruppa step per branch (approve/reject)
  - Crea ProtocolChoice invece di ProtocolStep
  - Tools: re module - STDLIB
  |
  v
[STAGE 4: PROPERTY EXTRACTOR]
  - Cerca safety/liveness keywords
  - Mappa a IntentProperties (nuovo dataclass frozen)
  - Es: "never loses data" -> no_data_loss=True
  - Tools: re module - STDLIB
  |
  v
[STAGE 5: PROTOCOL ASSEMBLER]
  - Raccoglie tutti i ruoli unici -> tuple[str, ...]
  - Assembla elements in ordine -> tuple[ProtocolElement, ...]
  - Costruisce Protocol(name, roles, elements, description)
  - Valida con Protocol.__post_init__ (gia presente!)
  - Tools: dataclasses, typing - STDLIB
  |
  v
OUTPUT: Protocol | ParseError
```

### 3.4 Struttura Dati Intermedia (Intermediate Representation)

Ispirato a OnionL e all'approccio dep-parsing -> tabular IR:

```python
@dataclass(frozen=True)
class IntentStep:
    """Un singolo step estratto dal testo naturale."""
    sender_raw: str          # "la Regina", "A", "coordinator"
    sender_resolved: str     # "regina", "worker", None
    receiver_raw: str
    receiver_resolved: str
    action_raw: str          # "asks", "delegates to", "sends"
    message_kind: MessageKind | None  # None se non risolto
    confidence: float        # 0.0-1.0, quant'e certa la risoluzione
    source_text: str         # il frammento originale


@dataclass(frozen=True)
class IntentBranch:
    """Un branch condizionale estratto dal testo."""
    condition_raw: str       # "if approved", "when rejected"
    branch_name: str         # "approve", "reject", "branch_1"
    steps: tuple[IntentStep, ...]


@dataclass(frozen=True)
class IntentParseResult:
    """Risultato intermedio del parsing, prima di Protocol assembly."""
    name: str                # derivato dal testo o parametro
    steps: tuple[IntentStep, ...]
    branches: tuple[IntentBranch, ...]
    properties: tuple[str, ...]  # "no_data_loss", "auth_required"
    warnings: tuple[str, ...]    # "role 'A' unresolved, defaulted to 'agent_a'"
    confidence: float            # media delle confidence degli step
```

### 3.5 Pattern di Errore da Evitare

Studiando i fallimenti comuni nella letteratura (Frontiers 2025, arXiv 2309.13272):

1. **Oversimplification trap**: non assumere che "A -> B" sia sempre TaskRequest.
   Il verb indica il tipo. Senza verb, la confidence deve essere bassa.

2. **Silent failures**: NON restituire Protocol vuoto su input ambiguo.
   Restituire IntentParseResult con warnings espliciti. L'utente deve sapere.

3. **Role conflation**: "reviewer" potrebbe essere "guardiana" o un ruolo custom.
   Soluzione: restituire il nome raw come fallback, non forzare la mappatura.

4. **Single-verb assumption**: "A asks B to do X and report back" e un STEP, non due.
   Il verb composto deve essere riconosciuto come unita.

5. **Order sensitivity**: "B reports to A, then A asks C" deve mantenere l'ordine.
   Non riordinare MAI le steps estratte.

---

## PARTE 4 - CONFRONTO APPROCCI: PRO E CONTRO

| Approccio | ZERO deps | Deterministico | Copertura | Manutenibilita |
|-----------|-----------|---------------|-----------|----------------|
| Regex puro (stdlib) | SI | SI | Bassa (brittle) | Alta (esplicito) |
| Keyword lookup (stdlib) | SI | SI | Media | Alta |
| TF-IDF cosine (scikit-learn) | NO | NO | Media-alta | Media |
| Adapt-style (adattato) | SI* | SI | Media-alta | Alta |
| OnionL full | NO (BERT) | Parziale | Alta | Bassa |
| LLM-based | NO | NO | Molto alta | Bassa |

*Adapt ha deps (PyPI), ma il suo PATTERN e replicabile stdlib-only

### La Nostra Scelta: Regex + Keyword (Adapt Pattern, stdlib-only)

**Perche:**
- Coerente con lean4_bridge.py e codegen.py (template-based, zero deps)
- Risultati deterministici: stessa input = stesso Protocol
- Confidence score esplicito per ogni risoluzione
- Fallback graceful: nomi raw come ruoli custom se non risolti
- Human-readable: le regole sono visibili nel codice, non in un modello opaco
- Test coverage: ogni regola e testabile in isolamento (come i nostri 1380 test)

---

## PARTE 5 - ARCHITETTURA MODULO intent.py

### 5.1 Struttura File (ispirata a codegen.py: 730 LOC, template-based)

```
intent.py (~500-600 LOC stimati)

SEZIONE 1: Constants (~80 LOC)
  - ROLE_ALIASES: dict[str, str | None]
  - ACTION_PATTERNS: list[tuple[re.Pattern, MessageKind]]
  - STEP_SEPARATOR_PATTERN: re.Pattern
  - BRANCH_INDICATOR_PATTERN: re.Pattern
  - PROPERTY_PATTERNS: list[tuple[re.Pattern, str]]

SEZIONE 2: Result types (~80 LOC)
  - IntentStep (frozen dataclass)
  - IntentBranch (frozen dataclass)
  - IntentProperties (frozen dataclass)
  - IntentParseResult (frozen dataclass)
  - ParseError (Exception subclass)

SEZIONE 3: Internal helpers (~120 LOC)
  - _normalize(text) -> str
  - _resolve_role(raw) -> tuple[str, float]  # (resolved, confidence)
  - _resolve_action(raw) -> tuple[MessageKind | None, float]
  - _split_steps(text) -> list[str]
  - _extract_step(sentence) -> IntentStep | None
  - _detect_branches(text) -> list[IntentBranch]
  - _extract_properties(text) -> IntentProperties

SEZIONE 4: Public API (~80 LOC)
  - parse_intent(text, name=None) -> IntentParseResult
  - intent_to_protocol(result) -> Protocol  # assembla il Protocol
  - parse_to_protocol(text, name=None) -> Protocol  # convenience shortcut

SEZIONE 5: Convenience functions (~40 LOC)
  - suggest_corrections(result) -> list[str]  # hint per warning risoluzione
  - format_parse_report(result) -> str  # debug output human-readable
```

### 5.2 API Pubblica Finale (come DSL)

```python
from cervellaswarm_lingua_universale import parse_to_protocol

# Caso semplice
p = parse_to_protocol(
    "Regina delegates task to worker. Worker returns result. "
    "Regina then asks guardiana to verify.",
    name="SimpleAuditFlow"
)
# -> Protocol(name="SimpleAuditFlow",
#             roles=("regina", "worker", "guardiana"),
#             elements=(step1, step2, step3))

# Caso con proprieta
result = parse_intent(
    "coordinator asks researcher for report. Researcher sends findings. "
    "System must never lose data. Always responds within timeout.",
    name="ResearchWithGuarantees"
)
result.properties  # ("no_data_loss", "always_responds")
result.warnings    # [] (tutto risolto)
result.confidence  # 0.87

# Caso con branch
p = parse_to_protocol(
    "Regina asks architect for plan. Architect proposes. "
    "If approved: Regina assigns to worker, worker returns result. "
    "If rejected: Regina sends feedback to architect.",
    name="ArchitectDecision"
)
```

### 5.3 Casi Limite da Gestire

Questi emergono dall'esperienza con lean4_bridge.py (Bug Hunt #9):

1. **Empty input**: `parse_to_protocol("")` -> `ParseError("text cannot be empty")`
2. **Single role**: solo un agente menzionato -> `ParseError("protocol needs at least 2 roles")`
3. **No action verb**: "regina e worker" senza verbo -> IntentStep con confidence=0.0
4. **Circular send**: "A asks B, B asks A" -> valido (A != B, check gia in ProtocolStep)
5. **Max repetitions keyword**: "up to 3 times" / "al massimo 3 ripetizioni" -> max_repetitions=3
6. **Multilingual**: italiano e inglese entrambi supportati (ROLE_ALIASES bilingue)

---

## PARTE 6 - FONTI COMPLETE

### Fonti Web (20)

1. [Adapt Intent Parser - Mycroft AI GitHub](https://github.com/MycroftAI/adapt)
2. [Adapt Tutorial - Mycroft AI Docs](https://mycroft-ai.gitbook.io/docs/mycroft-technologies/adapt/adapt-tutorial)
3. [Padatious - Mycroft AI Docs](https://mycroft-ai.gitbook.io/docs/mycroft-technologies/padatious)
4. [Use intent parsers for open source home automation - Opensource.com](https://opensource.com/article/20/6/mycroft-intent-parsers)
5. [Rule-based matching - spaCy Documentation](https://spacy.io/usage/rule-based-matching)
6. [Intent Classification Architecture - AI Monks / Medium](https://medium.com/aimonks/intent-classification-generative-ai-based-application-architecture-3-79d2927537b4)
7. [Rasa NLU in Depth: Intent Classification - Rasa Blog](https://rasa.com/blog/rasa-nlu-in-depth-part-1-intent-classification/)
8. [LUIS Patterns add accuracy - Microsoft Learn](https://learn.microsoft.com/en-us/azure/ai-services/LUIS/luis-how-to-model-intent-pattern)
9. [Dialogflow Intents Overview - Google Cloud](https://cloud.google.com/dialogflow/es/docs/intents-overview)
10. [Req2LTL: Bridging NL and Formal Spec via Hierarchical Semantics (arXiv 2512.17334)](https://arxiv.org/html/2512.17334v1)
11. [NLP for Requirements Formalization: New Approaches (arXiv 2309.13272)](https://arxiv.org/html/2309.13272)
12. [Formal Requirements Engineering and LLMs - ScienceDirect 2025](https://www.sciencedirect.com/science/article/pii/S0950584925000369)
13. [Transforming NL into Formal Specifications - AgenticSE 2025](https://conf.researchr.org/details/ase-2025/agenticse-2025-papers/6/Transforming-Natural-Language-into-Formal-Specifications)
14. [Bridging NL and Formal Spec - CEUR Workshop](https://ceur-ws.org/Vol-1564/paper20.pdf)
15. [Caruca: Effective Specification Mining (arXiv 2510.14279)](https://arxiv.org/abs/2510.14279)
16. [Research Directions for LLM in Requirements Engineering - Frontiers 2025](https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2025.1519437/full)
17. [Safety and Liveness Properties - Hillel Wayne](https://www.hillelwayne.com/post/safety-and-liveness/)
18. [Named Groups in Python Regex - Timothy Gebhard](https://timothygebhard.de/posts/named-groups-in-regex-in-python/)
19. [Inferring State Machine from Protocol via LLM (arXiv 2405.00393)](https://arxiv.org/html/2405.00393v3)
20. [Formal Specification Languages - Hillel Wayne / Buttondown](https://buttondown.com/hillelwayne/archive/formal-specification-languages/)
21. [Parsing in Python: All Tools and Libraries - Tomassetti](https://tomassetti.me/parsing-in-python/)
22. [Named Capture Groups Python - pyATL](https://pyatl.dev/2024/03/05/named-capture-groups-in-python/)
23. [NLP-Based Requirements Formalization - CEUR 2951](https://ceur-ws.org/Vol-2951/paper15.pdf)
24. [DSL-Xpert 2.0: LLM-driven code generation for DSLs - ScienceDirect 2025](https://www.sciencedirect.com/science/article/pii/S0950584925002939)

### Fonti Interne CervellaSwarm

25. `packages/lingua-universale/src/.../protocols.py` - struttura Protocol/ProtocolStep/ProtocolChoice
26. `packages/lingua-universale/src/.../types.py` - MessageKind (14 valori), AgentRole (17 ruoli)
27. `packages/lingua-universale/src/.../dsl.py` - pattern DSL Scribble-inspired, tokenizer regex
28. `RESEARCH_20260224_come_si_crea_un_linguaggio.md` - contesto linguaggi, ABC/Python lezioni

---

## SINTESI E RACCOMANDAZIONE

### Approccio Raccomandato: "Adapt Pattern, Stdlib-Only"

**Implementazione in 5 step:**

1. **Constants layer**: ROLE_ALIASES bilingue (IT+EN), ACTION_PATTERNS regex compilati,
   STEP_SEPARATOR_PATTERN, PROPERTY_PATTERNS (safety + liveness keywords)

2. **IR layer**: IntentStep/IntentBranch/IntentParseResult come frozen dataclasses
   (stesso pattern di GeneratedCode in codegen.py)

3. **Parser layer**: 3 funzioni private (_split_steps, _extract_step, _detect_branches)
   usando solo `re` module. Named groups per slot extraction.

4. **Assembler layer**: intent_to_protocol() converte IR -> Protocol con validazione
   Protocol.__post_init__ automatica. Warnings espliciti per ruoli non risolti.

5. **Public API**: parse_to_protocol(text, name) come convenience shortcut.
   parse_intent(text) per accesso all'IR intermedio.

### Metriche Attese

- LOC: ~500-600 (coerente con gli altri moduli B)
- ZERO deps (stessa regola di tutto il package)
- Test: stimati 80-120 (simile a confidence.py e trust.py)
- Copertura attesa: 95%+ (come da standard del package)
- Tempo parsing: < 1ms per input tipico (regex compilati)

### Limitazioni Esplicite (da documentare nel modulo)

- Copertura: ~70-80% dei casi tipici (role + action ben definiti)
- Casi ambigui: restituisce IntentParseResult con confidence < 0.5 e warnings
- Non gestisce: pronomi (it, they), ellissi ("then does the same"), impliciti
- Per copertura 95%+: serve optional LLM layer (Fase C, non ora)

---

## CONCLUSIONE

La Lingua Universale puo avere un Intent Parser ZERO deps che copre il
70-80% dei casi pratici con approccio deterministico e testabile.

Il pattern e consolidato in letteratura (Adapt, Req2LTL, dep-parsing pipelines).
La nostra implementazione sara piu semplice dei sistemi accademici perche:
- Il dominio e ristretto (protocolli multi-agent, non requirements generali)
- I ruoli sono enumerati (17 AgentRole + nomi custom)
- I MessageKind sono enumerati (14 valori)
- L'output e gia strutturato (Protocol frozen dataclass)

Questa ristrettezza del dominio e il nostro vantaggio competitivo.
**Fa bene UNA cosa sola: testo -> Protocol. E la fa deterministically.**

---

*Cervella Researcher - CervellaSwarm*
*"Ricerca PRIMA di implementare."*
*2026-02-25*
