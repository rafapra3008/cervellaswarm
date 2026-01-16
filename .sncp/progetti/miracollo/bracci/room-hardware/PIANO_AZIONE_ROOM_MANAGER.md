# PIANO DI AZIONE REALE - Room Manager

> **Data:** 14 Gennaio 2026 - Sessione 207
> **Validato da:** Guardiana Qualita + Ingegnera + Researcher
> **Status:** PRONTO PER ESECUZIONE

---

## LA VISIONE

```
+================================================================+
|                                                                |
|   ROOM MANAGER = LA PARTE TANGIBILE DI MIRACOLLO               |
|                                                                |
|   - Hardware VERO (VDA installato in hotel)                    |
|   - Dashboard VISUALE (governante vede camere)                 |
|   - Task REALI (pulizia, manutenzione)                        |
|   - Integrazione con pricing (Revenue + Operations)            |
|                                                                |
|   "Finalmente qualcosa che si VEDE e si TOCCA!"               |
|                                                                |
+================================================================+
```

---

## STATO ATTUALE

```
GIA' FATTO (Sessione 172):
+------------------------+-------+------------------+
| Cosa                   | Score | Location         |
+------------------------+-------+------------------+
| Ricerca Big Players    | 9/10  | 1606 righe!      |
| MVP Backend            | 8/10  | 858 righe        |
| MVP Frontend           | 7/10  | Dashboard base   |
| Migration DB           | 9/10  | 3 tabelle nuove  |
| VDA Strategy           | 8/10  | Documentata      |
+------------------------+-------+------------------+
| TOTALE                 | 8/10  | SOLIDO!          |
+------------------------+-------+------------------+

DOVE TROVARLO:
- Branch: feature/room-manager
- Worktree: ~/Developer/miracollo-worktrees/room-manager/
```

---

## DECISIONI DA PRENDERE (RAFA)

### Decisione 1: Stati Camera

```
OPZIONE B (RACCOMANDATA):

rooms.status              = OPERATIVO (booking usa questo)
  - vacant
  - occupied
  - checkout
  - out_of_order

rooms.housekeeping_status = PULIZIA (governante usa questo)
  - clean
  - dirty
  - cleaning
  - inspected

PERCHE: Una camera puo essere VACANT + DIRTY (partenza mattina)
        Semantiche diverse, campi diversi!

[ ] Rafa conferma Opzione B? (SI/NO)
```

### Decisione 2: Frontend

```
OPZIONE B (RACCOMANDATA):

planning.html      = RECEPTIONIST (booking + camere)
room-manager.html  = GOVERNANTE (task + manutenzione)

PERCHE: User persona diverse, esigenze diverse!

[ ] Rafa conferma due frontend? (SI/NO)
```

---

## MAPPA DELLE FASI

```
+================================================================+
|                    ROOM MANAGER ROADMAP                         |
+================================================================+

FASE 0: DECISIONI                              [ ] 1 ora
  |     Rafa conferma architettura
  |     (bloccante per tutto il resto!)
  v
FASE 1: CONSOLIDAMENTO BACKEND                 [ ] 4-5 ore
  |     - Unificare router /api/housekeeping
  |     - Rimuovere duplicazioni
  |     - Fix hotel_id placeholder
  v
FASE 2: SERVICES LAYER                         [ ] 2-3 ore
  |     - RoomService completo
  |     - HousekeepingService completo
  |     - Logica business centralizzata
  v
FASE 3: TRIGGER AUTOMATICI                     [ ] 2-3 ore
  |     - Check-out -> dirty automatico
  |     - Pulizia completata -> clean
  |     - Task auto-create
  v
FASE 4: FRONTEND ROOM-MANAGER                  [ ] 3-4 ore
  |     - Dashboard governante completa
  |     - Task management UI
  |     - Floor plan visualizzazione
  v
FASE 5: TEST & DEPLOY                          [ ] 2-3 ore
  |     - Test tutti gli endpoint
  |     - Verifica planning.html ancora funziona
  |     - Deploy produzione
  v
+================================================================+
|   MILESTONE: ROOM MANAGER v1.0 LIVE!         TOTALE: 14-18 ore |
+================================================================+
  |
  v
FASE 6: VDA HARDWARE (FUTURO)
        - Studio protocolli VDA
        - Bridge VDA -> Miracollo
        - Sensori real-time
        - "HACKER MODE" (nel buon senso!)

+================================================================+
```

