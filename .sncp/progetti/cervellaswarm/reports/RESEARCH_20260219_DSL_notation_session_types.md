# DSL Notation for Session Types and Protocol Description Languages

**Data:** 2026-02-19
**Autrice:** Cervella Researcher
**Status:** COMPLETA
**Fonti consultate:** 26 (WebSearch + WebFetch + file locali)
**Scope:** Notazioni DSL per session types multiparty con focus sul design pratico per CervellaSwarm

---

## EXECUTIVE SUMMARY

**Obiettivo:** Progettare una sintassi testuale per descrivere protocolli di comunicazione multi-agente CervellaSwarm (17 agenti AI, messaggi tipizzati come TaskRequest, AuditRequest, etc.).

**Conclusioni chiave:**

- Scribble e la notazione DSL piu matura per MPST, ma verbosa e Java-centric
- La notazione accademica MPST usa simboli Unicode non digitabili (`mu`, `oplus`, `amp`) - inadatta per DSL testuali
- Il Pi-calculus e eccessivamente teorico per usi pratici
- Proto3/gRPC e AsyncAPI sono riferimenti pratici eccellenti ma non catturano i protocolli multi-step
- La notazione `!`/`?` degli studi accademici (Stanford, wen.works) e intuitiva e adottata universalmente
- Per CervellaSwarm: una sintassi ibrida ispirata a Scribble + Pi-calculus + proto3 e la scelta ottimale
- Parsing senza dipendenze esterne: `re` stdlib + recursive descent e completamente fattibile

**Raccomandazione:** Adottare la notazione proposta in sezione 7 di questo report.

---

## PARTE 1: SCRIBBLE - IL RIFERIMENTO PRINCIPALE

### 1.1 Panoramica

Scribble e il DSL testuale piu maturo per Multiparty Session Types. Sviluppato a Imperial College London (Nobuko Yoshida, Raymond Hu) con implementazioni Java, OCaml (nuScr), Go, Scala.

**Struttura di un file Scribble:**
```
module <package.name>;                          // dichiarazione modulo
type <java> "java.lang.String" from "rt.jar" as String;  // import tipi
global protocol <Name>(role A, role B, ...) { ... }      // protocollo
```

### 1.2 Sintassi Completa

**Dichiarazione ruoli:**
```scribble
global protocol DelegateTask(role Regina, role Worker, role Guardiana) {
  ...
}
```

