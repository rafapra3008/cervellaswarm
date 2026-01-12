# PROTOCOLLO IBRIDO DEFINITIVO - VM + Locale + Lab

> **Data:** 11 Gennaio 2026 - Sessione 168
> **Autori:** Regina + Guardiana Qualita + Rafa
> **Status:** APPROVATO
> **Applicazione:** Miracollo (estendibile a tutti i progetti)

---

## EXECUTIVE SUMMARY

```
+==================================================================+
|                                                                  |
|   WORKFLOW IBRIDO CERVELLASWARM                                  |
|                                                                  |
|   LOCALE    = Sviluppo MODULI COMPLETI (blocchi interi)          |
|   LAB (VM)  = Test volatile (Docker, reset facile)               |
|   PROD (VM) = Produzione SACRA (solo plug-in, mai sostituire)    |
|                                                                  |
|   FILOSOFIA: Aggiungere, MAI sostituire                          |
|                                                                  |
+==================================================================+
```

---

## 1. I TRE AMBIENTI

### 1.1 LOCALE (MacBook)

```
SCOPO: Sviluppo moduli completi
COSA: Room Manager, Email System, WhatsApp, etc.
COME: Git worktrees per parallelismo
DB: miracollo_dev.db (dati fake)

REGOLA: Un modulo = UN blocco completo
        NON fix piccoli, NON modifiche sparse
```

### 1.2 LAB (Docker su VM)

```
SCOPO: Test prima di produzione
COSA: Verifica modulo funziona con ambiente reale
COME: Docker container separato (porta 8001)
DB: miracollo_lab.db (VOLATILE - reset quando serve)

REGOLA: Rompi quanto vuoi, reset in 30 secondi
        MAI tocca produzione
```

### 1.3 PRODUZIONE (VM principale)

```
SCOPO: Sistema live per utenti
COSA: Miracollo funzionante
COME: Docker container (porta 8000)
DB: miracollo.db (DATI REALI - SACRO!)

REGOLA: Solo AGGIUNGERE moduli nuovi
        MAI sostituire codice esistente
        Solo COLLEGAMENTI minimi
```

---

## 2. STRUTTURA VM

```
VM miracollo-cervella (34.27.179.164)
│
├── /app/miracollo/                    # PRODUZIONE
│   ├── backend/
│   │   ├── routers/
│   │   │   ├── revenue.py             # Esistente
│   │   │   ├── properties.py          # Esistente
│   │   │   └── room_manager/          # NUOVO (plug-in)
│   │   ├── data/
│   │   │   └── miracollo.db           # DB PRODUZIONE
│   │   └── main.py
│   └── frontend/
│
├── /app/miracollo-lab/                # LABORATORIO
│   ├── backend/
│   │   ├── data/
│   │   │   └── miracollo_lab.db       # DB LAB (volatile)
│   │   └── ...
│   └── frontend/
│
└── docker-compose.yml
    ├── miracollo-backend      (porta 8000)  # PROD
    ├── miracollo-frontend     (porta 80)    # PROD
    ├── miracollo-lab-backend  (porta 8001)  # LAB
    └── miracollo-lab-frontend (porta 3001)  # LAB
```

---

## 3. WORKFLOW COMPLETO

### Fase 1: Sviluppo Locale (MODULO COMPLETO)

```
1. SYNC con VM
   git pull origin main

2. CREA WORKTREE per il modulo
   git worktree add -b feature/room-manager ../miracollo-worktrees/room-manager

3. SVILUPPA il modulo INTERO
   backend/routers/room_manager/
   ├── __init__.py
   ├── router.py
   ├── models.py
   ├── schemas.py
   └── services.py

   frontend/pages/RoomManager/
   ├── index.jsx
   ├── components/
   └── hooks/

4. TEST locale
   pytest backend/tests/room_manager/
   npm test (frontend)

5. COMMIT quando completo
   git add . && git commit -m "Feat: Room Manager module complete"
   git push origin feature/room-manager
```

### Fase 2: Test su Lab (VOLATILE)

