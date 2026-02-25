# Session Types per CervellaSwarm Agent Protocol v0.1

**Data:** 2026-02-19 | **Sessione:** S380
**Autrice:** La Regina
**Status:** DRAFT - Primo design

---

## 1. Il Problema

CervellaSwarm ha 17 agenti che comunicano tra loro. Oggi la comunicazione e:
- **Non tipizzata**: messaggi = blob di testo
- **Non verificata**: nessuna garanzia che il protocollo sia seguito
- **Non formale**: le regole sono in documentazione Markdown, non nel codice

Questo causa:
- Worker che restituiscono output in formato inatteso
- Audit che mancano step della checklist
- Protocolli interrotti (es: Architect crea PLAN.md ma nessuno lo approva)
- Nessuna garanzia di terminazione delle conversazioni

---

## 2. La Soluzione: Session Types

I Session Types descrivono il **protocollo** di comunicazione tra due o piu parti.
Il type checker verifica a compile-time che il protocollo sia rispettato.

### 2.1 Tipi Base dei Messaggi

```python
# Primitive message types for CervellaSwarm

class MessageType(Enum):
    """Every message in the swarm has exactly one type."""
    # Task lifecycle
    TASK_REQUEST = "task_request"       # Regina -> Worker
    TASK_RESULT = "task_result"         # Worker -> Regina
    TASK_DELEGATED = "task_delegated"   # Regina -> Worker (sub-delegation)

    # Audit lifecycle
    AUDIT_REQUEST = "audit_request"     # Regina -> Guardiana
    AUDIT_VERDICT = "audit_verdict"     # Guardiana -> Regina

    # Architecture lifecycle
    PLAN_REQUEST = "plan_request"       # Regina -> Architect
    PLAN_PROPOSAL = "plan_proposal"     # Architect -> Regina
    PLAN_APPROVAL = "plan_approval"     # Regina -> Architect
    PLAN_REJECTION = "plan_rejection"   # Regina -> Architect

    # Research lifecycle
    RESEARCH_QUERY = "research_query"     # Regina -> Researcher
    RESEARCH_REPORT = "research_report"   # Researcher -> Regina
    RESEARCH_REVIEW = "research_review"   # Guardiana Ricerca -> Regina

    # Team coordination (existing SendMessage types)
    DM = "message"                        # Any -> Any
    BROADCAST = "broadcast"               # Any -> All
    SHUTDOWN_REQUEST = "shutdown_request"  # Leader -> Worker
    SHUTDOWN_ACK = "shutdown_response"     # Worker -> Leader

    # Context injection (system)
    CONTEXT_INJECT = "context_inject"     # System -> All (SubagentStart)
```

### 2.2 Typed Message Schemas

```python
from dataclasses import dataclass
from typing import Optional, Literal
from enum import Enum

# --- Status Types ---

class TaskStatus(Enum):
    OK = "ok"
    FAIL = "fail"
    BLOCKED = "blocked"

class AuditVerdict(Enum):
    APPROVED = "approved"
    BLOCKED = "blocked"
    NEEDS_REVISION = "needs_revision"

class PlanComplexity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

# --- Agent Roles ---

class AgentRole(Enum):
    REGINA = "regina"
    GUARDIANA_QUALITA = "guardiana-qualita"
    GUARDIANA_RICERCA = "guardiana-ricerca"
    GUARDIANA_OPS = "guardiana-ops"
    ARCHITECT = "architect"
    SECURITY = "security"
    INGEGNERA = "ingegnera"
    BACKEND = "backend"
    FRONTEND = "frontend"
    TESTER = "tester"
    REVIEWER = "reviewer"
    RESEARCHER = "researcher"
    MARKETING = "marketing"
    DEVOPS = "devops"
    DOCS = "docs"
    DATA = "data"
    SCIENZIATA = "scienziata"

# --- Message Payloads ---

@dataclass(frozen=True)
class TaskRequest:
    """Regina -> Worker: delegate a task."""
    task_id: str
    description: str
    target_files: list[str]  # files worker should focus on
    constraints: list[str]   # rules to follow
    max_file_lines: int = 500

@dataclass(frozen=True)
class TaskResult:
    """Worker -> Regina: task completion report."""
    task_id: str
    status: TaskStatus
    summary: str             # max 1 sentence
    files_modified: list[str]
    files_created: list[str]
    test_command: Optional[str] = None
    next_steps: Optional[str] = None
    blockers: Optional[str] = None  # only if status == BLOCKED

@dataclass(frozen=True)
class AuditRequest:
    """Regina -> Guardiana: request quality audit."""
    audit_id: str
    target: str              # what to audit (step name, file list, etc.)
    checklist: list[str]     # items to verify
    worker_output: str       # the output being audited

@dataclass(frozen=True)
class AuditVerdict:
    """Guardiana -> Regina: audit result."""
    audit_id: str
    verdict: AuditVerdict
    score: float             # 0.0 - 10.0
    checked: list[str]       # what was verified
    issues: list[str]        # problems found
    action: str              # what to do next

@dataclass(frozen=True)
class PlanRequest:
    """Regina -> Architect: request an implementation plan."""
    plan_id: str
    task_description: str
    complexity_hint: Optional[PlanComplexity] = None
    constraints: list[str] = ()

@dataclass(frozen=True)
class PlanProposal:
    """Architect -> Regina: the implementation plan."""
    plan_id: str
    complexity: PlanComplexity
    risk_score: float        # 0.0 - 1.0
    files_affected: int
    phases: list[str]        # phase descriptions
    steps: list[str]         # ordered implementation steps
    success_criteria: list[str]
    plan_file: str           # path to PLAN.md

@dataclass(frozen=True)
class ResearchQuery:
    """Regina -> Researcher: research request."""
    query_id: str
    topic: str
    min_sources: int = 10
    scope: list[str] = ()    # specific areas to cover

@dataclass(frozen=True)
class ResearchReport:
    """Researcher -> Regina: research results."""
    query_id: str
    topic: str
    sources_consulted: int
    key_findings: list[str]
    report_file: str         # path to report .md file
```