**Messaggio singolo (send + receive in un'unica notazione globale):**
```scribble
TaskRequest(Payload) from Regina to Worker;
```
Il mittente (`from`) manda, il destinatario (`to`) riceve. NON c'e `!` e `?` nella notazione globale Scribble. La proiezione locale genera:
- Lato Regina: `TaskRequest(Payload) to Worker;`
- Lato Worker: `TaskRequest(Payload) from Regina;`

**Choice (scelta):**
```scribble
choice at Regina {
    Approve(Decision) from Regina to Architect;
    TaskRequest(Payload) from Regina to Worker;
    TaskResult(Result) from Worker to Regina;
    AuditRequest(Data) from Regina to Guardiana;
    AuditVerdict(Score) from Guardiana to Regina;
} or {
    Reject(Reason) from Regina to Architect;
    PlanProposal(Plan) from Architect to Regina;
}
```
La regola fondamentale: ogni branch DEVE iniziare con un messaggio dal `role at` (il decider) verso lo stesso destinatario, con label DIVERSA. Questo garantisce che il ricevitore possa distinguere il branch dal primo messaggio.

**Recursion:**

Metodo 1 - `rec` / `continue`:
```scribble
rec loop {
    Add(Int, Int) from Client to Server;
    Result(Int) from Server to Client;
    continue loop;
}
```

Metodo 2 - `do` (sub-protocol invocation):
```scribble
global protocol Adder(role Client, role Server) {
    choice at Client {
        Add(Int, Int) from Client to Server;
        Result(Int) from Server to Client;
        do Adder(Client, Server);   // ricorsione tramite do
    } or {
        Quit() from Client to Server;
    }
}
```

**Parallel (parallelo):**
```scribble
par {
    Request(Data) from A to B;
} and {
    Notify(Info) from A to C;
}
```

**Interruptible:**
```scribble
interruptible BuyGoods(Buyer, Seller) by {
    Buyer: OrderExpired(Reason);
    Seller: OutOfStock(Reason);
} {
    QuoteRequest() from Buyer to Seller;
    Quote(Price) from Seller to Buyer;
    Order(Item) from Buyer to Seller;
    OrderConf() from Seller to Buyer;
}
```

**Esempio completo: BuyGoods**
```scribble
module commerce;
type <java> "java.lang.String" from "rt.jar" as String;
type <java> "java.lang.Integer" from "rt.jar" as Int;

global protocol BuyGoods(role Buyer, role Seller, role Shipper) {
    QuoteRequest(String) from Buyer to Seller;
    choice at Seller {
        Quote(Int) from Seller to Buyer;
        Order(String) from Buyer to Seller;
        OrderConfirmation() from Seller to Buyer;
        ShipRequest(String) from Seller to Shipper;
        ShipConfirmation() from Shipper to Seller;
    } or {
        OutOfStock() from Seller to Buyer;
    }
}
```

### 1.3 Proiezione Locale (Local Protocol)

Il tipo locale di `Buyer` nel protocollo sopra sarebbe:
```scribble
local protocol BuyGoods at Buyer(role Buyer, role Seller) {
    QuoteRequest(String) to Seller;
    choice at Seller {
        Quote(Int) from Seller;
        Order(String) to Seller;
        OrderConfirmation() from Seller;
    } or {
        OutOfStock() from Seller;
    }
}
```

### 1.4 BNF / Grammatica Formale Scribble (v0.3)

```ebnf
global_protocol ::= 'global' 'protocol' ID '(' role_list ')' '{' global_block '}'
role_list        ::= 'role' ID (',' 'role' ID)*
global_block     ::= global_interaction*
global_interaction ::=
    | message_sig 'from' ID 'to' ID ';'          -- send/receive
    | 'choice' 'at' ID '{' global_block '}' ('or' '{' global_block '}')+
    | 'par' '{' global_block '}' ('and' '{' global_block '}')+
    | 'rec' ID '{' global_block '}'
    | 'continue' ID ';'
    | 'do' ID '(' role_args ')' ';'
message_sig      ::= ID ('(' payload_list ')')?
payload_list     ::= payload_type (',' payload_type)*
```

### 1.5 Valutazione per CervellaSwarm

| Aspetto | Valutazione |
|---------|-------------|
| Espressivita | ALTA (choice, recursion, parallel, interruptible) |
| Verbosita | ALTA (`from X to Y` per ogni messaggio) |
| Adattabilita | MEDIA (Java-centric, type imports da JAR) |
| Tooling | BASSO (scribble-java dormiente, nuScr OCaml) |
| Familiarita per dev | MEDIA (syntassi Java-like) |
| Python DSL | NON esiste |

**Giudizio:** Ottima ispirazione architettonica, troppo verbosa per uso diretto.

---

## PARTE 2: NOTAZIONE ACCADEMICA MPST

### 2.1 Global Types: Notazione Formale

La notazione standard accademica (Coppo-Demangeon-Honda-Yoshida 2016):

```
G ::= p → q : {l_i(T_i).G_i}_{i∈I}    -- choice globale con label
    | mu t.G                             -- ricorsione
    | t                                  -- variabile ricorsione
    | end                                -- terminazione
```

**Esempio Travel Agency (classico MPST):**
```
G = c → a : query(String).
    a → h : available(Hotel).
    a → c : quote(Price).
    c → a : { accept().
               a → h : book(BookingRef).
               a → c : confirm(BookingRef).end
             | reject().end
             }
```

Dove:
- `c → a : m(T).G` = cliente manda messaggio `m` con tipo `T` all'agenzia, poi protocollo `G`
- `mu t.G` = ricorsione legata alla variabile `t`
- `{accept() ... | reject() ...}` = scelta interna al cliente (internal choice)

### 2.2 Local Types: Notazione Formale

La proiezione di G al participante `p` produce un tipo locale:

```
T ::= p!{l_i(T_i).S_i}_{i∈I}    -- send (internal choice, oplus)
    | p&{l_i(T_i).S_i}_{i∈I}    -- receive (external choice, ampersand)
    | mu t.T                      -- ricorsione
    | t                           -- variabile
    | end
```

**Simboli chiave:**
- `!` o `⊕` = send / internal choice (IO scelgo quale label mandare)
- `?` o `&` = receive / external choice (IO ricevo la scelta altrui)
- `mu t.T` = tipo ricorsivo legato alla variabile `t`
- `end` = fine protocollo

**Esempio: Binary Session Type per SMTP**
```
SMTPClient = ⊕ {
    EHLO: !Domain. !FromAddress. !ToAddress. !Message. SMTPClient
    QUIT: end
}
```
- `⊕` = il client sceglie tra EHLO e QUIT
- `!Domain` = manda un valore di tipo Domain
- Ricorsione: `SMTPClient` riappare (protocollo continua in loop)

Il duale (server):
```
SMTPServer = & {
    EHLO: ?Domain. ?FromAddress. ?ToAddress. ?Message. SMTPServer
    QUIT: end
}
```
- `&` = il server riceve (aspetta la scelta del client)
- `?Domain` = riceve un valore di tipo Domain

### 2.3 Binary Session Types: Notazione Minimale

Per protocolli binari (2 partecipanti), la notazione e piu semplice:
```
S ::= !T.S    -- manda T poi continua con S
    | ?T.S    -- ricevi T poi continua con S
    | mu a.S  -- ricorsione (a e la variabile)
    | a       -- variabile ricorsiva
    | end     -- terminazione

Dualita: dual(!T.S) = ?T.dual(S)
         dual(?T.S) = !T.dual(S)
         dual(end)  = end
```

**Esempio: ATM server perspective**
```
ATM = ?CardNum.
      choose {
        ok:  ATM_auth
        err: end
      }

ATM_auth = offer {
    deposit:  ?Amount. !Balance. end
    withdraw: ?Amount.
              choose {
                ok:  end
                err: end
              }
}
```

**BNF (da Stanford CS242):**
```ebnf
SessionType σ ::= recv τ; σ          -- receive message of type τ
                | send τ; σ          -- send message of type τ
                | choose {L: σ_L | R: σ_R}   -- choose sub-protocol
                | offer  {L: σ_L | R: σ_R}   -- offer sub-protocol
                | μ α. σ             -- recursive session type
                | α                  -- session type variable
                | ε                  -- end protocol
```

### 2.4 Valutazione per CervellaSwarm

| Aspetto | Valutazione |
|---------|-------------|
| Precisione formale | ALTA |
| Leggibilita pratica | BASSA (simboli Unicode: mu, oplus, &) |
| Multiparty | SI (MPST global types) |
| Testuale digitabile | NO (oplus, ampersand = Unicode) |
| Adattabilita | BASSA (notazione pensata per paper, non editors) |

**Giudizio:** Ottimo per comprendere la semantica. Inutilizzabile come DSL testuale diretto. Il simbolo `!` e `?` rimangono come convenzione adottata per la notazione locale.

---

## PARTE 3: PI-CALCULUS

### 3.1 Notazione di Base

Il Pi-calculus (Milner 1992) modella processi concorrenti con canali mobili:

```
P ::= 0                    -- processo nullo
    | a(x).P              -- input: ricevi x su canale a, continua P
    | a<x>.P              -- output: manda x su canale a, continua P
    | (nu x) P            -- new: crea nuovo nome x locale a P
    | P | Q               -- parallel composition
    | !P                  -- replication (P forever)
    | [x=y] P             -- match guard
    | P + Q               -- choice (nondeterministic)
```

**Esempio: Handoff di canale (la caratteristica distinctive del Pi-calc)**
```
Server: a(x).x<reply>.0
Client: (nu b) a<b>.(b(v).0)
```
Il client crea un nuovo canale `b`, lo manda al server su `a`. Il server risponde su `b`. Il Pi-calculus permette di passare canali come valori - questo e il "mobile" nel Calculus of Mobile Processes.

**CCS (Calculus of Communicating Systems, Milner 1980):**
```
a.P      -- prefix: esegui azione a, poi P
a.P      -- (overline a) = output su canale a
P + Q    -- choice
P | Q    -- parallel
P[f]     -- renaming
P\L      -- restriction (canali L privati)
```

**CSP (Communicating Sequential Processes, Hoare 1978):**
```
c!v      -- send valore v su canale c
c?x      -- receive da canale c in variabile x
P [] Q   -- external choice (environment decides)
P |~| Q  -- internal choice (process decides)
P || Q   -- parallel
SKIP     -- terminazione normale
STOP     -- deadlock
```

**Nota sulla notazione CSP:**
- `c!v` = manda `v` su `c` (analoga a `!` in session types)
- `c?x` = ricevi da `c` in `x` (analoga a `?`)
- La notazione `!`/`?` dei session types e DIRETTAMENTE derivata da CSP

### 3.2 Valutazione per CervellaSwarm

| Aspetto | Valutazione |
|---------|-------------|
| Espressivita | MASSIMA (Turing-complete) |
| Praticabilita | BASSA (troppo low-level) |
| Multiparty | NO (modello binario, moltiplicita via composizione) |
| Legame con session types | ALTO (pi-calculus = fondamento teorico) |
| DSL testuale | NO (notazione processo, non protocollo) |

**Giudizio:** Fondamento teorico utile. La notazione `!` e `?` viene da qui. NON adatto come DSL pratico per protocolli multi-agente.

---

## PARTE 4: PROTOCOL BUFFERS / GRPC

### 4.1 Sintassi proto3 per Servizi

```protobuf
syntax = "proto3";

// Dichiarazione messaggi (analogo dei message types)
message TaskRequest {
  string task_id     = 1;
  string description = 2;
  repeated string files = 3;
}

message TaskResult {
  string task_id = 1;
  bool   success = 2;
  string output  = 3;
}

message AuditRequest {
  string task_id    = 1;
  string work_done  = 2;
}

message AuditVerdict {
  string task_id = 1;
  float  score   = 2;
  string comment = 3;
}

// Definizione servizi (NON cattura sequenze multi-step)
service WorkerService {
  rpc ExecuteTask (TaskRequest)  returns (TaskResult);
}

service GuardianaService {
  rpc AuditWork (AuditRequest) returns (AuditVerdict);
}

// Streaming (piu vicino a protocolli continui)
service StreamingService {
  rpc ServerStream (TaskRequest)   returns (stream TaskResult);
  rpc ClientStream (stream TaskRequest) returns (TaskResult);
  rpc BidiStream   (stream TaskRequest) returns (stream TaskResult);
}
```

### 4.2 Analisi delle Lacune per Protocol Description

Proto3 descrive INTERFACCE di servizio (RPC singoli), NON PROTOCOLLI MULTI-STEP.

Non puo esprimere:
- "Prima manda A, poi ricevi B, poi scegli tra C e D"
- Choice condizionale basata sulla risposta
- Sequenze obbligatorie di messaggi

**Cio che proto3 fa bene:**
- Tipi di messaggio precisi con field numbers stabili
- Evoluzione backward-compatible dei messaggi
- Codegen per multiple lingue
- Definizione di servizi con contratti chiari per singole chiamate

### 4.3 AsyncAPI come Alternativa

AsyncAPI 3.0 (YAML/JSON) per event-driven:

```yaml
asyncapi: 3.0.0
info:
  title: CervellaSwarm Communication
  version: 1.0.0

channels:
  agentCommunication:
    address: 'swarm.{sessionId}'
    messages:
      taskRequest:
        $ref: '#/components/messages/taskRequest'
      taskResult:
        $ref: '#/components/messages/taskResult'

operations:
  sendTask:
    action: send
    channel:
      $ref: '#/channels/agentCommunication'
    messages:
      - $ref: '#/components/messages/taskRequest'
  receiveResult:
    action: receive
    channel:
      $ref: '#/channels/agentCommunication'
    messages:
      - $ref: '#/components/messages/taskResult'

components:
  messages:
    taskRequest:
      payload:
        type: object
        properties:
          task_id: {type: string}
          description: {type: string}
```

**AsyncAPI vs Session Types:**
- AsyncAPI descrive canali e messaggi SINGOLI
- NON descrive l'ORDINE o la SEQUENZA di messaggi
- NON ha choice o recursion per il flusso del protocollo
- Utile come complemento per definire i message schemas

### 4.4 Valutazione per CervellaSwarm

| Aspetto | Proto3 | AsyncAPI |
|---------|--------|----------|
| Definizione tipi messaggi | OTTIMO | BUONO |
| Sequenze multi-step | NO | NO |
| Choice/branching | NO | NO |
| Recursion/loop | NO | NO |
| Leggibilita | ALTA | ALTA |
| Tooling | ECCELLENTE | BUONO |

**Giudizio:** Eccellenti come riferimento per la definizione dei tipi di messaggio. NON sostituiscono un DSL per protocolli sequenziali con scelte.

---

## PARTE 5: PYTHON DSL SENZA DIPENDENZE ESTERNE

### 5.1 Strategie Disponibili

Tre approcci per DSL in Python puro (solo stdlib):

**A) Internal DSL con Fluent Interface (Builder Pattern)**
```python
# Nessun parsing, il DSL E Python
protocol = (
    Protocol("DelegateTask")
    .roles("regina", "worker", "guardiana")
    .step("regina", SEND, "TaskRequest", TO, "worker")
    .step("worker", SEND, "TaskResult", TO, "regina")
    .choice(
        AT, "regina",
        branch("approve").step("regina", SEND, "TaskApproved", TO, "worker"),
        branch("reject").step("regina", SEND, "TaskRejected", TO, "worker"),
    )
    .build()
)
```
- Pro: zero parsing, type-safe, IDE autocomplete
- Contro: non e DSL testuale (non si puo leggere da file `.proto`-like)

