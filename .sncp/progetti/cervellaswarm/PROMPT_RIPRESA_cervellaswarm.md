# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-03-14 - Sessione 458
> **STATUS:** LU Debugger LIVE! https://lu-debugger.fly.dev/ -- Primo progetto showcase DEPLOYED.

---

## COSA E SUCCESSO (S458) -- IL PRIMO SHOWCASE

### LU Debugger: COSTRUITO

7 file, 1474 righe. App web dove 3 agenti AI (Customer, Warehouse, Payment) comunicano in tempo reale su protocollo verificato. Bottone "Break" mostra la violazione BLOCCATA.

**Testato localmente -- FUNZIONA:**
- Demo mode: pre-scripted, zero API, instant
- Live mode: agenti Claude API reali (Haiku 4.5, ~$0.000005/run)
- Break mode: violazione catturata e mostrata (sia demo che live)
- UI: Monaco editor con syntax highlighting LU custom + chat log + violation display

**File:**
```
lu-debugger/
  server.py      165 righe  (FastAPI + SSE + rate limiting)
  runner.py      346 righe  (async adapter, Claude API agents)
  demo_data.py   184 righe  (protocol source + pre-scripted steps)
  static/
    index.html   748 righe  (Monaco + chat UI + dark theme)
  requirements.txt / Dockerfile / fly.toml
```

**4 endpoint SSE verificati:**
- `/api/run/demo` -- happy path pre-scripted
- `/api/run/demo-break` -- violazione pre-scripted
- `/api/run/live` -- agenti Claude reali, protocollo completato
- `/api/run/live-break` -- 1 step reale + violazione forzata

---

## CONTESTO (S455-S457)

S455-S456: svolta strategica. Identita fixata (LU = prodotto, CervellaSwarm = organizzazione). 5 progetti showcase pianificati. README riscritto. 7 report dalle ragazze.

S457: security fixes, bug hunt, ops cleanup (audit completo config + hooks + agenti).

S458: **costruito il LU Debugger** -- primo progetto showcase.

---

## MAPPA SITUAZIONE

```
LINGUA UNIVERSALE:
  31 moduli | 3684 test | PyPI v0.3.3 | VS Code v0.2.0
  Playground LIVE (+Chat tab!)
  Zero deps | 12 CLI cmd | 20 stdlib | 9 PropertyKind

5 PROGETTI SHOWCASE:
  1. LU Debugger      <- LIVE! lu-debugger.fly.dev
  2. Tour of LU       (2 sessioni)
  3. Incident Replay  (1 sessione)
  4. Protocol Zoo     (2-3 sessioni)
  5. AI Code Review   (3-4 sessioni)

LANCIO:
  Show HN v2: READY ma aspetta deploy Debugger
  Blog: READY (Guardiana 9.8/10)
  HN Playbook: 10 risposte pronte
  Discord: DA CREARE (Rafa)
```

---

## PROSSIMI STEP

### Immediato: Sync public repo + Show HN

| Step | Cosa | Note |
|------|------|------|
| 1 | Sync public repo | `./scripts/git/sync-to-public.sh` |
| 2 | Aggiungere link Debugger nel README | URL live per Show HN |
| 3 | Show HN v2 submit | Blog + Debugger link |

### Progetto 2: Tour of LU

Tutorial interattivo (come Tour of Go). 8-10 lezioni nel playground. Zero backend.

### Serve da Rafa (CEO)

- [x] ~~`fly auth login`~~ DONE (S458)
- [ ] Creare Discord "Lingua Universale"
- [ ] Lista 15-20 persone per DM pre-lancio

---

## DOVE TROVARE LE COSE

| Cosa | Path |
|------|------|
| **LU Debugger** | `lu-debugger/` (7 file, testato) |
| **MAPPA STRATEGICA** | `.sncp/roadmaps/MAPPA_STRATEGICA_2026.md` |
| **MAPPA 5 PROGETTI** | `.sncp/roadmaps/MAPPA_5_PROGETTI_LU.md` |
| **Debugger Architecture** | `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260314_LU_DEBUGGER_ARCHITECTURE.md` |
| **OrderProcessing.lu** | `packages/lingua-universale/examples/order_processing.lu` |
| **Show HN v2** | `docs/SHOW_HN_V2_DRAFT.md` (READY) |
| **Blog** | `packages/lingua-universale/docs/blog_vibe_to_vericoding.md` (READY) |

---

## Lezioni Apprese (S458)

### Cosa ha funzionato bene
- **Architettura pre-progettata**: il report della Researcher (S456) ha dato SSE vs WS, Fly.io, costi, UI pattern. Zero decisioni da prendere durante la build.
- **Prompt tuning per simulazione**: Haiku 4.5 ha safety features che bloccano "process payment". Fix: chiarire "SIMULATED demo" nel system prompt. 3 iterazioni, risolto.
- **Monaco custom language**: syntax highlighting LU con Monarch tokenizer in ~40 righe. Impatto visivo enorme per il costo.

### Cosa non ha funzionato
- **Stima righe sottovalutata**: architettura diceva ~820, reale 1474. HTML con CSS/JS embedded = +350 righe. Runner con 2 generator async = +226 righe. Non un problema, ma calibrare meglio.

### Pattern confermato
- **"Ricerca PRIMA, codice DOPO"** (Formula Magica): la sessione di ricerca S456 ha reso la build S458 fluida. Zero blocchi, zero decisioni architetturali da prendere live.

---
*"Non e sempre come immaginiamo... ma alla fine e il 100000%!"*
*S458: il giorno in cui il primo showcase ha preso vita.*
