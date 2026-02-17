# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-17 - Sessione 363
> **STATUS:** FASE 0 OPEN SOURCE - Sicurezza repo completata, 3 audit Guardiana (8.8 -> 9.3/10)

---

## SESSIONE 363 - FASE 0 OPEN SOURCE (sicurezza + docs + infra)

### Contesto
Prima sessione operativa di FASE 0 (preparazione repo per open source). Rafa: "attenzione per non toccare nulla che possa fare qualcosa per noi" - La Famiglia continua localmente come sempre.

### Cosa abbiamo fatto

**1. Audit completo (Ingegnera + Security in parallelo):**
- Ingegnera: 848 occorrenze path personali in 342 file (mappatura completa)
- Security: Score 4/10 privato, 8/10 pubblico. 21 finding. Report: `.sncp/progetti/cervellaswarm/reports/SECURITY_20260217.md`
- packages/ PULITO: zero dati personali (confermato da entrambi)

**2. .gitignore hardening (1006 file untracked, zero impatto locale):**
- Aggiunti: `.swarm/`, `data/`, `logs/`, `reports/`, `.mcp.json`, `.vscode/`, `config/claude-hooks/`, `cervellaswarm-extension/`, `RESEARCH_*.md`, `RICERCA_*.md`, `PASSAGGIO_CONSEGNA_*.txt`, `*.db`, `*.sqlite`
- `git rm --cached` su 1006 file (restano su disco, zero impatto La Famiglia)

**3. sync-to-public.sh v3.0 (content scanning):**
- Check 5 NUOVO: scansione contenuto file per 14 pattern sensibili
- Pattern: `/Users/rafapra`, `rafapra3008`, `~/Developer/`, `@gmail.com`, `192.168.`, tutti i nomi progetti privati
- Blacklist espansa: +5 root paths, +5 filename patterns, +1 dir
- `--dry-run` aggiunto

**4. Community files:**
- CODE_OF_CONDUCT.md (Contributor Covenant 2.1)
- SECURITY.md (responsible disclosure, cervellaswarm@pm.me)
- LICENSE, CONTRIBUTING.md, NOTICE gia esistenti e OK

**5. Fix sicurezza:**
- `.claude/settings.json`: path hardcoded -> `$CLAUDE_PROJECT_DIR`
- `docs/SEMANTIC_SEARCH.md`: 14 path personali sanitizzati
- `docs/GETTING_STARTED.md`: 2 path personali sanitizzati
- `docs/DUAL_REPO_STRATEGY.md`: whitelist docs aggiornata (+3 file)

**6. Audit Guardiana (3 round):**
- Round 1 (.gitignore): 8.8/10 (3 P2: data/retro, .vscode, settings hardcoded)
- Fix P2 -> tutte risolte
- Round 2 (finale): **9.3/10** (2 P2 self-blocking docs, 5 P3)
- P2 self-blocking risolti (SEMANTIC_SEARCH + GETTING_STARTED sanitizzati)

### Decisioni S363

| Decisione | Perche |
|-----------|--------|
| Whitelist approach (non ristrutturare repo) | La Famiglia resta identica, zero rischio |
| Content scanning nel sync | Defense-in-depth, cattura leak anche se whitelist sbaglia |
| git rm --cached (non delete) | File restano su disco, solo rimossi da tracking |
| .gitignore copre runtime data | data/, logs/, reports/ = operativi, non codice |

---

## S362 (archivio recente)
Brainstorm open source. 3 ricerche parallele (Scienziata/Ingegnera/Researcher). Subroadmap 5 fasi creata. 3 gap unici confermati (SNCP, Orchestrazione gerarchica, Hook system). Audit 8.4 -> 9.5/10.

---

## PROSSIMI STEP
- **F0 continua:** Sanitizzare 29 scripts con path hardcoded (Ingegnera ha mappato 848 occorrenze)
- **F0.4:** README.md killer per repo pubblico (hero section, examples, badges)
- **F0.5:** .github/ templates (issue, PR, CI/CD base)
- **F0.6:** Content scanner esteso (aggiungere *.html, *.css, *.txt per completezza)
- **F1:** AST Pipeline come primo pip package (dopo F0 completata)

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
| S356 | Studio SNCP 4.0 (3 esperte) + Clear Context (parcheggiato) |
| S357 | SNCP 4.0 IMPLEMENTATO! 6 file archiviati, 12+ puntatori fixati |
| S358 | AUDIT TOTALE! 13 agenti sync, 25 test fix, 4 hook fix, 8 docs fix |
| S359 | PULIZIA CHIRURGICA! 4 hook disabled, 2 test split, sync-agents.sh |
| S360 | POLISH + CODE REVIEW! 5 step, sync hook, logging, dry-run |
| S361 | REGOLA ANTI-DOWNGRADE! Policy modelli in 3 file, 3 audit Guardiana |
| S362 | OPEN SOURCE STRATEGY! 3 ricerche, subroadmap, 2 audit (9.5/10) |
| S363 | FASE 0 OPEN SOURCE! .gitignore hardening, sync v3.0, content scanning, 3 audit (9.3/10) |

---

*"Ultrapassar os proprios limites!" - Rafa & Cervella, S362*
