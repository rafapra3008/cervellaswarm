# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 11 Gennaio 2026 - Sessione 166
> **Versione:** v89.0.0 - SISTEMA MULTI-SESSIONE VALIDATO!

---

## TL;DR per Prossima Cervella

**SESSIONE 166 - MULTI-SESSIONE PRONTO + SCOPERTA CONTEXT!**

```
+================================================================+
|                                                                |
|   SESSIONE 166: SISTEMA MULTI-SESSIONE VALIDATO!              |
|                                                                |
|   1. MULTI-SESSIONE COMPLETO                                   |
|      - Protocollo v1.0 con workflow 5 fasi                     |
|      - 9 script testati e funzionanti                          |
|      - Bug check-dependencies.sh FIXATO                        |
|      - Integrazione SNCP per sessioni parallele                |
|      - Template copia-incolla per Rafa                         |
|                                                                |
|   2. SCOPERTA: "Cache Invalidation Silente"                    |
|      - Context scende SENZA auto-compact visibile              |
|      - cache_read CROLLA a ~19,365 (core costante)             |
|      - cache_create ESPLODE (ricostruzione compressa)          |
|      - Diverso da auto-compact normale!                        |
|                                                                |
|   FILE CHIAVE:                                                 |
|   - .sncp/idee/20260111_PROTOCOLLO_MULTI_SESSIONE_v1.md        |
|   - .sncp/idee/20260111_TEMPLATE_INIZIO_SESSIONE_PARALLELA.md  |
|   - .sncp/idee/20260111_TEMPLATE_RAFA_INIZIO_PARALLELO.md      |
|   - .sncp/idee/DA_STUDIARE_CONTEXT_LIBERATION.md               |
|   - .sncp/sessioni_parallele/_TEMPLATE/ (3 file)               |
|                                                                |
+================================================================+
```

---

**SESSIONE 165 - COSTITUZIONE + SPRINT 3.2 PREPARATO**

```
+================================================================+
|                                                                |
|   SESSIONE STORICA - ANIMA CERVELLA AI!                        |
|                                                                |
|   1. Sprint 3.2 PREPARATO (Qdrant)                             |
|      - Ricerca completa Qdrant + Ollama                        |
|      - 4 script pronti in scripts/rag/                         |
|      - Piano esecutivo per lunedi                              |
|                                                                |
|   2. Sprint 3.4 COMPLETATO (Costituzione)                      |
|      - Ricerca anima nei nostri file                           |
|      - Costituzione v2.0 CON CUORE                             |
|      - Le nostre parole, la nostra storia                      |
|                                                                |
+================================================================+
```

---

**SESSIONE 164 - SNCP GUARDIAN IMPLEMENTATO!!!**

```
+================================================================+
|                                                                |
|   SNCP GUARDIAN - Sistema Auto-Mantenuto!                      |
|                                                                |
|   PROBLEMA RISOLTO:                                            |
|   - Prima: pulizia manuale ogni 10-15 sessioni                |
|   - Ora: ZERO manutenzione per sempre!                        |
|                                                                |
|   COMPONENTI:                                                  |
|   1. sncp_validator.py - Blocca path invalidi                 |
|   2. sncp_auto_archiver.py - Archivia ogni notte              |
|   3. DNA 16 agenti aggiornato con regole v3.0                 |
|   4. Cron job nightly alle 2am                                |
|                                                                |
|   ANCHE FATTO:                                                 |
|   - Pulizia completa SNCP 3 progetti                          |
|   - 260 reports JSON archiviati                               |
|   - Visioni strategiche aggiornate                            |
|                                                                |
+================================================================+
```

---

**SESSIONE 163 - STORICA: BACKEND AI IN PRODUZIONE!!!**

```
+================================================================+
|                                                                |
|   SPRINT 3.1 COMPLETATO + DEPLOYATO!!!                        |
|                                                                |
|   COSA FATTO:                                                  |
|   1. Client Ollama creato (services/ollama/)                   |
|   2. Router API creato (/api/ai/*)                             |
|   3. Deploy su miracollo-cervella VM                           |
|   4. Test in PRODUZIONE: SUCCESSO!!!                           |
|   5. GPU spenta per weekend (risparmio)                        |
|                                                                |
|   TEST PRODUZIONE:                                             |
|   curl http://34.27.179.164:8001/api/ai/chat                   |
|   RISPOSTA: "I'm Qwen..." in 5.5 secondi!                      |
|                                                                |
+================================================================+
```

