# Show HN v2 Draft - Lingua Universale

> **Status:** READY (Regina review S455 - titolo fixato, lancio 18 Marzo)
> **Preparato:** Sessione 449, aggiornato S455 - 14 Marzo 2026
> **Focus:** LU come linguaggio di programmazione per AI

---

## TITOLO

```
Show HN: Lingua Universale – A language for verified AI agent protocols
```

---

## LINK

```
https://github.com/rafapra3008/cervellaswarm/tree/main/packages/lingua-universale
```

---

## PRIMO COMMENTO

```
Hey HN! I posted about CervellaSwarm (multi-agent system) back in January.
Since then, the project evolved into something different: a programming language.

Lingua Universale (LU) is a language that models AI agent communication with
session types -- who sends what to whom, in what order, under what contracts.
It compiles to Python and generates Lean 4 proofs.

What's real (not a pitch, just facts):

  - 3684 tests, 31 modules, ZERO external dependencies (pure stdlib)
  - Full compiler: tokenizer -> parser (64 rules) -> AST -> contract checker -> codegen
  - 9 verified property kinds (always_terminates, no_deadlock, no_deletion, role_exclusive...)
  - 20 standard library protocols (AI/ML, Business, Communication, Data, Security)
  - LSP server with diagnostics, hover, completion, go-to-def, formatting
  - VS Code extension on Marketplace: search "Lingua Universale" in Extensions
  - Linter (10 rules) + formatter (zero-config, like gofmt)
  - CI gate: `lu fmt --check` + `lu lint` enforce style on every push
  - NL pipeline: Italian/English/Portuguese -> IntentDraft -> parse -> verify -> Python
  - Browser playground: https://rafapra3008.github.io/cervellaswarm/
  - PyPI: pip install cervellaswarm-lingua-universale (v0.3.3)

The core idea: a 68-year-old Italian grandmother can describe a recipe management
system in plain Italian, and the system generates a protocol with 5 mathematically
proven safety properties. If someone tries to delete a recipe, the runtime blocks
it -- not because we trust the code, but because the session type makes it impossible.

Based on multiparty session types (Honda/Yoshida/Carbone, POPL 2008) and the
two-stage Req2LTL pattern (ASE 2025) for NL-to-formal translation.

What I'd love feedback on:
1. Is session types the right formalism for AI agent coordination?
2. The linter + formatter story -- useful for a DSL this young?
3. Would you use `lu init --template rag_pipeline` to scaffold AI protocols?

Try it:
  pip install cervellaswarm-lingua-universale
  lu chat --lang en          # build a protocol conversationally
  lu demo --lang it          # see the La Nonna demo

Source: https://github.com/rafapra3008/cervellaswarm
Playground: https://rafapra3008.github.io/cervellaswarm/
VS Code: search "Lingua Universale" in Extensions marketplace
```

---

## NOTE

### Cosa e cambiato da v1

| v1 (Gennaio 2026) | v2 (Marzo 2026) |
|--------------------|-----------------|
| Multi-agent framework | Programming language |
| 134 tests | 3684 tests |
| CLI tool | Full compiler + LSP + linter + formatter |
| No formal verification | 9 PropertyKind + Lean 4 |
| No language server | LSP with 5 features |
| No NL interface | 3-language NL pipeline |
| No voice | Local STT voice input |
| No stdlib | 20 verified protocols |
| No playground | Browser playground LIVE |
| No IDE support | VS Code extension on Marketplace |

### Messaggi chiave per HN

1. **"Zero dependencies"** -- HN loves this. Pure Python stdlib.
2. **"3684 tests"** -- Credibility. Show don't tell.
3. **"Lean 4 proofs"** -- Formal methods crowd will care.
4. **"Session types"** -- PL theory crowd will recognize Honda/Yoshida.
5. **"La Nonna"** -- Human story, not just tech.
6. **"gofmt for session types"** -- linter/formatter story resonates.
7. **"VS Code Marketplace"** -- Legitimate tooling, not just a CLI.

### Timing suggerito

- Mattina US West Coast (9-11am PT = 18-20 CET)
- Preferire martedi o mercoledi (piu traffico HN)

---

*Questa e una bozza. Rafa rivede prima del lancio.*
