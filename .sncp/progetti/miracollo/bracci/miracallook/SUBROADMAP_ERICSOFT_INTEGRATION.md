# SUBROADMAP: Integrazione Ericsoft - Miracollook

> **Aggiornato:** 30 Gennaio 2026 - Sessione 322
> **Obiettivo:** Miracollook legge dati ospiti da DB Ericsoft
> **Approccio:** Accesso diretto read-only (stessa rete hotel)

---

## ARCHITETTURA (CORRETTA!)

```
+================================================================+
|                                                                  |
|   RETE HOTEL (192.168.200.x) - TUTTO QUI!                       |
|                                                                  |
|   ┌──────────────┐         ┌──────────────────┐                 |
|   │   ERICSOFT   │         │   MIRACOLLOOK    │                 |
|   │   SQL Server │◄────────│   BACKEND        │                 |
|   │  (200.5)     │  SQL    │   (:8002)        │                 |
|   │              │ read-   │                  │                 |
|   │              │ only    │  - Connector     │                 |
|   └──────────────┘         │  - Cache         │                 |
|                            │  - API REST      │                 |
|                            └────────┬─────────┘                 |
|                                     │                           |
+═════════════════════════════════════╪═══════════════════════════+
                                      │ API REST
                                      ▼
                              ┌───────────────┐
                              │   FRONTEND    │
                              │   Browser     │
                              └───────────────┘
```

**NOTA IMPORTANTE:**
- ❌ NON serve VPN (siamo nella stessa rete!)
- ❌ NON serve Raspberry Pi gateway
- ❌ NON serve partnership Ericsoft
- ✅ Accesso diretto read-only al DB

---

## STATO FASI (30 Gen 2026)

```
FASE 1: Connector Base        [####################] 100% ✅
FASE 2: Guest Management      [############........] 60%
FASE 3: Cache Layer           [....................] 0%
FASE 4: API Endpoints         [....................] 0%
FASE 5: Frontend Integration  [....................] 0%
FASE 6: Test & Production     [....................] 0%
```

---

## FASE 1: Connector Base - COMPLETATA ✅

**Sessioni:** S317-S319
**Status:** 100% DONE

| Step | Cosa | Status |
|------|------|--------|
| 1.1 | Credenziali DB | ✅ .env configurato |
| 1.2 | Connector pymssql | ✅ v2.0.1 |
| 1.3 | Circuit breaker | ✅ 3 failures → 60s block |
| 1.4 | Timeout + Semaphore | ✅ 5s timeout, max 2 conn |
| 1.5 | Connessione testata | ✅ S319 (dalla rete hotel) |

**File:** `ericsoft/connector.py`

---

## FASE 2: Guest Management - IN CORSO

**Sessioni:** S320-S322
**Status:** 60%

| Step | Cosa | Status | File |
|------|------|--------|------|
| 2.1 | Studio best practices | ✅ 1988 righe ricerca | S320 |
| 2.2 | Modello GuestProfile | ✅ 9.4/10 | `models/guest_profile.py` |
| 2.3 | Query SQL Master | ✅ 9.2/10 | `queries/guest_queries.py` |
| 2.4 | Connector v2.0.1 | ✅ 9.8/10 | 6 nuovi metodi |
| 2.5 | Security fix LIKE | ✅ 10/10 | S322 |
| 2.6 | Test unitari | ✅ 18/18 pass | `tests/test_guest_profile.py` |
| 2.7 | Test su DB reale | ⏳ | Da fare in hotel |

**Metodi disponibili:**
- `get_all_guests(limit)` - Tutti gli ospiti
- `get_in_house_guests()` - Ospiti in casa (~111)
- `get_guests_by_status(status)` - Per stato
- `get_post_stay_guests(days)` - Partiti recentemente
- `get_pre_arrival_guests(days)` - In arrivo
- `get_guest_by_id(id)` - Profilo completo

---

## FASE 3: Cache Layer - DA FARE

**Obiettivo:** Ridurre carico DB, graceful degradation
**Priorità:** ALTA

| Step | Cosa | Dettagli |
|------|------|----------|
| 3.1 | Cache in-memory | cachetools TTL |
| 3.2 | Cache get_all_guests | TTL 5 min |
| 3.3 | Cache get_in_house | TTL 1 min |
| 3.4 | Graceful degradation | Serve stale se DB down |
| 3.5 | Cache invalidation | Manual + TTL |

---

## FASE 4: API Endpoints - DA FARE

**Obiettivo:** Esporre dati ospiti via REST API
**Priorità:** ALTA (dopo cache)

| Endpoint | Metodo | Descrizione |
|----------|--------|-------------|
| `/api/guests` | GET | Lista ospiti (paginata) |
| `/api/guests/in-house` | GET | Ospiti in casa |
| `/api/guests/search` | GET | Cerca per email/telefono |
| `/api/guests/{id}` | GET | Profilo completo |
| `/api/guests/post-stay` | GET | Partiti ultimi N giorni |
| `/api/ericsoft/status` | GET | Health check DB |

---

## FASE 5: Frontend Integration - DA FARE

**Obiettivo:** GuestContextCard quando leggi email
**Priorità:** MEDIA (dopo API)

| Step | Cosa | Dettagli |
|------|------|----------|
| 5.1 | GuestContextCard | Componente React |
| 5.2 | Hook useGuestContext | Fetch dati ospite |
| 5.3 | Integrazione EmailView | Mostra card se ospite trovato |
| 5.4 | Loading/Error states | UX completa |

---

## FASE 6: Test & Production - DA FARE

**Obiettivo:** Validare tutto su ambiente reale
**Priorità:** ALTA (gating per production)

| Step | Cosa | Dettagli |
|------|------|----------|
| 6.1 | Test dalla rete hotel | Verifica connessione |
| 6.2 | Test query performance | < 500ms response |
| 6.3 | Test circuit breaker | Simula DB offline |
| 6.4 | Test cache | Verifica TTL funziona |
| 6.5 | Documentazione | README setup |

---

## PROSSIMI STEP IMMEDIATI

1. **Test DB reale** - Quando in hotel, eseguire `test_guest_management.py`
2. **Cache Layer** - Implementare FASE 3
3. **API Endpoints** - Implementare FASE 4

---

## FILE CHIAVE

| File | Cosa | Versione |
|------|------|----------|
| `ericsoft/connector.py` | Connector principale | v2.0.1 |
| `ericsoft/models/guest_profile.py` | Modello GuestProfile | v1.0.0 |
| `ericsoft/queries/guest_queries.py` | Query SQL | v1.0.1 |
| `tests/test_guest_profile.py` | Test unitari | 18 test |

---

## DATI VERIFICATI (S321)

```
DB Ericsoft - Tabella SchedaConto/Anagrafica:

IdStatoScheda | Totale | Mapping
1             | 816    | PRE_ARRIVAL
2             | 132    | ARRIVAL_DAY
3             | 111    | IN_HOUSE
5             | 3211   | POST_STAY
--------------+--------+-----------
TOTALE        | 4270   | ospiti

NOTA: Stato 4 NON ESISTE!
```

---

*"Accesso diretto, semplice, sicuro. Stessa rete = zero complicazioni!"*

*Cervella & Rafa - Sessione 322*
