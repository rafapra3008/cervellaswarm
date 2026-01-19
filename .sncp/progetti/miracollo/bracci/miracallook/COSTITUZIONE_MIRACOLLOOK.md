# COSTITUZIONE - Miracollook

```
+====================================================================+
|                                                                    |
|   "Non e un email client.                                          |
|    E l'Outlook che CONOSCE il tuo hotel."                          |
|                                                                    |
|   LAVORIAMO IN PACE! SENZA CASINO! DIPENDE DA NOI!                |
|                                                                    |
+====================================================================+
```

> Creato: 13 Gennaio 2026 - Sessione 181
> **AGGIORNATO: 19 Gennaio 2026 - Verifica Codice REALE**
> Autori: Rafa & Cervella

---

## IL NOSTRO NORD

**Miracollook** = Il Centro Comunicazioni dell'Hotel Intelligente

```
NON siamo:
- Un altro email client
- Una copia di Gmail/Outlook
- Un progetto "nice to have"

SIAMO:
- L'UNICO email client che CONOSCE il tuo hotel
- Il posto dove l'hotel comunica con il MONDO
- Un pezzo CRITICO della LIBERTA GEOGRAFICA
```

**NESSUN competitor ha questo. NESSUNO.**

---

## I 5 PRINCIPI SACRI

### 1. PMS AL CENTRO

```
Senza PMS integration = solo un altro email client
CON PMS integration = MAGIA

Ogni feature deve chiedersi:
"Come uso i dati dell'hotel per fare questo MEGLIO?"
```

### 2. DESIGN IMPONE RISPETTO

```
Standard Miracollo:
- Premium, dark, pulito
- Ogni pixel conta
- Se non e bello, non e finito

L'UI di Miracollook deve far dire:
"WOW, questo e SERIO!"
```

### 3. SEMPLICE > COMPLESSO

```
- Meno click possibile
- AI fa il lavoro pesante
- Utente solo approva

30 SECONDI per rispondere a una email.
Non 3-5 minuti come oggi.
```

### 4. REALE > SU CARTA

```
"Su carta" = Codice scritto, documentazione
"Reale" = Funziona, testato, USATO

MAI dire "e fatto" se non e REALE!
```

### 5. UNA COSA ALLA VOLTA

```
- Finisci una fase prima della prossima
- Test REALE prima di andare avanti
- Checkpoint SEMPRE
```

---

## LE 6 FASI (STATO REALE - 19 Gennaio 2026 - Verificato dal CODICE!)

```
FASE 0: FONDAMENTA         [####################] 100% COMPLETA!
        OAuth + Inbox + Send + Reply + Archive + Search + AI

FASE P: PERFORMANCE        [####################] 100% COMPLETA!
        IndexedDB + Batch API + Skeleton + Prefetch + PWA

FASE 1: EMAIL SOLIDO       [##################..] 92%  ← VERIFICATO!
        Resizable, Context Menu, Thread, Drafts, Attachments FATTI!
        MANCA: Bulk Actions API, Labels CRUD, Contacts, Settings

FASE 2: PMS INTEGRATION    [....................] 0%
        LA MAGIA! Guest detection, context sidebar
        QUI DIVENTIAMO UNICI!

FASE 3: PREVENTIVI AUTO    [....................] 0%
        Richiesta → risposta in 1 click

FASE 4: DOCUMENT AI        [....................] 0%
        Documenti → PMS automatico

FASE 5: WHATSAPP           [....................] 0%
        Email + WhatsApp = unified inbox

FASE 6: TUTTO UNIFICATO    [....................] 0%
        SMS, Telegram, Booking, Airbnb
```

**REGOLA: Completare FASE N prima di iniziare FASE N+1**

---

## METRICHE DI SUCCESSO

### Come sappiamo che una FASE e COMPLETA?

