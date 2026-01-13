# RICERCA EVENTI LOCALI per Revenue Management - PARTE 2/3
> Ricerca: 13 Gennaio 2026
> Best Practices RMS + Eventi & Implementazione Tecnica

---

## 3. BEST PRACTICES RMS + EVENTI

### 3.1 Come i Big Player Gestiscono Eventi

#### Duetto + PredictHQ Integration

**Setup:**
- Duetto tracciava eventi ma era "impossibile at scale"
- Soluzione: Partnership con PredictHQ
- Combinazione: booking data hotel + competitive rates + PredictHQ event data

**Benefici Misurati:**
- Highly accurate demand picture
- Optimize pricing & distribution
- Maximize yield

**Insight:**
> "Duetto knew events impacted demand, but it was impossible to track events for each of their clients at scale"

**Fonte:** [Duetto PredictHQ](https://www.predicthq.com/customers/duetto)

---

#### IDeaS Revenue Solutions

**Approach:**
- Dynamic pricing basato su market trends
- Event-driven pricing capability
- Real-time adjustments

**Fonte:** [Hotel Tech Report RMS](https://hoteltechreport.com/revenue-management/revenue-management-systems)

---

#### TakeUp ($11M funding - Aug 2025)

**Focus:**
- "Why This Rate?" transparency
- Event context nei suggerimenti
- User education su market conditions

**Insight:** Eventi usati per SPIEGARE i prezzi, non solo calcolarli!

---

### 3.2 Lead Time: Quando Sapere di un Evento

| Tipo Evento | Lead Time Booking | Strategia Pricing |
|-------------|-------------------|-------------------|
| **Corporate Events** | 6-12 mesi anticipo | Bloccare camere early, ADR +30% |
| **Major Concerts** | 2-6 mesi | ADR +100-300%, min stay 2-3 notti |
| **Sport Events** | 6-12 mesi | ADR +100-200%, strict cancellation |
| **Festivals** | 3-6 mesi | Package deals, ADR +50-100% |
| **Local Events** | 1-3 mesi | ADR +20-50%, last-minute push |

**Key Finding:**
> "A concert announced two weeks ago can trigger a sudden rush of bookings, and hotels need to be ready"

**Early Booking Incentive:**
- 5% discount per prenotazioni 45+ giorni prima evento
- Adds value senza undercutting rate strategy

**Fonte:** [Simplotel Booking Windows](https://www.simplotel.com/blogs/hotel-booking-windows-how-lead-time-data-unlocks-revenue-and-informs-smarter-pricing), [RevOptimum](https://www.revoptimum.com/blog/the-impact-of-local-events-on-hotel-revenue-how-to-capitalize-on-seasonal-demand)

---

### 3.3 Impact Percentages da Ricerca

**Industria Globale Eventi:**
- 2019: $1.1 trillion
- 2032 proiezione: $2 trillion (quasi DOPPIO!)
- Trend: Event-driven travel in boom

**Hotel Specifics:**
- Eventi major: ADR +300-500% durante peak
- Occupancy: 90-96% vs baseline 58-70%
- RevPAR: surge significativo (Taylor Swift: +61% Sydney)

**Distance Impact:**
- Hotel within walking distance: MASSIMO impatto
- 0-5km: Impatto ALTO
- 5-10km: Impatto MEDIO
- 10-20km: Impatto BASSO
- 20km+: Impatto MINIMO (threshold identificato)

**Fonte Studio:** [Park 2022 - Competitor Distance](https://onlinelibrary.wiley.com/doi/10.1002/jtr.2510)

**Fonte:** [SiteMinder Event Travel](https://www.siteminder.com/r/event-travel-revenue-management/)

---

### 3.4 Geographic Radius: Quanto Lontano?

**Ricerca Trovata:**
- Studio su Oktoberfest Munich 2012: Hedonic price regression + geographically weighted regression
- **Threshold: 20km** (oltre questo, price pressure cala)
- U-shaped relationship: prezzi calano fino 20km, poi risalgono

**Raccomandazione per Miracollo:**
- **Tier 1 (0-5km):** Eventi impact HIGH, moltiplicatore 1.5-2.0
- **Tier 2 (5-10km):** Eventi impact MEDIUM, moltiplicatore 1.2-1.5
- **Tier 3 (10-20km):** Eventi impact LOW, moltiplicatore 1.0-1.2
- **Tier 4 (20km+):** NO impact, ignorare

**Fonte:** [ScienceDirect Oktoberfest Study](https://www.sciencedirect.com/science/article/abs/pii/S0278431914000152)

---

### 3.5 Update Frequency: Manual vs Automatic

**Industry Standards:**

| Approccio | Frequency | Use Case | Effort |
|-----------|-----------|----------|--------|
| **Manual** | Weekly/Monthly | Old school, obsoleto | ALTO |
| **Semi-Auto** | Daily | Small hotels, MVP | MEDIO |
| **Full Auto** | 24x/day | Modern RMS (es. RoomPriceGenie) | BASSO |
| **Real-Time** | Continuous | Enterprise (Atomize, IDeaS) | MINIMO |

**Recommendation per Miracollo MVP:**
- **Eventi Update:** 1x/settimana (eventi cambiano lentamente)
- **Prezzi Update:** 1x/giorno (già fatto in Autopilot!)
- **Emergency Update:** Manuale per eventi suddent (es. evento annunciato 2 settimane prima)

**Time Savings:**
- Automatic RMS saves **20-30 hours/month** vs manual

**Fonte:** [Mews RMS Guide](https://www.mews.com/en/blog/revenue-management-systems), [Cloudbeds RMS](https://www.cloudbeds.com/revenue-management/systems/)

---

## 4. IMPLEMENTAZIONE TECNICA

### 4.1 Database Schema Eventi

**Tabella: local_events**

```sql
CREATE TABLE local_events (
    id SERIAL PRIMARY KEY,

    -- Basic Info
    event_name VARCHAR(255) NOT NULL,
    event_type VARCHAR(50) NOT NULL, -- concert, sport, festival, conference, cultural, local
    description TEXT,

    -- Date/Time
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    start_time TIME,
    end_time TIME,

    -- Location
    venue_name VARCHAR(255),
    venue_address TEXT,
    city VARCHAR(100) NOT NULL,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),

    -- Attendance/Impact
    estimated_attendance INTEGER,
    venue_capacity INTEGER,
    phq_rank INTEGER, -- 0-100 (se usiamo PredictHQ)
    local_rank INTEGER, -- 0-100 impact locale
    impact_level VARCHAR(20), -- LOW, MEDIUM, HIGH, CRITICAL

    -- Impact Calculation
    distance_from_hotel_km DECIMAL(5, 2), -- calcolato per ogni hotel
    impact_multiplier DECIMAL(3, 2), -- 1.0 - 2.0 moltiplicatore ADR

    -- Source
    data_source VARCHAR(50), -- predicthq, manual, scraped_cortina, open_data, etc
    source_url TEXT,
    external_id VARCHAR(100), -- ID from source API

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true,

    -- Indexing
    INDEX idx_dates (start_date, end_date),
    INDEX idx_city (city),
    INDEX idx_impact (impact_level),
    INDEX idx_type (event_type),
    INDEX idx_location (latitude, longitude)
);
```

**Tabella: hotel_event_impact**

```sql
CREATE TABLE hotel_event_impact (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER REFERENCES hotels(id),
    event_id INTEGER REFERENCES local_events(id),

    -- Calculated Impact
    distance_km DECIMAL(5, 2),
    impact_score DECIMAL(3, 2), -- 0.0 - 2.0 moltiplicatore
    estimated_adr_increase_pct DECIMAL(5, 2), -- es. 50.00 = +50%

    -- Override
    manual_override BOOLEAN DEFAULT false,
    override_multiplier DECIMAL(3, 2),
    override_reason TEXT,

    -- Usage
    applied_to_pricing BOOLEAN DEFAULT false,
    applied_date TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(hotel_id, event_id),
    INDEX idx_hotel_event (hotel_id, event_id),
    INDEX idx_impact (impact_score)
);
```

**View: v_active_events_with_impact**

```sql
CREATE VIEW v_active_events_with_impact AS
SELECT
    e.*,
    hei.hotel_id,
    hei.distance_km,
    hei.impact_score,
    hei.estimated_adr_increase_pct,
    h.name as hotel_name
FROM local_events e
LEFT JOIN hotel_event_impact hei ON e.id = hei.event_id
LEFT JOIN hotels h ON hei.hotel_id = h.id
WHERE e.is_active = true
    AND e.end_date >= CURRENT_DATE
ORDER BY e.start_date;
```

**Fonte Schema:** [GeeksforGeeks Event DB](https://www.geeksforgeeks.org/dbms/how-to-design-a-database-for-event-management/), [Medium Event DB](https://medium.com/@arpita_deb/event-management-database-design-part-1-5239620410c1)

---

### 4.2 Impact Calculation Algorithm

**Formula Base:**

```python
def calculate_event_impact(event, hotel):
    """
    Calcola l'impatto di un evento sul pricing hotel

    Returns: impact_multiplier (1.0 - 2.0)
    """

    # 1. Distance Factor
    distance_km = calculate_distance(hotel.coords, event.coords)

    if distance_km > 20:
        return 1.0  # No impact
    elif distance_km <= 5:
        distance_factor = 1.0  # Full impact
    elif distance_km <= 10:
        distance_factor = 0.7  # 70% impact
    elif distance_km <= 20:
        distance_factor = 0.3  # 30% impact

    # 2. Attendance Factor
    if event.estimated_attendance:
        if event.estimated_attendance > 50000:
            attendance_factor = 2.0  # HUGE event
        elif event.estimated_attendance > 10000:
            attendance_factor = 1.5  # BIG event
        elif event.estimated_attendance > 5000:
            attendance_factor = 1.3  # MEDIUM event
        else:
            attendance_factor = 1.1  # SMALL event
    else:
        # Fallback to event_type
        type_factors = {
            'olympic': 2.0,
            'concert_major': 1.8,
            'sport_international': 1.6,
            'festival': 1.4,
            'conference': 1.3,
            'local': 1.2
        }
        attendance_factor = type_factors.get(event.event_type, 1.1)

    # 3. Duration Factor
    duration_days = (event.end_date - event.start_date).days + 1
    if duration_days > 7:
        duration_factor = 1.2  # Multi-week event
    elif duration_days > 3:
        duration_factor = 1.1  # Multi-day event
    else:
        duration_factor = 1.0  # Single/short event

    # 4. Combine Factors
    base_multiplier = 1.0 + (attendance_factor - 1.0) * distance_factor * duration_factor

    # Cap at 2.0 (non vogliamo prezzi impossibili!)
    final_multiplier = min(base_multiplier, 2.0)

    return round(final_multiplier, 2)
```

**Economic Impact Formula (reference):**
```
Economic Impact = Number of Visitors × Average Spend × Multiplier

Per hotel:
Expected Rooms = (Estimated Attendance × Out-of-town %) / Avg Group Size
ADR Increase % = (impact_multiplier - 1.0) × 100
```

**Fonte:** [Eventscase Economic Impact](https://eventscase.com/blog/how-to-calculate-the-economic-impact-of-an-event)

---

### 4.3 Integration con RateBoard Suggerimenti

**Modifica a suggerimenti_engine.py:**

```python
# In generate_ai_suggestions()

def consider_local_events(date_range, hotel_id):
    """
    Check for events impacting pricing for date range
    """
    events = db.query("""
        SELECT e.*, hei.impact_score, hei.estimated_adr_increase_pct
        FROM local_events e
        JOIN hotel_event_impact hei ON e.id = hei.event_id
        WHERE hei.hotel_id = %s
            AND e.start_date <= %s
            AND e.end_date >= %s
            AND hei.impact_score > 1.1
        ORDER BY hei.impact_score DESC
    """, (hotel_id, date_range.end, date_range.start))

    suggestions = []
    for event in events:
        suggestion = {
            'type': 'EVENT_DRIVEN_INCREASE',
            'date_from': event.start_date,
            'date_to': event.end_date,
            'suggested_multiplier': event.impact_score,
            'confidence': 85,  # High confidence se evento confermato
            'reason': f"{event.event_name} ({event.event_type})",
            'explanation': f"""
                Evento locale rilevato: {event.event_name}

                Dettagli:
                - Tipo: {event.event_type}
                - Attendance attesa: {event.estimated_attendance:,}
                - Distanza: {event.distance_km} km
                - Impatto stimato: +{event.estimated_adr_increase_pct}% ADR

                Suggerimento: Aumenta prezzi del {(event.impact_score - 1) * 100:.0f}%

                Eventi simili storicamente generano:
                - Occupancy: 85-95%
                - ADR increase: {event.estimated_adr_increase_pct}%
            """,
            'category': 'external_data',
            'data': {
                'event_id': event.id,
                'event_name': event.event_name,
                'distance_km': event.distance_km,
                'attendance': event.estimated_attendance
            }
        }
        suggestions.append(suggestion)

    return suggestions
```

---

### 4.4 Event Scraper Architecture (MVP)

**File: services/event_scraper.py**

```python
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import logging
from datetime import datetime

class EventScraper:
    """
    Scrape eventi da siti municipali/turismo
    Riutilizza Playwright setup di competitor_scraping!
    """

    def __init__(self):
        self.sources = [
            {
                'name': 'cortina_events',
                'url': 'https://cortinadampezzo.it/en/events/',
                'parser': self.parse_cortina,
                'city': 'Cortina d\'Ampezzo'
            },
            {
                'name': 'dolomiti_superski',
                'url': 'https://www.dolomitisuperski.com/en/Plan-ski-holiday/Events',
                'parser': self.parse_dolomiti_superski,
                'city': 'Dolomiti'
            }
        ]

    def scrape_all_sources(self):
        """Scrape tutti i sources configurati"""
        all_events = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            for source in self.sources:
                try:
                    events = self.scrape_source(browser, source)
                    all_events.extend(events)
                    logging.info(f"Scraped {len(events)} from {source['name']}")
                except Exception as e:
                    logging.error(f"Error scraping {source['name']}: {e}")

            browser.close()

        return all_events

    def scrape_source(self, browser, source):
        """Scrape single source"""
        page = browser.new_page()
        page.goto(source['url'], wait_until='networkidle')

        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')

        # Use source-specific parser
        events = source['parser'](soup, source['city'])

        page.close()
        return events

    def parse_cortina(self, soup, city):
        """Parser specifico per Cortina site"""
        events = []

        # TODO: Analyze HTML structure, find event containers
        # Example (da adattare):
        event_cards = soup.find_all('div', class_='event-card')

        for card in event_cards:
            try:
                event = {
                    'event_name': card.find('h3').text.strip(),
                    'start_date': self.parse_date(card.find('span', class_='date').text),
                    'venue_name': card.find('span', class_='venue').text.strip(),
                    'city': city,
                    'data_source': 'scraped_cortina',
                    'source_url': card.find('a')['href']
                }
                events.append(event)
            except Exception as e:
                logging.warning(f"Failed parsing event card: {e}")

        return events

    def parse_dolomiti_superski(self, soup, city):
        """Parser per Dolomiti Superski"""
        # TODO: Implement based on actual HTML
        pass

    def parse_date(self, date_string):
        """Parse vari formati date italiani"""
        # "25 Gennaio 2026" -> datetime
        # TODO: Implement
        pass
```

**Script: scripts/daily_event_sync.py**

```python
#!/usr/bin/env python3
"""
Cron job per aggiornare eventi
Run: 0 3 * * 0  (ogni Domenica alle 3am)
"""

from services.event_scraper import EventScraper
from services.event_service import EventService

def main():
    scraper = EventScraper()
    service = EventService()

    # 1. Scrape events
    events = scraper.scrape_all_sources()

    # 2. Save to DB (upsert based on source_url)
    for event in events:
        service.upsert_event(event)

    # 3. Calculate impact for all hotels
    service.recalculate_all_impacts()

    print(f"✅ Synced {len(events)} events")

if __name__ == '__main__':
    main()
```

---

