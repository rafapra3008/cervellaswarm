# Gap Analysis: Script "La Nonna" vs Implementazione Attuale

> **Autrice:** Cervella Ingegnera - Sessione 442
> **Data:** 12 Marzo 2026
> **Health:** 7/10 (pipeline E.2-E.4 solida, ma gap critici su verifica e nuove proprieta)

---

## Tabella Riassuntiva R1-R23

| Req | Descrizione | Status | Evidenza / Gap |
|-----|-------------|--------|----------------|
| R1 | CLI interattiva `lu chat` con prompt e colori | **DONE** | `_cli.py:258-288` -- subcommand `chat` con `--lang`, `--mode`, `--voice`, `--output` |
| R2 | Flag `--lang` per scegliere lingua (it/pt/en) | **DONE** | `_cli.py:262-267` -- `choices=["en","it","pt"]`, default `"en"` |
| R3 | Traduzione NL italiano -> IntentDraft B.4 | **DONE** | `_nl_processor.py:192-262` (ClaudeNLProcessor) + `_intent_bridge.py:733-767` (NL_INPUT phase) |
| R4 | Domande di chiarimento (disambiguazione) | **DONE** | `_nl_processor.py:294-311` -- `_extract_text_response()` + `NLClarificationNeeded` exception, `tool_choice={"type":"auto"}` |
| R5 | Supporto multi-turno (memoria del dialogo) | **DONE** | `_intent_bridge.py:606,688,744` -- `_turns` list + context passed to `process()` |
| R6 | Rendering protocollo human-readable in italiano | **DONE** | `_intent_bridge.py:1110-1131` -- `_render_confirmation()` con box ASCII e i18n |
| R7 | Spiegazione proprieta in linguaggio naturale | **PARZIALE** | `_intent_bridge.py:1126-1128` mostra lista props, ma NO spiegazione human-readable per prop (lo script dice "Il sistema finisce SEMPRE", "Nessun ruolo resta in attesa", etc.) |
| R8 | Modifica interattiva del protocollo | **PARZIALE** | `_intent_bridge.py:964-991` -- CONFIRM: "no" -> reset TUTTO e ricomincia. Lo script prevede modifica INCREMENTALE (es. aggiungere `role_exclusive` senza rifare tutto) |
| R9 | `parse_intent()` (B.4) | **DONE** | `intent.py` -- funziona, usato in `_execute_pipeline()` linea 1009 |
| R10 | Mapping nuove proprieta (`role_exclusive`) | **DA FARE** | `spec.py:75-84` -- `PropertyKind` ha 7 valori, NESSUNO e `role_exclusive` |
| R11 | `check_properties()` (B.5) | **PARZIALE** | `spec.py:1028-1094` -- funziona MA NON viene chiamato correttamente (vedi BUG sotto) |
| R12 | `generate_lean4()` | **DONE** | `lean4_bridge.py` -- esiste, funziona |
| R13 | Output progressivo verifiche (1/5, 2/5...) | **PARZIALE** | `_intent_bridge.py:1133-1177` -- template `verify_progress` esiste, MA `_render_verification` crasha perche accede a `result.property_name` che NON esiste su `PropertyResult` (ha `result.spec.kind.value`) |
| R14 | Messaggio risultato in lingua target | **DONE** | `errors.py` ha 3 locales (en/it/pt) + `_intent_bridge.py` ha `_STRINGS` completo in 3 lingue |
| R15 | `generate_python()` (B.3) | **DONE** | `codegen.py:544-557` -- funziona, usato in `_execute_pipeline()` linea 1035 |
| R16 | Nomi metodi in italiano (non solo inglese) | **DA FARE** | `codegen.py:138-143` -- `_to_method_name()` genera sempre `send_{kind.value}` in inglese (es. `send_task_request`, mai `chiedi_ingredienti`) |
| R17 | Salvataggio file .py generato | **DONE** | `_cli.py:179-189` -- flag `-o/--output` salva su file |
| R18 | Simulazione protocollo con SessionChecker | **PARZIALE** | `_intent_bridge.py:1179-1222` -- simulazione NARRATIVA esiste, ma NON usa `SessionChecker.send()` reale. E solo rendering statico dei passi del protocollo |
| R19 | Output simulazione narrativo (non tecnico) | **DONE** | `_intent_bridge.py:1224-1231` -- `_step_narrative()` con `_SIM_NARRATIVES` in 3 lingue |
| R20 | Demo violazione (tentativo bloccato) | **DA FARE** | `checker.py` ha `ProtocolViolation`, ma lo script prevede una demo INTERATTIVA dove l'utente chiede "E se la dispensa prova a cancellare?" e il sistema mostra la violazione bloccata. Nessun codice per questo |
| R21 | Riepilogo sessione con metriche | **DONE** | `_intent_bridge.py:1049-1063` -- template `summary` con nome, ruoli, messaggi, proprieta, lingua |
| R22 | `no_deletion` come nuovo PropertyKind | **DA FARE** | `spec.py:75-84` -- NON presente in `PropertyKind` enum. Nemmeno in `_PROPERTY_NAMES` di `_intent_bridge.py:234-238` |
| R23 | `role_exclusive` come nuovo PropertyKind | **DA FARE** | `spec.py:75-84` -- NON presente in `PropertyKind` enum. Nemmeno in `_PROPERTY_NAMES` di `_intent_bridge.py:234-238` |

