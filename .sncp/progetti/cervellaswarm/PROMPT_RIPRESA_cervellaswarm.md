# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-17 - Sessione 365
> **STATUS:** FASE 0 OPEN SOURCE - F0.3 DONE + Model Update Sonnet 4.6/Opus 4.6 COMPLETATO

---

## SESSIONE 365 - Model Update Sonnet 4.6 + Opus 4.6

### Contesto
Anthropic ha rilasciato Sonnet 4.6 (17 Feb 2026). Stesso prezzo di Sonnet 4.5, ma "Opus-level" coding, adaptive thinking, training data Jan 2026. Rafa: aggiorniamo la famiglia!

### Cosa abbiamo fatto

**1. Ricerca Sonnet 4.6:**
- API ID: `claude-sonnet-4-6` (+ `claude-opus-4-6`)
- $3/$15 MTok (stesso prezzo), 200K context (1M beta)
- Adaptive thinking NUOVO (Sonnet 4.5 non lo aveva)
- OSWorld: 72.5% vs 61.4% (+11pp)
- Training data: Jan 2026 vs Jul 2025 (+6 mesi)

**2. Aggiornamento packages JS/TS (8 file):**
- `packages/core/src/config/types.ts` - ClaudeModel union + VALID_MODELS
- `packages/core/src/config/schema.ts` - enum + default `claude-sonnet-4-6`
- `packages/mcp-server/src/config/manager.ts` - enum + default + API test call
- `packages/cli/src/config/schema.js` - enum + default
- `packages/cli/src/config/settings.js` - validModels array
- `packages/cli/src/config/diagnostics.js` - API test call
- `packages/core/test/config.test.js` - 4 assert aggiornati
- `packages/cli/README.md` - esempio model

**3. Aggiornamento Python + scripts + docs (10 file):**
- `cervella/api/client.py` - DEFAULT_MODEL + OPUS_MODEL
- `.github/workflows/weekly-maintenance.yml` - --model flag
- `scripts/utils/worker_attribution.json` - tutti model + v1.2.0
- `scripts/convert_agents_to_agent_hq.py` - MODEL_MAPPING + fallback
- `scripts/utils/git_worker_commit.sh` - 3 fallback
- `docs/GIT_ATTRIBUTION.md` - attribution examples
- `docs/roadmap/SUB_ROADMAP_QUICKWINS.md` - YAML example
- `tests/tools/test_convert_agents.py` - 3 assert fixati
- `tests/tools/TEST_REPORT_convert_agents.md` - doc model

**4. Strategia backward compatibility:**
- Nuovi modelli AGGIUNTI, non sostituiti
- Vecchi model ID restano nel enum (`claude-sonnet-4-20250514`, `claude-opus-4-5-20251101`)
- Utenti con config esistente non si rompono

**5. Audit Guardiana (3 round):**
- Round 1: **9.3/10** (P2: Python client, P3: workflow + attribution + docs)
- Round 2: **9.0/10** (P1: test stale in convert_agents trovati)
- Round 3: **9.3/10** (P2: fallback stale in convert_agents + git_worker_commit)
- Tutti fix applicati -> score atteso 9.5+

**6. Test TUTTI VERDI:**
- 1032/1032 Python fast suite PASS
- 17/17 core config + 20/20 workers + 30/30 convert_agents PASS
- TypeScript build OK (core + mcp-server, zero errori)

### Decisioni S365

| Decisione | Perche |
|-----------|--------|
| Backward compat (vecchi ID nel enum) | Utenti con config salvata non si rompono |
| Default cambiato a sonnet-4-6 | Nuovo modello e meglio a stesso prezzo |
| Agent files NON modificati | Usano `model: sonnet` (alias) - Claude Code risolve automaticamente |
| Worker attribution aggiornata | Commit signatures devono riflettere il modello reale |

### Stato agenti famiglia

- 10 Worker Sonnet: `model: sonnet` nel frontmatter -> auto-risolto a Sonnet 4.6 da Claude Code
- 7 Opus: `model: opus` -> auto-risolto a Opus 4.6
- Nessun cambio nei file agente necessario

---

## S364 (archivio recente)
FASE 0 F0.3: 25+ script sanitizzati, content scanner v3.1, 3 audit Guardiana (7.8 -> 8.8 -> 9.5/10).

## S363 (archivio recente)
.gitignore hardening, sync-to-public.sh v3.0 (content scanning), community files, docs sanitizzati. 3 audit (9.3/10).

---

## PROSSIMI STEP
- **F0.4:** README.md killer per repo pubblico (hero section, examples, badges)
- **F0.5:** .github/ templates (issue, PR, CI/CD base)
- **F0.6:** Content scanner esteso (*.html, *.css, *.txt)
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

---

*"Ultrapassar os proprios limites!" - Rafa & Cervella, S365*