---

## DETTAGLIO FASI

### FASE 0: DECISIONI (1 ora)

```
INPUT:  Questo documento
OUTPUT: Decisioni confermate

AZIONI:
[ ] Leggere raccomandazioni Ingegnera
[ ] Decidere Opzione A vs B (stati camera)
[ ] Decidere frontend unificato vs separato
[ ] Confermare ordine fasi

BLOCCANTE: Senza decisioni non si procede!
```

---

### FASE 1: CONSOLIDAMENTO BACKEND (4-5 ore)

```
INPUT:  Branch feature/room-manager
OUTPUT: Router unificato /api/housekeeping

AZIONI:
[ ] Creare housekeeping_v2.py (consolidato)
[ ] Migrare endpoint legacy
[ ] Implementare nuovi endpoint:
    - GET /tasks
    - POST /tasks
    - GET /maintenance
    - POST /maintenance
[ ] Fix hotel_id placeholder (11 occorrenze!)
[ ] Test: planning.html ancora funziona

WORKER: cervella-backend
```

---

### FASE 2: SERVICES LAYER (2-3 ore)

```
INPUT:  services.py esistente (369 righe)
OUTPUT: Services completi

AZIONI:
[ ] Completare RoomService:
    - get_room_status()
    - update_room_status()
    - get_rooms_by_floor()
    - get_status_history()
[ ] Completare HousekeepingService:
    - create_task()
    - assign_task()
    - complete_task() -> auto-update room status
    - create_maintenance_request()

WORKER: cervella-backend
DIPENDE DA: FASE 1
```

---

### FASE 3: TRIGGER AUTOMATICI (2-3 ore)

```
INPUT:  Services completati
OUTPUT: Automazione workflow

TRIGGER DA IMPLEMENTARE:

1. CHECK-OUT COMPLETATO:
   booking.complete_checkout()
     -> room.status = 'vacant'
     -> room.housekeeping_status = 'dirty'
     -> auto-create task 'checkout_clean'

2. PULIZIA COMPLETATA:
   housekeeping.complete_task()
     -> room.housekeeping_status = 'clean'
     -> if room.status == 'vacant':
           room.status = 'vacant_clean'

3. CHECK-IN:
   booking.complete_checkin()
     -> verify room.housekeeping_status == 'clean'
     -> if not clean: WARNING!

WORKER: cervella-backend
DIPENDE DA: FASE 2
```

---

### FASE 4: FRONTEND ROOM-MANAGER (3-4 ore)

```
INPUT:  API funzionanti (FASE 1-3)
OUTPUT: Dashboard governante completa

AZIONI:
[ ] Collegare a /api/housekeeping (unificato)
[ ] Task Management UI:
    - Lista task pending
    - Assign to personale
    - Mark complete
[ ] Maintenance UI:
    - Lista richieste
    - Priorita (urgent, high, medium, low)
    - Status tracking
[ ] Floor Plan:
    - Vista per piano
    - Colori per stato (clean=verde, dirty=rosso)
    - Click per dettagli

WORKER: cervella-frontend
DIPENDE DA: FASE 1 (API)
```

---

### FASE 5: TEST & DEPLOY (2-3 ore)

```
INPUT:  Tutto completato
OUTPUT: Room Manager LIVE in produzione!

AZIONI:
[ ] Test automatici endpoint
[ ] Test manuale workflow completo:
    - Check-out -> dirty -> task -> clean
[ ] Verifica planning.html ANCORA FUNZIONA!
[ ] Merge feature/room-manager -> main
[ ] Deploy produzione
[ ] Smoke test produzione

WORKER: cervella-tester + cervella-devops
GUARDIANA: cervella-guardiana-qualita (verifica finale)
```

---

### FASE 6: VDA HARDWARE (FUTURO)

