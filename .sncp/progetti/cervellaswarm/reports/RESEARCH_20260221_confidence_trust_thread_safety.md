# Confidence Types, Trust Composition, Thread Safety - Ricerca Fase B
**Status**: COMPLETA
**Fonti**: 28 consultate (articoli accademici, librerie Python, framework, paper DeepMind/MIT/arxiv)
**Data**: 2026-02-21
**Progetto**: Lingua Universale - Fase B
**Autore**: Cervella Researcher

---

## EXECUTIVE SUMMARY

Ricerca su tre topic per Lingua Universale Fase B:
1. **Confidence Types** - Come tipare la confidenza degli output agente
2. **Trust Composition** - Come il trust si compone nelle catene di delega
3. **Thread Safety** - Come rendere SessionChecker thread-safe in modo corretto

**Risultato chiave**: I tre topic hanno soluzioni ben studiate a livello teorico (logica soggettiva di Josang, beta reputation system, MPST). La sfida per Lingua Universale e l'INTEGRAZIONE con i tipi frozen dataclass gia esistenti, con ZERO dipendenze esterne.

---

## TOPIC 1: CONFIDENCE TYPES

### 1.1 Stato dell'Arte - Cosa Esiste

#### Approcci Teorici (accademici)
- **Gradual Typing con incertezza**: Ricerca attiva (POPL 2024) su type systems che ottimizzano basandosi su type inference probabilistica. Il tipo `Optional[T]` di Python e il caso piu semplice di "probabilistic type" (0% o 100% fiducia sul tipo).
- **Probabilistic Type Inference (OptTyper)**: Approccio che modella l'inferenza di tipi come ottimizzazione di constraints logici e naturali. Accademico, non libreria pratica.
- **Gradual Typing**: Permette di annotare solo parte del programma. Teorizzato da Siek & Taha (2006), implementato in Python 3.5+. Non gestisce la confidenza NUMERICA di un output, solo la certezza del TIPO.

#### Approcci Pratici (Python)
- **`uncertainties` package (PyPI)**: Libreria matura per propagazione di incertezza fisica (es: `2.5 +/- 0.1`). Usa automatic differentiation con operator overloading. **Problema**: pensata per valori fisici/scientifici, non per output semantici di agenti IA.
- **`auto-uncertainties` (PyPI, 2025)**: Versione piu moderna della stessa idea.
- **`llm-confidence` (VATBox, PyPI)**: Libreria Python per estrarre confidence scores da output LLM usando log probabilities. API: `LogprobsHandler.format_logprobs()` + `process_logprobs()`. **Pertinente ma limitato**: opera solo su logprobs OpenAI-compatibili, non su output strutturati generici.
- **PydanticAI**: Approccio piu diffuso nella pratica - definisce `confidence: float = Field(ge=0.0, le=1.0)` nel BaseModel dell'output. Strutturato, validato, ma non propaga la confidenza attraverso operazioni composte.

#### Come lo Fanno i Framework Principali
- **CrewAI**: Non ha un tipo `Confidence` nativo. La confidenza e un campo custom nel task output (es: `confidence: float` in un Pydantic model). Non c'e composizione automatica.
- **AutoGen**: Non ha confidence types. Il trust e implicito nella struttura della conversazione (reviewer agent che valida).
- **LangGraph**: No confidence type nativo. I nodi del grafo possono aggiungere confidence come campo nello state dict.
- **PydanticAI**: Il piu avanzato - supporta `Literal["low", "medium", "high"]` o `float` come campo confidence nell'output type dell'agente. Nessuna propagazione automatica.

#### Gap Identificato
**NESSUN framework esistente ha un tipo `Confidence[T]` che si propaga automaticamente attraverso operazioni multi-agente.** Tutti usano un semplice float nel payload. La composizione e manuale.

### 1.2 Cosa Dobbiamo Inventare (vs Cosa Esiste)

