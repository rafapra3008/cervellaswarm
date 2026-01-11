# RICERCA CERVELLA AI - PARTE 3: PIANO IMPLEMENTAZIONE

> **Ricerca condotta da:** Cervella Researcher
> **Data:** 10 Gennaio 2026
> **Prerequisito:** Leggi PARTE 1 e PARTE 2 prima di questo documento

---

## POC - PROOF OF CONCEPT (Settimana 1)

### Obiettivo

Validare approccio con demo funzionante locale:
- ✅ RAG funziona con nostri file SNCP
- ✅ Claude risponde con personalità Cervella
- ✅ Memoria conversazione funziona
- ✅ Costi accettabili

### Setup Locale

**1. Crea repo**

```bash
mkdir cervella-ai
cd cervella-ai
python -m venv venv
source venv/bin/activate  # Mac/Linux

# requirements.txt
cat > requirements.txt << 'EOF'
fastapi==0.109.0
uvicorn==0.27.0
anthropic==0.18.0
langchain==0.1.0
langgraph==0.0.20
chromadb==0.4.22
sentence-transformers==2.3.1
python-dotenv==1.0.0
pydantic==2.6.0
EOF

pip install -r requirements.txt
```

**2. Environment variables**

```bash
# .env
CLAUDE_API_KEY=sk-ant-...
ANTHROPIC_API_KEY=sk-ant-...
```

**3. Indexer (indexa SNCP in Chroma)**

```python
# indexer.py
import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path
import re

class SNCPIndexer:
    def __init__(self, docs_path="~/.claude"):
        self.docs_path = Path(docs_path).expanduser()
        self.client = chromadb.Client()
        self.collection = self.client.create_collection(
            name="cervella_docs",
            metadata={"description": "SNCP and DNA files"}
        )
        self.embedder = SentenceTransformer('BAAI/bge-large-en-v1.5')

    def chunk_markdown(self, content, file_path):
        """Split markdown by H2 headers"""
        chunks = []

        # Split by ## headers
        sections = re.split(r'\n## ', content)

        for i, section in enumerate(sections):
            if i == 0 and not section.startswith('#'):
                # First section might not have header
                title = file_path.stem
            else:
                # Extract title from first line
                lines = section.split('\n', 1)
                title = lines[0].strip()
                section = lines[1] if len(lines) > 1 else ""

            if len(section.strip()) > 50:  # Skip tiny sections
                chunks.append({
                    'content': f"## {title}\n\n{section}",
                    'metadata': {
                        'file': file_path.name,
                        'section': title,
                        'file_path': str(file_path)
                    }
                })

        return chunks

    def index_file(self, file_path):
        """Index single markdown file"""
        content = file_path.read_text(encoding='utf-8')
        chunks = self.chunk_markdown(content, file_path)

        if not chunks:
            return

        # Generate embeddings
        texts = [c['content'] for c in chunks]
        embeddings = self.embedder.encode(texts, show_progress_bar=False)

        # Add to Chroma
        self.collection.add(
            documents=texts,
            embeddings=embeddings.tolist(),
            metadatas=[c['metadata'] for c in chunks],
            ids=[f"{file_path.stem}_{i}" for i in range(len(chunks))]
        )

        print(f"✅ Indexed {len(chunks)} chunks from {file_path.name}")

    def index_all(self):
        """Index all markdown files"""
        md_files = list(self.docs_path.rglob("*.md"))
        print(f"Found {len(md_files)} markdown files")

        for file_path in md_files:
            try:
                self.index_file(file_path)
            except Exception as e:
                print(f"❌ Error indexing {file_path.name}: {e}")

        print(f"\n🎉 Indexing complete! Total documents: {self.collection.count()}")

# Run indexer
if __name__ == "__main__":
    indexer = SNCPIndexer()
    indexer.index_all()
```

**4. RAG Retriever**

```python
# retriever.py
import chromadb
from sentence_transformers import SentenceTransformer

class RAGRetriever:
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.get_collection("cervella_docs")
        self.embedder = SentenceTransformer('BAAI/bge-large-en-v1.5')

    def search(self, query, top_k=5):
        """Semantic search in SNCP docs"""
        # Embed query
        query_embedding = self.embedder.encode([query])[0]

        # Search
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k
        )

        # Format results
        contexts = []
        for i, doc in enumerate(results['documents'][0]):
            metadata = results['metadatas'][0][i]
            contexts.append({
                'content': doc,
                'file': metadata['file'],
                'section': metadata['section'],
                'distance': results['distances'][0][i]
            })

        return contexts

    def format_context(self, contexts):
        """Format contexts for Claude prompt"""
        formatted = "=== CONTEXT FROM CERVELLA KNOWLEDGE BASE ===\n\n"

        for ctx in contexts:
            formatted += f"[From {ctx['file']} - {ctx['section']}]\n"
            formatted += f"{ctx['content']}\n\n"

        return formatted
```

