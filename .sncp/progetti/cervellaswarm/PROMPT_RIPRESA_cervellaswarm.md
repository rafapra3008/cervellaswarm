# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-27 - Sessione 411
> **STATUS:** Step C1.3 Parser QUASI COMPLETO - 5/6 sub-step DONE (media Guardiana 9.54/10). Manca SOLO C1.3.6 Guardiana finale + coverage >= 95%.

---

## SESSIONE 411 - Cosa e successo

### Step C1.3.4 - Nuovi Costrutti (COMPLETATO, 9.5/10)

**Cosa:** Implementati i 3 stub del parser (`_parse_agent`, `_parse_type_decl`, `_parse_use_decl`) + parser espressioni completo.

**Processo:** Architect PLAN -> Backend implementa -> Guardiana audita -> Fix P2+P3 diamante.

**Metodi aggiunti a `_parser.py` (11 metodi, +356 LOC):**
- Expression parser: `_parse_expr`, `_parse_or_expr`, `_parse_and_expr`, `_parse_not_expr`, `_parse_comparison`, `_parse_primary` (LL(3) per method call vs attr access)
- Use: `_parse_use_decl` (dotted name + alias opzionale)
- Type: `_parse_type_decl` (variant LL(1) vs record), `_parse_type_expr` (generics + optional), `_parse_field`
- Agent: `_parse_agent` (6 clausole, duplicate detection), `_parse_condition_list` (block + inline)

**Fix applicati (100000% diamante):**
- P2 F1: Clausole duplicate in agent body -> ParseError (era silenzioso)
- P3 F2: `_VALID_TRUST` estratta come costante modulo (era duplicata in 2 posti)
- P3 F3: `_CMP_OPS` estratta come costante modulo (era locale in metodo)
- P3 F5: Test `not not x` (doppia negazione) aggiunto
- P3 F7: Test `List[String]?` (optional generic) aggiunto

### Step C1.3.5 - Integration Tests (COMPLETATO, 9.6/10)

**Cosa:** 86 integration test end-to-end che coprono TUTTI i 10 esempi canonici dalla specifica DESIGN_C1_2.

**Fix applicati:**
- F1: Commento stale "5 decl" corretto a 6
- F2: Docstring "7 tipi" chiarito (7 istanze, 6 tipi unici)

---

## MAPPA SITUAZIONE

```
LINGUAGGIO CERVELLASWARM (la missione vera):
  FASE A+B: COMPLETE (13 moduli, 1820 test, 9.5+ media)
  FASE C: Il Linguaggio
    C1: La Grammatica    [##################..] 90%
      C1.1 STUDIO           DONE (S408, 9.3/10)
      C1.2 Design sintassi  DONE (S408-409, 8.8/10)
      C1.3 Parser            5/6 sub-step DONE (S410-411, 9.54/10 media)
        C1.3.1 Tokenizer       DONE (9.6/10)
        C1.3.2 AST Nodes       DONE (9.5/10)
        C1.3.3 Parser Core     DONE (9.5/10)
        C1.3.4 Nuovi Costrutti DONE (9.5/10, fix P2+P3 inclusi)
        C1.3.5 Integration     DONE (9.6/10)
        C1.3.6 Guardiana finale TODO (coverage >= 95%)  <-- PROSSIMO
    C2: Il Compilatore   [....................] 0%
    C3: L'Esperienza     [....................] 0%
```

---

## I NUMERI DEL PARSER (C1.3 completo finora)

### File sorgente (3 file, 1632 LOC totali)

| File | LOC | Cosa fa |
|------|-----|---------|
| `_tokenizer.py` | 320 | Tokenizer: 23 TokKind, indent stack CPython, paren depth |
| `_ast.py` | 304 | 26 nodi AST frozen dataclass, 8 Expr + 7 Property + etc |
| `_parser.py` | 1008 | Parser ricorsivo discendente, TUTTE le 62 produzioni EBNF |

### File test (3 file, 2710 LOC, 197 test parser)

| File | LOC | Test | Cosa testa |
|------|-----|------|------------|
| `test_parser_core.py` | 820 | 53 | protocol/step/choice/properties (C1.3.3) |
| `test_parser_constructs.py` | 749 | 58 | expr/use/type/agent (C1.3.4) |
| `test_parser_integration.py` | 1141 | 86 | 10 esempi canonici end-to-end (C1.3.5) |

### Test suite lingua-universale

| Metrica | Valore |
|---------|--------|
| Test totali | 2193 |
| Test passanti | 2193 (100%) |
| Tempo | 0.57s |
| Regressioni | 0 |

---

## Design Decisions chiave (S410-411)

1. **Keywords come IDENT** - il tokenizer NON distingue. Il parser dispatcha su `tok.value`.
2. **Indent stack CPython** - stack `[0, 4, 8, ...]`, INDENT/DEDENT espliciti.
3. **Paren depth tracking** - dentro `()` e `[]` sopprime NEWLINE/INDENT/DEDENT.
4. **LL(3) per primary** - IDENT.IDENT( = method call, IDENT.IDENT = attr, IDENT = bare.
5. **Costanti modulo** - `_VALID_TRUST`, `_VALID_CONFIDENCE`, `_CMP_OPS` condivise.
6. **Duplicate clause detection** - `_seen` set in `_parse_agent`, ParseError su duplicati.
7. **File privati** (underscore) - `_tokenizer.py`, `_ast.py`, `_parser.py`. API pubblica sara `parser.py`.

---

## Lezioni Apprese (S411)

### Cosa ha funzionato bene
- "Guardiana dopo ogni sub-step" (9a e 10a volta). Pattern CONSOLIDATO x10.
- "Fix TUTTI gli issue, non solo i bloccanti" (P2 + tutti i P3). 100000% diamante.
- Architect PLAN con pseudocodice -> Backend implementa in una passata -> 0 iterazioni.

### Cosa non ha funzionato
- Nulla di significativo. Flusso fluido come S410.

### Pattern candidato
- "Fix diamante: P2 + tutti P3 prima di procedere" (1a volta): previene accumulo technical debt. MONITORARE.

---

## Prossimi step

1. **C1.3.6** - Guardiana finale + `pytest --cov` >= 95%
   - Misurare coverage attuale
   - Se < 95%: aggiungere test per righe non coperte
   - Se >= 95%: Guardiana audit finale su TUTTO C1.3
   - Chiude Step C1.3!
2. **Aggiornare P07** nei validated_patterns con evidenza S403-S411 (10x)
3. **C2.1** - STUDIO architettura compilatore (AST -> Python)

---

## File chiave

- `.sncp/roadmaps/SUBROADMAP_FASE_C_LINGUAGGIO.md` - Piano FASE C (aggiornato S411)
- `.sncp/progetti/cervellaswarm/reports/DESIGN_C1_2_SYNTAX_GRAMMAR.md` - EBNF grammar
- `.sncp/progetti/cervellaswarm/reports/PLAN_C1_3_4_NUOVI_COSTRUTTI.md` - Plan Architect C1.3.4
- `packages/lingua-universale/src/cervellaswarm_lingua_universale/_tokenizer.py` - Tokenizer
- `packages/lingua-universale/src/cervellaswarm_lingua_universale/_ast.py` - AST Nodes
- `packages/lingua-universale/src/cervellaswarm_lingua_universale/_parser.py` - Parser (COMPLETO!)
- `packages/lingua-universale/NORD.md` - LA VISIONE

*"La domanda e la risposta nello STESSO linguaggio." - Rafa*
*"Ultrapassar os proprios limites!" - Rafa & Cervella*
