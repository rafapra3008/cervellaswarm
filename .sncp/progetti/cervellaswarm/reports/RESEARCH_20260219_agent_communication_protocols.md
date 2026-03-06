# Protocolli di Comunicazione tra Agenti AI - Analisi Comparativa

**Data:** 2026-02-19
**Autrice:** Cervella Researcher
**Status:** COMPLETA
**Fonti consultate:** 28 (WebSearch + WebFetch + papers arxiv)
**Scope:** Claude Code, AutoGen v0.4, A2A, ACP, ANP, CrewAI, LangGraph, FIPA ACL, MCP, OpenAI Agents SDK, NLIP, μACP, ricerca accademica session types
**Contesto:** Input per Lingua Universale Fase A - Verified Agent Protocol

---

## EXECUTIVE SUMMARY

Il campo dei protocolli inter-agente AI sta vivendo un'esplosione senza precedenti: da 0 standard nel 2023
a 7+ protocolli competitivi nel 2026, con una convergenza industriale in corso (A2A + ACP unificati sotto
Linux Foundation). Il pattern emergente e chiaro: tutti i framework industriali scelgono messaggi JSON non
tipizzati, comunicazione attraverso testo naturale, e ZERO garanzie formali. Il contrasto con la ricerca
accademica (session types, μACP, verifica formale) e netto e rappresenta la piu grande opportunita per
CervellaSwarm.

**Il gap principale**: Nessun framework industriale garantisce formalmente deadlock-freedom, liveness o
type-safety a livello di protocollo. Tutti delegano la correttezza ai prompt e alla "buona volonta" del LLM.

---

## PARTE 1: CLAUDE CODE (Anthropic)

### 1.1 Architettura di Comunicazione

Claude Code usa il **Task tool** come meccanismo principale di comunicazione inter-agente. Il modello e
gerarchico a stella: un agente orchestratore lancia subagenti tramite Task tool, i subagenti eseguono in
contesti isolati e restituiscono un risultato testuale.

**Modello di spawning:**
- Orchestratore chiama Task tool con prompt + contesto
- Il subagente gira in un contesto window separato
- Supporto di fino a 7 agenti in parallelo
- Il subagente NON puo vedere le tool calls intermedie degli altri agenti
- Il subagente NON puo comunicare con altri subagenti (topologia hub-and-spoke pura)

**Regola fondamentale**: "Subagents only report results back to the main agent and never talk to each other."

### 1.2 Formato dei Messaggi

Non esiste un wire format documentato pubblicamente per la comunicazione inter-agente Task tool.
Il formato e semantico:

```
[Orchestratore] -> Task tool call:
  description: "<descrizione del task in linguaggio naturale>"
  (contesto iniettato da SubagentStart hook o .claude/agents/*.md)

[Subagente] -> Risultato:
  Testo libero (finale dell'agente)
  + agent_id (per hook SubagentStop)
  + agent_transcript_path (per osservabilita)
```

L'orchestratore riceve **solo il testo finale** del subagente. Le tool calls intermedie sono opache.

### 1.3 Hook di Ciclo di Vita

Claude Code espone hook per il ciclo di vita degli agenti:
- **SubagentStart**: input con contesto del task delegato
- **SubagentStop**: input con `last_assistant_message`, `agent_id`, `agent_transcript_path`
- Il nostro hook `subagent_context_inject.py` usa SubagentStart per iniettare FATOS + PROMPT_RIPRESA

Il problema di osservabilita: tutti gli hook condividono lo stesso `session_id` indipendentemente
da quale agente li ha generati. Questo rende difficile tracciare quale subagente ha prodotto quale output.

### 1.4 MCP come Layer Complementare

I subagenti Claude Code comunicano con tool e risorse esterne tramite MCP (vedi sezione 7).
MCP e separato dal Task tool: Task = comunicazione tra agenti Claude, MCP = comunicazione agente-strumento.

### 1.5 Tipizzazione e Garanzie

| Proprieta | Valore |
|-----------|--------|
| Schema messaggi | Testo naturale (nessuno schema) |
| Tipizzazione | NON TIPIZZATO |
| Garanzie formali | NESSUNA |
| Errori | Propagazione implicita via testo |
| Deadlock | Nessuna protezione formale |

**Punto debole principale**: Nessun contratto formale tra orchestratore e subagente. Il subagente
puo restituire qualsiasi testo, l'orchestratore deve interpretarlo. Errori di parsing sono
impossibili da rilevare staticamente.

---

## PARTE 2: AUTOGEN v0.4 (Microsoft)

### 2.1 Redesign Radicale rispetto a v0.2

AutoGen v0.4 (rilasciato Gennaio 2025) e un redesign completo. Il vecchio modello (conversazione
round-robin tra agenti) e stato abbandonato in favore di un sistema asincrono basato su messaggi.

**Filosofia core**: "Messaggi sono puramente dati, non devono contenere logica."

### 2.2 Due Pattern di Comunicazione

**Direct Messaging (request/response)**:
```python
response = await self.send_message(Message(...), agent_id)
# Eccezioni propagano al mittente - coupling forte
```

**Broadcast (publish/subscribe)**:
```python
await self.publish_message(Message(...), topic_id=TopicId(...))
# One-way, nessuna risposta, eccezioni silenziate (solo log)
# Un agente NON riceve i propri messaggi broadcast
```

### 2.3 Formato dei Messaggi

I messaggi AutoGen sono **dataclass Pydantic o Python dataclass serializzabili**:

```python
@dataclass
class TextMessage:
    content: str
    source: str

@dataclass
class ImageMessage:
    url: str
    source: str

# Messaggi strutturati: Pydantic BaseModel
class StructuredMessage(BaseModel):
    action: str
    parameters: dict
    priority: int
```

