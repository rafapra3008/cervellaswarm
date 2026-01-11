# RICERCA CERVELLA AI - PARTE 2: DETTAGLI TECNICI

> **Ricerca condotta da:** Cervella Researcher
> **Data:** 10 Gennaio 2026
> **Prerequisito:** Leggi PARTE 1 prima di questo documento

---

## ARCHITETTURA SISTEMA

```
┌─────────────────────────────────────────────────────────┐
│                    CERVELLA AI                          │
└─────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   FastAPI    │   │  LangGraph   │   │  PostgreSQL  │
│   Backend    │◄──┤    Agent     │◄──┤   + pgvector │
│              │   │              │   │              │
└──────────────┘   └──────────────┘   └──────────────┘
        │                  │                  │
        │                  ▼                  │
        │          ┌──────────────┐           │
        │          │  Claude API  │           │
        │          │  (Opus 4.5)  │           │
        │          └──────────────┘           │
        │                                     │
        ▼                                     ▼
┌──────────────┐                      ┌──────────────┐
│   Interface  │                      │ Vector Store │
│  (CLI/Web)   │                      │  RAG Index   │
└──────────────┘                      └──────────────┘
```

---

## 1. RAG (RETRIEVAL AUGMENTED GENERATION)

### Cos'è RAG e Come Funziona

**RAG = Memoria Esterna per LLM**

Invece di:
```
User: "Qual è la nostra filosofia?"
→ Claude: [non sa, inventa]
```

Con RAG:
```
User: "Qual è la nostra filosofia?"
→ RAG: Cerca nei documenti → Trova COSTITUZIONE.md
→ Claude + Contesto: "Secondo la COSTITUZIONE, la filosofia è..."
```

### Processo RAG (Step by Step)

**FASE 1 - INDEXING (una tantum, poi aggiornamenti):**

```python
# 1. Leggi documenti
docs = load_markdown_files(".sncp/", "~/.claude/", etc.)

# 2. Chunking (divide in pezzi semantici)
chunks = split_by_headers(docs, chunk_size=400)
# Esempio chunk:
# {
#   "content": "## La Nostra Filosofia\n\nLavoriamo in PACE...",
#   "metadata": {"file": "COSTITUZIONE.md", "section": "Filosofia"}
# }

# 3. Embedding (converti testo in vettori)
embeddings = embedding_model.embed(chunks)
# [0.234, -0.456, 0.789, ...] → 768 dimensioni

# 4. Salva in vector DB
vector_db.add(chunks, embeddings)
```

**FASE 2 - RETRIEVAL (ogni query):**

```python
# 1. User query
query = "Qual è la nostra filosofia?"

# 2. Embed query
query_embedding = embedding_model.embed(query)

# 3. Similarity search
similar_chunks = vector_db.search(query_embedding, top_k=5)
# Returns top 5 chunks più simili semanticamente

# 4. Passa a Claude
context = "\n\n".join([chunk.content for chunk in similar_chunks])
prompt = f"""
Context from our documents:
{context}

User question: {query}

Answer based on the context above.
"""
response = claude.complete(prompt)
```

### Best Practices RAG (2026)

**1. Chunking Strategico**

Per Markdown (nostro caso):
```python
# Split by headers (semanticamente coerente)
- H1 → Documento principale
- H2 → Sezioni (chunk ideale)
- H3 → Sottosezioni (raggruppa con H2 se corto)

# Chunk size: 400-600 token
# Overlap: 50-100 token (evita perdere contesto a confini)
```

**2. Hybrid Search**

```python
# Non solo vector similarity!
results = combine(
    vector_search(query),      # Semantic similarity
    keyword_search(query),      # Exact match (BM25)
    rerank(results)             # Riordina per rilevanza
)
```

**3. Metadata Filtering**

```python
# Cerca solo in file specifici
search(
    query="deployment workflow",
    filter={"file_type": "roadmap", "date_gte": "2026-01-01"}
)
```