**B) Tokenizer con `re` stdlib + Recursive Descent Parser**

Il pattern classico usando solo `re`:
```python
import re
from dataclasses import dataclass
from typing import Iterator

# Token definition
TOKEN_SPEC = [
    ('KEYWORD',    r'\b(protocol|roles|choice|at|or|rec|end|do)\b'),
    ('SEND_OP',    r'!'),
    ('RECV_OP',    r'\?'),
    ('ARROW',      r'->'),
    ('LBRACE',     r'\{'),
    ('RBRACE',     r'\}'),
    ('LPAREN',     r'\('),
    ('RPAREN',     r'\)'),
    ('COMMA',      r','),
    ('SEMICOLON',  r';'),
    ('IDENT',      r'[A-Za-z_][A-Za-z0-9_]*'),
    ('SKIP',       r'[ \t\n\r]+'),  # whitespace
    ('COMMENT',    r'//[^\n]*'),    # line comments
    ('MISMATCH',   r'.'),           # errore
]

# Master regex con named groups
MASTER_RE = re.compile(
    '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPEC)
)

@dataclass
class Token:
    kind: str
    value: str
    line: int

def tokenize(source: str) -> Iterator[Token]:
    line = 1
    for mo in MASTER_RE.finditer(source):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'SKIP':
            line += value.count('\n')
            continue
        if kind == 'COMMENT':
            continue
        if kind == 'MISMATCH':
            raise SyntaxError(f"Unexpected character {value!r} at line {line}")
        yield Token(kind, value, line)
```

