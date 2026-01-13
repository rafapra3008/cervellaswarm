# RICERCA EVENTI LOCALI per Revenue Management - PARTE 1/3
> Ricerca: 13 Gennaio 2026
> Cervella Researcher per Miracollo RMS
> Missione: Integrazione Eventi Locali in RateBoard

---

## Executive Summary

**TROVATO:** Opportunità ENORME per differenziazione RMS!

**Key Finding:**
- Eventi locali generano ADR +300-500% durante peak
- Occupancy raggiunge 90-96% vs baseline 58%
- I big player (Duetto) usano PredictHQ ($$ API)
- Esistono fonti GRATUITE alternative per MVP

**Raccomandazione:**
MVP con eventi manuali + scraping gratuito, poi valutare PredictHQ per scale.

---

## 1. TIPI DI EVENTI E IMPATTO

### 1.1 Categorie Eventi per Hotel

| Categoria | Esempi | Impatto Tipico | Lead Time |
|-----------|--------|----------------|-----------|
| **Concerti & Festival** | Taylor Swift, Lollapalooza | +300-500% ADR | 2-6 mesi |
| **Sport** | Olimpiadi, World Cup, Maratone | +100-300% ADR | 6-12 mesi |
| **Fiere & Congressi** | CES, Comic-Con | +50-150% ADR | 6-12 mesi |
| **Eventi Culturali** | Eurovision, Mostre | +100-200% ADR | 3-6 mesi |
| **Eventi Locali** | Sagre, mercatini, feste | +20-50% ADR | 1-3 mesi |

