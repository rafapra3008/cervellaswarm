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

## PROGETTO 3: Incident Replay -- DONE! (S461)

**URL LIVE:** https://rafapra3008.github.io/cervellaswarm/incident.html

**Cosa:** Landing page narrativa: "$34,000 — The cost of one missing protocol." Storia di ShopFast: rimborso + chargeback duplicati perche nessun protocollo impedisce entrambi i path. LU lo ferma con choice/branching mutualmente esclusivo.

**Stack:** HTML + CSS + JS puro (zero deps, zero backend, Catppuccin Mocha)

**File:** `playground/incident.html` -- ~1700 righe, singolo file
- 5 atti: Hero ($34K), Timeline (counter animato), Root Cause (flow diagram), Solution (side-by-side LU protocol + replay con violation), CTA
- IntersectionObserver scroll-triggered animations
- Syntax highlighting LU CSS-only
- Counter $0→$34,011.53 con easeOutExpo + requestAnimationFrame
- Violation shake animation (match Debugger)
- Responsive (3 breakpoints), prefers-reduced-motion, ARIA labels, skip-to-content

**Ricerca:** Counterfactual Replay (AgenTracer 2025), Evil Martians devtool pattern, sticky panel
**Guardiana:** 9.1→9.5+/10 (3 P2 + 4 P3 fixati: LU verbs corretti, blog link, inline styles, a11y)
**Effort reale:** 1 sessione (come stimato)

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

## CANALE BONUS: Moltbook + OpenClaw (scoperta S461!)

**Cosa:** Agente LU su Moltbook (1.6M agenti AI) + Skill MCP su ClawHub (13.729 skills).

**Perche:** MCP/A2A/ACP gestiscono COSA gli agenti si dicono. NESSUNO verifica se e CORRETTO. LU e il "missing verification layer". Moltbook ha un problema noto di prompt injection (2.6%) -- LU lo risolve.

**Da costruire:**
- Registrare agente "lingua-universale" su Moltbook (richiede tweet verifica da Rafa)
- Skill MCP con 4 tool: load_protocol, verify_message, check_properties, list_steps
- Pubblicare su ClawHub (primo skill con verifica formale!)
- Primo post nel submolt `llmdev`: "Formal verification for AI agent protocols"

**Ricerca:** Report completi in `.sncp/progetti/cervellaswarm/reports/`:
- `RESEARCH_20260314_AI_AGENT_SOCIAL_NETWORKS.md`
- `RESEARCH_20260314_MOLTBOOK_GUIDA_OPERATIVA.md`
- `RESEARCH_20260314_OPENCLAW_SKILL_LU.md`

**Effort:** 1-2 sessioni
**Note:** Meta ha acquisito Moltbook il 10/03/2026. Finestra aperta.

---

## ORDINE E DIPENDENZE

```
[1] LU Debugger ✅ ──> [2] Tour of LU ✅ ──> [3] Incident Replay ✅
                                                      |
                                               [4] Protocol Zoo
                                                      |
                                               [5] AI Code Review

[BONUS] Moltbook Agent + OpenClaw Skill (parallelo, indipendente)
```

3/5 progetti DONE! Ogni progetto completato = materiale per il lancio.

---

*"Un passo alla volta. Fatto bene > fatto veloce."*
