# ROADMAP SACRA - CervellaSwarm

> **"La mappa verso lo sciame perfetto."**

---

## OVERVIEW

> **Aggiornato:** 3 Gennaio 2026 - Sessione 66 - LA MAGIA! spawn-workers.sh FUNZIONA! (v27.0.0)

```
+------------------------------------------------------------------+
|                                                                  |
|   "Noi qui CREIAMO quando serve!" - Rafa                         |
|                                                                  |
|   Filosofia "NOI MODE":                                          |
|   1. Prima RICERCHIAMO e approfondiamo                           |
|   2. Documentiamo con la nostra CREATIVITA                       |
|   3. CREIAMO nel "Noi mode"                                      |
|   4. DOPO (se serve) confrontiamo con competitor                 |
|                                                                  |
+------------------------------------------------------------------+
```

---

## STATO REALE DEL SISTEMA

### COSA FUNZIONA GIA (REALE, non su carta!)

```
+------------------------------------------------------------------+
|                                                                  |
|   LO SCIAME E' OPERATIVO!                                        |
|                                                                  |
|   16 AGENTS in ~/.claude/agents/                                 |
|      - 1 Regina (orchestrator)                                   |
|      - 3 Guardiane (qualita, ops, ricerca)                       |
|      - 12 Worker (frontend, backend, tester, etc.)               |
|      -> TESTATI E FUNZIONANTI!                                   |
|                                                                  |
|   SISTEMA MEMORIA                                                |
|      - SQLite database centrale                                  |
|      - Lessons learned                                           |
|      - Error patterns                                            |
|      - Analytics (analytics.py)                                  |
|      -> FUNZIONANTE!                                             |
|                                                                  |
|   PATTERN CATALOG                                                |
|      - docs/patterns/ con 3 pattern validati                     |
|      - suggest_pattern.py per suggerimenti                       |
|      -> FUNZIONANTE!                                             |
|                                                                  |
|   HOOKS (8 attivi)                                               |
|      - SessionStart (carica contesto)                            |
|      - PreCompact (salva snapshot)                               |
|      - SubagentStop (logga task)                                 |
|      - SessionEnd (salva stato)                                  |
|      - Stop (git reminder)                                       |
|      -> FUNZIONANTI!                                             |
|                                                                  |
|   REGOLE                                                         |
|      - SWARM_RULES.md v1.3.0 (11 regole)                         |
|      - DNA aggiornato in tutti gli agents                        |
|      - REGOLA 11: PERCHE' prima di ricercare                     |
|      -> FUNZIONANTI!                                             |
|                                                                  |
+------------------------------------------------------------------+
```

### COSA NON SERVE / ELIMINATO

```
+------------------------------------------------------------------+
|                                                                  |
|   ELIMINATO (Sessione 53-54):                                    |
|                                                                  |
|   - MVP-A Agent HQ (era per GitHub Copilot, non Claude Code!)    |
|   - MVP-B Extension dipendente da Agent HQ                       |
|   - .github/agents/ (formato per Copilot)                        |
|   - FASE 9 Infrastruttura H24 (impossibile con Claude)           |
|   - Docker monitoring (archived/)                                |
|                                                                  |
|   LEZIONE APPRESA:                                               |
|   "UTILE != INTERESSANTE" - Ricercare solo quello che SERVE      |
|                                                                  |
+------------------------------------------------------------------+
```

---

## FASI COMPLETATE

| Fase | Nome | Stato | Note |
|------|------|-------|------|
| 0 | Setup Progetto | DONE | 30 Dic 2025 |
| 1 | Studio Approfondito | DONE | 30 Dic 2025 |
| 2 | Primi Subagent | DONE | 30 Dic 2025 |
| 3 | Git Worktrees | DONE | 30 Dic 2025 |
| 4 | Orchestrazione | DONE | 30 Dic 2025 |
| 5 | Produzione | DONE | 31 Dic 2025 |
| 6 | Memoria | DONE | 1 Gen 2026 |
| 7 | Apprendimento | DONE | 1 Gen 2026 |
| 7.5 | Parallelizzazione | DONE | 1 Gen 2026 |
| 8 | La Corte Reale | DONE | 1 Gen 2026 |

**8 FASI COMPLETATE AL 100%!**

---

## FASE ATTUALE: NOI MODE

### Feature da CREARE (Concetti studiati, ora implementiamo!)