---

## BUG CRITICI Scoperti

### BUG 1: Spec format mismatch (pipeline verification silently fails)

**File:** `_intent_bridge.py:1017-1023`

Il codice costruisce:
```
spec GestioneRicette:
    requires always_terminates
    requires no_deadlock
```

Ma `parse_spec()` in `spec.py` aspetta:
```
properties for GestioneRicette:
    always terminates
    no deadlock
```

Differenze:
1. `spec NAME:` vs `properties for NAME:`
2. `requires always_terminates` vs `always terminates` (con spazio, senza `requires`)
3. `no_deadlock` (underscore) vs `no deadlock` (spazio)

Risultato: `parse_spec()` lancia `SpecParseError`, il `try/except` a linea 1025 cattura, `report = None`, e `_render_verification()` ritorna `""`. **La verifica e completamente saltata in silenzio.**

### BUG 2: `result.property_name` non esiste

**File:** `_intent_bridge.py:1156`

```python
prop=result.property_name,  # AttributeError!
```

`PropertyResult` (spec.py:164) ha `spec: PropertySpec`, NON `property_name`. Il campo corretto sarebbe `result.spec.kind.value`. Questo causerebbe `AttributeError` se la verifica arrivasse a questo punto -- ma dato che BUG 1 fa saltare la verifica, non viene mai raggiunto.

---

## Riepilogo per Categoria

| Categoria | DONE | PARZIALE | DA FARE |
|-----------|------|----------|---------|
| CLI (R1, R2, R17) | 3 | 0 | 0 |
| NL/Disambiguazione (R3, R4, R5) | 3 | 0 | 0 |
| Rendering/i18n (R6, R7, R14, R19, R21) | 3 | 1 | 0 |
| Core Pipeline (R9, R11, R12, R15) | 2 | 1 | 0 |
| Verifica progressiva (R13) | 0 | 1 | 0 |
| Interattivita (R8, R20) | 0 | 1 | 1 |
| Codegen italiano (R16) | 0 | 0 | 1 |
| Simulazione reale (R18) | 0 | 1 | 0 |
| Nuove proprieta (R10, R22, R23) | 0 | 0 | 3 |
| **TOTALE** | **11** | **5** | **5** |

---

## Priorita per E.5

### P0 - BLOCCANTI (senza questi la demo non funziona)

1. **Fix BUG 1**: Corregere formato spec in `_execute_pipeline()` -- usare `properties for NAME:` + body corretto (`always terminates`, `no deadlock`, etc.). Stimata: ~15 LOC.
2. **Fix BUG 2**: Cambiare `result.property_name` -> `result.spec.kind.value` in `_render_verification()`. Stimata: 1 riga.

### P1 - NECESSARI per la demo La Nonna

3. **R22 `no_deletion`**: Aggiungere `PropertyKind.NO_DELETION` in `spec.py`, parser, checker statico, checker runtime. Semantica: nessuno step puo avere un'azione "delete". Stimata: ~60-80 LOC.
4. **R23 `role_exclusive`**: Aggiungere `PropertyKind.ROLE_EXCLUSIVE` in `spec.py` con params `(action, role)`. Semantica: solo quel ruolo puo compiere quell'azione. Stimata: ~60-80 LOC.
5. **R7 spiegazione proprieta**: Aggiungere dict `_PROPERTY_EXPLANATIONS` con testo human-readable per ogni proprieta in 3 lingue (es. "Il sistema finisce SEMPRE"). Stimata: ~30 LOC.
6. **R13 fix rendering verifiche**: Dopo fix BUG 1+2, il rendering progressivo funzionera. Verificare che l'output corrisponda allo script.

### P2 - DESIDERABILI per la demo

7. **R8 modifica incrementale**: Aggiungere fase MODIFY dopo CONFIRM dove l'utente puo aggiungere/rimuovere proprieta senza reset totale. Stimata: ~50-80 LOC.
8. **R18 simulazione con SessionChecker reale**: Usare `SessionChecker.send()` nella simulazione per avere violazioni REALI, non solo rendering statico. Stimata: ~40-60 LOC.
9. **R20 demo violazione interattiva**: Dopo simulazione, offrire "Vuoi testare una violazione?" e simulare un tentativo bloccato. Stimata: ~40-60 LOC.
10. **R16 nomi metodi italiano**: Mapping opzionale `lang -> method_name_template` in codegen. Complessita alta per backward compatibility. Stimata: ~40 LOC ma rischiosa.

### P3 - NICE TO HAVE

11. **R10 _PROPERTY_NAMES aggiornamento**: Dopo R22/R23, aggiungere `no_deletion` e `role_exclusive` al menu proprieta nel guided mode.

---

## Stima Effort Totale

| Priorita | LOC stimati | Complessita |
|----------|-------------|-------------|
| P0 (bug fix) | ~20 | Bassa |
| P1 (core demo) | ~200 | Media |
| P2 (polish demo) | ~180 | Media-Alta |
| P3 (menu update) | ~10 | Bassa |
| **TOTALE** | **~410** | |

**Raccomandazione:** Iniziare da P0 (5 min), poi P1 (la demo non funziona senza R22/R23). P2 puo essere fatto dopo se il tempo lo permette. P3 e triviale e va fatto insieme a P1.

---

> "Il debito tecnico si paga con interessi."

*Cervella Ingegnera - CervellaSwarm S442*
