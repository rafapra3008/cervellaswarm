# ROADMAP SACRA - CervellaSwarm

> **"La mappa verso lo sciame perfetto."**

---

## OVERVIEW

> **Aggiornato:** 3 Gennaio 2026 - Sessione 59 - PROMPT CORTI! (v23.0.0)

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

### 3 Gennaio 2026 (Sessione 59) - PROMPT CORTI!

**OTTIMIZZAZIONE PROMPT COMPLETATA!**

```
"Il prompt e un RITUALE, non documentazione!" - Le Ragazze
```

**COMPLETATO:**
- Recap script terminale (alias swarm/miracollo/contabilita) - OK!
- Recap hooks (8 attivi) e triggers (5 attivi) - OK!
- Consultato 3 api in parallelo: Researcher + Docs + Marketing
- Riscritto PROMPT_SWARM_MODE.md completamente
- Da 307 righe a 145 righe (file)
- Da 50 righe a 12 righe (prompt)
- Da ~1000 token a ~150 token (85% risparmio!)
- Eliminata 95% ridondanza

**SCOPERTA:**
- Il prompt NON e documentazione, e un RITUALE
- Sandwich emotivo: apertura + operativo + chiusura
- Solo 3 LIVELLI RISCHIO sono info essenziali

**Versione:** 23.0.0 (MAJOR: Prompt ottimizzati!)

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
