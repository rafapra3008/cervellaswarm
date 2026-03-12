# A2A Protocol Technical Research

> **Data:** 2026-03-12 | **Sessione:** 442 | **Agente:** Cervella Researcher
> **Status:** COMPLETA | **Fonti:** 14 consultate

---

## 1. Cos'e A2A Protocol

**Agent2Agent (A2A)** e un protocollo aperto per la comunicazione e interoperabilita tra agenti AI.
Lanciato da Google in aprile 2025, donato alla Linux Foundation in giugno 2025.
Da agosto 2025, l'IBM Agent Communication Protocol (ACP) si e fuso in A2A.
Da dicembre 2025, sia A2A che MCP hanno una casa permanente nell'Agentic AI Foundation (AAIF),
co-fondata da OpenAI, Anthropic, Google, Microsoft, AWS e Block.

**Problema risolto:** Come fanno agenti costruiti da vendor diversi, con framework diversi,
a collaborare senza condividere memoria, tool o contesto interno?

**Analogia:** Se MCP e il "cavo USB" (agente-tool), A2A e il "TCP/IP" (agente-agente).

---

## 2. Architettura Tecnica

### Stack protocollare

```
Transport: HTTP/HTTPS + SSE (streaming) + gRPC (nuovo in v0.3.x)
Encoding:  JSON-RPC 2.0
Discovery: Agent Card a /.well-known/agent-card.json
Auth:      API Key | Bearer | OAuth2 | OIDC | mTLS
```

### Ruoli

- **Client Agent**: formula task e li delega
- **Remote Agent**: riceve, esegue, risponde

### Agent Card (formato JSON)

Il documento di scoperta pubblicato da ogni agente server:

```json
{
  "name": "nome-agente",
  "description": "...",
  "url": "https://host/",
  "version": "1.0.0",
  "provider": { "organization": "...", "url": "..." },
  "capabilities": {
    "streaming": true,
    "pushNotifications": true,
    "stateTransitionHistory": false
  },
  "skills": [
    {
      "id": "skill-id",
      "name": "Nome Skill",
      "description": "...",
      "inputModes": ["text"],
      "outputModes": ["text", "data"],
      "examples": ["esempio query"]
    }
  ],
  "securitySchemes": { "apiKey": { "type": "apiKey", "in": "header" } }
}
```

### Task Lifecycle

```
working -> completed
        -> failed
        -> canceled
        -> rejected
        -> input-required  (multi-turn: serve altro input)
        -> auth-required   (richiede autenticazione)
```

### 11 Metodi JSON-RPC

| Metodo | Scopo |
|--------|-------|
| SendMessage | Inizia interazione |
| SendStreamingMessage | Con streaming SSE |
| GetTask | Recupera stato/artefatti |
| ListTasks | Elenca tasks con filtri |
| CancelTask | Cancella task |
| SubscribeToTask | Streaming updates |
| CreateTaskPushNotificationConfig | Configura webhook |
| GetTaskPushNotificationConfig | Legge config webhook |
| ListTaskPushNotificationConfigs | Elenca configs |
| DeleteTaskPushNotificationConfig | Elimina config |
| GetExtendedAgentCard | Card autenticata |

---

## 3. Requisiti Tecnici per Implementazione

### Python SDK (ufficiale)

```bash
pip install a2a-sdk
# oppure con extras:
pip install "a2a-sdk[http-server,grpc,telemetry]"
```

**Versione Python richiesta:** 3.10+

**Versione SDK:** v0.3.25 (10 marzo 2026) - spec v0.3.0

**Extra disponibili:**
- `http-server`: FastAPI/Starlette
- `grpc`: supporto gRPC
- `telemetry`: OpenTelemetry tracing
- `encryption`: cifratura dati
- `sql`: driver DB (PostgreSQL, MySQL, SQLite)

**Metriche maturita SDK:**
- 44 release totali
- 79 contributor
- 720+ progetti dipendenti
- Apache 2.0

### Struttura minima server A2A

Circa 100-120 righe Python (inclusi setup, agent, runner, async loop).
Componenti chiave: AgentCard, TaskHandler, A2AServer.

### Dipendenze indirette

- Starlette/FastAPI per HTTP server
- httpx per client HTTP
- Pydantic per validazione dati
- grpcio (opzionale, per gRPC transport)

