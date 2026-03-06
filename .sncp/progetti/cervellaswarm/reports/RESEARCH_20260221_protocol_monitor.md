# Protocol Monitor - Ricerca Approfondita
> **Data:** 2026-02-21
> **Ricercatrice:** Cervella Researcher
> **Status:** COMPLETA
> **Fonti:** 32 consultate (web search + fetch diretti)
> **Progetto:** CervellaSwarm - Lingua Universale Fase A Step 6+

---

## 1. Panoramica Fonti Consultate

### Fonti Web (fetch diretti)

| # | Fonte | URL | Rilevanza |
|---|-------|-----|-----------|
| 1 | OpenTelemetry AI Agent Observability | https://opentelemetry.io/blog/2025/ai-agent-observability/ | ALTA |
| 2 | OpenTelemetry GenAI Agent Spans | https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/ | ALTA |
| 3 | PyMOP Runtime Verification System | https://arxiv.org/html/2509.06324 | ALTA |
| 4 | OpenAI Agents SDK Tracing | https://openai.github.io/openai-agents-python/tracing/ | ALTA |
| 5 | AgentOps Session Concepts | https://github.com/AgentOps-AI/agentops/blob/main/docs/v1/concepts/sessions.mdx | ALTA |
| 6 | Strands SDK Hook Events | https://strandsagents.com/latest/documentation/docs/api-reference/python/experimental/hooks/events/ | ALTA |

### Fonti Web (ricerche)

| # | Area | Query | Risultati chiave |
|---|------|-------|------------------|
| 7 | Distributed tracing | OpenTelemetry patterns 2025 | LGTM Stack, span/trace model |
| 8 | Session types observability | Python runtime monitoring | Three pillars (logs/metrics/traces) |
| 9 | Multi-agent observability | LangSmith/AgentOps/CrewAI | Top 5 tools, metrics standard |
| 10 | Event emitter Python | stdlib threading weakref | threading.RLock + weakref.WeakSet |
| 11 | Runtime verification | temporal logic Python | PyMOP, LogScope/RULER, LTL/FSM |
| 12 | OTel GenAI conventions | semantic conventions 2025 | gen_ai.* attributes emerging |
| 13 | Python callbacks stdlib | monitoring design | logging.Filter, callback hooks |
| 14 | Jaeger/Zipkin internals | span trace protocol | Span data model |
| 15 | LangGraph LangSmith | inter-agent tracing | Run model, nested spans |
| 16 | Python event bus | deque + Lock stdlib | thread-safe patterns |
| 17 | Protocol conformance | safety/liveness monitoring | state machine replication |
| 18 | Google SRE golden signals | latency/traffic/errors/saturation | Canonical metrics framework |
| 19 | Python contextvars | tracing context propagation | ContextVar thread-safe |
| 20 | OpenAI agents SDK | tracing hooks 2025 | AgentHooks, TraceProcessor |

---

## 2. Pattern di Monitoring Trovati

### Pattern 1: Span/Trace Model (OpenTelemetry Standard)

**Origine:** OpenTelemetry, Jaeger, Zipkin, OpenAI Agents SDK

**Come funziona:**
- Una **Trace** e l'esecuzione end-to-end completa (= una sessione di protocollo)
- Ogni **Span** e un'unita di lavoro atomica (= un message exchange)
- Gli span hanno `trace_id`, `parent_id`, `start_time`, `end_time`, `attributes`
- Gli span sono annidati: un'esecuzione produce un albero di span

**Adattamento al nostro caso:**
```
Trace = SessionChecker (una sessione di protocollo)
Span  = ogni chiamata checker.send()
       |- span_id = step_index
       |- parent = session trace
       |- duration = end_time - start_time per step
       |- attributes: sender, receiver, kind, branch
```

**Dati catturati per span (da OTel GenAI):**
- `gen_ai.agent.id`, `gen_ai.agent.name` -> nostro: `sender`, `receiver`
- `gen_ai.operation.name` -> nostro: `message_kind`
- `gen_ai.conversation.id` -> nostro: `session_id`
- `error.type` se violazione
- Start/end timestamp, durata

**Pro:** Standard industriale, strumenti esistenti, well-understood
**Contro:** Overhead serializzazione, non nasce per session types

---

