# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-03-13 - Sessione 452
> **STATUS:** Opus 4.6 + 1M Context Adaptation COMPLETA. Guardiana 9.5/10. **3684 test.** PyPI v0.3.3 LIVE.

---

## S452 -- COSA ABBIAMO FATTO

### Opus 4.6 + 1M Context Adaptation (10/10 task DONE)

Anthropic ha rilasciato Opus 4.6 con 1M context nativo. Abbiamo adattato TUTTA l'infrastruttura:

1. **3 ricerche parallele** (researcher + researcher + ingegnera):
   - 1M = 5x (100K righe vs 20K). Intero codebase LU in un contesto.
   - Subagents: 1M CIASCUNO, contesto fresco (NON ereditano parent)
   - Pricing: >200K = 2x costo. Prompt caching (-90%) gia attivo.
   - Fast Mode: stesso modello, 2.5x veloce, 6x prezzo. MAI per agenti.
   - Context rot: esiste anche con 1M. Info critiche inizio/fine contesto.
   - SNCP "MINIMO in memoria" RESTA VALIDO: per qualita e costi, non spazio.

2. **7 file aggiornati:**
   - `_SHARED_DNA.md`: Context-smart con PERCHE, output 2000→3000
   - `subagent_context_inject.py` v1.4.0: RIPRESA 40→100, FATOS 100→150
   - `file_limits_guard.py` v3.3.0: PROMPT_RIPRESA 150→250
   - `cervella-researcher.md` v2.1.0: +memory: user
   - `cervella-scienziata.md` v2.1.0: +memory: user
   - `CLAUDE.md`: Fast Mode rules, costi 1M, limite 250
   - `CHECKLIST_SESSIONE.md`: 150→250
   - `PROMPT_INIZIO_SESSIONE.md`: "Task tool"→"Agent tool"

3. **Guardiana audit: 9.3→9.5/10** (3 fix P2 applicati)

### Reports scritti
- `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260313_CLAUDE_OPUS_4_6_1M_CONTEXT.md`
- `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260313_CLAUDE_CODE_FAST_MODE.md`
- `.sncp/progetti/cervellaswarm/reports/ENGINEER_20260313_1M_CONTEXT_INFRASTRUCTURE_ANALYSIS.md`

---

## DECISIONI PRESE (con PERCHE)

| Decisione | Perche |
|-----------|--------|
| MANTENERE "MINIMO in memoria" | Context rot + costi 2x sopra 200K. Non per spazio |
| MANTENERE COSTITUZIONE_OPERATIVA | Ha scopo proprio: focus per worker. Non hack 200K |
| Fast Mode MAI per agenti | 6x prezzo, qualita identica, invalida prompt cache |
| RIPRESA inject 40→100 | Workers hanno 1M, piu contesto = meno errori |
| PROMPT_RIPRESA 150→250 | Spazio per MAPPA+DECISIONI+LEZIONI senza compressione |
| Output max 2000→3000 | Workers possono dare sintesi piu ricche |
| +memory a researcher+scienziata | Cross-sessione: ricordano fonti e dati mercato |
| Security resta opus | Audit sicurezza meritano qualita opus |
| NON rimuovere agenti | Tutti hanno un ruolo, anche se poco usati |
| Agent Teams ancora EXPERIMENTAL | Env var CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS serve |

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

SPRINT 1+2+3: ALL COMPLETE (9.5/10 each)
INFRASTRUTTURA: Opus 4.6 + 1M ADATTATA (S452, 9.5/10)
CI/CD: TUTTO GREEN + lint-format gate
PUBLIC REPO: synced S450
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
| Guardiana | S452: 9.5/10 |

---

## DOVE TROVARE LE COSE

| Cosa | Path |
|------|------|
| Subroadmap S452 (1M Adaptation) | `.sncp/roadmaps/SUBROADMAP_S452_OPUS_4_6_1M.md` |
| Subroadmap E5+E6+Futuro | `.sncp/roadmaps/SUBROADMAP_E5_E6_FUTURO.md` |
| Research 1M Context | `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260313_CLAUDE_OPUS_4_6_1M_CONTEXT.md` |
| Research Fast Mode | `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260313_CLAUDE_CODE_FAST_MODE.md` |
| Ingegnera Analysis | `.sncp/progetti/cervellaswarm/reports/ENGINEER_20260313_1M_CONTEXT_INFRASTRUCTURE_ANALYSIS.md` |
| Blog post | `packages/lingua-universale/docs/blog_vibe_to_vericoding.md` |
| Playground | `playground/index.html` + `playground/examples.js` |

---

## Lezioni Apprese (S452)

### Cosa ha funzionato bene
- **3 ricerche parallele**: Researcher + Researcher + Ingegnera in parallelo = risultati completi in ~3 minuti. Pattern perfetto per esplorazione ampia.
- **Formula Magica applicata**: RICERCA PRIMA (3 agenti), poi ROADMAP (task list 10 step), poi IMPLEMENTAZIONE step by step. Zero sorprese.
- **Guardiana dopo ogni blocco**: Audit parziale (T2-T4) + audit finale (T2-T10) = 6 finding catturati e fixati. Standard 9.5/10 mantenuto.

### Cosa non ha funzionato
- **Output agenti difficile da leggere**: I file .output degli agenti sono JSONL, non text. Serve parsing per estrarre risultati. (Non un bug nostro, e il formato Claude Code)

### Pattern confermato
- **"MINIMO in memoria" resta il principio giusto**: Con 1M il rischio e RIEMPIRE il contesto, non esaurirlo. Disciplina > spazio.
- **Ingegnera analizza PRIMA** (S436+): L'analisi quantitativa (8,325 token Regina, 2,151 token worker) ha guidato TUTTE le decisioni numeriche. Evidenza: 3a sessione consecutiva.

---
*"Ultrapassar os proprios limites!" -- S452, la sessione del 1M!*
