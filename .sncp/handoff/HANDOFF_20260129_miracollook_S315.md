# HANDOFF - Miracollook S315

> **Data:** 29 Gennaio 2026
> **Progetto:** Miracollook (porta 8002)
> **Prossima sessione:** S316

---

## 1. COSA ABBIAMO FATTO

| Task | Stato | Note |
|------|-------|------|
| Test API Bedzzle | FATTO | Dati vengono da Ericsoft |
| Accesso DB SQL Server | FATTO | SSMS connesso |
| Backup database PRA | FATTO | 29/01/2026 |
| Guardiane analisi tabelle | FATTO | 452 tabelle, 6 prioritarie |

---

## 2. DOVE CI SIAMO FERMATI

```
SUBROADMAP CONNETTORE ERICSOFT:
- FASE 1: Impara da Bedzzle    [####################] 100%
- FASE 2: Accesso DB sicuro    [######..............] 30%
- FASE 3: Connettore nostro    [....................] 0%

Siamo a: FASE 2 - Studio struttura tabelle
```

---

## 3. PROSSIMI STEP (S316)

```
1. Studio struttura tabelle reali
   - In SSMS: click destro dbo.Scheda > Seleziona prime 1000 righe
   - Capire relazioni FK tra tabelle
   - Documentare colonne utili

2. Creare utente READ-ONLY
   - Nome: miracollook_reader
   - Permessi: solo SELECT
   - MAI usare sa per applicazioni!
```

---

## 4. FILE IMPORTANTI

| File | Cosa |
|------|------|
| `PROMPT_RIPRESA_miracollook.md` | Stato aggiornato S315 |
| `SUBROADMAP_CONNETTORE_ERICSOFT.md` | Piano 3 fasi |
| `ricerche/CREDENZIALI_ERICSOFT_S315.md` | Accesso DB (SENSIBILE!) |
| `archivio/S314_MYRECEPTION.md` | Sessione precedente |

---

## 5. TABELLE PRIORITARIE (Guardiana)

| Priorita | Tabella | Scopo |
|----------|---------|-------|
| P0 | Scheda | Prenotazioni/soggiorni |
| P0 | Ospite | Dati ospiti |
| P0 | Risorsa | Camere |
| P1 | Anagrafica | Email, telefono |
| P1 | AnagraficaContatto | Contatti |
| P1 | SchedaConto | Addebiti/servizi |

---

## 6. NOTE IMPORTANTI

- **GDPR:** Solo campi necessari, no documenti sensibili
- **Best practice:** READ COMMITTED SNAPSHOT, cache TTL 1-4h
- **Sicurezza:** Creare utente dedicato, non usare sa

---

*"Studiare prima, implementare dopo!"*
*"Fatto bene > Fatto veloce"*
