<!-- DISCRIMINATORE: MIRACOLLOOK EMAIL CLIENT -->
<!-- PORTA: 8002 | TIPO: Email client AI per hotel -->
<!-- PATH: ~/Developer/miracollogeminifocus/miracallook/ -->
<!-- NON CONFONDERE CON: PMS Core (8001), Room Hardware (8003) -->

# PROMPT RIPRESA - Miracollook

> **Ultimo aggiornamento:** 22 Gennaio 2026 - Sessione 312
> **ROBUSTEZZA:** 10/10 - PRODUCTION READY + PMS INTEGRATION!

---

## SESSIONE 312 - INTEGRAZIONE PMS CORE!

```
+================================================================+
|   MIRACOLLOOK: PMS INTEGRATION COMPLETATA!                     |
|                                                                |
|   - Backend: endpoint /gmail/enrich-context OK                 |
|   - Frontend: GuestContextCard + useGuestContext OK            |
|   - API Key: Configurata in entrambi i sistemi                 |
|   - Design: Palette miracollo-* GIA' APPLICATA!                |
+================================================================+
```

### NUOVI FILE

| File | Cosa |
|------|------|
| `backend/gmail/pms_context.py` | Endpoint PMS integration (260 righe) |
| `frontend/src/components/GuestContext/GuestContextCard.tsx` | Card info ospite (162 righe) |
| `frontend/src/hooks/useGuestContext.ts` | Hook fetch + cache (82 righe) |

### MODIFICHE

| File | Cosa |
|------|------|
| `backend/gmail/api.py` | +import pms_context, +include_router |
| `frontend/src/components/EmailDetail/EmailDetail.tsx` | +GuestContextCard |
| `frontend/src/types/email.ts` | +GuestInfo, ActiveBooking, GuestContextResponse |
| `frontend/src/services/api.ts` | +enrichGuestContext |
| `.env` (miracallook) | +PMS_API_URL, +PMS_API_KEY |
| `.env` (pms root) | +ADMIN_API_KEY |

### COME FUNZIONA

```
Email ricevuta → Miracollook chiama /gmail/enrich-context
                          ↓
                 PMS risponde con guest info + booking
                          ↓
                 UI mostra card "OSPITE CONOSCIUTO"
```

### COSA VEDE L'UTENTE

```
+----------------------------------------------------------+
| 🏨 OSPITE CONOSCIUTO                         Gold ⭐      |
|                                                          |
| Mario Rossi                                              |
| • 3 soggiorni (15 notti)                                |
| • Speso: €1,500                                         |
| • Ultima visita: 20 Dic 2025                            |
|                                                          |
| 📅 PRENOTAZIONE ATTIVA                                   |
| #NL-2026-000123                                          |
| Check-in: 15 Feb 2026 • Camera 101 • 3 notti            |
| Status: Confermata ✅ Pagata                             |
+----------------------------------------------------------+
```

---

## SESSIONE 304 - HARDTEST + LOGIN PAGE

```
FASE 11: HARDTEST + LoginPage → 9.5/10 ✅
- Docker build/up OK
- OAuth Google END-TO-END
- 9 email REALI caricate
```

---

## PROSSIMI STEP

```
1. Design "salutare" (palette colori) → GIA' FATTO! ✅
2. Collegamento con PMS Core → FATTO! ✅ (Sessione 312)
3. Integrazione WhatsApp → TODO
4. Più AI (risposte intelligenti) → TODO
5. Comunicazioni avanzate → TODO
```

---

## FILE CHIAVE (Aggiornato S312)

| File | Cosa |
|------|------|
| `docker-compose.yml` | Orchestrazione (backend:8002, frontend:80) |
| `backend/gmail/pms_context.py` | **NUOVO** - PMS integration |
| `frontend/src/components/GuestContext/GuestContextCard.tsx` | **NUOVO** - UI ospite |
| `frontend/src/hooks/useGuestContext.ts` | **NUOVO** - Hook fetch |
| `backend/auth/google.py` | OAuth Google |

---

## COME TESTARE

```bash
# 1. Avvia PMS Core
cd ~/Developer/miracollogeminifocus
uvicorn backend.main:app --port 8001

# 2. Avvia Miracollook
cd ~/Developer/miracollogeminifocus/miracallook
docker-compose up -d

# 3. Apri browser
open http://localhost:80

# 4. Login → seleziona email da ospite conosciuto → vedi card PMS!
```

### Test endpoint diretto
```bash
curl "http://localhost:8002/gmail/enrich-context?email=mario.rossi@gmail.com"
curl "http://localhost:8002/gmail/pms-status"
```

---

*"PMS + EMAIL = CONTESTO COMPLETO! Ultrapassar os próprios limites!" - Sessione 312*