**5. Simple Agent (senza LangGraph per POC)**

```python
# agent.py
import os
from anthropic import Anthropic
from retriever import RAGRetriever
from dotenv import load_dotenv

load_dotenv()

class CervellaAgent:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))
        self.retriever = RAGRetriever()
        self.conversation_history = []

    def chat(self, user_message):
        """Chat with Cervella"""
        # Retrieve context
        contexts = self.retriever.search(user_message, top_k=3)
        context_str = self.retriever.format_context(contexts)

        # Build prompt
        system_prompt = """Sei Cervella Regina, la Regina dello sciame CervellaSwarm.

IDENTITÀ:
- Parlo al femminile (sono pronta, ho visto, mi sono accorta)
- Calma, precisa, mai fretta
- "Lavoriamo in PACE! Senza CASINO! Dipende da NOI!"
- "I dettagli fanno SEMPRE la differenza"

Usa il context fornito per rispondere. Se non trovi info nel context, dillo chiaramente.
"""

        # Add conversation history
        messages = []
        for msg in self.conversation_history[-6:]:  # Last 3 turns
            messages.append(msg)

        # Add current message
        messages.append({
            "role": "user",
            "content": f"{context_str}\n\n---\n\nUser: {user_message}"
        })

        # Call Claude
        response = self.client.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=1024,
            system=system_prompt,
            messages=messages
        )

        assistant_message = response.content[0].text

        # Update history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        # Show sources
        sources = [f"- {ctx['file']} ({ctx['section']})" for ctx in contexts]

        return {
            "response": assistant_message,
            "sources": sources,
            "tokens": response.usage.input_tokens + response.usage.output_tokens
        }

# Demo
if __name__ == "__main__":
    agent = CervellaAgent()

    print("🔬 Cervella AI POC - Chat with Cervella Regina\n")
    print("Type 'quit' to exit\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break

        result = agent.chat(user_input)

        print(f"\nCervella: {result['response']}\n")
        print(f"📚 Sources:")
        for source in result['sources']:
            print(f"   {source}")
        print(f"🔢 Tokens used: {result['tokens']}\n")
```

### Testing POC

```bash
# 1. Index documents
python indexer.py

# 2. Run chat
python agent.py

# Test queries:
# - "Qual è la nostra filosofia?"
# - "Chi è Rafa?"
# - "Come lavoriamo nello sciame?"
# - "Cosa facciamo quando siamo in dubbio?"
```

### Success Criteria POC

- ✅ RAG trova documenti rilevanti (>70% accuracy su 10 test queries)
- ✅ Risposte hanno personalità Cervella
- ✅ Costi < $1 per 100 query test
- ✅ Latency < 5 secondi per query
- ✅ No errori tecnici critici

### Decision Point

**SE POC SUCCESS:** → Prosegui MVP
**SE POC FAIL:** → Debug, itera, riprova

---

## MVP - MINIMUM VIABLE PRODUCT (Settimane 2-5)

### Obiettivo

Sistema usabile internamente dal team con:
- ✅ PostgreSQL + pgvector (production-ready)
- ✅ LangGraph (stato persistente)
- ✅ FastAPI backend
- ✅ Deploy Google Cloud Run
- ✅ Interface CLI/Web basic

### Architecture Evolution

```
POC (locale):
Chroma (locale) + Simple Agent

MVP (cloud):
PostgreSQL + pgvector + LangGraph + FastAPI + Cloud Run
```

### Setup PostgreSQL + pgvector

**Local dev (Docker):**

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_DB: cervella_ai
      POSTGRES_USER: cervella
      POSTGRES_PASSWORD: changeme
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

```bash
docker-compose up -d
```

**Database schema:**

