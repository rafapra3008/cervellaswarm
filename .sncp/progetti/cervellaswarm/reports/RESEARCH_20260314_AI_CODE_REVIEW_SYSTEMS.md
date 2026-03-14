# AI Code Review Systems - Ricerca
**Data:** 2026-03-14
**Status:** COMPLETA
**Fonti:** 22 consultate
**Agente:** Cervella Researcher

---

## 1. Landscape: Existing AI Code Review Tools

### Il mercato nel marzo 2026

Il 9 marzo 2026, **Anthropic ha lanciato Code Review per Claude Code** -- un sistema multi-agent per PR review. Questo e il segnale piu chiaro possibile che il mercato e maturo e che la nostra direzione e quella giusta.

| Tool | Approccio | UX Pattern | Unique |
|------|-----------|------------|--------|
| **CodeRabbit** | PR-level inline + summaries | Inline comments + "Fix with AI" 1-click | Code graph analysis + LanceDB semantic search |
| **Greptile** | Repo-wide context (intero codebase indicizzato) | Inline comments contestuali al repo | Capisce dipendenze cross-file |
| **Qodo** (ex-CodiumAI) | IDE + PR + post-merge continuum | 15+ agenti specializzati, comandi `/compliance` `/improve` | Gartner Visionary 2025, 73.8% acceptance rate |
| **diffray** | 10 agenti paralleli specializzati | Findings deduplicati, confidence score | 87% meno falsi positivi, 3x piu bug reali |
| **Sourcery** | PR + IDE (GitHub Marketplace) | GitHub-native inline | Cross-PR/IDE seamless |
| **Anthropic Claude Code Review** | Multi-agent paralleli + verifica | Inline PR comments ranked by severity | **Verification step** che disprova findings prima di pubblicarli |

### Metriche reali da Anthropic (lancio 9/3/2026)
- 54% delle PR ricevono commenti sostanziali (era 16% prima)
- < 1% falsi positivi (engineers umani marcano come incorrect)
- 84% delle PR grandi ottengono findings
- Costo stimato: $15-25 per review (token-based)

### Fonte: [Anthropic Code Review launch - TechCrunch](https://techcrunch.com/2026/03/09/anthropic-launches-code-review-tool-to-check-flood-of-ai-generated-code/)

---

## 2. Multi-Agent Code Review: Pattern Architetturali

### Il pattern industriale 2026 (consensus)

1. **Orchestrator** coordina agenti specializzati
2. **Agenti paralleli** lavorano in silenzio sul loro dominio
3. **Verification agent** (o step interno) -- CRITICO: tenta di DISPROVA ogni finding prima di pubblicarlo
4. **Aggregator** deduplica, ranka per severity, pubblica

Questo e esattamente il nostro design (Orchestrator + Security + Performance + Quality). Stiamo costruendo la versione giusta.

### I 10 agenti di diffray (riferimento)
Security Expert | Performance Specialist | Bug Hunter | Quality Guardian | Architecture Advisor | Consistency Checker | Documentation Reviewer | Test Analyst | General Reviewer | SEO Expert

