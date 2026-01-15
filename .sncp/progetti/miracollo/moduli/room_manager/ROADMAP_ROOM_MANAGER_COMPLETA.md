# ROADMAP ROOM MANAGER COMPLETA - MIRACOLLO

> **QUESTO FILE È LA GUIDA DEFINITIVA.**
> **NON SI RIDISCUTE. SI SEGUE.**
>
> Creata: 15 Gennaio 2026 - Sessione 217
> Basata su: Ricerca + Analisi Ingegnera + Decisioni Rafa

---

## STATO ATTUALE

```
MVP BASE                    [####################] 100% LIVE!
├── Backend API             ✅ room_manager_service.py (541 righe)
├── Frontend Grid           ✅ room-manager.html + 5 moduli JS
├── Activity Log            ✅ Funziona, eventi loggati
├── Housekeeping Actions    ✅ Bottoni funzionano
├── Planning Integration    ✅ Pallini colorati visibili
└── Deploy                  ✅ https://miracollo.com/room-manager.html

VDA INTEGRATION             [....................] 0% DA FARE
├── MODBUS Client           🔲 Leggere sensori
├── HVAC Control            🔲 Scrivere temperatura
├── PIN Generation          🔲 Codici accesso
├── WebSocket               🔲 Real-time updates
└── Redis Cache             🔲 Performance
```

---

## PREREQUISITO CRITICO

```
+==================================================================+
|   PRIMA DI TUTTO: DOCUMENTAZIONE VDA MODBUS!                     |
|                                                                  |
|   Senza sapere quali registri leggere/scrivere,                 |
|   NON possiamo integrare i sensori.                              |
|                                                                  |
|   AZIONE RAFA: Contattare VDA support                            |
|   - Chiedere documentazione MODBUS                               |
|   - Register map dispositivi                                     |
|   - Specifiche RCU, termostati, serrature                        |
|                                                                  |
|   BLOCCO: Finché non abbiamo docs, non si procede!              |
+==================================================================+
```

---

## ARCHITETTURA TARGET

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND                                │
│  room-manager.html + WebSocket Client                        │
└─────────────────────────────────────────────────────────────┘
                           ↕
┌─────────────────────────────────────────────────────────────┐
│                      BACKEND (FastAPI)                       │
│  REST API + WebSocket Manager + Background Tasks             │
└─────────────────────────────────────────────────────────────┘
                           ↕
┌─────────────────────────────────────────────────────────────┐
│                   MIDDLEWARE (Redis)                         │
│  Cache sensori + Command Queue + PubSub                      │
└─────────────────────────────────────────────────────────────┘
                           ↕