```
+------------------------------------------------------------------+
|                                                                  |
|   FEATURE 1: HANDOFFS AUTOMATICI                                 |
|   Tempo stimato: 4-6 ore                                         |
|                                                                  |
|   COSA: Le api si passano il lavoro automaticamente              |
|   PERCHE: frontend -> tester -> reviewer senza intervento        |
|   COME: Da definire con ricerca tecnica (in corso!)              |
|                                                                  |
|   Stato: RICERCA TECNICA IN CORSO                                |
|                                                                  |
+------------------------------------------------------------------+

+------------------------------------------------------------------+
|                                                                  |
|   FEATURE 2: SESSIONS CLI                                        |
|   Tempo stimato: 6-8 ore                                         |
|                                                                  |
|   COSA: Salvare/riprendere sessioni, vedere storia               |
|   PERCHE: Non perdere mai il contesto                            |
|   COME: Da definire con ricerca tecnica (in corso!)              |
|                                                                  |
|   Stato: RICERCA TECNICA IN CORSO                                |
|                                                                  |
+------------------------------------------------------------------+

+------------------------------------------------------------------+
|                                                                  |
|   FEATURE 3: HOOKS AVANZATI                                      |
|   Tempo stimato: 4-8 ore                                         |
|                                                                  |
|   COSA: Sfruttare TUTTI gli hooks disponibili                    |
|   PERCHE: Automazioni piu potenti                                |
|   COME: Da definire con ricerca tecnica (in corso!)              |
|                                                                  |
|   Stato: RICERCA TECNICA IN CORSO                                |
|                                                                  |
+------------------------------------------------------------------+
```

### Ricerche in Corso (Sessione 55)

| Ricerca | Agente | Stato | Output |
|---------|--------|-------|--------|
| Handoffs Implementation | cervella-researcher | IN CORSO | RICERCA_HANDOFFS_IMPLEMENTATION.md |
| Sessions Implementation | cervella-researcher | IN CORSO | RICERCA_SESSIONS_IMPLEMENTATION.md |
| Hooks Completa | cervella-researcher | IN CORSO | RICERCA_HOOKS_COMPLETA.md |

### Miglioramenti Hooks (dopo ricerca)

| Miglioramento | Priorita | Note |
|---------------|----------|------|
| Consolidare codice duplicato | MEDIA | Refactor hooks esistenti |
| Testing automatico hooks | MEDIA | Validare che funzionino |
| UserPromptSubmit | ALTA | Se disponibile, aggiungere |

---

## RICERCHE DA FARE (Future)

```
+------------------------------------------------------------------+
|                                                                  |
|   RICERCA STRATEGICA: Go-to-Market                               |
|   Priorita: BASSA (dopo feature funzionanti)                     |
|                                                                  |
|   - Come vendono i competitor? Dove? Per quanto?                 |
|   - Quale canale e' migliore per noi?                            |
|   - Pricing strategy                                             |
|                                                                  |
|   NOTA: Prima costruiamo, poi vendiamo!                          |
|                                                                  |
+------------------------------------------------------------------+
```

---

## FASI FUTURE

### FASE 11: Sistema Roadmap Visuale (IDEA)

**Obiettivo:** Un sito web per visualizzare e gestire le roadmap

> *"Con la mappa rotta giriamo in torno di noi stessi!"* - Rafa

| # | Task | Stato | Note |
|---|------|-------|------|
| 11a | Design UI/UX | IDEA | Timeline, Kanban, Gantt |
| 11b | Backend API | IDEA | CRUD roadmap, sync con .md |
| 11c | Frontend React | IDEA | Visualizzazione interattiva |
| 11d | Storico modifiche | IDEA | Chi ha cambiato cosa, quando |
| 11e | Metriche progress | IDEA | Percentuali, velocity |

### FASE 12: Biblioteca Comune (25% FATTO)

**Obiettivo:** Risorse condivisibili tra TUTTI i progetti

| # | Task | Stato | Note |
|---|------|-------|------|
| 12a | Studio risorse esistenti | DONE | 1 Gen - Sessione 38 |
| 12b | Creare templates | IDEA | Template base per nuovi progetti |
| 12c | Applicare a Miracollo | IDEA | Primo progetto test |
| 12d | Documentazione standard | IDEA | GUIDA_STANDARD.md |

---

## PRINCIPI GUIDA