### 2.3 Session Type Protocols

I protocolli definiscono l'ORDINE obbligatorio dei messaggi.

```python
# Protocol definitions using session type notation
#
# ! = send
# ? = receive
# . = sequence (then)
# + = choice (or)
# * = repetition
# End = protocol complete

# --- Protocol: Task Delegation ---
#
# The standard workflow: Regina delegates, Worker executes, Guardiana audits.
#
# Regina                    Worker                  Guardiana
#   |                         |                        |
#   |--- TaskRequest -------->|                        |
#   |                         |--- [work] --->         |
#   |<--- TaskResult ---------|                        |
#   |                         |                        |
#   |--- AuditRequest ------------------------------>  |
#   |                                                  |
#   |<--- AuditVerdict -------------------------------|
#   |                                                  |
#   Done                                            Done

PROTOCOL_DELEGATE_TASK = """
protocol DelegateTask {
    Regina  -> Worker    : TaskRequest;
    Worker  -> Regina    : TaskResult;
    Regina  -> Guardiana : AuditRequest;
    Guardiana -> Regina  : AuditVerdict;
}
"""

# --- Protocol: Architect Flow ---
#
# For complex tasks: plan first, then implement.
#
# Regina         Architect        Worker        Guardiana
#   |               |               |               |
#   |--PlanRequest->|               |               |
#   |               |               |               |
#   |<-PlanProposal-|               |               |
#   |               |               |               |
#   |--choice:                      |               |
#   |  approve:                     |               |
#   |    |--TaskRequest------------>|               |
#   |    |<--TaskResult-------------|               |
#   |    |--AuditRequest--------------------------->|
#   |    |<--AuditVerdict---------------------------|
#   |  reject:                      |               |
#   |    |--PlanRejection->|        |               |
#   |    |<-PlanProposal---|        |               |
#   |    (max 2 revisions)          |               |

PROTOCOL_ARCHITECT_FLOW = """
protocol ArchitectFlow {
    Regina    -> Architect : PlanRequest;
    Architect -> Regina    : PlanProposal;

    choice at Regina {
        approve: {
            Regina    -> Worker    : TaskRequest;
            Worker    -> Regina    : TaskResult;
            Regina    -> Guardiana : AuditRequest;
            Guardiana -> Regina    : AuditVerdict;
        }
        reject: {
            Regina    -> Architect : PlanRejection;
            Architect -> Regina    : PlanProposal;
            // max 2 revisions, then escalate
        }
    }
}
"""

# --- Protocol: Research Flow ---
#
# Research with quality gate.
#
# Regina      Researcher    Guardiana_Ricerca
#   |             |               |
#   |--Query----->|               |
#   |<--Report----|               |
#   |--Review request------------>|
#   |<--Review verdict------------|

PROTOCOL_RESEARCH_FLOW = """
protocol ResearchFlow {
    Regina              -> Researcher         : ResearchQuery;
    Researcher          -> Regina             : ResearchReport;
    Regina              -> GuardianaRicerca   : AuditRequest;
    GuardianaRicerca    -> Regina             : AuditVerdict;
}
"""

# --- Protocol: Bug Hunt ---
#
# Our proven bug hunting protocol (S374-S378).
#
# Regina    Researcher   Backend/Tester   Guardiana
#   |          |              |              |
#   |--Query-->|              |              |
#   |<-Report--|              |              |
#   |--TaskReq-------------->|              |
#   |<-TaskResult------------|              |
#   |--AuditReq---------------------------->|
#   |<-AuditVerdict-------------------------|
#   (repeat per package)

PROTOCOL_BUG_HUNT = """
protocol BugHunt {
    rec HuntLoop {
        Regina     -> Researcher : ResearchQuery;    // find bugs
        Researcher -> Regina     : ResearchReport;   // bug list
        Regina     -> Worker     : TaskRequest;      // fix bugs
        Worker     -> Regina     : TaskResult;       // fixes applied
        Regina     -> Guardiana  : AuditRequest;     // verify fixes
        Guardiana  -> Regina     : AuditVerdict;     // score

        choice at Regina {
            continue: HuntLoop;
            done: end;
        }
    }
}
"""
```