### Pattern 2: Event-Driven Hook System (Strands SDK / OpenAI Agents SDK)

**Origine:** Amazon Strands Agents SDK, OpenAI Agents SDK, AgentOps

**Come funziona:**
Il monitor espone un sistema di hook dove i subscriber registrano callback per eventi specifici. Gli eventi sono immutabili (frozen dataclasses) con campi controllati.

**Architettura Strands SDK:**
```python
class BaseHookEvent:
    # immutable, should_reverse_callbacks
    invocation_state: dict  # stato condiviso multi-agente

# Tipi: BeforeModelCall, AfterModelCall,
#        BeforeToolCall, AfterToolCall,
#        BidiMessageAdded, BidiInterruption
```

**Architettura OpenAI Agents SDK:**
```python
class AgentHooks:
    def on_start(self, context, agent): ...
    def on_end(self, context, agent, output): ...
    def on_tool_start(self, context, agent, tool): ...
    def on_tool_end(self, context, agent, tool, result): ...

# TraceProcessor pattern:
class TraceProcessor:
    def on_trace_start(self, trace): ...
    def on_trace_end(self, trace): ...
    def on_span_start(self, span): ...
    def on_span_end(self, span): ...
```

**Adattamento al nostro caso:**
```
Hook events:
  - on_session_start(session_id, protocol_name)
  - on_message_sent(session_id, step, sender, receiver, kind, duration_ms)
  - on_branch_chosen(session_id, step, branch_name)
  - on_protocol_violation(session_id, step, violation)
  - on_session_complete(session_id, stats)
  - on_repetition(session_id, repetition_count)
```

**Pro:** Disaccoppiamento totale, multiple subscriber, zero impatto sul core
**Contro:** Callback hell se male strutturato, require disciplina

---

### Pattern 3: Parametric Monitoring con FSM (PyMOP / Runtime Verification)

**Origine:** PyMOP (accademico 2025), LogScope/RULER (NASA), RV-Monitor

**Come funziona:**
Ogni istanza di sessione crea un monitor separato (FSM), parametrizzato sull'ID di sessione. Il "trace slicing" separa le tracce di sessioni diverse per evitare falsi positivi.

**Algoritmi chiave (da PyMOP):**
- Algorithm A: offline (raccoglie tutto, verifica dopo)
- Algorithm B: online event-by-event, nessun storage
- Algorithm C: strutture ausiliarie per parametric matching veloce
- Algorithm D: "enable sets" statici per evitare monitor inutili

**Proprieta temporali monitorabili:**
- **Safety**: "il sender non invia mai due volte di fila senza risposta"
- **Liveness**: "ogni TaskRequest ottiene una TaskResult entro N passi"
- **Sequence**: "AuditRequest precede sempre AuditVerdict"
- **Completeness**: "ogni sessione raggiunge lo stato complete"

**Proprieta matematiche (da letteratura):**
```
Safety:  bad thing NEVER happens = invariante
Liveness: good thing EVENTUALLY happens = fairness
```

**Adattamento al nostro caso:**
Il nostro `SessionChecker` e gia un FSM! Il monitor si aggiunge sopra come layer di osservazione non-intrusivo. Non sostituisce il checker - lo osserva.

**Pro:** Fondamenta teoriche solide, verificabile formalmente
**Contro:** Complessita accademica, overkill per Fase A

---

### Pattern 4: Four Golden Signals Adattati (Google SRE)

**Origine:** Google SRE Book (capitolo "Monitoring Distributed Systems")

**I 4 golden signals originali:**
1. **Latency** - tempo per servire una request
2. **Traffic** - quanto demand sul sistema
3. **Errors** - rate di request fallite
4. **Saturation** - quanto "pieno" e il servizio

**Adattamento per session type monitoring:**

| Golden Signal | Adattamento nostro |
|---------------|-------------------|
| Latency | `step_duration_ms` - quanto tempo impiega ogni message exchange |
| Traffic | `messages_per_second` - throughput del protocollo |
| Errors | `violation_rate` - % di send() che sollevano ProtocolViolation |
| Saturation | `concurrent_sessions` - quante sessioni attive simultaneamente |