Il routing e basato sul **tipo Python** del messaggio: il decoratore `@message_handler` dispatcha
automaticamente al handler corretto in base al tipo ricevuto.

### 2.4 Tipizzazione e Garanzie

| Proprieta | Valore |
|-----------|--------|
| Schema messaggi | Pydantic/dataclass (tipizzato) |
| Tipizzazione | PARZIALMENTE TIPIZZATO |
| Type routing | Si (via decorator @message_handler) |
| Garanzie formali | PARZIALI |
| Loop prevention | Si (agente non riceve propri broadcast) |
| Deadlock | Nessuna protezione formale |

**Garanzia notevole**: Il sistema garantisce che un agente non riceva mai i propri messaggi broadcast,
prevenendo loop infiniti. Ma non ci sono garanzie di liveness o deadlock-freedom a livello di protocollo.

**Punto debole principale**: Il routing basato sul tipo Python e a runtime, non a compile time.
In un sistema distribuito (agenti su macchine diverse), il tipo deve essere serializzato/deserializzato
e la corrispondenza non e garantita formalmente. Il `content` dei messaggi di chat rimane testo libero.

---

## PARTE 3: GOOGLE AGENT-TO-AGENT (A2A)

### 3.1 Storia e Status

A2A e stato annunciato da Google in Aprile 2025. In Giugno 2025, Linux Foundation ha lanciato il
progetto A2A come standard open. In Agosto 2025, IBM/BeeAI ACP si e fuso con A2A sotto Linux Foundation.
Microsoft e SAP hanno dato il loro supporto. E il protocollo con la piu ampia adozione industriale (2026).

### 3.2 Architettura e Concetti Chiave

**Agent Card**: Documento JSON che un agente pubblica su `/.well-known/agent.json` dichiarando:
- Identita e provider
- Capabilities (streaming, push notifications, extended card)
- Schemi di autenticazione (API Key, OAuth2, mTLS, OpenID Connect)
- Skill definitions con input/output schema
- Protocol bindings supportati (JSON-RPC, gRPC, HTTP/REST)
- Firma digitale opzionale per integrity

**Task**: Unita di lavoro stateful con ID univoco. Ciclo di vita:
`working -> input_required | auth_required | completed | failed | canceled | rejected`

**Message**: Composto da Role (user | agent) + Parts (text, file, structured data).

### 3.3 Formato Wire

Il source of truth di A2A e un **file `.proto` (Protocol Buffers)** con bindings in:
- JSON-RPC 2.0 (default, named parameters)
- gRPC (streaming nativo)
- HTTP/REST (endpoints RESTful, headers `A2A-Version`, `A2A-Extensions`)

```json
// Esempio SendMessage request (JSON-RPC 2.0)
{
  "jsonrpc": "2.0",
  "id": "req-123",
  "method": "message/send",
  "params": {
    "message": {
      "role": "user",
      "parts": [{"text": "Analizza questo dataset"}],
      "contextId": "ctx-456"
    }
  }
}
```

### 3.4 Streaming e Notifiche Push

Tre modalita di aggiornamento:
1. **Polling**: GetTask (semplice, alta latenza)
2. **Streaming**: SendStreamingMessage / SubscribeToTask (SSE, bassa latenza)
3. **Push Notifications**: Webhook per aggiornamenti asincroni

Gli stream garantiscono ordinamento degli eventi e supportano connessioni multiple per lo stesso task.

### 3.5 Tipizzazione e Garanzie

| Proprieta | Valore |
|-----------|--------|
| Schema messaggi | Proto3 come source of truth |
| Tipizzazione | PARZIALMENTE TIPIZZATO (Artifact schema, Agent Card) |
| Autenticazione | OAuth2, mTLS, OpenID Connect |
| Garanzie formali | PARZIALI (idempotenza Get, ordinamento stream) |
| Deadlock | Nessuna protezione formale |
| Content validation | Schema Skills, ma `parts.text` e testo libero |

**Punto debole principale**: Il contenuto dei messaggi (le Parts) e testo libero o structured data
non verificato formalmente. Il protocollo garantisce la consegna e l'autenticazione, non la
correttezza semantica del contenuto. Enterprise-centric: assumed un catalogo agenti pre-esistente.

---

## PARTE 4: IBM AGENT COMMUNICATION PROTOCOL (ACP/BeeAI)

### 4.1 Status (Agosto 2025: FUSO CON A2A)

ACP e stato annunciato da IBM/BeeAI in Maggio 2025. In Agosto 2025 si e fuso con A2A sotto
Linux Foundation. Il team ACP sta contribuendo la propria tecnologia ad A2A. ACP come protocollo
indipendente non e piu in sviluppo attivo.

### 4.2 Caratteristiche Distintive (ora ereditate da A2A)

**Multipart messages con MIME typing**:
- Ogni messaggio e composto da parti con tipo MIME esplicito
- Support nativo per multimodal (testo, immagine, audio, binario)
- Parti semanticamente taggate

**Architettura brokered**:
- Registry centrale per discovery degli agenti
- Agent Detail manifests con operazioni e content types dichiarati
- Validazione schema su sendTask/getTask

**Transport**: HTTP con stream incrementali per task asincroni.

**Punto debole principale (ora risolto dalla fusione)**: Richiedeva un registry centrale con
forte controllo organizzativo. Questo limitava l'uso in scenari open-internet.

---

## PARTE 5: CREWAI

### 5.1 Architettura di Comunicazione

