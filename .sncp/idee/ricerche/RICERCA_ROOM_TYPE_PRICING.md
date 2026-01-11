# RICERCA: Multi-Room-Type Pricing & Discount Strategies

**Data:** 10 Gennaio 2026
**Researcher:** Cervella Researcher
**Status:** ✅ Completata

---

## 📊 EXECUTIVE SUMMARY

**RISPOSTA DIRETTA:**

I big players del revenue management (IDeaS, Duetto, Booking.com, Expedia) NON applicano lo stesso sconto percentuale a tutti i room type. Usano approcci sofisticati:

1. **IDeaS & Duetto:** Pricing INDIPENDENTE per ogni room type con discount dinamici basati su domanda
2. **Booking.com/Expedia:** Sistema "Derived Rates" con offsets dinamici (% o fissi)
3. **Best Practice Moderna:** "Open Pricing" - ogni room type ha il suo prezzo ottimale, non più BAR+offset fissi

**LA RACCOMANDAZIONE PER NOI:**
Implementare un sistema a **3 livelli di sofisticazione**, partendo da quello più semplice e scalando.

---

## 🏢 COME FANNO I BIG PLAYERS

### IDeaS G3 RMS

**Approccio:** Independent Products Pricing

**Come gestiscono i discount:**
- Il sistema **non usa più offset fissi** tra room type
- Applica "Linked Products" per discount dinamici basati su:
  - Stagionalità
  - Days-to-arrival
  - Day of week
  - **Room type demand individuale**

**Esempio pratico:**
> "Quando la domanda per il base room type è alta, il sistema aumenta quel prezzo ma applica offset RIDOTTI alle camere superiori (es. $30 invece di $50) per evitare di fare free-upgrade e massimizzare la vendita paid delle camere migliori."

**Fonte chiave:** Continuous Pricing feature elimina rate tiers e fixed offsets.

