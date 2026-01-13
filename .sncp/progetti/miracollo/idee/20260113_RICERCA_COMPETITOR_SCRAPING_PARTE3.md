# RICERCA: Competitor Price Scraping - PARTE 3
> **Data:** 13 Gennaio 2026
> **Ricercatrice:** Cervella Researcher
> **Progetto:** Miracollo RateBoard

*Continua da PARTE 2*

---

## PARTE 3: PIANO IMPLEMENTAZIONE E STIMA EFFORT

### 3.1 Strategia Raccomandata: 3-Tier Approach

```
+================================================================+
|                                                                |
|   TIER 1 (IMMEDIATO):    ScrapingBee MVP                       |
|   TIER 2 (PARALLELO):    Booking.com Affiliate API Application|
|   TIER 3 (FUTURO):       OTAInsight Partnership               |
|                                                                |
+================================================================+
```

**PERCHE TRE TIER:**
1. Tier 1 ci da feature SUBITO (time-to-market)
2. Tier 2 ci da sicurezza legale (parallel track)
3. Tier 3 ci da scale enterprise (quando cresciamo)

---

## TIER 1: MVP con ScrapingBee

### FASE 1: PoC (Proof of Concept)
**Durata:** 3-5 giorni
**Obiettivo:** Validare che possiamo scrapare Booking.com con successo

#### Step 1.1: Setup ScrapingBee (1 giorno)
```
[ ] Account ScrapingBee (free tier per test)
[ ] API key generata
[ ] Test chiamata API base
[ ] Verifica credits + pricing
```

**Code Example:**
```python
# backend/services/scraping_service.py
import httpx
from typing import Optional

class ScrapingBeeClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://app.scrapingbee.com/api/v1"

    async def scrape_url(self, url: str) -> Optional[str]:
        """Scrape URL usando ScrapingBee"""
        params = {
            'api_key': self.api_key,
            'url': url,
            'render_js': 'true',  # Booking.com usa React
            'premium_proxy': 'true',  # Booking.com è protected
            'country_code': 'it'  # Target italiano
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url, params=params)

            if response.status_code == 200:
                return response.text
            else:
                # Log error
                return None
```

#### Step 1.2: Test Scraping 1 Hotel (1 giorno)
```
[ ] URL Booking.com di test hotel
[ ] Chiamata ScrapingBee
[ ] Verifica HTML ritornato
[ ] Identificare selettori CSS per prezzi
```

**Challenge:** Trovare selettori CSS corretti
**Tool:** Chrome DevTools per ispezionare HTML

#### Step 1.3: Parse HTML → Extract Price (1-2 giorni)
```
[ ] Libreria parsing (BeautifulSoup4 o parsel)
[ ] Extract: prezzo, disponibilità, tipo camera
[ ] Handle prezzi multipli (standard, non-refundable, etc)
[ ] Data validation (prezzo ragionevole? data valida?)
```

**Code Example:**
```python
# backend/services/booking_parser.py
from bs4 import BeautifulSoup
from decimal import Decimal
from datetime import date

def parse_booking_prices(html: str, check_in: date, check_out: date):
    """Parse HTML di Booking.com per estrarre prezzi"""
    soup = BeautifulSoup(html, 'html.parser')

    results = []

    # Selettori CSS (da verificare su pagina reale!)
    price_elements = soup.select('.bui-price-display__value')
    room_elements = soup.select('.hprt-roomtype-title')

    for price_el, room_el in zip(price_elements, room_elements):
        try:
            # Extract prezzo (rimuovi € e converti)
            price_text = price_el.text.strip().replace('€', '').replace(',', '')
            price = Decimal(price_text)

            # Extract tipo camera
            room_type = room_el.text.strip()

            results.append({
                'check_in': check_in,
                'check_out': check_out,
                'room_type': room_type,
                'price': price,
                'currency': 'EUR'
            })
        except Exception as e:
            # Log parsing error
            continue

    return results
```

#### Step 1.4: Save to Database (0.5 giorni)
```
[ ] Insert in competitor_prices table
[ ] Handle duplicates (unique constraint)
[ ] Timestamp di scraping
```

**DELIVERABLE FASE 1:**
- Script funzionante che scrapa 1 hotel
- Dati salvati correttamente in DB
- Success rate documentato
- Costo per request calcolato

---

### FASE 2: Production-Ready (5-7 giorni)
**Obiettivo:** Sistema robusto per multi-hotel production

#### Step 2.1: Multi-Competitor Support (1 giorno)
```
[ ] Loop su lista competitor per hotel
[ ] Rate limiting (1 request ogni 2 secondi)
[ ] Batch processing
```

