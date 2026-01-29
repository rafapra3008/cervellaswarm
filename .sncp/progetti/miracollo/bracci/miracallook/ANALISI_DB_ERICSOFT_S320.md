# Analisi Database Ericsoft - Sessione 320

> **Data:** 29 Gennaio 2026
> **Obiettivo:** Capire perché vediamo solo 16 ospiti quando hotel ne ha di più
> **Status:** STUDIO APPROFONDITO

---

## PROBLEMA IDENTIFICATO

```
Query attuale (S319): 16 ospiti
Realtà hotel: > 16 ospiti

IPOTESI:
1. Filtro email esclude molti ospiti
2. Stati non compresi completamente
3. JOIN su Risorsa/Camera perde record
4. Logica date non corretta
```

---

## APPROCCIO STUDIO

### File Creati

| File | Scopo |
|------|-------|
| `sql_analysis_ericsoft.sql` | 10 query SQL per analisi approfondita |
| `analyze_ericsoft_db.py` | Script Python per eseguire analisi |
| Questo doc | Piano strategico e proposte |

### Come Eseguire Analisi

```bash
cd ~/Developer/miracollogeminifocus/miracallook/backend

# 1. Assicurati di essere sulla rete hotel (o VPN WireGuard)
# 2. Esegui analisi
python analyze_ericsoft_db.py

# 3. Risultati salvati in:
#    - ericsoft_analysis_TIMESTAMP.json
#    - Output console (human-readable)
```

---

## QUERY ANALISI (10)

### 1. Email Split
**Domanda:** Quanti ospiti hanno email vs quanti NO?

**Insight atteso:**
- Se molti senza email → query attuale (filtro email) esclude troppi

### 2. Distribuzione Stati
**Domanda:** Come sono distribuiti gli ospiti per `IdStatoScheda`?

**Insight atteso:**
- Capire quanti in stato 1, 2, 3, 4, 5
- Se stato 1 ha molti ospiti → dobbiamo includerlo

### 3. TUTTI Ospiti Attivi Oggi
**Domanda:** Quanti ospiti attivi TOTALI (con e senza email)?

**Insight atteso:**
- NUMERO REALE di ospiti in casa
- Confronto con i 16 attuali

### 4. Campi Timestamp
**Domanda:** Esiste campo "DataModifica" o "LastUpdate"?

**Insight atteso:**
- Come rilevare modifiche prenotazioni
- Polling intelligente

### 5. Cancellazioni
**Domanda:** `DataCancellazione IS NULL` è sufficiente?

**Insight atteso:**
- Verificare che non ci siano altri flag cancellazione
- Correlazione stato/data cancellazione

### 6. Ospiti per Stati 2 e 3
**Domanda:** Se filtriamo solo stati 2 (Arrivi) e 3 (InCasa)?

**Insight atteso:**
- Confronto con filtro date
- Quale è fonte verità?

### 7. Schede Multiple Ospiti
**Domanda:** Ci sono prenotazioni con più ospiti?

**Insight atteso:**
- Famiglie = 1 scheda, N ospiti
- Verifica JOIN non crea duplicati

### 8. Camera Assegnata/Non Assegnata
**Domanda:** Perdono record nel JOIN su Risorsa?

**Insight atteso:**
- Quante prenotazioni senza camera
- LEFT JOIN è corretto?

### 9. Periodi Date
**Domanda:** Distribuzione per periodo (passate/attive/future)?

**Insight atteso:**
- Logica date è corretta?
- Stati correlano con periodi?

### 10. Mapping Stati (se esiste tabella)
**Domanda:** Esiste tabella `StatoScheda` o simile?

**Nota:** Questa query potrebbe fallire se tabella non esiste.

---

## PROPOSTE QUERY CORRETTE

### Proposta A: Tutti Ospiti (No Filtro Email)

**Per:** Dashboard generale, statistiche

