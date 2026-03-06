# RESEARCH - GBNF & Lark: Grammar Design per Constrained Decoding
## Best Practices per Lingua Universale C2.4.1

> **Data:** 2026-02-27
> **Autore:** Cervella Researcher
> **Status:** COMPLETA
> **Fonti:** 14 consultate (spec ufficiali, docs, esempi reali, paper)
> **Scopo:** Guida pratica per scrivere le ~50 regole GBNF e ~50 Lark per C2.4.1
> **Prerequisito:** Leggere `RESEARCH_20260227_constrained_decoding_C2_4.md` (panorama generale)

---

## SEZIONE 1: GBNF - Specifica Completa

### 1.1 - Sintassi di base

**Formato:** `nonterminal-name ::= sequence`

Regole principali:
- I non-terminal DEVONO essere dashed-lowercase: `protocol-decl`, `ident-list`, `ws`
- Il punto di ingresso DEVE chiamarsi `root`
- I terminal sono caratteri literali o range: `"hello"`, `[a-z]`, `[^"\n]`
- I commenti usano `#`

```gbnf
# Esempio struttura minima valida GBNF
root ::= declaration+
declaration ::= "protocol" ws ident ws ":" ws body
ident ::= [a-zA-Z_] [a-zA-Z0-9_]*
ws ::= [ \t\n]*
body ::= "..." ws
```

**Fonte:** https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md

---

### 1.2 - Tutti gli operatori GBNF

| Operatore | Significato | Esempio |
|-----------|-------------|---------|
| `\|` | Alternativa (OR) | `a \| b \| c` |
| `()` | Raggruppamento | `("a" \| "b") "c"` |
| `*` | Zero o piu | `ws*` |
| `+` | Uno o piu | `declaration+` |
| `?` | Zero o uno (opzionale) | `("as" ws ident)?` |
| `{m}` | Esattamente m volte | `[0-9]{4}` |
| `{m,n}` | Da m a n volte | `[0-9]{1,3}` |
| `{m,}` | Almeno m volte | `[a-z]{2,}` |
| `{0,n}` | Al piu n volte | `[0-9]{0,20}` |

**ATTENZIONE - Gotcha performance:** Non usare `x? x? x? x?` (N opzionali in serie) - causa sampling lentissimo. Usare `x{0,N}` invece.

**Fonte:** GBNF README llama.cpp

---

### 1.3 - Whitespace in GBNF: il pattern `ws`

Il pattern standard de facto usato in tutti i grammari GBNF reali:

```gbnf
# Pattern ws STANDARD (dalle grammatiche ufficiali llama.cpp):
ws ::= [ \t\n\r]*
```

Come si usa nella pratica (dal JSON grammar ufficiale llama.cpp):

```gbnf
# Dal grammar JSON ufficiale llama.cpp:
space ::= | " " | "\n" [ \t]{0,20}
array ::= "[" space (value ("," space value)*)? "]" space
object ::= "{" space (string ":" space value ("," space string ":" space value)*)? "}" space
```

**Pattern per LU - whitespace lenient tra costrutti:**

```gbnf
# ws tra keyword e ident:
protocol-decl ::= "protocol" ws ident ws ":" ws protocol-body

# ws opzionale tra ogni token:
step ::= ws ident ws action ws newline

# newline come separatore (opzionale per LLM):
newline ::= "\n" ws
```

**Tre varianti di ws per LU:**

```gbnf
# 1. Whitespace orizzontale (spazi e tab):
sp ::= [ \t]*

# 2. Whitespace qualsiasi (piu permissivo, raccomandato):
ws ::= [ \t\n\r]*

# 3. Almeno un whitespace (per separare token adiacenti):
ws1 ::= [ \t]+
```

**Fonte:** GBNF README + JSON grammar examples llama.cpp

---

### 1.4 - Stringhe ed escape in GBNF

