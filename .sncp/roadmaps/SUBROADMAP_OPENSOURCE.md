# SUBROADMAP - CervellaSwarm Open Source

> **Creata:** 16 Febbraio 2026 - Sessione 362
> **Obiettivo:** Pubblicare CervellaSwarm come framework open source di riferimento
> **Filosofia:** "Ultrapassar os proprios limites!"
> **Score target:** 9.5/10 per ogni fase (audit Guardiana)

---

## VISIONE

```
+================================================================+
|   CervellaSwarm Open Source                                     |
|                                                                 |
|   "The first multi-agent framework with real session            |
|    continuity. Built before it was easy.                        |
|    Battle-tested in 361 sessions."                              |
|                                                                 |
|   3 GAPS UNICI (nessun competitor li risolve tutti):            |
|   1. Session Continuity nativa (SNCP 4.0)                      |
|   2. Orchestrazione gerarchica reale (3+ livelli)               |
|   3. Hook system first-class (15+ hooks, 9 lifecycle events)    |
|                                                                 |
|   TARGET: Developers Claude Code + Enterprise compliance        |
|   LICENSE: Apache 2.0 (protezione brevetti + enterprise safety) |
|   BUSINESS: Open Core (core free forever)                       |
+================================================================+
```

---

## CONTESTO - 3 Ricerche Base (S362)

### Landscape Competitivo (Scienziata)

| Framework | Stars | Session Memory | Hierarchy | Hooks | Transparent |
|-----------|-------|----------------|-----------|-------|-------------|
| AutoGen | 51.8k | NO | Basic | NO | Partial |
| CrewAI | 44.2k | NO | Basic | NO | Partial |
| LangGraph | 24.7k | NO | Manual | NO | Partial |
| **CervellaSwarm** | **0 (new)** | **SNCP 4.0** | **3 livelli** | **15+** | **100%** |

### Audit Tecnico (Ingegnera)

- 56.800 righe Python, 16.600 righe Bash
- 1.236 test, 95% coverage
- 135+ script files, 17 agent definitions
- Componente #1 per valore: AST Pipeline (ZERO dati personali)

### Autocompact & Session Memory (Researcher)

- Autocompact 2026 molto migliorato (buffer 45K -> 33K, -84% consumo)
- SNCP complementare (non sostituibile): Session Memory = RAM, SNCP = Disco
- Sessioni continue 4-6h ora viabili
- Overhead riducibile da 40min a 10min/sessione (-75%)

---

## FASI

---

### FASE 0: PREPARAZIONE REPO (3-4 sessioni, ~20h)

> Preparare il repository pubblico senza dati personali.
> **NOTA:** 29 script files hanno nomi progetto hardcoded, 105 occorrenze di paths personali.
> Effort maggiore del previsto -- la Guardiana ha verificato il codebase.

**F0.1 - Struttura repo open source** -- DONE (S363)
- [x] ~~Creare branch `opensource` da main~~ (usando dual-repo strategy instead)
- [x] Definire `.gitignore` per escludere dati personali (1006 file untracked)
- [x] Struttura directories: `packages/`, `examples/`, `docs/`, `tests/`
- [x] sync-to-public.sh v3.0 con whitelist + content scanning
- **Score:** Guardiana 9.3/10

**F0.2 - Licenza e docs base** -- DONE (S363)
- [x] LICENSE (Apache 2.0 - gia esistente)
- [x] README.md killer -- DONE in F0.4 (S366)
- [x] CONTRIBUTING.md (come contribuire)
- [x] CODE_OF_CONDUCT.md (Contributor Covenant 2.1)
- [x] SECURITY.md (responsible disclosure, cervellaswarm@pm.me)
- **Criterio:** Community files completi

