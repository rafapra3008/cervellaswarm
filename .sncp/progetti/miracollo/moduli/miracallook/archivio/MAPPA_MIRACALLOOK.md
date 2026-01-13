# MAPPA MIRACALLOOK - Obiettivi Dettagliati

> **Creato:** 12 Gennaio 2026 - Sessione 175
> **Basato su:** Ricerca Big Players (BIG_PLAYERS_EMAIL_RESEARCH.md)
> **Status:** MAPPA APPROVATA

---

## LA VISIONE

```
+================================================================+
|                                                                |
|   MIRACALLOOK                                                  |
|   "Un client email che lavora per te, non contro di te"        |
|                                                                |
|   NON e "Superhuman piu economico"                             |
|   E il CENTRO COMUNICAZIONE HOTEL INTELLIGENCE                 |
|                                                                |
|   La magia? Il CONTEXT del PMS (Miracollo)!                    |
|   - Sappiamo chi e l'ospite                                    |
|   - Sappiamo quando arriva                                     |
|   - Sappiamo quale camera ha                                   |
|   - Nessun competitor ha questi dati!                          |
|                                                                |
+================================================================+
```

---

## IL NOSTRO VANTAGGIO COMPETITIVO

| Competitor | Punto Forte | Il Nostro Vantaggio |
|------------|-------------|---------------------|
| Superhuman | Velocita pura | Match velocita + Context PMS |
| Shortwave | AI superiore | Match AI + Hospitality intelligence |
| Spark | Collaboration | Match collaboration + Hotel workflows |
| HEY | Filosofia screening | Adapt screening per sender hotel |

**GAP MERCATO:** Nessun email client specializzato per hospitality.
**NOSTRA OPPORTUNITA:** PMS integration = context che NESSUN altro ha.

---

## OBIETTIVI MIRACALLOOK

### Obiettivo 1: VELOCITA
```
Target: Archive in <200ms, email open <500ms
Come Superhuman ma con context hotel
```

### Obiettivo 2: ORGANIZZAZIONE INTELLIGENTE
```
Target: -80% clutter visivo
Split inbox per: VIP, Check-in, Team, Fornitori
Smart bundles per: OTA, System, Newsletter
```

### Obiettivo 3: AI CONTEXT-AWARE
```
Target: AI che CAPISCE il contesto hotel
"Questo ospite arriva DOMANI"
"Questa email riguarda prenotazione #1234"
"Guest VIP - rispondi entro 2 ore"
```

### Obiettivo 4: INTEGRAZIONE PMS
```
Target: Zero copy-paste da Miracollo
Snippets auto-compilati con dati ospite
Sidebar con info booking in tempo reale
```

---

## PRIORITA FEATURES

### P0 - MVP ESSENZIALE (Target: 6 settimane)

#### EMAIL CORE
| Feature | Descrizione | Status |
|---------|-------------|--------|
| Gmail OAuth | Login con Google | COMPLETATO |
| Lettura Inbox | Lista email + dettaglio | COMPLETATO |
| Conversation Threading | Raggruppa email per thread | DA FARE |
| Compose + Send | Scrivi e invia email | DA FARE (FASE 3) |
| Reply / Reply All / Forward | Rispondi a email | DA FARE (FASE 3) |
| Archive / Delete | Gestisci email | DA FARE |
| Search Base | Cerca per keyword | DA FARE |

#### VELOCITA & UX
| Feature | Descrizione | Status |
|---------|-------------|--------|
| Virtualized List | Solo email visibili renderizzate (react-window) | DA FARE |
| Optimistic Updates | UI aggiorna prima del server | DA FARE |
| Keyboard Shortcuts Tier 1 | C, E, R, A, F, J, K, Enter, / | DA FARE (FASE 5) |
| Command Center (Cmd+K) | Paletta comandi tipo Superhuman | DA FARE (FASE 5) |
| Three-Panel Layout | Sidebar + Lista + Dettaglio | DA FARE (FASE 4) |