**C) `re.Scanner` (stdlib non documentato)**
```python
import re

def make_scanner(rules):
    """Build scanner from (pattern, action) list."""
    scanner = re.Scanner([(pattern, action) for pattern, action in rules])
    return scanner
```

### 5.2 Recursive Descent Parser Pattern

```python
class Parser:
    """Hand-written recursive descent parser. Zero dependencies."""

    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> Token:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else Token('EOF', '', 0)

    def consume(self, kind: str = None) -> Token:
        tok = self.peek()
        if kind and tok.kind != kind:
            raise SyntaxError(f"Expected {kind}, got {tok.kind!r} ({tok.value!r}) at line {tok.line}")
        self.pos += 1
        return tok

    def match(self, kind: str) -> bool:
        return self.peek().kind == kind

    def parse_protocol(self) -> ProtocolAST:
        """protocol ::= 'protocol' IDENT '{' roles_decl body '}'"""
        self.consume('KEYWORD')  # 'protocol'
        name = self.consume('IDENT').value
        self.consume('LBRACE')
        roles = self.parse_roles()
        body = self.parse_body()
        self.consume('RBRACE')
        return ProtocolAST(name=name, roles=roles, body=body)

    def parse_roles(self) -> list[str]:
        """roles ::= 'roles' IDENT (',' IDENT)* ';'"""
        self.consume('KEYWORD')  # 'roles'
        names = [self.consume('IDENT').value]
        while self.match('COMMA'):
            self.consume('COMMA')
            names.append(self.consume('IDENT').value)
        self.consume('SEMICOLON')
        return names

    def parse_interaction(self) -> InteractionAST:
        """
        interaction ::= IDENT '!' MsgType '->' IDENT ';'   -- send
                      | IDENT '?' MsgType '->' IDENT ';'   -- receive (alternative)
                      | 'choice' 'at' IDENT '{' ... '}'    -- choice
                      | 'rec' IDENT '{' ... '}'             -- recursion
        """
        if self.match('IDENT') and self.tokens[self.pos + 1].kind in ('SEND_OP', 'RECV_OP'):
            return self.parse_send_recv()
        elif self.peek().value == 'choice':
            return self.parse_choice()
        elif self.peek().value == 'rec':
            return self.parse_recursion()
        else:
            raise SyntaxError(f"Unexpected token {self.peek()!r}")
```

