# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-18 - Sessione 370
> **STATUS:** FASE 2 IN CORSO (F2.1 DONE). Hook System pubblicabile. Prossimo: F2.2 Agent Templates

---

## SESSIONE 370 - F2.1: Hook System + Auto-Handoff Research

### Contesto
Prima sessione FASE 2. Obiettivo: creare `packages/agent-hooks/` come secondo package PyPI e studiare miglioramento auto-handoff.

### Cosa abbiamo fatto

**Package `cervellaswarm-agent-hooks` v0.1.0 creato:**
- 5 hooks pronti all'uso:
  - `cervella-bash-validator` (PreToolUse) - blocks/asks/auto-fixes bash commands
  - `cervella-git-reminder` (Stop) - desktop notification uncommitted files
  - `cervella-file-limits` (SessionEnd) - configurable file size limits
  - `cervella-context-inject` (SubagentStart) - injects project facts + state
  - `cervella-session-checkpoint` (SessionEnd) - auto-saves git state
- Config system YAML (project/user/env var) con defaults sensati
- CLI: `cervella-hooks setup` genera config + settings.json snippet
- README killer con "Create Your Own Hooks" guide + hook event reference
- 227 test, 98% coverage, 0.12s
- Build: wheel + sdist OK
- Guardiana: 9.1 -> **9.5/10** (2 round, 4 P2 fixed)

**Ricerca Auto-Handoff (Researcher, 14 fonti):**
- Aprire nuove finestre = antipattern confermato (0/5 community tool lo fanno)
- Autocompact 2026 migliorato: buffer 33K, compact istantaneo, session memory auto
- SNCP e autocompact COMPLEMENTARI (disco vs RAM), nessuno rende l'altro obsoleto
- Raccomandazione: eliminare "apri nuova finestra", handoff soft a fine sessione
- Aggiunto come F3.5 nella SUBROADMAP

### Decisioni S370

| Decisione | Perche |
|-----------|--------|
| pyyaml come unica dipendenza | Config system YAML per hooks configurabili. bash_validator e git_reminder funzionano anche senza (stdlib fallback) |
| Config a 3 livelli | CERVELLA_HOOKS_CONFIG env > .cervella/hooks.yaml project > ~/.claude/hooks.yaml user |
| Auto-handoff in F3.5 | Naturale sotto Session Memory (FASE 3), ricerca completata, ready to implement |
| find_project_root walk-up | Cerca .git risalendo directory - pattern standard, funziona in monorepo |

### Lezioni apprese S370
- **Hatchling richiede README.md**: build fallisce senza, creare placeholder prima di pip install -e
- **bash_validator config opzionale**: _load_extra_patterns() con try/except per funzionare senza pyyaml
- **git_reminder cross-platform**: osascript (macOS) + notify-send (Linux) con fallback silenzioso

---

## PROSSIMI STEP
- **F2.2: Agent Definitions come templates** - Template agents (coordinator, quality-gate, architect, worker), frontmatter YAML documentato, esempi (team di 3/7/17)
- **F2.3: Task Orchestration** - task_classifier, architect_flow, task_manager, output_validator
- **F2.4: Spawn Workers portabile** - config-driven, macOS + Linux
- **F3.5: Auto-handoff miglioramento** - rimuovi logica "apri nuova finestra", PreCompact auto-update
- **P3 residui F2.1:** dependabot entry agent-hooks, test config integration, .gitignore refinement

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

---

*"Ultrapassar os proprios limites!" - Rafa & Cervella, S370*