┌─────────────────────────────────────────────────────────────┐
│                   VDA GATEWAY (pymodbus)                     │
│  MODBUS Client → 112 dispositivi                             │
└─────────────────────────────────────────────────────────────┘
```

---

## FASI DI IMPLEMENTAZIONE

### FASE 0: PREREQUISITI (Rafa)
**Status:** 🔲 DA FARE
**Blocca tutto il resto!**

- [ ] Contattare VDA support
- [ ] Ottenere documentazione MODBUS
- [ ] Ottenere register map dispositivi
- [ ] Ottenere credenziali accesso rete MODBUS hotel

---

### FASE 1: FOUNDATION (2 settimane, 40h)
**Status:** 🔲 DA FARE
**Dipende da:** FASE 0 completata

**Obiettivo:** Connessione VDA e lettura sensori

**Task:**
1. [ ] Setup Redis (docker-compose)
2. [ ] Creare `vda_service.py` con pymodbus
3. [ ] Mapping dispositivi da register map VDA
4. [ ] Lettura temperatura (read-only test)
5. [ ] Lettura presenza/porta (read-only test)
6. [ ] Background polling task (ogni 30s)
7. [ ] Cache sensori in Redis (TTL 5min)
8. [ ] API endpoint GET /api/vda/rooms/{id}/sensors

**Output:** Dati sensori REALI visibili in Room Manager

**File da creare:**
```
backend/services/vda_service.py (~400 righe)
backend/services/vda_device_registry.py (~250 righe)
docker-compose.yml (aggiungere Redis)
```

---

### FASE 2: REAL-TIME (1.5 settimane, 30h)
**Status:** 🔲 DA FARE
**Dipende da:** FASE 1 completata

**Obiettivo:** Aggiornamenti live senza refresh

**Task:**
1. [ ] WebSocket Manager backend
2. [ ] Endpoint /ws/room-manager/{hotel_code}
3. [ ] Redis PubSub per broadcast
4. [ ] Frontend WebSocket client
5. [ ] Auto-reconnect logic
6. [ ] Optimistic UI updates

**Output:** Cambiamenti sensori visibili LIVE

**File da creare:**
```
backend/websocket/manager.py (~200 righe)
frontend/js/room-manager/websocket.js (~150 righe)
```

---

### FASE 3: CONTROL (2 settimane, 40h)
**Status:** 🔲 DA FARE
**Dipende da:** FASE 2 completata

**Obiettivo:** Controllo HVAC e dispositivi

**Task:**
1. [ ] Command Queue con Celery
2. [ ] MODBUS write operations
3. [ ] API PUT /api/vda/rooms/{id}/temperature
4. [ ] API PUT /api/vda/rooms/{id}/hvac-mode
5. [ ] Frontend UI controllo temperatura
6. [ ] Frontend UI scene luci (se supportato)
7. [ ] Timeout e retry logic
8. [ ] Audit log comandi

**Output:** Controllo temperatura da Room Manager!

**File da creare:**
```
backend/services/vda_command_service.py (~300 righe)
backend/tasks/vda_tasks.py (~200 righe)
```

---

### FASE 4: PIN ACCESS (1 settimana, 20h)
**Status:** 🔲 DA FARE
**Dipende da:** FASE 3 completata

**Obiettivo:** Generazione codici accesso

**Task:**
1. [ ] PIN generation sicura (secrets module)
2. [ ] API POST /api/access/rooms/{id}/generate-pin
3. [ ] Integrazione con booking (check-in/check-out)
4. [ ] UI mostra codici attivi
5. [ ] Revoca codici

**Output:** PIN automatici per ospiti!

---

### FASE 5: PWA MOBILE (2 settimane, 40h)
**Status:** 🔲 DA FARE
**Dipende da:** FASE 1-4 completate (o parallelo)

**Obiettivo:** App mobile per staff housekeeping

**Task:**
1. [ ] Service Worker per offline
2. [ ] manifest.json per installazione
3. [ ] UI mobile-first housekeeping
4. [ ] Sync quando online
5. [ ] Push notifications (opzionale)

**Output:** Staff usa cellulare per housekeeping!

---

### FASE 6: POLISH (1 settimana, 20h)
**Status:** 🔲 DA FARE

**Task:**
1. [ ] Energy monitoring dashboard
2. [ ] Device health alerts
3. [ ] Automation rules (eco mode, pre-arrival)
4. [ ] Load testing
5. [ ] Documentazione

---

## EFFORT TOTALE

```
FASE 0: Prerequisiti     Rafa (1-2 giorni contatti)
FASE 1: Foundation       40h (~2 settimane)
FASE 2: Real-time        30h (~1.5 settimane)
FASE 3: Control          40h (~2 settimane)
FASE 4: PIN Access       20h (~1 settimana)
FASE 5: PWA Mobile       40h (~2 settimane)
FASE 6: Polish           20h (~1 settimana)
─────────────────────────────────────────
TOTALE:                  ~190h (~10 settimane part-time)
```

---

## DECISIONI GIÀ PRESE (NON RIDISCUTERE!)

| Cosa | Decisione | Perché |
|------|-----------|--------|
| MODBUS library | pymodbus | Standard, stabile, documentata |
| Cache | Redis | PubSub + Cache + Queue in uno |
| Task Queue | Celery | Maturo, retry logic built-in |
| Mobile | PWA | No app store, installabile |
| PIN length | 6 cifre | Balance sicurezza/usabilità |
| Polling interval | 30s | Balance real-time/carico |
| Cache TTL | 5min | Dati sensori abbastanza fresh |

---

## RISCHI E MITIGAZIONI

| Rischio | Impatto | Mitigazione |
|---------|---------|-------------|
| VDA docs non disponibili | BLOCCO TOTALE | Plan B: reverse engineering (lento) |
| Latenza MODBUS 2-5s | UX frustrante | Command queue + optimistic UI |
| Redis down | No real-time | Fallback HTTP polling |
| Dispositivi offline | Dati stale | Health monitoring + alert |

---

## COME USARE QUESTA ROADMAP

```
+==================================================================+
|   REGOLA PER LA PROSSIMA CERVELLA:                               |
|                                                                  |
|   1. Leggi questo file                                           |
|   2. Guarda quale FASE è in corso                                |
|   3. Esegui i TASK di quella fase                                |
|   4. NON ridiscutere architettura                                |
|   5. NON ri-analizzare tutto                                     |
|   6. Se bloccata, chiedi a Rafa                                  |
|                                                                  |
|   "Il NORD ci guida. La ROADMAP ci mappa."                       |
+==================================================================+
```

---

## FILE CORRELATI

| Cosa | Path |
|------|------|
| NORD Miracollo | `miracollogeminifocus/NORD.md` |
| Ricerca VDA | `.sncp/progetti/miracollo/moduli/room_manager/studi/20260115_RICERCA_ROOM_MANAGER_AVANZATO.md` |
| Codice MVP | `miracollogeminifocus/backend/services/room_manager_service.py` |
| Frontend MVP | `miracollogeminifocus/frontend/room-manager.html` |

---

*"Fatto BENE > Fatto VELOCE"*
*"NON SI RIDISCUTE. SI SEGUE."*

**Cervella & Rafa - 15 Gennaio 2026**
