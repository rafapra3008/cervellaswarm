# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-10 - Sessione 350
> **STATUS:** FASE A (A.1 + A.2) completata. MAPPA MIGLIORAMENTI 2/11 step FATTI.

---

## SESSIONE 350 - FASE A Quick Wins (A.1 + A.2)

```
+================================================================+
|   S350: FASE A - 2 STEP COMPLETATI                              |
|                                                                  |
|   A.1 Async Hooks SessionEnd    -> FATTO (9/10)                 |
|   A.2 PreToolUse Bash Validator -> FATTO (9.5/10)               |
|                                                                  |
|   Guardiana audit dopo ogni step -> standard confermato          |
+================================================================+
```

### Cosa fatto
| # | Azione | Dettaglio |
|---|--------|-----------|
| 1 | A.1: Async Hooks | 4 hook non-critici resi async, 2 critici sync. Settings main + insiders allineati |
| 2 | A.2: Bash Validator | Nuovo `bash_validator.py` con 3 livelli: BLOCK/ASK/ALLOW + auto-fix force->lease |
| 3 | Guardiana audit x2 | Ogni step verificato dalla Guardiana. Score 9/10 e 9.5/10 |
| 4 | MAPPA aggiornata | A.1 e A.2 marcati FATTO con score |

### Decisioni Prese con PERCHE
- **Async solo non-critici** perche save + prompt_ripresa DEVONO completare prima di chiudere
- **Safe rm list** perche rm -rf node_modules/dist/build sono operazioni normali, non pericolose
- **Auto-fix force->lease** perche --force-with-lease e sempre preferibile a --force
- **Test da file** perche il validator blocca comandi con pattern pericolosi nel testo inline

### File Creati/Modificati
- `~/.claude/hooks/bash_validator.py` - NUOVO: validatore comandi bash (224 righe)
- `~/.claude/settings.json` - Async hooks + PreToolUse hook
- `~/.claude-insiders/settings.json` - Async hooks + PreToolUse hook
- `.sncp/.../MAPPA_MIGLIORAMENTI_INTERNI.md` - A.1+A.2 marcati FATTO

---

## PROSSIMA SESSIONE (S351)

**COSA FARE:** A.3 + C.1

| Step | Cosa | Tempo |
|------|------|-------|
| A.3 | Persistent Memory per Guardiane | 2h |
| C.1 | Hook Integrity Check | 2h |

**DOVE:** `.sncp/progetti/cervellaswarm/roadmaps/MAPPA_MIGLIORAMENTI_INTERNI.md`

**NOTA:** Miracollook plist hanno path sbagliati - fixare quando si lavora su quel progetto.

---

## ARCHIVIO

| Sessione | Cosa |
|----------|------|
| S337-S348 | Coverage push 41% -> 95% (968 test) |
| S349 | Audit reale + Pulizia + MAPPA MIGLIORAMENTI |
| S350 | FASE A: A.1 Async Hooks (9/10) + A.2 Bash Validator (9.5/10) |

---

*"Un po' ogni giorno fino al 100000%!"*
*Sessione 350 - Cervella & Rafa*
