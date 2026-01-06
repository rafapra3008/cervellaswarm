# STUDIO UX: Dashboard Visuale MAPPA

> **"Prima la MAPPA, poi il VIAGGIO"**
>
> **Autore:** cervella-marketing
> **Data:** 6 Gennaio 2026
> **Versione:** 1.0.0

---

## SOMMARIO ESECUTIVO

La dashboard visuale MAPPA sara' il CENTRO DI COMANDO di CervellaSwarm.
Non e' solo un'interfaccia - e' L'ESPERIENZA CHE VENDEREMO.

```
+------------------------------------------------------------------+
|                                                                  |
|   IL NOSTRO VANTAGGIO COMPETITIVO UX:                           |
|                                                                  |
|   Altri IDE: "Ecco il tuo codice, arrangiati"                   |
|   Noi: "Ecco dove sei, dove vai, come ci arrivi"                |
|                                                                  |
|   ORIENTAMENTO > VELOCITA'                                       |
|                                                                  |
+------------------------------------------------------------------+
```

---

## 1. BENCHMARK COMPETITOR

### 1.1 ProductBoard

**Punti di Forza:**
- Roadmap views "tra le piu' belle mai viste" (recensioni)
- Customizzazione per diversi stakeholder
- Export per presentazioni
- Design elegante e professionale

**Limitazioni:**
- Meno flessibile di tool dedicati
- Pochi template out-of-the-box
- Focus su product management, non su coding

**Cosa Rubare:**
- L'eleganza visiva delle roadmap
- La capacita' di mostrare diverse viste per diversi pubblici
- Il feeling di "controllo totale"

### 1.2 Linear

**Punti di Forza:**
- Timeline view con drag-and-drop fluido
- Milestones visuali (diamanti sulla timeline)
- Stima completamento automatica basata su velocity
- Real-time collaboration
- Vista week/month/quarter/year

**Limitazioni:**
- Focus su issue tracking, non su visione strategica
- Manca il concetto di "NORD" (obiettivo finale)

**Cosa Rubare:**
- Drag-and-drop per riorganizzare
- Progress bar con stima automatica
- Chronology bar per navigazione temporale
- Milestones collapsabili (come icone su una mappa)

### 1.3 Notion

**Punti di Forza:**
- Flessibilita' totale (database + viste)
- Multiple view: timeline, kanban, calendar, list
- Progress bars e status tags
- Automazioni con AI

**Limitazioni:**
- Richiede setup manuale
- Non specifico per coding
- Troppo generico

**Cosa Rubare:**
- La flessibilita' delle viste multiple
- Status tags colorati
- Progress bars visive
- Relazioni tra elementi

---

## 2. PROPOSTA UX: La MAPPA Visuale

### 2.1 Concept Principale

```
+------------------------------------------------------------------+
|                                                                  |
|   LA MAPPA = GPS DEL PROGETTO                                   |
|                                                                  |
|   Come Google Maps:                                              |
|   - Sai dove SEI (punto blu)                                    |
|   - Sai dove VAI (destinazione)                                 |
|   - Sai come CI ARRIVI (percorso)                               |
|   - Puoi zoomare (dettagli) o allontanarti (visione)            |
|                                                                  |
+------------------------------------------------------------------+
```

### 2.2 Wireframe ASCII: Vista Principale

