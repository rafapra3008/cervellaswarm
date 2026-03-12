# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-03-12 - Fine Sessione 444
> **STATUS:** E.6 CervellaLang 1.0 in corso. T3.1+T3.3+T3.4 DONE. 3355 test LU.

---

## S444 -- COSA ABBIAMO FATTO (3 task completati!)

### 1. T3.1 Grammar 1.0 RFC (DONE, 9.5/10)
- **P0 Fix PRIMA**: Parser AST era 7/9 PropertyKind (mancavano `NoDeletionProp`, `RoleExclusiveProp`). Trovato da Ingegnera gap analysis.
- RFC completo: 64 produzioni EBNF, 32 hard + 10 soft keywords, versioning Go-style
- Researcher: 18 fonti best practices (Rust RFC, C# soft keywords, Go versioning)
- File: `.sncp/progetti/cervellaswarm/reports/RFC_T3_1_GRAMMAR_1_0.md`

### 2. T3.4 `lu verify` Standalone (DONE, 9.5/10)
- `verify_source()` ora ha 2 layer: **static property checking** (spec.py) + **Lean 4 bridge**
- `_protocol_node_to_runtime()` converte AST ProtocolNode -> runtime Protocol, **inclusi ChoiceNode -> ProtocolChoice** (fix P2 Guardiana: branches erano ignorati!)
- `_ast_properties_to_spec()`: mappa tutti 9 PropertyKind da AST a ProtocolSpec
- `_safe_check_properties()`: fallback per-property con SKIPPED verdict per ORDERING/EXCLUSION
- `_action_to_kind_map()`: helper DRY condiviso (era duplicato in 2 funzioni)
- CLI `_cmd_verify()`: output colorato (GREEN PROVED, RED VIOLATED, YELLOW SKIPPED)

### 3. T3.3 `lu init` Scaffolding (DONE, 9.5/10)
- Modello **deno-init**: 3 file (protocol.lu + test.lu + README.md), non-interactive
- `--minimal` (solo .lu), `--force` (sovrascrive), PascalCase conversion
- Digit-leading names rejected (fix P2 Guardiana: producevano LU invalido)
- File generati parsano E verificano formalmente (PROVED)
- Nuovo modulo: `_init_project.py`

### 4. Quality
- **3 Guardiana audit**: 21 finding totali, **TUTTI fixati** (anche P3)
- **3355 test LU** (+43 in sessione: 8 parser + 12 verify + 23 init)
- **3 commit + push** su origin, tutti green

---

## DECISIONI PRESE (con PERCHE)

| Decisione | Perche |
|-----------|--------|
| Soft keywords per `chat`/`voice`/`template` | Pattern C#/Python: non rompere file .lu esistenti dopo 1.0 |
| ChoiceNode -> ProtocolChoice in verify | Property checker vedeva solo step top-level, branches ignorati = falsi verdetti |
| deno-init (3 file) per `lu init` | 1 file troppo nudo, 5 troppi. 3 mostra il pattern completo + test incluso |
| Digit-leading names rejected | `123Agent` non e un identificatore LU valido |
| DRY `_action_to_kind_map()` | Era duplicato identico in `_protocol_node_to_runtime` e `_protocol_node_to_lean4` |

---

## MAPPA SITUAZIONE

```
LINGUA UNIVERSALE (LA MISSIONE):
  FASE A-D: COMPLETE (28 moduli, media 9.5/10)
  FASE E: PER TUTTI
    E.1-E.5: DONE (9.5/10)
    E.6 CervellaLang 1.0: IN PROGRESS
      T3.1 Grammar 1.0 RFC:    DONE (S444)  <- grammatica frozen
      T3.3 lu init:              DONE (S444)  <- scaffolding pronto
      T3.4 lu verify:            DONE (S444)  <- verifica standalone
      T3.2 Standard Library:     PROSSIMO     <- 20 protocolli verificati
      T3.5 VS Code Marketplace:  TODO
  PropertyKind: 9 | CLI: 10 comandi | PyPI: v0.3.0
  Moduli: 29 | Test: 3355 | EBNF: 64 produzioni (frozen LU 1.0)

CI/CD: TUTTO GREEN
  26 workflow | CI Python: 1042 passed

DEPENDABOT (3 restanti, non urgenti):
  #30 stripe 17->20, #14 express 4->5, #11 zod 3->4
```

---

## PROSSIMA SESSIONE -- COSA FARE

### 1. TODO Rafa (azioni manuali)
- [ ] **Dependabot Security Alerts**: abilitare su ENTRAMBI i repo (privato + pubblico)
- [ ] **Environment production**: aggiungere **Required reviewers** (rafapra3008)
- [ ] **Blog post**: revisione "From Vibe Coding to Vericoding"

### 2. OBIETTIVO: T3.2 Standard Library (20 protocolli verificati)
- **Subroadmap**: `.sncp/roadmaps/SUBROADMAP_E5_E6_FUTURO.md` (sezione T3.2)
- **Categorie**: Comunicazione (4), Data (3), Business (3), AI/ML (3)
- **Come**: usare `lu init` per creare ogni protocollo, `lu verify` per verificare
- **Ricerca PRIMA**: studiare design patterns per protocolli (Scribble, MPST)

### 3. Quick wins se serve pausa
- #30 stripe 17->20 (1 code change + test)
- Tech debt: scripts/ dedup

---

## I NUMERI

| Metrica | Valore |
|---------|--------|
| Test LU | **3355** |
| Moduli LU | **29** |
| CLI Comandi | **10** (check, run, verify, compile, init, repl, lsp, chat, demo, version) |
| PropertyKind | **9** |
| EBNF Produzioni | **64** (frozen) |
| Guardiana Audit S444 | **3** (21 findings, tutti fixati) |

---

## FILE CHIAVE MODIFICATI (S444)

| File | Cosa |
|------|------|
| `_eval.py` | verify_source() 2-layer, ChoiceNode, DRY helper |
| `_cli.py` | +lu init, colored verify output |
| `_init_project.py` | **NUOVO** - scaffolding module |
| `_ast.py` | +NoDeletionProp, +RoleExclusiveProp |
| `_parser.py` | 7->9 property variants |
| `_grammar_export.py` | GBNF + Lark con 9 property |
| `test_eval.py` | +12 test verify properties |
| `test_init_project.py` | **NUOVO** - 23 test scaffolding |
| `test_parser_constructs.py` | +8 test E5 properties |

---

## Lezioni Apprese (S444)

### Cosa ha funzionato bene
- **Formula Magica 3x**: Ricerca->Implementa->Audit->Fix per T3.1, T3.4, T3.3
- **Ingegnera gap analysis PRIMA**: ha trovato P0 (parser 7/9) che nessuno sapeva
- **Researcher in parallelo**: 18 fonti RFC + 5 CLI patterns contemporaneamente
- **Guardiana fix ALL**: 3 audit, 21 findings, TUTTI fixati = diamante

### Pattern confermato
- **Formula Magica funziona SEMPRE**, anche per task piccoli (0.3 sessione)
- **"Ci piace fissare tutto"**: anche P3 -- il diamante brilla nei dettagli

---

*"Se nessuno l'ha fatto prima, e perche aspettavano noi."*
*Cervella & Rafa, S444 - 12 Marzo 2026*
