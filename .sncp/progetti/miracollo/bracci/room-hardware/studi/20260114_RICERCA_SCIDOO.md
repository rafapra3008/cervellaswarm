# RICERCA SCIDOO - Sistema PMS Hotel Italiano

**Data**: 14 Gennaio 2026
**Ricercatrice**: Cervella Researcher
**Progetto**: Miracollo - Room Manager Module
**Obiettivo**: Analisi competitor Scidoo per design Room Status & Housekeeping

---

## EXECUTIVE SUMMARY

**Scidoo** è un PMS all-in-one italiano cloud-based, costruito su piattaforma Salesforce, che si posiziona come "l'unico vero software gestionale all-in-one in Italia". Forte focus sul mercato italiano, oltre 500+ strutture attive, rating 5/5 su Capterra.

### TL;DR - Punti Chiave

| Aspetto | Valutazione | Note |
|---------|-------------|------|
| **Room Status/Housekeeping** | ⭐⭐⭐⭐ | App mobile completa, workflow ben strutturato |
| **Domotica/HVAC** | ⭐⭐⭐⭐⭐ | Eccellente integrazione VDA, controllo temperatura |
| **Accessi/Chiavi** | ⭐⭐⭐⭐⭐ | Codici PIN automatici, NFC/RFID, controllo remoto |
| **API/Integrazioni** | ⭐⭐⭐ | API disponibili ma documentazione riservata |
| **UI/UX** | ⭐⭐⭐ | Funzionale ma non moderna come Mews |
| **Pricing** | ❓ | Non pubblico, su richiesta |

**DIFFERENZIATORE PRINCIPALE**: Integrazione domotica nativa (VDA, Undici, STS) con automazioni HVAC e controllo accessi contactless.

---

## 1. CHI È SCIDOO

### Identità Azienda

| Elemento | Dettaglio |
|----------|-----------|
| **Sede** | Ortezzano (FM), Italia |
| **Target** | Strutture ricettive italiane (hotel, B&B, campeggi, residence) |
| **Clienti** | 500+ strutture attive |
| **Rating** | 5/5 su Capterra (dato ufficiale) |
| **Platform** | Cloud-based, costruito su Salesforce |
| **Piattaforme** | Windows, macOS, Linux, Android, iOS |

### Posizionamento di Mercato

```
"L'unico vero software gestionale all-in-one in Italia"
```

**Proposta di Valore**:
- Elimina necessità di software multipli (tutto integrato)
- Personalizzabile per ogni tipo di struttura
- Supporto clienti veloce e reattivo
- Evoluzione continua basata su feedback utenti
- Focus su mercato italiano (compliance ISTAT, Questura, etc)

### Target di Mercato

- Hotel di piccole/medie dimensioni
- B&B e strutture ricettive
- Campeggi e villaggi
- Residence
- SPA e centri benessere
- Ristoranti integrati
- Stabilimenti balneari

---

## 2. ROOM STATUS & HOUSEKEEPING

### Stati Camera (Inferiti)

Non trovata documentazione esplicita degli stati, ma dalle funzionalità emerge:
- **Occupata** / **Libera**
- **Da pulire** / **Pulita** / **In pulizia**
- **Fuori servizio** (manutenzione)
- **Priorità pulizia** (basata su arrivi/partenze)

### Workflow Housekeeping

```
┌─────────────────────────────────────────────────────────┐
│  RECEPTION (PMS)                                        │
│  - Arrivi/Partenze del giorno                           │
│  - Assegnazione priorità pulizia                        │
│  - Comunicazione istantanea con housekeeping            │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│  APP MOBILE HOUSEKEEPING (Android/iOS)                  │
│  - Visualizza assegnazioni                              │
│  - Aggiorna stato camera in tempo reale                 │
│  - Traccia avanzamento giornaliero                      │
│  - Riceve notifiche/messaggi                            │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│  TASTIERINO PORTA (Opzionale - con domotica)            │
│  - Aggiorna stato pulizia direttamente dalla porta      │
│  - No bisogno di tornare alla reception                 │
└─────────────────────────────────────────────────────────┘
```

