# MAPPA MIRACOLLOOK - LA VERITÀ

> **Creato:** 12 Gennaio 2026 - Sessione 176
> **Aggiornato:** 12 Gennaio 2026 - Sessione 178 (P0 + P1 COMPLETATI!)
> **Metodo:** Analisi codice REALE (non "su carta")
> **Status:** P1 COMPLETATO - PRODUTTIVO!

---

## LA VISIONE

```
+================================================================+
|                                                                |
|   MIRACOLLOOK                                                  |
|   "Il centro comunicazione dell'hotel intelligente"            |
|                                                                |
|   NON è "un altro email client"                                |
|   È l'EMAIL che CAPISCE il tuo hotel!                          |
|                                                                |
|   KILLER FEATURE: Context PMS (Miracollo)                      |
|   - Sappiamo chi è l'ospite                                    |
|   - Sappiamo quando arriva                                     |
|   - Sappiamo cosa ha prenotato                                 |
|   - NESSUN competitor ha questi dati!                          |
|                                                                |
+================================================================+
```

---

## STATO REALE - 12 Gennaio 2026 (POST P1!)

### Backend (98% funzionale)

```
COMPLETATO E FUNZIONANTE:
[x] OAuth Gmail (login/logout/callback)
[x] Lettura inbox + singola email
[x] Invio email (send con CC/BCC/HTML)
[x] Reply (thread-aware)
[x] Reply All (To + Cc destinatari)           ← NUOVO P1.3!
[x] Forward
[x] AI Summarization (Claude Haiku)
[x] AI Batch Summaries (/inbox/summaries)     ← NUOVO P1.4!
[x] Labels Gmail
[x] Search Gmail (/gmail/search?q=...)        ← NUOVO P1.1!
[x] Archive email (POST /gmail/archive)
[x] Trash email (POST /gmail/trash)
[x] Untrash email (POST /gmail/untrash)
[x] Database SQLite per token persistence

DA FARE (P2):
[ ] Multi-user support
[ ] Token auto-refresh
[ ] Guest Detection (PMS integration)
[ ] Rate limiting API AI
```

### Frontend (98% funzionale)

```
COMPLETATO E FUNZIONANTE:
[x] Layout ThreePanel (200px + 320px + flex + 280px)
[x] Sidebar 8 categorie
[x] EmailList con scroll + AI summaries       ← NUOVO P1.4!
[x] EmailDetail vista completa
[x] GuestSidebar (con MOCK data)
[x] Keyboard Shortcuts TUTTI (J/K/C/R/A/F/E/#// + Shift+R)
[x] Cmd+K Command Palette
[x] Smart Bundles 11 regole
[x] Design System Premium (Miracollo colors)
[x] Dark Mode
[x] ComposeModal FUNZIONANTE (CC/BCC, error handling, Cmd+Enter)
[x] ReplyModal FUNZIONANTE (quoted text, Cmd+Enter)
[x] ReplyAllModal FUNZIONANTE (tutti destinatari) ← NUOVO P1.3!
[x] ForwardModal FUNZIONANTE (body_prefix, Cmd+Enter)
[x] Archive con feedback toast
[x] Delete con confirm + toast
[x] Search UI con SearchBar + debounce       ← NUOVO P1.1!
[x] Refresh/Sync con bottone + Shift+R       ← NUOVO P1.5!
[x] "Last synced" timestamp                   ← NUOVO P1.5!

DA FARE (P2):
[ ] VIP/Check-in auto (usa MOCK, non PMS reale)
```

### STATO ATTUALE

```
+================================================================+
|                                                                |
|   MiracOllook ORA È PRODUTTIVO!                                |
|                                                                |
|   [x] Puoi LEGGERE email                                       |
|   [x] Puoi INVIARE email (C)                                   |
|   [x] Puoi RISPONDERE (R)                                      |
|   [x] Puoi RISPONDERE A TUTTI (A)           ← NUOVO!           |
|   [x] Puoi INOLTRARE (F)                                       |
|   [x] Puoi ARCHIVIARE (E)                                      |
|   [x] Puoi ELIMINARE (#)                                       |
|   [x] Puoi CERCARE (/)                      ← NUOVO!           |
|   [x] Puoi REFRESHARE (Shift+R)             ← NUOVO!           |
|   [x] Vedi AI SUMMARIES in lista            ← NUOVO!           |
|   [x] Token PERSISTONO al restart                              |
|                                                                |
|   = DA USABILE A PRODUTTIVO!                                   |
|                                                                |
+================================================================+
```

---

## PRIORITÀ - COSA FARE E IN CHE ORDINE

### P0 - CRITICO - COMPLETATO!

