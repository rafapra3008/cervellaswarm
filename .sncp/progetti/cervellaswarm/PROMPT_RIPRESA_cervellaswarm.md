# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-03-14 - Sessione 455
> **STATUS:** S455 COMPLETA. Playground Chat LIVE! Live dogfood runner PRONTO. Show HN READY 18 Marzo. **3684 test.** PyPI v0.3.3. VS Code v0.2.0 LIVE.

---

## S455 -- COSA ABBIAMO FATTO (3 blocchi)

### Blocco 1: Show HN v2 + Blog (Punto 1)

Audit completo (Guardiana 9.2+) di entrambi i draft per il lancio su HN.

**5 fix applicati:**
1. Titolo HN: 113→73 caratteri (sotto limite 80)
2. Conteggio moduli: 29→31 (aggiunta _lint.py e _fmt.py)
3. LSP features: 6→5 (conteggio accurato)
4. Honda et al. (1998) → Honda/Yoshida/Carbone (POPL 2008) nel blog
5. Prefissi interni B.4/B.5 rimossi dal blog

**Status: READY per lancio mercoledi 18 Marzo, 18:00 CET (9 AM Pacific)**

### Blocco 2: Playground Chat Tab (Punto 2, T2.3)

Chat tab nel playground -- costruisci protocolli conversando nel browser.

- **1 solo file modificato**: `playground/index.html` (+370 righe)
- **Architettura**: Sync bridge via `process_input()` -- zero modifiche al package Python
- **Flusso**: Tab Chat → lingua (EN/IT/PT) → Start → domande guidate → protocollo generato → auto-inject in Monaco → Check automatico
- **Guardiana**: 9.2 → fix F1 (JSON.stringify), F2 (ARIA tablist/tab/tabpanel) → 9.5+
- **Testato e2e** nel browser: protocollo GestioneOrdini costruito in italiano
- **Scoperta critica** (Researcher): `ChatSession.__init__` setta `_phase = WELCOME` ma `_handle()` non la gestisce. Fix: `_phase = ChatPhase.ROLES` dopo init (come `run()` linea 738)

### Blocco 3: Live Dogfood Runner (Punto 3)

Runner con agenti AI REALI via Claude API.

- **Nuovo file**: `examples/dogfood_runner_live.py` (319 righe)
- **3 agenti** (supervisor/worker/validator) come Claude API calls
- **Protocollo** definisce struttura, **AI** decide contenuto
- **SessionChecker** valida ogni messaggio a runtime
- **Fallback mock** quando no API key
- **Guardiana**: 9.3 → fix P1 (f-string mancante!), 3 P2, 4 P3 → 9.5+
- **BLOCCO**: serve `ANTHROPIC_API_KEY` per modalita live

---

## DECISIONI PRESE (con PERCHE)

| Decisione | Perche |
|-----------|--------|
| Titolo: "A language for verified AI agent protocols" | 73 char, sotto limite HN 80. I numeri nel primo commento. |
| "We" nel blog | Siamo un team (Rafa + Famiglia). Trasmette convinzione. |
| Lancio mercoledi 18 Marzo 18:00 CET | Picco traffico HN (Wed US morning). Post ha tutta la giornata US. |
| Chat tab sync (no WebWorker) | process_input() < 200ms, no freeze. KISS. |
| JSON.stringify per Python string | Pattern gia usato nel file (execLU, handleLint). Escaping manuale fragile. |
| Verdict parsing con word boundaries | `"PASS" in text.upper()` matcherebbe "COMPASSION". `re.search(r'\bPASS\b')` preciso. |

---

## MAPPA SITUAZIONE

