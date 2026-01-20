# SUBROADMAP W6 - CASA PERFETTA

> **Creato:** 20 Gennaio 2026 - Sessione 292
> **Obiettivo:** Portare la casa da 9.3/10 a 10/10
> **Target Score:** 9.5/10 per ogni Day

---

## VISIONE W6

```
+================================================================+
|                                                                |
|   W6: CASA PERFETTA                                            |
|                                                                |
|   "Prima la casa, poi il mondo."                               |
|                                                                |
|   Sistemare tutto per LA FAMIGLIA:                             |
|   - SNCP aggiornato                                            |
|   - Script perfetti                                            |
|   - Workflow fluidi                                            |
|   - Zero tech debt                                             |
|                                                                |
+================================================================+
```

---

## PREREQUISITI

| Cosa | Status | Verifica |
|------|--------|----------|
| W5 completata | DONE | NORD.md aggiornato |
| Infrastruttura OK | DONE | Guardiana Ops: 5/5 |
| Nessun blocco critico | DONE | Guardiana Qualita: 10/10 |

---

## DAY 1: SNCP + PULIZIA (Leggero)

### Obiettivo
Aggiornare tutti i file SNCP e pulire TODO/FIXME nei script.

### Task

| ID | Task | File | AC |
|----|------|------|-----|
| D1-01 | Aggiornare stato.md con W5 | `.sncp/progetti/cervellaswarm/stato.md` | Contiene W5 100% |
| D1-02 | Aggiornare oggi.md | `.sncp/stato/oggi.md` | Data corrente |
| D1-03 | Review TODO in script | `scripts/**/*.sh` | Lista TODO documentata |
| D1-04 | Fix TODO critici (se presenti) | vari | 0 TODO critici |

### Acceptance Criteria

```bash
# AC-D1-01: stato.md aggiornato
grep -c "W5" .sncp/progetti/cervellaswarm/stato.md
# Expected: >= 1

# AC-D1-02: oggi.md con data corrente
head -5 .sncp/stato/oggi.md
# Expected: contiene "Gennaio 2026"

# AC-D1-03: TODO documentati
grep -r "TODO\|FIXME" scripts/*.sh | wc -l
# Expected: documentato in report

# AC-D1-04: Nessun TODO critico
grep -r "TODO.*CRITICAL\|FIXME.*CRITICAL" scripts/*.sh | wc -l
# Expected: 0
```

### Deliverable
- stato.md aggiornato
- oggi.md aggiornato
- Report TODO: `.swarm/tasks/W6_D1_TODO_REPORT.md`

### Score Target: 9.5/10

---

## DAY 2: TREE-SITTER HOOKS (Medio)

### Obiettivo
Migrare i pre-commit hooks per usare Tree-sitter per validazione codice.

### Context
Da W2 abbiamo TreeSitterParser ma non lo usiamo nei hooks.
Opportunita: validare sintassi Python/JS prima del commit.

### Task

| ID | Task | File | AC |
|----|------|------|-----|
| D2-01 | Creare hook validate_syntax.py | `hooks/validate_syntax.py` | Usa TreeSitterParser |
| D2-02 | Integrare in pre-commit | `.hooks/pre-commit` | Chiama validate_syntax |
| D2-03 | Test su file Python valido | test manuale | Exit 0 |
| D2-04 | Test su file Python invalido | test manuale | Exit 1 + messaggio |
| D2-05 | Documentare in HOOKS.md | `docs/HOOKS.md` | Sezione validate_syntax |

### Acceptance Criteria

```bash
# AC-D2-01: Hook esiste
ls -la hooks/validate_syntax.py
# Expected: file presente

# AC-D2-02: Usa TreeSitterParser
grep -c "TreeSitterParser" hooks/validate_syntax.py
# Expected: >= 1

# AC-D2-03: Test valido
echo "def foo(): pass" > /tmp/test_valid.py
python3 hooks/validate_syntax.py /tmp/test_valid.py
echo "Exit: $?"
# Expected: Exit: 0

# AC-D2-04: Test invalido
echo "def foo(" > /tmp/test_invalid.py
python3 hooks/validate_syntax.py /tmp/test_invalid.py
echo "Exit: $?"
# Expected: Exit: 1
```

### Deliverable
- `hooks/validate_syntax.py` funzionante
- Pre-commit integrato
- `docs/HOOKS.md` aggiornato

### Score Target: 9.5/10

---

## DAY 3: WITH-CONTEXT DEFAULT (Medio)

### Obiettivo
Analizzare e decidere se `--with-context` deve essere default in spawn-workers.

### Context
Attualmente `--with-context` e opt-in.
Domanda: dovrebbe essere default per tutti i worker?

### Task

| ID | Task | File | AC |
|----|------|------|-----|
| D3-01 | Analisi pro/contro | Report | Decisione documentata |
| D3-02 | Test performance con context | Benchmark | Tempo misurato |
| D3-03 | Test performance senza context | Benchmark | Tempo misurato |
| D3-04 | Proposta finale | Report | Raccomandazione chiara |
| D3-05 | Implementare SE approvato | `spawn-workers.sh` | Codice aggiornato |

### Acceptance Criteria