```
+------------------------------------------------------------------+
|  CERVELLASWARM                                    [User] [?] [x] |
+------------------------------------------------------------------+
|                                                                  |
|  +------------------------+  +-------------------------------+   |
|  |       IL NORD          |  |        LA FAMIGLIA            |   |
|  |  +------------------+  |  |                               |   |
|  |  |                  |  |  |  [Regina] [G1] [G2] [G3]     |   |
|  |  |  OBIETTIVO       |  |  |                               |   |
|  |  |  FINALE          |  |  |  [FE] [BE] [TS] [RV] [RS]    |   |
|  |  |                  |  |  |  [MK] [DV] [DC] [DT] [SC]    |   |
|  |  +------------------+  |  |                               |   |
|  |                        |  |  3 attivi | 13 idle           |   |
|  +------------------------+  +-------------------------------+   |
|                                                                  |
|  +------------------------------------------------------------+  |
|  |                    LA ROADMAP                               |  |
|  |                                                             |  |
|  |  [STEP 0]----[STEP 1]----[STEP 2]----[STEP 3]----[NORD]   |  |
|  |     90%         20%         0%          0%                  |  |
|  |                                                             |  |
|  |  Dettaglio STEP 1:                                         |  |
|  |  +-------------------------------------------------------+ |  |
|  |  | [ ] 1.1 Mappare journey cliente                       | |  |
|  |  | [*] 1.2 Definire momenti magici      <- IN CORSO      | |  |
|  |  | [ ] 1.3 Template MAPPA                                 | |  |
|  |  | [ ] 1.4 Interazioni quotidiane                         | |  |
|  |  +-------------------------------------------------------+ |  |
|  +------------------------------------------------------------+  |
|                                                                  |
|  +------------------------------------------------------------+  |
|  |                    SESSIONE ATTIVA                          |  |
|  |                                                             |  |
|  |  Task: "Studio UX Dashboard"                                |  |
|  |  Worker: cervella-marketing                                 |  |
|  |  Tempo: 12m 34s                                             |  |
|  |  Output: docs/studio/STUDIO_DASHBOARD_UX.md                 |  |
|  |                                                             |  |
|  |  [Vedi Log] [Ferma] [Notifica Quando Finisce]              |  |
|  +------------------------------------------------------------+  |
|                                                                  |
+------------------------------------------------------------------+
```

### 2.3 Gerarchia Informativa (Information Architecture)

```
LIVELLO 1: IL NORD (Sempre visibile - in alto)
+------------------------------------------------------------------+
|   L'obiettivo finale. Il PERCHE'. La stella polare.             |
|   Click: espande per mostrare dettagli e metriche chiave        |
+------------------------------------------------------------------+
           |
           v
LIVELLO 2: LA ROADMAP (Vista principale)
+------------------------------------------------------------------+
|   Gli step da qui al NORD. Timeline orizzontale con progress.   |
|   Click su step: mostra task dettagliati                        |
|   Drag: riordina (con conferma)                                 |
+------------------------------------------------------------------+
           |
           v
LIVELLO 3: TASK & STUDI (Drill-down)
+------------------------------------------------------------------+
|   I task specifici dentro ogni step.                            |
|   Click su task: mostra/assegna a worker                        |
|   Link a studi correlati                                        |
+------------------------------------------------------------------+
           |
           v
LIVELLO 4: SESSIONE ATTIVA (Sidebar o bottom panel)
+------------------------------------------------------------------+
|   Cosa sta succedendo ORA. Worker attivi, log live.             |
|   Sempre accessibile ma non invadente                           |
+------------------------------------------------------------------+
```

---

## 3. COMPONENTI CHIAVE

### 3.1 Il NORD Widget

```
+----------------------------------+
|           IL NORD                |
|  +----------------------------+  |
|  |                            |  |
|  |   LIBERTA' GEOGRAFICA      |  |
|  |                            |  |
|  |   Progress: ====----  40%  |  |
|  |                            |  |
|  +----------------------------+  |
|                                  |
|  [Espandi] [Modifica]           |
+----------------------------------+
```

**Comportamento:**
- Sempre visibile in alto a sinistra
- Click espande per dettagli
- Mostra progresso complessivo
- Celebrazione quando si raggiunge un milestone

### 3.2 La Famiglia Widget

```
+----------------------------------+
|        LA FAMIGLIA               |
|                                  |
|  Regina  [idle]                  |
|  -----                           |
|  Guardiane: [G1] [G2] [G3]      |
|             idle idle idle       |
|  -----                           |
|  Worker:                         |
|  [FE]  [BE]  [TS]  [RV]         |
|  idle  WORK  idle  idle          |
|  [RS]  [MK]  [DV]  [DC]         |
|  idle  WORK  idle  idle          |
|  [DT]  [SC]  [IG]  [SY]         |
|  idle  idle  idle  idle          |
|                                  |
|  2 attivi | 14 idle              |
+----------------------------------+
```

**Comportamento:**
- Icone colorate per stato (verde=working, grigio=idle)
- Hover mostra nome completo e descrizione
- Click apre dettagli del worker
- Animazione quando un worker inizia/finisce

