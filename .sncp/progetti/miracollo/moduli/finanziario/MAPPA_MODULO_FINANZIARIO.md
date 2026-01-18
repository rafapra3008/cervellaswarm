# MAPPA MODULO FINANZIARIO - MIRACOLLO

> **QUESTO FILE E LA BUSSOLA DEL MODULO FINANZIARIO**
> **Score: 9.7/10 | Ultimo aggiornamento: 18 Gennaio 2026 - Sessione 262**
> **FASE 1 VERIFICATA REALE!**

---

## VISIONE

```
+====================================================================+
|                                                                    |
|   MODULO FINANZIARIO COMPLETO E ROBUSTO                           |
|                                                                    |
|   - Ricevute PDF professionali                                     |
|   - Scontrini RT (registratore telematico)                        |
|   - Fatture elettroniche XML                                       |
|   - Export per commercialista (SCP Spring)                        |
|                                                                    |
|   "Una cosa alla volta, ROBUSTO e COMPLETO"                       |
|                                                                    |
+====================================================================+
```

---

## CONTESTO ATTUALE

### Sistema in Uso (Hotel Rafa)
- **PMS attuale**: Ericsoft (da studiare per capire workflow)
- **Contabilita**: SCP Spring (importa XML da cartella)
- **RT**: Stampante fiscale esistente (marca/modello da verificare)

### Cosa Esiste in Miracollo
| Componente | Stato | Note |
|------------|-------|------|
| Payments CRUD | COMPLETO | IMMUTABLE GUARD attivo |
| Receipt Preview JSON | COMPLETO | Tutti i dati pronti |
| **Receipt PDF** | **REALE!** | **Verificato Sessione 262 - PDF 16KB professionale** |
| **Email con PDF** | **REALE!** | **Verificato Sessione 262** |
| **Checkout UI** | **REALE!** | **Bottoni funzionanti** |
| Scontrini RT | MANCA | Integrazione hardware (blocker: info RT) |
| Fatture XML | MANCA | FatturaPA format |
| Export Spring | MANCA | XML nella cartella |

---

## ARCHITETTURA TARGET

```
                    +------------------+
                    |   PMS MIRACOLLO  |
                    +--------+---------+
                             |
              +--------------+--------------+
              |              |              |
     +--------v----+  +------v------+  +----v--------+
     |  RICEVUTE   |  |  SCONTRINI  |  |   FATTURE   |
     |    PDF      |  |     RT      |  |    XML      |
     +------+------+  +------+------+  +------+------+
            |                |                |
     +------v------+  +------v------+  +------v------+
     |   Email     |  | RT Provider |  | SCP Spring  |
     |  Archivio   |  |   Plugin    |  |   Folder    |
     +-------------+  +------+------+  +-------------+
                             |
              +--------------+--------------+
              |              |              |
     +--------v----+  +------v------+  +----v--------+
     | Epson HTTP  |  | Custom XML  |  | Cloud API   |
     | (Primario)  |  | (Backup)    |  | (Futuro)    |
     +-------------+  +-------------+  +-------------+
```

---

## FASI DI SVILUPPO

### FASE 1: RICEVUTE PDF - COMPLETATA!
**Completata: Sessione 237 (16 Gennaio 2026)**

```
+====================================================================+
|                    SPRINT 1 COMPLETATO!                            |
+====================================================================+

DELIVERABLE - TUTTI COMPLETATI:
[x] Template HTML ricevuta (stile hotel professionale)
[x] Service generazione PDF (WeasyPrint)
[x] Endpoint GET /api/receipts/booking/{id}/pdf
[x] Endpoint GET /api/receipts/booking/{id}/pdf/preview
[x] Endpoint POST /api/receipts/booking/{id}/email
[x] Storage PDF in /data/receipts/{year}/{month}/
[x] Email con allegato PDF
[x] Test con dati reali (43KB PDF generato!)
```

**File creati:**
- `backend/services/receipt_pdf_service.py` - Service completo
- `backend/templates/receipts/receipt_template.html` - Template professionale
- `backend/routers/receipts.py` - Aggiornato con 3 nuovi endpoint
- `backend/services/email/sender.py` - Aggiunta funzione allegati

**Nota tecnica (produzione):**
```bash
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"
```

**TODO futuro:** Adattare PDF a 1 pagina quando dati sono pochi

### FASE 1B: CHECKOUT UI - COMPLETATA!
**Completata: Sessione 239 (16 Gennaio 2026)**

```
+====================================================================+
|                    SPRINT 1B COMPLETATO!                           |
+====================================================================+

DELIVERABLE - TUTTI COMPLETATI:
[x] Bottone "Genera Ricevuta PDF" nel Tab Folio
[x] Bottone "Invia via Email" con modal conferma
[x] Funzione generateReceiptPDF() - apre PDF preview
[x] Funzione showEmailReceiptModal() - modal inline
[x] Funzione sendEmailReceipt() - POST endpoint
[x] Stili inline responsive (flexbox)
```

