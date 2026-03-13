# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-03-13 - Sessione 453
> **STATUS:** T3.5 VS Code Marketplace PUBBLICATO! v0.2.0 LIVE. **3684 test.** PyPI v0.3.3. Guardiana 9.5/10.

---

## S453 -- COSA ABBIAMO FATTO

### T3.5 VS Code Marketplace -- PUBBLICATO!

Lingua Universale e ora sul VS Code Marketplace. Qualsiasi developer puo installarla cercando "Lingua Universale" in VS Code.

**Link:** `https://marketplace.visualstudio.com/items?itemName=cervellaswarm.lingua-universale`

**Cosa abbiamo fatto:**

1. **Explorer + Researcher in parallelo** per mappare stato estensione e requisiti Marketplace
2. **4 fix pre-pubblicazione:**
   - Grammar: +`no deletion` e +`X exclusive Y` (2 PropertyKind da E.5 mancanti)
   - package.json: +Formatters categoria, +`vscode:prepublish` script, +homepage/bugs
   - CHANGELOG: aggiornato v0.2.0 con formatting, lint, grammar
   - README: +sezione Marketplace install, +formatting feature, +properties table aggiornata
3. **Guardiana audit: 9.3/10** -- trovato **bug P2**: ROLE_EXCLUSIVE regex usava PascalCase invece di snake_case. Fixato subito.
4. **VSIX v0.2.0** ricostruito (13.73 KB, 10 file)
5. **Guidato Rafa passo passo** su Azure DevOps:
   - Creata organizzazione `cervellaswarm` su dev.azure.com
   - Creato PAT token (Marketplace Manage, 1 anno)
   - Publisher `cervellaswarm` gia esistente, aggiornato con logo + description + links
6. **Pubblicato con `vsce publish -p TOKEN`** -- LIVE!

### Infra Azure DevOps (per Rafa)

- **Organizzazione:** dev.azure.com/cervellaswarm
- **Progetto:** lu-vscode (creato per completare setup, non usato attivamente)
- **PAT token:** salvato in `.env` come `VSCE_PAT` (gitignored, scade 12/03/2027)
- **Publisher:** marketplace.visualstudio.com/manage/publishers/cervellaswarm

### Scoperte proattive

- `cervellaswarm-extension/` e una vecchia directory con VS Code scaricato dentro `.vscode-test/`. Da rimuovere (cleanup).
- dev.azure.com redirect: utenti nuovi vengono mandati a portal.azure.com. Usare **aex.dev.azure.com** per creare organizzazione.
- `vsce login` non funziona per setup nuovi. Usare `vsce publish -p TOKEN` direttamente.

---

## DECISIONI PRESE (con PERCHE)

| Decisione | Perche |
|-----------|--------|
| ROLE_EXCLUSIVE snake_case nel grammar | Parser usa `_expect_ident()` = solo snake_case. PascalCase non avrebbe mai matchato |
| `vscode:prepublish` aggiunto | vsce lo chiama automaticamente prima di package/publish, garantisce build fresco |
| PAT in .env SOLO | Regola security: MAI secrets in PROMPT_RIPRESA o file tracked |
| Publisher ID = cervellaswarm | Match esatto con package.json. Publisher gia esisteva |
| Non bumped a 0.3.0 | Versione indipendente da PyPI. 0.2.0 mai pubblicata prima, corretto mantenerla |

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
      T3.5 VS Code Marketplace:  DONE! (S453)      <- NUOVO!
  T2.1 PyPI v0.3.3:              LIVE!
  LU 1.1+1.2:                    DONE!
  B5 lu lint:                     DONE!
  B6 lu fmt:                      DONE!
  Moduli: 29 | Test: 3684 | CLI: 12 | Stdlib: 20

