# STEP C1.2 - Design della Sintassi: La Lingua Universale

> **Sessione:** 408-409
> **Data:** 26 Febbraio 2026
> **Versione:** v0.2 (dopo review Marketing + Ingegnera)
> **Designer:** Cervella Regina
> **Reviewers:** Marketing (leggibilita 6.8/10), Ingegnera (implementabilita 7/10)
> **Base:** STUDY_C1_1 (intent.py + spec.py + confidence/trust) + 2 report Researcher (S407)
> **Principi:** 7 proprieta dual-readable + 3 pilastri NORD.md + insight Rafa (S407)

---

## DECISIONE DI DESIGN: PERCHE COSI

### Sintassi Python-like (indent-based, `:`, no `{}` no `;`)
- **Ragione 1:** LLM hanno bias verso Python (90-97% nei benchmark - paper arXiv 2503.17181)
- **Ragione 2:** intent.py GIA funziona cosi e e il modulo piu "leggibile"
- **Ragione 3:** Riduce pain of adoption (sembra familiare)
- **Ragione 4:** Indent = struttura visiva = struttura logica (Proprieta 5: isomorfo)

### Keyword inglesi brevi (no simboli speciali)
- **Ragione:** ASCII-first, token-efficiente. Simboli speciali = multi-token per LLM tokenizer.

### Dichiarativo (COSA, non COME)
- **Ragione:** Riduce punti di decisione sequenziale per l'AI (Proprieta 2)

---

## GRAMMATICA EBNF - La Lingua Universale v0.2