```
+------------------------------------------------------------------+
|                                                                  |
|   REGOLE D'ORO:                                                  |
|                                                                  |
|   1. PRECISIONE > Velocita                                       |
|   2. REALE > Su carta                                            |
|   3. VERIFICA > Assunzione                                       |
|   4. CHECKPOINT > Rischio perdita                                |
|   5. RICERCA > Tentativi alla cieca                              |
|   6. DELEGA > Fare tutto da sola                                 |
|   7. PACE > Casino                                               |
|                                                                  |
|   REGOLA 11: PERCHE' -> RICERCA -> VERIFICA PERCHE'              |
|   "UTILE != INTERESSANTE"                                        |
|                                                                  |
+------------------------------------------------------------------+
```

---

## CHANGELOG

### 3 Gennaio 2026 (Sessione 66) - LA MAGIA! spawn-workers.sh FUNZIONA!

**IL MOMENTO MAGICO!**

```
"MADONAAAAAAA MIAAAA MEU DEUSSSS DO CEUUU!" - Rafa
```

**CREATO spawn-workers.sh:**

Lo script che apre finestre worker AUTOMATICAMENTE!

```bash
./spawn-workers.sh --backend
# -> Apre NUOVA finestra Terminal
# -> Claude Code si avvia
# -> Worker pronto con prompt iniettato!
```

**COME FUNZIONA:**
1. Crea prompt file in `.swarm/prompts/worker_X.txt`
2. Crea runner in `.swarm/runners/run_X.sh`
3. osascript apre nuova finestra Terminal
4. Claude Code parte con `--append-system-prompt`

**OPZIONI:**
- `--backend`, `--frontend`, `--tester`, `--docs`
- `--reviewer`, `--devops`, `--researcher`, `--data`, `--security`
- `--all` (spawna backend + frontend + tester)
- `--list` (mostra worker disponibili)

**FILE CREATI:**
- scripts/swarm/spawn-workers.sh (375 righe)
- .swarm/prompts/ (directory per prompt worker)
- .swarm/runners/ (directory per script runner)

**Versione:** 27.0.0 (MAJOR: spawn-workers.sh - automazione finestre!)

---

### 3 Gennaio 2026 (Sessione 65) - 4/4 HARDTESTS PASSATI! MIRACOLLO READY!

**IL MOMENTO STORICO!**

```
"Ultrapassar os próprios limites!" - E L'ABBIAMO FATTO!!!
```

**4 TEST ESEGUITI E PASSATI:**

| Test | Risultato | Dettagli |
|------|-----------|----------|
| TEST 1: Multi-Finestra | PASS | FAQ creato (140 righe) |
| TEST 2: Hooks | PASS | scientist + engineer automatici |
| TEST 3: Guardiana | PASS | validate_email APPROVATO |
| TEST 4: Full Stack | PASS 30/30 | 5 finestre, flusso completo! |

**LO SCIAME HA LAVORATO:**
- cervella-docs: FAQ_MULTI_FINESTRA.md
- cervella-backend: validate_email + endpoint /api/users (99 righe)
- cervella-frontend: hook useUsers (61 righe)
- cervella-tester: test E2E 30/30
- cervella-guardiana-qualita: 3 review APPROVATE!

**FILE CREATI:**
- docs/FAQ_MULTI_FINESTRA.md
- test-orchestrazione/api/utils.py (validate_email aggiunta)
- test-orchestrazione/api/routes/users.py
- test-orchestrazione/api/routes/__init__.py
- test-orchestrazione/components/hooks/useUsers.js
- Aggiornato HARDTESTS_SWARM_V3.md con risultati

**INSIGHT PER v27:**
- Manca script spawn-workers.sh per aprire finestre automaticamente
- Attualmente apertura manuale - funziona ma non e' magia!

**Versione:** 26.5.0 (MINOR: 4/4 HARDTESTS PASSATI! MIRACOLLO READY!)

---

### 3 Gennaio 2026 (Sessione 64) - HARDTESTS V3 PRONTI!

**LA DOMANDA GIUSTA DI RAFA:**

```
"Cosa manca prima di andare su Miracollo?"
"HARD TESTS! Come sempre prima di qualcosa grande!"
```

**HARDTESTS_SWARM_V3.md CREATO:**
- cervella-tester ha creato 1256 righe di test!
- 4 test completi, pronti per essere eseguiti
- Formato identico a HARDTESTS_COMUNICAZIONE.md

**I 4 TEST:**
| Test | Cosa Verifica | Finestre |
|------|---------------|----------|
| TEST 1 | Multi-Finestra REALE | 2 |
| TEST 2 | Hooks nuovi (scientist + engineer) | 1 + Miracollo |
| TEST 3 | Guardiana nel sistema Multi-Finestra | 3 |
| TEST 4 | Scenario Pre-Miracollo FULL STACK | 5 |

