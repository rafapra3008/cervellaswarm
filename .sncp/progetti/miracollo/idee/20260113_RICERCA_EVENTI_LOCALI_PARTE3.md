# RICERCA EVENTI LOCALI per Revenue Management - PARTE 3/3
> Ricerca: 13 Gennaio 2026
> Roadmap MVP & Conclusioni

---

## 5. MVP IMPLEMENTATION ROADMAP

### 5.1 MVP Scope (3 mesi)

**Obiettivo:** Dimostrare valore eventi locali con minimo effort

**Feature Set:**

| # | Feature | Effort | Valore | Priorità |
|---|---------|--------|--------|----------|
| 1 | **Eventi Manuali** | BASSO | ALTO | P0 |
| 2 | **Database Schema** | MEDIO | ALTO | P0 |
| 3 | **Impact Calculator** | MEDIO | ALTO | P0 |
| 4 | **Suggerimenti AI + Eventi** | MEDIO | ALTO | P0 |
| 5 | **Scraper Cortina** | MEDIO | MEDIO | P1 |
| 6 | **UI Eventi Calendar** | ALTO | MEDIO | P1 |
| 7 | **Cron Sync** | BASSO | MEDIO | P1 |

---

### 5.2 FASE 0: Preparazione (Week 1)

**Setup Database:**

```sql
-- Migration: 039_local_events.sql

CREATE TABLE local_events (
    id SERIAL PRIMARY KEY,
    event_name VARCHAR(255) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    description TEXT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    venue_name VARCHAR(255),
    city VARCHAR(100) NOT NULL,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    estimated_attendance INTEGER,
    impact_level VARCHAR(20),
    data_source VARCHAR(50),
    source_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

CREATE TABLE hotel_event_impact (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER REFERENCES hotels(id),
    event_id INTEGER REFERENCES local_events(id),
    distance_km DECIMAL(5, 2),
    impact_score DECIMAL(3, 2),
    estimated_adr_increase_pct DECIMAL(5, 2),
    manual_override BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(hotel_id, event_id)
);

CREATE INDEX idx_events_dates ON local_events(start_date, end_date);
CREATE INDEX idx_events_city ON local_events(city);
CREATE INDEX idx_impact_hotel ON hotel_event_impact(hotel_id);
```

**Deliverable:** Migration pronta, testata in sviluppo

---

### 5.3 FASE 1: Eventi Manuali (Week 1-2)

**Backend API:**

```python
# routers/local_events.py

@router.post("/api/events/")
def create_event(event: EventCreate):
    """
    Crea evento manualmente
    Admin/Hotelier può inserire eventi rilevanti
    """
    # Validazione
    # Insert DB
    # Calculate impact per hotels nearby
    # Return event with impact

@router.get("/api/events/")
def list_events(
    hotel_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
):
    """Lista eventi con impatto calcolato"""

@router.put("/api/events/{event_id}/impact-override")
def override_impact(event_id: int, hotel_id: int, multiplier: float):
    """
    Hotelier può fare override dell'impatto
    Se l'AI calcola male, hotelier corregge
    """

@router.delete("/api/events/{event_id}")
def delete_event(event_id: int):
    """Disattiva evento (soft delete)"""
```

**Frontend UI (SEMPLICE):**

```javascript
// events-manager.js

class EventsManager {
    constructor() {
        this.events = [];
    }

    async loadEvents() {
        const response = await fetch('/api/events/');
        this.events = await response.json();
        this.render();
    }

    renderEventCard(event) {
        return `
            <div class="event-card impact-${event.impact_level}">
                <h4>${event.event_name}</h4>
                <div class="event-meta">
                    <span class="date">${formatDate(event.start_date)} - ${formatDate(event.end_date)}</span>
                    <span class="type">${event.event_type}</span>
                </div>
                <div class="impact-info">
                    <span class="distance">${event.distance_km} km</span>
                    <span class="multiplier">+${(event.impact_score - 1) * 100}%</span>
                </div>
                <div class="actions">
                    <button onclick="editEvent(${event.id})">Edit</button>
                    <button onclick="deleteEvent(${event.id})">Delete</button>
                </div>
            </div>
        `;
    }

    async createEvent(eventData) {
        await fetch('/api/events/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(eventData)
        });
        this.loadEvents();
    }
}
```

