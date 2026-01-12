# DEPLOY What-If Simulator - FASE 1
> Creato: 12 Gennaio 2026
> Status: PRONTO PER DEPLOY

---

## FILE CREATI

```
moduli/whatif/
├── schemas_what_if.py      -> backend/schemas/what_if.py
├── services_what_if_calculator.py -> backend/services/what_if_calculator.py
├── routers_what_if_api.py  -> backend/routers/what_if_api.py
└── DEPLOY_INSTRUCTIONS.md  (questo file)
```

---

## STEP 1: Copia File sulla VM

```bash
# SSH alla VM
ssh miracollo-cervella

# Vai al backend
cd /app/miracollo/backend

# Crea backup (opzionale ma consigliato)
cp -r routers routers.backup.20260112
cp -r services services.backup.20260112
cp -r schemas schemas.backup.20260112
```

### Copia file (da locale a VM)

```bash
# Dal tuo Mac:
scp .sncp/progetti/miracollo/moduli/whatif/schemas_what_if.py \
    miracollo-cervella:/app/miracollo/backend/schemas/what_if.py

scp .sncp/progetti/miracollo/moduli/whatif/services_what_if_calculator.py \
    miracollo-cervella:/app/miracollo/backend/services/what_if_calculator.py

scp .sncp/progetti/miracollo/moduli/whatif/routers_what_if_api.py \
    miracollo-cervella:/app/miracollo/backend/routers/what_if_api.py
```

---

## STEP 2: Modifica main.py (2 righe)

```bash
ssh miracollo-cervella
cd /app/miracollo/backend
nano main.py
```

### AGGIUNTA 1: Import (cerca la sezione import routers)

```python
# Aggiungi questa riga con gli altri import router:
from routers import what_if_api
```

### AGGIUNTA 2: Registrazione (cerca app.include_router)

```python
# Aggiungi questa riga con le altre registrazioni:
app.include_router(what_if_api.router, tags=["What-If"])
```

---

## STEP 3: Restart Backend

```bash
# Restart container
docker restart miracollo-backend

# Oppure se non usi Docker:
# systemctl restart miracollo-backend

# Verifica logs
docker logs miracollo-backend -f --tail 50
```

---

## STEP 4: Test

### Test Health
```bash
curl https://miracollo.com/api/v1/what-if/health
```

**Expected:**
```json
{
    "status": "healthy",
    "module": "what-if-simulator",
    "version": "1.0.0"
}
```

### Test Simulate
```bash
curl -X POST https://miracollo.com/api/v1/what-if/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "property_id": 42,
    "date_target": "2026-01-20",
    "room_type_id": 3,
    "price_adjustment": 0.10
  }'
```

### Test Price Curve
```bash
curl "https://miracollo.com/api/v1/what-if/price-curve?property_id=42&date_target=2026-01-20&room_type_id=3"
```

---

## ROLLBACK (se problemi)

```bash
# Rimuovi le 2 righe aggiunte a main.py
# Oppure:
docker restart miracollo-backend

# Se backup fatto:
rm routers/what_if_api.py
rm services/what_if_calculator.py
rm schemas/what_if.py
docker restart miracollo-backend
```

---

## CHECKLIST FINALE

```
[ ] File copiati sulla VM
[ ] main.py modificato (2 righe)
[ ] Backend restartato
[ ] Health check OK
[ ] Simulate test OK
[ ] Price-curve test OK
```

---

## DOPO DEPLOY

Quando FASE 1 funziona:
1. Aggiorna stato.md Miracollo
2. Procedi con FASE 2 (Frontend UI)

---

*"Una cosa alla volta, fatta BENE!"*
