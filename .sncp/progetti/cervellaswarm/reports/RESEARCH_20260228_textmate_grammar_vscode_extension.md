# TextMate Grammar + VS Code Extension - Ricerca Lingua Universale

> **Data:** 2026-02-28
> **Researcher:** Cervella Researcher
> **Status:** COMPLETA
> **Fonti consultate:** 15 (VS Code API docs, TextMate manual, Sublime scope naming guide,
>   Gleam vscode-gleam source, pygls docs, vsce publishing guide, martinring/tmlanguage schema)

---

## 1. TextMate Grammar - Struttura JSON

### Schema di riferimento

```json
{
  "$schema": "https://raw.githubusercontent.com/martinring/tmlanguage/master/tmlanguage.json",
  "name": "Lingua Universale",
  "scopeName": "source.lu",
  "fileTypes": ["lu"],
  "patterns": [
    { "include": "#comment" },
    { "include": "#string" },
    { "include": "#keyword-declaration" },
    { "include": "#keyword-control" },
    { "include": "#keyword-other" },
    { "include": "#trust-tier" },
    { "include": "#confidence-level" },
    { "include": "#type-name" },
    { "include": "#number" },
    { "include": "#operator" },
    { "include": "#punctuation" }
  ],
  "repository": {
    "comment": { ... },
    "string": { ... },
    ...
  }
}
```

**Regole fondamentali della struttura:**
- `scopeName`: SEMPRE `source.{ext}` per linguaggi di programmazione, `text.{ext}` per markup
- `patterns`: lista ordinata di regole top-level (ordine conta - prima match vince)
- `repository`: dizionario di regole riusabili, referenziate via `{ "include": "#nome" }`
- `fileTypes`: estensioni senza il punto

### I tre tipi di pattern

**1. Match - singola riga:**
```json
{
  "match": "\\b(keyword)\\b",
  "name": "keyword.control.lu"
}
```

**2. Begin/End - multi-riga (es. blocchi indentati, stringhe):**
```json
{
  "begin": "\"",
  "end": "\"",
  "name": "string.quoted.double.lu",
  "patterns": [
    { "include": "#string-escape" }
  ]
}
```

**3. Captures - gruppi di cattura:**
```json
{
  "match": "(agent)\\s+([A-Z][A-Za-z0-9]*)",
  "captures": {
    "1": { "name": "storage.type.lu" },
    "2": { "name": "entity.name.type.lu" }
  }
}
```

**NOTA IMPORTANTE:** Oniguruma regex engine (NON PCRE, NON Python re).
Differenze chiave: lookbehind fixed-width, `\\b` funziona come atteso.

---

## 2. Scope Names Canonici - Guida Pratica

### Mapping per Lingua Universale

| Elemento LU | Scope Raccomandato | Motivazione |
|-------------|-------------------|-------------|
| `type`, `record`, `variant` | `storage.type.lu` | Type declaration keywords (standard per class/struct/type) |
| `agent`, `protocol` | `storage.type.lu` | Definition keywords per strutture complesse |
| `when`, `choice` | `keyword.control.lu` | Control flow / branching |
| `use` | `keyword.control.import.lu` | Import-like semantics |
| `requires`, `ensures` | `keyword.other.contract.lu` | Pre/post-conditions (non control flow) |
| `confidence`, `property`, `properties` | `keyword.other.lu` | Structural keywords |
| `asks`, `returns`, `sends`, `confirms`, `tells` | `keyword.operator.word.lu` | Communication operators (word form) |
| `role`, `trust`, `accepts`, `produces` | `variable.other.member.lu` | Agent field names |
| `trusted`, `standard`, `untrusted`, `verified` | `constant.language.lu` | Language-defined constants |
| `Confident`, `Certain`, `High`, `Medium`, `Low` | `constant.language.lu` | Confidence level constants |
| `true`, `false` | `constant.language.lu` | Boolean literals |
| Nomi PascalCase (AgentName, TypeName) | `entity.name.type.lu` | User-defined type/agent names |
| Stringhe `"..."` | `string.quoted.double.lu` | Standard double-quoted strings |
| Commenti `# ...` | `comment.line.number-sign.lu` | Number-sign comment (Python style) |
| Numeri `42`, `3.14` | `constant.numeric.lu` | Numeric literals |
| Operatori `>=`, `<=`, `==`, `!=`, `>`, `<` | `keyword.operator.comparison.lu` | Comparison operators |
| `=` (assignment) | `keyword.operator.assignment.lu` | Assignment |
| `|` (union) | `keyword.operator.lu` | Type union operator |
| `:` | `punctuation.separator.lu` | Field separator |
| `[`, `]` | `punctuation.section.brackets.lu` | Generic/List brackets |
| `(`, `)` | `punctuation.section.parens.lu` | Parentheses |

