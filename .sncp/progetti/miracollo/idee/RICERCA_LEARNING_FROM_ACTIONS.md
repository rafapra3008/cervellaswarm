# Ricerca: Learning from User Actions - Revenue Management Systems

**Data:** 12 Gennaio 2026
**Ricercatrice:** Cervella Researcher
**Progetto:** Miracollo Revenue Management

---

## Executive Summary

I big player del revenue management (Duetto, IDeaS, Atomize, TakeUp) utilizzano principalmente **Machine Learning predittivo** sui dati di mercato, ma con **limitata integrazione del feedback utente esplicito**. La ricerca rivela un'opportunità strategica: implementare un **sistema di apprendimento dal feedback umano (RLHF)** rappresenta un differenziatore competitivo significativo.

**Raccomandazione chiave:** Miracollo può distinguersi implementando un feedback loop che IMPARA dalle decisioni dell'utente, usando pattern di **Contextual Bandits** per adattamento real-time e **Reinforcement Learning** per miglioramento continuo.

---

## Come Fanno i Big

### Duetto (Leader di mercato 2022-2025)

**Approccio ML:**
- Machine Learning analizza pattern di domanda e identifica anomalie di pacing
- AI fornisce insight su stay dates ad alta opportunità
- Analytics real-time con algoritmi avanzati per forecast accurati
- Dynamic pricing basato su trend di mercato e comportamento consumatore

**Feedback Loop:**
- **NON evidenza** di sistema esplicito per apprendere da override utente
- Focus su automazione e riduzione intervento manuale
- Revenue manager dedica tempo a strategia vs task manuali

**Fonti:** La piattaforma enfatizza configurabilità e UI user-friendly, ma documentazione non menziona tracking delle decisioni utente come input per ML.

### IDeaS G3 RMS

**Approccio ML:**
- AI e ML "hard at work" per ottimizzare analytics core
- Automatizza decisioni di pricing, rate availability, overbooking
- Ingestion di: competitor rates, market occupancy indices, web shopping data
- Modelli ML combinano dati interni hotel + dati mercato forward-looking

**Feedback Loop:**
- Sistema progettato per "eliminare user error"
- Focus su "ottimizzare automazione con giusta interazione utente"
- **Filosofia:** RM risponde a condizioni dinamiche, ma **non evidenza** che ML apprenda da override specifici dell'utente
- Risultati "statisticamente provati" vs metodi manuali

**Gap identificato:** IDeaS enfatizza automazione ROBUSTA ma non personalizzazione basata su preferenze individuali dell'utente.

### Atomize (Acquired by Mews, 2024)

**Approccio ML:**
- Primo RMS a fornire **real-time price optimization**
- Big data + ML per aggiustamenti automatici room rate
- Pricing ottimale in real-time, forecast fino a 2 anni futuri
- 50+ paesi, proprietà 40-1250 camere

**Caratteristica distintiva:**
- "Transforms complex market data into actionable insights"
- Focus su automazione completa e riduzione setup
- **NON evidenza** di sistema feedback esplicito

### TakeUp

**Approccio ML:**
- AI forecasting + "human oversight"
- Combinazione ML + "TakeUp revenue experts"
- Adatto a boutique hotels, B&B, glamping
- **Non richiede dati storici** (interessante!)

**Differenziatore:**
- Unico che menziona esplicitamente "human oversight"
- Possibile indicazione di loop ibrido AI-human
- Target piccole proprietà = maggiore personalizzazione necessaria

---

## Best Practices Feedback Loop

### Pattern 1: Reinforcement Learning from Human Feedback (RLHF)

**Definizione:** Tecnica per allineare agente intelligente con preferenze umane.

**3 Fasi RLHF:**

1. **Creazione Preference Dataset**
   - Raccogliere decisioni utente (accetta/rifiuta suggerimenti)
   - Tracciare contesto di ogni decisione (data, occupancy, competitor rates, etc.)
   - Labeling: suggerimento + outcome + contesto

2. **Training Reward Model**
   - Supervised learning su preference dataset
   - Modello impara a predire "cosa piace all'utente"
   - Rappresenta preferenze come funzione reward

3. **RL Loop Fine-tuning**
   - Usa reward model per affinare base model
   - Loop continuo: suggerisci → feedback → aggiorna → ripeti