| Concetto | Esiste | Note |
|----------|--------|------|
| `confidence: float` in dataclass | SI (Pydantic pattern) | Semplice, robusto |
| Validazione range [0.0, 1.0] | SI (`__post_init__` o Field) | Gia nel nostro stile |
| Propagazione automatica | NO | Da inventare |
| `Confident[T]` generic wrapper | NO in Python (esiste in Rust) | Da inventare |
| Confidence da logprobs LLM | SI (`llm-confidence`) | Fuori scope Lingua Universale |

### 1.3 Design Raccomandato per Lingua Universale

**Opzione A (MINIMA, consigliata per Fase B Step 1)**:
Aggiungere `confidence: float` ai message types esistenti che ne hanno bisogno:
```python
@dataclass(frozen=True)
class TaskResult:
    task_id: str
    status: TaskStatus
    summary: str
    confidence: float = 1.0   # NUOVO - default piena confidenza
    # ... resto invariato

    def __post_init__(self) -> None:
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(f"confidence must be [0.0, 1.0], got {self.confidence}")
        # ... resto validazione
```

**Opzione B (MEDIA, consigliata per Fase B Step 2)**:
Generic wrapper `Confident[T]` come frozen dataclass:
```python
@dataclass(frozen=True)
class Confident(Generic[T]):
    value: T
    confidence: float  # [0.0, 1.0]
    source: str = ""   # quale agente/step ha generato

    def __post_init__(self) -> None:
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(f"confidence must be [0.0, 1.0]")

    def map(self, f: Callable[[T], U]) -> "Confident[U]":
        return Confident(value=f(self.value), confidence=self.confidence, source=self.source)

    def and_then(self, f: Callable[[T, float], "Confident[U]"]) -> "Confident[U]":
        """Compose with confidence decay."""
        return f(self.value, self.confidence)
```

**Opzione C (MASSIMA, Fase B Step 3+)**:
`ConfidenceInterval` con lower/upper bound (stile Bayesiano):
```python
@dataclass(frozen=True)
class ConfidenceInterval:
    point: float      # stima puntuale
    lower: float      # lower bound (es: 5th percentile)
    upper: float      # upper bound (es: 95th percentile)
    method: str = "bootstrap"  # come e stato calcolato
```

**RACCOMANDAZIONE**: Iniziare con Opzione A (campo `confidence: float` nei message types critici). Semplice, testabile, compatibile con il design frozen-dataclass esistente. Fase B piu avanzata puo aggiungere Opzione B.

### 1.4 Quale MessageKind Beneficia di Confidence

Basandomi sui tipi esistenti in `types.py`:
- `TaskResult`: SI - il worker sa quanto e sicuro del risultato
- `AuditVerdict`: GIA CE' lo `score` (0.0-10.0) - considerare se basta o serve confidence separata
- `PlanProposal`: SI - gia ha `risk_score` (0.0-1.0), considerare `confidence` complementare
- `ResearchReport`: SI - ricercatrice sa quanto le sue fonti sono affidabili
- `TaskRequest`, `AuditRequest`, etc.: NO - richieste non hanno confidenza, e azioni di routing

---

## TOPIC 2: TRUST COMPOSITION

### 2.1 Stato dell'Arte - Fondamenta Teoriche

#### Soggective Logic (Josang, 2016 - libro Springer)
Il framework teorico piu rigoroso. Un'opinione e una tripla `(b, d, u)`:
- `b` = belief (credenza che sia vero)
- `d` = disbelief
- `u` = uncertainty/ignorance
- Vincolo: `b + d + u = 1.0`

Operatori chiave per composizione:
- **Discounting** (trust transitivity): `A trusts B` con opinione `w_AB`, `B trusts C` con `w_BC` -> `A trusts C` tramite B = `w_AB ⊗ w_BC`. Formula: `b_AC = b_AB * b_BC`, `d_AC = b_AB * d_BC`, `u_AC = d_AB + u_AB + b_AB * u_BC`
- **Fusion** (combine multiple sources): `A` riceve trust da fonte 1 e fonte 2 -> combina con consensus operator o averaging operator