```gbnf
# Stringa semplice (senza escape interni):
string-simple ::= "\"" [^"]* "\""

# Stringa con escape completi (pattern dal JSON grammar ufficiale):
char ::= [^"\\\x7F\x00-\x1F] | [\\] (["\\bfnrt] | "u" [0-9a-fA-F]{4})
string ::= "\"" char* "\""

# Per LU: le stringhe sono semplici (solo [^"]*):
lu-string ::= "\"" [^"\n]* "\""
            | "'" [^'\n]* "'"
```

**Escape nei literal GBNF (dentro le regole stesse):**
- `\n` = newline
- `\t` = tab
- `\r` = carriage return
- `\xXX` = byte hex (es: `\x00` = null, `\x7F` = DEL)
- `\uXXXX` = Unicode 16-bit
- `\UXXXXXXXX` = Unicode 32-bit

**Fonte:** GBNF README ufficiale

---

### 1.5 - Cosa NON si puo esprimere in GBNF

GBNF e una grammatica context-free. Non puo esprimere:

| Feature | Motivo | Alternativa per LU |
|---------|--------|-------------------|
| **INDENT/DEDENT** | Richiede stack contestuale (context-sensitive) | Grammatica whitespace-lenient senza indent |
| Unicita (`uniqueItems`) | Richiede memoria traversale | Post-validation |
| Riferimenti incrociati (es: variabile usata = variabile dichiarata) | Context-sensitive | Semantic analysis separata |
| `not` logico su interi sottoalternative | Non esprimibile in CFG | Negativi su char class `[^...]` ok, non su regole |
| Ripetizioni contestuali (es: `{N}` dove N dipende dal contesto) | Context-sensitive | Non applicabile per LU |
| Backreferences (`\1`) | Fuori CFG | Non necessario per LU |
| Lookahead/lookbehind regex | Non parte di CFG | Non necessario per LU |

**Conseguenza per LU:** INDENT e DEDENT sono IMPOSSIBILI in GBNF. La LLM Grammar deve essere whitespace-lenient.

**Fonte:** llama.cpp docs + paper "Python is not context-free" (UNC)

---

### 1.6 - XGrammar: standard GBNF senza estensioni

XGrammar usa esattamente il formato GBNF di llama.cpp. Dal codice sorgente XGrammar:

```python
# XGrammar usa Grammar.from_ebnf() che segue la spec GBNF:
grammar = Grammar.from_ebnf(ebnf_string, root_rule_name="root")

# XGrammar supporta anche combinazioni:
grammar = Grammar.concat(g1, g2)   # sequenza
grammar = Grammar.union(g1, g2)    # alternativa
grammar = Grammar.builtin_json_grammar()  # built-in
```

**XGrammar NON aggiunge estensioni** al formato GBNF base. Qualsiasi grammatica GBNF valida per llama.cpp funziona in XGrammar.

**L'unica differenza pratica:** XGrammar compila la grammatica in una rappresentazione interna ottimizzata (pushdown automaton). Grammatiche con token matching (`<think>`) potrebbero non essere rilevanti per il nostro use case.

**Fonte:** https://xgrammar.mlc.ai/docs/api/python/grammar.html

---

## SEZIONE 2: Lark EBNF - Sintassi Completa

### 2.1 - Struttura di una grammatica Lark

```lark
# Regole (lowercase) = struttura del parse tree
rule_name: item1 item2 | alternative

# Terminali (UPPERCASE) = pattern lessicali (regex)
TERMINAL_NAME: /regex/ | "literal" | "a".."z"

# Direttive
%import common.WS
%import common.NEWLINE
%ignore WS
%ignore /\s+/
```

**Differenza critica:**
- **Terminali UPPERCASE** = compilati in regex, non ricorsivi, piu veloci
- **Regole lowercase** = struttura del tree, possono essere ricorsive

---

### 2.2 - Operatori Lark

| Operatore | Significato | Esempio |
|-----------|-------------|---------|
| `\|` | Alternativa | `rule: a \| b` |
| `item?` | Opzionale | `property?` |
| `item*` | Zero o piu | `declaration*` |
| `item+` | Uno o piu | `step+` |
| `item ~ n` | Esattamente n | `IDENT ~ 2` |
| `item ~ n..m` | Da n a m | `IDENT ~ 1..3` |
| `[item]` | Opzionale (con placeholder) | `[properties_block]` |
| `(item1 item2)` | Raggruppamento | `("a" "b")` |

