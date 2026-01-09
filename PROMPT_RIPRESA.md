# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 9 Gennaio 2026
> **Versione:** v51.0.0 - FASE 2.2 DNA Famiglia Completata

---

## Stato Attuale

| Cosa | Stato |
|------|-------|
| FASE 1: CLAUDE.md + PROMPT_RIPRESA snelli | COMPLETATA |
| FASE 2.2: DNA Famiglia (16 membri) | COMPLETATA |
| FASE 2.3: CLAUDE.md globale snello | IN CORSO |
| FASE 3: Rollout Miracollo | Da fare |

---

## Ultima Sessione - 135

**Cosa fatto:**
- Aggiornati tutti 16 DNA con sezione REGOLE CONTEXT-SMART
- 12 Worker (Sonnet) + 3 Guardiane (Opus) + 1 Orchestrator
- Ogni DNA ora ha: max 500 token, usa SNCP, regola 5 min, output strutturato

**File modificati:**
- `~/.claude/agents/cervella-*.md` (tutti e 16)

---

## Prossimi Step

1. FASE 2.3: CLAUDE.md globale snello (527 -> ~180 linee)
2. FASE 3: Rollout Miracollo
3. Test completo del workflow

---

## Puntatori

| Cosa | Dove |
|------|------|
| Roadmap completa | `.sncp/idee/LA_NOSTRA_STRADA_ROADMAP_FINALE.md` |
| Template sezione DNA | `templates/DNA_CONTEXT_SMART_SECTION.md` |
| Backup DNA originali | `~/.claude/agents_backup_20260109/` |
| Decisioni | `.sncp/memoria/decisioni/` |

---

## Note Tecniche

- CLAUDE.md progetto: 47 linee (snello)
- CLAUDE.md globale: 527 linee (da snellire a ~180)
- Test: `./tests/run_all_tests.sh` (23 test, tutti passano)
