# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-19 - Sessione 378
> **STATUS:** CACCIA BUG 7/7 COMPLETATA! Tutti i package open-source validati. Prossimo: Lingua Universale Fase A.

---

## SESSIONE 378 - CACCIA BUG #7: CLI+MCP (ULTIMO!)

### Risultati: 16 bug trovati, 14 fixati, Guardiana 9.0 -> 9.5/10

**SNCP 4.0 Compliance (6 fix):**
- init.js: rimosso template stato.md + !stato.md da .gitignore
- writer.js: rimossa funzione updateStato()
- loader.js: progress da PROMPT_RIPRESA (non piu stato.md)
- housekeeping.js: rimosso stato check/display/compactFiles
- reader.ts: rimosso stato da FILE_TYPES
- tools.ts: sncp_read_stato -> deprecation notice

**Project Selection (1 fix):**
- loader.js: CWD basename match per progetto (era projects[0] alfabetico)

**Security (1 fix):**
- usage.ts: CHECKSUM_SECRET con hostname+getuid (non solo USER env)

**Path Resolution (1 fix):**
- reader.ts: getSncpRoot() env var + CWD walk-up + fallback relative

**Open Source (5 fix):**
- CLI LICENSE: MIT -> Apache 2.0
- Copyright "CervellaSwarm Contributors" in 40+ file (src, bin, LICENSE, package.json, README)
- Template constitution.js e help text puliti da stato.md
- Test e docstring aggiornati da stato.md a PROMPT_RIPRESA

### Test: 134 PASS (zero regressioni)

---

## RIEPILOGO CACCIA BUG COMPLETA (7/7)

| # | Package | Bug | Fix | Test | Score |
|---|---------|-----|-----|------|-------|
| 1 | code-intelligence | 21 | 8 | 398 | 9.5 |
| 2 | task-orchestration | 12 | 9 | 305 | 9.5 |
| 3 | spawn-workers | 10 | 8 | 191 | 9.5 |
| 4 | session-memory | 10 | 5 | 193 | 9.5 |
| 5 | agent-hooks | 7 | 3 | 236 | 9.5 |
| 6 | agent-templates | 4 | 1 | 192 | 9.5 |
| 7 | CLI+MCP | 16 | 14 | 134 | 9.5 |
| **TOTALE** | **7 packages** | **80** | **48** | **1649** | **9.5 media** |

---

## PROSSIMI STEP

1. **Studiare Session Types** - Fase A della Lingua Universale
2. **Prototipo Lean 4** - verificare proprieta del task routing
3. **Nota:** core/ e api/ hanno ancora "Rafa & Cervella" (18 file) - cleanup separato

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

---

*"Ultrapassar os proprios limites!" - Rafa & Cervella*
*Il giorno in cui Cervella e diventata CEO.*