```ebnf
(* ============================================================ *)
(* La Lingua Universale - Grammatica Formale                     *)
(* Versione: 0.2 (Step C1.2, S408 - dopo review Ingegnera)      *)
(* Regole: 62 produzioni (target < 100)                          *)
(* Design: Python-like indent, dichiarativo, dual-readable       *)
(* Parsing: LL(1) ovunque tranne step (pattern matching) e       *)
(*          primary (LL(3) lookahead per IDENT.IDENT(            *)
(* Fix: P1-1 left recursion expr, P1-2 type_expr, P1-3 type_decl*)
(* ============================================================ *)

(* ============================================================ *)
(* 1. PROGRAMMA - Top Level                                      *)
(* ============================================================ *)

program          ::= declaration*

declaration      ::= protocol_decl
                   | agent_decl
                   | type_decl
                   | use_decl

(* ============================================================ *)
(* 2. PROTOCOL - Il cuore (da dsl.py + intent.py unificati)      *)
(* ============================================================ *)

protocol_decl    ::= 'protocol' IDENT ':' NEWLINE INDENT protocol_body DEDENT

protocol_body    ::= roles_clause
                     step_or_choice+
                     properties_block?

roles_clause     ::= 'roles' ':' ident_list NEWLINE

step_or_choice   ::= step | choice_block

(* NOTA: step usa pattern matching (come intent.py _resolve_step)  *)
(* Il receiver e SEMPRE interno alla action phrase.               *)
(* Non e LL(k) puro ma e un design deliberato per leggibilita.   *)
(* Fix F1 Guardiana: rimosso trailing IDENT dalla regola step.   *)
step             ::= IDENT action NEWLINE

action           ::= 'asks' IDENT 'to' verb           (* regina asks worker to do task *)
                   | 'returns' noun 'to' IDENT         (* worker returns result to regina *)
                   | 'tells' IDENT noun                (* regina tells architect decision *)
                   | 'proposes' noun 'to' IDENT        (* architect proposes plan to regina *)
                   | 'sends' noun 'to' IDENT           (* regina sends message to worker *)

verb             ::= 'do' 'task' | 'verify' | 'plan'
                   | 'research' | 'shutdown'

noun             ::= 'result' | 'verdict' | 'plan'
                   | 'decision' | 'report' | 'message'
                   | 'broadcast' | 'context' | 'ack'

choice_block     ::= 'when' IDENT 'decides' ':' NEWLINE INDENT branch+ DEDENT

branch           ::= IDENT ':' NEWLINE INDENT step+ DEDENT

(* ============================================================ *)
(* 3. PROPERTIES - Verifiche formali (da spec.py)                *)
(* ============================================================ *)

properties_block ::= 'properties' ':' NEWLINE INDENT property+ DEDENT

property         ::= 'always' 'terminates' NEWLINE
                   | 'no' 'deadlock' NEWLINE
                   | IDENT 'before' IDENT NEWLINE
                   | IDENT 'cannot' 'send' IDENT NEWLINE
                   | 'confidence' '>=' confidence_level NEWLINE
                   | 'trust' '>=' trust_tier NEWLINE
                   | 'all' 'roles' 'participate' NEWLINE

confidence_level ::= 'certain' | 'high' | 'medium' | 'low' | 'speculative'

trust_tier       ::= 'verified' | 'trusted' | 'standard' | 'untrusted'

(* ============================================================ *)
(* 4. AGENT - Specifica agente (NUOVO - Gap #1 da C1.1)         *)
(* ============================================================ *)

agent_decl       ::= 'agent' IDENT ':' NEWLINE INDENT agent_body DEDENT

agent_body       ::= agent_clause+

agent_clause     ::= 'role' ':' IDENT NEWLINE
                   | 'trust' ':' trust_tier NEWLINE
                   | 'accepts' ':' message_list NEWLINE
                   | 'produces' ':' message_list NEWLINE
                   | requires_clause
                   | ensures_clause

message_list     ::= IDENT (',' IDENT)*

(* ============================================================ *)
(* 5. REQUIRES / ENSURES - Contratti (NUOVO - Gap #1 da C1.1)   *)
(* Discriminante LL(1): dopo ':' -> NEWLINE = block, altro = inline *)
(* Nota v0.2: espressioni multi-riga NON supportate.             *)
(* Una condizione = una riga. Limite documentato.                *)
(* ============================================================ *)

(* Fix F4 Guardiana: NEWLINE consumato da condition, non dalla clausola *)
requires_clause  ::= 'requires' ':' NEWLINE INDENT condition+ DEDENT
                   | 'requires' ':' condition

ensures_clause   ::= 'ensures' ':' NEWLINE INDENT condition+ DEDENT
                   | 'ensures' ':' condition

condition        ::= expr NEWLINE

(* ============================================================ *)
(* 5b. ESPRESSIONI - Con livelli di precedenza (Fix P1-1)        *)
(* Precedenza (bassa -> alta): or, and, not, comparison, primary *)
(* NO left recursion. Parsabile con recursive descent puro.      *)
(* ============================================================ *)

expr             ::= or_expr

or_expr          ::= and_expr ('or' and_expr)*

and_expr         ::= not_expr ('and' not_expr)*

not_expr         ::= 'not' not_expr
                   | comparison

comparison       ::= primary (comparison_op primary)?

comparison_op    ::= '==' | '!=' | '<' | '>' | '<=' | '>='

primary          ::= IDENT '.' IDENT '(' args? ')'    (* tests.pass(80) - LL(3) *)
                   | IDENT '.' IDENT                    (* task.well_defined *)
                   | IDENT
                   | NUMBER
                   | STRING
                   | '(' expr ')'                       (* raggruppamento esplicito *)

args             ::= expr (',' expr)*

(* ============================================================ *)
(* 6. TYPE - Dichiarazione tipi (NUOVO - Gap #4 da C1.1)        *)
(* Fix P1-3: due produzioni esplicite per variant vs record      *)
(* Discriminante LL(1): dopo '=' -> IDENT = variant, NEWLINE = record *)
(* ============================================================ *)

type_decl        ::= 'type' IDENT '=' variant_type NEWLINE
                   | 'type' IDENT '=' NEWLINE INDENT field+ DEDENT

variant_type     ::= IDENT ('|' IDENT)+

field            ::= IDENT ':' type_expr NEWLINE

(* Fix P1-2: '?' come suffisso opzionale, no left recursion      *)
(* Confident trattato come IDENT nel parser, speciale in semantica *)
type_expr        ::= base_type '?'?

base_type        ::= IDENT '[' type_expr ']'           (* List[String], Confident[Code] *)
                   | IDENT                               (* String, Number, etc. *)

(* ============================================================ *)
(* 7. USE - Import Python (NUOVO - Gap #5 da C1.1)              *)
(* ============================================================ *)

use_decl         ::= 'use' 'python' dotted_name NEWLINE
                   | 'use' 'python' dotted_name 'as' IDENT NEWLINE

dotted_name      ::= IDENT ('.' IDENT)*

(* ============================================================ *)
(* 8. TERMINALI                                                  *)
(* ============================================================ *)

ident_list       ::= IDENT (',' IDENT)*

(* Terminali atomici *)
IDENT            ::= [A-Za-z_][A-Za-z0-9_]*
NUMBER           ::= [0-9]+('.'[0-9]+)?
STRING           ::= '"' [^"]* '"' | "'" [^']* "'"
NEWLINE          ::= '\n'
INDENT           ::= (aumento livello indentazione via indent stack, 4 spazi)
DEDENT           ::= (diminuzione livello indentazione via indent stack)
COMMENT          ::= '#' [^\n]*

(* Operatori e simboli - Fix F3 Guardiana: lista esplicita *)
GTE              ::= '>='
LTE              ::= '<='
EQ               ::= '=='
NEQ              ::= '!='
GT               ::= '>'
LT               ::= '<'
PIPE             ::= '|'
DOT              ::= '.'
QUESTION         ::= '?'
LBRACKET         ::= '['
RBRACKET         ::= ']'
LPAREN           ::= '('
RPAREN           ::= ')'
EQUALS           ::= '='
COLON            ::= ':'
COMMA            ::= ','

(* NOTA F2: 'proof' keyword (Gap #3 da C1.1) RIMANDATO a C2.     *)
(* Motivazione: proof richiede il compilatore Lean 4 (C2.2) per   *)
(* avere semantica. Aggiungere la keyword senza semantica in C1    *)
(* sarebbe "su carta, non reale". Coerente con COSTITUZIONE.       *)
```