**Per Lingua Universale**: Questo framework e maturo ma complesso. La semplificazione pratica e il discounting scalare: `t_AB * t_BC` (prodotto), oppure `min(t_AB, t_BC)` (conservative).

#### Beta Reputation System (Josang & Ismail, 2002)
Usa distribuzione Beta per rappresentare trust. Il trust di agente A verso B e rappresentato da `Beta(alpha, beta)` dove:
- `alpha` = numero di interazioni positive + 1
- `beta` = numero di interazioni negative + 1
- Stima puntuale: `E = alpha / (alpha + beta)`

Aggiornamento Bayesiano: ogni nuova interazione aggiorna alpha o beta. **Vantaggio**: il trust si "guadagna" gradualmente, non e statico. **Per Lingua Universale**: rilevante per un sistema di reputazione dinamica degli agenti.

#### Trust Inference and Propagation (TIP) - NSF/Springer 2024
Framework per team multi-robot/multi-human. Esplicita la differenza tra:
- **Direct trust**: esperienza diretta con l'agente
- **Indirect trust**: raccomandazioni di terzi (reputazione)
Formula TIP: `T_direct * alpha + T_indirect * (1-alpha)` dove alpha e peso della fiducia diretta.

#### Jøsang Trust Transitivity
Per catene `A -> B -> C`:
- **Conservative**: `trust(A,C) = min(trust(A,B), trust(B,C))`
- **Multiplicative**: `trust(A,C) = trust(A,B) * trust(B,C)`
- **Harmonic**: media armonica dei trust nella catena

La letteratura (Josang 2009) dimostra che il prodotto e piu corretto matematicamente per catene dove i trust sono condizionalmente indipendenti.

### 2.2 Come lo Fanno i Framework Principali

- **CrewAI**: Nessun modello di trust. La "fiducia" e implicita nella gerarchia dei ruoli (manager > worker).
- **AutoGen**: Nessun modello di trust. Il trust e strutturale: chi chiama chi.
- **LangGraph**: Nessun modello di trust. I nodi possono rifiutare, ma non c'e trust score.
- **DelegateOS** (TypeScript, 2026 - basato su paper DeepMind): Il piu avanzato. Trust engine con:
  - Composite trust score con exponential decay
  - Cold-start handling (trust iniziale basso per agenti nuovi)
  - Breakdown per reliability/quality/speed
  - Trust che migliora nel tempo (agenti affidabili vengono scelti prima)
  - **Non e Python** ma e MIT license e illustra il pattern

### 2.3 Paper DeepMind "Intelligent AI Delegation" (Feb 2026, arxiv:2602.11865)

Paper freschissimo e molto rilevante. Key points:
1. **Trust != Reputation**: Trust e privato e contestuale (soglia che il delegante imposta). Reputation e pubblica e verificabile (storico delle performance).
2. **Privilege Attenuation** (monotonica): quando un agente sub-delega, puo dare solo un sottoinsieme dei propri permessi. Mai espandere authority.
3. **Transitive Accountability via Attestation**: in catene `A -> B -> C`, B firma crittograficamente le performance di C e le manda ad A. A monitora la capacita di B di monitorare C, non C direttamente.
4. **Graduated Authority Model**: agenti con trust basso hanno constraints stretti. Agenti con alta reputazione operano con minima supervisione.
5. **Circuit Breakers**: revoca automatica dei permessi se il reputation score crolla o viene rilevata anomalia.

**Non fornisce formule matematiche esplicite** per composizione del trust, ma definisce i principi architetturali.

### 2.4 MIT "Authenticated Delegation" (Jan 2025, arxiv:2501.09674) - ICML 2025

Approccio complementare: estende OAuth 2.0 + OpenID Connect con credenziali specifiche per agenti. Rilevante per l'autenticazione, meno per la matematica del trust.

### 2.5 TRiSM per Agentic AI (arxiv:2506.04133, aggiornato Dic 2025)

