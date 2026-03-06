# Session Memory - Competitor Analysis for cervellaswarm-session-memory
**Data**: 2026-02-19
**Status**: COMPLETA
**Fonti**: 20 consultate
**Autore**: Cervella Researcher - S373

---

## Sintesi Esecutiva

Nessun competitor offre un sistema di memoria che sia simultaneamente:
plaintext/git-native, zero-dipendenze-cloud, compliance-ready, multi-progetto nativo,
e template-driven. I gap identificati sono reali e difendibili.

**Gap critico confermato**: I sistemi esistenti richiedono tutti un database
(vettoriale o SQL) + un modello di embedding per funzionare. Zero soluzioni usano
Markdown-on-disk come formato primario con git come audit trail nativo.

---

## 1. Competitor Analysis Dettagliata

---

### 1.1 Claude Code Session Memory (Anthropic, 2026)

**Disponibile da**: v2.0.64 (late 2025), visibile da v2.1.30 (Feb 2026)

**Architettura**:
- File-based ma formato proprietario (structured Markdown automatico)
- Storage: `~/.claude/projects/<project-hash>/<session-id>/session-memory/summary.md`
- CLAUDE.md: file scritto dall'utente, caricato intero a ogni sessione
- MEMORY.md: note scritte da Claude, prime 200 righe iniettate nel system prompt
- Auto-compaction: ogni ~5.000 token o 3 tool calls

**API pubblica**: NESSUNA. Sistema completamente automatico e opaco.

**Formato stato**: Structured Markdown (auto-generato, non user-controlled)

**CLI**: Nessuna. Solo `/remember` per promuovere patterns a CLAUDE.md.

**Setup**: Zero config. Automatico se hai Claude Pro/Max.

**Dipendenze**: Nessuna (solo abbonamento Anthropic)

**Limiti critici**:
- Solo Claude Pro/Max su API nativa (NO Bedrock, NO Vertex, NO Foundry)
- Zero controllo utente su cosa viene memorizzato
- Non cross-project (ogni repo ha memoria separata)
- Non condivisibile tra sessioni parallele (swarm)
- Non auditabile (non vedi cosa Claude ha memorizzato senza leggere files nascosti)
- Summary lossy: perde dettagli precisi dopo compact multipli

**Score setup**: 5 min (automatico)

**Il nostro vantaggio**: SNCP e esplicito, human-readable, user-controlled, cross-project,
condivisibile tra agenti paralleli, auditabile, funziona anche senza abbonamento Pro.

---

### 1.2 CrewAI Memory System

**Fonte**: https://docs.crewai.com/en/concepts/memory

**Architettura** (sistema unificato, aggiornato 2025):
- Backend default: LanceDB in `./.crewai/memory/`
- Embedding model richiesto (default: OpenAI text-embedding-3-small)
- LLM per analisi dei contenuti (default: gpt-4o-mini)
- Composite scoring: semantic similarity + recency + importance

**Tipi di memoria**:
- Short-term: ChromaDB (vecchia API) / LanceDB (nuova API) - contesto sessione corrente
- Long-term: SQLite3 (`long_term_memory_storage.db`) - risultati task cross-sessione
- Entity: RAG per tracciare entita (persone, luoghi, concetti)

**API pubblica**:
```python
crew = Crew(memory=True, ...)  # abilita tutto
memory.remember(content, scope, source)
memory.recall(query, limit, depth)
memory.extract_memories(raw_text)
memory.scope(path) / memory.slice(scopes)
memory.reset()
```

**Formato stato**: LanceDB (binario) + SQLite (binario). Non human-readable.

**CLI**: Nessuna dedicata alla memory.

**Setup**: 5-10 min se usi OpenAI. 15-30 min con Ollama locale. Problemi frequenti
con embedding dimension mismatch tra run diverse.

**Dipendenze**: lancedb, sentence-transformers o openai, chromadb (legacy), sqlalchemy