**Link:** [IDeaS Independent Products Pricing](https://ideas.com/independent-products-pricing/)

---

### Duetto Open Pricing

**Approccio:** Yield indipendente per ogni room type in real-time

**Come gestiscono i discount:**
- Ogni room type viene "yieldato" indipendentemente
- I discount sono **flessibili**, non fissi:
  - Compression nights: discount può scendere a 0% invece di chiudere disponibilità
  - Low demand: discount può salire fino a 20%

**Esempio pratico:**
> "Invece di offrire sempre 15% di sconto corporate, offri 'fino a 20% discount'. In bassa stagione dai 20%, in alta stagione riduci a 5% o 0%, ma mantieni il rate aperto."

**Strategia room type:**
> "Business travelers per convention: King room può costare $100-200 in più, non solo $50. Weekend con famiglie: double room (alta domanda) prezzata a premium invece di King."

**Fonte chiave:** AutoPilot + GameChanger per yield unlimited segments e room types.

**Link:** [Duetto Open Pricing](https://www.duettocloud.com/solutions/open-pricing)

---

### Booking.com & Expedia

**Approccio:** Derived Rates (Parent-Child relationship)

**Come funziona:**
1. Definisci un **primary rate** (es. Standard Room a €100)
2. Definisci **derived rates** con offset:
   - Percentage-based: Superior = +20% → €120
   - Fixed amount: Suite = +€50 → €150

**Particolarità:**
- Una volta definito parent-child, i **child NON possono essere gestiti manualmente**
- Aggiornamenti al parent si propagano automaticamente
- Expedia raccomanda "Occupancy Based Pricing" (OBP) per revenue increase medio del 3.5%

**Modello Day-of-Arrival (DOA):**
Gli ospiti pagano il prezzo del giorno di arrivo per tutti i giorni del soggiorno (pricing anchor sul check-in day).

**Link:**
- [Expedia Pricing Models](https://developers.expediagroup.com/supply/lodging/docs/avail_and_rate_apis/avail_rates/learn/)
- [Booking.com Derived Pricing](https://developers.booking.com/connectivity/docs/pricing-models)

---

## 📚 BEST PRACTICES REVENUE MANAGEMENT

### 1. **Traditional BAR Method (VECCHIO APPROCCIO)**

**Come funziona:**
- Best Available Rate (BAR) = prezzo base
- Ogni room type ha offset fisso: Twin +$20, Suite +$50
- Discount si applicano a tutti i room type con la stessa %:
  - Corporate: -15% su tutti
  - OTA package: -20% su tutti

**Problema:**
> "In alta stagione, se aumenti il BAR, tutti i prezzi salgono in lockstep. Questo può rendere le camere superiori troppo care, forzando free-upgrade invece di vendite paid."

**Fonte:** [Open Pricing Strategy - AltexSoft](https://www.altexsoft.com/blog/open-pricing-strategy/)

---

### 2. **Open Pricing (APPROCCIO MODERNO)**

**Principi:**
- Ogni room type ha pricing **indipendente** basato sulla sua domanda
- Discount sono **dinamici**, non fissi
- Non più "BAR + offset", ma "optimal price per room type per day"

**Vantaggi:**
- Revenue increase: studi mostrano 3-7% di incremento
- Flexibility: mantieni inventory aperto riducendo discount invece di chiudere
- Segmentation: prezzi differenti per canale/segmento basati su elasticità

**Come si applica un discount:**
- LOW demand → discount maggiore (es. 20% off)
- HIGH demand → discount minore (es. 5% off o 0%)
- Ogni room type può avere discount % diversi in base alla sua domanda specifica

**Fonte:** [Hotel Pricing Strategies 2026 - Oaky](https://oaky.com/en/blog/hotel-pricing-strategies)

---

### 3. **Rate Parity & Room Type Differential**

**Definizione Rate Parity:**
Stesso room type deve avere stesso prezzo su tutti i canali pubblici (OTA, sito hotel, GDS).

**IMPORTANTE:**
> "Se hai Standard come base room su Booking.com e Deluxe come base room su Expedia, avrai SEMPRE disparity."

**Best Practice:**
- Mantieni stesso room type mapping su tutti i canali
- Monitor con rate shopping tools
- Add value invece di abbassare prezzo (free parking, breakfast, Wi-Fi)
- Usa loyalty programs per bypass rate restrictions

**Fonti:**
- [Rate Parity Best Practices - Little Hotelier](https://www.littlehotelier.com/blog/get-more-bookings/rate-parity-best-practice-small-hotels/)
- [Rate Parity Issues - Lighthouse](https://www.mylighthouse.com/resources/blog/hotel-rate-parity-issues)

---

## 🎯 RACCOMANDAZIONE PER CERVELLA AI

### Strategia: 3 Livelli di Sofisticazione

Implementare progressivamente, partendo da Level 1:

---

#### **LEVEL 1: Derived Rates con Offset Configurabili** (MVP)

**Cosa implementare:**

```
Standard Room (Base)
├── Superior: +20% o +€30 (configurabile dall'utente)
├── Deluxe: +35% o +€60
└── Suite: +50% o +€100

Quando utente applica "Sconto 15%":
├── Standard: €100 → €85 (-15%)
├── Superior: €120 → €102 (-15%)
├── Deluxe: €135 → €114.75 (-15%)
└── Suite: €150 → €127.50 (-15%)
```

**Pro:**
- Semplice da implementare
- Facile da capire per gli utenti
- Mantiene rapporto prezzo tra room types
- Conforme a modello Booking.com/Expedia

**Contro:**
- Non ottimale in scenari complessi (domanda room type diversa)

**UI:**
```
[Applica Sconto]
┌─────────────────────────────────┐
│ Sconto: [15%] [v]               │
│                                 │
│ Applica a:                      │
│ ☑ Tutti i room type             │
│                                 │
│ Preview:                        │
│ • Standard: €100 → €85          │
│ • Superior: €120 → €102         │
│ • Deluxe: €135 → €114.75        │
│ • Suite: €150 → €127.50         │
│                                 │
│ [Applica] [Annulla]             │
└─────────────────────────────────┘
```

---

#### **LEVEL 2: Selective Room Type Discount** (V2)

**Cosa aggiungere:**

```
Quando utente applica "Sconto 15%":

Opzione A: [Tutti i room type] (default Level 1)

Opzione B: [Seleziona room types]
┌────────────────────────────────┐
│ ☑ Standard     €100 → €85      │
│ ☑ Superior     €120 → €102     │
│ ☐ Deluxe       €135 (no sconto)│
│ ☐ Suite        €150 (no sconto)│
└────────────────────────────────┘

Opzione C: [Sconto differenziato]
┌────────────────────────────────┐
│ Standard:  [15%] v  → €85      │
│ Superior:  [15%] v  → €102     │
│ Deluxe:    [10%] v  → €121.50  │
│ Suite:     [5%]  v  → €142.50  │
└────────────────────────────────┘
```

**Pro:**
- Flessibilità per revenue manager esperti
- Può gestire scenari di domanda asimmetrica
- Utile per promozioni targeted (es. "sconto solo su Standard/Superior")

**Quando usare:**
- Promotion specifiche per inventory excess su certe categorie
- Strategia di upselling (sconto solo su low-end rooms)

---

#### **LEVEL 3: AI-Driven Dynamic Discount** (Futuro - AI)

**Cosa implementare:**

Sistema intelligente che suggerisce discount ottimali per room type basandosi su:

```
Input:
├── Occupancy forecast per room type
├── Historical booking curve per room type
├── Competitor pricing per room type
├── Demand elasticity per room type
└── Days-to-arrival

Output:
┌────────────────────────────────────────┐
│ 🤖 AI Recommendation                   │
│                                        │
│ Target: +5% Revenue                    │
│                                        │
│ Discount suggeriti:                    │
│ • Standard: 18% (bassa domanda)        │
│ • Superior: 12% (domanda media)        │
│ • Deluxe: 5% (alta domanda)            │
│ • Suite: 0% (keep price - scarsità)    │
│                                        │
│ Estimated impact: +€450 RevPAR        │
│                                        │
│ [Accetta] [Modifica] [Rifiuta]        │
└────────────────────────────────────────┘
```

**Pro:**
- Massima ottimizzazione revenue
- Adatta automaticamente discount a domanda
- Compete con IDeaS/Duetto

**Contro:**
- Complessità implementativa alta
- Richiede training dati storici
- Può confondere utenti non esperti (serve trust nel sistema)

---

## 🛠️ IMPLEMENTAZIONE SUGGERITA

### Database Schema

```sql
-- Room Type Configuration
room_types:
  id, hotel_id, name, base_price, sort_order

-- Room Type Offset Configuration (Level 1)
room_type_offsets:
  id, base_room_type_id, derived_room_type_id
  offset_type ENUM('percentage', 'fixed_amount')
  offset_value DECIMAL

-- Discount Campaigns
discount_campaigns:
  id, hotel_id, name, start_date, end_date
  discount_type ENUM('uniform', 'selective', 'ai_optimized')

-- Discount Rules per Room Type (Level 2)
discount_rules:
  id, campaign_id, room_type_id
  discount_percentage DECIMAL
  apply_discount BOOLEAN

-- Price Override (sempre possibile)
price_overrides:
  id, hotel_id, room_type_id, date
  price DECIMAL
  reason TEXT
```

---

### API Design

```python
# Level 1: Apply uniform discount
POST /api/pricing/apply-discount
{
  "hotel_id": 123,
  "start_date": "2026-02-01",
  "end_date": "2026-02-14",
  "discount_percentage": 15,
  "apply_to_all_room_types": true
}

# Level 2: Selective discount
POST /api/pricing/apply-discount
{
  "hotel_id": 123,
  "start_date": "2026-02-01",
  "end_date": "2026-02-14",
  "room_type_discounts": [
    {"room_type_id": 1, "discount_percentage": 15},
    {"room_type_id": 2, "discount_percentage": 15},
    {"room_type_id": 3, "discount_percentage": 10},
    {"room_type_id": 4, "discount_percentage": 0}
  ]
}

# Level 3: AI suggestions
GET /api/pricing/ai-suggestions
{
  "hotel_id": 123,
  "target_date_range": "2026-02-01/2026-02-14",
  "optimization_goal": "maximize_revenue" // or "maximize_occupancy"
}

Response:
{
  "suggestions": [
    {
      "room_type_id": 1,
      "current_price": 100,
      "suggested_discount": 18,
      "final_price": 82,
      "reasoning": "Low demand forecast, high inventory",
      "estimated_bookings_increase": 5
    },
    // ...
  ],
  "estimated_revenue_impact": 450,
  "confidence_score": 0.87
}
```

---

### UI/UX Flow

**Step 1: Choose discount mode**
```
┌────────────────────────────────────┐
│ Applica Sconto/Promozione          │
│                                    │
│ Modalità:                          │
│ ○ Uniforme (stesso % tutti)        │
│ ○ Selettivo (scegli room types)    │
│ ○ AI-Ottimizzato (raccomandato)    │
│                                    │
│ [Continua]                         │
└────────────────────────────────────┘
```

**Step 2A: Uniform mode (Level 1)**
```
┌────────────────────────────────────┐
│ Sconto Uniforme                    │
│                                    │
│ Periodo: [01/02/26] - [14/02/26]   │
│ Sconto: [15]%                      │
│                                    │
│ Preview impatto:                   │
│ ┌────────────────────────────┐    │
│ │ Room Type   Ora    →  Nuovo│    │
│ │ Standard    €100   →  €85  │    │
│ │ Superior    €120   →  €102 │    │
│ │ Deluxe      €135   →  €115 │    │
│ │ Suite       €150   →  €128 │    │
│ └────────────────────────────┘    │
│                                    │
│ ⚠️ Mantiene rapporto prezzi        │
│                                    │
│ [Applica] [Annulla]                │
└────────────────────────────────────┘
```

**Step 2B: Selective mode (Level 2)**
```
┌────────────────────────────────────┐
│ Sconto Selettivo                   │
│                                    │
│ Periodo: [01/02/26] - [14/02/26]   │
│                                    │
│ ☑ Standard   [15]%  → €85         │
│ ☑ Superior   [15]%  → €102        │
│ ☐ Deluxe     [10]%  → €135 (orig) │
│ ☐ Suite      [0]%   → €150 (orig) │
│                                    │
│ 💡 Tip: Usa per promozioni         │
│    targeted su categorie specifiche│
│                                    │
│ [Applica] [Annulla]                │
└────────────────────────────────────┘
```

**Step 2C: AI mode (Level 3)**
```
┌────────────────────────────────────┐
│ 🤖 Ottimizzazione AI               │
│                                    │
│ Obiettivo: [Massimizza Revenue] v  │
│ Periodo: [01/02/26] - [14/02/26]   │
│                                    │
│ Analisi completata:                │
│ ✅ Forecast domanda                │
│ ✅ Competitor pricing              │
│ ✅ Historical patterns             │
│                                    │
│ Raccomandazione:                   │
│ • Standard: 18% (bassa domanda)    │
│ • Superior: 12% (media domanda)    │
│ • Deluxe: 5% (alta domanda)        │
│ • Suite: 0% (mantieni prezzo)      │
│                                    │
│ 📊 Impatto stimato: +€450 RevPAR   │
│ 🎯 Confidence: 87%                 │
│                                    │
│ [Accetta] [Modifica] [Rifiuta]     │
└────────────────────────────────────┘
```

---

## 📋 DECISIONI DA PRENDERE

| Decisione | Opzioni | Raccomandazione |
|-----------|---------|-----------------|
| **MVP Approach** | Level 1, 2, o 3? | **Level 1** (uniforme) per MVP, poi Level 2 |
| **Offset Type** | % o Fixed amount? | **Entrambi** (configurabile dall'utente) |
| **Default Behavior** | Tutti o Nessuno? | **Tutti** (più user-friendly per primo utilizzo) |
| **Override Manuale** | Sempre possibile? | **SI** (revenue manager deve sempre avere controllo finale) |
| **Rate Parity Check** | Implement warning? | **SI** (alert se crei disparity tra canali) |

---

## 🔗 FONTI PRINCIPALI

### Revenue Management Systems
- [IDeaS Independent Products Pricing](https://ideas.com/independent-products-pricing/)
- [IDeaS Modern Hotel Pricing](https://ideas.com/modern-hotel-pricing/)
- [Duetto Open Pricing](https://www.duettocloud.com/solutions/open-pricing)
- [Duetto RMS Review 2026](https://hoteltechreport.com/revenue-management/revenue-management-systems/duetto)

### OTA Platforms
- [Expedia Pricing Models](https://developers.expediagroup.com/supply/lodging/docs/avail_and_rate_apis/avail_rates/learn/)
- [Booking.com Pricing Implementation](https://developers.booking.com/connectivity/docs/pricing-models)
- [Expedia Direct Connect Guide](https://phgcdn.com/pdfs/uploads/Direct_Connect_Expedia_Rate_Loading_and_Operations.pdf)

### Best Practices & Strategy
- [Open Pricing Strategy - AltexSoft](https://www.altexsoft.com/blog/open-pricing-strategy/)
- [Hotel Pricing Matrix - Xotels](https://www.xotels.com/en/revenue-management/revenue-management-book/hotel-pricing-matrix)
- [Room Types as Strategic Yield Tool](https://www.xotels.com/en/revenue-management/hotel-pricing-strategies-using-room-types-as-a-rate-yield-tool)
- [Hotel Pricing Strategies 2026 - Oaky](https://oaky.com/en/blog/hotel-pricing-strategies)

### Rate Parity
- [Rate Parity Best Practices - Little Hotelier](https://www.littlehotelier.com/blog/get-more-bookings/rate-parity-best-practice-small-hotels/)
- [Hotel Rate Parity Issues - Lighthouse](https://www.mylighthouse.com/resources/blog/hotel-rate-parity-issues)
- [Rate Parity Guide - Cloudbeds](https://www.cloudbeds.com/articles/rate-parity/)

### Technology
- [RateGain Revenue Management](https://rategain.com/hotels/)
- [10 Best RMS Systems 2026](https://hoteltechreport.com/revenue-management/revenue-management-systems)

---

## 🎯 PROSSIMI STEP

1. **Validare approccio con Rafa** - Conferma Level 1 per MVP
2. **Design database schema** - Implementare room_type_offsets table
3. **Mockup UI** - Creare wireframe per discount application flow
4. **Implementare Level 1** - Uniform discount con offset configurabili
5. **Testing con casi reali** - Scenario Standard+Superior+Deluxe+Suite
6. **Roadmap Level 2** - Quando users chiedono più flessibilità

---

**Conclusione:**

La risposta alla domanda iniziale è chiara: i big players NON applicano lo stesso sconto a tutti i room types, ma usano pricing dinamico e indipendente per ogni categoria.

Per noi, la strategia vincente è:
- **MVP:** Implementare Level 1 (uniforme) con offset configurabili
- **Next:** Aggiungere Level 2 (selettivo) quando richiesto
- **Future:** Level 3 AI-driven quando avremo dati storici sufficienti

Questo ci permette di partire semplici (time-to-market veloce) mantenendo una roadmap chiara verso sophistication.

---

*Ricerca completata da Cervella Researcher*
*10 Gennaio 2026*
