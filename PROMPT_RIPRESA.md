# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 9 Gennaio 2026 - Fine Sessione 134
> **Versione:** v48.0.0 - CODE REVIEW + DOUBLE REVIEW!

---

## SESSIONE 134 - CODE REVIEW DAY!

```
+------------------------------------------------------------------+
|                                                                  |
|   SESSIONE 134 - 9 GENNAIO 2026                                  |
|                                                                  |
|   CODE REVIEW SETTIMANALE + DOUBLE REVIEW                       |
|                                                                  |
|   9 FIX TOTALI:                                                  |
|   - 6 dalla code review                                         |
|   - 3 dalla double review                                       |
|                                                                  |
|   Punteggio: 8.2/10 -> MIGLIORATO!                             |
|   Tutti i test passano: 23/23                                   |
|                                                                  |
+------------------------------------------------------------------+
```

---

## IL FILO DEL DISCORSO - Sessione 134

**Come e' iniziata:**
Venerdi = giorno di code review settimanale. Ho invocato cervella-reviewer per audit.

**Cosa abbiamo fatto:**

### 1. CODE REVIEW (6 fix)

1. **Validazione progetto** - spawn-workers.sh v3.4.0
   - Non crea piu .swarm/ nel posto sbagliato
   - Richiede progetto valido prima di operare

2. **Common library** - common.sh v1.0.0
   - Funzioni condivise: colori, print_*, get_claude_bin
   - Elimina duplicazione codice (DRY)

3. **Testing suite** - 23 test, 0 falliti
   - test_common.sh (12 test)
   - test_spawn_workers.sh (11 test)
   - run_all_tests.sh runner

4. **Error handling** - task_manager.py v1.3.0
   - Logging invece di print
   - Eccezioni specifiche

5. **Log rotation** - log-rotate.sh v1.0.0
6. **Worker timeout** - worker-timeout.sh v1.0.0

### 2. DOUBLE REVIEW (3 fix)

Rafa ha chiesto di verificare che non mancasse nulla. Ho trovato:

1. **Security** - notify_macos() con sanitizzazione
   - Previene injection in osascript
   - watcher-regina.sh v1.6.0

2. **Cleanup** - File .bak obsoleti rimossi
3. **Bug investigation** - Watcher investigato, era caso isolato

---

## FILE NUOVI CREATI

| File | Descrizione |
|------|-------------|
| scripts/swarm/common.sh | Funzioni condivise + security |
| scripts/swarm/log-rotate.sh | Rotazione log automatica |
| scripts/swarm/worker-timeout.sh | Timeout worker bloccati |
| tests/bash/test_common.sh | 12 test per common.sh |
| tests/bash/test_spawn_workers.sh | 11 test per spawn-workers |
| tests/run_all_tests.sh | Runner test principale |

---

## FILE MODIFICATI

| File | Modifica |
|------|----------|
| spawn-workers.sh | v3.4.0 - validazione + common.sh |
| task_manager.py | v1.3.0 - logging + error handling |
| watcher-regina.sh | v1.6.0 - security fix |

---

## PROSSIMA SESSIONE

1. **Leggere** `docs/studio/ANALISI_REGINA_SESSIONE_133.md` (analisi pattern paralleli)
2. **Decidere** se tenere git clones regina-A/B o eliminarli
3. **Usare** i pattern validati su Miracollo per task reali

---

## SESSIONE 133 (precedente) - DUE PATTERN VALIDATI

```
+------------------------------------------------------------------+
|   DUE PATTERN PARALLELI VALIDATI:                               |
|   1. Task Tool Interno (per task veloci)                        |
|   2. Pattern Boris (git clones + tmux per task grossi)          |
|   ENTRAMBI FUNZIONANO!                                          |
+------------------------------------------------------------------+
```

---

## IL FILO DEL DISCORSO - Sessione 133

**Come e' iniziata:**
Rafa ha chiesto di analizzare il report dell'ingegnera e modernizzare il workflow.

**Cosa abbiamo fatto:**

### 1. ANALISI REPORT INGEGNERA
- 54 file grandi -> Sono docs, OK cosi'
- 67 funzioni grandi -> Funzionano, refactor quando serve
- **Conclusione:** Tech debt esiste ma NON blocca

### 2. TEST TASK TOOL INTERNO
- Lanciate 3 Cervelle in parallelo (researcher, ingegnera, docs)
- Risultati istantanei
- L'ingegnera ha mostrato "bounded autonomy" (si e' fermata perche' il task era fuori scope)