**Metriche derivate:**
- `session_duration_ms` = completamento totale protocollo
- `completion_rate` = % sessioni che arrivano a is_complete=True
- `branch_distribution` = quante volte ogni branch viene scelto
- `p50/p95/p99_step_latency` = percentili per ogni tipo di step

**Pro:** Framework collaudato, comprensibile da tutti i team
**Contro:** Originale per sistemi web, adattamento richiede creativita

---

### Pattern 5: Session-Level Analytics (AgentOps Model)

**Origine:** AgentOps, LangSmith

**Come funziona:**
Ogni sessione ha un "waterfall" temporale di eventi. Alla fine della sessione si calcolano aggregate statistics. La sessione ha un `end_state` (Success/Failure/Indeterminate).

**Dati AgentOps per sessione:**
- LLM calls count, Tool calls count, Actions count, Errors count
- Duration totale
- Cost in USD (per noi: N/A, sostituiamo con "messages count")
- Token usage (per noi: N/A, sostituiamo con "step count")
- `session.get_analytics()` ritorna dict strutturato

**Pattern end_state nostro:**
```python
class SessionEndState(Enum):
    COMPLETE = "complete"       # is_complete = True
    VIOLATED = "violated"       # ProtocolViolation sollevata
    ABANDONED = "abandoned"     # sessione non completata
    INDETERMINATE = "unknown"   # stato non determinabile
```

**Pro:** Pragmatico, metriche utili per debugging
**Contro:** Post-hoc (non real-time), richiede storage

---

### Pattern 6: Contextual Propagation (Python contextvars)

**Origine:** Python 3.7+ stdlib, OpenTelemetry, OpenAI Agents SDK

**Come funziona:**
`contextvars.ContextVar` propaga contesto attraverso thread e coroutine. OpenAI Agents SDK lo usa per tracciare la trace corrente: `"Spans are automatically part of the current trace, tracked via a Python contextvar"`.

**Esempio OpenAI SDK:**
```python
# Ogni span sa automaticamente in quale trace si trova
_current_trace: ContextVar[Optional[Trace]] = ContextVar('current_trace', default=None)
_current_span: ContextVar[Optional[Span]] = ContextVar('current_span', default=None)
```

**Adattamento nostro:**
```python
# Permette multi-sessioni in thread separati
_current_session: ContextVar[Optional[str]] = ContextVar('current_session', default=None)
```

**Pro:** Thread-safe by design, async-safe, zero overhead se non usato
**Contro:** Richiede Python 3.7+, contesto non si propaga BACK dai thread

---

### Pattern 7: Publish-Subscribe Event Bus (stdlib puro)

**Origine:** Combinazione patterns: Python threading + collections, ActiveState recipe

**Come funziona stdlib:**
```
threading.RLock() -> protegge lista listener
collections.deque -> event queue thread-safe (append/popleft atomici)
weakref.WeakSet   -> listener senza memory leak
```

**Thread safety note:** `deque.append()` e `deque.popleft()` sono ATOMICI in CPython (GIL garantisce). Per handler registration/deregistration serve Lock esplicito.

**Due modalita:**
- **Synchronous**: handler chiamato nel thread di chi emette (semplice, default)
- **Asynchronous**: eventi in queue, thread separato consuma (per non bloccare)

**Pro:** ZERO dipendenze, controllabile al 100%, testabile facilmente
**Contro:** No persistence, no replay, no network distribution

---

## 3. Metriche Raccomandate per il Nostro Caso

### Metriche di Sessione (per SessionChecker)

```
# Contatori base
total_sessions_started: int
total_sessions_completed: int
total_sessions_violated: int
total_sessions_abandoned: int

# Metriche temporali
session_duration_ms: float          # dalla creazione a is_complete
session_duration_p50/p95/p99: float # percentili su N sessioni

# Metriche protocollo
total_messages_sent: int
total_violations: int
total_branch_choices: int

# Per sessione
messages_per_session: float (avg)
completion_rate: float (completed / started)
violation_rate: float (violated / started)
```

### Metriche di Step (per singolo message exchange)

```
step_duration_ms: float             # tempo per singolo send()
step_duration_by_kind: dict[MessageKind, float]  # avg per tipo
step_duration_by_sender: dict[str, float]        # avg per sender

# Distribuzione branch
branch_frequency: dict[str, int]    # quante volte ogni branch
branch_selection_time_ms: float     # tempo per choose_branch()
```

