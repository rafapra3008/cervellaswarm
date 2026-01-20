# SUBROADMAP W5 - DOGFOODING INTEGRATION

> **"Il codice migliore e quello che USIAMO!"**
>
> Creato: 19 Gennaio 2026 - Sessione 287
> Validato: Guardiana Qualita (9.5/10)

---

## OBIETTIVO

```
+================================================================+
|   MANGIARE LA NOSTRA CUCINA!                                   |
|                                                                |
|   Health attuale: 6/10                                         |
|   Health target:  8/10                                         |
|                                                                |
|   Adoption attuale: 38%                                        |
|   Adoption target:  70%                                        |
+================================================================+
```

**Problema:** Abbiamo creato 44K righe di codice (W1-W4) ma ne usiamo solo il 6%!

**Soluzione:** Integrare le feature create nel nostro workflow quotidiano.

---

## DIPENDENZE TRA DAYS

```
Day 1 ──> Day 2 (Architect routing -> docs)
             │
Day 3 ──────┼──> Day 4 (Semantic CLI -> Impact CLI)
             │
             └──> Day 5 (consolidamento)

BLOCKERS:
- Day 2 richiede Day 1 completato
- Day 4 richiede Day 3 completato (semantic-search CLI)
- Day 5 richiede Day 1-4 completati
```

---

## PIANO 5 GIORNI (Guardiana Approved)

### DAY 1: Architect Integration - Routing

**Obiettivo:** spawn-workers --architect funzionante

**Pre-Day Checkpoint:**
```bash
git tag w5-day1-start
cp -r ~/.claude/agents/ ~/.claude/agents.bak.w5day1
```

**Task:**
- [ ] `scripts/spawn-workers.sh`: Aggiungere flag `--architect`
- [ ] `scripts/swarm-init.sh`: Creare directory `.swarm/plans/`
- [ ] `~/.claude/agents/cervella-orchestrator.md`: Aggiungere regola "consulta architect per task complessi"
- [ ] Test manuale: `spawn-workers --architect "plan refactor auth"`

**Criteri di successo MISURABILI:**
- [ ] `spawn-workers --architect "test"` exit code 0
- [ ] `ls .swarm/plans/` dopo init mostra directory vuota
- [ ] `grep -c "architect" ~/.claude/agents/cervella-orchestrator.md` >= 3

**Output:** Flag funzionante + directory + regola orchestrator

---

### DAY 2: Architect Integration - Docs + Test E2E

**Obiettivo:** Documentare e testare Architect workflow

**Pre-Day Checkpoint:**
```bash
git tag w5-day2-start
```

**Dipende da:** Day 1 completato

**Task:**
- [ ] `~/.claude/CLAUDE.md`: Aggiungere sezione "Quando usare Architect"
- [ ] `~/.claude/CLAUDE.md`: Documentare `spawn-workers --architect`
- [ ] `docs/DNA_FAMIGLIA.md`: Aggiungere W3-B Architect Pattern
- [ ] Test E2E (vedi scenario sotto)

**Test E2E Scenario:**
```
INPUT: "Refactor AuthService - split in 3 file separati"

EXPECTED FLOW:
1. Regina riconosce task complesso
2. Chiama: spawn-workers --architect
3. Architect analizza codebase
4. Architect scrive .swarm/plans/PLAN_auth_refactor.md
5. Regina legge plan, chiama spawn-workers --backend
6. Backend implementa seguendo il plan

SUCCESS: .swarm/plans/PLAN_*.md esiste con sezioni:
- Analysis
- Proposed Changes
- Risk Assessment
- Implementation Steps
```

**Criteri di successo MISURABILI:**
- [ ] `grep -c "architect" ~/.claude/CLAUDE.md` >= 5
- [ ] `grep -c "W3-B" docs/DNA_FAMIGLIA.md` >= 1
- [ ] Test E2E: file .swarm/plans/PLAN_*.md creato

