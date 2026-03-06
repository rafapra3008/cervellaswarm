# DESIGN C2.4.1 -- LLM Grammar per Lingua Universale

> **Sessione:** 419
> **Data:** 2026-02-27
> **Autore:** Cervella Regina
> **Prerequisiti:** EBNF 62 produzioni (C1.2), STUDIO C2.4, RESEARCH GBNF+Lark
> **Fonti ricerca:** 14 fonti (GBNF spec, XGrammar, Outlines, llguidance, Lark docs)

---

## IL CONCETTO

La LLM Grammar e una versione **whitespace-lenient** della grammatica EBNF di Lingua
Universale. Serve per il constrained decoding: un LLM genera codice .lu che e
**sintatticamente valido per costruzione**.

```
Parser Grammar (62 produzioni, strict):
  protocol_decl ::= 'protocol' IDENT ':' NEWLINE INDENT protocol_body DEDENT
  ^^^^^ richiede token INDENT/DEDENT dal tokenizer

LLM Grammar (47 regole, lenient):
  protocol-decl ::= "protocol" ws1 ident ws ":" ws protocol-body
  ^^^^^ usa whitespace libero, struttura guidata da keyword
```

**Pipeline completa:**
1. LLM genera codice usando la LLM Grammar (whitespace-lenient)
2. Il parser ufficiale valida e corregge l'indentazione
3. Il compilatore (C2) produce Python eseguibile

---

## DECISIONI DI DESIGN

| # | Decisione | Alternativa scartata | Perche |
|---|-----------|---------------------|--------|
| D1 | Whitespace-lenient (no INDENT/DEDENT) | Indent-sensitive | INDENT/DEDENT impossibili in CFG (fondamentale, non limite tool) |
| D2 | Closed list per verb e noun | Open IDENT | Zero hallucination, allineato al parser ufficiale, solo 5+9 keyword |
| D3 | `ws ::= [ \t\n\r]*` per spazi | `ws ::= " "*` | Standard de facto GBNF (llama.cpp, XGrammar), piu permissivo |
| D4 | `ws1 ::= [ \t]+` per separatori obbligatori | Solo `ws` | Previene merge di token adiacenti: `protocolX` vs `protocol X` |
| D5 | Keyword-as-delimiter per blocchi | Marker espliciti `{}`/`end` | Consistente con la sintassi LU, l'LLM impara la struttura dal training |
| D6 | Lark: `%ignore /\s+/` + `%ignore /#[^\n]*/` | `_NL` per newline | Piu semplice, robusta, compatibile Outlines + llguidance |
| D7 | `comment` rule in GBNF | Omettere commenti | L'LLM potrebbe generare commenti utili |

---

## GRAMMATICA GBNF COMPLETA

