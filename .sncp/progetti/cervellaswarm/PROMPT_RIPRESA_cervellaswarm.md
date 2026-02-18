# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-18 - Sessione 372
> **STATUS:** FASE 2 IN CORSO (F2.1+F2.2+F2.3 DONE). Prossimo: F2.4 Spawn Workers

---

## SESSIONE 372 - F2.3: Task Orchestration Package

### Contesto
Terza sessione FASE 2. Obiettivo: creare `packages/task-orchestration/` come quarto package - orchestrazione deterministica task con zero LLM calls.

### Cosa abbiamo fatto

**Ricerca (Researcher, 18 fonti, 5 framework):**
- CrewAI: LLM-based routing, no deterministic classification
- AutoGen: max_turns only, no plan validation
- LangGraph: graph-based manual routing, no file-based state
- OpenAI SDK: basic tripwire guardrails, no scoring
- Claude Code: no task routing (manual tool use)
- **Risultato:** ZERO competitor hanno task classification rule-based + file-based state + atomic race protection

**Package `cervellaswarm-task-orchestration` v0.1.0 creato:**
- 5 moduli: task_classifier, architect_flow, task_manager, output_validator, cli
- ZERO dependencies esterne (il piu leggero di tutti i package!)
- Task classifier: 17 keyword, 4 livelli (SIMPLE/MEDIUM/COMPLEX/CRITICAL), fast-path
- Architect flow: routing deterministico + plan validation (4 fasi) + 3-level fallback
- Task manager: marker files (.ready/.working/.done) + atomic `open(f, 'x')` race protection
- Output validator: scoring 0-100 con deductions per errori/incomplete/short/log
- CLI: 6 entry points (cervella-classify/route/validate-plan/validate-output/task/orchestrate)
- 273 test, 0.13s
- Build: wheel + sdist OK
- Guardiana: 9.2 -> **9.5/10** (2 round, 4 P2 + 1 P3 fixed)

**Fix collaterali:**
- dependabot.yml: +1 entry (task-orchestration)
- .gitignore: +.swarm/ (prevenzione file residui)

### Decisioni S372

| Decisione | Perche |
|-----------|--------|
| ZERO dependencies | Classificazione rule-based non ha bisogno di nulla - piu leggero possibile |
| `tasks_dir` parametro ovunque | Original aveva path hardcoded, package deve essere portabile |
| WorkerType da "cervella-backend" a "backend" | Package generico, non CervellaSwarm-specific |
| Unified CLI `cervella-orchestrate` | Un singolo dispatcher per tutti i 5 subcommandi |
| Score clamping 0-100 | Coerenza con validate_plan (0-10 clamped) |

### Lezioni apprese S372
- **Test condizionali sono INVISIBILI**: `if score < 50: assert X` passa anche quando `if` e False. Sempre assert diretto
- **Confronta __all__ con README API**: ogni funzione documentata deve essere accessibile
- **Auto-compact spezza flusso**: checkpoint frequenti prevengono perdita lavoro

---

## PROSSIMI STEP
- **F2.4: Spawn Workers portabile** - config-driven, macOS + Linux
- **F3.5: Auto-handoff miglioramento** - rimuovi "apri nuova finestra", PreCompact auto-update
- **P3 residui F2.3:** README lists 12 functions not in __init__.py (by design - module import), broad except in output_validator

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
| S372 | **FASE 2: F2.3 Task Orchestration** (9.5/10) + Research 5 frameworks |

---

*"Ultrapassar os proprios limites!" - Rafa & Cervella, S372*
