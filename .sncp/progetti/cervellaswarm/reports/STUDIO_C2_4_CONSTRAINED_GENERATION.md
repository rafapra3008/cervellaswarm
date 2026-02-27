# STUDIO C2.4 -- Constrained Generation Export

> **Creato:** 2026-02-27 - Sessione 418
> **Prerequisiti:** C2.3 COMPLETO (6/6, media 9.5/10), grammatica EBNF 62 produzioni, parser 100% test
> **Fonti:** 12 fonti esterne (XGrammar paper MLSys 2025, llguidance, Outlines, GBNF spec, vLLM docs)
> **Zero nuove dipendenze runtime.**

---

## L'INSIGHT

> "Un LLM che genera codice nel nostro linguaggio non deve MAI produrre
> un errore di sintassi. La grammatica e il guardrail."
> -- SUBROADMAP Fase C, Step C2.4

Il constrained decoding permette a un LLM di generare testo che rispetta
una grammatica formale **per costruzione**. Invece di generare e poi validare
(reject + retry), il modello puo generare solo token che sono validi
secondo la grammatica. Errore di sintassi = impossibile.

---

## PANORAMA ESTERNO (dalla ricerca)

### Framework principali

| Framework | Autore | Formato | Integrazione | Status 2025 |
|-----------|--------|---------|-------------|-------------|
| **XGrammar** | MLC AI (MLSys) | GBNF | vLLM (default), SGLang, TRT-LLM | Standard de facto self-hosted |
| **llguidance** | Microsoft | Lark EBNF | Base di OpenAI Structured Outputs | Production |
| **Outlines** | dottxt | Lark EBNF | HuggingFace, SGLang, TGI | Ampiamente usato |
| **GBNF** | llama.cpp | GBNF nativo | llama.cpp, kobold, etc. | Standard locale |
| **Cloud APIs** | Anthropic/OpenAI | JSON Schema | API cloud | Solo JSON Schema |

### La scelta: GBNF + Lark

**GBNF** = il formato piu ampiamente supportato (XGrammar/vLLM + llama.cpp).
**Lark** = il formato piu Python-friendly (Outlines + llguidance).

Supportando entrambi copriamo **il 95% dell'ecosistema** di constrained decoding.

---

## IL PROBLEMA CRITICO: INDENT/DEDENT

Lingua Universale e **indentation-sensitive** (come Python). I sistemi di
constrained decoding **non gestiscono INDENT/DEDENT nativamente**.

### La soluzione: LLM Grammar vs Parser Grammar

```
PARSER GRAMMAR (62 produzioni, strict):
  protocol_decl ::= 'protocol' IDENT ':' NEWLINE INDENT protocol_body DEDENT
  ^^^^^ richiede token INDENT/DEDENT dal tokenizer

LLM GRAMMAR (semplificata, lenient):
  protocol-decl ::= ws "protocol" ws ident ws ":" ws newline protocol-body
  ^^^^^ usa whitespace libero, la struttura e guidata dalle keyword
```

**Pipeline:**
1. LLM genera codice usando la LLM Grammar (whitespace-lenient)
2. Il parser ufficiale valida e corregge l'indentazione
3. Se necessario, un auto-formatter normalizza lo stile

Questo e lo stesso approccio usato da Python (Black/autopep8 formattano dopo).

---

## SCOPE ESATTO C2.4

### IN C2.4

| Feature | Descrizione |
|---------|-------------|
| `GrammarExporter` class | Classe che esporta la grammatica in formati esterni |
| `to_gbnf() -> str` | Export in formato GBNF (XGrammar/vLLM/llama.cpp) |
| `to_lark() -> str` | Export in formato Lark EBNF (Outlines/llguidance) |
| LLM Grammar design | Versione whitespace-lenient delle 62 produzioni |
| Validation tests | Test che GBNF/Lark sono parsabili dai rispettivi tool |

### DEFERRED

| Feature | Perche | Quando |
|---------|--------|--------|
| `to_json_schema()` | Solo subset (tipi, non protocolli) | C3 se serve |
| Constrained decoding runtime | Richiede infra LLM | C3.3 |
| Auto-formatter | Nice-to-have, non critico per l'export | C3 |

---

## ARCHITETTURA

### Nuovo file: `_grammar_export.py`

```
Grammatica EBNF (62 regole, in _parser.py)
    |
    v
GrammarExporter
    |
    +-- to_gbnf() -> str    # XGrammar/vLLM/llama.cpp
    |
    +-- to_lark() -> str    # Outlines/llguidance
    |
    v
Stringa di grammatica (formato esterno)
```

La classe NON legge `_parser.py` a runtime. Le produzioni sono
**codificate staticamente** nella classe (source of truth = EBNF doc + parser).
Questo evita fragilita e coupling.