**File modificati:**
- `frontend/js/planning/reservation-tab-folio.js` - Due bottoni affiancati
- `frontend/js/planning/receipts.js` - 4 nuove funzioni PDF/Email

**UX Decision (cervella-marketing):**
- Bottone primario (blu gradient): Genera PDF (azione checkout)
- Bottone secondario (outline): Email (azione opzionale)
- Perche: 2 click vs 3 (dropdown) = velocita checkout

**WORKFLOW COMPLETO:**
```
Receptionist → Tab Folio → "Genera Ricevuta PDF" → PDF in nuova tab → Stampa
                        → "Invia via Email" → Modal → Conferma → Email inviata
```

---

### FASE 2: SCONTRINI RT (Registratore Telematico)
**Priorita: ALTA | Complessita: MEDIA-ALTA | Tempo: 4-6 settimane**

```
OBIETTIVO: Emettere scontrini fiscali via RT

NORMATIVA:
- RT obbligatorio per corrispettivi (pagamenti non fatturati)
- Chiusura giornaliera obbligatoria
- NOVITA 2026: Obbligo POS-RT collegato (Marzo 2026)
- XML 7.0 standard Agenzia Entrate

ARCHITETTURA PLUGIN:
- Interfaccia astratta RTProvider
- EpsonHTTPProvider (priorita - 80% mercato)
- CustomXMLProvider (backup)
- MockProvider (testing/sviluppo)
- CloudAPIProvider (futuro)

DELIVERABLE:
[ ] Studio RT esistente hotel (marca, modello, protocollo)
[ ] Interfaccia astratta RTProvider
[ ] MockProvider per testing
[ ] EpsonHTTPProvider (HTTP/XML Epson)
[ ] Service scontrino con retry logic
[ ] Endpoint POST /api/fiscal/receipt
[ ] Chiusura giornaliera automatica (23:55)
[ ] Dashboard stato RT
[ ] Gestione errori e ristampe
[ ] Test con RT reale
```

**File da creare:**
- `backend/services/fiscal/rt_provider.py` (interfaccia)
- `backend/services/fiscal/epson_provider.py`
- `backend/services/fiscal/mock_provider.py`
- `backend/services/fiscal/fiscal_service.py`
- `backend/routers/fiscal.py`

---

### FASE 3: FATTURE ELETTRONICHE XML
**Priorita: MEDIA | Complessita: MEDIA | Tempo: 2-3 settimane**

```
OBIETTIVO: Generare fatture XML per SCP Spring

NORMATIVA:
- Fattura solo su RICHIESTA cliente (B2C) o sempre per P.IVA (B2B)
- IVA: 10% pernottamenti, 22% servizi extra
- Formato: XML FatturaPA v1.2.3
- Numerazione progressiva annuale

WORKFLOW SEMPLIFICATO:
1. Operatore clicca "Emetti Fattura" su prenotazione
2. Miracollo genera XML FatturaPA
3. XML salvato in cartella Spring (es: /fatture/2026/)
4. Spring importa e gestisce invio SDI
5. Miracollo traccia stato (emessa, in Spring)

DELIVERABLE:
[ ] Studio formato XML FatturaPA
[ ] Configurazione cartella Spring (settings hotel)
[ ] Numerazione progressiva (tabella invoices)
[ ] Generazione XML con python-a38
[ ] Endpoint POST /api/invoices/booking/{id}/generate
[ ] Salvataggio XML in cartella Spring
[ ] Registro fatture emesse
[ ] Note di credito
[ ] Test con Spring reale
```

**File da creare:**
- `backend/services/invoice_service.py`
- `backend/models/invoice.py`
- `backend/routers/invoices.py`
- Migration: tabella `invoices`

---

### FASE 4: EXPORT COMMERCIALISTA
**Priorita: BASSA | Complessita: BASSA | Tempo: 1 settimana**

```
OBIETTIVO: Export dati per commercialista

DELIVERABLE:
[ ] Export CSV/Excel pagamenti periodo
[ ] Export CSV/Excel fatture emesse
[ ] Report prima nota
[ ] Report IVA periodica
[ ] Endpoint GET /api/export/accountant
```

---

## WORKFLOW OPERATIVO TARGET

```
CHECKOUT OSPITE
      |
      v
+-----+-----+
| Tipo doc? |
+-----+-----+
      |
      +---------> RICEVUTA (default)
      |               |
      |               v
      |          Genera PDF
      |               |
      |               v
      |          Invia Email (opzionale)
      |               |
      |               v
      |          Emetti Scontrino RT
      |
      +---------> FATTURA (su richiesta)
                      |
                      v
                 Chiedi dati fiscali
                      |
                      v
                 Genera XML FatturaPA
                      |
                      v
                 Salva in cartella Spring
                      |
                      v
                 Emetti Scontrino RT (se pagamento contestuale)
```

