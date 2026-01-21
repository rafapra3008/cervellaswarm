<!-- DISCRIMINATORE: MIRACOLLO PMS CORE -->
<!-- PORTA: 8001 | TIPO: Sistema alberghiero principale -->
<!-- PATH: ~/Developer/miracollogeminifocus/ (backend principale) -->
<!-- NON CONFONDERE CON: Miracollook (8002), Room Hardware (8003) -->

# PROMPT RIPRESA - PMS Core

> **Ultimo aggiornamento:** 21 Gennaio 2026 - Sessione 308
> **STATO:** 90% LIVE | Health 9.5/10

---

## SESSIONE 308 - F3.2 WEBHOOKS OUTBOUND COMPLETATO!

```
+================================================================+
|   F3.2 Webhooks Outbound  9/10 DONE                            |
|                                                                |
|   - HMAC SHA-256 signatures (timing-safe)                      |
|   - Exponential backoff retry (5 tentativi, 1s->1h)           |
|   - Dead Letter Queue (DLQ)                                    |
|   - 4 eventi: booking, payment, guest check-in                 |
|                                                                |
|   FASE 3 FEATURE = 2/5 (40%)                                   |
+================================================================+
```

---

## FASE 3 - PROGRESSO (2/5)

| Task | Status | Note |
|------|--------|------|
| **F3.1 Batch Operations** | **DONE 9/10** | POST /api/batch/* |
| **F3.2 Webhooks Outbound** | **DONE 9/10** | HMAC, retry, DLQ |
| F3.3 Revenue Dashboard | TODO | 5-7 sessioni |
| F3.4 Housekeeping Module | TODO | 6-8 sessioni |
| F3.5 Channel Manager 2-Way | FUTURO | dopo F3.2 (ora possibile!) |

---

## FILE CREATI SESSIONE 308

| File | Righe | Scopo |
|------|-------|-------|
| `migrations/044_webhooks_tables.sql` | 126 | Schema 4 tabelle |
| `models/webhook.py` | 221 | Pydantic models |
| `services/webhook_security.py` | 97 | HMAC SHA-256 |
| `services/webhook_emitter.py` | 171 | Event creation |
| `services/webhook_dispatcher.py` | 351 | HTTP delivery + retry |
| `routers/webhooks.py` | 561 | API endpoints |
| `docs/DESIGN_WEBHOOKS_OUTBOUND.md` | 1662 | Design completo |

---

## ENDPOINT WEBHOOKS CREATI

```
POST   /api/webhooks/subscriptions     - Crea subscription
GET    /api/webhooks/subscriptions     - Lista subscriptions
GET    /api/webhooks/subscriptions/:id - Dettaglio
PATCH  /api/webhooks/subscriptions/:id - Aggiorna
DELETE /api/webhooks/subscriptions/:id - Elimina
GET    /api/webhooks/events/:id/status - Status delivery
GET    /api/webhooks/dlq               - Dead Letter Queue
POST   /api/webhooks/dlq/:id/retry     - Retry da DLQ
GET    /api/webhooks/supported-events  - Lista eventi supportati
```

---

## PROSSIMA SESSIONE - OPZIONI

1. **F3.3 Revenue Dashboard** (5-7 sessioni) - Richiede subroadmap
2. **F3.4 Housekeeping Module** (6-8 sessioni)
3. **Emission Points** - Integrare webhooks in booking/payment/checkin

---

## WARNING ESISTENTI

- **FK violations:** 1262 nel DB (problema esistente, task separato)

---

*"Webhooks pronti! Real-time integrations abilitate!" - Sessione 308*
