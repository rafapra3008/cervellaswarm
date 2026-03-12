# SUBROADMAP MIGLIORAMENTI INTERNI V2 - CervellaSwarm

> **"Prima di costruire per altri, costruisci il MEGLIO per te."** - Rafa
> **Data creazione:** 12 Marzo 2026 - Sessione 442
> **Continua da:** MAPPA_MIGLIORAMENTI_INTERNI.md (V1, S349-S352, 11/11 FATTO)

---

## CONTESTO

```
+================================================================+
|   PUNTO DI PARTENZA (S442):                                     |
|                                                                  |
|   17 agenti, 16 hooks, 6612 test (0 collection errors!)        |
|   CLAUDE.md: ~151 righe (ottimizzato V1)                       |
|   _SHARED_DNA: 131 righe (ottimizzato S442)                    |
|   Context per subagent: ~13KB (era ~22KB, -40%)                 |
|   Tech debt: ZERO                                                |
|   SNCP root: 7 entries (era 18, pulito S442)                    |
|   Hooks: tutti su cervella_hooks_common.py (DRY!)               |
|                                                                  |
|   OBIETTIVO: Casa perfetta + evoluzione strategica               |
+================================================================+
```

---

# FASE A: QUICK FIXES (S442) -- COMPLETATA!

## A.1: Fix doppia iniezione COSTITUZIONE_OPERATIVA
**Stato:** [FATTO] - S442, Score TBD
**Impatto:** -3.2KB per ogni subagent spawn
**Fix:** Rimossa iniezione da subagent_context_inject.py (agenti la leggono via _SHARED_DNA)

## A.2: Auto-checkpoint compattato + PROMPT_RIPRESA
**Stato:** [FATTO] - S442, Score TBD
**Impatto:** Checkpoint da 14 a 5 righe (-64%), su tutti i progetti
**Fix:** update_prompt_ripresa.py v2.1.0 - rimossa sezione "Note" ridondante

## A.3: Pulizia SNCP legacy
**Stato:** [FATTO] - S442, Score TBD
**Impatto:** Root SNCP da 18 a 7 entries (-61%)
**Fix:** 11 directory legacy archiviate in archivio/legacy_sncp3/ (zero contenuto perso)

---

# FASE B: CONSOLIDAMENTO HOOKS/AGENTI (S442) -- COMPLETATA!

## B.1: Modulo comune cervella_hooks_common.py
**Stato:** [FATTO] - S442, Score TBD
**Impatto:** Aggiungere un progetto = toccare 1 file invece di 8
**Fix:** Nuovo modulo con PROJECTS, detect_project(), safe_read(), path helpers. 8 hook migrati.

## B.2: session_end_save + pre_compact_save -> common module
**Stato:** [FATTO] - S442, Score TBD
**Impatto:** KNOWN_PROJECTS eliminato + DRY V3: get_git_info, rotate_snapshots, send_notification, detect_project_info estratte nel modulo comune.
**Fix:** session_end 209->125 righe (-40%), pre_compact 214->129 righe (-40%). Zero duplicazione.

## B.3: _SHARED_DNA.md ottimizzato
**Stato:** [FATTO] - S442, Score TBD
**Impatto:** 159 -> 131 righe (-18%), rimossa sezione "TOOL DISPONIBILI" ridondante
**Fix:** Rimosso: lista tool (Claude sa i suoi tool), path SNCP 3.0 obsoleti

---

# FASE C: RICERCA STRATEGICA (S442) -- COMPLETATA!

## C.1: Prompt Caching Anthropic API
**Stato:** [STUDIATO] - S442
**Risultato:** GIA ATTIVO automaticamente in Claude Code! -60-80% costi input.
**Azione:** Nessuna. Mantenere _SHARED_DNA e COSTITUZIONE stabili (cache invalidation).
**Report:** reports/RESEARCH_20260312_PROMPT_CACHING.md

## C.2: Observability con Langfuse
**Stato:** [STUDIATO] - S442
**Risultato:** Langfuse self-hosted troppo pesante (PostgreSQL+ClickHouse+Redis).
**Raccomandazione:** Custom SQLite "F3.6 Observability Layer" su event-store esistente.
**Report:** reports/RESEARCH_20260312_OBSERVABILITY_LANGFUSE.md

## C.3: Studio A2A Protocol
**Stato:** [STUDIATO] - S442
**Risultato:** A2A e complementare a MCP (MCP=agent->tool, A2A=agent->agent). 150+ org, AAIF sotto Linux Foundation.
**Raccomandazione:** MCP PRIMA (valore immediato), A2A durante E.6 CervellaLang 1.0 (interoperabilita esterna).
**Reports:** RESEARCH_20260312_A2A_PROTOCOL_TECHNICAL.md (14 fonti) + SCIENTIST_20260312_A2A_STRATEGIC.md (17 fonti)

## C.4: Model Tiering (FUTURO)
**Stato:** [DA FARE] - Futuro
**Piano:** cervella-security da Opus a Sonnet (fa lavoro pattern matching, non ragionamento complesso).

---

# FASE D: P3 FIXATI (S442) -- COMPLETATA!

## D.1: Hook .DISABLED archiviati
**Stato:** [FATTO] - S442
**Impatto:** 9 hook, 42KB dead code -> _archived_disabled/