Framework strutturato: Trust, Risk, Security Management per sistemi multi-agente LLM-based. Introduce:
- **Component Synergy Score (CSS)**: quantifica la qualita della collaborazione inter-agente
- **Tool Utilization Efficacy (TUE)**: valuta l'efficienza dell'uso degli strumenti
Nessuna formula esplicita di trust composition pubblicata nel paper.

### 2.6 Design Raccomandato per Lingua Universale

**Modello scelto**: Trust scalare [0.0, 1.0] per ogni AgentRole, con composizione moltiplicativa per catene di delega.

**Struttura dati proposta:**
```python
@dataclass(frozen=True)
class TrustLevel:
    """Trust di un agente/ruolo in un contesto specifico."""
    value: float           # [0.0, 1.0]
    interactions: int = 0  # n. interazioni dirette (per Bayesian update)
    source: str = "default"  # "direct", "reputation", "default"

    def __post_init__(self) -> None:
        if not (0.0 <= self.value <= 1.0):
            raise ValueError(f"trust must be [0.0, 1.0], got {self.value}")

    def compose(self, other: "TrustLevel") -> "TrustLevel":
        """Composizione multiplicativa per catena di delega A->B->C."""
        return TrustLevel(
            value=self.value * other.value,
            source="composed",
        )

    def attenuate(self, factor: float) -> "TrustLevel":
        """Attenuazione per sub-delega (privilege attenuation)."""
        if not (0.0 <= factor <= 1.0):
            raise ValueError(f"factor must be [0.0, 1.0]")
        return TrustLevel(value=self.value * factor, source="attenuated")
```

**Default Trust per AgentRole (baseline CervellaSwarm):**
```
REGINA: 1.0 (hub, piena fiducia)
GUARDIANE: 0.95 (opus, alta fiducia)
ARCHITECT/SECURITY/INGEGNERA: 0.90 (opus strategico)
WORKERS: 0.75 (sonnet, fiducia media)
```

**Formula composizione catena `A->B->C`:**
```
trust(A, C through B) = trust(A, B) * trust(B, C)
```
Esempio: REGINA (1.0) delega a BACKEND (0.75) che delega a tool esterno (0.6):
`trust_chain = 1.0 * 0.75 * 0.6 = 0.45`

**Regola Privilege Attenuation (da DeepMind 2026):**
B non puo delegare piu authority di quanta ne abbia ricevuta da A. Implementazione: `trust_delegated = min(trust_from_A, trust_B_assigns_to_C)`.

**Gestione Cold Start:**
Agenti nuovi/sconosciuti ricevono trust di default basso (es: 0.5) invece di 0.0 (evita deadlock) o 1.0 (troppo ottimista). Documentato come pattern nel DelegateOS.

---

## TOPIC 3: THREAD SAFETY PER SESSION CHECKER

### 3.1 Situazione Attuale

Il `SessionChecker` attuale (checker.py) ha `SessionState` come oggetto mutable condiviso. In un contesto single-threaded (un checker per session, usato sequenzialmente) e perfettamente corretto. Il problema emerge se:
1. Lo stesso checker viene chiamato da thread multipli (es: asyncio + thread pool)
2. Python 3.13+ free-threaded (GIL opzionale - PEP 703)

### 3.2 Python GIL e Free-Threading

- **CPython 3.12 e prima**: GIL protegge automaticamente. `SessionChecker` e implicitamente safe se chiamato dallo stesso thread.
- **CPython 3.13+**: GIL e opzionale (`--disable-gil`, PEP 703). In free-threading, i built-in types (dict, list) hanno internal locks ma non e sufficiente per strutture compound.
- **Python 3.14**: Performance penalty del free-threaded mode ora ~5-10% (era 40% in 3.13) grazie a specializing adaptive interpreter thread-safe.
- **Implicazione**: Il codice che dipende implicitamente dal GIL diventa non-safe in Python 3.13+ free-threaded.

### 3.3 Pattern Esistenti - Cosa Fanno i Big