**Tools disponibili:**
- Transformers Reinforcement Learning (TRL)
- TRLX (fork di TRL)
- RL4LMs (Reinforcement Learning for Language Models)
- OpenAI codebase (TensorFlow)
- CMU tutorial con Llama-3-8B-it + UltraFeedback dataset

**Applicabilità a Miracollo:**
- Alta! Revenue pricing è sequential decision-making sotto incertezza
- Ogni suggerimento = "action", accettazione/rifiuto = reward signal
- Contesto = occupancy, stagione, competitor rates, historical data

### Pattern 2: Contextual Bandits

**Definizione:** Framework per decision-making sequenziale che impara da interazioni real-time.

**Caratteristiche chiave:**
- **No labeled data upfront** - impara online durante uso
- **Adattamento dinamico** - aggiorna predizioni su changing environment
- **Context-aware** - decisioni basate su situazione specifica

**Applicazioni reali:**
- Netflix: movie recommendation con user viewing history
- E-commerce: product recommendation real-time
- Smart tourism: adaptive user behavior learning

**Differenza vs Supervised Learning:**
- SL: richiede dataset pre-labeled, training offline
- CB: impara da feedback real-time, online learning

**Vantaggio per revenue management:**
- "People's preferences change over time" - CB può adattarsi
- Conversational feedback migliora velocità learning
- Gestisce "dynamic, real-time user contexts"

**Applicabilità a Miracollo:**
- Altissima! Preferenze pricing cambiano con esperienza utente
- Ogni decisione fornisce feedback per migliorare successiva
- Può iniziare senza dati storici (come TakeUp!)

### Pattern 3: Recommendation System Feedback Types

**Explicit Feedback:**
- Rating (1-5 stelle)
- Thumbs up/down
- Accetta/Rifiuta
- Motivazione testuale (optional)

**Implicit Feedback:**
- User-item interactions
- Purchase/browsing history
- Time spent reviewing suggestion
- Override frequency per tipo suggerimento

**Best Practice Hybrid:**
- Raccogli implicit sempre (zero friction)
- Richiedi explicit solo per high-value decisions
- Combina entrambi per training più robusto

**Negative Preferences = Più Importanti:**
- "Unwanted features provoke instant rejection"
- Peso maggiore a "NO" vs "YES" per evitare suggerimenti sgraditi
- High-scoring items ignorati = segnale forte di disallineamento

### Pattern 4: Field Experiment - Reinforcement Learning in Budget Hotels

**Studio:** Journal of Operations Management, 2023

**Approccio:**
1. RL algorithm calcola recommended average discount
2. Linear program converte in capacity allocation
3. Feedback loop aggiorna algoritmo basato su risultati

**Risultati:**
- **+11.80% revenue per available room** (field test reale)
- Approccio validato empiricamente su hotel budget chain

**Tecnica:** Multi-period dynamic pricing via Markov Decision Process

**Applicabilità a Miracollo:**
- Direct validation che RL funziona in contesto hospitality reale
- +11.8% revenue = ROI significativo
- MDP approach applicabile a decisioni pricing sequenziali

---

## Schema Database Suggerito

### Tabella: `pricing_suggestions`

Traccia ogni suggerimento generato dal sistema.

```sql
CREATE TABLE pricing_suggestions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    property_id UUID NOT NULL,
    room_type_id UUID NOT NULL,
    suggestion_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Contesto decisione
    target_date DATE NOT NULL,
    current_occupancy DECIMAL(5,2),
    forecast_occupancy DECIMAL(5,2),
    competitor_avg_rate DECIMAL(10,2),
    days_until_target INTEGER,
    season VARCHAR(50),
    day_of_week VARCHAR(20),

    -- Suggerimento
    suggested_rate DECIMAL(10,2) NOT NULL,
    suggested_discount_pct DECIMAL(5,2),
    current_rate DECIMAL(10,2) NOT NULL,
    confidence_score DECIMAL(5,4), -- 0-1
    reasoning_context JSONB, -- Spiega perché questo suggerimento

    -- Metadati ML
    model_version VARCHAR(50),
    algorithm_used VARCHAR(100),

    FOREIGN KEY (property_id) REFERENCES properties(id),
    FOREIGN KEY (room_type_id) REFERENCES room_types(id)
);

CREATE INDEX idx_suggestions_property_date ON pricing_suggestions(property_id, suggestion_date);
CREATE INDEX idx_suggestions_target ON pricing_suggestions(target_date);
```

