# Engineering Analysis: AI Code Review (Progetto 5)

> **Cervella Ingegnera** -- 2026-03-14
> **Health**: 7.5/10
> **Scope**: `lu-code-review/` -- server.py, runner.py, demo_data.py, static/index.html

---

## 1. Complessita Ciclomatica

### server.py (197 LOC) -- OK, nessun intervento necessario

Funzioni tutte brevi e lineari. La piu complessa e `run_live()` / `run_live_break()` con
un singolo `if not is_live_available()` branch. Nessuna funzione supera CC=3. Ben organizzata.

### runner.py (374 LOC) -- 2 funzioni da monitorare

| Funzione | LOC | CC stimato | Giudizio |
|----------|-----|------------|----------|
| `live_review()` | ~130 | ~6 | **Borderline.** Loop + branching + 3 reviewer + choice. Leggibile ma lunga. |
| `live_break()` | ~70 | ~3 | OK |
| `_extract_findings()` | ~20 | ~3 | OK |
| `_call_agent()` | ~15 | ~2 | OK |

**`live_review()` (L171-297)** e la funzione piu grande: 126 LOC. Contiene il loop dei 3 reviewer
con costruzione SSE event dict inline, API call, finding extraction, e choice branching.
Non e critica ma si avvicina alla soglia dove il refactoring paga (validated pattern S436-S437).

**Raccomandazione**: Estrarre helper `_review_one_agent(client, checker, code, reviewer, step_ask, step_return)`
che gestisce un singolo ciclo ask/return/extract. Ridurrebbe `live_review()` da 126 a ~50 LOC.

### demo_data.py (518 LOC) -- Nessun refactoring possibile

E pura data dichiarativa (3 scenari pre-scripted). 518 LOC sembrano tante ma il contenuto e
corretto: liste di dict con delays e contenuti. Non c'e logica da spezzare.

### index.html (1965 LOC) -- Accettabile per single-file showcase

~990 LOC CSS, ~800 LOC JavaScript, ~175 LOC HTML. Per un showcase monolitico (no build tool)
e accettabile. Il JS e organizzato in sezioni chiare con commenti separatori.
La funzione `appendActivity()` (L1639-1762, ~123 LOC) e la piu grande -- gestisce 6 tipi di
messaggio con rendering HTML inline. Spezzarla in sotto-render aiuterebbe ma per un showcase
il trade-off non vale.

---

## 2. Accoppiamento e Testabilita

### Positivo

- **Separazione server/runner/data**: 3 moduli con responsabilita chiare.
- **Optional imports con HAS_LU/HAS_ANTHROPIC**: Graceful degradation, testabile.
- **`_sse_event()` pura**: Nessun side effect, facilmente testabile.
- **`_extract_findings()` pura**: Regex + data, zero dipendenze esterne.
- **`_build_checker()` isolata**: Parsing LU incapsulato in un unico punto.

### Problemi

1. **`_sse_event()` duplicata tra server.py e runner.py**
   - `server.py` importa `_sse_event` da runner.py (L37) -- OK
   - Ma `lu-debugger/server.py` ha la SUA versione (L83-84) -- **duplicazione cross-progetto**
   - In lu-code-review la funzione e solo in runner.py -- qui e RISOLTO

2. **Nessun test**
   - Zero file di test. `_extract_findings()`, `_sanitize_code()`, `_sse_event()` sono
     funzioni pure perfettamente testabili.
   - `_build_checker()` testabile con protocollo inline.
   - I demo data (dict) sono validabili con schema check.

3. **`anthropic.Anthropic()` creato dentro la funzione**
   - `live_review()` e `live_break()` creano `client = anthropic.Anthropic()` inline (L178, L312)
   - Non iniettabile per testing. Minimo: accettare client come parametro opzionale.

4. **`PROTOCOL_SOURCE` duplicata**
   - Esiste come stringa in `demo_data.py` (518 LOC) E come file `protocol.lu` (91 LOC)
   - Fonte di verita: quale? Se si modifica il file .lu, `demo_data.py` non si aggiorna.
   - **Raccomandazione**: Caricare `protocol.lu` a runtime e eliminare la stringa duplicata.
   - lu-debugger ha lo STESSO problema (protocollo solo in demo_data.py, niente .lu file).

---

## 3. Pattern Architetturali FastAPI + SSE

### Ben fatto

- **Rate limiting con slowapi**: `10/min` per demo, `3/min` per live. Corretto.
- **Pydantic `CodeRequest`** con `max_length=5000`: Input validation al livello giusto.
- **SSE headers**: `Cache-Control: no-cache` + `X-Accel-Buffering: no`. Standard.
- **`asyncio.to_thread()`** per chiamate API sync: Pattern corretto per non bloccare l'event loop.
- **StreamingResponse** con async generator: Pattern FastAPI idiomatico.

### Miglioramenti

1. **Nessun CORS middleware**
   - Se servito da Fly.io su dominio diverso dal frontend, CORS blocchera le richieste.
   - lu-debugger ha lo STESSO problema. Entrambi funzionano perche servono HTML + API dallo
     stesso origin. Ma se si volesse integrare la UI altrove, servira.

2. **Nessun health check `/health` per Fly.io**
   - C'e `/api/status` ma fly.toml non configura `health_check`.
   - lu-debugger: stesso. Fly.io usa TCP check di default, funziona ma non e best practice.

3. **SSE: niente retry/id**
   - Gli eventi SSE non hanno `id:` field. Se il client si disconnette e riconnette,
     ricomincia da zero. Accettabile per demo, ma manca `retry:` header.
   - Pattern: `id: {step}\ndata: {json}\n\n`

