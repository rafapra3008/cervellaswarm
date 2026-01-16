# STUDIO CLOUDBEDS - Room Manager & Housekeeping

**Data**: 14 Gennaio 2026
**Progetto**: Miracollo - Room Manager
**Ricercatrice**: Cervella Researcher
**Contesto**: Studio big player PMS per best practices housekeeping

---

## EXECUTIVE SUMMARY

Cloudbeds è un **PMS cloud-based leader per SMB** (piccoli-medi hotel, B&B, vacation rentals) con presenza in 150+ paesi. La piattaforma combina PMS tradizionale con housekeeping management, channel manager, booking engine e marketplace di 400+ integrazioni.

**Target principale**: Hotel indipendenti 10-50 camere, B&B, ostelli, vacation rentals.

**Punto di forza**: Approccio "all-in-one" con pricing accessibile basato su numero camere, forte focus su mobile-first e facilità d'uso per staff con poco training.

---

## 1. ROOM STATUS & HOUSEKEEPING WORKFLOW

### 1.1 Stati Camera (Room Status)

Cloudbeds traccia **DUE livelli di stato**:

#### A) Front Desk Status
- **Check-in** - Riservata per arrivo oggi
- **Check-out** - Partenza oggi
- **Stayover** - Ospite in-house che resta
- **Turnover** - Check-out + Check-in stesso giorno
- **Not reserved** - Camera libera

#### B) Housekeeping Condition
- **Dirty** - Occupata, in manutenzione, o non pronta
- **Clean** - Pulita ma in attesa ispezione
- **Inspected** - Pulita + ispezionata = pronta ospiti

**NOTA IMPORTANTE**:
> "Housekeeping status (Clean, Dirty, Inspected) does NOT impact room availability in inventory. Rooms marked as Dirty remain bookable unless placed Out of Service or blocked."

Questo è un design choice preciso: separano inventory management da housekeeping workflow.

### 1.2 Inspection Table & Workflow

La vista principale housekeeping è una **tabella filtrable** con:
- Elenco camere con status attuale
- Assegnazione housekeeper (drag-and-drop o selezione)
- Filtri per organizzare workload giornaliero
- Bulk actions per aggiornamenti multipli

**Workflow tipico**:
```
1. Camera Dirty → Assegna housekeeper
2. Housekeeper pulisce → Marca Clean (da mobile)
3. Supervisor ispeziona → Marca Inspected
4. Camera pronta per nuovo ospite
```

### 1.3 Bulk Actions

Feature chiave per efficienza:
- Seleziona camere multiple (checkbox)
- Assegna a housekeeper in batch
- Update status multipli simultaneamente

**Pattern**: Usano filtri smart per ridurre click. Es: "Show only dirty rooms for today's departures" → assign all → done.

### 1.4 Limitazioni Note

Da recensioni utenti:
- **NO advance planning**: Puoi vedere solo oggi e domani, non settimana/mese ahead
- **NO calendar housekeeping view**: L'inspection symbol appare sul calendario ma non puoi gestire da lì
- Focus su operatività giornaliera, meno su pianificazione

---

## 2. MOBILE APP & REAL-TIME UPDATES

### 2.1 Cloudbeds Mobile App

Disponibile iOS + Android, **mobile-first approach** per housekeeping:

**Features housekeeping**:
- View room status in tempo reale
- Update room condition (Dirty → Clean)
- Assign housekeepers
- Accesso note camera e reservation notes

**Altre features app**:
- Dashboard con occupancy rate real-time
- Arrivals/departures oggi e domani
- Quick-search guest e reservations
- Room assignments
- Check-in/check-out mobile

### 2.2 Dashboard Real-Time

Il dashboard (desktop + mobile) mostra:
- **Occupancy rate meter** in tempo reale
- Activity riservazioni oggi + domani
- Design pulito, compatibile tutti gli schermi
- Performance migliorata vs vecchia versione

