# PyPI README Patterns - Code Analysis / Developer Tools Space
# Target: cervellaswarm-code-intelligence

**Status**: COMPLETA
**Data**: 2026-02-18
**Fonti**: 6 consultate (py-tree-sitter, jedi, rope, ast-grep, pylint, ruff GitHub + PyPI pages, pyopensci guide, existing RESEARCH_20260217_README_KILLER_BESTPRACTICES.md)
**Sintesi**: Best practices README specifiche per pacchetti PyPI nel segmento code analysis tools

---

## 1. Pattern Osservati (5 pacchetti analizzati)

| Pacchetto | Sezioni hero | Codice mostrato | Badges | "Supported Languages" | Limitazioni | Lunghezza |
|-----------|-------------|-----------------|--------|----------------------|-------------|-----------|
| tree-sitter | CI/PyPI/Docs badge -> Install -> Usage | 15+ esempi Python con assert | 3 (CI, PyPI, Docs) | In Installation: "install separately" | Solo "if platform not supported, submit issue" | ~350 righe |
| jedi | Badges -> descrizione -> screenshot IDE -> features/limitations | Nessun blocco codice sostanziale | 4 (maintenance, tests, PyPI downloads, issue time) | "Python 3.8+ only" | Sezione "Features and Limitations" esplicita | ~2500 parole |
| rope | Badges -> overview -> "Why use Rope?" bullets -> Getting Started links | Zero esempi codice | 5 (build, version, downloads, docs, coverage) | "Python 3.10+" in opening | In opening: "world's most advanced Python refactoring" | ~500 parole |
| ast-grep | Logo/badges -> intro -> screenshot -> install -> CLI example | 1 comando shell | 8 (CI, codecov, Discord, stars, forks, sponsors) | Non esplicito (multi-lang via tree-sitter) | Nessuna | ~1200 parole |
| pylint | Tagline -> badges -> What is pylint? -> Install -> Differentiation | Inline monospace only | 10+ (CI, coverage, PyPI, docs, Discord, scorecard) | "Python 3.10+" in primo paragrafo | "not smarter than you" - honest framing, sezione How to Use | ~1500-2000 parole |
| ruff | Badges -> tagline -> bullet features -> benchmark chart -> testimonials -> TOC -> getting started | Shell + TOML con commenti | 5 (PyPI, license, Python ver, CI, Discord) | No sezione esplicita, Python implicito | Link a FAQ esterno | ~14000 parole |

---

## 2. Struttura Raccomandata per cervellaswarm-code-intelligence

Basata su pattern tree-sitter (piu simile al nostro target) + pylint (tone) + ruff (hook):

```
1. HERO (3 badge max: CI, PyPI, Coverage)
2. TAGLINE (1 riga, benefit-driven)
3. INSTALL (1 comando)
4. QUICK DEMO (5-10 righe codice Python con output mostrato)
5. WHAT IT DOES (3-5 bullet, benefici non feature)
6. SUPPORTED LANGUAGES (sezione breve, onesta sui limiti)
7. EXAMPLES (2-3 use cases pratici con codice)
8. CLI COMMANDS (se presenti)
9. REQUIREMENTS (Python 3.10+, tree-sitter, etc.)
10. CONTRIBUTING / LICENSE (link esterni, 2 righe)
```

**Lunghezza target: 200-350 righe.** Tree-sitter e' il benchmark: abbastanza codice da convincere, non cosi' lungo da scoraggiare.

---

## 3. Come Mostrare il Codice (Pattern che Funziona)

Tree-sitter ha il pattern piu efficace nel segmento: esempi progressivi con assert che mostrano l'output atteso.

```python
# Pattern tree-sitter: mostra input -> output con assert
from cervellaswarm_code_intelligence import SymbolExtractor

extractor = SymbolExtractor()
symbols = extractor.extract("path/to/my_module.py")

assert symbols[0].name == "MyClass"
assert symbols[0].type == "class"
assert symbols[0].line == 5
```