```
████████████████████ 100% COMPLETATO!

[x] P0.1 Fix ComposeModal (CC/BCC, error handling, Cmd+Enter)
[x] P0.2 Creare ReplyModal (quoted text, success feedback)
[x] P0.3 Creare ForwardModal (body_prefix, preview)
[x] P0.4 Archive/Delete (backend endpoints + frontend hooks + toast)
[x] P0.5 Database Token (SQLite, persistenza al restart)

Sessione 176 - 12 Gennaio 2026
```

### P1 - IMPORTANTE - COMPLETATO!

```
████████████████████ 100% COMPLETATO!

Obiettivo: Da USABILE a PRODUTTIVO
Status: 5/5 COMPLETATI

6. [x] SEARCH UI                              ← Sessione 176
   - Backend: GET /gmail/search?q=...
   - Frontend: SearchBar con debounce
   - Shortcut / per focus
   - Query Gmail: from:, to:, subject:, is:unread, etc.

7. [x] RINOMINARE MiracAllook → MiracOllook   ← Sessione 176
   - Backend: 10 file
   - Frontend: 4 file
   - Docs: 2 file

8. [x] REPLY ALL MODAL                        ← Sessione 178!
   - Backend: reply_all parametro in /gmail/reply
   - Frontend: ReplyModal con prop replyAll
   - Mostra tutti destinatari (To + Cc)
   - Shortcut A funziona!

9. [x] AI BATCH SUMMARIES                     ← Sessione 178!
   - Backend: /inbox/summaries già esistente
   - Frontend: useEmails con merge automatico
   - EmailListItem mostra summary con icona
   - Cache TanStack Query

10. [x] REFRESH/SYNC                          ← Sessione 178!
    - Bottone refresh con icona animata
    - Shortcut Shift+R
    - "Last synced: Xm ago" timestamp
    - Toast feedback dopo sync

Sessione 176 + 178 - 12 Gennaio 2026
```

### P2 - VALORE AGGIUNTO (Differenziazione)

```
Obiettivo: Da PRODUTTIVO a MAGICO
Timeline: Dopo P1

11. PMS INTEGRATION REALE
    - API Miracollo per guest lookup
    - Auto-detect email ospite
    - GuestSidebar con dati VERI
    - VIP/Check-in categorie automatiche

12. SNIPPETS PMS
    - /checkin → template con dati ospite
    - /conferma → template prenotazione
    - Auto-fill da Miracollo DB

13. SMART COMPOSE
    - AI suggerisce mentre scrivi
    - Tone: professional, friendly
    - Context: hospitality language

14. MULTI-USER
    - Session management
    - Ogni utente i suoi token
    - Shared inbox support

15. MOBILE RESPONSIVE
    - Breakpoint tablet/phone
    - Touch gestures
    - PWA installabile
```

### P3 - FUTURO (Nice to have)

```
Obiettivo: ENTERPRISE features
Timeline: 3-6 mesi

16. Snooze/Reminders
17. Email scheduling
18. Team comments
19. Analytics dashboard
20. Outlook support
21. Light mode toggle
22. Read receipts
23. Follow-up automation
```

---

## STUDI DA FARE

### Prima di P1

```
STUDIO: Gmail Search API
- Come funziona il search?
- Syntax query Gmail
- Come mostrare risultati?
```

### Prima di P2 (PMS Integration)

```
STUDIO 1: API Miracollo Guest Lookup
- Come cercare ospite per email?
- Quale endpoint usare?
- Formato risposta?

STUDIO 2: Real-time Sync
- WebSocket vs Polling?
- Come sincronizzare inbox?
- Rate limits Gmail?

STUDIO 3: Snippets Engine
- Syntax per placeholders?
- Come parsare {guest.name}?
- Editor integration?
```

---

## ARCHITETTURA TECNICA

### Stack Attuale

```
BACKEND:
├── FastAPI 0.109
├── Google Gmail API
├── Anthropic Claude API (Haiku)
├── Python 3.11+
├── SQLite (miracallook.db)      ← NUOVO P0.5!
└── SQLAlchemy 2.0

FRONTEND:
├── React 18 + TypeScript
├── Vite (build)
├── Tailwind CSS v4
├── TanStack Query v5
├── cmdk (command palette)
├── react-hotkeys-hook
└── Axios
```

### File Principali

```
BACKEND (miracollogeminifocus/miracallook/backend/):
├── main.py              # Entry FastAPI
├── auth/google.py       # OAuth2 + DB integration
├── gmail/api.py         # 17 endpoint (era 14!)
├── ai/claude.py         # Summarization
├── db/                  # NUOVO P0.5!
│   ├── database.py      # SQLite setup
│   ├── models.py        # UserToken model
│   └── __init__.py
└── miracallook.db       # Database file

FRONTEND (miracollogeminifocus/miracallook/frontend/):
├── src/App.tsx          # Orchestratore
├── src/components/
│   ├── Layout/ThreePanel.tsx
│   ├── Sidebar/Sidebar.tsx
│   ├── EmailList/EmailList.tsx
│   ├── EmailDetail/EmailDetail.tsx
│   ├── GuestSidebar/GuestSidebar.tsx
│   ├── CommandPalette/CommandPalette.tsx
│   ├── Compose/ComposeModal.tsx   # FIXATO P0.1!
│   ├── Reply/ReplyModal.tsx       # NUOVO P0.2!
│   └── Forward/ForwardModal.tsx   # NUOVO P0.3!
├── src/hooks/
│   ├── useEmails.ts     # + useArchiveEmail, useTrashEmail
│   └── useKeyboardShortcuts.ts
└── src/services/api.ts  # + archiveEmail, trashEmail
```