**User feedback**:
> "The user interface is modern, clean and easy to navigate; this makes it quite easy to learn the software and/or teach it to others."

### 2.3 Calendar View (Beta)

Recent addition alla mobile app:
- Vista calendario tutte le reservations
- Tap su reservation block → dettagli
- Ancora in beta testing (aggiunta dopo feedback utenti)

**Nota**: Inizialmente l'app NON aveva calendar view e utenti lo consideravano "unacceptable for hospitality app" → Cloudbeds ha ascoltato e aggiunto feature.

---

## 3. INTEGRAZIONI ACCESSI & SMART BUILDING

### 3.1 Door Locks - Partner Hardware

Cloudbeds Marketplace include **sezione dedicata "Access Management and Door Locks"** con multipli partner:

#### Partner Principali:

**DwarPaal**
- Smart locks: D1, T1, N10
- Tech: Fingerprint, mobile app, RFID, offline keycodes, chiavi fisiche
- WiFi Smart Gateway per controllo centralizzato remoto
- **Automazione IoT**: Sync lighting + temperature con occupancy/time

**Lynx**
- Digital mobile keys per smart locks
- Guest access codes auto-generati
- Real-time alerts per check-in/out status
- Automation per locks, intercom, noise monitors, thermostats

**Operto + Yale Doorman**
- Access codes automatici generati da Cloudbeds
- Integrazione HVAC: auto-control temperatura per check-in

**Jervis Systems**
- Dashboard unificato per: smart locks, garage doors, thermostats, lights, switches, pool heaters
- Approccio "all IoT devices in one place"

**Hostkit**
- Contactless check-in workflow
- Mobile door access

### 3.2 HVAC / Energy Management

**Approach**: Cloudbeds non sviluppa hardware, ma integra con leader di mercato:

**Marketplace include categorie**:
- Energy Management Systems
- Smart Building Automation
- IoT Device Management