#### Multiparty Session Types in Rust (Springer 2020, PMC)
Le implementazioni MPST in Rust usano il type system per garantire la safety: il compilatore impedisce l'accesso concorrente allo stesso canale da thread diversi (ownership + borrow checker). In Python non abbiamo questo.

#### CoMPSeT (arxiv:2510.24205, 2025)
Framework per comparare implementazioni MPST. Usa semantica asincrona, ma non affronta direttamente il thread safety in Python. E compilato in JavaScript per uso browser, non server.

#### asyncio.Lock in Python
`asyncio.Lock` e coroutine-safe ma NON thread-safe. Non e la soluzione per threading.
`threading.Lock` e la soluzione corretta per thread multipli.
`threading.RLock` (reentrant) serve se lo stesso thread puo acquisire il lock piu volte (ricorsione).

#### Asyncio RLock (terze parti)
Il modulo asyncio non include RLock nativo. Esistono librerie come `fair-async-rlock` (PyPI) per casi async. **Non serve per il nostro caso** perche SessionChecker e sincrono.

### 3.4 Pattern Raccomandati

#### Pattern A: Lock per Session (RACCOMANDATO)
Un lock per ogni istanza di `SessionChecker`. Semplice, minimale:
```python
import threading

class SessionChecker:
    def __init__(self, protocol, session_id="", ...):
        self._lock = threading.Lock()
        self._state = SessionState(...)
        # ...

    def send(self, sender, receiver, msg):
        with self._lock:
            # tutto il corpo di send e atomico
            ...

    def choose_branch(self, branch_name):
        with self._lock:
            ...
```
**Pro**: Semplice, corretto, zero dipendenze. Lock acquisita per tutta la durata di send().
**Contro**: Contention se molti thread chiamano send() concorrentemente sullo stesso checker. Ma questo e improbabile nel design CervellaSwarm (un checker per session).

#### Pattern B: Immutable Snapshot + Atomic Replace (AVANZATO)
Invece di mutare `SessionState`, ogni `send()` crea un nuovo `SessionState` immutabile e lo sostituisce atomicamente:
```python
import threading

class SessionChecker:
    def __init__(self, ...):
        self._state_ref: list[SessionState] = [SessionState(...)]  # lista per mutabilita
        self._lock = threading.Lock()

    def send(self, ...):
        with self._lock:
            old_state = self._state_ref[0]
            new_state = old_state.evolved(...)  # produce nuovo stato immutabile
            self._state_ref[0] = new_state
```
**Pro**: `SessionState` puo diventare fully frozen (frozen=True dataclass). Snapshot facili.
**Contro**: Overhead di costruire nuovo oggetto ad ogni messaggio. Piu complesso.

#### Pattern C: Per-Session Isolation (DESIGN LEVEL - MEGLIO)
La soluzione migliore non e rendere il checker thread-safe, ma garantire che ogni session abbia un solo checker e che venga usato da un solo thread/coroutine alla volta. Questo e il pattern delle implementazioni MPST mature (Rust, Haskell):
```python
# In integration.py, create_session() restituisce un checker
# owned da chi lo crea. Ownership = responsabilita del caller di
# non condividere il checker tra thread.
```
Documentare nella docstring che `SessionChecker` non e thread-safe e che il chiamante deve usare un lock esterno se necessario.

### 3.5 Raccomandazione Concreta per Fase B

**Fase B Step 1**: Aggiungere `threading.Lock` interno a `SessionChecker` (Pattern A). Costo zero in single-thread (lock uncontested e praticamente gratis). Protegge per Python 3.13+ free-threading e usi multi-thread.

**Fase B Step 2**: Documentare che un `SessionChecker` corrisponde a esattamente una sessione e non va condiviso tra coroutines asyncio senza `asyncio.Lock` esterno.