### Gerarchia scope - come funziona il theming

I temi applicano stili dal meno specifico al piu specifico:
```
keyword          -> colore base per tutti i keyword
keyword.control  -> override per keyword di controllo
keyword.control.lu -> override specifico per LU (raramente usato dai temi)
```

**Regola d'oro:** Usa almeno `keyword.control`, `storage.type`, `entity.name.type`,
`string.quoted.double`, `comment.line` - questi sono supportati da TUTTI i temi.

### Scopes PIU supportati dai temi (priorita alta)

In ordine di supporto universale dai temi VS Code:
1. `comment.line.*` / `comment.block`
2. `string.quoted.*`
3. `keyword.control`
4. `storage.type`
5. `entity.name.type` / `entity.name.function`
6. `constant.numeric` / `constant.language`
7. `keyword.operator`
8. `variable.parameter`

---

## 3. tmLanguage.json Completo per Lingua Universale

```json
{
  "$schema": "https://raw.githubusercontent.com/martinring/tmlanguage/master/tmlanguage.json",
  "name": "Lingua Universale",
  "scopeName": "source.lu",
  "fileTypes": ["lu"],
  "patterns": [
    { "include": "#comment" },
    { "include": "#string" },
    { "include": "#agent-declaration" },
    { "include": "#protocol-declaration" },
    { "include": "#type-declaration" },
    { "include": "#keyword-control" },
    { "include": "#keyword-import" },
    { "include": "#keyword-contract" },
    { "include": "#trust-tier" },
    { "include": "#confidence-level" },
    { "include": "#communication-verb" },
    { "include": "#property-name" },
    { "include": "#type-name" },
    { "include": "#number" },
    { "include": "#operator" }
  ],
  "repository": {
    "comment": {
      "name": "comment.line.number-sign.lu",
      "match": "#.*$"
    },

    "string": {
      "name": "string.quoted.double.lu",
      "begin": "\"",
      "end": "\"",
      "patterns": [
        {
          "name": "constant.character.escape.lu",
          "match": "\\\\."
        }
      ]
    },

    "agent-declaration": {
      "comment": "agent AgentName: or agent AgentName (with captures)",
      "match": "\\b(agent)\\s+([A-Z][A-Za-z0-9]*)",
      "captures": {
        "1": { "name": "storage.type.lu" },
        "2": { "name": "entity.name.type.lu" }
      }
    },

    "protocol-declaration": {
      "match": "\\b(protocol)\\s+([A-Z][A-Za-z0-9]*)",
      "captures": {
        "1": { "name": "storage.type.lu" },
        "2": { "name": "entity.name.type.lu" }
      }
    },

    "type-declaration": {
      "match": "\\b(type|record|variant)\\s+([A-Z][A-Za-z0-9]*)",
      "captures": {
        "1": { "name": "storage.type.lu" },
        "2": { "name": "entity.name.type.lu" }
      }
    },

    "keyword-control": {
      "name": "keyword.control.lu",
      "match": "\\b(when|choice|roles)\\b"
    },

    "keyword-import": {
      "name": "keyword.control.import.lu",
      "match": "\\b(use)\\b"
    },

    "keyword-contract": {
      "name": "keyword.other.contract.lu",
      "match": "\\b(requires|ensures|confidence|property|properties|capability|asks|returns|sends|confirms|tells)\\b"
    },

    "trust-tier": {
      "name": "constant.language.lu",
      "match": "\\b(trusted|standard|untrusted|verified)\\b"
    },

    "confidence-level": {
      "name": "constant.language.lu",
      "match": "\\b(Confident|Certain|High|Medium|Low)\\b"
    },

    "communication-verb": {
      "name": "keyword.operator.word.lu",
      "match": "\\b(asks|returns|sends|confirms|tells|to|do|verify|revise)\\b"
    },

    "property-name": {
      "name": "variable.other.member.lu",
      "match": "\\b(role|trust|accepts|produces|reject|approve)\\b"
    },

    "boolean-constant": {
      "name": "constant.language.lu",
      "match": "\\b(true|false|True|False)\\b"
    },

    "type-name": {
      "comment": "PascalCase identifiers = type names or agent refs",
      "name": "entity.name.type.lu",
      "match": "\\b[A-Z][A-Za-z0-9]*\\b"
    },

    "number": {
      "name": "constant.numeric.lu",
      "match": "\\b\\d+(?:\\.\\d+)?\\b"
    },

    "operator": {
      "patterns": [
        {
          "name": "keyword.operator.comparison.lu",
          "match": ">=|<=|==|!=|>|<"
        },
        {
          "name": "keyword.operator.assignment.lu",
          "match": "="
        },
        {
          "name": "keyword.operator.lu",
          "match": "\\|"
        }
      ]
    }
  }
}
```

