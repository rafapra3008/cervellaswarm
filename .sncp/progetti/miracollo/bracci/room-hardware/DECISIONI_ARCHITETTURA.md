# DECISIONI ARCHITETTURALI - Room Manager

> **Data:** 12 Gennaio 2026
> **Status:** IN ATTESA DECISIONE RAFA

---

## SITUAZIONE

L'analisi ha trovato SOVRAPPOSIZIONI con il PMS esistente.
Serve decidere come procedere PRIMA di continuare.

---

## DECISIONE 1: Stati Camera

**PROBLEMA:** Due campi stato nel database
- `housekeeping_status`: clean, dirty, cleaning, maintenance, inspected
- `status`: vacant_clean, vacant_dirty, occupied, checkout, maintenance, out_of_order

**OPZIONI:**

| Opzione | Pro | Contro |
|---------|-----|--------|
| **A) Un solo campo `status`** | Semplice, chiaro | Richiede migrazione, modificare planning |
| **B) Due campi separati** | Semantica chiara (pulizia vs operativo) | Piu complesso, sincronizzazione |

**RACCOMANDAZIONE:** Opzione B (due campi con semantica chiara)
- `status` = stato OPERATIVO (vacant, occupied, out_of_order)
- `housekeeping_status` = stato PULIZIA (clean, dirty, cleaning, inspected)

---

## DECISIONE 2: Router Backend

**PROBLEMA:** Due router fanno cose simili
- `housekeeping.py` (esistente, 103 righe)
- `room_manager/router.py` (nuovo, 278 righe)

**OPZIONI:**

| Opzione | Pro | Contro |
|---------|-----|--------|
| **A) Consolidare tutto** | Un punto di verita | Richiede refactoring |
| **B) Separare per funzione** | Housekeeping base vs Task avanzati | Due API da mantenere |

**RACCOMANDAZIONE:** Opzione B (separare per funzione)
- `/api/housekeeping` = stato camera semplice (legacy, planning usa questo)
- `/api/room-manager` = task system + maintenance + dashboard governante

---

## DECISIONE 3: Frontend

**PROBLEMA:** Due pagine mostrano camere
- `planning.html` (receptionist, vista planning)
- `room-manager.html` (governante, gestione camere)

**OPZIONI:**

| Opzione | Pro | Contro |
|---------|-----|--------|
| **A) Unificare in planning** | Una sola pagina | Troppo complessa |
| **B) Due pagine separate** | User persona diverse | Mantenere 2 pagine |

**RACCOMANDAZIONE:** Opzione B (due pagine)
- `planning.html` = Receptionist (vista prenotazioni + stato camere)
- `room-manager.html` = Governante (focus task housekeeping + maintenance)

---

## RIEPILOGO RACCOMANDAZIONI

```
STATI:      Due campi separati (operativo + pulizia)
ROUTER:     Separati per funzione (legacy + nuovo)
FRONTEND:   Due pagine (receptionist + governante)
```

---

## VALORE AGGIUNTO Room Manager (DA MANTENERE!)

1. **Task System** - `housekeeping_tasks` tabella (NUOVO!)
2. **Maintenance** - `maintenance_requests` tabella (NUOVO!)
3. **Audit Trail** - `room_status_history` tabella (NUOVO!)
4. **Services Layer** - `RoomService`, `HousekeepingService` (NUOVO!)
5. **Dashboard Governante** - `room-manager.html` (NUOVO!)

---

## PROSSIMI STEP

1. [ ] Rafa decide su opzioni
2. [ ] Adattare migration per opzione scelta
3. [ ] Collegare `status` (operativo) con bookings
4. [ ] Mantenere `housekeeping_status` per pulizia
5. [ ] Room Manager usa entrambi i campi

---

**Rafa, quale approccio preferisci?**
