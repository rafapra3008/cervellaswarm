# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-03-12 - Sessione 442 (continua)
> **STATUS:** FASE E in progress. E.1-E.4 DONE! E.5 La Nonna Demo IN PROGRESS. Infra V2 87%!

---

## SESSIONE 442 - E.5 La Nonna Demo

### Step 1-3 DONE (inizio sessione)
- 2 bug critici fixati (pipeline verifica era rotta da S438, try/except mangiava errore)
- NO_DELETION + ROLE_EXCLUSIVE: PropertyKind 7->9, parser + static + runtime checker
- Property explanations i18n, SKIPPED verdict fix, 25 test nuovi

### Step 4: R20 Violation Demo (DONE, audit 9.0->fix->9.5+)
- `_render_violation_demo()` in `_intent_bridge.py`: mostra tentativo bloccato dopo simulazione
- Supporta NO_DELETION (delete bloccato) + ROLE_EXCLUSIVE (ruolo sbagliato bloccato)
- 6 stringhe i18n (3 lingue), integrato come step 5b nella pipeline
- **Guardiana audit 9.0**: F1 P1 BUG (params e tuple, non dict!), F2 P2, F3 P2 -- TUTTI FIXATI
- 15 test violation demo + 6 smoke test pipeline

### Step 5: Subroadmap + Ricerca
- `.sncp/roadmaps/SUBROADMAP_E5_E6_FUTURO.md` creata (4 fasi, ~20 task)
- Ricerca demo/blog (18 fonti): VHS per video, pattern Gleam/Rust/Elm per blog
- Report: `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260312_demo_launch_strategy.md`

---

## MAPPA SITUAZIONE

```
LINGUAGGIO CERVELLASWARM:
  FASE A-D: COMPLETE (25 moduli base, media 9.5/10)
  FASE E: PER TUTTI -- IN PROGRESS
    E.1 Script "La Nonna"           DONE (S438)
    E.2 IntentBridge Core           DONE (S438-S440, 9.5/10)
    E.3 NL Processing               DONE (S440, 9.5/10)
    E.4 Voice Interface              DONE (S441, 9.5/10)
    E.5 La Nonna Demo               IN PROGRESS (S442, T1.1+T1.2+T2.2 done)
    E.6 CervellaLang 1.0            TODO (subroadmap pronta)
  PropertyKind: 9 (+NO_DELETION, +ROLE_EXCLUSIVE)
  PropertyExplanations: 5 (+ role_exclusive)
  PyPI: v0.3.0 (waiting Rafa environment approval)
```

---

## PROSSIMA SESSIONE

### E.5 La Nonna Demo (SUBROADMAP: `.sncp/roadmaps/SUBROADMAP_E5_E6_FUTURO.md`)
- [x] T1.1: R20 Demo violazione interattiva (DONE, audit fixato)
- [x] T1.2: `lu demo` comando autonomo (DONE, 15 test, audit in progress)
- [ ] T1.3: Video recording (VHS tape file, `brew install vhs`)
- [ ] T1.4: Blog post "From Vibe Coding to Vericoding" (hook con Maria)
- [ ] T1.5: Test persona non-tecnica reale
- [ ] T1.6: Guardiana verifica finale 9.5/10
- [x] T2.2: CI Smoke Test pipeline (3 scenari, 6 test, DONE)

### TODO Rafa
- Approvare PyPI publish environment su GitHub

### BACKLOG
- 3 Dependabot PR (SKIP tier): #19, #14, #11
- VS Code Marketplace (publisher account)
- Refactoring P2: _lsp.create_server() 136 righe

---

## SESSIONE PARALLELA: Infrastruttura V2 (Fasi A-D DONE, E 87%)

**Mappa:** `.sncp/roadmaps/SUBROADMAP_MIGLIORAMENTI_INTERNI_V2.md`
**Fatto:** cervella_hooks_common.py v1.2.0 (DRY 10 hook), context/subagent -40%,
SNCP legacy -61%, _SHARED_DNA -18%, 27 test errors->0 (+605 test),
researcher/scienziata confini definiti, rotate-reports.sh (policy 60 giorni),
A2A Protocol studio (31 fonti, decisione: MCP prima, A2A post E.5/durante E.6).
**Pendente:** E.1 Observability (SQLite) -- unico task rimasto!

---

## I NUMERI TOTALI

| Metrica | Valore |
|---------|--------|
| Test LU | **3310** |
| Test TOTALI | **6514** (0 collection errors!) |
| Hooks | **14** su cervella_hooks_common.py v1.2.0 |
| Context/subagent | **~13KB** (-40%) |

---

## Lezioni Apprese (S442)

### Cosa ha funzionato bene
- **Guardiana trova P1 crash bug** -- params e tuple, non dict. Trovato prima del deploy.
- **Ingegnera gap analysis PRIMA** -- 2 bug + 5 gap, Opzione A (narrativa) raccomandata e implementata
- **Ricerca PRIMA di implementare** -- VHS, pattern Gleam/Elm, Czaplicki storytelling

### Pattern confermato
- **"Guardiana dopo ogni step"** (S441, S442 x2) -- anche P3 si fanno, diamante!
- **"Ingegnera analizza PRIMA, Regina implementa"** (S437, S442)
- **"Ricerca PRIMA, codice DOPO"** (Formula Magica, S438, S442)

---

*"Il diamante si lucida nei dettagli."*
*Cervella & Rafa, S442 - 12 Marzo 2026*
<!-- AUTO-CHECKPOINT-START -->
## AUTO-CHECKPOINT: 2026-03-12 07:53 (auto)
- **Branch**: main
- **Ultimo commit**: f1e52964 - S442: E.2 agent boundaries, E.4 report rotation, DRY V3, untrack .DS_Store
- **File modificati** (5):
  - claude/rules/lingua-universale.md
  - .sncp/progetti/cervellaswarm/PROMPT_RIPRESA_cervellaswarm.md
  - .sncp/progetti/contabilita/PROMPT_RIPRESA_contabilita.md
  - .sncp/progetti/miracollo/PROMPT_RIPRESA_miracollo.md
  - .sncp/roadmaps/MAPPA_LINGUAGGIO_CERVELLASWARM.md
<!-- AUTO-CHECKPOINT-END -->