### 5.3 AST Nodes come Dataclass

```python
from dataclasses import dataclass, field

@dataclass
class SendAST:
    sender: str
    message_type: str
    receiver: str

@dataclass
class ChoiceAST:
    decider: str
    branches: dict[str, list]  # label -> [interaction...]

@dataclass
class RecursionAST:
    label: str
    body: list

@dataclass
class ProtocolAST:
    name: str
    roles: list[str]
    body: list  # list of SendAST | ChoiceAST | RecursionAST
```

### 5.4 Valutazione

| Tecnica | Dipendenze | Complessita | Robustezza |
|---------|------------|-------------|------------|
| Fluent Builder | ZERO | BASSA | ALTA |
| re + Recursive Descent | ZERO | MEDIA | ALTA |
| re.Scanner | ZERO | BASSA | MEDIA |
| lark | +1 dep | BASSA | ALTA |
| pyparsing | +1 dep | MEDIA | ALTA |
| PLY | +1 dep | ALTA | ALTA |

**Giudizio:** Per CervellaSwarm (zero dipendenze e un vincolo del progetto), il combination `re` tokenizer + recursive descent parser e la scelta ideale. E la stessa tecnica usata da compilatori reali (Ruff ha un recursive descent parser hand-written).

---

## PARTE 6: LINGUAGGI E SISTEMI AFFINI

### 6.1 Ferrite (Rust) - Type-Level Encoding

```rust
// Tipi come algebraic data types nel type system
type ServerProto = ReceiveValue<i64,  // ricevi i64
                    SendValue<bool,   // manda bool
                    End>>;            // fine

// Internal choice
type ServiceProto = InternalChoice<HNil /* Empty */,
    // branch A: ricevi stringa, manda risultato
    ReceiveValue<String, SendValue<i64, End>>,
    // branch B: solo end
    End
>;

// External choice
type ClientProto = ExternalChoice<HNil,
    SendValue<String, ReceiveValue<i64, End>>,
    End
>;
```

**Pattern Ferrite:**
- `SendValue<T, Continuation>` = manda T, poi segui Continuation
- `ReceiveValue<T, Continuation>` = ricevi T, poi segui Continuation
- `InternalChoice` = provider sceglie (send)
- `ExternalChoice` = client sceglie (receive)
- `End` = fine sessione

### 6.2 Rust session_types (Munksgaard)

```rust
// Binary session types (solo 2 partecipanti)
type Server = Recv<i64, Send<bool, Eps>>;
type Client = <Server as HasDual>::Dual;  // = Send<i64, Recv<bool, Eps>>

// Usage
fn server(chan: Chan<(), Server>) {
    let (chan, n) = chan.recv();     // ricevi i64
    let result = n > 0;
    chan.send(result).close();       // manda bool, close
}
```

**Pattern:** `Send<T, P>`, `Recv<T, P>`, `Offer<P, Q>`, `Choose<P, Q>`, `Eps`, `Rec`, `Var`.

### 6.3 FIPA-ACL / KQML - Approccio Message-Centric

KQML (Knowledge Query and Manipulation Language, 1994) - approccio storico agli AI agents:
```
(ask-one
  :sender     joe
  :content    (PRICE IBM ?price)
  :receiver   stock-server
  :reply-with ibm-stock
  :language   LPROLOG
  :ontology   NYSE-TICKS
)
```

FIPA-ACL - struttura di un messaggio:
```
(inform
  :sender    (agent-identifier :name i)
  :receiver  (set (agent-identifier :name j))
  :content   "temperature(rome, 35)"
  :language  fipa-sl
  :ontology  weather-forecast
)
```

**Performativi FIPA (subset):** `inform`, `request`, `query-if`, `agree`, `refuse`, `failure`, `propose`, `accept-proposal`, `reject-proposal`.

**Analisi critica:** FIPA-ACL e KQML descrivono messaggi singoli con semantica speech-act. NON descrivono la SEQUENZA e il FLOW del protocollo. Ogni messaggio e indipendente. Questo e il gap che CervellaSwarm sta cercando di colmare.

### 6.4 nuScr - Il Tool Piu Moderno per MPST

