# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-03-11 - Sessione 440
> **STATUS:** FASE E in progress. E.1 DONE, E.2 DONE, E.3 NL Processing DONE! Pronta per E.4.

---

## SESSIONE 440 - E.2 Chiusura + E.3 NL Processing COMPLETO

### E.2 (inizio sessione)
E.2 completato: 3 protocolli e2e, narrativa 3 lingue, 202 test, 9.5/10.

### E.3 NL Processing (nuovo!)
**ClaudeNLProcessor** implementato: NL libero -> IntentDraft via Claude tool_use.
- `_nl_processor.py` (~450 LOC): TOOL_SCHEMA, SYSTEM_PROMPT (3 few-shot), _build_draft(), _extract_text_response()
- **Disambiguazione intelligente**: tool_choice "auto", NLClarificationNeeded exception, multi-turn
- **Bug fix critico**: back-to-back user messages (Guardiana F1 P2), fixato con `turns[:-1]`
- CLI: `lu chat --mode nl --lang it|pt|en`
- anthropic optional dep: `pip install cervellaswarm-lingua-universale[nl]`
- 2 audit Guardiana, 13 findings tutti fixati (9.2→9.5/10)
- **68 test** NL in 9 classi (schema, prompt, draft, extract, mock API, session, edge cases, CLI, disambiguation)

### File chiave (E.3)
- `_nl_processor.py` (NUOVO): ClaudeNLProcessor, NLProcessorError, TOOL_SCHEMA, _build_draft, _extract_text_response
- `_intent_bridge.py` (modificato): +NLClarificationNeeded, +ChatPhase.NL_INPUT, +_handle_nl_input
- `_cli.py` (modificato): +--mode guided|nl
- `pyproject.toml`: +[nl] optional dep
- `__init__.py`: +NLClarificationNeeded, ClaudeNLProcessor, NLProcessorError in __all__
- `test_nl_processor.py` (NUOVO): 68 test

---

## MAPPA SITUAZIONE

```
LINGUAGGIO CERVELLASWARM:
  FASE A-D: COMPLETE (A+B+C+D, 25 moduli base, media 9.5/10)
  FASE E: PER TUTTI -- IN PROGRESS
    E.1 Script "La Nonna"           DONE (S438)
    E.2 IntentBridge Core           DONE (S438-S440, 9.5/10)
    E.3 NL Processing               DONE (S440, 9.5/10)
    E.4 Voice Interface              TODO <-- PROSSIMO
    E.5 La Nonna Demo               TODO
    E.6 CervellaLang 1.0            TODO
  PyPI: v0.3.0 (waiting Rafa environment approval)
```

---

## PROSSIMA SESSIONE

### E.4 Voice Interface
1. STT -> NL -> pipeline IntentBridge (E.3 NL mode gia pronta)
2. Claude Code voice mode (nativo) oppure Whisper API
3. Subroadmap: `.sncp/roadmaps/SUBROADMAP_FASE_E_INTENTBRIDGE.md`
4. Ricerca: studiare opzioni STT (Whisper, Claude native, browser API)

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
| Test LU | **3179** |
| Test totali (13 pkg) | **~5491** |
| Moduli LU | **27** (+_nl_processor.py) |
| Audit Guardiana S440 | **9.5/10** (4 audit rounds: E.2 + E.3 x2) |
| PyPI | **v0.3.0** (waiting approval) |
| IntentBridge test | **270** (55 core + 47 session + 100 e2e + 68 NL) |

---

## Lezioni Apprese (S440)

### Cosa ha funzionato bene
- **Guardiana dopo ogni step** -- 4 audit rounds, 18+ findings tutti fixati nella stessa sessione
- **Bug critico trovato da Guardiana** -- back-to-back user messages nell'API (avrebbe causato 400 error in production)
- **Exception nel modulo Protocol** -- NLClarificationNeeded definita in _intent_bridge (contratto), importata in _nl_processor (implementazione)
- **P3 = diamante** -- fixare anche i P3 porta consistentemente da 9.2-9.3 a 9.5

### Cosa non ha funzionato
- **SYSTEM_PROMPT contradiction** -- "Always use tool" + "ask clarification" sono contraddittori. Trovato dalla Guardiana

### Pattern confermato
- **"Guardiana dopo ogni step"** -- Evidenza: S438 (9.3→9.5), S440 E.2 (9.5), S440 E.3 (9.2→9.5). 4 evidence points
- **tool_choice "auto" per disambiguation** -- permette sia structured output che clarification questions

---

*"Ultrapassar os proprios limites!" - Rafa & Cervella*