4. **Nessun timeout globale sui live endpoint**
   - Se Claude API e lenta, il client aspetta indefinitamente.
   - Il timeout di 30s e sulla singola `_call_agent()` ma 3 agent = potenziale 90s+.
   - Manca un watchdog/timeout a livello di StreamingResponse.

5. **EventSource per POST non funziona nativamente**
   - I demo endpoint (GET) usano `EventSource` nel browser. OK.
   - I live endpoint (POST) usano `fetch` + `ReadableStream` nel frontend. Funziona ma e
     un'implementazione custom meno robusta di `EventSource` (niente auto-reconnect).
   - Questo e un compromesso ragionevole: POST necessario per inviare codice.

---

## 4. Confronto con LU Debugger

### Architettura identica (buona coerenza)

| Aspetto | lu-debugger | lu-code-review | Coerenza |
|---------|-------------|----------------|----------|
| server.py pattern | FastAPI + SSE + slowapi | Identico | OK |
| runner.py pattern | Claude API + SessionChecker | Identico + findings | OK |
| demo_data.py | PROTOCOL_SOURCE + LINE + scenarios | Identico pattern | OK |
| Optional imports | try/except HAS_LU/HAS_ANTHROPIC | Identico | OK |
| Dockerfile base | python:3.12-slim | **python:3.13-slim** | INCONSISTENTE |
| Dockerfile EXPOSE | `EXPOSE 8000` | **Manca** | INCONSISTENTE |
| `_sse_event()` location | In server.py (duplicata) | Solo in runner.py (importata) | **code-review e MEGLIO** |
| SSE headers | Inline ogni endpoint | Costante `SSE_HEADERS` | **code-review e MEGLIO** |
| StaticFiles import | Importato ma non usato | Non importato | **code-review e MEGLIO** |

### Evoluzioni positive in code-review rispetto a debugger

1. **SSE_HEADERS costante** (L106) -- elimina duplicazione inline. Debugger ripete il dict 4 volte.
2. **`_sse_event()` solo in runner.py** -- debugger ha la funzione in entrambi i file.
3. **`_extract_findings()` con regex** -- nuovo, non necessario in debugger (nessun finding).
4. **`CodeRequest` Pydantic model** -- validation strutturata. Debugger non accetta input utente.
5. **`_sanitize_code()`** -- security layer aggiuntivo per user input.
6. **SAMPLE_CLEAN / SAMPLE_VULNERABLE** con endpoint `/api/samples` -- miglior UX.
7. **`StaticFiles` non importato inutilmente** -- debugger importa `StaticFiles` senza usarlo.

### Regressioni / inconsistenze

1. **Dockerfile Python version**: 3.12 (debugger) vs 3.13 (code-review). Allineare a 3.13.
2. **Dockerfile EXPOSE mancante**: code-review non dichiara EXPOSE 8000.
3. **Nessun `fly.toml` health check** in entrambi.

---

## 5. Miglioramenti Concreti (prioritizzati)

### P1 -- Quick Wins (< 30 min ciascuno)

| # | Cosa | Perche | Effort |
|---|------|--------|--------|
| 1 | **Aggiungere `EXPOSE 8000`** al Dockerfile | Coerenza con debugger, best practice Docker | 1 min |
| 2 | **Allineare Dockerfile debugger a 3.13** | Consistenza versione Python | 1 min |
| 3 | **Eliminare `PROTOCOL_SOURCE` duplicata** | Caricare da `protocol.lu` a runtime | 10 min |
| 4 | **Aggiungere test per funzioni pure** | `_sse_event`, `_extract_findings`, `_sanitize_code` | 20 min |

### P2 -- Solidita (pre-deploy)

| # | Cosa | Perche | Effort |
|---|------|--------|--------|
| 5 | **Estrarre `_review_one_agent()` da `live_review()`** | CC e LOC sotto soglia | 30 min |
| 6 | **Client inject in live_review/live_break** | Testabilita senza mock globale | 15 min |
| 7 | **Aggiungere timeout watchdog** sui live endpoint | Evitare hang su Claude API lenta | 20 min |
| 8 | **CORS middleware** (opzionale, configurabile) | Preparazione per integrazione esterna | 10 min |

### P3 -- Nice to Have (post-deploy)

| # | Cosa | Perche | Effort |
|---|------|--------|--------|
| 9 | **SSE event ID** per idempotency | Resilienza su disconnect/reconnect | 15 min |
| 10 | **Health check in fly.toml** | Monitoraggio Fly.io migliorato | 5 min |
| 11 | **Backport SSE_HEADERS costante al debugger** | Coerenza cross-progetto | 5 min |
| 12 | **Rimuovere `StaticFiles` import nel debugger** | Dead import | 1 min |

---

## Verdetto Complessivo

**Health: 7.5/10** -- Codice ben strutturato, pattern FastAPI idiomatici, buona evoluzione
rispetto al debugger. I problemi principali sono:
- Assenza totale di test (abbassa il voto di 1.5 punti)
- `PROTOCOL_SOURCE` duplicata (file .lu ignorato a runtime)
- `live_review()` un po' lunga ma non critica

Il progetto e in forma per un deploy showcase. I P1 si risolvono in meno di un'ora.
I P2 sono raccomandati prima di un deploy "serio" con traffico reale.

---

*COSTITUZIONE-APPLIED: SI | Principio: "Fatto BENE > Fatto VELOCE"*
*"Analizza prima, proponi poi."*
