# Task Orchestration Frameworks - Research
> **Data:** 2026-02-18 - Sessione 372
> **Scopo:** F2.3 - Package `cervellaswarm-task-orchestration`
> **Fonti:** 18 consultate (docs ufficiali, arxiv, blog tecnici, GitHub)
> **Status:** COMPLETA

---

## EXECUTIVE SUMMARY

Nessun framework ha un sistema di task classification deterministico (rule-based, zero LLM calls).
Tutti i competitor usano LLM o euristiche embedded nel LLM stesso per decidere routing.
Il nostro approccio (keyword scoring + file markers) e **unico nel panorama 2025-2026**.

---

## 1. CREWAI (44k stars)

### Task Classification
- **Meccanismo:** NON esiste classificazione automatica di complessita
- Tasks hanno due execution modes: sequential (ordine fisso) o hierarchical (manager agent decide)
- Il manager e un LLM che legge `role` + `goal` degli agenti e assegna basandosi su "capabilities"
- Zero complexity scoring, zero keyword detection

### Routing Logic
- **Hierarchical process:** Manager LLM decide chi lavora su cosa
- **Sequential process:** Ordine hardcoded nella definizione crew
- `context` attribute: task può dichiarare dipendenze da output di altri task
- `agent` parameter: assegnazione diretta (bypassa il routing)

### Output Validation
- **Function guardrails:** Python function `(task_output) -> (bool, Any)` - deterministico
- **LLM guardrails:** String description - LLM valuta in modo soggettivo
- Mix dei due tipi supportato nella stessa task
- `guardrail_max_retries` (default: 3) - retry automatico su failure

### Fallback/Retry
- Retry configurabile: `guardrail_max_retries=3`
- Su failure: feedback all'agente che riprova (stesso agente, non escalation)
- Nessun fallback a tier inferiore (no "se fallisce 3 volte, procedi minimal")

### State Management
- **In-memory:** TaskOutput class (raw, JSON, Pydantic formats)
- **Memoria persistente:** ChromaDB (short-term), SQLite (task results), entity memory via embeddings
- **NO file markers** - nessuna sincronizzazione cross-process nativa

### Gap vs Noi
- No complexity classification pre-routing
- Manager LLM = non deterministico, costoso
- No file-based state (no git audit trail nativo)
- Retry stesso agente (no escalation logic)

---

## 2. AUTOGEN / AG2 (51k stars)

### Task Classification
- **Meccanismo:** NESSUNO nativo per complexity
- `GroupChatManager` sceglie il prossimo speaker via LLM (analisi del conversation history)
- Hybrid routing pattern in produzione: FAISS embedding -> keyword rules -> LLM fallback
- Nessun classifier deterministico: tutto emergente dalla conversazione

### Routing Logic
- **GroupChat:** Manager LLM seleziona prossimo agente basandosi su chat context
- **Swarm:** pattern strutturato per handoff coordinati
- **Nested chats:** workflow gerarchici via sub-conversation
- Pattern produzione (community): fast similarity (FAISS) -> intent rules (regex) -> LLM arbitration

### Output Validation
- **Structured outputs:** schema enforcement sulle risposte
- `max_turns` come proxy di retry (non vera validazione)
- Human-in-the-loop: `ALWAYS`, `NEVER`, `TERMINATE` modes
- Nessuna validazione automatica content quality

### Fallback/Retry
- `max_turns` limita iterazioni ma non e retry logic vera
- Rischio noto: `UserProxyAgent` puo essere ri-selezionato ripetutamente (loop antipattern)
- v0.4 (2025): distributed runtime, architettura completamente rifattorizzata

### State Management
- **In-memory:** conversation history (context window)
- **Cross-session:** NO nativo (perdita contesto tra sessioni)
- Rischio documentato: "long chats risk context loss without buffering"
- v0.4 aggiunge pluggable memory, ma ancora non standard

