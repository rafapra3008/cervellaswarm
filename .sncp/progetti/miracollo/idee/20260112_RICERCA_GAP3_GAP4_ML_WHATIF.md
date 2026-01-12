# RICERCA: GAP #3 (ML Training) e GAP #4 (What-If Simulator)
## Revenue Intelligence - Miracollo

**Data**: 12 Gennaio 2026
**Ricercatrice**: Cervella Researcher
**Progetto**: Miracollo Revenue Intelligence
**Status**: ✅ Ricerca Completata

---

## EXECUTIVE SUMMARY

**TL;DR**: Ho studiato come i big player (IDeaS, Duetto, RateGain) implementano ML training e simulatori what-if per pricing dinamico hotel. La chiave è il **feedback loop intelligente** + **UI che costruisce fiducia**.

### Cosa Ho Scoperto

1. **ML Training richiede ~500+ samples minimi**, meglio 1000+ per convergenza
2. **Retraining ogni 7-14 giorni** per hotel con volumi normali
3. **Feature engineering = 15-20 features** (pace, competitor, eventi, meteo, etc.)
4. **What-If Simulator = React dashboard** con slider + grafici impatto real-time
5. **Architettura ibrida**: FastAPI + PostgreSQL partitioned + React TypeScript

### Raccomandazione Principale

**APPROCCIO IBRIDO GRADUATO:**
- Sprint 1-2: Tracking + Database (fondamenta)
- Sprint 3-4: ML Pipeline base (semplice, poi migliorare)
- Sprint 5-6: What-If Simulator (valore immediato per utenti)
- Sprint 7+: Refinement ML (quando abbiamo dati reali)

**PERCHÉ**: What-If Simulator dà valore SUBITO (anche senza ML perfetto), mentre ML migliora gradualmente con dati reali.

---

## PARTE 1: GAP #3 - ML ENHANCEMENT

### 1.1 Come Funziona il Training nei Big Player

#### IDeaS vs Duetto - Approcci Diversi

**IDeaS** (Approccio Strutturato):
- Predictive algorithms basati su data analysis massiva
- Training batch schedulato (probabilmente settimanale/mensile)
- Focus su consistenza e performance stabile
- Metodico, meno agile ma più affidabile

**Duetto** (Approccio Agile):
- Open Pricing con ML real-time
- **Collaborative AI**: impara dalle decisioni umane
- Self-learning engines che si aggiornano migliaia di volte al giorno
- Riduce override utente attraverso fiducia costruita nel tempo

