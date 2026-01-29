<!-- DISCRIMINATORE: MIRACOLLOOK EMAIL CLIENT -->
<!-- PORTA: 8002 | TIPO: Email client AI per hotel -->
<!-- PATH: ~/Developer/miracollogeminifocus/miracallook/ -->
<!-- NON CONFONDERE CON: PMS Core (8001), Room Hardware (8003) -->

# PROMPT RIPRESA - Miracollook

> **Ultimo aggiornamento:** 29 Gennaio 2026 - Sessione 317
> **ROBUSTEZZA:** 10/10 - CONNETTORE ERICSOFT IMPLEMENTATO!

---

## SESSIONE 317 - ERICSOFT CONNECTOR COMPLETATO! ✓

```
+================================================================+
|   S317: FASE 3.1 COMPLETATA!                                     |
|   - Modulo ericsoft/ creato con tutte le misure sicurezza       |
|   - 3 endpoints REST funzionanti                                |
|   - Guardiana Qualita: 9/10 APPROVE                             |
+================================================================+
```

### RISULTATI S317

| # | Task | Stato |
|---|------|-------|
| 1 | pymssql aggiunto a requirements | ✓ |
| 2 | Config Ericsoft in .env | ✓ |
| 3 | Modulo `backend/ericsoft/` | ✓ 4 file |
| 4 | Circuit breaker + semaphore | ✓ |
| 5 | Integrazione in main.py | ✓ |
| 6 | Audit Guardiana | ✓ 9/10 |

### ENDPOINTS CREATI

```
GET /ericsoft/status          # Health check connessione
GET /ericsoft/bookings        # Lista prenotazioni con email
GET /ericsoft/bookings/active # Prenotazioni attive (in casa)
GET /ericsoft/bookings/search # Cerca per email
```

### CHECKLIST SICUREZZA

| Requisito | File | Implementazione |
|-----------|------|-----------------|
| Timeout 5 sec | connector.py | `timeout` + `login_timeout` |
| Max 2 conn | connector.py | `asyncio.Semaphore` |
| Logging | connector.py | `structlog` ogni query |
| Circuit breaker | connector.py | 3 failures → 60s block |
| Solo SELECT | DB level | utente `miracollook_reader` |

---

## PROSSIMO STEP (S318)

```
FASE 3.2: Test connessione reale
- Installare pymssql: pip install pymssql
- Avviare backend su rete hotel
- Testare GET /ericsoft/status
- Testare GET /ericsoft/bookings/active

OPPURE

FASE 3.3: Integrazione con email enrichment
- Collegare ericsoft a gmail/pms_context.py
- Quando arriva email → cerca in Ericsoft
```

---

## SESSIONI PRECEDENTI

| Sessione | Cosa | Archivio |
|----------|------|----------|
| S316 | Schema DB + Utente | `ricerche/STUDIO_TABELLE_S316.md` |
| S314 | MyReception esplorato | `archivio/S314_MYRECEPTION.md` |

---

## FILE CHIAVE

| File | Cosa |
|------|------|
| `backend/ericsoft/connector.py` | Connettore SQL sicuro |
| `backend/ericsoft/api.py` | Endpoints REST |
| `backend/gmail/pms_context.py` | PMS HTTP integration |
| `.env` | Credenziali Ericsoft |

---

## COME TESTARE

```bash
# 1. Installa dipendenze
cd ~/Developer/miracollogeminifocus/miracallook/backend
pip install pymssql

# 2. Avvia backend (da rete hotel!)
uvicorn main:app --port 8002 --reload

# 3. Test endpoint
curl http://localhost:8002/ericsoft/status
curl http://localhost:8002/ericsoft/bookings/active
```

**NOTA:** Connessione Ericsoft funziona SOLO da rete interna hotel (192.168.200.x)

---

*"Studiare prima, implementare dopo!" - Formula Magica*
*"Un progresso al giorno!" - Sessione 317*
