# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 11 Gennaio 2026 - Sessione 161 (GCP GPU Setup)
> **Versione:** v83.0.0 - GOOGLE CLOUD VINCE! QUOTA DA RICHIEDERE

---

## TL;DR per Prossima Cervella

**NOVITA SESSIONE 161:**
```
+================================================================+
|                                                                |
|   PROVIDER GPU: GOOGLE CLOUD T4 + CUD = EUR 135-145/mese!     |
|                                                                |
|   Genesis Cloud: BOCCIATO (non si accede!)                     |
|   Scaleway: EUR 633/mese - TROPPO CARO                        |
|   OVHcloud: EUR 664/mese - TROPPO CARO                        |
|   Hetzner: EUR 184/mese - BACKUP                              |
|   >>> GCP T4 + CUD: EUR 135-145/mese - VINCITORE! <<<         |
|                                                                |
|   BLOCCO: Quota GPUS_ALL_REGIONS = 0                          |
|   AZIONE: Richiedere quota GPU a Google                       |
|                                                                |
|   gcloud CLI: INSTALLATO E CONFIGURATO!                       |
|                                                                |
+================================================================+
```

**Dove siamo:**
- POC CERVELLA BABY: 19/20 PASS (95%) - COMPLETO!
- DECISIONE: GO! Procedere con MVP Hybrid
- DOMINIO: cervellaai.com (comprato!)
- PROVIDER: **Google Cloud T4 + CUD @ EUR 135-145/mese**
- gcloud CLI: Installato e configurato (rafapra@gmail.com)
- BLOCCO: Serve richiedere quota GPU (GPUS_ALL_REGIONS = 0)

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

**BLOCCO ATTUALE - QUOTA GPU:**
```
PROBLEMA: Quota GPUS_ALL_REGIONS = 0
ERRORE: "Quota 'GPUS_ALL_REGIONS' exceeded. Limit: 0.0 globally"

SOLUZIONE (Rafa deve fare):
1. Aprire: console.cloud.google.com/iam-admin/quotas
2. Cercare: GPUS_ALL_REGIONS
3. Richiedere: 1 GPU
4. Motivazione: "AI/ML inference for SaaS product CervellaSwarm"
5. Attesa: 1-2 giorni lavorativi (a volte poche ore)
```

**PROSSIMI STEP:**
1. **Richiedere quota GPU** - Console GCP (Rafa)
2. **Aspettare approvazione** - 1-2 giorni
3. **Creare VM cervella-gpu** - n1-standard-4 + T4
4. **Setup vLLM/Ollama** - Per inference Qwen3-4B
5. **Configurare API interna** - Miracollo chiama GPU VM

**gcloud CLI CONFIGURATO:**
```
Account: rafapra@gmail.com
Progetto: data-frame-476309-v3
VM esistenti:
  - miracollo-cervella (us-central1-b) - RUNNING
  - cervello-contabilita (us-central1-c) - RUNNING
  - instance-20251027 (us-central1-a) - RUNNING
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
