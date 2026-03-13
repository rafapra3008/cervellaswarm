# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-03-13 - Sessione 448
> **STATUS:** lu lint + lu fmt DONE. **3641 test.** PyPI v0.3.2 LIVE. 12 CLI commands.

---

## S448 -- COSA ABBIAMO FATTO

### 1. PyPI v0.3.2 PUBLISHED (nested choice end-to-end)
- Tag pushed to public, Trusted Publisher, LIVE on pypi.org

### 2. Dependabot Security Cleanup
- 6 PR merged + zod 3→4 merged (MCP SDK supports it now)
- npm audit fix: 0 vulns across all 5 JS packages
- HOLD: stripe 17→20, express 4→5 (major, need dedicated session)

### 3. `lu lint` -- B5 (10 rules, 53+20 tests)
- `_lint.py`: single-pass AST walk (Ruff/Clippy pattern)
- 10 rules: 5 CORRECTNESS (exit=1) + 2 STYLE + 3 BEST PRACTICES
- 20 stdlib regression tests (parametrized)
- Guardiana: 9.5/10

### 4. `lu fmt` -- B6 (74 tests)
- `_fmt.py` (~450 LOC): zero-config auto-formatter (gofmt/buf pattern)
- AST + pre-scan comments + single-pass formatter
- Canonical property ordering, agent clause ordering, use sorting
- All 5 action types with correct word order
- Flags: --check (CI), --diff, --stdout (mutually exclusive)
- Idempotent: tested on ALL 20 stdlib protocols
- Research: `.sncp/.../RESEARCH_20260313_LU_FMT_DESIGN.md` (18 sources)
- Guardiana: 9.5/10, P3 findings fixed (dead import, mutex flags, +3 tests)

---

## DECISIONI PRESE (con PERCHE)

| Decisione | Perche |
|-----------|--------|
| Zero-config fmt (not configurable) | gofmt/elm-format: "one true style" elimina debates. LU e giovane. |
| AST + pre-scan (not CST) | Tokenizer ignora commenti. Pre-scan = semplice, funziona. |
| 1 blank line tra sezioni (not 2) | DSL concisa. Stdlib gia usa 1 blank. Research diceva 2 (Python). |
| Mutually exclusive flags | Guardiana F5: --check/--diff/--stdout non devono combinarsi. |

---

## MAPPA SITUAZIONE

```
LINGUA UNIVERSALE (LA MISSIONE):
  FASE A-D: COMPLETE (29 moduli, media 9.5/10)
  FASE E: PER TUTTI
    E.1-E.5: DONE (9.5/10)
    E.6 CervellaLang 1.0: IN PROGRESS
      T3.1 Grammar 1.0 RFC:    DONE (S444)
      T3.2 Standard Library:    DONE (S445)
      T3.3 lu init:              DONE (S444)
      T3.4 lu verify:            DONE (S444)
      T3.5 VS Code Marketplace:  TODO         <- blocco: Rafa
  T2.1 PyPI v0.3.2:              LIVE!
  LU 1.1+1.2:                    DONE!
  B5 lu lint:                     DONE!       <- 10 rules
  B6 lu fmt:                      DONE!       <- zero-config
  Moduli: 29 | Test: 3641 | CLI: 12 | Stdlib: 20

CI/CD: TUTTO GREEN
DEPENDABOT: 2 HOLD (stripe, express)
```

---

## PROSSIMA SESSIONE

### 1. TODO Rafa
- [ ] VS Code Publisher: creare account per T3.5
- [ ] Blog post: revisione "From Vibe Coding to Vericoding"

### 2. OBIETTIVI (priorita)
- **T3.5 VS Code Marketplace** (blocco: Rafa publisher)
- **T3.6 Community Seeding** (blog + showcase)
- **LSP fmt integration** (wire format_source in _lsp.py)
- **lu fmt stdlib** (format all 20 stdlib to canonical style)

---

## I NUMERI

| Metrica | Valore |
|---------|--------|
| Test LU | **3641** |
| Moduli LU | **29** |
| Stdlib | **20** (5 categorie) |
| CLI | **12** |
| Lint rules | **10** (3 categorie) |
| PropertyKind | **9** |
| EBNF | **64** (frozen) |
| Guardiana S448 | lu lint 9.5, lu fmt 9.5 |

---

## Lezioni Apprese (S448)

### Cosa ha funzionato bene
- **Formula Magica x2**: ricerca(14+18 fonti) -> design -> implement -> audit
- **Guardiana P3 = diamante**: comma-space, dead import, mutex flags, +3 test
- **Idempotency test = gold standard**: parametrized su tutti 20 stdlib

### Pattern confermato
- **Rule = plain function**: lint e fmt usano stesso pattern (facile estendere)
- **Research PRIMA**: il report del fmt ha evitato CST trap e config trap

---
*"Ultrapassar os proprios limites!" -- S448*
