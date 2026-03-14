# MAPPA 5 PROGETTI -- Showcase Lingua Universale

> **Data:** 14 Marzo 2026
> **Obiettivo:** Costruire 5 progetti REALI con LU prima del lancio al mondo.
> **Regola:** Uno alla volta. Finisci. Audit. Prossimo.

---

## PROGETTO 1: LU Debugger (PROSSIMO)

**Cosa:** App web dove 3 agenti AI comunicano in tempo reale. Bottone "Break" mostra la violazione bloccata.

**Scenario:** OrderProcessing -- Customer, Warehouse, Payment. Il protocollo impedisce a Payment di processare prima che Warehouse confermi.

**Architettura** (report: `RESEARCH_20260314_LU_DEBUGGER_ARCHITECTURE.md`):
- Frontend: HTML statico (Monaco + chat log + toolbar)
- Backend: FastAPI + SSE (Server-Sent Events)
- Hosting: Fly.io ($1.94/mese, no cold start)
- Costo: ~$0.000005 per run (Haiku 4.5)
- Demo mode: mock responses (zero API) + Live mode: Claude API reale
- Rate limit: 3 run/min per IP (SlowAPI)

**File gia pronti:**
- `examples/order_processing.lu` -- 4/4 PROVED
- `examples/dogfood_runner_live.py` -- runner con agenti reali

**Da costruire:**
```
lu-debugger/
├── server.py          ~180 righe  (FastAPI, SSE, rate limit)
├── runner.py          ~120 righe  (async adapter del dogfood runner)
├── demo_data.py       ~80 righe   (script pre-registrati)
├── requirements.txt   ~6 righe
├── Dockerfile         ~15 righe
├── fly.toml           ~20 righe
└── static/
    └── debugger.html  ~400 righe  (Monaco + chat + violation display)
```

**Effort:** 1.5-2 sessioni
**Output:** URL live (lu-debugger.fly.dev)

---

## PROGETTO 2: Tour of LU

**Cosa:** Tutorial interattivo nel browser (come Tour of Go). 8-10 lezioni progressive.

**Struttura:**
1. Definisci un agent
2. Scrivi un protocollo
3. Aggiungi proprieta
4. Verifica (PROVED!)
5. Esegui
6. Nested choice
7. La violazione
8. Da zero a protocollo completo

**Da costruire:**
- 8-10 lezioni (testo + .lu iniziale + soluzione)
- Sistema step nel playground (Prev/Next, stato)
- Validazione automatica

**Effort:** 2 sessioni
**Output:** Pagina nel playground (zero backend)

---

## PROGETTO 3: Incident Replay

**Cosa:** Storia interattiva: "Un bug AI e costato $34K. Ecco come LU lo avrebbe fermato."

**Da costruire:**
- Narrativa credibile (e-commerce, rimborsi duplicati)
- Animazione step-by-step del bug
- Replay "con LU" -- violazione bloccata
- Landing page standalone

**Effort:** 1 sessione
**Output:** Pagina statica (zero backend)

---

## PROGETTO 4: Protocol Zoo

**Cosa:** Libreria di 15 protocolli reali eseguibili (e-commerce, code review, RAG, triage, support).

**Da costruire:**
- 15 protocolli .lu ben documentati (stdlib ne ha 20, base pronta)
- Pagine per ogni protocollo (template generabile)
- Animazione flow (SVG/CSS)
- Bottone "Fork in Playground"

**Effort:** 2-3 sessioni
**Output:** Sito statico (GitHub Pages)

---

## PROGETTO 5: AI Code Review System

**Cosa:** Incolla codice, 4 agenti AI lo analizzano con protocollo verificato.

**Da costruire:**
- 4 agenti (Orchestrator, Security, Performance, Quality)
- Protocollo code_review.lu
- Server FastAPI + streaming SSE
- UI curata (non playground, app vera)

**Effort:** 3-4 sessioni
**Output:** App web live

---

## ORDINE E DIPENDENZE

```
[1] LU Debugger  ────> [2] Tour of LU  ────> [3] Incident Replay
                                                      |
                                               [4] Protocol Zoo
                                                      |
                                               [5] AI Code Review
```

Ogni progetto completato = materiale per il lancio. Non aspettiamo tutti e 5.

---

*"Un passo alla volta. Fatto bene > fatto veloce."*