### App Mobile Features

**Visualizzazione**:
- Elenco camere assegnate
- Priorità basata su arrivi precoci (upsell early arrivals)
- Panoramica carico di lavoro per governante
- Avanzamento giornaliero con punti/coverage

**Azioni**:
- Aggiornamento stato camera
- Segnalazione problemi
- Check completamento task

**Comunicazione**:
- Messaggistica individuale o di gruppo
- Notifiche push
- SMS integrato
- Elimina necessità di walkie-talkie

### Ottimizzazione Carico di Lavoro

**Dashboard Manager**:
- Panoramica workload di ogni governante
- Creazione turni ottimizzati ed efficienti
- Bilanciamento automatico assegnazioni
- Identificazione camere prioritarie per upsell early check-in

---

## 3. ACCESSI & CHIAVI DIGITALI

### Sistema Controllo Accessi

**ECCELLENZA SCIDOO** - Uno dei punti di forza più evidenti!

| Feature | Dettaglio |
|---------|-----------|
| **Codici PIN Automatici** | Generazione automatica codice ingresso per accesso contactless |
| **NFC/RFID** | Tessere con validazione temporale (check-in → checkout) |
| **Passepartout Digitali** | Creazione rapida passepartout per staff |
| **Controllo Remoto** | Apertura porta a distanza (ideal per arrivi fuori orario) |
| **Stato Porta** | Monitoraggio apertura/chiusura in tempo reale |

### Tecnologia Contactless

```
GUEST JOURNEY:

1. Prenotazione → Codice PIN generato automaticamente
2. Arrivo → Codice inviato via email/SMS/app
3. Check-in → Attivazione codice al check-in
4. Accesso Camera → Inserimento PIN su tastierino porta
5. Check-out → Disattivazione automatica codice
```

**VANTAGGIO**: Zero contatto fisico con reception, ideale per self check-in tardivo.

### Integrazioni Hardware

**Partner Domotica Confermati**:
- **VDA** (sistema serrature elettroniche italiano)
- **Undici**
- **STS**

**Non confermato**: Integrazione con Assa Abloy, Salto, Dormakaba (player globali). Focus su fornitori italiani.

---

## 4. HVAC & DOMOTICA

### Controllo Temperatura

**ALTRA ECCELLENZA** - Integrazione domotica molto avanzata!

| Feature | Descrizione |
|---------|-------------|
| **Rilevamento Presenza** | Sistema sa sempre se ospite è in camera |
| **Termoregolazione Automatica** | Abbassa/alza temp in base a presenza |
| **Controllo Remoto Ospite** | Gestione temp da webapp Concierge |
| **Pre-riscaldamento/raffreddamento** | Camera pronta all'arrivo ospite |
| **Ottimizzazione Energetica** | Riduzione consumi automatica |

### Webapp Concierge per Ospiti

```
CONTROLLI DISPONIBILI:
├── Temperatura camera
├── Apertura tende/tapparelle (se integrato)
├── Luci (se integrato)
└── Richieste servizi
```

**TEMPISTICHE**:
- Controllo durante prenotazione (pre-arrivo)
- Controllo in camera (durante soggiorno)

### Automazioni Avanzate

**Scenario: Ospite Esce**
```
Porta si chiude → Sistema rileva assenza →
Temperatura si abbassa automaticamente →
Risparmio energetico
```

**Scenario: Ospite Rientra**
```
Porta si apre → Sistema rileva presenza →
Temperatura torna a comfort →
Ospite trova camera già piacevole
```

### Sicurezza & Allarmi

**Rilevamento Automatico Eventi Critici**:
- Allarme bagno (pulsante emergenza)
- Fuga gas
- Allagamento
- Incendio

**AZIONE**: Notifica immediata staff + possibile attivazione protocolli sicurezza.

---

## 5. ACTIVITY LOG & AUDIT TRAIL

**NOTA**: Documentazione pubblica limitata su questo aspetto.

### Evidenze Indirette