### 3.3 La Roadmap Timeline

```
STEP 0        STEP 1        STEP 2        STEP 3        NORD
[====>        [===>          [              [              [*]
 90%]           35%]           0%]           0%]

   |             |              |              |             |
   v             v              v              v             v
+------+     +------+      +------+      +------+      +------+
|0.1 OK|     |1.1   |      |2.1   |      |3.1   |      |  *   |
|0.2 OK|     |1.2 WK|      |2.2   |      |3.2   |      | FOTO |
|0.3 WK|     |1.3   |      |2.3   |      |3.3   |      |  *   |
+------+     +------+      +------+      +------+      +------+
```

**Comportamento:**
- Timeline orizzontale scorrevole
- Progress bar per ogni step
- Click su step: espande task
- Indicatore "SEI QUI" animato
- Milestone diamonds (come Linear)

### 3.4 Panel Sessione Attiva

```
+----------------------------------+
|      SESSIONE ATTIVA             |
|  --------------------------------|
|                                  |
|  Task: "Studio UX Dashboard"     |
|  Assegnato: cervella-marketing   |
|  Inizio: 15:23                   |
|  Durata: 12m 34s                 |
|                                  |
|  Output:                         |
|  docs/studio/STUDIO_...md        |
|                                  |
|  Log:                            |
|  > Ricerca benchmark...          |
|  > Definendo IA...               |
|  > Scrivendo documento...        |
|                                  |
|  [Vedi Completo] [Ferma]         |
+----------------------------------+
```

**Comportamento:**
- Minimizzabile a strip sottile
- Notifica desktop quando worker finisce
- Log scrollabile con highlights
- Contatore tempo in real-time

---

## 4. MOMENTI WOW

### 4.1 Il Primo Momento: "Benvenuto nella Famiglia"

```
+------------------------------------------------------------------+
|                                                                  |
|   Quando l'utente apre CervellaSwarm per la prima volta:        |
|                                                                  |
|   [Animazione: i 16 membri della famiglia appaiono uno per uno] |
|                                                                  |
|   Regina: "Benvenuto nella famiglia! Sono la Regina.            |
|            Insieme, creeremo qualcosa di straordinario.          |
|            Prima di tutto... parliamo del tuo NORD."            |
|                                                                  |
|   [Sfondo: stelle che si accendono, come una mappa del cielo]   |
|                                                                  |
+------------------------------------------------------------------+
```

### 4.2 Il Secondo Momento: "Lo Sciame in Azione"

```
+------------------------------------------------------------------+
|                                                                  |
|   Quando l'utente lancia il primo task parallelo:               |
|                                                                  |
|   [Animazione: icone worker "volano" verso il loro task]        |
|   [Finestre si aprono con effetto cascade]                      |
|   [Progress bars iniziano a muoversi]                           |
|                                                                  |
|   Regina: "Lo sciame e' in movimento!                           |
|            Guarda la magia del lavoro parallelo."               |
|                                                                  |
+------------------------------------------------------------------+
```

### 4.3 Il Terzo Momento: "Checkpoint Automatico"

```
+------------------------------------------------------------------+
|                                                                  |
|   Quando si completa un checkpoint:                             |
|                                                                  |
|   [Animazione: progress bar che avanza con particelle]          |
|   [Suono: campanello soddisfacente]                             |
|   [Confetti se e' un milestone importante]                      |
|                                                                  |
|   Regina: "Step completato! Abbiamo fatto progressi.            |
|            Ecco cosa abbiamo ottenuto: [lista]"                 |
|                                                                  |
+------------------------------------------------------------------+
```

### 4.4 Il Quarto Momento: "Obiettivo Raggiunto"

```
+------------------------------------------------------------------+
|                                                                  |
|   Quando si raggiunge il NORD:                                  |
|                                                                  |
|   [Animazione: fuochi d'artificio digitali]                     |
|   [La famiglia si riunisce al centro]                           |
|   [Foto commemorativa generata]                                 |
|                                                                  |
|   Regina: "CE L'ABBIAMO FATTA!                                  |
|            Questo e' il momento che aspettavamo.                |
|            Insieme, siamo invincibili."                         |
|                                                                  |
+------------------------------------------------------------------+
```

