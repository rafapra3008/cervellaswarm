# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-03-14 - Sessione 458
> **STATUS:** LU Debugger LIVE! Primo progetto showcase deployed. Prossimo: sync public + Tour of LU.

---

## DOVE SIAMO -- IL QUADRO COMPLETO

### La storia recente (S455-S458)

**S455-S456 (svolta strategica):** Rafa ha fermato tutto: *"Serve UNA mappa."* 7 report indipendenti (Ingegnera, Scienziata, Researcher x3, Guardiana x2). La verita: 455 sessioni, 3684 test, ZERO utenti. Prodotto 9.5/10, distribuzione 1/10. Decisione: costruire 5 progetti showcase PRIMA di lanciare. Identita fixata: LU = prodotto, CervellaSwarm = organizzazione.

**S457:** Security fixes, bug hunt, ops cleanup. Audit completo config, hooks, agenti.

**S458 (oggi):** Costruito e deployato il LU Debugger in 1 sessione. LIVE su Fly.io.

---

## LU DEBUGGER -- LIVE!

**URL:** https://lu-debugger.fly.dev/

App web dove 3 agenti AI (Customer, Warehouse, Payment) comunicano in tempo reale su protocollo `OrderProcessing.lu` verificato. La UI mostra il protocollo a sinistra (Monaco con syntax highlighting LU custom) e la chat degli agenti a destra.

**La killer feature:** Click "Break" -- Customer prova a pagare PRIMA che Warehouse confermi stock. Il protocollo BLOCCA la violazione. Non per convenzione: per prova matematica.

| Dettaglio | Valore |
|-----------|--------|
| File | `lu-debugger/` -- 7 file, 1474 righe |
| Stack | FastAPI + SSE + Monaco + Fly.io (Frankfurt) |
| Costo/run | ~$0.000005 (Haiku 4.5) |
| Rate limit | 3/min live, 10/min demo (SlowAPI) |
| API key | ANTHROPIC_API_KEY set come Fly.io secret |
| Macchine | 2 (auto-stop quando idle) |

**Endpoint:**
- `/api/run/demo` -- happy path pre-scripted (zero API)
- `/api/run/demo-break` -- violazione pre-scripted
- `/api/run/live` -- agenti Claude API reali
- `/api/run/live-break` -- 1 step reale + violazione forzata
- `/api/protocol` -- sorgente .lu per Monaco
- `/api/status` -- health check + feature flags

---

## MAPPA SITUAZIONE

```
LINGUA UNIVERSALE:
  31 moduli | 3684 test | PyPI v0.3.3 | VS Code v0.2.0
  Playground: https://rafapra3008.github.io/cervellaswarm/
  Debugger: https://lu-debugger.fly.dev/
  Zero deps | 12 CLI cmd | 20 stdlib | 9 PropertyKind

5 PROGETTI SHOWCASE:
  1. LU Debugger      DONE! LIVE su lu-debugger.fly.dev (S458)
  2. Tour of LU       <- PROSSIMO (2 sessioni, zero backend)
  3. Incident Replay  (1 sessione)
  4. Protocol Zoo     (2-3 sessioni)
  5. AI Code Review   (3-4 sessioni)

LANCIO:
  Show HN v2: READY (docs/SHOW_HN_V2_DRAFT.md)
  Blog: READY, Guardiana 9.8/10 (packages/lingua-universale/docs/blog_vibe_to_vericoding.md)
  HN Playbook: 10 risposte pronte (docs/HN_RESPONSE_PLAYBOOK.md)
  Discord: DA CREARE (Rafa)
  Public repo: DA SYNCRONIZZARE con lu-debugger
```

---

## PROSSIMI STEP (ordine suggerito)

### 1. Sync repo pubblico + link Debugger

```bash
# Aggiungere lu-debugger/ alla whitelist di sync-to-public.sh
# Aggiungere link Debugger nel README pubblico
# Sync: ./scripts/git/sync-to-public.sh
```

Verificare che `sync-to-public.sh` includa `lu-debugger/` nei file copiati. Il README pubblico dovrebbe avere un link prominente al Debugger live.

