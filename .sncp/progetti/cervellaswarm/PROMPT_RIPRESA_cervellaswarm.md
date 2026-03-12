# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-03-12 - Sessione 444
> **STATUS:** E.6 T3.1 + T3.4 DONE. 3332 test LU. Parser 9/9 PropertyKind.

---

## S444 -- COSA ABBIAMO FATTO

1. **P0 Fix critico**: Parser AST allineato a 9/9 PropertyKind
   - `_ast.py`: +NoDeletionProp, +RoleExclusiveProp (frozen dataclass)
   - `_parser.py`: `_parse_property()` da 7 a 9 varianti + errore migliorato per `no <invalid>`
   - `_grammar_export.py`: GBNF + Lark aggiornati con 9 property
2. **T3.1 Grammar 1.0 RFC** scritto e auditato (9.5/10)
   - 64 produzioni EBNF, 9 sezioni, keyword classification (32 hard + 10 soft riservati)
   - RFC: `.sncp/progetti/cervellaswarm/reports/RFC_T3_1_GRAMMAR_1_0.md`
3. **T3.4 `lu verify` standalone** implementato e auditato (9.3 -> fix all -> 9.5+)
   - `verify_source()`: 2-layer (static property checking + Lean 4 bridge)
   - `_protocol_node_to_runtime()`: ChoiceNode -> ProtocolChoice (branches inclusi!)
   - `_ast_properties_to_spec()`: 9/9 PropertyKind mapping
   - `_safe_check_properties()`: graceful per-property fallback con SKIPPED verdict
   - `_action_to_kind_map()`: DRY helper condiviso (era duplicato in 2 funzioni)
   - CLI: colored output (GREEN PROVED, RED VIOLATED, YELLOW SKIPPED)
   - 12 test verify (11 property + 1 ChoiceNode)
4. **20 test nuovi totale** (8 parser + 12 verify)
5. **2 Guardiana audit** -> tutti finding fixati (7/7 T3.1 + 7/7 T3.4)

### Decisioni prese (con PERCHE)
- **ChoiceNode -> ProtocolChoice**: property checker vedeva solo step top-level, branches ignorati
- **Shared `_action_to_kind_map()`**: era duplicato in `_protocol_node_to_runtime` e `_protocol_node_to_lean4`
- **CLI verdict ordering**: summary (bold) PRIMA di per-property check (era unreachable)
- **Soft keywords per `chat`/`voice`/`template`**: pattern C#/Python, non rompere .lu esistenti

---

## MAPPA SITUAZIONE

```
LINGUA UNIVERSALE:
  FASE A-D: COMPLETE (28 moduli, media 9.5/10)
  FASE E: PER TUTTI
    E.1-E.5: DONE (9.5/10)
    E.6 CervellaLang 1.0: IN PROGRESS
      T3.1 Grammar RFC: DONE (S444)
      T3.4 lu verify:    DONE (S444)
      T3.2 Standard Library: PROSSIMO STEP
      T3.3 lu init: TODO
  PropertyKind: 9 | CLI: 9 comandi | PyPI: v0.3.0
  EBNF: 64 produzioni (frozen LU 1.0)

CI/CD: TUTTO GREEN
  [x] 26 workflow allineati v6/v7/v8
  [x] CI Python: 1042 passed (scipy/numpy inclusi)

DEPENDABOT (3 restanti):
  #30 stripe 17->20, #14 express 4->5, #11 zod 3->4
```

---

## PROSSIMA SESSIONE -- PIANO

### 1. TODO Rafa (prima di iniziare)
- [ ] Abilitare **Dependabot Security Alerts** su ENTRAMBI i repo
- [ ] Environment `production`: aggiungere **Required reviewers** (rafapra3008)
- [ ] Revisione blog post "From Vibe Coding to Vericoding"

### 2. OBIETTIVO: T3.2 Standard Library (20 protocolli verificati)
- Subroadmap: `.sncp/roadmaps/SUBROADMAP_E5_E6_FUTURO.md`
- Categorie: Comunicazione, Data, Business, AI/ML
- Parallelizzabile con T3.3 (`lu init`)

### 3. Quando serve pausa
- #30 stripe 17->20 (1 code change + test)
- Tech debt: scripts/ dedup, errors.py extraction

---

## I NUMERI

| Metrica | Valore |
|---------|--------|
| Test LU | **3332** (+20 sessione) |
| Test CI Python | **1042** (0 failed) |
| Hooks | **16** (cervella_hooks_common.py v1.2.0) |
| Moduli LU | **28** |
| EBNF Produzioni | **64** (frozen LU 1.0) |
| PropertyKind | **9** (parser + verify aligned) |

---

## Lezioni Apprese (S444)

### Cosa ha funzionato bene
- **Ingegnera gap analysis PRIMA** -- ha trovato P0 (parser 7/9) che nessuno sapeva
- **Researcher in parallelo** -- 18 fonti per RFC while Ingegnera analizzava codice
- **Guardiana fix ALL findings** -- 2 audit, 14 findings, TUTTI fixati (il diamante!)
- **ChoiceNode fix dalla Guardiana T3.4** -- F1 (P2) trovava false verdicts per branched protocols

### Pattern confermato
- **Formula Magica**: Ricerca -> Implementa -> Guardiana audit -> Fix ALL -> Diamante
- **Soft keywords C#/Python**: MAI aggiungere hard keywords dopo 1.0

---

*"Se nessuno l'ha fatto prima, e perche aspettavano noi."*
*Cervella & Rafa, S444 - 12 Marzo 2026*
