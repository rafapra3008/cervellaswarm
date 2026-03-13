# Changelog

## 0.2.0 (2026-03-13)

- **Language Server Protocol**: connects to `lu lsp` for real-time diagnostics (74 error codes)
- **Formatting**: zero-config document formatting via `lu fmt` (Format Document in VS Code)
- **Lint integration**: 10 lint rules published as diagnostics (naming, structure, completeness)
- **Hover**: type signatures and Markdown documentation on mouse hover
- **Code completion**: context-aware suggestions across 7 contexts (top-level, agent body, trust tiers, confidence levels, protocol body, properties, type references)
- **Go-to-definition**: click any type or agent name to jump to its definition
- **Grammar**: added `no deletion` and `X exclusive Y` property highlighting
- Updated description and keywords in package.json

## 0.1.0 (2026-02-28)

- Initial release
- TextMate grammar for `.lu` files with full syntax highlighting
- Language configuration: comments, brackets, folding, indentation
- Support for all Lingua Universale constructs: types, agents, protocols, properties