nuScr (OCaml, 2022) usa la stessa sintassi Scribble con alcune variazioni:
```
(* nuScr notation - compatibile Scribble *)
protocol TravelAgency(role C, role A, role H) {
  query(String) from C to A;
  available(Hotel) from A to H;
  quote(Price) from A to C;
  choice at C {
    accept() from C to A;
    book(Hotel) from A to H;
    confirm(Ref) from A to C;
  } or {
    reject() from C to A;
  }
}
```

**Tool capability di nuScr:**
- Parsing e validazione del protocollo globale
- Proiezione a tipi locali per ogni ruolo
- Conversione a CFSM (Communicating Finite State Machines)
- Generazione codice OCaml

---

## PARTE 7: DESIGN PROPOSTO PER CERVELLASWARM

### 7.1 Principi di Design

Dalla ricerca emergono questi principi per la notazione CervellaSwarm:

1. **Notazione globale** (come Scribble) - descrive il protocollo dall'esterno, non dal punto di vista di un singolo agente
2. **`!`/`?` nel testo**, ma come suggerimento opzionale nella notazione locale proiettata
3. **`sender -> receiver : MessageType`** - notazione compatta per i passi (ispirata al formalismo MPST con freccia)
4. **`choice at Role { branch_label: ... } or { ... }`** - esplicito chi decide
5. **`rec Label { ... continue Label }`** - ricorsione esplicita con label
6. **Tipi di messaggio come identificatori** - non richiedono dichiarazioni di tipo esplicite (si riferiscono a `MessageKind` esistenti)
7. **Commenti con `//`** - convenzione Unix standard

### 7.2 Proposta di Grammatica (EBNF)

```ebnf
protocol_file   ::= protocol_decl+
protocol_decl   ::= 'protocol' IDENT '{' roles_decl body '}'
roles_decl      ::= 'roles' role_list ';'
role_list       ::= IDENT (',' IDENT)*

body            ::= interaction*
interaction     ::= send_step
                  | choice_block
                  | rec_block
                  | do_stmt

send_step       ::= IDENT '->' IDENT ':' IDENT ';'
                    (* sender -> receiver : MessageType ; *)

choice_block    ::= 'choice' 'at' IDENT '{' branch ('or' branch)* '}'
branch          ::= IDENT ':' '{' body '}'

rec_block       ::= 'rec' IDENT '{' body '}'
continue_stmt   ::= 'continue' IDENT ';'
do_stmt         ::= 'do' IDENT '(' role_list ')' ';'

IDENT           ::= [A-Za-z_][A-Za-z0-9_]*
```

### 7.3 Sintassi Proposta con Esempi Concreti

**Esempio 1: SimpleTask**
```
protocol SimpleTask {
    roles regina, worker;

    regina -> worker : TaskRequest;
    worker -> regina : TaskResult;
}
```

**Esempio 2: DelegateTask (con audit)**
```
protocol DelegateTask {
    roles regina, worker, guardiana;

    // Regina delega il task
    regina -> worker    : TaskRequest;
    worker -> regina    : TaskResult;

    // Audit obbligatorio
    regina -> guardiana : AuditRequest;
    guardiana -> regina : AuditVerdict;
}
```

**Esempio 3: ArchitectFlow (con choice)**
```
protocol ArchitectFlow {
    roles regina, architect, worker, guardiana;

    // Fase planning
    regina    -> architect : PlanRequest;
    architect -> regina    : PlanProposal;

    // Regina decide
    choice at regina {
        approve: {
            regina    -> architect  : PlanDecision;
            regina    -> worker     : TaskRequest;
            worker    -> regina     : TaskResult;
            regina    -> guardiana  : AuditRequest;
            guardiana -> regina     : AuditVerdict;
        }
        reject: {
            regina    -> architect  : PlanDecision;
            architect -> regina     : PlanProposal;
        }
    }
}
```

**Esempio 4: Con recursion (AgentLoop)**
```
protocol AgentLoop {
    roles regina, worker;

    rec loop {
        regina -> worker : TaskRequest;
        worker -> regina : TaskResult;

        choice at regina {
            continue_loop: {
                continue loop;
            }
            stop: {
                // protocollo termina
            }
        }
    }
}
```

**Esempio 5: EscalationFlow (messaggi di errore)**
```
protocol EscalationFlow {
    roles regina, worker, guardiana_qualita;

    // Primo tentativo
    regina -> worker : TaskRequest;

    choice at worker {
        success: {
            worker  -> regina            : TaskResult;
            regina  -> guardiana_qualita : AuditRequest;
            guardiana_qualita -> regina  : AuditVerdict;
        }
        failure: {
            worker  -> regina : ErrorReport;
            regina  -> regina : Escalation;  // self-reflection
        }
        need_clarification: {
            worker  -> regina : ClarificationRequest;
            regina  -> worker : ClarificationResponse;
            // poi ritorna al TaskRequest via recursion esterna
        }
    }
}
```

**Esempio 6: ResearchFlow (3 partecipanti)**
```
protocol ResearchFlow {
    roles regina, researcher, guardiana_ricerca;

    regina             -> researcher      : ResearchQuery;
    researcher         -> regina          : ResearchReport;
    regina             -> guardiana_ricerca : AuditRequest;
    guardiana_ricerca  -> regina          : AuditVerdict;
}
```

