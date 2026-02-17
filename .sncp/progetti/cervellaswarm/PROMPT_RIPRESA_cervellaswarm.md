# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-17 - Sessione 366
> **STATUS:** FASE 0 OPEN SOURCE - F0.4 + F0.5 DONE

---

## SESSIONE 366 - F0.4 README Killer

### Contesto
Prossimo step della subroadmap open source: creare un README.md "killer" per il repo pubblico. Metodo: ricerca competitor + best practices -> scrittura -> audit Guardiana iterativo.

### Cosa abbiamo fatto

**1. Ricerca (2 researcher in parallelo):**
- Competitor README analysis (AutoGen 5/10, CrewAI 7.5/10, LangGraph 8/10)
- Best practices README killer 2026 (12 fonti: FOSDEM, awesome-readme, Daytona, etc.)
- Gap trovato: NESSUN competitor ha GIF demo, comparison table, o session continuity claim
- Reports salvati in `.sncp/progetti/cervellaswarm/reports/`

**2. README.md scritto (239 righe):**
- Tagline: "Build AI agent teams that remember."
- Hero: ASCII flow diagram (no immagine - vedi F1 sotto)
- Struttura: Problem -> Solution -> Quick Start -> Team -> Features -> Comparison -> Docs -> Battle-tested
- Comparison table onesta (ammette: competitors hanno ecosistema piu grande + multi-LLM)
- "Honest note" che costruisce fiducia
- Quick Start: clone from source (npm package non ancora pubblicato)
- Social proof: "365+ sessions", "1,032 tests (95% coverage)", "17 agents"

**3. Audit Guardiana (2 round):**
- Round 1: **8.3/10** - 2 P1 + 5 P2 trovati
- Round 2: **9.5/10** - tutti risolti + 1 nuovo P2 fixato

**Fix applicati:**
| Fix | Cosa | Perche |
|-----|------|--------|
| F1 (P1) | Hero image rimossa | `cli_workflow_en.png` conteneva "CONSTITUTION" e "[REGINA]" (termini interni) |
| F2 (P1) | GitHub URL fixato | Da `CervellaSwarm` a `cervellaswarm` (repo pubblico lowercase) |
| F3 (P2) | Go/Rust rimosso | treesitter_parser.py supporta solo .py/.ts/.js - claim era falso |
| F4 (P2) | Quick Start da source | npm package non pubblicato ancora, git clone + npm link |
| F5 (P2) | Opus/Sonnet precisato | "Guardians and critical analysts on Opus, most Workers on Sonnet" |
| F6 (P2) | Roadmap link rimosso | CHANGELOG != roadmap, cambiato in "planned" |
| F7 (P2) | "4 projects" genericizzato | Numeri specifici invitano domande senza risposta |
| N1 (P2) | "8 months" corretto | Era ~3 mesi, cambiato in "since December 2025" |

### Decisioni S366

| Decisione | Perche |
|-----------|--------|
| No hero image (per ora) | Entrambe le immagini (cli_workflow_en.png, collaboration_flow.png) hanno dati interni. ASCII diagram pulito per ora |
| Clone from source nel Quick Start | npm package non pubblicato. Onesta > aspettativa falsa |
| Tagline "that remember" (non "that check") | Session memory e il gap #1, quality gates e il gap #2. Scelto il differenziale piu forte |
| Comparison table con "Honest note" | Best practice: ammettere limiti costruisce fiducia (ricerca 2026 conferma) |

### P3 residui (non bloccanti, per sessioni future)
- N2: CHANGELOG.md riga 88 dice "5 languages (Go, Rust)" - da allineare
- N3: package.json URLs usano `CervellaSwarm` capitalized (GitHub case-insensitive, funzionale)
- N4: `cervellaswarm.com` non esiste (referenziato in CLI help)
- N5: Line counts (56,800/16,600) diventeranno stale
- Badges test/coverage sono statici (da rendere dinamici con CI in F0.5)
- Hero image da ricreare pulita (nessun riferimento interno)
- Doppia tagline: "that remember" + "17 brains are better than one" (footer)

## F0.5 - .github/ Templates (stessa sessione S366)

### Cosa abbiamo fatto