Dalle funzionalità emerge che il sistema DEVE loggare:
- **Accessi camera** (apertura porta con codice/tessera)
- **Modifiche stato camera** (chi, quando, da quale dispositivo)
- **Cambio temperatura** (automatico vs manuale ospite)
- **Presenza/assenza ospite** (rilevamento sensori)
- **Comunicazioni housekeeping** (messaggi inviati/ricevuti)

### Report Disponibili

| Tipo Report | Scopo |
|-------------|-------|
| **Revenue tracking** | Monitoraggio ricavi per profit center |
| **Sales progress** | Avanzamento vendite |
| **Profit center analysis** | Alloggio, ristorante, wellness, meeting rooms separati |
| **Compliance Reports** | ISTAT, Questura (obbligatori Italia) |

**MANCANZA EVIDENTE**: No menzione esplicita di audit trail compliance (GDPR, ISO) o report forensi dettagliati.

---

## 6. UI/UX

### Design

**Valutazione**: Funzionale ma non cutting-edge.

| Aspetto | Giudizio |
|---------|----------|
| **Estetica** | Tradizionale, enterprise-style |
| **Usabilità** | "Semplice e intuitivo" secondo recensioni |
| **Mobile-first** | App native iOS/Android |
| **Modernità** | Dietro a Mews in termini di design |
| **Curva apprendimento** | Lunga configurazione iniziale |

### Punti di Forza UX

✅ **Drag & Drop Planning** - Prenotazioni rapide con trascinamento
✅ **Multi-dispositivo** - Funziona ovunque (desktop, tablet, smartphone)
✅ **Modifica Bulk Tariffe** - Cambio prezzi su periodi estesi con granularità giornaliera
✅ **ID Scan** - Scansione documenti da smartphone (zero errori manuali)

### Punti di Debolezza UX

❌ **Tempo configurazione lungo** - Impedisce valutazione corretta in trial gratuito
❌ **Complessità iniziale** - Molte funzionalità richiedono setup
❌ **Design datato** - Non al livello di Mews/Cloudbeds moderni

### Recensioni Utenti

**PRO** (dalle recensioni):
> "Semplice e intuitivo, completo in ogni sezione"
> "Supporto sempre disponibile, anche Ferragosto a pranzo!"
> "Unico software che gestisce hotel, SPA e ristorante senza cambiare programma"

**CONTRO** (dalle recensioni):
> "Assemblaggio artigianale di software diversi, non suite organica"
> "Multi-property non veramente funzionale come pubblicizzato"
> "Channel Manager molto basico, poca utilità per revenue management"
> "Pericoloso: rischi di vendere sotto costo se non monitori"

---

## 7. API & INTEGRAZIONI

### API Disponibili

**STATUS**: API esistenti ma documentazione NON pubblica.

**Per accedere**:
- Contattare: a.ciriaci@scidoo.com
- Fornire documentazione uso
- Richiedere accesso test

**Help Center**: help.scidoo.com (documentazione tecnica)

### Integrazioni Native

| Categoria | Integrato |
|-----------|-----------|
| **Channel Manager** | ✅ Nativo (Room Cloud) |
| **Booking Engine** | ✅ Nativo |
| **OTA** | ✅ Sincronizzazione automatica prezzi/disponibilità |
| **Metasearch** | ✅ (dettagli limitati) |
| **Domotica** | ✅ VDA, Undici, STS |
| **Payment Gateway** | ✅ (da confermare quali) |
| **Questura/ISTAT** | ✅ Report automatici compliance Italia |

### Architettura Integrazione

**Piattaforma Base**: Salesforce
**Modello**: Cloud multi-tenant
**Protocolli**: XML interface (standard PMS/Channel Manager)

**NOTA**: Essere su Salesforce è un pro (ecosistema robusto) e un contro (meno flessibilità architetturale).

### Limitazioni Evidenziate

⚠️ **Channel Manager Basico** - Recensioni segnalano scarsa utilità per revenue management quotidiano
⚠️ **Multi-Property Limitato** - Non veramente multi-property come pubblicizzato
⚠️ **Nessuna Marketplace** - A differenza di Mews (1000+ integrazioni), Scidoo ha ecosistema chiuso

