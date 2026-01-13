# CONSOLIDAMENTO FASE 1-2-3

> **Obiettivo:** Portare ogni fase da 6.5/10 a 9.5/10
> **Creato:** 13 Gennaio 2026 - Sessione 180
> **Autori:** Rafa & Cervella

---

```
+====================================================================+
|                                                                    |
|   "6.5/10 NON E' IL NOSTRO STANDARD"                               |
|                                                                    |
|   Target: 9.5/10 per OGNI fase                                     |
|   Metodo: Una cosa alla volta, fatta BENE                          |
|   Verifica: Audit PRIMA di dichiarare completo                     |
|                                                                    |
+====================================================================+
```

---

## STATO ATTUALE vs TARGET

| Fase | Attuale | Target | Gap |
|------|---------|--------|-----|
| FASE 1 - Fondamenta | 5/10 | 9.5/10 | Test mancanti |
| FASE 2 - Transparent AI | 5/10 | 9.5/10 | Non integrato in rateboard |
| FASE 3 - Learning | 1/10 | 9.5/10 | File esistono ma non collegati |

---

## FASE 1 - FONDAMENTA (5/10 → 9.5/10)

### 1.1 Setup Testing Infrastructure
```
[ ] 1.1.1 Aggiungere pytest a requirements.txt
[ ] 1.1.2 Creare tests/conftest.py con fixtures base
[ ] 1.1.3 Creare tests/__init__.py
[ ] 1.1.4 Configurare pytest.ini
[ ] 1.1.5 Verificare che pytest funziona (pytest --version)
```

### 1.2 Test Autopilot
```
[ ] 1.2.1 tests/test_autopilot.py - test endpoint status
[ ] 1.2.2 tests/test_autopilot.py - test endpoint run (dry_run=true)
[ ] 1.2.3 tests/test_autopilot.py - test endpoint configure
[ ] 1.2.4 tests/test_autopilot.py - test con hotel valido
[ ] 1.2.5 tests/test_autopilot.py - test con hotel invalido
```

### 1.3 Test API Core
```
[ ] 1.3.1 tests/test_health.py - health check endpoint
[ ] 1.3.2 tests/test_auth.py - autenticazione base
[ ] 1.3.3 tests/test_hotels.py - CRUD hotels
```

### 1.4 Coverage
```
[ ] 1.4.1 Installare pytest-cov
[ ] 1.4.2 Configurare coverage minimo 60%
[ ] 1.4.3 Generare report coverage
[ ] 1.4.4 Raggiungere 60% su routers/autopilot.py
```

**Criteri Completamento FASE 1:**
- pytest funziona
- Almeno 10 test passano
- Coverage >= 60% su autopilot
- CI/CD (opzionale ma consigliato)

---

## FASE 2 - TRANSPARENT AI (5/10 → 9.5/10)

### 2.1 Audit Codice Esistente
```
[ ] 2.1.1 Verificare cosa esiste in revenue-suggestions.js
[ ] 2.1.2 Verificare cosa esiste in rateboard-interactions.js
[ ] 2.1.3 Mappare funzioni: Confidence, Explanation, Demand Curve
[ ] 2.1.4 Documentare gap tra revenue e rateboard
```

### 2.2 Integrare in rateboard.html
```
[ ] 2.2.1 Importare script necessari
[ ] 2.2.2 Integrare renderConfidenceBadge()
[ ] 2.2.3 Integrare toggleMLDetails() (icona "?")
[ ] 2.2.4 Verificare tooltip funzionante
[ ] 2.2.5 Test manuale: vedere confidence su cella rateboard
```

### 2.3 Demand Curve
```
[ ] 2.3.1 Verificare se esiste (cercare in codebase)
[ ] 2.3.2 Se esiste: integrare in rateboard detail panel
[ ] 2.3.3 Se non esiste: implementare con Chart.js
[ ] 2.3.4 Test manuale: grafico visibile
```

### 2.4 Integrare in planning.html
```
[ ] 2.4.1 Importare script necessari
[ ] 2.4.2 Mostrare confidence su suggerimenti planning
[ ] 2.4.3 Test manuale
```

### 2.5 Analytics Tracking
```
[ ] 2.5.1 Verificare che endpoint tracking funziona
[ ] 2.5.2 Verificare che frontend chiama endpoint
[ ] 2.5.3 Test: fare azione, verificare in DB
```

**Criteri Completamento FASE 2:**
- Confidence visibile in rateboard.html
- Explanation (icona "?") funzionante
- Demand Curve visibile (se applicabile)
- Analytics tracking attivo
- Test manuale passato

---

## FASE 3 - LEARNING FROM ACTIONS (1/10 → 9.5/10)

