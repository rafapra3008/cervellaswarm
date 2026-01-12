# Fix Bug EISDIR cervella-researcher

> **Data:** 12 Gennaio 2026
> **Sessione:** 172
> **Status:** RISOLTO

---

## Il Problema

```
Error: EISDIR: illegal operation on a directory, read
```

Succedeva quando cervella-researcher tentava:
1. `Read(".sncp")` invece di `Read(".sncp/file.md")`
2. Usare comandi Bash (non disponibili)

---

## Causa Root

Il DNA di cervella-researcher (linee 286-359) conteneva:
- Script bash helper (`scripts/swarm/update-status.sh`)
- Comandi `cat >` per creare output
- Workflow che richiedeva tool Bash

Ma i tool disponibili erano solo:
```
Read, Glob, Grep, Write, WebSearch, WebFetch
```

**NO Bash!**

---

## Fix Applicato

Sostituita sezione "PROTOCOLLI COMUNICAZIONE SWARM" con:
1. Lista chiara dei tool disponibili
2. Esempio errore EISDIR e come evitarlo
3. Workflow corretto senza Bash

File modificato: `~/.claude/agents/cervella-researcher.md`

---

## Verifica

- [x] DNA aggiornato
- [ ] Test con prossima ricerca

---

*Bug che esisteva dal 9 Gennaio, fixato 12 Gennaio*
