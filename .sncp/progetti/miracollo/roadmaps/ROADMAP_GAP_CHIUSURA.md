# ROADMAP GAP - Chiusura Definitiva
> Creato: 12 Gennaio 2026 - Sessione 171
> Obiettivo: Togliere i GAP dalla testa, uno alla volta

---

## Filosofia

> "Lavoriamo in pace! Togliamo questi di testa!"
> "Una cosa alla volta, fatta BENE"

---

## Stato GAP

| GAP | Nome | Status | Priorità |
|-----|------|--------|----------|
| #1 | Price History | RISOLTO | - |
| #2 | Modal Preview | DA TESTARE | P0 |
| #3 | ML Samples | RICERCA OK | P2 |
| #4 | What-If Simulator | RICERCA OK | P1 |

---

## GAP #1 - Price History

### Status: RISOLTO

**Cosa era:** Timeline prezzi non mostrava dati corretti
**Cosa fatto:** Fix API endpoint + date format + campo names
**Verifica:** 50 record mostrati, funziona

**Azione:** NESSUNA - Chiuso!

---

## GAP #2 - Modal Preview

### Status: DA TESTARE

**Cosa era:** Modal preview suggerimento non mostrava dati corretti
**Cosa fatto:** Backend aggiornato, campi allineati

**Test necessario:**
1. [ ] Creare nuovo suggerimento pricing su VM
2. [ ] Verificare che il modal mostri tutti i campi
3. [ ] Verificare formattazione date e prezzi
4. [ ] Screenshot di conferma

**Tempo stimato:** 30 minuti

**Come testare:**
```bash
# SSH alla VM
ssh miracollo-cervella

# Verificare API suggestions
curl https://api.miracollo.com/api/v1/pricing/suggestions

# Creare nuovo suggerimento (da RateBoard UI)
# Poi verificare modal preview
```

**Criterio di successo:** Modal mostra tutti i dati corretti

---

## GAP #3 - ML Samples

### Status: RICERCA COMPLETATA

**Cosa era:** Quanti dati servono per ML? Come raccoglierli?

**Ricerca completata:** `.sncp/progetti/miracollo/idee/20260112_RICERCA_GAP3_GAP4_ML_WHATIF.md`

**Scoperte chiave:**
- Minimum samples: 500 (2-3 mesi raccolta)
- Optimal samples: 1000+ (4-6 mesi)
- Retraining: ogni 7-14 giorni
- Algoritmo: XGBoost (MVP) → Q-Learning (Advanced)

**Decisione necessaria:**
- [ ] Quando iniziare implementazione?
- [ ] Prima What-If o prima ML?

**Raccomandazione:** What-If PRIMA di ML (valore immediato)

---

## GAP #4 - What-If Simulator

### Status: RICERCA COMPLETATA

**Cosa era:** Simulatore "cosa succede se cambio prezzo?"

**Ricerca completata:** `.sncp/progetti/miracollo/idee/20260112_RICERCA_GAP3_GAP4_ML_WHATIF.md`

**Scoperte chiave:**
- UI: React + TypeScript + Slider + Grafici
- Backend: FastAPI endpoints
- Valore: IMMEDIATO - utenti vedono subito
- Complessità: MEDIA - più UI che algoritmo

**Raccomandazione:** Fare PRIMA del ML avanzato perché:
1. Dà valore SUBITO agli utenti
2. Costruisce fiducia nel sistema
3. Funziona anche con ML semplice

---

## Piano d'Azione

### FASE 1: Chiudere GAP #2

```
[ ] Test GAP #2 Modal Preview
    - SSH a VM
    - Creare suggerimento
    - Verificare modal
    - Screenshot conferma
    - Marcare RISOLTO
```

### FASE 2: Decisione GAP #3 e #4

```
[ ] Decidere priorità tra ML e What-If
[ ] Decidere quando iniziare
[ ] Aggiornare roadmap Revenue
```

**La mia raccomandazione:**
1. What-If Simulator PRIMA
2. ML Base DOPO

**Perché:** What-If dà valore SUBITO, ML richiede tempo raccolta dati

### FASE 3: Implementazione (Future Sessioni)

Da pianificare dopo decisione Rafa.

---

## File di Riferimento

| File | Contenuto |
|------|-----------|
| `idee/20260112_RICERCA_GAP3_GAP4_ML_WHATIF.md` | Ricerca completa (1600+ righe) |
| `reports/DEBUG_GAP1_PRICE_HISTORY.md` | Debug GAP #1 |
| `reports/MAPPA_REVENUE_INTELLIGENCE_166.md` | Mappa sistema Revenue |
| `roadmaps/20260112_ROADMAP_REVENUE_7_TO_10.md` | Roadmap Revenue generale |

---

## Principio Guida

```
+================================================================+
|                                                                |
|   "RateBoard PERFETTO > Nuove Features"                        |
|                                                                |
|   Prima: chiudere GAP esistenti                                |
|   Poi: aggiungere nuove funzionalità                           |
|                                                                |
|   I dettagli fanno SEMPRE la differenza!                       |
|                                                                |
+================================================================+
```

---

*Roadmap creata con calma e pace*
*12 Gennaio 2026 - Sessione 171*