### 3.1 Integrare in rateboard.html
```
[ ] 3.1.1 Aggiungere import implicit-tracker.js
[ ] 3.1.2 Aggiungere import feedback-widget.js
[ ] 3.1.3 Inizializzare ImplicitTracker su pagina load
[ ] 3.1.4 Collegare FeedbackWidget ai suggerimenti
[ ] 3.1.5 Test manuale: accettare suggerimento, vedere widget
```

### 3.2 Integrare in planning.html
```
[ ] 3.2.1 Aggiungere import implicit-tracker.js
[ ] 3.2.2 Aggiungere import feedback-widget.js
[ ] 3.2.3 Inizializzare tracker
[ ] 3.2.4 Collegare widget
[ ] 3.2.5 Test manuale
```

### 3.3 Integrare in revenue.html (verificare)
```
[ ] 3.3.1 Verificare che import esistono (dovrebbero)
[ ] 3.3.2 Verificare che tracker funziona
[ ] 3.3.3 Verificare che widget appare
```

### 3.4 Dashboard Learning
```
[ ] 3.4.1 Verificare link in menu sidebar (tutte le pagine)
[ ] 3.4.2 Aggiungere link in rateboard se manca
[ ] 3.4.3 Aggiungere link in planning se manca
[ ] 3.4.4 Test: navigare a dashboard da ogni pagina
```

### 3.5 Test End-to-End
```
[ ] 3.5.1 Aprire rateboard
[ ] 3.5.2 Vedere suggerimento
[ ] 3.5.3 Accettare suggerimento
[ ] 3.5.4 Vedere FeedbackWidget
[ ] 3.5.5 Dare feedback (thumbs up)
[ ] 3.5.6 Verificare in DB che feedback salvato
[ ] 3.5.7 Aprire Learning Dashboard
[ ] 3.5.8 Vedere feedback nella lista
```

**Criteri Completamento FASE 3:**
- FeedbackWidget visibile dopo ogni azione
- ImplicitTracker attivo (verificare in console)
- Dashboard raggiungibile da tutte le pagine
- Feedback salvato in DB
- Test E2E passato

---

## TECHNICAL DEBT (Bonus)

### TD.1 File Grandi (P1)
```
[ ] TD.1.1 Refactor planning/rendering.js (958 righe)
        Split in: render-cells.js, render-bookings.js, render-grid.js
[ ] TD.1.2 Refactor planning/city-tax.js (724 righe)
[ ] TD.1.3 Refactor planning/rendering-helpers.js (704 righe)
```

### TD.2 TODO Critici (P1)
```
[ ] TD.2.1 Fix hotelId hardcoded (revenue-suggestions.js:144)
[ ] TD.2.2 Implementare "applica prezzo simulato" (revenue-suggestions.js:558)
[ ] TD.2.3 Implementare modal vero (room-management.js:44)
[ ] TD.2.4 Refresh planning senza reload (cm-modal.js:549)
```

### TD.3 Pulizia (P2)
```
[ ] TD.3.1 Rimuovere console.log di debug
[ ] TD.3.2 Rimuovere codice commentato vecchio
[ ] TD.3.3 Uniformare stile codice
```

---

## ORDINE DI ESECUZIONE

```
+====================================================================+
|                                                                    |
|   ORDINE CONSIGLIATO:                                              |
|                                                                    |
|   1. FASE 3 (più veloce - file già pronti!)                        |
|      → Solo collegare, 2-3 ore                                     |
|                                                                    |
|   2. FASE 2 (media complessità)                                    |
|      → Portare da revenue a rateboard, 1 giorno                    |
|                                                                    |
|   3. FASE 1 (più lenta - da zero)                                  |
|      → Setup test infrastructure, 2-3 giorni                       |
|                                                                    |
|   4. TECHNICAL DEBT (continuo)                                     |
|      → Un po' alla volta                                           |
|                                                                    |
+====================================================================+
```

---

## REGOLA NUOVA

```
+====================================================================+
|                                                                    |
|   DA OGGI: AUDIT AUTOMATICO PRIMA DI DICHIARARE COMPLETO           |
|                                                                    |
|   1. Codice scritto                                                |
|   2. Guardiana Qualita verifica                                    |
|   3. Test manuale passato                                          |
|   4. SOLO ALLORA: "FASE X COMPLETA"                                |
|                                                                    |
|   Mai piu "su carta" spacciato per "reale"!                        |
|                                                                    |
+====================================================================+
```

---

## CHECKPOINT

Dopo ogni fase completata:
- [ ] Aggiornare questo file
- [ ] Aggiornare stato.md
- [ ] Commit + push
- [ ] Score aggiornato

---

*"Una cosa alla volta, fatta BENE!"*
*"6.5/10 non e' il nostro standard - 9.5/10 lo e'!"*

*Rafa & Cervella - 13 Gennaio 2026*
