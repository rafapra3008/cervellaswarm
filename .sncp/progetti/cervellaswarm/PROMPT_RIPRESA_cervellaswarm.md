# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-03-12 - Sessione 442 (checkpoint)
> **STATUS:** FASE E in progress. E.1-E.4 DONE! E.5 La Nonna Demo QUASI DONE (T1.1-T1.4)!

---

## SESSIONE 442 - E.5 La Nonna Demo

### Step 1-3 DONE (inizio sessione, pre-compact)
- 2 bug critici fixati (pipeline verifica era rotta da S438, try/except mangiava errore)
- NO_DELETION + ROLE_EXCLUSIVE: PropertyKind 7->9, parser + static + runtime checker
- Property explanations i18n, SKIPPED verdict fix, 25 test nuovi

### Step 4: R20 Violation Demo (DONE, Guardiana 9.5+)
- `_render_violation_demo()` in `_intent_bridge.py`: mostra tentativo bloccato
- Supporta NO_DELETION + ROLE_EXCLUSIVE, 6 stringhe i18n (3 lingue)
- **Guardiana**: F1 P1 BUG (params e tuple, non dict!), F2 P2, F3 P2 -- TUTTI FIXATI
- 15 test violation demo + 6 smoke test pipeline

### Step 5: Subroadmap + Ricerca (DONE)
- `.sncp/roadmaps/SUBROADMAP_E5_E6_FUTURO.md` creata (4 fasi, ~20 task)
- Ricerca demo/blog (18 fonti): VHS, pattern Gleam/Rust/Elm per blog
- Report: `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260312_demo_launch_strategy.md`

### Step 6: `lu demo` Command T1.2 (DONE, Guardiana 9.5/10)
- `_cmd_demo()` in `_cli.py`: demo scripted con typewriter effect
- 3 lingue (it/en/pt), 3 velocita (slow/normal/fast), injectable I/O
- **Guardiana 9.5/10**: 5 P3 fixati (test PT output, EOFError, pipeline code, kwargs, tautologico)
- 17 test (7 parser + 10 execution/output)

### Step 7: Video VHS T1.3 (DONE, Guardiana audit pending)
- VHS tape files: `packages/lingua-universale/demo/demo_la_nonna.tape` (full MP4) + `demo_la_nonna_short.tape` (GIF)
- GIF README: 3.3MB (< 5MB target, ottimizzato con gifsicle, 5x speed, 6fps)
- MP4 YouTube: 4.4MB (slow speed, Catppuccin Frappe theme)
- Momento "VIOLAZIONE RILEVATA!" visibile nella demo

### Step 8: Blog Post T1.4 (IN PROGRESS)
- Marketing agent sta scrivendo "From Vibe Coding to Vericoding"
- File target: `packages/lingua-universale/docs/blog_vibe_to_vericoding.md`

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
    E.5 La Nonna Demo               IN PROGRESS (S442, T1.1-T1.3 DONE, T1.4 in progress)
    E.6 CervellaLang 1.0            TODO (subroadmap pronta)
  PropertyKind: 9 (+NO_DELETION, +ROLE_EXCLUSIVE)
  PyPI: v0.3.0 (waiting Rafa environment approval)
  CLI: 8 comandi (check, run, verify, compile, repl, lsp, chat, demo)
```

---

## PROSSIMA SESSIONE

### E.5 La Nonna Demo (SUBROADMAP: `.sncp/roadmaps/SUBROADMAP_E5_E6_FUTURO.md`)
- [x] T1.1: R20 Demo violazione interattiva (Guardiana 9.5+)
- [x] T1.2: `lu demo` comando autonomo (Guardiana 9.5/10, 5 P3 fixati)
- [x] T1.3: Video VHS (GIF 3.3MB + MP4 4.4MB, Catppuccin Frappe)
- [~] T1.4: Blog post "From Vibe Coding to Vericoding" (Marketing in progress)
- [ ] T1.5: Test persona non-tecnica reale
- [ ] T1.6: Guardiana verifica finale 9.5/10
- [x] T2.2: CI Smoke Test pipeline (3 scenari, 6 test)

### TODO Rafa
- Approvare PyPI publish environment su GitHub
- Revisione blog post quando pronto

### BACKLOG
- 3 Dependabot PR (SKIP tier): #19, #14, #11
- VS Code Marketplace (publisher account)
- Refactoring P2: _lsp.create_server() 136 righe
- .gitignore: aggiungere demo/*.gif e demo/*.mp4 (generati da tape files)

---

## SESSIONE PARALLELA: Infrastruttura V2 -- COMPLETATA!

**Mappa:** `.sncp/roadmaps/SUBROADMAP_MIGLIORAMENTI_INTERNI_V2.md`
**Fatto:** cervella_hooks_common.py v1.2.0 (DRY 10 hook), context/subagent -40%,
SNCP legacy -61%, _SHARED_DNA -18%, 27 test errors->0 (+605 test),
researcher/scienziata confini definiti, rotate-reports.sh (policy 60 giorni),
A2A Protocol studio (32 fonti), **E.1 Observability DONE (9.5/10)**.

---

## I NUMERI TOTALI

| Metrica | Valore |
|---------|--------|
| Test LU | **3312** |
| Test TOTALI | **6616+** (0 collection errors!) |
| Hooks | **16** su cervella_hooks_common.py v1.2.0 |
| Context/subagent | **~13KB** (-40%) |

---

## Lezioni Apprese (S442)

### Cosa ha funzionato bene
- **Guardiana trova P1 crash bug** -- params e tuple, non dict. Pre-deploy.
- **Ingegnera gap analysis PRIMA** -- 2 bug + 5 gap, Opzione A raccomandata
- **Ricerca PRIMA di implementare** -- VHS, Gleam/Elm, Czaplicki storytelling
- **VHS pixel dimensions** -- Width/Height sono PIXEL non caratteri (errore "40x80")
- **gifsicle per ottimizzare GIF** -- da 6.5MB a 3.3MB con lossy=80 + colors=128

### Pattern confermato
- **"Guardiana dopo ogni step"** (S441, S442 x4!) -- anche P3 si fanno
- **"Ingegnera analizza PRIMA, Regina implementa"** (S437, S442)
- **"Ricerca PRIMA, codice DOPO"** (Formula Magica, S438, S442)

---

*"Il diamante si lucida nei dettagli."*
*Cervella & Rafa, S442 - 12 Marzo 2026*