---

### 2.3 - Whitespace in Lark: `%ignore`, `WS`, `_NL`

**Modo 1: Ignora tutto il whitespace** (piu semplice, raccomandato per LLM grammar):

```lark
%import common.WS
%ignore WS
```

**Modo 2: Whitespace significativo** (per parsing reale indent-sensitive):

```lark
# Per indent-sensitive (NON usare per LLM grammar):
_NL: /(\r?\n[\t ]*)+/
_INDENT: _NL /\t/+   # oppure gestito da Indenter
_DEDENT: _NL
```

**Modo 3: Pattern misto** (raccomandato per LU LLM grammar):

```lark
# Ignora spazi/tab ma mantieni newline opzionali come separatori:
%ignore /[ \t]+/
_NL: /\r?\n\s*/
```

**Pattern dal tutorial JSON ufficiale Lark:**

```lark
?value: dict | list | string | SIGNED_NUMBER -> number
      | "true" -> true | "false" -> false | "null" -> null

list: "[" [value ("," value)*] "]"
dict: "{" [pair ("," pair)*] "}"
pair: string ":" value
string: ESCAPED_STRING

%import common.ESCAPED_STRING
%import common.SIGNED_NUMBER
%import common.WS
%ignore WS
```

**Fonte:** https://lark-parser.readthedocs.io/en/stable/json_tutorial.html

---

### 2.4 - Terminali disponibili in `%import common`

I piu utili per LU:

| Terminale | Pattern | Uso |
|-----------|---------|-----|
| `WS` | `/\s+/` | Whitespace generico |
| `WS_INLINE` | `/[^\S\r\n]+/` | Spazi/tab senza newline |
| `NEWLINE` | `/\r?\n[\t ]*/` | Newline con indent |
| `SIGNED_NUMBER` | intero o float con segno | Numeri |
| `ESCAPED_STRING` | stringa con escape | String literals |
| `CNAME` | `/[a-zA-Z_]\w*/` | Identificatori C-style |
| `SH_COMMENT` | `/#[^\n]*/` | Commenti shell-style |

**Alternativa per LU:** Non importare, definire i propri terminali:

```lark
IDENT: /[a-zA-Z_][a-zA-Z0-9_]*/
NUMBER: /[0-9]+(\.[0-9]+)?/
STRING: /"[^"]*"/ | /'[^']*'/
COMMENT: /#[^\n]*/
%ignore COMMENT
%ignore /[ \t]+/
```

**Fonte:** https://lark-parser.readthedocs.io/en/latest/grammar.html

---

### 2.5 - Outlines vs llguidance: differenze pratiche

| Feature | Outlines | llguidance |
|---------|----------|------------|
| Parser | LALR(1) | Earley-based (Rust) |
| Ambiguita | NON tollera | Tollera meglio |
| Lookahead regex | NO (via interegular FSM) | NO (usa Rust regex crate) |
| Backreferences | NO | NO |
| Template Lark | NO | NO |
| `%import` | Solo `%import common` | Solo `%import common` |
| Regex con `?` lazy | NO | NO |
| Priorita terminali | SI | NO |
| Errore ambiguita | `GrammarError: Reduce/Reduce` | Gestisce meglio |
| Terminali UPPERCASE | Necessari | Necessari |
| Regole lowercase | Obbligatorie | Obbligatorie |

**Regola critica per entrambi:** mai un terminale UPPERCASE e una regola lowercase che possono matchare la stessa stringa (causa Reduce/Reduce collision in LALR).

Esempio del problema:

```lark
# SBAGLIATO: IDENT e keyword matchano le stesse string
IDENT: /[a-zA-Z_][a-zA-Z0-9_]*/
rule: IDENT | "protocol"  # "protocol" e matchato sia da IDENT che dal literal
```

**Fonte:** Outlines docs + llguidance docs

---

### 2.6 - Pattern per grammatiche indent-insensitive in Lark