**HTML Pagina (revenue.html o separata):**

```html
<!-- Tab/Section in revenue.html -->
<div id="events-section" class="section">
    <div class="section-header">
        <h3>Eventi Locali</h3>
        <button class="btn-primary" onclick="openEventModal()">
            + Aggiungi Evento
        </button>
    </div>

    <div class="events-filter">
        <input type="date" id="filter-start" placeholder="Data inizio">
        <input type="date" id="filter-end" placeholder="Data fine">
        <select id="filter-type">
            <option value="">Tutti i tipi</option>
            <option value="concert">Concerti</option>
            <option value="sport">Sport</option>
            <option value="festival">Festival</option>
            <option value="local">Eventi locali</option>
        </select>
    </div>

    <div id="events-list" class="events-grid">
        <!-- Event cards rendered here -->
    </div>
</div>

<!-- Modal per creare/editare evento -->
<div id="event-modal" class="modal">
    <div class="modal-content">
        <h3>Aggiungi Evento Locale</h3>
        <form id="event-form">
            <input type="text" name="event_name" placeholder="Nome evento" required>

            <select name="event_type" required>
                <option value="concert">Concerto</option>
                <option value="sport">Evento sportivo</option>
                <option value="festival">Festival</option>
                <option value="conference">Conferenza</option>
                <option value="local">Evento locale</option>
            </select>

            <input type="date" name="start_date" required>
            <input type="date" name="end_date" required>

            <input type="text" name="venue_name" placeholder="Venue">
            <input type="text" name="city" placeholder="Città" required>

            <input type="number" name="estimated_attendance"
                   placeholder="Partecipanti attesi">

            <textarea name="description" placeholder="Descrizione"></textarea>

            <div class="modal-actions">
                <button type="submit" class="btn-primary">Salva</button>
                <button type="button" onclick="closeEventModal()">Annulla</button>
            </div>
        </form>
    </div>
</div>
```

**Deliverable:**
- API funzionante
- UI per CRUD eventi
- Calcolo impatto automatico
- Eventi visibili in lista

**Test:**
- Inserire evento "Olimpiadi 2026 Cortina"
- Verificare impact_score calcolato
- Verificare suggerimento AI include evento

---

### 5.4 FASE 2: Impact in AI Suggestions (Week 2)

**Modifica suggerimenti_engine.py:**