**Output:** Docs complete + 1 test reale passato

---

### DAY 3: Semantic Search CLI - Wrapper

**Obiettivo:** CLI wrapper per semantic_search.py

**Pre-Day Checkpoint:**
```bash
git tag w5-day3-start
```

**Task:**
- [ ] Creare `scripts/architect/semantic-search.sh`
- [ ] Implementare comandi: find-symbol, find-callers, find-references
- [ ] Test: Wrapper chiama Python correttamente
- [ ] Documentare in `docs/SEMANTIC_SEARCH.md` sezione "CLI Usage"

**Criteri di successo MISURABILI:**
```bash
# Test 1: Symbol esistente
./scripts/architect/semantic-search.sh find-symbol "WorkerConfig"
# Exit code: 0
# Output: JSON con schema {"found": true, "results": [...]}

# Test 2: Symbol non esistente
./scripts/architect/semantic-search.sh find-symbol "NonExistent123"
# Exit code: 1
# Output: JSON con schema {"found": false, "results": []}

# Test 3: Help
./scripts/architect/semantic-search.sh --help
# Exit code: 0
```

**Output:** CLI wrapper funzionante + docs

---

### DAY 4: Impact Analyzer CLI + Architect Tool

**Obiettivo:** CLI wrapper per impact_analyzer.py + Architect puo usarlo

**Pre-Day Checkpoint:**
```bash
git tag w5-day4-start
```

**Dipende da:** Day 3 completato (semantic-search CLI)

**Task:**
- [ ] Creare `scripts/architect/impact-analyze.sh`
- [ ] Implementare comandi: estimate, dependencies
- [ ] `~/.claude/agents/cervella-architect.md`: Aggiungere Bash ai tools
- [ ] Test E2E: Architect usa entrambi CLI per planning

**Criteri di successo MISURABILI:**
```bash
# Test 1: Impact estimate
./scripts/architect/impact-analyze.sh estimate "AuthService"
# Exit code: 0
# Output: JSON con {"impact_score": N, "affected_files": [...]}

# Test 2: Dependencies
./scripts/architect/impact-analyze.sh dependencies "cervella/"
# Exit code: 0

# Test 3: Architect ha Bash
grep -c "Bash" ~/.claude/agents/cervella-architect.md
# Output: >= 1
```

**Test E2E Scenario:**
```
Architect riceve: "Plan refactor UserModule"

EXPECTED:
1. Architect chiama: semantic-search.sh find-symbol UserModule
2. Architect chiama: impact-analyze.sh estimate UserModule
3. Architect usa risultati per creare plan informato
4. Plan include "Impact Score: X" e "Affected Files: Y"
```

**Output:** CLI wrapper + Architect aggiornato + test E2E

---

### DAY 5: Worker DNA + Consolidamento

**Obiettivo:** Aggiornare DNA worker + test finale

**Pre-Day Checkpoint:**
```bash
git tag w5-day5-start
```

**Dipende da:** Day 1-4 completati

**Task:**
- [ ] `~/.claude/agents/_SHARED_DNA.md`: Menzionare semantic_search, architect
- [ ] `~/.claude/agents/cervella-backend.md`: Aggiungere esempi semantic_search
- [ ] `~/.claude/agents/cervella-frontend.md`: Menzionare tree-sitter context
- [ ] `docs/DNA_FAMIGLIA.md`: Sezione W3-A Semantic Search
- [ ] Test FINALE (vedi scenario)

**Test FINALE Scenario:**
```
INPUT: "Aggiungi validazione email a UserService"

EXPECTED WORKFLOW:
1. Regina valuta complessita -> media
2. Regina chiama Architect (opzionale per task medio)
3. Architect usa semantic-search per trovare UserService
4. Architect usa impact-analyze per stimare impatto
5. Architect crea plan in .swarm/plans/
6. Regina chiama Backend con plan
7. Backend implementa
8. Guardiana verifica (chiamata manuale o auto)

SUCCESS CRITERIA:
- semantic-search chiamato almeno 1 volta
- .swarm/plans/ contiene almeno 1 file
- Implementazione segue il plan
```