**Code Example:**
```python
# backend/routers/competitor_scraping.py
from fastapi import APIRouter, BackgroundTasks
import asyncio

router = APIRouter()

@router.post("/api/competitors/{hotel_id}/scrape")
async def trigger_scrape(
    hotel_id: int,
    background_tasks: BackgroundTasks
):
    """Trigger scraping di tutti competitor per hotel"""
    background_tasks.add_task(scrape_all_competitors, hotel_id)
    return {"status": "scraping_started"}

async def scrape_all_competitors(hotel_id: int):
    """Background task per scraping"""
    competitors = await get_competitors(hotel_id)

    for competitor in competitors:
        # Rate limiting
        await asyncio.sleep(2)

        html = await scraping_client.scrape_url(competitor.booking_url)
        if html:
            prices = parse_booking_prices(html, check_in, check_out)
            await save_prices(competitor.id, prices)
```

#### Step 2.2: Cron Job Setup (1 giorno)
```
[ ] Script cron giornaliero
[ ] Ora esecuzione (3 AM Italia, basso traffico)
[ ] Logging in file
[ ] Email alert se fallisce
```

**Cron Config:**
```bash
# /etc/cron.d/miracollo-scraping
0 3 * * * www-data cd /var/www/miracollo && python backend/scripts/daily_scrape.py >> /var/log/miracollo/scraping.log 2>&1
```

**Script:**
```python
# backend/scripts/daily_scrape.py
import asyncio
from services.scraping_service import scrape_all_hotels
from utils.notifications import send_alert

async def main():
    try:
        results = await scrape_all_hotels()

        # Check success rate
        success_rate = results['success'] / results['total']

        if success_rate < 0.90:  # Alert se < 90%
            await send_alert(
                f"Scraping success rate basso: {success_rate:.1%}"
            )

        print(f"Scraping completato: {results}")

    except Exception as e:
        await send_alert(f"Scraping fallito: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
```

#### Step 2.3: Error Handling Robusto (1-2 giorni)
```
[ ] Retry logic (3 tentativi con exponential backoff)
[ ] Timeout handling
[ ] Invalid data detection
[ ] Fallback values
[ ] Error tracking (sentry?)
```

**Code Example:**
```python
# backend/utils/retry.py
import asyncio
from typing import Callable, Optional

async def retry_with_backoff(
    func: Callable,
    max_attempts: int = 3,
    base_delay: float = 1.0
) -> Optional[any]:
    """Retry con exponential backoff"""

    for attempt in range(max_attempts):
        try:
            return await func()
        except Exception as e:
            if attempt == max_attempts - 1:
                # Ultimo tentativo fallito
                raise

            delay = base_delay * (2 ** attempt)
            await asyncio.sleep(delay)
```

#### Step 2.4: Data Quality Checks (1 giorno)
```
[ ] Prezzo range validation (€20-€500?)
[ ] Outlier detection (prezzo 10x media = errore?)
[ ] Completeness check (tutti competitor scrapati?)
[ ] Historical comparison (prezzo cambiato troppo?)
```

#### Step 2.5: API Endpoints (1 giorno)
```
[ ] GET /api/competitors/{hotel_id}/prices?date=YYYY-MM-DD
[ ] GET /api/competitors/{hotel_id}/comparison
[ ] POST /api/competitors/{hotel_id}/scrape (manual trigger)
[ ] GET /api/competitors/{hotel_id}/status (last scrape info)
```

**DELIVERABLE FASE 2:**
- Sistema production-ready
- Cron job automatico
- API completa
- Error handling robusto
- Monitoring basic

---

### FASE 3: Frontend Integration (3-5 giorni)
**Obiettivo:** Mostrare dati competitor in RateBoard

#### Step 3.1: Competitor Price Widget (1-2 giorni)
```
[ ] Card con prezzi competitor
[ ] Grafico comparativo (line chart)
[ ] Color coding (nostro prezzo vs competitor)
[ ] Tooltip con dettagli
```

**UI Mock:**
```
+-------------------------------------------+
|  COMPETITOR PRICES - 15 Gennaio 2026      |
+-------------------------------------------+
|                                           |
|  Tuo prezzo:    €120                      |
|  Media mercato: €135  (+12%)              |
|                                           |
|  [Grafico line chart]                     |
|                                           |
|  Competitor 1: €140  [Hotel Best]         |
|  Competitor 2: €130  [Palace Inn]         |
|  Competitor 3: €135  [Grand Hotel]        |
|                                           |
|  Ultimo aggiornamento: 3:15 AM            |
+-------------------------------------------+
```