---

## 4. A2A vs MCP: Confronto e Complementarita

### Differenza fondamentale

| Dimensione | MCP | A2A |
|------------|-----|-----|
| Asse | Verticale (agente->tool) | Orizzontale (agente->agente) |
| Stato | Stateless (protocollo) | Stateful (task lifecycle) |
| Discovery | No nativo | Agent Card standard |
| Focus | Tool/resource access | Task delegation |
| Design | Consumer AI tools | Enterprise multi-agent |
| Maturita | Dominante (community) | Crescente (enterprise) |

### Architettura emergente a 3 livelli (2026)

```
Layer 3: A2A  -->  Agent-to-Agent coordination
Layer 2: MCP  -->  Individual agent-to-tool connections
Layer 1: Web  -->  Structured web access
```

### Sono complementari, non rivali

Un agente che riceve un task via A2A puo usare MCP internamente per accedere
ai suoi tool. Il confine e chiaro: A2A = "chi delega a chi", MCP = "quali tool uso".

### Status community

MCP ha dominato il mindshare dei developer indie (piu semplice, piu immediato).
A2A ha piu trazione enterprise (100+ aziende, incluse AWS, Microsoft, Cisco).
La convergenza nell'AAIF (dic 2025) suggerisce coesistenza lunga.

---

## 5. Limiti Tecnici e Maturita

### Limiti architetturali (enterprise scale)

1. **N-squared connectivity**: 50 agenti = 1200+ connessioni dirette
2. **Tight coupling**: ogni agente conosce endpoint e auth degli altri
3. **No orchestration built-in**: serve custom workflow engine per coordination
4. **State management**: HTTP stateless vs task long-running (giorni)
5. **Single channel response**: risultati tornano solo via request originale
6. **Authorization creep**: ogni agente deve reimporre permessi indipendentemente

### Maturita generale

- Protocollo: spec v0.3.0, stabile ma breaking changes possibili
- SDK Python: v0.3.25, active maintenance (release ogni settimana circa)
- Governance: Linux Foundation (AAIF) = buon segnale stabilita
- Produzione: testato da enterprise (Salesforce, SAP, ServiceNow) ma ancora early-stage
- Features mancanti: no skill I/O schema machine-readable, no "invoke skill X" primitive

### Breaking changes policy

Per extensions: nuova URI obbligatoria in caso di breaking change.
Per il core: changelog disponibile su GitHub, ma nessuna promessa di LTS ancora.

---

## 6. Implementazioni di Riferimento

### Chi lo usa

- **Google ADK**: integrazione nativa A2A (agent deployment su Cloud Run/Agent Engine)
- **LangGraph**: A2A endpoint per agents LangChain
- **Pydantic AI**: FastA2A library (ASGI, framework-agnostic)
- **AWS Strands 1.0**: supporto nativo A2A per multi-agent swarm
- **Amazon Bedrock AgentCore**: protocollo A2A per agent communication
- **Cisco Agentgateway**: gateway per MCP+A2A
- **LangSmith**: A2A server endpoint per agents

### Pattern architetturale tipico

```
Orchestrator Agent (Regina/Supervisor)
    |-- A2A --> Specialist Agent 1 (usa MCP tools)
    |-- A2A --> Specialist Agent 2 (usa MCP tools)
    |-- A2A --> Specialist Agent 3 (usa MCP tools)
```