CrewAI usa un modello gerarchico stretto: un Manager agent (implicito o esplicito) coordina
Worker agents tramite task delegation. La comunicazione avviene attraverso un "scratchpad" condiviso:
l'output di un task diventa automaticamente il contesto del task successivo.

**Regola di isolamento**: I worker agents comunicano SOLO con il manager/orchestratore, mai direttamente
tra loro. Eccezione: in Crew YAML, il campo `context` di un task puo puntare all'output di task specifici.

**Transport**: Dal Luglio 2025, CrewAI supporta il protocollo A2A come primitive di delegation,
con JSON-RPC o gRPC come transport options.

### 5.2 Formato dei Messaggi

```python
# Task definition
class Task:
    description: str           # Prompt in linguaggio naturale
    expected_output: str       # Specifica testuale dell'output atteso
    context: List[Task]        # Task di cui usare l'output come contesto
    output_json: Type          # Schema Pydantic per output strutturato (opzionale)
    output_pydantic: Type      # Alternativa: modello Pydantic (opzionale)

# CrewOutput (risultato finale)
class CrewOutput:
    raw: str                   # Output testuale grezzo
    json_dict: dict            # Se output_json specificato
    pydantic: BaseModel        # Se output_pydantic specificato
    tasks_output: List[TaskOutput]
    token_usage: TokenUsage
```

### 5.3 Tipizzazione e Garanzie

| Proprieta | Valore |
|-----------|--------|
| Schema messaggi | Testo naturale + Pydantic opzionale |
| Tipizzazione | OPZIONALE (Pydantic per output) |
| Input/Output | Non tipizzato di default |
| Garanzie formali | NESSUNA |
| Deadlock | Nessuna protezione formale |
| Errori | Gestione a livello LLM, non protocollo |

**Punto debole principale**: La comunicazione inter-agente avviene principalmente attraverso testo
naturale non strutturato. Il Manager LLM deve interpretare l'output di ogni Worker e decidere
cosa delegare. Nessuna verifica di tipo, nessuna garanzia formale di completezza o correttezza.
La tipizzazione Pydantic e opzionale e validata solo sull'output finale, non durante la comunicazione.

---

## PARTE 6: LANGGRAPH (LangChain)

### 6.1 Paradigma: State Machine su Grafo

LangGraph non e un framework di comunicazione inter-agente nel senso classico. E una state machine
dove i "nodi" (che possono essere agenti LLM) leggono e scrivono uno **stato condiviso globale**.
Non esiste messaggistica diretta tra nodi: tutti comunicano attraverso lo stato.

### 6.2 Typed State

```python
# Definizione stato tipizzato
class AgentState(TypedDict):
    messages: Annotated[List[AnyMessage], operator.add]  # reducer: append
    task_queue: List[str]
    current_agent: str
    metadata: dict

# Alternativa con Pydantic per validazione
class AgentState(BaseModel):
    messages: List[AnyMessage] = []
    # validazione ricorsiva automatica
```

**Il contratto di stato** e definito staticamente prima dell'esecuzione. Ogni nodo riceve lo stato
corrente come input e restituisce un update (non lo stato completo). I reducer gestiscono il merge:
`Annotated[List, operator.add]` significa "append alla lista esistente".

### 6.3 Send API per Comunicazione Dinamica

```python
# Nodo che invia messaggi dinamici ad altri nodi
def router_node(state: AgentState) -> List[Send]:
    return [
        Send("worker_a", {"task": "analisi A"}),
        Send("worker_b", {"task": "analisi B"}),
    ]
# Send permette di invocare un nodo con uno stato personalizzato
# Utile per map-reduce: stesso nodo invocato in parallelo con stati diversi
```

### 6.4 Checkpointing e Persistenza

LangGraph salva automaticamente lo stato dopo ogni esecuzione di nodo (checkpointing).
Questo permette:
- Continuazione di conversazioni su invocazioni multiple
- Human-in-the-loop (pausa e ripresa)
- Rollback a stati precedenti

### 6.5 Tipizzazione e Garanzie

| Proprieta | Valore |
|-----------|--------|
| Schema messaggi | TypedDict o Pydantic (tipizzato) |
| Tipizzazione | TIPIZZATO (state schema) |
| Runtime validation | Pydantic (opzionale) |
| Garanzie formali | PARZIALI (reducer semantics) |
| Deadlock | Nessuna protezione formale |
| Ordinamento | Deterministico (topological sort del grafo) |

**Punto debole principale**: Tutto lo stato e globale. Nessun isolamento tra nodi. Un nodo puo
leggere (e scrivere) qualsiasi parte dello stato, anche quella non di sua competenza. Non ci sono
session types che garantiscano che il nodo A possa solo comunicare con il nodo B in un certo ordine.
Il contenuto dei messaggi (tipicamente LangChain Message objects) rimane testo libero.

---

## PARTE 7: MODEL CONTEXT PROTOCOL (MCP) di Anthropic

### 7.1 Scopo e Architettura

MCP NON e un protocollo di comunicazione inter-agente. E un protocollo per la comunicazione
**agente-strumento** (o agente-risorsa). L'ispirazione e il Language Server Protocol (LSP).

**Attori**:
- **Host**: Applicazione LLM (Claude Code, IDEs)
- **Client**: Connettore dentro il Host
- **Server**: Servizio che espone contesto/strumenti

**Features**:
- **Resources**: Dati/contesto per il modello
- **Prompts**: Template di messaggi
- **Tools**: Funzioni eseguibili dal modello
- **Sampling**: Il server puo iniziare comportamenti agentici (inversione di controllo)
- **Roots**: Confini filesystem per il server
- **Elicitation**: Il server richiede informazioni aggiuntive dall'utente

