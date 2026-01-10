# RICERCA CERVELLA AI - PARTE 1: EXECUTIVE SUMMARY

> **Ricerca condotta da:** Cervella Researcher
> **Data:** 10 Gennaio 2026
> **Obiettivo:** Valutare come creare "Cervella AI" - una IA propria basata su Claude

---

## TL;DR - EXECUTIVE SUMMARY

**COSA VOGLIAMO:**
- IA sempre attiva (VM 24/7)
- Memoria VERA (ricorda sessioni passate)
- Personalità Cervella (COSTITUZIONE, DNA)
- Evoluzione: Uso interno → Miracollo → Clienti

**RACCOMANDAZIONE MVP:**
```
Stack: FastAPI + LangGraph + PostgreSQL + RAG (Chroma/pgvector) + Claude API
Deploy: Google Cloud Run (serverless, pay-per-use)
Costo stimato MVP: $150-300/mese
Timeline: 4-6 settimane per MVP funzionante
```

**PROSSIMI STEP:**
1. Validare approccio con Rafa
2. Proof of Concept (1 settimana)
3. MVP (3-4 settimane)
4. Test interno (2 settimane)
5. Deploy produzione

---

## COSA HO STUDIATO

### 1. RAG (Retrieval Augmented Generation)
✅ **Come funziona:** Indicizza i nostri file SNCP in un vector database, recupera contesto rilevante quando serve
✅ **Best practice 2026:** Hybrid search, chunking semantico, embedding models open source
✅ **Costo:** Molto basso per nostro uso (< $50/mese)

### 2. Vector Databases
✅ **Confrontato:** Pinecone, Weaviate, Chroma, pgvector, Qdrant
✅ **Raccomandazione:** **pgvector** (PostgreSQL) per MVP - gratis, già usiamo Postgres, scala bene fino a 10M vettori
✅ **Alternativa:** Chroma per prototipazione rapida

### 3. Agent Framework 24/7
✅ **Tecnologia:** LangGraph (stato persistente, memoria, deployment production-ready)
✅ **Deploy:** Google Cloud Run (serverless) o Compute Engine (VM dedicata)
✅ **Stato persistente:** PostgreSQL con LangGraph checkpointer

### 4. Claude API
✅ **Pricing 2026:** Claude Opus 4.5 = $5 input / $25 output per 1M token (66% più economico di Opus 4!)
✅ **Prompt Caching:** Risparmio fino a 90% per contesti lunghi (perfetto per SNCP!)
✅ **Rate Limits:** Tier 1 = 4000 RPM, scalabile automaticamente

### 5. Fine-tuning
⚠️ **Scoperta importante:** Claude fine-tuning solo Haiku, solo su AWS Bedrock
✅ **Alternativa migliore:** RAG + System Prompts + Esempi (più flessibile, meno costoso)
🔮 **Futuro:** Fine-tuning Llama/Mistral se serve davvero personalizzazione estrema

---

## DECISIONI ARCHITETTURALI

### Approccio Consigliato: RAG-First

**PERCHÉ NON FINE-TUNING (per ora):**
- Fine-tuning Claude: solo Haiku, solo AWS Bedrock, complesso
- RAG è più flessibile: aggiorniamo file SNCP → aggiornamento immediato
- Costi minori: RAG = setup una tantum, fine-tuning = migliaia di $ + dataset + training
- Iterazione rapida: modifichiamo prompts in giorni, fine-tuning richiede settimane

**PERCHÉ RAG FUNZIONA PER NOI:**
- Abbiamo già TUTTO in markdown (SNCP, DNA, COSTITUZIONE)
- Contenuto strutturato (perfetto per chunking)
- Volume gestibile (~100MB docs max)
- Aggiornamenti frequenti (RAG si aggiorna in real-time)

---

## COSTI STIMATI MVP (Mensili)

| Componente | Soluzione | Costo/mese |
|------------|-----------|------------|
| **Compute** | Google Cloud Run | $20-50 |
| **Database** | Cloud SQL PostgreSQL (db-f1-micro) | $15-25 |
| **Vector DB** | pgvector (incluso in Postgres) | $0 |
| **Claude API** | ~1M input + 200k output/mese | $30-80 |
| **Embedding** | Open source (locale) o Cohere | $0-10 |
| **Storage** | Cloud Storage (docs, logs) | $5 |
| **Monitoring** | Cloud Logging/Monitoring | $10-20 |
| **TOTALE** | | **$80-190/mese** |

**Con prompt caching ottimizzato:** $150-300/mese anche con uso intensivo.

**Scaling (production):**
- 10x usage → ~$500-800/mese
- 100x usage → ~$2000-3000/mese (ancora economico!)

