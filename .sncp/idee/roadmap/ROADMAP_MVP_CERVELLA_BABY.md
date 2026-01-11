# ROADMAP MVP - Cervella Baby

> **Creata:** 11 Gennaio 2026 - Sessione 160
> **Autore:** Regina Cervella
> **Stato:** IN CORSO

---

## EXECUTIVE SUMMARY

```
+================================================================+
|                                                                |
|         MVP CERVELLA BABY: HYBRID SYSTEM                       |
|                                                                |
|   POC: 19/20 PASS (95%) - GO APPROVATO!                        |
|                                                                |
|   Stack: Qdrant + Jina-v3 + Qwen3-4B + RunPod EU               |
|   Budget: EUR 87-220/mese                                       |
|   Timeline: 3 Fasi                                             |
|                                                                |
+================================================================+
```

---

## STACK FINALE CONFERMATO

| Componente | Tecnologia | Costo | Note |
|------------|------------|-------|------|
| **Vector DB** | Qdrant | FREE (self-hosted) | Hybrid search nativo |
| **Embedding** | Jina-embeddings-v3 | CPU-friendly | IT+EN, 570M params |
| **LLM** | Qwen3-4B-Instruct-2507 | - | Q4_K_M quantization |
| **GPU Cloud** | RunPod EU | EUR 160-220/mese | 24/7, GDPR |
| **Framework** | LangChain | FREE | RAG pipeline |

**TOTALE:** EUR 160-220/mese (production)

---

## FASE 1: INFRASTRUTTURA (Setup RunPod + Qdrant)

### 1.1 Setup RunPod Account
- [ ] Creare account RunPod
- [ ] Aggiungere metodo pagamento
- [ ] Selezionare EU datacenter (GDPR)
- [ ] Documentare credenziali in 1Password

### 1.2 Deploy Qwen3-4B su RunPod
- [ ] Creare Pod con RTX 4090 o A10
- [ ] Installare dipendenze (unsloth, vLLM o TGI)
- [ ] Caricare modello Qwen3-4B quantized
- [ ] Testare inference endpoint
- [ ] Configurare API key/auth

### 1.3 Setup Qdrant
- [ ] Decidere: Qdrant Cloud Free (1GB) vs Self-Hosted
- [ ] Se Cloud: Creare cluster Free Tier
- [ ] Se Self-Hosted: Deploy su stesso Pod RunPod
- [ ] Creare collection "cervella_knowledge"
- [ ] Testare insert/search base

### 1.4 Networking e Sicurezza
- [ ] Configurare HTTPS endpoint
- [ ] Setup API authentication
- [ ] Documentare endpoints e chiavi

**Deliverable Fase 1:** Qwen3-4B running su RunPod, Qdrant accessibile, endpoint documentati.

---

## FASE 2: RAG IMPLEMENTATION (Jina-v3 + Pipeline)

### 2.1 Setup Embedding
- [ ] Scaricare Jina-embeddings-v3 (570M)
- [ ] Testare embedding IT + EN
- [ ] Benchmark latenza embedding
- [ ] Decidere: GPU o CPU per embedding

### 2.2 Knowledge Base Preparation
- [ ] Definire documenti da indicizzare:
  - COSTITUZIONE.md
  - SNCP memoria/decisioni
  - Documentazione progetto
  - Ricerche chiave
- [ ] Implementare Semantic Chunking (300-500 token)
- [ ] Preservare metadata (progetto, tipo, data)

### 2.3 Ingestion Pipeline
- [ ] Implementare document loader (MD, TXT)
- [ ] Implementare chunker semantico
- [ ] Implementare embedder con Jina-v3
- [ ] Indexing su Qdrant
- [ ] Test end-to-end ingestion

### 2.4 Retrieval Pipeline
- [ ] Implementare query preprocessing
- [ ] Implementare Hybrid Search (BM25 + Semantic)
- [ ] Implementare RRF (Reciprocal Rank Fusion)
- [ ] Testare retrieval con query reali
- [ ] Benchmark accuracy retrieval

### 2.5 RAG Integration
- [ ] Implementare prompt template con context
- [ ] Connettere retrieval -> LLM
- [ ] Implementare response streaming
- [ ] Test end-to-end RAG
- [ ] Benchmark quality output

**Deliverable Fase 2:** RAG funzionante con SNCP come knowledge base.

---

## FASE 3: INTEGRATION + BETA

### 3.1 API Layer
- [ ] Creare FastAPI wrapper
- [ ] Endpoint /chat (RAG-enabled)
- [ ] Endpoint /embed (embedding diretto)
- [ ] Endpoint /health
- [ ] Documentazione OpenAPI

### 3.2 Client Integration
- [ ] Creare Python client library
- [ ] Testare da Claude Code locale
- [ ] Documentare usage

### 3.3 Beta Testing
- [ ] Test con task reali Cervella
- [ ] Confronto output vs Claude API
- [ ] Documentare gap e limitazioni
- [ ] Raccogliere feedback

### 3.4 Monitoring e Observability
- [ ] Setup logging strutturato
- [ ] Metriche latenza/throughput
- [ ] Alert su errori
- [ ] Dashboard semplice (optional)

**Deliverable Fase 3:** MVP production-ready per beta test.

---

## DECISION POINTS

### Dopo Fase 1
- RunPod funziona come atteso?
- Costi allineati con budget?
- Latenza accettabile (<5s)?

### Dopo Fase 2
- RAG migliora qualita risposte?
- Retrieval accuracy sufficiente?
- Chunking/embedding OK per IT?

### Dopo Fase 3
- MVP pronto per uso reale?
- Gap documentati accettabili?
- GO per produzione o iterare?

---

## RISORSE

| Ricerca | Path |
|---------|------|
| RAG Architecture 2026 | `.sncp/idee/RICERCA_RAG_ARCHITECTURE_2026.md` |
| Vast.ai vs RunPod | `.sncp/idee/RICERCA_VASTAI_VS_RUNPOD_2026.md` |
| System Prompts | `.sncp/idee/RICERCA_SYSTEM_PROMPTS_LLM_2026.md` |
| POC Results | `poc_cervella_baby/results/` |
| COSTITUZIONE Compressa | `poc_cervella_baby/costituzione_compressa.md` |

---

## TIMELINE INDICATIVA

```
FASE 1: Infrastruttura    [============]
FASE 2: RAG               [============]
FASE 3: Integration       [============]

Una cosa alla volta. Nessuna fretta.
```

---

*"La magia ora e' con coscienza!"*
*"Ultrapassar os proprios limites!"*