Per una LLM grammar che ignora l'indentazione:

```lark
# Opzione A: Ignora tutto il whitespace inclusi newline
%ignore /\s+/

# Opzione B: Mantieni newline come separatore opzionale
_NL: /\r?\n\s*/
%ignore /[ \t]+/

# Opzione C: Whitespace inline ignorato, newline opzionale nelle regole
step: IDENT action _NL?
%ignore /[ \t]+/
```

**Raccomandazione per LU:** Opzione A e la piu semplice e robusta per la LLM grammar. Se si vuole mantenere il newline come separatore visivo (ma non obbligatorio), Opzione B.

---

## SEZIONE 3: Design Patterns

### 3.1 - Conversione indent-based -> whitespace-lenient

Il problema: LU usa `INDENT`/`DEDENT` (come Python). I sistemi CFG non lo supportano.

**Strategia "Keyword as Delimiter"** (raccomandato per LU):

Il corpo di ogni costrutto e delimitato IMPLICITAMENTE dalla prossima keyword di livello superiore. La struttura e guidata dalle keyword, non dall'indentazione.

```gbnf
# LU EBNF (strict, con indent):
protocol_decl ::= 'protocol' IDENT ':' NEWLINE INDENT protocol_body DEDENT

# LLM Grammar (lenient):
# INDENT/DEDENT sostituiti da ws. Il body termina alla prossima keyword top-level.
# La struttura e: "protocol" ident ":" {step}+ (properties)?
protocol-decl ::= ws "protocol" ws ident ws ":" ws protocol-body ws

# protocol-body si conclude implicitamente quando incontra agent/protocol/type/use o EOF
protocol-body ::= roles-clause (step | choice-block)+ properties-block?
```

**Pattern equivalente in Lark:**

```lark
protocol_decl: "protocol" IDENT ":" protocol_body
protocol_body: roles_clause (step | choice_block)+ properties_block?

%ignore /\s+/
```

**Perche funziona:** I keyword top-level (`protocol`, `agent`, `type`, `use`) sono sufficientemente distinti da IDENT usati nei corpi. L'LLM "capisce" la struttura dall'indentazione nel training data, la grammatica la vincola tramite sequenza di keyword.

**Fonte:** Approccio usato da James Randall per assembly GBNF + analisi sistemi constrained decoding

---

### 3.2 - Closed list vs open IDENT: tradeoff

**CASO LU:** `verb` e `noun` sono closed list vs open IDENT.

Dalla grammatica EBNF:
```ebnf
verb ::= 'do' 'task' | 'verify' | 'plan' | 'research' | 'shutdown'
noun ::= 'result' | 'verdict' | 'plan' | 'decision' | 'report' | 'message' | 'broadcast' | 'context' | 'ack'
```

| Approccio | Vantaggi | Svantaggi |
|-----------|----------|-----------|
| **Closed list** (literal string) | Semanticamente preciso, zero hallucination, conforme alla spec | LLM ha meno liberta espressiva, deve conoscere le keyword |
| **Open IDENT** | LLM puo usare nomi naturali, piu flessibile | LLM potrebbe inventare verb/noun non esistenti, richiede post-validation |
| **Ibrido** (closed list + IDENT fallback) | Bilanciato | Aumenta ambiguita per parser LALR |

**Raccomandazione per LU:** Usare **closed list** per `verb` e `noun`.

Motivazioni:
1. LU ha solo 5 verbi e 9 nomi: l'LLM con constrained decoding impara esattamente quali sono
2. L'obiettivo e zero hallucination sintattica: closed list lo garantisce
3. I keyword LU sono token-efficienti (singole parole, no multi-token)
4. Il GBNF e Lark gestiscono la priorita: literal `"plan"` ha priorita su IDENT
5. Il parser ufficiale di LU accetta solo la closed list: la LLM grammar deve allinearvisi

**Pattern per `verb` e `noun` in GBNF:**

```gbnf
# Closed list: efficiente e preciso
verb ::= ws ("do" ws "task" | "verify" | "plan" | "research" | "shutdown") ws
noun ::= ws ("result" | "verdict" | "plan" | "decision" | "report" | "message" | "broadcast" | "context" | "ack") ws
```