**NOTE IMPLEMENTATIVE:**

1. Ordine dei pattern CONTA: `agent-declaration`, `protocol-declaration`, `type-declaration`
   devono venire PRIMA di `keyword-control` (che non ha `agent`/`protocol` ma per sicurezza).

2. `type-name` (PascalCase generico) va DOPO le dichiarazioni specifiche perche e un catch-all.

3. `communication-verb` include anche `to`, `do` - parole brevi comuni. Valutare se troppo
   aggressivo e rimuoverle se danno falsi positivi.

4. Il pattern `agent-declaration` usa captures per colorare `agent` e `AgentName` diversamente:
   - `agent` -> `storage.type.lu` (viola/orange nei temi)
   - `AgentName` -> `entity.name.type.lu` (giallo/verde nei temi)

---

## 4. VS Code Extension - Struttura File

### Directory minimale (solo syntax highlighting, NO LSP)

```
lingua-universale-vscode/
  package.json                          # Manifest estensione
  language-configuration.json           # Brackets, comments, folding
  syntaxes/
    lingua-universale.tmLanguage.json   # Il grammar
  .vscodeignore                         # File da escludere dal .vsix
  README.md                             # Pagina Marketplace
  CHANGELOG.md                          # Storia versioni
  LICENSE                               # Apache-2.0
  icon.png                              # 128x128px PNG (richiesto per pubblicazione)
```

### package.json Completo

```json
{
  "name": "lingua-universale",
  "displayName": "Lingua Universale",
  "description": "Syntax highlighting for Lingua Universale (.lu) - the first AI-native programming language",
  "version": "0.1.0",
  "publisher": "cervellaswarm",
  "engines": {
    "vscode": "^1.52.0"
  },
  "categories": [
    "Programming Languages"
  ],
  "keywords": [
    "lingua universale",
    "lu",
    "ai",
    "agent",
    "protocol",
    "cervellaswarm"
  ],
  "icon": "icon.png",
  "repository": {
    "type": "git",
    "url": "https://github.com/rafapra3008/cervellaswarm"
  },
  "license": "Apache-2.0",
  "galleryBanner": {
    "color": "#1a1a2e",
    "theme": "dark"
  },
  "contributes": {
    "languages": [
      {
        "id": "lingua-universale",
        "aliases": ["Lingua Universale", "lu"],
        "extensions": [".lu"],
        "configuration": "./language-configuration.json",
        "icon": {
          "light": "./icons/lu-light.png",
          "dark": "./icons/lu-dark.png"
        }
      }
    ],
    "grammars": [
      {
        "language": "lingua-universale",
        "scopeName": "source.lu",
        "path": "./syntaxes/lingua-universale.tmLanguage.json"
      }
    ]
  }
}
```