### Gap vs Noi
- No complexity scoring pre-routing
- Loop instability (UserProxyAgent re-selection)
- Context loss across sessions
- No audit trail naturale

---

## 3. LANGGRAPH (24k stars)

### Task Classification
- **Meccanismo:** NON esiste - sviluppatore deve implementarlo come nodo
- Il framework organizza in nodes (LLM, tool, function) e conditional edges
- Edges valutano runtime state per decidere il prossimo nodo
- "Conditions can range from simple checks to complex evaluations" - ma devi scriverle tu

### Routing Logic
- **Conditional edges:** predicati sullo stato globale -> routing basato su output
- **Fan-out/fan-in:** parallelismo nativo via edge multiple
- **State machine esplicita:** massima flessibilita, massima complessita setup
- DAG-based: debug difficile ("pinpointing root cause...far more challenging")

### Output Validation
- **NO built-in validation mechanism** - completamente delegato al developer
- I custom function nodes possono validare, ma zero standard
- Node-level retries: configurabili per singolo nodo
- Checkpoint-based recovery: riprendi da stato precedente su failure

### Fallback/Retry
- Node-level retry: configurabile
- Checkpoint recovery: "time travel" a stati precedenti
- Selective resume: riparti dal nodo fallito
- **Piu sofisticato dei competitor** per recovery, ma serve molto setup

### State Management
- **Centralizzato:** shared state object accessibile da tutti i nodi
- **In-memory + external:** MemorySaver (in-thread), InMemoryStore (cross-thread)
- External persistence: supportato ma da configurare
- "Pause and resume later, even in different computing environments"
- **LangSmith monitoring** quasi obbligatorio per produzione

### Gap vs Noi
- No built-in complexity classification
- "Developers must explicitly define reducers and termination rules" - overhead alto
- No standard output validation
- LangSmith dependency per debugging production

---

## 4. OPENAI AGENTS SDK (rilascio Marzo 2025)

### Task Classification
- **Meccanismo:** Triage Agent pattern (LLM-based)
- Il triage agent riceve task e invoca handoff verso specialista appropriato
- L'LLM decide quale handoff invocare basandosi sul contesto conversazionale
- Nessun complexity scoring deterministico

### Routing Logic
- **Handoff:** tool call specializzato che trasferisce controllo ad altro agente
- Tool name override, description override, callback `on_handoff`
- `input_filter`: funzione che trasforma dati prima di passarli al nuovo agente
- Transcript collapse (beta): collassa history in singolo messaggio prima di handoff
- Dichiarativo ed elegante, ma LLM-dipendente

### Output Validation
- **Input guardrails:** pre-agent (check user input)
- **Output guardrails:** post-agent (check final response)
- Eseguiti in **parallelo** con agent execution (non sequenziali)
- Fail fast: `OutputGuardrailTripwireTriggered` exception su failure
- Nessun retry automatico nativo nel guardrail (exception solo)

### Fallback/Retry
- NO retry automatico nativo su guardrail failure
- Eccezione -> sviluppatore gestisce retry loop esternamente
- `on_handoff` callback per side effects (logging, data fetching)

### State Management
- **Conversational history in-memory** - NON persistente tra sessioni
- NO file-based state
- NO git audit trail

### Gap vs Noi
- Triage LLM-based = non deterministico
- No complexity scoring
- Guardrails in parallelo (fail fast) vs il nostro scoring accumulativo
- No session continuity nativa
- No file-based audit trail

---

## 5. CLAUDE CODE NATIVO (Task Tool)

### Task Classification
- **Meccanismo:** Basato su agent description field
- L'agente orchestratore decide quale subagent delegare guardando la description
- "Clear descriptions explaining when the subagent should be used"
- "MUST BE USED" / "ONLY FOR" patterns aumentano affidabilita routing
- NO complexity scoring automatico - dipende da come scrivi le istruzioni

