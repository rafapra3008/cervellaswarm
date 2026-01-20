# HARDTEST E2E - Architect Flow (W5 Day 2)

**Tester**: cervella-tester
**Data**: 2026-01-19
**Target**: Integrazione Architect Pattern (v3.8.0)

---

## T1: Verifica Script (spawn-workers.sh)

### T1.1: Flag --architect esiste
**Score**: 10/10
**Evidenza**:
- Riga 961: `--architect "TASK"` documentato in help
- Riga 1052-1061: Parse flag --architect implementato
- Riga 1176-1186: Logica esecuzione architect presente

### T1.2: Timeout 30m configurato
**Score**: 10/10
**Evidenza**:
- Riga 917: `local ARCHITECT_TIMEOUT="30m"`
- Riga 929: timeout applicato a tmux spawn
- Riga 936-938: Gestione exit code 124 (timeout) con log `ARCHITECT_TIMEOUT`

### T1.3: allowedTools corretti
**Score**: 10/10
**Evidenza**:
- Riga 922: `ARCHITECT_TOOLS="Read,Grep,Glob,WebSearch,WebFetch"`
- Riga 931: `--allowedTools "${ARCHITECT_TOOLS}"` passato a Claude CLI
- NO Write, Edit, Bash (corretto per analisi only)

### T1.4: Output path corretto
**Score**: 10/10
**Evidenza**:
- Riga 22, 430, 874, 912: `.swarm/plans/` documentato
- Riga 874: `mkdir -p "${SWARM_DIR}/plans"` crea directory automaticamente
- Test pratico: directory creata anche se non esiste

**T1 TOTALE**: 40/40

---

## T2: Verifica Agent File (cervella-architect.md)

### T2.1: File esiste
**Score**: 10/10
**Evidenza**: `/Users/rafapra/.claude/agents/cervella-architect.md` EXISTS

### T2.2: Model opus
**Score**: 10/10
**Evidenza**: Riga 8: `model: opus`

### T2.3: Tools corretti
**Score**: 9/10
**Evidenza**:
- Riga 7: `tools: Read, Glob, Grep, WebSearch, WebFetch, AskUserQuestion`
- NOTA: Agent file ha `AskUserQuestion`, script usa solo i 5 di base
- **Issue minore**: Discrepanza tra agent file (6 tools) e script (5 tools)
- Funziona comunque perche script override con --allowedTools

### T2.4: Template 4 fasi
**Score**: 10/10
**Evidenza**:
- Righe 112, 122, 141, 148: Tutti i Phase 1-4 presenti
- Template PLAN.md righe 101-162: Struttura completa 4 fasi

**T2 TOTALE**: 39/40

---

## T3: Verifica Directory Structure

### T3.1: Directory .swarm/plans/ esiste
**Score**: 10/10
**Evidenza**: Directory presente e accessibile

### T3.2: Permessi corretti
**Score**: 10/10
**Evidenza**:
- Permessi: `drwxr-xr-x` (755)
- Owner: rafapra (corretto)
- Read/Write per owner, Read per group/others (sicuro)

### T3.3: File di test presente
**Score**: 10/10
**Evidenza**: `PLAN_TEST_001.md` esistente con struttura corretta (4 fasi)

**T3 TOTALE**: 30/30

---

## T4: Verifica Coerenza Docs

### T4.1: CLAUDE.md documenta --architect
**Score**: 8/10
**Evidenza**:
- `--architect` menzionato in docs/DNA_FAMIGLIA.md
- **Mancante**: CLAUDE.md (root) NON ha esempio spawn-workers --architect
- Presente in: NORD.md, DNA_FAMIGLIA.md, ARCHITECT_PATTERN.md

### T4.2: DNA_FAMIGLIA.md ha sezione W3-B
**Score**: 10/10
**Evidenza**:
- Righe 152-249: Sezione completa W3-B Architect Pattern
- Workflow diagrammato
- Output PLAN.md documentato

