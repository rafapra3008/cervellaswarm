# PLAN: Test Edge Case Directory Missing

> **Architect:** cervella-architect (Opus)
> **Data:** 2026-01-19
> **Task:** Implementare test per edge case "directory missing"

---

## Phase 1: Understanding

### Cosa Vuole l'Utente

Test specifici per verificare che il sistema gestisca correttamente i casi in cui directory critiche sono mancanti:
- `.swarm/` non esiste
- `.swarm/plans/` non esiste
- `.sncp/` non esiste
- Subdirectory mancanti

### Codebase Analysis

**Test Framework Esistente:**
- Bash tests: `tests/bash/test_*.sh` - Framework custom con `run_test()`
- Python tests: `tests/swarm/test_*.py` - pytest
- Node.js tests: `packages/cli/test/*.test.js` - node:test

**Helper per Directory:**
- `tests/bash/test_common.sh:88-90` - `assert_file_exists()` per verifiche
- `packages/cli/test/helpers/temp-dir.js` - `createTempDir()`, `verifyFileStructure()`

**Script Che Creano Directory:**
- `scripts/swarm/swarm-init.sh:80-86` - Crea struttura `.swarm/`
- `scripts/swarm/common.sh:135-154` - `find_project_root()` cerca `.swarm/`
- `packages/cli/src/sncp/init.js:22-35` - Crea struttura `.sncp/`

**Test Esistenti Simili:**
- `tests/bash/test_spawn_workers.sh:95-111` - `test_no_spawn_without_swarm()` verifica comportamento fuori progetto
- `packages/cli/test/edge-cases.test.js:77-84` - `handles missing .sncp directory`

### Gap Identificati

1. **Bash:** Nessun test per `.swarm/plans/` missing (nuovo in W5)
2. **Bash:** Nessun test per sottodirectory critiche mancanti
3. **Node:** Test esistente ma minimo per `.sncp/` missing
4. **Node:** Nessun test per recovery da init parziale con directory mancanti
5. **Python:** Nessun test specifico per directory missing in `test_architect_flow.py`

---

## Phase 2: Design

### Approach

Estendere i test esistenti con casi specifici per directory mancanti, seguendo i pattern consolidati del progetto.

### Critical Files

| File | Azione | Priorita |
|------|--------|----------|
| `tests/bash/test_spawn_workers.sh` | ESTENDERE | Alta |
| `tests/bash/test_swarm_init.sh` | CREARE | Alta |
| `packages/cli/test/edge-cases.test.js` | ESTENDERE | Media |
| `tests/swarm/test_architect_flow.py` | ESTENDERE | Media |

### Implementation Steps

#### Step 1: Test Bash - spawn-workers con directory mancanti

Aggiungere in `tests/bash/test_spawn_workers.sh`:

```bash
# T1: .swarm/ non esiste
test_spawn_fails_without_swarm_dir() {
    local tmp_test="/tmp/test_no_swarm_$$"
    mkdir -p "$tmp_test"
    # NON creiamo .swarm/

    local output
    output=$(cd "$tmp_test" && "$SPAWN_WORKERS" --backend 2>&1) || true

    # Deve fallire con messaggio chiaro
    [[ "$output" == *"Non sei in un progetto"* ]] || \
    [[ "$output" == *".swarm"* ]]
    local result=$?

    rm -rf "$tmp_test"
    return $result
}

# T2: .swarm/plans/ non esiste (per --architect)
test_architect_creates_plans_dir() {
    # Verifica che --architect crei .swarm/plans/ se mancante
    # Questo test richiede mock o skip se non in progetto reale
}
```

#### Step 2: Nuovo test file - swarm-init.sh

Creare `tests/bash/test_swarm_init.sh`:

```bash
#!/bin/bash
# Test Suite per swarm-init.sh

# T3: Init in directory vuota
test_init_in_empty_dir() {
    local tmp_test="/tmp/test_swarm_init_$$"
    mkdir -p "$tmp_test"

    # Esegui init
    "$SWARM_INIT" "$tmp_test" <<< "y"

    # Verifica struttura creata
    [[ -d "$tmp_test/.swarm" ]] && \
    [[ -d "$tmp_test/.swarm/tasks" ]] && \
    [[ -d "$tmp_test/.swarm/plans" ]] && \
    [[ -f "$tmp_test/NORD.md" ]]
    local result=$?

    rm -rf "$tmp_test"
    return $result
}

# T4: Init in directory non esistente (rifiuta)
test_init_nonexistent_dir_refused() {
    local output
    output=$("$SWARM_INIT" "/nonexistent/path/xyz" <<< "n" 2>&1) || true
    [[ "$output" == *"Annullato"* ]]
}

# T5: Re-init preserva file esistenti
test_reinit_asks_confirmation() {
    local tmp_test="/tmp/test_reinit_$$"
    mkdir -p "$tmp_test/.swarm"

    # Prima init
    echo "Contenuto originale" > "$tmp_test/NORD.md"

    # Re-init con "n"
    local output
    output=$("$SWARM_INIT" "$tmp_test" <<< "n" 2>&1) || true

    # File originale preservato
    [[ -f "$tmp_test/NORD.md" ]] && \
    grep -q "Contenuto originale" "$tmp_test/NORD.md"
    local result=$?

    rm -rf "$tmp_test"
    return $result
}
```

#### Step 3: Estendere edge-cases.test.js

Aggiungere in `packages/cli/test/edge-cases.test.js`:

```javascript
describe('Directory missing edge cases', () => {

  // T6: .sncp/ parent non esiste
  test('handles missing parent directory for .sncp', async (t) => {
    const tempDir = await createTempDir(t);
    // Non creiamo nulla

    const exists = await verifyFileStructure(tempDir, [
      '.sncp',
      '.sncp/progetti',
      '.sncp/stato'
    ]);

    assert.equal(exists['.sncp'], false);
    assert.equal(exists['.sncp/progetti'], false);
  });

  // T7: Directory con permessi insufficienti
  test('handles permission denied gracefully', async (t) => {
    const tempDir = await createTempDir(t);

    // Crea directory read-only
    await createFileStructure(tempDir, {
      '.sncp/.gitkeep': ''
    });

    // Il test verifica che il codice gestisca l'errore
    // senza crash
  });

  // T8: Symlink rotto a directory
  test('handles broken symlink to directory', async (t) => {
    const tempDir = await createTempDir(t);

    // Crea symlink a directory non esistente
    const fs = await import('fs/promises');
    const path = await import('path');

    try {
      await fs.symlink(
        '/nonexistent/target',
        path.join(tempDir, '.sncp'),
        'dir'
      );
    } catch {
      // Symlink creation might fail on some systems
      return;
    }

    // Verifica che sia rilevato come non-esistente/invalido
    const exists = await readTempFile(tempDir, '.sncp/config.json');
    assert.equal(exists, null);
  });
});
```

#### Step 4: Estendere test_architect_flow.py

Aggiungere in `tests/swarm/test_architect_flow.py`:

```python
# T9: validate_plan con directory plans/ non esistente
def test_T11_validate_plan_missing_plans_dir(tmp_path):
    """Verifica comportamento quando .swarm/plans/ non esiste."""
    # Non creiamo .swarm/plans/

    result = validate_plan_output(str(tmp_path / "PLAN_test.md"))

    # Deve fallire con errore chiaro
    assert result["valid"] is False
    assert "not found" in result.get("error", "").lower() or \
           "missing" in result.get("error", "").lower()

# T10: create_plan_file crea directory se mancante
def test_T12_create_plan_creates_dir_if_missing(tmp_path):
    """Verifica che create_plan crei la directory se mancante."""
    swarm_dir = tmp_path / ".swarm"
    swarm_dir.mkdir()
    # NON creiamo plans/

    from scripts.swarm.architect_flow import create_plan_file

    plan_path = create_plan_file(
        task="Test task",
        project_root=str(tmp_path)
    )

    # Directory dovrebbe essere stata creata
    assert (tmp_path / ".swarm" / "plans").exists()
    assert Path(plan_path).exists()
```

### Risks

| Rischio | Mitigazione | Probabilita |
|---------|-------------|-------------|
| Test flaky per race condition filesystem | Usa cleanup esplicito, temp dir isolate | Bassa |
| Permessi diversi su CI vs locale | Skip test permessi su CI, o usa mock | Media |
| Symlink non supportati su Windows | Conditional skip con `os.name` check | Bassa |

---

## Phase 3: Review

### Assumptions da Validare

1. **spawn-workers.sh** deve fallire gracefully quando `.swarm/` non esiste - CONFERMATO (test esistente)
2. **swarm-init.sh** deve creare `.swarm/plans/` - CONFERMATO (riga 86)
3. **architect_flow.py** gestisce directory mancante - DA VERIFICARE

### Domande per Rafa

Nessuna. Il task e' chiaro e i pattern sono consolidati.

---

## Phase 4: Final Plan

### Execution Order

```
1. [BASH] Estendere tests/bash/test_spawn_workers.sh
   - T1: test_spawn_fails_without_swarm_dir
   - T2: test_architect_handles_missing_plans_dir

2. [BASH] Creare tests/bash/test_swarm_init.sh
   - T3: test_init_in_empty_dir
   - T4: test_init_nonexistent_dir_refused
   - T5: test_reinit_asks_confirmation

3. [NODE] Estendere packages/cli/test/edge-cases.test.js
   - T6: handles missing parent directory
   - T7: handles permission denied (mock)
   - T8: handles broken symlink

4. [PYTHON] Estendere tests/swarm/test_architect_flow.py
   - T9: validate_plan_missing_plans_dir
   - T10: create_plan_creates_dir_if_missing

5. [RUN] Eseguire test suite completa
   - ./tests/run_all_tests.sh
   - npm test --prefix packages/cli
   - pytest tests/swarm/
```

### Success Criteria

- [ ] Tutti i nuovi test passano
- [ ] Nessun test esistente rotto
- [ ] Coverage edge case "directory missing" completa per:
  - `.swarm/` non esiste
  - `.swarm/plans/` non esiste
  - `.sncp/` non esiste
  - Directory con init parziale
- [ ] Test sono deterministici (no flaky)
- [ ] Cleanup corretto delle temp directory

### Worker Assignment

| Step | Worker | Tools |
|------|--------|-------|
| 1-2 | cervella-tester | Bash, Read, Write |
| 3 | cervella-tester | Read, Write, Bash |
| 4 | cervella-tester | Read, Write, Bash |
| 5 | cervella-tester | Bash |

### Stima Complessita

**Totale test da scrivere:** 10 test case
**File da modificare:** 3 esistenti + 1 nuovo
**Complessita:** Media (pattern esistenti, logica semplice)

---

*"Piano prima, codice dopo."*

**READY FOR IMPLEMENTATION**
