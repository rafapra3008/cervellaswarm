# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-19 - Sessione 379
> **STATUS:** Auto-Handoff System fixato (S379). Prossimo: Lingua Universale Fase A.

---

## SESSIONE 379 - FIX AUTO-HANDOFF SYSTEM (FINALE)

### Cosa: Pulizia sistema anti-compact/auto-handoff (13+ hook/script legacy da S79-S99)

8 step eseguiti, Guardiana audit dopo ogni blocco: media 9.5/10

### Cosa e cambiato

**Settings.json (main + insiders):**
- Rimosso `anti-compact.sh` da PreCompact "auto" (causa commit ANTI-COMPACT automatici)
- Rimosso `UserPromptSubmit` (context_check.py 100% ridondante con statusline CTX:XX%)

**Hook disabilitati:**
- `context_check.py` -> `.DISABLED` (main + insiders) + state file eliminato
- `pre-compact.sh` -> `.DISABLED` (main + insiders)

**Hook modernizzati (v3.0.0):**
- `pre_compact_save.py` + `session_end_save.py` (4 file: main + insiders)
  - Snapshot in `~/.claude/snapshots/` (era iCloud)
  - SECURITY A1: rimosso `read_transcript_summary()` (transcript puo contenere secrets)
  - Rotazione max 50 file per dir
  - 6 progetti KNOWN (era 4): +Chavefy, +CervellaCostruzione, +CervellaBrasil
  - Rimosso `million-dollar-ideas` + `ultimo_lavoro` (legacy)
  - `bare except:` -> typed exceptions

**Deploy update_prompt_ripresa.py v2.0.0:**
- Sorgente repo aggiornato (`config/claude-hooks/update_prompt_ripresa.py`)
- 6 progetti con path SNCP 4.0 corretti
- Deployato a main + insiders

**anti-compact.sh v2.0.0 (uso manuale):**
- SNCP 4.0: detect progetto da CWD con `SNCP_MAP`
- SECURITY A2: `git add -A` -> `git add .sncp/ docs/ NORD.md` esplicito
- Spawn VS Code RIMOSSO (confermato antipattern, 14 fonti S370)
- `--no-spawn` silently ignored (backward compat)

**Archivio + cleanup:**
- 180 file HANDOFF_*.md -> `.swarm/handoff/archive/`
- `memory-flush.sh`: rimosso riferimento a `stato.md` (bug SNCP 4.0)
- SUBROADMAP F3.5 marcato DONE (3/4 criteri)

### Guardiana Audit Trail

| Blocco | Score |
|--------|-------|
| Step 1 (settings.json) | 9.7/10 |
| Steps 3-4 (hooks v3.0.0) | 9.5/10 |
| Steps 5-8 (legacy + anti-compact + archive) | 9.5/10 |
| **Media** | **9.5/10** |

### Debito P3 (futuro, non bloccante)

- `context-monitor.py`: path hardcoded (funzionale, modernizzare dopo)
- Unificazione in `session_checkpoint.py` (proposta Ingegnera)
- 9 docs nel repo con "anti-compact" stale (OVERVIEW_FAMIGLIA, README_QUICK_WINS, etc)
- `settings.local.json`: permission stale per `pre-compact.sh`
- 1345 snapshot legacy in iCloud REGOLE_GLOBALI (da archiviare)

---

## MAPPA SITUAZIONE

```
OPEN SOURCE ROADMAP:
  FASE 0  [####################] 100% (S362-S367)
  FASE 1  [####################] 100% (S368-S369, PyPI LIVE!)
  FASE 2  [####################] 100% (S370-S372, 4 packages)
  FASE 3  [####................] 25% (F3.1 DONE, F3.5 DONE)
  FASE 4  [....................] TODO

CACCIA BUG: 7/7 COMPLETATA (80 bug, 48 fix, 1649 test, 9.5 media)
AUTO-HANDOFF: FIXATO (S379, 8 step, 9.5/10)
LINGUA UNIVERSALE: 95 fonti, 5 report, visione A->B->C->D (S375)
```

---

## PROSSIMI STEP

1. **Lingua Universale Fase A** - Session Types per agent protocol
2. **Prototipo Lean 4** - verificare proprieta del task routing
3. **F3.2 SQLite Event Database** - prossimo step open source
4. **Nota:** core/ e api/ hanno ancora "Rafa & Cervella" (18 file) - cleanup separato

---

## ARCHIVIO

| Sessione | Cosa |
|----------|------|
| S337-S348 | Coverage push 41% -> 95% (968 test) |
| S349-S361 | MAPPA MIGLIORAMENTI + SNCP 4.0 + POLISH + ANTI-DOWNGRADE |
| S362-S367 | **FASE 0 COMPLETA** (6/6 step, media 9.4/10) |
| S368-S369 | **FASE 1 COMPLETA** (F1.1-F1.4, PyPI LIVE!) |
| S370-S372 | **FASE 2 COMPLETA** (4/4 packages, media 9.5/10) |
| S373 | **FASE 3: F3.1 Session Memory** (9.6/10) |
| S374 | **CACCIA BUG #1: code-intelligence** (8 fix, 398 test, 9.5/10) |
| S375 | **LA LINGUA UNIVERSALE** (95 fonti, 5 report, visione A->B->C->D) |
| S376 | **CACCIA BUG #2+#3: task-orchestration + spawn-workers** (17 fix, 496 test) |
| S377 | **CACCIA BUG #4+#5+#6: session-memory + agent-hooks + agent-templates** (9 fix, 621 test) |
| S378 | **CACCIA BUG #7: CLI+MCP** (14 fix, 134 test, 9.5/10) - TUTTI COMPLETATI! |
| S379 | **FIX AUTO-HANDOFF** (8 step, 14 file, 180 handoff archiviati, 9.5/10) |

---

*"Ultrapassar os proprios limites!" - Rafa & Cervella*
*"Lavoriamo in pace! Senza casino! Dipende da noi!"*
