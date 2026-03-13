# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-03-13 - Sessione 447
> **STATUS:** LU 1.1+1.2 Nested Choice END-TO-END. **3494 test.** PyPI v0.3.1 LIVE.

---

## S447 -- COSA ABBIAMO FATTO

### 1. LU 1.1 Nested Choice (parser/compiler/spec -- 8 file + 28 test)
- `when X decides:` dentro branch di un altro `when Y decides:`
- Standard MPST/Scribble (Honda/Yoshida POPL 2008). Additive, zero breaking.
- Parser `_parse_choice()` ricorsivo, `MAX_CHOICE_DEPTH = 32`
- Spec: `_collect_all_steps`, `_find_violating_steps`, `_collect_all_paths` ricorsivi
- Guardiana S447: 9.0 -> 8 findings fixati -> 9.5+

### 2. LU 1.2 SessionChecker nested runtime (3 file + 28 test)
- **Stack-based ChoiceFrame**: `choice_stack` sostituisce flat `branch` + `branch_step_index`
- `_current_elements()`, `_peek_at()` ricorsivo, `_pop_exhausted_frames()` cascading
- Backward compat: flat protocols = stack vuoto = comportamento identico
- `summary()` espone `choice_depth` e `branch_path`
- **Bug fix**: `_eval.py:_protocol_node_to_runtime()` crashava su nested .lu (ChoiceNode.sender)
- **saga_order.lu**: ora usa vera nested choice (payment -> inventory decision)
- Guardiana: 9.5/10, 3 P3 tutti fixati

### 3. S446 recap
- PyPI v0.3.1 LIVE, README sweep, 3 CI JS, Dependabot cleanup

---

## DECISIONI PRESE (con PERCHE)

| Decisione | Perche |
|-----------|--------|
| Stack-based (non CFSM-flatten) | Struttura gia ricorsiva. Zero preprocessing. Backward compat. |
| ChoiceFrame frozen + _frame_positions | Separa metadata immutabile da contatore mutabile. |
| `_pop_exhausted_frames` idempotente | Chiamato 3x per send ma corretto per design (Guardiana F2: accept). |
| _eval.py recursive fix | verify_source crashava su nested .lu. Stesso pattern del compiler fix. |

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
  T2.1 PyPI v0.3.1:              LIVE!
  LU 1.1 Nested Choice:          DONE!       <- parser/compiler/spec
  LU 1.2 Nested Runtime:          DONE!       <- SessionChecker stack-based
  Moduli: 29 | Test: 3494 | EBNF: 64 | Stdlib: 20

CI/CD: TUTTO GREEN (local)
DEPENDABOT: 1 PR (#18 express 4->5)
```

---

## PROSSIMA SESSIONE

### 1. TODO Rafa
- [ ] VS Code Publisher: creare account per T3.5
- [ ] Blog post: revisione "From Vibe Coding to Vericoding"

### 2. OBIETTIVI (priorita)
- **PyPI v0.3.2** (nested choice + SessionChecker runtime)
- **T3.5 VS Code Marketplace** (blocco: Rafa publisher)
- **T3.6 Community Seeding** (blog + nested choice showcase)
- **Express 4->5 review** (PR #18)

### 3. Quick wins
- `lu lint` / `lu fmt` (backlog B5/B6)

---

## I NUMERI

| Metrica | Valore |
|---------|--------|
| Test LU | **3494** |
| Moduli LU | **29** |
| Stdlib | **20** (5 categorie) |
| CLI | **10** |
| PropertyKind | **9** |
| EBNF | **64** (frozen) |
| Guardiana S447 | LU 1.1: 9.5+, LU 1.2: 9.5/10 |

---

## Lezioni Apprese (S447)

### Cosa ha funzionato bene
- **Ricerca PRIMA x2**: LU 1.1 report + LU 1.2 report = implementazione precisa
- **Bug trovato dal quick win**: saga_order.lu con nested -> scoperto _eval.py crash
- **Stack-based design**: researcher propose, Regina implementa, Guardiana valida

### Pattern confermato
- **`_convert_elements` recursive**: stesso pattern in _compiler.py, _eval.py, codegen.py
- **Test-driven bug discovery**: test reali trovano bug che la theory non prevede

---
*"Ultrapassar os proprios limites!" -- S447*
<!-- AUTO-CHECKPOINT-START -->
## AUTO-CHECKPOINT: 2026-03-13 17:03 (auto)
- **Branch**: main
- **Ultimo commit**: f72e1739 - S447: LU 1.2 SessionChecker nested runtime -- stack-based ChoiceFrame, 28 new tests, Guardiana 9.5/10
- **File modificati** (3):
  - sncp/progetti/cervellaswarm/PROMPT_RIPRESA_cervellaswarm.md
  - .sncp/progetti/contabilita/PROMPT_RIPRESA_contabilita.md
  - .sncp/progetti/miracollo/PROMPT_RIPRESA_miracollo.md
<!-- AUTO-CHECKPOINT-END -->