#### Step 3.2: Price Comparison Table (1 giorno)
```
[ ] Tabella con tutti competitor
[ ] Sort by price
[ ] Filtri (date, room type)
[ ] Export CSV
```

#### Step 3.3: Alert System (1 giorno)
```
[ ] Badge "Competitor ha abbassato prezzo!"
[ ] Notifica in UI
[ ] Email opzionale
```

#### Step 3.4: Integrazione AI Suggestions (1 giorno)
```
[ ] Modify suggerimenti_engine.py
[ ] Usa dati competitor per suggestions
[ ] "Sei €20 sopra media mercato - considera riduzione"
```

**DELIVERABLE FASE 3:**
- UI completa per competitor prices
- Integrazione in RateBoard esistente
- Alert system funzionante

---

### FASE 4: Monitoring & Polish (2-3 giorni)
**Obiettivo:** Sistema production-grade con monitoring

#### Step 4.1: Monitoring Dashboard (1-2 giorni)
```
[ ] Metriche real-time
[ ] Success rate graph
[ ] Cost tracking
[ ] Error log viewer
```

**Metriche da tracciare:**
```
- Requests totali oggi
- Success rate (target 95%+)
- Average response time
- Costo totale mese
- Hotel coverage (% hotel con dati fresh)
- Data freshness (ore dall'ultimo scrape)
```

#### Step 4.2: Alerting (0.5 giorni)
```
[ ] Email se success rate < 90%
[ ] Email se costo > budget
[ ] Slack/Discord webhook opzionale
```

#### Step 4.3: Documentation (0.5 giorni)
```
[ ] README per team
[ ] Troubleshooting guide
[ ] API documentation
[ ] Runbook operativo
```

**DELIVERABLE FASE 4:**
- Sistema completo production-grade
- Monitoring robusto
- Documentazione completa

---

## TIER 2: Booking.com Affiliate API (Parallel Track)

**Timeline:** 2-8 settimane (dipende da approval)

### Step 1: Application (1 giorno)
```
[ ] Compilare form partnership Booking.com
[ ] Spiegare use case (RMS per independent hotels)
[ ] Attendere risposta
```

**URL:** https://www.booking.com/affiliate.html

### Step 2: Integration (SE approvati) (3-5 giorni)
```
[ ] API credentials
[ ] Leggere docs
[ ] Implement integration
[ ] Migrate da ScrapingBee (graduale)
```

**PRO:**
- Legalmente perfetto
- Dati ufficiali
- Rate limit ragionevoli

**CONTRO:**
- Approval incerto
- Potrebbe rifiutare (competitor comparison non è vendita)
- Timeline imprevedibile

---

## TIER 3: OTAInsight Partnership (Futuro)

**Timeline:** Quando Miracollo ha 50+ hotel clienti

### Quando Considerare:
```
✓ Miracollo ha traction (50+ hotel)
✓ Budget disponibile ($500-1500/mese)
✓ Vogliamo scale a 100+ hotel
✓ Serve supporto enterprise
```

### Benefits:
- Zero maintenance
- Legal compliance garantita
- Enterprise-grade reliability
- Supporto professionale
- Additional data (eventi, meteo, flight data)

---

## 3.2 Stima Effort Completa

### TIER 1 (MVP ScrapingBee)

| Fase | Durata | Chi |
|------|--------|-----|
| FASE 1: PoC | 3-5 giorni | Backend developer |
| FASE 2: Production | 5-7 giorni | Backend developer |
| FASE 3: Frontend | 3-5 giorni | Frontend developer |
| FASE 4: Polish | 2-3 giorni | Full-stack |
| **TOTALE** | **13-20 giorni** | **2-3 settimane** |

### Breakdown per Ruolo

**Backend Developer:**
- Scraping service: 3 giorni
- Parser: 2 giorni
- API endpoints: 2 giorni
- Cron job: 1 giorno
- Error handling: 2 giorni
- Monitoring: 1 giorno
- **Subtotal: 11 giorni**

**Frontend Developer:**
- Competitor widget: 2 giorni
- Price table: 1 giorno
- Charts: 1 giorno
- Alert system: 1 giorno
- **Subtotal: 5 giorni**

**Full-Stack (Polish):**
- Testing end-to-end: 1 giorno
- Bug fixes: 1 giorno
- Documentation: 1 giorno
- **Subtotal: 3 giorni**

---

## 3.3 Costi Stimati