**Conteggio regole: 62 produzioni** (target < 100 - ampio margine. Criterio: 1 `::=` = 1 regola)

### Changelog v0.1 -> v0.2 (Fix da review Ingegnera + Guardiana)

| Fix | Fonte | Descrizione |
|-----|-------|-------------|
| **P1-1** | Ingegnera | `expr` riscritta con livelli di precedenza. Zero left recursion. |
| **P1-2** | Ingegnera | `type_expr` riscritta: `base_type '?'?`. No left recursion. |
| **P1-3** | Ingegnera | `type_decl` separata in due produzioni esplicite. LL(1). |
| **P2-4** | Ingegnera | Aggiunta `'proposes' noun 'to'` alle action. |
| **P2-5** | Ingegnera | Espressioni multi-riga NON supportate in v0.2. |
| **P3-3** | Ingegnera | `'(' expr ')'` a primary per raggruppamento. |
| **F1** | Guardiana | `step ::= IDENT action NEWLINE` (receiver interno ad action). |
| **F3** | Guardiana | Terminali: lista esplicita di tutti operatori/simboli. |
| **F4** | Guardiana | Double NEWLINE fix: NEWLINE consumato solo da `condition`. |
| **F2** | Guardiana | `proof` keyword rimandato a C2 (serve semantica Lean 4). |
| **Es.8** | Marketing | Nomi dominio (Chef, recipes.saved) al posto di nomi tecnici. |

---

## I 10 ESEMPI CANONICI (Dual-Readable Annotati)

### Esempio 1: Il Protocollo Base (DelegateTask)

```
# La nonna lo legge: "La regina chiede al lavoratore di fare il compito,
# il lavoratore restituisce il risultato, poi la guardiana verifica."

protocol DelegateTask:
    roles: regina, worker, guardiana

    regina asks worker to do task
    worker returns result to regina
    regina asks guardiana to verify
    guardiana returns verdict to regina

    properties:
        always terminates
        no deadlock
        task_request before task_result
        all roles participate
```