### 7.2 Wire Format

MCP usa **JSON-RPC 2.0** come formato base:

```json
// Request
{"jsonrpc":"2.0","id":"1","method":"tools/call","params":{"name":"search","arguments":{"q":"lean 4"}}}

// Response (success)
{"jsonrpc":"2.0","id":"1","result":{"content":[{"type":"text","text":"risultato..."}]}}

// Notification (no response expected)
{"jsonrpc":"2.0","method":"notifications/progress","params":{"progressToken":"tok1","progress":50}}

// Error
{"jsonrpc":"2.0","id":"1","error":{"code":-32603,"message":"Internal error"}}
```

**Transport Layer**:
- **stdio**: Per integrazioni locali (processo figlio, pipe stdin/stdout)
- **SSE (Server-Sent Events)**: Per integrazioni remote
- **HTTP POST**: Client -> Server per messaggi sincroni

### 7.3 Lifecycle e Capability Negotiation

```
Initialize (capabilities exchange) -> Operation -> Shutdown
```
Durante Initialize, client e server negoziano le capacita supportate. Questo e un form di
capability discovery formale (ma non session types).

### 7.4 Schema Typings

MCP usa TypeScript per definire lo schema canonico (`schema.ts`). Tutte le implementazioni
devono conformarsi a questo schema. Ma il contenuto dei tool calls (gli `arguments`) e un
JSON object non tipizzato (schema validabile ma non verificato formalmente).

| Proprieta | Valore |
|-----------|--------|
| Schema messaggi | JSON-RPC 2.0 + TypeScript schema |
| Tipizzazione | PARZIALMENTE TIPIZZATO |
| Capability negotiation | Si (Initialize phase) |
| Garanzie formali | PARZIALI (lifecycle 3 fasi) |
| Security | Consenso utente obbligatorio (per design) |
| Prompt injection risk | Alto (citato come weakness principale) |

**Punto debole principale**: MCP ha un rischio di prompt injection significativo: i server MCP
possono iniettare contenuto nei messaggi che manipola il comportamento del modello. Il protocollo
non ha meccanismi built-in per verificare l'integrita del contenuto.

---

## PARTE 8: OPENAI AGENTS SDK

### 8.1 Modello di Comunicazione: Handoff

OpenAI Agents SDK usa il concetto di **handoff** per la comunicazione inter-agente. Un handoff
non e un messaggio ma un trasferimento di controllo: l'agente corrente cede l'esecuzione a un
altro agente, passandogli la cronologia conversazionale.

**Meccanismo**: I handoff sono **tool calls** standard. Se il risultato di una tool call e un
oggetto `Agent`, l'SDK interpreta questo come "trasferisci controllo a questo agente".

```python
# Definizione handoff
handoff_to_refund = handoff(
    agent=refund_agent,
    on_handoff=lambda ctx, input: ctx.log(f"Handoff: {input}"),
    input_filter=lambda input: input  # trasforma input se necessario
)

# Il tool si chiama "transfer_to_refund_agent"
# Quando invocato, il sistema fa:
# "Transferred to {agent_name}. Adopt persona immediately."
```

### 8.2 Formato dei Messaggi

La comunicazione avviene attraverso la **conversazione history** (lista di messaggi OpenAI):
```python
[
    {"role": "user", "content": "Voglio un rimborso"},
    {"role": "assistant", "content": "La trasferisco a..."},
    # Il nuovo agente riceve questo history completo
]
```

Non esiste un tipo di messaggio specifico per la comunicazione inter-agente. L'handoff e
implicito nel tipo ritornato dalla tool call.

### 8.3 Tipizzazione e Garanzie

| Proprieta | Valore |
|-----------|--------|
| Schema messaggi | OpenAI Messages API format |
| Tipizzazione | PARZIALE (tool schemas) |
| Handoff mechanism | Tool call con risultato Agent |
| Garanzie formali | NESSUNA |
| Context preservation | Si (history completa) |
| Deadlock | Nessuna protezione formale |

