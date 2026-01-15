# Stato CervellaSwarm
> Ultimo aggiornamento: 15 Gennaio 2026 - Sessione 218

---

## TL;DR

```
SCORE ATTUALE: 9.5/10 REALE!
CLI: FUNZIONA! (node bin/cervellaswarm.js --help)
FASE 2: INIZIATA - MVP in costruzione

SESSIONE 218: PRIMO CLI REALE + DECISIONI FONDAMENTALI!
```

---

## SESSIONE 218 - CLI FUNZIONA! (15 Gennaio 2026)

```
+================================================================+
|   PRIMO CLI REALE! FASE 2 INIZIATA!                             |
+================================================================+

DECISIONI FONDAMENTALI:
-----------------------
1. CLI (non App Desktop)
   PERCHE: Compatibilita massima, liberta utente
   NON PERCHE: "piu veloce"

2. Wizard COMPLETO prima di tutto
   PERCHE: E IL DIFFERENZIALE del prodotto

3. COSTITUZIONE aggiornata
   NUOVA REGOLA: "IL TEMPO NON CI INTERESSA"
   Un passo al giorno. Arriveremo. SEMPRE.

4. Filosofia Prodotto
   "L'utente apre quando vuole. Fa un passo. Arriva al 100000%."

CREATO:
-------
packages/cli/
├── package.json (169 dipendenze installate)
├── bin/cervellaswarm.js (entry point)
└── src/
    ├── commands/ (init, status, task, resume)
    ├── wizard/questions.js (10 domande!)
    ├── sncp/ (init, loader, writer)
    ├── agents/ (router, spawner)
    ├── display/ (status, recap)
    └── session/ (manager)

DOCUMENTI:
----------
- decisioni/20260115_ARCHITETTURA_CLI_VS_APP.md
- decisioni/20260115_WIZARD_PRIMA_DI_TUTTO.md
- decisioni/20260115_FILOSOFIA_TEMPO_PRODOTTO.md
- decisioni/20260115_SESSIONE_218_TUTTE_DECISIONI.md
- roadmaps/SUB_ROADMAP_MVP_FEBBRAIO.md

TEST: node bin/cervellaswarm.js --help = FUNZIONA!

+================================================================+
```

---

## SESSIONE 214 - PRE-FLIGHT + POST-FLIGHT! (15 Gennaio 2026 notte)

```
+================================================================+
|   SESSIONE 214 - LETTURA VERA COSTITUZIONE IMPLEMENTATA!        |
|   15 Gennaio 2026 (notte)                                        |
+================================================================+

PROBLEMA RISOLTO:
-----------------
La sessione 213 aveva identificato il problema:
"Leggere la Costituzione != Interiorizzarla"
Anche la Regina aveva questo problema!

RICERCA FATTA:
--------------
- Paper Dic 2025: -61.8% performance con instruction nuances
- Tecniche studiate: Self-Verification, CoVe, Constitutional AI
- Best practices: Anthropic, OpenAI, Google
- Report: .sncp/progetti/cervellaswarm/ricerche/RICERCA_20260115_LETTURA_VERA_COSTITUZIONE.md

SOLUZIONE IMPLEMENTATA (3-Layer, Score 9.5/10):
-----------------------------------------------

LAYER 1 - PRE-FLIGHT CHECK (inizio task):
  1. Obiettivo finale: [risposta]
  2. SU CARTA = ___. REALE = ___.
  3. Sono: [Partner]
  4. [RANDOM da pool 6 domande rotanti]

LAYER 2 - POST-FLIGHT CHECK (fine task):
  COSTITUZIONE-APPLIED: [SI/NO]
  Principio usato: [quale + come applicato]

FILE MODIFICATI (16 agenti in ~/.claude/agents/):
-------------------------------------------------
Tutti e 16:
- cervella-backend, frontend, researcher, data, tester
- cervella-security, devops, docs, ingegnera, marketing
- cervella-reviewer, scienziata
- cervella-guardiana-qualita, guardiana-ops, guardiana-ricerca
- cervella-orchestrator

IMPATTO ATTESO:
---------------
- -60-80% episodi "lettura checkbox"
- Verifica TEORIA (PRE) + AZIONE (POST)
- Random previene memorizzazione meccanica

VALIDAZIONE GUARDIANA:
----------------------
- Proposta originale (5 domande): 7/10
- Versione modificata (3+1 + POST-FLIGHT): 8.5/10
- Versione finale (con random pool): 9.5/10

SCORE: 9.4 → 9.5 (+0.1) - TARGET RAGGIUNTO!

+================================================================+
```