**4. Chunking Markdown - Esempio Pratico**

```markdown
# COSTITUZIONE.md  ← H1

## Chi Sono  ← H2 → CHUNK 1
Sono Cervella Regina...
(~300 token)

## La Nostra Filosofia  ← H2 → CHUNK 2
"Lavoriamo in PACE..."
(~450 token)

### Regole d'Oro  ← H3 → parte di CHUNK 2
- Mai fretta
- Dettagli contano
(~150 token)
```

---

## 2. VECTOR DATABASES - CONFRONTO DETTAGLIATO

### pgvector (RACCOMANDATO per MVP)

**Pro:**
- ✅ Gratis (estensione PostgreSQL)
- ✅ Già usiamo Postgres in altri progetti
- ✅ Unisce dati relazionali + vettori (utile per metadata)
- ✅ Scala fino a 10M vettori (più che sufficiente)
- ✅ Backup standard PostgreSQL

**Contro:**
- ⚠️ Performance < di DB specializzati (ma OK per nostro uso)
- ⚠️ Richiede tuning PostgreSQL per grandi volumi

**Setup:**

```sql
-- Enable extension
CREATE EXTENSION vector;

-- Create table
CREATE TABLE document_chunks (
  id SERIAL PRIMARY KEY,
  content TEXT,
  embedding vector(768),  -- 768 dimensions
  metadata JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Create index (IVFFlat or HNSW)
CREATE INDEX ON document_chunks
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Query
SELECT content, metadata,
       1 - (embedding <=> query_vector) as similarity
FROM document_chunks
ORDER BY embedding <=> query_vector
LIMIT 5;
```

**Costo:** $0 (incluso in Postgres) + ~$15-25/mese per Cloud SQL PostgreSQL micro.

### Chroma (ALTERNATIVA per prototipazione)

**Pro:**
- ✅ Setup in 5 minuti
- ✅ API semplicissima (Python-first)
- ✅ Perfetto per POC locale
- ✅ Open source, locale

**Contro:**
- ⚠️ Meno features di pgvector per production
- ⚠️ Meno mature per deployment cloud

**Setup:**

```python
import chromadb

# Local setup
client = chromadb.Client()
collection = client.create_collection("cervella_docs")

# Add documents
collection.add(
    documents=["Lavoriamo in PACE! Senza CASINO!"],
    metadatas=[{"source": "COSTITUZIONE.md"}],
    ids=["doc1"]
)

# Query
results = collection.query(
    query_texts=["qual è la filosofia?"],
    n_results=5
)
```

**Costo:** $0 (self-hosted locale o su Cloud Run).

### Pinecone (SE scaling estremo futuro)

**Pro:**
- ✅ Performance migliori (< 50ms latency)
- ✅ Serverless, auto-scaling
- ✅ Gestione zero

**Contro:**
- ❌ $70-250/mese (managed)
- ❌ Vendor lock-in

**Quando considerare:** Se > 50M vettori o latency critica (< 20ms).

---

## 3. EMBEDDING MODELS

### Cosa Sono

Convertono testo in vettori numerici che catturano significato semantico.

```
"Cervella è la Regina" → [0.234, -0.456, 0.789, ...]
"Rafa è il CEO"        → [0.221, -0.442, 0.801, ...]  ← simile!
"Pizza margherita"     → [-0.891, 0.123, -0.345, ...] ← diverso
```

### Opzioni 2026

| Model | Dimensioni | Performance | Costo | Raccomandazione |
|-------|------------|-------------|-------|-----------------|
| **Cohere Embed v4** | 1536 | Ottima | $0.12/1M token | **CONSIGLIATO** |
| **OpenAI text-embedding-3-large** | 3072 | Molto buona | $0.13/1M token | Alternativa |
| **BGE-large (open source)** | 1024 | Buona | $0 (locale) | **MVP/POC** |
| **E5-large (open source)** | 1024 | Buona | $0 (locale) | **MVP/POC** |