**Nota `engines.vscode`:** `"^1.52.0"` e il minimo compatibile per temi moderni.
Gleam usa `"^1.52.0"` - stesso riferimento.

**Nota `icon`:** Richiesto per pubblicazione. 128x128px PNG. SVG NON permesso.

**Nota `galleryBanner`:** Colore sfondo della pagina Marketplace. Scegli un colore
coordinato con l'icona.

---

## 5. language-configuration.json per LU

```json
{
  "comments": {
    "lineComment": "#"
  },
  "brackets": [
    ["[", "]"],
    ["(", ")"]
  ],
  "autoClosingPairs": [
    { "open": "[", "close": "]" },
    { "open": "(", "close": ")" },
    { "open": "\"", "close": "\"", "notIn": ["string", "comment"] }
  ],
  "surroundingPairs": [
    ["[", "]"],
    ["(", ")"],
    ["\"", "\""]
  ],
  "folding": {
    "markers": {
      "start": "^\\s*(agent|protocol|type|record|variant)\\s+[A-Z]",
      "end": "^(?!\\s)"
    }
  },
  "indentationRules": {
    "increaseIndentPattern": "^\\s*(agent|protocol|type|record|variant|when|choice|properties|roles)[^\\n]*:\\s*$",
    "decreaseIndentPattern": "^\\s*$"
  },
  "wordPattern": "(-?\\d*\\.\\d\\w*)|([^\\`\\~\\!\\@\\#\\%\\^\\&\\*\\(\\)\\-\\=\\+\\[\\{\\]\\}\\|\\;\\:\\'\\\"\\,\\.\\<\\>\\/\\?\\s]+)"
}
```

**Note:**
- `lineComment`: `#` (Python-style, coerente con il tokenizer che usa `#`)
- NO `blockComment`: LU non ha commenti multi-riga
- `brackets`: solo `[]` e `()` (LU non usa `{}`)
- `folding.markers`: regex che matcha le linee di apertura di blocchi (`agent Foo:`)
  e le linee non-indentate come fine blocco (approssimazione per folding)
- `indentationRules.increaseIndentPattern`: linee che terminano con `:` dopo keyword

---

## 6. Gleam Extension - Pattern di Riferimento

Dalla analisi di `vscode-gleam` (v2.12.1, 217 stelle, Apache-2.0):

**Scelte chiave di Gleam che possiamo replicare:**

1. `scopeName`: `source.gleam` - stesso pattern `source.{lang}`
2. `engines.vscode`: `"^1.52.0"` - target ragionevole
3. `language-configuration.json`: minimalista (solo comments, brackets, autoClosingPairs, surroundingPairs)
4. Due grammar: main + injection per markdown code blocks
5. Snippets separati in `snippets.json` (non inclusi nel grammar)
6. `categories`: `["Programming Languages"]` per la pagina Marketplace

**Pattern Gleam grammar (rilevante per noi):**
- Keywords con `\\b..\\b` word boundaries
- PascalCase identifiers come `constant.other` (Gleam) - noi usiamo `entity.name.type`
  perche i nostri PascalCase sono nomi di tipo/agente, non solo costanti
- Commenti `//` con scope `comment.line.double-slash.gleam`
- Noi usiamo `comment.line.number-sign.lu` per `#`

**Differenze LU vs Gleam:**
- LU usa `#` per commenti (non `//`)
- LU e indentation-based (non usa `{}`)
- LU ha concetti specifici: trust tiers, confidence levels, agent communication