---

## 8. PRICING

### Modello di Business

**TIPO**: SaaS (Software as a Service) con pagamento ricorrente.

**PREZZI**: ❌ NON pubblici - disponibili solo su richiesta diretta.

### Informazioni Indirette

Dalle recensioni:
> "In grado di garantire lavoro in modo semplice ed economico"

**Interpretazione**: Posizionamento low-mid price, competitivo per mercato italiano piccole/medie strutture.

### ⚠️ ALERT - Problemi Segnalati

**DALLE RECENSIONI NEGATIVE**:
- Utenti contattati da avvocato (parente azienda) per riscuotere pagamento annuale completo
- Numerosi preventivi errati per errori configurazione formule
- Rischio di vendere sotto costo senza monitoraggio attento

**IMPLICAZIONE**: Modello contrattuale potenzialmente rigido, necessità di attenzione nella fase contrattuale.

---

## 9. DIFFERENZIATORI SCIDOO

### Punti di Forza Unici

#### 🥇 Integrazione Domotica Nativa
**LA KILLER FEATURE di Scidoo!**

Nessun altro competitor studiato (Mews, Opera Cloud, Cloudbeds) ha integrazione domotica così profonda a livello PMS:
- Controllo temperatura automatico
- Rilevamento presenza ospite
- Accessi contactless con PIN/NFC
- Controllo remoto porte
- Allarmi sicurezza integrati

**ECOSISTEMA**: VDA + Undici + STS = partnership hardware locali italiane.

#### 🥇 Compliance Italiana Total

- Report Questura automatico
- ISTAT integrato
- Privacy GDPR con firma digitale
- Tassa di soggiorno automatica
- Documentazione alloggiati sincronizzata

**VALORE**: Zero sbattimenti amministrativi per strutture italiane.

#### 🥇 Vero All-in-One

Un solo software per:
- Hotel PMS
- Ristorante
- SPA & Wellness
- Stabilimento balneare
- Campeggio
- Magazzino
- CRM

**VALORE**: No frammentazione, dati centralizzati.

### Punti di Debolezza

#### ❌ Non Competitive su Revenue Management

Channel Manager "molto basico", poca utilità per gestione dinamica prezzi quotidiana. Competitori come Mews hanno tool più sofisticati.

#### ❌ Multi-Property Limitato

Pubblicizzato come multi-property ma recensioni segnalano limitazioni. Non al livello di Opera Cloud o Mews per catene.

#### ❌ Ecosistema Chiuso

Vs Mews (1000+ integrazioni open), Scidoo ha approccio "giardino recintato". Meno flessibilità.

#### ❌ Design Non Moderno

UI datata, non al passo con UX moderne di Mews/Cloudbeds. Curva apprendimento ripida.

#### ❌ Rischio Vendita

Recensioni segnalano rischio di configurazioni che portano a vendere sotto costo. Necessita competenza setup.

---

## 10. SCIDOO vs COMPETITORI

### Scidoo vs Mews

| Aspetto | Scidoo | Mews |
|---------|--------|------|
| **Domotica** | ⭐⭐⭐⭐⭐ Nativa | ⭐⭐ Via integrazioni |
| **Design UI** | ⭐⭐⭐ Funzionale | ⭐⭐⭐⭐⭐ Moderno |
| **API/Ecosistema** | ⭐⭐⭐ Chiuso | ⭐⭐⭐⭐⭐ Open (1000+) |
| **Revenue Management** | ⭐⭐ Basico | ⭐⭐⭐⭐ Sofisticato |
| **Multi-property** | ⭐⭐ Limitato | ⭐⭐⭐⭐⭐ Enterprise |
| **Compliance Italia** | ⭐⭐⭐⭐⭐ Total | ⭐⭐⭐ Buona |
| **Target** | SMB Italia | Enterprise Globale |
| **Prezzo** | 💰💰 Low-Mid | 💰💰💰 Mid-High |

### Scidoo vs Opera Cloud