```sql
SELECT
    sc.IdStatoScheda,
    sc.TrDataInizio AS check_in,
    sc.TrDataFine AS check_out,
    a.Cognome,
    a.Nome,
    a.TrListaEmail AS email,
    r.Codice AS camera,
    CASE
        WHEN a.TrListaEmail IS NOT NULL AND a.TrListaEmail != '' THEN 1
        ELSE 0
    END AS has_email
FROM SchedaConto sc
INNER JOIN SchedaContoAnagrafica sca ON sc.IdSchedaConto = sca.IdSchedaConto
INNER JOIN Anagrafica a ON sca.IdAnagrafica = a.IdAnagrafica
LEFT JOIN SchedaContoRisorsa scr ON sc.IdSchedaConto = scr.IdSchedaConto
LEFT JOIN Risorsa r ON scr.IdRisorsa = r.IdRisorsa
WHERE sc.DataCancellazione IS NULL
  AND sc.TrDataInizio <= GETDATE()
  AND sc.TrDataFine >= GETDATE()
ORDER BY r.Codice, a.Cognome;
```

**Pro:**
- Vede TUTTI gli ospiti
- Utile per conteggi totali

**Contro:**
- Include ospiti senza email (Miracollook non può mandare email!)

---

### Proposta B: Solo Ospiti Con Email (Attuale, ma migliore)

**Per:** Miracollook (invio email)

```sql
SELECT
    sc.IdStatoScheda,
    sc.TrDataInizio AS check_in,
    sc.TrDataFine AS check_out,
    a.Cognome,
    a.Nome,
    a.TrListaEmail AS email,
    r.Codice AS camera
FROM SchedaConto sc
INNER JOIN SchedaContoAnagrafica sca ON sc.IdSchedaConto = sca.IdSchedaConto
INNER JOIN Anagrafica a ON sca.IdAnagrafica = a.IdAnagrafica
LEFT JOIN SchedaContoRisorsa scr ON sc.IdSchedaConto = scr.IdSchedaConto
LEFT JOIN Risorsa r ON scr.IdRisorsa = r.IdRisorsa
WHERE sc.DataCancellazione IS NULL
  AND a.TrListaEmail IS NOT NULL
  AND a.TrListaEmail != ''
  AND sc.TrDataInizio <= GETDATE()
  AND sc.TrDataFine >= GETDATE()
ORDER BY r.Codice, a.Cognome;
```

**Nota:** È la query attuale, ma OK se i 16 ospiti sono SOLO quelli con email!

---

### Proposta C: Filtro per Stato invece Date

**Per:** Se `IdStatoScheda` è fonte verità

```sql
SELECT
    sc.TrDataInizio AS check_in,
    sc.TrDataFine AS check_out,
    a.Cognome,
    a.Nome,
    a.TrListaEmail AS email,
    r.Codice AS camera
FROM SchedaConto sc
INNER JOIN SchedaContoAnagrafica sca ON sc.IdSchedaConto = sca.IdSchedaConto
INNER JOIN Anagrafica a ON sca.IdAnagrafica = a.IdAnagrafica
LEFT JOIN SchedaContoRisorsa scr ON sc.IdSchedaConto = scr.IdSchedaConto
LEFT JOIN Risorsa r ON scr.IdRisorsa = r.IdRisorsa
WHERE sc.DataCancellazione IS NULL
  AND a.TrListaEmail IS NOT NULL
  AND a.TrListaEmail != ''
  AND sc.IdStatoScheda IN (2, 3)  -- Arrivi e InCasa
ORDER BY r.Codice, a.Cognome;
```

**Pro:**
- Più preciso se stati sono affidabili
- Non dipende da calcolo date

**Contro:**
- Dobbiamo capire TUTTI gli stati possibili
- Cosa significa stato 1? 4?

---

### Proposta D: Ibrida (Date + Stati)

**Per:** Massima sicurezza

```sql
SELECT
    sc.IdStatoScheda,
    sc.TrDataInizio AS check_in,
    sc.TrDataFine AS check_out,
    a.Cognome,
    a.Nome,
    a.TrListaEmail AS email,
    r.Codice AS camera
FROM SchedaConto sc
INNER JOIN SchedaContoAnagrafica sca ON sc.IdSchedaConto = sca.IdSchedaConto
INNER JOIN Anagrafica a ON sca.IdAnagrafica = a.IdAnagrafica
LEFT JOIN SchedaContoRisorsa scr ON sc.IdSchedaConto = scr.IdSchedaConto
LEFT JOIN Risorsa r ON scr.IdRisorsa = r.IdRisorsa
WHERE sc.DataCancellazione IS NULL
  AND a.TrListaEmail IS NOT NULL
  AND a.TrListaEmail != ''
  AND (
    -- Opzione 1: Filtro date
    (sc.TrDataInizio <= GETDATE() AND sc.TrDataFine >= GETDATE())
    OR
    -- Opzione 2: Stati attivi
    sc.IdStatoScheda IN (2, 3)
  )
ORDER BY r.Codice, a.Cognome;
```