### Costi di Sviluppo (One-Time)
```
Backend:   11 giorni × €400/giorno = €4,400
Frontend:  5 giorni × €350/giorno  = €1,750
Full-stack: 3 giorni × €400/giorno = €1,200
-------------------------------------------
TOTALE SVILUPPO:                    €7,350
```

### Costi Operativi Mensili (Recurring)

**SCENARIO 1: Small (10 hotel)**
```
ScrapingBee:
- 10 hotel × 5 competitor × 30 giorni = 1,500 requests/mese
- A $2.50/1K = $3.75/mese
- ~€3.50/mese

Server overhead: €0 (usa server esistente)
-------------------------------------------
TOTALE MENSILE:  €3.50 (~trascurabile!)
```

**SCENARIO 2: Medium (50 hotel)**
```
ScrapingBee:
- 50 hotel × 5 competitor × 30 giorni = 7,500 requests/mese
- A $2.50/1K = $18.75/mese
- ~€17/mese

Server overhead: €0
-------------------------------------------
TOTALE MENSILE:  €17
```

**SCENARIO 3: Large (200 hotel)**
```
ScrapingBee:
- 200 hotel × 10 competitor × 30 giorni = 60,000 requests/mese
- A $2.50/1K = $150/mese
- ~€140/mese

A questo punto considera:
- OTAInsight ($500-1000/mese) diventa competitivo
- O Bright Data enterprise plan
-------------------------------------------
TOTALE MENSILE:  €140
```

### ROI Analysis

**VALORE PER HOTEL:**
```
Se Competitor Scraping aiuta hotel a:
- Ottimizzare prezzi meglio
- Aumentare RevPAR anche solo 2-3%

Hotel con €50K revenue/anno:
2% RevPAR increase = €1,000/anno

Miracollo può giustificare:
€20-50/mese extra fee per questa feature
= €240-600/anno per hotel

Con 20 hotel = €4,800-12,000/anno
Costo sviluppo: €7,350 (one-time)
Payback: 6-18 mesi ✅
```

---

## 3.4 Rischi e Mitigazioni

### RISCHIO 1: Booking.com Cambia HTML
**Probabilità:** ALTA (ogni 2-6 mesi)
**Impatto:** ALTO (scraping smette di funzionare)

**Mitigazione:**
- Monitoring automatico (alert se parsing fallisce)
- Test suite che verifica selettori
- Budget per manutenzione (2-4 giorni/anno)
- Considera GraphQL API approach (più stabile)

### RISCHIO 2: Ban/Rate Limiting
**Probabilità:** MEDIA
**Impatto:** MEDIO

**Mitigazione:**
- Usa ScrapingBee (loro gestiscono proxy rotation)
- Rate limiting conservativo (1 request/2 sec)
- Scraping notturno (meno traffico)
- Fallback: se ban, wait 24h e riprova

### RISCHIO 3: Azione Legale
**Probabilità:** BASSA
**Impatto:** ALTO

**Mitigazione:**
- Rispetta robots.txt
- Rate limiting ragionevole
- Dati pubblici solo (no login)
- Legal disclaimer
- Piano B: pivot a Affiliate API o OTAInsight

### RISCHIO 4: Costi Inaspettati
**Probabilità:** MEDIA
**Impatto:** BASSO

**Mitigazione:**
- Budget cap su ScrapingBee
- Alert se costo > $100/mese
- Monitoring consumi giornaliero

---

## 3.5 Success Metrics

**METRICHE TECNICHE:**
```
✓ Success rate scraping: >95%
✓ Data freshness: <24h
✓ API response time: <500ms
✓ Uptime: >99%
✓ Parsing accuracy: >98%
```

**METRICHE BUSINESS:**
```
✓ Hotel che usano feature: >80%
✓ Decisioni pricing influenzate: >40%
✓ Feedback positivo: >4/5
✓ Churn reduction: -10% (grazie a feature)
```

**METRICHE COSTO:**
```
✓ Costo per hotel per mese: <€5
✓ Payback sviluppo: <18 mesi
✓ Margin positivo: >70%
```

---

## 3.6 RACCOMANDAZIONE FINALE

### LA MIA RACCOMANDAZIONE CHIARA

