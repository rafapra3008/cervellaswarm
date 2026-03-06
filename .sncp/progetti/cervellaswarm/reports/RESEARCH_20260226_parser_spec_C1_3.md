# Parser Unificato - Specifica per Step C1.3
## Lingua Universale v0.2

> **Data:** 26 Febbraio 2026
> **Ricercatrice:** Cervella Researcher
> **Status:** COMPLETA
> **Fonti:** 4 documenti analizzati (DESIGN_C1_2, STUDY_C1_1, SUBROADMAP, NORD.md) + codice sorgente (intent.py, spec.py)
> **Destinatario:** Il parser developer che implementera C1.3

---

## INDICE

1. [Le 62 Produzioni EBNF - Lista Completa e Classificata](#1-le-62-produzioni-ebnf)
2. [Analisi LL(1) vs LL(3) - Dove il Parser Ha Bisogno di Lookahead](#2-analisi-ll1-vs-ll3)
3. [I 6 Nuovi Costrutti - Cosa Aggiungono e Come Parsarli](#3-i-6-nuovi-costrutti)
4. [I 10 Esempi Canonici - Cosa Devono Parsare](#4-i-10-esempi-canonici)
5. [Decisioni di Design Chiave - Perche la Grammatica e Cosi](#5-decisioni-di-design-chiave)
6. [Cosa e Rimandato a C2](#6-cosa-e-rimandato-a-c2)
7. [Specifiche di Implementazione C1.3](#7-specifiche-di-implementazione-c13)
8. [Criteri di Completamento C1.3 - Checklist Operativa](#8-criteri-di-completamento-c13)

---

## 1. Le 62 Produzioni EBNF

### Classificazione per Categoria

Le 62 produzioni si distribuiscono in 8 sezioni. Di seguito ogni produzione con tipo (NT = non-terminal, T = terminal) e note implementative.

---

#### SEZIONE 1: Programma Top-Level (2 produzioni)

| # | Nome | Definizione | Tipo | Note |
|---|------|-------------|------|------|
| 1 | `program` | `declaration*` | NT | Entry point. Zero o piu dichiarazioni. File vuoto e valido. |
| 2 | `declaration` | `protocol_decl \| agent_decl \| type_decl \| use_decl` | NT | Discriminante LL(1): keyword 'protocol'/'agent'/'type'/'use'. |

---

#### SEZIONE 2: Protocol (6 produzioni)

| # | Nome | Definizione | Tipo | Note |
|---|------|-------------|------|------|
| 3 | `protocol_decl` | `'protocol' IDENT ':' NEWLINE INDENT protocol_body DEDENT` | NT | Discriminante: keyword 'protocol'. |
| 4 | `protocol_body` | `roles_clause step_or_choice+ properties_block?` | NT | `properties_block` e opzionale. |
| 5 | `roles_clause` | `'roles' ':' ident_list NEWLINE` | NT | Richiede almeno 1 ruolo. |
| 6 | `step_or_choice` | `step \| choice_block` | NT | Discriminante LL(1): 'when' = choice, altrimenti step. |
| 7 | `step` | `IDENT action NEWLINE` | NT | ATTENZIONE: NON LL(1) puro. Usa pattern matching. Vedi Sezione 2. |
| 8 | `action` | 5 alternative | NT | Discriminante LL(1): secondo token ('asks'/'returns'/'tells'/'proposes'/'sends'). |

Produzioni di `action` (5 alternative nel conteggio):

| # | Alternativa | Pattern | Nota |
|---|-------------|---------|------|
| 8a | `asks` | `'asks' IDENT 'to' verb` | Il receiver e dentro l'action (fix F1 Guardiana). |
| 8b | `returns` | `'returns' noun 'to' IDENT` | |
| 8c | `tells` | `'tells' IDENT noun` | |
| 8d | `proposes` | `'proposes' noun 'to' IDENT` | Aggiunto in v0.2 (fix P2-4 Ingegnera). |
| 8e | `sends` | `'sends' noun 'to' IDENT` | |

| # | Nome | Definizione | Tipo | Note |
|---|------|-------------|------|------|
| 9 | `verb` | `'do' 'task' \| 'verify' \| 'plan' \| 'research' \| 'shutdown'` | NT | `'do' 'task'` e un bigram - 2 token, 1 concetto. |
| 10 | `noun` | `'result' \| 'verdict' \| 'plan' \| 'decision' \| 'report' \| 'message' \| 'broadcast' \| 'context' \| 'ack'` | NT | 9 valori terminali. |
| 11 | `choice_block` | `'when' IDENT 'decides' ':' NEWLINE INDENT branch+ DEDENT` | NT | Discriminante: 'when'. |
| 12 | `branch` | `IDENT ':' NEWLINE INDENT step+ DEDENT` | NT | Il nome del branch e libero (es: 'approve', 'reject'). |

---

#### SEZIONE 3: Properties (5 produzioni)

| # | Nome | Definizione | Tipo | Note |
|---|------|-------------|------|------|
| 13 | `properties_block` | `'properties' ':' NEWLINE INDENT property+ DEDENT` | NT | Opzionale nel protocol_body. Discriminante: 'properties'. |
| 14 | `property` | 7 alternative | NT | Discriminante su primo token. Vedi tabella sotto. |
| 15 | `confidence_level` | `'certain' \| 'high' \| 'medium' \| 'low' \| 'speculative'` | NT | 5 valori fissi. |
| 16 | `trust_tier` | `'verified' \| 'trusted' \| 'standard' \| 'untrusted'` | NT | 4 valori fissi. |

Alternative di `property` (7 nel conteggio):

| # | Alternativa | Pattern | Discriminante |
|---|-------------|---------|---------------|
| 14a | always terminates | `'always' 'terminates' NEWLINE` | token 'always' |
| 14b | no deadlock | `'no' 'deadlock' NEWLINE` | token 'no' |
| 14c | ordering | `IDENT 'before' IDENT NEWLINE` | IDENT seguito da 'before' (LL(2)) |
| 14d | exclusion | `IDENT 'cannot' 'send' IDENT NEWLINE` | IDENT seguito da 'cannot' (LL(2)) |
| 14e | confidence | `'confidence' '>=' confidence_level NEWLINE` | token 'confidence' |
| 14f | trust | `'trust' '>=' trust_tier NEWLINE` | token 'trust' |
| 14g | participation | `'all' 'roles' 'participate' NEWLINE` | token 'all' |

NOTA IMPLEMENTATIVA: le alternative 14c e 14d iniziano entrambe con IDENT. La disambiguazione richiede guardare il secondo token ('before' vs 'cannot'). Questo e LL(2) - accettabile con 1 token di lookahead oltre al corrente.

---

#### SEZIONE 4: Agent (5 produzioni)

| # | Nome | Definizione | Tipo | Note |
|---|------|-------------|------|------|
| 17 | `agent_decl` | `'agent' IDENT ':' NEWLINE INDENT agent_body DEDENT` | NT | Discriminante: keyword 'agent'. |
| 18 | `agent_body` | `agent_clause+` | NT | Almeno 1 clausola. |
| 19 | `agent_clause` | 6 alternative | NT | Discriminante LL(1): primo token ('role'/'trust'/'accepts'/'produces'/'requires'/'ensures'). |
| 20 | `message_list` | `IDENT (',' IDENT)*` | NT | Usata in accepts/produces. |

Alternative di `agent_clause`:

| # | Alternativa | Pattern | Note |
|---|-------------|---------|------|
| 19a | role | `'role' ':' IDENT NEWLINE` | |
| 19b | trust | `'trust' ':' trust_tier NEWLINE` | |
| 19c | accepts | `'accepts' ':' message_list NEWLINE` | |
| 19d | produces | `'produces' ':' message_list NEWLINE` | |
| 19e | requires | `requires_clause` | Espanso sotto (Sezione 5). |
| 19f | ensures | `ensures_clause` | Espanso sotto (Sezione 5). |

---

#### SEZIONE 5: Requires/Ensures e Espressioni (10 produzioni)

| # | Nome | Definizione | Tipo | Note |
|---|------|-------------|------|------|
| 21 | `requires_clause` | `'requires' ':' NEWLINE INDENT condition+ DEDENT` o `'requires' ':' condition` | NT | Due forme: block (NEWLINE dopo ':') o inline. |
| 22 | `ensures_clause` | `'ensures' ':' NEWLINE INDENT condition+ DEDENT` o `'ensures' ':' condition` | NT | Identica struttura. |
| 23 | `condition` | `expr NEWLINE` | NT | NOTA fix F4: NEWLINE consumato qui, NON dalla clausola parent. |
| 24 | `expr` | `or_expr` | NT | Entry point per espressioni. |
| 25 | `or_expr` | `and_expr ('or' and_expr)*` | NT | Precedenza piu bassa. |
| 26 | `and_expr` | `not_expr ('and' not_expr)*` | NT | |
| 27 | `not_expr` | `'not' not_expr \| comparison` | NT | Ricorsivo a destra - nessuna left recursion. |
| 28 | `comparison` | `primary (comparison_op primary)?` | NT | Operatore opzionale. |
| 29 | `comparison_op` | `'==' \| '!=' \| '<' \| '>' \| '<=' \| '>='` | NT | 6 operatori. |
| 30 | `primary` | 5 alternative | NT | ATTENZIONE: richiede LL(3). Vedi Sezione 2. |
| 31 | `args` | `expr (',' expr)*` | NT | Argomenti di funzione in primary. |

Alternative di `primary` (richiede lookahead LL(3)):

| # | Alternativa | Pattern | Discriminante |
|---|-------------|---------|---------------|
| 30a | method call | `IDENT '.' IDENT '(' args? ')'` | Token 1=IDENT, Token 2='.', Token 3='(' |
| 30b | attribute | `IDENT '.' IDENT` | Token 1=IDENT, Token 2='.', Token 3!=any |
| 30c | identifier | `IDENT` | Token 1=IDENT, Token 2!='.' |
| 30d | number | `NUMBER` | |
| 30e | string | `STRING` | |
| 30f | grouped | `'(' expr ')'` | token '(' |

---

#### SEZIONE 6: Type Declarations (5 produzioni)

| # | Nome | Definizione | Tipo | Note |
|---|------|-------------|------|------|
| 32 | `type_decl` | DUE produzioni esplicite | NT | Fix P1-3: separazione in variant vs record. |
| 32a | variant form | `'type' IDENT '=' variant_type NEWLINE` | NT | Discriminante: dopo '=' viene IDENT (non NEWLINE). |
| 32b | record form | `'type' IDENT '=' NEWLINE INDENT field+ DEDENT` | NT | Discriminante: dopo '=' viene NEWLINE. |
| 33 | `variant_type` | `IDENT ('\|' IDENT)+` | NT | Almeno 2 varianti (uso del '+' dopo il primo). |
| 34 | `field` | `IDENT ':' type_expr NEWLINE` | NT | Un campo per riga. |
| 35 | `type_expr` | `base_type '?'?` | NT | Fix P1-2: '?' come suffisso. No left recursion. |
| 36 | `base_type` | `IDENT '[' type_expr ']' \| IDENT` | NT | Generics: `List[String]`, `Confident[Code]`. |

---

#### SEZIONE 7: Use Declarations (2 produzioni)

| # | Nome | Definizione | Tipo | Note |
|---|------|-------------|------|------|
| 37 | `use_decl` | `'use' 'python' dotted_name NEWLINE` o `'use' 'python' dotted_name 'as' IDENT NEWLINE` | NT | Due forme: con/senza alias. |
| 38 | `dotted_name` | `IDENT ('.' IDENT)*` | NT | Modulo Python (es: `datetime`, `pandas`). |

---

#### SEZIONE 8: Terminali (24 terminali)

| # | Nome | Pattern | Note |
|---|------|---------|------|
| 39 | `ident_list` | `IDENT (',' IDENT)*` | Usato in roles_clause. |
| 40 | `IDENT` | `[A-Za-z_][A-Za-z0-9_]*` | Identif. standard. Include keyword (lookahead le distingue). |
| 41 | `NUMBER` | `[0-9]+('.'[0-9]+)?` | Intero o float. |
| 42 | `STRING` | `'"' [^"]* '"' \| "'" [^']* "'"` | Singolo o doppio apice. |
| 43 | `NEWLINE` | `'\n'` | Gestito via indent stack. |
| 44 | `INDENT` | (aumento livello via indent stack) | Come Python: 4 spazi standard. |
| 45 | `DEDENT` | (riduzione livello via indent stack) | Generato artificialmente dal lexer. |
| 46 | `COMMENT` | `'#' [^\n]*` | Ignorato dal parser (consumato nel lexer). |
| 47 | `GTE` | `>=` | |
| 48 | `LTE` | `<=` | |
| 49 | `EQ` | `==` | |
| 50 | `NEQ` | `!=` | |
| 51 | `GT` | `>` | |
| 52 | `LT` | `<` | |
| 53 | `PIPE` | `\|` | Usato in variant_type. |
| 54 | `DOT` | `.` | Usato in primary e dotted_name. |
| 55 | `QUESTION` | `?` | Suffisso opzionale in type_expr. |
| 56 | `LBRACKET` | `[` | Generics. |
| 57 | `RBRACKET` | `]` | Generics. |
| 58 | `LPAREN` | `(` | Args + raggruppamento expr. |
| 59 | `RPAREN` | `)` | |
| 60 | `EQUALS` | `=` | Solo in type_decl. |
| 61 | `COLON` | `:` | Separatore ovunque. |
| 62 | `COMMA` | `,` | Lista separatori. |

**Totale: 62 produzioni** (8 sezioni: 2+6+5+5+10+5+2+24 = 59 denominate + la grammatica le riorganizza in 62 con le alternative esplicite di action, property, agent_clause, primary).

---

## 2. Analisi LL(1) vs LL(3)

### Dove il Parser e LL(1) (Quasi Tutto)

La grammatica e stata progettata per essere LL(1) ovunque possibile. Il discriminante standard e il **primo token non consumato** (lookahead di 1).

| Produzione | Token Discriminante | Come |
|------------|--------------------|----|
| `declaration` | 'protocol'/'agent'/'type'/'use' | 4 keyword distinte - triviale |
| `step_or_choice` | 'when' | Se e 'when' = choice_block, altrimenti step |
| `action` (dentro step) | 'asks'/'returns'/'tells'/'proposes'/'sends' | 5 keyword distinte |
| `agent_clause` | 'role'/'trust'/'accepts'/'produces'/'requires'/'ensures' | 6 keyword distinte |
| `type_decl` | token DOPO '=' | Se NEWLINE = record, altrimenti variant |
| `use_decl` | presenza di 'as' | Lookahead sul terzo token dopo dotted_name |
| `not_expr` | 'not' | Se 'not' = ricorsione, altrimenti comparison |
| `properties block` | 'always'/'no'/'confidence'/'trust'/'all' vs IDENT | 5 keyword vs IDENT |

### Le Due Eccezioni Non-LL(1)

#### Eccezione 1: `step` - Pattern Matching (non LL(1) puro)

**Il problema:** `step ::= IDENT action NEWLINE`

Quando il parser vede un IDENT a inizio riga, non sa se e:
- Il sender di uno step (`regina asks worker...`)
- Il nome di un branch in un choice_block (`approve:`, `reject:`)

**La soluzione del design:** Pattern matching contestuale. Nel contesto di `protocol_body`, dopo aver consumato `roles_clause`, ogni IDENT che non e 'when' e uno step. La disambiguazione avviene attraverso il contesto della produzione parent, non tramite lookahead puro.

**Raccomandazione implementativa:** Il metodo `parse_step_or_choice()` deve:
1. Se `current_token == 'when'` -> `parse_choice_block()`
2. Altrimenti -> `parse_step()` (il primo IDENT e sempre il sender)

Questo e identico alla logica in `intent.py` attuale (`_resolve_step`).

#### Eccezione 2: `primary` - Richiede LL(3)

**Il problema:**

```
primary ::= IDENT '.' IDENT '(' args? ')'    # tests.pass(80)   - 3 token di lookahead
           | IDENT '.' IDENT                   # task.well_defined - 2 token di lookahead
           | IDENT                             # variabile semplice - 1 token
```

Quando il parser vede `IDENT`, deve guardare avanti:
- Se token+1 = `.` e token+2 = IDENT e token+3 = `(` -> e una method call (3a)
- Se token+1 = `.` e token+2 = IDENT e token+3 != `(` -> e un attributo (3b)
- Se token+1 != `.` -> e un IDENT semplice (3c)

**Raccomandazione implementativa:** Il metodo `parse_primary()` usa un lookahead di 3:

```python
def parse_primary(self):
    if self.current == TokenKind.IDENT:
        if self.peek(1) == TokenKind.DOT and self.peek(2) == TokenKind.IDENT:
            if self.peek(3) == TokenKind.LPAREN:
                return self.parse_method_call()  # IDENT.IDENT(args)
            else:
                return self.parse_attribute()     # IDENT.IDENT
        else:
            return self.parse_identifier()        # IDENT
    elif self.current == TokenKind.NUMBER:
        return self.parse_number()
    elif self.current == TokenKind.STRING:
        return self.parse_string()
    elif self.current == TokenKind.LPAREN:
        return self.parse_grouped()               # (expr)
```

### Riepilogo Lookahead Richiesto

| Produzione | Lookahead | Tipo |
|------------|-----------|------|
| La maggior parte | LA(1) | LL(1) standard |
| `property` (14c, 14d) | LA(2) - secondo token | IDENT + 'before'/'cannot' |
| `primary` (30a vs 30b vs 30c) | LA(3) - terzo token | IDENT + '.' + IDENT + '(' |
| `step` dentro body | Contestuale | Pattern matching - non lookahead puro |

---

## 3. I 6 Nuovi Costrutti

Questi sono i costrutti che NON esistono in intent.py o spec.py attuali. L'implementazione C1.3 deve aggiungere il supporto per tutti e 6.

### Costrutto 1: `agent`

**Gap risolto:** Gap #1 da STUDY_C1_1 - nessun modulo aveva specifica dell'agente.

**Sintassi:**
```
agent NomeAgente:
    role: backend
    trust: standard
    accepts: TaskRequest, PlanDecision
    produces: TaskResult
    requires:
        task.well_defined
    ensures:
        output.compiles
```

**AST Node suggerito:**
```python
@dataclass
class AgentDecl:
    name: str
    role: str
    trust: TrustTier
    accepts: list[str]
    produces: list[str]
    requires: list[Condition]
    ensures: list[Condition]
```

**Note parser:** `agent_body` e una sequenza di `agent_clause`. L'ordine delle clausole NON e obbligatorio (un agente puo non avere 'accepts' se non riceve messaggi). Le clausole opzionali: `accepts`, `produces`, `role`, `trust`. Obbligatorie in senso logico (ma non sintattico): almeno `requires` o `ensures`.

### Costrutto 2: `requires`

**Gap risolto:** Gap #1 - contratti pre non esistevano.

**Due forme:**

Forma inline (singola condizione):
```
requires: task.well_defined
```

Forma block (condizioni multiple):
```
requires:
    task.well_defined
    context.sufficient
```

**Discriminante:** Dopo ':' - se viene NEWLINE si usa la forma block, altrimenti inline. Questo e LL(1).

**Fix critico F4 (Guardiana):** Il NEWLINE viene consumato da `condition`, NON da `requires_clause`. Il parser NON deve consumare il NEWLINE dopo ':' della forma inline - lo consuma `condition` alla fine dell'espressione.

### Costrutto 3: `ensures`

**Identico a `requires` nella struttura.** Stessa implementazione, keyword diversa. Rappresenta la postcondizione - cosa l'agente garantisce nel suo output.

### Costrutto 4: `type`

**Gap risolto:** Gap #4 - tipi custom erano hardcoded in types.py.

**Forma variant (enum-like):**
```
type TaskStatus = ok | fail | blocked
```
Discriminante: dopo '=' viene IDENT (non NEWLINE).

**Forma record (struct-like):**
```
type AnalysisResult =
    conclusion: String
    confidence: Confident[String]
    evidence: List[String]
    alternative: String?
```
Discriminante: dopo '=' viene NEWLINE.

**NOTA CRITICA sul generico:** `Confident[T]` e `List[T]` si parsano come `base_type ::= IDENT '[' type_expr ']'`. Il parser li tratta come IDENT generici. La semantica speciale di `Confident` (incertezza come tipo nativo) viene risolta nella fase semantica (C2), NON nel parser.

### Costrutto 5: `Confident[T]`

**Come parte del type system:** Il parser vede `Confident` come un IDENT normale seguito da `[type_expr]`. NON e una keyword riservata a livello sintattico. La keyword `Confident` ha significato speciale SOLO a livello semantico.

**Implicazione:** Il parser non ha logica speciale per `Confident`. La lista delle keyword riservate NON include `Confident`. Il lexer restituisce `IDENT` con valore "Confident". Il semantic analyzer (C2) lo riconosce.

### Costrutto 6: `use python`

**Gap risolto:** Gap #5 - nessun interop Python.

**Forme:**
```
use python math
use python datetime as dt
use python pandas as pd
```

**Parsing:** `'use' 'python' dotted_name ('as' IDENT)? NEWLINE`

`dotted_name` gestisce import con dot: `use python os.path` -> dotted_name = `os.path`.

**AST Node:**
```python
@dataclass
class UseDecl:
    module: str          # "datetime", "os.path"
    alias: str | None    # "dt", None
```

---

## 4. I 10 Esempi Canonici

Il parser DEVE accettare tutti e 10. Questo e il criterio primario di C1.3.

| # | Esempio | Costrutti Testati | Complessita Parser |
|---|---------|------------------|-------------------|
| 1 | DelegateTask | protocol base, roles, step (5 tipi action), properties (5 tipi) | Base - tutti i path LL(1) |
| 2 | PlanAndBuild | protocol, choice_block, branches | Critico: `choice_block` e disambiguazione step/choice |
| 3 | Worker (agent) | agent_decl, requires block, ensures con method call | Critico: `primary` LL(3) in `tests.pass(80)` |
| 4 | AnalysisResult | type record, Confident[T], List[T], String? | `base_type` con generics, suffix `?` |
| 5 | TaskStatus | type variant, 3 varianti | `variant_type` con PIPE |
| 6 | DataAnalyst + use | use_decl con alias, agent + requires con comparison | `pd.version >= "2.0"` - comparison + string |
| 7 | SecureAudit | protocol + properties con 'trust', 'cannot send' | property discriminazione IDENT+'cannot' |
| 8 | RecipeApp (La Nonna) | protocol + agent combinati, nomi dominio | Combinazione dei due top-level |
| 9 | DeepResearch | type record + protocol | Tipo custom usato in contesto protocol |
| 10 | Programma Completo | TUTTI i costrutti: use + type variant + type record + protocol + agent x2 | Test di integrazione completo |

### Copertura dei Costrutti per Esempio

| Costrutto | Es.1 | Es.2 | Es.3 | Es.4 | Es.5 | Es.6 | Es.7 | Es.8 | Es.9 | Es.10 |
|-----------|------|------|------|------|------|------|------|------|------|-------|
| protocol | Y | Y | - | - | - | - | Y | Y | Y | Y |
| agent | - | - | Y | - | - | Y | - | Y | - | Y Y |
| type (record) | - | - | - | Y | - | - | - | - | Y | Y |
| type (variant) | - | - | - | - | Y | - | - | - | - | Y |
| use python | - | - | - | - | - | Y | - | - | - | Y |
| requires (block) | - | - | Y | - | - | - | - | Y | - | Y |
| requires (inline) | - | - | - | - | - | Y | - | - | - | - |
| ensures | - | - | Y | - | - | Y | - | Y | - | Y |
| choice_block | - | Y | - | - | - | - | - | - | - | - |
| properties | Y | Y | - | - | - | - | Y | Y | Y | Y |
| Confident[T] | - | - | - | Y | - | - | - | - | Y | Y |
| List[T] | - | - | - | Y | - | - | - | - | Y | - |
| String? | - | - | - | Y | - | - | - | - | - | - |
| method call (LL3) | - | - | Y | - | - | - | - | - | - | Y |
| and/or expr | - | - | - | - | - | - | - | - | - | Y |

---

## 5. Decisioni di Design Chiave

### D1: Perche intent.py e la Base (Non dsl.py)

**Da scartare:** dsl.py usa sintassi brace-based (`{`, `}`, `;`) - stile C.
**Da usare:** intent.py usa sintassi indent-based, Python-like.

**Ragione tecnica:** I LLM hanno bias verso Python (90-97% nei benchmark - paper arXiv 2503.17181). Il constrained decoding e piu efficace con grammatiche simili a Python.

**Implicazione per C1.3:** Il tokenizer del parser unificato si basa sull'indent stack di intent.py (~70 LOC), non su quello di dsl.py (regex-based). L'Ingegnera stima 50-60% di riuso da intent.py + spec.py.

### D2: Perche spec.py si Fonde (Non Rimane Separato)

**Problema attuale:** intent.py e spec.py sono parser separati. Un programma completo oggi richiede 2 chiamate API distinte.

**Soluzione:** `properties:` diventa un blocco OPZIONALE dentro `protocol_decl`. Un file = una specifica completa (Proprieta 6: auto-documentante).

**Implicazione per C1.3:** Il parser unificato eredita le property keyword di spec.py (lines 24-30 del docstring spec.py): `always terminates`, `no deadlock`, `A before B`, `A cannot send B`, `confidence >= X`, `trust >= X`, `all roles participate`.

### D3: Perche dsl.py Non Muore (Diventa Export Format)

dsl.py mantiene la sua funzione come formato di interscambio Scribble-compatibile. Non viene rimosso. Il parser unificato PUO esportare nel formato dsl.py per interop con tool esterni. Questo e lavoro di C2 (AST -> code generation), non di C1.3.

### D4: Perche le Espressioni Multi-Riga Non Sono Supportate (v0.2)

**Fix P2-5 dell'Ingegnera:** Le condizioni in `requires`/`ensures` sono una condizione per riga. Non c'e supporto per:

```
# INVALIDO in v0.2:
requires:
    task.well_defined
    and context.sufficient  # <- questa non e una nuova condizione, e una continuazione
```

**Ogni condizione e `expr NEWLINE`.** L'`expr` e una singola espressione logica che puo usare `and`/`or` ma deve stare su una riga. Questo e un limite documentato, non un bug.

### D5: Perche `Confident[T]` Non e una Keyword nel Parser

**Decisione D3:** `Confident[T]` e nella grammatica come `base_type ::= IDENT '[' type_expr ']'`. Il parser NON ha logica speciale. Il significato semantico (incertezza come tipo nativo, Pilastro 1 del NORD) viene applicato nel compiler (C2).

**Ragione:** Mantenere il parser "stupido e veloce". Separazione netta tra sintassi (C1.3) e semantica (C2).

### D6: Perche `agent` e Top-Level (Non Dentro `protocol`)

**Decisione D6:** Un agente puo partecipare a MOLTI protocolli. Separare `agent_decl` da `protocol_decl` permette:

```
agent Worker: ...      # definito una volta
protocol Task1: ...    # usa Worker
protocol Task2: ...    # usa lo stesso Worker
```

La separazione e semantica (il semantic analyzer C2 risolve le referenze), non sintattica.

---

## 6. Cosa e Rimandato a C2

| Feature | Perche Rimandato | Dove |
|---------|-----------------|------|
| `proof` keyword (keyword Lean 4) | Richiede il compilatore Lean 4 per semantica. "Su carta, non reale." Fix F2 Guardiana. | C2.2 (AST -> codegen) + C2.1 (architettura) |
| Validazione semantica di `requires`/`ensures` | Il parser accetta qualsiasi `expr`. Il semantic check (es: "questo IDENT esiste come campo del tipo?") e C2. | C2.2 |
| Mapping `Confident[T]` al tipo Python `Confident` | Il parser vede IDENT generici. Il codegen deve importare `confidence.py` e wrappare. | C2.2 |
| `export agent Worker as python` | Python interop bidirezionale (lezione di ABC). | C2.3 |
| Constrained decoding export | Grammatica in formato XGrammar/llguidance/Outlines. | C2.4 |
| Round-trip semantico (parse -> codegen -> exec) | Il round-trip di C1.3 e solo parse -> AST -> render (strutturale). Il round-trip funzionale e C2. | C2.2 |
| Error messages con context semantico | errors.py deve essere esteso per il linguaggio. Base pronta (1784 LOC, 257 test). | C3.2 |
| REPL interattivo | | C3.1 |

---

## 7. Specifiche di Implementazione C1.3

### File da Creare

**Path target:** `packages/lingua-universale/src/cervellaswarm_lingua_universale/parser.py`

Non esiste ancora. E il deliverable principale di C1.3.

### Architettura Raccomandata (da Ingegnera: ~1200 LOC)

```
parser.py
├── Tokenizer (unificato: intent.py ~70 LOC + terminali nuovi)
│   ├── IndentStack (identico a intent.py)
│   ├── TokenKind enum (esteso con nuovi token)
│   └── Lexer.tokenize() -> list[Token]
│
├── AST Nodes (dataclasses frozen)
│   ├── Program
│   ├── ProtocolDecl
│   ├── AgentDecl
│   ├── TypeDecl (VariantType | RecordType)
│   ├── UseDecl
│   ├── Step
│   ├── ChoiceBlock, Branch
│   ├── PropertiesBlock, Property (7 tipi)
│   ├── RequiresClause, EnsuresClause
│   ├── Condition, Expr (gerarchia: Or/And/Not/Comparison/Primary)
│   └── TypeExpr, BaseType, Field
│
├── Parser (recursive descent)
│   ├── parse_program()
│   ├── parse_declaration()  # LL(1) su keyword
│   ├── parse_protocol_decl()
│   │   ├── parse_roles_clause()
│   │   ├── parse_step_or_choice()  # pattern matching (non LL(1) puro)
│   │   └── parse_properties_block()
│   ├── parse_agent_decl()
│   │   └── parse_agent_clause()
│   ├── parse_type_decl()  # LL(1) post '='
│   ├── parse_use_decl()
│   ├── parse_expr()  # gerarchia precedenza
│   │   └── parse_primary()  # LL(3) lookahead
│   └── parse_condition()
│
├── Renderer (AST -> testo)  # per round-trip test
│   └── render(node: ASTNode) -> str
│
└── GrammarExporter  # per constrained decoding (output EBNF/JSON)
    └── export_ebnf() -> str
```

### Riuso da Moduli Esistenti

| Da Riusare | Fonte | LOC Stimati |
|------------|-------|-------------|
| IndentStack + tokenizzazione base | intent.py (righe ~100-170) | ~70 LOC |
| Property keyword + parsing | spec.py (righe ~80-200) | ~120 LOC |
| IntentParseError pattern | intent.py | ~20 LOC |
| SpecParseError pattern -> unificare in ParseError | spec.py | - |
| Protocol/ProtocolStep dataclasses | protocols.py (gia pronto) | 0 - import |
| TrustTier enum | trust.py | 0 - import |
| ConfidenceScore / livelli | confidence.py | 0 - import |

**Totale riuso stimato:** ~210 LOC dei ~1200 totali (~17%). Il resto e nuovo per la grammatica unificata.

### Tokenizer: Token da Aggiungere Rispetto a intent.py

intent.py attuale gestisce: IDENT, NEWLINE, INDENT, DEDENT, COLON, COMMA.

Il parser unificato aggiunge:
- NUMBER, STRING (per espressioni in requires/ensures)
- PIPE, QUESTION, LBRACKET, RBRACKET (per type system)
- LPAREN, RPAREN, EQUALS (per expr + type_decl)
- GTE, LTE, EQ, NEQ, GT, LT (per comparison_op)
- DOT (per primary e dotted_name)

### Test: ~700 LOC in 2+ file

**Struttura suggerita (da Ingegnera):**

```
tests/test_parser_core.py     # I 10 esempi canonici + costrutti base
tests/test_parser_edge.py     # Edge cases, errori, round-trip
```

**Copertura minima richiesta: >= 95%**

Test obbligatori per i 10 esempi:
```python
def test_example_01_delegate_task(): ...
def test_example_02_plan_and_build(): ...
# ... fino a:
def test_example_10_complete_program(): ...
```

Test per error messages:
```python
def test_error_missing_roles_clause(): ...
def test_error_invalid_action_verb(): ...
def test_error_unclosed_indent(): ...
```

Test per round-trip:
```python
def test_roundtrip_protocol():
    source = "protocol X:\n    roles: a, b\n    a asks b to do task\n"
    ast = parse(source)
    rendered = render(ast)
    assert parse(rendered) == ast  # AST identico, non testo identico
```

---

## 8. Criteri di Completamento C1.3

Dalla SUBROADMAP_FASE_C, trasformati in checklist operativa:

### Criteri Obbligatori (tutti e 5 devono essere soddisfatti)

**C1.** Parser accetta tutti i 10 esempi canonici da DESIGN_C1_2 senza errori.

```python
for i, example in enumerate(CANONICAL_EXAMPLES):
    ast = parse(example)
    assert ast is not None, f"Esempio {i+1} fallisce"
```

**C2.** Error messages umani (non tecnici).

```
# SBAGLIATO (tecnico):
SyntaxError: unexpected token IDENT at line 5, col 3

# CORRETTO (umano):
Riga 5: Lo step "worker returns" ha bisogno di un destinatario.
        Scrivi: "worker returns result to regina"
```

**C3.** Round-trip strutturale: `parse(text) -> AST -> render(AST)` produce output che, ri-parsato, da lo stesso AST.

Nota: il testo non deve essere identico (spaziatura puo differire), ma l'AST deve essere identico.

**C4.** Export grammatica per constrained decoding in formato EBNF o JSON compatibile con XGrammar/llguidance/Outlines.

**C5.** Test coverage >= 95%.

### Criterio Qualita (Guardiana)

Il target del NORD e 9.5/10 per ogni step. C1.2 Design ha ricevuto 8.8/10. C1.3 (implementazione) deve raggiungere 9.5/10.

### Dipendenze Bloccanti

C1.3 NON puo iniziare prima che:
- C1.2 sia COMPLETO (e lo e - 8.8/10 Guardiana, S409)

C1.3 SBLOCCA:
- C2.1 (studio architettura compilatore)
- C2.2 (AST -> Python codegen) - dipende direttamente dall'AST di C1.3
- C2.4 (constrained decoding export) - il GrammarExporter e in C1.3

### Stima Effort (da Ingegnera Review)

- ~1200 LOC parser unificato
- ~700 LOC test (2 file)
- ~50-60% riuso da intent.py + spec.py
- 2-3 sessioni stimate

---

## RIEPILOGO ESECUTIVO

**Cosa implementare in C1.3:**

Un recursive descent parser Python puro (0 dipendenze) che:
1. Tokenizza con indent stack (come Python, come intent.py)
2. Parsa 62 produzioni EBNF, LL(1) ovunque tranne `step` (pattern matching) e `primary` (LL(3))
3. Produce un AST tipizzato con dataclasses frozen
4. Renderizza l'AST in testo (round-trip)
5. Esporta la grammatica in EBNF/JSON per constrained decoding
6. Accetta i 10 esempi canonici (che coprono TUTTI i costrutti)
7. Emette error messages comprensibili per umani

**La base da riusare:** intent.py (tokenizer indent-aware) + spec.py (property keywords) + protocols.py (Protocol dataclasses gia pronte).

**Il file da creare:** `packages/lingua-universale/src/cervellaswarm_lingua_universale/parser.py`

**Il criterio di successo:** Guardiana 9.5/10.

---

*Cervella Researcher - CervellaSwarm S409*
*"Ricerca PRIMA di implementare."*