### Metriche di Violazione (per ProtocolViolation)

```
violation_by_step: dict[int, int]           # violazioni per step index
violation_by_expected: dict[str, int]       # "expected X" -> count
violation_by_sender: dict[str, int]         # chi viola di piu
violation_by_protocol: dict[str, int]       # quale protocollo e piu violato

# Detection latency (quanto tardi si trova il bug)
avg_step_at_violation: float                # step medio quando esplode
```

### Metriche di Sistema (per ProtocolMonitor globale)

```
concurrent_sessions: int            # sessioni attive ora
sessions_per_protocol: dict[str, int]  # distribuzione per protocollo
peak_concurrent_sessions: int       # massimo storico
event_queue_depth: int              # backpressure indicator
listener_count: int                 # quanti handler registrati
```

---

## 4. Architettura Proposta

### Diagramma Componenti

```
 +================================================================+
 |              cervellaswarm_lingua_universale                   |
 +================================================================+
 |                                                                |
 |  [types.py]      [protocols.py]      [dsl.py]                 |
 |      |                |                  |                    |
 |      +----------------+------------------+                    |
 |                       |                                       |
 |               [checker.py]                                    |
 |            SessionChecker                                     |
 |            SessionState                                       |
 |                 |                                             |
 |                 | emits events                                |
 |                 v                                             |
 |         [monitor.py]  <-- NEW MODULE                         |
 |      +----------------+                                       |
 |      |  ProtocolMonitor  (event emitter, global registry)    |
 |      |  MonitorEvent     (base frozen dataclass)              |
 |      |  SessionStarted   (event: session begin)               |
 |      |  MessageSent      (event: successful send)             |
 |      |  BranchChosen     (event: choice made)                 |
 |      |  ViolationOccurred (event: ProtocolViolation)          |
 |      |  SessionEnded     (event: complete/violated/abandoned) |
 |      |  RepetitionStarted (event: protocol loop restart)      |
 |      +----------------+                                       |
 |                 |                                             |
 |                 | notifies (sync, in-order)                   |
 |                 v                                             |
 |      +------------------+    +------------------+            |
 |      |  MonitorListener |    | MetricsCollector |            |
 |      |  (ABC protocol)  |    | (built-in impl)  |            |
 |      +------------------+    +------------------+            |
 |                                                               |
 +================================================================+

 EXTERNAL WORLD (not in package)
 +------------------+    +------------------+    +-------------+
 | LoggingListener  |    |  AlertListener   |    | DebugPrinter|
 | (writes to log)  |    | (sends alert)    |    | (stdout)    |
 +------------------+    +------------------+    +-------------+
```

### Diagramma Flusso Dati

```
 checker.send(sender, receiver, msg)
          |
          v
   [Validate message]
          |
       PASS      FAIL
          |         |
          v         v
   [Update state]  [Raise ProtocolViolation]
          |              |
          v              v
   [Emit: MessageSent]  [Emit: ViolationOccurred]
          |              |
          v              |
   [if complete]         |
   [Emit: SessionEnded]  |
          |              |
          v              v
   ProtocolMonitor._notify_listeners(event)
          |
    [threading.RLock - snapshot listeners]
          |
    [call each listener.on_event(event)]
          |
    [update MetricsCollector counters]
```

### Design del Modulo monitor.py

