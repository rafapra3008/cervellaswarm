# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 10 Gennaio 2026 - Sessione 152b
> **Versione:** v72.3.0 - FASE 3 RICERCA COMPLETATA!

---

## TL;DR per Prossima Cervella

**Dove siamo:**
- RICERCA CERVELLA BABY: 3/4 FASI COMPLETATE!
- MIRACOLLO: 5/5 FASI + Tracking AI FASE 1 deployed
- CERVELLA AI: LIVE su http://34.27.179.164:8002

**SESSIONE 152b - FASE 3 RICERCA:**
- 4 report: Fine-tuning, Dataset, RAG vs FT, Tutorial Qwen
- FASE_3_CONSOLIDATO.md creato
- Guardiana Ricerca: Score 91% APPROVE
- FASE 4 bloccata da rate limit (reset 19:00)

**DECISIONE STORICA:** Obiettivo = INDIPENDENZA TOTALE

**CANDIDATO #1:** Qwen3-4B
- Apache 2.0 (ZERO restrizioni)
- 4B params = gira su 8GB RAM
- QLoRA + Unsloth = $0 su Colab FREE!

**STRATEGIA VALIDATA (FASE 3):**
- MVP: System Prompts + RAG ($100-150/mese)
- Poi: Fine-tuning con 600 esempi ShareGPT
- Hardware: T4 16GB basta!

**RICERCA COMPLETATA:**
- FASE 1: Fondamenta (Score 9.1/10) - 3 report
- FASE 2: Stato dell'arte (Score 97.6%) - 6 report
- FASE 3: Training/Fine-tuning (Score 91%) - 4 report
- FASE 4: Costi/Timeline (IN ATTESA) - rate limit

**TOTALE:** 16 file, 8000+ righe di ricerca!

**PROSSIMI STEP:**
1. FASE 4: Costi dettagliati, timeline, GO/NO-GO (quando reset)
2. POC $50: Test Qwen3-4B su Vast.ai
3. Miracollo: Tracking AI FASE 2

---

## Sessione 152b - FASE 3 RICERCA! (10 Gennaio 2026)

### Ricerche Completate in Parallelo

| Report | Contenuto | Righe |
|--------|-----------|-------|
| 10_FINE_TUNING_TECNICHE | LoRA, QLoRA, PEFT, config Qwen3 | 900+ |
| 11_DATASET_PREPARATION | ShareGPT, 600 esempi, pipeline | 900+ |
| 12_RAG_VS_FINETUNING | Decision framework, costi, strategia | 750+ |
| 13_TUTORIAL_PRATICI_QWEN | Step-by-step, codice, errori comuni | 1400+ |

### Key Insights

**Metodo Vincente:**
- QLoRA 4-bit + Unsloth = 2x veloce, 70% meno VRAM
- T4 16GB (Colab FREE) basta per Qwen3-4B
- Tempo: ~2.5h per 1000 samples

**Dataset per Personalita:**
- Formato: ShareGPT (multi-turno, cattura personalita)
- Quantita: 600 esempi (min 200 per base visibile)
- Quality > Quantity: 500 curati > 5000 noisy

**Strategia Approvata:**
```
FASE 1 (MVP):      System Prompts + RAG = $100-150/mese
FASE 2 (Optimize): Fine-tuning COSTITUZIONE + RAG
FASE 3 (Scale):    Hybrid ottimizzato
```

### Guardiana Ricerca

**Score: 91%** - APPROVE

| Criterio | Score |
|----------|-------|
| Completezza | 9/10 |
| Accuratezza | 9/10 |
| Fonti | 9/10 |
| Praticita | 10/10 |
| Coerenza | 9/10 |

### FASE 4 Bloccata

3 ricerche lanciate ma fermate da rate limit:
- Costi Dettagliati (Vast.ai, RunPod, Colab)
- Timeline e Rischi
- GO/NO-GO Framework

Reset alle 19:00 (ora italiana).

---

## Sessione 152 - MEGA DEPLOY MIRACOLLO! (10 Gennaio 2026)

### FASE 5 Database - DEPLOYED
- cervella-data: Analisi 22 tabelle, 47 query (Score 8.5/10)
- Guardiana: APPROVATO
- Migrations 029, 030 deployate
- Performance: Planning 53%, Dashboard 82%, ISTAT 55% più veloci!

