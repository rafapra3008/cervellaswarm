# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-12 - Sessione 355
> **STATUS:** MAPPA 100% + SubagentStart Context Injection LIVE

---

## SESSIONE 355 - MEMORIA DEGLI AGENTI

### Problema risolto
Le abelhas pesquisadoras iniziavano "da zero" - senza FATOS_CONFIRMADOS ne PROMPT_RIPRESA. Redescobrivano fatti gia validati o li contraddicevano.

### Soluzione implementata
Hook SubagentStart globale (`subagent_context_inject.py` v1.0.0) che inietta automaticamente:
- FATOS_CONFIRMADOS.md (fatti verificati - NON contraddire)
- PROMPT_RIPRESA (prime 50 righe - stato attuale)

In TUTTI gli agenti, per TUTTI e 6 i progetti. Performance: 22ms.

### Audit totale della Famiglia
| Area | Score | Fix applicati |
|------|-------|--------------|
| Hook SubagentStart | 9.5/10 | Creato, testato (8/8), live test OK |
| Settings sync | 9/10 | SubagentStart in entrambi global, rimosso da 3 project-level |
| Agenti sync | 10/10 | 6 file sincronizzati main→insiders (security, ingegnera, guardiana-qualita, architect, DNA, SNCP output) |
| SNCP | 8/10 | MASTER aggiornato con tutti 6 progetti, project settings per CervellaBrasil+Chavefy |

### File creati/modificati (S355)
- `~/.claude/hooks/subagent_context_inject.py` - NUOVO (hook principale)
- `~/.claude/settings.json` + `~/.claude-insiders/settings.json` - SubagentStart aggiunto
- `~/.claude/agents/_SHARED_DNA.md` - nota "FATOS gia iniettati"
- 3x project settings.json - SubagentStart rimosso (CervellaSwarm, Miracollo, Contabilita)
- 2x hook .py.DISABLED (Miracollo, Contabilita)
- 6x agent files synced main→insiders
- `~/Developer/CervellaBrasil/.claude/settings.json` - NUOVO
- `~/Developer/Chavefy/.claude/settings.json` - NUOVO
- `.sncp/PROMPT_RIPRESA_MASTER.md` - aggiunto CervellaBrasil + Chavefy

### Decisioni con PERCHE
- **Hook globale** (non per-progetto) perche 1 file copre 6 progetti, meno manutenzione
- **Matcher ""** (tutti gli agenti) perche anche Explore/Plan beneficiano del contesto
- **COSTITUZIONE NON iniettata** perche 510 righe = troppo, DNA gia la referenzia
- **Approccio ibrido** (Hook + DNA) per 100% reliability + no duplicazione

---

## ARCHIVIO

| Sessione | Cosa |
|----------|------|
| S337-S348 | Coverage push 41% -> 95% (968 test) |
| S349 | Audit reale + Pulizia + MAPPA MIGLIORAMENTI |
| S350 | FASE A: Async Hooks + Bash Validator |
| S351 | Persistent Memory + Hook Integrity |
| S352 | COMPLETAMENTO MAPPA: B+C+D = 7 step, score 9.1/10 |
| S353 | CervellaBrasil nasceu! 7 pesquisas, 10k+ linhas |
| S354 | Chavefy nasceu! SaaS Property Management Brasil |
| S355 | SubagentStart Context Injection + Audit totale Famiglia |

---

*"Lavoriamo in pace! Senza casino! Dipende da noi!"*
*Sessione 355 - Cervella & Rafa*
