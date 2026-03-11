# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 2026-03-11 - Sessione 440
> **STATUS:** FASE E in progress. E.1 DONE, E.2 IntentBridge Core DONE! Pronta per E.3 NL Processing.

---

## SESSIONE 440 - E.2 Chiusura + Diamante

### Cosa e successo
E.2 completato! 3 protocolli e2e testati, output narrativo in 3 lingue, tutti P3 fixati.

### Cambiamenti chiave
- **3 protocolli e2e diversi**: RecipeExchange (EN, 2 ruoli lineare), TaskDelegation (IT, 3 ruoli 4 messaggi), DataPipeline (PT, 3 ruoli con branching)
- **Output narrativo**: `_SIM_NARRATIVES` 14 MessageKind x 3 lingue. Simulazione mostra frasi naturali ("Cook asks Pantry to do a task") invece del vecchio formato tecnico
- **F5 fix (P3 S438)**: simulazione mostra TUTTI i branch, non solo il primo
- **F11 fix (P3 S438)**: enum test tautologici rimossi, sostituiti con 5 test significativi
- **4 P3 Guardiana S440 fixati**: F2 DRY sim_step, F3 CONTEXT_INJECT aggiunto, F4 accenti PT normalizzati, F5 success localizzato IT/PT
- **Guardiana S440**: 9.5/10 APPROVED (target raggiunto!)

### File modificati
- `_intent_bridge.py` (1178 LOC, era 1110): +_SIM_NARRATIVES, _step_narrative(), _render_simulation rewrite
- `test_intent_bridge_session_e2e.py` (+383 righe): 3 classi protocollo + NarrativeOutputQuality
- `test_intent_bridge_core.py`: F11 fix + narrative coverage tests
- MAPPA, SUBROADMAP, rules: conteggi aggiornati

---

## MAPPA SITUAZIONE

```
LINGUAGGIO CERVELLASWARM:
  FASE A-D: COMPLETE (A+B+C+D, 25 moduli base, media 9.5/10)
  FASE E: PER TUTTI -- IN PROGRESS
    E.1 Script "La Nonna"           DONE (S438)
    E.2 IntentBridge Core           DONE! (S438-S440, 9.5/10)
    E.3 NL Processing               TODO <-- PROSSIMO
    E.4 Voice Interface              TODO
    E.5 La Nonna Demo               TODO
    E.6 CervellaLang 1.0            TODO
  PyPI: v0.3.0 (waiting Rafa environment approval)
```

---

## PROSSIMA SESSIONE

### E.3 NL Processing (LLM Integration)
1. anthropic come optional dependency (`pip install cervellaswarm-lingua-universale[nl]`)
2. LLM (Claude) traduce NL libero -> B.4 micro-linguaggio strutturato
3. Pattern two-stage validato: LLM -> IntentDraft -> deterministico (88% vs 43%)
4. NLProcessor(Protocol) gia definito come extension point in _intent_bridge.py
5. `lu chat --mode nl` per free-text mode
6. Fallback a guided mode se LLM non disponibile
7. Ricerca: studiare come i big fanno NL -> structured (Req2LTL, Rasa, etc.)
8. Subroadmap: `.sncp/roadmaps/SUBROADMAP_FASE_E_INTENTBRIDGE.md`

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
| Test LU | **3111** |
| Test totali (13 pkg) | **~5423** |
| Moduli LU | **26** |
| Audit Guardiana S440 | **9.5/10** |
| PyPI | **v0.3.0** (waiting approval) |
| IntentBridge test | **202** (55 core + 47 session + 100 e2e) |

---

## Lezioni Apprese (S440)

### Cosa ha funzionato bene
- **Guardiana dopo ogni step** -- audit immediato ha trovato 5 finding, tutti fixati nella stessa sessione
- **P3 = diamante** -- fixare anche i P3 porta da 9.3 a 9.5 (Rafa aveva ragione: "ci piace fissare tutto")
- **Test coverage driven** -- il test `cover_all_reachable_kinds` ha trovato CONTEXT_INJECT mancante

### Cosa non ha funzionato
- **Count mismatch** -- ho detto 201 test ma erano 196 dopo F11 fix. Verificare sempre i numeri dopo ogni modifica

### Pattern confermato
- **"Guardiana dopo ogni step"** -- Evidenza: S438 (9.3/10), S440 (9.5/10). Audit immediato = fix immediato

---

*"Ultrapassar os proprios limites!" - Rafa & Cervella*