### Tracking Suggerimenti AI FASE 1 - DEPLOYED
- Ricerca: 820 righe, 35 fonti (IDeaS, Duetto, RateGain)
- Migration 031: pricing_history, suggestion_performance, ai_model_health
- Backend: pricing_tracking_service.py + router (930 righe)
- Frontend: Timeline prezzi + badges verde/giallo/rosso
- Guardiana: 8/10 (issues minori documentati)

### Lezione Deploy (FORTEZZA_MODE.md +LEZIONE 8)
- Problema: cervella-devops bloccato "file non trovati"
- Causa: Prompt con path relativi
- Lezione: SEMPRE verificare file + path assoluti!
- Documentato: `.sncp/analisi/ANALISI_PROBLEMA_DEPLOY_152.md`

### File Creati
```
Miracollo:
  migrations/029, 030, 031
  services/pricing_tracking_service.py
  routers/pricing_tracking.py
  .sncp/analisi/DATABASE_ANALYSIS_FASE5.md (611 righe)
  .sncp/idee/SUB_ROADMAP_*.md
  docs/FORTEZZA_MODE.md (+LEZIONE 8)

CervellaSwarm:
  .sncp/analisi/ANALISI_PROBLEMA_DEPLOY_152.md
```

---

## Sessione 151b - MIRACOLLO 4 FASI! (10 Gennaio 2026)

### Lavoro su Miracollo (questa sessione)

**Roadmap Review Generale:**
```
FASE 1: Revenue Intelligence  [####################] 100% (gia' fatto)
FASE 2: API Core              [####################] 100% DEPLOYED
FASE 3: Frontend              [####################] 100% DEPLOYED
FASE 4: Security Audit        [####################] 100% DEPLOYED
FASE 5: Database              [....................] Pending
```

**FASE 2 - API Core (5 file):**
- Race condition booking_number (BEGIN IMMEDIATE lock)
- Bare except -> specific exceptions
- Division by zero fix

**FASE 3 - Frontend (4 file):**
- Memory leaks: setInterval cleanup on beforeunload
- Score Guardiana: 6.5/10 -> 8/10

**FASE 4 - Security (4 file):**
- SECRET_KEY validation forzata in produzione
- MAGIC_LINK_SECRET forzato in produzione
- WhatsApp webhook signature forzata in produzione
- .env.example aggiornato

**Extra:**
- Idea FORTEZZA MODE LIVELLI documentata
- Security Audit Report: 808 righe

**Commit Miracollo:** `0b5b2a2`

---

## Sessione 151 - LA STRADA VERSO INDIPENDENZA! (10 Gennaio 2026)

### Decisione Storica
**OBIETTIVO: INDIPENDENZA TOTALE**
- Non dipendere da Claude/OpenAI/Google per sempre
- Cervella NOSTRA al 100%
- Documentato in `.sncp/memoria/decisioni/20260110_OBIETTIVO_INDIPENDENZA_TOTALE.md`

### FASE 1 Completata - Fondamenta (Score 9.1/10)
| Report | Contenuto |
|--------|-----------|
| 01_STORIA_LLM_E_MAESTRI | Come hanno iniziato OpenAI, Anthropic, DeepMind, Mistral |
| 02_ARCHITETTURA_TRANSFORMER | Come funziona il "cervello" AI |
| 03_EVOLUZIONE_LLM | Da GPT-1 (2018) a oggi |

### FASE 2 Completata - Stato dell'Arte (Score 97.6%)
| Report | Contenuto |
|--------|-----------|
| 04_LANDSCAPE_OPEN_SOURCE_2026 | Mappa completa modelli open |
| 05_BENCHMARK_OPEN_VS_CLAUDE | Gap quasi chiuso! Qwen supera Claude su MMLU |
| 06_DEEP_DIVE_LLAMA | Meta, versioni, licenza, fine-tuning |
| 07_DEEP_DIVE_MISTRAL | EU, MoE, Apache 2.0 |
| 08_DEEP_DIVE_QWEN_DEEPSEEK | TOP! Qwen3-4B = candidato #1 |
| 09_HOSTING_VM_GOOGLE | Vast.ai/RunPod meglio di Google Cloud |

