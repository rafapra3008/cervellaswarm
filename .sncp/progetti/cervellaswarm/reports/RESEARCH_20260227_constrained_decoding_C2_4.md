# Constrained Decoding / Structured Output Generation for LLMs
## Research Report - C2.4 Constrained Generation

> **Data:** 2026-02-27
> **Autore:** Cervella Researcher
> **Status:** COMPLETA
> **Fonti:** 12+ consultate (GitHub, docs ufficiali, paper arxiv, blog MLSys)
> **Scopo:** Guidare implementazione C2.4 - export grammatica Lingua Universale per constrained decoding

---

## CONTESTO TECNICO

La grammatica di Lingua Universale (LU) e un parser **recursive descent LL(1)/LL(3)** con **62 produzioni EBNF**.

Struttura attuale:
- `_tokenizer.py` - 15 tipi di token (IDENT, NUMBER, STRING, COLON, PIPE, INDENT, DEDENT, ...)
- `_parser.py` - recursive descent, no external deps
- Nodi AST: `ProgramNode`, `ProtocolNode`, `AgentNode`, `RecordTypeDecl`, `VariantTypeDecl`, `UseNode`, ...

**L'obiettivo di C2.4:** esportare la grammatica LU in un formato che permette a un LLM di generare
codice `.lu` **sintatticamente valido per costruzione**, senza post-processing.

---

## 1. XGRAMMAR (MLCSys)

**URL:** https://github.com/mlc-ai/xgrammar
**Paper:** https://arxiv.org/abs/2411.15100 (MLSys 2025)
**Autori:** MLC AI (Tianqi Chen group, CMU/Shanghai)

### Formato Grammatica

XGrammar usa **GBNF** (stesso formato di llama.cpp) come formato stringa EBNF.
La grammatica viene passata come stringa a `compile_grammar(ebnf_string)`.

```python
import xgrammar as xgr

tokenizer_info = xgr.TokenizerInfo.from_huggingface(tokenizer)
grammar_compiler = xgr.GrammarCompiler(tokenizer_info)

# Tre modi di usarlo:
compiled = grammar_compiler.compile_builtin_json_grammar()
compiled = grammar_compiler.compile_json_schema(schema_string)
compiled = grammar_compiler.compile_grammar(ebnf_string)  # <-- nostro caso
```

La documentazione rimanda esplicitamente al formato GBNF di llama.cpp per la specifica sintattica.

### Integrazione con inference engines

- **vLLM**: default backend per structured outputs (da vLLM 0.8.x)
- **SGLang**: integrazione nativa
- **TensorRT-LLM**: supportato
- **llama.cpp**: GBNF e il formato nativo

### Performance

>10x piu veloce di Outlines per grammatiche complesse.
Near-zero overhead su H100 per scenari low-latency.
Divide vocab in token "context-independent" (pre-calcolabili) e "context-dependent" (runtime).

### Complessita di esportazione dalla nostra EBNF

**MEDIO-BASSA.** La nostra EBNF e gia molto pulita.
Problemi principali:
1. INDENT/DEDENT: LU usa indentazione significativa (come Python). GBNF non ha nozione di indent stack - richiede encoding alternativo (es: { } o parole chiave `begin`/`end` nel formato esportato) oppure flatten della struttura
2. Keyword-as-IDENT: nel nostro tokenizer `protocol`, `agent`, `type` sono IDENT con valore specifico. GBNF richiede literal string terminal

### Pro
- Standard de facto nel 2025/2026
- Usato da vLLM (il principale runtime open source)
- Performance eccellente
- Formato GBNF ben documentato

### Contro
- INDENT/DEDENT e il problema principale: nessun framework di constrained decoding gestisce bene le grammatiche indentation-sensitive (Pythonic)
- Richiede tokenizer HuggingFace per setup

---

## 2. LLGUIDANCE (Microsoft/guidance-ai)

**URL:** https://github.com/guidance-ai/llguidance
**Autori:** Microsoft (guidance-ai team)

### Formato Grammatica

llguidance supporta due formati:
1. **Lark-like EBNF** (formato primario dal 2024-2025)
2. **Internal JSON format** (deprecando)

Il formato Lark-like permette di embedded JSON Schema e regex dentro le regole EBNF.