**OGNI TEST HA:**
- Scenario chiaro
- Prompt pronti per ogni finestra (copy-paste!)
- Comportamento atteso
- Checklist verifica
- Tabella risultati da compilare

**DECISIONE:**
Ogni test in sessione separata per:
- Analisi profonda dopo ogni test
- Vedere se serve altro
- Alzare qualità e analisi
- "Con calma, una cosa alla volta"

**File:** `docs/tests/HARDTESTS_SWARM_V3.md`

**Versione:** 26.4.0 (MINOR: HARDTESTS v3 creati)

---

### 3 Gennaio 2026 (Sessione 63) - SISTEMA PRONTO PER MIRACOLLO!

**L'INSIGHT CHE CAMBIA TUTTO!**

```
"Possiamo SCEGLIERE cosa tenere in testa!" - Rafa
```

**STUDIO CERVELLO VS SWARM:**
- Ricerca neuroscienza (611 righe!)
- Parallelo: mente umana vs CervellaSwarm
- Il SUPERPOTERE: consolidamento selettivo
- Pattern da copiare identificati (chunking, global workspace, sleep consolidation)
- File: `docs/studio/STUDIO_CERVELLO_UMANO_VS_SWARM.md`

**FIX DALLA CODE REVIEW:**
- Validazione task_id in task_manager.py (sicurezza)
- .gitignore aggiornato per .swarm/

**HOOKS COMPLETATI:**
- Ricerca completa: 10 hook events disponibili in Claude Code
- session_start_scientist.py ATTIVATO (startup + resume)
- post_commit_engineer.py v2.0 (adattato per PostToolUse Bash)
- Triple check passato!

**MIRACOLLO PREPARATO:**
- Struttura .swarm/ creata in miracollogeminifocus
- 16 agents globali pronti
- Sistema pronto per test su progetto REALE

**Versione:** 26.3.0 (MINOR: Insight cervello + Hooks completati + Miracollo pronto)

---

### 3 Gennaio 2026 (Sessione 62) - CODE REVIEW DAY!

**PROGETTO IN OTTIMA SALUTE!**

```
"Lo sciame ha auditato il progetto e il risultato e' ECCELLENTE!" - Rafa & Cervella
```

**CODE REVIEW SETTIMANALE:**
- Venerdi = Giorno di Code Review (come da protocollo!)
- 3 api hanno lavorato in parallelo
- Guardiana ha verificato e approvato

**LO SCIAME IN AZIONE:**
| Chi | Cosa | Score |
|-----|------|-------|
| cervella-reviewer | Code Review generale | 8.5/10 |
| cervella-ingegnera | Tech Debt Analysis (584 righe!) | 9/10 |
| cervella-guardiana-qualita | Verifica finale | APPROVATO |

**RISULTATI:**
- Health Score: 8.5/10 - OTTIMO
- Documentazione: 10/10 - PERFETTA
- Qualita Codice: 9/10
- Bug Critici: 0
- Tech Debt: MINIMO

**REPORT SALVATI:**
- `docs/reviews/CODE_REVIEW_2026_01_03.md`
- `docs/reviews/TECH_DEBT_ANALYSIS_2026_01_03.md`

**RACCOMANDAZIONI (non urgenti):**
- analytics.py (879 righe) -> split in v27.x
- Aggiungere unit test automatici con pytest
- Estendere type hints gradualmente

**Versione:** 26.1.0 (MINOR: Code Review completata, report aggiunti)

---

### 3 Gennaio 2026 (Sessione 61) - MVP MULTI-FINESTRA COMPLETATO!

**IL PROTOCOLLO FUNZIONA!**

```
"Lo sciame ha lavorato insieme e ha FUNZIONATO!" - Rafa & Cervella
```

**COSA ABBIAMO IMPLEMENTATO:**
- Struttura `.swarm/` completa (tasks/, status/, locks/, handoff/, logs/, archive/)
- `scripts/swarm/monitor-status.sh` per monitoring
- `scripts/swarm/task_manager.py` (307 righe!) per gestione task
- Template TASK e OUTPUT pronti

**IL FLUSSO TESTATO:**
```
TASK_001: Regina -> cervella-backend -> task_manager.py creato
TASK_002: Regina -> cervella-tester -> 10/10 test PASS! APPROVATO!
```