**F0.3 - Script sanitization e content scanner** -- DONE (S363-S364)
- [x] Scan completo: Ingegnera + Security audit (848 occorrenze mappate)
- [x] sync-to-public.sh v3.1: 12 content patterns, rafapra3008/contabilita ottimizzati
- [x] Zero `/Users/rafapra` in script eseguibili (25+ script sanitizzati)
- [x] Pattern SCRIPT_DIR portabile uniforme in tutti gli script
- [x] DEVELOPER_ROOT env var per multi-utente
- [x] docs/SEMANTIC_SEARCH.md + GETTING_STARTED.md sanitizzati
- [x] git-filter-repo: assessed NOT NEEDED in F0.6 (S367) - public repo uses orphaned clean history
- **Score:** Guardiana 7.8 -> 8.8 -> 9.5/10 (3 round)
- **Nota F3:** MCP KNOWN_PROJECTS hardcoded -> rendere configurabile

**F0.4 - README killer** -- DONE (S366)
- [x] Ricerca competitor (AutoGen, CrewAI, LangGraph) + best practices (12 fonti)
- [x] README.md 239 righe: hero, problem, quickstart, comparison table, docs
- [x] Tagline: "Build AI agent teams that remember."
- [x] Honest comparison table (ammette competitor piu grandi + multi-LLM)
- [x] Quick Start da source (clone + npm link)
- [x] Hero image rimossa (conteneva dati interni) -> ASCII diagram
- [x] Fix Go/Rust false claim, npm install, Opus/Sonnet, duration
- **Score:** Guardiana 8.3 -> 9.5/10 (2 round)
- **Residui P3:** hero image da ricreare pulita, badges dinamici con CI, CHANGELOG Go/Rust

**F0.5 - .github/ templates** -- DONE (S366)
- [x] Issue templates YAML form-based (bug report 7 campi, feature request 6 campi)
- [x] PR template (summary + type + test plan + checklist)
- [x] dependabot.yml (7 entry: 3 npm + 2 pip + github-actions, grouped)
- [x] CODEOWNERS + FUNDING.yml + stale.yml workflow
- [x] Sanitizzazione 5 file esistenti (CLAUDE.md, weekly-maintenance, publish, claude-review, ci+test)
- [x] cervella/pyproject.toml: MIT -> Apache-2.0, description + author genericizzati
- [ ] Dynamic badges (Codecov) -- DEFERRED to F1 (needs CI running on public repo)
- **Score:** Guardiana 9.0 -> 9.3/10 (2 round)

**F0.6 - Extended content scanner** -- DONE (S367)
- [x] Content scanner v3.2: scan ALL text files via `grep -rI` (was: 9 specific extensions)
- [x] Added "famiglia digitale" content pattern (COSTITUZIONE/NORD.md protected by root-path check, not content scan - avoids self-blocking)
- [x] Added Check 5: sensitive config files (.env, secrets.*, credentials.*)
- [x] Added .env to filename blacklist patterns
- [x] Fixed Co-Authored-By email (was cervellaswarm.com, now noreply@users.noreply.github.com)
- [x] All script messages AND comments translated to English (was Italian)
- [x] git-filter-repo: ASSESSED NOT NEEDED (public repo has orphaned clean history, sync script prevents leaks)
- [x] P3 fixes: CHANGELOG Go/Rust, pyproject.toml Italian->English + URLs, .egg-info removed from git
- **Score:** Guardiana 8.8 -> 9.5/10 (2 rounds, 1 P1 + 5 P2 fixed)

**Audit Guardiana dopo F0** -> target 9.5/10

---

### FASE 1: AST PIPELINE - "Quick Win" (2-3 sessioni, ~10h)

> Primo pacchetto: il componente con piu valore e zero cleanup.

**F1.1 - Estrarre AST Pipeline come pacchetto standalone** -- DONE (S368)
- [x] `packages/code-intelligence/` con pyproject.toml (Hatchling, PEP 639)
- [x] 14 moduli con import normalizzati (relative imports)
- [x] 3 CLI entry points: `cervella-search`, `cervella-impact`, `cervella-map`
- [x] SPDX headers Apache-2.0, LICENSE "CervellaSwarm Contributors"
- [x] pip install -e . funziona, smoke test OK, wheel build OK
- **Score:** Guardiana 9.6/10

