# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-03-13 - Sessione 448
> **STATUS:** lu lint DONE. **3547 test.** PyPI v0.3.2 LIVE. 11 CLI commands.

---

## S448 -- COSA ABBIAMO FATTO

### 1. PyPI v0.3.2 PUBLISHED (nested choice end-to-end)
- Tag `lingua-universale-v0.3.2` pushed to public repo
- Trusted Publisher workflow triggered, environment approved via `gh api`
- LIVE on pypi.org! Nested choice (parser+compiler+spec+runtime) for the world

### 2. Dependabot Security Cleanup (6 PR merged)
- 3 HIGH: ajv 8.18.0, express-rate-limit 7.5.0, hono 4.12.7
- 1 MEDIUM: send 1.2.0
- 2 devDep: flatted 3.4.1 (cli + dashboard)
- HOLD: stripe 17→20 (major), express 4→5 (major), zod 3→4 (MCP SDK peer dep blocks)

### 3. `lu lint` -- B5 Backlog (1 file + 1 test file + CLI)
- **`_lint.py`** (~430 LOC): single-pass AST walk (Ruff/Clippy pattern)
- 10 rules in 3 categories:
  - CORRECTNESS (5, exit=1): duplicate_role, empty_branch, self_message, duplicate_branch_label, undefined_role_in_step
  - STYLE (2, warning): protocol_name_convention, single_step_protocol
  - BEST PRACTICES (3, warning): no_properties, deep_nesting, agent_no_trust
- `--ignore LU-W002,LU-W020` flag with whitespace-tolerant parsing
- Public API: `lint_program()`, `lint_source()`, `lint_file()`
- Research report: `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260313_LU_LINT_DESIGN.md`
- Guardiana audit: 9.5/10, all P3 findings fixed (dead import, dead regex, comma-space)
- **53 new tests** (3547 total)

---

## DECISIONI PRESE (con PERCHE)

| Decisione | Perche |
|-----------|--------|
| LU-W prefix (not LU-E) | LU-E already used for errors (74 codes). W = warning/lint. Zero collision. |
| Single-pass walk (not multi-pass) | Ruff pattern: one walk, multiple rules. Simple, fast, extensible. |
| Rule = plain function `(node, ctx)` | Clippy pattern. Easy to add rules. No registration boilerplate. |
| `ignore` as frozenset | Immutable, hashable, fast lookup. Matches `frozenset` pattern in stdlib. |

---

## MAPPA SITUAZIONE

```
LINGUA UNIVERSALE (LA MISSIONE):
  FASE A-D: COMPLETE (29 moduli, media 9.5/10)
  FASE E: PER TUTTI
    E.1-E.5: DONE (9.5/10)
    E.6 CervellaLang 1.0: IN PROGRESS
      T3.1 Grammar 1.0 RFC:    DONE (S444)
      T3.2 Standard Library:    DONE (S445)  <- 20 protocolli
      T3.3 lu init:              DONE (S444)
      T3.4 lu verify:            DONE (S444)
      T3.5 VS Code Marketplace:  TODO         <- blocco: Rafa publisher
  T2.1 PyPI v0.3.2:              LIVE!
  LU 1.1 Nested Choice:          DONE!       <- parser/compiler/spec
  LU 1.2 Nested Runtime:          DONE!       <- SessionChecker stack-based
  B5 lu lint:                     DONE!       <- 10 rules, 53 tests
  Moduli: 29 | Test: 3547 | CLI: 11 | EBNF: 64 | Stdlib: 20

CI/CD: TUTTO GREEN (local)
DEPENDABOT: 3 HOLD (major: stripe, express, zod)
```

---

## PROSSIMA SESSIONE

### 1. TODO Rafa
- [ ] VS Code Publisher: creare account per T3.5
- [ ] Blog post: revisione "From Vibe Coding to Vericoding"

### 2. OBIETTIVI (priorita)
- **T3.5 VS Code Marketplace** (blocco: Rafa publisher)
- **T3.6 Community Seeding** (blog + nested choice + lu lint showcase)
- **`lu fmt`** (backlog B6 -- auto-formatter companion to lu lint)

### 3. Quick wins
- `lu lint` integration in `lu check` pipeline (--lint flag?)
- Stdlib protocols lint-clean verification

---

## I NUMERI

| Metrica | Valore |
|---------|--------|
| Test LU | **3547** |
| Moduli LU | **29** |
| Stdlib | **20** (5 categorie) |
| CLI | **11** |
| Lint rules | **10** (3 categorie) |
| PropertyKind | **9** |
| EBNF | **64** (frozen) |
| Guardiana S448 | lu lint: 9.5/10 |

---

## Lezioni Apprese (S448)

### Cosa ha funzionato bene
- **Formula Magica confermata**: Research report (14 sources) → design → implement → audit
- **Guardiana anche su P3**: comma-space bug in `--ignore` parsing trovato prima del commit
- **Dependabot triage strategy**: patch/minor merge safe, major HOLD = zero risk

### Pattern confermato
- **Rule = plain function**: facile aggiungere regole senza boilerplate (Clippy/Ruff)
- **Single commit per feature**: lint = 1 commit con tutto (code + test + CLI)

---
*"Ultrapassar os proprios limites!" -- S448*