### 7.4 Notazione Locale (Proiettata)

La proiezione del punto di vista di `worker` in `DelegateTask`:

```
local protocol DelegateTask at worker {
    roles regina, worker, guardiana;

    // Worker perspective: uses ! for send, ? for receive
    ? TaskRequest  from regina;    // ricevi da regina
    ! TaskResult   to   regina;    // manda a regina
    // nessuna interazione con guardiana - proiezione omette
}
```

La notazione locale usa `!` e `?` espliciti come in CSP/binary session types, con `from`/`to` espliciti per la controparte.

### 7.5 Mapping con il Package Esistente

La sintassi proposta mappa direttamente sull'attuale `protocols.py`:

| DSL notation | Python dataclass |
|---|---|
| `protocol DelegateTask { ... }` | `Protocol(name="DelegateTask", ...)` |
| `roles regina, worker;` | `roles=("regina", "worker")` |
| `regina -> worker : TaskRequest;` | `ProtocolStep(sender="regina", receiver="worker", message_kind=MessageKind.TASK_REQUEST)` |
| `choice at regina { approve: {...} or reject: {...} }` | `ProtocolChoice(decider="regina", branches={"approve": (...), "reject": (...)})` |

Il parser produrrebbe esattamente le stesse strutture `Protocol`, `ProtocolStep`, `ProtocolChoice` gia definite. Il DSL e uno strato SOPRA il modello Python esistente.

---

## PARTE 8: ANALISI COMPARATIVA DELLE NOTAZIONI

### 8.1 Tabella Comparativa Simboli

| Operazione | Scribble | MPST Formale | Pi-calc | CSP | Binary Session | Proposta CervellaSwarm |
|---|---|---|---|---|---|---|
| Manda msg | `Msg from A to B;` | `A → B : m(T)` | `a<x>.P` | `c!v` | `!T.S` | `A -> B : Msg;` |
| Ricevi msg | (proiezione) | (proiezione) | `a(x).P` | `c?x` | `?T.S` | (solo in local) |
| Choice interna | `choice at A { } or { }` | `⊕{l_i : T_i}` | `P + Q` | `P [] Q` | `choose{L: σ \| R: σ}` | `choice at A { l: {...} or l: {...} }` |
| Choice esterna | (proiezione) | `&{l_i : T_i}` | - | `P \|~\| Q` | `offer{L: σ \| R: σ}` | (solo in local) |
| Ricorsione | `rec L { continue L; }` | `mu t.T` | `!P` | `mu P.E` | `mu a.S` | `rec L { continue L; }` |
| Fine | (implicito) | `end` | `0` | `SKIP` | `ε` | (implicito o `end;`) |
| Parallelo | `par { } and { }` | - | `P \| Q` | `P \|\| Q` | - | (futuro) |

### 8.2 Strengths e Weaknesses per AI Agents

**Scribble:**
- Strength: multiparty nativo, proiezione automatica, tooling maturo
- Weakness: verboso (`from X to Y` ogni riga), Java-centric, nessun tooling Python

**MPST Formale:**
- Strength: semantica precisa, deadlock-freedom dimostrabile
- Weakness: simboli Unicode non digitabili, troppo teorico per developers

**Pi-calculus:**
- Strength: teoricamente completo, mobilita dei canali
- Weakness: nessuna nozione di "ruolo", troppo low-level, non leggibile

**Proto3:**
- Strength: pratico, ottimo per tipi messaggi, tooling eccellente
- Weakness: non cattura sequenze o protocolli multi-step

**Proposta CervellaSwarm:**
- Strength: compatta (freccia `->` vs verboso `from X to Y`), mappa 1:1 al modello dati esistente, leggibile, zero ambiguita su chi decide il choice
- Weakness: non ha proiezione automatica (da implementare), no parallel (per ora)

---

## PARTE 9: IMPLEMENTAZIONE DSL IN PYTHON (ZERO DEPS)

### 9.1 Schema Architettura

```
input: stringa DSL
    |
    v
[Tokenizer] re stdlib, named groups
    |
    v
[Recursive Descent Parser] dataclass puri
    |
    v
[AST] ProtocolFileAST -> ProtocolAST -> [SendAST | ChoiceAST | RecAST]
    |
    v
[Transpiler] AST -> Protocol / ProtocolStep / ProtocolChoice
    |
    v
[Validator] Protocol.__post_init__ gia esistente
    |
    v
output: Protocol objects (gia testati con 153 test)
```

### 9.2 Token Types Richiesti

```python
TOKEN_SPEC = [
    ('COMMENT',   r'//[^\n]*'),               # // commenti
    ('KEYWORD',   r'\b(protocol|roles|choice|at|or|rec|continue|do|end|local)\b'),
    ('ARROW',     r'->'),                      # ->
    ('LBRACE',    r'\{'),
    ('RBRACE',    r'\}'),
    ('LPAREN',    r'\('),
    ('RPAREN',    r'\)'),
    ('COMMA',     r','),
    ('SEMICOLON', r';'),
    ('COLON',     r':'),
    ('BANG',      r'!'),                       # per local notation
    ('QUESTION',  r'\?'),                      # per local notation
    ('IDENT',     r'[A-Za-z_][A-Za-z0-9_]*'), # identifier
    ('WHITESPACE',r'[ \t\n\r]+'),              # skip
]
```