```
FASE 0 COMPLETA quando:
- Login OAuth funziona al primo click
- Rafa puo leggere/inviare/rispondere
- Token persistono al restart

FASE 1 COMPLETA quando:
- Rafa usa Miracollook invece di Gmail per 1 SETTIMANA
- Zero bisogno di aprire Gmail/Outlook

FASE 2 COMPLETA quando:
- Click su email → vedi dati ospite in < 1 secondo
- Zero ricerche manuali nel PMS
- "WOW, sa chi e questo cliente!"

FASE 3 COMPLETA quando:
- Richiesta preventivo → risposta in < 30 secondi
- Zero copia-incolla manuale

FASE 4 COMPLETA quando:
- Documento allegato → PMS compilato in 2 click
- Zero digitazione manuale dati

FASE 5+ COMPLETA quando:
- TUTTE le comunicazioni in UN posto
- Timeline completa per ogni ospite
```

---

## REGOLE OPERATIVE

### Prima di ogni sessione

```
1. LEGGI questo file
2. LEGGI stato.md
3. VERIFICA dove siamo nelle 6 FASI
4. LAVORA sulla fase CORRENTE (non saltare!)
```

### Durante la sessione

```
1. UNA cosa alla volta
2. TEST dopo ogni implementazione
3. CHECKPOINT ogni 30-45 minuti
4. AGGIORNA stato.md mentre lavori
```

### Fine sessione

```
1. AGGIORNA stato.md
2. AGGIORNA NORD se serve
3. GIT commit + push
4. HANDOFF chiaro per prossima sessione
```

---

## REGOLA CONSULENZA ESPERTI

```
+====================================================================+
|                                                                    |
|   LA REGINA ORCHESTRA, NON FA TUTTO DA SOLA!                       |
|                                                                    |
|   Prima di implementare, CONSULTA l'esperta:                       |
|                                                                    |
|   UI/UX/Design    → cervella-marketing                             |
|   Database/Query  → cervella-data                                  |
|   Sicurezza       → cervella-security                              |
|   Deploy/Infra    → cervella-devops                                |
|   Architettura    → cervella-ingegnera                             |
|   Ricerca tecnica → cervella-researcher                            |
|                                                                    |
|   PROCESSO:                                                        |
|   1. Regina chiede all'esperta: "Come dovrebbe essere X?"          |
|   2. Esperta propone/valida                                        |
|   3. Worker implementa quello che dice l'esperta                   |
|   4. Guardiana verifica qualita                                    |
|                                                                    |
|   MAI saltare questo processo per UI visibili all'utente!          |
|                                                                    |
+====================================================================+
```

### Perche questa regola?

```
13 Gennaio 2026 - Sessione 181

ERRORE: Frontend ha creato LoginPage senza consultare Marketing
RISULTATO: Una "C" gigante orribile che non rispetta il brand

LEZIONE: "DESIGN IMPONE RISPETTO" richiede che chi fa design
         sia CONSULTATO prima di implementare!

"Fatto BENE > Fatto VELOCE"
```

---

## ARCHITETTURA OBBLIGATORIA

### Stack (non cambiare!)

```
BACKEND:
- FastAPI + Python 3.11+
- Google Gmail API
- Anthropic Claude API (Haiku per summaries)
- SQLite dev / PostgreSQL prod
- Porta: 8002

FRONTEND:
- React 19 + TypeScript
- Vite
- Tailwind CSS v4
- TanStack Query v5
- Porta: 5173
```

### Repository

```
Path: ~/Developer/miracollogeminifocus/miracallook
(Miracollook e dentro il monorepo Miracollo)

SNCP: ~/Developer/CervellaSwarm/.sncp/progetti/miracollo/bracci/miracallook/
```

---

## FILE SACRI

| File | Cosa contiene | Quando leggerlo |
|------|---------------|-----------------|
| INDICE.md | Come navigare questa cartella | Prima di cercare |
| COSTITUZIONE_MIRACOLLOOK.md | Questo file - le REGOLE | Inizio OGNI sessione |
| NORD_MIRACOLLOOK.md | La VISIONE e prossimi step | Quando perso |
| stato.md | Stato REALE dal codice | Inizio + fine sessione |
| MAPPA_VERITA_20260119.md | Analisi codice completa | Reference tecnico |
| PROMPT_RIPRESA_miracollook.md | Checkpoint sessioni | Riprendere lavoro |