**Implementazione minimale:**
```python
import threading
from dataclasses import dataclass, field

@dataclass
class SessionChecker:
    # NOTA: non usiamo frozen=True perche abbiamo il lock
    def __init__(self, protocol, session_id="", role_bindings=None, monitor=None):
        self._lock = threading.Lock()  # AGGIUNTO per thread safety
        self._state = SessionState(...)
        # ... resto invariato

    def send(self, sender, receiver, msg):
        with self._lock:
            # corpo invariato
            ...

    def choose_branch(self, branch_name):
        with self._lock:
            # corpo invariato
            ...

    # Properties read-only non necessitano lock (lettura atomica in CPython)
    # Ma per safety con free-threading, aggiungerlo anche a step_index, is_complete
    @property
    def is_complete(self) -> bool:
        with self._lock:
            return self._state.completed
```

**Nota sul `log` property**: il metodo `log` ritorna `list(self._state.log)` (gia una copia) - corretto. Con lock:
```python
@property
def log(self) -> list[MessageRecord]:
    with self._lock:
        return list(self._state.log)
```

---

## SINTESI COMPARATIVA

| Topic | Cosa Esiste | Cosa Inventare | Difficolta |
|-------|-------------|----------------|------------|
| Confidence types | `float` campo in dataclass (Pydantic pattern). Nessun `Confident[T]` generic nativo | `Confident[T]` wrapper + regole composizione | MEDIA |
| Trust composition | Josang Subjective Logic (teorico). DelegateOS (TS). Beta reputation | TrustLevel dataclass + formula moltiplicativa + default per ruolo | BASSA-MEDIA |
| Thread safety | `threading.Lock` standard Python. Pattern MPST in Rust | Aggiungere lock interno a SessionChecker | BASSA |

---

## RACCOMANDAZIONI PRIORITARIE PER FASE B

### Priorita 1 (Fase B Step 1) - Thread Safety
**Action**: Aggiungere `threading.Lock` a `SessionChecker.__init__` e wrappare `send()`, `choose_branch()`, `is_complete`, `log`, `step_index` con `with self._lock`.
**Effort**: 1-2 ore. **Rischio**: zero. **Valore**: protegge Python 3.13+ free-threading.

### Priorita 2 (Fase B Step 2) - Trust Module
**Action**: Nuovo file `trust.py` con `TrustLevel` frozen dataclass + `AgentTrust` (mapping AgentRole -> TrustLevel) + `compose_trust_chain()` helper.
**Effort**: 1 giorno. **Rischio**: basso (e matematica semplice). **Valore**: primo trust composition system tipato per agenti IA in Python.

### Priorita 3 (Fase B Step 3) - Confidence Types
**Action**: Aggiungere `confidence: float = 1.0` a `TaskResult`, `ResearchReport`, `PlanProposal`. Non rompere retrocompatibilita (default=1.0). Poi valutare `Confident[T]` generic.
**Effort**: 0.5 giorno per field, 1 giorno per `Confident[T]`. **Rischio**: basso. **Valore**: unico framework Python con typed confidence nei messaggi agente.

---

## FONTI CONSULTATE (28)