```bash
# AC-D3-01: Report analisi esiste
ls -la .swarm/tasks/W6_D3_CONTEXT_ANALYSIS.md
# Expected: file presente

# AC-D3-02/03: Benchmark documentato
grep -c "benchmark\|tempo\|performance" .swarm/tasks/W6_D3_CONTEXT_ANALYSIS.md
# Expected: >= 3

# AC-D3-04: Raccomandazione presente
grep -c "RACCOMANDAZIONE\|DECISIONE" .swarm/tasks/W6_D3_CONTEXT_ANALYSIS.md
# Expected: >= 1
```

### Deliverable
- `.swarm/tasks/W6_D3_CONTEXT_ANALYSIS.md`
- Implementazione (se approvata)

### Score Target: 9.5/10

---

## DAY 4: SCRIPT POLISH (Leggero)

### Obiettivo
Fix problemi minori trovati dalle Guardiane + spawn-workers --version.

### Task

| ID | Task | File | AC |
|----|------|------|-----|
| D4-01 | Implementare --version in spawn-workers | `spawn-workers.sh` | Flag funziona |
| D4-02 | Fix import path SymbolExtractor | `scripts/utils/` | Import funziona |
| D4-03 | Verificare tutti gli script hanno --help | `scripts/**/*.sh` | 100% coverage |
| D4-04 | Test spawn-workers tutti i flag | Test manuale | Tutti OK |

### Acceptance Criteria

```bash
# AC-D4-01: --version funziona
spawn-workers --version
# Expected: output con versione

# AC-D4-02: Import funziona
python3 -c "from scripts.utils.symbol_extractor import SymbolExtractor; print('OK')"
# Expected: OK

# AC-D4-03: --help coverage
for f in scripts/architect/*.sh; do $f --help > /dev/null 2>&1 && echo "$f OK"; done
# Expected: tutti OK

# AC-D4-04: spawn-workers flag test
spawn-workers --list > /dev/null && echo "list OK"
spawn-workers --help > /dev/null && echo "help OK"
# Expected: tutti OK
```

### Deliverable
- spawn-workers.sh con --version
- Import path fixato
- Report flag coverage

### Score Target: 9.5/10

---

## DAY 5: TEST FAMIGLIA COMPLETO (Leggero)

### Obiettivo
Test E2E di tutta la famiglia: ogni agente fa un task semplice.

### Task

| ID | Task | AC |
|----|------|-----|
| D5-01 | Test cervella-backend | Risponde correttamente |
| D5-02 | Test cervella-frontend | Risponde correttamente |
| D5-03 | Test cervella-tester | Risponde correttamente |
| D5-04 | Test cervella-architect | Crea plan |
| D5-05 | Test 3 Guardiane | Audit funziona |
| D5-06 | Report famiglia | Tutti 16 testati |

### Acceptance Criteria

```bash
# AC-D5-01 a D5-05: Test individuali
# Ogni agente risponde con output strutturato
# TIMEOUT: 2 minuti per agente (max 5 min per Guardiane Opus)

# AC-D5-06: Report completo
ls -la .swarm/tasks/W6_D5_FAMIGLIA_TEST.md
# Expected: file presente con 16+ test documentati
```

### Deliverable
- `.swarm/tasks/W6_D5_FAMIGLIA_TEST.md`
- Tutti i 16 agenti testati
- Score famiglia: target 16/16

### Score Target: 9.5/10

---

## RIEPILOGO W6

| Day | Focus | Effort | Target |
|-----|-------|--------|--------|
| 1 | SNCP + Pulizia | Leggero | 9.5/10 |
| 2 | Tree-sitter Hooks | Medio | 9.5/10 |
| 3 | With-context Default | Medio | 9.5/10 |
| 4 | Script Polish | Leggero | 9.5/10 |
| 5 | Test Famiglia | Leggero | 9.5/10 |

**Media Target W6:** 9.5/10

---

## DIPENDENZE

```
Day 1 → indipendente
Day 2 → indipendente
Day 3 → indipendente
Day 4 → dopo Day 1 (TODO review)
Day 5 → dopo Day 2-4 (script fixati)
```

---

## PRE-DAY CHECKPOINT

Prima di ogni Day, eseguire:
```bash
git status
git stash  # se modifiche pending
git tag w6-dayN-start  # N = numero day
```

---

## ROLLBACK PLAN

Se un Day fallisce:
```bash
git stash pop  # recupera modifiche
git reset --soft HEAD~1  # annulla ultimo commit
# Riprovare con fix
```

---

## CRITERI COMPLETAMENTO W6

```
[ ] Day 1: SNCP aggiornato, 0 TODO critici
[ ] Day 2: validate_syntax.py funzionante
[ ] Day 3: Analisi --with-context completata
[ ] Day 4: spawn-workers --version funziona
[ ] Day 5: 16/16 agenti testati

SCORE MINIMO ACCETTABILE: 9.0/10 per ogni Day
TARGET: 9.5/10 per ogni Day
```

---

## FILOSOFIA

> "Prima la casa, poi il mondo."
> "Fatto BENE > Fatto VELOCE"
> "I dettagli fanno SEMPRE la differenza."

---

*Creato: Sessione 292 - Cervella & Rafa*
*"Ultrapassar os proprios limites!"*
