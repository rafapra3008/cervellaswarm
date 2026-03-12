# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-03-12 - Fine Sessione 445
> **STATUS:** E.6 CervellaLang 1.0 in corso. T3.1-T3.4 DONE. **T3.2 DONE.** 3435 test LU.

---

## S445 -- COSA ABBIAMO FATTO (T3.2 Standard Library!)

### 1. T3.2 Standard Library -- 20 Protocolli Verificati (DONE)
- **Ricerca PRIMA**: Researcher ha studiato Scribble, MPST (Honda/Yoshida POPL 2008), gRPC, session type libraries (Rust, Haskell, OCaml), AI agent protocols
- **Report**: `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260312_T3_2_STANDARD_LIBRARY_PROTOCOLS.md`
- **5 categorie**, 20 protocolli, tutti PARSE + VERIFY = PROVED:
  - **Communication (5)**: request_response, ping_pong, pub_sub, scatter_gather, pipeline
  - **Data (3)**: crud_safe, data_sync, cache_invalidation
  - **Business (4)**: two_buyer (MPST canonico!), approval_workflow, auction, saga_order
  - **AI/ML (5)**: rag_pipeline, agent_delegation, tool_calling, human_in_loop, consensus
  - **Security (3)**: auth_handshake, mutual_tls, rate_limited_api
- **Tutte 9 PropertyKind coperte** (F1 Guardiana fixato: +confidence_min, +exclusion)
- **F2 Guardiana fixato**: tutti agenti ora usano tipi di dominio (non TaskRequest/TaskResult generici)
- **Nested choice non supportato**: saga_order ridisegnato con struttura flat (limitazione parser LU 1.0)

### 2. CLI Integration: `lu init --template`
- `lu init my-proj --template rag_pipeline` copia protocollo stdlib
- `lu init --list-templates` mostra i 20 template disponibili
- `_init_project.py` esteso con `list_templates()`, `_find_template()`, parametro `template`
- `_cli.py` aggiornato con `--template` e `--list-templates` args

### 3. Quality
- **Guardiana audit**: score 9.3 -> fix F1 (2 PropertyKind mancanti) + F2 (tipi generici) -> 9.5+
- **3435 test LU** (+80: 72 stdlib + 8 template CLI)
- **README stdlib** con tabelle complete, property coverage, referenze accademiche

---

## DECISIONI PRESE (con PERCHE)

| Decisione | Perche |
|-----------|--------|
| 5 categorie (non 4 originali) | Ricerca ha identificato Security come categoria essenziale (OAuth, mTLS da Scribble) |
| two_buyer incluso | IL protocollo canonico MPST (POPL 2008). Credibilita accademica obbligatoria |
| saga_order flat (no nested choice) | Parser LU 1.0 non supporta choice annidati. Ridisegnato con singola choice |
| confidence >= medium su consensus | F1 Guardiana: mancava coverage di confidence_min. Consensus = fit naturale |
| client cannot send token su auth | F1 Guardiana: mancava coverage di exclusion. Auth = fit semantico perfetto |
| Tipi dominio, non TaskRequest generico | F2 Guardiana: stdlib deve dimostrare type modeling RICCO, non generico |

---

## MAPPA SITUAZIONE

```
LINGUA UNIVERSALE (LA MISSIONE):
  FASE A-D: COMPLETE (28 moduli, media 9.5/10)
  FASE E: PER TUTTI
    E.1-E.5: DONE (9.5/10)
    E.6 CervellaLang 1.0: IN PROGRESS
      T3.1 Grammar 1.0 RFC:    DONE (S444)  <- grammatica frozen
      T3.2 Standard Library:    DONE (S445)  <- 20 protocolli!
      T3.3 lu init:              DONE (S444)  <- scaffolding + --template
      T3.4 lu verify:            DONE (S444)  <- verifica standalone
      T3.5 VS Code Marketplace:  TODO         <- blocco: Rafa publisher account
  PropertyKind: 9 (tutti coperti!) | CLI: 10 comandi | PyPI: v0.3.0
  Moduli: 29 | Test: 3435 | EBNF: 64 (frozen) | Stdlib: 20 protocolli

CI/CD: TUTTO GREEN
  26 workflow | CI Python: 1042 passed

DEPENDABOT (3 restanti):
  #30 stripe 17->20, #14 express 4->5, #11 zod 3->4
```

