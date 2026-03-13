# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-03-13 - Sessione 446 (in corso)
> **STATUS:** E.6 T3.1-T3.4 DONE. **T2.1 PyPI v0.3.1 PREP DONE.** 3436 test LU.

---

## S446 -- COSA ABBIAMO FATTO (PyPI v0.3.1 Prep + Quality Sweep)

### 1. P1 FIX CRITICO: stdlib nel wheel PyPI
- **Problema**: `stdlib/` era nella root del package, NON dentro `src/cervellaswarm_lingua_universale/`
- **Conseguenza**: `pip install` NON includeva i 20 template! `lu init --template` falliva dopo install.
- **Fix**: spostata `stdlib/` dentro `src/cervellaswarm_lingua_universale/stdlib/`
- **Path**: `_init_project.py` aggiornato da `parent.parent.parent` a `parent`
- **Verificato**: wheel build contiene 21 file stdlib (20 .lu + README)

### 2. v0.3.1 Release Prep
- **pyproject.toml**: version 0.3.0 → 0.3.1
- **__init__.py**: fallback version aggiornato
- **CHANGELOG.md**: entry completa E.5 + E.6 + 4 P1 fixes
- **.gitignore**: negation pattern aggiornato per nuovo path stdlib/data/

### 3. README Quality Sweep (12 stale refs fixate)
- Test count: 3312 → 3436 (in 5 posizioni)
- Module count: 28 → 29 (in 3 posizioni)
- Grammar rules: 62 → 64 (in 3 posizioni)
- CLI commands: 8 → 10 (+ `init`, `version`)
- Lean properties: 7 → 9
- Architecture: v0.3.0 → v0.3.1
- **NUOVA sezione "Standard Library"** nel README con tabella categorie
- **Standard Library row** aggiunta alla comparison table

### 4. Guardiana Audit
- **Score**: 9.3/10 → fix tutti P2+P3 → re-audit per 9.5+
- **F1 (P2)**: README stale counts → GIA FIXATO
- **F2 (P2)**: Test count 3435 vs 3436 (73 stdlib, non 72) → FIXATO
- **F3 (P3)**: Unused `import pytest` → RIMOSSO
- **F4 (P3)**: Copyright header mancante in 5 test files → AGGIUNTO
- **F6 (P3)**: stdlib README paths locali → AGGIUNTO `pip install` usage

### 5. Nested Choice Research
- **Report**: `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260313_NESTED_CHOICE_PARSER.md`
- Standard in MPST/Scribble (non feature speciale)
- Modifica additive (LU 1.x compatibile)
- 7 file da modificare in ordine: `_ast.py` → `_parser.py` → `_compiler.py` → `protocols.py` → `spec.py` → `_grammar_export.py`
- **Rischio**: spec.py checkers devono diventare ricorsivi (falsi PROVED altrimenti)
- Schedulare come **LU 1.1 feature**

### 6. Doc Sweep Globale
- `LU NORD.md`: test count aggiornato
- `.claude/rules/lingua-universale.md`: test count aggiornato
- `README.md` (main repo): 29 modules, 3436 tests
- `blog_vibe_to_vericoding.md`: numeri aggiornati
- Subroadmap E5_E6: T2.1 progress, metriche, priorita S446

---

## DECISIONI PRESE (con PERCHE)

| Decisione | Perche |
|-----------|--------|
| stdlib dentro src/ (non root) | Wheel PyPI include SOLO il package dir. Era un P1 critico. |
| Test usano `_STDLIB_DIR` import | DRY: stessa path resolution di produzione. Rotto in 1 posto = rotto ovunque. |
| Nested choice come LU 1.1 | Additive, non breaking, ma 7 file da cambiare. Serve sessione dedicata. |
| Dependabot PRs skip | Tutte 6 hanno CI failures. Serve investigation root cause separata. |

---

## MAPPA SITUAZIONE

```
LINGUA UNIVERSALE (LA MISSIONE):
  FASE A-D: COMPLETE (29 moduli, media 9.5/10)
  FASE E: PER TUTTI
    E.1-E.5: DONE (9.5/10)
    E.6 CervellaLang 1.0: IN PROGRESS
      T3.1 Grammar 1.0 RFC:    DONE (S444)  <- grammatica frozen
      T3.2 Standard Library:    DONE (S445)  <- 20 protocolli
      T3.3 lu init:              DONE (S444)  <- scaffolding + --template
      T3.4 lu verify:            DONE (S444)  <- verifica standalone
      T3.5 VS Code Marketplace:  TODO         <- blocco: Rafa publisher
  T2.1 PyPI v0.3.1:              PREP DONE   <- blocco: Rafa env approval
  PropertyKind: 9 | CLI: 10 | PyPI: v0.3.0 (v0.3.1 ready)
  Moduli: 29 | Test: 3436 | EBNF: 64 (frozen) | Stdlib: 20 protocolli

CI/CD: TUTTO GREEN (local)

DEPENDABOT (6 PR aperte, tutte CI fail):
  #27 qs 6.14.2, #26 @types/node 25.4.0, #24 eslint 10.0.3
  #21 api group, #18 express 4->5, #8 zod 3->4
```

---

## PROSSIMA SESSIONE -- COSA FARE

### 1. TODO Rafa (azioni manuali)
- [ ] **GitHub Environment approval** per PyPI v0.3.1 publish
- [ ] **VS Code Publisher**: creare account per T3.5
- [ ] **Blog post**: revisione "From Vibe Coding to Vericoding"
- [ ] **Dependabot Security Alerts**: abilitare su ENTRAMBI i repo

### 2. OBIETTIVI
- **T2.1 PyPI v0.3.1 PUBLISH** (Rafa approva env → publish automatico)
- **T3.5 VS Code Marketplace** (blocco: Rafa publisher account)
- **T3.6 Community Seeding** (blog update con stdlib + Show HN)
- **Nested choice LU 1.1** (ricerca DONE, implementazione ~1 sessione)
- **Dependabot investigation** (root cause CI failures)

### 3. Quick wins
- `lu lint` / `lu fmt` (backlog B5/B6)
- Tech debt: scripts/ dedup

---

## I NUMERI

| Metrica | Valore |
|---------|--------|
| Test LU | **3436** |
| Moduli LU | **29** |
| Stdlib Protocolli | **20** (5 categorie) |
| CLI Comandi | **10** |
| PropertyKind | **9** (tutti coperti!) |
| EBNF Produzioni | **64** (frozen) |
| Guardiana Audit S446 | **2** (9.3 → fix → 9.5+ pending re-audit) |

---

## Lezioni Apprese (S446)

### Cosa ha funzionato bene
- **P1 trovato PRIMA del publish**: stdlib fuori dal wheel sarebbe stato release rotto
- **Guardiana pattern**: implement → audit → fix → re-audit = diamante confermato
- **Doc sweep proattivo**: 12 stale refs in README, 3 in altri file = debito nascosto

### Cosa non ha funzionato
- **Dependabot CI**: tutte 6 PR con failure. Non investigato (separato dal focus).

### Pattern confermato
- **Wheel verification obbligatoria** prima di publish: `zipfile.ZipFile(whl).namelist()`
- **`git check-ignore -v`** per verificare .gitignore su nuovi path (lezione S445 confermata)

---
*"Ultrapassar os proprios limites!" -- S446*