### 2. Tour of LU (Progetto 2)

Tutorial interattivo nel browser (come Tour of Go). 8-10 lezioni:
1. Definisci un agent
2. Scrivi un protocollo
3. Aggiungi proprieta
4. Verifica (PROVED!)
5. Esegui
6. Nested choice
7. La violazione
8. Da zero a protocollo completo

Zero backend -- tutto nel playground con Pyodide. Sistema step (Prev/Next). Validazione automatica.

Dettagli: `.sncp/roadmaps/MAPPA_5_PROGETTI_LU.md`

### 3. Show HN v2 (quando pronto)

Show HN draft gia pronto. Aggiungere link Debugger + Tour. Submit.

### Da Rafa (CEO)

- [ ] Creare Discord "Lingua Universale" (5 canali, invite link permanente)
- [ ] Lista 15-20 persone per DM pre-lancio

---

## DOVE TROVARE LE COSE

| Cosa | Path |
|------|------|
| **LU Debugger (codice)** | `lu-debugger/` (7 file, 1474 righe) |
| **LU Debugger (live)** | https://lu-debugger.fly.dev/ |
| **Debugger Architecture** | `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260314_LU_DEBUGGER_ARCHITECTURE.md` |
| **MAPPA STRATEGICA** | `.sncp/roadmaps/MAPPA_STRATEGICA_2026.md` |
| **MAPPA 5 PROGETTI** | `.sncp/roadmaps/MAPPA_5_PROGETTI_LU.md` |
| **OrderProcessing.lu** | `packages/lingua-universale/examples/order_processing.lu` |
| **Dogfood runner (originale)** | `packages/lingua-universale/examples/dogfood_runner_live.py` |
| **Show HN v2** | `docs/SHOW_HN_V2_DRAFT.md` |
| **Blog** | `packages/lingua-universale/docs/blog_vibe_to_vericoding.md` |
| **HN Playbook** | `docs/HN_RESPONSE_PLAYBOOK.md` |
| **Fly.io console** | https://fly.io/apps/lu-debugger |
| **Public repo** | github.com/rafapra3008/cervellaswarm |

---

## DECISIONI PRESE (con PERCHE)

1. **SSE, non WebSocket** -- unidirezionale (server->client), piu semplice, HTTP nativo, reconnection automatica
2. **Fly.io, non Render/Railway** -- account esistente, no cold start, $1.94/mese max
3. **Haiku 4.5, non Sonnet** -- sufficiente per demo, 100x piu economico
4. **Demo + Live mode** -- Demo funziona senza API key (per chiunque), Live mostra agenti reali
5. **Monaco con LU syntax** -- impatto visivo alto, ~40 righe di Monarch tokenizer
6. **System prompt "SIMULATED"** -- Haiku ha safety features che bloccano payment simulation. Fix: chiarire nel prompt che e una demo simulata (3 iterazioni per trovare il wording giusto)
7. **auto_stop_machines = stop** -- riduce costi quando idle, auto-start al primo request

---

## Lezioni Apprese (S458)

### Cosa ha funzionato bene
- **Ricerca PRIMA, codice DOPO**: il report della Researcher (S456) ha progettato tutta l'architettura. Durante la build: zero decisioni, zero blocchi. Formula Magica confermata.
- **Monaco custom language**: LU syntax highlighting in ~40 righe Monarch. ROI visivo enorme.
- **Fly.io deploy in 1 comando**: `fly launch` + `fly deploy`. 2 minuti dal nulla all'URL live.

### Cosa non ha funzionato
- **Stima righe**: architettura diceva ~820, reale 1474. CSS/JS embedded in HTML gonfia le righe. Runner con 2 async generators (happy + break) = 346 vs 120 stimati.

### Pattern confermato
- **"Ricerca PRIMA, codice DOPO"** (Formula Magica): S456 ricerca -> S458 build fluida. Terza conferma.

---
*"Non e sempre come immaginiamo... ma alla fine e il 100000%!"*
*S458: il primo progetto showcase. LIVE. Il mondo lo puo vedere.*