**F1.2 - Test suite standalone** -- DONE (S368)
- [x] 20 test files + conftest.py (6774 linee) copiati e adattati
- [x] Bulk transformation: import paths + mock paths allineati al package
- [x] **396 test raccolti, 395 passed, 1 skipped, 0 failed, 0.47s**
- [ ] CI con GitHub Actions (Python 3.10, 3.11, 3.12) -- TODO: add to CI workflow
- [ ] Coverage badge (target: 90%+) -- DEFERRED: needs CI running
- **Score:** Guardiana 9.5/10

**F1.3 - Documentazione pacchetto** -- DONE (S368)
- [x] README 225 righe: architettura ASCII, API reference, limitazioni oneste, CLI examples
- [x] CHANGELOG.md per v0.1.0
- [x] ImpactResult aggiunto a __init__.py exports
- **Score:** Guardiana 9.5/10

**F1.4 - Pubblicazione** -- DONE (S369)
- [x] GitHub Actions workflow `publish-pypi.yml` (Trusted Publishing OIDC)
- [x] CI workflow `ci-code-intelligence.yml` (Python 3.10-3.13 matrix)
- [x] Configurato Trusted Publishing su PyPI + TestPyPI (cervellaswarm-internal)
- [x] GitHub Environments: testpypi (auto) + pypi (manual approval)
- [x] Fix: scipy dipendenza per PageRank + repo name mismatch
- [x] Tag `code-intelligence-v0.1.0` -> **LIVE su PyPI!**
- [x] GitHub Release con attestazioni PEP 740 (Sigstore)
- [ ] Post su Reddit r/ClaudeAI, r/Python, Twitter/X -- DEFERRED to F4.1
- **Score:** Guardiana 9.5/10

**Audit Guardiana dopo F1** -> target 9.5/10

---

### FASE 2: AGENT FRAMEWORK (8-12 sessioni, ~50h)

> Il cuore: definizioni di agenti, hooks, task orchestration.

**F2.1 - Hook System pubblicabile** -- DONE (S370)
- [x] `packages/agent-hooks/` con 5 hooks generici + CLI + config system
- [x] bash_validator.py (PreToolUse: block/ask/auto-fix) - zero deps
- [x] git_reminder.py (Stop: desktop notification) - zero deps
- [x] file_limits.py (SessionEnd: configurable size/count limits)
- [x] context_inject.py (SubagentStart: inject facts + state)
- [x] session_checkpoint.py (SessionEnd: auto-save git state)
- [x] Config: YAML config (project/user/env var), sensible defaults
- [x] CLI: `cervella-hooks setup` genera config + settings.json snippet
- [x] Docs: README with "Create your own hooks" guide + hook event reference
- [x] 227 tests, 98% coverage, 0.12s
- **Criterio:** Hook installabile e configurabile in < 5 min - SODDISFATTO
- **Score:** Guardiana 9.1 -> 9.5/10 (2 round, 4 P2 fixed)

**F2.2 - Agent Definitions come templates** -- DONE (S371)
- [x] Template agents: coordinator, quality-gate, architect, worker
- [x] _SHARED_DNA.md come esempio (senza filosofia personale)
- [x] Frontmatter YAML documentato (name, model, tools, version, role, permissionMode, maxTurns)
- [x] Esempi: team di 3 (minimal), team di 7 (standard), team di 17 (full)
- [x] CLI: `cervella-agent init/init-team/list/validate`
- [x] team.yaml composition format (no competitor has this!)
- [x] Worker specialties: backend, frontend, tester, researcher, devops, docs, generic
- [x] 188 tests, 0.16s
- [x] Research: 18 sources, 5 frameworks compared (CrewAI, AutoGen, LangGraph, Claude Code, OpenAI SDK)
- **Criterio:** Dev crea un agent custom in < 10 min - SODDISFATTO (`cervella-agent init worker --specialty backend`)
- **Score:** Guardiana 9.3 -> 9.5/10 (2 round, 4 P2 fixed)