```gbnf
# ============================================================
# Lingua Universale - LLM Grammar (GBNF)
# Target: XGrammar, vLLM, llama.cpp
# Versione: 1.0 (C2.4.1, S419)
# Regole: 47 (da 62 produzioni EBNF, whitespace-lenient)
# ============================================================

# ---- 1. TOP LEVEL ----

root           ::= ws program ws

program        ::= declaration+

declaration    ::= protocol-decl
                 | agent-decl
                 | type-decl
                 | use-decl
                 | comment

# ---- 2. PROTOCOL ----

protocol-decl  ::= "protocol" ws1 ident ws ":" ws protocol-body

protocol-body  ::= roles-clause step-or-choice+ properties-block?

roles-clause   ::= "roles" ws ":" ws ident-list ws

step-or-choice ::= step | choice-block

step           ::= ident ws1 action ws

action         ::= "asks" ws1 ident ws1 "to" ws1 verb
                 | "returns" ws1 noun ws1 "to" ws1 ident
                 | "tells" ws1 ident ws1 noun
                 | "proposes" ws1 noun ws1 "to" ws1 ident
                 | "sends" ws1 noun ws1 "to" ws1 ident

verb           ::= "do" ws1 "task"
                 | "verify"
                 | "plan"
                 | "research"
                 | "shutdown"

noun           ::= "result"
                 | "verdict"
                 | "plan"
                 | "decision"
                 | "report"
                 | "message"
                 | "broadcast"
                 | "context"
                 | "ack"

choice-block   ::= "when" ws1 ident ws1 "decides" ws ":" ws branch+

branch         ::= ident ws ":" ws step+

# ---- 3. PROPERTIES ----

properties-block ::= "properties" ws ":" ws property+

property       ::= "always" ws1 "terminates"
                 | "no" ws1 "deadlock"
                 | ident ws1 "before" ws1 ident
                 | ident ws1 "cannot" ws1 "send" ws1 ident
                 | "confidence" ws ">=" ws confidence-level
                 | "trust" ws ">=" ws trust-tier
                 | "all" ws1 "roles" ws1 "participate"

confidence-level ::= "certain"
                   | "high"
                   | "medium"
                   | "low"
                   | "speculative"

trust-tier     ::= "verified"
                 | "trusted"
                 | "standard"
                 | "untrusted"

# ---- 4. AGENT ----

agent-decl     ::= "agent" ws1 ident ws ":" ws agent-body

agent-body     ::= agent-clause+

agent-clause   ::= "role" ws ":" ws ident
                 | "trust" ws ":" ws trust-tier
                 | "accepts" ws ":" ws ident-list
                 | "produces" ws ":" ws ident-list
                 | requires-clause
                 | ensures-clause

# ---- 5. CONTRACTS (requires / ensures) ----

requires-clause ::= "requires" ws ":" ws condition+

ensures-clause  ::= "ensures" ws ":" ws condition+

condition      ::= expr ws

# ---- 6. EXPRESSIONS ----

expr           ::= or-expr

or-expr        ::= and-expr (ws1 "or" ws1 and-expr)*

and-expr       ::= not-expr (ws1 "and" ws1 not-expr)*

not-expr       ::= "not" ws1 not-expr
                 | comparison

comparison     ::= primary (ws comparison-op ws primary)?

comparison-op  ::= "==" | "!=" | "<=" | ">=" | "<" | ">"

primary        ::= ident "." ident "(" args? ")"
                 | ident "." ident
                 | ident
                 | number
                 | string
                 | "(" ws expr ws ")"

args           ::= expr (ws "," ws expr)*

# ---- 7. TYPES ----

type-decl      ::= "type" ws1 ident ws "=" ws type-body

type-body      ::= variant-type | record-type

variant-type   ::= ident (ws "|" ws ident)+

record-type    ::= field+

field          ::= ident ws ":" ws type-expr ws

type-expr      ::= base-type "?"?

base-type      ::= ident "[" ws type-expr ws "]"
                 | ident

# ---- 8. USE (Python import) ----

use-decl       ::= "use" ws1 "python" ws1 dotted-name (ws1 "as" ws1 ident)?

dotted-name    ::= ident ("." ident)*

# ---- 9. COMMON ----

ident-list     ::= ident (ws "," ws ident)*

# ---- 10. TERMINALS ----

ident          ::= [a-zA-Z_] [a-zA-Z0-9_]*

number         ::= [0-9]+ ("." [0-9]+)?

string         ::= "\"" [^"\n]* "\""
                 | "'" [^'\n]* "'"

comment        ::= "#" [^\n]*

ws             ::= [ \t\n\r]*

ws1            ::= [ \t\n]+
```

**Conteggio regole: 47** (target ~50, da 62 EBNF)

### Mapping EBNF -> GBNF: cosa e cambiato

