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
| 1.7 | **PyPI v0.3.3 publish** | 15 min | TODO -- sync + tag + push public |

**Criterio completamento Sprint 1:**
- [x] 20/20 stdlib formatted canonically
- [x] VS Code `lu` extension: Format Document works (textDocument/formatting)
- [x] VS Code `lu` extension: diagnostics show lint findings (source: lu-lint)
- [  ] PyPI v0.3.3 LIVE con lu lint + lu fmt

---

### SPRINT 2: Quality & Testing (1 sessione)

| # | Task | Effort | Cosa |
|---|------|--------|------|
| 2.1 | **lu fmt examples** | 10 min | Format example .lu files. |
| 2.2 | **Pre-commit hook** | 30 min | `lu fmt --check .` + `lu lint .` in pre-commit. |
| 2.3 | **CI integration** | 30 min | Add `lu fmt --check` + `lu lint` to CI workflow. |
| 2.4 | **Multi-file support** | 45 min | `lu fmt .` formats all .lu in directory (glob). |
| 2.5 | **Multi-file lint** | 30 min | `lu lint .` lints all .lu in directory. |
| 2.6 | **Guardiana audit** | 15 min | Full audit. |

**Criterio completamento Sprint 2:**
- [  ] CI checks lu fmt + lu lint
- [  ] `lu fmt .` and `lu lint .` work on directories
- [  ] Pre-commit hook prevents unformatted commits

---

### SPRINT 3: Community Prep (1 sessione)

| # | Task | Effort | Cosa |
|---|------|--------|------|
| 3.1 | **README update** | 30 min | Add lu lint + lu fmt sections, update numbers. |
| 3.2 | **Blog post update** | 30 min | Add lu lint/fmt to "From Vibe Coding to Vericoding". |
| 3.3 | **Playground update** | 1h | Add lint tab to online playground. |
| 3.4 | **Show HN v2 draft** | 30 min | New post with nested choice + lint + fmt. |

**Criterio completamento Sprint 3:**
- [  ] README reflects 3641+ test, 12 CLI
- [  ] Blog post includes lu lint + lu fmt story
- [  ] Playground has lint functionality

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
