# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-03-06 - Sessione 438
> **STATUS:** FASE E avviata! E.1 DONE, E.2 IntentBridge Core quasi completo. PyPI v0.3.0.

---

## SESSIONE 438 - IntentBridge: "Per Tutti"

### Cosa e successo
FASE E avviata. Script "La Nonna" scritto (E.1 DONE). IntentBridge Core implementato (E.2 quasi DONE).

### Cambiamenti chiave
- **E.1 Script "La Nonna"**: screenplay 5 atti, 23 requisiti (R1-R23), pipeline architetturale
  - File: `.sncp/progetti/cervellaswarm/reports/SCRIPT_LA_NONNA_DEMO.md`
- **E.2 IntentBridge Core** (`_intent_bridge.py`, 1088 righe):
  - ChatSession: state machine con injectable I/O, 10 fasi (WELCOME->DONE)
  - IntentDraft: frozen dataclass IR (two-stage pattern Req2LTL)
  - render_intent_source(): bridge deterministico IntentDraft -> B.4 source
  - Pipeline completa: guided input -> B.4 -> parse_intent -> check_properties -> generate_python -> simulazione
  - i18n: 25+ chiavi x 3 locales (en/it/pt), _ACTION_VERBS (10), _ACTION_MENU localizzato
  - NLProcessor(Protocol): extension point per E.3 LLM
  - CLI: `lu chat --lang it|pt|en` con `--output` per salvare codice
- **Guardiana S438**: 9.3/10 APPROVED, 3 P2 tutti fixati (F1 attrs init, F2 confirm reset, F3 NLProcessor export)
- **MAPPA/SUBROADMAP/NORD aggiornati** per FASE E

### Numeri
- Suite LU: **3062 test** (era 2909, +153 IntentBridge: 56 core + 47 session + 50 e2e)
- Suite completa (13 pkg): ~5374 test
- Guardiana S438: **9.3/10** APPROVED (3 P2 fixati, 8 P3 cosmetici)
- Moduli LU: **26** (era 25, +_intent_bridge.py)

---

## MAPPA SITUAZIONE

```
LINGUAGGIO CERVELLASWARM:
  FASE A-D: COMPLETE (A+B+C+D, 25 moduli base, media 9.5/10)
  FASE E: PER TUTTI -- IN PROGRESS
    E.1 Script "La Nonna"           DONE (S438)
    E.2 IntentBridge Core           QUASI DONE (S438, mancano: 3 protocolli e2e test)
    E.3 NL Processing               TODO
    E.4 Voice Interface              TODO
    E.5 La Nonna Demo               TODO
    E.6 CervellaLang 1.0            TODO
  PyPI: v0.3.0 (waiting Rafa environment approval)
```

---

## PROSSIMA SESSIONE

### E.2 completamento
1. Testare 3 protocolli end-to-end diversi (ricette, task delegation, data pipeline)
2. Migliorare output narrativo in lingua target
3. Guardiana audit finale E.2 -> target 9.5/10

### E.3 NL Processing (se E.2 chiuso)
1. anthropic come optional dependency ([nl] extra)
2. LLM traduce NL libero -> B.4 micro-linguaggio
3. Pattern two-stage: LLM -> IntentDraft -> deterministico

### TODO Rafa
- Approvare PyPI publish environment su GitHub
- Attivare 2FA GitHub (SCADUTO!)

### BACKLOG
- 3 Dependabot PR rimaste (SKIP tier): #19 stripe, #14 express, #11 zod
- VS Code Marketplace (publisher account)
- Refactoring P2 residuo: _lsp.create_server() 136 righe (rimandato)

---

## I NUMERI TOTALI

| Metrica | Valore |
|---------|--------|
| Test LU | **3062** |
| Test totali (13 pkg) | **~5374** |
| Moduli LU | **26** |
| Audit Guardiana S438 | **9.3/10** |
| PyPI | **v0.3.0** (waiting approval) |
| IntentBridge test | **153** (56 core + 47 session + 50 e2e) |

---

## Lezioni Apprese (S438)

### Cosa ha funzionato bene
- **Script PRIMA del codice** -- "La Nonna" ha guidato TUTTE le decisioni (pattern validato)
- **Two-stage (Req2LTL)** -- IntentDraft come IR: guided input -> deterministic output funziona perfettamente
- **Fix proattivi** -- trovati e fixati 2 bug (attrs init, confirm reset) PRIMA della Guardiana

### Cosa non ha funzionato
- **Auto-compact** -- context perso a meta lavoro, ripresa OK ma costo tempo

### Pattern candidato
- **"Script PRIMA, codice DOPO"** -- Evidenza: S438 (script ha estratto 23 requisiti, zero ambiguita)

---

*"Ultrapassar os proprios limites!" - Rafa & Cervella*
