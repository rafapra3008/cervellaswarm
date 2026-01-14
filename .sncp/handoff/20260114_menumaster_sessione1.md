# HANDOFF - MenuMaster Sessione 1

> **Data:** 14 Gennaio 2026
> **Sessione:** 196
> **Progetto:** MenuMaster (NUOVO!)

---

## COPIA-INCOLLA PER NUOVA SESSIONE

```
Ciao! Continuo il progetto MENUMASTER.

DOVE SIAMO:
- Sessione 196 completata
- MVP prototipo FUNZIONANTE!
- Backend: Auth + Categories + Dishes (testato!)
- Frontend: struttura pronta, da collegare

LEGGI:
1. .sncp/progetti/menumaster/stato.md
2. /Users/rafapra/Developer/MenuMaster/docs/ROADMAP.md

PROSSIMI STEP (Sprint 2):
1. Frontend collegato a API reali
2. QR Code generation completo
3. Public menu view
4. Image upload (Cloudflare R2)

COME AVVIARE:
cd /Users/rafapra/Developer/MenuMaster
make dev   # Backend su :8000, Frontend: cd frontend && npm run dev -> :5173

NOTA: Questo e un progetto NUOVO separato da Miracollo!
Path: /Users/rafapra/Developer/MenuMaster/
```

---

## STATO TECNICO

### Backend (FUNZIONANTE)
- FastAPI + PostgreSQL 15
- 3 Alembic migrations applicate
- Auth JWT: register, login, me
- CRUD Categories con tenant isolation
- CRUD Dishes con tenant isolation
- QR endpoints implementati (da testare)

### Frontend (STRUTTURA PRONTA)
- Vite + React 18 + TypeScript + Tailwind
- 5 pagine: Login, Register, Dashboard, MenuEditor, PublicMenu
- API client creato, da collegare
- Build production OK

### Docker (PRONTO)
- docker-compose.yml (dev)
- docker-compose.prod.yml (prod)
- Makefile con 20+ comandi

---

## BUG RISOLTI

| Bug | Fix |
|-----|-----|
| Enum FREE vs free | `values_callable` in SQLAlchemy |
| bcrypt/passlib | Pin `bcrypt==4.0.1` |
| Tabelle mancanti | Migration `20260114_0003` |
| Tenant isolation | Aggiunti `tenant_id` ai models e filtri alle API |

---

## FILE IMPORTANTI

```
/Users/rafapra/Developer/MenuMaster/
├── backend/
│   ├── app/main.py              # Entry point
│   ├── app/api/v1/              # Endpoints
│   ├── app/models/              # SQLAlchemy models
│   └── alembic/versions/        # Migrations
├── frontend/
│   ├── src/pages/               # React pages
│   └── src/api/                 # API client
├── docs/ROADMAP.md              # Piano lavoro
└── docker-compose.yml
```

---

## CERVELLE USATE

Researcher, Ingegnera, Marketing, Guardiana Ricerca, Backend, Frontend, Guardiana Ops, Tester, Guardiana Qualita

---

*"Menu digitale professionale in 5 minuti"*