### Tabella: `user_feedback`

Traccia ogni azione dell'utente sui suggerimenti.

```sql
CREATE TABLE user_feedback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    suggestion_id UUID NOT NULL,
    user_id UUID NOT NULL,

    -- Feedback
    action VARCHAR(20) NOT NULL, -- 'ACCEPTED', 'REJECTED', 'MODIFIED', 'IGNORED'
    feedback_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Se MODIFIED
    actual_rate_applied DECIMAL(10,2),
    modification_reason TEXT,

    -- Explicit feedback (optional)
    thumbs_rating VARCHAR(10), -- 'UP', 'DOWN', NULL
    comment TEXT,

    -- Implicit feedback
    time_to_decision_seconds INTEGER, -- Tempo impiegato a decidere
    viewed_details BOOLEAN DEFAULT false, -- Ha aperto dettagli suggerimento?

    FOREIGN KEY (suggestion_id) REFERENCES pricing_suggestions(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_feedback_suggestion ON user_feedback(suggestion_id);
CREATE INDEX idx_feedback_user ON user_feedback(user_id);
CREATE INDEX idx_feedback_action ON user_feedback(action);
CREATE INDEX idx_feedback_timestamp ON user_feedback(feedback_timestamp);
```

### Tabella: `user_preferences_learned`

Memorizza pattern appresi dalle decisioni utente.

```sql
CREATE TABLE user_preferences_learned (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    property_id UUID NOT NULL,

    -- Pattern identificato
    pattern_type VARCHAR(100) NOT NULL, -- 'DISCOUNT_THRESHOLD', 'SEASON_PREFERENCE', etc.
    pattern_context JSONB NOT NULL, -- Dettagli pattern

    -- Metriche pattern
    confidence DECIMAL(5,4), -- 0-1, quanto siamo sicuri
    sample_size INTEGER, -- Basato su quante decisioni
    accuracy_rate DECIMAL(5,4), -- Accuracy predittiva del pattern

    -- Lifecycle
    first_observed TIMESTAMPTZ NOT NULL,
    last_updated TIMESTAMPTZ NOT NULL,
    is_active BOOLEAN DEFAULT true,

    UNIQUE(user_id, property_id, pattern_type),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (property_id) REFERENCES properties(id)
);

CREATE INDEX idx_preferences_user ON user_preferences_learned(user_id);
CREATE INDEX idx_preferences_active ON user_preferences_learned(is_active);
```

### Tabella: `model_performance_metrics`

Traccia performance del sistema nel tempo.

```sql
CREATE TABLE model_performance_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    calculation_date DATE NOT NULL,
    property_id UUID,
    user_id UUID,

    -- Metriche aggregazione periodo
    total_suggestions INTEGER,
    accepted_count INTEGER,
    rejected_count INTEGER,
    modified_count INTEGER,
    ignored_count INTEGER,

    -- Metriche calcolate
    acceptance_rate DECIMAL(5,4), -- accepted / total
    override_rate DECIMAL(5,4), -- modified / total
    avg_confidence_accepted DECIMAL(5,4),
    avg_confidence_rejected DECIMAL(5,4),

    -- Revenue impact
    estimated_revenue_with_suggestions DECIMAL(12,2),
    actual_revenue DECIMAL(12,2),
    revenue_improvement_pct DECIMAL(5,2),

    FOREIGN KEY (property_id) REFERENCES properties(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_metrics_date ON model_performance_metrics(calculation_date);
CREATE INDEX idx_metrics_property ON model_performance_metrics(property_id);
```

### Tabella: `activity_tracking` (Scalable User Activity)

Pattern da articolo Medium "Scalable User Activity Tracking with SQL".

