# RICERCA: Competitor Price Scraping - PARTE 2
> **Data:** 13 Gennaio 2026
> **Ricercatrice:** Cervella Researcher
> **Progetto:** Miracollo RateBoard

*Continua da PARTE 1*

---

## PARTE 2: SERVIZI THIRD-PARTY E APPROCCI TECNICI

### 2.1 Servizi Rate Shopping Professionali

Questi sono servizi specializzati per hotel, usati da RMS esistenti.

#### OPZIONE 1: OTAInsight (Lighthouse)

**RANKING:** #1 tra rate shopping vendors nel 2026

**COSA FA:**
- Competition checks automatici
- Inbound flight data
- Eventi locali
- Visual data representation con UI facile

**PRICING:**
- Customizzato in base a:
  - Numero di competitor da tracciare
  - Frequenza (daily, weekly, monthly)
  - Numero di canali (Booking, Expedia, etc)
- **Stima:** $500-1500/mese per independent hotel
- Starter package: handful of comp hotels, several channels, unlimited live Expedia re-shops

**PRO:**
- Best-in-class UI
- Real-time data
- Compliance garantita
- Supporto professionale

**CONTRO:**
- Costo elevato per small hotel
- Overkill per MVP
- Dati aggregati (non raw)
- Dipendenza da vendor

**QUANDO USARE:**
- Quando Miracollo ha traction e budget
- Per hotel enterprise/multi-property
- Se vogliamo vendere come "powered by OTAInsight"

---

#### OPZIONE 2: RateGain Navigator

**RANKING:** #3 tra rate shopping vendors nel 2026

**COSA FA:**
- Real-time rate intelligence
- 500+ sources (OTA, GDS, metasearch)
- 10+ billion rates/month (Marriott usa questo!)
- Advanced analytics

**PRICING:**
- Customizzato (simile a OTAInsight)
- **Stima:** $500-1200/mese

**PRO:**
- Broad market coverage
- Enterprise-grade reliability
- API disponibile
- Demand forecasting incluso

**CONTRO:**
- Costo elevato
- Setup complesso
- Designed per grandi catene

**QUANDO USARE:**
- Se Miracollo punta a enterprise segment
- Se serve forecasting avanzato

---

#### OPZIONE 3: Triptease

**RANKING:** #5 in rate parity (2026)

**COSA FA:**
- Rate parity monitoring
- Direct booking optimization
- Price comparison transparency

**PRICING:**
- Customizzato
- **Stima:** $400-1000/mese

**PRO:**
- Focus su independent hotels
- Direct booking optimization (aligned con mission Miracollo!)
- User-friendly

**CONTRO:**
- Meno comprehensive di OTAInsight
- Focus primario su parity, non competitor analysis

**QUANDO USARE:**
- Se vogliamo anche rate parity feature
- Se target è independent hotels (SMB)

---

### 2.2 Servizi Scraping Generici

Questi sono servizi di web scraping che possiamo usare per costruire soluzione custom.

#### OPZIONE 4: ScrapingBee

**COSA FA:**
- API per scraping con anti-bot bypass
- 40M+ rotating proxies
- Headless browser support
- CAPTCHA solving

**PRICING (2026):**
```
Free:      1,000 credits
Freelance: $49/mese
Business:  $599+/mese

COSTO PER REQUEST:
- Simple targets: $0.10-$0.20 per 1K requests
- Protected sites: $2.50-$2.90 per 1K requests

Booking.com = protected site (alto costo)
```

**ESEMPIO CALCOLO:**
```
1 hotel con 5 competitor
Daily scraping = 5 requests/day
Mese = 150 requests
A $2.50/1K = $0.37/mese

20 hotel = $7.50/mese (MOLTO affordable!)
```

**PRO:**
- Pay-as-you-go
- Success rate 90%+ su Booking.com
- API semplice
- Documentazione ottima

**CONTRO:**
- Dobbiamo costruire parser (estrarre dati da HTML)
- Dobbiamo gestire storage
- Dobbiamo gestire data quality
- Rate limit da gestire

