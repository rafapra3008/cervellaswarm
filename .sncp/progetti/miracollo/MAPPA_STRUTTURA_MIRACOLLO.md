# MAPPA STRUTTURA - Ecosistema Miracollo

> **Aggiornato:** 16 Gennaio 2026 - Sessione 241
> **Score Target:** 9.5/10

---

## ARCHITETTURA 3 BRACCI

```
+====================================================================+
|                       ECOSISTEMA MIRACOLLO                         |
+====================================================================+
|                                                                    |
|   +------------------+                                             |
|   |    PMS CORE      |  <-- FONTE DI VERITA                       |
|   |     :8000        |      85% - PRODUZIONE                       |
|   +--------+---------+                                             |
|            |                                                       |
|    +-------+-------+                                               |
|    |               |                                               |
|  +-v------+    +---v--------+                                      |
|  |MIRACOL |    |ROOM        |                                      |
|  |LOOK    |    |HARDWARE    |                                      |
|  | :8002  |    | :8003      |                                      |
|  | 80%    |    | 10%        |                                      |
|  +--------+    +------------+                                      |
|  Email         Automazione                                         |
|  client        stanze                                              |
|                                                                    |
+====================================================================+
```

---

## STRUTTURA SNCP

```
.sncp/progetti/miracollo/
|
+-- bracci/                          # I 3 servizi dell'ecosistema
|   |
|   +-- pms-core/                    # Braccio 1 - Backend principale
|   |   +-- COSTITUZIONE_pms-core.md    [NUOVO]
|   |   +-- NORD_PMS-CORE.md            [NUOVO]
|   |   +-- PROMPT_RIPRESA_pms-core.md  [NUOVO]
|   |   +-- stato.md
|   |
|   +-- miracollook/                 # Braccio 2 - Email client
|   |   +-- COSTITUZIONE_MIRACOLLOOK.md
|   |   +-- NORD_MIRACOLLOOK.md
|   |   +-- PROMPT_RIPRESA_miracollook.md  [NUOVO]
|   |   +-- stato.md
|   |   +-- studi/                   (27 ricerche)
|   |   +-- ricerche/                (competitor, API)
|   |   +-- decisioni/               (design specs)
|   |   +-- reports/                 (audit, review)
|   |   +-- roadmaps/                (sprint, fasi)
|   |
|   +-- room-hardware/               # Braccio 3 - Automazione
|       +-- COSTITUZIONE_room-hardware.md  [NUOVO]
|       +-- NORD_ROOM-HARDWARE.md          [NUOVO]
|       +-- PROMPT_RIPRESA_room_hardware.md
|       +-- stato.md
|       +-- studi/                   (21 ricerche VDA)
|       +-- reports/
|
+-- moduli/                          # Moduli INTERNI a PMS Core
|   +-- rateboard/                   # Pricing intelligente
|   +-- whatif/                      # Simulatore
|   +-- finanziario/                 # Contabilita
|   +-- in_room_experience/          # (legacy?)
|
+-- stato.md                         # Stato GENERALE ecosistema
+-- PROMPT_RIPRESA_miracollo.md      # Ripresa GENERALE (deprecato?)
+-- MAPPA_STRUTTURA_MIRACOLLO.md     # QUESTO FILE
```

---

## TABELLA COMPLETEZZA

| Braccio | COSTITUZIONE | NORD | PROMPT_RIPRESA | stato.md | Score |
|---------|--------------|------|----------------|----------|-------|
| PMS-Core | OK | OK | OK | OK | 4/4 |
| Miracollook | OK | OK | OK | OK | 4/4 |
| Room-Hardware | OK | OK | OK | OK | 4/4 |

**Tutti i bracci ora hanno documentazione COMPLETA!**

---

## COMUNICAZIONE TRA BRACCI

```
+------------------------------------------------------------------+
|                    FLUSSO DATI                                    |
+------------------------------------------------------------------+

PMS CORE (fonte di verita)
    |
    +---> Miracollook
    |     - GET /guests/{email}     Chi e questo ospite?
    |     - GET /bookings/current   Prenotazioni attive
    |     - Miracollook LEGGE, non scrive
    |
    +---> Room Hardware
          - POST /rooms/{id}/status  Camera check-in/out
          - Room Hardware SCRIVE stato sensori
          - Room Hardware LEGGE eventi PMS

+------------------------------------------------------------------+
|                    PORTE                                          |
+------------------------------------------------------------------+

:8000  PMS Core (FastAPI backend)
:8002  Miracollook (FastAPI backend)
:8003  Room Hardware (FastAPI + pymodbus) [futuro]
:80    Frontend React (nginx)
:443   Frontend React (SSL)
:5432  PostgreSQL
```

---

## REGOLE OPERATIVE

### Quando Lavori su un Braccio

```
1. LEGGI il PROMPT_RIPRESA del braccio
2. LEGGI la COSTITUZIONE del braccio
3. CONTROLLA il NORD per la visione
4. LAVORA
5. AGGIORNA stato.md E PROMPT_RIPRESA
```

### Dove Salvare Cosa

| Tipo | Path |
|------|------|
| Ricerche | `bracci/{braccio}/studi/` |
| Decisioni | `bracci/{braccio}/decisioni/` |
| Audit/Review | `bracci/{braccio}/reports/` |
| Roadmap | `bracci/{braccio}/roadmaps/` |
| Stato | `bracci/{braccio}/stato.md` |

### Moduli vs Bracci

```
BRACCI = Servizi SEPARATI con porta propria
  - PMS Core (:8000)
  - Miracollook (:8002)
  - Room Hardware (:8003)

MODULI = Funzionalita INTERNE a PMS Core
  - rateboard (pricing)
  - whatif (simulatore)
  - finanziario (contabilita)
```

---

## STATO ATTUALE

| Braccio | Progresso | Fase | Note |
|---------|-----------|------|------|
| PMS Core | 85% | PRODUZIONE | Stabile, manutenzione |
| Miracollook | 80% | FASE 1 | Drag/resize in corso |
| Room Hardware | 10% | RICERCA | Attesa hardware |

---

## FILE DEPRECATI (da verificare)

```
? .sncp/progetti/miracollo/PROMPT_RIPRESA_miracollo.md
  - Ora ogni braccio ha il suo!
  - Tenere come "panoramica generale"?

? .sncp/progetti/miracollo/moduli/in_room_experience/
  - Legacy? Merge con Room Hardware?
```

---

*"Lavoriamo in pace! Senza casino! Dipende da noi!"*
*Ecosistema Miracollo - 3 Bracci, 1 Visione*
