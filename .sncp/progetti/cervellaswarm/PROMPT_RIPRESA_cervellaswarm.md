# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-03-12 - Sessione 442
> **STATUS:** FASE E in progress. E.1-E.4 DONE! E.5 La Nonna Demo IN PROGRESS. Infra V2 DONE!

---

## SESSIONE 442 - Due fronti paralleli

### Fronte 1: E.5 La Nonna Demo (Step 1-3 DONE)

**2 Bug Critici Fixati (P0):**
- `_intent_bridge.py`: spec format sbagliato (`spec NAME:` doveva essere `properties for NAME:`, `requires prop` doveva essere `prop.replace('_', ' ')`). Il try/except mangiava l'errore in silenzio da S438.
- `result.property_name` non esiste su PropertyResult. Corretto: `result.spec.kind.value`.

**2 Nuove Proprieta (R22/R23):** NO_DELETION + ROLE_EXCLUSIVE in spec.py (parser + static + runtime).
Property Explanations (R7): 4 proprieta x 3 lingue in `_render_confirmation()`.
SKIPPED verdict fix (F10): giallo non rosso. Test: 3274 (25 nuovi), 0 regressioni.

### Fronte 2: Infrastruttura V2 (Fasi A-D COMPLETE!)

**Mappa completa:** `.sncp/roadmaps/SUBROADMAP_MIGLIORAMENTI_INTERNI_V2.md`

| Fase | Cosa | Impatto |
|------|------|---------|
| A.1 | Fix doppia iniezione COSTITUZIONE | -3.2KB/subagent |
| A.2 | Checkpoint compattato | -64% template |
| A.3 | SNCP legacy archiviato | 18 a 7 entries (-61%) |
| B.1 | cervella_hooks_common.py (NUOVO!) | 1 file vs 8 per aggiungere progetto |
| B.2 | session_end + pre_compact DRY | git separator %x00, docstring fix |
| B.3 | _SHARED_DNA ottimizzato | 159 a 131 righe (-18%) |
| C.1 | Prompt caching ricerca | Gia attivo! Nessuna azione |
| C.2 | Observability ricerca | Custom SQLite > Langfuse |
| D.1 | 9 hook .DISABLED archiviati | -42KB dead code |
| D.2 | Test collection errors fixati | 27 a 0, +605 test recuperati |

**Risultato:** Context/subagent -40%, test 5909 a 6514, zero collection errors.
**Hook:** 14/14 funzionanti, tutti su cervella_hooks_common.py (DRY!).
**Report S442:** 3 ricerche + 1 audit + 1 analisi ingegnera in reports/

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
    E.5 La Nonna Demo               IN PROGRESS (S442, Step 1-3 done)
    E.6 CervellaLang 1.0            TODO
  PropertyKind: 9 (+NO_DELETION, +ROLE_EXCLUSIVE)
  PyPI: v0.3.0 (waiting Rafa environment approval)

INFRA V2 (S442): Fasi A-D COMPLETE!
  Fase E (next): Observability, Agent unificazione, A2A, Report rotation
```

---

## PROSSIMA SESSIONE

### E.5 La Nonna Demo -- Step rimanenti
- [ ] R20: Demo violazione interattiva (Atto 5 Scena 5.3)
- [ ] Video registrato + blog post
- [ ] Test persona non-tecnica reale
- [ ] Guardiana verifica finale 9.5/10

### Infra V2 Fase E (next)
- [ ] E.1: Observability Layer (custom SQLite su event-store, ~150 LOC stop hook)
- [ ] E.2: Researcher/Scienziata unificazione ruoli
- [ ] E.3: A2A Protocol studio approfondito
- [ ] E.4: Report rotation policy (263 file, 3.5MB)

### TODO Rafa
- Approvare PyPI publish environment su GitHub

### BACKLOG
- 3 Dependabot PR (SKIP tier): #19, #14, #11
- VS Code Marketplace (publisher account)
- Refactoring P2: _lsp.create_server() 136 righe

---

## I NUMERI TOTALI

| Metrica | Valore |
|---------|--------|
| Test LU | **3274** |
| Test TOTALI | **6514** (0 collection errors!) |
| Moduli LU | **28** |
| PropertyKind | **9** |
| Hooks | **14** su cervella_hooks_common.py |
| Context/subagent | **~13KB** (-40%) |

---

## Lezioni Apprese (S442)

### Cosa ha funzionato bene
- **DRY hooks con modulo comune** -- cervella_hooks_common.py elimina duplicazione progetto
- **importlib import mode** -- risolve module collision monorepo senza rinominare file
- **Ingegnera gap analysis PRIMA** -- 2 bug + 5 gap trovati, zero sorprese
- **Sessione parallela miglioramenti** -- non tocca codice prodotto, lavora in pace

### Pattern confermato
- **"Guardiana dopo ogni step"** (S441, S442) -- anche P3 si fanno, diamante!
- **"Ingegnera analizza PRIMA, Regina implementa"** (S437, S442)

---

*"Il diamante si lucida nei dettagli."*
*Cervella & Rafa, S442 - 12 Marzo 2026*