**Pro:**
- Cattura ospiti sia per date che per stato
- Più robusto

**Contro:**
- Potrebbe creare duplicati se logica sovrapposta
- Più complesso

---

## RILEVAMENTO MODIFICHE

### Opzione 1: Se esiste campo DataModifica

```sql
WHERE sc.DataModifica > @last_check_timestamp
```

### Opzione 2: Polling completo con hash

```python
# Ogni X minuti:
current_bookings = get_active_bookings()
current_hash = hash(json.dumps(current_bookings, sort_keys=True))

if current_hash != last_hash:
    # Qualcosa è cambiato!
    detect_changes(last_bookings, current_bookings)
```

### Opzione 3: Trigger SQL Server (richiede privilegi)

**Nota:** Utente read-only probabilmente non può creare trigger.

---

## MAPPING STATI (Da Confermare)

| IdStatoScheda | Ipotesi S319 | Da Verificare |
|---------------|--------------|---------------|
| 1 | Confermata? | Query 2, 10 |
| 2 | Arrivi | OK |
| 3 | InCasa | OK |
| 4 | ??? | Query 2, 10 |
| 5 | Partiti | OK |

**Come Confermare:**
1. Eseguire Query 2 (distribuzione stati)
2. Eseguire Query 10 (se esiste tabella mapping)
3. Chiedere a staff hotel (se possibile)
4. Osservare comportamento nel tempo

---

## PIANO VERIFICA DATI

### Step 1: Esegui Analisi
```bash
python analyze_ericsoft_db.py
```

### Step 2: Valuta Risultati

**Scenario A: Molti senza email**
→ Query attuale OK, ma serve dashboard totali separata

**Scenario B: Molti in stato 1**
→ Includere stato 1 in filtro (capire cosa significa!)

**Scenario C: Perdono record in JOIN camera**
→ Verificare LEFT JOIN corretto

### Step 3: Aggiorna Connector

Modificare `connector.py` con query corretta basata su risultati.

### Step 4: Test Reale

Confrontare con:
- Dashboard Ericsoft (quanti ospiti vede?)
- Staff hotel (conteggio manuale)

---

## CHECKLIST DECISIONALE

```
[ ] Eseguito analyze_ericsoft_db.py?
[ ] Salvato ericsoft_analysis_TIMESTAMP.json?
[ ] Verificato numero totale ospiti attivi?
[ ] Capito distribuzione email/senza email?
[ ] Mappato tutti stati IdStatoScheda?
[ ] Trovato campo per rilevare modifiche?
[ ] Verificato LEFT JOIN camera non perde record?
[ ] Confrontato risultati con realtà hotel?
[ ] Deciso quale query usare (A, B, C, D)?
[ ] Aggiornato connector.py?
[ ] Testato query nuova?
[ ] Documentato decisione in PROMPT_RIPRESA?
```

---

## PROSSIMI STEP POST-ANALISI

### Se Query OK → WireGuard
1. Setup VPN WireGuard per accesso remoto
2. Test connettore da remoto
3. Automazione sync periodica

### Se Query DA RIVEDERE → Iterazione
1. Modificare query basata su insight
2. Test su DB
3. Ripetere analisi

### Sempre → Documentazione
1. Aggiornare PROMPT_RIPRESA_miracollook.md
2. Documentare mapping stati in questo file
3. Creare diagramma ER se utile

---

## METRICHE ATTESE

```
Tempo analisi: ~5 minuti (dipende da dimensione DB)
Query eseguite: 9-10 (Query 10 potrebbe fallire)
Output: JSON + console
Decisione finale: Quale query usare
```

---

## NOTE TECNICHE

### Sicurezza
- Tutte query READ-ONLY
- Circuit breaker attivo
- Timeout 5 sec per query

### Performance
- LIMIT/TOP per evitare result set enormi
- Indici presunti su IdSchedaConto, IdAnagrafica

### Compatibilità
- SQL Server syntax (GETDATE, TOP, STRING_AGG)
- pymssql connector

---

*Cervella Data - "I dati non mentono, bisogna saperli leggere"* 📊

*Sessione 320 - Studio Approfondito Database Ericsoft*
