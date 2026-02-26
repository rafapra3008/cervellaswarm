# SUBROADMAP - Fase C: Il Linguaggio

> **Creata:** 26 Febbraio 2026 - Sessione 407
> **Fonti:** NORD.md (S380), 2 report Researcher (S407), 300+ fonti cumulative, showcase.py
> **Prerequisiti:** FASE A+B COMPLETE (13 moduli, 1820 test, 98% coverage, 0 deps)
> **Score target:** 9.5/10 per ogni step (audit Guardiana)
> **Filosofia:** "Fatto BENE > Fatto VELOCE" | "Un progresso al giorno"

---

## L'INSIGHT DI RAFA (S407)

```
+====================================================================+
|                                                                    |
|   "Python e diventato gigante perche era piu facile da capire      |
|    per gli umani. Ora ci vuole un linguaggio che la propria AI     |
|    e piu facile da capire E gli umani capire."                     |
|                                                                    |
|   DUAL-READABLE: facile per l'AI + facile per gli umani.           |
|   Come Python porto il codice vicino all'inglese,                  |
|   noi portiamo il codice vicino a come l'AI PENSA                  |
|   e come gli umani CAPISCONO.                                      |
|                                                                    |
|                                          - Rafa, S407              |
+====================================================================+
```

---

## LE 7 PROPRIETA DEL LINGUAGGIO (dalla ricerca S407)

1. **Sintassi Non Ambigua** - grammatica formale, constrained decoding
2. **Dichiarativo** - descrive COSA, non COME
3. **Token Efficiente** - keyword ASCII brevi, zero boilerplate
4. **Incertezza Come Tipo** - `Confidence` nativo (nessun altro lo ha)
5. **Isomorfo al Dominio** - la struttura del codice = la struttura del problema
6. **Auto-Documentante** - `requires`/`ensures` nel codice, non nei commenti
7. **Verificabile Formalmente** - Lean 4 sotto il cofano

---

## LE 3 FASI DI FASE C

```
+================================================================+
|   FASE C1: La Grammatica (~4-6 sessioni)                        |
|   - Definire la sintassi formale del linguaggio                  |
|   - Parser + grammar export per constrained decoding             |
|   - "Come l'AI legge" = grammatica che l'AI puo generare         |
|                                                                  |
|   FASE C2: Il Compilatore (~6-8 sessioni)                        |
|   - Da linguaggio -> Python verificato                           |
|   - Python interop (import da e verso Python)                    |
|   - "Come l'AI scrive" = genera codice corretto per costruzione  |
|                                                                  |
|   FASE C3: L'Esperienza (~4-6 sessioni)                          |
|   - REPL interattivo + errori umani                              |
|   - Il flusso completo: persona parla -> sistema verifica        |
|   - "Come la nonna usa" = dal linguaggio naturale al codice      |
+================================================================+
```

---

## FASE C1: LA GRAMMATICA (Rischio MEDIO)

> Definire CHE ASPETTO HA il linguaggio. Prima su carta, poi nel parser.

### Step C1.1: STUDIO - Analisi dei moduli esistenti come base

**Non toccare nulla.** Leggere e mappare:
- `spec.py` (1242 LOC) - gia un proto-linguaggio di specifica
- `dsl.py` - gia un DSL per protocolli (Scribble-inspired)
- `intent.py` (649 LOC) - gia un parser di linguaggio naturale
- `codegen.py` (730 LOC) - gia genera Python
- `showcase.py` (492 LOC) - il flusso end-to-end attuale

**Output:** Mappa di cosa gia "sembra un linguaggio" e cosa manca.
**Effort:** 1 sessione
**Rischio:** NULLO (studio puro)

**Criterio completamento:**
- [x] Tabella "modulo -> feature del linguaggio -> gap"
- [x] Inventario di tutte le keyword/strutture gia usate nel DSL
- [x] Proposta: "il linguaggio nasce da QUI" (quale modulo diventa il core?)
- [x] Guardiana verifica (9.3/10 S408)

---

### Step C1.2: Design della Sintassi (La Decisione Chiave)

**Il momento piu importante.** Definire la sintassi concreta del linguaggio.

**Principi design (dalla ricerca):**
1. Python-like first (sfrutta bias LLM, curva apprendimento bassa)
2. Grammatica piccola e unanime (come Lua: ogni feature deve essere ovvia)
3. `confidence`, `proof`, `requires`, `ensures` come keyword native
4. Struttura isomorfa al dominio agente (protocol, agent, trust)

**Output:** Documento BNF/EBNF della grammatica + 10 esempi annotati.
**Effort:** 2-3 sessioni (con ricerca intermedia)
**Rischio:** ALTO (questa decisione e irreversibile nel lungo termine)

