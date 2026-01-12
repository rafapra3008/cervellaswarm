# VISIONE REVENUE INTELLIGENCE - Futuro

> **Data:** 12 Gennaio 2026 - Sessione 169
> **Autore:** Rafa + Regina
> **Status:** IDEE DA DOCUMENTARE (non implementare ora)

---

## 1. EVOLUZIONE SUGGERIMENTI AI

### Situazione Attuale
- 4 tipi di suggerimenti basati su regole
- Weekend, eventi, bassa domanda, YoY

### Visione Futura

**A) Studiare Big Players**
- Analizzare cosa fanno IDeaS, Duetto, RateGain, PriceLabs
- Capire quali tipi di suggerimenti offrono
- Identificare pattern che possiamo replicare

**B) Nuove Tipologie Suggerimenti**
| Tipo | Descrizione | Priorita |
|------|-------------|----------|
| Last-Minute | Prezzi dinamici per date vicine | Alta |
| Far-Out | Strategia per prenotazioni anticipate | Alta |
| Competitor-Based | Reagire ai prezzi competitor | Media |
| Event-Driven | Suggerimenti per eventi locali | Media |
| Weather-Based | Adattarsi a previsioni meteo | Bassa |
| Group/MICE | Suggerimenti per gruppi/eventi | Bassa |

**C) AI che Impara**
- Il sistema deve imparare dalle decisioni umane
- Se Revenue Manager rifiuta suggerimento, capire perche
- Adattare confidence score basato su storico accettazione
- Retraining periodico del modello

---

## 2. SISTEMA MANUALE + AI SUPERVISOR

### Concetto
Il Revenue Manager puo fare modifiche MANUALI ai prezzi, e AI:
1. **Traccia** ogni modifica manuale
2. **Analizza** l'impatto della modifica
3. **Impara** dai pattern del Revenue Manager
4. **Suggerisce** miglioramenti basati sui risultati

### Flusso

```
+----------------+     +-------------+     +-------------+
| Revenue Manager| --> | Modifica    | --> | AI Analizza |
| cambia prezzo  |     | salvata in  |     | e traccia   |
| manualmente    |     | pricing_    |     | performance |
|                |     | history     |     |             |
+----------------+     +-------------+     +-------------+
                                                  |
                                                  v
                            +---------------------+
                            | Dopo X giorni:      |
                            | - Occupancy delta?  |
                            | - Revenue delta?    |
                            | - Era scelta giusta?|
                            +---------------------+
                                                  |
                                                  v
                            +---------------------+
                            | AI impara pattern:  |
                            | - Revenue Manager   |
                            |   alza prezzi quando|
                            |   occupancy > 80%   |
                            | - Suggerisco io?    |
                            +---------------------+
```

### Storico e Analisi

**Cosa tracciare:**
- Ogni modifica manuale (chi, quando, perche)
- Metriche prima/dopo
- Confronto con suggerimento AI (se esisteva)
- Esito finale (successo/neutro/fallimento)

**Dashboard Analytics:**
- Quante modifiche manuali vs AI-suggested
- Acceptance rate AI
- Performance modifiche manuali vs AI
- Trend nel tempo

---

## 3. REVENUE INTELLIGENCE AVANZATA

### Fase Attuale
- Suggerimenti base
- Tracking azioni
- Performance evaluation

### Fasi Future

**Fase A: ML Enhancement (GAP #3)**
- Training con dati storici
- Feature engineering avanzato
- Confidence scoring dinamico
- Retraining schedulato

**Fase B: What-If Simulator (GAP #4)**
- "Cosa succede se metto X?"
- Simulazione impatto su occupancy
- Confronto scenari
- Ottimizzazione automatica

**Fase C: Autopilot Completo**
- AI applica suggerimenti automaticamente
- Regole di sicurezza (min/max, % variazione)
- Revenue Manager approva solo eccezioni
- Learning continuo

**Fase D: Competitive Intelligence**
- Monitoraggio prezzi competitor real-time
- Alerting su cambi significativi
- Strategie di risposta automatiche
- Positioning analysis

**Fase E: Demand Forecasting**
- Previsione domanda ML-based
- Integrazione dati esterni (eventi, meteo, voli)
- Forecast accuracy tracking
- Ottimizzazione inventory

---

## 4. ARCHITETTURA NECESSARIA

### Database
| Tabella | Scopo | Esiste |
|---------|-------|--------|
| pricing_history | Audit trail prezzi | SI |
| suggestion_performance | Metriche suggerimenti | SI |
| ml_training_samples | Dati per training | NO |
| competitor_tracking | Prezzi competitor | PARZIALE |
| demand_forecast | Previsioni | NO |
| manual_decisions | Decisioni manuali | NO |

### API
| Endpoint | Scopo | Esiste |
|----------|-------|--------|
| /api/ml/train | Trigger retraining | NO |
| /api/ml/what-if | Simulazione | PARZIALE |
| /api/analytics/manual-vs-ai | Confronto | NO |
| /api/competitor/alert | Alert competitor | NO |

### Frontend
| Componente | Scopo | Esiste |
|------------|-------|--------|
| AI Health Dashboard | Salute modello | SI |
| What-If Modal | Simulazione | PARZIALE |
| Manual Decision Logger | Log decisioni | NO |
| Competitor Monitor | Visualizza competitor | PARZIALE |

---

## 5. PRIORITA SUGGERITE

### Breve Termine (1-2 mesi)
1. Completare GAP #3 (ML samples e training)
2. Completare GAP #4 (What-If simulator)
3. Migliorare tracking modifiche manuali

### Medio Termine (3-6 mesi)
4. Dashboard analytics manuale vs AI
5. Autopilot con regole di sicurezza
6. Competitive intelligence base

### Lungo Termine (6-12 mesi)
7. Demand forecasting ML
8. Integrazione dati esterni
9. Ottimizzazione inventory automatica

---

## 6. DOMANDE APERTE

1. Quanti hotel prima di avere dati sufficienti per ML?
2. Qual e il minimo di storico per training efficace?
3. Come bilanciare AI autonomia vs controllo umano?
4. Competitor data: scraping o API ufficiali?
5. Pricing: feature premium o inclusa?

---

*"Non facciamo ora, ma documentiamo bene per il futuro!"*

*Sessione 169 - Regina & Rafa*
