# PROMPT RIPRESA - Miracollo

> **Ultimo aggiornamento:** 19 Gennaio 2026 - Sessione 268
> **Status:** FASE 3 Fatture: GUIDA COMPLETA | Miracollook: 6.5 → 9.5

---

## STATO MODULO FINANZIARIO

```
FASE 1: Ricevute PDF      [####################] 100% REALE!
FASE 1B: Checkout UI      [####################] 100% REALE!
FASE 2: Scontrini RT      [##################..] 90% ADAPTER FIXATO!
FASE 3: Fatture XML       [########............] 40% GUIDA COMPLETA!
FASE 4: Export            [....................] 0%

TOTALE MODULO: 75%
```

---

## SESSIONE 268: FATTURE XML - GUIDA COMPLETA

```
+================================================================+
|   GUIDA COMPLETA CREATA E VERIFICATA DA 3 GUARDIANE!           |
|   - Studiati 4 XML reali (Lodge + SHE)                         |
|   - Estratti dati fiscali, aliquote, codici                    |
|   - Schema DB pronto (cervella-data)                           |
+================================================================+
```

### Dati Estratti

| Campo | Valore |
|-------|--------|
| P.IVA | 00658350251 |
| Denominazione | Famiglia Pra Srl |
| Regime | RF01 (ordinario) |
| SPRING | 3.5.02A (server) |
| Numerazione test | 200/NL in poi |

### File Creati

| File | Contenuto |
|------|-----------|
| `.sncp/progetti/miracollo/guide/GUIDA_FATTURE_XML_MIRACOLLO.md` | Guida completa |
| `~/Desktop/fatture_xml_test/` | Cartella output test |

### Prossimi Step FASE 3

```
1. [ ] Generare 1 XML test (fattura 200/NL)
2. [ ] Validare con tool online
3. [ ] Test import in SPRING (con contabilista)
4. [ ] Se OK: implementare in Miracollo
```

---

## SESSIONE 268: MIRACOLLOOK ROBUSTEZZA

```
CODICE: 100% | ROBUSTEZZA: 6.5/10 → target 9.5/10
Add Label implementato + SUBROADMAP creata
```

### Prossimi Step Miracollook

```
FASE 1 - SECURITY (BLOCKER):
[ ] Token encryption
[ ] ANTHROPIC_API_KEY in env
[ ] CORS produzione

FASE 2 - ROBUSTEZZA:
[ ] Auto-start launchd
[ ] Backup automatico
```

**File:** `docs/roadmap/SUBROADMAP_MIRACOLLOOK_ROBUSTEZZA.md`

---

## SESSIONE 266: SOAP ADAPTER

```
✅ Fix completato - epson_adapter.py funziona!
   - URL con ?devid=local_printer&timeout=10000
   - Content-Type: text/xml
   - SOAP Envelope wrapper

TESTATO: Mac → Epson 192.168.200.240 (BAR) = OK
PARCHEGGIATO: IP Reception da trovare
```

---

## FLUSSO FATTURE (Referenza)

```
Miracollo → XML FatturaPA → Cartella → SPRING → SDI

- Miracollo genera solo XML
- SPRING gestisce firma/invio/conservazione
- 10-15 fatture/mese
```

---

## FILE CHIAVE

| File | Contenuto |
|------|-----------|
| `.sncp/guide/GUIDA_FATTURE_XML_MIRACOLLO.md` | Guida fatture |
| `docs/roadmap/SUBROADMAP_FASE3_FATTURE_XML.md` | Piano FASE 3 |
| `docs/roadmap/SUBROADMAP_MIRACOLLOOK_ROBUSTEZZA.md` | Piano robustezza |
| `backend/services/fiscal/epson_adapter.py` | Adapter SOAP |

---

*"Non reinventiamo la ruota - usiamo lo standard!" - Sessione 268*