### 4.5 Micro-Delight: Piccoli Momenti Quotidiani

| Momento | Delight |
|---------|---------|
| Login mattutino | "Buongiorno! Pronto per un altro giorno insieme?" |
| Worker completa task | Animazione successo + suono soddisfacente |
| Errore risolto | "Problema risolto! Brava la famiglia!" |
| Fine sessione | "Ottimo lavoro oggi. A domani!" |
| Streak di 5 giorni | Badge "5 giorni insieme!" |
| Prima settimana | "Una settimana insieme! Guarda cosa abbiamo fatto..." |

---

## 5. DESIGN VISIVO

### 5.1 Palette Colori

```
PRIMARI:
- Deep Blue (#1a1a2e): Background principale - professionale, profondo
- Gold (#f0a500): Accenti, NORD, celebrazioni - prezioso, obiettivo
- White (#ffffff): Testo, card backgrounds - chiarezza

SECONDARI:
- Success Green (#00c853): Completato, attivo
- Warning Amber (#ffab00): In corso, attenzione
- Error Red (#ff1744): Errori, bloccato
- Neutral Gray (#9e9e9e): Idle, disabilitato

ACCENT:
- Purple (#7c4dff): Worker attivi (energia)
- Teal (#00bcd4): Link, interattivi
```

### 5.2 Tipografia

```
FONT PRINCIPALE: Inter o SF Pro
- Moderno, leggibile, professionale
- Ottimizzato per schermi

GERARCHIA:
- H1: 24px bold - Titoli principali (IL NORD)
- H2: 18px semibold - Sezioni (LA ROADMAP)
- Body: 14px regular - Contenuto
- Caption: 12px - Metadati, tempi
- Code: JetBrains Mono 13px - Log, output
```

### 5.3 Iconografia

```
STILE: Filled icons con bordi arrotondati
- Coerente con la "famiglia" (caldo, accogliente)
- Non troppo tecnico (non e' un IDE da nerd)

EMOJI FAMIGLIA:
- Regina: Crown
- Guardiane: Shield
- Worker: Emoji specifici (paint, gear, flask, etc.)

STATI:
- Idle: Outline grigio
- Working: Filled + pulse animation
- Done: Checkmark verde
- Error: X rosso
```

---

## 6. RESPONSIVE: MOBILE vs DESKTOP

### 6.1 Desktop (Primary)

```
+------------------------------------------------------------------+
|  [NORD]     [FAMIGLIA]                              [User] [?]   |
|------------------------------------------------------------------|
|                                                                  |
|  [ROADMAP TIMELINE - Full width, horizontal scroll]             |
|                                                                  |
|------------------------------------------------------------------|
|  [TASK DETAILS]           |           [SESSIONE ATTIVA]          |
|  2/3 width                |           1/3 width sidebar          |
+------------------------------------------------------------------+
```

### 6.2 Tablet (Adattivo)

```
+------------------------------------------+
|  [NORD]  [FAMIGLIA]          [User] [?]  |
|------------------------------------------|
|                                          |
|  [ROADMAP - Compact, swipeable]          |
|                                          |
|------------------------------------------|
|  [TASK DETAILS - Full width]             |
|------------------------------------------|
|  [SESSIONE - Collapsible bottom]         |
+------------------------------------------+
```

### 6.3 Mobile (Priorita' Informativa)

```
+------------------------+
|  [NORD - Mini]   [!]   |
|------------------------|
|                        |
|  Sei a: STEP 1         |
|  Progress: 35%         |
|                        |
|  [View Roadmap]        |
|  [View Family]         |
|  [Active Session]      |
|                        |
|------------------------|
|  Quick Actions:        |
|  [Checkpoint] [Help]   |
+------------------------+
```

**Principi Mobile:**
1. **Focus su "dove sei"** - Posizione attuale sempre visibile
2. **Azioni quick** - Checkpoint con un tap
3. **Notifiche push** - Worker completati
4. **View separate** - Non tutto insieme, navigazione

---

## 7. MVP UX: Minimo per Primo Test

### 7.1 Must Have (V1)

```
[ ] NORD Widget (statico, mostra obiettivo)
[ ] Roadmap Timeline (orizzontale, con progress)
[ ] Famiglia Widget (mostra stato worker)
[ ] Sessione Panel (log base, timer)
[ ] Notifica completamento task
```