```python
# ============================================================
# Event types (frozen dataclasses)
# ============================================================

@dataclass(frozen=True)
class MonitorEvent:
    """Base class per tutti gli eventi del monitor."""
    session_id: str
    protocol_name: str
    timestamp: float           # time.time()

@dataclass(frozen=True)
class SessionStarted(MonitorEvent):
    roles: tuple[str, ...]

@dataclass(frozen=True)
class MessageSent(MonitorEvent):
    step_index: int
    sender: str
    receiver: str
    message_kind: str          # MessageKind.value
    duration_ms: float         # tempo per validazione
    branch: Optional[str]

@dataclass(frozen=True)
class BranchChosen(MonitorEvent):
    step_index: int
    branch_name: str
    auto_detected: bool        # True se _detect_branch, False se choose_branch

@dataclass(frozen=True)
class ViolationOccurred(MonitorEvent):
    step_index: int
    expected: str
    got: str
    violation_type: str        # "wrong_sender"|"wrong_receiver"|"wrong_kind"|...

@dataclass(frozen=True)
class SessionEnded(MonitorEvent):
    end_state: str             # "complete"|"violated"|"abandoned"
    total_messages: int
    duration_ms: float
    repetitions: int

@dataclass(frozen=True)
class RepetitionStarted(MonitorEvent):
    repetition_number: int     # 1-based

# ============================================================
# Listener interface
# ============================================================

class MonitorListener(Protocol):
    """Protocol (structural typing) per listener del monitor."""
    def on_event(self, event: MonitorEvent) -> None: ...

# ============================================================
# Core monitor
# ============================================================

class ProtocolMonitor:
    """Global monitor per sessioni di protocollo.

    Thread-safe. Zero dipendenze esterne.
    Singleton o istanza per contesto.
    """

    def __init__(self) -> None:
        self._listeners: list[MonitorListener] = []
        self._lock = threading.RLock()
        self._metrics = MetricsCollector()

    def add_listener(self, listener: MonitorListener) -> None:
        with self._lock:
            self._listeners.append(listener)

    def remove_listener(self, listener: MonitorListener) -> None:
        with self._lock:
            self._listeners = [l for l in self._listeners if l is not listener]

    def emit(self, event: MonitorEvent) -> None:
        # Snapshot per evitare lock durante chiamata
        with self._lock:
            listeners = list(self._listeners)
        # Aggiorna metriche (sempre)
        self._metrics.record(event)
        # Notifica listener
        for listener in listeners:
            listener.on_event(event)

    @property
    def metrics(self) -> MetricsSnapshot:
        return self._metrics.snapshot()

# ============================================================
# MetricsCollector (built-in)
# ============================================================

@dataclass
class MetricsSnapshot:
    sessions_started: int
    sessions_completed: int
    sessions_violated: int
    total_messages: int
    total_violations: int
    avg_session_duration_ms: float
    avg_step_duration_ms: float
    violation_by_step: dict[int, int]
    branch_frequency: dict[str, int]
    sessions_per_protocol: dict[str, int]

class MetricsCollector:
    """Raccoglie e aggrega metriche. Thread-safe."""
    # usa threading.Lock + dict per contatori
    # usa collections.deque per sliding windows
    # NO deps esterne
```

### Integrazione con SessionChecker

**Opzione A: Monitor passato al checker (Dependency Injection)**
```python
checker = SessionChecker(DelegateTask, session_id="S001", monitor=my_monitor)
# Il checker emette eventi automaticamente
```

**Opzione B: Monitor globale (registry pattern)**
```python
# Monitor globale opzionale
_default_monitor: Optional[ProtocolMonitor] = None

def set_default_monitor(m: ProtocolMonitor) -> None: ...
def get_default_monitor() -> Optional[ProtocolMonitor]: ...
```

**Raccomandazione:** Opzione A (DI) e piu testabile. Opzione B e piu ergonomica.
**Decisione proposta:** Supportare ENTRAMBE: DI come primario, global come fallback.

---

## 5. Rischi e Mitigazioni

### Rischio 1: Performance overhead nei listener

**Problema:** Se un listener fa I/O (log su file, network), il thread del checker si blocca.

**Mitigazione:** Documentare chiaramente che `on_event()` deve essere veloce. Per I/O heavy, usare un listener con `queue.Queue` interno + worker thread separato. La libreria fornisce `AsyncListener` come esempio.

**Pattern sicuro:**
```python
class AsyncListener:
    def __init__(self, delegate):
        self._queue = queue.Queue()
        self._delegate = delegate
        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()

    def on_event(self, event):
        self._queue.put_nowait(event)  # non blocca mai

    def _worker(self):
        while True:
            event = self._queue.get()
            self._delegate.on_event(event)
```

### Rischio 2: Exception nei listener non deve rompere il checker

**Problema:** Se `listener.on_event()` solleva eccezione, il checker potrebbe crashare.

**Mitigazione:** Il `ProtocolMonitor.emit()` wrappa ogni call con `try/except Exception` e logga via `warnings.warn()` invece di propagare. Il checker non deve mai essere affetto da un listener bacato.