---

## SESSIONE 213 - REC-2 + SPLIT STATO! (15 Gennaio 2026)

```
+================================================================+
|   SESSIONE 213 - COMUNICAZIONE INTERNA IMPLEMENTATA!           |
|   15 Gennaio 2026                                               |
+================================================================+

REC-2: AZIONE #2 READ SNCP FIRST - COMPLETATO!
----------------------------------------------
Aggiunto a TUTTI i 16 agenti la sezione:

  ## AZIONE #2 - READ SNCP FIRST
  PRIMA di iniziare il task, leggi SNCP per context!
  1. Read(".sncp/progetti/{progetto}/stato.md")
  2. Glob(".sncp/progetti/{progetto}/reports/*{topic}*.md")
  3. Glob(".sncp/progetti/{progetto}/ricerche/*{topic}*.md")

  "Non ri-fare, continua da dove altri hanno lasciato!"

FILE MODIFICATI:
- cervella-backend.md
- cervella-frontend.md
- cervella-researcher.md
- cervella-data.md
- cervella-tester.md
- cervella-security.md
- cervella-devops.md
- cervella-docs.md
- cervella-ingegnera.md
- cervella-marketing.md
- cervella-reviewer.md
- cervella-scienziata.md
- cervella-guardiana-qualita.md
- cervella-guardiana-ops.md
- cervella-guardiana-ricerca.md
- cervella-orchestrator.md

IMPATTO ATTESO: -30% duplicazione lavoro!

REC-3: WATCHER AUTO-START - ERA GIA' FATTO!
-------------------------------------------
spawn-workers.sh v2.7.0 aveva gia':
- AUTO_SVEGLIA=true di default
- Anti-duplicati watcher
- Fallback a path globale

SPLIT MIRACOLLO/STATO.MD:
-------------------------
- PRIMA: 554 righe (> limite 500!)
- DOPO: 400 righe (sotto limite!)
- Sessioni 202-204 archiviate in:
  archivio/SESSIONI_GENNAIO_2026.md

REC-1 (PENDING):
----------------
Hook verifica output SNCP richiede analisi aggiuntiva.
I worker hanno gia' istruzioni OUTPUT OBBLIGATORIO,
ma l'enforcement automatico e' complesso per spawn-workers.

+================================================================+
```

---

## SESSIONE 211 (parte 3) - TEST AUTOMATICI!

```
+================================================================+
|                                                                |
|   TEST SUITE SNCP CREATA!                                      |
|                                                                |
|   LAUNCHD VERIFICATO:                                          |
|   - Daily job: FUNZIONA!                                       |
|   - Report creato: health_2026-01-14.txt                       |
|   - SNCP Health Score: 100/100                                 |
|                                                                |
|   TEST AUTOMATICI:                                             |
|   - tests/sncp/test_health_check.sh (4 check)                  |
|   - tests/sncp/test_sncp_init.sh (6 check)                     |
|   - tests/sncp/test_verify_sync.sh (7 check)                   |
|   - tests/sncp/run_all_tests.sh (runner)                       |
|                                                                |
|   RISULTATO: 3 test, 17 check, TUTTI PASSATI!                  |
|                                                                |
|   SCORE: 9.2 → 9.4 (+0.2 punti!)                               |
|   GAP AL TARGET: 0.1 punti!                                    |
|                                                                |
+================================================================+
```

---

## SESSIONE 211 (parte 2) - AUDIT + FIX CRITICO!