---

## 7. Pubblicazione VS Code Marketplace

### Steps completi

```bash
# 1. Installa vsce
npm install -g @vscode/vsce

# 2. Login con PAT (una volta sola per macchina)
vsce login cervellaswarm

# 3. Package locale per test
vsce package
# genera: lingua-universale-0.1.0.vsix

# 4. Installa localmente per test
code --install-extension lingua-universale-0.1.0.vsix

# 5. Pubblica (richiede PAT attivo)
vsce publish

# 6. Bumpa versione e pubblica
vsce publish patch   # 0.1.0 -> 0.1.1
vsce publish minor   # 0.1.0 -> 0.2.0
vsce publish major   # 0.1.0 -> 1.0.0
```

### Setup Publisher (una tantum)

1. Crea account su https://marketplace.visualstudio.com/manage
2. Click "Create publisher" -> ID: `cervellaswarm` (immutabile dopo creazione)
3. Vai su https://dev.azure.com/ -> User Settings -> Personal Access Tokens
4. Crea token: Scopes = **Marketplace -> Manage**, Organization = **All accessible**
5. `vsce login cervellaswarm` -> incolla il token

### Campi package.json richiesti per pubblicazione

| Campo | Obbligatorio | Note |
|-------|-------------|------|
| `name` | SI | kebab-case, unico globalmente |
| `version` | SI | semver `major.minor.patch` |
| `publisher` | SI | ID publisher creato sul Marketplace |
| `engines.vscode` | SI | versione minima VS Code |
| `description` | SI (praticamente) | Mostrata nel Marketplace |
| `icon` | RACCOMANDATO | 128x128px PNG, NON SVG |
| `repository` | RACCOMANDATO | GitHub link nella pagina Marketplace |
| `categories` | RACCOMANDATO | Classifica nell'estore |
| `license` | RACCOMANDATO | SPDX identifier |

### .vscodeignore

```
.gitignore
.prettierrc
tsconfig.json
**/*.map
**/*.ts
!out/**
node_modules/**
```

Per un'estensione solo-grammar (no TypeScript), molto piu semplice:
```
.gitignore
**/*.md
!README.md
!CHANGELOG.md
```

### Open VSX Registry (alternativa open-source)

Per VSCodium, Gitpod, Zed, Eclipse Theia - stessa estensione, altro registry.

```bash
npm install -g ovsx
ovsx publish lingua-universale-0.1.0.vsix -p <token>
```

Token da: https://open-vsx.org/ (registrazione con GitHub)

**Raccomandazione:** Pubblica su ENTRAMBI. Stessa .vsix, zero lavoro extra.

---

## 8. Markdown Code Block Injection (bonus)

Permette syntax highlighting di code blocks `lu` nei file .md:

```json
{
  "grammars": [
    {
      "language": "lingua-universale",
      "scopeName": "source.lu",
      "path": "./syntaxes/lingua-universale.tmLanguage.json"
    },
    {
      "scopeName": "markdown.lu.codeblock",
      "path": "./syntaxes/lingua-universale-markdown.tmLanguage.json",
      "injectTo": ["text.html.markdown"],
      "embeddedLanguages": {
        "meta.embedded.block.lu": "lingua-universale"
      }
    }
  ]
}
```