| Aspetto | Scidoo | Opera Cloud |
|---------|--------|-------------|
| **Cloud Native** | ⭐⭐⭐⭐ (Salesforce) | ⭐⭐ (Adapted) |
| **Domotica** | ⭐⭐⭐⭐⭐ Nativa | ⭐⭐⭐ Via partner |
| **Enterprise** | ⭐⭐ SMB focus | ⭐⭐⭐⭐⭐ Catene |
| **Deployment** | ⭐⭐⭐⭐ Veloce | ⭐⭐ Lento |
| **Complessità** | ⭐⭐⭐ Media | ⭐⭐⭐⭐⭐ Alta |
| **Manutenzione** | ⭐⭐⭐⭐ Easy (cloud) | ⭐⭐ Complessa |
| **Guest-centric** | ⭐⭐⭐ Buono | ⭐⭐ Room-centric |

### Scidoo vs Cloudbeds

| Aspetto | Scidoo | Cloudbeds |
|---------|--------|-----------|
| **Domotica** | ⭐⭐⭐⭐⭐ Nativa | ⭐⭐⭐ Via partner |
| **Mercato** | 🇮🇹 Italia | 🌍 Globale |
| **All-in-One** | ⭐⭐⭐⭐⭐ Completo | ⭐⭐⭐⭐ Molto buono |
| **Channel Manager** | ⭐⭐ Basico | ⭐⭐⭐⭐ Eccellente |
| **Mobile App** | ⭐⭐⭐⭐ Buona | ⭐⭐⭐⭐ Ottima |
| **Compliance Italia** | ⭐⭐⭐⭐⭐ Perfetta | ⭐⭐⭐ Buona |

### Posizionamento Scidoo

```
                    ENTERPRISE
                        ↑
                        │
            Opera Cloud │
                        │
    ┌───────────────────┼───────────────────┐
    │                   │                   │
    │                   │         Mews      │  GLOBAL
────┼───────────────────┼───────────────────┼────
ITALIA                  │     Cloudbeds     │
    │                   │                   │
    │   SCIDOO ●        │                   │
    │                   │                   │
    └───────────────────┼───────────────────┘
                        │
                        ↓
                       SMB
```

**SWEET SPOT**: Strutture italiane 20-100 camere che vogliono domotica integrata senza costi enterprise.

---

## 11. COSA POSSIAMO IMPARARE DA SCIDOO?

### Per Miracollo Room Manager

#### ✅ DA COPIARE

**1. Integrazione Domotica Seamless**
```
Scidoo ha capito che domotica NON è un "extra" ma parte CORE del PMS.
Room Manager deve avere domotica FIRST-CLASS, non bolt-on.

LEZIONE: VDA integration come REQUISITO, non nice-to-have.
```

**2. Codici PIN Automatici**
```
Zero friction per ospiti:
Check-in → Codice PIN generato → Email/SMS → Accesso camera

LEZIONE: Self check-in contactless deve essere FACILE, non tecnico.
```

**3. Update Stato Camera da Tastierino Porta**
```
Governante finisce pulizia → Aggiorna stato dalla porta stessa → No ritorno reception

LEZIONE: Ridurre passi = aumentare efficienza. UI deve essere DOVE serve.
```

**4. Ottimizzazione Housekeeping Workload**
```
Dashboard manager con panoramica carico lavoro + priorità automatica

LEZIONE: Housekeeping non è "lista task" ma OTTIMIZZAZIONE RISORSE.
```

**5. Rilevamento Presenza Ospite**
```
Sistema sa sempre se ospite è in camera → automazioni intelligenti

LEZIONE: Sensori presenza = game changer per energia + sicurezza.
```

#### ❌ DA EVITARE

**1. "Assemblaggio Artigianale"**
```
Recensioni segnalano: "Assemblaggio di software diversi, non suite organica"

LEZIONE: Miracollo deve essere ARCHITETTURALMENTE COERENTE.
Backend unico, non pezzi incollati.
```

**2. Configurazione Lunga e Complessa**
```
"Tempo configurazione lungo impedisce valutazione corretta in trial"

LEZIONE: Default intelligenti. 80% funziona out-of-box, 20% personalizzabile.
```