### Routing Logic
- Subagent description field controlla quando viene invocato
- Routing decision: LLM (orchestratore) interpreta description vs task
- Parallel vs sequential: non nativo, richiede istruzioni esplicite in CLAUDE.md
- Contesti isolati: ogni subagent ha proprio context window

### Output Validation
- **NO framework di validazione nativo**
- Dipende da istruzioni nel system prompt dell'agente
- Nessun guardrail built-in
- Output validation completamente manuale (o via hook)

### Fallback/Retry
- NO retry automatico
- Fallback: istruzioni esplicite nel prompt dell'agente o dell'orchestratore
- `maxTurns` come safety net (hard stop, non retry logic)

### State Management
- **In-memory:** context window del subagent (isolato)
- **NO cross-session memory nativa** (autocompact perde stato)
- File system: accesso diretto tramite tools (Read/Write)
- NO standard per file markers o state tracking

### Gap vs Noi
- Routing 100% LLM-based (no determinism)
- No complexity classification
- No output validation framework
- No file-based task state (no race condition protection)

---

## COMPARISON TABLE

| Meccanismo | CervellaSwarm | CrewAI | AutoGen | LangGraph | OpenAI SDK | Claude Code |
|------------|:---:|:---:|:---:|:---:|:---:|:---:|
| **Task Classification** | Rule-based (zero LLM) | LLM (manager) | LLM (GroupChat) | Manual nodes | LLM (triage) | LLM (desc.) |
| **Complexity Scoring** | Yes (keyword+file count) | No | No | No | No | No |
| **Deterministic Routing** | Yes | No | No | Partial | No | No |
| **Output Validation** | Score 0-100 + retry_needed | LLM/Function guardrail | Manual/Structured | Manual nodes | Guardrail tripwire | None |
| **Retry Logic** | score < 50 -> retry_needed | max_retries=3 (same agent) | max_turns | Node retry + checkpoint | Exception only | None |
| **Fallback Escalation** | Yes (FALLBACK_TO_WORKER) | No | No | Checkpoint resume | No | No |
| **File-based State** | Yes (.ready/.working/.done) | No | No | No | No | No |
| **Atomic Race Protection** | Yes (exclusive create 'x') | No | No | No | No | No |
| **Git-friendly Audit** | Yes (markers in git) | No | No | No | No | No |
| **Cross-session State** | Yes (via SNCP) | Partial (ChromaDB) | No | Partial (external) | No | No |
| **Zero LLM Calls** | Yes (classifier) | No | No | No | No | No |

---

## DIFFERENZIALI UNICI - ANALISI DETTAGLIATA

### 1. Rule-Based Classifier (UNICO)
**Nessun framework ha un complexity classifier deterministico.**

Il nostro `task_classifier.py`:
- Keyword scoring con pesi (refactor=0.8, architecture=0.9, migrate=0.7...)
- File count estimation (regex patterns)
- Simple keyword fast-path (fix typo, rename -> immediate SIMPLE)
- Confidence score 0.0-1.0
- Zero LLM calls = zero costo, zero latenza, risultato deterministico

Vantaggio: prevedibile, testabile (95% coverage), nessun costo API per il routing.
Ricerca DAAO (arxiv 2025): sistemi ibridi (rule-based + learned) outperformano sistemi puramente LLM-based in costo/performance.

### 2. File-Based State Machine (UNICO)
**Nessun framework usa file markers per state management.**

Il nostro `task_manager.py`:
- `.ready`, `.working`, `.done`, `.ack_received`, `.ack_understood`
- Atomic exclusive create (`open(f, 'x')`) - race condition protection
- Git-native: ogni stato e tracciabile con `git log`
- Cross-process: piu worker vedono lo stesso stato senza DB
- Path traversal protection: `validate_task_id()` con regex strict

LangGraph usa checkpointing in-memory/external ma richiede configurazione esplicita e non e git-native.
CrewAI usa SQLite per task results ma non ha state machine esplicita con markers.

### 3. Plan Validation Strutturata (UNICO)
**Nessun framework valida struttura plan in modo deterministico.**

