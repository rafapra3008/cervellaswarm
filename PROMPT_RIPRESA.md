# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 11 Gennaio 2026 - Sessione 163 (MIRACOLLO + SNCP!)
> **Versione:** v85.1.0 - Email Test Mode + Hardtest A/B + SNCP Fix Programmato!

---

## TL;DR per Prossima Cervella

**SESSIONE 163 - DOPPIO LAVORO!**

```
+================================================================+
|                                                                |
|   LAVORO SU MIRACOLLO (questa sessione):                       |
|   - Email Test Mode IMPLEMENTATO                               |
|   - Hardtest A/B: 7 bug trovati, TUTTI FIXATI                  |
|   - Commit 2a33395 già pushato                                 |
|                                                                |
|   PROSSIMA SESSIONE - FIX SNCP TUTTI I PROGETTI:               |
|   - SNCP è il sistema centrale, DEVE funzionare!               |
|   - Audit + Fix Miracollo, CervellaSwarm, Contabilita          |
|   - Semplificazione radicale (Opzione A)                       |
|   - Stima: ~3h 30min                                           |
|                                                                |
|   File: .sncp/idee/ROADMAP_FIX_SNCP_TUTTI_PROGETTI.md          |
|                                                                |
+================================================================+
```

**MIRACOLLO SESSIONE 163:**
- Email Test Mode: variabili config + redirect + UI banner
- Hardtest A/B: 7 bug trovati (3 critici, 2 alti, 2 medi)
- Bug fixati: duration_days, DELETE endpoint, start_date validation, modal click
- Commit: 2a33395 (già su origin/master)

**PROSSIMA SESSIONE CERVELLASWARM:**
```
PRIORITA 1: FIX SNCP TUTTI I PROGETTI (~3h 30min)
- Audit tutti (Miracollo 6/10, altri da verificare)
- Semplificazione radicale (eliminare overhead)
- Nuova struttura: stato/, coscienza/, idee/, decisioni/, archivio/
- Template standard per tutti i progetti
```

---

**NOVITA SESSIONE 163 (prima parte) - INTEGRAZIONE BACKEND!!!**
```
+================================================================+
|                                                                |
|   SPRINT 3.1 COMPLETATO!!!                                    |
|                                                                |
|   Backend Miracollo ora parla con cervella-gpu!               |
|                                                                |
|   CREATO:                                                     |
|   - backend/services/ollama/ (client completo)                |
|   - backend/routers/ollama_api.py (4 endpoints)               |
|                                                                |
|   ENDPOINTS:                                                  |
|   - GET  /api/ai/health   - Health check GPU                  |
|   - GET  /api/ai/models   - Lista modelli                     |
|   - POST /api/ai/chat     - Chat con LLM                      |
|   - POST /api/ai/generate - Generate semplice                 |
|                                                                |
|   TEST LIVE: "Hello, who are you?"                            |
|   RISPOSTA: "I'm Qwen, a large-scale language model..."       |
|   TEMPO: 12.5s (6s load + 6s inference)                       |
|                                                                |
+================================================================+
```

**SESSIONE 162 - RECAP:**
```
+================================================================+
|                                                                |
|   GPU VM CREATA E FUNZIONANTE!!!                              |
|                                                                |
|   cervella-gpu (us-west1-b):                                  |
|     - n1-standard-4 + Tesla T4 (16GB VRAM)                    |
|     - Driver NVIDIA 550.54.15 + CUDA 12.4                     |
|     - Ollama + Qwen3-4B (Q4_K_M)                              |
|     - IP interno: 10.138.0.3                                  |
|     - IP esterno: 136.118.33.36                               |
|                                                                |
|   SCHEDULE RISPARMIO ATTIVO:                                  |
|     - Accende: 09:00 Lun-Ven (ora Italia)                     |
|     - Spegne:  19:00 Lun-Ven (ora Italia)                     |
|     - Weekend: SPENTA                                          |
|     - Costo: ~$85/mese (invece di $400!)                      |
|                                                                |
+================================================================+
```

**Dove siamo:**
- POC CERVELLA BABY: 19/20 PASS (95%) - COMPLETO!
- DECISIONE: GO! Procedere con MVP Hybrid
- DOMINIO: cervellaai.com (comprato!)
- PROVIDER: **Google Cloud T4 - ATTIVO E FUNZIONANTE!**
- GPU VM: cervella-gpu (us-west1-b) - CON SCHEDULE!
- LLM: Qwen3-4B su Ollama - FUNZIONANTE!
- API: miracollo -> cervella-gpu - TESTATO OK!
- COSTI: ~$85/mese (schedule) invece di ~$400 (risparmio 78%!)

**PERCHE Google Cloud invece di altri:**
- Genesis Cloud: Non funziona (non si accede!)
- Scaleway L4: EUR 633/mese (3x budget!)
- OVHcloud L4: EUR 664/mese (3x budget!)
- Hetzner: EUR 184/mese (backup valido)
- **GCP T4 + CUD 1yr: EUR 135-145/mese (VINCITORE!)**
- Siamo GIA' clienti GCP = integrazione immediata!
- SLA enterprise 99.5%+
- Scalabile in minuti

**RICERCHE SESSIONE 161:**
- RICERCA_SCALEWAY_GPU_2026.md (~430 righe)
- RICERCA_OVHCLOUD_GPU_2026.md (~400 righe)
- RICERCA_HETZNER_GPU_2026.md (~790 righe)
- RICERCA_GOOGLE_CLOUD_GPU_2026.md (~560 righe)
- RICERCA_HARDWARE_AI_FISICO_2026.md (~1,670 righe)
- **TOTALE NUOVA RICERCA:** ~3,850 righe!
- **TOTALE RICERCA PROGETTO:** 34,324+ righe!