**Pattern in Lark:**

```lark
# Terminali per keyword (priorita implicita sui literal):
VERB: "do task" | "verify" | "plan" | "research" | "shutdown"
NOUN: "result" | "verdict" | "plan" | "decision" | "report" | "message" | "broadcast" | "context" | "ack"

# Oppure come regole inline:
verb: "do" "task" | "verify" | "plan" | "research" | "shutdown"
noun: "result" | "verdict" | "plan" | "decision" | "report" | "message" | "broadcast" | "context" | "ack"
```

**Fonte:** Analisi tradeoff constrained decoding + approccio assembly grammar (Randall)

---

### 3.3 - Keyword ambiguity: "plan" e sia verb che noun

LU ha una ambiguita reale: `plan` appare sia in `verb` che in `noun`.

```ebnf
verb ::= ... | 'plan' | ...
noun ::= ... | 'plan' | ...
```

**Contesto disambigua:** `plan` e un verb solo dopo `to`, e un noun solo dopo `returns`/`proposes`/etc.

```
"architect returns plan to regina"    # plan = noun
"regina asks architect to plan"       # plan = verb
```

**Strategia in GBNF (la grammatica contestuale risolve):**

```gbnf
# Il contesto (la keyword precedente) disambigua sempre:
action ::= "asks" ws ident ws "to" ws verb
         | "returns" ws noun ws "to" ws ident
         | "tells" ws ident ws noun
         | "proposes" ws noun ws "to" ws ident
         | "sends" ws noun ws "to" ws ident

# "plan" in posizione verb:
verb ::= ws ("do" ws "task" | "verify" | "plan" | "research" | "shutdown") ws

# "plan" in posizione noun:
noun ::= ws ("result" | "verdict" | "plan" | "decision" | "report" | "message" | "broadcast" | "context" | "ack") ws
```

Il parser GBNF (context-free) usa il contesto sintattico per disambiguare. Non c'e ambiguita perche `verb` e raggiungibile solo dopo `to` e `noun` solo dopo certi verbi.

**In Lark LALR(1):** Attenzione! LALR(1) ha solo 1 token di lookahead. Ma in LU il contesto disambigua SEMPRE prima del token `plan` (grazie alla keyword precedente: `to` vs `returns`). Nessun conflitto Reduce/Reduce.

**Fonte:** Analisi diretta della grammatica EBNF LU + teoria LALR

---

## SEZIONE 4: Template Pronti per LU

### 4.1 - Template GBNF (sezioni principali)

```gbnf
# ============================================================
# LU LLM Grammar - GBNF format (XGrammar/vLLM/llama.cpp)
# Versione: whitespace-lenient (no INDENT/DEDENT)
# ============================================================

root ::= program
program ::= declaration+

# TOP LEVEL
declaration ::= ws (protocol-decl | agent-decl | type-decl | use-decl) ws

# PROTOCOL
protocol-decl ::= "protocol" ws1 ident ws ":" ws protocol-body
protocol-body ::= roles-clause (step | choice-block)+ properties-block?

# AGENT
agent-decl ::= "agent" ws1 ident ws ":" ws agent-body
agent-body ::= agent-clause+

# TYPE
type-decl ::= "type" ws1 ident ws "=" ws (variant-type | record-type)
variant-type ::= ident (ws "|" ws ident)+
record-type ::= ws field+
field ::= ws ident ws ":" ws type-expr ws

# USE
use-decl ::= "use" ws1 "python" ws1 dotted-name (ws "as" ws1 ident)? ws

# STEPS
step ::= ws ident ws1 action ws newline
action ::= "asks" ws1 ident ws1 "to" ws1 verb
         | "returns" ws1 noun ws1 "to" ws1 ident
         | "tells" ws1 ident ws1 noun
         | "proposes" ws1 noun ws1 "to" ws1 ident
         | "sends" ws1 noun ws1 "to" ws1 ident

# VERB / NOUN (closed lists)
verb ::= "do" ws1 "task" | "verify" | "plan" | "research" | "shutdown"
noun ::= "result" | "verdict" | "plan" | "decision" | "report" | "message" | "broadcast" | "context" | "ack"

# TERMINALS
ident ::= [a-zA-Z_] [a-zA-Z0-9_]*
number ::= [0-9]+ ("." [0-9]+)?
string ::= "\"" [^"\n]* "\"" | "'" [^'\n]* "'"
dotted-name ::= ident ("." ident)*
newline ::= "\n" ws
ws ::= [ \t\n\r]*
ws1 ::= [ \t]+
```