**Fonte:** [BAE Ventures](https://www.baeventures.com/en/insights/the-impact-of-events-on-hospitality-and-hotel-bookings/865/), [Smartness](https://www.smartness.com/en/blog/impact-event-hotel-rates)

### 1.2 Casi Studio REALI con Percentuali

**Taylor Swift Eras Tour (2024):**
- Melbourne/Sydney: Occupancy +81%, ADR +61%
- London/Los Angeles: Occupancy >90% costante
- RevPAR surge durante concerti

**Lollapalooza Chicago:**
- ADR: $321/notte (peak festival nights)
- Occupancy: 81.35% vs 58% normale weekend Luglio
- Aumento: +42% sui prezzi centrali

**Oasis Concerts Cardiff:**
- ADR: $165 (2024) → $807 (2025) = **+388%**
- Demand surge: +125% YoY

**Comic-Con San Diego:**
- Occupancy media: 96%
- Ogni notte >93%

**Eurovision Basel (2025):**
- ADR: $247 (2024) → $512 (2025) = **+107%**

**Fonte:** [Lighthouse](https://www.mylighthouse.com/resources/blog/concerts-impact-on-hospitality-industry), [HospitalityNet](https://www.hospitalitynet.org/news/4126374.html)

### 1.3 Eventi Specifici Montagna (Naturae Lodge Focus)

| Tipo Evento | Esempi | Impatto | Frequenza |
|-------------|--------|---------|-----------|
| **Sci Competizioni** | World Cup Cortina, Gare FIS | ALTO (+100-200%) | Mensile (inverno) |
| **Apertura Impianti** | Opening Day Dolomiti Superski | MEDIO (+30-50%) | Annuale |
| **Wellness Retreats** | Yoga, meditazione | MEDIO (+20-40%) | Mensile |
| **Mercatini Natale** | Mercatini locali, sagre | ALTO (+50-100%) | Dic-Gen |
| **Olimpiadi 2026** | Milano-Cortina | ALTISSIMO (+400%+) | Feb-Mar 2026 |

**Olimpiadi 2026 Cortina:**
- Date: 6-22 Feb 2026 (Olimpiadi), 6-15 Mar 2026 (Paralimpiadi)
- Eventi: Alpine skiing women, bobsleigh, skeleton, luge
- Impatto atteso: Occupancy 100%, ADR +400-500%

**World Cup Sci:**
- Cortina: Women's Downhill/Super-G (Olympia slope, Tofane)
- Val Gardena (Saslong): Men's Downhill/Super-G
- Alta Badia (Gran Risa): Men's Giant Slalom
- Faloria: Snowboard Parallel Giant Slalom

**Fonte:** [Dolomiti Superski](https://www.dolomitisuperski.com/en/Plan-ski-holiday/Events), [Cortina Events](https://cortinadampezzo.it/en/events/)

### 1.4 Eventi Non Ovvi (Hidden Gems)

**Trovati in ricerca:**
- **School Holidays** - Famiglie prenotano alloggi
- **Academic Events** - Università vicine = conferenze
- **Public Holidays & Observances** - Ponti = weekend lunghi
- **Yoga/Wellness Retreats** - Trend crescente montagna
- **Corporate Retreats** - Booking 6-12 mesi anticipo

**Fonte:** [PredictHQ Categories](https://docs.predicthq.com/getting-started/predicthq-data/event-categories/attendance-based-events)

---

## 2. FONTI DATI EVENTI

### 2.1 API Commerciali (A Pagamento)

#### PredictHQ (Leader Mercato) 💰💰💰

**Cosa Offre:**
- 19 categorie eventi
- 200+ data sources aggregati
- PHQ Rank (0-100 impact score)
- Local Rank (impact su popolazione locale)
- Predicted attendance
- Geolocation, venue, date/time
- Predicted event spend

**Utilizzato da:**
- Duetto (RMS leader)
- Amadeus Airlines
- Lighthouse platform

**Risultati Clienti:**
- +10% RevPAR average
- +10% forecast accuracy in 30 giorni

**Pricing:** NON pubblico (contact sales)

**Fonti:** [PredictHQ API](https://www.predicthq.com/apis), [Duetto Case](https://www.predicthq.com/customers/duetto), [PHQ Rank](https://www.predicthq.com/tools/rankings/phq-rank)

**Valutazione:**
✅ PRO: Dati completi, affidabili, usati dai big
❌ CONTRO: Costo probabilmente alto, overkill per MVP

---

#### Ticketmaster Discovery API 💰

**Cosa Offre:**
- API gratuita per eventi ticketed
- Search per location, date range, category
- Event details (venue, date, pricing tiers)
- Coverage: principalmente USA/UK

**Limitazioni:**
- Rate limits su free tier
- Non include tutti eventi locali/gratuiti
- Focus ticketing, non tutto spettro

**Fonti:** [Ticketmaster API](https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/)

**Valutazione:**
✅ PRO: Gratuito, API documentata, concerti/sport coperti
⚠️ CONTRO: Coverage Italia limitata, solo eventi a pagamento

---

#### Eventbrite API 💰

**Cosa Offre:**
- API per eventi Eventbrite platform
- Dettagli evento (date, venue, attendees se owner)
- Create/manage eventi
- Coverage globale

**Limitazioni:**
- Solo eventi su Eventbrite
- Molti eventi locali NON usano Eventbrite
- API rate limits

**Fonti:** [Eventbrite API](https://www.eventbrite.com/platform/api)

**Valutazione:**
✅ PRO: Gratuito, ben documentato
⚠️ CONTRO: Coverage parziale, solo Eventbrite ecosystem

---

#### TicketsData API 💰

**Cosa Offre:**
- Aggregatore: Ticketmaster, StubHub, SeatGeek, VividSeats, Eventbrite
- Normalized data (formato unificato)
- Event pricing real-time

**Pricing:** Non chiaro, probabile pagamento

**Fonti:** [TicketsData](https://ticketsdata.com/)

**Valutazione:**
✅ PRO: Aggregato multi-fonte
❌ CONTRO: Costo, probabile enterprise-only

---

### 2.2 Fonti GRATUITE Open Data

#### Italian Government Open Data ⭐ GRATIS

**Ministero della Cultura:**
- ~25,000 eventi culturali
- Format: XML
- License: Creative Commons BY 3.0
- Coverage: Eventi organizzati da enti pubblici

**Dati.gov.it:**
- Catalogo nazionale open data PA
- Aggregatore dati enti locali/nazionali
- Include: cultura, turismo, sport

**GitHub awesome-italian-public-datasets:**
- Dataset curato: eventi culturali/locali
- Community-maintained
- Formato vario (CSV, JSON, XML)

**Fonti:** [Ministero Cultura](https://cultura.gov.it/open-data-e-linked-data), [Dati.gov.it](https://www.dati.gov.it/), [GitHub Italia](https://github.com/italia/awesome-italian-public-datasets)

**Valutazione:**
✅ PRO: GRATIS, legale, dati ufficiali
⚠️ CONTRO: Coverage parziale (solo PA), aggiornamento irregolare, formato non uniforme

---

#### Municipality Event Calendars ⭐ GRATIS

**Esempi trovati:**
- Cortina d'Ampezzo: [cortinadampezzo.it/en/events/](https://cortinadampezzo.it/en/events/)
- Dolomiti.org: [dolomiti.org/en/cortina/events/](https://www.dolomiti.org/en/cortina/events/)
- Dolomiti Superski: [dolomitisuperski.com/en/Plan-ski-holiday/Events](https://www.dolomitisuperski.com/en/Plan-ski-holiday/Events)

**Caratteristiche:**
- HTML calendar pages
- Scrapable con BeautifulSoup/Selenium
- Update variabile (settimanale?)

**Valutazione:**
✅ PRO: GRATIS, specifici per località, dettagliati
⚠️ CONTRO: Scraping necessario, fragile (se cambiano HTML), manuale per ogni località

---

### 2.3 Scraping Approach (Per MVP)

**Target Sites:**
- Municipality calendars (es. Cortina)
- Tourism board sites (es. Dolomiti.org)
- Venue websites (es. impianti sci)

**Tools (GIÀ DISPONIBILI in Miracollo!):**
- Playwright (abbiamo già client per competitor scraping!)
- Python BeautifulSoup
- Scheduled scraping (cron job)

**Strategia:**
1. Identificare 3-5 siti chiave per località hotel
2. Scraper per ogni sito (parsing HTML)
3. Normalizzare in DB unificato
4. Update 1x/settimana (eventi cambiano lentamente)

**Fonti Scraping Tutorials:** [GitHub booking_scraper](https://github.com/HexNio/booking_scraper), [Medium Booking Scraping](https://medium.com/swlh/scraping-hotel-listings-from-booking-com-with-python-and-beautifulsoup-50fb9c435d9e)

**Valutazione:**
✅ PRO: GRATIS, flessibile, custom per hotel
⚠️ CONTRO: Manutenzione scraper, legality checks, fragile

---

## 2.4 Hybrid Approach (RACCOMANDATO) ⭐⭐⭐

**FASE 1 - MVP (0-3 mesi):**
- Eventi MANUALI inseriti da hoteliers
- Scraping 2-3 siti locali chiave (Cortina, Dolomiti Superski)
- Update settimanale automatico
- Focus: eventi GROSSI con alto impatto

**FASE 2 - Growth (3-12 mesi):**
- Expandi scraping a più fonti
- Integra Open Data italiano (Dati.gov.it)
- API gratuite (Ticketmaster, Eventbrite) per concerti/sport

**FASE 3 - Scale (12+ mesi):**
- Valuta PredictHQ se il ROI è chiaro
- Solo se: molti hotel, dati eventi critici per valore
- Benefit: meno manutenzione, più coverage, più affidabile

---

