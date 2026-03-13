# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Grammar exporter: Lingua Universale -> GBNF / Lark (C2.4).

Exports the Lingua Universale grammar in external formats for constrained
decoding by LLMs.  Two formats are supported:

  - **GBNF** -- target: XGrammar, vLLM, llama.cpp
  - **Lark EBNF** -- target: Outlines, llguidance

The exported grammars are *whitespace-lenient* versions of the strict EBNF
grammar used by the parser (64 productions).  INDENT/DEDENT tokens are
replaced by free whitespace (``ws`` / ``%ignore``), so an LLM can generate
syntactically valid ``.lu`` code without tracking indentation depth.

Design decisions (DESIGN C2.4.1, S419, Guardiana 9.6/10):
  D1  Whitespace-lenient (no INDENT/DEDENT -- impossible in CFG).
  D2  Closed list for ``verb`` (5) and ``noun`` (9) -- zero hallucination.
  D3  ``ws`` = ``[ \\t\\n\\r]*``, ``ws1`` = ``[ \\t\\n]+`` (standard de facto).
  D4  Keyword-as-delimiter for blocks (consistent with LU syntax).
  D5  ``comment`` rule in GBNF; ``%ignore`` directive in Lark.
  D6  STRING without internal newlines (aligned GBNF <-> Lark).

Architecture:
  - Rules are **statically encoded** (not derived from ``_parser.py``).
  - Source of truth: EBNF doc + DESIGN_C2_4_1_LLM_GRAMMAR.md.
  - Zero external dependencies.  Zero runtime coupling with the parser.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Version of the exported grammar (bump when rules change).
# ---------------------------------------------------------------------------

GRAMMAR_VERSION = "1.0"

# ---------------------------------------------------------------------------
# GBNF grammar -- 47 rules, whitespace-lenient
# Target: XGrammar, vLLM, llama.cpp
# ---------------------------------------------------------------------------

_GBNF_GRAMMAR = """\
# ============================================================
# Lingua Universale - LLM Grammar (GBNF)
# Target: XGrammar, vLLM, llama.cpp
# Version: {version}
# Rules: 47 (from 64 EBNF productions, whitespace-lenient)
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
                 | "no" ws1 "deletion"
                 | ident ws1 "before" ws1 ident
                 | ident ws1 "cannot" ws1 "send" ws1 ident
                 | ident ws1 "exclusive" ws1 ident
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

string         ::= "\\"" [^"\\n]* "\\""
                 | "'" [^'\\n]* "'"

comment        ::= "#" [^\\n]*

ws             ::= [ \\t\\n\\r]*

ws1            ::= [ \\t\\n]+
"""

# ---------------------------------------------------------------------------
# Lark grammar -- 40 rules + 4 terminals + 2 directives = 46
# Target: Outlines, llguidance
# ---------------------------------------------------------------------------

_LARK_GRAMMAR = """\
# ============================================================
# Lingua Universale - LLM Grammar (Lark EBNF)
# Target: Outlines, llguidance
# Version: {version}
# Rules: 40 rules + 4 terminals + 2 directives = 46 (whitespace-lenient)
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
        | "no" "deletion"
        | IDENT "before" IDENT
        | IDENT "cannot" "send" IDENT
        | IDENT "exclusive" IDENT
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
NUMBER: /[0-9]+(\\.[0-9]+)?/
STRING: /"[^"\\n]*"/ | /'[^'\\n]*'/
COMP_OP: ">=" | "<=" | "==" | "!=" | ">" | "<"

# ---- 11. WHITESPACE & COMMENTS ----

%ignore /\\s+/
%ignore /#[^\\n]*/
"""


class GrammarExporter:
    """Export Lingua Universale grammar for LLM constrained decoding.

    The grammars are statically encoded (not derived from ``_parser.py``).
    They are whitespace-lenient versions of the strict 64-production EBNF
    grammar, designed so an LLM can generate valid ``.lu`` code without
    tracking indentation depth.

    Usage::

        exporter = GrammarExporter()

        # For vLLM / XGrammar / llama.cpp
        gbnf = exporter.to_gbnf()

        # For Outlines / llguidance
        lark_grammar = exporter.to_lark()
    """

    @staticmethod
    def version() -> str:
        """Return the grammar version string."""
        return GRAMMAR_VERSION

    @staticmethod
    def to_gbnf() -> str:
        """Export grammar in GBNF format (47 rules).

        Target runtimes: XGrammar, vLLM, llama.cpp.

        Returns:
            A complete GBNF grammar string ready for
            ``xgrammar.compile_grammar()`` or ``llama.cpp --grammar``.
        """
        return _GBNF_GRAMMAR.format(version=GRAMMAR_VERSION)

    @staticmethod
    def to_lark() -> str:
        """Export grammar in Lark EBNF format (46 rules).

        Target runtimes: Outlines, llguidance.

        Returns:
            A complete Lark grammar string ready for
            ``outlines.generate.cfg(model, grammar)`` or
            ``lark.Lark(grammar)``.
        """
        return _LARK_GRAMMAR.format(version=GRAMMAR_VERSION)