Regole:
- Usa assert per mostrare output atteso (non print statements)
- Blocchi codice Python con syntax highlighting (```python)
- Max 10-15 righe per esempio - se e' piu lungo, link a examples/
- Mostra sempre l'import nella prima riga di ogni esempio
- NO boilerplate (setup, auth, env vars) nei quick examples

---

## 4. Badges - Pattern per Nuovo Package PyPI

**Usa esattamente 3 badge all'inizio:**

```markdown
[![CI](https://github.com/rafapra3008/cervellaswarm/actions/workflows/ci.yml/badge.svg)](...)
[![PyPI version](https://badge.fury.io/py/cervellaswarm-code-intelligence.svg)](...)
[![Coverage](https://codecov.io/gh/rafapra3008/cervellaswarm/badge.svg)](...)
```

**NON usare per un nuovo package:**
- Stars badge (mostra 0)
- Downloads badge (mostra 0 per settimane)
- Contributors badge (mostra 1)
- "Maintained" badge (non aggiunge info, occupa spazio)

Rope usa 5 badge (incluso downloads e version) - funziona perche ha storia. Per v0.1.0, 3 e' il numero corretto.

---

## 5. "Supported Languages" - Come Gestirlo

tree-sitter non ha una sezione dedicata ma menziona il pattern nella installation (install language bindings separately). Questo e' il pattern corretto per noi dato che treesitter_parser.py supporta SOLO .py/.ts/.tsx/.js/.jsx (confermato da MEMORY.md).

**Sezione raccomandata:**

```markdown
## Supported Languages

| Language  | Extension      | Status |
|-----------|----------------|--------|
| Python    | `.py`          | Full   |
| TypeScript| `.ts`, `.tsx`  | Full   |
| JavaScript| `.js`, `.jsx`  | Full   |

Other languages: the tree-sitter grammar is available, but symbol extraction
is not yet implemented. Contributions welcome.
```

**Non mentire o gonfiare.** Pylint dichiara onestamente i limiti. Rope dichiara "Python 3.10+". Tree-sitter dice "se la tua piattaforma non e' supportata, apri issue". L'onesta' costruisce fiducia con i developer.

---

## 6. Trigger Psicologici che Convertono in "pip install"

Dalle ricerche incrociate (pyopensci guide + analisi dei 5 pacchetti):

**Trigger 1: "Works out of the box" (installazione sotto 30 secondi)**
- tree-sitter: `pip install tree-sitter` + 1 import
- Il developer VUOLE un workaround da testare, non un setup guide
- Formula: install -> import -> output utile in < 5 comandi

**Trigger 2: Codice reale, non pseudocodice**
- Mostra output reale con numeri reali (linee, simboli, dipendenze)
- ast-grep mostra un comando vero con pattern reale su file reale
- Il developer vuole sentire "questo funziona sulla mia codebase adesso"

**Trigger 3: Dimostrazione di completezza tecnica (test count / coverage)**
- pylint: non lo dice nel README ma ha 10+ badge di qualita'
- Per noi: "400+ tests, 95% coverage" e' piu convincente di qualsiasi adjective
- Developer tools: la qualita' del tooling e' il prodotto

**Trigger 4: Limitazioni dichiarate onestamente**
- Paradossalmente, dichiarare limiti AUMENTA la credibilita'
- Pylint: "not smarter than you"
- Jedi: sezione "Features and Limitations" esplicita
- Formula: "Does X well. Does not do Y yet."

**Trigger 5: Associazione con tool noti**
- Tree-sitter usa il nome "tree-sitter" (noto) nel titolo -> instant credibility
- Noi: "Built on tree-sitter. Works with Python, TypeScript, JavaScript."
- L'associazione con un tool consolidato riduce il rischio percepito

**Trigger 6: Sezione "Why not just use X?"**
- Non presente in nessuno dei 5 pacchetti analizzati (omessa per umilta' o mancanza di competitor diretti)
- Per noi: considerare una breve sezione "vs grep / vs ctags" se arriviamo a F1.3

---

## 7. Delta tra GitHub README e PyPI Page

PyPI renderizza il README.md ma con alcune differenze:
- Le emoji potrebbero non renderizzarsi (usare con cautela)
- HTML raw (`<div align="center">`) NON funziona su PyPI (funziona solo su GitHub)
- Badges con shields.io funzionano su entrambi
- Usare Markdown standard, non GitHub-Flavored Markdown extensions

**Conseguenza pratica:** Il README per cervellaswarm-code-intelligence deve essere standard Markdown puro (no HTML divs, no emoji in sezioni critiche). Contrariamente al README principale di CervellaSwarm che puo usare HTML per l'hero.

---

## 8. Sintesi Pratica - 30 Linee di Regole

1. Tagline su riga 1, benefit non tecnico: "Find any symbol, anywhere in your codebase. Fast."
2. 3 badge (CI, PyPI, Coverage) - non di piu per v0.1.0
3. Install in 1 comando, visibile entro 5 righe dall'inizio
4. Primo esempio codice entro 20 righe dall'inizio
5. Pattern tree-sitter: `from package import Class` -> chiamata -> assert output
6. Max 10-15 righe per esempio di codice
7. Sezione "Supported Languages" obbligatoria, con tabella onesta
8. Non esagerare il supporto: .py/.ts/.tsx/.js/.jsx SOLO per ora
9. Dichiarare "Other languages: contributions welcome" per apertura community
10. Lunghezza target: 200-350 righe (non di piu')
11. No HTML divs: PyPI non le renderizza, usare solo Markdown standard
12. Mostrare output reale, non solo codice di input
13. Test count + coverage nel README ("400+ tests, 95% coverage")
14. Link a examples/ per casi d'uso avanzati, non tutto inline
15. CLI commands: mostrare output del comando, non solo il comando
16. Section "Requirements" prima di Contributing: Python 3.10+, tree-sitter
17. Zero emoji nelle sezioni critiche (tagline, install, codice)
18. Tono: peer-to-peer, non tutorial-mode, non corporate-mode
19. Limitazioni oneste aumentano la credibilita' (paradosso della trasparenza)
20. "Built on tree-sitter" come anchor di credibilita' (associazione con noto)
21. "400+ tests" e' social proof per developer tools (meglio di stars con 0)
22. Non mettere Getting Started in FAQ esterna: dev vuole il quickstart inline
23. Comparison con grep/ctags (FUTURO): solo quando abbiamo benchmark reali
24. Changelog link: metti CHANGELOG.md e aggiornalo ad ogni release
25. License badge + 1 riga: Apache 2.0 - niente di piu' serve
26. No "WIP", "Early alpha", "experimental" nell'hero section - spaventa
27. No Discord badge per v0.1.0 se il Discord non esiste ancora
28. Testimonianze: aggiungi solo quando hai utenti reali (non inventare)
29. TOC: utile solo oltre 400 righe - non aggiungerla per ora
30. Testare il quickstart su macchina pulita prima della pubblicazione

---

## Raccomandazione Finale

**Per F1.3 (documentazione pacchetto):**

Struttura README ottimale in ordine:
1. Badges (3: CI + PyPI + Coverage)
2. Tagline benefit-driven 1 riga
3. Install (`pip install cervellaswarm-code-intelligence`)
4. Quick demo: SymbolExtractor in 8 righe con output mostrato
5. Supported Languages table (onesta: 3 linguaggi confermati)
6. Core features (3 bullet: symbol extraction, dependency graph, semantic search)
7. CLI commands (3 comandi con output esempio)
8. Examples (link a examples/ directory)
9. Requirements (Python 3.10+, OS Independent)
10. Contributing + License (2 righe ciascuno)

**Il pattern da copiare: tree-sitter README**
- Struttura pulita Install -> Usage -> sottosezioni progressive
- Codice reale con assert che dimostra il comportamento
- Nessun marketing hype - la qualita' del codice parla da sola

---

*COSTITUZIONE-APPLIED: SI*
*Principio: "Ricerca PRIMA di implementare. Non inventare, studia come fanno i big."*
*Report: /Users/rafapra/Developer/CervellaSwarm/.sncp/progetti/cervellaswarm/reports/RESEARCH_20260218_pypi_readme_code_intelligence.md*