**1. Ricerca (14 fonti):** GitHub Docs ufficiali, CrewAI/LangGraph/Fiber .github/ live, Codecov docs

**2. 8 nuovi file creati:**
- `ISSUE_TEMPLATE/config.yml` - disabilita blank issues, link discussions
- `ISSUE_TEMPLATE/bug_report.yml` - YAML form, 7 campi (6 required), dropdown OS/version
- `ISSUE_TEMPLATE/feature_request.yml` - YAML form, "Problem Statement first", contribution willingness
- `PULL_REQUEST_TEMPLATE.md` - summary + type + test plan + checklist
- `dependabot.yml` - 7 entry (3 npm packages + 2 pip + github-actions), grouped minor/patch
- `CODEOWNERS` - @rafapra3008 default owner
- `FUNDING.yml` - GitHub Sponsors
- `workflows/stale.yml` - 60+7 days, exempt labels

**3. Sanitizzazione 5 file ESISTENTI:**
- `.github/CLAUDE.md` - riscritto completamente in inglese (rimossa "Filosofia", "famiglia digitale")
- `workflows/weekly-maintenance.yml` - tradotto in inglese (rimosso "Cervella-Ingegnera")
- `workflows/publish.yml` - rimosso "Rafa", motto italiano, URL fixato lowercase
- `workflows/claude-review.yml` - checkout@v5->v4, commenti inglese
- `workflows/ci.yml` + `test-python.yml` - commenti italiani -> inglese

**4. Fix bonus:**
- `cervella/pyproject.toml` - MIT -> Apache-2.0 (license + classifier), description inglese, author genericizzato

**5. Audit Guardiana (2 round):**
- Round 1: **9.0/10** - 0 P1, 4 P2 trovati
- Round 2: **9.3/10** - tutti P2 risolti, 1 nuovo P2 fixato (license classifier)

### P3 residui F0.5
- Duplicate publish workflows (npm-publish.yml + publish.yml) - consolidare in futuro
- 3 commenti italiani in cervella/pyproject.toml (markers, threshold)

---

## S365 (archivio recente)
Model Update Sonnet 4.6 + Opus 4.6: 18 file aggiornati, backward compat, 3 audit Guardiana (9.3/10), 1032 test PASS. 1M context research PARCHEGGIATO.

## S364 (archivio recente)
FASE 0 F0.3: 25+ script sanitizzati, content scanner v3.1, 3 audit Guardiana (7.8 -> 8.8 -> 9.5/10).

---

## PROSSIMI STEP
- **F0.6:** Content scanner esteso (*.html, *.css, *.txt) + git-filter-repo
- **Hero image:** Creare immagine/GIF pulita senza riferimenti interni
- **Badge dinamici:** Codecov integration per badge CI reali
- **F1:** AST Pipeline come primo pip package
- **F3 nota:** MCP SNCP KNOWN_PROJECTS hardcoded -> rendere configurabile

---

## ARCHIVIO

| Sessione | Cosa |
|----------|------|
| S337-S348 | Coverage push 41% -> 95% (968 test) |
| S349 | Audit reale + Pulizia + MAPPA MIGLIORAMENTI |
| S350-S352 | MAPPA MIGLIORAMENTI A+B+C+D completata |
| S353-S354 | CervellaBrasil + Chavefy nasceu! |
| S355-S356 | SubagentStart Context Injection + Studio SNCP 4.0 |
| S357-S360 | SNCP 4.0 + AUDIT TOTALE + PULIZIA + POLISH |
| S361 | REGOLA ANTI-DOWNGRADE modelli in 3 file |
| S362 | OPEN SOURCE STRATEGY! 3 ricerche, subroadmap (9.5/10) |
| S363 | FASE 0: .gitignore, sync v3.0, content scanning (9.3/10) |
| S364 | FASE 0 F0.3: script sanitization, content scanner v3.1 (9.5/10) |
| S365 | Model Update Sonnet 4.6 + Opus 4.6, 18 file (9.3/10) |
| S366 | F0.4 README killer (9.5/10) + F0.5 .github/ templates (9.3/10) |

---

*"Ultrapassar os proprios limites!" - Rafa & Cervella, S366*