```
+================================================================+
|   QUESTA FASE E' IL VANTAGGIO COMPETITIVO!                     |
|   Nessun competitor (Mews, Cloudbeds, OPERA) ha VDA nativo!    |
+================================================================+

SITUAZIONE:
- Server VDA: COLLEGATO (abbiamo accesso!)
- Hardware: INSTALLATO in hotel
- Portale: https://room-manager.rc-onair.com

STRATEGIA "HACKER ETICO":
1. Mappare dispositivi VDA
2. Studiare protocolli (probabilmente Modbus legacy)
3. Creare bridge VDA -> Miracollo (MQTT?)
4. Sync room status real-time
5. TEST TEST TEST!

OPPORTUNITA:
- Sensori presenza (camera occupata?)
- Termostati (energia quando vuota)
- Serrature smart (check-in keyless)
- Luci automatiche

TEMPO: Da definire (ricerca + sviluppo)
DIPENDE DA: FASE 1-5 completate
```

---

## VALORE AGGIUNTO ROOM MANAGER

```
COSA ABBIAMO CHE I COMPETITOR NON HANNO:

1. TASK SYSTEM (NUOVO!)
   housekeeping_tasks
   - Assegnazione personale
   - Tracking completamento
   - Storico task

2. MAINTENANCE TRACKING (NUOVO!)
   maintenance_requests
   - Richieste manutenzione
   - Priorita e status
   - Assignment tecnici

3. AUDIT TRAIL (NUOVO!)
   room_status_history
   - Chi ha cambiato cosa
   - Quando
   - Compliance garantita

4. VDA INTEGRATION (FUTURO!)
   - Nessun competitor ce l'ha
   - Hardware GIA' installato
   - Vantaggio ENORME
```

---

## CONFRONTO COMPETITOR

```
| Feature              | Mews | Cloudbeds | OPERA | MIRACOLLO |
|----------------------|------|-----------|-------|-----------|
| Task System          |  OK  |    OK     |  OK   |   NUOVO!  |
| Maintenance          |  OK  |    NO     |  OK   |   NUOVO!  |
| Audit Trail          |  OK  |  Parziale |  OK   |   NUOVO!  |
| VDA Hardware         |  NO  |    NO     |  NO   |   SI!!!   |
| Revenue Integration  | Plugin| Plugin   |Separato| NATIVO!  |
| Setup Fees           | $$$  |    $$     | $$$$  |   ZERO    |
```

---

## TIMELINE SUGGERITA

```
SESSIONE 208 (prossima):
  [ ] FASE 0: Decisioni Rafa
  [ ] FASE 1: Inizio consolidamento backend

SESSIONE 209:
  [ ] FASE 1: Completamento backend
  [ ] FASE 2: Services layer

SESSIONE 210:
  [ ] FASE 3: Trigger automatici
  [ ] FASE 4: Inizio frontend

SESSIONE 211:
  [ ] FASE 4: Completamento frontend
  [ ] FASE 5: Test & Deploy

SESSIONE 212+:
  [ ] FASE 6: VDA Hardware exploration
```

---

## METRICHE SUCCESSO

```
ROOM MANAGER v1.0 E' SUCCESSO QUANDO:

[ ] Task housekeeping funzionano end-to-end
[ ] Governante puo vedere e completare task
[ ] Check-out -> dirty automatico
[ ] Pulizia -> clean automatico
[ ] planning.html ANCORA FUNZIONA (backward compatible)
[ ] Zero errori console
[ ] Response time < 200ms
```

---

## PRINCIPI GUIDA

```
+================================================================+
|                                                                |
|   "Non ci sono cose difficili, ci sono cose non studiate!"     |
|                                                                |
|   "Fatto BENE > Fatto VELOCE"                                  |
|                                                                |
|   "Una cosa alla volta, 100000%!"                              |
|                                                                |
|   "Il lato TANGIBILE di Miracollo!"                            |
|                                                                |
+================================================================+
```

---

## PROSSIMO STEP

**Rafa, confermi le decisioni?**

1. [ ] Opzione B: Due campi separati (status + housekeeping_status)
2. [ ] Frontend separati: planning.html + room-manager.html
3. [ ] Ordine fasi: 0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6

**Quando confermi, PARTIAMO!**

---

*Piano creato da: Regina + Guardiana Qualita + Ingegnera + Researcher*
*"Il team che lavora insieme, vince insieme!"*

