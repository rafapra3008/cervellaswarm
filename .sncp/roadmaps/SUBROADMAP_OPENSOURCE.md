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

**F1.1 - Estrarre AST Pipeline come pacchetto standalone**
- [ ] `packages/code-intelligence/` con pyproject.toml
- [ ] Files: treesitter_parser, symbol_extractor, python_extractor, typescript_extractor
- [ ] Files: symbol_cache, symbol_types, language_builtins
- [ ] Files: dependency_graph, semantic_search, impact_analyzer, repo_mapper
- [ ] CLI entry points: `cervella-search`, `cervella-impact`, `cervella-map`
- **Criterio:** `pip install cervella-code-intelligence` funziona

**F1.2 - Test suite standalone**
- [ ] Copiare/adattare 400+ test esistenti (AST pipeline)
- [ ] CI con GitHub Actions (Python 3.10, 3.11, 3.12)
- [ ] Coverage badge (target: 90%+)
- **Criterio:** `pytest` passa su macOS + Linux

**F1.3 - Documentazione pacchetto**
- [ ] README con esempi pratici
- [ ] API reference auto-generata
- [ ] Tutorial: "Analyze your codebase in 5 minutes"
- **Criterio:** Un dev usa il pacchetto senza leggere il codice

**F1.4 - Pubblicazione**
- [ ] PyPI: `cervella-code-intelligence`
- [ ] GitHub release con changelog
- [ ] Post su Reddit r/ClaudeAI, r/Python, Twitter/X
- **Criterio:** Installabile via pip, 0 errori

**Audit Guardiana dopo F1** -> target 9.5/10

---

### FASE 2: AGENT FRAMEWORK (8-12 sessioni, ~50h)

> Il cuore: definizioni di agenti, hooks, task orchestration.

**F2.1 - Hook System pubblicabile**
- [ ] `packages/agent-hooks/` con hooks generici
- [ ] bash_validator.py (gia 100% generico)
- [ ] Template per: context_inject, file_limits, session_end
- [ ] Docs: "Create your own hooks"
- **Criterio:** Hook installabile e configurabile in < 5 min

**F2.2 - Agent Definitions come templates**
- [ ] Template agents: coordinator, quality-gate, architect, worker
- [ ] _SHARED_DNA.md come esempio (senza filosofia personale)
- [ ] Frontmatter YAML documentato (name, model, tools, version)
- [ ] Esempi: team di 3 (minimal), team di 7 (standard), team di 17 (full)
- **Criterio:** Dev crea un agent custom in < 10 min

**F2.3 - Task Orchestration**
- [ ] task_classifier.py (zero dati personali)
- [ ] architect_flow.py (zero dati personali)
- [ ] task_manager.py (zero dati personali)
- [ ] output_validator.py (zero dati personali)
- [ ] Docs: "Automatic task routing"
- **Criterio:** Pipeline classify -> route -> validate funziona standalone

**F2.4 - Spawn Workers (versione portabile)**
- [ ] spawn-workers.sh adattato per config-driven (no paths hardcoded)
- [ ] Supporto: macOS (Terminal.app + tmux) + Linux (tmux)
- [ ] Docs: "Launch parallel agent sessions"
- **Criterio:** Funziona su macOS e Linux (Ubuntu 22.04+)

**Audit Guardiana dopo F2** -> target 9.5/10

---

### FASE 3: SESSION MEMORY SYSTEM (9-13 sessioni, ~54h)

> Il differenziale: nessun competitor ha questo.

**F3.1 - SNCP come pacchetto**
- [ ] `packages/session-memory/` con SNCP generalizzato
- [ ] Template: PROMPT_RIPRESA, NORD.md
- [ ] Scripts: sncp-init, quality-check, verify-sync
- [ ] audit-secrets (generico, non legato ai nostri progetti)
- [ ] Refactor tutti i paths hardcoded -> config file
- **Criterio:** `cervella-sncp init my-project` crea struttura completa

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