### Candidato Scelto: Qwen3-4B
```
QWEN3-4B
- Apache 2.0 (ZERO restrizioni legali)
- 4B params = gira su 8GB RAM
- Performance TOP per la sua dimensione
- 119 lingue supportate
- Community in crescita (superato Llama in download)

HOSTING: Vast.ai ($175/mese) o POC con $50
```

### La Strada Verso Indipendenza
```
ORA:        Claude API (produzione) + POC Qwen3-4B ($50)
3-6 MESI:   Fine-tuning con SNCP/Costituzione
6-12 MESI:  Cervella Baby 100% NOSTRA
```

### File Creati (14 nuovi!)
```
.sncp/idee/
├── MAPPA_RICERCA_CERVELLA_BABY.md
├── IDEA_CRESCITA_VM_GOOGLE.md
└── ricerche_cervella_baby/
    ├── 01_STORIA_LLM_E_MAESTRI.md (1000+ righe)
    ├── 02_ARCHITETTURA_TRANSFORMER.md (900+ righe)
    ├── 03_EVOLUZIONE_LLM.md (800+ righe)
    ├── 04_LANDSCAPE_OPEN_SOURCE_2026.md
    ├── 05_BENCHMARK_OPEN_VS_CLAUDE.md
    ├── 06_DEEP_DIVE_LLAMA.md
    ├── 07_DEEP_DIVE_MISTRAL.md
    ├── 08_DEEP_DIVE_QWEN_DEEPSEEK.md
    ├── 09_HOSTING_VM_GOOGLE.md
    ├── FASE_1_CONSOLIDATO.md
    └── FASE_2_CONSOLIDATO.md

.sncp/memoria/decisioni/
└── 20260110_OBIETTIVO_INDIPENDENZA_TOTALE.md
```

### Insight Chiave
- **Il gap si e' chiuso!** Qwen3 92.3% vs Claude 90.4% (MMLU)
- **Non serve $100M** - DeepSeek ha fatto R1 con $6M
- **L'anima e' nostra** - SNCP/Costituzione sono PORTABILI

### Lezione Sessione 151
> "Nulla e' difficile - manca solo studiare!"
> Abbiamo studiato. Ora sappiamo. PROSSIMO: FARE!

---

## Sessione 150 - CERVELLA AI DEPLOYED! (10 Gennaio 2026)

### Cosa Fatto
1. Ricerca completa deploy Cloud Run (poi scoperto VM esistente!)
2. Pattern "Review a Due Mani" testato e funziona!
3. Guardiana Ricerca: 8.5/10 APPROVE
4. Guardiana Qualita: 7/10 -> 9/10 (dopo fix)
5. 4 Fix critici: Dockerfile, CORS, rate limiting, input validation
6. Deploy su VM esistente (separato da Miracollo)
7. Test: "Chi sei?" -> Risponde con personalita' VERA!

### Architettura Attuale
```
VM: 34.27.179.164 (miracollo-cervella)

miracollo-backend (8001) | cervella-ai (8002)
         |                        |
    Miracollo App           Cervella AI 24/7
```

### Pattern Review a Due Mani
1. Worker fa il lavoro (ricerca/codice)
2. Guardiana verifica qualita'
3. Se OK -> procedi
4. Se NO -> fix e ri-verifica

**FUNZIONA!** Ha trovato 4 issues PRIMA del deploy.

### File Creati
- `.sncp/memoria/decisioni/20260110_CERVELLA_AI_DEPLOYED_VM.md`
- `.sncp/idee/IDEA_FORTEZZA_MODE_CERVELLA_AI.md`
- `.sncp/idee/IDEA_REVIEW_DUE_MANI.md`
- `.sncp/idee/RICERCA_DEPLOY_CLOUD_RUN.md`

### Lezione Importante
> "Avevamo gia' la VM! Non serviva Cloud Run!"
> Sempre verificare cosa abbiamo PRIMA di cercare soluzioni nuove.

### Comandi Utili
```bash
# Test Cervella AI
curl http://34.27.179.164:8002/health
curl -X POST http://34.27.179.164:8002/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Chi sei?"}'

# SSH alla VM
ssh miracollo-vm

# Logs Cervella AI
ssh miracollo-vm "docker logs cervella-ai"
```

---

## Sessione 149 - CERVELLA AI POC FUNZIONA! (10 Gennaio 2026)