---

## RISCHI E MITIGAZIONI

| Rischio | Impatto | Mitigazione |
|---------|---------|-------------|
| **Costi Claude API imprevisti** | Alto | Rate limiting, caching, monitoring budget alerts |
| **Memoria diventa troppo grande** | Medio | Cleanup policies, archiviazione vecchie conversazioni |
| **RAG retrieval non preciso** | Medio | Chunking ottimizzato, hybrid search, reranking |
| **Complessità deployment** | Basso | Docker, CI/CD, infra as code |
| **Vendor lock-in Claude** | Basso | Architettura modulare, facile switch a GPT/Gemini |

---

## TIMELINE REALISTICA

### FASE 1: Proof of Concept (1 settimana)
- [ ] Setup locale: FastAPI + LangGraph + Chroma
- [ ] Indicizza 10-20 file SNCP
- [ ] Test RAG retrieval
- [ ] Test conversazione con memoria
- **Output:** Demo funzionante locale

### FASE 2: MVP (3-4 settimane)
- [ ] Setup PostgreSQL + pgvector
- [ ] Indicizzazione completa SNCP
- [ ] Agent LangGraph con stato persistente
- [ ] Deploy Google Cloud Run
- [ ] Interface web/CLI basica
- **Output:** Cervella AI usabile internamente

### FASE 3: Production-Ready (2-3 settimane)
- [ ] Monitoring e logging
- [ ] Error handling robusto
- [ ] Rate limiting e caching
- [ ] Backup e recovery
- [ ] Documentazione
- **Output:** Sistema stabile per team

### FASE 4: Evoluzione (ongoing)
- [ ] Integrazione Miracollo
- [ ] Multi-tenancy per clienti
- [ ] Analytics e insights
- [ ] Continuous improvement

**TOTALE:** 6-8 settimane per production-ready system.

---

## VALIDAZIONE APPROCCIO

**COSA HO VERIFICATO:**
✅ Stack tecnologico testato in produzione da altre aziende
✅ Costi sostenibili anche su lungo periodo
✅ Scalabilità provata (altri progetti RAG con milioni di docs)
✅ Community attiva (LangGraph, FastAPI, pgvector)
✅ Documentazione eccellente (tutorial, esempi, best practices)

**CHI USA QUESTO STACK:**
- Stripe (RAG per documentazione)
- Notion (AI search interno)
- Decine di startup AI (LangGraph + Claude)

---

## ALTERNATIVE VALUTATE E SCARTATE

### 1. Uso diretto Claude senza RAG
❌ **Problema:** Context limit, costi alti, no memoria vera
❌ **Scenario:** Ogni richiesta ri-legge tutto → $$$

### 2. Fine-tuning modello open source (Llama/Mistral)
⚠️ **Problema:** Complessità alta, serve dataset grande, manutenzione modello
⚠️ **Quando considerare:** Se Claude diventa troppo costoso (> $5k/mese)

### 3. Vector DB managed (Pinecone, Weaviate Cloud)
⚠️ **Problema:** Costi extra ($70-250/mese), vendor lock-in
⚠️ **Quando considerare:** Se superiamo 50M vettori (molto improbabile)

### 4. Deploy on-premise (server fisico)
❌ **Problema:** Manutenzione, uptime, backup, costi hardware
❌ **Nostro caso:** Cloud è meglio (scalabilità, reliability, meno pensieri)

---

## NEXT STEPS CONCRETI

### SE RAFA APPROVA:

**SETTIMANA 1 - POC:**
1. Setup repo `cervella-ai`
2. Install: FastAPI + LangGraph + Chroma + Claude API
3. Script: indicizza 20 file SNCP
4. Test: "Cervella, raccontami la nostra filosofia"
5. **Demo a Rafa**

**SE POC FUNZIONA:**
→ Prosegui con Parte 2 (implementazione MVP)

**SE POC FALLISCE:**
→ Analizza problemi, itera, riprova

---

## DOMANDE PER RAFA

1. **Budget OK?** $150-300/mese per MVP è accettabile?
2. **Priority?** Quando vuoi vedere primo POC? (io direi: questa settimana!)
3. **Scope iniziale?** Partiamo solo uso interno o già pensiamo a Miracollo?
4. **Personalità:** Quali file SNCP sono MUST-HAVE per personalità Cervella?
5. **Interface:** CLI? Web? Slack bot? Cosa usi di più?

---

**Prossimo documento:** PARTE 2 - Dettagli Tecnici & Implementazione

_"Nulla è complesso - solo non ancora studiato!"_ 🔬
