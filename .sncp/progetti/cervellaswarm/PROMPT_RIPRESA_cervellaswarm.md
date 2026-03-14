# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-03-14 - Sessione 454
> **STATUS:** S454 COMPLETA. Primo dogfooding LU! 8/8 PROVED. **3684 test.** PyPI v0.3.3. VS Code v0.2.0 LIVE.

---

## S454 -- COSA ABBIAMO FATTO (2 blocchi)

### Blocco 1: 1M Context Freedom (infrastruttura)

Adattamento PROFONDO da 200K a 1M context. Non solo parametri (S452) ma COMPORTAMENTO, REGOLE e MENTALITA.

**17 modifiche principali** (30+ file toccati):
1. context-monitor.py v3.0.0: soglie 85/92/85%, DRY import, 200K cliff gate
2. subagent_context_inject.py v2.0.0: RIPRESA senza limite, FATOS 200
3. _SHARED_DNA output 3000->5000 token, task inline 5->15 min
4. bash_validator v1.1.0: P1 sicurezza (long flag bypass rm --force /)
5. session_end_sync_agents: P1 logic (message loss)
6. observability v1.1.0: transcript fallback < 5 min
7. 17/17 agenti v2.1.0, +memory Security/Ingegnera, architect limiti 1M
8. Settings sync, validated patterns (P18 700, P20 250, +P22), ANSI+notify DRY
9. **REGOLE "ANSIA 200K" RIMOSSE**: checkpoint guidato dal LAVORO, non dalla PAURA
10. 12 file stali insiders archiviati, dead code disabilitato, 520MB cleanup

**5 agenti paralleli**: Tester 15/15, Reviewer 7.5->9+, Ingegnera 8.5->9.5, Researcher 20+ fonti, Guardiana 9.5+

### Blocco 2: Primo Dogfooding LU (momento storico!)

**Il primo programma REALE scritto in Lingua Universale.**

- `examples/dogfood_agent_orchestration.lu`: 3 agenti (supervisor/worker/validator), nested choice (pass/fail), **8/8 proprieta PROVED**
- `examples/dogfood_runner.py`: parse, verify, codegen, happy path, fail branch, violation BLOCCATA a runtime
- Guardiana audit: 9.3 -> fix (SPDX, dead type, TODO comment) -> 9.5+
- Gap trovato: serve public API `load_protocol(path) -> Protocol` (TODO per T4.1)

### Ricerche completate (3 report)
- Big players (Cursor/Aider/Windsurf/Cline) context strategies: 20+ fonti
- Playground Chat tab: architettura sync bridge (process_input API gia esiste!)
- Dogfooding strategy: Guardiana valutazione 3 opzioni -> Agent Orchestration (8.5/10)

---

## DECISIONI PRESE (con PERCHE)

| Decisione | Perche |
|-----------|--------|
| Soglie 85/92% | 85% = 150K liberi (piu del vecchio context!). 92% = 80K per checkpoint |
| Regole "ansia 200K" rimosse | COSTITUZIONE dice "il tempo crea paura". Checkpoint meccanici contraddicevano |
| Dogfood = Agent Orchestration | Score 8.5/10 vs 6.0 (ricette) e 6.8 (task). IL differenziatore T4.1 |
| Costo rimosso da statusline | Rafa preferisce pulizia. Costo in observability DB |

---

## MAPPA SITUAZIONE

```
LINGUA UNIVERSALE (LA MISSIONE):
  FASE A-D: COMPLETE (29 moduli, media 9.5/10)
  FASE E: PER TUTTI
    E.1-E.5: DONE (9.5/10)
    E.6 CervellaLang 1.0: T3.1-T3.5 ALL DONE
  PyPI v0.3.3 LIVE | VS Code v0.2.0 LIVE | Playground LIVE
  Moduli: 29 | Test: 3684 | CLI: 12 | Stdlib: 20

DOGFOODING: PRIMO PROGRAMMA REALE IN LU!  <- NUOVO S454!
  dogfood_agent_orchestration.lu: 8/8 PROVED
  dogfood_runner.py: happy + fail + violation
  Gap: load_protocol() public API (T4.1)

INFRASTRUTTURA: 1M CONTEXT FREEDOM (S454, 9.5/10)
  18 hooks, 17 agenti v2.1.0, regole "ansia" rimosse

CI/CD: TUTTO GREEN
PUBLIC REPO: synced S454 (packages/ non cambiati = gia sync)
DEPENDABOT: 2 HOLD (stripe #30, express #14)
```

