# MAPPA 5 PROGETTI -- Showcase Lingua Universale

> **Data:** 14 Marzo 2026
> **Obiettivo:** Costruire 5 progetti REALI con LU prima del lancio al mondo.
> **Regola:** Uno alla volta. Finisci. Audit. Prossimo.

---

## PROGETTO 1: LU Debugger -- DONE! (S458)

**URL LIVE:** https://lu-debugger.fly.dev/

**Cosa:** App web dove 3 agenti AI (Customer, Warehouse, Payment) comunicano in tempo reale su protocollo OrderProcessing.lu verificato. Bottone "Break" mostra la violazione BLOCCATA.

**Stack:** FastAPI + SSE + Monaco editor + Fly.io (Frankfurt, 2 macchine)

**File:** `lu-debugger/` -- 7 file, 1474 righe
- `server.py` (165) -- FastAPI + SSE + rate limiting (SlowAPI)
- `runner.py` (346) -- async Claude API agents (Haiku 4.5, ~$0.000005/run)
- `demo_data.py` (184) -- protocol source + pre-scripted steps
- `static/index.html` (748) -- Monaco + LU syntax + chat UI + dark theme
- `Dockerfile` + `fly.toml` + `requirements.txt`

**4 endpoint:** `/api/run/demo`, `/api/run/demo-break`, `/api/run/live`, `/api/run/live-break`

**Effort reale:** 1 sessione (architettura pre-progettata da Researcher S456)

---

## PROGETTO 2: Tour of LU -- DONE! (S459)

**URL LIVE:** https://rafapra3008.github.io/cervellaswarm/?tour

**Cosa:** Tutorial interattivo nel browser. 24 step, 4 capitoli, 4 esercizi con soluzioni.

**Capitoli:**
1. Types (7 step) -- variant, record, Confident[T], Optional, exercise
2. Agents (7 step) -- trust tiers, contracts, team building, exercise
3. Protocols (6 step) -- actions, choice/branching, properties, exercise
4. Putting It All Together (4 step) -- check, errors, run, finale

**Scoperta:** Il tour era gia implementato al 90% nel playground (tour.js 413 righe, tour-ui.js 450 righe). S459 ha aggiunto completion tracking ("done" vs "visited") e celebration finale con link a Debugger e PyPI.

**File:** `playground/tour.js`, `playground/tour-ui.js`, `playground/tour.css`
**Guardiana:** 9.5/10. P2 fixato (progress regression), P3 fixati (keyframes, noopener, a11y).
**Effort reale:** ~1 ora (era al 90%, +77 righe di polish)

---

## PROGETTO 3: Incident Replay (PROSSIMO)

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
[1] LU Debugger ✅ ──> [2] Tour of LU ✅ ──> [3] Incident Replay
                                                      |
                                               [4] Protocol Zoo
                                                      |
                                               [5] AI Code Review
```

Ogni progetto completato = materiale per il lancio. Non aspettiamo tutti e 5.

---

*"Un passo alla volta. Fatto bene > fatto veloce."*