```
LINGUA UNIVERSALE (LA MISSIONE):
  FASE A-D: COMPLETE (31 moduli, media 9.5/10)
  FASE E: PER TUTTI
    E.1-E.5: DONE (9.5/10)
    E.6 CervellaLang 1.0: T3.1-T3.5 ALL DONE
  PyPI v0.3.3 LIVE | VS Code v0.2.0 LIVE | Playground LIVE (+Chat!)
  Moduli: 31 | Test: 3684 | CLI: 12 | Stdlib: 20

DOGFOODING:
  dogfood_agent_orchestration.lu: 8/8 PROVED
  dogfood_runner.py: mock (happy + fail + violation)
  dogfood_runner_live.py: Claude API (serve ANTHROPIC_API_KEY)
  Gap: load_protocol() public API (T4.1)

LAUNCH: READY 18 MARZO
  Show HN v2: READY (Guardiana 9.5+)
  Blog vibe-to-vericoding: READY (Guardiana 9.5+)
  Playground Chat: LIVE (testato e2e)

INFRASTRUTTURA: 1M CONTEXT FREEDOM (S454, 9.5/10)
  18 hooks, 17 agenti v2.1.0, regole "ansia" rimosse

CI/CD: TUTTO GREEN
PUBLIC REPO: sync needed (playground Chat = nuova feature!)
DEPENDABOT: 2 HOLD (stripe #30, express #14)
```

---

## PROSSIMA SESSIONE (S456)

### Priorita 1: Launch Prep

| # | Cosa | Blocco | Effort |
|---|------|--------|--------|
| 1 | **Rafa review Show HN + Blog** | Decisione CEO | 15 min |
| 2 | **Sync public repo** (playground Chat) | sync-to-public.sh | 5 min |
| 3 | **API key setup** per live dogfood | Rafa account Anthropic | 5 min |

### Priorita 2: Launch Day (18 Marzo)

| # | Cosa | Note | Effort |
|---|------|------|--------|
| 4 | **Submit Show HN** | 18:00 CET = 9 AM Pacific | 5 min |
| 5 | **Demo video VHS** (playground Chat + dogfood) | VHS installato, pattern validato | 0.5 sessione |

### Priorita 3: Post-Launch

| # | Cosa | Note | Effort |
|---|------|------|--------|
| 6 | **Public API load_protocol()** | Gap dal dogfooding, serve per T4.1 | 0.5 sessione |
| 7 | **Monitor HN + risposte** | Community engagement | ongoing |

### Backlog

| # | Cosa | Effort |
|---|------|--------|
| 8 | Dependabot (stripe #30, express #14) | 0.5 sessione |
| 9 | Dynamic context discovery (Cursor-style) | Ricerca fatta |
| 10 | Retrieval semantico su SNCP | Lungo termine |

---

## DOVE TROVARE LE COSE

| Cosa | Path |
|------|------|
| **Playground Chat** | `playground/index.html` (Chat tab, ~370 righe aggiunte) |
| **Live dogfood runner** | `packages/lingua-universale/examples/dogfood_runner_live.py` |
| **Mock dogfood runner** | `packages/lingua-universale/examples/dogfood_runner.py` |
| **Dogfood protocollo** | `packages/lingua-universale/examples/dogfood_agent_orchestration.lu` |
| **Show HN v2 draft** | `docs/SHOW_HN_V2_DRAFT.md` (READY) |
| **Blog post** | `packages/lingua-universale/docs/blog_vibe_to_vericoding.md` (READY) |
| **Piano Chat tab** | `.sncp/progetti/cervellaswarm/reports/PLAN_20260314_PLAYGROUND_CHAT_TAB.md` |
| Subroadmap E5+E6+Futuro | `.sncp/roadmaps/SUBROADMAP_E5_E6_FUTURO.md` |

---

## Lezioni Apprese (S455)

### Cosa ha funzionato bene
- **Guardiana su ogni step**: 3 audit (Show HN+Blog, Playground, Runner) hanno trovato 1 P1 + 10 P2. Il diamante brilla perche OGNI dettaglio e controllato.
- **Researcher in background**: Piano Chat completo (778 righe) con scoperta critica (_phase = WELCOME). Ha risparmiato ore di debug.
- **Browser testing end-to-end**: Playwright MCP ha verificato il Chat tab in tempo reale -- dal tab click al protocollo generato.

### Cosa non ha funzionato
- **f-string mancante (P1)**: Stringa multi-riga con implicit concatenation -- facile dimenticare il `f` prefix. La Guardiana l'ha trovato, non io.

### Pattern confermato
- **"Step -> Guardiana -> Fix -> Avanti"**: Ogni blocco di lavoro seguito da audit formale. 3 cicli in questa sessione, tutti con fix significativi. Evidenza: S455 (6a conferma del pattern).

---
*"Ultrapassar os proprios limites!" -- S455, il giorno del lancio.*
