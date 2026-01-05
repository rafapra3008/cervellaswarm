# Output: TASK_REVIEW_HOOKS_SCRIPTS

**Completato:** 5 Gennaio 2026
**Worker:** cervella-reviewer
**Durata:** ~10 minuti

---

## Risultato

Review COMPLETA eseguita su:
- 8 hooks Python in `~/.claude/hooks/`
- 4 scripts Bash in `~/.local/bin/`
- 2 file config (`~/.swarm/config`, `~/.local/lib/swarm-common.sh`)

---

## Rating Finale: 8.5/10

---

## Problemi Trovati

| Livello | Conteggio | Principali |
|---------|-----------|------------|
| ALTO | 3 | Path NVM hardcodato, escape incompleto, command injection potenziale |
| MEDIO | 5 | Error handling silenzioso, codice duplicato, timeout mancanti |
| BASSO | 4 | Versioni inconsistenti, logging non standard, file temporanei |

---

## Report Completo

Salvato in: `reports/review_hooks_scripts_20260105.md`

---

## Azioni Raccomandate

1. **Subito:** Fix path NVM con glob pattern
2. **Presto:** Creare `~/.claude/hooks/common.py` per DRY
3. **Nice to have:** Standardizzare logging

---

*cervella-reviewer - CervellaSwarm*
