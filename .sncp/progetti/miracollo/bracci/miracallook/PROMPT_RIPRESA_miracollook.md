<!-- DISCRIMINATORE: MIRACOLLOOK EMAIL CLIENT -->
<!-- PORTA: 8002 | TIPO: Email client AI per hotel -->
<!-- PATH: ~/Developer/miracollogeminifocus/miracallook/ -->
<!-- NON CONFONDERE CON: PMS Core (8001), Room Hardware (8003) -->

# PROMPT RIPRESA - Miracollook

> **Ultimo aggiornamento:** 30 Gennaio 2026 - Sessione 323
> **STATUS:** FASE 3 Cache Layer COMPLETATA!

---

## SESSIONE 323 - CACHE LAYER IMPLEMENTATO

### Cosa Abbiamo Fatto

| # | Task | Risultato |
|---|------|-----------|
| 1 | aiocache aggiunto | requirements.txt |
| 2 | Decoratori @cached | 6 metodi |
| 3 | StaleCache class | Graceful degradation |
| 4 | Invalidation API | 4 metodi |
| 5 | Test unitari | 20/20 PASS |
| 6 | **Guardiana Audit** | **9/10 APPROVE** |

### Connector v2.1.0

**Nuove features:**
- Cache in-memory con aiocache
- TTL differenziati per metodo
- Graceful degradation (1h stale fallback)
- Cache invalidation API

**TTL Strategy:**
| Metodo | TTL |
|--------|-----|
| get_all_guests | 5 min |
| get_in_house_guests | 1 min |
| get_guests_by_status | 1 min |
| get_post_stay_guests | 2 min |
| get_pre_arrival_guests | 2 min |
| get_guest_by_id | 2 min |
| Stale fallback | 1 ora |

---

## STATO INTEGRAZIONE ERICSOFT

```
FASE 1: Connector Base        [####################] 100%
FASE 2: Guest Management      [############........] 60%
FASE 3: Cache Layer           [####################] 100% ← S323!
FASE 4: API Endpoints         [....................] 0%
FASE 5: Frontend Integration  [....................] 0%
FASE 6: Test & Production     [....................] 0%
```

---

## PROSSIMI STEP (S324+)

1. **Test DB reale** - Quando in hotel
2. **API Endpoints** - FASE 4 (GET /api/guests/*)
3. **Frontend** - GuestContextCard

---

## FILE CHIAVE

| File | Path |
|------|------|
| Connector v2.1.0 | `miracallook/backend/ericsoft/connector.py` |
| Test cache | `miracallook/backend/tests/test_cache_layer.py` |
| **SUBROADMAP** | `.sncp/progetti/miracollo/bracci/miracallook/SUBROADMAP_ERICSOFT_INTEGRATION.md` |

---

## TEST TOTALI: 38/38 PASS

- test_guest_profile.py: 18/18
- test_cache_layer.py: 20/20

---

*"Cache layer per performance! Stessa rete = semplice!"*
*Cervella & Rafa - Sessione 323*
