# ROADMAP MVP GPU - FASE 2

> **Data:** 11 Gennaio 2026
> **Sessione:** 162
> **Stato:** INFRASTRUTTURA COMPLETATA! Prossimi step definiti.

---

## DOVE SIAMO

```
+================================================================+
|                                                                |
|   FASE 1: RICERCA E POC                    [COMPLETATA]       |
|   - 34,324+ righe di ricerca                                  |
|   - POC Cervella Baby: 95% PASS                               |
|   - Decisione: GO per MVP Hybrid                              |
|                                                                |
|   FASE 2: INFRASTRUTTURA GPU               [COMPLETATA]       |
|   - Dominio: cervellaai.com                                   |
|   - VM cervella-gpu: T4 GPU attiva                            |
|   - Ollama + Qwen3-4B funzionante                             |
|   - API miracollo -> GPU testata OK                           |
|   - Schedule risparmio configurato                            |
|                                                                |
|   FASE 3: INTEGRAZIONE MVP                 [DA FARE]          |
|   - Miracollo backend integrato                               |
|   - Qdrant per RAG                                            |
|   - Costituzione Cervella                                     |
|   - UI/UX base                                                |
|                                                                |
+================================================================+
```

---

## INFRASTRUTTURA ATTUALE (Sessione 162)

```
cervella-gpu (us-west1-b):
  Machine: n1-standard-4 + Tesla T4 (16GB VRAM)
  IP interno: 10.138.0.3
  API: http://10.138.0.3:11434
  Modello: qwen3:4b (Q4_K_M)
  Schedule: 9-19 Lun-Ven (Italia)
  Costo stimato: ~$85/mese (con schedule)

miracollo-cervella (us-central1-b):
  Backend esistente
  Chiama cervella-gpu via API interna
```

---

## FASE 3: INTEGRAZIONE MVP

### Sprint 3.1: Integrazione Backend Miracollo
**Priorità:** ALTA
**Stima:** 1-2 sessioni

- [ ] Creare client HTTP per Ollama API in backend
- [ ] Endpoint `/api/ai/chat` per chat con LLM
- [ ] Gestione errori e timeout
- [ ] Test integrazione end-to-end

### Sprint 3.2: Setup Qdrant (Vector DB)
**Priorità:** ALTA
**Stima:** 1 sessione

- [ ] Installare Qdrant su cervella-gpu (o VM separata)
- [ ] Configurare collection per documenti
- [ ] Test inserimento e query vettoriale

### Sprint 3.3: RAG Pipeline Base
**Priorità:** ALTA
**Stima:** 2-3 sessioni

- [ ] Embedding con Jina-embeddings-v3 (o alternativa)
- [ ] Chunking documenti
- [ ] Retrieval da Qdrant
- [ ] Integration con Qwen3-4B per generation

### Sprint 3.4: Costituzione Cervella
**Priorità:** MEDIA
**Stima:** 1 sessione

- [ ] System prompt con valori CervellaSwarm
- [ ] Personalita' e tono
- [ ] Test conversazioni
- [ ] Iterare su feedback

### Sprint 3.5: UI/UX Base
**Priorità:** MEDIA
**Stima:** 2-3 sessioni

- [ ] Pagina chat semplice
- [ ] Input/output styled
- [ ] Loading states
- [ ] Mobile responsive

---

## OTTIMIZZAZIONI COSTI (Scoperte Sessione 162)

### Gia' Implementato
- [x] Schedule Start/Stop (9-19 Lun-Ven) → ~70% risparmio
- [x] SUD automatico (30%) → gratis

### Da Valutare Dopo 1-2 Mesi
- [ ] CUD 1 anno se usage diventa 24/7
- [ ] Spot VM per ambiente dev separato
- [ ] Rightsizing se n1-standard-4 e' troppo

### Costi Stimati Attuali
```
ON-DEMAND 24/7:        ~$400/mese
CON SUD (automatico):  ~$280/mese
CON SCHEDULE:          ~$85/mese  <-- ATTUALE

Risparmio totale: ~$315/mese = ~$3,780/anno!
```

---

## DECISIONI APERTE

### 1. Qdrant: Dove installarlo?
**Opzioni:**
- A) Su cervella-gpu (stesso server, latenza zero)
- B) VM separata (isolamento, ma costo extra)
- C) Qdrant Cloud (managed, ma costo)

**Raccomandazione:** A) su cervella-gpu per iniziare

### 2. Embedding Model
**Opzioni:**
- A) Jina-embeddings-v3 (come pianificato)
- B) all-MiniLM-L6-v2 (piu' leggero)
- C) Ollama embedding (tutto integrato)

**Raccomandazione:** C) Ollama embedding per semplicita'

### 3. Frontend
**Opzioni:**
- A) Aggiungere a Miracollo esistente
- B) App separata (Next.js/React)
- C) Solo API per ora (no UI)

**Raccomandazione:** A) aggiungere a Miracollo

---

## PROSSIME SESSIONI SUGGERITE

### Sessione 163: Integrazione Backend
- Creare client Ollama in Miracollo
- Endpoint chat base
- Test e2e

### Sessione 164: Qdrant + Embedding
- Setup Qdrant
- Configurare embedding
- Test retrieval

### Sessione 165: RAG Pipeline
- Collegare tutto
- Test con documenti reali
- Iterare

### Sessione 166: Costituzione
- System prompt
- Personalita'
- Test conversazioni

---

## METRICHE SUCCESSO

| Metrica | Target | Status |
|---------|--------|--------|
| GPU VM attiva | Si | DONE |
| API funzionante | Si | DONE |
| Costo < $150/mese | Si | DONE (~$85) |
| Chat e2e funziona | - | TODO |
| RAG funziona | - | TODO |
| Costituzione OK | - | TODO |

---

## COMANDI UTILI

```bash
# SSH a cervella-gpu
gcloud compute ssh cervella-gpu --zone=us-west1-b --project=data-frame-476309-v3

# Accendere manualmente (fuori schedule)
gcloud compute instances start cervella-gpu --zone=us-west1-b --project=data-frame-476309-v3

# Spegnere manualmente
gcloud compute instances stop cervella-gpu --zone=us-west1-b --project=data-frame-476309-v3

# Test API Ollama
curl http://10.138.0.3:11434/api/tags

# Test inference
curl http://10.138.0.3:11434/api/generate -d '{"model":"qwen3:4b","prompt":"Ciao!","stream":false}'
```

---

*"Provare sempre ci piace!"*
*"La magia ora e' con coscienza!"*
*"Il mondo lo facciamo meglio, con il cuore!"*

---

**Aggiornato:** 11 Gennaio 2026 - Sessione 162
