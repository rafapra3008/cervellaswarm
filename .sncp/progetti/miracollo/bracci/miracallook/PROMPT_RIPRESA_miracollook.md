<!-- DISCRIMINATORE: MIRACOLLOOK EMAIL CLIENT -->
<!-- PORTA: 8002 | TIPO: Email client AI per hotel -->
<!-- PATH: ~/Developer/miracollogeminifocus/miracallook/ -->
<!-- NON CONFONDERE CON: PMS Core (8001), Room Hardware (8003) -->

# PROMPT RIPRESA - Miracollook

> **Ultimo aggiornamento:** 29 Gennaio 2026 - Sessione 315
> **ROBUSTEZZA:** 10/10 - PRODUCTION READY + PMS INTEGRATION!

---

## SESSIONE 315 - ACCESSO DATABASE ERICSOFT ✓

```
+================================================================+
|   ACCESSO DIRETTO AL DATABASE ERICSOFT OTTENUTO!               |
|   452 tabelle - Backup fatto - Pronto per studio               |
+================================================================+
```

### COSA ABBIAMO FATTO

| # | Task | Stato |
|---|------|-------|
| 1 | Test API Bedzzle | ✓ Dati vengono da Ericsoft |
| 2 | Accesso DB SQL Server | ✓ SSMS connesso |
| 3 | Backup database PRA | ✓ 29/01/2026 |
| 4 | Guardiane analisi | ✓ 452 tabelle mappate |

### TABELLE PRIORITARIE (Guardiana Qualità)

| Priorità | Tabella | Scopo |
|----------|---------|-------|
| P0 | Scheda | Prenotazioni/soggiorni |
| P0 | Ospite | Dati ospiti |
| P0 | Risorsa | Camere |
| P1 | Anagrafica | Email, telefono |
| P1 | SchedaConto | Addebiti/servizi |

### FILE CREATI S315

| File | Cosa |
|------|------|
| `SUBROADMAP_CONNETTORE_ERICSOFT.md` | Piano 3 fasi |
| `ricerche/CREDENZIALI_ERICSOFT_S315.md` | Accesso DB (sensibile!) |

---

## PROSSIMO STEP (S316)

```
1. Studio struttura tabelle reali
   - SELECT TOP 5 * FROM Scheda
   - Capire relazioni FK

2. Creare utente READ-ONLY
   - miracollook_reader (no sa!)
   - Solo permessi SELECT
```

---

## SESSIONI PRECEDENTI

| Sessione | Cosa | Archivio |
|----------|------|----------|
| S314 | MyReception esplorato | `archivio/S314_MYRECEPTION.md` |

---

## CREDENZIALI MYRECEPTION

```
URL: https://marketplace.bedzzle.com/admin/apps/MyReception/
Username: naturaelodge
Password: Dolomiti*2026
```

---

## FILE CHIAVE

| File | Cosa |
|------|------|
| `miracallook/CLAUDE.md` | Istruzioni workspace |
| `docker-compose.yml` | Orchestrazione |
| `backend/gmail/pms_context.py` | PMS integration |

---

## COME TESTARE

```bash
# 1. Avvia PMS Core
cd ~/Developer/miracollogeminifocus
uvicorn backend.main:app --port 8001

# 2. Avvia Miracollook
cd ~/Developer/miracollogeminifocus/miracallook
docker-compose up -d

# 3. Browser
open http://localhost:80
```

---

*"Studiare prima, implementare dopo!" - Formula Magica*
*"Fatto bene > Fatto veloce" - Sessione 315*