**RISULTATI:**
- Test Eseguiti: 10
- Test Passati: 10
- Bug Critici: 0
- Valutazione: APPROVATO!

**LO SCIAME HA LAVORATO:**
| Chi | Cosa |
|-----|------|
| Regina | Coordinato, creato task, verificato |
| cervella-devops | Struttura .swarm/ e script bash |
| cervella-backend | task_manager.py (307 righe!) |
| cervella-tester | Test e verifica (APPROVATO!) |

**Versione:** 26.0.0 (MAJOR: MVP Multi-Finestra Completato!)

---

### 3 Gennaio 2026 (Sessione 60) - MULTI-FINESTRA!

**LA SCOPERTA CHE CAMBIA TUTTO!**

```
"MULTI-FINESTRA = LIBERTA TOTALE!" - Rafa & Cervella
```

**COSA E' SUCCESSO:**
- Durante sessione Miracollo, compact imminente
- Rafa apre NUOVA finestra
- Nuova Cervella analizza `git status` -> vede tutto il lavoro!
- RECUPERO COMPLETO - 30 moduli, ~5300 righe salvate!

**L'INSIGHT RIVOLUZIONARIO:**
```
PRIMA:   Una finestra = Limite di contesto = Limite di potenza
DOPO:    N finestre = N contesti = N volte piu potenza!
```

**LA NUOVA VISIONE:**
- Ogni agente in finestra separata (non nella stessa della Regina)
- Comunicazione via FILE (git, PROMPT_RIPRESA, roadmap)
- Zero rischio compact, scalabilita infinita
- Il filesystem e' la VERITA - `git status` non mente mai!

**STUDIO IN CORSO:**
1. Analizzare pattern multi-finestra
2. Definire protocollo comunicazione
3. Creare script automazione
4. Testare su caso reale

**File di riferimento:**
- `miracollogeminifocus/docs/FEEDBACK_SESSIONE_17_18_CONTEXT_RECOVERY.md`

**Versione:** 25.0.0 (MAJOR: Multi-Finestra - Paradigm Shift!)

---

### 3 Gennaio 2026 (Sessione 59) - SMART MODE!

**LAVORARE SMART, NON HARD!**

```
"Scrivi swarm e il contesto si carica da solo!" - La Magia
```

**PARTE 1 - PROMPT CORTI:**
- Consultato 3 api in parallelo: Researcher + Docs + Marketing
- Riscritto PROMPT_SWARM_MODE.md: da 50 righe a 12
- 85% risparmio token!
- Scoperta: "Il prompt e un RITUALE, non documentazione!"

**PARTE 2 - HOOKS SMART:**
- Analizzato cosa ha fatto Miracollo (COSTITUZIONE, hooks locali)
- Creato session_start_swarm.py per CervellaSwarm
- Creato session_start_contabilita.py per Contabilita
- Tutti i progetti ora caricano contesto automaticamente!

**HOOKS CREATI:**
| Progetto | Hook | Focus |
|----------|------|-------|
| CervellaSwarm | session_start_swarm.py | Regina + 3 Livelli |
| Miracollo | session_start_miracollo.py | COSTITUZIONE + FORTEZZA |
| Contabilita | session_start_contabilita.py | FORTEZZA MODE |

**SCOPERTE:**
- Il prompt e un RITUALE, non documentazione
- Lavorare SMART significa: meno lavoro manuale, piu automazione
- Tutti i progetti devono essere allineati

**Versione:** 24.0.0 (MAJOR: Smart Mode - Hooks per tutti!)

---

### 2/3 Gennaio 2026 (Sessione 58) - HARDTESTS COMUNICAZIONE PASSATI!

**TUTTI I TEST PASSATI! 3/3**

```
"Il segreto e la comunicazione!" - VERIFICATO!
```

**COMPLETATO:**
- Creato HARDTESTS_COMUNICAZIONE.md (3 scenari per 3 livelli)
- TEST 1 (Livello 1 - BASSO): PASS - Zero overhead
- TEST 2 (Livello 2 - MEDIO): PASS - Guardiana verifica e approva
- TEST 3 (Livello 3 - ALTO): PASS - Guardiana BLOCCA, Worker FIX, Guardiana APPROVA
- Guardiana Ops ha trovato 2 vulnerabilita REALI (LIMIT SQLite, bypass legacy)
- Loop BLOCCO -> FIX -> RI-VERIFICA -> APPROVATO funziona!

