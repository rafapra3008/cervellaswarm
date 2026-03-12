# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-03-12 - Sessione 443 (continuazione pulizia + infra fix)
> **STATUS:** E.5 T1.6 Guardiana 9.5/10. CI fix. GH Actions allineate. Dependabot piano aggiornato.

---

## QUESTA SESSIONE (S443)

### Cosa abbiamo fatto
1. **T1.6 Guardiana round 2**: F6 Sleep 75s fixato (commento timing + re-measure), F8 role_exclusive doc (docstring PropertyKind arricchita). Score: **9.3 -> 9.5/10**
2. **CI fix critico**: `@cervellaswarm/core` non buildato in CI. Aggiunto `npm ci && npm run build` per core PRIMA dei test CLI in `ci.yml` (lint, test, build-check). Sblocca TUTTE le PR future.
3. **claude-review.yml fix**: Skip Dependabot PRs (`github.actor != 'dependabot[bot]'`). Secret `ANTHROPIC_API_KEY` non accessibile a bot.
4. **GH Actions allineate**: checkout@v6, upload-artifact@v7, download-artifact@v8, upload-pages-artifact@v4. 12 workflow aggiornati. Supera PR #24, #28, #32, #33.
5. **deploy-playground.yml**: checkout v4→v6, upload-pages-artifact v3→v4

### Decisioni prese (con PERCHE)
- **Aggiornamento diretto GH Actions** invece di merge Dependabot: le PR erano parzialmente stale (checkout gia v6 altrove). Fix diretto piu pulito e completo.
- **upload-artifact v6→v7 + download-artifact v4→v8**: v7 backward compatible (nuovo param `archive` default true). Pairing con download-artifact v8 per compatibilita.
- **CI core build step**: la root cause era che `packages/core` e TypeScript ma CI non lo compilava. `file:../core` dep in CLI funziona solo con `dist/`.

---

## MAPPA SITUAZIONE

```
LINGUAGGIO CERVELLASWARM:
  FASE A-D: COMPLETE (28 moduli, media 9.5/10)
  FASE E: PER TUTTI -- QUASI DONE
    E.1 Script "La Nonna"           DONE (S438)
    E.2 IntentBridge Core           DONE (S440, 9.5/10)
    E.3 NL Processing               DONE (S440, 9.5/10)
    E.4 Voice Interface              DONE (S441, 9.5/10)
    E.5 La Nonna Demo               DONE (S442-S443, 9.5/10)
      T1.1-T1.4: DONE | T1.5: pending (tester reale) | T1.6: 9.5/10
    E.6 CervellaLang 1.0            TODO (subroadmap pronta)
  PropertyKind: 9 | CLI: 8 comandi | PyPI: v0.3.0

CI/CD:
  [x] CI core build fix (sblocca TUTTE le PR!)
  [x] claude-review.yml Dependabot skip
  [x] GH Actions allineate (12 workflow)
  [!] CI su main: da verificare dopo push (era rotto pre-fix)

CODEBASE HEALTH (Ingegnera report):
  [!] 5,783 LOC duplicati scripts/ vs packages/ (32%)
  [!] errors.py 2,209 LOC (_CATALOG inline)
  [!] 13 test file > 800 LOC
  [i] 33 funzioni pubbliche senza docstring (22%)
```

---

## PROSSIMA SESSIONE -- COSA FARE

### Commit e verifica CI
- [ ] Commit tutto lavoro S443 (CI fix, GH Actions, tape fix, spec doc, claude-review)
- [ ] Verificare CI verde su main dopo push
- [ ] Chiudere PR Dependabot superate: #24, #28, #32, #33 (GH Actions)

### Dependabot (piano aggiornato)
- [ ] #25 (@types/node patch), #26 (eslint patch), #27 (api minor-patch group) -- SAFE, merge dopo CI verde
- [ ] #11 (zod 3→4), #14 (express 4→5), #29 (inquirer 7→8), #30 (stripe 17→20), #31 (dotenv 16→17) -- MAJOR, sessione dedicata

### Technical debt (sessione dedicata)
- [ ] scripts/ duplication cleanup (5,783 LOC)
- [ ] errors.py extraction: _CATALOG in _error_catalog.py
- [ ] _intent_bridge.py i18n extraction: _STRINGS in file separato
- [ ] Test file splitting: 13 file > 800 LOC

### E.5 completamento
- [ ] T1.5: Test persona non-tecnica (dipende da tester reale)

### Poi: torniamo su LU (Rafa ha detto!)
- E.6 CervellaLang 1.0 (subroadmap: `.sncp/roadmaps/SUBROADMAP_E5_E6_FUTURO.md`)

### TODO Rafa
- Approvare PyPI publish environment su GitHub
- Revisione blog post "From Vibe Coding to Vericoding"

---

## I NUMERI TOTALI

| Metrica | Valore |
|---------|--------|
| Test LU | **3312** |
| Test TOTALI | **6612** (0 collection errors!) |
| Hooks | **16** su cervella_hooks_common.py v1.2.0 |
| Moduli LU | **28** |
| PropertyKind | **9** |

---

## Lezioni Apprese (S443)

### Cosa ha funzionato bene
- **CI debugging con `gh run view --log-failed`** -- trovata root cause in 2 min
- **GH Actions batch fix** -- aggiornare direttamente > merge 4 PR stale
- **Audit strategy confermata** -- implement → Guardiana audit → fix → next step (9.3→9.5)

### Pattern confermato
- **"Se lo vedi, lo sistemi ORA"** -- CI rotto da chissa quando, fixato oggi
- **Workspace deps in CI** -- SEMPRE buildare deps locali prima di test

---

*"Il diamante si lucida nei dettagli."*
*Cervella & Rafa, S443 - 12 Marzo 2026*