| EBNF (62 regole) | GBNF (47 regole) | Cambiamento |
|-------------------|-------------------|-------------|
| `INDENT` / `DEDENT` | `ws` | Rimossi (impossibili in CFG) |
| `NEWLINE` | `ws` (assorbito) | Newline opzionale, non obbligatorio. STUDIO C2.4 proponeva `newline ::= "\n" ws` separata; assorbita in `ws` per semplicita |
| `ident_list` | `ident-list` | Dashed-lowercase naming |
| `message_list` | `ident-list` | Merged: struttura identica a `ident_list` (`IDENT (',' IDENT)*`) |
| `program ::= declaration*` | `program ::= declaration+` | Almeno 1 decl (piu utile per LLM) |
| `step ::= IDENT action NEWLINE` | `step ::= ident ws1 action ws` | NEWLINE -> ws |
| `condition ::= expr NEWLINE` | `condition ::= expr ws` | NEWLINE -> ws |
| `requires_clause` (2 alt: block+inline) | `requires-clause` (1 regola) | Fusione: `ws` assorbe newline, una sola regola copre entrambe le forme (superset lenient) |
| `ensures_clause` (2 alt: block+inline) | `ensures-clause` (1 regola) | Idem: fusione block+inline in regola unica |
| -- | `type-body` | Nuova regola intermedia: `variant-type \| record-type` (refactoring, riduce duplicazione in `type-decl`) |
| Terminali separati (GTE, LTE...) | Inline in `comparison-op` | Merged (meno regole) |
| -- | `comment` | Aggiunto in GBNF (LLM puo generare commenti). In Lark: gestito via `%ignore /#[^\n]*/` (non serve come regola, asimmetria intenzionale) |
| `STRING ::= '"' [^"]* '"'` | `string ::= "\"" [^"\n]* "\""` | Restrizione: no newline nelle stringhe (piu sicuro per LLM generation). Allineato GBNF e Lark |

---

## GRAMMATICA LARK COMPLETA

```lark
# ============================================================
# Lingua Universale - LLM Grammar (Lark EBNF)
# Target: Outlines, llguidance
# Versione: 1.0 (C2.4.1, S419)
# Regole: 40 rules + 4 terminals + 2 directives = 46 (whitespace-lenient)
# ============================================================

# ---- 1. TOP LEVEL ----

?start: program

program: declaration+

declaration: protocol_decl
           | agent_decl
           | type_decl
           | use_decl

# ---- 2. PROTOCOL ----

protocol_decl: "protocol" IDENT ":" protocol_body

protocol_body: roles_clause step_or_choice+ properties_block?

roles_clause: "roles" ":" ident_list

step_or_choice: step | choice_block

step: IDENT action

action: "asks" IDENT "to" verb
      | "returns" noun "to" IDENT
      | "tells" IDENT noun
      | "proposes" noun "to" IDENT
      | "sends" noun "to" IDENT

verb: "do" "task"
    | "verify"
    | "plan"
    | "research"
    | "shutdown"

noun: "result"
    | "verdict"
    | "plan"
    | "decision"
    | "report"
    | "message"
    | "broadcast"
    | "context"
    | "ack"

choice_block: "when" IDENT "decides" ":" branch+

branch: IDENT ":" step+

# ---- 3. PROPERTIES ----

properties_block: "properties" ":" property+

property: "always" "terminates"
        | "no" "deadlock"
        | IDENT "before" IDENT
        | IDENT "cannot" "send" IDENT
        | "confidence" ">=" confidence_level
        | "trust" ">=" trust_tier
        | "all" "roles" "participate"

confidence_level: "certain"
                | "high"
                | "medium"
                | "low"
                | "speculative"

trust_tier: "verified"
          | "trusted"
          | "standard"
          | "untrusted"

# ---- 4. AGENT ----

agent_decl: "agent" IDENT ":" agent_body

agent_body: agent_clause+

agent_clause: "role" ":" IDENT
            | "trust" ":" trust_tier
            | "accepts" ":" ident_list
            | "produces" ":" ident_list
            | requires_clause
            | ensures_clause

# ---- 5. CONTRACTS ----

requires_clause: "requires" ":" condition+

ensures_clause: "ensures" ":" condition+

condition: expr

# ---- 6. EXPRESSIONS ----

expr: or_expr

or_expr: and_expr ("or" and_expr)*

and_expr: not_expr ("and" not_expr)*

not_expr: "not" not_expr
        | comparison

comparison: primary (COMP_OP primary)?

primary: IDENT "." IDENT "(" args? ")"
       | IDENT "." IDENT
       | IDENT
       | NUMBER
       | STRING
       | "(" expr ")"

args: expr ("," expr)*

# ---- 7. TYPES ----

type_decl: "type" IDENT "=" type_body

type_body: variant_type | record_type

variant_type: IDENT ("|" IDENT)+

record_type: field+

field: IDENT ":" type_expr

type_expr: base_type "?"?

base_type: IDENT "[" type_expr "]"
         | IDENT

# ---- 8. USE ----

use_decl: "use" "python" dotted_name ("as" IDENT)?

dotted_name: IDENT ("." IDENT)*

# ---- 9. COMMON ----

ident_list: IDENT ("," IDENT)*

# ---- 10. TERMINALS ----

IDENT: /[a-zA-Z_][a-zA-Z0-9_]*/
NUMBER: /[0-9]+(\.[0-9]+)?/
STRING: /"[^"\n]*"/ | /'[^'\n]*'/
COMP_OP: ">=" | "<=" | "==" | "!=" | ">" | "<"

# ---- 11. WHITESPACE & COMMENTS ----

%ignore /\s+/
%ignore /#[^\n]*/
```