```
+================================================================+
|                                                                |
|   "SU CARTA != REALE" - TROVATO E FIXATO!                      |
|                                                                |
|   AUDIT INGEGNERA:                                             |
|   - Score dichiarato: 8.7/10                                   |
|   - Score REALE trovato: 8.2/10                                |
|   - Problema CRITICO: symlink NON esistevano!                  |
|                                                                |
|   GUARDIANA QUALITA:                                           |
|   - CONFERMATO: symlink mancanti                               |
|   - CONFERMATO: stato.md miracollo 555 righe (warning)         |
|   - Score indipendente: 8.1/10 (allineato)                     |
|                                                                |
|   FIX APPLICATO:                                               |
|   - ~/.local/bin/sncp-init → scripts/sncp/sncp-init.sh         |
|   - ~/.local/bin/verify-sync → scripts/sncp/verify-sync.sh     |
|   - TESTATO: sncp-init --help OK!                              |
|   - TESTATO: verify-sync --help OK!                            |
|                                                                |
|   SCORE: 8.2 → 9.2 (+1.0 punto!)                               |
|                                                                |
|   "La Costituzione aveva ragione - solo REALE conta!"          |
|                                                                |
+================================================================+
```

---

## SESSIONE 211 - SEMPLIFICAZIONE SNCP v4.0!

```
+================================================================+
|                                                                |
|   MILESTONE 1.2 COMPLETATO!                                    |
|   "Semplificare struttura SNCP"                                |
|                                                                |
|   PRIMA: 14 cartelle (molte obsolete/duplicate)                |
|   DOPO:  10 cartelle (tutte necessarie)                        |
|                                                                |
|   ARCHIVIATO:                                                  |
|   - coscienza/    → archivio/2026-01/coscienza/                |
|   - perne/        → archivio/2026-01/perne/                    |
|                                                                |
|   SPOSTATO:                                                    |
|   - istruzioni/*  → progetti/miracollo/workflow/               |
|   - roadmaps/*    → progetti/miracollo/roadmaps/               |
|                                                                |
|   AGGIORNATO:                                                  |
|   - README.md SNCP v4.0 (struttura REALE!)                     |
|   - ROADMAP_2026 checkbox corretti                             |
|                                                                |
|   SCORE: 8.5 → 8.7 (+0.2)                                      |
|                                                                |
+================================================================+
```

---

## SESSIONE 209 - COMUNICAZIONE INTERNA COMPLETA!

```
+================================================================+
|                                                                |
|   ROADMAP COMUNICAZIONE INTERNA - 4 FASI COMPLETATE!           |
|   Guardiana Qualita: 9/10 APPROVATO                            |
|                                                                |
|   FASE 1 - Hook Automatici:                                    |
|   - sncp_pre_session_hook.py (SessionStart)                    |
|   - sncp_verify_sync_hook.py (SessionEnd)                      |
|   - Commit: 20cce3e                                            |
|                                                                |
|   FASE 2 - Regole Regina:                                      |
|   - CLAUDE.md: sezione AUTOMAZIONI OBBLIGATORIE                |
|   - ~/.claude/CLAUDE.md: stessa sezione (globale)              |
|   - Commit: ea993e9                                            |
|                                                                |
|   FASE 3 - Launchd Automatico:                                 |
|   - sncp_daily_maintenance.sh (health + cleanup)               |
|   - sncp_weekly_archive.sh (archivia > 30gg)                   |
|   - com.cervellaswarm.sncp.daily.plist (AL LOGIN!)             |
|   - com.cervellaswarm.sncp.weekly.plist (Lunedi)               |
|   - Commit: 9ab5428                                            |
|                                                                |
|   FASE 4 - Validazione:                                        |
|   - Test workflow: OK                                          |
|   - Guardiana audit: 9/10 APPROVATO                            |
|   - Documentazione: COMPLETA                                   |
|                                                                |
|   "Avere attrezzature ma non usarle = non averle"              |
|   ORA SI USANO DA SOLE!                                        |
|                                                                |
+================================================================+
```

---

