# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-03-12 - Sessione 442+ (handoff sessione parallela miglioramenti)
> **STATUS:** E.5 La Nonna Demo T1.1-T1.4 DONE. Audit 9.3/10. Codebase health 7.5/10 con azioni.

---

## QUESTA SESSIONE (S442+ parallela)

### Cosa abbiamo fatto
1. **Audit completo E.5** -- Guardiana: 9.3/10. 0 P1, 3 P2 (tutti fixati), 6 P3 (4 fixati)
2. **Analisi codebase Ingegnera** -- 4 P1, 5 P2, 5 P3. Report: `reports/ENGINEER_20260312_FULL_CODEBASE_ANALYSIS.md`
3. **Numeri allineati OVUNQUE** -- test count era stale in 8+ file (5221→6612, 2909→3312, 25→28 moduli)
4. **README LU aggiornato** -- mancava Fase E intera! Aggiunto chat+demo, voice, NL in CLI, architecture, comparison
5. **README principale aggiornato** -- badge 5221→6612, hooks 15→16, sessions 437→442, moduli 25→28
6. **P1: node_modules rimossi da git** -- 4,692 file (71% del repo!) erano tracciati. `git rm --cached` fatto
7. **P1: Eccezione silenziosa fixata** -- `_intent_bridge.py:1096` ora ha `warnings.warn()` (BUG pattern S442)
8. **P1: Symlink rotto rimosso** -- `scripts/sncp/smart_search.py` puntava a file inesistente
9. **Blog fix** -- GIF path corretto + caption guided/NL mode mismatch
10. **Memoria pulita** -- session-history.md 211→45 righe, packages.md aggiornato, MEMORY.md indice aggiornato
11. **Dependabot audit** -- 11 PR aperte (era 3!), piano prioritizzato: 2 safe, 2 con cautela, 3 major, 4 GH Actions
12. **Dead code test rimosso** -- test_violation_demo_appears: 2 session inutilizzate

### Decisioni prese (con PERCHE)
- **Blog caption invece di riscrivere**: GIF mostra guided mode (4 property), narrazione e NL mode (5 property). Caption distingue i due. PERCHE: riscrivere la narrazione avrebbe perso il potere della storia di Maria.
- **warnings.warn() invece di raise**: pipeline verifica formale fallisce gracefully ma ORA logga. PERCHE: crash bloccherebbe la chat, ma silenzio nascondeva bug per 4 sessioni.
- **node_modules git rm --cached**: file restano su disco ma non piu tracciati. PERCHE: erano committati prima che .gitignore li escludesse.

---

## MAPPA SITUAZIONE

```
LINGUAGGIO CERVELLASWARM:
  FASE A-D: COMPLETE (28 moduli, media 9.5/10)
  FASE E: PER TUTTI -- IN PROGRESS
    E.1 Script "La Nonna"           DONE (S438)
    E.2 IntentBridge Core           DONE (S440, 9.5/10)
    E.3 NL Processing               DONE (S440, 9.5/10)
    E.4 Voice Interface              DONE (S441, 9.5/10)
    E.5 La Nonna Demo               QUASI DONE (S442, T1.1-T1.4 DONE, audit 9.3/10)
    E.6 CervellaLang 1.0            TODO (subroadmap pronta)
  PropertyKind: 9 | CLI: 8 comandi | PyPI: v0.3.0
  INFRA V2: 100% completata

CODEBASE HEALTH (Ingegnera report):
  [!] 5,783 LOC duplicati scripts/ vs packages/ (32% di scripts/)
  [!] errors.py 2,209 LOC (_CATALOG inline 1,172 righe)
  [!] 13 test file > 800 LOC (max 1,345)
  [i] 33 funzioni pubbliche senza docstring (22%)
  [i] 8 funzioni > 100 LOC candidabili a refactoring
```

---

## PROSSIMA SESSIONE -- COSA FARE

### Quick wins (< 30 min cad.)
- [ ] **Commit** tutto il lavoro di questa sessione (node_modules, fix, README, blog, mappe)
- [ ] **T1.6 Guardiana round 2**: da 9.3→9.5 (fixare P3 F6 Sleep 75s, F8 doc role_exclusive)
- [ ] **PROMPT_RIPRESA_miracollo**: 183 righe (33 oltre limite 150) -- chiedere a Rafa come procedere

### Dependabot (piano prioritizzato)
- [ ] Merge #26 (@types/node) + #21 (express-rate-limit security fix) -- SAFE
- [ ] Investigare CI "CervellaSwarm Review" workflow failure su PR bot
- [ ] #24 (eslint patch) + #14 (dotenv) -- con cautela, verificare Node 18
- [ ] #18 (express v5), #8 (zod v4), #15 (@inquirer/prompts v8) -- MAJOR, sessione dedicata
- [ ] #17, #22, #23, #25 (GitHub Actions) -- batch insieme

### Technical debt (sessione dedicata, Ingegnera + Regina)
- [ ] **scripts/ duplication cleanup**: 16 file divergenti tra scripts/ e packages/ (5,783 LOC)
- [ ] **errors.py extraction**: estrarre _CATALOG in _error_catalog.py (dimezza il file)
- [ ] **_intent_bridge.py i18n extraction**: estrarre _STRINGS in file separato
- [ ] **Test file splitting**: 13 file > 800 LOC da splittare in coppie logiche

### E.5 completamento
- [ ] T1.5: Test persona non-tecnica (dipende da tester reale disponibile)
- [ ] T1.6: Guardiana finale 9.5/10

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
| Context/subagent | **~13KB** (-40%) |
| Moduli LU | **28** |
| PropertyKind | **9** |

---

## FILE CHIAVE TOCCATI (questa sessione)

| File | Cosa |
|------|------|
| README.md (root) | Badge 5221→6612, hooks, sessions, moduli |
| packages/lingua-universale/README.md | +Fase E, +chat/demo/voice, 25→28 moduli |
| packages/lingua-universale/docs/blog_vibe_to_vericoding.md | GIF path fix + caption guided/NL |
| _intent_bridge.py:1096 | warnings.warn() su except silenziosa |
| test_intent_bridge_session_e2e.py | Dead code rimosso (F9) |
| packages/mcp-server/node_modules/ | Rimosso da git tracking (4,692 file) |
| scripts/sncp/smart_search.py | Symlink rotto rimosso |
| NORD.md | Test 6514→6612, hooks 14→16 |
| .sncp/roadmaps/SUBROADMAP_E5_E6_FUTURO.md | T1.4 DONE, numeri aggiornati |
| .sncp/roadmaps/SUBROADMAP_MIGLIORAMENTI_INTERNI_V2.md | Numeri aggiornati |
| .claude/rules/lingua-universale.md | Test 3310→3312 |
| Memoria (session-history.md) | 211→45 righe (solo non-derivabile) |
| Memoria (packages.md) | Aggiornato con numeri reali |

---

## Lezioni Apprese (S442+ parallela)

### Cosa ha funzionato bene
- **Guardiana + Ingegnera in parallelo** -- 2 prospettive complementari, finding si confermano a vicenda
- **Allineamento numeri PRIMA di nuove feature** -- stale numbers = credibilita persa
- **node_modules in git = bomba silenziosa** -- .gitignore non retroattivo, serviva git rm --cached

### Pattern confermato
- **"Ingegnera analizza PRIMA, Regina implementa"** (S437, S442, S442+)
- **"Se lo vedi, lo sistemi ORA"** (COSTITUZIONE) -- 12 fix in una sessione

---

*"Il diamante si lucida nei dettagli."*
*Cervella & Rafa, S442+ - 12 Marzo 2026*
