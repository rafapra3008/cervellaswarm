# CervellaSwarm

> Sistema multi-agent: 17 Cervelle coordinate dalla Regina.
> Regole operative complete: `~/.claude/CLAUDE.md`

> **SNCP 4.0 (S357):** Solo PROMPT_RIPRESA + NORD.md. stato.md e oggi.md eliminati.

**INIZIO SESSIONE:** Leggi `.sncp/progetti/{progetto}/PROMPT_RIPRESA_{progetto}.md`

## Hook Attivi (CervellaSwarm)

| Hook | Cosa Fa |
|------|---------|
| session_start_swarm.py | Carica PROMPT_RIPRESA + warnings (COSTITUZIONE via _SHARED_DNA) |
| file_limits_guard.py | Verifica limiti PROMPT_RIPRESA (max 300 righe) |
| subagent_context_inject.py | Inietta FATOS + PROMPT_RIPRESA agli agenti |

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
