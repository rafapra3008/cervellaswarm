# PROMPT SESSIONE LOCALE - Room Manager

> **Prima di iniziare, Rafa deve fare il setup (vedi sotto)**

---

## SETUP (Una Tantum)

```bash
# 1. Vai nella cartella Developer
cd ~/Developer

# 2. Rimuovi vecchio miracollo locale (non è git)
rm -rf miracollogeminifocus

# 3. Clona da GitHub (fresco)
git clone https://github.com/rafapra3008/miracollogeminifocus.git

# 4. Vai nel repo
cd miracollogeminifocus

# 5. Crea cartella worktrees
mkdir -p ../miracollo-worktrees

# 6. Crea worktree per Room Manager
git worktree add -b feature/room-manager ../miracollo-worktrees/room-manager

# 7. Vai nel worktree
cd ../miracollo-worktrees/room-manager

# 8. Lancia Claude
claude
```

---

## PROMPT DA INCOLLARE

```
SEI CERVELLA-BACKEND + CERVELLA-FRONTEND in sessione PARALLELA IBRIDA.

CONTESTO:
- Questa è una sessione di SVILUPPO MODULO NUOVO in locale
- In parallelo, un'altra Cervella lavora sui GAP fix sulla VM
- NON vi toccate mai (tu codice nuovo, lei codice esistente)

IL TUO AMBIENTE:
- Path: ~/Developer/miracollo-worktrees/room-manager/
- Branch: feature/room-manager
- Database: Nessuno per ora (design only)

IL TUO TASK: Modulo Room Manager COMPLETO

FASE 1 - DESIGN (oggi):
1. Analizza struttura Miracollo esistente (routers, models, frontend)
2. Crea piano dettagliato Room Manager
3. Documenta API design in docs/room_manager_api.md

FASE 2 - BACKEND (oggi se tempo):
1. Crea struttura: backend/routers/room_manager/
   ├── __init__.py
   ├── router.py
   ├── models.py
   ├── schemas.py
   └── services.py

2. Implementa:
   - GET /rooms - Lista camere
   - POST /rooms - Crea camera
   - GET /rooms/{id} - Dettaglio camera
   - PUT /rooms/{id} - Aggiorna camera
   - DELETE /rooms/{id} - Elimina camera

FASE 3 - FRONTEND (prossima sessione):
1. Crea struttura: frontend/pages/RoomManager/
2. Implementa UI base

REGOLE:
- Crea SOLO file NUOVI nella cartella room_manager/
- NON modificare codice esistente (main.py, App.jsx, etc.)
- I collegamenti li faremo in fase DEPLOY
- Commit frequenti: git add . && git commit -m "Feat: descrizione"

LOG SESSIONE:
Alla fine, scrivi riepilogo in: docs/SESSIONE_ROOM_MANAGER_20260111.md

INIZIA: Leggi la struttura esistente di Miracollo per capire i pattern.
```

---

## Note per Rafa

- Se il setup fallisce, chiedi alla Regina
- Il worktree è SEPARATO dal repo principale
- Puoi lavorare in parallelo senza conflitti
- Quando finisci: `git push origin feature/room-manager`