```
# Esempio sintassi Lark-like llguidance:
program: declaration+
declaration: protocol_decl | agent_decl | type_decl | use_decl
protocol_decl: "protocol" IDENT ":" body
IDENT: /[a-zA-Z_][a-zA-Z0-9_]*/
```

**Tecnica interna:** Rust-based, derivative-based regex engine (derivre) + Earley parser.
Performance: ~50 microseconds CPU per token, 128K tokenizer vocabulary.

### Integrazione

- **OpenAI Structured Outputs**: OpenAI ha creditato llguidance (maggio 2025) come base del loro implementation
- **guidance Python library**: genera il formato interno
- **FuriosaAI**: usa llguidance come backend default
- **Transformers (HuggingFace)**: supportato

### Complessita di esportazione

**BASSA** per la parte grammaticale.
Stessi problemi INDENT/DEDENT di GBNF.
Il formato Lark-like e piu espressivo del GBNF puro (supporta regex inline).

### Pro
- Usato da OpenAI in produzione (validazione massima)
- Supporto regex embedded nelle regole (utile per IDENT, NUMBER, STRING)
- Formato Lark e gia familiare (Outlines usa Lark puro)
- Performance Rust-level

### Contro
- Meno diffuso a livello di runtime self-hosted rispetto a XGrammar+vLLM
- API ancora in evoluzione

---

## 3. OUTLINES (dottxt)

**URL:** https://github.com/dottxt-ai/outlines
**Autori:** .txt company (ex-Normal Computing)

### Formato Grammatica

Outlines usa **Lark EBNF nativo** (il formato della libreria Python `lark`).

```python
from outlines import models, generate

model = models.transformers("model-name")

grammar = """
    ?start: program
    program: declaration+
    declaration: protocol_decl | agent_decl
    protocol_decl: "protocol" IDENT ":" body
    IDENT: /[a-zA-Z_][a-zA-Z0-9_]*/
    %import common.NEWLINE
"""

generator = generate.cfg(model, grammar)
result = generator("Scrivi un protocollo per...")
```

### Meccanismo interno

1. Grammar compilation -> token masks
2. Prefix trees per potare percorsi invalidi durante beam search
3. Finite automata per selezione token validi

### Performance

Sub-millisecond latency per CFG-guided generation.
Nota: usa rejection sampling (greedy), non campionamento puro.

### Integrazione

- **Transformers HuggingFace**: supporto diretto
- **SGLang**: supportato
- **TGI (Text Generation Inference)**: supportato
- **vLLM**: fallback quando XGrammar non basta

### Complessita di esportazione

**LA PIU BASSA** perche Lark e gia una libreria Python (zero dipendenze nuove se la usassimo solo per export).
La conversione EBNF nostra -> Lark e quasi 1:1 per le regole non-whitespace-sensitive.

### Pro
- Il formato Lark e gia Python-native
- `generate.cfg(model, grammar)` e la API piu semplice
- Ottima documentazione
- Grammars pre-built (arithmetic, json)
- Supporto TGI e Transformers (uso locale senza vLLM)

### Contro
- Piu lento di XGrammar per grammatiche grandi
- Rejection sampling vs. vero constrained decoding (differenza semantica)
- Non default in vLLM (XGrammar ha precedenza)

---

## 4. GBNF (llama.cpp)

**URL:** https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md
**Autori:** Georgi Gerganov e community

### Formato

GBNF = "GGML BNF" - estensione di BNF con feature regex-like.

```
# Sintassi GBNF completa:
root ::= program
program ::= declaration+
declaration ::= protocol-decl | agent-decl | type-decl | use-decl
protocol-decl ::= "protocol" ws ident ws ":" ws body
agent-decl ::= "agent" ws ident ws ":" ws agent-body

# Terminal rules:
ident ::= [a-zA-Z_] [a-zA-Z0-9_]*
ws ::= [ \t\n]*
number ::= [0-9]+ ("." [0-9]+)?
string ::= "\"" [^"]* "\""

# Operatori: * + ? {m} {m,n} {m,}
# Alternativa: |
# Grouping: ()
# Character ranges: [a-z] [^abc]
# Unicode: \u0041 \U0001F600
# Token matching (unico di GBNF): <[1000]> <think>
# Commenti: # linea
```

### Differenze chiave da EBNF standard