```python
for listener in listeners:
    try:
        listener.on_event(event)
    except Exception as exc:
        import warnings
        warnings.warn(f"Listener {listener!r} raised {exc!r}", RuntimeWarning)
```

### Rischio 3: Memory leak con listener non deregistrati

**Problema:** Listener aggiunti ma mai rimossi -> memory leak.

**Mitigazione (opzione 1):** Context manager pattern:
```python
with monitor.listening(my_listener):
    # listener attivo solo qui
    checker.send(...)
```

**Mitigazione (opzione 2):** `weakref.ref()` per i listener. Usato da Qt signals, psygnal, etc. Complicato per metodi (bisogna usare `weakref.WeakMethod`).

**Raccomandazione:** Implementare context manager. E piu pythonic e non richiede weakref.

### Rischio 4: Thread safety del MetricsCollector

**Problema:** Contatori in dict possono avere race condition in multi-thread.

**Mitigazione:** Ogni update al MetricsCollector e protetto da `threading.Lock`. Per i counter semplici, usare `threading.Lock` granulare o `collections.Counter` protetto. Non usare `+=` su int senza lock.

**Pattern corretto:**
```python
with self._lock:
    self._counters["total_messages"] += 1
    self._step_durations.append(duration_ms)
```

### Rischio 5: Evento emesso prima o dopo l'eccezione?

**Problema:** Per `ViolationOccurred`, deve essere emesso prima o dopo che `ProtocolViolation` viene sollevata?

**Risposta definitiva:** PRIMA. Il monitor osserva SEMPRE, anche le violazioni. Il checker:
1. Rileva violazione
2. Emette `ViolationOccurred` al monitor
3. Solleva `ProtocolViolation`

Questo garantisce che il monitor veda tutto, anche se il chiamante cattura l'eccezione.

### Rischio 6: Timestamp precision e monotonicity

**Problema:** `time.time()` non e monotono su tutti i sistemi.

**Mitigazione:** Usare `time.monotonic()` per durate (non confrontabili tra processi), `time.time()` per timestamp assoluti. Documentare la scelta.

```python
_start = time.monotonic()  # per misurare durate
timestamp = time.time()    # per timestamp wall clock
duration_ms = (time.monotonic() - _start) * 1000
```

### Rischio 7: Cicli di importazione (circular imports)

**Problema:** checker.py importa monitor.py, monitor.py importa checker.py per i tipi.

**Mitigazione:** monitor.py usa `TYPE_CHECKING` guard per import condizionale. I tipi degli eventi sono autonomi (non dipendono da checker). Solo `MonitorEvent` usa stringhe di tipo per forward references.

---

## 6. Analisi Competitor: Come Fanno i Big

### OpenAI Agents SDK (Marzo 2025)

```
Architettura: Trace > Spans > SpanData
Hook: subclass AgentHooks, override on_start/on_end/on_tool_*
TraceProcessor: on_trace_start/end, on_span_start/end
Integrazione: add_trace_processor() o set_trace_processors()
Storage: BatchTraceProcessor + BackendSpanExporter (async batch)
ContextVar: _current_trace, _current_span (thread/async safe)
```

**Cosa prendere:** TraceProcessor pattern, ContextVar per nesting, batch processing

### Strands Agents SDK (Amazon 2025)

```
Architettura: BaseHookEvent (frozen dataclass) con should_reverse_callbacks
Tipi: Before*/After* pairs (Model, Tool, BidiMessage, BidiInterruption)
State: invocation_state dict condiviso tra agenti
Control: retry flags, cancel_tool booleans
```

**Cosa prendere:** Frozen dataclass per eventi, Before/After pairs, should_reverse

### AgentOps

```
Architettura: Session > Events (record(event))
Metriche: LLM calls, tool calls, errors, duration, cost, tokens
End state: Success | Failure | Indeterminate
Analytics: session.get_analytics() -> dict
Export: REST API /v2/sessions/<id>/export
```

**Cosa prendere:** End state enum, get_analytics() pattern, session-level aggregation

### LangSmith / LangGraph

```
Architettura: Run = unita base, progetti > traces > runs
Tracking: LLM, tool, node separati
Overhead: "virtually no measurable overhead" (LangSmith)
Alerting: alert su latency threshold, error rate
```

**Cosa prendere:** Overhead minimo, threshold alerting

### PyMOP (Ricerca Accademica 2025)

