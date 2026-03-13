# Lingua Universale for VS Code

Full language support for [Lingua Universale](https://github.com/rafapra3008/cervellaswarm) (`.lu` files) -- the first programming language designed for AI agent orchestration with formal verification.

## Features

- **Syntax highlighting** -- full TextMate grammar for `.lu` files
- **Real-time diagnostics** -- errors and lint warnings shown inline as you type (74 error codes, 10 lint rules, 3 languages)
- **Formatting** -- zero-config document formatting via Format Document (Shift+Alt+F)
- **Hover information** -- type signatures and Markdown documentation on mouse hover
- **Code completion** -- context-aware suggestions across 7 contexts (top-level keywords, agent body, trust tiers, confidence levels, protocol body, properties, type references)
- **Go-to-definition** -- click any type or agent name to jump to its definition
- Support for all language constructs:
  - **Type declarations** (variant types, record types, generics, optionals)
  - **Agent definitions** with trust tiers and contracts
  - **Protocol specifications** with roles, actions, and choice branches
  - **Property blocks** (termination, deadlock-freedom, ordering, exclusion)
  - **Expressions** in requires/ensures clauses
  - **Comments** and string/number literals
  - **`use` imports** for Python interop
- Auto-closing brackets and quotes
- Code folding for agents, protocols, and blocks
- Indentation support (4-space)

## Language Constructs

```lu
type TaskStatus = Pending | Running | Done

agent Worker:
    role: backend
    trust: standard
    accepts: TaskRequest
    produces: TaskResult
    requires: task.well_defined
    ensures: result.done

protocol DelegateTask:
    roles: regina, worker, guardiana
    regina asks worker to do task
    worker returns result to regina
    properties:
        always terminates
        no deadlock
```

## Highlighted Elements

| Element | Examples |
|---------|----------|
| Declarations | `type`, `agent`, `protocol` |
| Trust tiers | `verified`, `trusted`, `standard`, `untrusted` |
| Confidence | `Confident`, `Certain`, `High`, `Medium`, `Low`, `Speculative` |
| Actions | `asks`, `returns`, `tells`, `proposes`, `sends` |
| Properties | `always terminates`, `no deadlock`, `no deletion`, `before`, `cannot send`, `exclusive` |
| Clauses | `role`, `trust`, `accepts`, `produces`, `requires`, `ensures` |
| Built-in types | `String`, `Number`, `Boolean`, `List` |
| Control | `when...decides`, `use python` |

## Requirements

For diagnostics, hover, completion, and go-to-definition, install the language server:

```bash
pip install "cervellaswarm-lingua-universale[lsp]"
```

Syntax highlighting works without any additional installation.

## Installation

### From VS Code Marketplace (recommended)

1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X / Cmd+Shift+X)
3. Search for **"Lingua Universale"**
4. Click **Install**

### From VSIX

```bash
code --install-extension lingua-universale-0.2.0.vsix
```

## The Language

Lingua Universale is a domain-specific language for defining AI agent systems with:

- **Uncertainty as a type** -- `Confident[T]` instead of strings
- **Composable trust** -- `verified > trusted > standard > untrusted`
- **Self-proving protocols** -- formal verification via Lean 4

Install the language tools: `pip install cervellaswarm-lingua-universale`

## Try It Online

No install needed -- [try Lingua Universale in your browser](https://rafapra3008.github.io/cervellaswarm/)
with an interactive tutorial (24 steps, 4 chapters).

## License

Apache-2.0