**Partner citati** (da ricerca generale settore):
- **Verdant** (#2 ranked EMS): Smart thermostats con occupancy sensors, riduzione consumo camere unoccupied
- **Telkonet**: Cloud-based Rhapsody EMS, integra via BACnet, tracking room-by-room, real-time alerts

**Pattern di integrazione**:
1. Cloudbeds via API comunica occupancy + reservation status
2. Partner EMS riceve eventi (check-in, check-out, no-show)
3. Sistema HVAC adatta temperatura automaticamente
4. Report energia aggregati tornano in Cloudbeds dashboard (via integrazione)

### 3.3 Architettura Integrazioni

**Cloudbeds Marketplace** = 400+ partner apps:
- Categorie: PMS, Channel Manager, Booking Engine, Access Control, Energy, Payments, etc.
- Pattern: "Best of breed" approach - Cloudbeds fa PMS core, partner specializzati per verticali

**Benefit per hotel**:
- Pick and choose cosa serve
- Cloudbeds garantisce compatibilità API
- Setup guidato per ogni integrazione

---

## 4. ACTIVITY LOG / AUDIT TRAIL

### 4.1 Sistema di Logging

Cloudbeds traccia **tutte le azioni** con Activity Log accessibile da:
```
Account Menu → Logs → Activity Log
```

**Filtrabile per**:
- Tipo di modifica (es: "ROOM TYPE MODIFIED")
- User che ha fatto azione
- Date range
- Specifica entità (camera, reservation, etc.)

### 4.2 Night Audit Trail

**Tutte le Night Audit actions** vengono loggate con:
- Metodo esecuzione (automatico vs manuale)
- Data e ora
- User information

**Purpose**: Trasparenza e accountability per operazioni critiche.

### 4.3 Report Housekeeping

Cloudbeds offre **7 categorie report**:
1. Financial
2. Guests
3. Reservations
4. Occupancy
5. Payment
6. Invoices
7. **Housekeeping** ← include room-level info

**Report Housekeeping include**:
- Front desk status
- Room conditions
- Accommodation comments
- Housekeeper assignments

**Export options**: PDF, Excel, Print (per condividere con staff)

### 4.4 Analytics & Insights

**Useful reports for operations**:
- Rooms Sold/Occupancy Report
- Night Audit Reports (13 report types consigliati per ogni notte)
- Custom reports via Cloudbeds Insights API

**Pattern**: Cloudbeds push forte su data-driven decisions con report pre-built + custom via API.

---

## 5. UI/UX & DESIGN PHILOSOPHY

### 5.1 Design Principles

**Mobile-first, Cloud-native**:
- App nativa iOS/Android
- Responsive design per tutti gli schermi
- Performance ottimizzata (nuovo dashboard più veloce)

**Clean & Modern**:
> "The user interface is modern, clean and easy to navigate"

**Ease of Learning**:
> "As someone who helps train new front desk staff, the Cloudbeds system is intuitive and user-friendly, enabling new team members to get up to speed fast."

### 5.2 User Feedback - Pros

Da recensioni verificate (4.5/5 rating medio):

✅ **Facilità d'uso**: "Intuitive and easy-to-use, with everything in one place"
✅ **Staff training**: "Simple UI, important from staff training perspective"
✅ **Fewer clicks**: "Get more done with fewer clicks"
✅ **All-in-one**: "Manage reservations, channels, inventory, finances from one platform"
✅ **Staff favorite**: "Compared to previous PMS, Cloudbeds has been the favorite amongst staff"

### 5.3 User Feedback - Cons

⚠️ **Learning curve per feature avanzate**: "Extensive functionalities can present steep learning curve, requiring significant training time"
⚠️ **Alcuni workflow non intuitivi**: Alcuni utenti riportano checkout page "not user-friendly" e UI "not intuitive" per certi flussi
⚠️ **Housekeeping planning limitato**: No advance planning oltre oggi/domani

### 5.4 UX Philosophy (da Cloudbeds stesso)

Cloudbeds ha pubblicato whitepaper **"PMS UX Report - How UX Empowers Hotel Staff"**:
- Focus su ridurre clicks e friction
- Design per utenti NON tech-savvy
- Mobile accessibility come priorità
- Continuous improvement basato su feedback

**Pattern**: Ascolto attivo users → iteration rapide (es: calendar view aggiunta dopo richieste)

---

## 6. API & DEVELOPER ECOSYSTEM

### 6.1 Cloudbeds API Overview

**Developer Hub**: https://developers.cloudbeds.com

**API Coverage**:
- **50+ endpoints** covering core operations
- Hotel details, guests, rooms, reservations, payments
- Multiple API versions: v1.2, v1.3, GraphQL
- Specialized APIs: Insights API, Accounting API, Fiscal Document API, Group Profile API

### 6.2 Authentication & Security

**Metodi supportati**:
- **API Keys** - Per technology partners
- **OAuth 2.0** - Standard modern auth
- **Bearer tokens** - HTTP bearer scheme
- **JWT** - JSON Web Token format

**Pattern**: Flessibilità per diversi use cases (server-to-server vs user authorization)

### 6.3 Webhooks

**Support attivo**:
- Create, delete, retrieve webhooks
- Payload delivery per eventi real-time
- Webhook migration guides tra versioni API

**Note**: Rate limits non esplicitamente documentati pubblicamente (info probabilmente in developer docs post-signup)

### 6.4 Documentation Quality

**Comprehensive coverage**:
- 20+ implementation guides per use case (booking engines, POS, RMS, channel managers, etc.)
- API reference con endpoint specs
- Changelog per deprecations e updates
- FAQ sections
- Integration examples e code samples
- Migration guides per API version transitions

**Developer Support**:
- Email: integrations@cloudbeds.com
- Partner launch checklists
- Regular changelog updates

### 6.5 Marketplace Integration Process

**Path to marketplace**:
1. Complete "Become a Partner" form
2. **Limited Release phase** (requires 5 properties minimum)
3. App non visibile in marketplace durante LR
4. Post-validation → Public marketplace listing

**Goal**: Quality control prima di esporre app a tutti i clienti.

### 6.6 Use Cases API (from docs)

Cloudbeds API permette di:
- Extend PMS functionality
- Create advanced features
- Seamlessly integrate own products
- Make products available on Marketplace

**Pattern**: API-first approach per ecosystem growth, non solo internal use.

---

## 7. PRICING & TARGET MARKET

### 7.1 Pricing Tiers

Cloudbeds offre **4 piani** con pricing basato su **numero camere**:

#### **1. Cloudbeds Flex** - $108/mese (base)
- **Target**: Piccole properties che vogliono flessibilità
- **Include**:
  - Core PMS
  - Multi-property management
  - Integrated payments
  - Access to Marketplace
- **Approccio**: Pick apps independently, pay for what you use

#### **2. Cloudbeds One** - Prezzo custom
- **Target**: Hotel indipendenti, ostelli
- **Include**: Flex +
  - Channel Manager
  - Booking Engine
  - Google Free Booking Links
- **Approccio**: Unified solution per reservations e direct bookings

#### **3. Cloudbeds Experience** - Prezzo custom
- **Target**: Growing hotels focus su guest experience
- **Include**: One +
  - Guest messaging
  - Mobile check-in
  - Reputation management
- **Approccio**: Improve guest communication attraverso stay

#### **4. Cloudbeds Enterprise** - Prezzo custom
- **Target**: Hotel groups e brand multi-property
- **Include**: Fully customizable suite
- **Approccio**: Tailored solutions per catene

### 7.2 Housekeeping in Pricing

**IMPORTANTE**: Housekeeping module è **incluso in tutti i piani**, anche Flex base.

Non è un add-on premium → filosofia "core functionality, not optional extra"

### 7.3 Target Market

**Primary**: Small to Medium Business (SMB)
- Hotel indipendenti 10-50 camere
- B&B e boutique properties
- Ostelli
- Vacation rentals
- Alternative accommodations

**Geografia**: 150+ paesi worldwide

**Positioning**:
> "Ideal for small to medium-sized hotels, increasing productivity while reducing operational errors"

> "Pricing structure based on number of rooms is lauded for affordability and scalability, making it accessible to hotels of all sizes"

### 7.4 Ease of Onboarding

**Key selling point**: Fast setup, minimal training

**From reviews**:
- "Easy to learn and teach to others"
- "New team members get up to speed fast"
- "Intuitive for both beginners and experienced users"

**Pattern**: Cloudbeds compete su TIME TO VALUE, non feature overload.

---

## 8. MAINTENANCE & WORK ORDERS

### 8.1 Sistema Manutenzione

Cloudbeds include **maintenance management** integrato:

**Features**:
- **Maintenance Work Order List** - Traccia riparazioni attive
- **Out-of-Service room notes** - Documentation per camere non disponibili
- Real-time visibility via mobile

### 8.2 Ticketing System (Cloudbeds GX Tickets)

**Purpose**: Track requests, tasks, issues per guest services e property management

**Capabilities**:
- Create new tasks, access existing
- Manage open, scheduled, complete tickets
- Configure escalation rules con notifications
- Assign departments per ticket types

**Workflow**:
```
Guest request/issue → Ticket creato →
Assigned to department → Tracked →
Escalation se needed → Resolved → Logged
```

### 8.3 Room Status & Maintenance

**Integration con housekeeping**:
- Camera può essere marcata "Dirty" se under maintenance
- Per bloccare inventory: mark **Out of Service** (separato da Dirty)
- Maintenance notes visibili a front desk + housekeeping team

### 8.4 Third-Party Integrations

**CleanMeNext** (Marketplace partner):
- Real-time info a staff e management
- Room occupancy, cleanliness, **maintenance issues**, guest requests
- Comunicazione bidirezionale

**Instio** e altri task management tools:
- Track work orders
- Assign tecnici
- Timeline completion

**Pattern**: Core maintenance in Cloudbeds, integrations per workflow avanzati (preventive maintenance, asset tracking, etc.)

---

## 9. COSA POSSIAMO IMPARARE PER MIRACOLLO

### 9.1 ✅ BEST PRACTICES DA ADOTTARE

#### A) Separazione Stati
**Cloudbeds pattern**: Front Desk Status ≠ Housekeeping Condition

**Applicazione Miracollo**:
- **Availability** (bookable vs blocked) è SEPARATO da
- **Cleanliness** (dirty/clean/inspected)
- Camera dirty può rimanere bookable (hotel decide policy)

**Benefit**: Flessibilità per hotel con policy diverse.

#### B) Bulk Actions & Filtri Smart
**Cloudbeds pattern**: Filtri + selezione multipla + bulk assign

**Applicazione Miracollo**:
- Implementare filtri pre-built ("Today's departures", "Dirty rooms", etc.)
- Checkbox per selezione multipla
- Actions: Assign, Update status, Add note, etc.

**Benefit**: Riduce DRASTICAMENTE clicks per operatività quotidiana.

#### C) Mobile-First per Housekeeping
**Cloudbeds pattern**: App nativa con focus su housekeeper workflow

**Applicazione Miracollo**:
- PWA o app nativa per housekeepers
- Focus su: View assigned rooms, Update status, Report issues
- Sync real-time con dashboard manager

**Benefit**: Housekeepers lavorano in movimento, non alla scrivania.

#### D) Activity Log Completo
**Cloudbeds pattern**: Log TUTTO con filtri granulari

**Applicazione Miracollo**:
- Log ogni cambio status con user + timestamp
- Filterabile per camera, user, tipo azione, date range
- Export per audit esterni

**Benefit**: Accountability, debugging, compliance.

#### E) Approccio "All-in-One" ma Modulare
**Cloudbeds pattern**: Core functionality inclusa, ma estendibile via Marketplace

**Applicazione Miracollo**:
- Room Manager core con stati, assignments, log
- Integrazione FACILE con VDA hardware (Etheos, Dingz, etc.)
- API-first per future integrazioni (POS, energy, etc.)

**Benefit**: Start simple, grow complex quando hotel è pronto.

### 9.2 ⚠️ EVITARE QUESTI LIMITI

#### A) NO Advance Planning
**Cloudbeds limit**: Solo oggi/domani visible, no week/month view

**Miracollo improvement**:
- Vista calendario estesa (settimana, mese)
- Pianificazione pulizie preventive
- Forecast workload basato su reservations

**Why**: Seasonal properties (Naturae Lodge) hanno bisogno pianificazione >2 giorni.

#### B) Housekeeping Separato da Calendar
**Cloudbeds limit**: Inspection symbol su calendar, ma gestione solo da pagina dedicated

**Miracollo improvement**:
- Grid view con calendar + housekeeping status overlay
- Drag-and-drop assignments direttamente su timeline
- Visual immediato: "Questa settimana 20 check-out venerdì → pianifica staff"

**Why**: Manager hanno bisogno vista integrata, non context switch tra schermate.

#### C) Integrazioni Hardware via Marketplace Only
**Cloudbeds approach**: Partner integrations, non direct hardware control

**Miracollo improvement**:
- Integrazioni hardware DIRETTE (VDA Etheos, Dingz, etc.)
- Control panel per device settings
- Automation rules visibili e editabili da UI

**Why**: Remote properties need MORE control, not less.

### 9.3 🎯 DIFFERENZIATORI MIRACOLLO

Cose che Cloudbeds NON fa (e noi possiamo fare meglio):

#### 1. Remote First Architecture
- Cloudbeds assume connectivity stabile
- Miracollo: Offline-first, sync when possible
- Critical per locations remote come Naturae Lodge

#### 2. Deep Hardware Integration
- Cloudbeds: Software focus, hardware via partners
- Miracollo: Direct hardware control (locks, HVAC, energy)
- Single source of truth per room state (physical + digital)

#### 3. Sustainability Focus
- Cloudbeds: Energy management via partner apps (Verdant, Telkonet)
- Miracollo: Native sustainability tracking, reporting, guest communication
- Naturae Lodge case study: "Energia risparmiata in tua assenza" messaging

#### 4. Multi-Property con Context Switching
- Cloudbeds: Multi-property support generico
- Miracollo: Context intelligente basato su location type
  - Retreat center → focus wellness activities
  - Hotel urbano → focus speed check-in
  - Lodge eco → focus sustainability

#### 5. Guest Experience Integration
- Cloudbeds: Guest messaging come add-on
- Miracollo: Guest experience EMBEDDED in room status
  - Es: "Camera pronta early per ospite VIP" → notifica automatica
  - Es: "Richiesta pulizia eco" → housekeeping usa prodotti green

### 9.4 📊 COMPETITOR POSITIONING

| Feature | Cloudbeds | Miracollo (Target) |
|---------|-----------|-------------------|
| **Target Market** | SMB 10-50 camere, global | Eco-lodges, remote, sustainability-focused |
| **Pricing** | $108+ based on rooms | TBD - Value-based per property type |
| **Housekeeping** | Basic + mobile | Advanced + hardware-aware |
| **Hardware** | Via marketplace partners | Direct integration core |
| **Offline** | Cloud-dependent | Offline-first architecture |
| **Sustainability** | Partner integrations | Native feature |
| **Planning** | Today/tomorrow only | Week/month forecast |
| **Calendar** | Separate from housekeeping | Integrated grid view |
| **Guest Experience** | Add-on module | Embedded core |
| **API** | 50+ endpoints, mature | Will build focused on hardware + automation |

### 9.5 🎓 LESSON LEARNED: PRICING PHILOSOPHY

**Cloudbeds approach**:
- Housekeeping INCLUDED in base tier ($108/month)
- Not a premium add-on
- Philosophy: "This is CORE, not optional"

**Miracollo takeaway**:
- Room Manager deve essere CORE offering
- Hardware integrations = differentiator, not paywall
- Premium tiers per: multi-property, analytics avanzati, white-label, non per basic functionality

**Why**: Build trust con small properties. Monetize su value-adds, not essentials.

---

## 10. CONCLUSIONI & RACCOMANDAZIONI

### 10.1 Punti di Forza Cloudbeds

1. **Ease of Use** - UI pulita, onboarding veloce, staff training minimal
2. **Mobile-First** - App solida per housekeepers in movimento
3. **All-in-One** - PMS + housekeeping + channel manager + marketplace
4. **API Mature** - 50+ endpoints, docs complete, active developer ecosystem
5. **Pricing Accessibility** - $108/month entry point, scalabile
6. **Bulk Actions** - Riduzione drastica clicks per operatività quotidiana
7. **Activity Logging** - Audit trail completo, accountability built-in
8. **Marketplace Ecosystem** - 400+ partners per estensibilità

### 10.2 Gap da Exploitare (Miracollo Opportunities)

1. **Advance Planning** - Settimana/mese view, forecast workload
2. **Hardware Integration** - Direct control locks/HVAC, non solo via partners
3. **Offline Capability** - Remote locations con connectivity intermittente
4. **Integrated Calendar** - Housekeeping + reservations in single view
5. **Sustainability Native** - Energy tracking, eco messaging embedded
6. **Guest Experience** - Room status tied to guest preferences, non solo operations

### 10.3 Next Steps per Miracollo

**IMMEDIATE** (MVP Room Manager):
1. Implementare stati separati (Availability vs Cleanliness)
2. Bulk actions + filtri smart
3. Activity log completo
4. Mobile-friendly interface (PWA)

**SHORT-TERM** (Post-MVP):
1. Calendar integrato con housekeeping overlay
2. Planning view settimana/mese
3. Integrazioni hardware VDA (Etheos priorità)
4. Offline-first architecture

**LONG-TERM** (Differentiation):
1. Sustainability dashboard native
2. Guest experience automation
3. Multi-property con context switching intelligente
4. API ecosystem per partners eco-tech

### 10.4 Decisione Architetturale: Build vs Integrate

**Cloudbeds model**: Build PMS core, integrate tutto il resto (hardware, energy, etc.)

**Miracollo recommendation**: **Hybrid approach**
- Build: Room status, housekeeping workflow, planning
- Direct integrate: Hardware (VDA, locks, HVAC) - too important to delegate
- Marketplace integrate: Nice-to-have (POS, accounting, etc.)

**Reasoning**:
- Eco-lodges remote NEED hardware reliability → direct control
- Guest experience differentiator → in-house control
- Back-office tools → ok partner integrations

---

## FONTI & RIFERIMENTI

### Documentazione Ufficiale
- [Cloudbeds Property Management System](https://www.cloudbeds.com/property-management-system/)
- [Housekeeping - Everything you need to know](https://myfrontdesk.cloudbeds.com/hc/en-us/articles/25695101078427-Housekeeping-Everything-you-need-to-know)
- [Housekeeping room conditions](https://myfrontdesk.cloudbeds.com/hc/en-us/articles/216540808-Housekeeping-room-conditions)
- [Cloudbeds Mobile App Overview](https://myfrontdesk.cloudbeds.com/hc/en-us/articles/21011188971035-Cloudbeds-App-Overview)
- [Cloudbeds API Developer Hub](https://developers.cloudbeds.com/)
- [Access Management and Door Locks Apps](https://myfrontdesk.cloudbeds.com/hc/en-us/articles/7295607768603-Access-Management-and-Door-Locks-Apps)

### Reviews & Analysis
- [Cloudbeds Reviews 2026 - HotelTechReport](https://hoteltechreport.com/operations/hotel-management-software/cloudbeds-hms)
- [PMS UX explained: How good design transforms hotel operations](https://www.cloudbeds.com/articles/pms-user-experience/)
- [Cloudbeds Pricing Plans](https://www.cloudbeds.com/pricing/)
- [Cloudbeds 2026 Pricing, Features, Reviews - GetApp](https://www.getapp.com/hospitality-travel-software/a/cloudbeds/)

### Integrations & Marketplace
- [Cloudbeds Marketplace](https://www.cloudbeds.com/integrations/)
- [DwarPaal - Smart Locks](https://www.cloudbeds.com/integrations/dwarpaal/)
- [Whistle for Cloudbeds Integration](https://myfrontdesk.cloudbeds.com/hc/en-us/articles/8700089277339-Whistle-for-Cloudbeds-Integration-RemoteLock-Connection-Guide)
- [Cloudbeds GX Tickets](https://myfrontdesk.cloudbeds.com/hc/en-us/articles/8699963316379-Cloudbeds-GX-Tickets-Everything-you-Need-to-Know)

### Reporting & Audit
- [Report Types & Cloudbeds Data Fields](https://myfrontdesk.cloudbeds.com/hc/en-us/articles/6621695765531-Report-Types-Cloudbeds-Data-Fields)
- [Useful reports for night audit](https://myfrontdesk.cloudbeds.com/hc/en-us/articles/219104088-Reports-Night-Audit-Reporting)

---

**Fine Studio Cloudbeds**

*"Studiare prima di agire - i player grossi hanno già risolto questi problemi!"*

**Prossimo step suggerito**: Confronto Cloudbeds vs VDA Etheos per identificare gap/overlaps.