**Annotazione:** Questo e esattamente intent.py + spec.py UNIFICATI in un singolo blocco. Zero nuova sintassi - solo fusione. L'AI lo genera correttamente perche ogni riga ha UNA sola interpretazione possibile.

---

### Esempio 2: Protocollo con Scelta (PlanAndBuild)

```
protocol PlanAndBuild:
    roles: regina, architect, worker, guardiana

    regina asks architect to plan
    architect returns plan to regina

    when regina decides:
        approve:
            regina tells architect decision
            regina asks worker to do task
            worker returns result to regina
            regina asks guardiana to verify
            guardiana returns verdict to regina
        reject:
            regina tells architect decision
            architect returns plan to regina

    properties:
        always terminates
        no deadlock
        confidence >= high
```

**Annotazione:** `when X decides:` e gia in intent.py. Il branching e naturale. Un product manager legge e capisce il flusso decisionale. L'AI sa che dopo `approve:` deve generare la sequenza completa.

---

### Esempio 3: Agente con Contratti (Worker)

```
agent Worker:
    role: backend
    trust: standard

    accepts: TaskRequest, PlanDecision
    produces: TaskResult

    requires:
        task.well_defined
        context.sufficient

    ensures:
        output.compiles
        tests.pass(80)
```

**Annotazione:** NUOVO costrutto `agent`. `requires`/`ensures` sono i contratti pre/post che mancavano (Gap #1 da C1.1). Leggibilita: un non-dev capisce che il Worker accetta certi compiti e garantisce certe cose. L'AI sa generare codice Python con assert per requires e postcondizioni per ensures.

---

### Esempio 4: Tipo con Confidence Nativa (AnalysisResult)

```
type AnalysisResult =
    conclusion: String
    confidence: Confident[String]
    evidence: List[String]
    alternative: String?
```

**Annotazione:** `Confident[T]` diventa keyword NATIVA del linguaggio (Gap #2 da C1.1). Non e un import Python - e nel type system. `String?` = opzionale (come TypeScript/Kotlin). L'AI genera esattamente questi campi perche la grammatica li vincola.

---

### Esempio 5: Tipo Variante (enumerazione)

```
type TaskStatus = ok | fail | blocked

type AuditVerdict = approved | blocked | needs_revision

type Priority = critical | high | medium | low
```

**Annotazione:** Tipi custom (Gap #4 da C1.1). Come gli enum di Rust/Haskell ma con sintassi leggibile. `|` e universale (anche in TypeScript, Python typing, Haskell). Un non-dev capisce: "lo stato e ok, fail, o blocked."

---

### Esempio 6: Import Python (interop bidirezionale)

```
use python math
use python datetime as dt
use python pandas as pd

agent DataAnalyst:
    role: data
    trust: standard

    requires:
        pd.version >= "2.0"

    ensures:
        output.format == "dataframe"
```

**Annotazione:** `use python X` (Gap #5 da C1.1). La lezione di ABC: mai essere un sistema chiuso. Il codice Python esistente e immediatamente disponibile. L'AI sa che `pd` e pandas e genera codice interop corretto.

---

### Esempio 7: Protocollo con Proprieta Trust

```
protocol SecureAudit:
    roles: regina, guardiana, backend

    regina asks backend to do task
    backend returns result to regina
    regina asks guardiana to verify
    guardiana returns verdict to regina

    properties:
        always terminates
        no deadlock
        trust >= trusted
        backend cannot send audit_verdict
        confidence >= high
```

**Annotazione:** Combina trust + confidence + exclusion. La property `trust >= trusted` significa: tutti i ruoli devono avere trust almeno "trusted". `backend cannot send audit_verdict` = separazione dei doveri. Leggibile come policy aziendale.

---

### Esempio 8: Il Flusso Completo (La Nonna e le Ricette)

```
# La nonna dice: "Voglio un'app per le mie ricette"
# Il sistema traduce in specifica verificabile:

protocol RecipeApp:
    roles: regina, chef, guardiana

    regina asks chef to do task
    chef returns result to regina
    regina asks guardiana to verify
    guardiana returns verdict to regina

    properties:
        always terminates
        no deadlock
        all roles participate

agent Chef:
    role: backend
    trust: standard

    requires:
        user.authenticated

    ensures:
        no_recipe_deleted_by_accident
        recipes.saved
```

**Annotazione:** Il demo "nonna con le ricette" dal NORD.md. Due costrutti (protocol + agent) esprimono TUTTO: il flusso di comunicazione E le garanzie di sicurezza. Un non-dev legge: "la regina chiede al chef di fare il compito, la guardiana verifica, e il chef garantisce che nessuna ricetta viene cancellata per sbaglio e le ricette vengono salvate." I nomi dei ruoli (`chef`) parlano il linguaggio del dominio, non del codice (feedback Marketing). La "zona tecnica" (requires/ensures) e separata dalla "zona narrativa" (protocol).

---

### Esempio 9: Composizione di Protocolli

```
type ResearchResult =
    findings: Confident[String]
    sources: List[String]
    methodology: String

protocol DeepResearch:
    roles: regina, researcher, guardiana

    regina asks researcher to research
    researcher returns report to regina
    regina asks guardiana to verify
    guardiana returns verdict to regina

    properties:
        always terminates
        confidence >= medium
        trust >= standard
```

**Annotazione:** Mostra che il linguaggio funziona per qualsiasi dominio agente, non solo task delegation. I tipi custom (`ResearchResult`) si combinano con i protocolli. `Confident[String]` nel tipo = il risultato porta con se il suo livello di certezza.

---

### Esempio 10: Programma Completo (Multi-Protocol)

```
# Un programma completo nella Lingua Universale
# Tutto in un file, tutto verificabile

use python logging

type Priority = critical | high | medium | low

type CodeResult =
    code: Confident[String]
    tests_passed: Number
    coverage: Number

protocol CodeReview:
    roles: regina, backend, tester, guardiana

    regina asks backend to do task
    backend returns result to regina
    regina asks tester to verify
    tester returns verdict to regina
    regina asks guardiana to verify
    guardiana returns verdict to regina

    properties:
        always terminates
        no deadlock
        task_request before task_result
        backend cannot send audit_verdict
        tester cannot send task_result
        trust >= standard
        all roles participate

agent CodeBackend:
    role: backend
    trust: standard

    accepts: TaskRequest
    produces: TaskResult

    requires:
        task.well_defined
        task.priority != critical or regina.approved

    ensures:
        output.compiles
        tests.pass(80)
        coverage >= 70

agent CodeTester:
    role: tester
    trust: trusted

    accepts: AuditRequest
    produces: AuditVerdict

    requires:
        code.compiles

    ensures:
        all_tests.executed
        report.complete
```

**Annotazione:** Un programma completo: import Python + tipi custom + protocollo multi-ruolo + 2 agenti con contratti + 7 proprieta formali. **62 righe** di specifica dual-readable che l'AI puo generare (constrained decoding dalla grammatica EBNF) e un non-dev puo leggere e capire. Il compilatore (C2) verifichera staticamente le proprieta e generera Python con contratti runtime.

---

## CONFRONTO CON SINTASSI ATTUALE

| Aspetto | DSL attuale (dsl.py) | Intent attuale (intent.py) | **Lingua Universale v0.1** |
|---------|---------------------|---------------------------|----------------------------|
| Stile | Brace-based (`{}`, `;`) | Indent-based (`:`) | **Indent-based (`:`)** |
| Protocolli | `protocol X { ... }` | `protocol X:` | **`protocol X:`** |
| Step | `a -> b : Msg;` | `a asks b to verb` | **`a asks b to verb`** |
| Choice | `choice at X { ... }` | `when X decides:` | **`when X decides:`** |
| Proprieta | Separato (spec.py) | NON supportato | **Inline (`properties:`)** |
| Tipi AI | NON supportato | NON supportato | **`Confident[T]` nativo** |
| Contratti | NON supportato | NON supportato | **`requires:` / `ensures:`** |
| Tipi custom | NON supportato | NON supportato | **`type X = a \| b`** |
| Python interop | NON supportato | NON supportato | **`use python X`** |
| Agenti | NON supportato | NON supportato | **`agent X:`** |

**Cosa CAMBIA:** 6 costrutti nuovi (agent, requires, ensures, type, Confident[T], use python)
**Cosa RESTA:** La base sintattica di intent.py (Python-like, indent, verbi naturali)
**Cosa MUORE:** La sintassi brace-based di dsl.py (diventa solo formato export Scribble)

---

## DESIGN DECISIONS LOG

| # | Decisione | Alternativa scartata | Perche |
|---|-----------|---------------------|--------|
| D1 | Indent-based (Python-like) | Brace-based (C-like, come dsl.py) | LLM bias verso Python (90-97%), leggibilita non-dev |
| D2 | `requires`/`ensures` come clausole | `contract { ... }` blocco separato | Piu vicino a Python (decoratori), meno nesting |
| D3 | `Confident[T]` nella grammatica | `confidence: float` tipo primitivo | Incertezza come tipo di prima classe (Pilastro 1 NORD) |
| D4 | `type X = a \| b` per varianti | `enum X { a, b }` stile Java/Rust | Piu leggibile, meno boilerplate, token-efficiente |
| D5 | `use python X` per import | `import X from python` | Distinto da Python import (non siamo Python, USIAMO Python) |
| D6 | `agent X:` come top-level | Agent come parte del protocol | Un agente puo partecipare a MOLTI protocolli (separation of concerns) |
| D7 | Verbi naturali per step | Frecce `->` come dsl.py | Dual-readable: la nonna capisce "asks worker to do task" |
| D8 | Properties inline nel protocol | Properties in file separato | Un file = una specifica completa (Proprieta 6: auto-documentante) |

---

## METRICHE

```
REGOLE EBNF:           62 produzioni (target < 100, criterio: 1 ::= = 1 regola)
KEYWORD NUOVE:         6 (agent, requires, ensures, type, Confident, use)
KEYWORD DA INTENT.PY:  ~25 (mantenute identiche, +proposes)
KEYWORD DA SPEC.PY:    ~14 (mantenute identiche)
ESEMPI CANONICI:       10 (annotati con spiegazione dual-readable)
COSTRUTTI TOP-LEVEL:   4 (protocol, agent, type, use)
COMPATIBILITY:         intent.py 100% (i programmi intent esistenti sono validi)
PARSING:               LL(1) ovunque tranne step (pattern match) e primary (LL(3))
LEFT RECURSION:        ZERO (eliminata in v0.2)
```

---

## REVIEW LOG

| Reviewer | Score | Fix applicati |
|----------|-------|---------------|
| **Marketing** | 6.8/10 leggibilita | Esempio 8 riscritto (nomi dominio). Nota: confine zona narrativa/tecnica e feature. |
| **Ingegnera** | 7/10 implementabilita | P1-1 expr fix, P1-2 type_expr fix, P1-3 type_decl fix, proposes aggiunto, parentesi. |
| **Guardiana** | 8.8/10 qualita | F1 step fix, F3 terminali, F4 double NEWLINE, F2 proof rimandato C2. |

### Feedback Marketing chiave (da indirizzare in C1.3/C2)
- Notazione a punto (`task.well_defined`) rompe flusso narrativo nelle condizioni
- `>=` nelle properties potrebbe avere alternativa verbale futura (`at least high`)
- Confine "zona narrativa" (protocol) vs "zona tecnica" (agent/conditions) e una FEATURE: "Il protocollo lo scrivi tu. Le garanzie tecniche le scrive l'AI."

### Stima Ingegnera per C1.3 (Parser)
- ~1200 LOC parser unificato, ~700 LOC test
- ~50-60% riuso da intent.py + spec.py
- 5-6 sessioni stimate
- Tokenizer unificato con indent stack (come Python)

---

*Cervella Regina - CervellaSwarm S408-409*
*"La domanda e la risposta nello STESSO linguaggio."*
*"Ultrapassar os proprios limites!"*