---

## PROSSIMA SESSIONE -- COSA FARE

### 1. TODO Rafa (azioni manuali, ancora aperti)
- [ ] **Dependabot Security Alerts**: abilitare su ENTRAMBI i repo
- [ ] **Environment production**: Required reviewers (rafapra3008)
- [ ] **Blog post**: revisione "From Vibe Coding to Vericoding"
- [ ] **VS Code Publisher**: creare account per T3.5

### 2. OBIETTIVI POSSIBILI
- **T3.5 VS Code Marketplace** (blocco: Rafa publisher account)
- **T3.6 Community Seeding** (blog + Show HN update con stdlib)
- **T2.1 PyPI v0.3.1** (include stdlib + --template + E.5 bug fix)
- **Nested choice support** (parser enhancement per saga con compensazione)

### 3. Quick wins
- #30 stripe 17->20 (1 code change + test)
- Tech debt: scripts/ dedup
- `lu lint` / `lu fmt` (backlog B5/B6)

---

## I NUMERI

| Metrica | Valore |
|---------|--------|
| Test LU | **3435** |
| Moduli LU | **29** |
| Stdlib Protocolli | **20** (5 categorie) |
| CLI Comandi | **10** (+--template, +--list-templates su init) |
| PropertyKind | **9** (tutti coperti da stdlib!) |
| EBNF Produzioni | **64** (frozen) |
| Guardiana Audit S445 | **1** (2 findings P2, tutti fixati) |

---

## FILE CHIAVE MODIFICATI (S445)

| File | Cosa |
|------|------|
| `stdlib/` | **NUOVO** - 20 file .lu in 5 categorie |
| `stdlib/README.md` | **NUOVO** - indice + property coverage + referenze |
| `_init_project.py` | +list_templates(), +_find_template(), +template param |
| `_cli.py` | +--template, +--list-templates su lu init |
| `test_stdlib_*.py` (5) | **NUOVO** - 72 test stdlib |
| `test_init_project.py` | +8 test (template CLI + list) |

---

## Lezioni Apprese (S445)

### Cosa ha funzionato bene
- **Formula Magica**: Ricerca (Scribble/MPST) -> 20 protocolli -> Audit -> Fix = diamante
- **Guardiana 9 PropertyKind check**: ha trovato 2 property mancanti che nessuno sapeva
- **Batch approach**: 5 categorie scritte e verificate in sequenza, test dopo ciascuna
- **Tipi di dominio**: Guardiana ha insistito su tipi specifici vs generici = qualita

### Cosa non ha funzionato
- **Nested choice**: saga_order aveva choice annidato (non supportato). Ridisegnato flat.
  Considerare supporto nested choice in futuro (parser enhancement).

### Pattern confermato
- **Guardiana dopo ogni batch**: trovare errori PRESTO, non alla fine
- **Ricerca accademica vale**: two_buyer da MPST, OAuth da Scribble = credibilita

---

*"Se nessuno l'ha fatto prima, e perche aspettavano noi."*
*Cervella & Rafa, S445 - 12 Marzo 2026*
<!-- AUTO-CHECKPOINT-START -->
## AUTO-CHECKPOINT: 2026-03-12 23:03 (auto)
- **Branch**: main
- **Ultimo commit**: 13e4d2f9 - S444: Final handoff -- auto-checkpoint updated, subroadmap metrics fixed
- **File modificati** (5):
  - .sncp/progetti/cervellaswarm/PROMPT_RIPRESA_cervellaswarm.md
  - .sncp/progetti/contabilita/PROMPT_RIPRESA_contabilita.md
  - .sncp/progetti/miracollo/PROMPT_RIPRESA_miracollo.md
  - .sncp/roadmaps/SUBROADMAP_E5_E6_FUTURO.md
  - NORD.md
<!-- AUTO-CHECKPOINT-END -->