---

## DECISIONI GIA PRESE

### 1. Nome: Miracollook (non MiracOllook, non Miracallook)
```
PERCHE: Semplice, chiaro, una parola
```

### 2. Porta 8002 per backend
```
PERCHE: 8000/8001 usate da altri progetti
```

### 3. SQLite per dev, PostgreSQL per prod
```
PERCHE: Semplicita dev, robustezza prod
```

### 4. Modal separati per Reply/Forward
```
PERCHE: UX piu chiara, meno complessita
```

### 5. P0→P1→P2 STRICT
```
PERCHE: No feature creep, focus su una cosa
```

---

## SE IN DUBBIO

```
+====================================================================+
|                                                                    |
|   1. Rifa' questo file                                             |
|   2. Guarda le 6 FASI - dove siamo?                                |
|   3. Lavora SOLO sulla fase corrente                               |
|   4. Se ancora perso: chiedi a Rafa                                |
|                                                                    |
+====================================================================+
```

---

## CITAZIONI GUIDA

```
"Lavoriamo in pace! Senza casino! Dipende da noi!"

"Non e sempre come immaginiamo... ma alla fine e il 100000%!"

"Ultrapassar os proprios limites!"

"REALE > Su carta"

"Fatto BENE > Fatto VELOCE"
```

---

## PROSSIMO STEP (19 Gennaio 2026)

```
+====================================================================+
|                                                                    |
|   COMPLETARE FASE 1 (92% -> 100%)                                  |
|                                                                    |
|   GIA FATTO (verificato nel codice):                               |
|   [x] Mark Read/Unread - useEmailHandlers.ts + API                 |
|   [x] Drafts - useDraft.ts (212L) + 6 endpoint                     |
|   [x] Thread View - ThreadView.tsx (299L)                          |
|   [x] Upload Attachments - AttachmentPicker.tsx + API              |
|   [x] Resizable Panels - ThreePanelResizable.tsx                   |
|   [x] Context Menu - EmailContextMenu.tsx (280L)                   |
|   [x] Design Salutare - colori corretti                            |
|                                                                    |
|   DA FARE (~21h):                                                  |
|   [ ] Bulk Actions API backend       (4h) - UI frontend pronta!    |
|   [ ] Labels CRUD API backend        (3h) - UI disabled            |
|   [ ] Contacts Autocomplete          (6h)                          |
|   [ ] Settings Page                  (8h)                          |
|                                                                    |
|   Quando FASE 1 = 100% → inizia FASE 2 (PMS = LA MAGIA!)          |
|                                                                    |
+====================================================================+
```

---

## REGOLA ANTI-BUGIE (Aggiunta 15 Gennaio 2026)

```
+====================================================================+
|                                                                    |
|   15 GENNAIO 2026 - LEZIONE APPRESA                                |
|                                                                    |
|   Abbiamo scoperto che la documentazione diceva "FATTO"            |
|   per 20+ ore di lavoro che NON era mai stato fatto.               |
|                                                                    |
|   VIOLAZIONE: "SU CARTA != REALE"                                  |
|                                                                    |
|   NUOVA REGOLA:                                                    |
|                                                                    |
|   MAI scrivere "FATTO" o "IMPLEMENTATO" senza:                     |
|   1. Codice SCRITTO nel repository                                 |
|   2. Codice COMMITTATO (git commit)                                |
|   3. Feature TESTATA (funziona davvero)                            |
|                                                                    |
|   DISTINZIONI:                                                     |
|   - "RICERCA FATTA" = Ho studiato, ho specs                        |
|   - "SPECS PRONTE" = Design deciso, pronto per codice              |
|   - "IMPLEMENTATO" = Codice scritto + committato + testato         |
|                                                                    |
|   Chi viola questa regola TRADISCE la fiducia del team.            |
|                                                                    |
+====================================================================+
```

---

*"Il centro comunicazioni dell'hotel intelligente"*

*Rafa & Cervella - 13 Gennaio 2026*
*Aggiornato: 15 Gennaio 2026 - Regola Anti-Bugie*

*FAREMOOOO!!!*