```
Architettura: Monitor Synthesizer > Instrumenter > Monitoring Engine
Pattern: parametric trace slicing (per session isolation)
Logiche: LTL, ERE, FSM, CFG - pluggable
Algoritmi: A (offline) a D (enable sets statici)
```

**Cosa prendere:** Parametric slicing concept, FSM per ogni sessione, pluggable logics

---

## 7. Confronto con Approcci Esistenti

| Aspetto | OpenTelemetry | AgentOps | PyMOP | Il Nostro Monitor |
|---------|---------------|----------|-------|-------------------|
| Deps | Molte | SDK + API | None | ZERO |
| Session types | No | No | Si (FSM) | Si (nativo) |
| Real-time | Si | Batch | Si | Si |
| Thread-safe | Si | Si | Si | Si |
| Hooks | TraceProcessor | record() | Instrumenter | on_event() |
| Metriche | Standard | Custom | Custom | Custom |
| Storage | Backend | Cloud | In-memory | In-memory |
| Costo | Gratis | Paid | Gratis | Gratis |
| Integrabile | Si ma pesante | No (cloud) | Si | Si (nativo) |

**Conclusione:** Nessun competitor fa exactamente quello che noi facciamo - monitoring di session types con ZERO deps integrato nel runtime checker. Questo e un **DIFFERENZIATORE UNICO**.

---

## 8. Raccomandazione Finale

### Modulo da Implementare: `monitor.py`

**File:** `packages/lingua-universale/src/cervellaswarm_lingua_universale/monitor.py`

**Struttura finale:**
```
monitor.py
  MonitorEvent          - base frozen dataclass
  SessionStarted        - evento inizio sessione
  MessageSent           - evento messaggio validato
  BranchChosen          - evento branch selezionato
  ViolationOccurred     - evento violazione rilevata
  SessionEnded          - evento fine sessione
  RepetitionStarted     - evento ripetizione protocollo

  MonitorListener       - Protocol (structural typing ABC)
  ProtocolMonitor       - emettitore + registry listener
  MetricsCollector      - raccoglitore metriche thread-safe
  MetricsSnapshot       - snapshot immutabile delle metriche

  # Listener built-in
  LoggingListener       - emette eventi al modulo logging stdlib
  NoOpListener          - per testing (no-op)
```

**Integrazione con SessionChecker:**
- `SessionChecker.__init__` accetta `monitor: Optional[ProtocolMonitor] = None`
- Emissione eventi in `send()`, `choose_branch()`, `__init__`
- Nessun impatto se monitor=None (guard `if self._monitor:`)

**Principi:**
1. ZERO dipendenze esterne (stdlib: threading, time, dataclasses, weakref, warnings)
2. Listener non deve mai rompere il checker (try/except con warnings.warn)
3. Thread-safe: threading.RLock + snapshot prima di notificare
4. Timing: time.monotonic() per durate, time.time() per wall clock
5. Frozen dataclasses per eventi (immutabili, hashable, confrontabili)
6. Context manager per listening (no memory leak)
7. Global default monitor opzionale (ergonomia)

**Test target:** 96%+ coverage (allineato al package)

**Dimensione stimata:** ~400 righe sorgente + ~200 test

**Priorita metriche da implementare:**
1. (P0) sessions_started/completed/violated - base health check
2. (P0) total_messages, total_violations - volumetria base
3. (P1) step_duration_ms - latency per step
4. (P1) violation_by_step - dove i protocolli si rompono
5. (P1) branch_frequency - uso reale dei branch
6. (P2) sessions_per_protocol - quale protocollo e piu usato
7. (P2) avg_session_duration_ms - quanto durano le sessioni
8. (P3) p95/p99 latencies - percentili (richiede sliding window)

---

## Appendice A: Riferimenti Tecnici Python Stdlib

```python
# Thread-safe listener notification
import threading
_lock = threading.RLock()
with _lock:
    snapshot = list(_listeners)  # snapshot fuori dal lock
for listener in snapshot:        # notifica senza lock
    listener.on_event(event)

# Context propagation
import contextvars
_current_monitor: contextvars.ContextVar[Optional['ProtocolMonitor']] = \
    contextvars.ContextVar('current_monitor', default=None)

# Durate precise
import time
start = time.monotonic()
# ... operazione ...
duration_ms = (time.monotonic() - start) * 1000.0

# Frozen dataclass evento
from dataclasses import dataclass
@dataclass(frozen=True)
class MonitorEvent:
    session_id: str
    timestamp: float = 0.0
    def __post_init__(self):
        object.__setattr__(self, 'timestamp', time.time())
```

