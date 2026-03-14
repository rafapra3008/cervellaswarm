# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-03-14 - Sessione 454
> **STATUS:** S454 "1M Context Freedom" COMPLETA. **3684 test.** PyPI v0.3.3. VS Code v0.2.0 LIVE.

---

## S454 -- 1M CONTEXT FREEDOM

Sessione dedicata all'infrastruttura: adattamento PROFONDO da 200K a 1M context. Non solo parametri (gia fatto in S452) ma COMPORTAMENTO, REGOLE e MENTALITA.

### Cosa abbiamo fatto

1. **Soglie context-monitor.py v3.0.0**: WARNING 70->85%, CRITICAL 75->92%, FLUSH 75->85%
2. **Subagent inject v2.0.0**: RIPRESA senza limite (era 100 righe), FATOS 150->200
3. **Output agenti**: 3000->5000 token nel _SHARED_DNA
4. **Task inline**: 5->15 min prima di delegare a spawn-workers
5. **Settings sync**: observability_hook + effortLevel allineati main/insiders
6. **DRY fix**: context-monitor + subagent_stop usano cervella_hooks_common
7. **Sicurezza P1**: bash_validator long flag bypass fixato (rm --force /)
8. **Logic P1**: session_end_sync_agents message loss fixato
9. **Famiglia allineata**: 17/17 agenti a v2.1.0, +memory a Security e Ingegnera
10. **Architect 1M**: limiti 10->25 files, 2000->4000 tokens plan
11. **Cleanup**: 12 file stali archiviati in insiders, dead code disabilitato
12. **ANSI strip + send_notification**: centralizzati in hooks_common (DRY)
13. **Validated patterns**: P18 500->700, P20 150->250, +P22 completo
14. **Observability v1.1.0**: transcript fallback limitato a 5 min (no sessione precedente)
15. **200K cliff gate**: statusline mostra "2x" sopra 200K
16. **REGOLE "ANSIA 200K" RIMOSSE**: CHECKLIST, CLAUDE.md, MANUALE aggiornati
    - Eliminato "checkpoint ogni 20 min" e "3+ task -> checkpoint"
    - "Anti-Compact Strategy" -> "Context Awareness"
    - Checkpoint guidato dal LAVORO, non dalla PAURA
17. **Ricerca big players**: Cursor/Aider/Windsurf/Cline analizzati (20+ fonti)
    - Report: `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260314_1M_CONTEXT_BIG_PLAYERS.md`

### Agenti utilizzati (5)
Tester (15/15 pass), Reviewer (7.5->fix->9+), Ingegnera (8.5->fix->9.5), Researcher (20+ fonti), Guardiana QA (9.3->fix->9.5+)

---

## DECISIONI PRESE (con PERCHE)

| Decisione | Perche |
|-----------|--------|
| Soglie 85/92% (non 80/90) | 85% = 150K liberi (piu del vecchio context intero!). 92% = 80K (abbastanza per checkpoint) |
| RIPRESA inject senza limite | File gia capped a 250 dal guard. 250 righe = 0.2% di 1M. Perche tagliare? |
| Output 5000 (non illimitato) | Report lunghi restano su disco (SNCP). 5000 = snippet codice senza forzare report per micro-task |
| "Ansia 200K" rimossa dalle regole | La COSTITUZIONE dice "il tempo crea paura, la paura crea fretta". Le regole checkpoint meccaniche contraddicevano il principio |
| Costo rimosso da statusline | Rafa preferisce pulizia. Costo tracciato in observability DB, non necessario in statusline |

---

## MAPPA SITUAZIONE

```
LINGUA UNIVERSALE (LA MISSIONE):
  FASE A-D: COMPLETE (29 moduli, media 9.5/10)
  FASE E: PER TUTTI
    E.1-E.5: DONE (9.5/10)
    E.6 CervellaLang 1.0: IN PROGRESS
      T3.1-T3.5: ALL DONE (S444-S453)
  T2.1 PyPI v0.3.3:              LIVE!
  LU 1.1+1.2:                    DONE!
  Moduli: 29 | Test: 3684 | CLI: 12 | Stdlib: 20

INFRASTRUTTURA: 1M CONTEXT FREEDOM (S454, 9.5/10)
  context-monitor v3.0.0, subagent_inject v2.0.0
  bash_validator v1.1.0, observability v1.1.0
  17/17 agenti v2.1.0, hooks_common v1.2.0+
  Regole "ansia 200K" eliminate

CI/CD: TUTTO GREEN + lint-format gate
PUBLIC REPO: synced S450 (serve sync S454!)
VS CODE MARKETPLACE: LIVE! v0.2.0
DEPENDABOT: 2 HOLD (stripe 17->20 #30, express 4->5 #14)
```

---

## PROSSIMA SESSIONE

| # | Cosa | Blocco | Effort |
|---|------|--------|--------|
| 1 | **Sync public repo** (S450->S454) | Nessuno | 10 min |
| 2 | **Blog + Show HN review con Rafa** | Rafa review | 15 min |
| 3 | **T2.3 Playground Chat tab** | Nessuno | 1-2 sessioni |
| 4 | **Dependabot: stripe 17->20, express 4->5** | Testing | 0.5 sessione |
| 5 | **T3.6 Community Seeding** | Dopo blog/Show HN | Continuo |
| 6 | **Cleanup cervellaswarm-extension/** | Nessuno | 5 min |

### Idee dalla ricerca big players
- Dynamic context discovery (Cursor-style, -46.9% token)
- Retrieval semantico su SNCP (lungo termine)
- T4.1 AI Agent Framework Integration

---

## DOVE TROVARE LE COSE

| Cosa | Path |
|------|------|
| Research Big Players | `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260314_1M_CONTEXT_BIG_PLAYERS.md` |
| Ingegnera Agent Audit | `.sncp/progetti/cervellaswarm/reports/ENGINEER_20260314_AGENT_DEFINITIONS_AUDIT.md` |
| Subroadmap S452 (1M) | `.sncp/roadmaps/SUBROADMAP_S452_OPUS_4_6_1M.md` |
| VS Code Extension | `extensions/lingua-universale-vscode/` |
| Blog post | `packages/lingua-universale/docs/blog_vibe_to_vericoding.md` |
| Playground | `playground/index.html` + `playground/examples.js` |

---

## Lezioni Apprese (S454)

### Cosa ha funzionato bene
- **5 agenti in parallelo per audit completo**: Tester + Reviewer + Ingegnera + Researcher + Guardiana. Copertura totale in ~2 ore. Pattern confermato.
- **Rafa insight "ansia da 200K"**: Il CEO ha notato che il COMPORTAMENTO non seguiva i PARAMETRI aggiornati. Feedback prezioso che ha portato a riscrivere 4 file di regole.
- **Fixare anche P3**: "ci piace fissare tutto" - ogni finding trovato e stato risolto. Zero finding aperti.

### Cosa non ha funzionato
- **Proporre checkpoint compulsivamente**: La Regina continuava a proporre "checkpoint?" per abitudine 200K, interrompendo il flusso. Fixato nelle regole e in memoria.

### Pattern confermato
- **"Ricerca big players prima di decidere"**: La Researcher ha trovato il 200K pricing cliff (TUTTO l'input costa 2x, non solo l'extra). Questo ha portato al gate "2x" nella statusline. Formula Magica confermata.

---
*"Ultrapassar os proprios limites!" -- S454, 1M Context Freedom!*
