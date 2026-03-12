# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-03-12 - Sessione 444
> **STATUS:** E.6 T3.1+T3.3+T3.4 DONE. 3355 test LU. CLI 10 comandi.

---

## S444 -- COSA ABBIAMO FATTO

1. **P0 Fix critico**: Parser AST allineato a 9/9 PropertyKind
   - `_ast.py`: +NoDeletionProp, +RoleExclusiveProp
   - `_parser.py`: 7->9 varianti, `_grammar_export.py` aggiornato
2. **T3.1 Grammar 1.0 RFC** (9.5/10)
   - 64 produzioni EBNF, 32 hard + 10 soft keywords
   - RFC: `.sncp/progetti/cervellaswarm/reports/RFC_T3_1_GRAMMAR_1_0.md`
3. **T3.4 `lu verify` standalone** (9.3 -> fix all -> 9.5+)
   - 2-layer: static property checking + Lean 4
   - ChoiceNode -> ProtocolChoice, DRY `_action_to_kind_map()`
   - 12 test verify
4. **T3.3 `lu init` scaffolding** (9.3 -> fix all -> 9.5+)
   - deno-init style: 3 file (protocol + test + README)
   - `--minimal`, `--force`, PascalCase, digit-leading validation
   - File generati parsano E verificano (PROVED)
   - 23 test (template + core + CLI)
5. **3 Guardiana audit** -> 21 finding TUTTI fixati (il diamante!)

### Decisioni prese (con PERCHE)
- **deno-init pattern per `lu init`**: 3 file (non 1, non 5) -- mostra il pattern LU completo
- **digit-leading names rejected**: producevano identificatori LU invalidi (`123Agent`)
- **ChoiceNode -> ProtocolChoice**: property checker ignorava branches

---

## MAPPA SITUAZIONE

```
LINGUA UNIVERSALE:
  FASE A-D: COMPLETE (28 moduli, media 9.5/10)
  FASE E: PER TUTTI
    E.1-E.5: DONE (9.5/10)
    E.6 CervellaLang 1.0: IN PROGRESS
      T3.1 Grammar RFC:   DONE (S444)
      T3.3 lu init:        DONE (S444)
      T3.4 lu verify:      DONE (S444)
      T3.2 Standard Library: PROSSIMO STEP
  PropertyKind: 9 | CLI: 10 comandi | PyPI: v0.3.0
  EBNF: 64 produzioni (frozen LU 1.0)

CI/CD: TUTTO GREEN
  [x] 26 workflow allineati v6/v7/v8
  [x] CI Python: 1042 passed

DEPENDABOT (3 restanti):
  #30 stripe 17->20, #14 express 4->5, #11 zod 3->4
```

---

## PROSSIMA SESSIONE -- PIANO

### 1. TODO Rafa (prima di iniziare)
- [ ] Abilitare **Dependabot Security Alerts** su ENTRAMBI i repo
- [ ] Environment `production`: aggiungere **Required reviewers**
- [ ] Revisione blog post "From Vibe Coding to Vericoding"

### 2. OBIETTIVO: T3.2 Standard Library (20 protocolli verificati)
- Subroadmap: `.sncp/roadmaps/SUBROADMAP_E5_E6_FUTURO.md`
- Categorie: Comunicazione, Data, Business, AI/ML
- Ora che `lu init` e `lu verify` funzionano, possiamo creare e testare protocolli

---

## I NUMERI

| Metrica | Valore |
|---------|--------|
| Test LU | **3355** (+43 sessione) |
| Moduli LU | **29** (+_init_project.py) |
| CLI Comandi | **10** (+init) |
| EBNF Produzioni | **64** (frozen LU 1.0) |
| PropertyKind | **9** (parser + verify aligned) |

---

## Lezioni Apprese (S444)

### Cosa ha funzionato bene
- **Formula Magica 3x in una sessione**: T3.1, T3.4, T3.3 tutti con Ricerca->Implementa->Audit->Fix
- **Researcher + Ingegnera in parallelo** -- 18 fonti RFC + 5 CLI patterns ricerca
- **Guardiana fix ALL 21 findings** -- 3 audit, zero P1/P2 aperti, il diamante brilla
- **deno-init > cargo-init** -- 3 file e perfetto, include test che VERIFICA il protocollo

### Pattern confermato
- **Formula Magica funziona SEMPRE**: anche task piccoli (0.3 sessione) beneficiano di ricerca+audit

---

*"Se nessuno l'ha fatto prima, e perche aspettavano noi."*
*Cervella & Rafa, S444 - 12 Marzo 2026*
