# AUDIT SNCP - Guardiana Ricerca
> Data: 14 Gennaio 2026
> Auditor: cervella-guardiana-ricerca
> Versione SNCP: 3.0

---

## EXECUTIVE SUMMARY

```
+================================================================+
|                                                                |
|   VERDETTO: BASE SOLIDA                                        |
|                                                                |
|   La struttura SNCP e' COERENTE con le best practices          |
|   del settore (CLAUDE.md, Cursor Rules, Memory Banks).         |
|                                                                |
|   PUNTI FORZA: Filosofia corretta, tools utili                 |
|   PUNTI DEBOLI: oggi.md troppo lungo, compaction manuale       |
|                                                                |
|   Score Coerenza: 8/10                                         |
|                                                                |
+================================================================+
```

---

## 1. ANALISI STRUTTURA ATTUALE

### 1.1 Struttura .sncp/ Root

```
.sncp/
├── README.md              [OK] Documentazione chiara
├── stato/oggi.md          [WARN] 448 righe > 300 limite consigliato
├── coscienza/             [OK] Pensieri liberi
├── idee/                  [OK] Con templates
├── memoria/decisioni/     [OK] Decisioni con PERCHE
├── perne/                 [?] Non chiaro uso
├── archivio/2026-01/      [OK] Archivio mensile
└── progetti/              [OK] Per-project memory
```

### 1.2 Struttura Progetti

```
.sncp/progetti/
├── miracollo/             [OK] Molto usato (100+ file)
├── cervellaswarm/         [OK] Reports e idee
└── contabilita/           [OK] stato.md presente
```

**Osservazione:** Ogni progetto ha la sua "memoria" separata - CORRETTO secondo best practices.

### 1.3 Tools SNCP

| Tool | Cosa Fa | Valutazione |
|------|---------|-------------|
| sncp-init.sh | Wizard nuovo progetto | ECCELLENTE - Auto-detect stack |
| verify-sync.sh | Verifica coerenza docs/codice | BUONO - 4 check automatici |
| health-check.sh | Dashboard ASCII | BUONO - Score visivo |
| pre-session-check.sh | Check inizio sessione | BUONO - Freshness + size |
| compact-state.sh | Compattazione file | BUONO - Anti-bloat |
| post-session-update.sh | Update fine sessione | BUONO - Reminder |

---

## 2. CONFRONTO BEST PRACTICES

### 2.1 CLAUDE.md Best Practices (Anthropic)

| Best Practice | SNCP | Valutazione |
|---------------|------|-------------|
| File < 300 righe | oggi.md = 448 | WARNING |
| Struttura gerarchica | progetti/ nested | OK |
| Progressive Disclosure | handoff/ per sessioni | OK |
| Conciso e human-readable | README.md chiaro | OK |
| Iterare su efficacia | Versioning (v3.0) | OK |
| Version control | .sncp in git | OK |

**Fonte:** [Anthropic Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)

### 2.2 Cursor Rules Best Practices

| Best Practice | SNCP | Valutazione |
|---------------|------|-------------|
| Regole specifiche | CONFIG.md per progetto | OK |
| Split quando bloated | archivio/ + progetti/ | OK |
| Memory Banks | decisioni/ con PERCHE | OK |
| Tech stack documentato | CONFIG.md detect | OK |
| One task per session | handoff/ per sessioni | OK |