---

## METRICHE SUCCESSO

### P0 Complete (USABILE) - FATTO!

```
[x] Posso inviare email nuova
[x] Posso rispondere a email
[x] Posso inoltrare email
[x] Posso archiviare email
[x] Token persistono al restart
[x] Uso quotidiano possibile
```

### P1 Complete (PRODUTTIVO) - FATTO!

```
[x] Posso cercare email (/ shortcut)
[x] Vedo AI summary in lista
[x] Sync/Refresh funziona (Shift+R)
[x] Reply All funziona (A shortcut)
[x] Nome corretto "MiracOllook"
```

### P2 Complete (MAGICO)

```
[ ] Vedo info ospite REALI
[ ] Uso snippets con dati PMS
[ ] AI mi aiuta a scrivere
[ ] Più utenti supportati
[ ] Funziona su mobile
```

---

## RISCHI E MITIGAZIONI

| Rischio | Impatto | Mitigazione |
|---------|---------|-------------|
| Gmail API rate limit | Alto | Caching aggressivo |
| Token expiry | Alto | Refresh token automatico (P1) |
| AI costs | Medio | Cache summaries, limits |
| PMS coupling | Medio | API versionate |
| Feature creep | Alto | STRICT P0→P1→P2 |

---

## DECISIONI PRESE

### 1. P0 prima di tutto
```
PERCHÉ: Senza send/reply non è un email client
RISULTATO: P0 COMPLETATO! ✓
```

### 2. SQLite per dev, PostgreSQL per prod
```
PERCHÉ: Semplicità dev, robustezza prod
IMPLEMENTATO: miracallook.db funzionante ✓
```

### 3. Modal separati per Reply/Forward
```
PERCHÉ: UX più chiara, meno complessità
IMPLEMENTATO: ReplyModal.tsx + ForwardModal.tsx ✓
```

### 4. PMS integration in P2
```
PERCHÉ: Prima deve funzionare BASE
STATUS: Base completata, PMS in P2
```

---

## CRONOLOGIA SESSIONE 176

```
1. [x] Analisi codice REALE (cervella-ingegnera x2)
2. [x] Creazione MAPPA VERA (questo file)
3. [x] P0.1 Fix ComposeModal (cervella-frontend)
4. [x] P0.2 Creare ReplyModal (cervella-frontend)
5. [x] P0.3 Creare ForwardModal (cervella-frontend)
6. [x] P0.4 Archive/Delete (cervella-backend + cervella-frontend)
7. [x] P0.5 Database Token (cervella-backend)
8. [x] Checkpoint + aggiornamento mappa
```

---

## PROSSIMI STEP

### PROSSIMA SESSIONE (P2)

```
P2.1 [ ] PMS Integration reale (Guest Detection)
P2.2 [ ] Snippets PMS (/checkin, /conferma)
P2.3 [ ] Smart Compose (AI suggerisce)
P2.4 [ ] Multi-user support
P2.5 [ ] Mobile responsive
```

---

## NOTA FINALE

```
+================================================================+
|                                                                |
|   SESSIONE 176 + 178 STORICHE!                                 |
|                                                                |
|   P0 + P1 COMPLETATI = MiracOllook PRODUTTIVO!                 |
|                                                                |
|   P0 (Sessione 176):                                           |
|   - Send, Reply, Forward FUNZIONANO                            |
|   - Archive, Delete FUNZIONANO                                 |
|   - Token PERSISTONO                                           |
|                                                                |
|   P1 (Sessione 176 + 178):                                     |
|   - Search UI con shortcut /                                   |
|   - Reply All con shortcut A                                   |
|   - AI Summaries in lista email                                |
|   - Refresh/Sync con Shift+R                                   |
|   - Nome corretto: MiracOllook                                 |
|                                                                |
|   "Non è sempre come immaginiamo...                            |
|    ma alla fine è il 100000%!"                                 |
|                                                                |
+================================================================+
```

---

*"Ultrapassar os próprios limites!"*

*Mappa creata: 12 Gennaio 2026 - Sessione 176*
*P0 completato: 12 Gennaio 2026 - Sessione 176*
*P1 completato: 12 Gennaio 2026 - Sessione 178*
*Metodo: Analisi codice reale + implementazione con sciame*
