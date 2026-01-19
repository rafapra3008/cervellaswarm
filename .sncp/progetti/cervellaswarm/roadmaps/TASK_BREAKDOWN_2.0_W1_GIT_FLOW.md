# TASK BREAKDOWN - CervellaSwarm 2.0 Week 1

> **Feature:** Git Flow + Attribution
> **Periodo:** 20-26 Gennaio 2026
> **Basato su:** Studio Aider Git Integration
> **Ultimo aggiornamento:** 19 Gennaio 2026 - Sessione 272

---

## OBIETTIVO

```
OGGI:
  Commit manuali → inconsistenti → storia confusa

DOPO W1:
  Auto-commit → conventional → storia professionale
  "feat(api): add login (cervella-backend)"
```

---

## STATO REALE (Sessione 272)

```
+================================================================+
|  Day 1: SETUP           [####################] 100% DONE       |
|  Day 2: CONVENTIONAL    [####################] 100% DONE 9.7!  |
|  Day 3: ATTRIBUTION     [####################] 100% DONE       |
|  Day 4: INTEGRAZIONE    [                    ]   0% DA FARE    |
|  Day 5: UNDO            [####################] 100% DONE       |
|  Day 6-7: DOCS          [                    ]   0% DA FARE    |
+================================================================+
```

---

## TASK GIORNALIERI

### Giorno 1 (Sessione 271): SETUP + SCRIPT BASE ✅ COMPLETATO

**Task 1.1: Creare script auto-commit** ✅
```
File: scripts/utils/git_worker_commit.sh (v1.2.2, 720+ righe)

Funzionalita IMPLEMENTATE:
- Riceve: worker_name, scope, message ✅
- Genera: conventional commit ✅
- Aggiunge: Co-authored-by attribution ✅
- EXTRA: --dry-run, --staged-only, --allow-hooks ✅
```

**Task 1.2: Creare template prompt** ✅
```
File: .sncp/templates/commit_message_prompt.txt ✅
```

**Definition of Done:**
- [x] Script creato
- [x] Template creato
- [x] Test manuale OK
- [x] Audit Guardiana: 9.5/10

---

### Giorno 2 (Sessione 272): CONVENTIONAL COMMITS ✅ COMPLETATO

**Task 2.1: Implementare parser tipo commit** ✅
```
TIPI SUPPORTATI (10 tipi):
- feat, fix, docs, style, refactor, test, chore, perf, ci, build ✅

EXTRA Day 2:
- auto_detect_type() - suggerisce tipo dai file! ✅
- Flag --auto per auto-detect completo ✅
```

**Task 2.2: Implementare scope detection** ✅
```
SCOPE AUTO-DETECT (13 patterns):
- packages/cli/* → cli ✅
- packages/mcp-server/* → mcp ✅
- src/* → src ✅ (aggiunto Day 2)
- .sncp/* → sncp ✅ (aggiunto Day 2)
- reports/* → reports ✅ (aggiunto Day 2)
- docs/* → docs ✅
- scripts/* → scripts ✅
- *api* → api ✅
- *component* → ui ✅
- *test* → test ✅
- .claude/* → hooks ✅
- *.config.* → config ✅ (aggiunto Day 2)
- *migration* → db ✅ (aggiunto Day 2)
```

**Definition of Done:**
- [x] Parser tipo funziona
- [x] Scope auto-detect funziona (13 patterns!)
- [x] Test su 5 commit diversi
- [x] Audit Guardiana: 9.7/10

---

### Giorno 3 (Sessione 271): ATTRIBUTION ✅ COMPLETATO

**Task 3.1: Implementare Co-authored-by** ✅
```
FORMATO IMPLEMENTATO:
Co-authored-by: CervellaSwarm (backend-worker/claude-sonnet-4-5) <noreply@cervellaswarm.com>

Legge da JSON (single source of truth) ✅
```