| Feature | EBNF standard | GBNF |
|---------|---------------|------|
| Token matching | Non previsto | `<[id]>` o `<text>` |
| Non-terminal names | Qualsiasi | Dashed-lowercase (`chess-piece`) |
| Root rule | Dipende | `root` e il punto di ingresso |
| Comments | Varia | `#` |
| Negation | Varia | `[^...]` |

### Complessita esportazione

**MEDIO.** La nostra EBNF si converte abbastanza direttamente.
Bisogna:
1. Rinominare non-terminal con dashed-lowercase
2. Gestire INDENT/DEDENT (vedi problema sotto)
3. Aggiungere `root ::= program`

### Pro
- Standard de facto per llama.cpp (enorme ecosistema local LLM)
- E lo stesso formato usato internamente da XGrammar
- Tool esistenti: json-schema-to-grammar.py, tree_sitter_grammar_to_gbnf

### Contro
- Pensato per local inference (llama.cpp), non per API cloud
- Gestione whitespace piu verbosa

---

## 5. LM-FORMAT-ENFORCER

**URL:** https://github.com/noamgat/lm-format-enforcer
**Autori:** Noam Gat

### Formato

Supporta: **JSON Schema**, **JSON Mode**, **Regular Expression**.
Non supporta CFG/EBNF arbitrario in modo diretto.

### Performance e benchmark 2025

In zero-shot: 8.9% hallucination rate (molto bassa).
In two-shot: 0.7% hallucination rate (eccellente).

### Integrazione

Transformers, LangChain, LlamaIndex, llama.cpp, vLLM, Haystack, TensorRT-LLM, ExLlamaV2.

### Complessita esportazione

**ALTA** per il nostro caso. LM-format-enforcer non ha supporto diretto per CFG.
Non e adatto per esportare la nostra grammatica completa.

### Pro/Contro per C2.4

Non e la scelta giusta per esportare una grammatica di linguaggio di programmazione.
E ottimo per JSON/regex ma non per CFG complesse.

---

## 6. OPENAI STRUCTURED OUTPUTS

**URL:** https://developers.openai.com/api/docs/guides/structured-outputs/

### Come funziona

OpenAI converte JSON Schema in CFG, poi usa constrained sampling durante inference.
Internamente basato su llguidance (creditato pubblicamente maggio 2025).

### Cosa supporta

- **JSON Schema**: formato principale
- **guided_grammar con EBNF**: disponibile via parametro `guided_grammar` in alcuni endpoint
- Grammatiche via `response_format` con `json_schema`

### Disponibilita

- Claude (Anthropic): **Solo JSON Schema** (nessun EBNF arbitrario esposto nelle API pubbliche)
- OpenAI: JSON Schema + limitato EBNF
- Google Gemini: JSON Schema

### Implicazione per C2.4

Per LLM cloud (Claude, GPT-4, Gemini): l'unico formato standard e **JSON Schema**.
Se vogliamo che il nostro linguaggio sia generabile da API cloud, dobbiamo considerare
anche un export in JSON Schema (che pero non copre grammatiche indentation-sensitive).

---

## 7. IL PROBLEMA CRITICO: INDENTAZIONE

**Lingua Universale e un linguaggio indentation-sensitive (come Python).**

Nessun sistema di constrained decoding gestisce bene l'indentazione significativa.

### Perche e difficile

I sistemi CFG-based lavorano su sequenze di token. L'indentazione richiede
stato contestuale (stack di livelli) che non e esprimibile in una CFG standard.

### Soluzioni adottate da altri linguaggi

1. **Python con GBNF**: non esiste una grammatica GBNF pulita per Python completo.
   La grammatica ufficiale Python e una PEG (non CFG) per questo motivo.

2. **Approccio "flat" per LLM**: usare una versione linearizzata del linguaggio
   che usa `begin`/`end` o `{` `}` invece di indentazione.

3. **Post-filter**: generare senza constraint sull'indentazione, poi validare
   con il parser reale. Meno potente ma piu semplice.

4. **Whitespace-lenient grammar**: la grammatica LLM accetta qualsiasi whitespace
   tra token (niente INDENT/DEDENT). Il linter/formatter poi normalizza l'output.

### Raccomandazione per C2.4

**Approccio "Whitespace-Lenient"** e il piu pragmatico:

```
# Versione LLM della grammatica LU:
# Non ha INDENT/DEDENT, accetta newline/spazi liberamente
root ::= program
program ::= declaration+
declaration ::= protocol-decl | agent-decl | type-decl | use-decl

protocol-decl ::= ws "protocol" ws ident ws ":" ws "{" ws protocol-body ws "}"
# OPPURE mantieni newline ma ignora indentazione:
protocol-decl ::= ws "protocol" ws ident ws ":" ws step+
```

Oppure esportare due grammatiche:
1. **Grammatica "strict"** (con indent) per il parser ufficiale
2. **Grammatica "LLM-friendly"** (senza indent) per constrained decoding

---

## 8. BENCHMARK COMPARATIVO 2025

Da **JSONSchemaBench** (10K JSON schemas reali, 6 framework):

| Framework | Copertura Schema | Velocita | Uso Ideale |
|-----------|-----------------|----------|-----------|
| XGrammar | Alta | >10x (best) | vLLM/SGLang self-hosted |
| llguidance | Altissima | Molto alta (Rust) | OpenAI-compatible, cloud |
| Outlines | Alta | Media | HuggingFace/local |
| LM-Format-Enforcer | Media | Media | JSON/regex only |
| llama.cpp (GBNF) | Alta | Alta | Local llama |
| OpenAI SO | Altissima | N/A (cloud) | API OpenAI |

---

## 9. MAPPA DI CONVERSIONE: NOSTRA EBNF -> FORMATI

### La nostra EBNF (estratto dalle 62 produzioni)

```ebnf
program        ::= declaration*
declaration    ::= protocol_decl | agent_decl | type_decl | use_decl
protocol_decl  ::= 'protocol' IDENT ':' NEWLINE INDENT protocol_body DEDENT
agent_decl     ::= 'agent' IDENT ':' NEWLINE INDENT agent_body DEDENT
type_decl      ::= 'type' IDENT '=' variant_type | record_type
use_decl       ::= 'use' ('python')? IDENT ('as' IDENT)?
IDENT          ::= [a-zA-Z_][a-zA-Z0-9_]*
NUMBER         ::= [0-9]+ ('.' [0-9]+)?
STRING         ::= '"' [^"]* '"'
```

### Conversione in GBNF (XGrammar/llama.cpp)

```
# GBNF per LU (versione LLM-friendly, senza indent)
root ::= program
program ::= declaration+
declaration ::= ws (protocol-decl | agent-decl | type-decl | use-decl) ws
protocol-decl ::= "protocol" ws ident ws ":" ws NEWLINE protocol-body
agent-decl ::= "agent" ws ident ws ":" ws NEWLINE agent-body
type-decl ::= "type" ws ident ws "=" ws (variant-type | record-type)
use-decl ::= "use" ws ("python" ws)? ident (ws "as" ws ident)?
ident ::= [a-zA-Z_] [a-zA-Z0-9_]*
number ::= [0-9]+ ("." [0-9]+)?
string ::= "\"" [^"]* "\""
ws ::= [ \t\n\r]*
NEWLINE ::= "\n"
```

### Conversione in Lark (Outlines/llguidance)

```
?start: program
program: declaration+
declaration: protocol_decl | agent_decl | type_decl | use_decl
protocol_decl: "protocol" IDENT ":" body
agent_decl: "agent" IDENT ":" agent_body
type_decl: "type" IDENT "=" (variant_type | record_type)
use_decl: "use" ("python")? IDENT ("as" IDENT)?
IDENT: /[a-zA-Z_][a-zA-Z0-9_]*/
NUMBER: /[0-9]+(\.[0-9]+)?/
STRING: /"[^"]*"/
%import common.WS
%ignore WS
```

### Difficolta stimate per implementazione

| Aspetto | Difficolta | Note |
|---------|-----------|------|
| Regole base (protocol, agent, type, use) | BASSA | Conversione quasi 1:1 |
| Terminal (IDENT, NUMBER, STRING) | BASSA | Regex diretta |
| Keyword come literal string | BASSA | "protocol" invece di IDENT |
| INDENT/DEDENT | ALTA | Non convertibile direttamente |
| Espressioni (BinOp, AttrExpr) | MEDIA | Ricorsione da gestire |
| Choice/Branch in protocol body | MEDIA | Alternativa con `|` |
| Properties (requires/ensures) | MEDIA | Struttura annidata |