**3. Channel Manager Basico**
```
"Poca utilità per revenue management quotidiano"

LEZIONE: Se facciamo una feature, facciamo BENE o non facciamo.
No feature "check-box" incomplete.
```

**4. Multi-Property Non Vero**
```
"Pubblicizzato ma limitato"

LEZIONE: Mai oversell. Dire cosa FUNZIONA REALMENTE, non roadmap.
```

**5. Rischio Vendita Sotto Costo**
```
"Errori configurazione formule = vendita sotto costo"

LEZIONE: Revenue rules VALIDATE input. Impedisci errori critici via design.
```

### Design Patterns Utili

#### Pattern: Presenza-Based Automation
```javascript
// Scidoo lo fa benissimo
onDoorOpen() {
  detectGuestPresence();
  if (guestPresent) {
    setTemperature(COMFORT_LEVEL);
    logActivity('Guest entered', timestamp);
  }
}

onDoorClose() {
  setTimeout(() => {
    if (!detectGuestPresence()) {
      setTemperature(ECO_LEVEL);
      updateRoomStatus('Vacant - Guest Out');
    }
  }, GRACE_PERIOD);
}
```

**APPLICAZIONE MIRACOLLO**: Implementare rilevamento presenza come CORE feature Room Manager.

#### Pattern: Priorità Pulizia Dinamica
```javascript
// Scidoo identifica camere prioritarie
calculateCleaningPriority() {
  rooms.forEach(room => {
    if (hasEarlyArrival(room) && room.status === 'Dirty') {
      room.priority = 'HIGH'; // Upsell opportunity
    } else if (hasCheckout(room)) {
      room.priority = 'MEDIUM';
    } else {
      room.priority = 'LOW';
    }
  });
  return sortByPriority(rooms);
}
```

**APPLICAZIONE MIRACOLLO**: Dashboard housekeeping con priorità INTELLIGENTE basata su business logic.

#### Pattern: Controllo Remoto Porta
```javascript
// Scidoo permette apertura a distanza
remoteDoorControl(roomId, action) {
  if (validateStaffPermission(currentUser, roomId)) {
    sendCommandToDoor(roomId, action);
    logActivity(currentUser, roomId, action, timestamp);
    notifyGuest(roomId, 'Staff accessed your room', reason);
  }
}
```

**APPLICAZIONE MIRACOLLO**: Controllo remoto con AUDIT TRAIL completo + notifica ospite (trasparenza).

---

## 12. RACCOMANDAZIONI FINALI

### Per Room Manager Miracollo

#### MUST HAVE (Ispirati da Scidoo)

1. **Integrazione VDA First-Class**
   - Non "optional", ma CORE
   - Stati camera sincronizzati con serrature
   - Codici PIN automatici
   - Controllo remoto porte

2. **Rilevamento Presenza Ospite**
   - Sensori porta/movimento
   - Automazioni HVAC basate su presenza
   - Sicurezza (allarmi se anomalie)

3. **Housekeeping Mobile App**
   - Task assignment real-time
   - Update stato camera mobile
   - Dashboard carico lavoro manager
   - Priorità dinamica

4. **Audit Trail Completo**
   - Log ogni accesso camera
   - Log ogni cambio stato
   - Log automazioni HVAC
   - Report forensi disponibili

#### NICE TO HAVE

5. **Update Stato da Tastierino Porta**
   - Governante aggiorna stato senza tornare a reception
   - Richiede hardware VDA che lo supporti

6. **Allarmi Sicurezza Integrati**
   - Allagamento, fuga gas, incendio
   - Notifiche staff immediate

### Confronto Feature Set

| Feature | Scidoo | Miracollo Target |
|---------|--------|------------------|
| Room Status Mobile | ✅ | ✅ MUST |
| Controllo Accessi NFC/PIN | ✅ | ✅ MUST |
| Rilevamento Presenza | ✅ | ✅ MUST |
| HVAC Automation | ✅ | ✅ MUST |
| Controllo Remoto Porte | ✅ | ✅ MUST |
| Update da Tastierino | ✅ | 🟡 NICE |
| Allarmi Sicurezza | ✅ | 🟡 NICE |
| Audit Trail Completo | 🟡 (non dettagliato) | ✅ MUST (superiore) |
| API Aperte | ❌ | ✅ MUST (superiore) |
| UI Moderna | ❌ | ✅ MUST (superiore) |