Fonte: [diffray Meet the Agents](https://diffray.ai/blog/meet-the-agents/)

### Il nostro vantaggio: NOI verifichiamo il PROTOCOLLO, non i finding

Anthropic verifica "questo finding e vero?". Noi verifichiamo "gli agenti hanno rispettato il protocollo durante la review stessa?". Sono cose diversissime.

### I 5 pattern del futuro (Qodo predictions 2026)

1. **Context-First Review** -- assemblare artefatti prima di analizzare
2. **Severity-Driven** -- Action Required / Recommended / Minor (non tutto uguale)
3. **Specialist-Agent** -- coordinator + specialisti per dominio
4. **Attribution-Based** -- traccia se ogni suggestion viene accepted/dismissed
5. **Flow-to-Fix** -- i findings diventano metadata machine-readable

**Il nostro P5 implementa 1, 2, 3. Possiamo mostrarlo esplicitamente.**

Fonte: [Qodo 5 AI Code Review Pattern Predictions 2026](https://www.qodo.ai/blog/5-ai-code-review-pattern-predictions-in-2026/)

---

## 3. SSE Streaming per Code Analysis: Best Practices

### Architettura consigliata

Identica a quella del LU Debugger (gia validata). Il pattern centrale:

```python
# FastAPI + sse-starlette
from sse_starlette.sse import EventSourceResponse
import asyncio, json

async def review_stream(code: str):
    # 1. Orchestrator kickoff
    yield {"data": json.dumps({"type": "agent_start", "agent": "orchestrator", "msg": "Parsing code..."})}

    # 2. Lancia agenti in parallelo via asyncio.gather
    tasks = [
        asyncio.create_task(security_agent.analyze(code)),
        asyncio.create_task(performance_agent.analyze(code)),
        asyncio.create_task(quality_agent.analyze(code)),
    ]
    # Stream findings as they arrive (asyncio.as_completed)
    for coro in asyncio.as_completed(tasks):
        finding = await coro
        yield {"data": json.dumps({"type": "finding", **finding})}

    yield {"data": json.dumps({"type": "done"})}

@app.post("/api/review")
async def stream_review(request: CodeRequest):
    return EventSourceResponse(review_stream(request.code))
```

### Pattern critici per multi-agent streaming

1. **`asyncio.as_completed()`** -- Stream findings nell'ordine in cui arrivano, non nell'ordine degli agenti. Crea l'effetto "agenti che lavorano in parallelo" visivamente.
2. **Event types strutturati:** `agent_start` | `agent_thinking` | `finding` | `protocol_check` | `summary` | `done` | `error`
3. **Keep-alive ping ogni 15 sec** -- previene che i proxy chiudano la connessione
4. **Header obbligatori:** `Cache-Control: no-cache` + `X-Accel-Buffering: no`
5. **`asyncio.Queue` per multi-client** -- ogni connessione ha la sua coda

### Riferimento tecnico aggiunto: AG-UI Protocol (2026)

[AG-UI](https://docs.ag-ui.com/) e un protocollo open (CopilotKit) che standardizza gli eventi SSE per agent UI. Event types che adottano: `TEXT_MESSAGE_START`, `TEXT_MESSAGE_CONTENT`, `TEXT_MESSAGE_END`, `TOOL_CALL_START`, `TOOL_CALL_END`, `RUN_STARTED`, `RUN_FINISHED`.

**Raccomandazione:** Non serve adottare AG-UI per P5, ma i suoi tipi di evento sono un template eccellente per il nostro formato JSON interno.

Fonti:
- [SSE con FastAPI - DevDojo](https://devdojo.com/post/bobbyiliev/how-to-use-server-sent-events-sse-with-fastapi)
- [sse-starlette PyPI](https://pypi.org/project/sse-starlette/)
- [AG-UI Overview](https://docs.ag-ui.com/)

---

## 4. Code Review UX: Pattern che Funzionano

### Layout pattern vincenti (dal mercato)

#### A) Panel Split (il piu comune, CodeRabbit/Greptile style)
```
+---------------------------+---------------------------+
|  CODE INPUT               |  FINDINGS PANEL           |
|  (editor, paste qui)      |  [Security] [Perf] [Qual] |
|                           |                           |
|  function foo() {         |  CRITICAL                 |
|    // ...                 |  > SQL injection risk      |
|  }                        |    Line 42: raw query      |
|                           |                           |
|                           |  WARNING                  |
|                           |  > O(n²) loop detected    |
|                           |                           |
+---------------------------+---------------------------+
```

#### B) Chat-style / Timeline (diffray / Anthropic Claude Code Review style)
```
[Orchestrator] Starting review...
[Security Agent] Analyzing authentication patterns...
[Security Agent] CRITICAL: No input sanitization on line 42
[Performance Agent] Scanning loop complexity...
[Performance Agent] WARNING: O(n²) in processItems()
[Quality Agent] Checking code structure...
[Protocol: VERIFIED] All agents followed review protocol ✓
[Summary] 1 critical, 2 warnings, 3 suggestions
```

#### C) Timeline + inline (il nostro sweet spot)
- Parte B (timeline/chat live durante la review)
- Poi si condensa in panel sintetico con findings filtrabili per agent/severity
- Click su finding -> highlight riga nel code editor

### Severity Framework (standard de facto)

Tutti i tool big usano questo schema:

| Livello | Colore | Significato | Azione |
|---------|--------|-------------|--------|
| CRITICAL | Rosso | Blocca merge / security hole | Obbligatorio fixare |
| WARNING | Arancione | Performance degradation, logic bug | Fortemente raccomandato |
| INFO | Blu | Style, naming, docs | Facoltativo |
| VERIFIED | Verde | Protocol check passed | (nostro, unico) |

### Evil Martians: 6 principi per developer tool trust (2026)

1. **Speed** -- 100ms per UI feedback, progress indicator per job lenti
2. **Discoverability** -- command palette stile VS Code, progressive disclosure
3. **UI Consistency** -- pattern stabili, keyboard-first
4. **Multitasking** -- profili, workspace, layout configurabili
5. **Resilience** -- preserva stato dopo crash, auditable AI actions
6. **AI Governance** -- opt-in, propose-then-apply, action log, reversibility

**Il #6 e il piu critico per noi:** i developer nel 2026 hanno AI adoption alta ma trust bassa. Vogliono vedere COSA stanno facendo gli agenti, PERCHE hanno flaggato qualcosa, e poterli CONTESTARE.

Il nostro protocol verification risponde esattamente a questo bisogno: "puoi fidarti di questa review perche il protocollo e stato verificato formalmente."

Fonte: [Evil Martians - 6 things devtools must have](https://evilmartians.com/chronicles/six-things-developer-tools-must-have-to-earn-trust-and-adoption)

---

## 5. Cosa Rende il Nostro Approccio UNICO

### Il gap nel mercato (CONFERMATO dalla ricerca)

**Nessun tool verifica il PROTOCOLLO della review stessa.**

| Cosa verificano gli altri | Cosa verifichiamo noi (IN PIU) |
|--------------------------|-------------------------------|
| Il codice utente ha bug? | Gli agenti hanno rispettato il protocollo? |
| Il finding e un falso positivo? | La comunicazione tra agenti e conforme? |
| Il codice e sicuro? | Il review workflow e certificato? |

### Come pitcharlo

**Testo A (tecnico):**
> "Every AI code review tool asks: *is this finding correct?* We ask a different question: *did the review agents follow the verified protocol?* Using session types from multiparty session type theory (Honda et al., POPL 2008), we formally verify that the Orchestrator, Security, Performance, and Quality agents communicated in the correct order, with the correct messages, and without deadlock or message loss. The review is not just accurate — it's *certified*."

**Testo B (developer emotion):**
> "You've seen AI code reviews that confidently flag the wrong thing. We fixed the root cause: we verify the *review process itself*, not just the output. If the agents deviate from the protocol — wrong message order, unexpected recipient, missing step — you see it. Every time."

**Testo C (one-liner per HN / tagline):**
> "4 AI agents review your code. LU verifies the review protocol. The first code review system that's formally verified, from end to end."

### Differenziatori concreti per la UI

1. **PROTOCOL STATUS badge** -- visible, prominente, con VERIFIED / VIOLATION distinguibile
2. **Timeline degli agenti** -- mostra la sequenza ESATTA di messaggi tra agenti (cosa nessuno fa)
3. **Protocol highlight** -- quando un agente comunica con un altro, mostra QUALE riga del .lu viene rispettata
4. **"Why this review is trustworthy"** -- sezione dedicata che spiega il meccanismo a chi non conosce LU

---

## 6. Architettura P5 Raccomandata

### Backend (FastAPI + SSE, Fly.io)

```
POST /api/review
  -> orchestrator.kickoff(code)
  -> asyncio.gather(
       security_agent.analyze(code),
       performance_agent.analyze(code),
       quality_agent.analyze(code),
     )
  -> protocol_checker.verify(conversation_log)
  -> SSE stream: agent_start | thinking | finding | protocol_event | summary | done

GET /api/review/demo
  -> stessi eventi SSE, dati pre-recorded (no API cost)
```

### Frontend (vanilla JS, GitHub Pages)

```
+------------------------------------------+
| [DEMO] [LIVE]  Paste code: [____code____]|
|                              [REVIEW ▶]  |
+----------------------+-------------------+
| AGENT TIMELINE       | FINDINGS PANEL    |
|                      |                   |
| [orch] Parsing...    | Filter: [All▼]    |
| [sec]  Analyzing...  |                   |
| [sec]  CRITICAL:     | CRITICAL (1)      |
|   SQL injection L42  |   > SQL injection |
| [perf] O(n²) L15     |   L42             |
| [qual] Naming L7     |                   |
| [orch] Aggregating.. | WARNING (2)       |
| [proto] VERIFIED ✓   |   > O(n²) L15    |
|                      |   > Naming L7     |
|                      |                   |
|                      | PROTOCOL: ✓ CLEAN |
+----------------------+-------------------+
```

### Event stream format (JSON in SSE data)

```json
{"type": "agent_start", "agent": "security", "ts": 1234}
{"type": "thinking", "agent": "security", "msg": "Scanning SQL patterns..."}
{"type": "finding", "agent": "security", "severity": "CRITICAL",
  "line": 42, "title": "SQL Injection", "body": "...", "suggestion": "..."}
{"type": "protocol_event", "step": 3, "from": "security", "to": "orchestrator",
  "status": "ok", "protocol_line": 12}
{"type": "protocol_summary", "status": "VERIFIED", "steps_checked": 8, "violations": 0}
{"type": "summary", "critical": 1, "warning": 2, "info": 3, "protocol_status": "VERIFIED"}
{"type": "done"}
```

### Costo stimato per review (Claude Haiku)

Ogni agente: ~500 tok input (system + code snippet) + ~300 tok output
4 agenti = 2000 tok input + 1200 tok output
Con Haiku 4.5 ($1/MTok in, $5/MTok out):
- Input: 2000 tok = $0.000002
- Output: 1200 tok = $0.000006
**TOTALE per review: ~$0.000008 (< 1 centesimo di centesimo)**

Rate limit: 5 review/minuto per IP (SlowAPI) sufficiente.

---

## 7. Spunti UX per il "WOW" Moment

### Cosa fa dire "questo e diverso"

1. **Vedere gli agenti comunicare in live** -- non solo il risultato, ma il processo. La timeline che si popola in real-time mentre gli agenti "lavorano" e il momento WOW.

2. **Il PROTOCOL badge che diventa verde** -- dopo che tutti i finding sono arrivati, vedere "PROTOCOL: VERIFIED" lampeggiare verde e un momento catartico. Dimostra che il sistema stesso e corretto.

3. **Protocol violation demo** -- un modalita "Break Protocol" (come nel LU Debugger) dove si mostra cosa succede se un agente non rispetta l'ordine. Questo educa l'utente sul valore UNICO.

4. **Severity filtering real-time** -- mentre arrivano i finding, poterli filtrare senza refresh. Interazione istantanea = tool che "sembra vivo".

5. **"Why should I trust this?" sezione** -- link diretto a LU spec, spiegazione in 2 righe. Trasparenza = trust (Evil Martians #6).

### Pattern da evitare

- **Spinner generico** -- il browser sa che "sta pensando", ma non SA COSA sta pensando. Meglio "Security Agent scanning SQL patterns..." che "Loading..."
- **Flood di commenti uguali** -- tutti i tool ci soffrono. Il nostro dedup nell'orchestrator e il fix.
- **Severity inflation** -- se tutto e CRITICAL niente e CRITICAL. Usare sparingly.
- **Modal/dialog per i finding** -- il panel split e piu efficiente: zero click aggiuntivi.

---

## 8. Riferimenti Chiave

### Tool analizzati
- [CodeRabbit](https://www.coderabbit.ai/) -- PR inline + code graph analysis
- [Greptile](https://www.greptile.com/) -- repo-wide context aware
- [Qodo](https://www.qodo.ai/) -- 15+ agenti, Gartner Visionary
- [diffray](https://diffray.ai/) -- 10 agenti paralleli, 87% meno falsi positivi
- [Anthropic Claude Code Review](https://claude.com/blog/code-review) -- lanciato 9/3/2026, multi-agent con verification step
- [Sourcery](https://sourcery.ai/) -- PR + IDE

### Architettura e UX
- [Evil Martians - 6 devtool principles](https://evilmartians.com/chronicles/six-things-developer-tools-must-have-to-earn-trust-and-adoption)
- [Qodo 5 pattern predictions 2026](https://www.qodo.ai/blog/5-ai-code-review-pattern-predictions-in-2026/)
- [AG-UI Protocol docs](https://docs.ag-ui.com/)
- [sse-starlette PyPI](https://pypi.org/project/sse-starlette/)
- [diffray Multi-Agent How It Works](https://diffray.ai/multi-agent-code-review/)

---

## Sintesi Finale

**5 bullet chiave:**

1. **Il mercato e gia lì** -- Anthropic ha lanciato Claude Code Review il 9/3/2026. Multi-agent e lo standard. Noi arriveremo con il P5 come tutorial interattivo che insegna COME funziona con verifica formale.

2. **Il nostro gap unico** -- Nessuno verifica il protocollo della review. Anthropic verifica i finding dopo. Noi verifichiamo la COMUNICAZIONE tra agenti durante. E la differenza tra "l'output e corretto" e "il processo e certificato".

3. **SSE + asyncio.as_completed** -- La UI piu impressive mostra gli agenti lavorare in parallelo in real-time. `asyncio.as_completed()` e il pattern: stream i finding nell'ordine in cui arrivano, non in ordine predefinito. Crea l'illusione (reale) di parallelismo.

4. **Severity + Protocol badge** -- Lo schema CRITICAL/WARNING/INFO e il minimo. Il nostro differenziatore e il PROTOCOL STATUS (VERIFIED / VIOLATION) che nessuno ha.

5. **Costo irrisorio** -- Review con Haiku ~$0.000008. 1000 demo = $0.008. Rate limit 5/min/IP. Nessun problema economico per lancio.

**Raccomandazione:** Costruire P5 con:
- Backend FastAPI + SSE + asyncio.as_completed (identico a LU Debugger pattern, gia validato)
- UI split: timeline agenti (sinistra) + findings panel filtrabili (destra) + PROTOCOL badge centrale
- Demo Mode (no API cost) + Live Mode (Haiku $0.000008/review)
- "Break Protocol" mode per mostrare il valore unico di LU
- Fly.io deploy (gia account, no cold start)

---

*Cervella Researcher | Progetto: CervellaSwarm | 2026-03-14*

COSTITUZIONE-APPLIED: SI | Principio: "Ricerca PRIMA di implementare"