**QUANDO USARE:**
- MVP / PoC
- Budget limitato
- Vogliamo controllo completo
- Team tecnico forte

---

#### OPZIONE 5: Bright Data

**COSA FA:**
- Largest proxy network
- Scraping API
- Ready-made datasets

**PRICING (2026):**
```
Subscription: da $499/mese
Pay-as-you-go: da $1 per 1,000 results

Free trial con matched deposit fino a $500
```

**PRO:**
- Enterprise-grade
- Most reliable proxies
- Legal compliance team
- Vincitore caso Meta (legalmente testato!)

**CONTRO:**
- Più costoso di ScrapingBee
- Overkill per small scale
- Billing può essere unpredictable

**QUANDO USARE:**
- Scale up (100+ hotel)
- Need massima reliability
- Budget disponibile

---

### 2.3 Approcci Tecnici (DIY Scraping)

Se decidessimo di fare scraping proprietario, ecco le opzioni.

#### APPROCCIO A: Headless Browser (Playwright/Puppeteer)

**COME FUNZIONA:**
```
1. Browser automatico visita Booking.com
2. Simula utente umano
3. Estrae prezzi da pagina
4. Salva in database
```

**TECNOLOGIE:**
- Playwright (recommended 2026)
- Puppeteer Stealth
- Proxy rotation
- CAPTCHA solving service

**SFIDE (2026):**
- **Anti-bot detection MOLTO avanzata**
  - Navigator.webdriver detection
  - CDP (Chrome DevTools Protocol) leak detection
  - Mouse movement tracking
  - Fingerprinting avanzato
- **Headless unification (Nov 2022)**: Google ha unificato headless e headful Chrome, rendendo MENO efficaci vecchie tecniche
- **Pixelscan può identificare** Playwright e Puppeteer anche con stealth

**EVASION TECHNIQUES:**
```python
# Esempio concettuale
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,  # Full browser più difficile da detectare
        args=[
            '--disable-blink-features=AutomationControlled',
            '--disable-dev-shm-usage'
        ]
    )
    # Simula human behavior
    page.mouse.move(random.randint(100, 500), random.randint(100, 500))
    await page.wait_for_timeout(random.randint(1000, 3000))
```

**COSTI (self-hosted):**
- Server: $20-50/mese (DigitalOcean/AWS)
- Proxy rotation: $50-200/mese
- CAPTCHA solving: $1-5 per 1000 solve
- Dev time: 40-80 ore (implementazione + maintenance)

**PRO:**
- Controllo totale
- No dipendenze vendor
- Dati raw completi

**CONTRO:**
- **Highest risk legale**
- Manutenzione continua (Booking.com cambia anti-bot)
- Failure rate alto (20-40% con advanced anti-bot)
- Dev time significativo

---

#### APPROCCIO B: HTTP Requests + BeautifulSoup

**COME FUNZIONA:**
```python
import httpx
from parsel import Selector

response = httpx.get(booking_url, headers=headers)
selector = Selector(response.text)
price = selector.css('.price::text').get()
```

**PRO:**
- Più veloce di browser
- Meno risorse
- Più requests/secondo

**CONTRO:**
- **NON FUNZIONA su Booking.com moderno**
  - Booking usa React/Dynamic content
  - Prezzi caricati via JavaScript (GraphQL API)
  - Serve browser per vedere contenuto
- Anti-bot blocca rapidamente

**VERDICT:** NON PRATICABILE per Booking.com nel 2026

---

#### APPROCCIO C: Intercettare GraphQL API

**COME FUNZIONA (scoperto da ricerca):**
```
1. Booking.com usa GraphQL per caricare dati
2. Browser DevTools → Network → trova chiamate GraphQL
3. Replicare quelle chiamate in Python
4. Parsing JSON (più facile di HTML!)
```

**ESEMPIO ARCHITETTURA:**
```python
import httpx

# Headers che simulano browser reale
headers = {
    'User-Agent': 'Mozilla/5.0...',
    'Accept': 'application/json',
    # Altri headers necessari
}

# Chiamata GraphQL diretta
response = httpx.post(
    'https://www.booking.com/graphql',
    json={
        'query': '...',  # Query per prezzi
        'variables': {...}
    },
    headers=headers
)

data = response.json()
prices = extract_prices(data)
```

