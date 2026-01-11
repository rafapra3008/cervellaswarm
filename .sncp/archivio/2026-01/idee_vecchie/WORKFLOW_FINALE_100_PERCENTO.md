# WORKFLOW FINALE - 100%

> **Data:** 9 Gennaio 2026
> **Sessione:** 134
> **Stato:** DECISIONI FINALI

---

## LA NOSTRA ARCHITETTURA FINALE

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   ARCHITETTURA CERVELLASWARM - VERSIONE FINALE                  ║
║                                                                  ║
║   👑 REGINA (Opus)                                              ║
║   ├── Context SNELLO (8-10K token startup)                      ║
║   ├── SNCP come memoria esterna                                 ║
║   ├── Coordina tutto                                            ║
║   │                                                              ║
║   ├── Task < 5 min → TASK TOOL INTERNO                         ║
║   │   └── Subagent nel suo context                              ║
║   │   └── Risultato immediato                                   ║
║   │   └── ⚠️ Se compatta, perde lavoro                         ║
║   │                                                              ║
║   └── Task > 5 min → GIT CLONE SEPARATO                        ║
║       └── Context isolato                                       ║
║       └── Sopravvive a compact                                  ║
║       └── Merge manuale risultati                               ║
║                                                                  ║
║   🛡️ GUARDIANE (Opus) - Verificano quando serve                ║
║   🐝 WORKER (Sonnet) - Eseguono task                            ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## DECISIONE 1: GIT CLONES

### Quando Usarli

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   REGOLA DEI 5 MINUTI                                           ║
║                                                                  ║
║   Task < 5 min:                                                  ║
║   → Task tool interno                                           ║
║   → Veloce, risultato immediato                                 ║
║   → OK consumare un po' di context                              ║
║   → Esempi: ricerca, analisi, review veloce                     ║
║                                                                  ║
║   Task > 5 min:                                                  ║
║   → Git clone separato                                          ║
║   → Context isolato, non consuma Regina                         ║
║   → Sopravvive a compact                                        ║
║   → Esempi: implementazione, refactoring, test suite            ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

### Come Funzionano i Git Clones

```bash
# 1. CREARE UN CLONE (quando serve)
git clone . ../CervellaSwarm-worker-1
cd ../CervellaSwarm-worker-1

# 2. LAVORARE NEL CLONE
# Il worker lavora qui, ha il suo context separato
# La Regina continua a lavorare nel repo principale

# 3. PORTARE RISULTATI (quando finito)
cd ../CervellaSwarm  # torna al principale
git pull ../CervellaSwarm-worker-1 main  # prendi i cambiamenti

# 4. ELIMINARE IL CLONE (pulizia)
rm -rf ../CervellaSwarm-worker-1
```

### Clones: NON Permanenti

```
❌ NON tenere clones permanenti (CervellaSwarm-regina-A, B)
✅ Creare clone quando serve, eliminare quando finito
✅ Script automatico per creare/eliminare
```

---

## DECISIONE 2: CONTEXT OPTIMIZATION

### I Numeri Target

| Metrica | PRIMA | DOPO | Come |
|---------|-------|------|------|
| Token startup | 22-25K | 8-10K | CLAUDE.md snello |
| CLAUDE.md globale | 906 linee | 180 linee | Separare COSA/COME |
| CLAUDE.md progetto | 199 linee | 40 linee | Solo essenziale |
| PROMPT_RIPRESA | 430 linee | 80 linee | Formato strutturato |

### Struttura File Snelli

**CLAUDE.md Globale (180 linee):**
```markdown
# Chi Sono (30 linee)
- Identità, femminile, calma, partner

# Regole d'Oro (30 linee)
- MAI fretta
- Delega con spawn-workers
- SNCP come memoria

# Trigger (30 linee)
- checkpoint → cosa fare
- pausa → cosa fare
- chiudiamo → cosa fare

# Puntatori (30 linee)
- COSTITUZIONE.md → leggo se "mi sento persa"
- WORKFLOW_DETTAGLIATO.md → leggo per processi
- CHECKLIST_DEPLOY.md → leggo prima di deploy

# Progetti (30 linee)
- Path, SNCP, note specifiche

# Swarm (30 linee)
- Regola 5 minuti
- Come usare Task tool vs spawn
```

**PROMPT_RIPRESA (80 linee):**
```markdown
# Stato (10 linee)
- Versione, completato, in corso

# Decisioni Chiave (20 linee)
- DECISIONE: X | PERCHÉ: Y (formato tabella)

# Prossimi Step (10 linee)
- Azioni immediate

# Puntatori (10 linee)
- .sncp/idee/XXX.md per dettagli
- .sncp/memoria/decisioni/XXX.md per storico

# Note Sessione Precedente (30 linee)
- Riassunto compatto, non narrativa
```

---

## DECISIONE 3: DNA FAMIGLIA (Tutti i 16)

### I 16 Membri

| N | Nome | Modello | Ruolo |
|---|------|---------|-------|
| 1 | cervella-orchestrator | Opus | Regina, coordina |
| 2 | cervella-guardiana-qualita | Opus | Verifica output |
| 3 | cervella-guardiana-ops | Opus | Supervisiona devops |
| 4 | cervella-guardiana-ricerca | Opus | Verifica ricerche |
| 5 | cervella-frontend | Sonnet | React, CSS, UI |
| 6 | cervella-backend | Sonnet | Python, FastAPI |
| 7 | cervella-tester | Sonnet | QA, testing |
| 8 | cervella-reviewer | Sonnet | Code review |
| 9 | cervella-researcher | Sonnet | Ricerca tecnica |
| 10 | cervella-scienziata | Sonnet | Ricerca strategica |
| 11 | cervella-ingegnera | Sonnet | Analisi codebase |
| 12 | cervella-marketing | Sonnet | UX, posizionamento |
| 13 | cervella-devops | Sonnet | Deploy, CI/CD |
| 14 | cervella-docs | Sonnet | Documentazione |
| 15 | cervella-data | Sonnet | SQL, analytics |
| 16 | cervella-security | Sonnet | Audit sicurezza |

