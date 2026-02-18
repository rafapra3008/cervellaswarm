# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-18 - Sessione 372
> **STATUS:** FASE 2 IN CORSO (F2.1+F2.2+F2.3+F2.4 DONE). Prossimo: F2.5 o FASE 3

---

## SESSIONE 372 - F2.3 + F2.4

### F2.3: Task Orchestration Package (DONE)
- Package `cervellaswarm-task-orchestration` v0.1.0
- 5 moduli, ZERO deps, 273 test, Guardiana 9.5/10

### F2.4: Spawn Workers Package (DONE)
- Package `cervellaswarm-spawn-workers` v0.1.0 at `packages/spawn-workers/`
- 5 moduli: backend (tmux/nohup auto-detect), team_loader (YAML), spawner (SpawnManager), prompt_builder (10 specialties), cli (cervella-spawn)
- 1 dependency: pyyaml
- Config-driven spawn da team.yaml (riusa F2.2 schema + sezione `spawn:`)
- Signal handling SIGINT/SIGTERM -> kill_all -> cleanup + atexit
- Cross-invocation status/kill via tracking files (_load_tracked_workers)
- Shell injection safety (shlex.quote)
- 171 test, 0.13s (tutti mocked, zero processi reali)
- Guardiana: 9.2 -> **9.5/10** (2 round, 4 P2 + 1 P3 fixed)
- Research: 18 fonti, ZERO competitor hanno file-based state + tmux isolation + config-driven spawn

### Decisioni S372

| Decisione | Perche |
|-----------|--------|
| tmux > nohup auto-detect | tmux preferito (sessions, remain-on-exit), nohup fallback universale |
| shlex.quote su command building | Safety: claude_bin, prompt_file, initial_prompt sono user-influenced |
| _load_tracked_workers in __init__ | --status e --kill devono funzionare tra invocazioni separate |
| importlib.metadata per version | Single source of truth (solo pyproject.toml), nessun rischio drift |
| team.yaml spawn section unconditional | Fragile confrontare con default magic ("!= .swarm/tasks"), applicare sempre |

### Lezioni apprese S372
- **Shell injection in subprocess**: `shell=True` + f-string = injection risk. Sempre `shlex.quote()`
- **Tracking files write-only = non-functional CLI**: se scrivi PID/session, DEVI leggerli nel costruttore
- **Version dual source**: `importlib.metadata.version()` e il modo standard, NO hardcoded `__version__`

---

## PROSSIMI STEP
- **F2.5+:** Verificare SUBROADMAP per prossimi package FASE 2
- **FASE 3:** SNCP (session continuity) - il differenziatore piu unico
- **P3 residui F2.4:** status_dir CLI passthrough, duplicate worker entries, .start ValueError guard

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
| S372 | **FASE 2: F2.3 Task Orchestration** (9.5/10) + **F2.4 Spawn Workers** (9.5/10) |

---

*"Ultrapassar os proprios limites!" - Rafa & Cervella, S372*
