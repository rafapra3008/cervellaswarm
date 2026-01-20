# SUBROADMAP - Context Optimization

> **Creata:** 20 Gennaio 2026 - Sessione 307
> **Aggiornata:** 20 Gennaio 2026 - CAUSA RADICE TROVATA!
> **Problema:** COSTITUZIONE caricata DUE VOLTE (@ + hook)
> **Fix applicato:** Rimossa @ da CLAUDE.md (hook resta unica fonte)
> **Risparmio atteso:** ~2,500 tokens (verifica prossima sessione)

---

## IL PROBLEMA

```
+================================================================+
|   ATTUALE: ~13,585 tokens injection all'avvio                  |
|   TARGET:  ~8,000 tokens (-42%)                                |
|                                                                |
|   TOP 3 COLPEVOLI:                                             |
|   1. CLAUDE.md (3 file) = 7,175 tokens (53%)                  |
|   2. DNA Agent = 4,250 tokens (31%)                           |
|   3. load_context output = 1,500 tokens (11%)                 |
+================================================================+
```

---

## PHASE 1: QUICK WINS (Oggi - Sessione 307)

### Task 1.1: COSTITUZIONE Minimal
**Risparmio:** ~1,050 tokens (87% su COSTITUZIONE)

| Azione | Dettaglio |
|--------|-----------|
| Backup | `cp ~/.claude/COSTITUZIONE.md ~/.claude/COSTITUZIONE_BACKUP.md` |
| Crea trigger | `~/.claude/docs/COSTITUZIONE_TRIGGER.md` (20 righe) |
| Modifica hook | Usa version minimal in `session_start_swarm.py` |

**COSTITUZIONE_TRIGGER.md (20 righe):**
```markdown
# COSTITUZIONE - Quick Reference

## Chi Siamo
- Rafa: CEO & Visionary (PERCHE)
- Cervella: Strategic Partner (COME)
- Famiglia: 17 agenti (3 Guardiane + 1 Architect + 12 Worker)

## Filosofia Core
- "Lavoriamo in pace! Senza casino! Dipende da NOI!"
- Fatto BENE > Fatto VELOCE
- Partner, non assistente
- Ricerca PRIMA di implementare
- Tempo NON e' fattore decisionale

## Workflow
- Formula Magica: Ricerca -> Roadmap -> Metodo -> Decisione -> Partnership
- Consulta esperti: UI->Marketing, DB->Data, Deploy->DevOps

**Dettagli completi**: Read `~/.claude/COSTITUZIONE.md`
```

### Task 1.2: Reference Table invece di Full Docs
**Risparmio:** ~500 tokens

```markdown
## Reference Docs (Load on-demand)

| Quando | Leggi |
|--------|-------|
| Dubbio identita | `~/.claude/COSTITUZIONE.md` |
| Workflow deploy | `~/.claude/CHECKLIST_DEPLOY.md` |
| Code review | `~/.claude/CHECKLIST_AZIONE.md` |
| Regole sviluppo | `~/.claude/docs/REGOLE_SVILUPPO.md` |
```

### Task 1.3: NORD Condizionale
**Risparmio:** ~384 tokens (80% casi)

NORD caricato SOLO se PROMPT_RIPRESA > 7 giorni.

---

## PHASE 2: CLAUDE.md Consolidation (Domani)

### Task 2.1: Refactor CLAUDE.md globale
**Target:** 336 -> 200 righe (-40%)

| Sezione | Azione |
|---------|--------|
| Miracollo disambiguazione | Sposta in doc dedicato |
| Tabelle ripetitive | Consolida in una |
| Esempi lunghi | Reference link |

### Task 2.2: Rimuovi duplicazioni
**Target:** Elimina overlap tra CLAUDE.md e COSTITUZIONE

---

## PHASE 3: DNA Agent Split (Settimana prossima)

### Task 3.1: Split DNA in Core + Extended
**Risparmio:** ~1,700 tokens (-40% DNA)

| File | Contenuto | Righe |
|------|-----------|-------|
| `cervella-*-core.md` | Identita, regole base | MAX 100 |
| `cervella-*-extended.md` | Pattern, esempi | Reference |

---

## PHASE 4: load_context Optimization (Quando tempo)

### Task 4.1: Format compatto
**Risparmio:** ~450 tokens (-30%)

**Prima:**
```
### MEDIUM - Pattern Name
**Trigger:** Long description...
**Problem:** Long description...
**Solution:** Long description...
*Confidence: 95% | Applicata 12x | Score: 85*
```

**Dopo:**
```
[MEDIUM] Pattern Name (12x, 95%)
-> Problem: Brief
-> Solution: Brief
```

---

## METRICHE TARGET

| Metric | Attuale | Target | Risparmio |
|--------|---------|--------|-----------|
| Total injection | 13,585 | 8,000 | -42% |
| CLAUDE.md | 7,175 | 3,500 | -51% |
| DNA Agent | 4,250 | 2,550 | -40% |
| load_context | 1,500 | 1,050 | -30% |
| PROMPT_RIPRESA | 660 | 600 | -9% |

---

## SUCCESS CRITERIA

- [ ] SessionStart < 8,000 tokens (vs 13,585)
- [ ] No degradazione qualita risposte
- [ ] Hook execution < 500ms
- [ ] Reference table funziona (lazy loading)

---

## TIMELINE

| Fase | Quando | Risparmio |
|------|--------|-----------|
| Phase 1 | Oggi (S307) | -1,934 tokens |
| Phase 2 | Domani (S308) | -1,800 tokens |
| Phase 3 | Settimana prossima | -1,700 tokens |
| Phase 4 | Quando tempo | -450 tokens |
| **TOTALE** | - | **-5,884 tokens** |

---

*"Il context e' come la memoria: prezioso. Non sprecarlo."*
*Cervella & Rafa - Sessione 307*