SPRINT 1+2+3: ALL COMPLETE (9.5/10 each)
INFRASTRUTTURA: Opus 4.6 + 1M ADATTATA (S452, 9.5/10)
CI/CD: TUTTO GREEN + lint-format gate
PUBLIC REPO: synced S450 (serve sync S453!)
VS CODE MARKETPLACE: LIVE! cervellaswarm.lingua-universale v0.2.0
DEPENDABOT: 2 HOLD (stripe 17->20 #30, express 4->5 #14)
```

---

## PROSSIMA SESSIONE

### 1. TODO Rafa

- [ ] **Verificare pagina Marketplace** (puo servire 5-30 min dopo pubblicazione): `https://marketplace.visualstudio.com/items?itemName=cervellaswarm.lingua-universale`
- [ ] **Fix publisher details** (Support e Source code repository invertiti): marketplace.visualstudio.com/manage
- [ ] **Blog post review**: `packages/lingua-universale/docs/blog_vibe_to_vericoding.md`
- [ ] **Show HN v2 review**: `docs/SHOW_HN_V2_DRAFT.md` + decidere timing

### 2. OBIETTIVI (priorita)

| # | Cosa | Blocco | Effort |
|---|------|--------|--------|
| 1 | **Sync public repo** (S450->S453) | Nessuno | 10 min |
| 2 | **Blog + Show HN review con Rafa** | Rafa review | 15 min insieme |
| 3 | **T2.3 Playground Chat tab** | Nessuno | 1-2 sessioni |
| 4 | **Dependabot: stripe 17->20, express 4->5** | Testing needed | 0.5 sessione |
| 5 | **T3.6 Community Seeding** | Dopo blog/Show HN | Continuo |
| 6 | **Cleanup cervellaswarm-extension/** | Nessuno | 5 min |

### 3. Idee proattive (non urgenti)

- T2.4 Property Templates Library (quick wins per guided mode)
- Documentation site (Sphinx/MkDocs) per la community
- T4.1 AI Agent Framework Integration (il vero differenziatore)
- Show HN v2 con VS Code Marketplace link (piu completo!)

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
| VS Code ext | **v0.2.0 LIVE** |
| Guardiana S453 | 9.3 -> fix -> 9.5+ |

---

## DOVE TROVARE LE COSE

| Cosa | Path |
|------|------|
| **VS Code Extension** | `extensions/lingua-universale-vscode/` |
| **VS Code Marketplace** | `marketplace.visualstudio.com/items?itemName=cervellaswarm.lingua-universale` |
| Subroadmap E5+E6+Futuro | `.sncp/roadmaps/SUBROADMAP_E5_E6_FUTURO.md` |
| Subroadmap S452 (1M) | `.sncp/roadmaps/SUBROADMAP_S452_OPUS_4_6_1M.md` |
| Research Marketplace Publish | `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260313_VSCODE_MARKETPLACE_PUBLISH.md` |
| Blog post | `packages/lingua-universale/docs/blog_vibe_to_vericoding.md` |
| Playground | `playground/index.html` + `playground/examples.js` |
| PAT token | `.env` (VSCE_PAT, gitignored, scade 12/03/2027) |

---

## Lezioni Apprese (S453)

### Cosa ha funzionato bene
- **Guardiana dopo ogni step**: Trovato bug P2 (ROLE_EXCLUSIVE regex PascalCase) prima della pubblicazione. Pattern confermato per la 4a sessione.
- **Explorer + Researcher in parallelo**: Mappa completa dell'estensione + requisiti Marketplace in ~2 min. Zero sorprese.
- **Guida passo passo Rafa**: Screenshot-driven workflow funziona perfettamente per task che richiedono azione umana. Ogni passo verificato visivamente.

### Cosa non ha funzionato
- **dev.azure.com redirect**: Rafa finiva su portal.azure.com. Il fix e usare aex.dev.azure.com. Documentato per il futuro.
- **vsce login fallisce per setup nuovi**: `vsce publish -p TOKEN` funziona direttamente. Non perdere tempo con login.

### Pattern confermato
- **"Screenshot-driven guidance" per task Rafa**: Chiedere screenshot ad ogni passo = zero errori, zero confusione. 6 passi guidati, tutti perfetti. Evidenza: S453 (Azure DevOps + publisher + PAT).

---
*"Ultrapassar os proprios limites!" -- S453, Lingua Universale sul VS Code Marketplace!*
