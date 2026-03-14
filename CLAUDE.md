# CervellaSwarm

> Sistema multi-agent: 17 Cervelle coordinate dalla Regina.
> Regole operative complete: `~/.claude/CLAUDE.md`

> **SNCP 4.0 (S357):** Solo PROMPT_RIPRESA + NORD.md. stato.md e oggi.md eliminati.

## Hook Attivi (CervellaSwarm)

| Hook | Cosa Fa |
|------|---------|
| sncp_pre_session_hook.py | Pre-session checks + puntatori (v1.1.0) |
| file_limits_guard.py | Verifica limiti PROMPT_RIPRESA (max 250 righe, v3.3.0) |
| subagent_context_inject.py | Inietta contesto COMPLETO agli agenti (v2.0.0 - no truncation) |
| context-monitor.py | Statusline CTX + soglie 85/92% (v3.0.0 - 1M era) |

## La Famiglia

17 agenti in `~/.claude/agents/`:
- 1 Regina (opus) + 3 Guardiane (opus) + 1 Architect (opus) + 2 Analiste (opus)
- 10 Worker (sonnet). Dettagli: `docs/DNA_FAMIGLIA.md`

## File Chiave

| File | Scopo |
|------|-------|
| `NORD.md` | Direzione progetto |
| `.sncp/PROMPT_RIPRESA_MASTER.md` | Overview tutti progetti |
| `.sncp/roadmaps/` | Piani e subroadmap |

## DUAL REPO - REGOLA SACRA

```
+================================================================+
|   MAI FARE: git push public main                               |
|   SEMPRE USARE: ./scripts/git/sync-to-public.sh                |
|                                                                |
|   origin = privato (tutto)                                     |
|   public = pubblico (solo packages/, docs pubbliche)           |
|                                                                |
|   Docs: docs/DUAL_REPO_STRATEGY.md                            |
+================================================================+
```

**LEZIONE APPRESA (Sessione 286):** Terza volta che incontriamo questo problema!
