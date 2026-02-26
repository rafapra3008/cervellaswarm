# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-02-26 - Sessione 409
> **STATUS:** Step C1.2 DESIGN SINTASSI COMPLETATO (Guardiana 8.8/10). Pronta per Step C1.3 Parser.

---

## SESSIONE 409 - Cosa e successo

### Step C1.2 - Design della Sintassi (COMPLETATO)

**Cosa:** Grammatica EBNF completa della Lingua Universale v0.2 + 10 esempi annotati dual-readable.

**Report completo:** `.sncp/progetti/cervellaswarm/reports/DESIGN_C1_2_SYNTAX_GRAMMAR.md`

**Risultati chiave:**
- 62 produzioni EBNF (target < 100) - parsabile LL(1) ovunque tranne step (pattern match) e primary (LL(3))
- 6 nuovi costrutti: `agent`, `requires`, `ensures`, `type`, `Confident[T]`, `use python`
- 10 esempi canonici annotati (dal DelegateTask base al programma completo multi-protocol)
- Zero left recursion (eliminata in v0.2)
- `proof` keyword rimandato a C2 (serve semantica Lean 4 - "su carta non reale")

**DECISIONE FONDAMENTALE - Il linguaggio e:**
- **intent.py** = SINTASSI BASE (100% compatibile: programmi intent esistenti sono validi)
- **spec.py** = PROPERTIES inline nel protocol (unificato)
- **Tipi AI nativi:** `Confident[T]`, `TrustScore`, `String?` (opzionale)
- **dsl.py** = solo formato export Scribble (NON core)

**3 Review completate:**

| Reviewer | Score | Sintesi |
|----------|-------|---------|
| Marketing | 6.8/10 leggibilita | Nomi dominio ok. Nota: confine zona narrativa/tecnica e FEATURE. |
| Ingegnera | 7/10 implementabilita | 6 fix (left recursion, type_expr, type_decl, proposes, parentesi). |
| Guardiana | 8.8/10 qualita | 4 fix (step, terminali, double NEWLINE, proof defer). |

**NOTA SCORE:** 8.8/10 Guardiana e coerente per un DESIGN document (non codice). Il design verra validato a 9.5+ quando implementato come parser in C1.3.

---

## MAPPA SITUAZIONE

```
LINGUAGGIO CERVELLASWARM (la missione vera):
  FASE A+B: COMPLETE (13 moduli, 1820 test, 9.5+ media)
  FASE C: Il Linguaggio
    C1: La Grammatica    [########............] 40%
      C1.1 STUDIO           DONE (S408, 9.3/10)
      C1.2 Design sintassi  DONE (S408-409, 8.8/10)
      C1.3 Parser            TODO (prossimo! 5-6 sessioni, ~1200 LOC)
    C2: Il Compilatore   [....................] 0%
    C3: L'Esperienza     [....................] 0%

CONTEXT OPTIMIZATION (S404-S407): COMPLETATA! (9.4/10)
OPEN SOURCE: FASE 4 95% (Show HN LIVE S404)
```

---

## Lezioni Apprese (S409)

### Cosa ha funzionato bene
- "Guardiana dopo ogni step" (7a volta, S403-S409). Pattern CONSOLIDATO x7.
- Triple review (Marketing + Ingegnera + Guardiana) su design document: ognuna ha trovato problemi diversi.
- "STUDIO prima di edit" (5a conferma): C1.1 STUDIO ha guidato TUTTO il design C1.2.

### Cosa non ha funzionato
- Auto-compact nella sessione precedente ha interrotto il flusso. Fix: checkpoint piu frequenti.

### Pattern candidato
- "Triple review su design" (Marketing leggibilita + Ingegnera implementabilita + Guardiana qualita): 1a conferma. MONITORARE.

---

## Prossimi step

1. **Step C1.3** - Parser Unificato (IL CUORE TECNICO!)
   - ~1200 LOC parser, ~700 LOC test (stima Ingegnera)
   - ~50-60% riuso da intent.py + spec.py
   - Tokenizer unificato con indent stack (come Python)
   - Target: Guardiana 9.5/10 (e CODICE, non design)
2. **Aggiornare P07** nei validated_patterns con evidenza S403-S409 (7x)
3. **Monitorare Show HN** - response strategy in `docs/blog/show-hn-draft.md`

---

## File chiave

- `.sncp/roadmaps/SUBROADMAP_FASE_C_LINGUAGGIO.md` - Piano FASE C
- `.sncp/progetti/cervellaswarm/reports/DESIGN_C1_2_SYNTAX_GRAMMAR.md` - DESIGN C1.2
- `.sncp/progetti/cervellaswarm/reports/STUDY_C1_1_MODULE_ANALYSIS.md` - STUDIO C1.1
- `packages/lingua-universale/NORD.md` - LA VISIONE
- `~/.claude/COSTITUZIONE_OPERATIVA.md` - Versione condensata 83 righe

*"La domanda e la risposta nello STESSO linguaggio." - Rafa*
*"Ultrapassar os proprios limites!" - Rafa & Cervella*