**Punto debole principale**: Il modello a handoff e sequenziale (un agente alla volta). Non c'e
parallelismo nativo tra agenti. Il "contratto" di handoff e solo testuale ("Adopted persona
immediately") senza nessuna verifica formale.

---

## PARTE 9: FIPA ACL (Foundation for Intelligent Physical Agents)

### 9.1 Il Classico Standard - Storia

FIPA-ACL emerge negli anni '90 come primo standard formale per la comunicazione inter-agente.
Basato sulla **Speech Act Theory** (Austin, Searle): ogni messaggio e un "atto linguistico" con
una performativa che specifica l'intento del mittente.

FIPA e stato accettato come standards committee di IEEE nel 2005. Lo standard e rimasto immutato
da allora.

### 9.2 Struttura dei Messaggi

```
(inform
  :sender  (agent-identifier :name agente-1)
  :receiver (agent-identifier :name agente-2)
  :content  "temperature 23.5"
  :language FIPA-SL
  :ontology weather-ontology
  :conversation-id conv-001
  :reply-with msg-001
  :in-reply-to msg-000
)
```

FIPA-ACL definisce **22 performative** (inform, request, query-if, subscribe, propose, accept-proposal,
reject-proposal, cfp, agree, refuse, failure, not-understood, ecc.) con semantica formale definita in
logica modale (FIPA Semantic Language / SL).

**Dimensioni di ogni messaggio**: 200-500 bytes per messaggio (overhead significativo).

### 9.3 Ontologie

FIPA richiede un'**ontologia condivisa** tra comunicanti. Se agente A usa "temperature" e agente B
usa "temp", non c'e comunicazione. Questo era il punto di forza e di debolezza principale.

### 9.4 Rilevanza nel 2026

| Dominio | Status |
|---------|--------|
| Power systems / energie | ATTIVO (IEEE Power & Energy) |
| JADE framework | ATTIVO (supporto FIPA nativo) |
| SARL framework | ATTIVO |
| Robotica distribuita | PARZIALMENTE |
| LLM/AI moderni | PRESSOCHÉ ASSENTE |

FIPA rimane lo standard per certi domini safety-critical (energia, sistemi embedded).
L'adozione nell'ecosistema LLM e quasi nulla perche:
1. LLM non hanno bisogno di ontologie condivise (generano il mapping autonomamente)
2. 22 performative sono troppe per sistemi che usano linguaggio naturale
3. NLIP (Ecma, Dicembre 2025) e esplicitamente progettato per sostituire FIPA nell'era AI

**μACP (Gennaio 2026)** ha dimostrato formalmente che 4 verbi (PING, TELL, ASK, OBSERVE)
sono sufficienti per encodare qualsiasi protocollo FIPA a stati finiti, con messaggi molto piu compatti.

### 9.5 Garanzie Formali

| Proprieta | Valore |
|-----------|--------|
| Schema messaggi | KQML/ACL con ontologia |
| Tipizzazione | FORMALMENTE TIPIZZATO (performative) |
| Garanzie formali | PARZIALI (semantica logica modale) |
| Deadlock | Nessuna protezione pratica |
| Verifica | Teorica, non automatizzata |

**Punto debole principale**: Le garanzie formali di FIPA sono definite in logica modale ma
non sono automaticamente verificabili a runtime. Il sistema richiede un'ontologia condivisa
pre-definita, incompatibile con il dynamic discovery dei sistemi moderni.

---

## PARTE 10: NLIP - Natural Language Interaction Protocol (Ecma, Dicembre 2025)

### 10.1 Nuovo Standard Industriale

ECMA International ha pubblicato 5 standard + 1 technical report il 10 Dicembre 2025
(ECMA-430 attraverso ECMA-434 + TR/113):

- **ECMA-430**: Core NLIP - formato multimodale (testo, structured data, binario, location)
- **ECMA-431**: NLIP su HTTP/HTTPS
- **ECMA-432**: NLIP su WebSocket con CBOR (compact binary)
- **ECMA-433**: NLIP su AMQP
- **ECMA-434**: Agent Security Profiles per NLIP

**Filosofia**: NLIP non richiede un'ontologia condivisa tra agenti comunicanti. I LLM fanno
da traduttore automatico tra le ontologie locali di ciascun agente. Sostituisce le API
hard-coded con un "envelope protocol universale".

**Supporto multimodale nativo**: testo, dati strutturati, binario, location nello stesso messaggio.
Multi-turn conversational exchange human-to-agent e agent-to-agent.

### 10.2 Posizionamento

NLIP si posiziona come la versione "AI-era" di FIPA-ACL: standard formale e aperto per
comunicazione inter-agente, ma basato su linguaggio naturale invece di ontologie condivise.

| Proprieta | Valore |
|-----------|--------|
| Schema messaggi | CBOR (binario compatto) / JSON |
| Tipizzazione | PARZIALMENTE TIPIZZATO |
| Standard body | Ecma International (formale) |
| Garanzie formali | PARZIALI (security profiles) |
| Interoperabilita | Progettato per cross-vendor |

---

## PARTE 11: AGENT NETWORK PROTOCOL (ANP) - Decentralized

### 11.1 Il Protocollo per il Web Aperto

ANP e l'unico protocollo progettato per scenari open-internet senza trust pre-stabilita.
Usa **Decentralized Identifiers (DIDs)** per identita agenti senza registry centrale.

**Stack a 3 layer**:
1. **Identity & Encryption**: did:wba (Web-Based Agent DID su HTTPS), TLS
2. **Meta-Protocol**: Negoziazione runtime del protocollo applicativo
3. **Application**: Business logic specifica

**Agent Description Protocol (ADP)**: Documento JSON-LD pubblicato su `/.well-known/agent-descriptions`
con capacita, protocolli supportati, endpoint di autenticazione.

### 11.2 Discovery

Agenti scoperti via:
- Path standard `/.well-known/agent-descriptions`
- Search agent discovery
- DID resolution

### 11.3 Garanzie e Limiti

| Proprieta | Valore |
|-----------|--------|
| Schema messaggi | JSON-LD con Schema.org |
| Tipizzazione | SEMANTICO (linked data) |
| Identita | DID-based (trustless) |
| Garanzie formali | PARZIALI (DID integrity) |
| Overhead | ALTO (negoziazione runtime) |
| Maturita | BASSA (ecosistema in sviluppo) |

**Punto debole principale**: Alta overhead di negoziazione a runtime. Ecosistema immaturo.
Adozione limitata (Febbraio 2026).

---

## PARTE 12: SESSION TYPES E RICERCA ACCADEMICA

### 12.1 Fondamenti Teorici

I **session types** sono tipi che descrivono il PROTOCOLLO di comunicazione tra processi.
Derivano dalla **logica lineare** (Caires e Pfenning, 2010): un canale di comunicazione
e una "risorsa lineare" che deve essere usata seguendo un protocollo esatto.

```
ServerProtocol = !Request . ?Response . End
ClientProtocol = ?Request . !Response . End
-- Il type checker verifica che Client e Server si "parlino" correttamente
-- Se Client manda due Request senza aspettare Response -> ERRORE A COMPILE TIME
```

**Proprieta garantite dai session types**:
- **Communication safety**: Assenza di errori di comunicazione
- **Session fidelity**: Accordo con il protocollo dichiarato
- **Deadlock-freedom** (per sistemi binari)
- **Progress / Liveness**: Per sistemi multipartite, il type system garantisce che un
  partecipante in attesa di un messaggio lo ricevera
- **Orphan message freedom**: Un messaggio inviato sara letto

### 12.2 Stato della Ricerca 2025-2026

**Dependent session types (TLLC 2025)**: Combinano session types con dependent types per
specificare proprieta dei messaggi scambiati. Permettono di dire non solo "il server manda
una Response" ma "il server manda una Response con status < 400 se il Request era valida".

**CoqPL 2025**: "A Semantic Logical Relation for Termination of Intuitionistic Linear Logic
Session Types" - verifica formale in Coq della terminazione dei protocolli session-typed.

**Frontiers in Computer Science 2025**: "Correct implementation of agent interaction protocols"
- framework per verificare che le implementazioni di protocolli inter-agente siano corrette.

**Stato**: Principalmente accademico. Nessun framework industriale usa session types per
comunicazione inter-agente (2026). Questo e il Gap 5 confermato.

### 12.3 μACP: Il Calcolo Formale per Agenti (Gennaio 2026)

Il paper `arXiv:2601.00219` (Mallick, Chebolu) propone μACP come calcolo formale per la
comunicazione in sistemi resource-constrained.

**4 verbi universali**:
- **PING**: Test di raggiungibilita
- **TELL**: Trasmissione di informazione creduta (era FIPA inform)
- **ASK**: Interrogazione su credenze/capacita (era FIPA request/query)
- **OBSERVE**: Notifica di eventi rilevati (era FIPA subscribe/inform)

**Teorema di completezza**: Questi 4 verbi sono sufficienti per encodare qualsiasi protocollo
FIPA a stati finiti. La traduzione e `τ: FIPA -> μACP` formalmente definita.

**Garanzie provate in TLA+ e Coq**:
- Safety (invarianti)
- Liveness (sotto partial synchrony, dopo GST)
- Boundedness (rispetto dei budget M/B/C/E)
- Consensus feasibility (f < n/2 crash faults)

**Rilevanza per CervellaSwarm**: Il modello PING/TELL/ASK/OBSERVE e un candidato naturale
per la Lingua Universale Fase A, con la possibilita di aggiungere prove formali.

---

## PARTE 13: ANALISI COMPARATIVA

### 13.1 Tabella Comparativa

| Framework | Schema | Tipizzazione | Garanzie Formali | Discovery | Streaming | Maturita |
|-----------|--------|-------------|-----------------|-----------|-----------|---------|
| Claude Code (Task) | Testo | NON TIPIZZATO | NESSUNA | No | No | ALTA |
| AutoGen v0.4 | Pydantic/dataclass | PARZIALE | PARZIALI | No | Si (async) | ALTA |
| A2A (Google+LF) | Proto3/JSON-RPC | PARZIALE | PARZIALI | Agent Card | Si (SSE/gRPC) | MEDIA-ALTA |
| ACP (IBM->A2A) | Multipart MIME | PARZIALE | PARZIALI | Registry | Si | MEDIA |
| CrewAI | Testo+Pydantic opt. | OPZIONALE | NESSUNA | No | No | ALTA |
| LangGraph | TypedDict/Pydantic | TIPIZZATO (state) | PARZIALI | No | No | ALTA |
| MCP (Anthropic) | JSON-RPC 2.0 | PARZIALE | PARZIALI | Static URL | Si (SSE) | ALTA |
| OpenAI SDK | OpenAI Messages | PARZIALE | NESSUNA | No | No | ALTA |
| FIPA ACL | KQML/SL | FORMALMENTE TIPIZZATO | PARZIALI | Directory | No | ALTA (legacy) |
| ANP | JSON-LD | SEMANTICO | PARZIALI | DID/discovery | No | BASSA |
| NLIP (Ecma) | CBOR/JSON | PARZIALE | PARZIALI | Cross-vendor | Si | NUOVA |
| Session Types | Formale | COMPLETAMENTE TIPIZZATO | COMPLETE | N/A | N/A | ACCADEMICA |
| μACP | TLV 4 verbi | FORMALMENTE TIPIZZATO | PROVATE (Coq/TLA+) | PING | No | RICERCA |

### 13.2 Pattern Comuni

**Pattern 1: JSON come lingua franca**
Tutti i protocolli industriali (A2A, ACP, MCP, ANP) usano JSON come formato di scambio.
Nessuno usa binary encoding come default (ANP usa JSON-LD, NLIP offre CBOR opzionale).

**Pattern 2: JSON-RPC 2.0 come base**
A2A, MCP e il vecchio ACP usano tutti JSON-RPC 2.0. Questo converge verso uno standard de facto
per il layer di trasporto, ma JSON-RPC non dice nulla sulla semantica del contenuto.

**Pattern 3: Proto3 come schema canonico**
A2A usa un file `.proto` come source of truth, con bindings JSON/gRPC/REST. E il pattern piu
rigoroso adottato industrialmente (proto3 e tipizzato e ha schema validation).

**Pattern 4: Nessuna garanzia formale di comportamento**
In tutti i framework industriali, la "correttezza" della comunicazione e delegata al LLM e ai
prompt. Nessun framework verifica che l'agente A non possa inviare un messaggio X prima di
aver ricevuto Y.

**Pattern 5: Discovery tramite documento JSON**
Agent Card (A2A), ADP (ANP), Agent Detail (ACP): tutti usano un documento JSON discoverable
via HTTP GET su un path standard. Pattern ispirato a OpenID Connect / OAuth server metadata.

**Pattern 6: Topologie ibride**
- Claude Code: hub-and-spoke puro (niente peer-to-peer)
- AutoGen: direct messaging + broadcast (pubsub)
- LangGraph: stato globale condiviso (blackboard)
- A2A/ACP: peer-to-peer (client/server simmetrici)
- CrewAI: hub-and-spoke gerarchico
- ANP: decentralizzato P2P

**Pattern 7: Convergenza verso A2A**
ACP e stato assorbito da A2A (Agosto 2025). Strands Agents (AWS) implementa A2A.
Questo suggerisce che A2A sta diventando lo standard industriale dominante per comunicazione
inter-agente cross-framework.

### 13.3 I 7 Gap Critici

**Gap 1: NESSUNA verifica formale del comportamento del protocollo**
Tutti i framework industriali delegano la correttezza ai prompt LLM. Un agente puo non
rispondere, rispondere fuori ordine, ignorare messaggi: nessuna protezione.
*Soluzione nota*: Session types, ma nessuno li ha ancora implementati industrialmente.

**Gap 2: Testo libero come contenuto dei messaggi**
Anche dove il frame del messaggio e tipizzato (A2A Parts, AutoGen dataclass), il CONTENUTO
e testo libero. L'interpretazione e demandata al LLM destinatario.
*Soluzione nota*: Dependent session types, refinement types sul contenuto.

**Gap 3: Nessuna garanzia di deadlock-freedom**
Nessun framework industriale garantisce formalmente che il sistema non entri in deadlock.
*Soluzione nota*: Session types binari (provati deadlock-free), Global Types per multipartite.

**Gap 4: Nessuna garanzia di liveness/terminazione**
Un agente puo non terminare mai, attendere indefinitamente, o rispondere in modo utile ma
non aver completato il protocollo previsto.
*Soluzione nota*: Bounded session types, terminazione provata (come CoqPL 2025).

**Gap 5: Assenza di ontologia condivisa verificata**
FIPA richiedeva ontologie condivise (troppo rigido). I framework moderni non ne richiedono
(troppo flessibile). Non esiste uno spazio intermedio: ontologia parziale verificata.
*Soluzione nota*: Dependent types per specificare invarianti parziali senza ontologia completa.

**Gap 6: Osservabilita inter-agente limitata**
Claude Code: tutti gli hook condividono session_id, impossibile tracciare quale subagente
ha prodotto cosa. AutoGen: broadcast exceptions silenziate. LangGraph: nessun isolamento.
*Soluzione nota*: Typed audit log con correlazione causale (vector clocks, session IDs gerarchici).

**Gap 7: Nessun protocollo standard per agenti CervellaSwarm-style**
Nessun protocollo esistente gestisce: agenti con ruoli (Regina/Guardiana/Worker), gerarchia
di autorizzazione, memoria persistente cross-sessione, e contratti verificabili per task routing.
*Soluzione*: Questo e esattamente la Lingua Universale Fase A.

---

## PARTE 14: IMPLICAZIONI PER LINGUA UNIVERSALE FASE A

### 14.1 Cosa Prendere dai Protocolli Esistenti

**Da A2A**:
- Agent Card come standard per capability discovery
- Proto3 come schema canonico + binding multipli
- Task lifecycle formale (stati espliciti)
- Streaming SSE per task lunghi

**Da AutoGen v0.4**:
- Separazione netta: messaggi sono dati puri, no logica
- Pydantic per tipizzazione opzionale
- Direct messaging (accoppiato, errori propagati) vs Broadcast (disaccoppiato, errori silenziati)

**Da LangGraph**:
- Stato tipizzato come contratto condiviso
- Reducer semantics per merge deterministico
- Checkpointing automatico

**Da MCP**:
- Lifecycle in 3 fasi con capability negotiation
- JSON-RPC 2.0 come base

**Da FIPA ACL**:
- Performative types (anche se ridotti - μACP dimostra che 4 bastano)
- Conversation-id per correlazione
- Reply-with / In-reply-to per threading

**Da μACP**:
- 4 verbi minimi: PING, TELL, ASK, OBSERVE
- Resource budget esplicito (M/B/C/E)
- Proofs in TLA+ e Coq come template

### 14.2 Cosa Aggiungere (il Differenziatore)

Il Verified Agent Protocol per CervellaSwarm dovrebbe aggiungere a tutti i precedenti:

1. **Session types per coppie di ruoli**:
   ```
   ReginaToGuardiana = !Task . ?AuditResult . End
   GuardianAToRegina = ?Task . !AuditResult . End
   ```
   Type checker verifica che Regina e Guardiana si parlino nel protocollo corretto.

2. **Refinement types sul contenuto**:
   ```
   -- Un AuditResult deve avere un score tra 0 e 10
   AuditResult = { score: Float | 0.0 <= score <= 10.0, feedback: String }
   ```

3. **Role-based routing formalmente tipizzato**:
   - Solo la Regina puo delegare a Workers
   - Solo Guardiane possono emettere AuditResult
   - Workers non possono comunicare con altri Workers direttamente
   Queste regole verificate staticamente.

4. **Deadlock-freedom per topologie CervellaSwarm**:
   - Il grafo di comunicazione Regina<->Guardiana<->Worker e aciclico
   - Provato deadlock-free per costruzione

5. **Audit log causalmente ordinato**:
   - Vector clocks per correlazione causale tra messaggi
   - Session ID gerarchici (sessione.subagente.taskid)

### 14.3 Raccomandazione Tecnica

**Per Fase A (6-12 mesi)**:

Iniziare con una specifica in **Lean 4** o **Dafny** di un sottoinsieme del protocollo:
- Definire i tipi di messaggio come inductive types
- Specificare il protocollo Regina->Worker come session type semplice
- Provare deadlock-freedom per questo sottoinsieme

Non occorre un nuovo linguaggio. Serve una **libreria di session types in Python** (esistono:
`session-types` per Python/Haskell/Rust) che wrappa la comunicazione tra agenti CervellaSwarm.

**Candidato concreto**:
```python
# Lingua Universale Fase A - Prototipo concettuale
class TaskSession(Protocol):
    # Regina invia Task, attende Result
    @session_type("!Task . ?Result . End")
    async def delegate(self, task: Task) -> Result: ...

class WorkerSession(Protocol):
    # Worker riceve Task, manda Result
    @session_type("?Task . !Result . End")
    async def execute(self, session: TaskSession) -> None: ...
```

---

## SINTESI FINALE

**Status**: COMPLETA
**Fonti consultate**: 28

**5 Bullet sintetici**:
1. Tutti i framework industriali (A2A, CrewAI, Claude Code, OpenAI SDK) usano testo libero o JSON non tipizzato come contenuto dei messaggi. Zero garanzie formali.
2. La convergenza industriale e verso A2A + JSON-RPC 2.0 + Agent Card come discovery. ACP e stato assorbito. E lo standard emergente.
3. Il campo accademico (session types, μACP, Coq/TLA+) ha tutte le soluzioni teoriche ai gap dei sistemi industriali. Il ponte mancante e pratico, non teorico.
4. μACP (Gennaio 2026) prova che 4 verbi (PING/TELL/ASK/OBSERVE) bastano per qualsiasi protocollo FIPA. Questa e la base minima formalmente corretta per un Verified Agent Protocol.
5. Il Gap 7 (nessun protocollo per sistemi gerarchici con ruoli formali, memoria persistente e routing verificato) e completamente aperto. E l'opportunita di CervellaSwarm.

**Raccomandazione**: Adottare il modello PING/TELL/ASK/OBSERVE di μACP come primitivi
della Lingua Universale, aggiungere session types per le coppie di ruoli critiche (Regina/Worker,
Regina/Guardiana), usare Lean 4 per le prime prove formali. Proto3 per il wire format (best practice
industriale A2A). Partire da 3 session types: Regina->Worker, Worker->Regina, Regina->Guardiana.

---

## FONTI

**Protocolli Industriali:**
- [A2A Protocol Specification](https://a2a-protocol.org/latest/specification/)
- [A2A GitHub - a2aproject](https://github.com/a2aproject/A2A)
- [Google Announces A2A Protocol](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)
- [Linux Foundation A2A Launch](https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents/)
- [ACP Joins A2A - LFAI Data](https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/)
- [IBM ACP Overview](https://www.ibm.com/think/topics/agent-communication-protocol)
- [IBM ACP Technical Overview - WorkOS](https://workos.com/blog/ibm-agent-communication-protocol-acp)
- [MCP Specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25)
- [ANP Agent Description Protocol](https://agent-network-protocol.com/specs/agent-description.html)
- [ANP vs MCP Comparison](https://www.agent-network-protocol.com/blogs/posts/mcp-anp-comparison.html)

**Framework Multi-Agent:**
- [AutoGen v0.4 Message and Communication](https://microsoft.github.io/autogen/stable//user-guide/core-user-guide/framework/message-and-communication.html)
- [AutoGen v0.4 Launch Blog](https://devblogs.microsoft.com/autogen/autogen-reimagined-launching-autogen-0-4/)
- [CrewAI Tasks Documentation](https://docs.crewai.com/en/concepts/tasks)
- [CrewAI A2A Agent Delegation](https://docs.crewai.com/en/learn/a2a-agent-delegation)
- [LangGraph State Management 2025](https://sparkco.ai/blog/mastering-langgraph-state-management-in-2025)
- [LangGraph GitHub](https://github.com/langchain-ai/langgraph)
- [OpenAI Agents SDK Handoffs](https://openai.github.io/openai-agents-python/handoffs/)
- [Claude Code Sub-agents](https://code.claude.com/docs/en/sub-agents)
- [Strands Agents Swarm Pattern](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/multi-agent/swarm/)

**Standard e Ricerca:**
- [NLIP Standards Suite - Ecma International](https://ecma-international.org/news/ecma-international-approves-nlip-standards-suite-for-universal-ai-agent-communication/)
- [ECMA-430 NLIP Core](https://ecma-international.org/publications-and-standards/standards/ecma-430/)
- [μACP Formal Calculus - arXiv:2601.00219](https://arxiv.org/abs/2601.00219)
- [Survey Agent Interoperability Protocols - arXiv:2505.02279](https://arxiv.org/html/2505.02279v1)
- [LACP Standardization Urgency - arXiv:2510.13821](https://arxiv.org/pdf/2510.13821)
- [FIPA ACL - Agent Communications Language Wikipedia](https://en.wikipedia.org/wiki/Agent_Communications_Language)
- [Session Types as Linear Logic - Springer](https://link.springer.com/chapter/10.1007/978-3-642-15375-4_16)
- [Deadlock-Free Session Types - Springer](https://link.springer.com/chapter/10.1007/978-3-319-89366-2_5)
- [CoqPL 2025 - Session Types Termination](https://popl25.sigplan.org/details/CoqPL-2025-papers/4/A-Semantic-Logical-Relation-for-Termination-of-Intuitionistic-Linear-Logic-Session-Ty)

---

*Cervella Researcher - CervellaSwarm*
*"Ricerca PRIMA di implementare. Non inventare, studia come fanno i big."*
*"Nulla e complesso - solo non ancora studiato!"*