```
+================================================================+
|                                                                |
|   PROCEDERE CON TIER 1 (ScrapingBee MVP)                       |
|                                                                |
|   PERCHE:                                                      |
|   ✓ Time-to-market rapido (2-3 settimane)                     |
|   ✓ Costi bassissimi (€3-20/mese per 10-50 hotel)             |
|   ✓ Risk legale accettabile (zona grigia ma praticabile)      |
|   ✓ ROI positivo in 6-18 mesi                                 |
|   ✓ Completa il GAP critico in RateBoard                      |
|   ✓ Possiamo sempre pivotare a Tier 2/3 dopo                  |
|                                                                |
|   IN PARALLELO:                                                |
|   → Applicare a Booking.com Affiliate API (Tier 2)            |
|   → Se approvati, migrare. Se no, continuiamo con Tier 1.     |
|                                                                |
+================================================================+
```

### Prossimi Step IMMEDIATI

1. **Decision Point (Regina):** Approva strategia?
2. **SE SÌ:**
   - Setup ScrapingBee account (free trial)
   - Assign a Backend developer
   - Start FASE 1 PoC (3-5 giorni)
3. **IN PARALLELO:**
   - Apply to Booking.com Affiliate Program
   - Research legal counsel (optional, per sicurezza)

### Alternative SE la Regina decide "NO"

```
ALTERNATIVA 1: Aspettare Booking.com API
- PRO: Zero risk legale
- CONTRO: Timeline incerta (2-6 mesi?), approval incerta

ALTERNATIVA 2: Iniziare con OTAInsight
- PRO: Zero dev, zero risk
- CONTRO: Costo alto ($500-1500/mese), dipendenza vendor

ALTERNATIVA 3: Feature freeze (non implementare)
- PRO: Zero costo, zero risk
- CONTRO: Gap critico rimane, competitor hanno vantaggio
```

**LA MIA OPINIONE:**
ALTERNATIVA 3 è la peggiore. Competitor pricing è **TABLE STAKES** per RMS nel 2026. Tutti i competitor lo hanno. Non averlo è un gap competitivo significativo.

---

## CONCLUSIONI FINALI

### Summary per la Regina

**DOMANDA ORIGINALE:**
"Come fare scraping prezzi competitor da Booking.com per Miracollo RMS?"

**RISPOSTA:**
```
1. LEGALITA: Zona grigia ma praticabile con cautela
2. APPROCCIO: ScrapingBee (third-party) per MVP
3. COSTI: €7K sviluppo + €3-20/mese operativi
4. TIMELINE: 2-3 settimane implementazione
5. ROI: Positivo in 6-18 mesi
6. RISCHIO: Medio-basso con mitigazioni
```

**RACCOMANDAZIONE:**
✅ **PROCEDERE** con TIER 1 (ScrapingBee MVP)
✅ **PARALLELO** apply to Booking.com Affiliate API
✅ **FUTURO** consider OTAInsight quando scale (50+ hotel)

**VALORE:**
Questa feature completa il GAP CRITICO identificato nell'audit:
```
DA: RATEBOARD 8.5/10 (senza competitor pricing)
A:  RATEBOARD 9.5/10 (con competitor pricing)
```

**IL MOMENTO È ADESSO:**
- Database schema GIA pronto
- Team tecnico disponibile
- RateBoard base solido (FASE 1-2-3 complete)
- Competitor TUTTI hanno questa feature

> "Non esistono cose difficili, esistono cose non studiate!"
> Abbiamo studiato. Ora implementiamo. 🚀

---

*Fine PARTE 3 - Fine ricerca completa*

---

**Fonti Consultate (PARTE 3):**
Tutte le fonti delle PARTE 1 e PARTE 2, più:
- [Understanding hotel rate shopping software | Duetto](https://www.duettocloud.com/library/understanding-hotel-rate-shopping-software)
- [What is a hotel rate shopper | Cloudbeds](https://www.cloudbeds.com/articles/hotel-rate-shopper/)
- [Hotel Rate Intelligence Tool | MakCorps](https://www.makcorps.com/hotel-rate-intelligence.html)
- [Best Hotel Rate Shopping Software 2026 | HotelMinder](http://www.hotelminder.com/best-hotel-rate-shopping-market-intelligence-software)

---

**Files Creati Questa Ricerca:**
```
.sncp/progetti/miracollo/idee/
├── 20260113_RICERCA_COMPETITOR_SCRAPING_PARTE1.md (Legalità)
├── 20260113_RICERCA_COMPETITOR_SCRAPING_PARTE2.md (Approcci)
└── 20260113_RICERCA_COMPETITOR_SCRAPING_PARTE3.md (Implementation)
```

**Total Research:** 3 documenti, ~1,500 righe, 30+ fonti consultate

*Cervella Researcher - "Un'ora di ricerca risparmia dieci ore di codice sbagliato!"* 🔬
