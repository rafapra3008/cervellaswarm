# Lingua Universale for VS Code

Syntax highlighting for [Lingua Universale](https://github.com/rafapra3008/cervellaswarm) (`.lu` files) -- the first programming language designed for AI agent orchestration with formal verification.

## Features

- Full syntax highlighting for `.lu` files
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
| Confidence | `Confident`, `Certain`, `High`, `Medium`, `Low` |
| Actions | `asks`, `returns`, `tells`, `proposes`, `sends` |
| Properties | `always terminates`, `no deadlock`, `before`, `cannot send` |
| Clauses | `role`, `trust`, `accepts`, `produces`, `requires`, `ensures` |
| Built-in types | `String`, `Number`, `Boolean`, `List` |
| Control | `when...decides`, `use python` |

## Installation

### From VS Code Marketplace

Search for "Lingua Universale" in the VS Code Extensions panel.

### From VSIX

```bash
code --install-extension lingua-universale-0.1.0.vsix
```

## The Language

Lingua Universale is a domain-specific language for defining AI agent systems with:

- **Uncertainty as a type** -- `Confident[T]` instead of strings
- **Composable trust** -- `verified > trusted > standard > untrusted`
- **Self-proving protocols** -- formal verification via Lean 4

Install the language tools: `pip install cervellaswarm-lingua-universale`

## License

Apache-2.0