## D.2: Test collection errors fixati
**Stato:** [FATTO] - S442
**Impatto:** 27 errors -> 0. +605 test recuperati (5909 -> 6514)
**Root cause:** pytest module name collision. Fix: pyproject.toml --import-mode=importlib

---

# FASE E: NEXT -- COMPLETATA!

## E.1: F3.6 Observability Layer (custom SQLite)
**Stato:** [FATTO] - S442, Score 9.5/10
**Dipende da:** C.2 (ricerca completa)
**Implementazione:**
- Modulo `observability.py`: TokenUsage dataclass, estimate_cost(), query con filtri
- Tabella `token_usage` nello schema (4 indici + session_id UNIQUE, INSERT OR REPLACE)
- Hook `observability_hook.py`: parsa JSONL transcript, estrae usage metadata, fail-open
- CLI `cervella-events usage --today --by-project --by-model --json`
- **58 test nuovi** (37 observability + 15 hook + 6 CLI usage), 309 totali event-store
- Pricing: Opus $15/$75, Sonnet $3/$15, Haiku $0.80/$4 (per MTok in/out)
**Guardiana audit:** 9.3 -> 9.5+ (7 finding, tutti fixati: dedup P2, test coverage, cleanup)

## E.2: Researcher/Scienziata confini definiti
**Stato:** [FATTO] - S442
**Soluzione:** Opzione B (Ingegnera: sovrapposizione 65%, non unire). Definiti confini espliciti.
Researcher = TECNICO (paper, API, benchmark). Scienziata = STRATEGICO (mercato, funding, go-to-market).
Aggiunta sezione "NON Faccio" in entrambi. Aggiornato spawn-workers.sh.

## E.3: A2A Protocol studio approfondito
**Stato:** [FATTO] - S442
**Soluzione:** Due report paralleli (Researcher tecnico 14 fonti + Scienziata strategico 18 fonti).
A2A = protocollo orizzontale agent-to-agent (complementare a MCP verticale agent-to-tool).
150+ org, AAIF Linux Foundation. SDK Python v0.3.25, spec v0.3.0.
**Decisione:** MONITOR. MCP prima (valore oggi), A2A durante E.6 (interoperabilita esterna).
AgentCard A2A nativo per agenti LU = differenziatore narrativo forte.

## E.4: Report rotation policy
**Stato:** [FATTO] - S442
**Soluzione:** Script `scripts/sncp/rotate-reports.sh` (--dry-run per preview).
Policy: report con data > 60 giorni -> `reports/archivio/YYYY-MM/`. Report senza data non toccati.
**Dati:** 267 report (215 con data, 52 senza). Gen=39, Feb=98, Mar=78. Totale 3.6MB.

---

# RIEPILOGO

```
+================================================================+
|   SUBROADMAP MIGLIORAMENTI INTERNI V2                           |
+================================================================+

FASE A: Quick Fixes            [####################] 100%
  A.1 Doppia iniezione          FATTO (S442)
  A.2 Checkpoint compattato     FATTO (S442)
  A.3 SNCP legacy pulito        FATTO (S442)

FASE B: Consolidamento         [####################] 100%
  B.1 Modulo comune hooks       FATTO (S442)
  B.2 session/compact DRY       FATTO (S442)
  B.3 _SHARED_DNA ottimizzato   FATTO (S442)

FASE C: Ricerca Strategica    [####################] 100%
  C.1 Prompt Caching            STUDIATO (gia attivo!)
  C.2 Observability             STUDIATO (custom SQLite)
  C.3 A2A Protocol              STUDIATO (MCP prima, A2A post E.5)
  C.4 Model Tiering             DA FARE (futuro)

FASE D: P3 Fixati              [####################] 100%
  D.1 Hook .DISABLED            FATTO (S442)
  D.2 Test collection errors    FATTO (S442)

FASE E: Next                   [####################] 100%
  E.1 F3.6 Observability        FATTO (S442, 9.5/10, 309 test)
  E.2 Agent confini definiti    FATTO (S442)
  E.3 A2A Protocol              FATTO (S442, 32 fonti, decisione: MCP prima)
  E.4 Report rotation           FATTO (S442)

IMPATTO TOTALE S442:
  Context/subagent: -40% (22KB -> 13KB)
  SNCP root: -61% (18 -> 7 entries)
  _SHARED_DNA: -18% (159 -> 131 righe)
  Hooks DRY: 8 hook su modulo comune + observability hook
  Test: +605 recuperati + 58 nuovi observability (6612 totali)
  Dead code: -42KB (hook .DISABLED archiviati)
  Observability: token tracking automatico per sessione
```

---

## RICERCHE COMPLETATE (5 report)

| Report | Path |
|--------|------|
| **AI DevTools Landscape** | reports/RESEARCH_20260312_AI_DEVTOOLS_LANDSCAPE.md |
| **Prompt Caching** | reports/RESEARCH_20260312_PROMPT_CACHING.md |
| **Observability/Langfuse** | reports/RESEARCH_20260312_OBSERVABILITY_LANGFUSE.md |
| **A2A Protocol (tecnico)** | reports/RESEARCH_20260312_A2A_PROTOCOL_TECHNICAL.md |
| **A2A Protocol (strategico)** | reports/SCIENTIST_20260312_A2A_STRATEGIC.md |

---

*"Il diamante si lucida nei dettagli."*
*Cervella & Rafa, S442 - 12 Marzo 2026*