### Struttura della LLM Grammar

62 produzioni EBNF -> ~50-55 regole LLM Grammar (merging terminali triviali).

**Mapping chiave EBNF -> GBNF:**

| EBNF | GBNF |
|------|------|
| `protocol_decl ::= 'protocol' IDENT ':' NEWLINE INDENT ...` | `protocol-decl ::= ws "protocol" ws ident ws ":" ws newline ...` |
| `IDENT ::= [A-Za-z_][A-Za-z0-9_]*` | `ident ::= [A-Za-z_] [A-Za-z0-9_]*` |
| `INDENT` / `DEDENT` | (rimossi, whitespace libero) |
| `NEWLINE` | `newline ::= "\n"` (opzionale in molti contesti) |
| `step ::= IDENT action NEWLINE` | `step ::= ws ident ws action ws newline` |

**Mapping chiave EBNF -> Lark:**

| EBNF | Lark |
|------|------|
| `protocol_decl ::= ...` | `protocol_decl: "protocol" IDENT ":" _NL body` |
| `IDENT` | `IDENT: /[A-Za-z_][A-Za-z0-9_]*/` |
| `INDENT` / `DEDENT` | `_NL: /\n\s*/` |
| alternation `\|` | `\|` (same) |

---

## SUB-STEPS (4)

### C2.4.1 -- STUDIO + LLM Grammar design
- Scrivere le ~50 regole della LLM Grammar (versione lenient)
- Decidere come gestire: verb/noun (open list vs closed), keyword ambiguity
- **Output:** grammatica LLM documentata in questo report
- **Effort:** 0.5 sessione | **Rischio:** BASSO

### C2.4.2 -- GrammarExporter implementation
- Nuovo file `_grammar_export.py`
- `GrammarExporter` con `to_gbnf()` e `to_lark()`
- Regole codificate staticamente (no parsing di _parser.py)
- ~200-300 LOC
- **Effort:** 1 sessione | **Rischio:** MEDIO

### C2.4.3 -- Validation tests
- Test che `to_gbnf()` produce output parsabile da GBNF validator
- Test che `to_lark()` produce output parsabile da `lark` library
- Test round-trip: genera sorgente .lu con constrained grammar -> il nostro parser lo accetta
- ~15-25 test in `test_grammar_export.py`
- **Dipendenze test-only:** `lark` (pip install, solo in test)
- **Effort:** 0.5 sessione | **Rischio:** BASSO

### C2.4.4 -- Guardiana audit finale
- Update `__init__.py` se serve
- Target: 9.5/10
- **Effort:** 0.5 sessione

---

## RISCHI E MITIGAZIONI

| Rischio | Probabilita | Impatto | Mitigazione |
|---------|-------------|---------|-------------|
| INDENT/DEDENT non rappresentabili | CERTO | ALTO | LLM Grammar whitespace-lenient (decisione presa) |
| verb/noun closed list troppo restrittiva | MEDIO | MEDIO | Due strategie: (a) closed list in grammar, (b) open IDENT con post-validation |
| XGrammar non installabile su macOS (solo GPU) | MEDIO | BASSO | Validazione GBNF con regex/parser locale, XGrammar solo in CI |
| Lark `pip install` fallisce | BASSO | BASSO | Lark e pure Python, zero deps native |
| Grammar diverge dal parser nel tempo | MEDIO | ALTO | Test che ogni keyword/rule del parser e presente nella grammar export |

---

## STIMA TOTALE

| Metrica | Valore |
|---------|--------|
| **File nuovi** | 2 (`_grammar_export.py`, `test_grammar_export.py`) |
| **LOC stimate** | ~200-300 (source) + ~300-400 (test) |
| **Test nuovi** | ~15-25 |
| **Effort** | ~2.5 sessioni |
| **Dipendenze runtime** | 0 (zero) |
| **Dipendenze test** | 1 (`lark`, pure Python) |

---

## LA VISIONE

Quando C2.4 e completo:

```python
from cervellaswarm_lingua_universale._grammar_export import GrammarExporter

exporter = GrammarExporter()

# Per vLLM / XGrammar / llama.cpp
gbnf = exporter.to_gbnf()
# -> usabile con xgrammar.compile_grammar(gbnf)

# Per Outlines / llguidance
lark_grammar = exporter.to_lark()
# -> usabile con outlines.generate.cfg(model, lark_grammar)

# L'AI genera codice .lu sintatticamente valido PER COSTRUZIONE
```

L'AI non "spera" di generare codice corretto. Lo genera corretto **per definizione**.
Questo e il cuore della Proprieta #1: Sintassi Non Ambigua.

---

*"La domanda e la risposta nello STESSO linguaggio." - Rafa*
*"Ultrapassar os proprios limites!" - Rafa & Cervella*