Ogni specialist e opaco: l'orchestratore non sa come funziona internamente,
sa solo cosa puo fare (dall'Agent Card) e come delegare (A2A task).

---

## 7. Effort POC con CervellaSwarm

### Scenario POC minimo

Esporre 1-2 agenti CervellaSwarm come A2A server (es. Ricercatrice, Guardiana)
e creare un client A2A per la Regina che li chiami.

### Effort stimato

| Task | Effort |
|------|--------|
| Setup dipendenze + Agent Card | 2-3 ore |
| A2A Server wrapper per 1 agente | 3-4 ore |
| A2A Client nella Regina | 2-3 ore |
| Test end-to-end + smoke tests | 3-4 ore |
| Documentazione + review | 1-2 ore |
| **Totale POC** | **~12-16 ore (1-2 sessioni)** |

### Considerazioni specifiche CervellaSwarm

**VANTAGGIO**: I nostri agenti sono gia specializzati con interfacce chiare.
Le Agent Card scriverebbero facilmente le nostre skills (ricerca, audit, coding, etc.).

**SFIDA 1**: La comunicazione attuale Regina->Worker e via Claude Task tool (subprocess).
A2A richiederebbe agenti come server HTTP separati, non subprocess.

**SFIDA 2**: Il modello attuale e sincrono (Task tool blocca). A2A e asincrono con
streaming. Cambio architetturale non banale.

**SFIDA 3**: Il valore attuale di A2A e principalmente con agenti di vendor DIVERSI.
Intra-swarm (tutti Cervelle) il protocollo aggiunge overhead senza beneficio immediato.

### Quando ha senso per noi?

A2A ha senso per CervellaSwarm quando:
1. Vogliamo esporre agenti a sistemi ESTERNI (es. un cliente usa la Ricercatrice)
2. Vogliamo integrare agenti di terzi nel nostro swarm (es. un agente Salesforce)
3. Costruiamo CervellaLang 1.0 come linguaggio interoperabile con altri sistemi AI

**NON ha senso ora** per la comunicazione interna Regina<->Worker (il Task tool e piu semplice).

---

## Sintesi (5 bullet)

- A2A e il protocollo standard per agenti di VENDOR DIVERSI che collaborano; non e un sostituto dei pattern interni
- Spec v0.3.0, SDK Python v0.3.25 (mar 2026), attivamente mantenuto, Python 3.10+ richiesto
- Complementare a MCP: MCP = agente->tool, A2A = agente->agente; architettura ottimale usa entrambi
- Limiti reali: N-squared connections, no built-in orchestration, nessuna promessa LTS ancora
- Per CervellaSwarm: valore futuro (interoperabilita esterna), non immediato (overhead inutile intra-swarm)

---

## Raccomandazione

**MONITOR, non implementare ora.**

Aggiornare subroadmap E.3 con decisione:
- A2A studio COMPLETATO
- POC rinviato a FASE E.6 (CervellaLang 1.0) dove interoperabilita esterna diventa rilevante
- Prerequisito POC: avere almeno 1 use case concreto di integrazione con sistema esterno

Azione concreta per ora: aggiungere A2A come "interfaccia esterna supportata" nel design
di CervellaLang 1.0 (ogni agente CervellaLang espone automaticamente Agent Card).

---

## Fonti (14)

1. [A2A Protocol Specification](https://a2a-protocol.org/latest/specification/)
2. [Announcing A2A - Google Developers Blog](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)
3. [A2A Protocol GitHub](https://github.com/a2aproject/A2A)
4. [A2A Python SDK GitHub](https://github.com/a2aproject/a2a-python)
5. [Google Cloud A2A Upgrade](https://cloud.google.com/blog/products/ai-machine-learning/agent2agent-protocol-is-getting-an-upgrade)
6. [MCP vs A2A - Clarifai](https://www.clarifai.com/blog/mcp-vs-a2a-clearly-explained)
7. [MCP vs A2A 2026 - DEV Community](https://dev.to/pockit_tools/mcp-vs-a2a-the-complete-guide-to-ai-agent-protocols-in-2026-30li)
8. [A2A Enterprise Limitations - HiveMQ](https://www.hivemq.com/blog/a2a-enterprise-scale-agentic-ai-collaboration-part-1/)
9. [What happened to A2A - fka.dev](https://blog.fka.dev/blog/2025-09-11-what-happened-to-googles-a2a/)
10. [Linux Foundation Launches A2A Project](https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents/)
11. [Practical A2A Guide - DEV Community](https://dev.to/composiodev/a-practical-guide-to-agent-to-agent-a2a-protocol-31fd)
12. [IBM Think - What is A2A](https://www.ibm.com/think/topics/agent2agent-protocol)
13. [Agent Discovery - A2A Protocol](https://a2a-protocol.org/latest/topics/agent-discovery/)
14. [MCP and A2A - Cisco Blogs](https://blogs.cisco.com/ai/mcp-and-a2a-a-network-engineers-mental-model-for-agentic-ai)

---

*Cervella Researcher - CervellaSwarm S442*
<!-- COSTITUZIONE-APPLIED: SI -->