File `lingua-universale-markdown.tmLanguage.json`:
```json
{
  "scopeName": "markdown.lu.codeblock",
  "injectionSelector": "L:text.html.markdown",
  "patterns": [
    {
      "begin": "(^|\\G)(\\s*)(```|~~~)(\\s*)(lu|lingua-universale)\\s*$",
      "end": "(^|\\G)(\\2)(```|~~~)\\s*$",
      "beginCaptures": {
        "3": { "name": "punctuation.definition.fenced.markdown" },
        "5": { "name": "entity.name.language.lu" }
      },
      "patterns": [{ "include": "source.lu" }]
    }
  ]
}
```

**Valore:** I code block `lu` nel Tour tutorial e README avranno syntax highlighting
anche su VS Code preview. Gleam fa esattamente questo.

---

## 9. Testing del Grammar Localmente

### Metodo 1: F5 Extension Development Host

```bash
# Nella cartella dell'estensione
npm install     # se c'e package.json con devDeps
# Poi F5 in VS Code apre una nuova finestra con l'estensione carica
```

### Metodo 2: Installa .vsix direttamente

```bash
vsce package
code --install-extension lingua-universale-0.1.0.vsix
```

### Metodo 3: Developer Tools - Scope Inspector

In VS Code: `Ctrl+Shift+P` -> "Developer: Inspect Editor Tokens and Scopes"
Posiziona cursore su un token -> vedi esattamente quali scopi sono applicati.
FONDAMENTALE per debug del grammar.

---

## 10. Struttura Directory Consigliata

```
extensions/
  lingua-universale-vscode/
    package.json
    language-configuration.json
    .vscodeignore
    README.md
    CHANGELOG.md
    LICENSE
    icon.png
    syntaxes/
      lingua-universale.tmLanguage.json
      lingua-universale-markdown.tmLanguage.json  # opzionale, per .md injection
```

Questa directory va nella ROOT di CervellaSwarm, a fianco di `packages/`.
NON dentro `packages/lingua-universale/` perche e un progetto VS Code separato.

---

## 11. Raccomandazione Finale

**Ordine di implementazione per D1:**

1. Crea `extensions/lingua-universale-vscode/` con i file minimi
2. `language-configuration.json`: commenti `#`, brackets `[]` `()`, autoclose
3. `syntaxes/lingua-universale.tmLanguage.json`: il grammar completo dalla sezione 3
4. `package.json`: contributes.languages + contributes.grammars
5. Test locale: `vsce package` + installa .vsix + Scope Inspector
6. `icon.png`: 128x128 (anche semplice logo testuale, purche PNG)
7. Setup publisher su Marketplace (una tantum)
8. `vsce publish` + `ovsx publish`

**Effort stimato:** 1 sessione. Il grammar dalla sezione 3 e quasi pronto da usare.
Richiede solo fine-tuning dopo il test con Scope Inspector.

---

## Fonti

- [VS Code Syntax Highlight Guide](https://code.visualstudio.com/api/language-extensions/syntax-highlight-guide)
- [VS Code Language Configuration Guide](https://code.visualstudio.com/api/language-extensions/language-configuration-guide)
- [VS Code Publishing Extensions](https://code.visualstudio.com/api/working-with-extensions/publishing-extension)
- [TextMate Language Grammars Manual](https://macromates.com/manual/en/language_grammars)
- [Sublime Text Scope Naming (authoritative)](https://www.sublimetext.com/docs/scope_naming.html)
- [martinring/tmlanguage JSON Schema](https://github.com/martinring/tmlanguage)
- [gleam-lang/vscode-gleam](https://github.com/gleam-lang/vscode-gleam)
- [Gleam tmLanguage.json source](https://github.com/gleam-lang/vscode-gleam/blob/6ed1e8a5acb5c4dbe2d44fe7d01d835ddc09cc9e/syntaxes/gleam.tmLanguage.json)
- [Writing a TextMate Grammar: Lessons Learned](https://www.apeth.com/nonblog/stories/textmatebundle.html)
- [VS Code Extension Anatomy](https://code.visualstudio.com/api/get-started/extension-anatomy)
- [Open VSX Registry](https://open-vsx.org/)
- [DEV.to: Publishing to both Marketplaces](https://dev.to/diana_tang/complete-guide-publishing-vs-code-extensions-to-both-marketplaces-4d58)
- [VS Code Grammar Tips (GitHub Gist)](https://gist.github.com/dannymcgee/96b09dc2a061e7b23dc7930ff0f218f4)
