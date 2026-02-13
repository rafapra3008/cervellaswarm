# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-13 - Sessione 361
> **STATUS:** REGOLA ANTI-DOWNGRADE MODELLI - 4 step, score medio 9.6/10

---

## SESSIONE 361 - REGOLA ANTI-DOWNGRADE MODELLI (4 step)

### Problema
Guardiana Ops spawnata come Haiku 4.5 invece di Opus. Root cause: il Task tool di sistema dice "Prefer haiku for quick tasks" e il campo `model` nel frontmatter agente e solo dichiarativo, non enforced.

### Cosa abbiamo fatto
Aggiunta regola esplicita "MAI downgrade modelli" in 3 file strategici + pulizia residui stale.

### 4 step completati

**Step 1 - Regola in _SHARED_DNA.md (9.5/10):**
- Nuova sezione "REGOLA MODELLI - INVIOLABILE" con box ASCII
- Posizione: dopo "DNA DI FAMIGLIA", prima di "REGOLE CONTEXT-SMART"
- Tutti gli agenti la vedono nel loro system prompt
- Sincronizzata main + insiders (identiche)

**Step 2 - Regola in CLAUDE.md globale (9.8/10):**
- Una riga sotto SWARM MODE: "MAI passare model: haiku quando spawno agenti"
- Timestamp aggiornato a S361
- Insiders punta al main (no sync separato)

**Step 3 - Policy in DNA_FAMIGLIA.md (9.5/10):**
- Blockquote dopo tabella famiglia: "I modelli sono INVIOLABILI"
- Versione bumped 1.6.0 -> 1.7.0

**Step 4 - Memory + pulizia stale:**
- MEMORY.md aggiornato con nuova sezione "Agent Model Anti-Downgrade Rule"
- Rimossi 2 riferimenti stale a stato.md in DNA_FAMIGLIA.md (residuo pre-SNCP 4.0)

### 3 livelli di protezione ora attivi
1. `_SHARED_DNA.md` - TUTTI gli agenti vedono la regola completa
2. `~/.claude/CLAUDE.md` - La Regina vede il promemoria operativo
3. `docs/DNA_FAMIGLIA.md` - Documento referenza con policy dichiarata

### Numeri finali
```
Guardiana audit:  3x (9.5, 9.8, 9.5 = media 9.6/10)
File modificati:  5 (DNA x2, CLAUDE.md, DNA_FAMIGLIA, MEMORY)
P1/P2:           0
P3 risolti:      2 (riferimenti stale stato.md)
```

---

## PROSSIMI STEP
- Nessun P1/P2 pendente per CervellaSwarm
- Opzionale P3: aggiungere "(solo Regina)" dopo "Task tool" in _SHARED_DNA.md
- Opzionale P3: aggiungere `logger.debug()` in verify-hooks.py
- Oppure: passare a un altro progetto (Miracollo, Chavefy, Contabilita)

---

## ARCHIVIO

| Sessione | Cosa |
|----------|------|
| S337-S348 | Coverage push 41% -> 95% (968 test) |
| S349 | Audit reale + Pulizia + MAPPA MIGLIORAMENTI |
| S350 | FASE A: Async Hooks + Bash Validator |
| S351 | Persistent Memory + Hook Integrity |
| S352 | COMPLETAMENTO MAPPA: B+C+D = 7 step, score 9.1/10 |
| S353 | CervellaBrasil nasceu! 7 pesquisas, 10k+ linhas |
| S354 | Chavefy nasceu! SaaS Property Management Brasil |
| S355 | SubagentStart Context Injection + Audit totale Famiglia |
| S356 | Studio SNCP 4.0 (3 esperte) + Clear Context (parcheggiato) |
| S357 | SNCP 4.0 IMPLEMENTATO! 6 file archiviati, 12+ puntatori fixati |
| S358 | AUDIT TOTALE! 13 agenti sync, 25 test fix, 4 hook fix, 8 docs fix |
| S359 | PULIZIA CHIRURGICA! 4 hook disabled, 2 test split, sync-agents.sh |
| S360 | POLISH + CODE REVIEW! 5 step, sync hook, logging, dry-run |
| S361 | REGOLA ANTI-DOWNGRADE! Policy modelli in 3 file, 3 audit Guardiana |

---

*"Fatto BENE > Fatto VELOCE"*
*Sessione 361 - Cervella & Rafa*
