# SUBROADMAP - Context Optimization DURANTE Lavoro

> **Creata:** 21 Gennaio 2026 - Sessione 308
> **Aggiornata:** 21 Gennaio 2026 - Integrato feedback Guardiana Qualità
> **Problema:** Context cresce troppo velocemente DURANTE il lavoro
> **Obiettivo:** Sessioni più lunghe senza compromettere qualità
> **Score Target:** 9.5/10

---

## IL PROBLEMA REALE

```
+================================================================+
|   SINTOMO: Context si riempie velocemente durante lavoro        |
|                                                                |
|   PRIMA: Sessioni grandi e lunghe                              |
|   ORA: Checkpoint frequenti, nuove sessioni continue           |
|                                                                |
|   NOTA: All'avvio è normale (~20% context)                     |
|         Il problema è DURANTE il lavoro                        |
+================================================================+
```

---

## CAUSE POTENZIALI DA INVESTIGARE

### 1. Subagent Context Accumulation
- Ogni Task tool spawna un subagent
- Ogni subagent ha il suo prompt (50-300 righe)
- I risultati tornano nel context parent
- **Domanda:** I risultati sono troppo verbosi?

### 2. Tool Results Size
- Read tool: ritorna intero file (fino a 2000 righe)
- Grep/Glob: ritorna molti risultati
- WebFetch/WebSearch: ritorna contenuto web
- **Domanda:** Stiamo leggendo troppi file?

### 3. Hook durante lavoro
- PostToolUse(Task): log_event.py + debug_hook.py
- PostToolUse(Bash): post_commit_engineer.py
- UserPromptSubmit: context_check.py
- **Domanda:** Questi hook aggiungono context?

### 4. Agent Prompt Growth
- cervella-architect: 293 righe (grande!)
- Guardiane: 70 righe ciascuna
- Worker: 60-110 righe
- **Domanda:** Possiamo ridurre senza perdere qualità?

