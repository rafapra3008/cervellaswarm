# SUBROADMAP - S449+ Polish & Ship

> **Creata:** 13 Marzo 2026 - Sessione 448 (planning)
> **Autrice:** Cervella Regina (CEO)
> **Prerequisiti:** S448 completa (lu lint + lu fmt + security cleanup)
> **Score target:** 9.5/10 per ogni step
> **Filosofia:** "Con calma, ma sempre ben fatto!"

---

## DOVE SIAMO

```
+================================================================+
|   S448 COMPLETATA:                                              |
|     lu lint: 10 rules, 73 tests          DONE                  |
|     lu fmt: zero-config, 74 tests        DONE                  |
|     Security: 0 npm vulns, zod 4         DONE                  |
|     PyPI v0.3.2: LIVE                    DONE                  |
|                                                                |
|   ASSET: 29 moduli, 3641 test, 12 CLI, ZERO deps core         |
|                                                                |
|   BLOCCATO: T3.5 VS Code (serve Rafa publisher account)        |
|   HOLD: stripe 17->20, express 4->5 (major, sessione dedicata) |
+================================================================+
```

---

## TASK LIST (priorita decrescente)

### SPRINT 1: Dogfood & Polish (1 sessione)

| # | Task | Effort | Stato |
|---|------|--------|-------|
| 1.1 | **lu fmt stdlib** | 15 min | DONE (S449) |
| 1.2 | **LSP format integration** | 30 min | DONE (S449) |
| 1.3 | **LSP lint integration** | 30 min | DONE (S449) |
| 1.4 | **Guardiana audit LSP** | 15 min | DONE (9.3→9.5, 8 findings fixed) |
| 1.5 | **CHANGELOG v0.3.3** | 15 min | DONE (S449) |
| 1.6 | **Version bump 0.3.3** | 5 min | DONE (S449) |
| 1.7 | **PyPI v0.3.3 publish** | 15 min | DONE (S449) |

**Criterio completamento Sprint 1:**
- [x] 20/20 stdlib formatted canonically
- [x] VS Code `lu` extension: Format Document works (textDocument/formatting)
- [x] VS Code `lu` extension: diagnostics show lint findings (source: lu-lint)
- [x] PyPI v0.3.3 LIVE con lu lint + lu fmt

---

### SPRINT 2: Quality & Testing (1 sessione)

| # | Task | Effort | Cosa |
|---|------|--------|------|
| 2.1 | **lu fmt examples** | 10 min | DONE (S449) |
| 2.2 | **Pre-commit hook** | 30 min | DONE (S449) -- section 5 in scripts/hooks/pre-commit |
| 2.3 | **CI integration** | 30 min | DONE (S449) -- lint-format job + multi-path nargs="+" |
| 2.4 | **Multi-file support** | 45 min | DONE (S449) |
| 2.5 | **Multi-file lint** | 30 min | DONE (S449) |
| 2.6 | **Guardiana audit** | 15 min | DONE (9.3→9.5, all P2 fixed: dedup + ricette.lu, 3684 test) |

**Criterio completamento Sprint 2:**
- [x] CI checks lu fmt + lu lint (lint-format job before test matrix)
- [x] `lu fmt .` and `lu lint .` work on directories (+ multi-path)
- [x] Pre-commit hook prevents unformatted commits

---

### SPRINT 3: Community Prep (1 sessione)

| # | Task | Effort | Cosa |
|---|------|--------|------|
| 3.1 | **README update** | 30 min | DONE (S449) -- 3684 test, 12 CLI, lu lint/fmt docs, .lu syntax |
| 3.2 | **Blog post update** | 30 min | DONE (S449) -- 3684 test, lu lint/fmt story, v0.3.3 |
| 3.3 | **Playground update** | 1h | DONE (S450) -- Lint button + lint_source/format_source public API, Guardiana 9.5/10 |
| 3.4 | **Show HN v2 draft** | 30 min | DONE (S449) -- docs/SHOW_HN_V2_DRAFT.md |

**Criterio completamento Sprint 3:**
- [x] README reflects 3684 test, 12 CLI
- [x] Blog post includes lu lint + lu fmt story
- [x] Playground has lint functionality (Lint button + Ctrl+Shift+L, Guardiana 9.5/10)
- [x] Show HN v2 draft ready for Rafa review

---

### HOLD (blocco esterno)

| Task | Blocco | Quando |
|------|--------|--------|
| T3.5 VS Code Marketplace | Rafa publisher account | Quando Rafa crea |
| Stripe 17->20 | Major upgrade, testing needed | Sessione dedicata |
| Express 4->5 | Major upgrade, breaking changes | Sessione dedicata |

---

## DECISIONE: PERCHE QUESTO ORDINE

1. **Sprint 1 (Dogfood):** Usiamo i nostri strumenti. Se lu fmt non funziona sulla stdlib, nessuno lo usera. LSP integration = esperienza VS Code immediata. PyPI = il mondo ne beneficia.

2. **Sprint 2 (Quality):** CI enforcement assicura che nessuno rompa lo stile. Multi-file = usabilita reale. Pre-commit = zero sorprese.

3. **Sprint 3 (Community):** Solo DOPO che gli strumenti funzionano e CI li protegge, comunichiamo. Nessuno vuole leggere di un formatter che non funziona.

---

*"Con calma, chiaro e precisi. Ogni punto alla volta."*
