# Studio: Best Practices Guest Management nei PMS Professionali

**Data:** 29 Gennaio 2026
**Ricercatrice:** Cervella Researcher
**Obiettivo:** Capire come i big player (Mews, Opera, Cloudbeds, RoomRaccoon, Protel) gestiscono gli ospiti professionalmente

---

## Executive Summary

**Problema identificato:** Miracollook attualmente filtra solo ospiti con email. Approccio superficiale.

**Scoperta chiave:** I PMS professionali separano GUEST PROFILE (entità permanente) da BOOKING/RESERVATION (entità transazionale), con relazione 1:N. Un ospite può avere zero contatti, ma il profilo esiste sempre.

**Raccomandazione:** Miracollook deve:
1. Tracciare TUTTI gli ospiti (anche senza email)
2. Implementare stati booking standard del settore
3. Supportare comunicazione multi-canale (email, SMS, WhatsApp)
4. Gestire lifecycle post-stay per loyalty

---

## PARTE 1: Guest Profile vs Booking - L'Architettura Fondamentale

### Il Modello Dati Standard

**Tutti i PMS professionali usano questo pattern:**

```
GUEST PROFILE (1) ←────→ (N) BOOKINGS
     │                        │
     │                        │
  Permanente              Transazionale
  (chi è)                (quando viene)
```

### Perché Questa Separazione?

**GUEST PROFILE = Entità Permanente**
- Memorizza chi è l'ospite
- Contiene preferenze, storico, loyalty status
- Persiste nel tempo attraverso più soggiorni
- Può esistere anche SENZA prenotazioni attive

**BOOKING/RESERVATION = Entità Transazionale**
- Memorizza quando l'ospite soggiorna
- Date, camera, tariffe, servizi
- Ha un lifecycle (tentative → confirmed → in-house → checked-out)
- Sempre linkato a UN guest profile

**PERCHÉ È IMPORTANTE:**
Un ospite che torna 5 volte = 1 profilo ospite + 5 prenotazioni.
Questo permette di:
- Tracciare storico completo
- Personalizzare servizio basato su soggiorni precedenti
- Calcolare lifetime value
- Gestire loyalty programs

