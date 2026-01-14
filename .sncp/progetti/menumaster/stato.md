# MenuMaster - Stato Progetto

> **Ultimo aggiornamento:** 14 Gennaio 2026 - Sessione 2 (Checkpoint)
> **Status:** SPRINT 2 COMPLETATO - GUARDIANA QUALITA 8/10

---

## VISIONE

```
+================================================================+
|                                                                |
|   MenuMaster = Sistema Gestione Menu Digitali Ristoranti       |
|                                                                |
|   "Menu digitale professionale in 5 minuti"                    |
|   "Il Canva dei menu digitali"                                 |
|                                                                |
|   Target: Ristoranti piccoli/medi (5-50 coperti)               |
|   USP: Zero commissioni, AI translations, self-hosted option   |
|                                                                |
+================================================================+
```

---

## SPRINT 2 COMPLETATO

### 1. Frontend Collegato a Backend
- Auth API (login, register, me) funzionanti
- Types allineati: `name_translations`, `base_price`, `description_translations`
- React Query hooks per Categories e Dishes
- `getTranslation()` helper per multi-lingua
- Zustand store per auth state

### 2. QR Code System
- Backend: genera, lista, update, delete QR codes
- Download: PNG (600x600), SVG, PDF con branding
- Frontend: pagina `/qr-codes` nel dashboard
- Ogni QR ha URL unico per menu pubblico

### 3. Public Menu View
- API pubbliche senza auth: `/public/menu/{slug}/categories`, `/dishes`
- Pagina mobile-first con category tabs sticky
- DishCard e DishModal con traduzioni
- Filtro automatico piatti non disponibili

### 4. Image Upload (Local Placeholder)
- Backend: `storage_service.py` con Pillow processing
- Endpoint: `POST /api/v1/uploads/image`
- Frontend: `ImageUpload` component drag-and-drop
- Integrato in DishForm per foto piatti
- Pronto per conversione a Cloudflare R2

### 5. Bug Fix Post-Review
- `uploads.py`: fix import (`get_current_user` invece di `get_current_restaurant`)
- `qrApi.ts`: fix type (`url` invece di `qr_url`, aggiunto `code`)
- `MenuEditor.tsx`: rimosso `as any`, usa `DishCreate` con validazione

---

## COME AVVIARE (TESTATO!)

```bash
# 1. Backend (Docker)
cd /Users/rafapra/Developer/MenuMaster
docker-compose up -d
# Verifica: http://localhost:8000/docs

# 2. Frontend (Dev Server)
cd /Users/rafapra/Developer/MenuMaster/frontend
npm run dev
# Apri: http://localhost:5173

# 3. Menu Pubblico Demo
http://localhost:5173/menu/demo-ristorante-1768381547
```

### Credenziali Demo
```
Email: demo@menumaster.com
Password: demo123456
```

---

## API ENDPOINTS FUNZIONANTI

| Endpoint | Metodo | Auth | Status |
|----------|--------|------|--------|
| `/api/v1/auth/register` | POST | No | OK |
| `/api/v1/auth/login` | POST | No | OK |
| `/api/v1/auth/me` | GET | JWT | OK |
| `/api/v1/categories` | CRUD | JWT | OK |
| `/api/v1/dishes` | CRUD | JWT | OK |
| `/api/v1/qr/generate` | POST | JWT | OK |
| `/api/v1/qr/codes` | GET | JWT | OK |
| `/api/v1/qr/codes/{id}/download` | GET | JWT | OK (PNG) |
| `/api/v1/qr/codes/{id}/download/svg` | GET | JWT | OK |
| `/api/v1/qr/codes/{id}/download/pdf` | GET | JWT | OK |
| `/api/v1/uploads/image` | POST | JWT | OK |
| `/api/v1/public/menu/{slug}/categories` | GET | No | OK |
| `/api/v1/public/menu/{slug}/dishes` | GET | No | OK |

---

## DATI DEMO NEL DATABASE

```
Tenants: 3
  - demo-ristorante-1768381547 (Demo Ristorante)
  - test-ristorante-1768381533
  - pizzeria-bella

Categorie: 5
  - Antipasti, Primi Piatti, Secondi Piatti, Dolci

Piatti: 5
  - Bruschetta al Pomodoro (EUR 6.50)
  - Spaghetti alla Carbonara (EUR 14.00)
  - Risotto ai Funghi Porcini (EUR 16.00)
  - Tiramisu (EUR 7.00)
  - (+ altri)

QR Codes: 1
  - vq2w2o (Tavolo 1)
```

---

## FRONTEND PAGES

| Route | Pagina | Status |
|-------|--------|--------|
| `/login` | Login | OK |
| `/register` | Registrazione | OK |
| `/dashboard` | Dashboard overview | OK |
| `/menu-editor` | Editor categorie/piatti | OK |
| `/qr-codes` | Gestione QR codes | OK |
| `/menu/{slug}` | Menu pubblico | OK |

---

## PROSSIMI STEP (Sprint 3)

1. **Polish UI/UX**
   - Toast notifications (react-hot-toast?)
   - Loading skeletons
   - Error boundaries

2. **Testing**
   - pytest per backend
   - Playwright per E2E frontend

3. **Multi-tenancy**
   - Fix TODO nel backend (slug hardcoded "demo")
   - Tenant isolation completa

4. **Deploy**
   - Railway/Fly.io
   - Cloudflare R2 per immagini
   - Domain menumaster.app

---

## PATH PROGETTO

```
/Users/rafapra/Developer/MenuMaster/
├── backend/
│   ├── app/
│   │   ├── api/v1/        # auth, categories, dishes, qr, uploads, public
│   │   ├── models/        # user, tenant, category, dish, qr_code
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # qr_service, storage_service
│   │   └── core/          # auth, security
│   ├── static/uploads/    # Local image storage
│   ├── alembic/           # 3 migrations
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/           # authApi, menuApi, qrApi, uploadApi
│   │   ├── components/    # ui/, menu/
│   │   ├── hooks/         # useMenu, useQR, useToast
│   │   ├── pages/         # Login, Register, Dashboard, MenuEditor, QRCodes, PublicMenu
│   │   ├── store/         # authStore, menuStore
│   │   └── types/         # TypeScript types
│   └── dist/              # Build: 324KB JS, 20KB CSS
├── research/              # Competitor, UX analysis
├── docs/                  # ROADMAP, architettura
└── docker-compose.yml
```

---

## DECISIONI ARCHITETTURALI

| Decisione | Perche |
|-----------|--------|
| `name_translations` multi-lingua | Pronto per AI translations future |
| Local upload poi R2 | MVP veloce, upgrade facile |
| React Query + Zustand | State management pulito e performante |
| Public API senza auth | Menu accessibile da QR scan |
| Schema `global` PostgreSQL | Tenant isolation forte |

---

## NOTE TECNICHE

- **Workbox warning**: NON e bug del codice, e service worker residuo browser
  - Fix: DevTools > Application > Service Workers > Unregister
- **TODO backend**: 4 placeholder per multi-tenant (slug hardcoded "demo")
- **console.error**: 4 occorrenze per error handling (OK in produzione)

---

*"Menu digitale professionale in 5 minuti"*
*MenuMaster - Sprint 2 COMPLETATO!*
*Guardiana Qualita: 8/10 APPROVED*
*"Ultrapassar os proprios limites!"*