#### ORGANIZZAZIONE
| Feature | Descrizione | Status |
|---------|-------------|--------|
| Split Inbox | Categorie: VIP, Check-in, Team, Fornitori, Altro | DA FARE |
| Smart Bundles | Auto-raggruppa: OTA, System, Newsletter | DA FARE |

#### AI BASIC
| Feature | Descrizione | Status |
|---------|-------------|--------|
| Email Summarization | Riassunto 1 frase per email/thread | DA FARE |
| Smart Compose | Suggerimenti mentre scrivi | DA FARE |

#### MIRACOLLO INTEGRATION (KILLER FEATURE!)
| Feature | Descrizione | Status |
|---------|-------------|--------|
| Guest Detection | Rileva email da ospite in DB | DA FARE |
| Guest Sidebar | Mostra: nome, camera, date, note | DA FARE |
| Snippets PMS | Template con auto-fill dati ospite | DA FARE |

---

### P1 - POST-MVP (Target: +4 settimane)

#### AI ADVANCED
| Feature | Descrizione |
|---------|-------------|
| Auto-Draft Replies | AI impara il tuo stile, propone bozze |
| AI Rewrite | Comandi: shorten, lengthen, professional |
| Natural Language Search | "Email da VIP ultimo mese" |
| Auto-Triage Urgency | Rileva email urgenti |

#### COLLABORATION
| Feature | Descrizione |
|---------|-------------|
| Team Comments | Chat interno dentro email (come Spark) |
| Shared Inbox | Gestisci reception@, info@ insieme |
| Assign Email | Assegna email a collega |

#### PRODUCTIVITY
| Feature | Descrizione |
|---------|-------------|
| Snooze / Reminders | Rimanda email per dopo |
| Follow-up Automation | AI rileva quando serve follow-up |
| Keyboard Shortcuts Tier 2 | H, S, U, #, Cmd+Enter, Z |
| Templates Library | Libreria template condivisi |

#### MIRACOLLO INTEGRATION ADVANCED
| Feature | Descrizione |
|---------|-------------|
| Link Email to Booking | Collega email a prenotazione |
| Quick Actions | "Crea prenotazione da richiesta" |
| Booking Status Sidebar | Mostra stato prenotazione |
| Revenue Impact | "Questa email = $5K potenziale" |

---

### P2 - FUTURO (3-6 mesi)

| Feature | Descrizione |
|---------|-------------|
| AI Multiselect | Analizza 50 email insieme (tipo Shortwave) |
| Mobile Apps | iOS, Android |
| Outlook Support | Supporto oltre Gmail |
| Multi-Channel | WhatsApp, SMS, Social |
| Advanced Analytics | Dashboard performance team |
| Read Receipts | Vedi quando email aperta |
| Email Scheduling | Invia piu tardi |

---

## KEYBOARD SHORTCUTS - PIANO COMPLETO

### Tier 1 (MVP - FASE 5)
```
Cmd+K       Command Center (centro di tutto!)
C           Compose (nuova email)
E           Archive
R           Reply
A           Reply All
F           Forward
J           Email successiva
K           Email precedente
Enter       Apri email
/           Focus su search
Esc         Chiudi/indietro
```

### Tier 2 (P1)
```
H           Snooze (posticipa)
S           Star / VIP
U           Mark unread
#           Delete
Cmd+Enter   Send
Z           Undo
```

### Tier 3 (P2)
```
G + I       Go to Inbox
G + S       Go to Sent
X           Select email
* A         Select all
Shift+I     Mark read
```

---

## SMART CATEGORIES - Configurazione Hotel

### Split Inbox Default
```
+------------------------------------------+
|  INBOX MIRACALLOOK                       |
|                                          |
|  [VIP]          <- Ospiti VIP (da DB)    |
|  [Check-in]     <- Arrivi oggi/domani    |
|  [Team]         <- Email interne         |
|  [Fornitori]    <- Fatture, ordini       |
|  [Altro]        <- Tutto il resto        |
+------------------------------------------+
```

