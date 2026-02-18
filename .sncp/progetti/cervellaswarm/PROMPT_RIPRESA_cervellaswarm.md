# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-18 - Sessione 371
> **STATUS:** FASE 2 IN CORSO (F2.1+F2.2 DONE). Prossimo: F2.3 Task Orchestration

---

## SESSIONE 371 - F2.2: Agent Templates Package

### Contesto
Seconda sessione FASE 2. Obiettivo: creare `packages/agent-templates/` come terzo package - template agenti riusabili per chiunque.

### Cosa abbiamo fatto

**Ricerca (Researcher, 18 fonti, 5 framework):**
- CrewAI: role/goal/backstory ottimo per onboarding -> aggiunto `role:` field
- AutoGen/AG2: pure Python, zero DX -> confermato che Markdown+YAML e meglio
- LangGraph: state machines, maximum flexibility, maximum complexity
- Claude Code nativo: campi non usati (permissionMode, maxTurns, skills) -> integrati
- OpenAI SDK: handoff dichiarativo elegante
- **Risultato:** il nostro formato e GIA il migliore. Gap: 4-5 campi nativi da aggiungere

**Package `cervellaswarm-agent-templates` v0.1.0 creato:**
- 4 template agents: coordinator, quality-gate, architect, worker
- 7 worker specialties: backend, frontend, tester, researcher, devops, docs, generic
- `_shared_dna.md` generico (zero riferimenti personali)
- `team.yaml` formato composizione team (NESSUN competitor ce l'ha!)
- CLI: `cervella-agent init/init-team/list/validate`
- 3 team examples: minimal (3), standard (7), full (17)
- Frontmatter reference completa (16 campi documentati)
- README killer con comparison table + honest note
- 188 test, 0.16s
- Build: wheel + sdist OK
- Guardiana: 9.3 -> **9.5/10** (2 round, 4 P2 + 3 P3 fixed)

**Fix collaterali:**
- dependabot.yml: +2 entry (agent-hooks + agent-templates)
- .gitignore: +dist/ +build/ (era mancante)

### Decisioni S371

| Decisione | Perche |
|-----------|--------|
| `role:` field aggiunto | Ispirato da CrewAI (best idea), human-readable label per routing |
| `team.yaml` formato | Zero competitor hanno composizione team dichiarativa - differenziale unico |
| `permissionMode:` + `maxTurns:` | Campi nativi Claude Code, non li usavamo ancora |
| 7 worker specialties | Copertura completa dei ruoli comuni + generic catch-all |
| pyyaml come unica dep | YAML per team.yaml rendering, leggerissimo |

### Lezioni apprese S371
- **Team.yaml e un differenziale reale**: 0 su 5 framework hanno composizione team dichiarativa
- **Shared DNA via Markdown > Python inheritance**: piu leggibile, editabile da non-dev
- **Worker specialty con template variables**: `{{ specialty_details }}` evita duplicazione

---

## PROSSIMI STEP
- **F2.3: Task Orchestration** - task_classifier, architect_flow, task_manager, output_validator
- **F2.4: Spawn Workers portabile** - config-driven, macOS + Linux
- **F3.5: Auto-handoff miglioramento** - rimuovi "apri nuova finestra", PreCompact auto-update
- **P3 residui F2.2:** CI workflow agent-templates, validator per campi extra, specialist content per full-team

---

## ARCHIVIO

| Sessione | Cosa |
|----------|------|
| S337-S348 | Coverage push 41% -> 95% (968 test) |
| S349-S361 | MAPPA MIGLIORAMENTI + SNCP 4.0 + POLISH + ANTI-DOWNGRADE |
| S362 | OPEN SOURCE STRATEGY! subroadmap 5 fasi |
| S363-S367 | **FASE 0 COMPLETA** (6/6 step, media 9.4/10) |
| S368-S369 | **FASE 1 COMPLETA** (F1.1-F1.4, media 9.5/10, PyPI LIVE!) |
| S370 | **FASE 2: F2.1 Hook System** (9.5/10) + Auto-Handoff Research |
| S371 | **FASE 2: F2.2 Agent Templates** (9.5/10) + Research 5 frameworks |

---

*"Ultrapassar os proprios limites!" - Rafa & Cervella, S371*