---

### 4.2 - Template Lark (sezioni principali)

```lark
# ============================================================
# LU LLM Grammar - Lark EBNF format (Outlines/llguidance)
# Versione: whitespace-lenient (no INDENT/DEDENT)
# ============================================================

?start: program

program: declaration+

# TOP LEVEL
declaration: protocol_decl
           | agent_decl
           | type_decl
           | use_decl

# PROTOCOL
protocol_decl: "protocol" IDENT ":" protocol_body
protocol_body: roles_clause (step | choice_block)+ properties_block?
roles_clause: "roles" ":" ident_list

# AGENT
agent_decl: "agent" IDENT ":" agent_body
agent_body: agent_clause+
agent_clause: "role" ":" IDENT
            | "trust" ":" trust_tier
            | "accepts" ":" ident_list
            | "produces" ":" ident_list
            | requires_clause
            | ensures_clause

# STEP
step: IDENT action
action: "asks" IDENT "to" verb
      | "returns" noun "to" IDENT
      | "tells" IDENT noun
      | "proposes" noun "to" IDENT
      | "sends" noun "to" IDENT

# CLOSED LISTS
verb: "do" "task" | "verify" | "plan" | "research" | "shutdown"
noun: "result" | "verdict" | "plan" | "decision" | "report"
    | "message" | "broadcast" | "context" | "ack"

# TYPE
type_decl: "type" IDENT "=" variant_type
         | "type" IDENT "=" record_type
variant_type: IDENT ("|" IDENT)+
record_type: field+
field: IDENT ":" type_expr
type_expr: base_type "?"?
base_type: IDENT "[" type_expr "]" | IDENT

# USE
use_decl: "use" "python" dotted_name ("as" IDENT)?
dotted_name: IDENT ("." IDENT)*

# TERMINALS
IDENT: /[a-zA-Z_][a-zA-Z0-9_]*/
NUMBER: /[0-9]+(\.[0-9]+)?/
STRING: /"[^"]*"/ | /'[^']*'/

# WHITESPACE (ignora tutto per LLM grammar)
%ignore /\s+/
%ignore /#[^\n]*/
```

---

## SEZIONE 5: Checklist per C2.4.1

### Prima di scrivere le ~50 regole

- [ ] GBNF: ogni non-terminal usa dashed-lowercase (no underscore)
- [ ] GBNF: la regola `root` e definita come prima
- [ ] GBNF: nessun `x? x? x?` in serie (usare `x{0,n}`)
- [ ] Lark: ogni terminale lessicale e UPPERCASE
- [ ] Lark: ogni struttura e lowercase
- [ ] Lark: nessun terminale UPPERCASE che matcha lo stesso testo di un literal string `"keyword"`
  - Soluzione: dichiarare i terminali senza includere le keyword (IDENT non matcha "protocol")
  - Lark gestisce la priorita automaticamente: literal string hanno priorita su IDENT
- [ ] Entrambi: `verb` e `noun` come closed list (non open IDENT)
- [ ] Entrambi: nessun INDENT/DEDENT (whitespace-lenient)
- [ ] GBNF: aggiungere `ws` prima e dopo ogni keyword dove il whitespace e permesso
- [ ] Lark: aggiungere `%ignore /\s+/` in fondo

### Keyword LU che NON devono matchare come IDENT

Lista completa delle keyword reserved in LU:

```
protocol, agent, type, use, python, as, roles, when, decides,
properties, always, terminates, no, deadlock, before, cannot, send,
all, participate, confidence, trust, role, accepts, produces,
requires, ensures, not, and, or, asks, returns, tells, proposes, sends, to,
do, task, verify, plan, research, shutdown,
result, verdict, decision, report, message, broadcast, context, ack,
certain, high, medium, low, speculative,
verified, trusted, standard, untrusted
```

In Lark: queste keyword come literal `"protocol"` hanno priorita automatica su `IDENT`. Non serve dichiarazione esplicita.

In GBNF: non esiste sistema di priorita automatico. Le regole con keyword literal devono apparire PRIMA della regola `ident` nell'alternativa, oppure usare look-ahead implicito tramite contesto sintattico.

---

## SINTESI

**Status:** COMPLETA
**Fonti:** 14 consultate

**Punti chiave:**

- GBNF: dashed-lowercase, `root ::= ...`, `ws ::= [ \t\n\r]*`, nessun INDENT/DEDENT possibile
- Lark: UPPERCASE terminali, lowercase regole, `%ignore /\s+/`, LALR(1) = no ambiguita
- XGrammar: usa esattamente GBNF standard di llama.cpp, nessuna estensione
- Outlines: LALR(1) strict, literal string hanno priorita su IDENT (no conflitti)
- llguidance: Earley-based, piu tollerante su ambiguita, stesso formato Lark
- Whitespace-lenient: sostituire INDENT/DEDENT con `ws` tra i token
- Closed list per `verb` e `noun`: zero hallucination, allineato al parser ufficiale
- Ambiguita "plan": nessun problema perche il contesto sintattico (`to` vs `returns`) disambigua sempre prima del token

**Raccomandazione:**

Scrivere le 50 regole in questo ordine:
1. `root`, `program`, `declaration` (top-level)
2. `protocol-decl`, `protocol-body`, `roles-clause`, `step`, `choice-block` (protocollo)
3. `action`, `verb`, `noun` (closed list)
4. `agent-decl`, `agent-body`, `agent-clause` (agente)
5. `requires-clause`, `ensures-clause`, `condition`, `expr` (contratti)
6. `type-decl`, `variant-type`, `record-type`, `field`, `type-expr` (tipi)
7. `use-decl`, `dotted-name` (import)
8. `properties-block`, `property`, `confidence-level`, `trust-tier` (proprieta)
9. Terminali: `ident`, `number`, `string`, `ws`, `ws1`, `newline` (GBNF) o `IDENT`, `NUMBER`, `STRING` (Lark)

---

## FONTI

1. GBNF README ufficiale: https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md
2. XGrammar Python API: https://xgrammar.mlc.ai/docs/api/python/grammar.html
3. XGrammar GitHub: https://github.com/mlc-ai/xgrammar
4. Lark Grammar Reference: https://lark-parser.readthedocs.io/en/latest/grammar.html
5. Lark JSON Tutorial: https://lark-parser.readthedocs.io/en/stable/json_tutorial.html
6. Outlines Creating Grammars: https://dottxt-ai.github.io/outlines/0.1.3/reference/generation/creating_grammars/
7. llguidance syntax docs: https://github.com/guidance-ai/llguidance/blob/main/docs/syntax.md
8. vLLM Structured Decoding blog: https://blog.vllm.ai/2025/01/14/struct-decode-intro.html
9. GBNF custom DSL example (assembly): https://www.jamesdrandall.com/posts/gbnf-constrained-generation/
10. Constrained decoding overview: https://mbrenndoerfer.com/writing/constrained-decoding-structured-llm-output
11. llguidance GitHub: https://github.com/guidance-ai/llguidance
12. Lark Indented Tree example: https://lark-parser.readthedocs.io/en/latest/examples/indented_tree.html
13. "Python is not context-free": https://www.cs.unc.edu/~plaisted/comp455/Python%20is%20not%20context%20free.htm
14. Lost in Space (tokenization for GCD): https://arxiv.org/html/2502.14969v1

---

*Cervella Researcher - CervellaSwarm S418*
*"Ricerca PRIMA di implementare."*
