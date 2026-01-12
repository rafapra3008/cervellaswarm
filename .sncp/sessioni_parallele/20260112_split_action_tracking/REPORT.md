# SESSIONE PARALLELA: Split action_tracking_api.py

**Data:** 2026-01-12
**Agente:** cervella-backend
**Durata:** ~20 minuti

---

## MISSIONE

Split del file `backend/routers/action_tracking_api.py` (962 righe) in 3 file modulari.

---

## RISULTATO: COMPLETATO

### File Creati

| File | Righe | Descrizione |
|------|-------|-------------|
| `action_tracking_api.py` | 350 | Router + Models + Thin endpoints |
| `action_tracking_service.py` | 515 | Business logic (snapshot, validation, lists) |
| `action_tracking_rollback.py` | 414 | Rollback logic (undo, pause, restore) |
| **TOTALE** | **1279** | vs 962 originali (+33% per modularità) |

### Struttura Nuovo Codice

```
backend/routers/
├── action_tracking_api.py        # Router endpoints (thin)
│   ├── ApplySuggestionRequest    # Pydantic models
│   ├── ApplySuggestionResponse
│   ├── RollbackRequest
│   └── 10 endpoints              # Tutti delegano a service/rollback
│
├── action_tracking_service.py    # Business logic
│   ├── get_snapshot_before()
│   ├── apply_pricing_change()    # DEPRECATED
│   ├── validate_suggestion()
│   ├── create_pricing_version()
│   ├── create_suggestion_application()
│   ├── get_application_list()
│   ├── get_application_detail()
│   ├── get_monitoring_data()
│   └── get_export_report()
│
└── action_tracking_rollback.py   # Rollback logic
    ├── restore_previous_prices()
    ├── perform_undo()
    ├── perform_pause()
    ├── perform_resume()
    ├── perform_rollback()
    └── perform_restore()
```

### Endpoint API (10 totali)

1. `POST /api/suggestions/apply` - Applica suggerimento
2. `GET /api/suggestions/applications` - Lista applicazioni
3. `GET /api/suggestions/applications/{id}` - Dettaglio
4. `POST /api/suggestions/applications/{id}/undo` - Undo (10s)
5. `POST /api/suggestions/applications/{id}/pause` - Pausa
6. `POST /api/suggestions/applications/{id}/resume` - Riprende
7. `POST /api/suggestions/applications/{id}/rollback` - Rollback
8. `POST /api/suggestions/applications/{id}/restore` - Ripristina
9. `GET /api/suggestions/applications/{id}/monitoring` - Dashboard
10. `GET /api/suggestions/applications/{id}/export` - Export JSON

---

## TEST

```
Container: miracollo-backend-12
Status: 200 OK
Count: 6 applications
Import: All modules OK
Routes: 10 registered
```

**NOTA:** Il container 35 (quello esposto su porta 8001) ha un database più vecchio senza le migrazioni. Il codice split funziona correttamente nel container 12.

---

## FIX APPLICATI

1. **Colonna `rt.nome` -> `rt.name`**: La tabella `room_types` ha colonna `name`, non `nome`

---

## FILE SU VM

```
/app/miracollo/backend/routers/action_tracking_api.py
/app/miracollo/backend/routers/action_tracking_service.py
/app/miracollo/backend/routers/action_tracking_rollback.py
/app/miracollo/backend/routers/action_tracking_api.py.backup  # Original
```

---

## PROSSIMI STEP

1. [ ] Deploy container 12 sulla porta 8001 (o migrare DB container 35)
2. [ ] Push su GitHub dopo deploy confermato
3. [ ] Split simile per `revenue.js` (frontend)

---

*Report generato da cervella-backend*