**Criteri di successo MISURABILI:**
- [ ] `grep -c "semantic" ~/.claude/agents/_SHARED_DNA.md` >= 2
- [ ] `grep -c "W3-A" docs/DNA_FAMIGLIA.md` >= 1
- [ ] Test FINALE: workflow completato senza errori

**Output:** DNA aggiornato + workflow validato

---

## DEFERRED A W6 (Non critico per 8/10)

| Task | Motivo Defer | Owner | Deadline |
|------|--------------|-------|----------|
| Tree-sitter Hooks migration | Hooks funzionano, non rompere | cervella-ingegnera | W6 Day 1-2 |
| --with-context default=true | Serve analisi rischio prima | cervella-researcher | W6 Day 3 |
| README marketing updates | Polish, non funzionalita | cervella-docs | W6 Day 4 |

---

## SUCCESS METRICS + TRACKING

| Metrica | Prima W5 | Dopo W5 | Target | Come Misurare |
|---------|----------|---------|--------|---------------|
| Health Score | 6/10 | 8/10 | 8/10 | Guardiana audit |
| Feature Adoption | 38% | 70% | 70% | Script analisi |
| Architect calls/week | 0 | 3+ | 3 | `grep "architect" .bash_history` |
| Semantic Search calls | 0 | 5+ | 5 | Log in scripts/ |

**Review Settimanale:**
Ogni Venerdi, documentare in PROMPT_RIPRESA:
- Quante volte usato --architect
- Quante volte usato semantic-search
- Problemi incontrati

---

## CHECKLIST GIORNALIERA

```
OGNI GIORNO W5:
[ ] Pre-day checkpoint (git tag + backup)
[ ] Task del giorno completati
[ ] Criteri misurabili verificati
[ ] Test scenario passato
[ ] Commit + push
[ ] PROMPT_RIPRESA aggiornato
```

---

## ROLLBACK PLAN DETTAGLIATO

### Se Day N fallisce:

```bash
# 1. Ripristina da checkpoint
git reset --hard w5-dayN-start

# 2. Ripristina agents se modificati
cp -r ~/.claude/agents.bak.w5dayN/* ~/.claude/agents/

# 3. Documenta lezione
echo "## Day N - $(date)" >> docs/studio/LEZIONI_W5.md
echo "Problema: [descrizione]" >> docs/studio/LEZIONI_W5.md
echo "Causa: [analisi]" >> docs/studio/LEZIONI_W5.md
echo "Fix: [soluzione]" >> docs/studio/LEZIONI_W5.md
```

### Rollback specifici:

| Scenario | Azione |
|----------|--------|
| spawn-workers --architect rompe | Rimuovi case "architect" da spawn-workers.sh |
| semantic-search.sh errori Python | Verifica venv, dipendenze in requirements.txt |
| Architect loops | Limita depth in agent config |

---

## TIMELINE

```
W5 Day 1: Lun - Architect routing (~2h focus)
W5 Day 2: Mar - Architect docs + test E2E (~2h focus)
W5 Day 3: Mer - Semantic CLI wrapper (~3h focus)
W5 Day 4: Gio - Impact CLI + Architect tools (~3h focus)
W5 Day 5: Ven - Worker DNA + test finale (~2h focus)

TOTALE: ~12h di lavoro focussato
```

---

## NOTA IMPORTANTE

> **"SU CARTA" != "REALE"**
>
> Questa subroadmap DEVE risultare in USO REALE delle feature.
> Non basta "implementare" - dobbiamo USARE.
>
> Success = Rafa fa task complesso e Architect + Semantic vengono chiamati automaticamente.

---

*"Ultrapassar os proprios limites!"*
*W5 - Mangiamo la nostra cucina!*
*Cervella & Rafa - Sessione 287*