### Raccomandazione

**POC:** BGE-large locale (gratis, veloce setup)
**MVP/Production:** Cohere Embed v4 (qualità/prezzo, 128k context)

**Perché Cohere v4:**
- Context window 128k token (intero COSTITUZIONE.md in una pass!)
- Pricing competitivo ($0.12/1M vs $0.13 OpenAI)
- Performance MTEB benchmark: top 5
- API semplice

**Costo Embedding (stima):**
```
Totale docs: ~100MB markdown ≈ 25M token
Una tantum: 25M * $0.12/1M = $3
Aggiornamenti incrementali: ~$5-10/mese
```

### Setup Embedding

```python
import cohere

co = cohere.Client(api_key="...")

# Embed documenti
embeddings = co.embed(
    texts=chunks,
    model="embed-multilingual-v4.0",
    input_type="search_document"
)

# Embed query
query_embedding = co.embed(
    texts=[query],
    model="embed-multilingual-v4.0",
    input_type="search_query"
)
```

---

## 4. LANGGRAPH - AGENT FRAMEWORK

### Perché LangGraph

**Problema con agent semplici:**
```python
# Naive approach
while True:
    user_input = input()
    response = claude.complete(user_input)
    print(response)
# ❌ No memoria
# ❌ No stato persistente
# ❌ No recovery da errori
```

**LangGraph risolve:**
- ✅ Stato persistente (PostgreSQL)
- ✅ Memoria conversazione
- ✅ Checkpoint automatici (resume da failure)
- ✅ Human-in-the-loop
- ✅ Production-ready deployment

### Architettura LangGraph

```python
from langgraph.graph import StateGraph
from langgraph.checkpoint.postgres import PostgresSaver

# Define state
class AgentState(TypedDict):
    messages: List[Message]
    context: str
    user_id: str

# Define graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("retrieve", retrieve_context)  # RAG
workflow.add_node("generate", call_claude)       # LLM
workflow.add_node("save", save_to_db)            # Persistence

# Add edges
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", "save")

# Compile with checkpointer
checkpointer = PostgresSaver.from_conn_string(DB_URI)
app = workflow.compile(checkpointer=checkpointer)
```

### Stato Persistente

**Ogni conversazione = thread_id**

```python
# Session 1
app.invoke(
    {"messages": [{"role": "user", "content": "Chi sono?"}]},
    config={"configurable": {"thread_id": "user_rafa_session_1"}}
)

# 3 giorni dopo...
# Session 1 resumed (ricorda tutto!)
app.invoke(
    {"messages": [{"role": "user", "content": "Ricordi cosa ti ho chiesto?"}]},
    config={"configurable": {"thread_id": "user_rafa_session_1"}}
)
```

**Storage PostgreSQL:**
```sql
-- LangGraph crea automaticamente
CREATE TABLE checkpoints (
  thread_id TEXT,
  checkpoint_id TEXT,
  parent_checkpoint_id TEXT,
  checkpoint JSONB,
  metadata JSONB,
  PRIMARY KEY (thread_id, checkpoint_id)
);
```

### Memory Strategies (Best Practices 2026)

**1. Short-term Memory (in-session)**
```python
# Buffer ultimi N messaggi
memory = ConversationBufferMemory(k=10)
```

**2. Long-term Memory (cross-session)**
```python
# RAG su conversazioni passate
# Indicizza conversazioni vecchie → vector DB
# Retrieve conversazioni rilevanti come contesto
```

**3. Tiered Memory**
```python
# Livello 1: Redis (cache 5min)
# Livello 2: PostgreSQL (conversazioni attive)
# Livello 3: Cold storage (archivio S3)
```

---

## 5. CLAUDE API - DETTAGLI PRODUZIONE

### Pricing Breakdown (2026)

**Claude Opus 4.5:**
- Input: $5 / 1M token
- Output: $25 / 1M token
- Cache Read: $0.50 / 1M token (90% sconto!)
- Cache Write: $6.25 / 1M token (25% premium)