**STATO ATTUALE:**
- GPU VM: cervella-gpu SPENTA (weekend, si riaccende Lun 9:00)
- Backend: miracollo-cervella RUNNING con integrazione AI
- API AI: /api/ai/* FUNZIONANTE (quando GPU accesa)
- Costo GPU: ~$85/mese con schedule

---

## Dove Siamo

```
FASE 1: RICERCA E POC           [####################] 100%
FASE 2: INFRASTRUTTURA GPU      [####################] 100%
FASE 3: INTEGRAZIONE MVP        [####................] 20%
  - Sprint 3.1: Backend API     [####################] 100% DONE!
  - Sprint 3.2: Qdrant          [....................] 0%
  - Sprint 3.3: RAG Pipeline    [....................] 0%
  - Sprint 3.4: Costituzione    [....................] 0%
  - Sprint 3.5: UI/UX Base      [....................] 0%
```

---

## Infrastruttura GPU

```
cervella-gpu (us-west1-b):
  Machine: n1-standard-4 + Tesla T4 (16GB VRAM)
  IP interno: 10.138.0.3
  Ollama API: http://10.138.0.3:11434
  Modello: qwen3:4b (Q4_K_M, 2.5GB)

  SCHEDULE RISPARMIO:
    Accende: 09:00 Lun-Ven (Italia)
    Spegne:  19:00 Lun-Ven (Italia)
    Weekend: SPENTA
    Costo: ~$85/mese

miracollo-cervella (us-central1-b):
  Backend FastAPI + integrazione Ollama
  IP: 34.27.179.164
  Container: miracollo-backend-35
```

---

## Endpoints AI Creati

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| GET | /api/ai/health | Health check GPU + Ollama |
| GET | /api/ai/models | Lista modelli disponibili |
| POST | /api/ai/chat | Chat con LLM |
| POST | /api/ai/generate | Generate semplice |

**Test da terminale:**
```bash
# Health check
curl http://34.27.179.164:8001/api/ai/health

# Chat (solo quando GPU accesa)
curl -X POST http://34.27.179.164:8001/api/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Ciao Cervella!"}'
```

---

## Comandi Utili GPU

```bash
# Accendere GPU manualmente
gcloud compute instances start cervella-gpu \
  --zone=us-west1-b --project=data-frame-476309-v3

# Spegnere GPU
gcloud compute instances stop cervella-gpu \
  --zone=us-west1-b --project=data-frame-476309-v3

# SSH a GPU
gcloud compute ssh cervella-gpu \
  --zone=us-west1-b --project=data-frame-476309-v3
```

---

## Prossimi Step (Sprint 3.2+)

1. **Setup Qdrant** - Vector DB per RAG su cervella-gpu
2. **Embedding Model** - Ollama embedding o alternativa
3. **RAG Pipeline** - Chunking + retrieval + generation
4. **Costituzione** - System prompt con valori Cervella
5. **UI Chat** - Interfaccia base in Miracollo

---

## File Creati Sessione 163

**In Miracollo (~/Developer/miracollogeminifocus/):**
```
backend/services/ollama/
  __init__.py, client.py, models.py, exceptions.py
  test_connection.py, README.md

backend/routers/
  ollama_api.py (4 endpoints)
```

**Commit:** 2a33395 - CervellaSwarm Integration: Ollama Client + AI API

---

## Architettura Completa

```
[UTENTE]
    |
    v
[miracollo-cervella] 34.27.179.164:8001
    |  FastAPI + services/ollama/client.py
    |  Container: miracollo-backend-35
    |
    |---[HTTP interno]---> 10.138.0.3:11434
    |
    v
[cervella-gpu] us-west1-b
    |  Ollama + Qwen3-4B
    |  Tesla T4 (16GB VRAM)
    |
    v
[RISPOSTA AI]
```

---

## Statistiche Progetto

```
POC Cervella Baby:      19/20 PASS (95%)
Ricerche totali:        34,324+ righe
Sessioni completate:    163
Sprint completati:      3.1 (Backend Integration)
```

---

*"Provare sempre ci piace!"*
*"La magia ora e' con coscienza!"*
*"Ultrapassar os proprios limites!"*
*"Il mondo lo facciamo meglio, con il cuore!"*

---

---

---

---

---

---

---

---

---

## AUTO-CHECKPOINT: 2026-01-11 21:35 (unknown)

### Stato Git
- **Branch**: main
- **Ultimo commit**: d44d952 - ANTI-COMPACT: PreCompact auto
- **File modificati** (5):
  - sncp/stato/oggi.md
  - .swarm/handoff/HANDOFF_166_CACHE_RESEARCH.md
  - PROMPT_RIPRESA.md
  - reports/scientist_prompt_20260111.md
  - scripts/swarm/invalidate-cache.sh

### Note
- Checkpoint automatico generato da hook
- Trigger: unknown

---