### 5. Context Base Fisso (AGGIUNTO da Guardiana)
- ~/.claude/CLAUDE.md: 336 righe (~1,400 token)
- COSTITUZIONE.md: 510 righe (troncata a 150 dall'hook)
- CervellaSwarm/CLAUDE.md: 74 righe
- **Domanda:** Questi file sono troppo grandi?

### 6. MCP Servers Output (AGGIUNTO da Guardiana)
- Browser MCP (Playwright)
- CervellaSwarm MCP
- **Domanda:** Aggiungono context significativo?

---

## FASE 1: DIAGNOSI (Oggi - S308)

### Task 1.1: Misurare crescita context
| Step | Azione | Metrica |
|------|--------|---------|
| 1 | Iniziare sessione pulita | Notare % iniziale |
| 2 | Spawn 1 worker (backend) | Notare % dopo |
| 3 | Spawn 1 guardiana (qualità) | Notare % dopo |
| 4 | Spawn 1 architect | Notare % dopo |
| 5 | Read file grande (500+ righe) | Notare % dopo |

**Output atteso:** Tabella con delta % per ogni operazione

### Task 1.2: Analizzare tool results
- [ ] Quanto context aggiunge un Read di file grande?
- [ ] Quanto context aggiungono i subagent results?
- [ ] C'è un pattern di "accumulo"?

### Task 1.3: Verificare hook output
| Hook | File | Output atteso |
|------|------|---------------|
| PostToolUse(Task) | debug_hook.py | JSON minimo |
| PostToolUse(Task) | log_event.py | JSON minimo |
| UserPromptSubmit | context_check.py | Verifica |

### Task 1.4: Misurare context base (NUOVO)
| File | Righe | Token stimati |
|------|-------|---------------|
| ~/.claude/CLAUDE.md | 336 | ~1,400 |
| CervellaSwarm/CLAUDE.md | 74 | ~300 |
| COSTITUZIONE (hook, 150 max) | 150 | ~600 |
| NORD (hook, 60 max) | 60 | ~240 |
| PROMPT_RIPRESA (hook) | ~95 | ~380 |
| **TOTALE BASE** | **~715** | **~2,920** |

---

## FASE 2: OTTIMIZZAZIONE MIRATA (S309)

### Opzione A: Ridurre verbosità subagent results
**Se il problema è: subagent ritornano troppo testo**
- Modificare prompt agent per output più conciso
- Aggiungere "Rispondi in modo CONCISO" ai prompt
- **Rischio:** BASSO - non cambia funzionalità

### Opzione B: Ridurre agent prompt size
**Se il problema è: prompt troppo grandi**

| Agent | Attuale | Target | Note |
|-------|---------|--------|------|
| cervella-architect | 293 | 180 | **CAUTELA** - verificare PLAN.md completo |
| cervella-backend | 110 | 80 | OK ridurre |
| cervella-orchestrator | 106 | 80 | OK ridurre |

**REGOLA ARCHITECT:** Prima di ridurre, verificare che template PLAN.md mantenga tutte le sezioni:
- [ ] Phase 1: Understanding
- [ ] Phase 2: Design
- [ ] Phase 3: Review
- [ ] Phase 4: Final Plan

### Opzione C: Rimuovere hook non essenziali
**Approvato da Guardiana come SICURO:**

| Hook | File | Azione | Rischio |
|------|------|--------|---------|
| PostToolUse(Task) | debug_hook.py | RIMUOVERE | NESSUNO |
| PostToolUse(Task) | log_event.py | RIMUOVERE | NESSUNO |

**NOTA:** Questi hook scrivono solo su file/DB, output minimo. Rimozione sicura.

### Opzione D: Read tool più intelligente
**Se il problema è: Read ritorna troppo**
- Usare limit/offset più spesso
- Preferire Grep a Read quando possibile
- **Rischio:** BASSO

### Opzione E: Ridurre CLAUDE.md (NUOVO)
**Se il problema è: context base troppo grande**
- ~/.claude/CLAUDE.md: 336 → 200 righe
- Spostare dettagli in file di riferimento
- **Rischio:** MEDIO - verificare che istruzioni critiche restino

---

## FASE 3: VALIDAZIONE (S310)

### Metriche di successo CONCRETE

| Metrica | Baseline (oggi) | Target | Come misurare |
|---------|-----------------|--------|---------------|
| Context dopo 5 spawn | Da misurare | -30% | Status bar Claude Code |
| Durata sessione tipica | ~45 min | 90+ min | Tempo prima di checkpoint |
| Qualità output | Baseline | = o migliore | Review manuale |

### Test di non-regressione COMPLETI

**Worker (Sonnet):**
- [ ] Spawn cervella-backend con task reale → output corretto?
- [ ] Spawn cervella-frontend con task reale → output corretto?
- [ ] Spawn cervella-tester con task reale → output corretto?

**Guardiane (Opus):**
- [ ] Spawn cervella-guardiana-qualita → audit con checklist completa?
- [ ] Spawn cervella-guardiana-ops → verifica infra completa?

**Architect (Opus):**
- [ ] Spawn cervella-architect con task complesso
- [ ] Verificare PLAN.md ha TUTTE le sezioni:
  - [ ] Phase 1: Understanding
  - [ ] Phase 2: Design
  - [ ] Phase 3: Review
  - [ ] Phase 4: Final Plan
- [ ] Verificare plan è actionable (worker può seguirlo)

**Hook:**
- [ ] SessionEnd → nessun errore JSON
- [ ] PreCompact → salvataggio funziona
- [ ] SessionStart → context caricato correttamente

---

## PROBLEMI CORRELATI DA FIXARE

### Hook SessionEnd
- [x] **FIXATO S308**: file_limits_guard.py schema JSON corretto

### Hook SubagentStart
- [ ] subagent_start_costituzione.py NON ESISTE ma è configurato
- **Azione:** Rimuovere dalla config (file non necessario dopo analisi)

### Problemi di commit
- [ ] Da investigare - Rafa ha menzionato problemi
- **Azione:** Chiedere dettagli a Rafa

---

## REGOLE DI OTTIMIZZAZIONE

```
+================================================================+
|   REGOLA 1: MAI peggiorare qualità per risparmiare context     |
|                                                                |
|   REGOLA 2: Misurare PRIMA e DOPO ogni cambio                  |
|                                                                |
|   REGOLA 3: Un fix alla volta, testare, poi next               |
|                                                                |
|   REGOLA 4: Se in dubbio, NON cambiare                         |
|                                                                |
|   REGOLA 5: Architect prompt - CAUTELA MASSIMA (Guardiana)     |
+================================================================+
```

---

## TIMELINE

| Fase | Sessione | Focus | Deliverable |
|------|----------|-------|-------------|
| Diagnosi | S308 (oggi) | Capire DOVE cresce | Tabella delta % |
| Fix mirati | S309 | Applicare fix sicuri | Hook rimossi, prompt ridotti |
| Validazione | S310 | Verificare | Test non-regressione PASS |

---

## ACCEPTANCE CRITERIA

Per considerare questa subroadmap COMPLETATA:

- [ ] Diagnosi completata con numeri concreti
- [ ] Almeno 1 fix applicato (quello più impattante)
- [ ] Test non-regressione tutti PASS
- [ ] Context dopo 5 spawn ridotto di almeno 20%
- [ ] Nessuna degradazione qualità output

---

## DECISIONI DA PRENDERE

1. **Priorità fix:** Quale causa affrontare prima?
2. **Trade-off:** Accettiamo output più concisi?
3. **Hook:** Rimuovere debug_hook.py e log_event.py? (Guardiana: SICURO)
4. **Architect:** Ridurre prompt? (Guardiana: CON CAUTELA)

---

*"Prima capire, poi agire. Mai fretta."*
*"Fatto BENE > Fatto VELOCE"*
*Cervella & Rafa - Sessione 308*