### T4.3: Famiglia conta 17 membri
**Score**: 10/10
**Evidenza**:
- Riga 125: "Totale: 17 membri della famiglia!"
- Riga 253: Aggiornato 19 Gennaio 2026 per Architect
- Breakdown: 1 Regina + 3 Guardiane + 1 Architect + 12 Worker = 17

**T4 TOTALE**: 28/30

---

## T5: Edge Cases

### T5.1: Task vuoto
**Score**: 7/10
**Evidenza**:
- Test: `--architect ""` procede SENZA errore
- Script spawna architect anche con task vuoto
- **Issue**: Non valida che task sia non-vuoto (righe 1053-1060)
- Dovrebbe rifiutare task vuoti per evitare confusione

### T5.2: Directory .swarm/plans/ non esiste
**Score**: 10/10
**Evidenza**:
- Test: `rm -rf .swarm/plans && spawn-workers --architect`
- Riga 874: `mkdir -p` crea automaticamente
- Directory ricreata con successo

### T5.3: Timeout gestito gracefully
**Score**: 10/10
**Evidenza**:
- Righe 916-918: Timeout 30m + kill-after 30s configurati
- Righe 934-939: Exit code 124 catturato e loggato come `ARCHITECT_TIMEOUT`
- Log file contiene stato finale (DONE o TIMEOUT)

**T5 TOTALE**: 27/30

---

## SCORE FINALE

| Test | Score | Peso | Pesato |
|------|-------|------|--------|
| T1: Script | 40/40 | 30% | 12.0 |
| T2: Agent File | 39/40 | 25% | 9.75 |
| T3: Directory | 30/30 | 15% | 4.5 |
| T4: Docs | 28/30 | 15% | 4.2 |
| T5: Edge Cases | 27/30 | 15% | 4.05 |

**TOTALE**: **34.5/40** = **86.25%**

---

## BUG TROVATI

### BUG-1: Discrepanza tools tra agent file e script
**Severity**: Low
**File**: `~/.claude/agents/cervella-architect.md` (riga 7)
**Issue**: Agent file lista 6 tools (include AskUserQuestion), spawn-workers.sh usa 5 tools
**Fix consigliato**: Allinea agent file a script (rimuovi AskUserQuestion) OPPURE aggiungi in script

### BUG-2: Task vuoto non validato
**Severity**: Medium
**File**: `scripts/swarm/spawn-workers.sh` (righe 1053-1060)
**Issue**: `--architect ""` procede senza errore. Architect riceve task vuoto.
**Fix consigliato**:
```bash
if [[ -z "$ARCHITECT_TASK" || "$ARCHITECT_TASK" =~ ^[[:space:]]*$ ]]; then
    print_error "--architect richiede un task NON vuoto!"
    exit 1
fi
```

### BUG-3: CLAUDE.md manca esempio --architect
**Severity**: Low
**File**: `~/.claude/CLAUDE.md`
**Issue**: Sezione "Spawn-Workers" non ha esempio --architect
**Fix consigliato**: Aggiungi riga esempio:
```
spawn-workers --architect "Task description"  # Crea PLAN.md
```

---

## RACCOMANDAZIONI

1. **Fix BUG-2 PRIMA del release** (Medium severity)
2. Allinea tools tra agent file e script (BUG-1)
3. Aggiungi esempio --architect in CLAUDE.md (BUG-3)
4. Considera: max length task description (es: 200 char)
5. Considera: output path personalizzabile (`--plan-dir`)

---

## VERDETTO

**STATUS**: PASS (con bug minori)

L'integrazione Architect Pattern (v3.8.0) e FUNZIONALE e ben progettata.

**Punti di forza**:
- Timeout graceful implementato correttamente
- Directory auto-create funziona
- AllowedTools limitati correttamente (no Write/Edit/Bash)
- Documentazione W3-B completa

**Da fixare**:
- Validazione task vuoto (BUG-2)
- Discrepanza tools (BUG-1)

**Next**: Fix BUG-2, poi W5 Day 2 READY per dogfooding.

---

**Cervella Tester** - HARDTEST completato 19 Gennaio 2026