---

## CONFIGURAZIONE HOTEL

```
SETTINGS DA AGGIUNGERE:

fiscal_settings:
  # RT
  rt_enabled: true
  rt_provider: "epson"  # epson, custom, cloud, mock
  rt_ip: "192.168.1.100"
  rt_port: 80
  rt_daily_close_time: "23:55"

  # Fatture
  invoice_enabled: true
  invoice_folder: "/path/to/spring/fatture"
  invoice_prefix: "FE"
  invoice_current_number: 1

  # Azienda
  company_name: "Hotel Example Srl"
  company_vat: "IT12345678901"
  company_fiscal_code: "12345678901"
  company_address: "Via Roma 1"
  company_city: "Milano"
  company_postal_code: "20100"
  company_country: "IT"

  # IVA
  vat_rate_accommodation: 10
  vat_rate_services: 22
```

---

## DIPENDENZE TECNICHE

```
LIBRERIE DA AGGIUNGERE:

# PDF Generation
weasyprint>=60.0        # HTML to PDF
jinja2>=3.0             # Templates (gia presente)

# XML Fatture
python-a38>=0.1.0       # FatturaPA generation/validation

# RT Communication
requests>=2.28          # HTTP calls (gia presente)
```

---

## RISCHI E MITIGAZIONI

| Rischio | Impatto | Mitigazione |
|---------|---------|-------------|
| RT hardware incompatibile | ALTO | Studio preventivo modello esistente |
| Formato XML Spring cambia | MEDIO | Configurazione template esterna |
| Normativa cambia 2026 | MEDIO | Architettura plugin flessibile |
| Timeout RT | BASSO | Retry logic + fallback manuale |

---

## METRICHE SUCCESSO

```
FASE 1 (Ricevute PDF):
- [ ] PDF generato < 2 secondi
- [ ] Email inviata < 5 secondi
- [ ] 0 errori su 100 generazioni test

FASE 2 (Scontrini RT):
- [ ] Scontrino emesso < 3 secondi
- [ ] Chiusura giornaliera automatica 100%
- [ ] Recovery automatico dopo errore RT

FASE 3 (Fatture XML):
- [ ] XML valido 100% (validazione python-a38)
- [ ] File in cartella Spring correttamente
- [ ] Numerazione progressiva corretta

FASE 4 (Export):
- [ ] Export completo < 10 secondi
- [ ] Formato compatibile Excel/Spring
```

---

## CRONOLOGIA DECISIONI

| Data | Decisione | Perche |
|------|-----------|--------|
| 16/01/2026 | Architettura plugin RT | Flessibilita, supporta hardware diversi |
| 16/01/2026 | XML in cartella Spring | Semplice, Spring gestisce SDI |
| 16/01/2026 | WeasyPrint per PDF | Open source, HTML templates |
| 16/01/2026 | python-a38 per fatture | Libreria matura, validazione inclusa |

---

## PROSSIMO STEP

```
+====================================================================+
|                                                                    |
|   FASE 2: CHECKOUT UI + RT                                        |
|                                                                    |
|   Opzioni per prossima sessione:                                  |
|   A) Checkout UI - Interfaccia frontend per generare ricevute     |
|   B) Studio RT - Verificare hardware esistente hotel              |
|                                                                    |
|   BLOCKER RT: Serve info hardware (marca, IP, protocollo)         |
|                                                                    |
+====================================================================+
```

---

## SCORE VALUTAZIONE

| Area | Score | Note |
|------|-------|------|
| Completezza requisiti | 9.5/10 | Copre tutto il workflow fiscale |
| Chiarezza architettura | 9.5/10 | Plugin modulare, flessibile |
| Fattibilita tecnica | 9.5/10 | **FASE 1 + 1B COMPLETATE!** |
| Prioritizzazione | 10/10 | Dal semplice al complesso |
| Rischi identificati | 9/10 | Mitigazioni concrete |
| **TOTALE** | **9.7/10** | **SPRINT 1 END-TO-END!** |

---

## CRONOLOGIA COMPLETAMENTI

| Data | Fase | Sessione |
|------|------|----------|
| 16/01/2026 | **FASE 1: Ricevute PDF** (Backend) | **237** |
| 16/01/2026 | **FASE 1B: Checkout UI** (Frontend) | **239** |
| 18/01/2026 | **FASE 1 VERIFICATA REALE!** (Fix bug + Test) | **262** |

---

*"Una cosa alla volta, ROBUSTO e COMPLETO"*
*"Da SU CARTA a REALE!"*

**Sessione 262 - Cervella & Rafa** ❤️‍🔥