```sql
CREATE TABLE user_activity_cumulated (
    user_id UUID NOT NULL,
    property_id UUID NOT NULL,
    activity_date DATE NOT NULL,

    -- Array di date attività
    active_dates DATE[] NOT NULL,

    -- Bit representation per mese (31 bit)
    -- Bit 1 = attivo quel giorno, Bit 0 = non attivo
    active_date_bits BIT(31),

    -- Contatori
    total_suggestions_viewed INTEGER DEFAULT 0,
    total_decisions_made INTEGER DEFAULT 0,
    total_modifications INTEGER DEFAULT 0,

    PRIMARY KEY (user_id, property_id, activity_date)
);

CREATE INDEX idx_activity_date ON user_activity_cumulated(activity_date);
```

---

## UI/UX Raccolta Feedback

### Best Practice: Thumbs Up/Down

**Quando usare:**
- ✅ Feedback ultra-veloce, low-friction
- ✅ Sentiment rapido su suggerimenti
- ✅ Grande user base (genera volume sufficiente)
- ❌ NON usare con piccola community

**Implementazione:**
1. **Semplicità:**
   - Solo 2 opzioni: 👍 👎
   - Character counter per comment opzionale (max 200 char)
   - Evita complicated survey questions

2. **Follow-up intelligente:**
   - Thumbs first (zero friction)
   - Se 👎 → lightweight text prompt: "Perché?" (optional)
   - Pattern: "Thumbs → Why (optional)"

3. **Timing:**
   - Subito dopo applicazione suggerimento
   - Non interrompere workflow decisionale
   - Posizionare in context (vicino al suggerimento applicato)

**Case Study Netflix:**
- Switch da 5-star a thumbs up/down
- **Risultato:** +200% ratings in A/B test
- Motivo: "Widely understood to imply training an algorithm"
- Users capiscono che stanno insegnando al sistema

### Pattern: Binary + Optional Text

**Riferimento:** Double Finance "default/override" pattern

**UI Mockup per Miracollo:**

```
┌─────────────────────────────────────────────────┐
│ Suggerimento Applicato: €120 (-15%)            │
│                                                 │
│ Questo suggerimento ti è stato utile?          │
│                                                 │
│  [👍 Si]  [👎 No]                              │
│                                                 │
│ [Opzionale] Vuoi dirci perché?                 │
│ ┌───────────────────────────────────────────┐  │
│ │ [Text area - max 200 caratteri]           │  │
│ └───────────────────────────────────────────┘  │
│                                                 │
│ [Invia] [Salta]                                │
└─────────────────────────────────────────────────┘
```

**Caratteristiche:**
- **Non invasivo:** Appare DOPO decisione, non prima/durante
- **Skippable:** Sempre opzione "Salta" per non bloccare
- **Context-aware:** Mostra suggerimento a cui si riferisce
- **Progressive disclosure:** Text field appare solo se interessato

### Pattern: Rating Scale (Alternativa)

**Quando usare:**
- Se serve intensità preferenza (non solo SI/NO)
- Per decisioni complesse con sfumature
- Se user base è engagement-oriented

**Trade-off:**
- 5-star: Più info granulare, ma meno engagement
- Thumbs: Meno info, ma +200% participation (Netflix data)

**Raccomandazione per Miracollo:**
- **Fase 1 (MVP):** Thumbs up/down (massimizzare volume feedback)
- **Fase 2:** Aggiungere rating scale opzionale per power users

### Principio: Feedback Without Friction

**Best Practice NN/g (Nielsen Norman Group):**

1. **Timing perfetto:**
   - Non chiedere troppo presto (utente non ha info per giudicare)
   - Non chiedere troppo tardi (utente ha dimenticato)
   - **Sweet spot:** Immediatamente dopo applicazione suggerimento

2. **Contestuale:**
   - Mostra dettagli suggerimento (rate, discount, reasoning)
   - User deve vedere COSA sta valutando

3. **Non ripetitivo:**
   - Non chiedere feedback su OGNI suggerimento
   - Algoritmo intelligente: chiedi feedback strategico
   - Es: dopo primo suggerimento applicato, poi 1 ogni 5

4. **Gamification (opzionale):**
   - "Hai aiutato Miracollo a migliorare 15 volte questo mese!"
   - Progress bar contribution al ML model

### Pattern: Implicit Tracking (Zero Friction)

Oltre a explicit feedback, traccia **sempre** implicit:

```javascript
// Esempio tracking implicit
{
  time_to_decision: 45, // secondi tra visualizzazione e decisione
  viewed_details: true, // Ha aperto "Perché questo suggerimento?"
  hover_time_reasoning: 12, // Secondi hover su reasoning
  compared_with_competitors: true, // Ha controllato competitor rates?
  action: 'MODIFIED', // Outcome
  modification_delta: -5.00 // Ha abbassato di €5 vs suggerimento
}
```

**Vantaggio:** Impari anche da chi NON dà feedback esplicito.

---

## Raccomandazioni per Miracollo

### Fase 1: Foundation (Sprint 1-2)

**Obiettivo:** Iniziare a raccogliere dati per future ML.

1. **Database Schema**
   - ✅ Implementa `pricing_suggestions` table
   - ✅ Implementa `user_feedback` table
   - ✅ Track implicit feedback (time_to_decision, viewed_details)

2. **UI Feedback Minima**
   - 👍 👎 buttons dopo applicazione suggerimento
   - Text field opzionale "Perché?"
   - "Salta" sempre disponibile

3. **Metriche Baseline**
   - Calcola acceptance_rate iniziale
   - Calcola override_rate
   - Identifica quando utente ignora completamente suggerimenti

**Output:** Inizi a costruire preference dataset per future ML.

### Fase 2: Pattern Recognition (Sprint 3-4)

**Obiettivo:** Identificare pattern nelle decisioni utente.

1. **Analisi SQL Pattern**
   - Query ricorrenti per identificare:
     - "Utente accetta sempre sconti > 20%"
     - "Utente rifiuta suggerimenti per weekend"
     - "Utente modifica sempre abbassando di €5"

2. **Populate `user_preferences_learned`**
   - Script automatico che analizza `user_feedback`
   - Identifica pattern con confidence > 0.7
   - Salva in `user_preferences_learned` table

3. **Validazione Pattern**
   - Testa predittività pattern identificati
   - Accuracy rate su hold-out set
   - Rimuovi pattern con accuracy < 60%

**Output:** Sistema conosce preferenze base di ogni utente.

### Fase 3: Adaptive Suggestions (Sprint 5-6)

**Obiettivo:** Usare pattern appresi per personalizzare suggerimenti.

1. **Contextual Bandits Implementation**
   - Python service che genera suggerimenti
   - Input: contesto (occupancy, season, etc.) + user_preferences
   - Output: suggerimento personalizzato + confidence

2. **A/B Testing Framework**
   - 50% utenti: suggerimenti baseline (no personalizzazione)
   - 50% utenti: suggerimenti personalizzati
   - Confronta acceptance_rate tra gruppi

3. **Feedback Loop**
   - Ogni decisione utente aggiorna contextual bandit
   - Real-time adjustment di confidence scores
   - Pattern nuovi aggiunti automaticamente

**Output:** Sistema che IMPARA e migliora continuamente.

### Fase 4: Reinforcement Learning (Sprint 7-8)

**Obiettivo:** Implementare RL completo per ottimizzazione revenue.

1. **MDP Formulation**
   - State: contesto completo (occupancy, competitor rates, season, user_preferences)
   - Action: suggerisci rate specifico
   - Reward: revenue generato + penalty per rifiuto

2. **Training Pipeline**
   - Usa historical `pricing_suggestions` + `user_feedback`
   - Train RL model offline inizialmente
   - Implementa RLHF loop per continuous improvement

3. **Model Performance Tracking**
   - Populate `model_performance_metrics` giornalmente
   - Dashboard per monitorare acceptance_rate, revenue_improvement
   - Alert se performance degrada

**Output:** Sistema full RLHF che ottimizza revenue E soddisfazione utente.

### Fase 5: Explainability & Trust (Sprint 9-10)

**Obiettivo:** Aumentare fiducia utente tramite trasparenza.

1. **Reasoning Display**
   - Per ogni suggerimento, mostra:
     - "Perché questo rate?" → [Occupancy X%, Competitor avg €Y, Stagione Z]
     - Confidence score visuale (es: 95% confidenza)
     - Pattern utilizzato (es: "In passato hai preferito sconti > 15%")

2. **Explainable AI (XAI) Features**
   - Feature importance visualization
   - "Se modifichi X, rate diventa Y"
   - Comparazione con decisioni passate simili

