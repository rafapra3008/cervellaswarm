# Bug Fix: Reviewer DNA ha riferimenti Bash ma non ha tool Bash

**Data:** 10 Gennaio 2026
**Sessione:** 146
**Scoperto su:** Miracollo

---

## Problema

Il DNA di `cervella-reviewer` contiene istruzioni per:
- Eseguire script bash (`scripts/swarm/update-status.sh`)
- Scrivere file output (`.swarm/tasks/TASK_001_OUTPUT.md`)

Ma il reviewer ha solo questi tool:
```
tools: Read, Glob, Grep, WebSearch
```

**NON ha:** Bash, Write, Edit

---

## Errori Risultanti

1. `Error: No such tool available: Bash`
2. `Error: EISDIR: illegal operation on a directory, read` (quando tenta di leggere una directory)

---

## Causa Root

La sezione "PROTOCOLLI COMUNICAZIONE SWARM v1.0.0" (linee 244-317) contiene:
- Script Helper che richiede Bash
- Workflow Task Standard che richiede scrittura file
- Esempio che usa `cat >` per creare output

Queste istruzioni sono state copiate da un template generico senza considerare i tool disponibili.

---

## Fix

Rimuovere/sostituire le sezioni 244-317 con istruzioni che usano SOLO Read, Glob, Grep, WebSearch.

Il reviewer comunica tramite:
- Output testuale diretto (non file)
- WebSearch per trovare best practices

---

## Lezione Imparata

Quando si copia un template DNA, verificare che le istruzioni siano compatibili con i `tools:` dichiarati nel frontmatter.