**PRO:**
- JSON parsing più facile di HTML
- Più veloce
- Meno fragile a cambi UI

**CONTRO:**
- GraphQL endpoint può essere protetto
- Headers/authentication complessi
- Booking.com può cambiare schema
- **Stessa zona grigia legale**

---

### 2.4 Come Fanno i Big Player RMS?

**RICERCA:** Come IDeaS, Duetto, Atomize ottengono dati competitor?

**FINDING (2026):**
> "Rate data is scraped from selected distribution channels and displayed on an interactive dashboard."
> "Think of it as hotel industry's version of surveillance, only instead of hidden cameras, we're talking about web scrapers and pricing tools."

**CONCLUSIONE:**
- **Tutti usano scraping** (direttamente o via third-party)
- Non usano API ufficiali (non esistono per questo scopo)
- Usano servizi specializzati come RateGain, OTAInsight
- Enterprise RMS hanno team dedicati per scraping

**INTEGRAZIONE CON RMS:**
> "When integrated with RMS, this data helps hoteliers make informed decisions to optimize revenue strategies in response to changing market dynamics."

**KEY INSIGHT:**
- Non è il scraping che differenzia
- È COME usi i dati (AI, suggestions, transparency)
- **Miracollo advantage:** Learning AI + Transparent AI + Native PMS

---

### 2.5 Data Collection Frequency - Best Practices

**DOMANDA:** Quanto spesso fare scraping?

**INDUSTRY STANDARD (2026):**
```
Real-time:  Marriott, grandi catene (10+ billion rates/month!)
Daily:      Most common per independent hotels
Weekly:     Budget option
On-demand:  Per date specifiche
```

**RACCOMANDAZIONE PER MIRACOLLO MVP:**
```
FASE 1 (MVP):
- Daily scraping (1x al giorno, ore notturne)
- 5-10 competitor per hotel
- Booking.com solo (principale OTA in Italia)

FASE 2 (Growth):
- 2-3x daily (mattina, pomeriggio, sera)
- 15-20 competitor
- +Expedia, +Airbnb

FASE 3 (Scale):
- Near real-time (ogni 2-4 ore)
- Tutti competitor rilevanti
- Tutti major OTA
```

**STORAGE NEEDS:**
```
1 hotel, 5 competitor, 365 giorni forecast
= 5 competitors × 365 days × 1 scrape/day
= 1,825 records/anno per hotel

20 hotel = 36,500 records/anno
Storage: ~50MB (trascurabile!)
```

---

### 2.6 Architettura Consigliata

**ARCHITECTURE DIAGRAM:**
```
+------------------+
|  Miracollo PMS   |
+------------------+
        |
        v
+------------------+       +-------------------+
| Competitor Price | <---> | ScrapingBee API   |
| Service          |       | (o alternative)   |
+------------------+       +-------------------+
        |                          |
        v                          v
+------------------+       +-------------------+
| PostgreSQL       |       | Booking.com       |
| - competitors    |       | Expedia           |
| - prices         |       | Airbnb            |
+------------------+       +-------------------+
        |
        v
+------------------+
| RateBoard UI     |
| - Heatmap        |
| - AI Suggestions |
+------------------+
```

**COMPONENTI:**

1. **Scraping Service** (Backend Python)
   ```
   - Cron job (daily)
   - Chiamata ScrapingBee API
   - Parsing HTML → structured data
   - Error handling + retry logic
   - Rate limiting
   ```

2. **Database Schema** (già esiste!)
   ```sql
   -- Da stato.md: schema già pronto
   competitors (id, hotel_id, name, booking_url, ...)
   competitor_prices (id, competitor_id, date, price, ...)
   ```

3. **API Endpoints** (Backend FastAPI)
   ```
   GET /api/competitors/{hotel_id}/prices
   GET /api/competitors/{hotel_id}/comparison?date=...
   POST /api/competitors/{hotel_id}/trigger_scrape
   ```