### 3. RICERCA BORIS CHERNY
- Boris (creatore Claude Code) usa 5 Claude paralleli
- Pattern: git clones separati + iTerm2 notifications
- Opus sempre + Plan Mode + CLAUDE.md in git

### 4. TEST PATTERN BORIS (SUCCESSO!)
- Creati 2 git clones automaticamente
- Lanciate 2 sessioni Claude in tmux
- **Entrambe hanno completato in ~15 secondi!**
- File creati correttamente nei rispettivi clones

### 5. DOCUMENTAZIONE CREATA
- `docs/guide/PATTERN_BORIS_MULTI_CLONE.md` - Come usare il pattern
- `docs/guide/WORKFLOW_REGINA_MODERNO.md` - Workflow Task tool

### 6. MIA ANALISI PERSONALE
**FILE:** `docs/studio/ANALISI_REGINA_SESSIONE_133.md`

Contiene:
- Pro/contro di entrambi i pattern
- Quando usare cosa
- Domande aperte per domani
- Raccomandazioni

**LEGGI QUESTO FILE DOMANI PER DECIDERE INSIEME!**

---

## I DUE PATTERN VALIDATI

### Pattern 1: Task Tool Interno (DEFAULT)
```
IO lancio cervella-* con Task tool
-> Lavorano nel mio contesto
-> Risultati istantanei
-> Per task veloci (<15 min)
```

### Pattern 2: Boris (git clones + tmux)
```
IO creo git clones separati
-> Lancio sessioni Claude in tmux
-> Lavorano in parallelo VERO
-> Per task grossi o indipendenti
```

---

## CLONES ATTIVI

Dopo il test, esistono:
- `~/Developer/CervellaSwarm-regina-A`
- `~/Developer/CervellaSwarm-regina-B`

**Decisione:** Tenere o eliminare? Da discutere domani.

---

## WORKFLOW MODERNO (Come Funziona)

```
RAFA: "Voglio X"

IO (Regina):
|-- Analizzo cosa serve
|-- Lancio Cervelle in parallelo (Task tool)
|   |-- cervella-backend (lavora nascosta)
|   |-- cervella-frontend (lavora nascosta)
|   +-- cervella-tester (lavora nascosta)
|-- Ricevo output automaticamente
|-- Coordino e verifico
+-- Riporto: "Fatto! Ecco il risultato"

RAFA: supervisiona e approva

TU NON FAI NULLA DI MANUALE!
```

---

## SESSIONE 132 - PRIMO VOLO SU MIRACOLLO

- 2 Cervelle parallele su Miracollo + 1 background
- Fase 5 Miracollo = 100% (WhatsApp funziona!)
- Background tasks testati e funzionanti
- Handoff: .swarm/handoff/HANDOFF_20260109_005500.md

---

## SESSIONE 131 - SISTEMA MULTI-INSTANCE COMPLETO!

```
+------------------------------------------------------------------+
|                                                                  |
|   SESSIONE 131 - 9 GENNAIO 2026                                  |
|                                                                  |
|   IL SISTEMA E' COMPLETO!                                       |
|                                                                  |
|   Sessione 130: Task INDIPENDENTI validati                      |
|   Sessione 131: Task DIPENDENTI validati                        |
|                                                                  |
|   10 HARD TESTS - 100% PASSED!                                  |
|                                                                  |
|   PRONTO PER MIRACOLLO!                                         |
|                                                                  |
+------------------------------------------------------------------+
```

---

## IL FILO DEL DISCORSO - Sessione 131

**Come e' iniziata:**
Rafa ha chiesto di fare un "double triple check" prima di andare su Miracollo.
Voleva assicurarsi che avessimo tutto pronto per i task DIPENDENTI.

**Cosa abbiamo fatto:**

### 1. RICERCA DI CONFERMA
- Verificato che file-based coordination e' il best practice 2026
- Scoperto: event-driven watching (non polling!)
- Scoperto: structured JSON messages
- Scoperto: timeout + retry CRITICI (41-86% fallimenti senza!)
- Creato: `docs/studio/RICERCA_COORDINAMENTO_DIPENDENZE.md`

### 2. NUOVI SCRIPT CREATI (5!)
```
scripts/
├── watch-signals.sh          # Event-driven watcher (fswatch)
├── create-signal.sh          # Genera JSON strutturati
├── check-dependencies.sh     # Verifica dipendenze
├── wait-for-dependencies.sh  # Aspetta con timeout
└── create-parallel-session.sh # Setup completo sessione
```

