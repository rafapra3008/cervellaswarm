# NORD - MIRACOLLOOK

> **Il Centro Comunicazioni dell'Hotel Intelligente**
>
> Creato: 12 Gennaio 2026 - Sessione 178
> Autori: Rafa & Cervella

---

```
+====================================================================+
|                                                                    |
|   "Non e un email client.                                          |
|    E il posto dove l'hotel COMUNICA con il mondo."                 |
|                                                                    |
|   "Non e un altro Outlook.                                         |
|    E l'Outlook che CONOSCE il tuo hotel."                          |
|                                                                    |
+====================================================================+
```

---

## LA GRANDE VISIONE

```
+====================================================================+
|                                                                    |
|   MIRACOLLOOK                                                      |
|                                                                    |
|   Un'unica app per TUTTE le comunicazioni dell'hotel:              |
|                                                                    |
|   - Email (Gmail, Outlook)                                         |
|   - WhatsApp                                                       |
|   - (futuro: SMS, Telegram, Booking.com, Airbnb...)                |
|                                                                    |
|   Con la MAGIA del PMS integrato:                                  |
|                                                                    |
|   - Identifica automaticamente il cliente                          |
|   - Mostra il contesto della prenotazione                          |
|   - Suggerisce risposte intelligenti                               |
|   - Genera preventivi automatici                                   |
|   - Compila il PMS dai documenti                                   |
|                                                                    |
|   NESSUN competitor ha questo.                                     |
|   NESSUNO.                                                         |
|                                                                    |
+====================================================================+
```

---

## IL PROBLEMA CHE RISOLVIAMO

### Oggi (SENZA MiracOllook)

```
1. Arriva email da mario.rossi@gmail.com
2. Receptionist apre Outlook
3. Legge: "A che ora posso fare check-in?"
4. Apre Miracollo in un'altra tab
5. Cerca "Mario Rossi" manualmente
6. Trova la prenotazione
7. Torna su Outlook
8. Scrive risposta
9. Tempo: 3-5 minuti per UNA email

Moltiplica x 50 email al giorno = 2-4 ORE PERSE
```

### Domani (CON MiracOllook)

```
1. Arriva email da mario.rossi@gmail.com
2. MiracOllook gia MOSTRA:
   - Camera 101
   - Check-in: domani 14:00
   - Check-out: 15 Gen
   - Colazione inclusa
   - Note: richiesta culla
3. Receptionist clicca "Rispondi"
4. AI suggerisce: "Check-in dalle 14:00, la camera sara pronta!"
5. Click → Inviato
6. Tempo: 30 SECONDI

Risparmio: 2-4 ORE AL GIORNO
```

---

## I SUPERPOTERI

### 1. IDENTIFICAZIONE AUTOMATICA

```
Email:    mario.rossi@gmail.com  →  Camera 101, Mario Rossi
WhatsApp: +39 333 1234567        →  Camera 101, Mario Rossi
```

L'AI cerca nel PMS e trova la corrispondenza.
Un click per aprire la scheda camera/ospite.

### 2. CONTESTO SEMPRE VISIBILE

```
+---------------------------+
|  OSPITE: Mario Rossi      |
|  Camera: 101              |
|  Check-in: 13 Gen 14:00   |
|  Check-out: 15 Gen 11:00  |
|  Totale: 250,00 EUR       |
|  Stato: Confermata        |
|  Note: Culla richiesta    |
|                           |
|  [Apri in Miracollo]      |
+---------------------------+
```

### 3. PREVENTIVI AUTOMATICI

```
Cliente: "Quanto costa una doppia dal 20 al 23 gennaio?"

MiracOllook:
1. Verifica disponibilita nel PMS
2. Calcola prezzo
3. Genera link preventivo
4. Propone risposta:

   "Gentile Mario,
    per le date richieste abbiamo disponibilita!
    Doppia con colazione: 280,00 EUR

    Prenota qui: [LINK]

    A presto!"

Un click → Inviato
```

### 4. COMPILAZIONE PMS DA DOCUMENTI