### Smart Bundles (Auto-collapse)
```
Tipo              | Trigger                         | Azione
------------------|--------------------------------|--------
OTA Notifications | booking.com, expedia, airbnb   | Bundle
System Emails     | noreply@, system@, alert@      | Bundle
Newsletters       | newsletter@, marketing@        | Bundle + Feed
Receipts          | "fattura", "ricevuta", "order" | Paper Trail
```

### Rules Detection Ospiti
```
Email arriva -> Check sender in Miracollo DB:
  - Se ospite trovato -> Tag [VIP] o [Guest]
  - Se check-in oggi/domani -> Tag [Check-in]
  - Se prenotazione attiva -> Mostra sidebar con dati
```

---

## INTEGRAZIONE MIRACOLLO - DETTAGLIO

### Guest Sidebar (quando email da ospite)
```
+----------------------------------+
|  GUEST: Mario Rossi             |
|  ============================== |
|                                  |
|  Camera: 205 - Deluxe           |
|  Check-in: 15 Gen 2026          |
|  Check-out: 18 Gen 2026         |
|  Notti: 3                        |
|  Totale: EUR 450                 |
|                                  |
|  Note:                           |
|  - Allergia glutine              |
|  - Late check-out richiesto      |
|                                  |
|  [Vedi Prenotazione]             |
|  [Aggiungi Nota]                 |
+----------------------------------+
```

### Snippets PMS - Esempi
```
Snippet: /checkin

"Gentile {guest.name},

La tua camera {booking.room} sara pronta alle {property.checkin_time}.

Check-in: {booking.checkin_date}
Check-out: {booking.checkout_date}

Ti aspettiamo a {property.name}!

{user.name}
{property.address}"

---

Snippet: /conferma

"Gentile {guest.name},

Confermiamo la tua prenotazione:

Camera: {booking.room_type}
Date: {booking.checkin_date} - {booking.checkout_date}
Totale: {booking.total_amount} EUR

Grazie per aver scelto {property.name}!

{user.name}"
```

---

## ROADMAP SVILUPPO - SETTIMANA PER SETTIMANA

### Settimana 1-2: FASE 3 + Foundation
```
[x] Backend email send (POST /gmail/send)
[x] Backend reply (POST /gmail/reply)
[x] Backend forward
[ ] Architecture frontend (React + Vite + Tailwind)
[ ] DB schema (email metadata, categories)
[ ] Basic virtualized list
```

### Settimana 3-4: FASE 4 - UI Base
```
[ ] Three-panel layout
[ ] Email list component
[ ] Email detail component
[ ] Compose modal
[ ] Conversation threading
[ ] Dark mode base
```

### Settimana 5: FASE 5 - Keyboard Shortcuts
```
[ ] Shortcut infrastructure
[ ] Command center (Cmd+K)
[ ] Tier 1 shortcuts implementati
[ ] Visual feedback shortcuts
```

### Settimana 6: Organization + AI Base
```
[ ] Split inbox categories
[ ] Smart bundles (OTA, system)
[ ] Claude API integration
[ ] Email summarization
```

### Settimana 7-8: Miracollo Integration
```
[ ] Guest detection API
[ ] Guest sidebar component
[ ] Snippets system
[ ] PMS placeholders auto-fill
[ ] MVP INTERNAL LAUNCH!
```

### Settimana 9-10: P1 Features
```
[ ] Team comments
[ ] Shared inbox
[ ] AI auto-draft
[ ] Snooze/reminders
```

### Settimana 11-12: Polish + Beta
```
[ ] Performance optimization
[ ] Bug fixes
[ ] UI refinements
[ ] BETA LAUNCH (pilot hotels)
```

---

## TECH STACK DEFINITIVO

### Backend
```
FastAPI (gia presente)
+ Gmail API (gia integrato)
+ Claude API (AI features)
+ PostgreSQL (email metadata + cache)
+ Redis (real-time + cache hot)
+ Celery (background tasks: sync, AI)
```