```python
# services/suggerimenti_engine.py

def generate_ai_suggestions(hotel_id, date_range):
    suggestions = []

    # ... existing suggestions (price_increase, last_rooms, etc)

    # NEW: Eventi locali
    event_suggestions = consider_local_events(hotel_id, date_range)
    suggestions.extend(event_suggestions)

    return suggestions

def consider_local_events(hotel_id, date_range):
    """
    Genera suggerimenti basati su eventi locali
    """
    events = db.query("""
        SELECT
            e.id, e.event_name, e.event_type,
            e.start_date, e.end_date,
            e.estimated_attendance,
            hei.distance_km, hei.impact_score,
            hei.estimated_adr_increase_pct
        FROM local_events e
        JOIN hotel_event_impact hei ON e.id = hei.event_id
        WHERE hei.hotel_id = %s
            AND e.is_active = true
            AND e.start_date <= %s
            AND e.end_date >= %s
            AND hei.impact_score > 1.1
        ORDER BY hei.impact_score DESC
    """, (hotel_id, date_range.end, date_range.start))

    suggestions = []
    for event in events:
        suggestion = {
            'id': f"event_{event.id}",
            'type': 'EVENT_DRIVEN_INCREASE',
            'category': 'external_data',
            'date_from': event.start_date,
            'date_to': event.end_date,
            'suggested_action': 'increase_price',
            'suggested_value': event.impact_score,
            'confidence': 85,  # High confidence
            'reason': f"📅 Evento: {event.event_name}",
            'explanation': f"""
Evento locale rilevato: {event.event_name}

📍 Distanza: {event.distance_km:.1f} km
👥 Partecipanti attesi: {event.estimated_attendance or 'N/A'}
📈 Impatto stimato: +{event.estimated_adr_increase_pct:.0f}% ADR

💡 Suggerimento: Aumenta prezzi del {(event.impact_score - 1) * 100:.0f}%

Eventi simili storicamente generano:
- Occupancy: 85-95%
- Booking lead time: 2-4 mesi
            """.strip(),
            'impact_data': {
                'event_id': event.id,
                'event_name': event.event_name,
                'event_type': event.event_type,
                'distance_km': event.distance_km,
                'attendance': event.estimated_attendance,
                'impact_multiplier': event.impact_score
            }
        }
        suggestions.append(suggestion)

    return suggestions
```

**UI Update (revenue-suggestions.js):**

```javascript
// Aggiungi icona evento nel suggestion card
function renderSuggestionCard(suggestion) {
    const icon = suggestion.type === 'EVENT_DRIVEN_INCREASE'
        ? '📅'  // Calendario per eventi
        : getIconForType(suggestion.type);

    // ... existing card render

    // Se evento, mostra dettagli extra
    if (suggestion.impact_data?.event_name) {
        cardHTML += `
            <div class="event-details">
                <span class="event-badge">${suggestion.impact_data.event_type}</span>
                <span class="event-distance">${suggestion.impact_data.distance_km}km</span>
            </div>
        `;
    }

    return cardHTML;
}
```

**Deliverable:**
- Eventi appaiono in suggerimenti AI
- Icona/badge distingue suggerimenti evento
- Explanation mostra dettagli evento
- Confidence alto (85%)

**Test:**
- Evento "Olimpiadi 2026" inserito
- Genera suggerimenti per Feb 2026
- Verifica suggerimento presente con +400% ADR

---

### 5.5 FASE 3: Event Scraper (Week 3) - OPZIONALE

**Se tempo disponibile, altrimenti POST-MVP**

**Scraper Cortina Events:**

```python
# services/event_scraper_cortina.py

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from datetime import datetime
import logging

class CortinaEventScraper:
    """
    Scraper per cortinadampezzo.it/en/events/
    """

    BASE_URL = "https://cortinadampezzo.it/en/events/"

    def scrape(self):
        """
        Scarica eventi da Cortina website
        Returns: lista eventi
        """
        events = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            try:
                page.goto(self.BASE_URL, wait_until='networkidle')
                html = page.content()
                soup = BeautifulSoup(html, 'html.parser')

                events = self._parse_events(soup)

            except Exception as e:
                logging.error(f"Scraping failed: {e}")
            finally:
                browser.close()

        return events

    def _parse_events(self, soup):
        """
        Parse HTML per estrarre eventi
        NOTA: Questa implementazione è PLACEHOLDER!
        Serve analizzare HTML reale del sito!
        """
        events = []

        # TODO: Analizzare struttura HTML reale
        # Possibili selettori:
        # - .event-item, .event-card, article.event
        # - .calendar-event, .event-listing

        event_containers = soup.find_all('div', class_='event-item')  # DA VERIFICARE!

        for container in event_containers:
            try:
                event = {
                    'event_name': container.find('h3').text.strip(),
                    'start_date': self._parse_date(container.find('time')['datetime']),
                    'venue_name': container.find('span', class_='venue').text.strip(),
                    'city': 'Cortina d\'Ampezzo',
                    'data_source': 'scraped_cortina',
                    'source_url': container.find('a')['href']
                }

                # Optional fields
                desc = container.find('p', class_='description')
                if desc:
                    event['description'] = desc.text.strip()

                events.append(event)

            except Exception as e:
                logging.warning(f"Failed parsing event: {e}")
                continue

        return events

    def _parse_date(self, date_string):
        """
        Parse date formats:
        - ISO: "2026-02-15"
        - IT: "15 Febbraio 2026"
        """
        # TODO: Implement
        pass
```