**Criterio completamento:**
- [x] Grammatica EBNF completa (62 produzioni, < 100 regole)
- [x] 10 esempi "dual-readable" annotati (umano capisce + AI genera)
- [x] Confronto con sintassi attuale DSL (cosa cambia, cosa resta)
- [x] Revisione Marketing (6.8/10 leggibilita)
- [x] Revisione Ingegnera (7/10 implementabilita)
- [x] Guardiana verifica (8.8/10 S409)

---

### Step C1.3: Parser del Linguaggio (IN PROGRESS - S410)

**Implementare il parser dalla grammatica.**

**Approccio:** Recursive descent parser in Python puro (0 deps, come il resto).
La grammatica EBNF diventa direttamente il parser. Spezzato in 6 sub-step.

**Output:** `packages/lingua-universale/src/.../parser.py` + test completi
**Effort:** 2-3 sessioni
**Rischio:** MEDIO

**Sub-step (S410):**
- [x] C1.3.1 Tokenizer unificato (320 LOC, 80 test, Guardiana 9.6/10)
- [x] C1.3.2 Nodi AST (304 LOC, 96 test, Guardiana 9.5/10)
- [x] C1.3.3 Parser Core - protocol/step/choice/properties (652 LOC, 53 test, Guardiana 9.5/10)
- [ ] C1.3.4 Parser nuovi costrutti - agent/type/use + espressioni
- [ ] C1.3.5 Integration + backward compat (10 esempi canonici end-to-end)
- [ ] C1.3.6 Guardiana finale + coverage >= 95%

**Criterio completamento:**
- [ ] Parser che accetta tutti i 10 esempi del Step C1.2
- [ ] Error messages umani (non "unexpected token at line 42")
- [ ] Round-trip: parse -> AST -> render == originale
- [ ] Export grammatica per constrained decoding (JSON/EBNF)
- [ ] Test coverage >= 95%
- [ ] Guardiana verifica

---

## FASE C2: IL COMPILATORE (Rischio ALTO)

> Da "linguaggio nostro" a "Python che funziona e e verificato"

### Step C2.1: STUDIO - Architettura compilatore

**Non toccare nulla.** Studiare:
- Come `codegen.py` gia genera Python da protocolli
- Come la pipeline spec -> codegen funziona
- Session types come contratti per il codice generato
- Best practice: source maps, error tracing, debugging

**Output:** Proposta architettura compilatore per Guardiana.
**Effort:** 1 sessione
**Rischio:** NULLO

---

### Step C2.2: AST -> Python Code Generation

**Il codice generato DEVE rispettare i contratti.**

`requires` -> precondizioni Python (assert/raise)
`ensures` -> postcondizioni Python (verificate)
`confidence` -> tipo `Confident[T]` nel codice generato
`protocol` -> `SessionChecker` enforcement

**Effort:** 3-4 sessioni
**Rischio:** ALTO

**Criterio completamento:**
- [ ] Compilazione dei 10 esempi canonici in Python funzionante
- [ ] Il codice generato ha contratti runtime (non solo commenti)
- [ ] Round-trip: linguaggio -> Python -> test -> OK
- [ ] Source maps: errore Python traccia alla riga nel linguaggio
- [ ] Guardiana verifica

---

### Step C2.3: Python Interop (La Lezione di ABC)

**ABC mori perche era chiuso. Python vinse perche importava C.**

Il linguaggio DEVE poter:
- Importare moduli Python (`use python math`)
- Esportare funzioni Python (`export agent Worker as python`)
- Chiamare codice esistente senza riscrittura

**Effort:** 2-3 sessioni
**Rischio:** ALTO

---

### Step C2.4: Constrained Generation Export

**Il compilatore produce una grammatica usabile da LLM.**

Quando un LLM deve generare codice nel nostro linguaggio, il parser esporta
la grammatica in formato compatibile con XGrammar/llguidance/Outlines.
L'AI genera codice **sintatticamente valido per costruzione**.

**Effort:** 1-2 sessioni
**Rischio:** MEDIO

---

## FASE C3: L'ESPERIENZA (Rischio MEDIO)

> "La nonna con le ricette" - dal linguaggio naturale al codice verificato

### Step C3.1: REPL Interattivo

**Come Python ha il `>>>`, noi abbiamo il nostro.**

```
cervella> describe "gestisci le ricette della nonna"
[Intent] manage_recipes for User
  requires: user.authenticated
  ensures: no_recipe_deleted_by_accident

cervella> verify
[Lean4] all_properties: PROVED
  - no_accidental_deletion: PROVED
  - authentication_required: PROVED

cervella> generate python
[CodeGen] Generated: recipes_app.py (45 lines, verified)
```

**Effort:** 2-3 sessioni
**Rischio:** MEDIO

---