---

## 10. RACCOMANDAZIONE FINALE

### Formato primario: GBNF (XGrammar-compatible)

**Perche GBNF:**
1. E il formato accettato da `xgr.GrammarCompiler.compile_grammar()`
2. vLLM usa XGrammar come default - copre il 90% dei deployment self-hosted
3. E lo stesso formato di llama.cpp - copre tutto il mondo local LLM
4. Conversione dalla nostra EBNF e diretta per le parti non-indent

### Formato secondario: Lark (Outlines-compatible)

**Perche Lark come secondo:**
1. Outlines e il fallback di vLLM quando XGrammar non basta
2. llguidance (Microsoft/OpenAI) usa formato Lark-like
3. `lark` e gia una libreria Python matura, il formato e ben specificato
4. Una grammatica Lark si converte facilmente a GBNF (e viceversa)

### Cosa NON fare

- NON tentare di esportare con INDENT/DEDENT nel formato constrained: nessun sistema lo supporta bene
- NON limitarsi a JSON Schema: non copre un linguaggio di programmazione
- NON usare lm-format-enforcer per questo use case

### Piano implementazione C2.4

```
C2.4.1 - STUDIO (questa ricerca, fatto)
  - Capire i formati: GBNF, Lark, llguidance
  - Identificare il problema INDENT/DEDENT

C2.4.2 - Design "LLM Grammar" (separata dalla "Parser Grammar")
  - La grammatica LLM non ha INDENT/DEDENT
  - Usa whitespace-lenient + struttura piu flat
  - Documentata separatamente nella nuova "LLM grammar spec"

C2.4.3 - Implementazione GrammarExporter
  - Classe `GrammarExporter` in un nuovo `_grammar_export.py`
  - Metodi:
    - `to_gbnf() -> str` (GBNF string)
    - `to_lark() -> str` (Lark EBNF string)
    - `to_json_schema() -> dict` (per API cloud, limitato)
  - Input: le 62 produzioni EBNF gia note (hard-coded o da AST del parser)

C2.4.4 - Test + Validazione
  - Test: GBNF generato e parsabile da llama.cpp (syntax check)
  - Test: Lark generato e parsabile da libreria `lark` (syntax check)
  - Golden test: XGrammar compile_grammar(our_gbnf) non crasha
  - Guardiana audit

C2.4.5 - Demo End-to-End (opzionale per C2.4, potrebbe essere C3)
  - Caricare il GBNF in XGrammar/vLLM
  - Chiedere a un LLM di generare codice .lu
  - Verificare che parse(output) non dia ParseError
```

### Note sulle dipendenze

**Zero nuove dipendenze** per l'exporter stesso.
Le grammatiche GBNF e Lark sono semplici file di testo.
L'esportatore scrive stringhe Python - nessuna dipendenza.

Per i test di validazione:
- `lark` (gia nel Python ecosystem, potrebbe essere test-only)
- `xgrammar` (test-only, non nel package principale)

Seguire la regola "0 dipendenze runtime" del progetto: le dipendenze di test sono ok.

---

## FONTI CONSULTATE

1. XGrammar GitHub: https://github.com/mlc-ai/xgrammar
2. XGrammar paper (MLSys 2025): https://arxiv.org/abs/2411.15100
3. XGrammar blog MLC: https://blog.mlc.ai/2024/11/22/achieving-efficient-flexible-portable-structured-generation-with-xgrammar
4. llguidance GitHub: https://github.com/guidance-ai/llguidance
5. Outlines GitHub: https://github.com/dottxt-ai/outlines
6. Outlines CFG docs: https://dottxt-ai.github.io/outlines/reference/generation/cfg/
7. GBNF README: https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md
8. lm-format-enforcer: https://github.com/noamgat/lm-format-enforcer
9. vLLM Structured Outputs: https://docs.vllm.ai/en/latest/features/structured_outputs/
10. OpenAI Structured Outputs: https://developers.openai.com/api/docs/guides/structured-outputs/
11. Constrained Decoding overview: https://mbrenndoerfer.com/writing/constrained-decoding-structured-llm-output
12. JSONSchemaBench (benchmark 2025): https://arxiv.org/html/2501.10868v1

---

*Cervella Researcher - CervellaSwarm*
*"Ricerca PRIMA di implementare."*