Il nostro `architect_flow.py`:
- 4 fasi obbligatorie (Understanding, Design, Review, Final Plan)
- Metadata fields check (Task ID, Complexity, Files Affected)
- Success Criteria pattern check (regex)
- Length bounds (500 < x < 10000)
- Score 0-10 con deductions precise

CrewAI ha guardrails per task output, non per plan di lavoro.
LangGraph non ha nulla di simile.

### 4. Fallback Escalation a 3 Livelli (UNICO)
**Nessun framework ha fallback escalation strutturata.**

Il nostro `architect_flow.py`:
- Revision 1: REQUEST_REVISION (prima chance)
- Revision 2: REQUEST_REVISION (ultima chance con avviso)
- Revision 3+: FALLBACK_TO_WORKER (procedi senza plan)
- Fallback instruction generation: guida specifica per worker in fallback mode

CrewAI: retry stesso agente N volte, poi errore. Nessuna escalation.
OpenAI: eccezione, developer gestisce retry esternamente.

### 5. Output Validator con Reflection Pattern (UNICO)
**Nessun framework ha output validator con log correlation.**

Il nostro `output_validator.py`:
- Error markers check (Traceback, ERROR, RuntimeError...)
- Incompleteness markers (TODO, FIXME, XXX...)
- Code block awareness (ignora markers nei block)
- Log correlation (cerca log worker con task_id)
- Score 0-100 accumulativo + retry_needed boolean
- Exit codes: 0=VALID, 1=INVALID, 2=ERROR

OpenAI guardrails: tripwire (bool), no scoring.
CrewAI guardrails: function (bool, Any) o LLM string, no scoring accumulativo.

---

## WHAT TO BORROW FROM COMPETITORS

### Da CrewAI
- **Guardrail type mixing:** function + LLM nella stessa validazione
  - Applicazione: `output_validator.py` potrebbe accettare custom validator functions oltre ai pattern fissi
- **guardrail_max_retries come parametro:** configurabile (ora e hardcoded a 3)
  - Applicazione: `MAX_RETISIONS = 2` in `architect_flow.py` -> rendere configurabile

### Da LangGraph
- **Node-level retry con exponential backoff**
  - Applicazione: `output_validator` potrebbe suggerire delay prima del retry