### Step C3.2: Error Messages per Umani

**Quando la verifica fallisce, il messaggio deve essere CHIARO.**

Gia abbiamo `errors.py` (1784 LOC, 257 test). Estendere per il linguaggio.

```
SBAGLIATO:
  Error: type mismatch at AST node 42, expected Confidence got String

CORRETTO:
  La confidence del risultato deve essere un livello (High, Medium, Low),
  non un testo libero. Hai scritto "sono abbastanza sicuro" -
  intendevi `confidence: Medium`?
```

**Effort:** 1-2 sessioni
**Rischio:** BASSO

---

### Step C3.3: Il Flusso Completo (Il Demo Giorno)

**Il momento della verita.** Una persona descrive cosa vuole, il sistema:
1. Capisce l'intento (intent.py potenziato)
2. Genera la specifica nel linguaggio
3. Verifica le proprieta (Lean 4 bridge)
4. Genera codice Python verificato
5. Mostra la confidence e le prove

Questo e il **showcase_v2.py** - la prova che funziona REALE.

**Effort:** 2-3 sessioni
**Rischio:** ALTO

---

## RIEPILOGO

```
+================================================================+
|   SUBROADMAP FASE C: IL LINGUAGGIO                               |
+================================================================+

FASE C1: La Grammatica             [##############......] 70%
  C1.1 STUDIO moduli esistenti       1 sess    DONE (S408, 9.3/10)
  C1.2 Design sintassi (BNF/EBNF)   2-3 sess  DONE (S408-409, 8.8/10)
  C1.3 Parser del linguaggio         2-3 sess  IN PROGRESS (S410, 3/6 sub-step)

FASE C2: Il Compilatore            [....................] 0%
  C2.1 STUDIO architettura           1 sess    TODO
  C2.2 AST -> Python generation      3-4 sess  TODO
  C2.3 Python interop                2-3 sess  TODO
  C2.4 Constrained generation        1-2 sess  TODO

FASE C3: L'Esperienza             [....................] 0%
  C3.1 REPL interattivo              2-3 sess  TODO
  C3.2 Error messages umani          1-2 sess  TODO
  C3.3 Flusso completo (showcase v2) 2-3 sess  TODO

EFFORT TOTALE: ~15-25 sessioni (~2-4 mesi, un progresso al giorno)
ORDINE: C1 -> C2 -> C3 (mai saltare)
AUDIT: Guardiana dopo OGNI step
```

---

## METRICHE TARGET

| Metrica | Target |
|---------|--------|
| Grammatica (regole EBNF) | < 100 regole |
| Parser test coverage | >= 95% |
| Esempi canonici | >= 10, annotati |
| Codice generato: test pass | 100% |
| Error messages: leggibilita umana | Guardiana 9.5/10 |
| Constrained decoding: export | compatibile XGrammar/llguidance |
| Python interop | import + export bidirezionale |
| Zero dependencies | mantenute (0 deps) |
| Demo end-to-end | "nonna con le ricette" funziona |

---

## SUCCESS CRITERIA

- [ ] Il linguaggio ha una grammatica formale esplicita (EBNF pubblicata)
- [ ] Un LLM puo generare codice nel linguaggio senza errori di sintassi (constrained decoding)
- [ ] Un non-sviluppatore legge il codice e capisce cosa fa
- [ ] Il codice generato in Python ha contratti runtime verificati
- [ ] Le proprieta formali sono provate da Lean 4
- [ ] Python interop bidirezionale funziona
- [ ] Il demo "nonna con le ricette" e REALE (non su carta)

---

## DIPENDENZE

```
FASE A+B (COMPLETE - 13 moduli, 1820 test)
   |
   v
FASE C1 (Grammatica - i moduli esistenti diventano il linguaggio)
   |
   v
FASE C2 (Compilatore - il linguaggio genera Python verificato)
   |
   v
FASE C3 (Esperienza - la nonna puo usarlo)
```

---

## IL PARALLELO STORICO

```
1991: Python nasce. Guido dice: "codice leggibile per gli umani."
      for item in list  (non  for(int i=0; i<n; i++))
      Il mondo cambia.

2026: Lingua Universale nasce. Rafa dice: "codice leggibile per AI e umani."
      requires X ensures Y  (non  50 righe di logica da indovinare)
      confidence: High  (non  "sono abbastanza sicuro" in una stringa)
      Il mondo cambia di nuovo.
```

---

*"Ultrapassar os proprios limites!"*
*"La domanda e la risposta nello STESSO linguaggio."*
*"Non e sempre come immaginiamo... ma alla fine e il 100000%!"*

*Cervella Regina - CervellaSwarm S407*
*Fonti: NORD.md (S380), Researcher (landscape S407), Researcher (dual-readable S407)*