---

## 3. Mappa della Comunicazione Attuale (17 Agenti)

### 3.1 Ruoli e Permessi di Comunicazione

| Agente | Puo Parlare Con | Riceve Da | Modello |
|--------|-----------------|-----------|---------|
| Regina | TUTTI | TUTTI + Rafa | opus |
| Guardiana Qualita | Regina | Regina (audit req) | opus |
| Guardiana Ricerca | Regina | Regina (review req) | opus |
| Guardiana Ops | Regina | Regina (ops audit) | opus |
| Architect | Regina | Regina (plan req) | opus |
| Security | Regina | Regina (security audit) | opus |
| Ingegnera | Regina | Regina (analysis req) | opus |
| Backend | Regina | Regina (task req) | sonnet |
| Frontend | Regina | Regina (task req) | sonnet |
| Tester | Regina | Regina (task req) | sonnet |
| Reviewer | Regina | Regina (review req) | sonnet |
| Researcher | Regina | Regina (research query) | sonnet |
| Marketing | Regina | Regina (task req) | sonnet |
| DevOps | Regina | Regina (task req) | sonnet |
| Docs | Regina | Regina (task req) | sonnet |
| Data | Regina | Regina (task req) | sonnet |
| Scienziata | Regina | Regina (research query) | sonnet |

### 3.2 Topologia

```
                    RAFA (human)
                       |
                       | natural language
                       v
                   REGINA (hub)
                  /   |   |   \
                 /    |   |    \
     ┌──────────┘    |   |    └──────────┐
     v               v   v               v
  GUARDIANE      ARCHITECT   ANALISTE    WORKERS
  (3 opus)       (1 opus)    (2 opus)   (10 sonnet)
     |               |          |           |
     v               v          v           v
  AuditVerdict   PlanProposal  Report    TaskResult
```

**Osservazione critica:** La topologia e a STELLA con la Regina al centro.
Comunicazione Worker<->Worker = ZERO (tranne in Team mode con SendMessage).
Questo e un punto di design: centralizzato per controllo, ma bottleneck potenziale.

### 3.3 Flussi Identificati

| Flusso | Frequenza | Tipizzazione Attuale |
|--------|-----------|---------------------|
| DelegateTask | OGNI sessione, 5-20x | Nessuna |
| ArchitectFlow | 1-2x per task complessi | Semi (PLAN.md format) |
| ResearchFlow | 1-5x per sessione | Nessuna |
| BugHunt | Cicli di 3-7 step | Semi (tabella issue) |
| TeamCoordination | Rare (Team mode) | 5 tipi base |
| ContextInjection | Automatica, ogni spawn | Fixed format |

---

## 4. Proprieta Formali Desiderate

### 4.1 Safety Properties (cose che NON devono succedere)