**Fonte chiave**: [IDeaS vs Duetto Comparison](https://www.epic-rev.com/post/ideas-vs-duetto-the-ultimate-showdown-of-revenue-management-systems-for-hotels)

#### Il Modello "Collaborative AI" di Duetto

```
Human Decision → ML Observes → ML Adapts → Suggests Better → Human Trusts More
                                    ↑                              ↓
                                    └──────── Feedback Loop ───────┘
```

**INSIGHT CRITICO**: Non è solo "ML fa suggerimenti", ma "ML impara da cosa accetti/rifiuti".

**Citazione chiave**:
> "With a thorough understanding of the system and following a strategic workflow, users rarely override Duetto's pricing recommendations."

Questo significa che il **tasso di acceptance** diventa automaticamente **metrica di qualità del modello**.

---

### 1.2 Feature Engineering - Cosa Serve al Modello

#### Le 5 Categorie di Features (da ricerca 2026)

**Fonte principale**: [How AI Will Rewrite Hotel RMS 2026](https://hoteltechnologynews.com/2025/11/how-ai-will-rewrite-hotel-revenue-management-systems-in-2026/)

```
1. DEMAND SIGNALS (Real-Time)
   - Booking pace (velocità prenotazioni)
   - Look-to-book ratio (quanti guardano vs prenotano)
   - Occupancy rate attuale
   - Pickup rate (quanto si riempie vs forecast)
   - Lead time (quanto in anticipo prenotano)

2. COMPETITOR INTELLIGENCE
   - Prezzi competitor (min 3-5 competitor)
   - Timing dei loro cambi prezzo
   - Pattern di risposta a eventi
   - Position relativa (siamo sopra/sotto?)

3. MARKET CONTEXT
   - Eventi locali (concerti, fiere, sport)
   - Meteo previsto (impatta weekend/vacanze)
   - Search trends (metasearch data)
   - Flight demand (voli verso la destinazione)
   - Social event density (cosa succede in città)

4. HISTORICAL PATTERNS
   - Stagionalità (alta/bassa stagione)
   - Day of week patterns (weekend vs weekday)
   - Cancellation rate storico
   - No-show rate storico
   - RevPAR storico per periodo simile

5. INTERNAL OPERATIONS
   - Costi operativi variabili
   - Min/max price boundaries (policy aziendale)
   - Segment mix target (FIT, Group, OTA)
   - Channel distribution strategy
```

**Fonte dettagliata**: [Dynamic Pricing ML Feature Engineering](https://www.valuecoders.com/blog/ai-ml/leveraging-ai-for-dynamic-pricing-in-hospitality-sector/)

#### Feature Prioritization per Miracollo

**FASE 1 - MVP (Sprint 1-3)**: 5-8 features
```
✅ Occupancy rate
✅ Booking pace (last 7 days)
✅ Lead time
✅ Day of week
✅ Seasonality (high/low season flag)
✅ Competitor avg price (se disponibile)
✅ Historical RevPAR stesso periodo
✅ Current price acceptance rate
```

**FASE 2 - Enhanced (Sprint 4-6)**: +7 features
```
✅ Eventi locali (API esterna o manuale)
✅ Meteo forecast
✅ Cancellation rate trend
✅ Search/inquiry volume
✅ Competitor price delta (quanto siamo sopra/sotto)
✅ Segment mix attuale
✅ Channel performance
```

**FASE 3 - Advanced (Sprint 7+)**: +5 features
```
✅ Flight demand data
✅ Social media buzz (eventi trending)
✅ Website heatmaps (dove cliccano)
✅ Abandoned booking rate
✅ Competitor pricing velocity (quanto veloce cambiano)
```

---

### 1.3 Training Samples - Quanti Servono?

#### Ricerca su Minimum Viable Dataset

**Fonte**: [ML Model Training Requirements](https://labelyourdata.com/articles/machine-learning/model-training)

**Regole generali ML**:
- Image recognition: migliaia di samples
- Pricing/regression: 100-1000+ samples (dipende da features)
- Time series: minimo 2-3 cicli completi (es. 2-3 anni per stagionalità)

**Per Hotel Pricing specifico**:

```
MINIMUM VIABLE: 500 samples
- 500 decisioni tracciare = ~2-3 mesi per hotel medio
- Permette primo training "naive"
- Accuracy bassa (60-70%), ma meglio di niente

RECOMMENDED: 1000-2000 samples
- 1000+ decisioni = ~4-6 mesi raccolta dati
- Training più robusto
- Accuracy media (75-85%)
- Sufficiente per produzione

OPTIMAL: 5000+ samples
- 1+ anno di dati
- Copre stagionalità completa
- Accuracy alta (85-95%)
- Confident deployment
```

**INSIGHT per Miracollo**:
Non aspettare 5000 samples! Fare training incrementale:
1. Primo training a 500 samples (baseline naive)
2. Retraining a 1000 samples (primo miglioramento)
3. Retraining ogni +500 samples fino a 5000
4. Poi retraining schedulato (vedi sotto)

---

### 1.4 Retraining Frequency - Quanto Spesso?

#### Strategie dai Big Player

**Fonte**: [ML Pipeline Retraining Strategies](https://www.altexsoft.com/blog/machine-learning-pipeline/)

**3 Approcci possibili**:

```
1. SCHEDULED RETRAINING (più semplice)
   - Fisso: ogni 7, 14, 30 giorni
   - Pro: prevedibile, facile da implementare
   - Contro: può essere troppo frequente (spreca) o troppo raro (drift)
   - Usano: hotel con pattern stabili

2. PERFORMANCE-BASED (più smart)
   - Trigger: quando accuracy scende sotto soglia
   - Pro: efficiente, retrain solo quando serve
   - Contro: richiede monitoring continuo
   - Usano: sistemi ML maturi

3. CONTINUOUS LEARNING (più avanzato)
   - Real-time: modello si aggiorna continuamente
   - Pro: sempre aggiornato
   - Contro: complesso, costoso computazionalmente
   - Usano: Duetto e altri enterprise RMS
```

**Raccomandazione per Miracollo**:

**FASE 1 (primi 6 mesi)**:
- Scheduled retraining ogni **14 giorni**
- Motivo: vogliamo dati freschi mentre impariamo

**FASE 2 (6-12 mesi)**:
- Scheduled retraining ogni **7 giorni**
- Aggiungiamo monitoring: alert se accuracy < 75%
- Trigger manuale se performance degrada

**FASE 3 (12+ mesi)**:
- Hybrid: scheduled **weekly** + performance-based triggers
- Auto-retrain se accuracy scende sotto 80% per 3 giorni consecutivi
- Monitoring drift con [Evidently AI](https://www.evidentlyai.com/blog/fastapi-tutorial)

---

### 1.5 Algoritmi ML - Cosa Usare?

#### Ricerca su Reinforcement Learning vs Supervised Learning

**Fonti**:
- [Q-Learning for Hotel Pricing](https://www.tandfonline.com/doi/full/10.1080/03155986.2023.2235223)
- [Deep RL for Dynamic Pricing](https://www.mdpi.com/0718-1876/20/4/337)

#### Confronto Approcci

**SUPERVISED LEARNING** (Regressione, Gradient Boosting):
```
✅ Pro:
- Più semplice da implementare
- Richiede meno dati per convergere
- Interpretabile (vedi quali features contano)
- Scikit-learn, XGBoost, LightGBM pronte

❌ Contro:
- Non impara da feedback (accetto/rifiuto)
- Statico (non migliora da solo)
- Richiede retraining esplicito
```

**REINFORCEMENT LEARNING** (Q-Learning, SARSA, Deep Q-Learning):
```
✅ Pro:
- Impara da reward (acceptance = +1, rejection = -1)
- Self-improving nel tempo
- Adatta pricing strategy dinamicamente
- Esplora nuove strategie (exploration)

❌ Contro:
- Complesso da implementare
- Richiede molti più samples (1000+)
- Training più lento
- Può essere instabile inizialmente
```

**Ricerca evidenza**:
> "Q-learning has better performance than SARSA as it achieves higher profits and lower volatility"
> "Deep reinforcement learning algorithms can learn better pricing strategies than tabular Q-learning"

#### Raccomandazione per Miracollo

**APPROCCIO GRADUATO**:

**Sprint 1-4: Supervised Learning (Gradient Boosting)**
```python
# XGBoost o LightGBM
- Input: features (occupancy, pace, competitor, etc.)
- Output: suggested_price
- Training: su decisioni passate (acceptance rate come peso)
- Semplice, veloce, interpretabile
```

**Sprint 5-8: Hybrid (Supervised + Acceptance Feedback)**
```python
# Supervised con re-weighting
- Usa acceptance_rate per pesare training samples
- Samples accettati → peso 1.0
- Samples rifiutati → peso 0.3
- Migliora gradualmente verso ciò che funziona
```

**Sprint 9+: Reinforcement Learning (se volumi OK)**
```python
# Q-Learning o Deep Q-Learning
- State: (occupancy, pace, lead_time, competitor_delta, ...)
- Action: price adjustment (-10%, -5%, 0%, +5%, +10%)
- Reward: acceptance (1.0) vs rejection (-0.5)
- Policy: epsilon-greedy (exploration + exploitation)
```

**PERCHÉ questo ordine?**
1. Supervised = risultati veloci, valore immediato
2. Hybrid = migliora senza riscrivere tutto
3. RL = quando abbiamo dati sufficienti e vogliamo optimum

---

### 1.6 Preventing Feedback Loops - CRITICAL!

**PROBLEMA REALE**: [ML Feedback Loops in Pricing](https://arxiv.org/abs/2302.09438)

#### Il Rischio

```
ML suggerisce prezzo alto → Utente accetta → Prezzo alto diventa training data
    → ML impara "prezzo alto è giusto" → Suggerisce ancora più alto
        → Utente accetta (fiducia cieca) → LOOP INFINITO = Overpricing!
```

**Citazione chiave**:
> "Machine learning-based prices anchor the realized sales prices, which will in turn become training samples for future iterations, leading algorithms to become overconfident in their own accuracy."

#### Soluzioni dai Paper

**1. Delayed Feedback Buffer**
```python
# Non trainare su decisioni immediate
# Attendere 30-60 giorni per vedere RISULTATO REALE:
# - Prezzo accettato → occupancy raggiunta? Revenue OK?
# - Prezzo rifiutato → era davvero troppo alto? O troppo basso?

training_data = decisions.filter(
    created_at < today - 60_days,
    has_outcome_data=True  # occupancy finale, revenue reale
)
```

**2. Exploration Strategy (Epsilon-Greedy)**
```python
# 10-20% delle volte, suggerisci prezzo RANDOM (esplora)
# Evita che ML si "innamori" di una strategia sola

if random() < 0.15:  # 15% exploration
    suggested_price = explore_random_price()
else:  # 85% exploitation
    suggested_price = ml_model.predict()
```

**3. Human-in-the-Loop Validation**
```python
# Flagga suggerimenti "estremi" per review umana
# Es: +20% vs ieri, o -15% vs competitor

if abs(price_delta) > 0.15:
    require_manual_approval = True
    explanation_required = True
```

**4. A/B Testing Continuo**
```python
# 10% traffico = prezzo ML
# 10% traffico = prezzo regola semplice (baseline)
# Confronta performance settimana dopo settimana

if ab_group == 'control':
    use_rule_based_price()
else:
    use_ml_price()
```

**Raccomandazione Miracollo**:
- Implementare **Delayed Feedback** (Sprint 3)
- Implementare **Exploration 15%** (Sprint 4)
- Implementare **Human validation** per delta > 15% (Sprint 2)
- A/B testing opzionale (Sprint 6+, quando volumi OK)

---

### 1.7 Database Schema - Tracking Decisioni

#### Schema Proposto PostgreSQL

```sql
-- Tabella principale: decisioni AI tracciare
CREATE TABLE ai_pricing_decisions (
    id BIGSERIAL PRIMARY KEY,

    -- Contesto
    property_id BIGINT NOT NULL,
    room_type_id BIGINT,
    date_target DATE NOT NULL,  -- per quale data il prezzo
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    -- Input Features (JSON per flessibilità)
    features JSONB NOT NULL,
    /*
    {
        "occupancy_rate": 0.65,
        "booking_pace_7d": 12,
        "lead_time_days": 45,
        "day_of_week": "Friday",
        "season": "high",
        "competitor_avg_price": 120.0,
        "historical_revpar": 95.0,
        "events": ["concert", "festival"],
        "weather_forecast": "sunny"
    }
    */

    -- ML Suggestion
    suggested_price DECIMAL(10,2) NOT NULL,
    suggestion_confidence DECIMAL(3,2),  -- 0.0-1.0
    model_version VARCHAR(50) NOT NULL,  -- "v1.2.3"

    -- Human Decision
    user_decision VARCHAR(20),  -- 'accepted', 'rejected', 'modified', 'pending'
    final_price DECIMAL(10,2),
    user_id BIGINT,
    decision_at TIMESTAMP,

    -- Outcome (delayed, filled later)
    outcome_occupancy_rate DECIMAL(3,2),
    outcome_revenue DECIMAL(10,2),
    outcome_competitor_position VARCHAR(20),  -- 'above', 'below', 'match'
    outcome_evaluated_at TIMESTAMP,

    -- Indexes
    INDEX idx_property_date (property_id, date_target),
    INDEX idx_created_at (created_at),
    INDEX idx_user_decision (user_decision),
    INDEX idx_outcome (outcome_evaluated_at) WHERE outcome_evaluated_at IS NOT NULL
);

-- Partitioning per performance (time-series data)
CREATE TABLE ai_pricing_decisions_y2026m01
    PARTITION OF ai_pricing_decisions
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');

CREATE TABLE ai_pricing_decisions_y2026m02
    PARTITION OF ai_pricing_decisions
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
-- etc per ogni mese

-- Tabella: Training Runs
CREATE TABLE ml_training_runs (
    id BIGSERIAL PRIMARY KEY,
    model_version VARCHAR(50) NOT NULL,
    started_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,

    -- Training Config
    algorithm VARCHAR(50),  -- 'xgboost', 'lightgbm', 'q_learning'
    hyperparameters JSONB,

    -- Training Data
    samples_count INT,
    samples_date_from DATE,
    samples_date_to DATE,

    -- Performance Metrics
    accuracy DECIMAL(5,4),
    mae DECIMAL(10,2),  -- Mean Absolute Error
    rmse DECIMAL(10,2),  -- Root Mean Squared Error
    acceptance_rate DECIMAL(3,2),  -- % di suggerimenti accettati

    -- Deployment
    deployed_at TIMESTAMP,
    is_active BOOLEAN DEFAULT FALSE,

    INDEX idx_version (model_version),
    INDEX idx_active (is_active) WHERE is_active = TRUE
);

-- Tabella: Model Performance Monitoring
CREATE TABLE ml_model_metrics (
    id BIGSERIAL PRIMARY KEY,
    model_version VARCHAR(50) NOT NULL,
    measured_at TIMESTAMP NOT NULL,

    -- Drift Detection
    feature_drift_score DECIMAL(5,4),
    prediction_drift_score DECIMAL(5,4),

    -- Performance
    rolling_7d_accuracy DECIMAL(5,4),
    rolling_7d_acceptance_rate DECIMAL(3,2),
    rolling_7d_avg_error DECIMAL(10,2),

    -- Alert
    requires_retraining BOOLEAN DEFAULT FALSE,

    INDEX idx_version_measured (model_version, measured_at)
);
```

**Fonte design**: [PostgreSQL Time Series Best Practices](https://aws.amazon.com/blogs/database/designing-high-performance-time-series-data-tables-on-amazon-rds-for-postgresql/)

#### Partitioning Strategy

**PERCHÉ Partitioning?**
- Dati time-series crescono velocemente (100+ decisioni/giorno = 36K/anno)
- Query tipiche = "ultimi 90 giorni" → partition pruning velocizza
- Drop old partitions facile per GDPR/retention policy

**Fonte**: [PostgreSQL Partitioning for Time Series](https://stormatics.tech/blogs/improving-postgresql-performance-with-partitioning)

**Raccomandazione**:
- Partition MONTHLY per primi 2 anni
- Se volumi >10K decisioni/mese → switch a WEEKLY partitions
- Retention: 24 mesi, poi archive o drop

---

## PARTE 2: GAP #4 - WHAT-IF SIMULATOR

### 2.1 Cosa Fanno i Competitor

#### Power BI Revenue Management Dashboard

**Fonte**: [Hotel Revenue Management Dashboard - Microsoft](https://marketplace.microsoft.com/en-us/product/power-bi/iop1700042055418.pbiapp001)

**Features chiave**:
```
✅ Live What-If Scenarios
   - Adjust price → see impact on occupancy, revenue, RevPAR
   - Slider-based input (price -20% to +30%)
   - Real-time calculation

✅ KPI Dashboard
   - ADR (Average Daily Rate)
   - RevPAR (Revenue Per Available Room)
   - OCC (Occupancy Rate)
   - Segmentation (FIT, Group, OTA)

✅ Forecast Integration
   - Incorporate forecast data from external tools
   - Run scenarios on future dates
```

#### UI/UX Patterns Emersi

**Fonte**: [2026 Hotel Pricing Trends](https://www.hospitalitynet.org/opinion/4130285.html)

**Principi chiave**:

1. **Reduce Cognitive Load**
   > "Tools should reduce workload, not add oversight. Systems requiring constant monitoring don't solve the labor problem."

2. **Build Trust Through Transparency**
   > "The best AI pricing tools make confident decisions and keep humans informed."

3. **Natural Language Explanations**
   > "AI copilots embedded inside RMS dashboards transform complex data into natural language explanations."

4. **Manual Override Always Available**
   > "Manual override capabilities and locked pricing for specific date ranges when needed."

---

### 2.2 What-If Simulator - Specifiche Funzionali

#### User Stories

```
US-1: Come revenue manager, voglio regolare il prezzo con uno slider
      per vedere l'impatto su occupancy e revenue previsti.

US-2: Come revenue manager, voglio confrontare 3-5 scenari side-by-side
      per scegliere la strategia migliore.

US-3: Come revenue manager, voglio capire PERCHÉ il sistema prevede
      un certo impatto (spiegazione ML).

US-4: Come revenue manager, voglio salvare scenari favoriti
      e applicarli rapidamente.

US-5: Come revenue manager, voglio vedere la posizione competitiva
      prevista per ogni scenario (above/below/match competitors).
```

#### Features MVP (Sprint 5-6)

**INPUT**:
```
- Property selector
- Date range selector (single date o range 7-30 giorni)
- Room type selector
- Price adjustment: slider -30% to +50%
```

**CALCULATION** (real-time):
```
- Occupancy impact: +/- %
- Revenue impact: +/- €
- RevPAR impact: +/- €
- Competitor position: above/below/match
- Confidence score: low/medium/high
```

**OUTPUT**:
```
- Cards con KPIs (before → after)
- Grafici:
  * Price vs Occupancy curve
  * Price vs Revenue curve
  * Competitive position bar chart
- Explanation text: "Con prezzo +10%, prevedo occupancy -5%
  ma revenue +8% perché competitor sono a +15% sopra di noi"
```

---

### 2.3 Architecture What-If Simulator

#### Stack Tecnologico

**Frontend**: React + TypeScript
```typescript
// Components
- WhatIfSimulator.tsx (container)
- PriceSlider.tsx (Material-UI Slider)
- ImpactCards.tsx (KPI display)
- ComparisonChart.tsx (Recharts)
- ExplanationPanel.tsx (natural language)
```

**Fonti UI Components**:
- [Material-UI Slider](https://mui.com/material-ui/react-slider/)
- [React Pricing Slider Tutorial](https://medium.com/cruip/how-to-build-a-pricing-slider-react-71545d81d63d)

**Backend**: FastAPI + Python
```python
# Endpoint principale
@router.post("/api/v1/what-if/simulate")
async def simulate_pricing_scenario(
    property_id: int,
    date_from: date,
    date_to: date,
    price_adjustment: float,  # -0.3 to +0.5
    room_type_id: Optional[int] = None
) -> WhatIfResult:
    """
    Calcola impatto pricing scenario in real-time.
    """
    # 1. Fetch current context (occupancy, competitor, etc.)
    # 2. Load ML model
    # 3. Predict occupancy at new price
    # 4. Calculate revenue impact
    # 5. Determine competitive position
    # 6. Generate explanation
    return WhatIfResult(...)
```

**Fonte architettura**: [FastAPI for ML Deployment](https://blog.jetbrains.com/pycharm/2024/09/how-to-use-fastapi-for-machine-learning/)

**Database**: PostgreSQL (già esistente)
```sql
-- Cache simulation results per performance
CREATE TABLE what_if_simulations (
    id BIGSERIAL PRIMARY KEY,
    property_id BIGINT NOT NULL,
    date_target DATE NOT NULL,
    price_adjustment DECIMAL(5,2) NOT NULL,

    -- Cached Results
    predicted_occupancy DECIMAL(3,2),
    predicted_revenue DECIMAL(10,2),
    competitor_position VARCHAR(20),
    confidence DECIMAL(3,2),
    explanation TEXT,

    -- Metadata
    model_version VARCHAR(50),
    calculated_at TIMESTAMP DEFAULT NOW(),

    -- TTL: 1 ora (simulations non sono "truth", solo preview)
    INDEX idx_cache (property_id, date_target, price_adjustment),
    INDEX idx_ttl (calculated_at)
);

-- Cleanup job: DELETE WHERE calculated_at < NOW() - INTERVAL '1 hour'
```

---

### 2.4 Calculation Logic - Come Prevedere Impatto

#### Approccio Semplificato (MVP - Sprint 5)

**Elasticity-Based Estimation**:

```python
def calculate_what_if_simple(
    current_price: float,
    new_price: float,
    current_occupancy: float,
    price_elasticity: float = -0.5  # default hotel elasticity
) -> dict:
    """
    Stima semplice basata su price elasticity.

    Elasticity = % change in demand / % change in price
    Hotel tipico: -0.5 (se prezzo +10%, domanda -5%)
    """
    price_change_pct = (new_price - current_price) / current_price
    occupancy_change_pct = price_elasticity * price_change_pct

    new_occupancy = current_occupancy * (1 + occupancy_change_pct)
    new_occupancy = max(0.0, min(1.0, new_occupancy))  # clamp 0-100%

    new_revenue = new_price * new_occupancy * total_rooms
    current_revenue = current_price * current_occupancy * total_rooms

    return {
        'predicted_occupancy': new_occupancy,
        'occupancy_delta': new_occupancy - current_occupancy,
        'predicted_revenue': new_revenue,
        'revenue_delta': new_revenue - current_revenue,
        'confidence': 'low'  # elasticity-based = low confidence
    }
```

#### Approccio ML-Based (Advanced - Sprint 7+)

```python
async def calculate_what_if_ml(
    property_id: int,
    date_target: date,
    new_price: float
) -> dict:
    """
    Usa ML model per previsione accurata.
    """
    # 1. Fetch current features
    features = await get_current_features(property_id, date_target)

    # 2. Override price in features
    features['current_price'] = new_price
    features['price_vs_competitor'] = new_price - features['competitor_avg']

    # 3. ML Prediction
    model = load_active_model()
    predicted_occupancy = model.predict_occupancy(features)
    confidence = model.predict_confidence(features)

    # 4. Calculate revenue
    predicted_revenue = new_price * predicted_occupancy * total_rooms

    # 5. Competitor position
    if new_price > features['competitor_avg'] * 1.1:
        position = 'above'
    elif new_price < features['competitor_avg'] * 0.9:
        position = 'below'
    else:
        position = 'match'

    # 6. Generate explanation
    explanation = generate_explanation(
        features, new_price, predicted_occupancy, position
    )

    return {
        'predicted_occupancy': predicted_occupancy,
        'predicted_revenue': predicted_revenue,
        'competitor_position': position,
        'confidence': confidence,
        'explanation': explanation
    }
```

**Fonte logica**: [Hotel Dynamic Pricing Calculations](https://kodytechnolab.com/blog/how-hotel-dynamic-pricing-works/)

---

### 2.5 UI Design - Wireframe Concettuale

```
┌─────────────────────────────────────────────────────────────┐
│ What-If Pricing Simulator                                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ 📅 Date: Jan 15, 2026    🏠 Property: Villa Bella          │
│ 🛏️  Room Type: Deluxe Suite                                 │
│                                                             │
│ ── Current Price: €120 ─────────────────────────────────── │
│                                                             │
│ New Price:                                                  │
│ €80 ◄─────────●──────────────────────► €180               │
│       -33%         €120 (current)        +50%              │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ IMPACT PREVIEW                                              │
├──────────────────┬──────────────────┬──────────────────────┤
│   OCCUPANCY      │     REVENUE      │   COMPETITOR POS     │
│                  │                  │                      │
│   78% → 82%      │  €9,360 → €9,840 │   Below → Match     │
│   +4% ✅         │   +€480 ✅       │   Neutral 〰️        │
└──────────────────┴──────────────────┴──────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 📊 PRICE vs OCCUPANCY CURVE                                 │
│    100% │                                                   │
│         │         ●  (your scenario)                        │
│     80% │      ●                                            │
│         │   ●                                               │
│     60% │●                                                  │
│         └─────────────────────────────                      │
│          €80   €100  €120  €140  €160                      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 💡 AI EXPLANATION                                           │
│                                                             │
│ "A €120, prevedo occupancy 82% (+4%) perché:               │
│  • Competitors medi a €125 (+4%) - posizione competitiva   │
│  • Booking pace sopra media (+12% vs last week)            │
│  • Weekend con evento locale (Concerto Arena)              │
│  • Stagionalità alta (Gennaio = alta stagione)             │
│                                                             │
│ Revenue totale: +€480 (+5.1%) - scenario ottimale."        │
│                                                             │
│ Confidence: ███████░░░ 75% (High)                          │
└─────────────────────────────────────────────────────────────┘

[Reset]  [Save Scenario]  [Apply This Price] ←─ Actions
```

**Fonte design principles**: [Duetto Training & Adoption](https://www.duettocloud.com/solutions/training-and-adoption)

---

### 2.6 Real-Time vs Batch Calculation

#### Trade-off Analysis

**REAL-TIME** (FastAPI endpoint chiamato on-demand):
```
✅ Pro:
- Sempre dati freschi
- No pre-calculation waste
- Semplice da implementare

❌ Contro:
- Latenza 200-500ms per prediction
- Carico CPU ad ogni slider move
- Può essere lento con UI fluida
```

**BATCH + CACHE** (pre-calcola scenari comuni):
```
✅ Pro:
- Latenza <50ms (cache hit)
- UI super fluida
- Meno carico server

❌ Contro:
- Dati possono essere stale (1-6h vecchi)
- Spreco storage per scenari non usati
- Più complesso (cache invalidation)
```

#### Raccomandazione Hybrid

**Sprint 5-6 (MVP)**: Real-time puro
- Slider onChange → debounce 300ms → API call
- Acceptable UX, semplice implementazione

**Sprint 7+ (Optimization)**: Hybrid
- Pre-calcola 10 scenari comuni (-20%, -10%, ..., +40%, +50%)
- Cache 1 ora
- Slider onChange → se scenario in cache, usa cache, altrimenti real-time
- Best of both worlds

```typescript
// React Hook per debounced simulation
const useDebouncedSimulation = (
  priceAdjustment: number,
  delay: number = 300
) => {
  const [result, setResult] = useState<WhatIfResult | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    const timer = setTimeout(() => {
      // Check cache first
      const cached = checkCache(priceAdjustment);
      if (cached) {
        setResult(cached);
        setLoading(false);
      } else {
        // API call
        fetchSimulation(priceAdjustment).then(setResult);
      }
    }, delay);

    return () => clearTimeout(timer);
  }, [priceAdjustment]);

  return { result, loading };
};
```

---

## PARTE 3: ARCHITETTURA INTEGRATA

### 3.1 System Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         FRONTEND                            │
│                    (React + TypeScript)                     │
├────────────────────┬────────────────────────────────────────┤
│ Revenue Dashboard  │  What-If Simulator │  ML Insights     │
└────────────────────┴────────────────────┴──────────────────┘
                             ↓ REST API
┌─────────────────────────────────────────────────────────────┐
│                      BACKEND (FastAPI)                      │
├─────────────────────────────────────────────────────────────┤
│  /api/v1/pricing/suggest     ← ML Prediction endpoint      │
│  /api/v1/pricing/decide      ← Track human decision        │
│  /api/v1/what-if/simulate    ← What-if simulator           │
│  /api/v1/training/trigger    ← Manual retrain trigger      │
│  /api/v1/metrics/performance ← Model monitoring            │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│                    ML PIPELINE (Python)                     │
├─────────────────────────────────────────────────────────────┤
│  • Feature Engineering                                      │
│  • Model Training (XGBoost/LightGBM → Q-Learning)          │
│  • Model Evaluation                                         │
│  • Model Registry (versions, metrics)                      │
│  • Drift Detection (Evidently AI)                          │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│                  DATABASE (PostgreSQL)                      │
├─────────────────────────────────────────────────────────────┤
│  • ai_pricing_decisions (partitioned by month)             │
│  • ml_training_runs                                         │
│  • ml_model_metrics                                         │
│  • what_if_simulations (cache, TTL 1h)                     │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│                 SCHEDULED JOBS (Celery/Cron)               │
├─────────────────────────────────────────────────────────────┤
│  • Retraining Job (every 7-14 days)                        │
│  • Drift Monitoring (daily)                                 │
│  • Outcome Evaluation (daily, fill delayed feedback)       │
│  • Cache Cleanup (hourly)                                   │
│  • Partition Management (monthly)                           │
└─────────────────────────────────────────────────────────────┘
```

---

### 3.2 API Endpoints Dettagliati

#### 1. GET /api/v1/pricing/suggest

**Purpose**: Ottieni suggerimento prezzo da ML per una data specifica.

```python
@router.get("/api/v1/pricing/suggest")
async def get_pricing_suggestion(
    property_id: int,
    date_target: str,  # "2026-01-15"
    room_type_id: Optional[int] = None
) -> PricingSuggestion:
    """
    Ritorna suggerimento ML + confidence + explanation.
    """
    # 1. Fetch features
    features = await build_features(property_id, date_target, room_type_id)

    # 2. Load active model
    model = load_active_model()

    # 3. Predict
    suggested_price = model.predict(features)
    confidence = model.predict_confidence(features)

    # 4. Generate explanation
    explanation = generate_explanation(features, suggested_price)

    # 5. Save decision (status='pending')
    decision_id = await save_decision(
        property_id=property_id,
        date_target=date_target,
        features=features,
        suggested_price=suggested_price,
        confidence=confidence,
        model_version=model.version,
        user_decision='pending'
    )

    return PricingSuggestion(
        decision_id=decision_id,
        suggested_price=suggested_price,
        confidence=confidence,
        explanation=explanation,
        features_summary={
            'occupancy_rate': features['occupancy_rate'],
            'booking_pace_7d': features['booking_pace_7d'],
            'competitor_avg': features['competitor_avg_price'],
            'events': features.get('events', [])
        }
    )
```

**Response Example**:
```json
{
  "decision_id": 12345,
  "suggested_price": 125.00,
  "confidence": 0.82,
  "explanation": "Prezzo €125 ottimale per 15 Jan perché: occupancy 68% (+5% vs last week), competitors avg €130, evento locale (concerto), stagione alta.",
  "features_summary": {
    "occupancy_rate": 0.68,
    "booking_pace_7d": 14,
    "competitor_avg": 130.00,
    "events": ["concert"]
  }
}
```

---

#### 2. POST /api/v1/pricing/decide

**Purpose**: Tracciare decisione umana (accetto/rifiuto/modifico).

```python
@router.post("/api/v1/pricing/decide")
async def record_pricing_decision(
    decision_id: int,
    user_decision: str,  # 'accepted', 'rejected', 'modified'
    final_price: Optional[float] = None,
    user_id: int = Depends(get_current_user)
) -> dict:
    """
    Salva decisione umana per feedback loop.
    """
    # 1. Validate
    if user_decision not in ['accepted', 'rejected', 'modified']:
        raise HTTPException(400, "Invalid user_decision")

    if user_decision == 'modified' and final_price is None:
        raise HTTPException(400, "final_price required when modified")

    # 2. Update decision record
    await db.execute(
        """
        UPDATE ai_pricing_decisions
        SET user_decision = $1,
            final_price = $2,
            user_id = $3,
            decision_at = NOW()
        WHERE id = $4
        """,
        user_decision,
        final_price,
        user_id,
        decision_id
    )

    # 3. Trigger monitoring (check if acceptance rate dropping)
    await check_model_performance()

    return {"status": "recorded", "decision_id": decision_id}
```

---

#### 3. POST /api/v1/what-if/simulate

**Purpose**: Simulare impatto pricing scenario.

```python
@router.post("/api/v1/what-if/simulate")
async def simulate_pricing_scenario(
    request: WhatIfRequest
) -> WhatIfResult:
    """
    Calcola impatto pricing in real-time.
    """
    # 1. Check cache
    cached = await get_cached_simulation(
        request.property_id,
        request.date_target,
        request.price_adjustment
    )
    if cached and not_expired(cached):
        return cached

    # 2. Fetch current context
    features = await build_features(
        request.property_id,
        request.date_target,
        request.room_type_id
    )
    current_price = features['current_price']
    new_price = current_price * (1 + request.price_adjustment)

    # 3. Calculate impact (ML or elasticity-based)
    if ML_ENABLED:
        result = await calculate_what_if_ml(
            request.property_id,
            request.date_target,
            new_price
        )
    else:
        result = calculate_what_if_simple(
            current_price=current_price,
            new_price=new_price,
            current_occupancy=features['occupancy_rate']
        )

    # 4. Cache result (TTL 1h)
    await cache_simulation(request, result, ttl=3600)

    return WhatIfResult(**result)
```

**Request Example**:
```json
{
  "property_id": 42,
  "date_target": "2026-01-20",
  "room_type_id": 3,
  "price_adjustment": 0.10  // +10%
}
```

**Response Example**:
```json
{
  "predicted_occupancy": 0.75,
  "occupancy_delta": -0.03,
  "predicted_revenue": 9000.00,
  "revenue_delta": 450.00,
  "competitor_position": "match",
  "confidence": 0.78,
  "explanation": "Con prezzo +10% (€132), prevedo occupancy 75% (-3%) ma revenue +€450 (+5%) perché competitors a €135. Posizione competitiva buona."
}
```

---

#### 4. POST /api/v1/training/trigger

**Purpose**: Trigger manuale retraining ML model.

```python
@router.post("/api/v1/training/trigger")
async def trigger_model_retraining(
    min_samples: int = 500,
    force: bool = False,
    user_id: int = Depends(get_admin_user)
) -> dict:
    """
    Avvia retraining job. Admin only.
    """
    # 1. Check samples count
    samples = await count_training_samples()
    if samples < min_samples and not force:
        raise HTTPException(
            400,
            f"Insufficient samples: {samples} < {min_samples}. Use force=true to override."
        )

    # 2. Enqueue training job (Celery/background)
    job = train_model_task.delay(
        samples_date_from=date.today() - timedelta(days=180),
        samples_date_to=date.today(),
        triggered_by=user_id
    )

    return {
        "status": "training_started",
        "job_id": job.id,
        "samples_count": samples
    }
```

---

### 3.3 ML Pipeline - Training Workflow

```python
# celery_tasks.py

@celery_app.task
def train_model_task(
    samples_date_from: date,
    samples_date_to: date,
    triggered_by: int
) -> str:
    """
    Background task: train new model version.
    """
    # 1. Create training run record
    run = create_training_run(
        algorithm='xgboost',  # or 'q_learning' later
        samples_date_from=samples_date_from,
        samples_date_to=samples_date_to
    )

    try:
        # 2. Fetch training data
        data = fetch_training_data(samples_date_from, samples_date_to)

        # 3. Feature engineering
        X, y = prepare_features_and_targets(data)

        # 4. Train/test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, shuffle=True
        )

        # 5. Train model
        model = train_xgboost_model(X_train, y_train)

        # 6. Evaluate
        metrics = evaluate_model(model, X_test, y_test)

        # 7. Save model + metrics
        version = save_model_version(model, metrics, run.id)

        # 8. Update training run
        complete_training_run(
            run.id,
            model_version=version,
            accuracy=metrics['accuracy'],
            mae=metrics['mae'],
            rmse=metrics['rmse']
        )

        # 9. If better than current, mark for deployment
        if should_deploy(metrics):
            mark_for_deployment(version)

        return f"Training completed: {version}"

    except Exception as e:
        fail_training_run(run.id, str(e))
        raise


def train_xgboost_model(X_train, y_train):
    """
    Train XGBoost regressor for pricing.
    """
    import xgboost as xgb

    model = xgb.XGBRegressor(
        objective='reg:squarederror',
        n_estimators=200,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    )

    model.fit(
        X_train,
        y_train,
        eval_set=[(X_train, y_train)],
        verbose=False
    )

    return model


def evaluate_model(model, X_test, y_test):
    """
    Evaluate model performance.
    """
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    import numpy as np

    y_pred = model.predict(X_test)

    return {
        'accuracy': r2_score(y_test, y_pred),  # R² score
        'mae': mean_absolute_error(y_test, y_pred),
        'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
        'samples_count': len(y_test)
    }
```

---

### 3.4 Scheduled Jobs - Cron/Celery Beat

```python
# celerybeat_schedule.py

CELERYBEAT_SCHEDULE = {
    # Retraining ogni 14 giorni
    'retrain-pricing-model': {
        'task': 'train_model_task',
        'schedule': crontab(day_of_month='1,15', hour=2, minute=0),  # 1st and 15th at 2am
        'kwargs': {
            'samples_date_from': date.today() - timedelta(days=180),
            'samples_date_to': date.today(),
            'triggered_by': 0  # system
        }
    },

    # Drift monitoring giornaliero
    'monitor-model-drift': {
        'task': 'monitor_drift_task',
        'schedule': crontab(hour=3, minute=0),  # daily at 3am
    },

    # Evaluate outcomes (fill delayed feedback)
    'evaluate-outcomes': {
        'task': 'evaluate_outcomes_task',
        'schedule': crontab(hour=4, minute=0),  # daily at 4am
    },

    # Cache cleanup
    'cleanup-what-if-cache': {
        'task': 'cleanup_cache_task',
        'schedule': crontab(minute='*/30'),  # every 30 min
    },

    # Partition management (mensile)
    'manage-partitions': {
        'task': 'manage_partitions_task',
        'schedule': crontab(day_of_month=1, hour=1, minute=0),  # 1st of month at 1am
    }
}


@celery_app.task
def monitor_drift_task():
    """
    Controlla drift giornaliero, alert se necessario.
    """
    from evidently.metrics import DataDriftPreset
    from evidently.report import Report

    # 1. Fetch reference data (training set)
    reference_data = fetch_reference_data()

    # 2. Fetch current data (last 7 days)
    current_data = fetch_current_data(days=7)

    # 3. Run drift detection
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=reference_data, current_data=current_data)

    # 4. Extract drift score
    drift_score = report.as_dict()['metrics'][0]['result']['drift_score']

    # 5. Save metric
    save_drift_metric(drift_score)

    # 6. Alert if high drift
    if drift_score > 0.3:
        send_alert(
            type='model_drift',
            message=f'High drift detected: {drift_score:.2f}',
            severity='warning'
        )


@celery_app.task
def evaluate_outcomes_task():
    """
    Riempie outcome data per decisioni passate (delayed feedback).
    """
    # 1. Fetch decisions 60+ giorni fa senza outcome
    decisions = fetch_decisions_without_outcome(days_ago=60)

    for decision in decisions:
        # 2. Fetch actual outcome (occupancy, revenue)
        outcome = fetch_actual_outcome(
            decision.property_id,
            decision.date_target
        )

        # 3. Update decision record
        update_decision_outcome(
            decision.id,
            outcome_occupancy_rate=outcome.occupancy_rate,
            outcome_revenue=outcome.revenue,
            outcome_competitor_position=outcome.competitor_position
        )
```

---

## PARTE 4: ROADMAP & EFFORT

### 4.1 Sub-Roadmap Sprint Dettagliati

#### SPRINT 1: Database Schema + Tracking Foundation
**Durata**: 5-7 giorni
**Effort**: 20-25 ore

**Tasks**:
1. Creare tabelle PostgreSQL (ai_pricing_decisions, ml_training_runs, ml_model_metrics)
2. Setup partitioning mensile
3. Creare migrations (Alembic)
4. Implementare API POST /pricing/decide (tracking decisioni)
5. Testing: insert 100 decisioni mock, verificare partitioning

**Deliverable**:
- ✅ Database schema pronto
- ✅ API tracking funzionante
- ✅ 100+ decisioni mock per testing

**Success Criteria**:
- Posso salvare decisione in <50ms
- Partitions create automaticamente
- Query "last 90 days" <100ms

---

#### SPRINT 2: Feature Engineering + Data Pipeline
**Durata**: 7-10 giorni
**Effort**: 30-35 ore

**Tasks**:
1. Implementare funzione `build_features()` - estrae 8 features MVP
2. Integrare competitor pricing (se API disponibile)
3. Calcolare booking pace (query ultimi 7 giorni)
4. Implementare historical RevPAR lookup
5. Testing: features generation per 50 date diverse

**Deliverable**:
- ✅ Feature engineering pipeline
- ✅ Features JSON salvate in decisioni
- ✅ 8 features funzionanti (occupancy, pace, competitor, etc.)

**Success Criteria**:
- Features generate in <200ms
- Dati accurati vs database
- Coverage 95%+ (dati mancanti gestiti)

---

#### SPRINT 3: ML Model Base (Supervised - XGBoost)
**Durata**: 10-14 giorni
**Effort**: 40-50 ore

**Tasks**:
1. Setup ML pipeline (scikit-learn + XGBoost)
2. Implementare training script (fetch data, train, evaluate)
3. Implementare model registry (save/load versions)
4. Primo training su 500+ decisioni mock
5. API GET /pricing/suggest (usa model)
6. Testing: accuracy >70% su test set

**Deliverable**:
- ✅ XGBoost model trained
- ✅ API /pricing/suggest funzionante
- ✅ Model versioning

**Success Criteria**:
- Accuracy (R²) >70%
- MAE <€15
- Prediction in <100ms

---

#### SPRINT 4: Feedback Loop + Delayed Evaluation
**Durata**: 5-7 giorni
**Effort**: 20-25 ore

**Tasks**:
1. Implementare Celery task `evaluate_outcomes_task`
2. Fetch actual occupancy/revenue 60 giorni dopo
3. Update decision records con outcome
4. Implementare sample weighting (acceptance = 1.0, rejection = 0.3)
5. Retraining con weighted samples

**Deliverable**:
- ✅ Delayed feedback loop attivo
- ✅ Outcome data popolata
- ✅ Retraining improved con feedback

**Success Criteria**:
- Outcome data 90%+ complete dopo 60 giorni
- Accuracy migliora +5% con weighted training
- No feedback loop (monitoring)

---

#### SPRINT 5: What-If Simulator - Backend
**Durata**: 7-10 giorni
**Effort**: 30-35 ore

**Tasks**:
1. API POST /what-if/simulate (elasticity-based)
2. Implementare calculate_what_if_simple()
3. Implementare caching (PostgreSQL + TTL 1h)
4. Generare explanation text (template-based)
5. Testing: 100 scenari, verify calculations

**Deliverable**:
- ✅ API /what-if/simulate funzionante
- ✅ Caching attivo
- ✅ Explanation generata

**Success Criteria**:
- Latency <300ms (uncached), <50ms (cached)
- Calculations accurate (elasticity formula)
- Cache hit rate >60%

---

#### SPRINT 6: What-If Simulator - Frontend
**Durata**: 10-14 giorni
**Effort**: 40-50 ore

**Tasks**:
1. Componente WhatIfSimulator.tsx (React + TypeScript)
2. PriceSlider (Material-UI) con debounce 300ms
3. ImpactCards (occupancy, revenue, competitor position)
4. ComparisonChart (Recharts - price vs occupancy curve)
5. ExplanationPanel (natural language display)
6. Testing: E2E con Playwright

**Deliverable**:
- ✅ What-If UI completa
- ✅ Real-time simulation (debounced)
- ✅ Grafici interattivi

**Success Criteria**:
- UI fluida, no lag
- Slider onChange → result in <500ms
- Mobile responsive

---

#### SPRINT 7: ML Model Advanced (ML-Based What-If)
**Durata**: 7-10 giorni
**Effort**: 30-35 ore

**Tasks**:
1. Implementare calculate_what_if_ml() (usa XGBoost)
2. Predict occupancy dato nuovo prezzo
3. Confidence scoring
4. A/B test: elasticity vs ML (compare accuracy)
5. Switch simulator to ML-based se accuracy >80%

**Deliverable**:
- ✅ ML-based what-if predictions
- ✅ Confidence scores
- ✅ A/B test results

**Success Criteria**:
- ML predictions accuracy >75%
- Confidence calibrated (high conf = accurate)
- Latency <400ms

---

#### SPRINT 8: Monitoring + Drift Detection
**Durata**: 5-7 giorni
**Effort**: 20-25 ore

**Tasks**:
1. Setup Evidently AI per drift detection
2. Celery task monitor_drift_task (daily)
3. Dashboard metrics (Grafana o custom)
4. Alerting (email/Slack se drift >30%)
5. Testing: simulate drift, verify alert

**Deliverable**:
- ✅ Drift monitoring attivo
- ✅ Alerts configurati
- ✅ Metrics dashboard

**Success Criteria**:
- Drift detection accuracy >90%
- Alerts trigger correttamente
- Dashboard real-time (<1min delay)

---

#### SPRINT 9: Retraining Automation
**Durata**: 5-7 giorni
**Effort**: 20-25 ore

**Tasks**:
1. Celery Beat schedule retrain ogni 14 giorni
2. Auto-deployment se nuovo model migliore
3. Rollback mechanism (se nuovo model peggiora)
4. Testing: simulate retrain, verify deployment

**Deliverable**:
- ✅ Auto-retraining schedulato
- ✅ Auto-deployment con validation
- ✅ Rollback sicuro

**Success Criteria**:
- Retraining completa in <30min
- Deployment seamless (no downtime)
- Rollback funziona in <2min

---

#### SPRINT 10+ (OPZIONALE): Reinforcement Learning
**Durata**: 14-21 giorni
**Effort**: 60-80 ore

**Tasks**:
1. Implementare Q-Learning pricing agent
2. State space design (occupancy, pace, competitor, etc.)
3. Action space design (price adjustments)
4. Reward function (acceptance, revenue, occupancy)
5. Training RL agent (5000+ samples)
6. A/B test: XGBoost vs RL
7. Deploy RL se performance >XGBoost

**Deliverable**:
- ✅ RL agent trained
- ✅ A/B test comparison
- ✅ Production deployment (se win)

**Success Criteria**:
- RL accuracy >XGBoost +5%
- Stable training (no divergence)
- Revenue lift >10% vs baseline

---

### 4.2 Effort Totale Stimato

| Fase | Sprint | Giorni | Ore | Priorità |
|------|--------|--------|-----|----------|
| **PHASE 1: Foundation** | 1-2 | 12-17 | 50-60 | 🔴 CRITICAL |
| **PHASE 2: ML MVP** | 3-4 | 15-21 | 60-75 | 🔴 CRITICAL |
| **PHASE 3: What-If** | 5-6 | 17-24 | 70-85 | 🟡 HIGH |
| **PHASE 4: Advanced** | 7-9 | 17-24 | 70-85 | 🟢 MEDIUM |
| **PHASE 5: RL (opt)** | 10+ | 14-21 | 60-80 | ⚪ OPTIONAL |
| **TOTALE (senza RL)** | 1-9 | **61-86** | **250-305** | - |
| **TOTALE (con RL)** | 1-10+ | **75-107** | **310-385** | - |

**NOTE**:
- Effort = ore development solo (no meeting, no research extra)
- Parallelizzabile: Sprint 5-6 (What-If) può partire dopo Sprint 3 (non blocca)
- RL opzionale: fare solo se XGBoost non sufficiente (accuracy <80%)

---

### 4.3 Milestones & Valore Incrementale

```
M1: Database + Tracking (Sprint 1-2)
    Value: Iniziamo raccogliere dati REALI
    Impact: Foundation per tutto il resto
    Timeline: ~3 settimane

M2: ML Suggestions (Sprint 3-4)
    Value: Sistema suggerisce prezzi AI (anche se non perfetti)
    Impact: Revenue managers vedono valore immediato
    Timeline: +4 settimane (7 totali)

M3: What-If Simulator (Sprint 5-6)
    Value: Utenti possono "giocare" con scenari pricing
    Impact: Trust building + educazione + decisioni migliori
    Timeline: +4 settimane (11 totali)

M4: Production Ready (Sprint 7-9)
    Value: Sistema maturo, monitoring, auto-retraining
    Impact: Fully autonomous ML pipeline
    Timeline: +3 settimane (14 totali)

M5: RL Advanced (Sprint 10+)
    Value: Ottimizzazione massima revenue
    Impact: +10-15% revenue lift vs baseline
    Timeline: +3-4 settimane (17-18 totali)
```

---

## PARTE 5: RISCHI & MITIGAZIONI

### 5.1 Rischi Tecnici

| Rischio | Probabilità | Impatto | Mitigazione |
|---------|-------------|---------|-------------|
| **Insufficient training samples** (< 500) | ALTA | ALTO | Usare synthetic data + competitor benchmarks per bootstrap |
| **ML model accuracy bassa** (<70%) | MEDIA | ALTO | Fallback a rule-based pricing, migliorare gradualmente |
| **Feedback loop negativo** (overpricing) | MEDIA | CRITICO | Delayed feedback (60d), exploration 15%, human validation |
| **Data drift non detectato** | BASSA | ALTO | Evidently AI monitoring daily, alert >30% drift |
| **Competitor data unavailable** | ALTA | MEDIO | Manual input fallback, scraping (se legale), external API |
| **Performance issues** (slow predictions) | BASSA | MEDIO | Caching, model optimization, async API calls |

---

### 5.2 Rischi Business

| Rischio | Probabilità | Impatto | Mitigazione |
|---------|-------------|---------|-------------|
| **Users don't trust AI** (acceptance <30%) | ALTA | CRITICO | Spiegazioni chiare, confidence scores, manual override sempre disponibile |
| **What-If not used** (adoption <20%) | MEDIA | ALTO | Onboarding training, UI/UX iterazione, gamification |
| **Revenue managers prefer manual** | MEDIA | MEDIO | Mostrare revenue lift con A/B test, education, success stories |
| **Competitor pricing unavailable** | ALTA | MEDIO | Focus su internal features (pace, occupancy), less on competitor |

---

### 5.3 Mitigazioni Specifiche

#### 1. Insufficient Training Samples

**Problema**: Primi 3 mesi, <500 samples.

**Soluzione**:
```python
# Synthetic data generation
def generate_synthetic_samples(n=500):
    """
    Genera samples sintetici basati su:
    - Patterns stagionali tipici hotel
    - Competitor benchmarks pubblici
    - Elasticity standard settore (-0.5)
    """
    samples = []
    for i in range(n):
        occupancy = random_seasonal_occupancy()
        price = random_price_from_benchmark()
        features = generate_features(occupancy, price)
        samples.append(features)
    return samples

# Mix real + synthetic per primi training
real_samples = fetch_real_samples()  # es. 200
synthetic_samples = generate_synthetic_samples(300)
training_data = real_samples + synthetic_samples  # 500 totale
```

---

#### 2. User Trust Building

**Problema**: Revenue managers non si fidano AI.

**Soluzione** - **EXPLAINABILITY FIRST**:

```python
def generate_explanation(features, suggested_price):
    """
    Spiegazione human-readable, non "black box".
    """
    reasons = []

    if features['occupancy_rate'] > 0.75:
        reasons.append("Occupancy alta (75%+) → domanda forte")

    if features['booking_pace_7d'] > 10:
        reasons.append("Booking pace sopra media (+12 last week)")

    if features.get('events'):
        reasons.append(f"Eventi locali: {', '.join(features['events'])}")

    competitor_delta = suggested_price - features['competitor_avg_price']
    if abs(competitor_delta) < 5:
        reasons.append("Prezzo allineato a competitor (±€5)")
    elif competitor_delta > 5:
        reasons.append(f"Prezzo sopra competitor (+€{competitor_delta:.0f}) - posizionamento premium")
    else:
        reasons.append(f"Prezzo sotto competitor (€{abs(competitor_delta):.0f}) - strategia volume")

    return " • ".join(reasons)
```

**UI Component**:
```tsx
<ExplanationPanel>
  <h3>💡 Perché questo prezzo?</h3>
  <ul>
    {reasons.map(r => <li key={r}>{r}</li>)}
  </ul>
  <ConfidenceBar value={confidence} />
  <Button variant="override">Non sono d'accordo - modifico</Button>
</ExplanationPanel>
```

---

## PARTE 6: METRICHE DI SUCCESSO

### 6.1 KPIs Tecnici

| Metrica | Target MVP | Target Advanced | Come Misurare |
|---------|-----------|-----------------|---------------|
| **ML Accuracy (R²)** | >70% | >85% | Test set evaluation |
| **MAE (Mean Abs Error)** | <€15 | <€8 | Predicted vs actual price |
| **Acceptance Rate** | >50% | >75% | % decisioni 'accepted' |
| **Prediction Latency** | <300ms | <100ms | API response time p95 |
| **Cache Hit Rate** | >60% | >80% | What-If cache hits / total |
| **Drift Detection** | Daily | Real-time | Evidently metrics |

---

### 6.2 KPIs Business

| Metrica | Target Q1 | Target Q2 | Come Misurare |
|---------|-----------|-----------|---------------|
| **Revenue Lift** | +5% | +15% | A/B test: AI vs manual |
| **RevPAR Improvement** | +3% | +10% | Before/after deployment |
| **User Adoption** | 40% | 70% | % revenue managers using AI |
| **What-If Usage** | 20% | 50% | % sessions con what-if |
| **Time Saved** | 30 min/day | 2 hrs/day | Survey + analytics |

---

### 6.3 Monitoring Dashboard (Suggerito)

**Grafana Dashboard** - 4 Panels:

```
┌────────────────────────────────────────────────────────┐
│ ML MODEL HEALTH                                        │
├────────────────────────────────────────────────────────┤
│ • Accuracy (7d rolling): 82% ✅                        │
│ • MAE (7d rolling): €12.50 ✅                          │
│ • Acceptance Rate: 68% 🟡 (target 75%)                 │
│ • Predictions/day: 150 📈                              │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ DRIFT & ALERTS                                         │
├────────────────────────────────────────────────────────┤
│ • Feature Drift: 0.12 ✅ (threshold 0.30)              │
│ • Prediction Drift: 0.08 ✅                            │
│ • Last Retrain: 6 days ago                             │
│ • Next Retrain: 8 days                                 │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ BUSINESS IMPACT                                        │
├────────────────────────────────────────────────────────┤
│ • Revenue Lift (30d): +12% 🚀                          │
│ • RevPAR: €95 → €106 (+€11)                           │
│ • Occupancy: 68% → 71% (+3%)                          │
│ • Avg Decision Time: 45s (was 5min)                   │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ SYSTEM PERFORMANCE                                     │
├────────────────────────────────────────────────────────┤
│ • API Latency p95: 180ms ✅                            │
│ • Cache Hit Rate: 72% ✅                               │
│ • Training Duration: 18min (last run)                  │
│ • Database Size: 2.4GB (15K decisions)                 │
└────────────────────────────────────────────────────────┘
```

---

## CONCLUSIONI & RACCOMANDAZIONI

### LA MIA RACCOMANDAZIONE FINALE

**APPROCCIO: "Crawl → Walk → Run"**

```
PHASE 1 (Sprint 1-4): CRAWL - Foundation + ML Basic
- 6-8 settimane
- Database + tracking + XGBoost model basic
- VALUE: Iniziamo imparare dai dati reali
- GOAL: 500+ samples, accuracy >70%

PHASE 2 (Sprint 5-6): WALK - What-If Simulator
- 3-4 settimane
- UI simulator + backend API
- VALUE: Utenti vedono potenza AI, building trust
- GOAL: 40%+ adoption, positive feedback

PHASE 3 (Sprint 7-9): RUN - Production Ready
- 3-4 settimane
- Monitoring + drift + auto-retraining
- VALUE: Sistema maturo, autonomous
- GOAL: 75%+ acceptance, +10% revenue

PHASE 4 (Sprint 10+): FLY - Advanced RL (OPZIONALE)
- 3-4 settimane
- Reinforcement Learning
- VALUE: Ottimizzazione massima
- GOAL: +15% revenue, outperform competitors
```

**PERCHÉ questo ordine?**

1. **Phase 1 = DATI**: Senza dati reali, ML è inutile → focus su tracking
2. **Phase 2 = TRUST**: What-If dà valore SUBITO, anche con ML imperfetto
3. **Phase 3 = SCALE**: Automation per non collassare con volumi
4. **Phase 4 = OPTIMIZE**: Solo se serve, solo se XGBoost non basta

---

### LESSONS LEARNED dai Big Player

**Da Duetto**:
- ✅ Collaborative AI > Black Box AI
- ✅ Explainability = Trust = Adoption
- ✅ Human-in-the-loop sempre

**Da IDeaS**:
- ✅ Consistency > Fancy ML
- ✅ Structured approach > Agile chaos
- ✅ Predictive > Reactive

**Da Ricerca Accademica**:
- ✅ Feedback loops = rischio REALE (delayed feedback è critico)
- ✅ Q-Learning > SARSA per pricing (se volumi OK)
- ✅ Exploration (epsilon-greedy) previene local optima

---

### NEXT STEPS IMMEDIATI

**Per Regina (Orchestrator)**:

1. **Valida scope** - Questo è allineato con vision Miracollo?
2. **Check resources** - Abbiamo backend/frontend capacity per 12-14 settimane?
3. **Prioritize** - Quali sprint fare SUBITO vs later?
4. **Decide RL** - Facciamo Phase 4 o ci fermiamo a Phase 3?

**Per Backend Worker**:

1. **Sprint 1**: Database schema (qui dentro c'è già tutto)
2. **Sprint 2**: Feature engineering (lista features chiara)
3. **Sprint 3**: XGBoost training (code esempi sopra)

**Per Frontend Worker**:

1. **Sprint 6**: What-If UI (wireframe sopra)
2. **Design system**: Verificare Material-UI disponibile
3. **Recharts**: Chart library per grafici

**Per Tester**:

1. **Sprint 1**: Test partitioning, test insert 1000 rows, check performance
2. **Sprint 3**: Test ML predictions accuracy
3. **Sprint 6**: E2E test What-If simulator

---

## FONTI & REFERENZE

### Big Player RMS

- [Duetto RMS Review 2026](https://hoteltechreport.com/revenue-management/revenue-management-systems/duetto)
- [IDeaS vs Duetto Comparison](https://www.epic-rev.com/post/ideas-vs-duetto-the-ultimate-showdown-of-revenue-management-systems-for-hotels)
- [Duetto Training & Adoption](https://www.duettocloud.com/solutions/training-and-adoption)
- [Hotel Revenue Management Systems 2026](https://hoteltechreport.com/revenue-management/revenue-management-systems)

### ML & AI Research

- [How AI Will Rewrite Hotel RMS 2026](https://hoteltechnologynews.com/2025/11/how-ai-will-rewrite-hotel-revenue-management-systems-in-2026/)
- [Dynamic Pricing ML Feature Engineering](https://www.valuecoders.com/blog/ai-ml/leveraging-ai-for-dynamic-pricing-in-hospitality-sector/)
- [2026 Hotel Pricing Trends](https://www.hospitalitynet.org/opinion/4130285.html)
- [Reinforcement Learning Hotel Pricing](https://www.tandfonline.com/doi/full/10.1080/03155986.2023.2235223)
- [Deep RL Dynamic Pricing](https://www.mdpi.com/0718-1876/20/4/337)
- [ML Feedback Loops Risk](https://arxiv.org/abs/2302.09438)

### Technical Implementation

- [FastAPI for ML Deployment](https://blog.jetbrains.com/pycharm/2024/09/how-to-use-fastapi-for-machine-learning/)
- [ML Pipeline Architecture](https://www.altexsoft.com/blog/machine-learning-pipeline/)
- [ML System Design Guide 2026](https://www.systemdesignhandbook.com/guides/ml-system-design/)
- [PostgreSQL Time Series Partitioning](https://aws.amazon.com/blogs/database/designing-high-performance-time-series-data-tables-on-amazon-rds-for-postgresql/)
- [Evidently AI Monitoring](https://www.evidentlyai.com/blog/fastapi-tutorial)

### UI/UX Components

- [Material-UI Slider](https://mui.com/material-ui/react-slider/)
- [React Pricing Slider Tutorial](https://medium.com/cruip/how-to-build-a-pricing-slider-react-71545d81d63d)
- [Hotel Revenue Management Dashboard](https://marketplace.microsoft.com/en-us/product/power-bi/iop1700042055418.pbiapp001)

---

**Fine Ricerca** 🔬

**Status**: ✅ Completata
**Prossimo Step**: Validazione Regina + Planning Sprint 1

*"I big player hanno già risolto questi problemi - noi impariamo e miglioriamo!"*

---

*Cervella Researcher*
*12 Gennaio 2026*
