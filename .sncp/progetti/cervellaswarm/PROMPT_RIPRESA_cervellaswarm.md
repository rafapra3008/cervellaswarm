# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-26 - Sessione 410
> **STATUS:** Step C1.3 Parser IN PROGRESS - 3/6 sub-step completati (media Guardiana 9.53/10). Prossimo: C1.3.4 agent/type/use + espressioni.

---

## SESSIONE 410 - Cosa e successo

### Step C1.3 - Parser Unificato (IN PROGRESS)

**Cosa:** Implementazione del parser ricorsivo discendente per la Lingua Universale v0.2. Spezzato in 6 sub-step, 3 completati oggi.

**Sub-step completati:**

| Sub-step | File | LOC | Test | Guardiana |
|----------|------|-----|------|-----------|
| C1.3.1 Tokenizer | `_tokenizer.py` | 320 | 80 | 9.6/10 |
| C1.3.2 AST Nodes | `_ast.py` | 304 | 96 | 9.5/10 |
| C1.3.3 Parser Core | `_parser.py` | 652 | 53 | 9.5/10 |
| **TOTALE** | **3 file src + 3 test** | **1276** | **229** | **9.53 media** |

**Cosa parsa GIA:**
- `protocol X:` con roles, steps, choice blocks, properties (tutte e 7)
- 5 azioni: asks, returns, tells, proposes, sends
- `when X decides:` con branch multipli
- Error messages con line/col
- INDENT/DEDENT espliciti (pattern CPython, non il vecchio _count_indents)

**Cosa MANCA (3 sub-step rimanenti):**
- C1.3.4: Parser nuovi costrutti (`agent`, `type`, `use`) + parser espressioni (per requires/ensures)
- C1.3.5: Integration test con tutti i 10 esempi canonici end-to-end
- C1.3.6: Guardiana finale + coverage >= 95%

### Architettura dei 3 file creati

```
packages/lingua-universale/src/cervellaswarm_lingua_universale/
  _tokenizer.py   320 LOC  Tokenizer con indent stack (CPython pattern)
                           23 TokKind, Tok frozen dataclass, tokenize()
  _ast.py         304 LOC  26 nodi AST frozen dataclass
                           8 Expr + 7 Property + 3 Step/Choice + 8 altri
  _parser.py      652 LOC  Parser ricorsivo discendente
                           ParseError, Parser class, parse() API pubblica
                           Stub per agent/type/use (alzano ParseError)
```

**API pubblica:** `parse(source: str) -> ProgramNode` (in `_parser.py`)

### Design Decisions chiave (S410)

1. **Keywords come IDENT** - il tokenizer NON distingue keyword. Il parser fa dispatching su `tok.value`. Motivazione: semplicita, soft keywords future, pattern intent.py.
2. **Indent stack con colonne assolute** (pattern CPython) - stack `[0, 4, 8, ...]`. INDENT/DEDENT espliciti. Il parser usa `_expect(TokKind.INDENT)` / `_expect(TokKind.DEDENT)`.
3. **Paren depth tracking** - dentro `()` e `[]` sopprime INDENT/DEDENT/NEWLINE (come Python).
4. **Step parsing con pattern matching** - come intent.py `_resolve_step` ma adattato al nuovo tokenizer. I 5 verbi sono parsati con guardie sulla lunghezza delle parole.
5. **LL(2) per property disambiguation** - `_peek_at(1)` per distinguere `X before Y` da `X cannot send Y`.
6. **File privati** (underscore) - `_tokenizer.py`, `_ast.py`, `_parser.py`. L'API pubblica sara in `parser.py` (senza underscore) quando C1.3 e completo.

---

## MAPPA SITUAZIONE

```
LINGUAGGIO CERVELLASWARM (la missione vera):
  FASE A+B: COMPLETE (13 moduli, 1820 test, 9.5+ media)
  FASE C: Il Linguaggio
    C1: La Grammatica    [##############......] 70%
      C1.1 STUDIO           DONE (S408, 9.3/10)
      C1.2 Design sintassi  DONE (S408-409, 8.8/10)
      C1.3 Parser            IN PROGRESS (S410, 3/6 sub-step, 9.53/10)
        C1.3.1 Tokenizer       DONE (9.6/10)
        C1.3.2 AST Nodes       DONE (9.5/10)
        C1.3.3 Parser Core     DONE (9.5/10)
        C1.3.4 Nuovi costrutti TODO (agent/type/use + espressioni)
        C1.3.5 Integration     TODO (10 esempi canonici e2e)
        C1.3.6 Guardiana finale TODO (coverage 95%+)
    C2: Il Compilatore   [....................] 0%
    C3: L'Esperienza     [....................] 0%

CONTEXT OPTIMIZATION (S404-S407): COMPLETATA! (9.4/10)
OPEN SOURCE: FASE 4 95% (Show HN LIVE S404)
```

---

## Lezioni Apprese (S410)

### Cosa ha funzionato bene
- "Guardiana dopo ogni sub-step" (8a volta, S403-S410). Pattern CONSOLIDATO x8.
- "RICERCA parallela prima di implementare" (4 Ricercatrici in parallelo): ha prodotto report dettagliati che hanno guidato l'Architect e il Backend senza ambiguita.
- "Architect PLAN prima di codice": il piano del tokenizer (PLAN_C1_3_1_TOKENIZER.md) ha permesso al Backend di implementare in una sola passata.
- Spezzare C1.3 in 6 sub-step: ogni pezzo e testabile e auditabile indipendentemente.

### Cosa non ha funzionato
- Nulla di significativo. La sessione e stata fluida.

### Pattern candidato
- "Sub-step con Guardiana intermedia" (1a conferma su implementazione multi-file): permette di correggere rotta DURANTE lo sviluppo, non solo alla fine. MONITORARE.

---

## Prossimi step

1. **C1.3.4** - Parser nuovi costrutti + espressioni
   - `_parse_agent()`: agent con role, trust, accepts, produces, requires, ensures
   - `_parse_type_decl()`: variant (`type X = a | b`) e record (`type X =\n field: Type`)
   - `_parse_use_decl()`: `use python X` con alias opzionale
   - `_parse_expr()`: gerarchia or > and > not > comparison > primary (LL(3) per primary)
   - Le espressioni servono per requires/ensures conditions
   - Stima: ~300 LOC parser + ~250 LOC test
2. **C1.3.5** - Integration test con 10 esempi canonici
3. **C1.3.6** - Guardiana finale + coverage >= 95%
4. **Aggiornare P07** nei validated_patterns con evidenza S403-S410 (8x)

---

## File chiave

- `.sncp/roadmaps/SUBROADMAP_FASE_C_LINGUAGGIO.md` - Piano FASE C (aggiornato S410)
- `.sncp/progetti/cervellaswarm/reports/DESIGN_C1_2_SYNTAX_GRAMMAR.md` - DESIGN C1.2 (la grammatica)
- `.sncp/progetti/cervellaswarm/reports/PLAN_C1_3_1_TOKENIZER.md` - Piano tokenizer (Architect)
- `packages/lingua-universale/src/cervellaswarm_lingua_universale/_tokenizer.py` - Tokenizer
- `packages/lingua-universale/src/cervellaswarm_lingua_universale/_ast.py` - AST Nodes
- `packages/lingua-universale/src/cervellaswarm_lingua_universale/_parser.py` - Parser Core
- `packages/lingua-universale/NORD.md` - LA VISIONE

*"La domanda e la risposta nello STESSO linguaggio." - Rafa*
*"Ultrapassar os proprios limites!" - Rafa & Cervella*
