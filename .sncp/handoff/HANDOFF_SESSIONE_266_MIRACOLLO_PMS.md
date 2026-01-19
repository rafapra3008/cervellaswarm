# HANDOFF SESSIONE 266 - MIRACOLLO PMS

> **Data:** 19 Gennaio 2026
> **Progetto:** Miracollo PMS
> **Focus:** Fix SOAP Adapter + FASE 3 Fatture Studiata

---

## RISULTATO SESSIONE

```
+================================================================+
|                                                                |
|   1. FIX SOAP ADAPTER EPSON - COMPLETATO!                     |
|   2. FASE 3 FATTURE XML - STUDIATA E PIANIFICATA!             |
|                                                                |
+================================================================+
```

---

## COSA È STATO FATTO

### 1. Fix SOAP Adapter Epson

**File:** `backend/services/fiscal/epson_adapter.py`

| Fix | Prima | Dopo |
|-----|-------|------|
| URL | `/cgi-bin/fpmate.cgi` | `?devid=local_printer&timeout=10000` |
| Content-Type | `application/xml` | `text/xml` |
| XML | Nudo | Wrappato in SOAP Envelope |
| Parse | Root diretta | Naviga dentro soap:Body |

**Perché:** Sessione 264 ha scoperto che Epson richiede SOAP, non XML nudo.

### 2. Ricerca FASE 3 Fatture (3 ricerche)

- FatturaPA per hotel (aliquote, tassa soggiorno N1)
- Import XML in SPRING SQL
- Flusso Ericsoft (come era prima)

**Scoperta:** L'hotel usa SPRING per contabilità → Miracollo deve solo generare XML!

### 3. Flusso Fatture Chiarito

```
Miracollo → XML FatturaPA → Cartella → SPRING → SDI

- Solo 10-15 fatture/mese
- SPRING già gestisce SDI
- Come faceva Ericsoft!
- Zero costi extra
```

---

## STATO MODULO FINANZIARIO

```
FASE 1: Ricevute PDF      [####################] 100% REALE!
FASE 1B: Checkout UI      [####################] 100% REALE!
FASE 2: Scontrini RT      [##################..] 90% ADAPTER FIXATO!
FASE 3: Fatture XML       [##..................] 10% STUDIATO!
FASE 4: Export            [....................] 0%
```

---

## FILE CREATI/MODIFICATI

| File | Azione |
|------|--------|
| `backend/services/fiscal/epson_adapter.py` | Fix SOAP |
| `docs/roadmap/SUBROADMAP_FASE3_FATTURE_XML.md` | Creato |
| `.sncp/ricerca/RICERCA_*.md` | 3 file ricerca |
| `NORD.md` | Aggiornato |
| `PROMPT_RIPRESA_miracollo.md` | Aggiornato |

---

## PROSSIMI STEP

### FASE 2 - Scontrini RT
```
[ ] Test adapter su stampante Bar (quando in hotel)
[ ] Trovare IP Reception (parcheggiato)
```

### FASE 3 - Fatture XML
```
[ ] Parlare con contabilista:
    - Path cartella export XML
    - Dati cedente (P.IVA, ragione sociale)
    - Progressivo fatture
[ ] Test import XML in SPRING
[ ] Implementare (python-a38)
```

---

## NOTE TECNICHE

- **Tassa soggiorno:** N1 (NON N2!)
- **Libreria:** python-a38
- **Aliquote:** Pernottamento 10%, Extra 22%

---

## GIT

```
Miracollo:     f01fe54, 64d4504
CervellaSwarm: 17f14ef, 4baddd0
```

---

*"Non reinventiamo la ruota - usiamo lo standard!"*