**Fonte:** [Cursor Rules Docs](https://cursor.com/docs/context/rules), [Memory Banks Guide](https://www.lullabot.com/articles/supercharge-your-ai-coding-cursor-rules-and-memory-banks)

### 2.3 AI Agent Memory Patterns

| Pattern | SNCP | Valutazione |
|---------|------|-------------|
| Short-term (session) | oggi.md | OK |
| Long-term (persistent) | decisioni/ + archivio/ | OK |
| Scratchpad | handoff/ | OK |
| File-based persistence | Tutto su .md | OK |
| Context pruning | compact-state.sh | OK |
| Retrieval when needed | Struttura per topic | OK |

**Fonte:** [AI Memory Management 2025](https://medium.com/@nomannayeem/building-ai-agents-that-actually-remember-a-developers-guide-to-memory-management-in-2025-062fd0be80a1)

---

## 3. GAP IDENTIFICATI

### 3.1 CRITICO: oggi.md Bloat

```
PROBLEMA: oggi.md ha 448 righe (limite: 300)
CAUSA: AUTO-CHECKPOINT spam (10 entries identiche)
IMPATTO: Context pollution, slow read

SOLUZIONE SUGGERITA:
1. Dedupe auto-checkpoint (max 1 per sessione)
2. Compaction automatica a fine giornata
3. Limite hard 300 righe con alert
```

### 3.2 MEDIO: Manca Cleanup Automatico

```
PROBLEMA: compact-state.sh esiste ma non schedulato
CAUSA: Dipende da esecuzione manuale
IMPATTO: File crescono senza controllo

SOLUZIONE SUGGERITA:
1. Cron job weekly compaction
2. Pre-commit hook per size check
3. health-check.sh auto-run a inizio sessione
```

### 3.3 BASSO: Naming Inconsistente

```
PROBLEMA: Mix di convenzioni naming
ESEMPI:
- 20260112_RICERCA_... (corretto)
- CRITICO_WORKFLOW_... (senza data)
- INDEX.md (troppo generico)

SOLUZIONE SUGGERITA:
Standardizzare: YYYYMMDD_TIPO_NOME.md
```

### 3.4 BASSO: cartella "perne/" non documentata

```
PROBLEMA: .sncp/perne/ esiste con template ma nessun uso chiaro
IMPATTO: Confusione su scopo

SOLUZIONE SUGGERITA:
Documentare in README.md o rimuovere se non usata
```

---

## 4. COSA MANCA (vs Best Practices)

### 4.1 Manca: Auto-Retrieval Intelligente

```
BEST PRACTICE (2025):
AI dovrebbe auto-recuperare info rilevanti dalla memoria

SNCP ATTUALE:
Read manuale di file specifici

GAP:
- Nessun indexing semantico
- Nessun vector search
- Read sequenziale

PRIORITA: BASSA (funziona comunque)
```

### 4.2 Manca: Validation Schema

```
BEST PRACTICE (Cursor):
Schema JSON per validare struttura output

SNCP ATTUALE:
Templates manuali (_TEMPLATE_*.md)

GAP:
- Nessuna validazione automatica
- Dipende da disciplina umana

PRIORITA: MEDIA
```

### 4.3 Manca: Cross-Project Search

```
BEST PRACTICE:
Cercare info across tutti i progetti

SNCP ATTUALE:
Grep manuale per progetto

GAP:
- Nessun search unificato
- Difficile trovare decisioni passate

PRIORITA: BASSA (Grep funziona)
```

---

## 5. COSA E' RIDONDANTE

### 5.1 AUTO-CHECKPOINT Duplicati

```
PROBLEMA: 10 entries identiche in oggi.md
OGNI entry:
  ---
  ## AUTO-CHECKPOINT: 2026-01-14 XX:XX (session_end)
  - **Progetto**: CervellaSwarm
  - **Evento**: session_end
  - **Generato da**: sncp_auto_update.py v2.0.0
  ---

SPRECO: ~50 righe inutili

SOLUZIONE: Dedupe o summarize
```

### 5.2 File Molto Simili

```
.sncp/progetti/miracollo/workflow/ contiene:
- CRITICO_WORKFLOW_LOCALE_VM_PRODUZIONE.md
- WORKFLOW_MIRACOLLO_SOLO_VM.md
- 20260111_REGOLE_WORKFLOW_IBRIDO.md
- 20260112_WORKFLOW_SOLO_VM_DEFINITIVO.md

OSSERVAZIONE: Potrebbe essere consolidato in 1-2 file
```

---

## 6. CONFRONTO CON COMPETITOR

### SNCP vs CLAUDE.md (Anthropic)

| Aspetto | CLAUDE.md | SNCP | Winner |
|---------|-----------|------|--------|
| Semplicita | 1 file | Multi-file | CLAUDE.md |
| Struttura | Flat | Gerarchico | SNCP |
| Memoria long-term | No | Si (decisioni/) | SNCP |
| Auto-context | Si (#tag) | No | CLAUDE.md |

### SNCP vs Cursor Rules

| Aspetto | Cursor | SNCP | Winner |
|---------|--------|------|--------|
| Memory Banks | Si | Si (decisioni/) | Pari |
| Auto-activation | Si (.mdc) | No | Cursor |
| Project isolation | Si | Si (progetti/) | Pari |
| Size limits | 100 righe | 300 righe | Cursor |

### SNCP vs Generic AI Memory

| Aspetto | Generic | SNCP | Winner |
|---------|---------|------|--------|
| Vector search | Si | No | Generic |
| File-based | Varia | Si | Pari |
| Human readable | Varia | Si | SNCP |
| No dependencies | Varia | Si | SNCP |

---

## 7. VALUTAZIONE TOOLS

### sncp-init.sh (9/10)

```
PRO:
- Auto-detect stack (Python, FastAPI, React, etc.)
- Auto-detect deploy (Docker, Vercel, etc.)
- Crea struttura completa
- Output colorato e chiaro

CONTRO:
- Hardcoded project mappings
- No update di progetti esistenti
```

### verify-sync.sh (8/10)

```
PRO:
- 4 check utili (freshness, commits, migrations, changes)
- Verbose mode
- Exit codes corretti

CONTRO:
- Solo 3 progetti hardcoded
- Non suggerisce azioni specifiche
```

### health-check.sh (8/10)

```
PRO:
- Dashboard ASCII visiva
- Score complessivo
- Raccomandazioni

CONTRO:
- Score arbitrario (non spiegato)
- No history tracking
```

### pre-session-check.sh (7/10)

```
PRO:
- Check essenziali
- Fast execution

CONTRO:
- Non blocca se critico
- No auto-fix
```

---

## 8. RISPOSTA ALLE DOMANDE

### Q1: La struttura e' SEMPLICE abbastanza?

```
RISPOSTA: SI, ma con margini di miglioramento.

La struttura base (stato/, coscienza/, idee/, memoria/, progetti/)
e' intuitiva e segue pattern consolidati.

PERO:
- Troppi file in progetti/miracollo/ (100+)
- oggi.md cresce troppo
- Alcune cartelle non chiare (perne/)

RACCOMANDAZIONE: Mantenere, ma aggiungere cleanup automatico
```

### Q2: I tools coprono i casi d'uso principali?

```
RISPOSTA: SI, coprono il 90% dei casi.

COPERTI:
[x] Inizializzazione progetto (sncp-init)
[x] Verifica coerenza (verify-sync)
[x] Health check (health-check)
[x] Pre-session (pre-session-check)
[x] Compaction (compact-state)
[x] Post-session (post-session-update)

NON COPERTI:
[ ] Search cross-project
[ ] Auto-cleanup scheduled
[ ] Validation schema
```

### Q3: Manca qualcosa di CRITICO?

```
RISPOSTA: NO, nulla di CRITICO manca.

NICE-TO-HAVE (non critici):
- Vector search per retrieval intelligente
- Schema validation per output
- Auto-cleanup schedulato

MA: Il sistema funziona bene senza questi.
La filosofia "file-based, human-readable" e' valida.
```

### Q4: C'e' qualcosa di RIDONDANTE?

```
RISPOSTA: SI, alcuni elementi ridondanti.

RIDONDANTE:
1. AUTO-CHECKPOINT duplicati (50+ righe spreco)
2. File workflow simili non consolidati
3. perne/ non documentata/usata

IMPATTO: Basso (non blocca, solo spreco spazio)
```

---

## 9. VERDETTO FINALE

```
+================================================================+
|                                                                |
|   VERDETTO: BASE SOLIDA                                        |
|                                                                |
|   Score Complessivo: 8/10                                      |
|                                                                |
|   BREAKDOWN:                                                   |
|   - Filosofia e Design: 9/10                                   |
|   - Implementazione Tools: 8/10                                |
|   - Coerenza Best Practices: 8/10                              |
|   - Manutenibilita: 7/10 (auto-cleanup manca)                  |
|   - Documentazione: 8/10                                       |
|                                                                |
|   RACCOMANDAZIONE:                                             |
|   Continuare con struttura attuale.                            |
|   Prioritizzare: auto-cleanup e dedupe checkpoint.             |
|                                                                |
+================================================================+
```

---

## 10. SUGGERIMENTI PRIORITIZZATI

### P0 - FARE SUBITO

1. **Dedupe AUTO-CHECKPOINT in oggi.md**
   - Rimuovere entries duplicate
   - Limitare a max 1 per sessione

2. **Compaction oggi.md a <300 righe**
   - Archiviare sessioni vecchie
   - Mantenere solo ultime 3-5

### P1 - FARE QUESTA SETTIMANA

3. **Cron job weekly cleanup**
   - compact-state.sh ogni domenica
   - health-check.sh a inizio settimana

4. **Documentare cartella perne/**
   - Se usata: aggiungere a README
   - Se non usata: rimuovere

### P2 - FARE QUANDO C'E' TEMPO

5. **Consolidare file workflow simili**
   - miracollo/workflow/ da 5 file a 2

6. **Standardizzare naming**
   - YYYYMMDD_TIPO_NOME.md everywhere

---

## FONTI

- [Anthropic Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Writing a Good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- [Cursor Rules Docs](https://cursor.com/docs/context/rules)
- [Memory Banks for AI Coding](https://www.lullabot.com/articles/supercharge-your-ai-coding-cursor-rules-and-memory-banks)
- [AI Agent Memory Management 2025](https://medium.com/@nomannayeem/building-ai-agents-that-actually-remember-a-developers-guide-to-memory-management-in-2025-062fd0be80a1)
- [JetBrains Context Management Research](https://blog.jetbrains.com/research/2025/12/efficient-context-management/)

---

*Report generato da cervella-guardiana-ricerca*
*"Info verificata > Info veloce"*
*14 Gennaio 2026*