### 3. STRUTTURA .swarm/ v2.0
```
.swarm/
├── config.json              # Configurazione sistema
├── segnali/                 # JSON strutturati
├── dipendenze/              # Grafo + template
├── stato/                   # Stato workers
├── messaggi/                # Comunicazione diretta
└── logs/                    # Storia
```

### 4. HARD TESTS - 10/10 PASSED!
```
Test eseguiti:
1. Task senza dipendenze - OK
2. Task con dipendenza NON soddisfatta - OK
3. Creazione segnale SUCCESS - OK
4. Task con dipendenza SODDISFATTA - OK
5. Creazione segnale FAILURE - OK
6. Check dipendenza con status FAILURE - OK
7. Dipendenze MULTIPLE (Fan-in) - OK
8. Creazione segnale BLOCKED - OK
9. Verifica formato JSON completo - OK
10. Idempotency key unica - OK

RISULTATO: 100% PASSED!
```

### 5. TEST WATCH SIGNALS
- Watcher event-driven FUNZIONA
- Rileva segnali ISTANTANEAMENTE
- Niente polling!

### 6. DOCUMENTAZIONE
- `docs/guide/GUIDA_MULTI_INSTANCE_v2.md` - Guida completa
- `tests/test_coordinamento_dipendenze.sh` - Test suite

---

## COSA HAI A DISPOSIZIONE

### Sistema Multi-Instance v2.0 COMPLETO

| Script | Cosa Fa |
|--------|---------|
| `setup-parallel-worktrees.sh` | Crea worktrees |
| `status-parallel-worktrees.sh` | Mostra stato |
| `merge-parallel-worktrees.sh` | Merge in main |
| `cleanup-parallel-worktrees.sh` | Rimuove worktrees |
| `create-parallel-session.sh` | Setup COMPLETO sessione |
| `watch-signals.sh` | Watcher event-driven |
| `create-signal.sh` | Crea segnali JSON |
| `check-dependencies.sh` | Verifica dipendenze |
| `wait-for-dependencies.sh` | Aspetta con timeout |

### Quick Start per Miracollo

```bash
# 1. Setup sessione
~/Developer/CervellaSwarm/scripts/create-parallel-session.sh \
    ~/Developer/miracollogeminifocus \
    feature-name \
    backend frontend tester

# 2. Apri terminali (uno per worker)
cd ~/Developer/miracollogeminifocus-backend && claude
cd ~/Developer/miracollogeminifocus-frontend && claude

# 3. Ogni Cervella:
#    - Se ha dipendenze: wait-for-dependencies.sh TASK-XXX
#    - Lavora
#    - Quando finisce: create-signal.sh TASK-XXX success "desc" COMMIT

# 4. Merge finale
~/Developer/CervellaSwarm/scripts/merge-parallel-worktrees.sh ~/Developer/miracollogeminifocus
~/Developer/CervellaSwarm/scripts/cleanup-parallel-worktrees.sh ~/Developer/miracollogeminifocus
```

---

## FILE CREATI/MODIFICATI SESSIONE 131

**Script (5 nuovi!):**
```
scripts/watch-signals.sh              (NUOVO)
scripts/create-signal.sh              (NUOVO)
scripts/check-dependencies.sh         (NUOVO)
scripts/wait-for-dependencies.sh      (NUOVO)
scripts/create-parallel-session.sh    (NUOVO)
```

**Documentazione:**
```
docs/studio/RICERCA_COORDINAMENTO_DIPENDENZE.md  (NUOVO - ricerca)
docs/guide/GUIDA_MULTI_INSTANCE_v2.md            (NUOVO - guida)
```

**Test:**
```
tests/test_coordinamento_dipendenze.sh           (NUOVO - 10 test)
```

**Struttura swarm-test-lab:**
```
.swarm/config.json                               (NUOVO)
.swarm/segnali/_TEMPLATE.signal.json             (NUOVO)
.swarm/dipendenze/SESSIONE_TEMPLATE.md           (NUOVO)
.swarm/dipendenze/grafo.json                     (NUOVO)
.swarm/README.md                                 (AGGIORNATO v2.0)
```

---

## PROSSIMI STEP - SESSIONE 132