**F2.3 - Task Orchestration** -- DONE (S372)
- [x] `packages/task-orchestration/` con pyproject.toml (Hatchling, PEP 639, ZERO dependencies!)
- [x] task_classifier.py: rule-based complexity scoring (17 keywords, 4 levels, fast-path)
- [x] architect_flow.py: routing + plan validation + 3-level fallback escalation
- [x] task_manager.py: file-based state machine with atomic race protection (`open(f, 'x')`)
- [x] output_validator.py: reflection pattern scoring 0-100 with retry logic
- [x] cli.py: 6 entry points (cervella-classify/route/validate-plan/validate-output/task/orchestrate)
- [x] 273 tests, 0.13s, zero external dependencies
- [x] Research: 18 sources, 5 frameworks confirmed NO competitor has deterministic task routing
- [x] README killer with comparison table + honest note
- [x] dependabot.yml entry added
- **Criterio:** Pipeline classify -> route -> validate funziona standalone - SODDISFATTO
- **Score:** Guardiana 9.2 -> 9.5/10 (2 round, 4 P2 + 1 P3 fixed)

**F2.4 - Spawn Workers (versione portabile)** DONE S372
- [x] Package `cervellaswarm-spawn-workers` v0.1.0 at `packages/spawn-workers/`
- [x] 5 modules: backend (tmux/nohup auto-detect), team_loader (YAML), spawner (SpawnManager), prompt_builder (10 specialties), cli (cervella-spawn)
- [x] Config-driven spawn from team.yaml (reuses F2.2 schema + `spawn:` section)
- [x] Signal handling (SIGINT/SIGTERM -> kill_all -> cleanup) + atexit
- [x] Cross-invocation status/kill via tracking files (_load_tracked_workers)
- [x] Shell injection safety (shlex.quote)
- [x] 171 tests, 0.13s (all mocked, no real processes)
- [x] README killer with comparison table + honest note
- [x] dependabot.yml entry added
- [x] Research: 18 sources, NO competitor has file-based state + tmux isolation + config-driven spawn
- **Criterio:** Funziona su macOS e Linux (Ubuntu 22.04+) - SODDISFATTO
- **Score:** Guardiana 9.2 -> 9.5/10 (2 round, 4 P2 + 1 P3 fixed)

**Audit Guardiana dopo F2** -> target 9.5/10

---

### FASE 3: SESSION MEMORY SYSTEM (9-13 sessioni, ~54h)

> Il differenziale: nessun competitor ha questo.

**F3.1 - SNCP come pacchetto** DONE (S373, 9.6/10)
- [x] `packages/session-memory/` con SNCP generalizzato (6 moduli, 1.8k LOC)
- [x] Template: session_state.md (PROMPT_RIPRESA), project_compass.md (NORD.md)
- [x] Scripts portati: sncp-init -> project_manager, quality-check -> quality_checker, verify-sync -> sync_checker
- [x] audit-secrets -> secret_auditor (generico, 6 CRITICAL + 3 HIGH patterns, extensible)
- [x] Refactor tutti i paths hardcoded -> config YAML con project registry
- [x] CLI: `cervella-session init my-project` crea struttura completa
- [x] 177 test, 0.13s, Guardiana 9.3 -> 9.6/10 (2 round, 3 P2 fixed)
- [x] Research: 20 sources, Letta Context Repositories (Feb 12 2026) - finestra aperta ORA
- **Criterio:** `cervella-session init my-project` crea struttura completa - SODDISFATTO