3. **User Control**
   - Toggle: "Suggerimenti conservativi" vs "Suggerimenti aggressivi"
   - Override temporaneo: "Ignora mie preferenze per questa settimana"
   - Transparency: "Mostra dati usati per questo suggerimento"

**Output:** Utente comprende e FIDATI del sistema.

---

## Metriche Success

### KPI Fase 1-2 (Foundation)

| Metrica | Target | Rationale |
|---------|--------|-----------|
| **Feedback Rate** | >30% | % suggerimenti con feedback esplicito |
| **Data Quality** | >95% | % record senza campi NULL critici |
| **Baseline Acceptance Rate** | Misura | Stabilire benchmark pre-ML |

### KPI Fase 3-4 (Adaptive)

| Metrica | Target | Rationale |
|---------|--------|-----------|
| **Acceptance Rate** | +15% | vs baseline Fase 1 |
| **Override Rate** | -20% | Meno modifiche = suggerimenti più accurati |
| **User Satisfaction** | >4/5 | Rating medio suggerimenti |
| **Pattern Confidence** | >0.75 | Media confidence pattern identificati |

### KPI Fase 5 (RL Production)

| Metrica | Target | Rationale |
|---------|--------|-----------|
| **Revenue Improvement** | +10% | Target conservativo (studio citato: +11.8%) |
| **Acceptance Rate** | >80% | Utente accetta maggioranza suggerimenti |
| **Clean Suggestion Rate** | >95% | Suggerimenti senza errori (equivalente clean claim rate) |
| **Trust Score** | >4.5/5 | Survey dedicato su fiducia nel sistema |

### North Star Metric

**Primary:** Revenue per Available Room (RevPAR) improvement
**Secondary:** User time saved + Acceptance rate

**Formula:**
```
Success = (RevPAR_improvement * 0.6) + (Time_saved * 0.2) + (Acceptance_rate * 0.2)
```

---

## Pattern Anti-Pattern

### ✅ DO

1. **Start Small, Learn Fast**
   - Implementa feedback minimo (thumbs) prima di RL complesso
   - 1000 decisioni tracciate > 100 con ML perfetto

2. **Explicit + Implicit**
   - Combina entrambi tipi feedback
   - Implicit = zero friction, sempre disponibile

3. **Transparency First**
   - Spiega SEMPRE perché un suggerimento
   - Users che capiscono = users che fidano

4. **Continuous Monitoring**
   - Dashboard real-time acceptance_rate
   - Alert se degrada performance

5. **User Control**
   - Toggle per disattivare temporaneamente
   - Override sempre possibile

### ❌ DON'T

1. **Non Overwhelming**
   - ❌ Chiedere feedback su OGNI suggerimento
   - ✅ Strategico: 1 ogni 5, o dopo decisioni significative

2. **Non Black Box**
   - ❌ "Il sistema ha deciso €120" (basta)
   - ✅ "€120 perché occupancy 65%, competitor €125, tua preferenza sconto moderato"

3. **Non Ignora Negative Feedback**
   - ❌ Dare più peso a thumbs up
   - ✅ Negative preference = instant avoid future

4. **Non Assume Stationary Preferences**
   - ❌ "Utente preferisce sempre X"
   - ✅ Re-validate pattern periodicamente (preferences change)

5. **Non Over-Automate Troppo Presto**
   - ❌ RL in produzione senza dati sufficienti
   - ✅ 6 mesi raccolta dati → poi RL training

---

## Technology Stack Suggerito

### Database
- **PostgreSQL 14+** con PostgresML extension
- Permette ML in-database (no data movement)
- Support per JSONB (reasoning_context storage)
- Array types per active_dates tracking

### ML Framework

**Fase 1-3 (Pattern Recognition):**
- **Python 3.11+**
- **Pandas** - data manipulation
- **Scikit-learn** - pattern identification, clustering
- **FastAPI** - API per suggestion service

**Fase 4-5 (RL/RLHF):**
- **PyTorch** - RL implementation
- **TRL (Transformers RL)** - se vogliamo RLHF approach
- **Stable-Baselines3** - RL algorithms pronti
- **Ray RLlib** - distributed RL training

