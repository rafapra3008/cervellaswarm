# RICERCA: Agent Memory Systems 2025-2026

> **Ricerca:** Cugino #1 (cervella-researcher)
> **Data:** 1 Gennaio 2026
> **Contesto:** PoC Cugini - Ricerca Parallela

---

## EXECUTIVE SUMMARY

La memoria è LA capability fondamentale degli agenti AI moderni. Il 2025-2026 ha portato:
1. **Context window grandi ≠ buona memoria** - Servono architetture esplicite
2. **RAG da solo non basta** - Necessari hybrid approaches (graph + vector + semantic)
3. **Strategic forgetting = feature** - Non tutto va ricordato
4. **GraphRAG = standard emergente** - Knowledge graphs coordinano multi-agent
5. **Memory corruption = nuovo problema critico** - Serve validazione continua

---

## 1. STATE OF THE ART

### Il Problema Fondamentale
Gli LLM non hanno memoria nativa. Ogni conversazione parte da zero. Le soluzioni 2025-2026:

- **Context Window** - Claude: 200K tokens, GPT-4: 128K, Gemini: 1M+
- **Ma**: Più lungo ≠ migliore. Needle-in-haystack test mostra degradazione
- **Soluzione**: Architetture esplicite di memoria

### Trend Dominante: Memoria Multi-Livello
```
┌─────────────────────────────────────────┐
│  WORKING MEMORY (Immediata)             │
│  - Context window attivo                │
│  - ~10K tokens efficaci                 │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│  SHORT-TERM MEMORY (Sessione)           │
│  - Riassunti conversazione              │
│  - Key-value cache                      │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│  LONG-TERM MEMORY (Persistente)         │
│  - Vector DB (Pinecone, Chroma)         │
│  - Knowledge Graph                      │
│  - File system                          │
└─────────────────────────────────────────┘
```

---

## 2. PATTERN PRINCIPALI

### Pattern 1: MemGPT Virtual Memory
- **Concept**: Tratta LLM come CPU con memoria virtuale
- **Architettura**: Core Memory (RAM) + Recall Memory (Cache) + Archive (Disk)
- **Pro**: Gestione automatica paging
- **Contro**: Overhead computazionale

### Pattern 2: RAG Evolution (2025)
- **Vanilla RAG** → problemi di retrieval accuracy
- **Agentic RAG** → agent decide QUANDO e COSA recuperare
- **GraphRAG** → knowledge graph + vector search ibrido
- **Best practice**: Query rewriting + reranking + hybrid search

### Pattern 3: Context Engineering
4 strategie fondamentali:
1. **Write Context** - Scrivi riassunti strutturati
2. **Select Context** - RAG per scegliere cosa includere
3. **Compress Context** - Summarization aggressiva
4. **Isolate Context** - Separazione per dominio

### Pattern 4: Shared Memory Multi-Agent
- **Blackboard Pattern** - Memoria condivisa centrale
- **Stigmergy** - Comunicazione indiretta via ambiente
- **Message Passing** - Queue per comunicazione
- **Per CervellaSwarm**: ROADMAP.md = stigmergy!

---

## 3. BEST PRACTICES

### Do's
- ✅ Struttura esplicita memoria (non solo context dump)
- ✅ Separazione per tipo (facts vs procedures vs episodes)
- ✅ Validazione periodica (memory può corrompersi)
- ✅ Forgetting strategico (non tutto va ricordato)
- ✅ Human-readable format (debug facile)

### Don'ts
- ❌ Affidarsi solo a context window grande
- ❌ Memorizzare tutto senza filtro
- ❌ Ignorare memory drift over time
- ❌ Mixing concerns in single memory store

---

## 4. LIMITI E SFIDE

### Problemi Non Risolti

| Problema | Descrizione | Mitigazione |
|----------|-------------|-------------|
| **Memory Corruption** | Info false persistono | Validazione periodica |
| **Context Drift** | Memoria diverge da realtà | Refresh da source of truth |
| **Forgetting** | Quando dimenticare? | TTL + relevance scoring |
| **Coordination** | Multi-agent memory sync | Leader election + consensus |
| **Cost** | Più memoria = più token | Compression + caching |

---

## 5. APPLICABILITA CERVELLASWARM

### Architettura Raccomandata

```
┌─────────────────────────────────────────────────────────────────┐
│                     CERVELLASWARM MEMORY                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  LIVELLO 1: FILE-BASED (Attuale) ✅                            │
│  ├── ROADMAP_SACRA.md (strategia)                              │
│  ├── PROMPT_RIPRESA.md (contesto sessione)                     │
│  ├── NORD.md (direzione)                                       │
│  └── swarm_memory.db (eventi + lezioni)                        │
│                                                                 │
│  LIVELLO 2: DATABASE (Attuale) ✅                              │
│  ├── swarm_events (log task)                                   │
│  ├── lessons_learned (knowledge base)                          │
│  └── error_patterns (pattern detection)                        │
│                                                                 │
│  LIVELLO 3: FUTURO (Da Valutare)                               │
│  ├── Vector DB per semantic search                             │
│  ├── Knowledge Graph per relazioni                             │
│  └── Real-time sync per multi-agent                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Raccomandazioni Immediate

1. **Continuare con file-based** - Funziona, è debuggabile, human-readable
2. **Potenziare SQLite** - Già in uso, aggiungere indici e views
3. **Stigmergy via ROADMAP** - Pattern validato per coordinamento
4. **Validazione settimanale** - Review memoria per evitare drift

### Raccomandazioni Future

1. **Vector search** - Per lezioni simili (semantic similarity)
2. **Knowledge Graph** - Per relazioni tra concetti (GraphRAG)
3. **Memory compression** - Per sessioni lunghe

---

## FONTI

1. MemGPT Paper (Berkeley, 2023-2024)
2. LangChain Memory Documentation (2025)
3. Anthropic Context Engineering Guide
4. Microsoft AutoGen Memory Patterns
5. OpenAI Best Practices for LLM Memory
6. Google ADK Agent Memory Architecture
7. Pinecone RAG Best Practices 2025
8. Neo4j GraphRAG Documentation

---

*"La memoria è ciò che trasforma un LLM in un agente."* 🧠

*Ricerca completata da Cugino #1 - PoC Parallelizzazione* 🐝