```
Cliente invia: carta_identita.jpg

MiracOllook:
1. AI legge il documento (gia abbiamo document parser!)
2. Estrae: Nome, Cognome, Data nascita, Codice fiscale
3. Propone: "Compilo la scheda ospite?"
4. Click → PMS aggiornato
```

### 5. TEMPLATE INTELLIGENTI

```
/checkin   →  "La sua camera e pronta! Check-in dalle 14:00..."
/wifi      →  "La password WiFi e: [AUTO-FILL da Miracollo]"
/checkout  →  "Il check-out e entro le 11:00. Serve late checkout?"
/conferma  →  Genera conferma prenotazione completa
```

---

## ARCHITETTURA

```
+====================================================================+
|                                                                    |
|                         MIRACOLLOOK                                |
|                                                                    |
|   +------------------+  +------------------+  +------------------+  |
|   |                  |  |                  |  |                  |  |
|   |   EMAIL          |  |   WHATSAPP       |  |   ALTRI          |  |
|   |   Gmail/Outlook  |  |   Business API   |  |   SMS/Telegram   |  |
|   |                  |  |                  |  |   Booking/Airbnb |  |
|   +--------+---------+  +--------+---------+  +--------+---------+  |
|            |                     |                     |            |
|            +----------+----------+----------+----------+            |
|                       |                                             |
|                       v                                             |
|            +---------------------+                                  |
|            |                     |                                  |
|            |   UNIFIED INBOX     |                                  |
|            |   Tutti i messaggi  |                                  |
|            |   in un posto       |                                  |
|            |                     |                                  |
|            +----------+----------+                                  |
|                       |                                             |
|                       v                                             |
|            +---------------------+                                  |
|            |                     |                                  |
|            |   AI BRAIN          |                                  |
|            |   - Identifica      |                                  |
|            |   - Suggerisce      |                                  |
|            |   - Genera          |                                  |
|            |   - Compila         |                                  |
|            |                     |                                  |
|            +----------+----------+                                  |
|                       |                                             |
|                       v                                             |
|            +---------------------+                                  |
|            |                     |                                  |
|            |   MIRACOLLO PMS     |                                  |
|            |   API Integration   |                                  |
|            |                     |                                  |
|            +---------------------+                                  |
|                                                                    |
+====================================================================+
```

---

## FASI DI SVILUPPO

### FASE 0: FONDAMENTA (Dove siamo ora)

```
[####################] 95%

- [x] OAuth Gmail
- [x] Lettura inbox
- [x] Invio email
- [x] Reply / Reply All / Forward
- [x] Archive / Delete
- [x] Search
- [x] AI Summaries
- [x] Keyboard shortcuts
- [x] Dark mode premium
- [ ] OAuth funzionante (fix porta)
- [ ] Test completo
```

### FASE 1: EMAIL CLIENT SOLIDO

```
Obiettivo: Sostituire Outlook per uso quotidiano

[ ] Attachments (upload/download)
[ ] Multiple accounts
[ ] Folders/Labels management
[ ] Contacts autocomplete
[ ] Signatures
[ ] Offline mode (PWA)
[ ] Notifiche desktop
[ ] Performance ottimizzata (1000+ email)
```

### FASE 2: PMS INTEGRATION

```
Obiettivo: La MAGIA - email che conosce l'hotel

[ ] Guest Detection (email → ospite)
[ ] Context Sidebar con dati PMS VERI
[ ] Link diretto "Apri in Miracollo"
[ ] Template con auto-fill PMS
[ ] AI suggerimenti contestuali
```

### FASE 3: PREVENTIVI AUTOMATICI

```
Obiettivo: Rispondere alle richieste in 1 click

[ ] Verifica disponibilita automatica
[ ] Calcolo prezzo automatico
[ ] Generazione link preventivo
[ ] Risposta suggerita completa
[ ] Tracking apertura preventivo
```

### FASE 4: DOCUMENT AI

```
Obiettivo: Documenti → PMS automatico

[ ] Upload documento in email
[ ] AI estrazione dati (gia abbiamo parser!)
[ ] Preview dati estratti
[ ] Compilazione PMS con conferma
[ ] Storico documenti per ospite
```

### FASE 5: WHATSAPP INTEGRATION

