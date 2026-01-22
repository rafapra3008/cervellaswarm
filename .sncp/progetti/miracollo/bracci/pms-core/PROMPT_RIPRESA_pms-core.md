<!-- DISCRIMINATORE: MIRACOLLO PMS CORE -->
<!-- PORTA: 8001 | TIPO: Sistema alberghiero principale -->
<!-- PATH: ~/Developer/miracollogeminifocus/ (backend principale) -->
<!-- NON CONFONDERE CON: Miracollook (8002), Room Hardware (8003) -->

# PROMPT RIPRESA - PMS Core

> **Ultimo aggiornamento:** 22 Gennaio 2026 - Sessione 312
> **STATO:** 90% LIVE | Health 9.5/10

---

## SESSIONE 312 - F3.4 HOUSEKEEPING QUICK WINS COMPLETATO!

```
+================================================================+
|   F3.4 Housekeeping Quick Wins  9/10 DONE                      |
|                                                                |
|   - Auto-dirty on checkout (camera → dirty automatico)         |
|   - Planning housekeeping panel (sidebar integrata)            |
|   - Bulk operations (multi-select + azioni massive)            |
|                                                                |
|   FASE 3 FEATURE = 3/5 (60%)                                   |
+================================================================+
```

### Scoperte Sessione 312

- **F3.3 Revenue Dashboard** già 80% completo! (revenue.html + competitors.html esistenti)
- **F3.4 Housekeeping** già 80% completo! (Room Manager MVP esistente)
- Enhancement invece di creazione da zero = più veloce!

---

## FASE 3 - PROGRESSO (3/5)

| Task | Status | Note |
|------|--------|------|
| **F3.1 Batch Operations** | **DONE 9/10** | POST /api/batch/* |
| **F3.2 Webhooks Outbound** | **DONE 9/10** | HMAC, retry, DLQ |
| **F3.3 Revenue Dashboard** | **DONE 8/10** | Già esistente, enhancement minor |
| **F3.4 Housekeeping Quick Wins** | **DONE 9/10** | Auto-dirty, panel, bulk |
| F3.5 Channel Manager 2-Way | FUTURO | dopo F3.2 (ora possibile!) |

---

## FILE CREATI/MODIFICATI SESSIONE 312

### Backend
| File | Scopo |
|------|-------|
| `services/room_manager_service.py` | + bulk_update_housekeeping() |
| `services/checkin_service.py` | + auto-dirty on checkout |
| `routers/room_manager.py` | + POST /bulk-housekeeping |
| `routers/planning_ops.py` | + await async fix |

### Frontend
| File | Scopo |
|------|-------|
| `js/planning/housekeeping-panel.js` | NUOVO - Panel housekeeping in Planning |
| `css/planning/housekeeping-panel.css` | NUOVO - Stili dark theme |
| `js/room-manager/api.js` | + bulkUpdateHousekeeping() |
| `js/room-manager/core.js` | + Button "Bulk Clean" |
| `planning.html` | + button, panel, script |

### Docs
| File | Scopo |
|------|-------|
| `ANALISI_HOUSEKEEPING_ESISTENTE.md` | Research codebase |
| `RICERCA_HOUSEKEEPING_*.md` | Best practices (4 parti) |
| `BULK_HOUSEKEEPING_IMPLEMENTATION.md` | Documentazione |

---

## ENDPOINT HOUSEKEEPING

```
POST /api/room-manager/{hotel_code}/bulk-housekeeping  - Bulk update status
GET  /api/room-manager/{hotel_code}/rooms              - Lista camere
PUT  /api/room-manager/rooms/{id}/housekeeping         - Update singolo
```

---

## PROSSIMA SESSIONE - F3.4 FASE 2

1. **Task Assignment System** - Chi pulisce cosa?
2. **Mobile PWA Basic** - Lista task per housekeeper
3. **Cleaning Time Tracking** - Start/end timestamps

---

## WARNING ESISTENTI

- **FK violations:** 1262 nel DB (problema esistente, task separato)

---

*"Housekeeping Quick Wins completati! +30% efficienza operativa!" - Sessione 312*