**Cron Job:**

```python
# scripts/weekly_event_sync.py

#!/usr/bin/env python3
"""
Sync eventi da sources configurati
Cron: 0 3 * * 0  (Domenica 3am)
"""

from services.event_scraper_cortina import CortinaEventScraper
from services.event_service import EventService

def main():
    scraper = CortinaEventScraper()
    service = EventService()

    # Scrape
    events = scraper.scrape()
    logging.info(f"Scraped {len(events)} events from Cortina")

    # Upsert in DB
    for event in events:
        service.upsert_event(event)

    # Recalculate impact
    service.recalculate_all_impacts()

    logging.info("✅ Event sync completed")

if __name__ == '__main__':
    main()
```

**Deliverable:**
- Scraper Cortina funzionante
- Cron job configurato
- Eventi auto-inseriti settimanalmente

**NOTA:** Questo è OPZIONALE per MVP! Manuali bastano per dimostrare valore!

---

### 5.6 FASE 4: UI Events Calendar (Week 3-4) - NICE TO HAVE

**Calendar View per eventi:**

```html
<!-- Eventi in calendar view invece di lista -->
<div id="events-calendar">
    <!-- Integrazione FullCalendar.js o similar -->
</div>
```

**Features:**
- Vista mensile eventi
- Color coding per impact_level
- Click evento → dettagli + impact
- Filtri per tipo evento

**Deliverable:** UI più user-friendly (opzionale MVP)

---

## 6. POST-MVP: FULL IMPLEMENTATION

### 6.1 Fase Growth (Mesi 4-12)

**Expand Data Sources:**

1. **Scraping multi-source:**
   - Dolomiti Superski events
   - Local municipality calendars
   - Tourism board websites
   - 5-10 sources totali

2. **Italian Open Data Integration:**
   - Ministero Cultura XML import
   - Dati.gov.it API (se disponibile)
   - Regional tourism data

3. **Free APIs:**
   - Ticketmaster (concerti/sport)
   - Eventbrite (eventi locali)

4. **User Contributed Events:**
   - Hotel staff possono aggiungere
   - Community-sourced events

**Features:**

- **Event Alerts:** Email/notification quando evento rilevante
- **Historical Analysis:** "Evento X l'anno scorso → +Y% occupancy"
- **Predictive Model:** ML per predire impatto basato su storico
- **Competitor Integration:** "Competitor alzano prezzi per questo evento"

---

### 6.2 Fase Scale (Mesi 12+)

**PredictHQ Evaluation:**

**Quando valutare:**
- 50+ hotels usando Miracollo
- Eventi dimostrano ROI chiaro
- Manutenzione scraper diventa onerosa

**ROI Calculation:**
```
Costo PredictHQ: $X/mese (da quotare)
Beneficio: +10% RevPAR per hotel (loro dato)

Break-even:
Se X hotel × RevPAR increase > Costo API
→ vale la pena

Esempio:
20 hotels × €1000/mese RevPAR × 10% = €2000/mese extra
Se PredictHQ costa <€2000/mese → PROCEED
```

**Features con PredictHQ:**
- 19 categorie eventi (vs nostri 5-6)
- PHQ Rank affidabile
- Predicted attendance preciso
- Local Rank (pop density aware)
- Meno manutenzione, più coverage

---

## 7. ALTERNATIVE APPROACHES

### 7.1 Manual Only (No Scraping)