### Confidence Types
1. [Python Typing Survey 2025 - Meta Engineering](https://engineering.fb.com/2025/12/22/developer-tools/python-typing-survey-2025-code-quality-flexibility-typing-adoption/)
2. [Type-based Gradual Typing Performance Optimization - POPL 2024](https://popl24.sigplan.org/details/POPL-2024-popl-research-papers/91/Type-based-Gradual-Typing-Performance-Optimization)
3. [Gradual Typing in Type Theory - Number Analytics](https://www.numberanalytics.com/blog/ultimate-guide-gradual-typing-type-theory)
4. [uncertainties package - PyPI](https://pypi.org/project/uncertainties/)
5. [AutoUncertainties - OSTI 2025](https://www.osti.gov/servlets/purl/2575193)
6. [llm-confidence - VATBox GitHub](https://github.com/VATBox/llm-confidence)
7. [llm-confidence - PyPI](https://pypi.org/project/llm-confidence/)
8. [Pydantic AI - Output types](https://ai.pydantic.dev/output/)
9. [Estimating LLM confidence with logprobs - Eric Jinks 2025](https://ericjinks.com/blog/2025/logprobs/)
10. [Mastering Confidence Scoring in AI Agents - SparkCo](https://sparkco.ai/blog/mastering-confidence-scoring-in-ai-agents/)
11. [Pydantic AI issue #1228 - logprobs in agent response](https://github.com/pydantic/pydantic-ai/issues/1228)

### Trust Composition
12. [Intelligent AI Delegation - DeepMind, arXiv:2602.11865 (Feb 2026)](https://arxiv.org/abs/2602.11865)
13. [Authenticated Delegation and Authorized AI Agents - MIT, arXiv:2501.09674 (Jan 2025)](https://arxiv.org/abs/2501.09674)
14. [TRiSM for Agentic AI - arXiv:2506.04133 (aggiornato Dic 2025)](https://arxiv.org/abs/2506.04133)
15. [DelegateOS - newtro/delegateos GitHub](https://github.com/newtro/delegateos)
16. [DelegateOS HackerNews discussion](https://news.ycombinator.com/item?id=47043354)
17. [TIP: Trust Inference and Propagation - Springer/NSF 2024](https://link.springer.com/article/10.1007/s10514-024-10175-3)
18. [A General Trust Framework for Multi-Agent Systems - AAMAS 2021](https://www.ifaamas.org/Proceedings/aamas2021/pdfs/p332.pdf)
19. [Subjective Logic - Josang, Springer 2016](https://link.springer.com/book/10.1007/978-3-319-42337-1)
20. [The Beta Reputation System - Semantic Scholar](https://www.semanticscholar.org/paper/The-Beta-Reputation-System-Ismail-J%C3%B8sang/2c9736ba3ffcfec14a3cce61ae7592c05498f505)
21. [Trust Transitivity and Conditional Belief Reasoning - ResearchGate](https://www.researchgate.net/publication/285983031_Trust_Transitivity_and_Conditional_Belief_Reasoning)
22. [Model checking combined trust and commitments - ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0957417423033584)
23. [Advanced Features in Bayesian Reputation Systems - Josang 2009](https://www.mn.uio.no/ifi/english/people/aca/josang/publications/jq2009-trustbus.pdf)

### Thread Safety
24. [Python free-threading guide - Python 3.14 docs](https://docs.python.org/3/howto/free-threading-python.html)
25. [PEP 703 - Making GIL Optional in CPython](https://peps.python.org/pep-0703/)
26. [Implementing Multiparty Session Types in Rust - PMC/Springer](https://pmc.ncbi.nlm.nih.gov/articles/PMC7282848/)
27. [CoMPSeT: Framework for Comparing MPST - arXiv:2510.24205 (2025)](https://arxiv.org/abs/2510.24205)
28. [asyncio Synchronization Primitives - Python 3.14 docs](https://docs.python.org/3/library/asyncio-sync.html)

---

## APPENDICE: CONFIDENCE COMPOSITION RULES

Quando la confidenza deve propagarsi attraverso passi multipli, le regole piu comuni:

**Regola Prodotto** (piu comune, conservativa):
`confidence_out = confidence_step1 * confidence_step2 * ... * confidence_stepN`
Esempio: ricercatrice (0.9) -> regina (1.0) -> guardiana (0.95) = `0.9 * 1.0 * 0.95 = 0.855`

**Regola Minimo** (piu conservativa):
`confidence_out = min(confidence_step1, ..., confidence_stepN)`
Esempio: `min(0.9, 1.0, 0.95) = 0.9`

**Regola Media Pesata** (bilancia):
`confidence_out = sum(w_i * c_i) / sum(w_i)` dove `w_i` e il peso del passo i

**Consensus Multi-Agente** (da ricerca 2025):
Quando piu agenti contribuiscono con lo stesso dato:
`confidence_consensus = min(c_i for c_i in confidences)` - il minimo vince (la catena e forte quanto il suo anello piu debole).

---

*Ricerca completata: 2026-02-21*
*Agente: Cervella Researcher*
*Sessione: S388 (presumibile)*