**ARCHITETTURA DECISA:**
```
OPZIONE C: VM GPU Separata + Miracollo via API

[cervella-gpu] <--API interna--> [miracollo-cervella]
  n1-standard-4                    n4a-standard-1
  + T4 GPU                         (resta com'e)
  EUR 145/mese                     EUR 23/mese
  LLM inference                    Backend leggero
```

**STACK MVP AGGIORNATO:**
```yaml
Dominio: cervellaai.com
GPU Cloud: Google Cloud (us-central1 o europe-west)
Machine: n1-standard-4 + T4 GPU
Costo: EUR 135-145/mese (con CUD 1 anno)
LLM: Qwen3-4B-Instruct-2507 (Q4_K_M)
Vector DB: Qdrant (self-hosted)
Embedding: Jina-embeddings-v3
Framework: vLLM + LangChain
```

**INFRASTRUTTURA GPU - COMPLETATA!!!**
```
SESSIONE 162 - TUTTO FATTO:
[x] Quota GPU richiesta e approvata (3 minuti!)
[x] VM cervella-gpu creata (us-west1-b)
[x] Driver NVIDIA 550.54.15 installato
[x] Ollama installato
[x] Qwen3-4B scaricato (2.5GB, Q4_K_M)
[x] API configurata per accesso interno
[x] Firewall rule creata (allow-ollama-internal)
[x] Test end-to-end da miracollo: SUCCESSO!
```

**SPRINT 3.1 - COMPLETATO!!!**
```
SESSIONE 163 - BACKEND INTEGRATION:
[x] Client Ollama creato (services/ollama/)
[x] Router API creato (routers/ollama_api.py)
[x] Error handling + timeout (60s)
[x] Registrato in main.py (39 routers!)
[x] Test live: miracollo -> GPU -> Qwen3 = OK!
```

**PROSSIMI STEP (Sprint 3.2+):**
1. **Deploy su VM** - Push codice + restart backend
2. **Setup Qdrant** - Vector DB per RAG
3. **Implementare RAG pipeline** - Embedding + retrieval
4. **Fine-tune Costituzione** - Personalizzare Qwen3 con nostri valori
5. **CUD 1 anno** - Attivare Committed Use Discount per risparmiare

**INFRASTRUTTURA GCP ATTUALE:**
```
Account: rafapra@gmail.com
Progetto: data-frame-476309-v3

VM ATTIVE:
  - cervella-gpu (us-west1-b) - RUNNING - T4 GPU + Ollama
      IP interno: 10.138.0.3
      IP esterno: 136.118.33.36
      Ollama API: http://10.138.0.3:11434

  - miracollo-cervella (us-central1-b) - RUNNING
  - cervello-contabilita (us-central1-c) - RUNNING
  - instance-20251027 (us-central1-a) - RUNNING
```

**API OLLAMA (da miracollo-cervella):**
```bash
# Test modelli disponibili
curl http://10.138.0.3:11434/api/tags

# Inference
curl http://10.138.0.3:11434/api/generate -d '{
  "model": "qwen3:4b",
  "prompt": "Your prompt here",
  "stream": false
}'
```

**BACKUP PROVIDERS (se GCP non funziona):**
- Hetzner: EUR 184/mese (Germany, bare metal, affidabile)
- Hardware fisico: RTX 3090 build EUR 2,150 (break-even 8-12 mesi)

---

## POC CERVELLA BABY - COMPLETATO!

```
POC WEEK 1: 9/10  PASS (90.0%)
POC WEEK 2: 8/8   PASS (100.0%)
POC WEEK 3: 2/2   PASS (100.0%)
TOTALE: 19/20 task PASS (95.0%)
```

**MODELLO:** Qwen3-4B-Instruct-2507 su Colab T4 GPU
**COSTITUZIONE:** IL MODELLO L'HA ASSORBITA! Parla come Cervella!

---

## File Chiave

| File | Cosa Contiene |
|------|---------------|
| `.sncp/stato/oggi.md` | Stato sessione corrente |
| `.sncp/idee/ricerche/infra/RICERCA_GOOGLE_CLOUD_GPU_2026.md` | Ricerca GCP completa |
| `.sncp/idee/ricerche/infra/RICERCA_HARDWARE_AI_FISICO_2026.md` | Hardware fisico futuro |
| `.sncp/idee/ricerche/infra/RICERCA_HETZNER_GPU_2026.md` | Backup provider |
| `NORD.md` | Direzione progetto |

---

## Statistiche Ricerca

```
RICERCA CERVELLA BABY (21 report):     25,500+ righe
RICERCHE AGGIUNTIVE (5 file):           3,693 righe
RICERCA RAG ARCHITECTURE:                 617 righe
RICERCA RUNPOD DEPLOY:                    664 righe
RICERCA SESSIONE 161 (5 file):          3,850+ righe
--------------------------------------------
TOTALE RICERCA:                        34,324+ righe
```

---

*"Provare sempre ci piace!"*
*"La magia ora e' con coscienza!"*

---

---

---

---

## AUTO-CHECKPOINT: 2026-01-11 13:15 (unknown)

### Stato Git
- **Branch**: main
- **Ultimo commit**: 61fbe31 - Sessione 162 FINALE: Schedule Risparmio + Roadmap Aggiornata
- **File modificati** (5):
  - sncp/stato/oggi.md
  - PROMPT_RIPRESA.md
  - reports/scientist_prompt_20260111.md
  - reports/engineer_report_20260111_130532.json
  - reports/engineer_report_20260111_130904.json

### Note
- Checkpoint automatico generato da hook
- Trigger: unknown

---