**PRO:**
- Zero manutenzione scraper
- Zero legal issues
- Hotelier conosce eventi meglio di chiunque

**CONTRO:**
- Richiede disciplina hotelier
- Eventi minori potrebbero essere skippati
- No automation

**Quando usare:** Hotel molto piccoli, low-tech, eventi rari

---

### 7.2 Hybrid (Manual + Selective Scraping)

**PRO:**
- Bilancia automation + human input
- Scraping solo per fonti affidabili/stabili
- Hotelier può override/aggiungere

**CONTRO:**
- Complessità media
- Serve UI per gestione

**Quando usare:** MVP approach, 90% dei casi ✅

---

### 7.3 Full API (PredictHQ from Day 1)

**PRO:**
- Coverage massima
- Affidabilità massima
- Zero manutenzione

**CONTRO:**
- Costo alto
- Overkill per pochi hotel
- Lock-in vendor

**Quando usare:** Scale, molti hotel, ROI dimostrato

---

## 8. RACCOMANDAZIONI FINALI

### 8.1 Per Naturae Lodge (Caso Studio)

**Setup Consigliato:**

1. **Eventi Manuali Priority:**
   - Olimpiadi 2026 (Feb-Mar)
   - World Cup Sci Cortina (stagionale)
   - Mercatini Natale locali (Dic-Gen)
   - Wellness Retreats (mensili)
   - Apertura/chiusura impianti sci

2. **Scraping (opzionale):**
   - Cortina events calendar
   - Dolomiti Superski calendar
   - Update settimanale

3. **Impact Settings:**
   - Olimpiadi: multiplier 2.0 (max!)
   - World Cup: multiplier 1.8
   - Mercatini: multiplier 1.5
   - Wellness retreats: multiplier 1.2

4. **Monitoring:**
   - Track occupancy durante eventi
   - A/B test impact multiplier
   - Refine algoritmo basato su dati reali

**Expected Results:**
- +30-50% RevPAR durante eventi
- Booking window increase (3-6 mesi anticipo)
- Competitive advantage (altri hotel non usano RMS)

---

### 8.2 Implementazione Strategy

**DO:**
✅ Iniziare con eventi MANUALI (veloce, value immediato)
✅ Testare impact algorithm su dati reali
✅ Documentare ROI chiaramente
✅ UI semplice e intuitiva
✅ Integrazione SEAMLESS con suggerimenti esistenti
✅ Permettere override manuale (hotelier è esperto!)

**DON'T:**
❌ Over-engineering (PredictHQ non serve per MVP!)
❌ Scraping fragile (HTML changes = rottura)
❌ Eventi troppo lontani (>20km = no impact)
❌ Impatti irrealistici (2.0 è MAX!)
❌ Nascondere eventi ai competitors (è pubblico!)

---

### 8.3 Success Metrics

**MVP Success Criteria (3 mesi):**

| Metric | Target | Come Misurare |
|--------|--------|---------------|
| Eventi inseriti | 20+ | DB count |
| Eventi con impatto >1.3 | 5+ | High-impact events |
| Suggerimenti generati | 50+ | AI suggestions log |
| Acceptance rate eventi | >60% | User accepts event suggestions |
| RevPAR increase | +10-15% | Durante eventi vs baseline |
| Time saved | 5-10h/mese | Vs manual tracking |

**Scale Success (12+ mesi):**
- 50+ hotels using
- 1000+ eventi trackati
- +10% RevPAR average across fleet
- ROI positivo per PredictHQ (se adottato)

---

## 9. CONCLUSIONI

### 9.1 Key Findings Summary

**Eventi Impattano MASSIVAMENTE:**
- ADR: +300-500% per major events
- Occupancy: 90-96% vs 58% baseline
- Industria in boom: $2T by 2032

**Big Players Usano Già:**
- Duetto + PredictHQ
- IDeaS event-driven pricing
- TakeUp transparency eventi