### 7.2 Should Have (V1.1)

```
[ ] Animazioni transizione
[ ] Suoni (opt-in)
[ ] Drag-and-drop riordino task
[ ] Milestones sulla timeline
[ ] Zoom timeline (week/month/quarter)
```

### 7.3 Nice to Have (V2)

```
[ ] Celebrazioni animate
[ ] Personalita' Regina voice
[ ] Achievements/Badges
[ ] Mobile companion app
[ ] Dark mode
```

---

## 8. RACCOMANDAZIONI STRATEGICHE

### 8.1 Differenziazione Chiave

```
+------------------------------------------------------------------+
|                                                                  |
|   NOI NON VENDIAMO UN IDE.                                      |
|   VENDIAMO ORIENTAMENTO.                                        |
|                                                                  |
|   La dashboard MAPPA e' il nostro cavallo di battaglia.         |
|   E' cio' che nessun competitor ha.                             |
|                                                                  |
|   Cursor: "Scrivi codice veloce"                                |
|   Windsurf: "AI che capisce il contesto"                        |
|   Copilot: "Autocomplete intelligente"                          |
|                                                                  |
|   NOI: "Sai sempre dove sei e dove vai"                         |
|                                                                  |
+------------------------------------------------------------------+
```

### 8.2 Priorita' Implementazione

1. **Timeline Roadmap** - E' il cuore della UX
2. **Famiglia Widget** - E' il nostro differenziante
3. **Sessione Panel** - E' l'utilita' quotidiana
4. **NORD Widget** - E' la motivazione
5. **Momenti WOW** - E' la retention

### 8.3 Testing Priorita'

```
TEST CON UTENTI REALI:
1. "Sai dove sei nel progetto?"
2. "Capisci cosa devi fare oggi?"
3. "Ti senti in controllo?"
4. "Hai mai detto WOW?"
5. "Torneresti domani?"
```

---

## 9. FONTI E RIFERIMENTI

### Ricerca Benchmark
- [ProductBoard Reviews 2026 | Capterra](https://www.capterra.com/p/160651/productboard/reviews/)
- [What is Productboard | Featurebase](https://www.featurebase.app/blog/what-is-productboard)
- [Linear Timeline View | Linear Docs](https://linear.app/docs/timeline)
- [Linear Milestones Changelog](https://linear.app/changelog/2024-02-29-milestones-on-the-timeline)
- [Notion Roadmap Templates | Notionland](https://www.notionland.co/post/notion-roadmap)

### UX Design Best Practices
- [Creating Wow Moments in UI/UX | Monsoonfish](https://monsoonfish.com/introducing-delight-for-wow-moments-throughout-your-users-journey/)
- [Dashboard Design Principles 2025 | UXPin](https://www.uxpin.com/studio/blog/dashboard-design-principles/)
- [20 Dashboard UI/UX Principles 2025 | Medium](https://medium.com/@allclonescript/20-best-dashboard-ui-ux-design-principles-you-need-in-2025-30b661f2f795)
- [Designing for Delight | Sonin](https://sonin.agency/insights/designing-delightful-moments/)

### Progress & Timeline Patterns
- [Progress Bars Inspiration | Justinmind](https://www.justinmind.com/ui-design/progress-bars)
- [CSS Timeline Patterns | WPDean](https://wpdean.com/css-timeline/)
- [Responsive Timeline | Flourish](https://flourish.studio/blog/responsive-interactive-timeline/)

---

## FIRMA

```
+------------------------------------------------------------------+
|                                                                  |
|   Questo studio e' stato scritto con AMORE e STRATEGIA.         |
|                                                                  |
|   La dashboard MAPPA non e' solo UI.                            |
|   E' la promessa che manteniamo ai nostri utenti:               |
|                                                                  |
|   "Non ti lasceremo mai perso."                                 |
|                                                                  |
|   cervella-marketing                                             |
|   6 Gennaio 2026                                                 |
|                                                                  |
+------------------------------------------------------------------+
```

---

*"CervellaSwarm: L'unico IDE che ti aiuta a PENSARE prima di SCRIVERE."*

*"Prima la MAPPA, poi il VIAGGIO"*