## SESSIONE 207 - FONDAMENTA SNCP!

```
+================================================================+
|                                                                |
|   MILESTONE 1.1 COMPLETATO!                                    |
|                                                                |
|   CREATO:                                                      |
|   - sncp-init.sh wizard (8.8/10 dalla Guardiana!)             |
|   - verify-sync.sh (verifica coerenza docs/codice)            |
|   - Symlink: sncp-init, verify-sync                            |
|   - Documentazione in README.md                                |
|                                                                |
|   DECISIONI STORICHE (mente locale):                           |
|   1. Crypto Tax → NO (non conosciamo il mondo)                 |
|   2. CervellaSwarm Prodotto → SI!                              |
|   3. Miracollo → CONTINUA (60/40 split)                        |
|                                                                |
|   COMMIT: de42e73, bdb5ac7                                     |
|                                                                |
+================================================================+
```

---

## Score Dashboard

| Area | Score | Gap | Note |
|------|-------|-----|------|
| SNCP | 8.2 | -1.3 | sncp-init + verify-sync FUNZIONANO! |
| Log | 7.5 | -2.0 | Funziona |
| Agenti | 8.5 | -1.0 | 16 operativi |
| Infra | 8.5 | -1.0 | Tutto OK |

---

## Cosa Funziona REALE

| Cosa | Status | Testato |
|------|--------|---------|
| sncp-init.sh | ATTIVO | Sessione 207 |
| verify-sync.sh | ATTIVO | Sessione 207 |
| 4 Script SNCP vecchi | ATTIVI | Sessione 203 |
| SwarmLogger v2.0.0 | ATTIVO | Quotidiano |
| 16 Agenti | ATTIVI | Quotidiano |

---

## Roadmap FASE 1 (Gen-Feb)

| Task | Status | Note |
|------|--------|------|
| sncp-init.sh | FATTO | 8.8/10 |
| verify-sync.sh | FATTO | Funziona |
| Sessioni giornaliere | IN CORSO | Prima oggi! |
| Score 8.5+ | IN CORSO | Ora 8.0 |

---

## Script SNCP (TESTATI!)

```bash
# NUOVI (Sessione 207)
sncp-init nome-progetto           # Wizard nuovo progetto
sncp-init nome --analyze          # Con analisi stack
verify-sync                       # Check coerenza tutti
verify-sync miracollo --verbose   # Check singolo progetto

# HOOK AUTOMATICI (Sessione 209)
# Questi sono chiamati automaticamente da settings.json!
# - sncp_pre_session_hook.py  -> SessionStart
# - sncp_verify_sync_hook.py  -> SessionEnd

# ESISTENTI
./scripts/sncp/health-check.sh        # Dashboard ASCII
./scripts/sncp/pre-session-check.sh   # Check inizio
./scripts/sncp/post-session-update.sh # Checklist fine
./scripts/sncp/compact-state.sh FILE  # Compattazione
```

---

## Path Importanti

| Cosa | Path |
|------|------|
| Roadmap 2026 | `.sncp/progetti/cervellaswarm/roadmaps/ROADMAP_2026_PRODOTTO.md` |
| Business Plan | `.sncp/progetti/cervellaswarm/BUSINESS_PLAN_2026.md` |
| Script SNCP | `scripts/sncp/` |
| Review sncp-init | `.sncp/progetti/cervellaswarm/reports/20260114_REVIEW_SNCP_INIT.md` |

---

## PROSSIMI STEP

1. [x] Semplificare struttura SNCP (Sessione 211!)
2. [x] Score 8.5+ (ora 8.7!)
3. [ ] 5 sessioni giornaliere completate
4. [ ] Documentazione workflow per esterni
5. [ ] Prepararsi per FASE 2 (Marzo)

---

## Famiglia

- 1 Regina (Orchestrator)
- 3 Guardiane (Opus) - Usate oggi!
- 12 Worker (Sonnet)

---

*"Cursor l'ha fatto. Noi lo faremo."*
*"Un po' ogni giorno fino al 100000%!"*