---

## Appendice B: Fonti Complete

- [OpenTelemetry Observability Primer](https://opentelemetry.io/docs/concepts/observability-primer/)
- [OpenTelemetry AI Agent Observability Standards 2025](https://opentelemetry.io/blog/2025/ai-agent-observability/)
- [OpenTelemetry GenAI Agent Spans Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/)
- [PyMOP - Generic Python Runtime Verification System (arXiv 2025)](https://arxiv.org/html/2509.06324)
- [OpenAI Agents SDK - Tracing Architecture](https://openai.github.io/openai-agents-python/tracing/)
- [AgentOps Python SDK - GitHub](https://github.com/AgentOps-AI/agentops)
- [AgentOps Session Concepts](https://github.com/AgentOps-AI/agentops/blob/main/docs/v1/concepts/sessions.mdx)
- [Strands Agents SDK - Hook Events](https://strandsagents.com/latest/documentation/docs/api-reference/python/experimental/hooks/events/)
- [LangSmith AI Agent & LLM Observability](https://www.langchain.com/langsmith/observability)
- [AI Agent Observability Tools 2026 - AIM Multiple](https://research.aimultiple.com/agentic-monitoring/)
- [Top 5 AI Agent Observability Platforms 2026](https://www.getmaxim.ai/articles/top-5-ai-agent-observability-platforms-in-2026/)
- [OpenTelemetry Distributed Tracing Best Practices](https://www.withcoherence.com/articles/opentelemetry-distributed-tracing-tutorial-and-best-practices)
- [Google SRE Book - Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)
- [Jaeger vs Zipkin - Complete Comparison](https://signoz.io/blog/jaeger-vs-zipkin/)
- [Python Threading - Thread-Safe Observer Pattern](https://code.activestate.com/recipes/577106-threadsafe-observer-pattern-implemented-as-descrip/)
- [Python Observability Complete Guide](https://speedscale.com/blog/python-observability/)
- [Python contextvars - Context Variables](https://docs.python.org/3/library/contextvars.html)
- [Python weakref - Weak References](https://docs.python.org/3/library/weakref.html)
- [Safety and Liveness Properties - Wikipedia](https://en.wikipedia.org/wiki/Safety_and_liveness_properties)
- [UML Protocol State Machine Diagrams](https://www.uml-diagrams.org/protocol-state-machine-diagrams.html)
- [Threadsafe observer pattern - ActiveState](https://code.activestate.com/recipes/577106-threadsafe-observer-pattern-implemented-as-descrip/)
- [HTTPX Event Hooks Pattern](https://www.python-httpx.org/advanced/event-hooks/)
- [CrewAI AgentOps Integration](https://docs.crewai.com/how-to/agentops-observability)
- [OpenTelemetry Semantic Conventions GenAI](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
- [Agentic Frameworks Production 2026](https://zircon.tech/blog/agentic-frameworks-in-2026-what-actually-works-in-production/)
- [Robust Python - Event-Driven Architecture Ch.18](https://www.oreilly.com/library/view/robust-python/9781098100650/ch18.html)
- [Python collections.deque thread safety](https://bugs.python.org/issue15329)
- [Python queue module docs](https://docs.python.org/3/library/queue.html)
- [Runtime Verification - Lectures (INRIA)](https://inria.hal.science/hal-01762298v1/file/rv-book-editor-version.pdf)
- [Comparing Trace Expressions and LTL for RV](https://www.researchgate.net/publication/308417742_Comparing_Trace_Expressions_and_Linear_Temporal_Logic_for_Runtime_Verification)
- [Python Logging Module - Complete Guide](https://www.dash0.com/guides/logging-in-python)
- [SuperFastPython - Thread Context Variables](https://superfastpython.com/thread-context-variables-in-python/)

---

*Report generato da Cervella Researcher - CervellaSwarm*
*"Ricerca PRIMA di implementare. Non inventare, studia come fanno i big."*