**Conteggio: 40 regole + 4 terminali + 2 direttive = 46** (Lark non ha ws/ws1 perche `%ignore` gestisce whitespace)

---

## VALIDAZIONE DEL DESIGN

### Checklist (dalla ricerca)

- [x] GBNF: ogni non-terminal usa dashed-lowercase (`protocol-decl`, `ws1`)
- [x] GBNF: la regola `root` e definita come prima
- [x] GBNF: nessun `x? x? x?` in serie
- [x] Lark: ogni terminale lessicale e UPPERCASE (`IDENT`, `NUMBER`, `STRING`, `COMP_OP`)
- [x] Lark: ogni struttura e lowercase (`protocol_decl`, `step`)
- [x] Lark: literal `"protocol"` ha priorita automatica su `IDENT` (no conflitto)
- [x] Entrambi: `verb` e `noun` come closed list
- [x] Entrambi: nessun INDENT/DEDENT
- [x] GBNF: `ws` prima/dopo keyword dove permesso
- [x] Lark: `%ignore /\s+/` in fondo

### Mapping 10 Esempi Canonici -> LLM Grammar

Ogni esempio dal DESIGN_C1_2 e parsabile dalla LLM Grammar senza modifiche,
perche la grammatica e un superset (accetta whitespace libero):

| Esempio | Costrutti usati | Parsabile GBNF | Parsabile Lark |
|---------|-----------------|----------------|----------------|
| 1. DelegateTask | protocol, step, properties | Si | Si |
| 2. PlanAndBuild | protocol, step, choice, properties | Si | Si |
| 3. Worker agent | agent, requires, ensures | Si | Si |
| 4. AnalysisResult | type (record), Confident[T] | Si | Si |
| 5. TaskStatus | type (variant) | Si | Si |
| 6. Import Python | use python, agent, requires, ensures | Si | Si |
| 7. SecureAudit | protocol, properties (trust, cannot send) | Si | Si |
| 8. RecipeApp | protocol + agent combinati | Si | Si |
| 9. DeepResearch | type + protocol + properties | Si | Si |
| 10. CodeReview | use + type + protocol + agent (multi) | Si | Si |

### Keyword Ambiguity: "plan"

Verificato: il contesto sintattico disambigua SEMPRE:
- `to plan` -> verb (dopo `asks IDENT to`)
- `returns plan to` -> noun (dopo `returns`)
- `proposes plan to` -> noun (dopo `proposes`)

Zero conflitto in GBNF (context-free) e Lark LALR(1).

---

## PROSSIMO STEP

C2.4.2 -- GrammarExporter implementation:
- `_grammar_export.py` con classe `GrammarExporter`
- `to_gbnf() -> str` che emette la grammatica GBNF sopra
- `to_lark() -> str` che emette la grammatica Lark sopra
- Le regole sono codificate staticamente (no parsing di _parser.py)
- ~200-300 LOC stimati

---

*"La domanda e la risposta nello STESSO linguaggio." - Rafa*
*"Ultrapassar os proprios limites!" - Rafa & Cervella*
