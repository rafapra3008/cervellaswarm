<!-- DISCRIMINATORE: MIRACOLLOOK EMAIL CLIENT -->
<!-- PORTA: 8002 | TIPO: Email client AI per hotel -->
<!-- PATH: ~/Developer/miracollogeminifocus/miracallook/ -->
<!-- NON CONFONDERE CON: PMS Core (8001), Room Hardware (8003) -->

# PROMPT RIPRESA - Miracollook

> **Ultimo aggiornamento:** 30 Gennaio 2026 - Sessione 322
> **STATUS:** Guest Management 60% - Code Review + Security Fix completati

---

## SESSIONE 322 - CODE REVIEW + ARCHITETTURA CHIARITA

### Cosa Abbiamo Fatto

| # | Task | Risultato |
|---|------|-----------|
| 1 | Code Review S321 | 8.5/10 → 3 issue trovate |
| 2 | Fix LIKE injection | 10/10 - Security fix |
| 3 | Fix TOP default | 10/10 - Performance |
| 4 | Fix logging stati | 10/10 - Robustness |
| 5 | Test unitari | 18/18 PASS |
| 6 | **CHIARIMENTO ARCHITETTURA** | **Stessa rete = NO VPN!** |

### CHIARIMENTO IMPORTANTE

```
+================================================================+
|                                                                  |
|   ARCHITETTURA CORRETTA:                                        |
|                                                                  |
|   Miracollook backend gira nella STESSA RETE dell'hotel!        |
|                                                                  |
|   ❌ NON serve VPN                                               |
|   ❌ NON serve Raspberry Pi                                      |
|   ❌ NON serve partnership Ericsoft                              |
|   ✅ Accesso diretto read-only al DB                            |
|                                                                  |
+================================================================+
```

### Versioni Aggiornate

| File | Versione | Modifica |
|------|----------|----------|
| connector.py | 2.0.0 → 2.0.1 | LIKE sanitizer + logging |
| guest_queries.py | 1.0.0 → 1.0.1 | Costanti limite + warning |
| models/__init__.py | 1.0.0 → 1.0.1 | Export legacy models |

---

## STATO INTEGRAZIONE ERICSOFT

```
FASE 1: Connector Base        [####################] 100% ✅
FASE 2: Guest Management      [############........] 60%
FASE 3: Cache Layer           [....................] 0%
FASE 4: API Endpoints         [....................] 0%
FASE 5: Frontend Integration  [....................] 0%
FASE 6: Test & Production     [....................] 0%
```

### FASE 2 - Dettaglio

| Step | Status |
|------|--------|
| Modello GuestProfile | ✅ 540 righe |
| Query SQL Master | ✅ 443 righe |
| Connector v2.0.1 | ✅ 6 metodi nuovi |
| Security fix | ✅ S322 |
| Test unitari | ✅ 18/18 pass |
| **Test DB reale** | ⏳ **Da fare in hotel** |

---

## PROSSIMI STEP (S323+)

1. **Test DB reale** - Quando in hotel: `python test_guest_management.py`
2. **Cache Layer** - FASE 3 della subroadmap
3. **API Endpoints** - FASE 4 (GET /api/guests/*)
4. **Frontend** - GuestContextCard

---

## FILE CHIAVE

| File | Path |
|------|------|
| Connector | `miracallook/backend/ericsoft/connector.py` |
| GuestProfile | `miracallook/backend/ericsoft/models/guest_profile.py` |
| Query SQL | `miracallook/backend/ericsoft/queries/guest_queries.py` |
| Test unitari | `miracallook/backend/tests/test_guest_profile.py` |
| **SUBROADMAP** | `.sncp/progetti/miracollo/bracci/miracallook/SUBROADMAP_ERICSOFT_INTEGRATION.md` |

---

## CONNETTORE ERICSOFT v2.0.1

**Metodi disponibili:**
- `get_all_guests(limit)` - Tutti ospiti (4270!)
- `get_in_house_guests()` - In casa (~111)
- `get_guests_by_status(status)` - Per stato
- `get_post_stay_guests(days)` - Partiti
- `get_pre_arrival_guests(days)` - In arrivo
- `get_guest_by_id(id)` - Profilo completo

---

## SESSIONI PRECEDENTI

| Sessione | Cosa |
|----------|------|
| S322 | Code Review + Security Fix + Architettura chiarita |
| S321 | Implementazione GuestProfile + Query + Connector |
| S320 | Studio Guest Management (1988 righe ricerca) |
| S319 | Connessione funzionante (porta 54081) |

---

*"Stessa rete = semplice. Zero complicazioni!"*
*Cervella & Rafa - Sessione 322*