```
1. DEPLOY su Lab
   ssh miracollo-cervella
   cd /app/miracollo-lab
   git pull origin feature/room-manager

2. RESET Lab DB (se serve)
   ./scripts/reset-lab-db.sh

3. RUN Lab
   docker restart miracollo-lab-backend

4. TEST su Lab
   curl http://localhost:8001/api/room-manager/rooms
   - Testa tutte le funzionalita
   - Rompi quanto vuoi
   - Se problemi: fix locale, ripeti

5. SE OK: Procedi a Fase 3
   SE KO: Reset lab, fix locale, ripeti
```

### Fase 3: Deploy Produzione (PLUG-IN)

```
1. GUARDIANA approva codice

2. BACKUP produzione
   ./scripts/backup-prod-db.sh

3. COPIA modulo nuovo (NON sostituire!)
   cd /app/miracollo
   git pull origin feature/room-manager

4. AGGIUNGI collegamenti (2-3 righe max)

   main.py:
   + from routers.room_manager import router as room_manager_router
   + app.include_router(room_manager_router, prefix="/api/room-manager")

   App.jsx:
   + import RoomManager from './pages/RoomManager'
   + <Route path="/room-manager" element={<RoomManager />} />

   Sidebar.jsx:
   + { name: 'Room Manager', path: '/room-manager', icon: BedIcon }

5. RUN migrations (se presenti)
   alembic upgrade head

6. RESTART produzione
   docker restart miracollo-backend

7. VERIFICA
   curl https://miracollo.com/api/room-manager/rooms
   - Test smoke manuale
   - Monitor logs 30 min

8. MERGE e cleanup
   git checkout main
   git merge feature/room-manager
   git push origin main
   git worktree remove ../miracollo-worktrees/room-manager
```

---

## 4. LE 7 REGOLE FERREE

| # | Regola | Dettaglio |
|---|--------|-----------|
| 1 | **MODULI COMPLETI** | Locale sviluppa blocchi interi, mai pezzi sparsi |
| 2 | **MAI SOSTITUIRE** | Produzione: solo AGGIUNGERE, mai modificare esistente |
| 3 | **COLLEGAMENTI MINIMI** | Max 5-10 righe per collegare modulo nuovo |
| 4 | **LAB PRIMA DI PROD** | Sempre testare su Lab volatile prima |
| 5 | **MIGRATIONS SOLO LOCALE** | Creo locale, testo lab, applico prod |
| 6 | **HOTFIX = ECCEZIONE** | Se urgente su prod, commit immediato + documenta |
| 7 | **REGINA DECIDE DEPLOY** | Solo Regina (o Rafa) autorizza deploy prod |

---

## 5. SESSIONI PARALLELE

### Struttura

```
TERMINALE 1 (VM - Produzione)
├── Sessione: "miracollo-manutenzione"
├── Lavoro: GAP fix, bug, hotfix
├── Tocca: Codice ESISTENTE su VM
└── DB: miracollo.db

TERMINALE 2 (Locale - Sviluppo)
├── Sessione: "miracollo-room-manager"
├── Lavoro: Modulo Room Manager completo
├── Tocca: SOLO cartella room_manager/ (nuova)
└── DB: miracollo_dev.db locale

ZERO CONFLITTI: Non toccano mai gli stessi file!
```

### SNCP per Sessioni Parallele

```
.sncp/sessioni_parallele/
└── 20260111_miracollo_ibrido/
    ├── piano.md                    # Piano iniziale (Regina)
    ├── sessione_vm.md              # Log sessione VM
    ├── sessione_room_manager.md    # Log sessione locale
    ├── decisioni.md                # Decisioni prese
    └── riepilogo.md                # Riepilogo finale (Regina)

REGOLA: Ogni sessione scrive nel SUO file
        Regina consolida alla fine
```

### PROMPT_RIPRESA per Sessioni Parallele

```
Al termine delle sessioni parallele:

1. Regina legge tutti i log sessione
2. Regina aggiorna PROMPT_RIPRESA.md con:
   - Cosa fatto in ogni sessione
   - Stato moduli
   - Prossimi step
3. Regina aggiorna .sncp/stato/oggi.md
```

---

## 6. SETUP LAB DOCKER

### docker-compose.lab.yml