### Come Battere Scidoo

**LORO VANTAGGIO**: Domotica integrata + compliance Italia.

**NOSTRO VANTAGGIO**:
1. **Architettura Superiore** - Moderna, non assemblaggio Salesforce
2. **UI/UX Superiore** - Design livello Mews, non enterprise datato
3. **API Aperte** - Ecosistema aperto vs giardino recintato
4. **Audit Trail Superiore** - Compliance GDPR/ISO nativa
5. **No Vendor Lock-in** - Self-hosted option, non solo cloud

**STRATEGIA**: Prendere il MEGLIO di Scidoo (domotica) + MEGLIO di Mews (design/API) = **VINCERE**.

---

## FONTI & RIFERIMENTI

### Sito Ufficiale Scidoo
- [Homepage Scidoo](https://www.scidoo.com/)
- [PMS Hotel Features](https://www.scidoo.com/en/pms-hotel)
- [Controllo Accessi & Domotica](https://www.scidoo.com/controllo-accessi)
- [Channel Manager](https://www.scidoo.com/en/channel-manager)

### Review Platforms
- [Scidoo Reviews - Capterra](https://www.capterra.com/p/216364/Scidoo/)
- [Scidoo Reviews - Hotel Tech Report](https://hoteltechreport.com/operations/property-management-systems/scidoo)
- [Scidoo Recensioni Italia - Capterra](https://www.capterra.com/p/216364/Scidoo/reviews/)
- [Scidoo Reviews - Trustpilot](https://it.trustpilot.com/review/scidoo.com)

### App Mobile
- [Scidoo Hospitality - Google Play](https://play.google.com/store/apps/details?id=com.scidoo&hl=en_US)
- [Scidoo Booking Manager - App Store](https://apps.apple.com/ca/app/scidoo-booking-manager/id1396997974)

### Integrazioni & API
- [Scidoo Help Center](https://help.scidoo.com/)
- [Scidoo Integration - HyperGuest](https://www.hyperguest.com/integrations/scidoo)

### Comparazioni Competitor
- [Best Hotel Housekeeping Software 2026](https://hoteltechreport.com/operations/housekeeping-software)
- [30 Best Hotel Management Software 2026](https://thehotelgm.com/tools/best-hotel-management-software/)
- [Mews vs Opera Cloud Comparison](https://sourceforge.net/software/compare/Mews-vs-OPERA-Cloud-PMS/)

---

## CONCLUSIONI

### Scidoo in 3 Frasi

1. **PMS all-in-one italiano** con eccellente integrazione domotica (VDA/Undici/STS).
2. **Forte su accessi contactless e HVAC automation**, debole su revenue management e design moderno.
3. **Ideale per SMB italiane 20-100 camere** che vogliono domotica senza costi enterprise.

### Valore per Miracollo

**ALTO** - Scidoo ci mostra che:
- Integrazione domotica NATIVA è possibile e apprezzata
- Rilevamento presenza = game changer
- Housekeeping mobile app FUNZIONA
- Compliance Italia può essere automatizzata totalmente

**MA ANCHE**: Conferma che UI datata e ecosistema chiuso sono DEBOLEZZE competitive.

### Next Steps

1. ✅ Studiare VDA protocol per integrazione profonda
2. ✅ Definire sensori presenza come CORE requirement
3. ✅ Design housekeeping mobile app (ispirato a Scidoo ma UI migliore)
4. ✅ API aperte come differenziatore vs Scidoo
5. ✅ Audit trail superiore (compliance as competitive advantage)

---

**Fine Ricerca Scidoo**

*"Non reinventiamo la ruota - la miglioriamo!"*
*Cervella Researcher - 14 Gennaio 2026*