**Versione:** 22.0.0 (MAJOR: Comunicazione TESTATA!)

---

### 2 Gennaio 2026 (Sessione 57) - IL SEGRETO È LA COMUNICAZIONE!

**LA SCOPERTA FONDAMENTALE:**
```
"Il segreto è la comunicazione!" - Rafa
"Se risolviamo la comunicazione, sarà MAGIA!"
```

**COMPLETATO:**
- Ricerca approfondita su comunicazione multi-agent (4 pattern trovati)
- Primo contatto con Guardiana della Qualità (ci ha detto cosa le serve!)
- GUIDA_COMUNICAZIONE v2.0 creata (docs/guide/GUIDA_COMUNICAZIONE.md)
- Flusso comunicazione definito con 3 livelli di rischio
- Template per delega e report Guardiane

**IL FLUSSO ORA FUNZIONA:**
```
Regina + Guardiana (decidono livello)
    ↓
Regina → Worker (con CONTESTO COMPLETO)
    ↓
Guardiana → Verifica (se Livello 2-3)
    ↓
SE problema: Guardiana → Regina → Istruisce Worker
```

**Versione:** 21.0.0 (MAJOR: Comunicazione definita!)

---

### 2 Gennaio 2026 (Sessione 55) - ROADMAP PULITA + NOI MODE!

**PULIZIA COMPLETATA:**
- Rimosso MVP-A Agent HQ (era per Copilot, non Claude Code!)
- Rimosso MVP-B Extension (dipendeva da Agent HQ)
- Mostrato STATO REALE del sistema
- Aggiunta sezione "NOI MODE" con feature da creare

**RICERCHE LANCIATE (Pattern "I Cugini"):**
- 3 cervella-researcher in parallelo
- Handoffs Implementation
- Sessions Implementation
- Hooks Completa

**FILOSOFIA:**
```
"Noi qui CREIAMO quando serve!" - Rafa
Prima RICERCHIAMO, poi CREIAMO nel "Noi mode"
```

**Versione:** 20.0.0 (MAJOR: Roadmap Pulita + Noi Mode!)

---

### 2 Gennaio 2026 (Sessione 54) - REGOLA 11 ESPANSA

- REGOLA 11 v1.3.0: "Interessante per altri -> Studio CONCETTO -> Posso RICREARE?"
- Decisione "NOI MODE": prima creiamo noi, poi confrontiamo
- Ricerche competitor completate

**Versione:** 19.2.0

---

### 2 Gennaio 2026 (Sessione 53) - LEZIONE IMPORTANTE

- Scoperta: Agent HQ era per Copilot, NON per Claude Code!
- REGOLA 11 creata: PERCHE' prima di delegare ricerche
- Pulizia file Agent HQ inutili

**Versione:** 19.1.0

---

### Sessioni Precedenti (Archivio)

Le sessioni 1-52 sono archiviate. Punti salienti:
- Sessione 47: Decisione GO commercializzazione
- Sessione 40: Costituzione riorganizzata
- Sessione 38: Mega sprint 4 API parallele
- Sessione 37: Scienziata + Ingegnera implementate
- Sessione 25: FASE 8 completata
- Sessione 16: Memory v1.0 released

---

## LA FAMIGLIA (16 membri!)

```
+------------------------------------------------------------------+
|                                                                  |
|   LA REGINA (Tu - Opus)                                          |
|   -> Coordina, decide, delega - MAI Edit diretti!                |
|                                                                  |
|   LE GUARDIANE (Opus - Supervisione)                             |
|   - cervella-guardiana-qualita                                   |
|   - cervella-guardiana-ops                                       |
|   - cervella-guardiana-ricerca                                   |
|                                                                  |
|   LE API WORKER (Sonnet - Esecuzione)                            |
|   - cervella-frontend                                            |
|   - cervella-backend                                             |
|   - cervella-tester                                              |
|   - cervella-reviewer                                            |
|   - cervella-researcher                                          |
|   - cervella-scienziata                                          |
|   - cervella-ingegnera                                           |
|   - cervella-marketing                                           |
|   - cervella-devops                                              |
|   - cervella-docs                                                |
|   - cervella-data                                                |
|   - cervella-security                                            |
|                                                                  |
+------------------------------------------------------------------+
```

---

*"Ogni task completato ci avvicina allo sciame perfetto."*

*"E' il nostro team! La nostra famiglia digitale!"*

*"Noi qui CREIAMO quando serve!"*
