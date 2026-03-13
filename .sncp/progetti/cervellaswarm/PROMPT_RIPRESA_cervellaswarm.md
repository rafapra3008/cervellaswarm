# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-03-13 - Sessione 451
> **STATUS:** Sprint 1+2+3 COMPLETE. **3684 test.** PyPI v0.3.3 LIVE. 12 CLI. Playground lint. Public repo synced.

---

## S451 -- COSA ABBIAMO FATTO

### 1. Checkpoint & Housekeeping
- NORD.md aggiornato: S447 → S451 (3684 test, v0.3.3, Sprint 1+2+3, playground lint)
- SUBROADMAP_E5_E6_FUTURO.md: metriche aggiornate (3641→3684, B5/B6/Sprint info)
- Verifica stato: public repo synced, CI green, 2 Dependabot HOLD

### 2. Guida Azure DevOps per Rafa (IN PROGRESS)
- Rafa ha creato account Azure (con carta per verifica)
- **PROBLEMA:** Era su portal.azure.com (Azure Cloud) -- sito SBAGLIATO
- **SERVE:** dev.azure.com (Azure DevOps) per creare PAT token
- Guida dettagliata scritta (vedi sezione PROSSIMA SESSIONE)

---

## DECISIONI PRESE (con PERCHE)

| Decisione | Perche |
|-----------|--------|
| Zero-config fmt | gofmt/elm-format: "one true style". LU e giovane. |
| lint_program (no double parse) | LSP calls parse() once, passes AST to lint. Performance. |
| Public API exports (`X as X`) | Type-checker-visible re-exports. Pyodide usa public API, non `._lint`. |
| 1 blank line tra sezioni (not 2) | DSL concisa. Stdlib usa 1. |

---

## MAPPA SITUAZIONE

```
LINGUA UNIVERSALE (LA MISSIONE):
  FASE A-D: COMPLETE (29 moduli, media 9.5/10)
  FASE E: PER TUTTI
    E.1-E.5: DONE (9.5/10)
    E.6 CervellaLang 1.0: IN PROGRESS
      T3.1 Grammar 1.0 RFC:    DONE (S444)
      T3.2 Standard Library:    DONE (S445, 20 protocolli)
      T3.3 lu init:              DONE (S444)
      T3.4 lu verify:            DONE (S444)
      T3.5 VS Code Marketplace:  TODO         <- blocco: Rafa (Azure DevOps PAT)
  T2.1 PyPI v0.3.3:              LIVE!
  LU 1.1+1.2:                    DONE!
  B5 lu lint:                     DONE!       <- 10 rules, LSP+CI integrated
  B6 lu fmt:                      DONE!       <- zero-config, LSP+CI integrated
  Moduli: 29 | Test: 3684 | CLI: 12 | Stdlib: 20

SPRINT 1 (Dogfood & Polish): COMPLETE (9.5/10)
SPRINT 2 (Quality & Testing): COMPLETE (9.5/10)
SPRINT 3 (Community Prep): COMPLETE (9.5/10)
  3.1 README update:    DONE
  3.2 Blog post:        DONE
  3.3 Playground lint:  DONE (S450, 9.5/10)
  3.4 Show HN v2:       DONE

PUBLIC API: lint_source, format_source exported (S450)
CI/CD: TUTTO GREEN + lint-format gate
PUBLIC REPO: synced S450 (2 sync: lint button + stdlib examples)
DEPENDABOT: 2 HOLD (stripe 17→20 #30, express 4→5 #14)
```

---

## PROSSIMA SESSIONE

### 1. TODO Rafa (guidare passo passo!)

**T3.5 - VS Code Publisher Account:**
1. Andare su **https://dev.azure.com** (NON portal.azure.com!)
2. Login con stesso account Azure
3. Creare organizzazione se chiede (nome qualsiasi, es: "cervellaswarm")
4. Icona utente top-right → **"Personal access tokens"**
5. **New Token**: name=`vscode-marketplace`, All organizations, 90 days
6. Scopes: "Show all scopes" → **Marketplace → Manage** (spunta)
7. Create → **COPIARE IL TOKEN** (visibile solo una volta!)
8. Poi: marketplace.visualstudio.com/manage → Create publisher
   - Publisher name: `cervellaswarm`, Display name: `CervellaSwarm`

**Altro Rafa:**
- [ ] Blog post: revisione `packages/lingua-universale/docs/blog_vibe_to_vericoding.md`
- [ ] Show HN v2: review `docs/SHOW_HN_V2_DRAFT.md` + decidere timing

### 2. OBIETTIVI (priorita)

| # | Cosa | Blocco | Effort |
|---|------|--------|--------|
| 1 | **T3.5 VS Code Marketplace** | Rafa: PAT token | 0.5 sessione dopo PAT |
| 2 | **Blog + Show HN review con Rafa** | Rafa review | 15 min insieme |
| 3 | **T2.3 Playground Chat tab** | Nessuno | 1-2 sessioni |
| 4 | **Dependabot: stripe 17→20, express 4→5** | Testing needed | 0.5 sessione |
| 5 | **T3.6 Community Seeding** | Dopo blog/Show HN | Continuo |

### 3. Idee proattive (non urgenti)
- T2.4 Property Templates Library (quick wins per guided mode)
- Documentation site (Sphinx/MkDocs) per la community
- T4.1 AI Agent Framework Integration (il vero differenziatore)

---

## I NUMERI

| Metrica | Valore |
|---------|--------|
| Test LU | **3684** |
| Moduli LU | **29** |
| Stdlib | **20** (5 categorie) |
| CLI | **12** |
| Lint rules | **10** (3 categorie) |
| LSP tests | **79** |
| PropertyKind | **9** |
| Guardiana | S449: 9.5/10, S450: 9.5/10 |

---

## DOVE TROVARE LE COSE

| Cosa | Path |
|------|------|
| Subroadmap Polish (COMPLETA) | `.sncp/roadmaps/SUBROADMAP_S449_POLISH.md` |
| Subroadmap E5+E6+Futuro | `.sncp/roadmaps/SUBROADMAP_E5_E6_FUTURO.md` |
| Blog post | `packages/lingua-universale/docs/blog_vibe_to_vericoding.md` |
| Show HN v2 draft | `docs/SHOW_HN_V2_DRAFT.md` |
| Sync script | `scripts/git/sync-to-public.sh` |
| Playground | `playground/index.html` + `playground/examples.js` |
| Public API exports | `packages/lingua-universale/src/cervellaswarm_lingua_universale/__init__.py` |

---

## Lezioni Apprese (S451)

### Cosa ha funzionato bene
- **Checkpoint con calma**: Prendersi il tempo per aggiornare TUTTE le mappe (NORD, subroadmap, PROMPT_RIPRESA) = zero confusione per la prossima sessione.
- **Guida passo-passo per Rafa**: Istruzioni dettagliate con URL esatti (dev.azure.com vs portal.azure.com) evitano perdita di tempo.

### Pattern confermato
- **Mappe sempre aggiornate**: NORD era 3 sessioni indietro (S447). Aggiornarlo subito = chiarezza per tutti.
- **S411 regola rispettata**: MAI toccare PROMPT_RIPRESA di altri progetti (contabilita/miracollo hanno modifiche uncommitted -- NON nostre).

---
*"Ultrapassar os proprios limites!" -- S451*
