# SUBROADMAP: CervellaSwarm 2.0 - Aider Features

> **"Non reinventiamo la ruota - studiamo chi l'ha gia fatta bene!"**
> **Fonte:** docs/studio/RICERCA_AIDER_APPROFONDITA.md (1129 righe)

**Creata:** 18 Gennaio 2026
**Aggiornata:** 19 Gennaio 2026 - SHOW HN ANTICIPATO!
**Post-Launch:** Da avviare dopo Show HN (19 Gennaio 2026)
**Duration:** 3-4 settimane totali

---

## EXECUTIVE SUMMARY

Quattro feature chiave per CervellaSwarm 2.0:

| Feature | Impact | Effort | Priority |
|---------|--------|--------|----------|
| Tree-sitter Repo Mapping | -80% token usage | 1 settimana | P1 |
| Architect/Editor Pattern | +15% accuracy | 1 settimana | P2 |
| Git Flow + Attribution | Professional history | 2-3 giorni | P1 |
| **SNCP Evolution** | Memoria intelligente | Da studiare | P2 |

**ROI Totale:** Costi ridotti, accuracy migliore, git professionale, memoria evoluta.

---

## FEATURE 1: TREE-SITTER REPO MAPPING

### Cosa E
Parser strutturale che analizza codice e genera "mappa" ottimizzata per AI.
- Input: 50k tokens di codice
- Output: 1-2k tokens di signature rilevanti
- Risultato: Worker ricevono SOLO cio che serve

### Perche Serve
```
OGGI:
  Worker ricevono file interi → token waste → costi alti

DOMANI (con tree-sitter):
  Worker ricevono repo map → solo simboli rilevanti → -80% costi
```

### File da Creare

| File | Scopo |
|------|-------|
| `scripts/utils/repo_mapper.py` | Core mapping logic |
| `scripts/utils/treesitter_parser.py` | Wrapper tree-sitter |
| `tests/test_repo_mapper.py` | Unit tests |
| `docs/REPO_MAPPING.md` | Documentazione |

### Dipendenze
- `pip install py-tree-sitter-languages` (100+ linguaggi)
- Python 3.10+

### Definition of Done
- [ ] Parse Python, JS, TS files
- [ ] Genera mappa < 2k tokens
- [ ] Integrato in `spawn-workers`
- [ ] Test su CervellaSwarm stesso
- [ ] Docs complete

---

## FEATURE 2: ARCHITECT/EDITOR PATTERN

### Cosa E
Separazione tra ragionamento (Architect) e implementazione (Editor):
1. **Architect**: "Come risolvere X?" (focus su logica)
2. **Editor**: "Implementa questa soluzione" (focus su codice)

### Perche Serve
```
SINGLE-PROMPT (oggi):
  "Risolvi X E formatta come diff" → attenzione divisa → errori

TWO-STEP (domani):
  Step 1: "Risolvi X" → soluzione pulita
  Step 2: "Formatta" → codice pulito
  Risultato: +15% success rate
```

### File da Creare

| File | Scopo |
|------|-------|
| `~/.claude/agents/cervella-architect.md` | Agent prompt Architect |
| `scripts/swarm/spawn-architect.sh` | Launcher |
| `scripts/utils/architect_editor_flow.py` | Orchestration logic |
| `docs/ARCHITECT_EDITOR.md` | Documentazione |

### Dipendenze
- Nessuna dipendenza esterna
- Usa modelli esistenti (Opus per Architect, Sonnet per Editor)

### Definition of Done
- [ ] Agent `cervella-architect` funzionante
- [ ] Flow 2-step implementato
- [ ] Benchmark su 10 task complessi
- [ ] Integrato in task routing Regina
- [ ] Docs complete

---

## FEATURE 3: GIT FLOW + ATTRIBUTION

### Cosa E
Auto-commit professionale con:
- Conventional Commits (feat/fix/docs/...)
- Attribution chiara (Rafa + worker name)
- Commit atomici per ogni changeset

### Perche Serve
```
OGGI:
  Commit manuali → inconsistenti → storia confusa

DOMANI:
  Auto-commit → conventional → storia professionale
  "feat(auth): add login (cervella-backend)"
  Rollback pulito, blame chiaro
```

