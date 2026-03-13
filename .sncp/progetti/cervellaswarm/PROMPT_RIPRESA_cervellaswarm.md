# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-03-13 - Sessione 447
> **STATUS:** Nested Choice LU 1.1 DONE. **3466 test.** PyPI v0.3.1 LIVE.

---

## S447 -- COSA ABBIAMO FATTO (Nested Choice LU 1.1)

### 1. Nested Choice implementato (8 file core + 28 test)
- **Feature**: `when X decides:` dentro branch di un altro `when Y decides:`
- **Standard**: MPST/Scribble (Honda/Yoshida POPL 2008). Era un limite LU 1.0.
- **Additive puro**: tutti 20 stdlib protocolli invariati. Zero breaking changes.
- **File modificati**: `_ast.py`, `_parser.py`, `_compiler.py`, `codegen.py`, `protocols.py`, `spec.py`, `_grammar_export.py`, `checker.py` (doc), `_tokenizer.py` (doc), `saga_order.lu` (commento)
- **Parser**: `_parse_branch` accetta `when` -> `_parse_choice()` ricorsivo
- **Depth guard**: `MAX_CHOICE_DEPTH = 32` (anti stack overflow)
- **Spec checkers**: `_collect_all_steps` + `_find_violating_steps` + `_collect_all_paths` tutti ricorsivi
- **28 test**: parser 7, compiler 3, protocol 3, spec 10, grammar 2, depth 2, e2e 2

### 2. Guardiana Audit: 9.0/10 -> tutti 8 findings fixati
- **F1 (P1)**: SessionChecker non supporta nested runtime -> documentato (LU 1.2)
- **F2 (P2)**: `_check_no_deadlock_static` ricorsivo
- **F3 (P2)**: `_has_choices` corretto per construction (commento)
- **F4 (P2)**: saga_order.lu commento stale -> aggiornato
- **F5 (P3)**: Depth guard `MAX_CHOICE_DEPTH = 32` + test
- **F6 (P3)**: 5 docstring "v0.2" -> rimosse
- **F7 (P3)**: Test multi-level context "outer > inner"
- **F8 (P3)**: Test ALWAYS_TERMINATES + NO_DEADLOCK su nested

### 3. S446 recap (sessione precedente)
- PyPI v0.3.1 PUBLISHED (stdlib nel wheel fix + publish flow)
- README quality sweep (12 stale refs), 3 CI workflows JS, Dependabot cleanup
- Research report nested choice: `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260313_NESTED_CHOICE_PARSER.md`

---

## DECISIONI PRESE (con PERCHE)

| Decisione | Perche |
|-----------|--------|
| Nested choice LU 1.1 (non 2.0) | Additive, non breaking. Standard MPST. |
| SessionChecker runtime TBD LU 1.2 | Richiede stack-based tracking. Sessione dedicata. |
| `MAX_CHOICE_DEPTH = 32` | Sufficiente per protocolli reali. Protegge da input malevolo. |
| codegen.py `_render_elements` ricorsivo | Settimo file non previsto dalla ricerca. Trovato dai test. |

---

## MAPPA SITUAZIONE

```
LINGUA UNIVERSALE (LA MISSIONE):
  FASE A-D: COMPLETE (29 moduli, media 9.5/10)
  FASE E: PER TUTTI
    E.1-E.5: DONE (9.5/10)
    E.6 CervellaLang 1.0: IN PROGRESS
      T3.1 Grammar 1.0 RFC:    DONE (S444)  <- grammatica frozen
      T3.2 Standard Library:    DONE (S445)  <- 20 protocolli
      T3.3 lu init:              DONE (S444)  <- scaffolding + --template
      T3.4 lu verify:            DONE (S444)  <- verifica standalone
      T3.5 VS Code Marketplace:  TODO         <- blocco: Rafa publisher
  T2.1 PyPI v0.3.1:              LIVE!       <- published 13 Mar 2026
  LU 1.1 Nested Choice:          DONE!       <- S447, 28 test
  Moduli: 29 | Test: 3466 | EBNF: 64 (frozen) | Stdlib: 20 protocolli

CI/CD: TUTTO GREEN (local)
DEPENDABOT: 1 PR aperta (#18 express 4->5, needs review)
```

---

## PROSSIMA SESSIONE -- COSA FARE

### 1. TODO Rafa (azioni manuali)
- [ ] **VS Code Publisher**: creare account per T3.5
- [ ] **Blog post**: revisione "From Vibe Coding to Vericoding"

### 2. OBIETTIVI (priorita)
- **SessionChecker nested runtime** (LU 1.2 -- stack-based branch tracking)
- **T3.5 VS Code Marketplace** (blocco: Rafa publisher account)
- **T3.6 Community Seeding** (blog update con stdlib + nested choice)
- **Express 4->5 review** (PR #18, unica Dependabot rimasta)
- **PyPI v0.3.2** (include nested choice, SessionChecker doc)

### 3. Quick wins
- `lu lint` / `lu fmt` (backlog B5/B6)
- Stdlib: saga_order.lu con vera nested choice (ora che e supportato)

---

## I NUMERI

| Metrica | Valore |
|---------|--------|
| Test LU | **3466** |
| Moduli LU | **29** |
| Stdlib Protocolli | **20** (5 categorie) |
| CLI Comandi | **10** |
| PropertyKind | **9** (tutti coperti!) |
| EBNF Produzioni | **64** (frozen) |
| Guardiana Audit S447 | **9.0** → 8 fix → 9.5+ |

---

## Lezioni Apprese (S447)

### Cosa ha funzionato bene
- **Ricerca PRIMA**: report 401 righe (14 fonti) -> implementazione precisa in 6 file (poi 8)
- **Guardiana pattern**: implement → audit → fix = trova bug reali (F2 deadlock non ricorsivo!)
- **Test-driven discovery**: i 23 test iniziali hanno trovato codegen.py (7° file non previsto)

### Cosa non ha funzionato (poi fixato)
- **Research sottostima**: report diceva 7 file, erano 8 (codegen.py mancava dalla lista)

### Pattern confermato
- **`_collect_all_steps` helper**: DRY ricorsivo per tutti i checker che iterano elementi
- **`_find_violating_steps`**: preserva branch context nel evidence (diagnostica migliore)

---
*"Ultrapassar os proprios limites!" -- S447*
<!-- AUTO-CHECKPOINT-START -->
## AUTO-CHECKPOINT: 2026-03-13 16:37 (auto)
- **Branch**: main
- **Ultimo commit**: ced61a36 - S447: Nested Choice LU 1.1 -- 8 files, 28 tests, Guardiana 9.0 all findings fixed
- **File modificati** (3):
  - sncp/progetti/cervellaswarm/PROMPT_RIPRESA_cervellaswarm.md
  - .sncp/progetti/contabilita/PROMPT_RIPRESA_contabilita.md
  - .sncp/progetti/miracollo/PROMPT_RIPRESA_miracollo.md
<!-- AUTO-CHECKPOINT-END -->