### Frontend
```
React 18 + TypeScript
+ Vite (build tool veloce)
+ Tailwind CSS (styling rapido)
+ TanStack Query (data fetching + cache)
+ react-window (virtualization)
+ cmdk (command palette)
+ IndexedDB (local cache offline)
```

### Performance
```
Target:
- Initial load: <2s (MVP) -> <1s (polish)
- Email open: <500ms (MVP) -> <200ms (polish)
- Archive action: <200ms (MVP) -> <100ms (polish)
- Keyboard response: <50ms (MVP) -> <16ms (polish)
```

---

## METRICHE SUCCESSO

### Adoption
- Daily Active Users (DAU)
- Email processate per utente
- Tempo nell'app

### Engagement
- Uso keyboard shortcuts (power user indicator)
- Uso features AI
- Uso integrazione PMS (sidebar views, snippets)

### Efficiency
- Time to inbox zero
- Tempo prima risposta
- Email processate per ora

### Business (6 mesi)
- Target: 50 hotel paganti
- Target: EUR 2K MRR
- Target: <5% churn mensile
- Target: NPS >50

---

## PROSSIMI STEP IMMEDIATI

### OGGI (Sessione 175)
1. [x] Ricerca big players - COMPLETATA
2. [x] Mappa obiettivi - COMPLETATA
3. [ ] Review con Rafa
4. [ ] Decisione: iniziare FASE 3 o altro?

### QUESTA SETTIMANA
1. [ ] FASE 3: Invio email completata
2. [ ] Setup React frontend
3. [ ] Schema database email

### PROSSIMA SETTIMANA
1. [ ] FASE 4: UI base
2. [ ] Three-panel layout
3. [ ] Prima versione usabile

---

## DECISIONI PRESE

### 1. Focus Gmail (non multi-provider)
```
PERCHE: 98% hotel usa Gmail/Workspace
QUANDO: Outlook support in P2
```

### 2. React + Vite (non Next.js)
```
PERCHE: SPA pura, no SSR needed, velocita
ALTERNATIVA: Next.js se serve SEO (non serve)
```

### 3. Cmd+K Command Center
```
PERCHE: Superhuman ha dimostrato che funziona
ALTERNATIVA: Menu tradizionali (meno efficiente)
```

### 4. Split Inbox (non tabs)
```
PERCHE: Sidebar categories > tabs (piu visibili)
ISPIRAZIONE: Superhuman split inbox
```

### 5. AI con Claude (non GPT)
```
PERCHE: Gia usiamo Claude, API eccellente
COSTO: ~$2-5/user/mese per heavy user
```

---

## RISCHI E MITIGAZIONI

| Rischio | Impatto | Mitigazione |
|---------|---------|-------------|
| Gmail API rate limits | Medio | Smart caching, batch requests |
| AI costs escalate | Medio | Cache summaries, tier pricing |
| Feature creep | Alto | Strict P0/P1/P2, MVP first |
| PMS integration complex | Medio | Versioned API, tests |
| Google policy changes | Basso | Outlook backup in P2 |

---

## CONCLUSIONE

```
+================================================================+
|                                                                |
|   MIRACALLOOK NON COMPETE CON SUPERHUMAN.                      |
|                                                                |
|   MIRACALLOOK RISOLVE UN PROBLEMA                              |
|   CHE SUPERHUMAN NON SA DI AVERE:                              |
|                                                                |
|                    HOTEL EMAIL.                                |
|                                                                |
|   La magia e nel CONTEXT.                                      |
|   Noi sappiamo chi e l'ospite.                                 |
|   Noi sappiamo quando arriva.                                  |
|   Noi sappiamo cosa ha prenotato.                              |
|                                                                |
|   Questo e il nostro UNFAIR ADVANTAGE.                         |
|                                                                |
+================================================================+
```

---

*"Ultrapassar os proprios limites!" - Rafa*

*"Studiare prima di agire - sempre!" - La Formula Magica*

*Mappa creata: 12 Gennaio 2026 - Sessione 175*