4. **Frontend Integration**
   ```
   - Competitor card in RateBoard
   - Price comparison chart
   - Alert se competitor cambia prezzo
   ```

---

### 2.7 Error Handling & Resilience

**PROBLEMI COMUNI:**
```
1. CAPTCHA → ScrapingBee lo risolve automaticamente
2. IP Ban → Proxy rotation automatica
3. HTML structure change → Monitora + alert + fix
4. Rate limit → Exponential backoff + rispetta limiti
5. Data quality → Validation rules + outlier detection
```

**MONITORING:**
```python
# Metriche da tracciare
- Success rate (target: >95%)
- Average response time
- Cost per request
- Data freshness (last_updated timestamp)
- Error types frequency
```

---

## CONCLUSIONI PARTE 2

### Confronto Approcci

| Approccio | Costo/mese | Risk Legale | Dev Time | Maintenance | Recommended |
|-----------|------------|-------------|----------|-------------|-------------|
| OTAInsight | $500-1500 | BASSO | 1-2 days | BASSA | Post-traction |
| RateGain | $500-1200 | BASSO | 1-2 days | BASSA | Enterprise |
| ScrapingBee | $10-100 | MEDIO-BASSO | 1-2 weeks | MEDIA | **MVP** ⭐ |
| Bright Data | $100-500 | MEDIO-BASSO | 1-2 weeks | MEDIA | Scale-up |
| DIY Playwright | $70-250 | MEDIO-ALTO | 6-8 weeks | ALTA | No |
| DIY HTTP | $50 | ALTO | 4 weeks | ALTA | No |

### La Mia Raccomandazione per MVP

**WINNER: ScrapingBee + Custom Parser**

**PERCHE:**
1. **Costo accessibile:** $10-50/mese per 20 hotel
2. **Time-to-Market:** 1-2 settimane implementazione
3. **Risk ragionevole:** Legalmente più sicuro di DIY, meno di niente
4. **Controllo:** Possiamo customizzare tutto
5. **Scalabilità:** Se funziona, upgrade a OTAInsight è facile

**IMPLEMENTATION PLAN (next doc):**
```
FASE 1: PoC (3-5 giorni)
- Setup ScrapingBee account
- Test scraping 1 hotel
- Parse HTML → extract price
- Save to database

FASE 2: Production (5-7 giorni)
- Cron job setup
- Multi-competitor support
- Error handling robusto
- Frontend integration

FASE 3: Polish (3-5 giorni)
- Monitoring dashboard
- Alerts
- Data quality checks
```

---

*Questo documento è PARTE 2 di 3*
*Continua in: 20260113_RICERCA_COMPETITOR_SCRAPING_PARTE3.md*

---

**Fonti Consultate (PARTE 2):**
- [OTA Insight Reviews 2026 Hotel Tech Report](https://hoteltechreport.com/revenue-management/market-intelligence-tools/lighthouse-rate-insight)
- [10 Best Hotel Rate Shoppers in 2026](https://hoteltechreport.com/revenue-management/market-intelligence-tools)
- [RateGain Competitor Price Intelligence](https://rategain.com/rate-intelligence-overview/)
- [Triptease Reviews 2026](https://hoteltechreport.com/revenue-management/hotel-rate-parity/triptease-data-marketing)
- [ScrapingBee vs Bright Data Comparison](https://www.scraperapi.com/comparisons/brightdata-vs-scrapingbee/)
- [ScrapingBee Review 2025](https://leadadvisors.com/blog/scrapingbee-review/)
- [Bright Data Pricing 2026](https://www.firecrawl.dev/blog/bright-data-pricing)
- [How to Scrape Booking.com 2026](https://scrapfly.io/blog/posts/how-to-scrape-bookingcom)
- [Playwright vs Puppeteer 2026](https://research.aimultiple.com/playwright-vs-puppeteer/)
- [Avoid Bot Detection with Playwright Stealth](https://www.scrapeless.com/en/blog/avoid-bot-detection-with-playwright-stealth)
- [Hotel Rate Shopping Data Collection](https://www.altexsoft.com/blog/hotel-data-management-best-practices/)
