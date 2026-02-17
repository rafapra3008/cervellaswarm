# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-17 - Sessione 364
> **STATUS:** FASE 0 OPEN SOURCE - F0.3 sanitizzazione scripts COMPLETATA, 3 audit Guardiana (7.8 -> 8.8 -> 9.5/10)

---

## SESSIONE 364 - FASE 0 OPEN SOURCE (sanitizzazione scripts)

### Contesto
Seconda sessione operativa di FASE 0. Rafa: "facciamo tutto come abbiamo pianificato, un punto alla volta, con calma." Strategia Guardiana: audit dopo ogni step, target 9.5/10.

### Cosa abbiamo fatto

**1. Mappatura completa (Ingegnera + grep):**
- 26 file .sh con `/Users/rafapra` hardcoded
- 8 file .md/.cron/.plist con path personali in docs
- 1 file .py (convert_agents) con Path() hardcoded

**2. Sanitizzazione scripts/sncp/ (12 file):**
- Pattern: `SCRIPT_DIR -> REPO_ROOT -> ${VAR:-$REPO_ROOT/relative}`
- sncp-init.sh, verify-sync.sh, pre-session-check.sh, health-check.sh, consolidate-ripresa.sh, expand-daily.sh, load-daily-memory.sh, compact-state.sh.DISABLED, post-session-update.sh.DISABLED, compliance-check.sh, auto-summary.sh, memory-persist.sh

**3. Sanitizzazione scripts/cron/ (4 file):**
- weekly_retro_cron.sh, log_rotate_cron.sh, sncp_daily_maintenance.sh, sncp_weekly_archive.sh
- Pattern: `SCRIPT_DIR -> SWARM_DIR`

**4. Sanitizzazione scripts restanti (7 file):**
- start-session.sh: SNCP_ROOT + get_project_path() con DEVELOPER_ROOT
- update-roadmap.sh: PROGETTI con DEVELOPER_ROOT
- swarm-report.sh, task-new.sh, swarm-session-check.sh, swarm-roadmaps.sh, swarm-helper.sh
- convert_agents_to_agent_hq.py: `Path(__file__).resolve()` al posto di hardcoded

**5. Sanitizzazione docs (8 file):**
- README.md, .cron, .plist.example in scripts/cron/, scripts/swarm/, scripts/learning/, scripts/engineer/

**6. Content scanner v3.1 (sync-to-public.sh):**
- Aggiunto `$HOME/Developer` ai content patterns
- Rimosso `rafapra3008` (username GitHub PUBBLICO, non sensibile)
- Rimosso `contabilita` (parola generica, "ContabilitaAntigravity" gia copre)
- Cambiato `cervellacostruzione` -> `progetti/cervellacostruzione` (evita self-blocking su codice MCP)
- Commenti esplicativi aggiunti per ogni scelta

**7. Audit Guardiana (3 round):**
- Round 1: **7.8/10** (3 sncp/ mancati, 5 swarm/, update-roadmap, scanner gap)
- Round 2: **8.8/10** (tutti P1/P2 fixati, scoperto self-blocking rafapra3008)
- Round 3: **9.5/10** (self-blocking fixato, pattern scanner ottimizzati)

### Decisioni S364

| Decisione | Perche |
|-----------|--------|
| Pattern SCRIPT_DIR uniforme | Portabilita: funziona ovunque, non solo su macchina Rafa |
| DEVELOPER_ROOT env variable | Multi-utente: `export DEVELOPER_ROOT=/my/path` sovrascrive |
| rafapra3008 NON in blacklist | E username GitHub PUBBLICO, URL del repo. @gmail.com copre email |
| contabilita NON in blacklist | Parola italiana generica (=accounting). "ContabilitaAntigravity" copre il repo |
| cervellacostruzione -> path-specific | `"progetti/cervellacostruzione"` cattura SNCP paths ma non array in codice MCP |
| P3 cosmetic accettati | Commenti crontab, ~/Developer in echo/help = zero rischio |

### Stato residuo

| Cosa | Status | Quando |
|------|--------|--------|
| P3: commenti crontab con $HOME/Developer | ACCETTATO | Non in whitelist pubblica |
| P3: ~/Developer in echo/help ~13 script | ACCETTATO | Non in whitelist pubblica |
| MCP KNOWN_PROJECTS hardcoded | TODO F3 | Rendere configurabile prima di F3 |

---

## S363 (archivio recente)
.gitignore hardening (1006 file untracked), sync-to-public.sh v3.0 (content scanning con 14 pattern), community files, docs sanitizzati. 3 audit Guardiana (8.8 -> 9.3/10).

## S362 (archivio recente)
Brainstorm open source. 3 ricerche parallele (Scienziata/Ingegnera/Researcher). Subroadmap 5 fasi creata. 3 gap unici confermati.

---

## PROSSIMI STEP
- **F0.4:** README.md killer per repo pubblico (hero section, examples, badges)
- **F0.5:** .github/ templates (issue, PR, CI/CD base)
- **F0.6:** Content scanner esteso (aggiungere *.html, *.css, *.txt per completezza)
- **F1:** AST Pipeline come primo pip package (dopo F0 completata)
- **F3 nota:** MCP SNCP code ha KNOWN_PROJECTS hardcoded -> rendere configurabile

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
| S361 | REGOLA ANTI-DOWNGRADE! Policy modelli in 3 file |
| S362 | OPEN SOURCE STRATEGY! 3 ricerche, subroadmap, 2 audit (9.5/10) |
| S363 | FASE 0 OPEN SOURCE! .gitignore, sync v3.0, content scanning (9.3/10) |

---

*"Ultrapassar os proprios limites!" - Rafa & Cervella, S362*
