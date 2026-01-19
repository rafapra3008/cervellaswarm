<!-- DISCRIMINATORE: MIRACOLLO PMS CORE -->
<!-- PORTA: 8001 | TIPO: Sistema alberghiero principale -->
<!-- PATH: ~/Developer/miracollogeminifocus/ (backend principale) -->
<!-- NON CONFONDERE CON: Miracollook (8002), Room Hardware (8003) -->

# PROMPT RIPRESA - PMS Core

> **Ultimo aggiornamento:** 19 Gennaio 2026 - Sessione 272
> **STATO:** 90% LIVE | Health 6.5/10 (in miglioramento)

---

## SESSIONE 272 - PULIZIA CASA PMS

```
+================================================================+
|                                                                |
|   PULIZIA CASA COMPLETATA!                                     |
|                                                                |
|   - Audit tecnico: Health 6.5/10 mappato                       |
|   - Modulo subscription organizzato                            |
|   - 4 TODO tecnici fixati                                      |
|   - SUBROADMAP split file creata                               |
|                                                                |
+================================================================+
```

### Fix Applicati (Sessione 272)

| File | Fix |
|------|-----|
| `routers/settings/rooms.py` | Check prenotazioni prima delete |
| `services/email/bookingengine.py` | num_guests da email |
| `routers/weather.py` | Location/type da database |
| `routers/ml_api.py` | TODO obsoleto rimosso |

### File Creati

| File | Scopo |
|------|-------|
| `modules/subscription/` | Modulo parcheggiato (README incluso) |
| `core/encryption.py` | TokenEncryptor Fernet per Twilio |

---

## MAPPA SPLIT FILE GIGANTI

**SUBROADMAP:** `.sncp/progetti/miracollo/roadmaps/SUBROADMAP_SPLIT_FILE_GIGANTI.md`

| # | File | Righe | Rischio | Sessioni |
|---|------|-------|---------|----------|
| 1 | test_action_tracking.py | 820 | Basso | 1 |
| 2 | ml_api.py | 705 | Basso | 1 |
| 3 | cm_import_service.py | 762 | Medio | 1.5 |
| 4 | planning_core.py | 746 | ALTO | 2 |
| 5 | ab_testing_api.py | 768 | Medio | 1.5 |
| 6 | city_tax.py | 721 | Medio | 1.5 |

**Totale:** 8-9 sessioni

---

## MODULO FINANZIARIO - STATO

| Fase | Componente | Stato |
|------|------------|-------|
| 1 | Ricevute PDF | 100% REALE |
| 1B | Checkout UI | 100% REALE |
| 2 | Scontrini RT | 90% - test stampante DA FARE |
| 3 | Fatture XML | 60% - PARCHEGGIATO |
| 4 | Export | 0% - PARCHEGGIATO |

---

## PROSSIMO STEP

```
OPZIONE A - Split File (consigliato):
  1. test_action_tracking.py (warm-up, zero rischio)
  2. ml_api.py (basso rischio)
  3. ... seguire SUBROADMAP

OPZIONE B - Test Scontrini RT:
  Quando in hotel: test stampante Bar
```

---

## PARCHEGGIATI

| Cosa | Motivo |
|------|--------|
| Subscription system | In `modules/`, pronto quando serve |
| Fatture XML impl. | Test SPRING OK |
| Export commercialista | Manuale OK per 10-15 fatt/mese |
| Notifiche CM | Modulo futuro |

---

## ARCHITETTURA

```
Internet -> Nginx (443) -> Backend (8001) -> SQLite
VM: miracollo-cervella (Google Cloud)
PATH: /home/rafapra/app/
```

---

## GUIDE E DOC

| File | Scopo |
|------|-------|
| SUBROADMAP_SPLIT_FILE_GIGANTI.md | Piano split 6 file |
| GUIDA_FATTURE_XML_MIRACOLLO.md | Fatture XML |
| MAPPA_MODULO_FINANZIARIO.md | Stato modulo completo |

---

*"Pulizia casa prima di costruire nuovo!" - Sessione 272*