**Fonte:** [Redgate - Data Model for Hotel Management System](https://www.red-gate.com/blog/data-model-for-hotel-management-system)

---

## PARTE 2: Dati Minimi Guest Profile

### Cosa Tracciano i Big Player

Secondo l'analisi di PMS professionali, questi sono i campi ESSENZIALI:

#### DATI BASE (Obbligatori)
```
✓ Guest Type (Guest o Booker)
✓ Name (Full name, Title, First/Last name separati)
✓ Contact Info:
  - Email (può essere NULL!)
  - Phone (può essere NULL!)
  - Address + ZIP/Postal Code
```

#### PREFERENZE (Opzionali ma critici)
```
✓ Room Preferences (tipo camera, piano, vista)
✓ Dietary Needs (allergie, preferenze alimentari)
✓ Pillow Type (dettaglio che fa la differenza!)
✓ Special Requests
✓ Travel Purpose (Business vs Leisure)
```

#### STORICO & LOYALTY
```
✓ Booking History (link a tutte le prenotazioni passate)
✓ Loyalty Status (VIP, member, first-time guest)
✓ Past Service Requests
✓ Stay Anniversaries / Special Occasions
✓ Communication Preferences (preferenza canale)
```

#### FINANCIAL
```
✓ Default Payment Method
✓ Billing Preferences (per corporate guests)
✓ Company Details (se business traveler)
```

### Cosa Significa per Miracollook?

**❌ ERRORE ATTUALE:** Filtriamo solo ospiti con email
**✅ APPROCCIO CORRETTO:** Tracciamo TUTTI gli ospiti, email è solo un campo opzionale

**CASO D'USO REALE:**
Famiglia di 4 persone:
- Padre (booker) → ha email
- Madre → no email
- 2 bambini → no email

Approccio superficiale: Vediamo solo il padre
Approccio professionale: Vediamo tutti e 4, con flag "booker" sul padre

**Fonti:**
- [AltexSoft - Hotel PMS Complete Guide](https://www.altexsoft.com/blog/hotel-property-management-systems-products-and-features/)
- [RoomMaster - Hotel Guest Profile Basics](https://www.roommaster.com/blog/hotel-guest-profile)

---

## PARTE 3: Stati Booking/Reservation - Il Lifecycle Standard

### Gli Stati Standard del Settore

Ecco gli stati che TUTTI i PMS professionali implementano:

```
TENTATIVE (Richiesta iniziale)
    ↓
WAITLISTED (In attesa disponibilità)
    ↓
CONFIRMED (Prenotazione confermata)
    ├─→ NON-GUARANTEED (senza garanzia)
    └─→ GUARANTEED (con carta/deposito)
        ↓
    CHECKED-IN / IN-HOUSE (Ospite in hotel)
        ↓
    CHECKED-OUT (Fine soggiorno)
        ↓
    POST-STAY (Comunicazione post-partenza)

STATI ALTERNATIVI:
├─→ CANCELLED (Cancellato)
├─→ NO-SHOW (Non si è presentato)
└─→ MODIFIED (Modificato, torna a CONFIRMED)
```

### Dettaglio Stati

#### 1. TENTATIVE
**Quando:** Richiesta iniziale, ancora da confermare
**Durata:** Fino a cutoff date (12-48h prima arrivo)
**Se non confermato:** Automaticamente rilasciato
**Opera PMS:** "Configuring Guest Status" permette stati custom

#### 2. WAITLISTED
**Quando:** Camera richiesta non disponibile
**Azione:** Viene confermato se altro ospite cancella
**Nota:** Non tutti i PMS hanno questo stato

#### 3. CONFIRMED
**Quando:** Prenotazione garantita
**Sottotipo Guaranteed:** Con carta credito o deposito
**Sottotipo Non-Guaranteed:** Solo conferma verbale
**Cutoff Rule:** Se non si presenta e non-guaranteed, no addebito

#### 4. CHECKED-IN / IN-HOUSE
**Quando:** Ospite ha fatto check-in
**Flag sistema:** occupied = YES
**Durata:** Dal check-in al check-out
**Cloudbeds:** "In-House" è lo stato durante soggiorno

#### 5. CHECKED-OUT
**Quando:** Ospite ha lasciato l'hotel
**Flag sistema:** occupied = NO
**Azione successiva:** Trigger per post-stay communication
**Timing:** Entro 24-48h parte comunicazione post-stay

#### 6. NO-SHOW
**Quando:** Ospite non si presenta senza cancellare
**Timing:** Se non check-in entro 22:00 (o cutoff time hotel)
**Addebito standard:** 1 notte di room rate
**Azione staff:** Deve essere processato giornalmente (daily no-show task)

#### 7. CANCELLED
**Quando:** Ospite cancella in anticipo
**Policy:** Tipicamente 24-72h prima arrivo per evitare fee
**Differenza da No-Show:** Qui c'è comunicazione preventiva

#### 8. POST-STAY (implicito)
**Quando:** Dopo check-out
**Non è uno stato booking, è una FASE del guest lifecycle**
**Durata:** Indefinita, fino a prossima prenotazione
**Importanza:** Critica per loyalty e repeat bookings

### Stati Operativi Aggiuntivi

Opera PMS traccia anche stati ROOM (non guest):
- Clean / Dirty
- Inspected
- Pick Up
- Out of Order / Out of Service

**Fonti:**
- [Oracle Opera - Configuring Guest Status](https://docs.oracle.com/en/industries/hospitality/opera-cloud/21.5/ocsuh/t_admin_booking_configuring_guest_status.htm)
- [Cloudbeds - Check-in and Check-out Guide](https://myfrontdesk.cloudbeds.com/hc/en-us/articles/221677468-Check-in-and-check-out-guests-in-Cloudbeds-PMS)
- [SetupMyHotel - Reservation Status Sample](https://setupmyhotel.com/hotel-formats/front-office-formats/reservation-status-sample-for-hotels-and-resorts/)

---

## PARTE 4: Canali di Comunicazione - L'Approccio Multi-Canale

### Il Paradigma Moderno: Unified Inbox

**Statistica chiave:** 70% dei viaggiatori preferisce canali digitali (chat, WhatsApp, SMS, Messenger) rispetto a telefono/email.

### I 3 Canali Principali

#### 1. EMAIL
**Quando usarlo:**
- Conferme prenotazione
- Fatture e documenti ufficiali
- Policy e termini
- Newsletter mensili
- Riassunto viaggio (pre-arrival)

**Caratteristica:** Formale, dettagliato, ha valore legale

#### 2. SMS
**Quando usarlo:**
- Notifiche urgenti e time-sensitive
- "Camera pronta" alerts
- Check-in reminders
- Codici accesso keyless entry
- Quick updates

**Caratteristica:** Immediato, breve, high open-rate (98%)
**Preferito da:** Guest domestici (Nord America)

#### 3. WhatsApp
**Quando usarlo:**
- Conversazioni interattive
- Richieste servizi durante soggiorno
- Supporto pre-arrivo
- Media sharing (foto, documenti)
- Follow-up post-stay

**Caratteristica:** Casuale, conversazionale, supporta media
**Preferito da:** Guest internazionali, mercati non-US

### Altri Canali Emergenti

- **Live Chat** (website)
- **OTA Messaging** (Booking.com, Expedia inbox)
- **Facebook Messenger**
- **WeChat** (mercato cinese)
- **LINE** (mercato giapponese)

### Smart Channel Routing

**Best Practice moderna:** Sistema intelligente sceglie canale basato su:
- Profilo ospite (nazionalità, preferenze)
- Tipo messaggio (urgente → SMS, formale → Email)
- Storico comunicazioni (risponde più su WhatsApp? Usa quello)

**Esempio Cloudbeds:**
Unified inbox gestisce SMS, email, WhatsApp, Booking.com, Expedia, Airbnb in un'unica interfaccia.

**Esempio GuestTouch:**
Routing automatico WhatsApp ↔ SMS basato su geolocalizzazione e preferenze.

### Regola d'Oro: "Right Message, Right Time, Right Channel"

NON è "mandare più messaggi", è "mandare il messaggio GIUSTO sul canale GIUSTO".

**Fonti:**
- [Cloudbeds - Guest Messaging Best Practices](https://www.cloudbeds.com/hotel-guest/messaging/)
- [Chekin - Hotel Guest Communication Guide](https://chekin.com/en/blog/hotel-guest-communication/)
- [INTELITY - Unified Guest Messaging](https://intelity.com/blog/unified-guest-messaging-for-hotels-why-sms-and-whatsapp-must-live-in-one-platform/)

---

## PARTE 5: Post-Stay Communication - La Fase Dimenticata

### Perché È Critica?

**DATO SCIOCCANTE:**
- Aumentare retention del 5% → aumenta profitti del 95%
- Guest loyalty spende 67% in più rispetto a non-loyal
- Effective post-stay CRM → +31-40% repeat bookings (Deloitte)

**IL PROBLEMA:** Molti hotel si dimenticano dell'ospite dopo check-out.
**LA SOLUZIONE:** Comunicazione strutturata post-stay.

### Timing Ottimale

#### Opzione 1: Immediata (24-48h)
**Pro:** Esperienza fresca nella mente
**Usato da:** Maggioranza dei big player
**Ideale per:** Review requests, feedback surveys

#### Opzione 2: Ritardata (2-3 giorni)
**Pro:** Ospite è tornato a casa, più rilassato
**Usato da:** Nallikari Holiday Village
**Ideale per:** Feedback più pensato, offerte future stay

**BEST PRACTICE:** Combinare entrambi!
- 24h: "Grazie per il soggiorno" + quick feedback
- 3-5 giorni: Review request + offerta speciale return

### Strategia Post-Stay Strutturata

**Caso Studio: Hyatt Hotels**
Sequenza in 3 step:
1. **Immediate Thank-You** (same day check-out)
2. **Personalized Feedback Request** (48h dopo)
3. **Targeted Booking Incentive** (1 settimana dopo, basato su storico)

**Risultato:** +28% rebooking rate vs standard follow-up

### Tipologie Messaggio Post-Stay

#### A. Review Requests
**Timing:** 24-48h dopo check-out
**Piattaforme:** Google, TripAdvisor, Booking.com
**Tone:** Cortese, non insistente
**CTA:** Link diretto alla review page

**Template Efficace:**
```
Caro [Nome],
Grazie per aver soggiornato con noi!

Ci piacerebbe sapere cosa hai pensato del tuo soggiorno.
Lasciare una recensione ci aiuta a migliorare.

[Link Review Google]

Grazie,
[Hotel Name]
```

#### B. Feedback Surveys
**Timing:** 24-48h dopo check-out
**Formato:** NPS (Net Promoter Score), satisfaction score
**Integrazione:** Mews PMS connette feedback direttamente al guest profile

#### C. Recovery Communication (per esperienze negative)
**Trigger:** Feedback score < soglia
**Timing:** IMMEDIATO (entro ore)
**Obiettivo:** Risolvere problema, salvare relazione
**Approccio:** Personalizzato, management involvement

#### D. Loyalty & Future Booking Incentives
**Timing:** 5-7 giorni dopo check-out
**Segmentazione:** Business vs Leisure, repeat vs first-time
**Contenuto:** Offerte speciali, early-bird rates, loyalty program

### Automazione Intelligente

**CHIAVE:** Automated ma PERSONALIZED

**Trigger Eventi:**
- Check-out → Thank you email
- Feedback negativo → Alert a manager + recovery email
- Feedback positivo → Review request
- 7 giorni dopo → Booking incentive
- Anniversario soggiorno → "Torna per l'anniversario" offer

**Segmentazione:**
- Business traveler: enfasi convenience, wifi, servizi lavoro
- Leisure guest: enfasi relax, attrazioni, famiglia
- VIP: comunicazione da management, benefit esclusivi

### Mobile-First Approach

**CRITICO:** 95% dei post-stay message vengono letti su mobile.

**Best Practices:**
- Subject line < 40 caratteri
- Email responsive design
- Link clickabili (review, booking)
- CTA chiara e grande
- Load rapido (no immagini pesanti)

**Fonti:**
- [Digital Guest - Post-Stay Email Templates](https://digitalguest.com/post-stay-email-templates/)
- [Typsy - CRM Transform Guest Experience](https://blog.typsy.com/from-check-in-to-loyalty-how-crm-can-transform-hotel-guest-experience)
- [SiteMin der - Hotel CRM Complete Guide](https://www.siteminder.com/r/customer-relationship-management/)

---

## PARTE 6: CRM Integration - Il Cuore del Sistema

### PMS vs CRM: Complementari, Non Sostitutivi

**PMS (Property Management System):**
Gestisce OPERAZIONI in tempo reale
- Check-in/out
- Room inventory
- Billing
- Housekeeping

**CRM (Customer Relationship Management):**
Gestisce RELAZIONI nel tempo
- Guest preferences
- Marketing campaigns
- Loyalty programs
- Lifetime value tracking

### Il Trend: PMS con CRM Integrato

**Esempi:**
- **Cloudbeds:** "More than hotel CRM" - CRM nativo nel PMS
- **Mews:** PMS-CRM integration per "transform guest experiences"
- **Opera Cloud:** Integrazione con CRM esterni via API

### Funzionalità CRM Essenziali

#### 1. Unified Guest Profile
- Dati da tutte le fonti (PMS, direct booking, OTA)
- Merge automatico duplicati
- Lifetime value calculation
- Cross-property tracking (catene)

#### 2. Segmentation Engine
- Business vs Leisure
- High-value vs Budget
- Repeat vs First-time
- Geographic origin
- Booking channel

#### 3. Automated Campaigns
- Trigger-based (eventi: check-out, compleanno, anniversario)
- Scheduled (newsletter mensile, seasonal offers)
- Personalized (basato su preferenze, storico)

#### 4. Guest Journey Mapping
```
PRE-ARRIVAL
├─ Booking confirmation
├─ Pre-stay email (info hotel, upsells)
└─ Check-in reminder

DURING STAY
├─ Welcome message
├─ Service requests
├─ Upsell opportunities
└─ Daily touchpoints

POST-STAY
├─ Thank you + feedback
├─ Review request
├─ Future booking offers
└─ Loyalty nurture
```

#### 5. Analytics & Insights
- Guest satisfaction trends
- Repeat booking patterns
- Revenue per guest (lifetime)
- Campaign effectiveness
- Channel performance

### ROI del CRM

**Statistiche importanti:**
- +23% repeat bookings con targeted CRM (media settore)
- +31-40% repeat rate con effective post-stay CRM (Deloitte)
- 67% more spending da loyal guests
- 5% retention increase → 95% profit increase

**Fonte:** [Callin.io - CRM in Hotel Industry 2025](https://callin.io/customer-relationship-management-in-hotel-industry/)

---

## PARTE 7: Privacy & Compliance

### GDPR & Data Protection

**Requisiti fondamentali:**

1. **Transparent Privacy Policies**
   - Ospite deve sapere quali dati vengono raccolti
   - Perché vengono raccolti
   - Come vengono usati

2. **Guest Data Rights**
   - Accesso ai propri dati
   - Richiesta modifica
   - Richiesta cancellazione (right to be forgotten)
   - Opt-out comunicazioni marketing

3. **Data Security**
   - Encryption at rest e in transit
   - Access control (staff autorizzato)
   - Audit logs
   - Breach notification procedures

### Consent Management

**Mews Approach:**
Guests possono:
- Gestire i propri dati personali
- Richiedere cancellazione profilo
- Selezionare quali dati condividere con la property

**Best Practice:**
Durante check-in (o pre-arrival), ospite sceglie:
- ✓ Accetto email marketing
- ✓ Accetto SMS/WhatsApp
- ✓ Salva preferenze per soggiorni futuri
- ✓ Condividi dati con partner loyalty programs

### Data Retention Policies

**Bilanciare:**
- Compliance regulations (GDPR: max 7 anni per dati fiscali)
- Business needs (storico guest per CRM)
- Guest wishes (richiesta cancellazione)

**Soluzione comune:**
- Dati fiscali/legali: retention period obbligatorio
- Marketing data: fino a opt-out o inattività (es. 3 anni senza soggiorni)
- Preferenze: fino a richiesta cancellazione

**Fonte:** [Mews - PMS Security](https://www.mews.com/en/security-at-mews)

---

## PARTE 8: Esempi Concreti dai Big Player

### Mews PMS

**Focus:** Guest eco-system
**Innovazione 2025:** "Capire chi è il guest e chi viaggia con loro"
**Significa:** Linking tra profili (famiglia, gruppo)

**Guest Feedback Integration:**
- NPS e satisfaction scores connessi direttamente al PMS
- Review automaticamente pushate nel customer profile notes
- Feedback live nel sistema operativo

**CRM Integration:**
- Connessione con CRM esterni
- Personalizzazione automatica: "camera preferita pronta + minibar personalizzato"

**Link:** [Mews PMS Reviews - HotelTechReport](https://hoteltechreport.com/operations/property-management-systems/mews)

---

### Oracle Opera PMS

**Focus:** Enterprise-grade, customizable
**Punti forti:**
- Guest Status Codes completamente configurabili
- Tracciamento regulatory (tourist-cl1, government-cl1)
- Graphical indicators: VIP, first-time, repeat, loyalty, restricted

**Guest Lifecycle:**
- Accesso immediato a: arriving, departing, staying over
- Communication history completa
- Membership details
- Past stays
- Guest preferences

**Room Status Integration:**
- Clean/Dirty, Inspected, Pick Up, Out of Order/Service

**Link:** [Oracle Opera Cloud PMS](https://www.oracle.com/hospitality/hotel-property-management/hotel-pms-software/)

---

### Cloudbeds

**Focus:** All-in-one platform con CRM nativo
**Punti forti:**
- **Guest Profile Deduplication:** Merge automatico duplicati
- **Unified Inbox:** SMS, email, WhatsApp, Booking.com, Expedia, Airbnb in una vista
- **AI-powered assistant:** Gestisce comunicazioni website, WhatsApp, SMS
- **Cross-property profiles:** Consolida lifetime value attraverso più strutture

**Multichannel Excellence:**
"Manage SMS, email, WhatsApp, Booking.com, Expedia, Airbnb and more in a single view"

**Guest Messaging:**
- Automated messaging basato su reservation data
- Digital registration forms
- Team internal communication

**Link:** [Cloudbeds Platform](https://www.cloudbeds.com/hospitality-platform/)

---

### RoomRaccoon

**Focus:** Small-medium properties, ease of use
**Punti forti:**
- **RaccoonID:** Online check-in, ID verification, keyless entry
- **Corporate Profiles:** Company details, negotiated rates, billing preferences
- **Guest Communication Tools:** Automated + personalized
- **Payment Request Links:** Streamline payments, upsells pre-arrival

**Guest Experience:**
- Contactless check-in/out
- Guest preferences recorded e acted upon
- Instant access to guest data per staff

**Link:** [RoomRaccoon PMS](https://roomraccoon.com/platform/pms)

---

### Protel PMS

**Focus:** European market, 14,000+ hotels
**Punti forti:**
- **Detailed Guest Profiles:** Preferences, history, special requests
- **Reservation History:** All past + future reservations nel profilo
- **Revenue Tracking:** Revenues e statistics stored sia in guest profile che in company/TA/source/group profile

**Workflow:**
- Auto-open guest profile search quando crei reservation
- Data transfer automatico da profile a reservation
- VIP status editabile
- Real-time operations

**Link:** [Protel Hotel PMS](https://www.protel-io.com/hotel-property-management-system)

---

## PARTE 9: Raccomandazioni per Miracollook

### Problema Attuale

**Approccio superficiale identificato:**
- Filtriamo solo ospiti con email
- Non tracciamo guest profiles separati da bookings
- Non gestiamo stati booking
- Comunicazione limitata a email

### Architettura Raccomandata

#### 1. Separare Guest Profile da Booking

**Database Schema suggerito:**

```sql
-- GUEST PROFILE (permanente)
CREATE TABLE guest_profiles (
    id UUID PRIMARY KEY,
    guest_type VARCHAR(10), -- 'GUEST' o 'BOOKER'
    title VARCHAR(10),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255), -- NULLABLE!
    phone VARCHAR(50), -- NULLABLE!
    address TEXT,
    zip_code VARCHAR(20),
    country_code VARCHAR(2),

    -- Preferences
    room_preferences JSONB,
    dietary_needs TEXT,
    special_requests TEXT,
    communication_preference VARCHAR(20), -- 'email', 'sms', 'whatsapp'

    -- Loyalty
    loyalty_status VARCHAR(20), -- 'VIP', 'REGULAR', 'FIRST_TIME'
    vip_notes TEXT,

    -- Compliance
    marketing_consent BOOLEAN DEFAULT FALSE,
    data_sharing_consent BOOLEAN DEFAULT FALSE,

    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_stay_date DATE,
    total_stays INTEGER DEFAULT 0
);

-- BOOKINGS (transazionale)
CREATE TABLE bookings (
    id UUID PRIMARY KEY,
    guest_profile_id UUID REFERENCES guest_profiles(id),

    -- Dates
    arrival_date DATE NOT NULL,
    departure_date DATE NOT NULL,
    booking_date TIMESTAMP DEFAULT NOW(),

    -- Room
    room_number VARCHAR(10),
    room_type VARCHAR(50),

    -- Status
    booking_status VARCHAR(20) NOT NULL,
    -- 'TENTATIVE', 'CONFIRMED', 'CHECKED_IN', 'CHECKED_OUT',
    -- 'CANCELLED', 'NO_SHOW', 'WAITLISTED'

    is_guaranteed BOOLEAN DEFAULT FALSE,
    guarantee_type VARCHAR(20), -- 'CREDIT_CARD', 'DEPOSIT', 'NONE'

    -- Financial
    rate_per_night DECIMAL(10,2),
    total_amount DECIMAL(10,2),

    -- Source
    booking_source VARCHAR(50), -- 'DIRECT', 'BOOKING_COM', 'EXPEDIA', etc

    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    checked_in_at TIMESTAMP,
    checked_out_at TIMESTAMP
);

-- COMMUNICATION LOG
CREATE TABLE communication_log (
    id UUID PRIMARY KEY,
    guest_profile_id UUID REFERENCES guest_profiles(id),
    booking_id UUID REFERENCES bookings(id), -- NULLABLE

    channel VARCHAR(20), -- 'EMAIL', 'SMS', 'WHATSAPP', 'PHONE'
    direction VARCHAR(10), -- 'INBOUND', 'OUTBOUND'
    message_type VARCHAR(50), -- 'BOOKING_CONFIRMATION', 'CHECK_IN_REMINDER', etc

    subject VARCHAR(255),
    content TEXT,

    status VARCHAR(20), -- 'SENT', 'DELIVERED', 'READ', 'FAILED'

    sent_at TIMESTAMP DEFAULT NOW(),
    delivered_at TIMESTAMP,
    read_at TIMESTAMP
);
```

**PERCHÉ:**
- Guest profile persiste nel tempo
- Booking è transazione specifica
- Communication log traccia TUTTA la comunicazione (storico completo)

---

#### 2. Implementare Stati Booking Standard

**Macchina a Stati consigliata:**

```python
from enum import Enum

class BookingStatus(Enum):
    TENTATIVE = "tentative"
    WAITLISTED = "waitlisted"
    CONFIRMED = "confirmed"
    CHECKED_IN = "checked_in"
    CHECKED_OUT = "checked_out"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"

# Transizioni permesse
ALLOWED_TRANSITIONS = {
    BookingStatus.TENTATIVE: [BookingStatus.CONFIRMED, BookingStatus.WAITLISTED, BookingStatus.CANCELLED],
    BookingStatus.WAITLISTED: [BookingStatus.CONFIRMED, BookingStatus.CANCELLED],
    BookingStatus.CONFIRMED: [BookingStatus.CHECKED_IN, BookingStatus.CANCELLED, BookingStatus.NO_SHOW],
    BookingStatus.CHECKED_IN: [BookingStatus.CHECKED_OUT],
    BookingStatus.CHECKED_OUT: [], # stato finale
    BookingStatus.CANCELLED: [], # stato finale
    BookingStatus.NO_SHOW: [], # stato finale
}

def transition_booking_status(booking, new_status):
    """Transizione sicura con validazione"""
    current = booking.status

    if new_status not in ALLOWED_TRANSITIONS.get(current, []):
        raise ValueError(f"Invalid transition: {current} -> {new_status}")

    # Trigger azioni basate su transizione
    if new_status == BookingStatus.CHECKED_OUT:
        trigger_post_stay_communication(booking)

    booking.status = new_status
    booking.save()
```

**Automazioni trigger:**
- `CONFIRMED` → Invia confirmation email
- `CHECKED_IN` → Invia welcome message + upsell offers
- `CHECKED_OUT` → Trigger post-stay workflow
- `NO_SHOW` → Alert staff, addebito no-show fee

---

#### 3. Sistema Multi-Canale

**Implementazione consigliata:**

```python
class CommunicationChannel(Enum):
    EMAIL = "email"
    SMS = "sms"
    WHATSAPP = "whatsapp"
    PHONE = "phone"

def get_preferred_channel(guest_profile, message_type):
    """Smart channel routing"""

    # 1. Verifica preferenza esplicita guest
    if guest_profile.communication_preference:
        return guest_profile.communication_preference

    # 2. Fallback basato su tipo messaggio
    urgent_types = ['CHECK_IN_REMINDER', 'ROOM_READY']
    formal_types = ['BOOKING_CONFIRMATION', 'INVOICE']

    if message_type in urgent_types:
        # Preferisci SMS/WhatsApp per urgenti
        if guest_profile.phone:
            return CommunicationChannel.SMS

    if message_type in formal_types:
        # Email per formali
        if guest_profile.email:
            return CommunicationChannel.EMAIL

    # 3. Fallback a canale disponibile
    if guest_profile.email:
        return CommunicationChannel.EMAIL
    if guest_profile.phone:
        return CommunicationChannel.SMS

    # 4. Nessun canale digitale disponibile
    return CommunicationChannel.PHONE  # Staff deve chiamare

async def send_message(guest_profile, message_type, content):
    """Invio multi-canale intelligente"""

    channel = get_preferred_channel(guest_profile, message_type)

    if channel == CommunicationChannel.EMAIL:
        await send_email(guest_profile.email, content)
    elif channel == CommunicationChannel.SMS:
        await send_sms(guest_profile.phone, content)
    elif channel == CommunicationChannel.WHATSAPP:
        await send_whatsapp(guest_profile.phone, content)
    else:
        # Log per staff follow-up manuale
        log_manual_contact_needed(guest_profile, message_type)

    # Log communication
    save_communication_log(guest_profile, channel, message_type, content)
```

**Vantaggi:**
- Raggiungi TUTTI gli ospiti (non solo quelli con email)
- Usa canale preferito da ospite
- Fallback automatico se canale primario non disponibile
- Storico completo comunicazioni

---

#### 4. Post-Stay Workflow

**Implementazione raccomandata:**

```python
from datetime import datetime, timedelta

def trigger_post_stay_communication(booking):
    """Trigger post-stay sequence automatica"""

    guest = booking.guest_profile
    checkout_date = booking.checked_out_at

    # Schedule comunicazioni
    schedule_communication(
        guest=guest,
        booking=booking,
        message_type='THANK_YOU',
        send_at=checkout_date + timedelta(hours=2)  # 2h dopo checkout
    )

    schedule_communication(
        guest=guest,
        booking=booking,
        message_type='FEEDBACK_REQUEST',
        send_at=checkout_date + timedelta(days=1)  # 24h dopo
    )

    schedule_communication(
        guest=guest,
        booking=booking,
        message_type='REVIEW_REQUEST',
        send_at=checkout_date + timedelta(days=2)  # 48h dopo
    )

    schedule_communication(
        guest=guest,
        booking=booking,
        message_type='FUTURE_BOOKING_OFFER',
        send_at=checkout_date + timedelta(days=7)  # 1 settimana dopo
    )

def process_scheduled_communications():
    """Cron job che gira ogni ora"""

    now = datetime.now()
    pending = CommunicationQueue.objects.filter(
        status='SCHEDULED',
        send_at__lte=now
    )

    for comm in pending:
        # Personalizza contenuto basato su guest profile + booking
        content = personalize_message(
            comm.message_type,
            comm.guest,
            comm.booking
        )

        # Invia via canale appropriato
        send_message(comm.guest, comm.message_type, content)

        # Aggiorna status
        comm.status = 'SENT'
        comm.save()
```

**Personalizzazione esempio:**

```python
def personalize_message(message_type, guest, booking):
    """Personalizza messaggio basato su dati guest + booking"""

    if message_type == 'THANK_YOU':
        return f"""
        Caro/a {guest.first_name},

        Grazie per aver soggiornato con noi dal {booking.arrival_date} al {booking.departure_date}.
        Speriamo che tu abbia apprezzato la tua camera {booking.room_number}.

        {"Siamo felici di rivederti!" if guest.total_stays > 1 else "Speriamo di rivederti presto!"}

        Il Team {hotel_name}
        """

    elif message_type == 'REVIEW_REQUEST':
        # Segmenta basato su loyalty
        if guest.loyalty_status == 'VIP':
            return generate_vip_review_request(guest, booking)
        else:
            return generate_standard_review_request(guest, booking)

    # ... altri message_type
```

---

#### 5. Dashboard Miracollook - Vista Consigliata

**Invece di filtrare per email, mostra:**

```
┌─────────────────────────────────────────────────────┐
│ GUESTS - All Current & Upcoming                     │
├─────────────────────────────────────────────────────┤
│                                                      │
│ Filters:                                             │
│ [Status: All ▼] [Contact: All ▼] [VIP: All ▼]      │
│                                                      │
│ Guest Name        | Status      | Contact  | Room   │
│ ─────────────────────────────────────────────────── │
│ 👤 Mario Rossi    | IN-HOUSE    | 📧 📱    | 201   │
│ 👥 Rossi Family   |             |          |       │
│   ├─ Anna Rossi   | IN-HOUSE    | ❌ 📱    | 201   │
│   └─ Luca Rossi   | IN-HOUSE    | ❌ ❌    | 201   │
│                                                      │
│ 👤 John Smith     | CONFIRMED   | 📧 📱    | 305   │
│   (Booker)        | (arr: +2d)  |          |       │
│                                                      │
│ 👤 Laura Bianchi  | CHECKED-OUT | 📧 ❌    | 102   │
│   (VIP)           | (3d ago)    |          |       │
│                                                      │
│ 👤 Marco Verdi    | CONFIRMED   | ❌ 📱    | 210   │
│   ⚠️ NO EMAIL     | (arr: +1d)  | SMS only |       │
└─────────────────────────────────────────────────────┘

Legenda:
📧 = Email available
📱 = Phone available
❌ = Not available
👥 = Multiple guests in booking (family/group)
⚠️ = Attenzione (no email, VIP, etc)
```

**Cosa cambia:**
- Vediamo TUTTI gli ospiti (anche senza email)
- Chiaro quali canali disponibili per ogni ospite
- Indicazione famiglie/gruppi
- Warning visivi per edge cases

**Click su guest → Profile view:**

```
┌─────────────────────────────────────────────────────┐
│ GUEST PROFILE: Mario Rossi                          │
├─────────────────────────────────────────────────────┤
│                                                      │
│ CONTACT INFO                                         │
│ Email: mario.rossi@example.com                      │
│ Phone: +39 333 1234567                              │
│ Address: Via Roma 10, Milano                        │
│                                                      │
│ PREFERENCES                                          │
│ Room: High floor, quiet, no smoking                 │
│ Pillow: Soft                                        │
│ Dietary: Vegetarian                                 │
│                                                      │
│ LOYALTY                                              │
│ Status: Regular (3 total stays)                     │
│ Last stay: 3 months ago                             │
│                                                      │
│ CURRENT BOOKING                                      │
│ Status: IN-HOUSE                                     │
│ Room: 201 (Deluxe Double)                           │
│ Dates: 27 Jan - 30 Jan 2026                         │
│                                                      │
│ PAST BOOKINGS (2)                                    │
│ • Oct 2025 - Room 305 - 3 nights                    │
│ • Jul 2025 - Room 201 - 2 nights                    │
│                                                      │
│ COMMUNICATION HISTORY                                │
│ [Timeline view di tutte le comunicazioni]           │
│                                                      │
│ ACTIONS                                              │
│ [Send Message] [Add Note] [Mark VIP] [Edit Profile] │
└─────────────────────────────────────────────────────┘
```

---

### Quick Wins Implementabili Subito

**Fase 1 (Settimana 1):**
1. ✅ Aggiungere `guest_profiles` table separata da `bookings`
2. ✅ Aggiungere campo `booking_status` con enum
3. ✅ Modificare UI per mostrare TUTTI gli ospiti (non solo con email)

**Fase 2 (Settimana 2-3):**
4. ✅ Implementare `communication_log` table
5. ✅ Aggiungere campo `phone` a guest profiles
6. ✅ Supporto SMS basic (via Twilio o simile)

**Fase 3 (Settimana 4+):**
7. ✅ Post-stay workflow automatico
8. ✅ Smart channel routing
9. ✅ WhatsApp integration
10. ✅ Guest preferences tracking

---

## PARTE 10: Considerazioni Implementazione

### Migrazione Dati Esistenti

**Se avete già dati:**

```sql
-- Step 1: Crea guest_profiles da booking esistenti
INSERT INTO guest_profiles (id, email, first_name, last_name, ...)
SELECT
    gen_random_uuid(),
    email,
    first_name,
    last_name,
    ...
FROM bookings
WHERE email IS NOT NULL
GROUP BY email; -- Un profile per email unica

-- Step 2: Link bookings a guest_profiles
UPDATE bookings b
SET guest_profile_id = (
    SELECT id FROM guest_profiles gp
    WHERE gp.email = b.email
    LIMIT 1
);

-- Step 3: Gestisci bookings SENZA email
-- Opzione A: Un profile per ogni booking senza email
-- Opzione B: Merge manuale successivo basato su nome/phone
```

### Performance Considerations

**Indicizzazione critica:**

```sql
-- Guest profiles
CREATE INDEX idx_guest_profiles_email ON guest_profiles(email);
CREATE INDEX idx_guest_profiles_phone ON guest_profiles(phone);
CREATE INDEX idx_guest_profiles_loyalty ON guest_profiles(loyalty_status);
CREATE INDEX idx_guest_profiles_last_stay ON guest_profiles(last_stay_date);

-- Bookings
CREATE INDEX idx_bookings_guest_profile ON bookings(guest_profile_id);
CREATE INDEX idx_bookings_status ON bookings(booking_status);
CREATE INDEX idx_bookings_dates ON bookings(arrival_date, departure_date);
CREATE INDEX idx_bookings_arrival ON bookings(arrival_date);

-- Communication log
CREATE INDEX idx_comm_log_guest ON communication_log(guest_profile_id);
CREATE INDEX idx_comm_log_booking ON communication_log(booking_id);
CREATE INDEX idx_comm_log_sent_at ON communication_log(sent_at);
```

**Query comuni ottimizzate:**

```sql
-- Current in-house guests
SELECT gp.*, b.*
FROM guest_profiles gp
JOIN bookings b ON b.guest_profile_id = gp.id
WHERE b.booking_status = 'CHECKED_IN';

-- Upcoming arrivals (next 7 days)
SELECT gp.*, b.*
FROM guest_profiles gp
JOIN bookings b ON b.guest_profile_id = gp.id
WHERE b.booking_status = 'CONFIRMED'
  AND b.arrival_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '7 days'
ORDER BY b.arrival_date;

-- VIP guests history
SELECT gp.*, COUNT(b.id) as total_bookings, SUM(b.total_amount) as lifetime_value
FROM guest_profiles gp
LEFT JOIN bookings b ON b.guest_profile_id = gp.id
WHERE gp.loyalty_status = 'VIP'
GROUP BY gp.id;
```

### Testing Checklist

**Test essenziali:**

- [ ] Guest profile creation (con e senza email)
- [ ] Booking status transitions (tutte le transizioni permesse)
- [ ] Booking status validazione (transizioni NON permesse devono fallire)
- [ ] Multi-channel message routing (email, SMS, fallback)
- [ ] Post-stay workflow trigger (dopo checkout)
- [ ] Communication log storage (tutte le comunicazioni loggato)
- [ ] Guest profile merge (duplicati)
- [ ] GDPR compliance (data access, deletion requests)
- [ ] Performance con 1000+ guest profiles
- [ ] Concurrent bookings stesso guest

---

## Conclusioni Finali

### Cosa Abbiamo Imparato

**1. GUEST PROFILE ≠ BOOKING**
È l'architettura fondamentale. Separare chi è l'ospite (permanente) da quando viene (transazionale).

**2. TRACCIARE TUTTI, NON SOLO CHI HA EMAIL**
I PMS professionali non filtrano. Email è solo un campo opzionale. Altri canali esistono (SMS, WhatsApp, phone).

**3. STATI BOOKING STANDARD SONO UNIVERSALI**
Tentative → Confirmed → Checked-In → Checked-Out → Post-Stay
Con varianti: Cancelled, No-Show, Waitlisted

**4. POST-STAY È DOVE SI CREA LOYALTY**
+31-40% repeat bookings con effective post-stay CRM (Deloitte).
La maggior parte degli hotel lo trascura = opportunità.

**5. MULTI-CANALE È STANDARD, NON OPZIONALE**
70% viaggiatori preferisce canali digitali. Email da sola non basta.
Smart routing: right message, right time, right channel.

### Prossimi Step Consigliati per Miracollook

**PRIORITÀ ALTA (Subito):**
1. Separare `guest_profiles` da `bookings` nel database
2. Implementare `booking_status` enum con stati standard
3. Mostrare TUTTI gli ospiti in UI (non solo con email)
4. Aggiungere flag visivi per canali disponibili (email, phone)

**PRIORITÀ MEDIA (Prossime settimane):**
5. Implementare `communication_log` per storico completo
6. Aggiungere supporto SMS basic
7. Post-stay workflow automatico (thank you + review request)
8. Guest preferences tracking

**PRIORITÀ BASSA (Future enhancement):**
9. WhatsApp integration
10. Advanced segmentation (business vs leisure)
11. Predictive analytics (lifetime value, churn risk)
12. Multi-property guest profiles (se Miracollook scala a catene)

### Risorse per Approfondimento

**Documentazione Ufficiale:**
- [Oracle Opera PMS Documentation](https://docs.oracle.com/cd/E53533_01/opera_5_05_00_core_help/welcome_to_pms.htm)
- [Mews API Documentation](https://mews.com/en)
- [Cloudbeds Developer Portal](https://www.cloudbeds.com/)

**Guide Settore:**
- [AltexSoft - Complete Hotel PMS Guide](https://www.altexsoft.com/blog/hotel-property-management-systems-products-and-features/)
- [Hotel Tech Report - PMS Buyer's Guide](https://hoteltechreport.com/operations/property-management-systems)

**Best Practices:**
- [Chekin - Hotel Guest Communication Guide](https://chekin.com/en/blog/hotel-guest-communication/)
- [Cloudbeds - Guest Messaging Best Practices](https://www.cloudbeds.com/hotel-guest/messaging/)

---

## Fonti Complete

**PMS Vendor Documentation:**
- [Mews PMS Reviews - HotelTechReport](https://hoteltechreport.com/operations/property-management-systems/mews)
- [Oracle Opera Cloud PMS](https://www.oracle.com/hospitality/hotel-property-management/hotel-pms-software/)
- [Oracle Opera - Configuring Guest Status](https://docs.oracle.com/en/industries/hospitality/opera-cloud/21.5/ocsuh/t_admin_booking_configuring_guest_status.htm)
- [Cloudbeds Platform](https://www.cloudbeds.com/hospitality-platform/)
- [Cloudbeds - Check-in and Check-out Guide](https://myfrontdesk.cloudbeds.com/hc/en-us/articles/221677468-Check-in-and-check-out-guests-in-Cloudbeds-PMS)
- [RoomRaccoon PMS](https://roomraccoon.com/platform/pms)
- [Protel Hotel PMS](https://www.protel-io.com/hotel-property-management-system)
- [Protel - Guest Profile Documentation](https://connect.protel.net/files/source/pairexthelp/en_US/gast-gaestekartei.htm)

**Industry Guides & Best Practices:**
- [AltexSoft - Hotel PMS Complete Guide](https://www.altexsoft.com/blog/hotel-property-management-systems-products-and-features/)
- [Redgate - Data Model for Hotel Management System](https://www.red-gate.com/blog/data-model-for-hotel-management-system)
- [Redgate - Hotel Room Booking System Data Model](https://www.red-gate.com/blog/designing-a-data-model-for-a-hotel-room-booking-system)
- [RoomMaster - Hotel Guest Profile Basics](https://www.roommaster.com/blog/hotel-guest-profile)

**Guest Communication:**
- [Chekin - Hotel Guest Communication Guide](https://chekin.com/en/blog/hotel-guest-communication/)
- [Cloudbeds - Guest Messaging Best Practices](https://www.cloudbeds.com/hotel-guest/messaging/)
- [INTELITY - Unified Guest Messaging](https://intelity.com/blog/unified-guest-messaging-for-hotels-why-sms-and-whatsapp-must-live-in-one-platform/)
- [Touchstay - Hotel Communication Ultimate Guide](https://touchstay.com/blog/hotel-communication)

**Post-Stay & CRM:**
- [Digital Guest - Post-Stay Email Templates](https://digitalguest.com/post-stay-email-templates/)
- [Typsy - CRM Transform Guest Experience](https://blog.typsy.com/from-check-in-to-loyalty-how-crm-can-transform-hotel-guest-experience)
- [SiteMinder - Hotel CRM Complete Guide](https://www.siteminder.com/r/customer-relationship-management/)
- [Callin.io - CRM in Hotel Industry 2025](https://callin.io/customer-relationship-management-in-hotel-industry/)

**Reservation Status Standards:**
- [SetupMyHotel - Reservation Status Sample](https://setupmyhotel.com/hotel-formats/front-office-formats/reservation-status-sample-for-hotels-and-resorts/)
- [SetupMyHotel - Releasing Tentative Bookings SOP](https://setupmyhotel.com/hotel-sop-standard-operating-procedures/front-office-sop/sop-reservations-releasing-tentative-and-non-guaranteed-bookings/)

**Privacy & Compliance:**
- [Mews - PMS Security](https://www.mews.com/en/security-at-mews)

---

**Fine Studio**

*Ricerca completata: 29 Gennaio 2026*
*Cervella Researcher - CervellaSwarm* 🔬