**Task 3.2: Creare mapping worker → attribution** ✅
```
File: scripts/utils/worker_attribution.json (v1.1.0)

MAPPING COMPLETO 16/16:
- 12 workers (backend, frontend, tester, docs, reviewer, devops,
              researcher, data, security, scienziata, ingegnera, marketing)
- 3 guardiane (qualita, ops, ricerca)
- 1 special (regina + orchestrator alias)
```

**Definition of Done:**
- [x] Attribution corretta per ogni worker
- [x] JSON mapping creato (16/16 agenti)
- [x] Test integration

---

### Giorno 4: INTEGRAZIONE CLI ❌ DA FARE

**Task 4.1: Integrare in spawn-workers** ❌
```
STATO: NON INIZIATO

spawn-workers (v3.5.0) NON chiama git_worker_commit.sh
Richiede decisione architetturale:
  A) Auto-commit sempre
  B) Commit manuale
  C) Flag --auto-commit

COMPLESSITA: spawn-workers apre finestre/tmux separate
```

**Task 4.2: Flag --no-commit** ❌
```
STATO: NON INIZIATO
Dipende da Task 4.1
```

**Definition of Done:**
- [ ] Integrazione spawn-workers completa
- [ ] Flag --no-commit funziona
- [ ] Test end-to-end

---

### Giorno 5 (Sessione 271+272): UNDO COMMAND ✅ COMPLETATO

**Task 5.1: Implementare /undo** ✅
```
COMPORTAMENTO IMPLEMENTATO:
1. Verifica ultimo commit e CervellaSwarm ✅
2. git reset --soft HEAD^ ✅ (fixato Sessione 272!)
3. Mostra stato modifiche ✅
```

**Task 5.2: Safety checks** ✅
```
PROTEZIONI IMPLEMENTATE:
- Non undo commit non-CervellaSwarm ✅
- Mostra warning prima di undo ✅
- Preserva modifiche staged (--soft) ✅
```

**Definition of Done:**
- [x] /undo funziona
- [x] Safety checks attivi
- [ ] Documentazione scritta (Day 6-7)

---

### Giorno 6-7: DOCS + POLISH ❌ DA FARE

**Task 6.1: Documentazione** ❌
```
File: docs/GIT_ATTRIBUTION.md

Contenuto DA SCRIVERE:
- Come funziona auto-commit
- Formato messaggi
- Come fare undo
- Esempi
```

**Task 6.2: Test completi** ⚠️ PARZIALE
```
Test scenarios:
- [x] Nuovo file creato (dry-run test)
- [x] File modificato (dry-run test)
- [ ] File eliminato
- [x] Multiple file changes (dry-run test)
- [ ] Undo dopo commit (test reale)
```

**Definition of Done:**
- [ ] Docs complete
- [ ] Tutti i test passano
- [ ] README aggiornato

---

## COMMIT MESSAGE ESEMPIO FINALE

```
feat(api): Add authentication endpoints

Implemented login/register/me endpoints with JWT tokens.
Added password hashing and token validation.

Co-authored-by: CervellaSwarm (backend-worker/claude-sonnet-4-5) <noreply@cervellaswarm.com>
```

---

## METRICHE SUCCESSO W1

| Metrica | Target | Stato |
|---------|--------|-------|
| Script funzionante | 100% | ✅ v1.2.2 |
| Conventional Commits | 100% formato | ✅ 10 tipi |
| Attribution | Tutti mappati | ✅ 16/16 |
| /undo | Funziona + safety | ✅ --soft |
| Scope auto-detect | Funziona | ✅ 13 patterns |
| Type auto-detect | Funziona | ✅ --auto flag |
| CLI Integration | Completa | ❌ Da fare |
| Docs | Complete | ❌ Da fare |

---

## PROSSIMI STEP

1. **Decisione architetturale**: Come integrare in spawn-workers?
2. **Documentazione**: docs/GIT_ATTRIBUTION.md
3. **Test reali**: Undo dopo commit vero

---

*Creato: 19 Gennaio 2026 - Sessione 270*
*Aggiornato: 19 Gennaio 2026 - Sessione 272 (stato reale verificato)*
