# ROADMAP SACRA - CervellaSwarm

> **"La mappa verso lo sciame perfetto."**

---

## OVERVIEW

> **Aggiornato:** 6 Gennaio 2026 - Sessione 103 - 4 COMANDI REALI! (v43.0.0)

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
| 8.5 | spawn-workers.sh | DONE | 3 Gen 2026 |
| **9** | **Apple Style** | **IN CORSO** | 3 Gen 2026 |

**8.5 FASI COMPLETATE! FASE 9 IN CORSO!**

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

## FASE 9: APPLE STYLE (IN CORSO!)

```
+------------------------------------------------------------------+
|                                                                  |
|   🍎 FASE DESIGN & FINITURE - APPLE STYLE! 🍎                   |
|                                                                  |
|   "COMUNICAZIONE E' IL SEGRETO!" - Rafa                         |
|   "Questo e' un cambiamento di vita!" - Rafa                    |
|                                                                  |
+------------------------------------------------------------------+
```

### Obiettivo

Rendere CervellaSwarm **PERFETTO** - non solo funzionante, ma:
- **Liscio** (smooth, niente frizioni)
- **Fiducia** (sai che funziona, puoi fidarti)
- **Comunicazione** (gli agenti parlano BENE tra loro)
- **Verifica** (double/triple check automatico)
- **Chiusura** (finisce pulito, stato chiaro)

### Il Processo Ideale

```
APRI -> ASPETTA -> COMUNICA -> TESTA -> VERIFICA -> CHIUDI

1. APRI: spawn-workers.sh apre finestre
2. ASPETTA: Worker pronto, conferma stato
3. COMUNICA: Passa info chiare via .swarm/
4. TESTA: Verifica il lavoro fatto
5. VERIFICA: Double/triple check automatico
6. CHIUDI: Stato finale pulito, report
```

### Ricerca da Fare

