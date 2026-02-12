# STATO PROGETTO MIRACOLLO

> **Data:** 2026-01-19 - Sessione 272
> **Architettura:** 3 Bracci (PMS Core, Miracollook, Room Hardware)

---

## ECOSISTEMA ATTUALE

```
MIRACOLLO
├── PMS CORE (:8001)        90%  PRODUZIONE STABILE | Health 6.5/10
├── MIRACOLLOOK (:8002)     Codice 100% | Robustezza 9.2/10
└── ROOM HARDWARE (:8003)   10%  Attesa hardware
```

| Braccio | Stato | Score | Prossimo |
|---------|-------|-------|----------|
| PMS Core | LIVE, pulizia casa | 6.5/10 | Split file giganti |
| Miracollook | Robustezza OK | 9.2/10 | Prod quando serve |
| Room Hardware | Ricerca OK | 10% | Setup hardware |

---

## PMS CORE - SESSIONE 272 (PULIZIA CASA)

### Fix Applicati

| File | Fix |
|------|-----|
| `routers/settings/rooms.py` | Check prenotazioni prima delete |
| `services/email/bookingengine.py` | num_guests estratto da email |
| `routers/weather.py` | Location/type da database |
| `routers/ml_api.py` | TODO obsoleto rimosso |

### File Creati

| File | Scopo |
|------|-------|
| `backend/modules/subscription/` | Modulo subscription organizzato |
| `backend/core/encryption.py` | TokenEncryptor Fernet per Twilio |
| `SUBROADMAP_SPLIT_FILE_GIGANTI.md` | Piano split 6 file >700 righe |

---

## PMS CORE - MODULO FINANZIARIO

```
FASE 1: Ricevute PDF        [####################] 100% REALE!
FASE 1B: Checkout UI        [####################] 100% REALE!
FASE 2: Scontrini RT        [##################..] 90% Test stampante DA FARE
FASE 3: Fatture XML         [############........] 60% PARCHEGGIATO
FASE 4: Export              [....................] 0% PARCHEGGIATO
```

**Prossimo:** Test stampante Bar quando in hotel

---

## MAPPA SPLIT FILE GIGANTI

**SUBROADMAP:** `roadmaps/SUBROADMAP_SPLIT_FILE_GIGANTI.md`

| # | File | Righe | Rischio | Sessioni |
|---|------|-------|---------|----------|
| 1 | test_action_tracking.py | 820 | Basso | 1 |
| 2 | ml_api.py | 705 | Basso | 1 |
| 3 | cm_import_service.py | 762 | Medio | 1.5 |
| 4 | planning_core.py | 746 | ALTO | 2 |
| 5 | ab_testing_api.py | 768 | Medio | 1.5 |
| 6 | city_tax.py | 721 | Medio | 1.5 |

**Totale stimato:** 8-9 sessioni

---

## PARCHEGGIATI

| Cosa | Motivo | Risveglio |
|------|--------|-----------|
| Subscription system | In `modules/` organizzato | Quando vendita B2B |
| Fatture XML impl. | Test SPRING OK | Quando serve |
| Export commerc. | 10-15 fatt/mese | Mai (manuale OK) |
| Miracollook FASE 4-5 | 9.2 sufficiente | Dopo prod |
| Room Hardware | Attesa hardware | Quando arriva |
| Notifiche CM | Modulo futuro | Q2 2026? |

---

## SESSIONI RECENTI

| Sess | Data | Focus | Risultato |
|------|------|-------|-----------|
| **272** | **19 Gen** | **Pulizia Casa PMS** | **9 task + SUBROADMAP** |
| 271 | 19 Gen | Fatture XML Test | TEST SPRING OK! |
| 270 | 19 Gen | Miracollook Robustezza | 6.5->9.2/10 |
| 268 | 19 Gen | Labels + SUBROADMAP | Codice 100% |
| 266 | 19 Gen | SOAP Adapter Epson | Fix completo |

---

## PUNTATORI

| Cosa | Dove |
|------|------|
| NORD.md | `miracollogeminifocus/NORD.md` |
| SUBROADMAP Split | `roadmaps/SUBROADMAP_SPLIT_FILE_GIGANTI.md` |
| Guida Fatture XML | `guide/GUIDA_FATTURE_XML_MIRACOLLO.md` |
| MAPPA Finanziario | `moduli/finanziario/MAPPA_MODULO_FINANZIARIO.md` |

---

*"Pulizia casa prima di costruire nuovo!"*
*Aggiornato: 19 Gennaio 2026 - Sessione 272*