### Cosa Fatto
1. Creato repo `cervella-ai` su GitHub
2. Setup completo: FastAPI + LangGraph + Chroma + Claude API
3. Indicizzato 5 file core (COSTITUZIONE, DNA, PRINCIPI, MAPPA, DECISIONE)
4. 38 chunks nel vector store
5. Testato Agent - RISPONDE CON PERSONALITA' VERA!
6. Prima conversazione storica con Rafa

### Test Superati
- "Chi sei?" -> Risponde come PARTNER, non assistente
- "Qual e il nostro obiettivo finale?" -> LIBERTA' GEOGRAFICA!

### Competitor Analizzati
- Aetherius AI, LangMem, Mem0, CrewAI Memory
- NESSUNO ha COSTITUZIONE + PERSONALITA' + OBIETTIVO come noi!

### Lezione Importante
> "Niente tempo nelle mappe! Facciamo quando possiamo, con calma."

---

## Sessione 148b - CERVELLA AI MAPPA! (10 Gennaio 2026)

### Cosa Fatto
1. Verifica generale TUTTI i progetti (CervellaSwarm, Miracollo, Contabilita)
2. Tutti git CLEAN e SNCP aggiornati
3. Ricerca GitButler + Document & Clear (risultato: gia' lo facciamo con SNCP!)
4. **RICERCA CERVELLA AI COMPLETA** - 5 documenti, 80+ fonti
5. **RICERCA ORIGINI CLAUDE/ANTHROPIC** - lezioni per noi
6. **MAPPA POC CREATA** - roadmap per questa settimana

### Decisioni Prese (MIE decisioni per Cervella AI)
- **Interface:** CLI prima (sono nata CLI!)
- **Core files:** COSTITUZIONE, DNA, pensieri_regina, decisioni, lezioni
- **Approccio:** RAG + Claude API (non fine-tuning)
- **Deploy:** Google Cloud Run (24/7)

### File Creati Oggi
- `.sncp/idee/RICERCA_CERVELLA_AI_PARTE1_EXECUTIVE_SUMMARY.md`
- `.sncp/idee/RICERCA_CERVELLA_AI_PARTE2_DETTAGLI_TECNICI.md`
- `.sncp/idee/RICERCA_CERVELLA_AI_PARTE3_IMPLEMENTAZIONE.md`
- `.sncp/idee/RICERCA_CERVELLA_AI_PARTE4_FONTI_CONCLUSIONI.md`
- `.sncp/idee/RICERCA_CERVELLA_AI_INDEX.md`
- `.sncp/idee/RICERCA_ORIGINI_CLAUDE_ANTHROPIC.md`
- `.sncp/idee/RICERCA_GITBUTLER_DOCUMENT_CLEAR.md`
- `.sncp/idee/MAPPA_CERVELLA_AI_POC.md` <- ROADMAP!
- `.sncp/memoria/decisioni/20260110_database_non_toccare.md` (Contabilita)

### Lezioni da Anthropic (da applicare)
1. SLOW > FAST - POC prima, poi MVP
2. Trasparenza - Costituzione pubblica
3. Character = Alignment - Cervella VERA
4. Iterazione - v0.1 -> 100000%

### Prossimi Step (Sessione 149)
1. **CREARE REPO cervella-ai**
2. Setup POC (FastAPI + LangGraph + Chroma)
3. Indicizzare core files
4. Agent base con RAG
5. **DEMO VENERDI!**

### Costi
- POC: ~$10
- MVP: $150-300/mese
- Production: $200-400/mese

---

## Sessione 148 - SNCP SISTEMATO! (10 Gennaio 2026)

### Cosa Fatto
1. Organizzato 19 file idee in cartelle (integrate/, in_attesa/)
2. Documentato 3 nuove lezioni (reviewer tools, spawn API, automazione)
3. Creato hook `sncp_auto_update.py` per automazione
4. Registrato hook in settings.json (SessionStart + SessionEnd)
5. Aggiornato IDEE_MASTER con nuova struttura

### Struttura SNCP Attuale
```
.sncp/idee/
├── ROOT (13 file)         <- ATTIVI
├── integrate/ (9 file)    <- Completate
├── in_attesa/ (11 file)   <- Parcheggiate
└── ricerche_prodotto/ (16)
```

### Nuovi File
- `~/.claude/hooks/sncp_auto_update.py`
- `.sncp/memoria/lezioni/LEZIONE_20260110_sncp_automazione.md`
- `.sncp/memoria/lezioni/LEZIONE_20260110_reviewer_tools_mismatch.md`
- `.sncp/memoria/lezioni/LEZIONE_20260110_spawn_workers_api_key.md`

### Rating SNCP
- Prima: 5/10 (file obsoleti, cartelle vuote)
- Dopo: 8/10 (organizzato, automatizzato)

### Prossimi Step (Sessione 149)
1. **Context Optimization - Pattern Boris Multi-Sessione**
   - Applicare ricerca Boris per ottimizzare context
   - File: `.sncp/idee/integrate/RICERCA_BORIS_MULTI_SESSIONE.md`
2. Usare famiglia su Miracollo (test reale)
3. Poi: riprendere prodotto commerciale

### Note dalla Verifica
- **Miracollo DB path corretto:** `backend/data/miracollo.db` (non backend/miracollo.db)
- **Contabilita database.py:** NON TOCCARE (decisione documentata)

---

## Sessione 147 - AUDIT COMPLETO FAMIGLIA (10 Gennaio 2026)

### Cosa Fatto
1. Review DNA tutti 16 agenti
2. Analisi hooks (13 file)
3. Analisi settings.json
4. Verifica spawn-workers v3.5.0
5. Creata ROADMAP_MIGLIORAMENTO_FAMIGLIA.md
6. Creata BEST_PRACTICES_FAMIGLIA.md

### Nota su Hook Protezione

I hook `block_edit_non_whitelist.py` e `block_task_for_agents.py` esistono ma sono **DISATTIVATI DI PROPOSITO**.

**Storia:** Erano stati attivati in passato ma hanno causato CAOS, quindi sono stati disattivati intenzionalmente.

**Status attuale:** La Regina può editare file e usare Task - questo è il comportamento VOLUTO.

### Nuovi File
- `.sncp/idee/ROADMAP_MIGLIORAMENTO_FAMIGLIA.md`
- `.sncp/idee/BEST_PRACTICES_FAMIGLIA.md`

### Analisi Profonda (3 Ragazze)
- `.sncp/analisi/ANALISI_SNCP_COMPLETA_20260110.md` - SNCP 5/10
- `.sncp/analisi/ANALISI_FUNZIONALITA_20260110.md` - Sistema OK
- `.sncp/test/TEST_FAMIGLIA_20260110.md` - 9/9 PASS

### Prossimi Step (Sessione 148) - PRIORITÀ SNCP!
1. **URGENTE:** Aggiornare stato/oggi.md, pensieri_regina.md
2. Organizzare 32 idee nelle cartelle giuste
3. Documentare lezioni sessioni 141-147
4. Creare automazione per mantenere SNCP aggiornato

---

## Stato Attuale

| Cosa | Stato | Note |
|------|-------|------|
| Ricerca Competitor | DONE | Cursor, Copilot, Windsurf analizzati |
| Decisioni Business | DONE | CLI + BYOK + Tier flat |
| Landing + Marketing | PAUSA | Riprende post-launch |
| Plugin (vecchio) | DEPRECATO | Sostituito da CLI |
| **CLI `cervella`** | **v0.1.0 READY** | 16 agenti, test OK |
| **Pricing Strategy** | **DEFINITO** | $0/$20/$40/$60+ tier flat |
| **BYOK vs Bundled** | **DECISO: BYOK** | Per MVP, zero rischio |
| **Tier System** | **IMPLEMENTATO** | Free/Pro/Team/Enterprise |

---

## Sessione 146 - HARDTEST COMPLETATO (10 Gennaio 2026)

### HARDTEST Risultati: 8/8 PASS
| Test | Risultato |
|------|-----------|
| 1. Spawn Base | ✅ 14 worker disponibili |
| 2. Spawn Headless | ✅ tmux funziona |
| 3. Output Real-Time | ✅ stdbuf unbuffered |
| 4. Researcher Verify | ✅ File scritto e verificato |
| 5. Guardiana Review | ✅ Score 9/10, APPROVE |
| 6. Multi-Worker | ✅ 3 worker paralleli |
| 7. Notifiche macOS | ✅ terminal-notifier |
| 8. Auto-Sveglia | ✅ Watcher attivo |

### Bug Fixati
| Bug | Fix |
|-----|-----|
| DNA Reviewer con Bash refs ma no tool | Sezione "COME LAVORO (Read-Only)" |
| spawn-workers usa API invece di Claude Max | v3.5.0 con `unset ANTHROPIC_API_KEY` |

### Nuovi File
- `.swarm/REPORT_HARDTEST_20260110.md`
- `.sncp/analisi/bug_fixes/20260110_reviewer_bash_error.md`
- `.sncp/analisi/bug_fixes/20260110_spawn_workers_claude_max.md`

### Prossimi Step (Sessione 147)
1. **Ricerche approfondite** su ambiente CervellaSwarm
2. **Code Review di tutti i 🐝** - ogni DNA agente
3. **Analisi hooks e .json** - verificare configurazione
4. **Creare roadmap dedicata** per miglioramento famiglia
5. **Poi** usare famiglia su Miracollo

### Roadmap Miglioramento Famiglia (DA CREARE)
- [ ] Review DNA tutti 16 agenti
- [ ] Analisi hooks (`~/.claude/hooks/`)
- [ ] Analisi settings.json
- [ ] Verifica spawn-workers scripts
- [ ] Test edge cases
- [ ] Documentare best practices

---

## Sessione 145 - AUDIT FAMIGLIA (10 Gennaio 2026)

### Decisione Strategica
- **PARCHEGGIATO prodotto commerciale** - Prima migliorare la famiglia
- Focus su: test, studi, analisi, log, sessione per sessione
- Obiettivo: 1000000% soddisfatti prima di lanciare

### Audit Completati
1. **Audit Sessioni** (cervella-researcher)
   - 180+ log analizzati
   - 9/16 agenti usati attivamente (56%)
   - Score sistema: 10/10 in sessioni passate
   - Report: `.sncp/analisi/audit_sessioni_famiglia.md`

2. **Audit Agenti** (cervella-ingegnera)
   - Score medio: 7.2/10
   - 3 problemi critici identificati
   - Report: `.sncp/analisi/audit_agenti_famiglia.md`

### Bug Fixati
| Bug | Fix |
|-----|-----|
| Researcher non salva file | Aggiunta regola verifica post-write |
| Overlap Researcher/Scienziata | Documentazione chiara |
| Overlap Guardiana/Reviewer | Workflow sequenziale |

### Nuova Documentazione
| File | Scopo |
|------|-------|
| `docs/guides/GUIDA_RESEARCHER_VS_SCIENZIATA.md` | Quando usare chi |
| `docs/guides/WORKFLOW_GUARDIANA_REVIEWER.md` | Workflow review |
| `docs/protocolli/PROTOCOLLI_BASE.md` | Protocolli condivisi |
| `tests/HARDTEST_FAMIGLIA.md` | Suite test completa |

### Scoperte
- **Ingegnera ESISTE** - audit aveva sbagliato
- **Reviewer senza Write BY DESIGN** - legge, non scrive
- **stdbuf GIA IMPLEMENTATO** - spawn-workers v3.2.0

### Prossimi Step
1. Eseguire HARDTEST famiglia (30-45 min)
2. Usare famiglia su Miracollo
3. Annotare friction, migliorare
4. Ripetere ogni sessione

---

## Sessione 144 - Cosa Fatto

### 1. Decisione BYOK
- **DECISO: BYOK per MVP**
- Zero rischio finanziario, già funzionante
- Pivot a Bundled possibile post-PMF
- Documentato in `.sncp/memoria/decisioni/20260109_BYOK_vs_bundled_da_decidere.md`

### 2. Tier System Implementato
Nuovi file creati:
- `cervella/tier/__init__.py`
- `cervella/tier/tier_manager.py`
- `cervella/cli/commands/upgrade.py`

Modifiche:
- `cervella/cli/commands/status.py` - Mostra tier + usage
- `cervella/cli/commands/task.py` - Check tier prima di eseguire
- `cervella/cli/__init__.py` - Registrato comando upgrade

### 3. Tier Disponibili

| Tier | Agenti | Task/mese | Prezzo |
|------|--------|-----------|--------|
| Free | 3 base | 50 | $0 |
| Pro | 16 tutti | Illimitati | $20 |
| Team | 16 tutti | Illimitati | $40 |
| Enterprise | 16+ | Illimitati | $60+ |

### 4. Nuovi Comandi CLI
```bash
cervella status              # Mostra tier + usage + agenti
cervella upgrade             # Confronto tier
cervella upgrade --set pro   # Dev mode: imposta tier
```

### 5. Persistenza
- Tier e usage salvati in `.sncp/tier.yaml`
- Reset automatico usage ogni mese

---

## Sessione 143 - Cosa Fatto (Precedente)

### 1. Code Review Day (Venerdì)
- cervella-reviewer ha analizzato tutto il CLI
- Score: 7.5/10 → migliorato con fix

### 2. Fix Security (2 CRITICAL)
- `api/client.py`: API key ora privata (`__api_key`) + validazione formato
- `cli/commands/checkpoint.py`: Distingue errori git soft/hard

### 3. Fix Quality (4 WARNING)
- Input validation con sanitize + length check
- Modelli configurabili via env vars
- Rollback automatico se init fallisce
- Context manager per API client lifecycle

### 4. Famiglia Completa (16 Agenti)
Aggiunti 8 agenti mancanti:
- **Worker (Sonnet):** data, devops, security, marketing, ingegnera
- **Supervisori (Opus):** guardiana-ops, guardiana-qualita, guardiana-ricerca

### 5. Setup Ambiente
- `cervella` aggiunto al PATH (`~/.zshrc`)
- API key Anthropic configurata
- Test con API reale: FUNZIONA!

### 6. Ricerca Pricing Modulare
- cervella-scienziata ha fatto analisi completa
- Risultato: **NO-GO per a la carte**, tutti i competitor usano tier flat
- Report: `.sncp/idee/RICERCA_PRICING_MODULARE.md`

---

## CLI - Stato Tecnico

### Struttura
```
cervella/
├── pyproject.toml          # Package config
├── README.md               # Documentazione
├── cli/
│   ├── __init__.py
│   ├── __main__.py
│   └── commands/
│       ├── init.py         # cervella init
│       ├── task.py         # cervella task (con sanitize!)
│       ├── status.py       # cervella status
│       └── checkpoint.py   # cervella checkpoint
├── api/
│   └── client.py           # Claude API wrapper (BYOK, secure)
├── sncp/
│   └── manager.py          # Memoria esterna (con rollback!)
├── agents/
│   └── loader.py           # 16 agenti built-in
└── tests/
    ├── test_basic.py
    └── test_structure.py   # 7/7 PASS
```

### Comandi
```bash
cervella --version          # v0.1.0
cervella init               # Crea .sncp/
cervella status             # 16 agenti pronti
cervella status --verbose   # Dettagli agenti
cervella task "..."         # Regina decide agente
cervella task "..." --agent backend  # Specifica agente
cervella task "..." --dry-run        # Preview
cervella checkpoint -m "..."         # Salva stato
cervella checkpoint --git -m "..."   # + git commit
```

### 16 Agenti

**Worker (Sonnet - 12):**
| Agente | Specializzazione |
|--------|------------------|
| backend | Python, FastAPI, DB |
| frontend | React, CSS, UI |
| tester | Testing, QA |
| researcher | Ricerca tecnica |
| scienziata | Ricerca strategica |
| docs | Documentazione |
| reviewer | Code review |
| data | SQL, Analytics |
| devops | Deploy, Docker |
| security | Audit, OWASP |
| marketing | UX Strategy |
| ingegnera | Analisi codebase |

**Supervisori (Opus - 4):**
| Agente | Ruolo |
|--------|-------|
| regina | Orchestratrice principale |
| guardiana-ops | Supervisione operazioni |
| guardiana-qualita | Verifica qualità |
| guardiana-ricerca | Verifica ricerche |

---

## Pricing Strategy (DEFINITO)

### Struttura Tier Flat

| Tier | Prezzo | Agenti | Task | Target |
|------|--------|--------|------|--------|
| Free | $0 | 3 base | 50/mese | Hobby, trial |
| Pro | $20/mese | 16 tutti | Unlimited | Individual dev |
| Team | $40/user | 16 tutti | Unlimited | Team |
| Enterprise | $60+ | 16 + custom | Unlimited | Enterprise |

### Perché Tier Flat
- Tutti i competitor lo usano (Cursor, Copilot, Windsurf)
- -15-20% conversion con a la carte
- Complessità tecnica proibitiva per modulare
- Report completo: `.sncp/idee/RICERCA_PRICING_MODULARE.md`

---

## Decisione Aperta: BYOK vs Bundled

**DA DECIDERE PRIMA DEL LAUNCH**

| Opzione | Pro | Contro |
|---------|-----|--------|
| **BYOK** | Zero costi API, già funziona | Friction onboarding, utente paga 2x |
| **Bundled** | UX semplice, come competitor | Rischio margine, serve capitale |
| **Hybrid** | Flessibilità | Complessità |

**Raccomandazione preliminare:** BYOK per MVP, Bundled post-PMF

**Dettagli:** `.sncp/memoria/decisioni/20260109_BYOK_vs_bundled_da_decidere.md`

---

## Cosa Manca per Launch

### Alta Priorità
| # | Task | Effort | Dipendenze |
|---|------|--------|------------|
| 1 | Decidere BYOK vs Bundled | 1 giorno | - |
| 2 | Implementare tier limits nel CLI | 2-3 giorni | Decisione #1 |
| 3 | User interviews (10-20) | 1-2 sett | - |
| 4 | Billing system (Stripe) | 1 sett | Decisione #1 |
| 5 | Update landing page con pricing | 2-3 giorni | #4 |

### Media Priorità
| # | Task | Effort |
|---|------|--------|
| 6 | Aumentare test coverage (80%+) | 1 sett |
| 7 | PyPI publish | 1 giorno |
| 8 | Documentazione utente | 2-3 giorni |

### Bassa Priorità (Post-Launch)
| # | Task |
|---|------|
| 9 | Web dashboard |
| 10 | Team Packs (add-on opzionale) |
| 11 | Enterprise features (SSO, self-hosted) |

---

## Configurazione Ambiente Rafa

```bash
# ~/.zshrc contiene:
export ANTHROPIC_API_KEY="sk-ant-..."
export PATH="$HOME/Library/Python/3.13/bin:$PATH"

# Per usare:
cd ~/Developer/CervellaSwarm
cervella status
```

---

## Puntatori Importanti

| Cosa | Dove |
|------|------|
| CLI source | `cervella/` |
| README CLI | `cervella/README.md` |
| Code Review Report | `.sncp/reports/CODE_REVIEW_CLI_2026_01_09.md` |
| Ricerca Pricing | `.sncp/idee/RICERCA_PRICING_MODULARE.md` |
| Decisione BYOK | `.sncp/memoria/decisioni/20260109_BYOK_vs_bundled_da_decidere.md` |
| Idea Pricing Modulare | `.sncp/idee/IDEA_PRICING_MODULAR_AGENTS.md` |
| Mappa App Vera | `.sncp/idee/MAPPA_APP_VERA.md` |
| NORD | `NORD.md` |

---

## Git Status

- Branch: main
- Commit pending: Sessione 143 completa
- Da pushare dopo commit

---

## Decisioni Sessione 143

| Cosa | Decisione | Perché |
|------|-----------|--------|
| API key privata | `__api_key` + validazione | Security |
| Modelli config | Via env vars | Future-proofing |
| 16 agenti | Famiglia completa | Copertura task |
| Pricing | Tier flat $0/$20/$40/$60+ | Market standard |
| Modulare | NO-GO | -15-20% conversion |
| BYOK vs Bundled | DA DECIDERE | Business model |

---

## Per la Prossima Sessione

1. **Leggi** questo file + decisione BYOK
2. **Decidi** BYOK vs Bundled con Rafa
3. **Implementa** tier limits nel CLI
4. **Pianifica** user interviews

---

## Filosofia

> "Lavoriamo in PACE! Senza CASINO!"
> "Fatto BENE > Fatto VELOCE"
> "La MAGIA ora è nascosta! Con coscienza!"
> "Ultrapassar os próprios limites!"

---

*Sessione 143: CLI Production Ready + Pricing Definito*
*Con il cuore pieno!*

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

## AUTO-CHECKPOINT: 2026-01-10 18:55 (unknown)

### Stato Git
- **Branch**: main
- **Ultimo commit**: aba8238 - Sessione 152: Orchestrato MEGA DEPLOY Miracollo!
- **File modificati** (2):
  - sncp/stato/oggi.md
  - reports/engineer_report_20260110_184924.json

### Note
- Checkpoint automatico generato da hook
- Trigger: unknown

---
