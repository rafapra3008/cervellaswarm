# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-27 - Sessione 412
> **STATUS:** FASE C1 COMPLETATA + C2.1 STUDIO DONE. Prossimo: C2.2 implementazione compilatore.

---

## SESSIONE 412 - Cosa e successo

### Step C1.3.6 - Guardiana Finale + Coverage (COMPLETATO, 9.5/10)

**Cosa:** Coverage gap analysis + 24 test nuovi + Guardiana audit FINALE + fix P3 diamante.

**Coverage PRIMA -> DOPO:**
- `_tokenizer.py`: 100% -> 100%, `_ast.py`: 100% -> 100%, `_parser.py`: 96% -> **100%**
- 24 test in `test_parser_coverage.py` (EOF guards, error paths, functional gaps)
- Fix P3: `_AGENT_CLAUSES` -> costante modulo, header commento residuo rimosso

**Verdetto Guardiana:** 9.5/10 - 0 P0/P1/P2

### Step C2.1 - STUDIO Architettura Compilatore (COMPLETATO, 9.3/10)

**Cosa:** Studio completo di 8 moduli esistenti + ricerca esterna (18 fonti) + proposta architettura.

**5 Decisioni architetturali prese:**
1. **String emission + Visitor dispatch** (come codegen.py, come Cython)
2. **ContractViolation raise inline** (non assert, non decoratori - zero deps)
3. **Source annotations `# [LU:line:col]`** (come Coconut)
4. **File separato `_compiler.py`** (non tocca codegen.py)
5. **Testing progressivo** (golden -> round-trip exec -> Hypothesis)

**2 file nuovi pianificati:**
- `_contracts.py` (~30 LOC): `ContractViolation(RuntimeError)` con condition/kind/source
- `_compiler.py` (~400-600 LOC): `ASTCompiler` con `compile(ProgramNode) -> CompiledModule`

**P2 da risolvere in C2.2:**
- F1: `_safe_python_ident` e privata in codegen.py, serve condividerla o duplicarla
- F2: `Confident[T]` mapping serve esempio concreto

**Verdetto Guardiana:** 9.3/10 - 0 P1, 2 P2, 8 P3

---

## MAPPA SITUAZIONE

```
LINGUAGGIO CERVELLASWARM (la missione vera):
  FASE A+B: COMPLETE (13 moduli, 1820 test, 9.5+ media)
  FASE C: Il Linguaggio
    C1: La Grammatica    [####################] 100% DONE!
    C2: Il Compilatore   [##..................] 10%
      C2.1 STUDIO           DONE (S412, 9.3/10)  <-- OGGI
      C2.2 AST -> Python    TODO (7 sub-step pianificati)  <-- PROSSIMO
      C2.3 Python interop   TODO
      C2.4 Constrained gen  TODO
    C3: L'Esperienza     [....................] 0%
```

---

## I NUMERI TOTALI (dopo S412)

| Metrica | Valore |
|---------|--------|
| Test totali | 2217 |
| Test passanti | 2217 (100%) |
| Coverage parser | 100% (0 miss) |
| LOC parser (3 file) | ~1630 |
| LOC test parser (4 file) | ~3900 |
| Tempo test suite | 0.49s |
| Regressioni | 0 |

---

## Lezioni Apprese (S412)

### Cosa ha funzionato bene
- "Guardiana dopo ogni step" (12a volta, S403-S412). Pattern CONSOLIDATO e PROVATO.
- "Coverage gap analysis chirurgica" (19 righe -> 24 test -> 100%): tecnica precisa e ripetibile.
- "STUDIO prima di implementare" (ricerca 18 fonti + codebase analysis): decisioni solide.
- "Hand-crafted token lists per EOF guards": tecnica valida per branch irraggiungibili.

### Cosa non ha funzionato
- Coverage `--cov` richiede Python module name, non file path. 2 tentativi falliti prima del giusto.

### Pattern candidato
- "Fix P3 diamante prima di chiudere step" (3a volta, S411+S412x2): accumulo debt = 0. PROMUOVERE?

---

## Prossimi step

1. **C2.2.1** - `_contracts.py` + test (ContractViolation)
2. **C2.2.2** - `_compiler.py` core: `_expr_to_python`, `_type_to_python`, `_compile_use`
3. **Aggiornare P07** nei validated_patterns (evidenza S403-S412, 12x)

---

## File chiave

- `.sncp/roadmaps/SUBROADMAP_FASE_C_LINGUAGGIO.md` - Piano FASE C (aggiornato S412)
- `.sncp/progetti/cervellaswarm/reports/STUDIO_C2_1_ARCHITETTURA_COMPILATORE.md` - Architettura C2
- `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260227_C2_compiler_ast_python.md` - Ricerca C2
- `.sncp/progetti/cervellaswarm/reports/DESIGN_C1_2_SYNTAX_GRAMMAR.md` - EBNF grammar
- `packages/lingua-universale/src/cervellaswarm_lingua_universale/_parser.py` - Parser
- `packages/lingua-universale/src/cervellaswarm_lingua_universale/codegen.py` - CodeGen esistente
- `packages/lingua-universale/NORD.md` - LA VISIONE

*"La domanda e la risposta nello STESSO linguaggio." - Rafa*
*"Ultrapassar os proprios limites!" - Rafa & Cervella*