### File da Creare

| File | Scopo |
|------|-------|
| `scripts/utils/git_worker_commit.sh` | Auto-commit logic |
| `.sncp/templates/commit_message_prompt.txt` | Prompt per messaggi |
| `docs/GIT_ATTRIBUTION.md` | Documentazione |

### Dipendenze
- Git 2.20+
- Nessuna altra dipendenza

### Definition of Done
- [ ] Auto-commit funziona per tutti i worker
- [ ] Attribution "(worker-name)" nel commit
- [ ] Conventional Commits rispettati
- [ ] `/undo` command implementato
- [ ] Docs complete

---

## FEATURE 4: SNCP EVOLUTION

### Cosa E
Evoluzione del Sistema Nervoso Centrale Persistente per memoria più intelligente.

### Problema Attuale (Sessione 265)
```
OGGI:
  oggi.md = 1 file condiviso → si sovrascrive tra progetti
  PROMPT_RIPRESA = già contiene tutto → ridondanza
  Cross-progetto = non funziona bene

DOMANI (da studiare):
  Memoria intelligente cross-sessione
  Struttura più pulita
  Zero ridondanza
```

### Da Studiare (Researcher)
- Come Aider gestisce memoria (`.aider.chat.history.md`)
- Best practices state management cross-sessione
- Altri tool multi-agent e loro memoria

### Definition of Done
- [ ] Ricerca completata su alternative
- [ ] Design nuovo SNCP proposto
- [ ] Decisione su oggi.md (eliminare/evolvere)
- [ ] Implementazione se necessario
- [ ] Docs aggiornate

---

## TIMELINE POST-LAUNCH

```
SHOW HN (19 Gen) ← ANTICIPATO!
       |
       v
+------+------+------+------+
| W1   | W2   | W3   | W4   |
+------+------+------+------+
| Git  |Tree- |Archi-|Polish|
| Flow |sitter|tect/ |+Test |
|      |      |Editor|      |
+------+------+------+------+
       |             |
       v             v
    v2.0-alpha    v2.0-beta
```

### Settimana 1 (20 Gen - 26 Gen): Git Flow
- Day 1-2: `git_worker_commit.sh`
- Day 3: Template commit message
- Day 4-5: Test + integrazione

### Settimana 2 (27 Gen - 2 Feb): Tree-sitter
- Day 1-2: Setup py-tree-sitter
- Day 3-4: `repo_mapper.py`
- Day 5-7: Test + integrazione spawn-workers

### Settimana 3 (3-9 Feb): Architect/Editor
- Day 1-2: Agent `cervella-architect`
- Day 3-4: Flow orchestration
- Day 5-7: Benchmark + tuning

### Settimana 4 (10-16 Feb): Polish
- Test end-to-end
- Documentation complete
- Release v2.0-beta

---

## RISCHI E MITIGAZIONI

| Rischio | Probabilita | Impatto | Mitigazione |
|---------|-------------|---------|-------------|
| Tree-sitter parsing errors | Media | Alto | Fallback a file interi |
| Architect loop infinito | Bassa | Medio | Timeout + max iterations |
| Git hook conflicts | Media | Basso | Flag `--no-verify` option |
| Context window overflow | Bassa | Alto | Budget dinamico |

---

## METRICHE SUCCESSO

| Metrica | Baseline | Target | Come Misurare |
|---------|----------|--------|---------------|
| Token usage/task | 10k | 2k | Log API calls |
| Task success rate | 70% | 85% | Benchmark interno |
| Commit quality | N/A | 100% conventional | Git log review |
| Worker productivity | 1x | 1.5x | Task/ora |

---

## LINK E RIFERIMENTI

- **Ricerca completa:** `docs/studio/RICERCA_AIDER_APPROFONDITA.md`
- **Aider docs:** https://aider.chat/docs/
- **Tree-sitter:** https://github.com/tree-sitter/tree-sitter
- **Architect pattern:** https://aider.chat/2024/09/26/architect.html

---

*Subroadmap creata da: Cervella Guardiana Qualita*
*Data: 18 Gennaio 2026*
*Review: Prima di iniziare ogni feature, rileggere ricerca originale*

*"Impariamo dai migliori, implementiamo a modo nostro!"*
