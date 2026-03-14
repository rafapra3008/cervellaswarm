# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-03-14 - Sessione 459
> **STATUS:** 2/5 progetti showcase LIVE e synced al pubblico. Prossimo: Incident Replay o Show HN.

---

## DOVE SIAMO -- IL QUADRO COMPLETO

### La storia recente (S455-S459)

**S455-S456 (svolta strategica):** Rafa ha fermato tutto. 7 report indipendenti. Verita: 455 sessioni, 3684 test, ZERO utenti. Decisione: 5 progetti showcase PRIMA di lanciare. Identita fixata: LU = prodotto, CervellaSwarm = organizzazione.

**S457:** Security fixes, bug hunt, ops cleanup.

**S458:** Costruito e deployato il **LU Debugger** su Fly.io in 1 sessione.

**S459 (oggi):** Sync pubblico del Debugger + README. Scoperto che il **Tour of LU** era gia al 90% nel playground -- aggiunto completion tracking + celebration. 2 audit Guardiana (9.5/10 entrambi), tutti i fix applicati. 2 sync al repo pubblico.

---

## COSA E LIVE

### 1. LU Debugger -- https://lu-debugger.fly.dev/

3 agenti AI (Customer, Warehouse, Payment) su protocollo verificato. Demo + Live (Claude API). Click "Break" = violazione BLOCCATA.
- Stack: FastAPI + SSE + Monaco + Fly.io (Frankfurt, 2 macchine)
- Codice: `lu-debugger/` (7 file, 1474 righe)
- Costo: ~$0.000005/run (Haiku 4.5)
- Fly.io console: https://fly.io/apps/lu-debugger

### 2. Tour of LU -- https://rafapra3008.github.io/cervellaswarm/?tour

24 step interattivi, 4 capitoli (Types, Agents, Protocols, Putting It All Together). 4 esercizi con soluzioni. Completion tracking + celebration finale.
- Codice: `playground/tour.js` + `playground/tour-ui.js` + `playground/tour.css`
- Zero backend (Pyodide + Monaco nel browser)

---

## MAPPA SITUAZIONE

```
LINGUA UNIVERSALE:
  31 moduli | 3684 test | PyPI v0.3.3 | VS Code v0.2.0
  Playground: https://rafapra3008.github.io/cervellaswarm/
  Tour: playground/?tour (24 step, 4 capitoli)
  Debugger: https://lu-debugger.fly.dev/

5 PROGETTI SHOWCASE:
  1. LU Debugger      DONE! LIVE (S458)
  2. Tour of LU       DONE! LIVE (S459)
  3. Incident Replay  <- PROSSIMO (1 sessione, pagina statica)
  4. Protocol Zoo     (2-3 sessioni)
  5. AI Code Review   (3-4 sessioni)

LANCIO:
  Show HN v2: READY (docs/SHOW_HN_V2_DRAFT.md) -- da aggiornare con link Debugger+Tour
  Blog: READY, Guardiana 9.8/10
  HN Playbook: 10 risposte pronte
  Discord: DA CREARE (Rafa)
  Public repo: SYNCED (Debugger + Tour + README aggiornato)
```

---

## PROSSIMI STEP (ordine suggerito)

### Opzione A: Incident Replay (Progetto 3)

Storia interattiva: "Un bug AI e costato $34K. Ecco come LU lo avrebbe fermato."
- Narrativa credibile (e-commerce, rimborsi duplicati)
- Animazione step-by-step del bug
- Replay "con LU" -- violazione bloccata
- Pagina statica (zero backend), 1 sessione
- Dettagli: `.sncp/roadmaps/MAPPA_5_PROGETTI_LU.md`

### Opzione B: Show HN v2 (lancio con 2 progetti)

Abbiamo gia Debugger + Tour + Playground + Blog + Colab. Potremmo lanciare ora:
1. Aggiornare Show HN draft con link Debugger + Tour
2. Aggiornare blog con link
3. Submit su Hacker News
- Draft pronto: `docs/SHOW_HN_V2_DRAFT.md`
- Playbook: `docs/HN_RESPONSE_PLAYBOOK.md`

### Da Rafa (CEO)

- [ ] Decidere: Incident Replay prima o Show HN ora?
- [ ] Creare Discord "Lingua Universale" (5 canali, invite link permanente)
- [ ] Lista 15-20 persone per DM pre-lancio

---

## DOVE TROVARE LE COSE

| Cosa | Path |
|------|------|
| **LU Debugger (codice)** | `lu-debugger/` (7 file) |
| **LU Debugger (live)** | https://lu-debugger.fly.dev/ |
| **Tour of LU (codice)** | `playground/tour.js`, `tour-ui.js`, `tour.css` |
| **Tour of LU (live)** | https://rafapra3008.github.io/cervellaswarm/?tour |
| **MAPPA 5 PROGETTI** | `.sncp/roadmaps/MAPPA_5_PROGETTI_LU.md` |
| **MAPPA STRATEGICA** | `.sncp/roadmaps/MAPPA_STRATEGICA_2026.md` |
| **Show HN v2** | `docs/SHOW_HN_V2_DRAFT.md` |
| **Blog** | `packages/lingua-universale/docs/blog_vibe_to_vericoding.md` |
| **HN Playbook** | `docs/HN_RESPONSE_PLAYBOOK.md` |
| **Fly.io console** | https://fly.io/apps/lu-debugger |
| **Public repo** | github.com/rafapra3008/cervellaswarm |
| **Debugger Architecture** | `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260314_LU_DEBUGGER_ARCHITECTURE.md` |
| **Tour Research** | `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260314_TOUR_OF_LU.md` |

---

## DECISIONI PRESE (S458-S459)

1. **SSE, non WebSocket** per Debugger -- unidirezionale, piu semplice
2. **Fly.io** per hosting -- account esistente, no cold start
3. **Tour al 90% gia esistente** -- non ricostruire, polish e ship
4. **Completion tracking "done" vs "visited"** -- distingue chi ha cliccato Check/Run
5. **Celebration finale** con link a Debugger + PyPI -- cross-promotion tra showcase

---

## Lezioni Apprese (S459)

### Cosa ha funzionato bene
- **Guardiana su ogni step**: 2 audit, 1 P2 critico trovato (progress regression). Pattern "step -> audit -> fix" funziona.
- **Researcher in background**: ha scoperto che il Tour era gia al 90%. Ha risparmiato 2 sessioni di lavoro.
- **Cross-promotion**: ogni nuovo progetto linka gli altri (Debugger celebration -> Tour, README -> Debugger)

### Cosa non ha funzionato
- **Stima sforzo Tour**: MAPPA diceva 2 sessioni, reale ~1 ora. Leggere il codice PRIMA di stimare.

### Pattern confermato
- **"Leggi prima, costruisci dopo"**: controllare cosa esiste prima di pianificare da zero. Il Tour era GIA LA.

---
*"Non e sempre come immaginiamo... ma alla fine e il 100000%!"*
*S459: due progetti showcase LIVE. Il mondo ci puo trovare.*