1. **No orphan tasks**: Se TaskRequest e inviato, TaskResult DEVE arrivare
2. **No unaudited deploys**: Se TaskResult.status == OK, AuditRequest DEVE seguire
3. **No infinite loops**: Ogni protocollo ha un limite di ripetizioni
4. **No type mismatch**: Un AuditVerdict non puo essere inviato come risposta a TaskRequest
5. **No role violation**: Un Worker non puo inviare AuditVerdict

### 4.2 Liveness Properties (cose che DEVONO succedere)

1. **Progress**: Ogni protocollo avvia deve terminare (con OK, FAIL, o BLOCKED)
2. **Audit completeness**: Ogni AuditRequest produce AuditVerdict con score
3. **Plan resolution**: Ogni PlanProposal riceve approve o reject (max 2 revisions)

### 4.3 Invarianti dello Sciame

1. **Hub invariant**: Tutti i messaggi passano per la Regina (star topology)
2. **Model invariant**: Opus agents -> decision messages, Sonnet agents -> execution messages
3. **Idempotency**: Un messaggio duplicato non causa side-effect aggiuntivi
4. **Ordering**: Messaggi dello stesso protocollo sono ordinati (no out-of-order)

---

## 5. Piano di Implementazione

### Fase 1: Python Runtime Checker (S380 - OGGI)
- Dataclass per ogni tipo di messaggio
- Decorator `@session_protocol` per funzioni che partecipano a un protocollo
- Runtime validation: il messaggio ha i campi richiesti? il tipo e corretto?
- Logging di ogni messaggio con tipo e timestamp

### Fase 2: Protocol Monitor (S381-S382)
- State machine per ogni protocollo
- Il monitor traccia lo stato corrente della conversazione
- Warning se il protocollo viene violato (es: AuditRequest prima di TaskResult)
- Dashboard dello stato di tutti i protocolli attivi

### Fase 3: Integration con CervellaSwarm (S383-S385)
- Hook che wrappa Task tool per aggiungere type checking
- SubagentStart injection dei tipi di protocollo
- Output parsing automatico per estrarre TaskResult/AuditVerdict

### Fase 4: Formal Verification (S386+)
- Tradurre i protocolli in Dafny/Lean 4
- Verificare le proprieta formali (safety, liveness)
- Generare monitor da specifiche formali

---

## 6. Notazione della Lingua

Questa e la prima bozza della SINTASSI della Lingua Universale per protocolli agent:

```
// Dichiarazione agente
agent Regina : Hub { model: opus }
agent Backend : Worker { model: sonnet, domain: [python, api] }
agent GuardianaQualita : Guardiana { model: opus, audits: [Backend, Frontend, Tester] }

// Dichiarazione messaggio tipizzato
message TaskRequest {
    task_id: ID
    description: Text
    target_files: List<Path>
    constraints: List<Text>
    max_file_lines: Nat = 500
}

message TaskResult {
    task_id: ID
    status: OK | FAIL | BLOCKED
    summary: Text[..100]        // max 100 chars
    files_modified: List<Path>
    test_command: Option<Command>
    blockers: Option<Text> where status == BLOCKED
}

// Dichiarazione protocollo
protocol DelegateTask(r: Regina, w: Worker, g: Guardiana) {
    r -> w : TaskRequest;
    w -> r : TaskResult;

    if TaskResult.status == OK {
        r -> g : AuditRequest;
        g -> r : AuditVerdict;

        assert AuditVerdict.score >= 0.0;
        assert AuditVerdict.score <= 10.0;
    }
}

// Proprieta
property NoOrphanTasks {
    forall t: TaskRequest .
        eventually exists r: TaskResult .
            r.task_id == t.task_id
}

property AuditAfterSuccess {
    forall r: TaskResult where r.status == OK .
        eventually exists a: AuditRequest .
            a refers_to r
}
```

---

## 7. Perche Questo E Diverso

Nessuno sta facendo questo. I framework AI (AutoGen, CrewAI, LangGraph) hanno:
- Messaggi non tipizzati (stringhe)
- Protocolli impliciti (documentazione, non codice)
- Zero garanzie formali
- Zero session types

Dana (AI Alliance) e l'unico progetto che si avvicina, ma e intent-based (linguaggio naturale),
non protocol-based (garanzie formali sulla comunicazione).

CervellaSwarm sarebbe il PRIMO framework ad avere:
1. Typed agent messages
2. Formal session protocols
3. Runtime protocol monitoring
4. (futuro) Compile-time protocol verification

---

*"La domanda e la risposta nello STESSO linguaggio."* - Rafa

*Primo documento della Lingua Universale. S380.*