**Stima dimensioni:** Tokenizer ~50 righe, Parser ~150 righe, AST ~30 righe, Transpiler ~50 righe = ~280 righe totali. Completamente testabile con pytest. Zero dipendenze esterne.

### 9.3 Error Messages

Inspirati dalla qualita di Rust:
```
SyntaxError at line 5:
    regina -> wrker : TaskRequest;
               ^^^^^
    Unknown role 'wrker'. Declared roles: regina, worker, guardiana.
    Hint: Did you mean 'worker'?
```

---

## SINTESI E RACCOMANDAZIONE FINALE

### Cosa Adottare

**Per la notazione DSL testuale di CervellaSwarm:**

1. **Usare la sintassi proposta in sezione 7** - `sender -> receiver : MessageType;`
2. **Ispirarsi a Scribble** per: `choice at Role`, `rec Label / continue Label`, struttura del file
3. **Prendere `!`/`?` da Binary Session Types** per la notazione locale proiettata
4. **Ignorare Pi-calculus** come notazione diretta (troppo low-level)
5. **Usare proto3 come riferimento** solo per la definizione dei message types (non il flow)
6. **Implementare con `re` + recursive descent** - zero deps, ~280 righe

### Gap CervellaSwarm Confermati

- Nessun DSL testuale per AI agents in Python esiste (confermato dal report precedente)
- La proposta CervellaSwarm sarebbe la PRIMA notazione DSL open source per protocolli AI agent con:
  - Multiparty nativo (non solo binario)
  - Ruoli gerarchici (Regina > Guardiana > Worker)
  - Mapping diretto a runtime checker esistente
  - Zero dipendenze
  - Python puro

---

## FONTI CONSULTATE (26)

1. Scribble Language Reference v0.3 - http://www.doc.ic.ac.uk/~rhu/scribble/langref.html
2. Scribble Java Tutorial - https://www.doc.ic.ac.uk/~rhu/scribble/tutorial/
3. Scribble Protocol Guide (JBoss) - https://docs.jboss.org/scribble/releases/2.0.x/protocolguide/pdf/Scribble-Protocol-Guide.pdf
4. JBoss Scribble Constructs 1.0 - https://docs.jboss.org/scribble/1.0.x/protocolguide/html/constructs.html
5. The Scribble Protocol Language (paper) - https://www.dmi.unict.it/barba/FOND-LING-PROG-DISTR/PROGRAMMI-TESTI/READING-MATERIAL/ScribbleTutorial.pdf
6. scribble/scribble-language-guide (GitHub) - https://github.com/scribble/scribble-language-guide
7. nuscr/nuscr (GitHub) - https://github.com/nuscr/nuscr
8. Simon Fowler - Session type implementations - https://simonjf.com/2016/05/28/session-type-implementations.html
9. Stanford CS242 - Session Types - https://stanford-cs242.github.io/f19/lectures/09-1-session-types.html
10. An Introduction to Session Types (wen.works) - https://wen.works/2020/12/17/an-introduction-to-session-types/
11. A Very Gentle Introduction to MPST (Imperial College) - http://mrg.doc.ic.ac.uk/publications/a-very-gentle-introduction-to-multiparty-session-types/main.pdf
12. Multiparty Session Types as Communicating Automata - https://www.cs.rhul.ac.uk/~malo/papers/msa_in_ca.pdf
13. Pi-calculus Wikipedia - https://en.wikipedia.org/wiki/%CE%A0-calculus
14. CSP Wikipedia - https://en.wikipedia.org/wiki/Communicating_sequential_processes
15. CCS Wikipedia - https://en.wikipedia.org/wiki/Calculus_of_communicating_systems
16. Process Calculus Wikipedia - https://en.wikipedia.org/wiki/Process_calculus
17. FAQ on Pi-Calculus (CMU) - https://www.cs.cmu.edu/~wing/publications/Wing02a.pdf
18. Proto3 Language Guide - https://protobuf.dev/programming-guides/proto3/
19. gRPC Introduction - https://grpc.io/docs/what-is-grpc/introduction/
20. AsyncAPI 3.0.0 Spec - https://www.asyncapi.com/docs/reference/specification/v3.0.0
21. AsyncAPI Document Structure - https://www.asyncapi.com/docs/concepts/asyncapi-document/structure
22. Ferrite Session Types Book - https://ferrite-rs.github.io/ferrite-book/01-getting-started/05-session-types.html
23. Regex-based Lexical Analysis in Python (Eli Bendersky) - https://eli.thegreenplace.net/2013/06/25/regex-based-lexical-analysis-in-python-and-javascript
24. Recursive Descent Parser in Python (vey.ie) - https://vey.ie/2018/10/04/RecursiveDescent.html
25. Ruff v0.4.0 hand-written recursive descent - https://astral.sh/blog/ruff-v0.4.0
26. Agent Interoperability Protocols Survey 2025 - https://arxiv.org/html/2505.02279v1

---

*Cervella Researcher - 2026-02-19*
*"Ricerca PRIMA di implementare. Non inventare, studia come fanno i big."*

COSTITUZIONE-APPLIED: SI
Principio usato: "Nulla e complesso - solo non ancora studiato!"
