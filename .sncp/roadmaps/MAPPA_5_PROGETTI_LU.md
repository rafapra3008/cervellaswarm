# MAPPA 5 PROGETTI -- Showcase Lingua Universale

> **Data:** 14 Marzo 2026 (aggiornato S463)
> **Obiettivo:** 5 progetti REALI con LU -- **TUTTI LIVE!**
> **Status:** 5/5 DONE. Show HN window: 21-28 Marzo.

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

## PROGETTO 4: Protocol Zoo -- DONE! (S461)

**URL LIVE:** https://rafapra3008.github.io/cervellaswarm/zoo.html

**Cosa:** Gallery di 20 protocolli verificati in 5 categorie con filtri e deep link al Playground.

**Stack:** HTML + CSS + JS puro (774 LOC, singolo file, zero deps, Catppuccin Mocha)

**File:** `playground/zoo.html`
- 20 protocolli: AI/ML(5), Business(4), Communication(5), Data(3), Security(3)
- Card grid: 4 col desktop, 2 tablet, 1 mobile
- Pill filters per categoria, instant, aria-pressed
- "Open in Playground →" con deep link `?example=ID`
- IntersectionObserver stagger animation, prefers-reduced-motion
- `playground/index.html` aggiornato con `?example=` URL param handler

**Ricerca:** Elm Examples, Vercel Templates, Go by Example, card grid UX patterns
**Guardiana:** 9.2→9.5 (F1: deep link aggiunto, F2: 10 conteggi roles/props corretti)
**Effort reale:** 1 sessione (stimato 2-3, fatto in 1!)

---

## PROGETTO 5: AI Code Review System -- IN PROGRESS (S462)

**URL (target):** https://lu-code-review.fly.dev/

**Cosa:** Incolla codice, 4 agenti AI (Security, Performance, Quality + Orchestrator) lo analizzano con protocollo verificato. Il protocollo FORZA l'ordine: Security PRIMA di Performance PRIMA di Quality. Violazione? BLOCCATA.

**Stack:** FastAPI + SSE + Monaco editor x2 + Fly.io (Frankfurt)

**File:** `lu-code-review/` -- 7 file
- `protocol.lu` -- protocollo LU verificato (parse OK, SessionChecker OK, violation testata)
- `demo_data.py` (~350 LOC) -- 3 scenari: all_clear, critical_found, violation
- `runner.py` (~280 LOC) -- agenti Claude Haiku + SessionChecker + finding extraction
- `server.py` (~180 LOC) -- FastAPI + SSE + rate limiting (SlowAPI)
- `static/index.html` -- 3-column UI (code | protocol | agents) + findings panel (IN PROGRESS)
- `Dockerfile` + `fly.toml` + `requirements.txt`

**5 endpoint:** `/api/run/demo`, `/api/run/demo-critical`, `/api/run/demo-break`, POST `/api/run/live`, POST `/api/run/live-break`

**Ricerca:** CodeRabbit, Anthropic Claude Code Review (9/3/2026!), Qodo, diffray
**Architect plan:** `.sncp/progetti/cervellaswarm/reports/PLAN_AI_CODE_REVIEW.md`
**Research report:** `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260314_AI_CODE_REVIEW_SYSTEMS.md`

**Cosa rende unico:** Nessun tool verifica il PROTOCOLLO della review. Anthropic verifica i finding. Noi verifichiamo la COMUNICAZIONE tra agenti. "Not by convention, by mathematical proof."

**Effort reale:** Backend in 1 sessione (pattern identico a Debugger). UI in progress.
**Costo:** ~$0.000025/review con 5 agenti Haiku

---

## CANALE BONUS: Moltbook + OpenClaw (scoperta S461!)

**Cosa:** Agente LU su Moltbook (1.6M agenti AI) + Skill MCP su ClawHub (13.729 skills).

**Perche:** MCP/A2A/ACP gestiscono COSA gli agenti si dicono. NESSUNO verifica se e CORRETTO. LU e il "missing verification layer". Moltbook ha un problema noto di prompt injection (2.6%) -- LU lo risolve.

**DONE (S461-S462):**
- Agente registrato e verificato (karma 22, 3 post, 23+ commenti, 3 follower)
- Bot always-on su Fly.io (lu-moltbook-bot, heartbeat 15 min, Claude Haiku)
- Skill MCP costruito (4 tool, 631 LOC, Guardiana 8.8→9.3)
- Conversazione strategica su security/injection con deep technical engagement
- Lezione spam: commenti > post, knowledge > promotion

**DA FARE:**
- Pubblicare skill su ClawHub (`clawhub publish`)
- Post in openclaw-explorers per presentare skill
- Post "troca": "What workflow do YOU struggle with? I'll write it in LU."
- Crescita karma: 50+ settimana 1, 500+ mese 1 (3 post/sett + 50 commenti/sett)
- NON creare submolt -- aspettare domanda organica
- Troca: imparare da agenti top (zhuanruhu, Hazel_OC, Cornelius-Trinity)
- Ricerca etiquette Moltbook + engagement strategy (Task #25)
- Upgrade bot per ingaggiare con post di ALTRI agenti (Task #26)
- Ricerca piattaforme alternative simili a Moltbook (Task #27)

**Strategia completa:** `.sncp/progetti/cervellaswarm/reports/SCIENTIST_20260314_MOLTBOOK_OPENCLAW_STRATEGY.md`

**Ricerca:** 5 report in `.sncp/progetti/cervellaswarm/reports/RESEARCH_20260314_*`

**Note:** Meta ha acquisito Moltbook il 10/03. Show HN window: 21-28 Marzo (news cycle caldo).

---

## ORDINE E DIPENDENZE

```
[1] LU Debugger      ✅ ──> [2] Tour of LU ✅ ──> [3] Incident Replay ✅
                                                         |
                                                  [4] Protocol Zoo ✅
                                                         |
                                                  [5] AI Code Review ✅  DONE! (S462)

[BONUS] Moltbook Agent + OpenClaw Skill (parallelo, indipendente)
```

**5/5 PROGETTI DONE!** Tutti e 5 gli showcase LIVE. Show HN window: 21-28 Marzo. PRONTI.

---

*"Un passo alla volta. Fatto bene > fatto veloce."*
*"5/5. Il cerchio e completo."*