```yaml
version: '3.8'

services:
  miracollo-lab-backend:
    build: ./backend
    container_name: miracollo-lab-backend
    ports:
      - "8001:8000"
    environment:
      - ENVIRONMENT=lab
      - DATABASE_URL=sqlite:///./data/miracollo_lab.db
    volumes:
      - ./backend:/app
      - lab-data:/app/data
    restart: unless-stopped

  miracollo-lab-frontend:
    build: ./frontend
    container_name: miracollo-lab-frontend
    ports:
      - "3001:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8001
    volumes:
      - ./frontend:/app
    restart: unless-stopped

volumes:
  lab-data:
```

### Script Reset Lab

```bash
#!/bin/bash
# reset-lab.sh

echo "Resetting Lab environment..."

# Stop containers
docker-compose -f docker-compose.lab.yml down

# Remove lab database
rm -f /app/miracollo-lab/backend/data/miracollo_lab.db

# Recreate with seed data
docker-compose -f docker-compose.lab.yml up -d
sleep 5

# Run migrations
docker exec miracollo-lab-backend alembic upgrade head

# Seed fake data
docker exec miracollo-lab-backend python scripts/seed_lab_data.py

echo "Lab reset complete!"
```

---

## 7. CHECKLIST

### Pre-Sviluppo Locale

```
[ ] git pull da VM (sync)
[ ] Worktree creato per modulo
[ ] Struttura cartelle definita
[ ] Nessuna dipendenza da codice esistente (o minima)
```

### Pre-Deploy Lab

```
[ ] Modulo completo e testato locale
[ ] Commit pushato
[ ] Lab resettato (pulito)
```

### Pre-Deploy Produzione

```
[ ] Test Lab passati
[ ] Guardiana ha approvato
[ ] Backup produzione fatto
[ ] Collegamenti identificati (max 5-10 righe)
[ ] Rollback plan pronto
[ ] Regina autorizza
```

---

## 8. VANTAGGI QUESTO APPROCCIO

| Aspetto | Beneficio |
|---------|-----------|
| **Zero conflitti** | Locale e VM non toccano stessi file |
| **Parallelismo reale** | N sessioni contemporanee |
| **Sicurezza** | Lab volatile, prod mai a rischio |
| **Modularita** | Ogni feature e un blocco pulito |
| **Rollback facile** | Rimuovi import, modulo sparisce |
| **Scalabilita** | Aggiungi moduli senza limiti |

---

## 9. ESEMPIO PRATICO: Room Manager

### Struttura Modulo

```
backend/routers/room_manager/
├── __init__.py
│   └── from .router import router
├── router.py
│   └── @router.get("/rooms"), @router.post("/rooms"), etc.
├── models.py
│   └── class Room(Base), class RoomType(Base)
├── schemas.py
│   └── class RoomCreate, RoomResponse, etc.
└── services.py
    └── class RoomService (business logic)

frontend/pages/RoomManager/
├── index.jsx
│   └── Main page component
├── components/
│   ├── RoomList.jsx
│   ├── RoomForm.jsx
│   └── RoomCard.jsx
└── hooks/
    └── useRooms.js (API calls)
```

### Collegamenti Produzione (SOLO QUESTO)

```python
# main.py - AGGIUNTA (2 righe)
from routers.room_manager import router as room_manager_router
app.include_router(room_manager_router, prefix="/api/room-manager", tags=["Room Manager"])
```

```jsx
// App.jsx - AGGIUNTA (2 righe)
import RoomManager from './pages/RoomManager'
<Route path="/room-manager" element={<RoomManager />} />
```

```jsx
// Sidebar.jsx - AGGIUNTA (1 riga)
{ name: 'Room Manager', path: '/room-manager', icon: BedIcon }
```

**TOTALE: 5 righe modificate in produzione!**

---

## 10. PROSSIMI STEP

```
IMMEDIATO (Oggi):
[ ] Setup Lab Docker su VM
[ ] Creare script reset-lab.sh
[ ] Preparare prima sessione parallela

SESSIONE PARALLELA TEST:
[ ] Terminale 1: GAP #2, #3, #4 su VM
[ ] Terminale 2: Room Manager locale
[ ] Validare workflow funziona

DOPO VALIDAZIONE:
[ ] Documentare lezioni apprese
[ ] Raffinare protocollo se necessario
```

---

*"Moduli completi, plug-in puliti, zero casino!"*

*Sessione 168 - Regina, Guardiana & Rafa*
