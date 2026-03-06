# SUBROADMAP: Migliora Casa - Configurazione & SNCP

> **Creata:** 6 Marzo 2026 - Sessione 431
> **Status:** COMPLETATA (MC1-MC7 DONE + Backlog S432 DONE)
> **Filosofia:** "Mai avanti senza fixare le cose" | "I dettagli fanno SEMPRE la differenza"
> **Metodo:** Ogni step -> Guardiana audit -> standard 9.5/10

---

## MAPPA STEP

### MC1: Pulizia Settings -- DONE 9.7/10
- [x] settings.local.json: 34 regole ridondanti rimosse (entrambi)
- [x] .claude/ e .claude-insiders/ settings.json: byte-identical
- [x] Rimosso "model": "opus" da insiders (Opus 4.6 e default)

### MC2: Review Hooks -- DONE 9.5/10
- [x] Researcher: nuove hook API studiate (HTTP, WorktreeCreate -> FUTURO)
- [x] subagent_stop.py v1.1->v2.0: agent_type reale, CREATE TABLE, WAL mode
- [x] P1 critico: DB swarm_events era VUOTO da sempre! Ora funziona

### MC3: MCP & Status Line -- DONE 9.3/10
- [x] health_check.py: docstring corretto (MCP server USA API key per spawn-worker)
- [x] context-monitor.py: worktree fields non critici (usiamo raramente worktrees)

### MC4: SNCP Maintenance -- DONE
- [x] SNCP gia solido (Researcher conferma), no evoluzione architetturale
- [x] PROMPT_RIPRESA_MASTER aggiornato (era fermo a S384!)
- [ ] 32 report obsoleti da committare (attendono conferma Rafa)

### MC5: Review Agenti -- DONE 9.5/10
- [x] 17/17 agenti OK, modelli opus/sonnet alias auto-update a 4.6
- [x] cervella-architect v1.0->v2.1 (unica anomalia, fixata)

### MC6: P3 Batch Fix -- DONE 9.5/10
- [x] file_limits_guard: dead code stato.md rimosso, 6 progetti aggiunti (v3.1.0)
- [x] post_commit_engineer: timeout 300s->55s
- [x] 7x bare `except:` -> `except Exception:` in 3 hook

### MC7: Bug Hunt (3 round) -- DONE
- [x] R1 Guardiana OPS: 11 bug (2P1 + 4P2 + 5P3)
- [x] R2 Ingegnera: 7 inconsistenze cross-reference
- [x] R3 Researcher: 3 bug + 6 opportunita
- [x] Fix applicati: 7 fix critici (vedi sotto)
- [ ] MC7.4: Guardiana Qualita audit finale - IN CORSO

---

## FIX TOTALI APPLICATI (S431)

| # | Cosa | Impatto |
|---|------|---------|
| 1 | DB swarm_events: CREATE TABLE IF NOT EXISTS | P1: DB era vuoto da sempre |
| 2 | update_prompt_ripresa: marker HTML univoci | P1: PROMPT_RIPRESA non si corrompe |
| 3 | memory_flush_auto rimosso (duplicato rotto) | P1: flush sbagliati eliminati |
| 4 | SQLite WAL mode + timeout=10 | P2: niente piu eventi persi |
| 5 | PROJECT_MAPPING universale (7 hook, 6 progetti) | P2: tutti i progetti riconosciuti |
| 6 | post_commit_engineer async: true | P2: commit non bloccati 60s |
| 7 | db.py Python 3.9 compat (Optional) | BUG: weekly_retro funziona |
| 8 | subagent_stop v2.0 su 3 repos | Contabilita + Miracollo aggiornati |
| 9 | settings.local.json puliti | 34 regole ridondanti rimosse |
| 10 | settings.json .claude/.claude-insiders sync | Byte-identical |
| 11 | cervella-architect v1.0->v2.1 | Versione allineata |
| 12 | file_limits_guard v3.0->v3.1 | Dead code + nuovi progetti |
| 13 | post_commit timeout 300s->55s | Allineato a settings 60s |
| 14 | 7x bare except fixati | except Exception in 3 hook |

---

## BACKLOG RESIDUO -- COMPLETATO S432

| # | Sev | Descrizione | Status |
|---|-----|-------------|--------|
| 1 | P2 | bash_validator: bypass con $() e backtick | FIXED S432 |
| 2 | P3 | git_reminder: state file cresce indefinitamente | FIXED S432 |
| 3 | P3 | pre_compact_save: git log `|` separator fragile | FIXED S432 |
| 4 | P3 | context-monitor: CONTEXT_LIMIT 200k hardcoded | DOCUMENTED S432 |
| 5 | P3 | context-monitor: 6x bare except | FIXED S432 |
| 6 | P3 | hook_debug.log a 33MB senza rotation | FIXED S432 (5MB rotation) |
| 7 | INFO | 32 reports + 2 log da committare | COMMITTED S432 |
| 8 | OPP | .claude/rules/ path-specific scoping per LU | FUTURO |
| 9 | OPP | opusplan alias per Architect | FUTURO |

---

## DOPO QUESTA SUBROADMAP

Riprendiamo da **D5 LSP Avanzato** (Hover + Completion + Go-to-def).
Contesto in PROMPT_RIPRESA_cervellaswarm.md.

---

*"Mai avanti senza fixare le cose" - Rafa*
*"I dettagli fanno SEMPRE la differenza"*
