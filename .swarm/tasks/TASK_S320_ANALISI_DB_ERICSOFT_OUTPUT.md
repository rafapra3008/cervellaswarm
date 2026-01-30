# Output: Studio Database Ericsoft

## Status
✅ **COMPLETO**

## Fatto
Creato piano analisi completo per capire perché vediamo solo 16 ospiti.

## File Creati

### 1. SQL Analysis (Query)
**Path:** `miracollogeminifocus/miracallook/backend/sql_analysis_ericsoft.sql`
- 10 query SQL per analisi approfondita
- Commenti su ogni query (cosa testa, perché)
- Sicure (READ-ONLY, con LIMIT/TOP)

### 2. Python Analyzer
**Path:** `miracollogeminifocus/miracallook/backend/analyze_ericsoft_db.py`
- Esegue le 10 query in sequenza
- Output console (human-readable) + JSON
- Riepilogo finale con insights

### 3. Piano Strategico
**Path:** `.sncp/progetti/miracollo/bracci/miracallook/ANALISI_DB_ERICSOFT_S320.md`
- Contesto problema
- 4 Proposte query (A, B, C, D)
- Piano verifica dati
- Checklist decisionale

### 4. Quick Start
**Path:** `miracollogeminifocus/miracallook/backend/README_ANALISI_DB.md`
- Come eseguire analisi
- Output esempio
- Troubleshooting

## Query Principali

### Q1: Email Split
Conta ospiti CON email vs SENZA email
→ **Ipotesi:** Filtro email esclude molti

### Q2: Distribuzione Stati
Conta per `IdStatoScheda`
→ **Ipotesi:** Stati non compresi completamente

### Q3: Tutti Ospiti Attivi
TUTTI (no filtro email, solo date + cancellazione)
→ **NUMERO REALE** ospiti in casa

### Q4-9: Altre Analisi
- Campi timestamp (rilevare modifiche)
- Cancellazioni
- Stati 2 e 3 vs date
- Schede multiple ospiti
- JOIN camera
- Periodi date

## Proposte Query Corrette

### A: Tutti Ospiti (No Filtro Email)
Per dashboard totali. Include campo `has_email`.

### B: Solo Con Email (Attuale, ma OK se...)
Per Miracollook. Query attuale è corretta SE i 16 sono SOLO quelli con email.

### C: Filtro Stati invece Date
Se `IdStatoScheda` è fonte verità. Stati 2, 3 (+ forse 1?).

### D: Ibrida (Date + Stati)
Massima sicurezza. Cattura sia per date che stati.

## Come Rafa Esegue

```bash
cd ~/Developer/miracollogeminifocus/miracallook/backend
python analyze_ericsoft_db.py
```

**Output:**
- Console: tabelle formattate
- JSON: `ericsoft_analysis_TIMESTAMP.json`

## Insights Attesi

1. **Perché 16?** → Query 1, 3 rispondono
2. **Stati mapping?** → Query 2 + eventuale Query 10
3. **Modifiche come?** → Query 4 cerca campi timestamp
4. **Cancellazioni OK?** → Query 5, 6 verificano

## Performance

- 9-10 query (Query 10 potrebbe fallire se no tabella)
- Tempo: ~5 min (dipende DB size)
- Sicurezza: Circuit breaker, timeout 5s, READ-ONLY

## Next

1. Rafa esegue analisi (rete hotel o VPN)
2. Valuta risultati JSON
3. Sceglie query corretta (A, B, C, D)
4. Cervella Backend aggiorna `connector.py`
5. Test nuova query
6. WireGuard per accesso remoto

## Note

**DECISIONE REGINA:** Query attuale potrebbe essere GIÀ corretta!
Se hotel ha 40 ospiti ma solo 16 con email → Miracollook vede solo quelli (perché deve inviare email).

Ma serve **conferma** tramite analisi.

---

*Cervella Data - S320*