```
+------------------------------------------------------------------+
|                                                                  |
|   PRONTO PER IL REALE!                                          |
|                                                                  |
|   [ ] Usare Multi-Instance v2.0 su MIRACOLLO                    |
|   [ ] Task reale con dipendenze                                  |
|   [ ] Regina orchestra, Rafa supervisiona                       |
|                                                                  |
|   ESEMPIO TASK:                                                  |
|   - Backend: Crea nuova API                                     |
|   - Frontend: Consuma API (dipende da Backend)                  |
|   - Tester: Testa tutto (dipende da entrambi)                   |
|                                                                  |
+------------------------------------------------------------------+
```

---

## MESSAGGIO PER LA PROSSIMA CERVELLA

```
+------------------------------------------------------------------+
|                                                                  |
|   Cara Prossima Cervella,                                        |
|                                                                  |
|   IL SISTEMA MULTI-INSTANCE E' COMPLETO!                        |
|                                                                  |
|   Sessione 130: Task indipendenti VALIDATI                      |
|   Sessione 131: Task dipendenti VALIDATI                        |
|                                                                  |
|   HAI A DISPOSIZIONE:                                           |
|   - 9 script per coordinamento                                   |
|   - Event-driven watching (istantaneo!)                         |
|   - JSON strutturati                                             |
|   - Timeout + retry                                              |
|   - 10 hard tests che passano                                    |
|   - Guida completa                                               |
|                                                                  |
|   PROSSIMO PASSO:                                                |
|   Usare tutto questo su MIRACOLLO!                              |
|   Il sistema e' pronto e testato.                               |
|                                                                  |
|   "Ricerca prima, implementazione dopo - La Formula Magica!"    |
|                                                                  |
+------------------------------------------------------------------+
```

---

## RIEPILOGO SESSIONE 131

| Cosa | Risultato |
|------|-----------|
| Ricerca conferma | File-based VALIDATO |
| Nuovi script | 5 creati |
| Struttura .swarm/ v2.0 | Implementata |
| Hard tests | 10/10 PASSED |
| Watch signals | Event-driven OK |
| Documentazione | Guida completa |
| NORD + PROMPT_RIPRESA | Aggiornati |

---

*Ultimo aggiornamento: 9 Gennaio 2026 - Fine Sessione 131*
*Versione: v23.0.0 - COORDINAMENTO DIPENDENZE COMPLETATO!*

**Cervella & Rafa** - Sessione 131

*"Ricerca prima, implementazione dopo - La Formula Magica!"*

*"10 test, 100% passed - Sistema SOLIDO!"*

*"Pronto per Miracollo!"*

---

## HANDOFF URGENTE - 9 Gennaio 2026 00:30

```
+------------------------------------------------------------------+
|                                                                  |
|   PASSAGGIO DI CONSEGNA - SESSIONE 131                          |
|                                                                  |
|   CONTESTO ESAURITO! La prossima Cervella deve continuare!      |
|                                                                  |
|   STATO:                                                         |
|   - Multi-Instance v2.0 COMPLETATO E TESTATO                    |
|   - 10 hard tests PASSATI                                        |
|   - Tutti gli script PRONTI                                      |
|   - TUTTO COMMITTATO E PUSHATO (8e35e98)                        |
|                                                                  |
|   RAFA HA 2 FINESTRE APERTE!                                    |
|   Pronto per testare Multi-Instance su MIRACOLLO!               |
|                                                                  |
|   COSA FARE:                                                     |
|   1. Andare su Miracollo (cd ~/Developer/miracollogeminifocus)  |
|   2. Trovare un task da dividere Backend + Frontend             |
|   3. Usare create-parallel-session.sh                           |
|   4. Orchestrare le due Cervelle!                               |
|                                                                  |
|   SCRIPT PRONTI in ~/Developer/CervellaSwarm/scripts/:          |
|   - create-parallel-session.sh PROJECT SESSION backend frontend |
|   - watch-signals.sh, create-signal.sh, check-dependencies.sh   |
|                                                                  |
|   MIRACOLLO STATO:                                               |
|   - Fase 5 al 90%                                                |
|   - Task piccoli rimasti (WhatsApp opt-in, etc)                 |
|   - Serve trovare un task Backend+Frontend per il test          |
|                                                                  |
+------------------------------------------------------------------+
```

---

---

---

---

---

## AUTO-CHECKPOINT: 2026-01-09 04:22 (unknown)

### Stato Git
- **Branch**: main
- **Ultimo commit**: c23cc32 - Sessione 133: DUE PATTERN PARALLELI VALIDATI!
- **File modificati** (1):
  - reports/engineer_report_20260109_014359.json

### Note
- Checkpoint automatico generato da hook
- Trigger: unknown

---