### Monitoring
- **Prometheus** - metriche time-series
- **Grafana** - dashboard acceptance_rate, revenue_impact
- **PostgreSQL materialized views** - aggregazioni veloci

### Frontend
- **React** (già in uso)
- **Recharts** - visualization confidence scores
- **Framer Motion** - animazioni feedback UI

---

## Competitive Advantage Analysis

### Dove Miracollo Può Vincere

| Area | Big Players | Miracollo Opportunity |
|------|-------------|----------------------|
| **User Feedback Loop** | ❌ Non evidenza | ✅ RLHF completo, impara da ogni decisione |
| **Transparency** | ⚠️ Black box | ✅ XAI, spiega ogni suggerimento |
| **Personalizzazione** | ⚠️ Generica | ✅ Pattern individuali utente |
| **Small Properties** | ❌ Complesso setup | ✅ Contextual bandits no historical data needed |
| **Trust Building** | ⚠️ Automazione opaca | ✅ User control + reasoning chiaro |

### Positioning Statement

**Duetto/IDeaS:** "Ti diciamo il miglior price basato su big data di mercato"
**Miracollo:** "Impariamo DA TE per suggerirti il price perfetto per il TUO stile"

**Differenziatore:** Non solo dati di mercato, ma **partnership personale utente-AI**.

---

## Next Steps Immediati

### Sprint Planning

**Sprint Prossimo (13-26 Gennaio):**

1. **Database:**
   - [ ] Crea `pricing_suggestions` table
   - [ ] Crea `user_feedback` table
   - [ ] Migration script + seed data test

2. **Backend:**
   - [ ] Endpoint POST `/api/feedback/suggestion/:id`
   - [ ] Endpoint GET `/api/suggestions/:id/context` (per display reasoning)
   - [ ] Implicit tracking service (time_to_decision, etc.)

3. **Frontend:**
   - [ ] Componente `<FeedbackWidget>` (thumbs + optional text)
   - [ ] Integra in existing suggestion flow
   - [ ] A/B test: 50% con widget, 50% senza (misura impact)

4. **Analytics:**
   - [ ] Dashboard Grafana: acceptance_rate real-time
   - [ ] SQL query weekly pattern analysis
   - [ ] Export dataset per future ML training

**Deliverable:** Foundation per iniziare raccolta dati + primi insight pattern.

---

## Rischi e Mitigazioni

| Rischio | Probabilità | Impact | Mitigazione |
|---------|-------------|--------|-------------|
| **Low feedback rate** | Media | Alto | Gamification, incentivi, UI non invasiva |
| **Cold start problem** | Alta | Medio | Contextual bandits (no historical data needed) |
| **Privacy concerns** | Bassa | Alto | Anonimizzazione, transparency su uso dati |
| **ML complexity** | Media | Alto | Phased approach, start simple (pattern SQL) |
| **User distrust AI** | Media | Alto | XAI, reasoning display, user control |

---

## Fonti