- **Selective resume:** riparti dal nodo fallito (non dall'inizio)
  - Applicazione: task_manager potrebbe tracciare quale fase e fallita

### Da OpenAI SDK
- **Input filter pattern** prima di passare task ad agente
  - Applicazione: `route_task()` potrebbe filtrare/trasformare description prima del routing
- **on_handoff callback** per side effects
  - Applicazione: hook in `create_session()` per logging/telemetry

### Da DAAO (arxiv research)
- **Difficulty continua (0-1) vs discreta (4 livelli)**
  - Il nostro `confidence` float e gia in questo spirito
  - Applicazione: workflow depth `L = ceil(d * max_phases)` per scaling dinamico

---

## RACCOMANDAZIONI PER IL PACKAGE F2.3

### Architettura Raccomandata

```
cervellaswarm-task-orchestration/
├── src/cervellaswarm_task_orchestration/
│   ├── __init__.py              # exports: classify_task, route_task, TaskManager, validate_output
│   ├── task_classifier.py       # PURO: zero deps, zero LLM - MANTIENI COSI
│   ├── architect_flow.py        # ROUTING: aggiungi configurable MAX_REVISIONS
│   ├── task_manager.py          # STATE: mantieni atomic, aggiungi configurable SWARM_DIR
│   └── output_validator.py      # VALIDATION: aggiungi custom_validators parameter
├── tests/
└── pyproject.toml
```

### Miglioramenti Prioritari (P1)

1. **Configurable SWARM_DIR** in `task_manager.py`
   - Ora hardcoded `.swarm/tasks`
   - Serve `TaskManager(base_dir=Path("my_project/.swarm"))` per uso standalone
   - Impatto: rende il package usabile su qualsiasi progetto

2. **Configurable MAX_REVISIONS** in `architect_flow.py`
   - Ora hardcoded `MAX_REVISIONS = 2`
   - Serve `handle_plan_rejection(session, reason, max_revisions=3)`

3. **Custom validators in `output_validator.py`**
   - Aggiungere `validate_output(file, custom_validators=[fn1, fn2])`
   - Ispirato al pattern CrewAI function guardrails

4. **Remove hardcoded sys.path** in `architect_flow.py`
   - `sys.path.insert(0, str(_root))` non funziona in package standalone
   - Sostituire con relative imports

### Miglioramenti P2 (Nice to Have)

5. **Retry delay suggestion** in `output_validator.py`
   - Ispirato da LangGraph exponential backoff
   - `retry_delay_seconds: int` nel risultato

6. **Phase-level failure tracking** in `task_manager.py`
   - Aggiungere `.failed_phase` marker per selective resume

### NON FARE (Evitare)

- NON aggiungere LLM calls al classifier - romperebbe il differenziale principale
- NON aggiungere dipendenze pesanti (ChromaDB, SQLite per state) - rimani file-based
- NON replicare LangGraph state machine - troppo complessa per il nostro caso d'uso
- NON togliere il design deterministico per inseguire "AI-powered" routing

---

## FONTI CONSULTATE

1. [CrewAI Tasks - Documentazione ufficiale](https://docs.crewai.com/en/concepts/tasks)
2. [AG2 Quickstart](https://docs.ag2.ai/latest/docs/home/quickstart/)
3. [LangGraph AI Framework 2025 Guide](https://latenode.com/blog/langgraph-ai-framework-2025-complete-architecture-guide-multi-agent-orchestration-analysis)
4. [OpenAI Agents SDK - Guardrails](https://openai.github.io/openai-agents-python/guardrails/)
5. [OpenAI Agents SDK - Handoffs](https://openai.github.io/openai-agents-python/handoffs/)
6. [Orchestrator-Worker Comparison - Arize AI](https://arize.com/blog/orchestrator-worker-agents-a-practical-comparison-of-common-agent-frameworks/)
7. [Claude Code Sub-Agents](https://code.claude.com/docs/en/sub-agents)
8. [DAAO: Difficulty-Aware Agent Orchestration (arxiv)](https://arxiv.org/html/2509.11079v1)
9. [CrewAI Guardrails Analysis](https://towardsdatascience.com/how-to-implement-guardrails-for-your-ai-agents-with-crewai-80b8cb55fa43/)
10. [AutoGen Multi-Agent Framework](https://microsoft.github.io/autogen/0.2/docs/Use-Cases/agent_chat/)
11. [LangGraph Multi-Agent Orchestration](https://latenode.com/blog/ai-frameworks-technical-infrastructure/langgraph-multi-agent-orchestration/)
12. [OpenAI New Tools for Building Agents](https://openai.com/index/new-tools-for-building-agents/)
13. [AI Agent Orchestration Frameworks Comparison](https://blog.n8n.io/ai-agent-orchestration-frameworks/)
14. [LangGraph vs CrewAI performance](https://www.getmaxim.ai/articles/top-5-ai-agent-frameworks-in-2025-a-practical-guide-for-ai-builders/)
15. [AG2 Hybrid Routing Pattern](https://medium.com/the-constellar-digital-technology-blog/geek-out-time-supercharging-multi-agent-ai-hybrid-routing-with-ag2-formerly-autogen-4ad68946b855)
16. [AutoGen v0.4 Architecture](https://github.com/ag2ai/ag2)
17. [OpenAI Agents SDK Practical Guide](https://datasciencedojo.com/blog/openai-agents-sdk/)
18. [AI Agent Orchestration Patterns - Azure](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)

---

*Ricerca completata da Cervella Researcher - Sessione 372 - 2026-02-18*