**Limiti critici**:
- Richiede embedding model (costo o setup locale)
- Formato binario: non human-readable, non git-friendly
- Memory content inviato a LLM esterno per analisi (privacy issue)
- Dimension mismatch bug documentato su GitHub (#2464)
- Long-term memory buggy per molti utenti (GitHub issue #1222)
- Non multi-progetto nativo
- Setup Ollama per privacy = 30+ min

**Score setup**: 10-30 min (dipende da embedding provider)

---

### 1.3 AutoGen Memory (Microsoft)

**Fonte**: https://microsoft.github.io/autogen/stable//user-guide/agentchat-user-guide/memory.html

**Architettura**:
- Protocol-based: `Memory` interface con `add`, `query`, `update_context`, `clear`, `close`
- Il framework inietta automaticamente memoria nel context dell'agente prima di ogni task

**Backend disponibili**:
- `ListMemory`: lista cronologica in-memory (solo sessione corrente, perde tutto a restart)
- `ChromaDBVectorMemory`: vector DB con `persistence_path` per persistenza
- `RedisMemory`: Redis per deployment distribuiti
- `Mem0Memory`: integrazione con Mem0.ai (cloud o locale)

**API pubblica**:
```python
memory = ChromaDBVectorMemory(persistence_path="./memory")
agent = AssistantAgent(..., memory=[memory])
# No explicit save/load: automatico via add() e query()
memory.add(content)
memory.query(context)
memory.clear()
```

**Formato stato**: Vettori binari (ChromaDB) o Redis. Non human-readable.

**CLI**: Nessuna.

**Setup**:
- ListMemory: 0 min (no persistenza)
- ChromaDB: 5-10 min + SentenceTransformer o OpenAI embeddings
- Redis: 15+ min (Redis server running)

**Limiti critici**:
- AutoGen Studio 0.4: ogni sessione parte da zero, nessun access a history precedente
- ChromaDB: richiede embedding model (costo o setup locale)
- Redis: infrastruttura aggiuntiva richiesta
- Non multi-progetto
- Non git-friendly
- Qualita dipende da chunking e tuning parametri (score threshold, k)
- Roadmap persistenza in GitHub issue #2358 (ancora aperta)

**Score setup**: 10-15 min per ChromaDB (senza Redis)

---

### 1.4 LangGraph Checkpointing

**Fonte**: https://docs.langchain.com/oss/python/langgraph/persistence

**Architettura**:
- Checkpoint-based: salva stato del grafo a ogni "super-step"
- Thread model: ogni `thread_id` = una conversazione/sessione
- Cross-thread memory richiede `Store` interface separata

**Backend disponibili**:
- In-memory (dev only, perde tutto)
- SQLite (via `SqliteSaver`)
- PostgreSQL (via `PostgresSaver` - produzione)
- DynamoDB + S3 (AWS, payload > 350KB su S3)
- Couchbase, MongoDB, Redis (community checkpointers)

**API pubblica**:
```python
checkpointer = SqliteSaver.from_conn_string("./state.db")
graph = workflow.compile(checkpointer=checkpointer)
graph.invoke(inputs, config={"configurable": {"thread_id": "session-1"}})
# Time travel:
graph.get_state(config)
graph.update_state(config, new_values)
graph.get_state_history(config)
```

**Formato stato**: SQLite/PostgreSQL (binario, JSON serializzato). Non human-readable nativamente.

**CLI**: Nessuna.

**Setup**:
- SQLite: 5 min
- PostgreSQL: 20+ min (server + config)
- LangGraph Platform (hosted): signup + credit card

**Features uniche**: Time travel (rollback a checkpoint precedente), human-in-the-loop.

**Limiti critici**:
- Cross-session (cross-thread) richiede Store separato: "checkpointers alone cannot share information across threads"
- PostgreSQL per produzione = infrastruttura pesante
- LangGraph Platform (hosted) = costo mensile
- Fortemente accoppiato all'ecosistema LangChain
- Non human-readable
- Non git-friendly
- Complessita alta: "graph nodes + edges" model

**Score setup**: 5 min (SQLite locale) / 20+ min (PostgreSQL) / 30 min (LangGraph Platform)

---

### 1.5 LangMem (LangChain SDK)

**Fonte**: https://langchain-ai.github.io/langmem/

**Architettura** (rilasciato Febbraio 2026):
- Due layer: Core API (stateless, funziona con qualsiasi storage) + LangGraph Integration (stateful)
- Due modalita: Hot Path (real-time, in conversazione) + Background (async, estrae da conversazioni passate)

**Tipi di memoria**:
- Episodic: ricorda interazioni specifiche passate (few-shot examples distillati)
- Procedural: istruzioni generalizzate salvate come updates al system prompt
- Semantic: fatti e conoscenze estratte

**API pubblica**:
```python
from langmem import create_manage_memory_tool, create_search_memory_tool
manage_tool = create_manage_memory_tool(namespace=("user", user_id))
search_tool = create_search_memory_tool(namespace=("user", user_id))
# Background:
from langmem import create_memory_store_manager
manager = create_memory_store_manager("anthropic:claude-3-5-haiku-latest", ...)
```

**Storage backend**:
- InMemoryStore (dev, perde tutto a restart)
- AsyncPostgresStore (produzione)
- Qualsiasi LangGraph BaseStore-compatible

**Formato stato**: JSON in PostgreSQL. Non human-readable.

**CLI**: Nessuna.

**Setup**: 5 min (in-memory) / 30+ min (PostgreSQL per persistenza reale)

**Limiti critici**:
- "Memories will be lost on restart" con InMemoryStore
- Produzione richiede PostgreSQL obbligatoriamente
- Fortemente accoppiato a LangGraph/LangChain
- Richiede LLM per estrazione memoria (costo API)
- Nessuna CLI standalone

**Score setup**: 30+ min per persistenza reale (PostgreSQL)

---

### 1.6 Mem0 (formerly MemGPT memory layer)

**Fonte**: https://mem0.ai / https://docs.mem0.ai

**Architettura**:
- Memory orchestration layer tra agenti e storage
- Dual-storage: vector store (embedding search) + SQLite (history/audit)
- Graph layer opzionale per entity relationships

**Tipi di memoria**:
- User memory: persiste cross-sessione per utente specifico
- Session memory: contesto singola conversazione
- Agent memory: specifico a istanza agente

**API pubblica**:
```python
from mem0 import Memory, MemoryClient
m = Memory()  # self-hosted
# oppure:
client = MemoryClient(api_key="...")  # cloud
m.add("text", user_id="user1", agent_id="agent1")
m.search("query", user_id="user1")
m.get_all(user_id="user1")
m.delete(memory_id)
```

**Storage backend** (24+ opzioni):
- Default locale: Qdrant in `/tmp/qdrant/` + SQLite history
- Qdrant, Chroma, Pinecone, PostgreSQL (pgvector), MongoDB, Milvus, ...
- Cloud: managed Mem0 Platform (nessun setup infrastruttura)

**Formato stato**: Vettori binari. Non human-readable.

**CLI**: Nessuna standalone. OpenMemory MCP server per Claude Desktop.

**Setup**:
- Cloud (Mem0 Platform): 5 min (signup + API key)
- Self-hosted default (Qdrant locale): 10 min
- Self-hosted production (PostgreSQL + pgvector): 30+ min

**Pricing cloud**: Non pubblico ufficialmente. Raised $24M (Oct 2025).

**Performance**: 26% accuracy boost vs OpenAI memory, 91% lower p95 latency.

**Limiti critici**:
- Cloud = dati sensibili su infrastruttura terza
- Self-hosted = Qdrant da installare e mantenere
- Non human-readable (vettori)
- Non git-friendly
- OpenMemory MCP: ancora in early access
- Probabilistic retrieval: non deterministico

**Score setup**: 5 min (cloud) / 10-30 min (self-hosted)

---

### 1.7 Zep (Knowledge Graph Memory)

**Fonte**: https://www.getzep.com / https://blog.getzep.com/announcing-a-new-direction-for-zeps-open-source-strategy/

**Architettura**:
- Bi-temporal knowledge graph (event time + ingestion time)
- Powered by Graphiti (open source, Apache 2.0)
- Estratura relazioni e fatti automaticamente dalle conversazioni
- Quando fatti cambiano, quelli vecchi vengono invalidati (temporal reasoning)

**Tipi di memoria**:
- Conversational history
- Extracted entities + relationships
- Temporal facts (con validita temporale)

**API pubblica**:
```python
zep = Zep(api_key="...")  # cloud
zep.memory.add(session_id, messages=[...])
zep.memory.get(session_id)
zep.graph.search(query)
zep.user.add(user_id="user1")
```

**Storage backend**:
- Cloud (Zep Cloud): managed, <200ms latency, SOC2 Type 2 / HIPAA
- Self-hosted OSS: richiede Neo4j/Falkor/Neptune + OpenSearch + LLM infrastruttura

**Formato stato**: Graph database (binario). Non human-readable.

**CLI**: Nessuna.

**Setup**:
- Cloud: 10 min
- Self-hosted: 60+ min (Neo4j + OpenSearch + LLM setup)

**IMPORTANTE**: Community Edition DEPRECATA (Maggio 2025). Solo Graphiti (framework graph)
rimane open source senza infrastruttura cloud. Zep OSS richede infrastruttura pesante.

**Limiti critici**:
- Community Edition deprecata: di fatto richiede cloud per uso pratico
- Self-hosted = infrastruttura enterprise (Neo4j, OpenSearch)
- Cloud = compliance issue per dati sensibili
- Altissima complessita di setup self-hosted
- Non human-readable
- Non git-friendly

**Score setup**: 10 min (cloud) / 60+ min (self-hosted)

---

### 1.8 Letta / MemGPT (Stateful Agents)

**Fonte**: https://www.letta.com/blog/letta-code

**Architettura**:
- Stateful agents con memoria persistente
- MemGPT pattern: LLM gestisce la propria memoria come tool calls
- Nuova feature (Feb 12, 2026): Context Repositories con git-based versioning

**Tipi di memoria**:
- Core memory: in-context sempre
- Archival memory: external searchable storage
- Recall memory: conversation history

**API pubblica**: Server-based (Letta Server + SDK)

**Formato stato**: JSON + database interno. Context Repositories: git-versioned files (novita 2026)

**CLI**: `letta server` + web dashboard

**Setup**: 15-30 min (Docker o pip install letta)

**Limiti critici**:
- Server richiesto (non libreria standalone)
- Context Repositories (git-versioning) in early development (annunciato Feb 2026)
- Complessita alta: agent loop + server + client
- Non multi-progetto nativo nel senso SNCP

**Score setup**: 15-30 min

---

## 2. Tabella Comparativa

| Sistema | Formato Stato | Git-friendly | CLI | Setup Time | Cloud Req | Multi-Prog | Audit Trail | Deps |
|---------|---------------|--------------|-----|------------|-----------|------------|-------------|------|
| **Claude Code Session Memory** | Markdown auto | Parziale | No | 0 min (Pro only) | Si (Pro) | No | No | Pro sub |
| **CrewAI Memory** | LanceDB binario | No | No | 10-30 min | No (locale) | No | No | lancedb + embedding |
| **AutoGen Memory** | ChromaDB/Redis | No | No | 10-15 min | Opzionale | No | No | chromadb + embeddings |
| **LangGraph Checkpoint** | SQLite/PG | No | No | 5-20 min | Opzionale | No | Parziale | sqlalchemy |
| **LangMem** | JSON in PG | No | No | 30+ min | No (PG req) | No | No | postgres |
| **Mem0** | Qdrant vettori | No | No | 5-30 min | Opzionale | No | Parziale (SQLite) | qdrant |
| **Zep** | Neo4j graph | No | No | 10-60 min | Raccomandato | No | Parziale | neo4j + opensearch |
| **Letta** | JSON + Server | Emergente | Si (server) | 15-30 min | No (server) | No | No | server stack |
| **SNCP (nostro)** | **Markdown** | **Si (nativo)** | **Si (sncp-init)** | **< 5 min** | **No** | **Si (nativo)** | **Si (git history)** | **Zero** |

---

## 3. Analisi Gap Specifici

### Gap #1: Human-Readable Format (NESSUNO lo fa)

Tutti i competitor usano formati binari o semi-binari (vector embeddings, SQLite blob,
Neo4j graph). Solo Claude Code usa Markdown, ma in modo opaco e non controllabile.

**SNCP**: PROMPT_RIPRESA.md e NORD.md sono plaintext Markdown. Un umano li legge
direttamente. Un dev li modifica con `vim`. Git fa diff tra versioni.

### Gap #2: Git as Native Audit Trail (NESSUNO lo fa nativamente)

Nessun competitor usa git come sistema di versioning nativo per la memoria.
LangGraph ha "time travel" via checkpoint IDs nel DB. Letta ha appena annunciato
Context Repositories con git (Feb 2026, work in progress).

**SNCP**: ogni `git commit` e un punto di audit. `git log .sncp/` mostra l'intera
storia delle decisioni. `git diff HEAD~1 PROMPT_RIPRESA.md` mostra cos'e cambiato.
EU AI Act Article 19 (high-risk AI: logs per almeno 6 mesi) -> SNCP e compliant
by default con git history.

### Gap #3: Zero Cloud Dependencies (NESSUNO e veramente zero-deps)

- CrewAI: richiede embedding model (OpenAI API o Ollama locale)
- AutoGen: ChromaDB + sentence-transformers
- LangMem: PostgreSQL per persistenza reale
- Mem0: Qdrant o cloud managed
- Zep: Neo4j + OpenSearch (o cloud)
- Letta: server stack completo

**SNCP**: dipendenze Python = ZERO. `mkdir .sncp && touch PROMPT_RIPRESA.md`.

### Gap #4: Multi-Progetto Nativo (NESSUNO lo ha)

Tutti i sistemi attuali sono single-project o single-agent. Multi-project richiede
istanze separate (diversi DB, diverse collection, diversi server).

**SNCP**: `.sncp/progetti/` con subdirectory per ogni progetto. Un singolo checkout
del repo CervellaSwarm gestisce cervellaswarm/, miracollo/, contabilita/ etc.
Context injection hook sa automaticamente quale progetto caricare dal CWD.

### Gap #5: Template-Driven (SOLO SNCP lo ha)

Nessun competitor ha il concetto di template strutturato per la memoria.
CrewAI "ricorda" frammenti. LangGraph "checkpointa" stati arbitrari.
Mem0 "estrae" fatti da conversazioni.

**SNCP**: PROMPT_RIPRESA ha una struttura definita (sessione, decisioni con perche,
prossimi step). Un developer nuovo legge il PROMPT_RIPRESA e sa esattamente
cosa e stato fatto e perche. I templates F2.2 (cervellaswarm-agent-templates)
integrano gia questa struttura.

---

## 4. Analisi Debolezze SNCP (Honesty First)

Per costruire il package correttamente, e importante conoscere i nostri limiti:

| Debolezza | Competitor che la risolve meglio | Come mitigarla in F3 |
|-----------|----------------------------------|----------------------|
| **Semantic search** mancante (SNCP e keyword-only) | Mem0, Zep, LangGraph | Aggiungere `cervella-search` da code-intelligence package come optional enhancement |
| **No automatic extraction** (un umano deve scrivere PROMPT_RIPRESA) | Mem0, LangMem (background extraction) | SessionEnd hook che auto-aggiorna campi chiave |
| **Scale**: difficile con 100+ sessioni storiche | LangGraph (time travel strutturato) | archivio/ directory + quality-check script |
| **No entity tracking** (non traccia persone/concetti automaticamente) | CrewAI entity memory, Zep knowledge graph | Opzionale: SQLite per analytics (F3.2) |
| **No probabilistic recall** (e tutto-o-niente: leggi file o non leggi) | Tutti i sistemi vector-based | Accettabile per compliance/auditabilita |

---

## 5. Architettura Raccomandata per F3 Package

Basato sull'analisi dei competitor, proponiamo questa architettura per
`cervellaswarm-session-memory`:

```
packages/session-memory/
├── src/cervellaswarm_session_memory/
│   ├── __init__.py
│   ├── sncp_init.py          # cervella-sncp init <project>
│   ├── quality_check.py      # cervella-sncp check (lint PROMPT_RIPRESA)
│   ├── audit_secrets.py      # cervella-sncp audit (trova secrets)
│   ├── context_loader.py     # carica PROMPT_RIPRESA per iniezione
│   ├── session_logger.py     # append entry a work log
│   ├── template_engine.py    # render template PROMPT_RIPRESA/NORD.md
│   └── cli.py                # entry point: cervella-sncp
```

**API core** (ispirata da Mem0 ma file-based):
```python
sncp = SessionMemory(project="cervellaswarm", base_dir=".sncp")
sncp.init()                          # crea struttura directory
sncp.load()                          # legge PROMPT_RIPRESA corrente
sncp.save(section="decisioni", content="...")  # aggiorna sezione
sncp.log_event(event_type, details)  # appende a work log
sncp.audit()                         # check secrets + quality
sncp.export_context()                # formato per SubagentStart
```

**CLI target** (< 5 min setup come da criterio F2):
```bash
cervella-sncp init my-project        # crea .sncp/progetti/my-project/
cervella-sncp check                  # lint PROMPT_RIPRESA
cervella-sncp audit                  # security scan
cervella-sncp log "decisione X per Y"  # appende entry
cervella-sncp export                 # stdout JSON per context injection
```

**ZERO dipendenze**: solo stdlib Python (pathlib, json, re, datetime).
Compatibile con F2.1 (agent-hooks context_inject.py usa gia questo pattern).

---

## 6. Raccomandazioni per Differenziazione nel README

Basato sull'analisi, la tabella comparativa del README dovrebbe evidenziare:

| Feature | SNCP | CrewAI | LangGraph | Mem0 | Zep |
|---------|------|--------|-----------|------|-----|
| Human-readable format | Yes (Markdown) | No (binary) | No (SQLite) | No (vectors) | No (graph DB) |
| Git-native audit trail | Yes (native) | No | No | No | No |
| Zero cloud dependencies | Yes | No* | No** | No*** | No**** |
| Multi-project native | Yes | No | No | No | No |
| Template-driven structure | Yes | No | No | No | No |
| Setup time | < 5 min | 10-30 min | 5-30 min | 5-30 min | 10-60 min |
| Compliance-ready | Yes (git log) | Partial | Partial | Partial | Partial (cloud) |
| Works offline | Yes | No* | Yes** | No*** | No**** |

*richiede embedding model (OpenAI API o Ollama)
**SQLite locale OK, ma LangGraph Platform per features avanzate
***default usa Qdrant locale ma richiede installazione
****Community Edition deprecata, cloud raccomandato

**Honest note** (come da nostro pattern): "SNCP doesn't do semantic similarity
search or automatic memory extraction. It's deterministic and human-curated.
If you need probabilistic recall across thousands of memories, consider
combining SNCP with cervellaswarm-code-intelligence."

---

## 7. Positioning Statement

> "cervellaswarm-session-memory is the only AI agent memory system where every
> decision is a git commit, every state is human-readable Markdown, and every
> audit trail is a `git log` command away. No vector databases. No cloud services.
> No embedding models. Just files and git."

---

## Fonti Consultate (20 totali)

1. [CrewAI Memory Docs](https://docs.crewai.com/en/concepts/memory)
2. [CrewAI Memory DeepWiki](https://deepwiki.com/crewAIInc/crewAI/7.2-memory-configuration-and-storage)
3. [LangGraph Persistence Docs](https://docs.langchain.com/oss/python/langgraph/persistence)
4. [LangGraph Checkpointing Best Practices 2025](https://sparkco.ai/blog/mastering-langgraph-checkpointing-best-practices-for-2025)
5. [LangGraph DynamoDB + S3](https://aws.amazon.com/blogs/database/build-durable-ai-agents-with-langgraph-and-amazon-dynamodb/)
6. [LangMem Launch Post](https://blog.langchain.com/langmem-sdk-launch/)
7. [LangMem Docs](https://langchain-ai.github.io/langmem/)
8. [LangMem DeepWiki](https://deepwiki.com/langchain-ai/langmem)
9. [Mem0 Overview](https://docs.mem0.ai/overview)
10. [Mem0 GitHub](https://github.com/mem0ai/mem0)
11. [Mem0 Research Paper](https://arxiv.org/abs/2504.19413)
12. [Mem0 Graph Memory Jan 2026](https://mem0.ai/blog/graph-memory-solutions-ai-agents)
13. [Zep Open Source Direction](https://blog.getzep.com/announcing-a-new-direction-for-zeps-open-source-strategy/)
14. [Zep Feature Retirements May 2025](https://blog.getzep.com/zep-feature-retirements-may-2025/)
15. [AutoGen Memory Docs](https://microsoft.github.io/autogen/stable//user-guide/agentchat-user-guide/memory.html)
16. [AutoGen State Management](https://microsoft.github.io/autogen/stable//user-guide/agentchat-user-guide/tutorial/state.html)
17. [Letta Context Repositories](https://www.letta.com/blog/letta-code)
18. [Claude Code Session Memory - claudefa.st](https://claudefa.st/blog/guide/mechanics/session-memory)
19. [Manus Context Engineering](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
20. [EU AI Act Audit Requirements - ISACA](https://www.isaca.org/resources/news-and-trends/industry-news/2025/the-growing-challenge-of-auditing-agentic-ai)

---

*Report generato da Cervella Researcher - Sessione 373*
*CervellaSwarm - 2026-02-19*