**F3.2 - Memory Database**
- [ ] SQLite memory system (init_db, log_event, query_events)
- [ ] Analytics per agente/progetto
- [ ] Lessons learned con confidence scoring
- [ ] Context loader con agent filtering
- **Criterio:** DB si auto-crea, zero config manuale

**F3.3 - Quality Gate Scripts**
- [ ] quality-check.py (generico)
- [ ] verify-hooks.py (generico)
- [ ] sync-agents.sh (generico)
- [ ] Docs: "Keep your swarm healthy"
- **Criterio:** Scripts funzionano su qualsiasi progetto

**F3.4 - Documentazione architetturale**
- [ ] ARCHITECTURE.md (come tutto si connette)
- [ ] GETTING_STARTED.md (from zero to swarm in 30 min)
- [ ] MIGRATION.md (per chi gia usa CrewAI/AutoGen)
- **Criterio:** Dev migra da CrewAI in < 1 ora

**F3.5 - Auto-Handoff Miglioramento** (ricerca S370)
- [ ] Rimuovere logica "apri nuova finestra" dall'auto-handoff
- [ ] PreCompact hook: aggiorna PROMPT_RIPRESA automaticamente prima del compact
- [ ] Configurare `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=85` per threshold ottimale
- [ ] Handoff diventa archivio storico, non trigger per nuova sessione
- **Criterio:** Zero nuove finestre durante sessione, PROMPT_RIPRESA sempre aggiornato
- **Ricerca:** `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260218_auto_handoff_improvements.md`
- **Nota:** Community conferma antipattern (14 fonti). SNCP e autocompact sono complementari.

**Audit Guardiana dopo F3** -> target 9.5/10

---

### FASE 4: LANCIO E CRESCITA (ongoing)

> Go to market!

**F4.1 - Launch pubblico**
- [ ] GitHub repo pubblico (gia esiste sync-to-public.sh)
- [ ] Product Hunt launch
- [ ] Blog post: "How we built a 17-agent AI swarm before it was cool"
- [ ] Video demo (5 min)
- **Criterio:** 100+ stars prima settimana

**F4.2 - Community building**
- [ ] Discord server
- [ ] Contributing guide dettagliata
- [ ] "Good first issue" labels
- [ ] Monthly release cadence
- **Criterio:** 5+ contributors esterni in 3 mesi

**F4.3 - Multi-LLM (futuro)**
- [ ] Adapter pattern per provider LLM
- [ ] Supporto: Claude (nativo), GPT-4, Gemini, local (Ollama)
- [ ] Abstract hook protocol (non solo Claude Code)
- **Criterio:** Stesso swarm funziona con 2+ provider

**F4.4 - CervellaSwarm Cloud (futuro)**
- [ ] Hosted version (freemium)
- [ ] Dashboard web per monitorare agenti
- [ ] Enterprise: SSO, audit logs, multi-tenancy
- **Criterio:** Beta con 10 utenti paganti

---

## METRICHE DI SUCCESSO

| Tempo | Metrica | Target |
|-------|---------|--------|
| 1 mese | GitHub stars | 500+ |
| 1 mese | PyPI downloads/mese | 200+ |
| 3 mesi | Stars + contributors | 1.000+ stars, 10 contributors |
| 3 mesi | Issue response time | < 48h media |
| 6 mesi | Stars + downloads PyPI | 5.000+ stars, 1.000 downloads/mese |
| 6 mesi | Documentation coverage | 90%+ API documentata |
| 12 mesi | Community + revenue | 10.000+ stars, primo enterprise pilot |

---

## RISCHI E MITIGAZIONI