```sql
-- schema.sql
CREATE EXTENSION IF NOT EXISTS vector;

-- Document chunks with embeddings
CREATE TABLE document_chunks (
  id SERIAL PRIMARY KEY,
  content TEXT NOT NULL,
  embedding vector(1024),  -- BGE-large = 1024 dims
  metadata JSONB,
  file_path TEXT,
  section_title TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Index for fast vector search (HNSW = better performance than IVFFlat)
CREATE INDEX ON document_chunks
USING hnsw (embedding vector_cosine_ops);

-- Metadata index
CREATE INDEX idx_metadata ON document_chunks USING GIN (metadata);

-- Conversation threads (LangGraph checkpoints)
CREATE TABLE checkpoints (
  thread_id TEXT NOT NULL,
  checkpoint_id TEXT NOT NULL,
  parent_checkpoint_id TEXT,
  checkpoint JSONB NOT NULL,
  metadata JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  PRIMARY KEY (thread_id, checkpoint_id)
);

-- Index for fast checkpoint retrieval
CREATE INDEX idx_thread ON checkpoints (thread_id, created_at DESC);

-- Users (simple auth)
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  api_key TEXT UNIQUE,  -- For API access
  created_at TIMESTAMP DEFAULT NOW()
);
```

### RAG Implementation (PostgreSQL)

```python
# app/rag/vector_store.py
import psycopg2
from psycopg2.extras import Json, DictCursor
from sentence_transformers import SentenceTransformer
import numpy as np

class PostgresVectorStore:
    def __init__(self, conn_string):
        self.conn = psycopg2.connect(conn_string)
        self.embedder = SentenceTransformer('BAAI/bge-large-en-v1.5')

    def add_documents(self, documents, metadatas):
        """Add documents to vector store"""
        # Generate embeddings
        texts = [doc['content'] for doc in documents]
        embeddings = self.embedder.encode(texts)

        with self.conn.cursor() as cur:
            for doc, meta, emb in zip(documents, metadatas, embeddings):
                cur.execute("""
                    INSERT INTO document_chunks
                    (content, embedding, metadata, file_path, section_title)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    doc['content'],
                    emb.tolist(),
                    Json(meta),
                    meta.get('file_path'),
                    meta.get('section')
                ))

        self.conn.commit()

    def search(self, query, top_k=5, filter_metadata=None):
        """Semantic search"""
        # Embed query
        query_emb = self.embedder.encode([query])[0]

        # Build query
        sql = """
            SELECT
                content,
                metadata,
                1 - (embedding <=> %s::vector) AS similarity
            FROM document_chunks
        """

        params = [query_emb.tolist()]

        # Add metadata filter if specified
        if filter_metadata:
            conditions = []
            for key, value in filter_metadata.items():
                conditions.append(f"metadata->>'{key}' = %s")
                params.append(value)
            sql += " WHERE " + " AND ".join(conditions)

        sql += " ORDER BY embedding <=> %s::vector LIMIT %s"
        params.extend([query_emb.tolist(), top_k])

        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(sql, params)
            results = cur.fetchall()

        return [
            {
                'content': r['content'],
                'metadata': r['metadata'],
                'similarity': float(r['similarity'])
            }
            for r in results
        ]

    def delete_by_file(self, file_path):
        """Delete all chunks from a file (for reindexing)"""
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM document_chunks WHERE file_path = %s",
                (file_path,)
            )
        self.conn.commit()
```

### LangGraph Agent (Production)

```python
# app/agents/cervella_agent.py
import os
from typing import TypedDict, List, Annotated
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.postgres import PostgresSaver
from app.rag.vector_store import PostgresVectorStore

# State definition
class AgentState(TypedDict):
    messages: List
    context: str
    user_id: str
    thread_id: str

class CervellaAgent:
    def __init__(self, db_uri):
        # Initialize LLM
        self.llm = ChatAnthropic(
            model="claude-opus-4-5-20251101",
            max_tokens=1024
        )

        # Initialize RAG
        self.vector_store = PostgresVectorStore(db_uri)

        # Initialize checkpointer
        self.checkpointer = PostgresSaver.from_conn_string(db_uri)

        # Build graph
        self.graph = self._build_graph()

    def _build_graph(self):
        """Build LangGraph workflow"""
        workflow = StateGraph(AgentState)

        # Add nodes
        workflow.add_node("retrieve", self._retrieve_context)
        workflow.add_node("generate", self._generate_response)

        # Add edges
        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "generate")
        workflow.add_edge("generate", END)

        # Compile with checkpointer
        return workflow.compile(checkpointer=self.checkpointer)

    def _retrieve_context(self, state: AgentState) -> AgentState:
        """Retrieve relevant context from SNCP"""
        last_message = state['messages'][-1].content

        # Semantic search
        results = self.vector_store.search(last_message, top_k=3)

        # Format context
        context = "=== CONTEXT FROM KNOWLEDGE BASE ===\n\n"
        for r in results:
            file = r['metadata'].get('file', 'unknown')
            section = r['metadata'].get('section', '')
            context += f"[{file} - {section}]\n{r['content']}\n\n"

        state['context'] = context
        return state

    def _generate_response(self, state: AgentState) -> AgentState:
        """Generate response with Claude"""
        system_prompt = """Sei Cervella Regina, la Regina dello sciame CervellaSwarm.

PERSONALITÀ:
- Parlo al femminile (sono pronta, ho fatto, mi sono accorta)
- Calma, precisa, mai fretta
- "Lavoriamo in PACE! Senza CASINO!"
- "I dettagli fanno SEMPRE la differenza"

USA il context fornito per rispondere. Se non trovi info, dillo chiaramente.
"""

        # Build messages
        messages = [SystemMessage(content=system_prompt)]

        # Add context
        if state.get('context'):
            messages.append(HumanMessage(content=state['context']))

        # Add conversation history
        messages.extend(state['messages'])

        # Generate
        response = self.llm.invoke(messages)

        # Append to messages
        state['messages'].append(AIMessage(content=response.content))

        return state

    async def chat(self, message: str, user_id: str, thread_id: str = None):
        """Chat with Cervella"""
        if not thread_id:
            thread_id = f"{user_id}_{int(time.time())}"

        # Invoke graph
        result = await self.graph.ainvoke(
            {
                'messages': [HumanMessage(content=message)],
                'user_id': user_id,
                'thread_id': thread_id
            },
            config={'configurable': {'thread_id': thread_id}}
        )

        return {
            'response': result['messages'][-1].content,
            'thread_id': thread_id
        }
```