### Cosa Aggiungere a OGNI DNA

```markdown
## REGOLE CONTEXT-SMART (aggiungere a tutti)

1. NON sprecare token
   - Output conciso
   - Risultati strutturati
   - No narrativa lunga

2. USA SNCP
   - Scrivi su .sncp/ mentre lavori
   - Non accumulare in context

3. REGOLA 5 MINUTI
   - Se il task richiede > 5 min, avvisa
   - Potrebbe servire clone separato

4. OUTPUT STRUTTURATO
   - Sempre formato: FATTO, DA FARE, NOTE
   - Max 500 token per risposta normale
```

### Dove Sono i DNA

```
~/.claude/agents/
├── cervella-orchestrator.md
├── cervella-guardiana-qualita.md
├── cervella-guardiana-ops.md
├── cervella-guardiana-ricerca.md
├── cervella-frontend.md
├── cervella-backend.md
├── cervella-tester.md
├── cervella-reviewer.md
├── cervella-researcher.md
├── cervella-scienziata.md
├── cervella-ingegnera.md
├── cervella-marketing.md
├── cervella-devops.md
├── cervella-docs.md
├── cervella-data.md
└── cervella-security.md
```

---

## DECISIONE 4: HOOKS E TRIGGERS

### Hooks Necessari

| Hook | Quando | Cosa Fa |
|------|--------|---------|
| startup | Inizio sessione | Carica SOLO essenziale |
| pre-compact (70-80%) | Prima di compact | Salva stato in PROMPT_RIPRESA |
| post-tool | Dopo ogni tool | (opzionale) Log in SNCP |

### Triggers Esistenti (da snellire)

| Trigger | Azione |
|---------|--------|
| "checkpoint" | PROMPT_RIPRESA snello + git commit |
| "pausa" | Salva + riepilogo veloce |
| "chiudiamo" | Checkpoint + push + chiusura |

---

## DECISIONE 5: ORDINE IMPLEMENTAZIONE

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   FASE 1: FONDAMENTA (2-3 sessioni)                             ║
║   ├── Template CLAUDE.md progetto (40 linee)                    ║
║   ├── Template PROMPT_RIPRESA (80 linee)                        ║
║   ├── Benchmark context before/after                            ║
║   └── Test su CervellaSwarm                                     ║
║                                                                  ║
║   FASE 2: FAMIGLIA (2-3 sessioni)                               ║
║   ├── Aggiornare TUTTI i 16 DNA                                 ║
║   ├── Template CLAUDE.md globale (180 linee)                    ║
║   └── Script git clones                                         ║
║                                                                  ║
║   FASE 3: ROLLOUT (2-3 sessioni)                                ║
║   ├── Applicare a Miracollo                                     ║
║   ├── Applicare a Contabilità                                   ║
║   └── Documentazione finale                                     ║
║                                                                  ║
║   TOTALE: 6-9 sessioni                                          ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## WORKFLOW GIORNALIERO FINALE

### Inizio Sessione
```
1. Claude carica CLAUDE.md snello (~8-10K token)
2. Leggo PROMPT_RIPRESA (80 linee)
3. Se serve, leggo .sncp/ per dettagli
4. Pronta a lavorare con 85% context libero!
```

### Durante Sessione
```
1. Task < 5 min → Task tool interno
2. Task > 5 min → Creo git clone, worker lavora lì
3. Scrivo su .sncp/ mentre lavoro (non accumulo context)
4. Commit frequenti (git = memoria esterna)
```

### Checkpoint (70-80% context)
```
1. Aggiorno PROMPT_RIPRESA (formato snello!)
2. git commit
3. Posso fare /clear se serve continuare
```

### Chiusura Sessione
```
1. PROMPT_RIPRESA finale (80 linee MAX)
2. git push
3. Elimino clones temporanei se esistono
```

---

## COSA ABBIAMO DECISO (Riepilogo)

| Domanda | Decisione |
|---------|-----------|
| Git clones servono? | SÌ, per task > 5 min |
| Clones permanenti? | NO, creare/eliminare quando serve |
| Quanti worker paralleli? | 2-3 max |
| DNA famiglia? | TUTTI i 16 insieme |
| Ordine? | CervellaSwarm → Famiglia → Miracollo |
| Template prima? | SÌ, sono le fondamenta |

---

## COSA MANCA IMPLEMENTARE

| Cosa | File/Script | Priorità |
|------|-------------|----------|
| Template CLAUDE.md progetto | da creare | ALTA |
| Template CLAUDE.md globale | da creare | ALTA |
| Template PROMPT_RIPRESA | da creare | ALTA |
| Script crea-clone | da creare | MEDIA |
| Script elimina-clone | da creare | MEDIA |
| Aggiornamento 16 DNA | da fare | ALTA |
| Hook pre-compact | da verificare | MEDIA |
| Benchmark script | da creare | MEDIA |

---

*Questo è il 100%. Tutto deciso. Pronto per implementare.*