| # | Rischio | Probabilita | Impatto | Mitigazione |
|---|---------|-------------|---------|-------------|
| R1 | Claude Agent SDK aggiunge session memory nativa -> gap #1 scompare | MEDIA | ALTO | Differenziarsi su trasparenza (plaintext, git-native, auditabile). SNCP e piu di memory -- e compliance-ready |
| R2 | Bus factor = 1 (solo Rafa) | ALTA | ALTO | Community building ASAP (FASE 4.2). Documentazione eccellente riduce dipendenza. Contributor onboarding prioritario |
| R3 | Lock-in perceptivo "solo Claude" | MEDIA | MEDIO | Comunicazione chiara: "Claude-first, not Claude-only". Adapter pattern in roadmap (F4.3). AST Pipeline gia e LLM-agnostico |
| R4 | Git history leak di dati personali | BASSA | ALTO | git-filter-repo assessed NOT NEEDED (S367): orphaned clean history. Sync script content scanning prevents leaks at push time. Repo pubblico fresh (non fork del privato) |
| R5 | Giganti copiano (Anthropic, Microsoft) | BASSA | ALTO | Speed-to-market + community loyalty. Precedente OpenClaw: community value > corporate copy |
| R6 | Complessita tecnica spaventa nuovi utenti | MEDIA | MEDIO | DX killer: quickstart in 5 min, tutorial video, esempi minimal (3 agenti). Progressive disclosure |

---

## COSA NON PUBBLICARE (MAI)

- `.sncp/progetti/` (dati sessione personali)
- `.sncp/handoff/` (handoff con dati personali)
- `.swarm/` (handoff, tasks, research con dati personali)
- NORD.md con dati reali dei progetti
- PROMPT_RIPRESA con stato attuale
- Ricerche personali (RESEARCH_*, RICERCA_*)
- Riferimenti a: CervellaBrasil, Chavefy, Contabilita, Miracollo
- API keys, tokens, dati clienti
- `logs/`, `data/` (eventi reali)
- `scripts/cron/` (contiene paths /Users/rafapra/ hardcoded)
- `scripts/start-session.sh` (config personale con nomi progetto)
- `.mcp.json` (potenziali API keys)
- `docs/studio/` (analisi interne)
- `cervellaswarm-extension/` (VS Code extension con config personale)
- Qualsiasi file con dati del figlio (MEI, debiti, PIR)

---

## DIPENDENZE

```
FASE 0 ──> FASE 1 ──> FASE 2 ──> FASE 3 ──> FASE 4
(prep)     (AST)      (agents)   (memory)   (launch)
                                     │
                                     └──> F4.3 Multi-LLM
                                     └──> F4.4 Cloud
```

**Ogni fase e indipendente dopo F0.** F1 puo essere lanciata prima di F2/F3.

---

## PACKAGES ESISTENTI (TypeScript)

Il repo ha gia 4 pacchetti TypeScript in `packages/`:
- `@cervellaswarm/core` - Core library
- `@cervellaswarm/cli` - CLI tool
- `@cervellaswarm/mcp-server` - MCP server
- `@cervellaswarm/api` - API client

**Decisione necessaria in F0.1:** Questi pacchetti sono complementari ai nuovi Python packages.
I nuovi pacchetti Python vanno in `packages/` accanto ai TS, con naming coerente.
Prefix PyPI: `cervellaswarm-` (es: `cervellaswarm-code-intelligence`).
Prefix npm: `@cervellaswarm/` (gia in uso).

---

## NOTE

- **Sessione di riferimento:** S362 (16 Feb 2026)
- **Ricerche base:** Scienziata (landscape), Ingegnera (audit tecnico), Researcher (autocompact)
- **Pattern audit:** Guardiana Qualita dopo ogni fase -> target 9.5/10
- **Stima sessioni:** 4-6h/sessione (dato Researcher), totale ~134h, ~25-33 sessioni
- **Lingua docs:** Inglese (target internazionale)
- **Lingua interna:** Italiano/Portoghese (come sempre)
- **Licenza:** Apache 2.0 (decisione Regina S362: protezione brevetti + gia in package.json + enterprise-friendly)

---

*"Ultrapassar os proprios limites!" - Rafa & Cervella, S362*
