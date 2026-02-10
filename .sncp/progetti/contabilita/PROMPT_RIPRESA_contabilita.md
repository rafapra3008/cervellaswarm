# PROMPT RIPRESA - Contabilita

> **Ultimo aggiornamento:** 9 Febbraio 2026 - Sessione pomeriggio
> **Per SOLO questo progetto!**

---

## STATO ATTUALE

```
+================================================================+
|   CONTABILITA ANTIGRAVITY                                       |
|   Produzione: v2.9.0 LIVE (parser v1.8.0)                      |
|   Locale: parser v1.9.0 (testato, DA DEPLOYARE)                |
|   Rating: 9.9/10                                                |
+================================================================+
```

---

## SISTEMA LIVE

| Componente | Versione LIVE | Versione Locale |
|------------|--------------|-----------------|
| Backend | v1.12.0 | v1.12.0 |
| PDF Parser | **v1.8.0** | **v1.9.0** (da deployare) |
| Security | v1.1.0 | v1.1.0 |
| FORTEZZA MODE | v4.3.0 | v4.3.0 |
| Landing Page | - | v1.0.0 (locale) |

---

## SESSIONE 9 FEBBRAIO - COSA FATTO

### 1. Deploy parser v1.8.0 (COMPLETATO)
- FORTEZZA MODE 10/10 step OK
- Tag: `vm-deployed-v2.9.0`
- Fix: page break duplicati, PR docs, apostrofo nomi

### 2. Fix parser v1.9.0 (LOCALE, da deployare)
- **Bug**: Nomi con parentesi (tour operator) non riconosciuti
- **Caso**: "Jarosch Bettina (Paartour) - [3602]" → nome ereditato dal cliente precedente (Catalina Cazacu)
- **Fix**: Aggiunto `(?:\s*\([^)]*\))*` in 3 punti regex per saltare parentesi prima di ` - [ID]`
- **Risultato**: nome = "Jarosch Bettina", id = 3602 (corretto!)
- **Test**: 31/31 PASS (8 nuovi in sezione F: TestNomiConParentesi)
- **Guardiana**: APPROVED 9/10 (due audit: pre-fix + post-fix)
- **Prova reale**: PDF SHE 29_1_2026 riprocessato, 17/17 caparre OK, totale 7.882,60

---

## PROSSIMA SESSIONE: DEPLOY + ALTRO

### DEPLOY FORTEZZA MODE
```
COSA DEPLOYARE:
- backend/processors/pdf_parser.py (v1.8.0 → v1.9.0)

UN SOLO FILE. Vale per TUTTI i portali (HP, NL, SHE).
```

### ALTRE COSE DA FARE
Rafa aveva menzionato 2-3 altre cose oltre al fix parentesi.
Non specificate - chiedere a Rafa all'inizio sessione.

---

## DECISIONI CHIAVE

| Decisione | Perche |
|-----------|--------|
| `*` invece di `?` per parentesi | Gestisce anche parentesi multiple (improbabile ma sicuro) |
| NON aggiunto `()` al char class | Rischio catturare info stanza - troppo pericoloso |
| Nome senza parentesi | "Jarosch Bettina" (senza "(Paartour)") - sufficiente per matching |
| DB SHE pulito e riprocessato | Verificato fix con dati reali prima di deploy |

---

## PUNTATORI

| Cosa | Dove |
|------|------|
| Backup DB SHE | `db_test_local/contabilita_she_BACKUP_20260209.db` |
| Backup DB HP | `db_test_local/contabilita_hp_BACKUP_20260209.db` |
| Hardtests | `tests/test_pdf_parser_hp.py` (31 test) |
| PDF test parentesi | Desktop: `29_1_2026 (1).pdf` (file SHE) |
| Git tag produzione | `vm-deployed-v2.9.0` |

---

## DATI PRODUZIONE

| Cosa | Valore |
|------|--------|
| Host | contabilitafamigliapra.it |
| User | root |
| Path | /opt/contabilita-system/ |
| Tag Git | vm-deployed-v2.9.0 |

---

*Parser v1.9.0 pronto per deploy! Un solo file, FORTEZZA MODE.*