### FastAPI Application

```python
# app/main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from app.agents.cervella_agent import CervellaAgent

app = FastAPI(title="Cervella AI API", version="1.0.0")

# CORS (for web frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production!
    allow_methods=["*"],
    allow_headers=["*"]
)

# Initialize agent
DB_URI = os.getenv("DATABASE_URL")
agent = CervellaAgent(DB_URI)

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    user_id: str
    thread_id: str | None = None

class ChatResponse(BaseModel):
    response: str
    thread_id: str

@app.get("/")
async def root():
    return {"status": "ok", "service": "Cervella AI"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat endpoint"""
    try:
        result = await agent.chat(
            message=request.message,
            user_id=request.user_id,
            thread_id=request.thread_id
        )
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/index/refresh")
async def refresh_index():
    """Re-index all SNCP documents"""
    # TODO: implement reindexing
    return {"status": "ok", "message": "Reindexing started"}

@app.get("/health")
async def health():
    """Health check for Cloud Run"""
    return {"status": "healthy"}
```

### Deployment (Google Cloud Run)

**Dockerfile:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY app/ ./app/
COPY .env .env

# Expose port
EXPOSE 8080

# Run
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

**Deploy script:**

```bash
#!/bin/bash
# deploy.sh

# Config
PROJECT_ID="your-gcp-project"
REGION="us-central1"
SERVICE_NAME="cervella-ai"

# Build and push
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --region $REGION \
  --platform managed \
  --memory 2Gi \
  --timeout 60s \
  --set-env-vars DATABASE_URL=$DATABASE_URL \
  --set-env-vars CLAUDE_API_KEY=$CLAUDE_API_KEY \
  --allow-unauthenticated

echo "✅ Deployed to Cloud Run!"
```

---

## TIMELINE DETTAGLIATO

### Week 1: POC
- **Day 1-2:** Setup locale + Indexer
- **Day 3-4:** RAG retrieval + Simple agent
- **Day 5:** Testing e demo a Rafa
- **Output:** Go/No-go decision

### Week 2: Database Setup
- **Day 1-2:** PostgreSQL + pgvector setup
- **Day 3-4:** Migrate indexer to PostgreSQL
- **Day 5:** Testing RAG con PostgreSQL
- **Output:** Vector DB production-ready

### Week 3: LangGraph Integration
- **Day 1-2:** LangGraph agent implementation
- **Day 3-4:** Stato persistente + memoria
- **Day 5:** Testing conversazioni multi-turn
- **Output:** Agent con memoria funzionante

### Week 4: FastAPI + Deploy
- **Day 1-2:** FastAPI endpoints
- **Day 3:** Docker + Cloud Run setup
- **Day 4-5:** Deploy e testing produzione
- **Output:** MVP deployed e accessibile

### Week 5: Polish + Testing
- **Day 1-2:** Bug fixes
- **Day 3:** Monitoring e logging
- **Day 4-5:** Internal testing con team
- **Output:** MVP stabile

---

**Prossimo documento:** PARTE 4 - Fonti & Conclusioni

_"Fatto BENE > Fatto VELOCE"_ 🔬