### Competitor Analysis
- [Duetto RMS Review 2026](https://hoteltechreport.com/revenue-management/revenue-management-systems/duetto)
- [AI-powered future of revenue management - Duetto](https://www.duettocloud.com/library/the-ai-powered-future-of-revenue-management-duetto)
- [IDeaS G3 Revenue Management System](https://www.capterra.com/p/171036/IDeaS-G3-RMS/)
- [Atomize Reviews 2026](https://hoteltechreport.com/revenue-management/revenue-management-systems/atomize)
- [TakeUp Hotel Revenue Management](https://www.takeup.ai/product)

### Reinforcement Learning & Revenue Management
- [A reinforcement learning approach for hotel revenue management](https://onlinelibrary.wiley.com/doi/abs/10.1002/joom.1246) - Journal of Operations Management, 2023
- [Dynamic pricing of hotel rooms based on reinforcement learning](https://sysengi.cjoe.ac.cn/EN/10.12011/SETP2022-1705)
- [Deep Learning Based Dynamic Pricing Model for Hotel Revenue Management](https://www.researchgate.net/publication/338602035_Deep_Learning_Based_Dynamic_Pricing_Model_for_Hotel_Revenue_Management)

### RLHF Implementation
- [Illustrating Reinforcement Learning from Human Feedback (RLHF)](https://huggingface.co/blog/rlhf)
- [RLHF 101: Technical Tutorial - CMU](https://blog.ml.cmu.edu/2025/06/01/rlhf-101-a-technical-tutorial-on-reinforcement-learning-from-human-feedback/)
- [How to Implement RLHF - Labelbox](https://labelbox.com/guides/how-to-implement-reinforcement-learning-from-human-feedback-rlhf/)

### Recommendation Systems & Feedback
- [Recommender Systems Overview - Dive into Deep Learning](http://d2l.ai/chapter_recommender-systems/recsys-intro.html)
- [AI-based recommendation system types and development](https://www.leewayhertz.com/build-recommendation-system/)
- [Using Context of User Feedback in Recommender Systems](https://arxiv.org/pdf/1612.04978)

### Contextual Bandits
- [Understanding Contextual Bandits](https://medium.com/@kapardhikannekanti/understanding-contextual-bandits-advanced-decision-making-in-machine-learning-85c7c20417d7)
- [Contextual Bandits for adapting to changing User preferences](https://arxiv.org/abs/2009.10073)
- [Contextual Bandits dynamic decision-making - Kameleoon](https://www.kameleoon.com/blog/contextual-bandits)

### Database & Tracking Patterns
- [Default/Override Schema for User Settings](https://double.finance/blog/default_override)
- [Scalable User Activity Tracking with SQL](https://medium.com/@TheGenerativeMind/tracking-user-activity-efficiently-with-postgresql-a-step-by-step-guide-cb111ad82740)
- [PostgreSQL and Machine Learning](https://www.enterprisedb.com/blog/postgresql-and-machine-learning)
- [PostgresML - Machine Learning with SQL](https://www.datacamp.com/tutorial/postgresml-tutorial-machine-learning-with-sql)

### UI/UX Best Practices
- [5 stars vs. thumbs up/down rating systems](https://www.appcues.com/blog/rating-system-ux-star-thumbs)
- [Thumbs Up/Down Surveys - Zonka Feedback](https://www.zonkafeedback.com/blog/collecting-feedback-with-thumbs-up-thumbs-down-survey)
- [User Feedback Requests: 5 Guidelines - Nielsen Norman Group](https://www.nngroup.com/articles/user-feedback/)
- [UX Guidelines for Recommended Content - NN/g](https://www.nngroup.com/articles/recommendation-guidelines/)

### Explainable AI & Trust
- [Trust in Transparency: How Explainable AI Shapes User Perceptions](https://arxiv.org/html/2510.04968v1)
- [Explainable AI in E-Commerce: Enhancing Trust](https://www.semanticscholar.org/paper/Explainable-AI-In-E-Commerce:-Enhancing-Trust-And-Sarkar/9784066a2acf67fcb3aa4eecddfe02415dec8c20)
- [AI Transparency - Salesforce](https://www.salesforce.com/artificial-intelligence/ai-transparency/)
- [How transparency modulates trust in AI](https://pmc.ncbi.nlm.nih.gov/articles/PMC9023880/)

### Metrics & KPIs
- [Revenue Cycle Management KPIs](https://puredi.com/blog/10-revenue-cycle-management-metrics-kpis)
- [Revenue Operations Metrics](https://www.abacum.ai/blog/revenue-operations-metrics)

---

**Conclusione:**

L'implementazione di un sistema di apprendimento dalle azioni utente rappresenta un **differenziatore competitivo strategico** per Miracollo. I big player si concentrano su automazione e dati di mercato, ma **nessuno enfatizza l'apprendimento personalizzato dalle decisioni del singolo utente**.

La roadmap proposta è pragmatica: **inizia con raccolta dati semplice (thumbs + tracking)**, poi evolve verso pattern recognition, contextual bandits, e infine RL completo. Questo approccio permette di **generare valore fin da subito** (insights da pattern analysis) mentre costruisci la foundation per ML avanzato.

**Il campo di battaglia è la fiducia:** utente che capisce PERCHÉ un suggerimento e può VEDERE il sistema imparare dalle sue decisioni = utente che adotta e fida del sistema.

---

*Ricerca completata: 12 Gennaio 2026*
*Prossimo step: Review con Regina + prioritizzazione Sprint*