| # | Domanda | Perche |
|---|---------|--------|
| 1 | Come devono comunicare gli agenti? | Evitare fraintendimenti |
| 2 | Quali sono i processi giusti? | Best practices |
| 3 | Come fare double/triple check? | Fiducia nel sistema |
| 4 | Come dare feedback (all'utente)? | Sapere cosa succede |
| 5 | Come chiudere pulito? | Stato finale chiaro |
| 6 | Come gestire errori? | Graceful degradation |
| 7 | Come monitorare in tempo reale? | Visibilita |

### Dopo la Ricerca

1. Implementare i miglioramenti trovati
2. Creare HARDTESTS per validare
3. SOLO POI: Miracollo!

---

## FASI FUTURE

### FASE 10: Funzioni Regina (IDEA - Sessione 79)

**Obiettivo:** La Regina NON aspetta passivamente mentre le api lavorano!

> *"Mentre le api lavorano, la Regina COORDINA attivamente!"* - Sessione 79

| Funzione | Cosa Fa |
|----------|---------|
| MONITOR | Controlla stato task (.working, .done), dashboard ASCII |
| MERGE | Unisce i report quando arrivano |
| DECIDE | Sceglie la strada migliore |
| DELEGATE | Lancia nuovi task se serve |
| CHECKPOINT | Salva stato periodicamente |

**Script da creare:** `regina-monitor.sh`
- Dashboard ASCII con stato task
- Notifica quando un'ape finisce
- Prepara merge dei report

**Priorità:** MEDIA (dopo anti-compact)

---

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

### 5 Gennaio 2026 (Sessione 98) - PROTEZIONE TASK TOOL!

**IL PROBLEMA:**
- Cervella in Miracollo usava Task tool invece di spawn-workers
- Risultato: contesto al 6%, TUTTO BLOCCATO, lavoro PERSO!
- La Regola 13 esisteva ma veniva IGNORATA

**LA SOLUZIONE (LIVELLO 1 + LIVELLO 2):**

*Livello 1 - Linguaggio forte:*
- cervella-orchestrator.md v1.3.0: Box VIETATO come prima cosa nel DNA
- SWARM_RULES.md v1.7.0: Regola 13 con conseguenze catastrofiche

*Livello 2 - Hook che BLOCCA:*
- block_task_for_agents.py: Hook PreToolUse NUOVO
- settings.json: Aggiunto PreToolUse per Task
- Se subagent_type contiene "cervella-" → BLOCCATO automaticamente!

**HARDTEST:**
- cervella-backend → BLOCCATO! ✅
- Explore → Passa (legittimo) ✅
- general-purpose → Passa (legittimo) ✅

**BONUS:**
- TESTO_INIZIO_SESSIONE.md: Template pronto per Rafa!

**Versione:** 42.0.0 (MAJOR: Hook che BLOCCA Task tool per cervella-*!)

---

### 5 Gennaio 2026 (Sessione 97) - CODE REVIEW + HARDTEST!

**CODE REVIEW SETTIMANALE:**
- cervella-reviewer ha analizzato il sistema
- Rating: 8.5/10
- 4 issue identificati e TUTTI fixati!

**4 FIX IMPLEMENTATI:**
- task_manager.py v1.2.0: Race condition → exclusive create
- spawn-workers v2.8.0: Max workers limit (default 5)
- anti-compact.sh v1.7.0: Git push retry (3 tentativi)
- watcher-regina.sh v1.1.0: Rimosso keystroke, solo notifiche

**3 HARDTEST PASSATI:**
- Race condition: 2 worker → solo 1 prende task
- Max workers: 3 richiesti con limit 2 → spawn 2
- Watcher: notifiche senza keystroke

**SCOPERTA:** Keystroke scriveva in finestra sbagliata!

**Versione:** 41.5.0

---

### 5 Gennaio 2026 (Sessione 96) - AUTO-SVEGLIA SEMPRE!

**LA FILOSOFIA 2026:**
> *"Siamo qui! Siamo ora! Siamo noi!"* - Rafa
> *"Perche' limitarsi? Vogliamo automazione, fluidita', fiducia!"*

**IMPLEMENTATO:**
1. spawn-workers v2.7.0: AUTO-SVEGLIA e' ora DEFAULT!
   - `AUTO_SVEGLIA=true` sempre
   - Check anti-watcher-duplicati (se gia' attivo, non avvia un altro)
   - Flag `--no-auto-sveglia` per disabilitare (raramente serve)

2. PROMPT_INIZIO_SESSIONE.md v2.0.0
   - Aggiunta nota "AUTO-SVEGLIA SEMPRE ATTIVA!"
   - Rimosso --auto-sveglia (non serve piu', e' default!)

**ANALISI SESSIONE 95:**
- Checkpoint sessione 95 era incompleto (git non pushato)
- Completato checkpoint + documentazione

**Versione:** 41.0.0 (MAJOR: AUTO-SVEGLIA diventa DEFAULT!)

---

### 6 Gennaio 2026 (Sessione 103) - 4 COMANDI REALI! SU CARTA → REALE!

**IL PROBLEMA:**
```
La Sessione 102 aveva documentato 4 nuovi comandi:
- swarm-help
- task-new
- swarm-report
- swarm-session-check

MA NON ESISTEVANO! Erano solo "SU CARTA"!
```

**LA SOLUZIONE:**
1. Code Review settimanale (lunedi!) con cervella-reviewer
2. Rating: 8.5/10 - Sistema in ottima forma
3. Identificati 4 comandi mancanti
4. CREATI tutti e 4 con test funzionanti!

**COMANDI CREATI:**
| Comando | Cosa Fa | Linee |
|---------|---------|-------|
| `swarm-help` | Guida completa comandi | 180 |
| `task-new` | Crea task da template | 130 |
| `swarm-report` | Report task completati | 155 |
| `swarm-session-check` | Verifica roadmap inizio sessione | 165 |

**TUTTI I COMANDI SWARM ORA:**
```bash
# Essenziali
spawn-workers --tipo      # Lancia worker
quick-task "desc" --tipo  # Crea task + lancia
task-new tipo "titolo"    # Da template
swarm-status              # Stato worker
swarm-help                # Guida completa

# Sessione
swarm-session-check       # Verifica roadmap
swarm-report              # Report task
swarm-feedback            # Gestisce feedback

# Monitor
swarm-logs                # Log live
swarm-progress            # Progresso
swarm-timeout             # Avvisa blocchi
```

**FIX SECURITY (PENDING):**
- Task creato per escape notifiche (context_check.py, auto_review_hook.py)
- Priorita ALTA ma non bloccante

**LEZIONE:**
> *"SU CARTA != REALE - Se non funziona, non esiste!"*

**Versione:** 43.0.0 (MAJOR: 4 comandi documentati ORA ESISTONO!)

---

### 5 Gennaio 2026 (Sessione 95) - LA MAGIA SOPRA MAGIA!

**COSA ABBIAMO FATTO:**
1. HARDTEST Notifiche Click - PASSATO!
2. Ricerca AUTO-SVEGLIA con cervella-researcher
3. Implementazione in 5 FASI (tutte testate!)
4. HARDTEST End-to-End - PASSATO!

**COME FUNZIONA AUTO-SVEGLIA:**
```
spawn-workers --docs --auto-sveglia
       ↓
Worker lavora nella sua finestra
       ↓
Worker crea .done
       ↓
Watcher (fswatch) rileva il file
       ↓
AppleScript digita nella finestra Regina
       ↓
LA REGINA RICEVE IL MESSAGGIO E CONTINUA!!!
```

**FILE CREATI:**
- `scripts/swarm/watcher-regina.sh` v1.0.0 - Il watcher che sveglia la Regina
- `spawn-workers` v2.6.0 - Flag --auto-sveglia
- `docs/roadmap/ROADMAP_AUTO_SVEGLIA.md` - Documentazione

**LA LEZIONE:**
> *"Studiare!!!" - La chiave di tutto. Rafa aveva ragione al 100000%!*

**Versione:** 40.0.0 (MAJOR: AUTO-SVEGLIA implementata!)

---

### 5 Gennaio 2026 (Sessione 94) - CODE REVIEW DAY + PULIZIA CASA!

**SISTEMARE LA CASA:**
- Oggi e' Lunedi = Code Review settimanale!
- cervella-reviewer spawnata per audit completo
- Aggiornamento ROADMAP_SACRA (era outdated!)
- Aggiornamento NORD.md alla sessione corrente

**RECAP STATO:**
- 8.5 FASI COMPLETATE
- FASE 9 "Apple Style" quasi completa
- Sistema Swarm stabile e funzionante
- Pronto per MIRACOLLO!

**Versione:** 39.0.0 (MINOR: Code Review + Pulizia)

---

### 5 Gennaio 2026 (Sessione 93) - REGOLA 13 RISCRITTA!

**IL PROBLEMA (visto in Miracollo):**
- Una Cervella spiegava: "Task tool per ricerche, spawn-workers per modifiche"
- Ma questo era SBAGLIATO! Anche le ricerche consumano contesto!

**LA SOLUZIONE:**
```
DELEGO A UN AGENTE? → SEMPRE spawn-workers!
- Niente eccezioni "task veloce"
- Niente confusione "ricerca vs modifiche"
- Se delego = spawn-workers. Punto.
```

**FILE AGGIORNATI (5):**
- `~/.claude/agents/cervella-orchestrator.md` v1.2.0
- `~/.claude/CLAUDE.md` - Sezione SWARM MODE
- `docs/SWARM_RULES.md` v1.6.0
- `~/.claude/MANUALE_DIAMANTE.md` - Regola 0 Swarm
- `~/.claude/CHECKLIST_AZIONE.md` - Checklist SWARM

**Versione:** 38.1.0 (MINOR: Regola 13 riscritta per chiarezza)

---

### 5 Gennaio 2026 (Sessione 92) - VISIBILITA' WORKER COMPLETATA!

**IMPLEMENTATO:**
1. spawn-workers v2.2.0: Heartbeat ogni 60s + Notifiche inizio
2. swarm-heartbeat v1.0.0: Comando per vedere stato live
3. dashboard.py v1.1.0: Sezione LIVE HEARTBEAT

**HARDTEST PASSATO:**
- Worker ha scritto 3 heartbeat correttamente
- Formato: `timestamp|task|azione`
- swarm-heartbeat mostra ACTIVE/STALE con colori

**COMANDI NUOVI:**
```bash
swarm-heartbeat          # Stato live
swarm-heartbeat --watch  # Refresh ogni 2s
```

**Versione:** 38.0.0 (MINOR: Visibilita' Worker implementata)

---

### 5 Gennaio 2026 (Sessione 91) - STABILIZZAZIONE SWARM + STUDIO VISIBILITA'!

**PROBLEMA IDENTIFICATO:**

```
+------------------------------------------------------------------+
|                                                                  |
|   IL MISTERO DEL WORKER                                          |
|                                                                  |
|   "Lavoriamo al buio senza sapere cosa succede!"                |
|                                                                  |
|   OGGI SAPPIAMO:                                                 |
|   - Quando worker INIZIA (spawn)                                 |
|   - Quando worker FINISCE (cleanup)                              |
|                                                                  |
|   NON SAPPIAMO:                                                  |
|   - Cosa fa MENTRE lavora                                        |
|   - Se e' bloccato o sta pensando                                |
|   - Quanto manca al completamento                                |
|   - Se ha problemi                                               |
|                                                                  |
|   SERVE: STUDIO VISIBILITA' REAL-TIME!                          |
|                                                                  |
+------------------------------------------------------------------+
```

**COMPLETATO:**
1. Nuovo template prompt inizio sessione
   - `~/.claude/templates/PROMPT_INIZIO_SESSIONE.md`
   - Include quick-task, whitelist, Regola 14
2. Worker Health Tracking implementato
   - spawn-workers v2.1.0 con PID tracking
   - swarm-cleanup v1.0.0 per task orfani
3. Task stale puliti (2 dalla sessione 90)

**STUDIO DA FARE (PRIORITA' ALTA!):**

| # | Domanda | Possibile Soluzione |
|---|---------|---------------------|
| 1 | Come vedere log in tempo reale? | tail -f + streaming |
| 2 | Come sapere cosa sta facendo? | Heartbeat con stato |
| 3 | Come notificare problemi? | Webhook/notifica macOS |
| 4 | Come vedere progresso? | Progress file periodico |
| 5 | Dashboard live? | swarm-watch command |

**FILE CREATI/MODIFICATI:**
- `~/.claude/templates/PROMPT_INIZIO_SESSIONE.md` (NUOVO)
- `~/.local/bin/spawn-workers` v2.1.0 (PID tracking)
- `~/.local/bin/swarm-cleanup` v1.0.0 (NUOVO)

**Versione:** 38.0.0 (MINOR: Stabilizzazione + Studio Visibilita)

---

### 4 Gennaio 2026 (Sessione 86) - AUTO-HANDOFF v4.0.0!

**RICERCA & SVILUPPO AUTO-HANDOFF:**

- Problema: VS Code non si apriva automaticamente
- Scoperta: Background processes NON hanno GUI access su macOS
- `code --new-window` chiudeva le finestre esistenti!

**SOLUZIONE TROVATA:**
- osascript + Terminal + claude -p FUNZIONA!
- context_check.py v4.0.0 implementato
- La nuova Cervella parte con prompt iniziale

**DA PERFEZIONARE:**
- claude -p esce dopo risposta (serve restare aperto)
- Studiare apertura su VS Code (sarebbe meglio)

**LEZIONI APPRESE:**
- "Siamo nel 2026!" - servono soluzioni moderne
- VS Code command problematico da automazione
- Terminal + osascript affidabile

---

### 4 Gennaio 2026 (Sessione 84) - SWARM OVUNQUE! v1.9.0

**GLOBALIZZAZIONE SPAWN-WORKERS!**

- spawn-workers v1.9.0: PROJECT-AWARE!
- Symlink globale in ~/.local/bin/spawn-workers
- Trova automaticamente .swarm/ nella directory corrente

**PROGETTI ABILITATI (3/3):**
- CervellaSwarm - FULL SWARM
- Miracollo - FULL SWARM (testato!)
- Contabilita - FULL SWARM (testato!)

**VERIFICHE COMPLETATE:**
- 16 Agents globali in ~/.claude/agents/
- 8 Hooks globali in ~/.claude/hooks/
- Hooks progetto Miracollo/Contabilita funzionanti
- README aggiornati in tutti i progetti

**Versione:** 34.0.0 (MAJOR: Swarm globale funzionante!)

---

### 4 Gennaio 2026 (Sessione 83) - SPAWN-WORKERS v1.8.0 LA MAGIA!

**FIX ELEGANTE: Worker Auto-Exit!**

- PROBLEMA: Worker scrivevano "/exit" come testo invece di eseguirlo
- SOLUZIONE: Aggiunto `-p` mode = uscita automatica dopo task!
- Finestre Terminal si chiudono da sole dopo completamento

**HARDTEST PASSATI (3/3):**
- Worker singolo (backend) - analisi log_event.py, report 8/10
- Guardiana Qualita (Opus) - review APPROVED
- Multi-worker parallelo - 3 finestre insieme! MAGIA!

**BONUS:**
- Log files in `.swarm/logs/`
- MANUALE_DIAMANTE.md globale creato

**Versione:** 33.0.0 (MAJOR: Sistema Multi-Finestra FUNZIONA!)

---

### 4 Gennaio 2026 (Sessione 82) - FINITURE & VERIFICA

**VERIFICA SISTEMI PRIMA DI LIVE**

- Controllato swarm_memory.db: FUNZIONA correttamente
- Hook SubagentStop: Logga nel database
- Puliti log errori vecchi (dal 1 Gennaio)

**DECISIONE:**
- Mancano finiture generali prima di andare live
- Serve double/triple check di tutti i sistemi
- "Una cosa alla volta, con calma" - Rafa

**Versione:** 32.1.0 (PATCH: Verifica e pulizia sistemi)

---

### 3 Gennaio 2026 (Sessione 71) - I 4 CRITICI IMPLEMENTATI!

**LO SCIAME HA LAVORATO IN PARALLELO!**

3 api lanciate contemporaneamente:
- cervella-docs: Template DUBBI e PARTIAL
- cervella-devops: Spawn Guardiane
- cervella-backend: Triple ACK system

**FILE CREATI/MODIFICATI:**
- `.swarm/tasks/TEMPLATE_DUBBI.md` (62 righe) - Template per dubbi worker
- `.swarm/tasks/TEMPLATE_PARTIAL.md` (76 righe) - Template per compact imminente
- `scripts/swarm/spawn-workers.sh` v1.1.0 - Aggiunto supporto Guardiane
- `scripts/swarm/task_manager.py` v1.1.0 - Aggiunto Triple ACK
- `scripts/swarm/triple-ack.sh` v2.0.0 - Helper script ACK

**NUOVI COMANDI:**
```bash
# Spawn Guardiane
./spawn-workers.sh --guardiana-qualita
./spawn-workers.sh --guardiana-ops
./spawn-workers.sh --guardiana-ricerca
./spawn-workers.sh --guardiane  # Tutte e 3

# Triple ACK
./triple-ack.sh received TASK_ID
./triple-ack.sh understood TASK_ID
./triple-ack.sh status TASK_ID
```

**FRASI DELLA SESSIONE:**
- "Ultrapassar os proprios limites!" - Rafa
- "L'abbiamo STUDIATO! L'abbiamo IMPLEMENTATO! Ora USIAMOLO!"

**Versione:** 27.5.0 (MINOR: 4 Critici implementati)

---

### 3 Gennaio 2026 (Sessione 70) - STUDIO COMUNICAZIONE COMPLETATO! BLEND FATTO!

**LO STUDIO E' FINITO!**

Abbiamo studiato e consolidato TUTTO:
- Letto 2000+ righe di documentazione esistente
- Risposto alle 7 domande fondamentali della comunicazione
- Fatto BLEND con STUDIO_APPLE_STYLE.md
- Creato STUDIO_COMUNICAZIONE_DEFINITIVO.md (870+ righe!)

**LE 7 DOMANDE RISPOSTE:**
1. Cosa deve sapere worker? Template TASK completo
2. Cosa torna alla Regina? Template OUTPUT completo
3. Se worker ha dubbi? Template DUBBI creato (NUOVO!)
4. Se Regina fa compact? Pattern HANDOFF definito
5. Se worker fa compact? Template PARTIAL creato (NUOVO!)
6. Come Guardiana verifica? Flusso completo
7. Come mantenere MOMENTUM? AUTO-HANDOFF pattern

**PATTERN INTEGRATI (da Apple Style):**
- Triple ACK (ACK_RECEIVED -> ACK_UNDERSTOOD -> ACK_COMPLETED)
- Quality Gates (4 livelli)
- Circuit Breaker + Retry Backoff
- Graceful Shutdown Sequence
- Dashboard ASCII
- Escalation Matrix

**PRONTO PER IMPLEMENTARE:**
1. Template DUBBI (.swarm/tasks/)
2. Template PARTIAL (worker compact)
3. Spawn Guardiane (spawn-workers.sh)
4. Triple ACK flag files

**FRASE DELLA SESSIONE:**
- "L'ironia e' FORTISSIMA - stiamo creando ANTI-COMPACT e rischiamo compact!" - Rafa

**FILE CREATO:**
- docs/studio/STUDIO_COMUNICAZIONE_DEFINITIVO.md (870+ righe!)

**Versione:** 27.4.0 (MINOR: Studio Comunicazione completato + BLEND)

---

### 3 Gennaio 2026 (Sessione 69) - INSIGHT COMUNICAZIONE MULTI-FINESTRA!

**L'INSIGHT FONDAMENTALE**

Rafa ha fatto la domanda giusta:
"Perche' fai ancora sulla stessa finestra?"

SCOPERTA:
- Il sistema multi-finestra ESISTE gia' (.swarm/)
- Ma NON lo stavamo usando!
- Usavamo Task tool = tutto nel contesto Regina
- Questo NON riduce il compact!

**DECISIONE: FERMIAMO TUTTO**

Prima di continuare Sprint 9.2, dobbiamo STUDIARE:
- Come funziona DAVVERO la comunicazione tra finestre?
- Cosa manca nel protocollo?
- Come lo facciamo nel NOSTRO modo (Rafa e Cervella style)?

**QUICK WINS CREATI (via Task tool)**
- scripts/swarm/anti-compact.sh (~227 righe)
- scripts/swarm/triple-ack.sh (~233 righe)
- scripts/swarm/shutdown-sequence.sh (~300 righe)
- src/patterns/circuit_breaker.py
- src/patterns/retry_backoff.py
- src/patterns/structured_logging.py

**FRASI DELLA SESSIONE:**
- "Noi abbiamo il mondo davanti a noi. Dobbiamo vederlo." - Rafa
- "Prima capire BENE, poi implementare."
- "Nulla e' complesso - solo non ancora studiato!"

**PROSSIMO:** Studio comunicazione multi-finestra

---

### 3 Gennaio 2026 (Sessione 67) - CODE REVIEW 9.0/10 + ROADMAP FASE 9!

**CODE REVIEW SETTIMANALE (Venerdi!)**

Lo sciame ha lavorato in parallelo:
- cervella-reviewer: Score 9.0/10 (+0.5 da Sessione 62)
- cervella-ingegnera: Tech Debt Analysis 9.2/10
- cervella-guardiana-qualita: APPROVATO!

```
Sistema PRODUCTION READY!
spawn-workers.sh valutato 10/10!
Documentazione 10/10!
```

**ROADMAP FASE 9 CREATA!**

File: `docs/roadmap/FASE_9_APPLE_STYLE.md` (594 righe!)

Le 8 Domande Sacre:
1. Come devono comunicare gli agenti?
2. Quali sono i processi giusti?
3. Come fare double/triple check?
4. Come dare feedback all'utente?
5. Come chiudere pulito?
6. Come gestire errori?
7. Come monitorare in tempo reale?
8. **Come gestire il COMPACT?** (ANTI-COMPACT salvavita!)

I 5 Sprint:
- 9.1: Ricerca (8 domande)
- 9.2: Quick Wins (se servono)
- 9.3: Implementazione Pattern
- 9.4: HARDTESTS (6 test!)
- 9.5: MIRACOLLO READY!

**FRASI DELLA SESSIONE:**
- "Vogliamo MAGIA, non debugging!" - Rafa
- "Una cosa alla volta, molto ben fatta" - Rafa
- "La gente non sa cosa vuole finche non glielo mostri" - Steve Jobs

**FILE CREATI:**
- docs/roadmap/FASE_9_APPLE_STYLE.md (594 righe!)
- docs/reviews/TECH_DEBT_ANALYSIS_2026_01_03_v2.md
- docs/reviews/QUICK_WINS_APPLE_POLISH.md
- docs/reviews/METRICS_TRACKING.md
- docs/reviews/README.md

**Versione:** 27.1.0 (MINOR: Code Review + Roadmap FASE 9)

---

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