---

## PROSSIMA SESSIONE (S455)

### Priorita 1: Community & Launch

| # | Cosa | Blocco | Effort |
|---|------|--------|--------|
| 1 | **Show HN v2 review finale con Rafa** | Rafa review | 15 min insieme |
| 2 | **Blog post review** (blog_vibe_to_vericoding.md) | Rafa review | 10 min |
| 3 | **Decidere timing lancio** (martedi/mercoledi US mattina) | Decisione Rafa | 5 min |

### Priorita 2: Playground Chat (T2.3)

| # | Cosa | Note | Effort |
|---|------|------|--------|
| 4 | **Playground Chat tab** | Ricerca FATTA, architettura sync bridge. `process_input()` API gia esiste. ~50 righe JS + HTML bubbles | 1 sessione |

### Priorita 3: Dogfooding Fase 2

| # | Cosa | Note | Effort |
|---|------|------|--------|
| 5 | **Dogfood con Claude API reale** (non mock) | Integrare anthropic SDK nel runner | 1 sessione |
| 6 | **Public API load_protocol()** | Gap trovato dal dogfooding, serve per T4.1 | 0.5 sessione |
| 7 | **Demo video VHS** (dogfood + playground) | VHS gia installato, pattern validato | 0.5 sessione |

### Backlog

| # | Cosa | Effort |
|---|------|--------|
| 8 | Dependabot (stripe #30, express #14) | 0.5 sessione |
| 9 | T1.5 Test persona non-tecnica | Dipende da tester |
| 10 | Dynamic context discovery (Cursor-style) | Ricerca fatta, implementazione futura |
| 11 | Retrieval semantico su SNCP | Lungo termine |

---

## DOVE TROVARE LE COSE

| Cosa | Path |
|------|------|
| **Dogfood protocollo** | `packages/lingua-universale/examples/dogfood_agent_orchestration.lu` |
| **Dogfood runner** | `packages/lingua-universale/examples/dogfood_runner.py` |
| **Research Big Players** | `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260314_1M_CONTEXT_BIG_PLAYERS.md` |
| **Research Playground Chat** | `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260314_PLAYGROUND_CHAT_TAB.md` |
| **Ingegnera Agent Audit** | `.sncp/progetti/cervellaswarm/reports/ENGINEER_20260314_AGENT_DEFINITIONS_AUDIT.md` |
| Show HN v2 draft | `docs/SHOW_HN_V2_DRAFT.md` (aggiornato con VS Code link) |
| Blog post | `packages/lingua-universale/docs/blog_vibe_to_vericoding.md` |
| Subroadmap E5+E6+Futuro | `.sncp/roadmaps/SUBROADMAP_E5_E6_FUTURO.md` |
| Subroadmap S452 (1M) | `.sncp/roadmaps/SUBROADMAP_S452_OPUS_4_6_1M.md` |

---

## Lezioni Apprese (S454)

### Cosa ha funzionato bene
- **5 agenti paralleli per audit**: Tester + Reviewer + Ingegnera + Researcher + Guardiana. Copertura totale. Pattern confermato per la 5a volta.
- **Dogfooding trova gap REALI**: Il primo programma in LU ha trovato `load_protocol()` mancante + 3 gap API doc. Evidenza concreta per T4.1.
- **"Fixare anche P3"**: Ogni finding risolto, zero aperti. Il diamante brilla nei dettagli.

### Cosa non ha funzionato
- **Proporre checkpoint compulsivamente**: Abitudine da 200K. Fixato nelle regole E in memoria. Con 1M, il lavoro guida il ritmo.

### Pattern confermato
- **Dogfooding come metodo di sviluppo**: Usare il proprio linguaggio per costruire qualcosa di REALE trova gap che nessun test unitario troverebbe. Il runner ha rivelato 4 gap in 2 ore che sarebbero rimasti nascosti per mesi. Evidenza: S454.

---
*"Ultrapassar os proprios limites!" -- S454, il giorno in cui LU e diventato REALE.*