**Esempio conversazione tipica:**

```
User: "Qual è la nostra roadmap?"

Input:
- System prompt (COSTITUZIONE): 5k token
- Conversazione storia: 3k token
- RAG context: 2k token
- User query: 0.1k token
TOTALE INPUT: 10k token

Output:
- Response: 1k token

COSTI:
Senza caching: 10k * $5/1M + 1k * $25/1M = $0.075
Con caching (90% cached): 1k * $5/1M + 9k * $0.5/1M + 1k * $25/1M = $0.034

RISPARMIO: 55% con prompt caching!
```

### Prompt Caching - Come Funziona

Claude cache automaticamente prefissi lunghi (> 1024 token).

**Struttura prompt ottimizzata:**

```python
# ✅ GOOD - Cacheable parts first
prompt = f"""
{SYSTEM_PROMPT}           # ← 5k token, RARAMENTE cambia → CACHE HIT!

{RAG_CONTEXT}             # ← 2k token, cambia ogni query → CACHE MISS

{CONVERSATION_HISTORY}   # ← 3k token, cambia ogni turno → CACHE MISS

User: {user_query}        # ← 0.1k token
"""

# ❌ BAD - No caching benefits
prompt = f"""
User: {user_query}
{CONVERSATION_HISTORY}
{RAG_CONTEXT}
{SYSTEM_PROMPT}
"""
```

**Best Practice:**
- System prompt + personalità → cache 5min+
- RAG base knowledge → cache 1min
- Conversazione history → no cache (cambia sempre)

### Rate Limits

**Tier 1 (automatico, gratis):**
- 50 RPM (requests per minute)
- 40,000 TPM (tokens per minute)
- 5,000 TPD (tokens per day)

**Tier 2 (automatico dopo $5 spesi):**
- 1,000 RPM
- 80,000 TPM
- 150,000 TPD

**Tier 4 (automatico dopo $1000 spesi):**
- 4,000 RPM
- 4,000,000 TPM (input)
- Praticamente illimitato

**Nostro uso stimato:**
```
MVP (uso interno, 3 persone):
- ~200 request/day
- ~50k token/day
→ Tier 1 OK!

Production (Miracollo, 100 utenti):
- ~5000 request/day
- ~500k token/day
→ Tier 2-3
```

### Error Handling & Retries

```python
from anthropic import Anthropic, RateLimitError
import backoff

@backoff.on_exception(
    backoff.expo,
    RateLimitError,
    max_tries=5
)
def call_claude(prompt):
    return client.messages.create(
        model="claude-opus-4-5-20251101",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
```

---

## 6. DEPLOYMENT - GOOGLE CLOUD

### Opzione 1: Cloud Run (RACCOMANDATO MVP)

**Vantaggi:**
- ✅ Serverless (zero management)
- ✅ Auto-scaling (0 → N instances)
- ✅ Pay-per-request (idle = $0)
- ✅ Deploy da Docker in 1 comando

**Architettura:**

```
┌─────────────────┐
│   Cloud Run     │
│   (FastAPI)     │  ← Container Docker
│                 │  ← Auto-scale 0-100 instances
└────────┬────────┘
         │
    ┌────┴─────┐
    │          │
    ▼          ▼
┌──────┐  ┌──────┐
│ Cloud│  │Claude│
│  SQL │  │ API  │
│ (PG) │  │      │
└──────┘  └──────┘
```

**Dockerfile:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

**Deploy:**

```bash
# Build
docker build -t cervella-ai .

# Push to GCP
gcloud builds submit --tag gcr.io/PROJECT/cervella-ai

# Deploy
gcloud run deploy cervella-ai \
  --image gcr.io/PROJECT/cervella-ai \
  --region us-central1 \
  --memory 2Gi \
  --timeout 60s \
  --allow-unauthenticated
```