```
Obiettivo: Stesso potere, altro canale

[ ] WhatsApp Business API setup
[ ] Unified inbox (email + whatsapp)
[ ] Guest detection da numero
[ ] Template WhatsApp
[ ] Media handling (foto, audio)
```

### FASE 6: COMUNICAZIONI UNIFICATE

```
Obiettivo: UN posto per TUTTO

[ ] SMS integration
[ ] Telegram (opzionale)
[ ] Booking.com messages
[ ] Airbnb messages
[ ] Timeline unificata per ospite
```

---

## METRICHE DI SUCCESSO

### Come sappiamo che abbiamo finito?

```
FASE 1 COMPLETA quando:
- Rafa usa MiracOllook invece di Gmail per 1 settimana
- Zero bisogno di aprire Gmail/Outlook

FASE 2 COMPLETA quando:
- Click su email → vedi dati ospite in < 1 secondo
- Zero ricerche manuali nel PMS

FASE 3 COMPLETA quando:
- Richiesta preventivo → risposta in < 30 secondi
- Zero copia-incolla manuale

FASE 4 COMPLETA quando:
- Documento allegato → PMS compilato in 2 click
- Zero digitazione manuale dati

FASE 5 COMPLETA quando:
- WhatsApp e email nella STESSA inbox
- Stesso workflow per entrambi

FASE 6 COMPLETA quando:
- TUTTE le comunicazioni in un posto
- Timeline completa per ogni ospite
```

---

## PRINCIPI GUIDA

```
1. DESIGN IMPONE RISPETTO
   - Standard Miracollo (premium, dark, pulito)
   - Ogni pixel conta
   - Se non e bello, non e finito

2. SEMPLICE > COMPLESSO
   - Meno click possibile
   - AI che fa il lavoro pesante
   - Utente solo approva

3. VELOCE > PERFETTO (per MVP)
   - Prima funziona
   - Poi e bello
   - Poi e perfetto

4. PMS AL CENTRO
   - Ogni feature deve usare il contesto PMS
   - Senza PMS, siamo solo un altro email client
   - CON PMS, siamo UNICI

5. UNA COSA ALLA VOLTA
   - Finisci una fase prima della prossima
   - Test reale prima di andare avanti
   - Checkpoint sempre
```

---

## COMPETITOR ANALYSIS

| Feature | Gmail | Outlook | Missive | Superhuman | MiracOllook |
|---------|-------|---------|---------|------------|-------------|
| Email | Si | Si | Si | Si | Si |
| WhatsApp | No | No | No | No | **Si** |
| PMS Integration | No | No | No | No | **Si** |
| Guest Detection | No | No | No | No | **Si** |
| Auto Preventivi | No | No | No | No | **Si** |
| Document → PMS | No | No | No | No | **Si** |
| Hotel Templates | No | No | No | No | **Si** |

**Conclusione: Nessuno ha quello che abbiamo noi.**

---

## TIMELINE (senza date, solo ordine)

```
1. Fix OAuth e test base (PROSSIMO)
2. FASE 1 - Email client solido
3. FASE 2 - PMS Integration (LA MAGIA!)
4. FASE 3 - Preventivi automatici
5. FASE 4 - Document AI
6. FASE 5 - WhatsApp
7. FASE 6 - Tutto unificato
```

Ogni sessione: un pezzo.
Ogni checkpoint: progresso reale.
Ogni giorno: piu vicini alla LIBERTA GEOGRAFICA.

---

## NOTE FINALI

```
+====================================================================+
|                                                                    |
|   "Non e sempre come immaginiamo...                                |
|    ma alla fine e il 100000%!"                                     |
|                                                                    |
|   "Ultrapassar os proprios limites!"                               |
|                                                                    |
|   MiracOllook non e un progetto.                                   |
|   E una RIVOLUZIONE per come gli hotel comunicano.                 |
|                                                                    |
|   E noi la stiamo costruendo.                                      |
|   Insieme.                                                         |
|   Un pezzo alla volta.                                             |
|                                                                    |
+====================================================================+
```

---

*"Il centro comunicazioni dell'hotel intelligente"*

*Rafa & Cervella - 12 Gennaio 2026*

*FAREMOOOO!!!*