**Miracollo Può Competere:**
- MVP con eventi manuali + scraping
- Native PMS = vantaggio vs esterni
- Costo zero vs PredictHQ ($$/mese)

---

### 9.2 Raccomandazione FINALE

**PROCEDI con MVP Hybrid:**

1. **Settimana 1-2:** Database + Eventi Manuali + API
2. **Settimana 2:** Integration AI Suggestions
3. **Settimana 3-4:** (Opzionale) Scraper Cortina + UI calendar

**Effort:** 40-60 ore totali
**Value:** ALTO (differenziazione + RevPAR)
**Risk:** BASSO (fallback a manual sempre possibile)

**Post-MVP:**
- Expand scraping sources
- Italian Open Data
- Valuta PredictHQ a 50+ hotels

---

### 9.3 Next Steps

**Per Rafa & Regina:**

1. **Decidere:** Procediamo con MVP eventi?
2. **Priorità:** P0 subito o dopo altri task?
3. **Resource:** Chi implementa? (Backend, Frontend, Full-stack)
4. **Timeline:** 3 settimane realistiche? O diverso?

**Per Worker Assegnato:**

1. Leggere PARTE 1-2-3 di questa ricerca
2. Studiare schema DB proposto
3. Analizzare integrazione con suggerimenti_engine.py esistente
4. Proporre variazioni se necessarie
5. Implementare per fasi (non tutto insieme!)

---

## FONTI COMPLETE

Questa ricerca si basa su 30+ fonti web analizzate:

**Impatto Eventi:**
- [BAE Ventures Impact Study](https://www.baeventures.com/en/insights/the-impact-of-events-on-hospitality-and-hotel-bookings/865/)
- [Smartness Event Impact](https://www.smartness.com/en/blog/impact-event-hotel-rates)
- [HospitalityNet 2025 Events](https://www.hospitalitynet.org/news/4126374.html)
- [Lighthouse Concerts Impact](https://www.mylighthouse.com/resources/blog/concerts-impact-on-hospitality-industry)
- [SiteMinder Event Travel](https://www.siteminder.com/r/event-travel-revenue-management/)

**RMS Best Practices:**
- [Hotel Tech Report RMS](https://hoteltechreport.com/revenue-management/revenue-management-systems)
- [Mews RMS Guide](https://www.mews.com/en/blog/revenue-management-systems)
- [Cloudbeds RMS Systems](https://www.cloudbeds.com/revenue-management/systems/)

**API & Data Sources:**
- [PredictHQ Events API](https://www.predicthq.com/apis)
- [PredictHQ PHQ Rank](https://www.predicthq.com/tools/rankings/phq-rank)
- [Ticketmaster Discovery API](https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/)
- [Eventbrite API](https://www.eventbrite.com/platform/api)
- [Italian Open Data](https://cultura.gov.it/open-data-e-linked-data)
- [Dati.gov.it](https://www.dati.gov.it/)

**Technical Implementation:**
- [GeeksforGeeks Event DB](https://www.geeksforgeeks.org/dbms/how-to-design-a-database-for-event-management/)
- [Medium Event DB Design](https://medium.com/@arpita_deb/event-management-database-design-part-1-5239620410c1)
- [Eventscase Economic Impact](https://eventscase.com/blog/how-to-calculate-the-economic-impact-of-an-event)

**Mountain Events:**
- [Dolomiti Superski Events](https://www.dolomitisuperski.com/en/Plan-ski-holiday/Events)
- [Cortina Events Calendar](https://cortinadampezzo.it/en/events/)
- [Olympics 2026 Info](https://www.dolomites.org/international-winter-sports-event-2026/)

---

*Fine Ricerca - 13 Gennaio 2026*
*Cervella Researcher per Miracollo RMS*

*"Studiare prima di agire - sempre!"*
*"I player grossi hanno già risolto questi problemi - impariamo da loro!"*