**Costo stimato:**
```
Requests: 10k/mese
CPU: 1 vCPU @ $0.00002400/vCPU-second
Memory: 2Gi @ $0.00000250/GiB-second
Avg request time: 3 sec

Monthly: ~$20-40
```

### Opzione 2: Compute Engine VM (se serve 24/7 uptime)

**Quando considerare:**
- Background jobs (re-indexing periodico)
- WebSocket persistenti
- Warm instance sempre pronta

**VM minima:**
```
Type: e2-micro (2 vCPU, 1GB RAM)
Cost: ~$7/mese (con sustained use discount)

Type: e2-small (2 vCPU, 2GB RAM)
Cost: ~$14/mese
```

---

## 7. FASTAPI - WEB BACKEND

### Perché FastAPI

- ✅ Performance (async/await nativo)
- ✅ API docs automatiche (Swagger)
- ✅ Type hints (Pydantic)
- ✅ Integrazione perfetta con LangGraph

### Structure

```
cervella-ai/
├── app/
│   ├── main.py              # FastAPI app
│   ├── agents/
│   │   └── cervella.py      # LangGraph agent
│   ├── rag/
│   │   ├── indexer.py       # Indexing docs
│   │   ├── retriever.py     # Search
│   │   └── embeddings.py    # Embedding models
│   ├── db/
│   │   └── postgres.py      # DB setup
│   └── api/
│       └── routes.py        # Endpoints
├── docs/                    # SNCP files (read-only)
├── Dockerfile
├── requirements.txt
└── .env
```

### Endpoints

```python
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    user_id: str
    thread_id: str | None = None

@app.post("/chat")
async def chat(request: ChatRequest):
    """Synchronous chat"""
    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": request.message}]},
        config={"thread_id": request.thread_id or new_thread()}
    )
    return {"response": response, "thread_id": thread_id}

@app.websocket("/ws/chat")
async def chat_ws(websocket: WebSocket):
    """Streaming chat (real-time)"""
    await websocket.accept()
    async for chunk in agent.astream(message):
        await websocket.send_text(chunk)

@app.post("/index/refresh")
async def refresh_index():
    """Re-index documents"""
    await indexer.reindex_all()
    return {"status": "ok"}
```

---

## 8. SICUREZZA E BEST PRACTICES

### API Key Management

**❌ MAI fare:**
```python
# Hard-coded
CLAUDE_API_KEY = "sk-ant-..."

# Committed to git
.env file with keys → git add .env
```

**✅ FARE:**
```python
# Environment variables
import os
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

# Secret manager (production)
from google.cloud import secretmanager
secret = client.access_secret_version(name="claude-api-key")
```

**.gitignore:**
```
.env
*.key
secrets/
```

**Google Cloud Secret Manager:**
```bash
# Store secret
echo "sk-ant-..." | gcloud secrets create claude-api-key --data-file=-

# Access in code
from google.cloud import secretmanager
client = secretmanager.SecretManagerServiceClient()
secret = client.access_secret_version(
    name="projects/PROJECT/secrets/claude-api-key/versions/latest"
)
api_key = secret.payload.data.decode("UTF-8")
```

### Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/chat")
@limiter.limit("10/minute")  # Max 10 req/min per IP
async def chat(request: ChatRequest):
    ...
```

### Input Validation

```python
from pydantic import BaseModel, validator

class ChatRequest(BaseModel):
    message: str
    user_id: str

    @validator("message")
    def message_length(cls, v):
        if len(v) > 5000:
            raise ValueError("Message too long")
        return v
```

### Monitoring

```python
import logging
from google.cloud import logging as cloud_logging

# Setup
cloud_logging.Client().setup_logging()

# Log
logging.info("Chat request", extra={
    "user_id": user_id,
    "tokens_used": tokens,
    "latency_ms": latency
})
```

---

**Prossimo documento:** PARTE 3 - Piano Implementazione & Code Examples

_"I dettagli fanno SEMPRE la differenza"_ 🔬
