# ROADMAP - Miracallook

> **Progetto:** Client Email AI tipo Superhuman - Modulo Miracollo
> **Creato:** 12 Gennaio 2026
> **Status:** FASE 0 - STUDIO
> **Nome:** Miracallook (Miracollo + Outlook)

---

## VISIONE

```
+================================================================+
|                                                                |
|   MIRACALLOOK = Miracollo + Outlook                            |
|                                                                |
|   Client email AI integrato in Miracollo!                      |
|                                                                |
|   - Si collega ai vostri Gmail esistenti                       |
|   - AI scrive bozze nel VOSTRO stile                           |
|   - Keyboard shortcuts per velocita                            |
|   - Integrato nella dashboard Miracollo                        |
|   - Tutto self-hosted, dati nostri                             |
|                                                                |
+================================================================+
```

**Ispirazione:** Superhuman ($30-40/mese per utente)
**Noi:** Costruiamo il nostro, gratis, DENTRO Miracollo!

---

## ARCHITETTURA

```
+------------------+
|   React Frontend |  <- UI moderna, keyboard shortcuts
|   (Miracallook)  |
+------------------+
         |
         v
+------------------+
|  FastAPI Backend |  <- Logica, cache, AI
|   (Python)       |
+------------------+
         |
    +----+----+
    |         |
    v         v
+-------+  +--------+
| Gmail |  | Claude |
| API   |  | API    |
+-------+  +--------+
```

---

## GMAIL API - Limiti (OK per noi!)

| Risorsa | Limite | Note |
|---------|--------|------|
| Quota per utente | 15,000 units/min | Abbondante |
| Quota per progetto | 1,200,000 units/min | Illimitato praticamente |
| messages.list | 5 units | Leggere lista email |
| messages.get | 5 units | Leggere singola email |
| messages.send | 100 units | Inviare email |
| Invio giornaliero (Workspace) | 2,000 email/giorno | Piu che sufficiente |
| Invio giornaliero (Gmail free) | 500 email/giorno | OK per uso personale |

**Conclusione:** Limiti NON sono un problema per uso team.

---

## OAUTH2 - Setup

### Per Team Interno (Workspace)
Se usate Google Workspace (email @vostrodominio):
- App "Internal" = NO verifica Google
- Accesso immediato
- Piu semplice

### Per Gmail Personali (@gmail.com)
- App in "Testing mode"
- Max 100 test users (piu che sufficiente per team)
- Refresh token 7 giorni (poi re-auth)
- Per produzione: serve verifica Google (2-3 settimane)

---

## FASI SVILUPPO

### FASE 0: STUDIO (Questa settimana)
- [x] Ricerca Superhuman features
- [x] Ricerca Gmail API limiti
- [x] Ricerca OAuth2 requirements
- [x] Architettura definita
- [ ] Definire MVP features (cosa nella prima versione?)
- [ ] Setup Google Cloud Project

**Output:** Roadmap completa, decisioni prese

---

### FASE 1: FONDAMENTA (Backend Base)
**Obiettivo:** Connessione Gmail funzionante

**Task:**
1. [ ] Creare Google Cloud Project
2. [ ] Configurare OAuth2 consent screen
3. [ ] Ottenere credentials (client_id, client_secret)
4. [ ] FastAPI endpoint: `/auth/google` (login)
5. [ ] FastAPI endpoint: `/auth/callback` (OAuth callback)
6. [ ] Salvare refresh tokens (encrypted)
7. [ ] Test: login con account Gmail

**Tech:**
- FastAPI
- google-auth, google-auth-oauthlib
- SQLite o PostgreSQL per tokens

**Output:** Login Gmail funzionante

---

### FASE 2: LETTURA EMAIL (Backend)
**Obiettivo:** Leggere inbox da Gmail

**Task:**
1. [ ] Endpoint: `GET /emails` (lista email)
2. [ ] Endpoint: `GET /emails/{id}` (singola email)
3. [ ] Endpoint: `GET /threads/{id}` (conversazione)
4. [ ] Parsing email (HTML to text, attachments)
5. [ ] Cache locale (evitare chiamate ripetute)
6. [ ] Sync incrementale (solo nuove email)

**Tech:**
- Gmail API (messages.list, messages.get)
- Redis o SQLite per cache

**Output:** API che restituisce email

---

### FASE 3: INVIO EMAIL (Backend)
**Obiettivo:** Inviare email da Gmail

**Task:**
1. [ ] Endpoint: `POST /emails/send`
2. [ ] Endpoint: `POST /emails/reply`
3. [ ] Endpoint: `POST /drafts` (salva bozza)
4. [ ] Gestione allegati
5. [ ] Gestione CC, BCC
6. [ ] Rate limiting interno

**Output:** Invio email funzionante

---

### FASE 4: UI BASE (Frontend)
**Obiettivo:** Interfaccia usabile

**Task:**
1. [ ] Setup React + Vite + Tailwind
2. [ ] Layout: sidebar + email list + email view
3. [ ] Lista email con preview
4. [ ] Visualizzazione singola email
5. [ ] Composizione email (editor)
6. [ ] Reply/Forward
7. [ ] Dark mode

**Design:**
- Ispirazione: Superhuman, Linear, Notion
- Minimalista, veloce, keyboard-first

**Output:** Client email funzionante base

---

### FASE 5: KEYBOARD SHORTCUTS
**Obiettivo:** Velocita tipo Superhuman

**Task:**
1. [ ] Sistema shortcut globale
2. [ ] `j/k` = navigazione su/giu
3. [ ] `o/Enter` = apri email
4. [ ] `e` = archivia
5. [ ] `#` = elimina
6. [ ] `r` = rispondi
7. [ ] `c` = componi nuova
8. [ ] `g+i` = vai a inbox
9. [ ] `/` = cerca
10. [ ] `?` = mostra shortcuts

**Tech:**
- react-hotkeys-hook o custom

**Output:** Navigazione senza mouse

---

### FASE 6: AI - AUTO DRAFT
**Obiettivo:** AI scrive bozze risposte

**Task:**
1. [ ] Analisi stile scrittura utente (da sent emails)
2. [ ] Prompt engineering per risposte
3. [ ] Endpoint: `POST /ai/draft` (genera bozza)
4. [ ] UI: mostra bozza suggerita
5. [ ] Comandi: "shorten", "lengthen", "formal", "casual"
6. [ ] Salvataggio preferenze stile

**Tech:**
- Claude API (claude-3-5-sonnet)
- Prompt con contesto email ricevuta + stile utente

**Output:** AI che scrive come te

---

### FASE 7: AI - SMART FEATURES
**Obiettivo:** Automazione intelligente

**Task:**
1. [ ] Auto Labels (categorizza email)
2. [ ] Priority detection (urgente vs no)
3. [ ] Ask AI (cerca con domande naturali)
4. [ ] Riassunto thread lunghi
5. [ ] Suggerimenti follow-up

**Output:** Email management intelligente

---

### FASE 8: MULTI-ACCOUNT + POLISH
**Obiettivo:** Prodotto completo

**Task:**
1. [ ] Supporto account multipli
2. [ ] Unified inbox
3. [ ] Notifiche desktop
4. [ ] Offline mode (cache)
5. [ ] Performance optimization
6. [ ] Mobile responsive (o app dedicata)

**Output:** Prodotto production-ready

---

## MVP - Prima Versione Usabile

**Cosa DEVE avere il MVP:**
- [ ] Login Gmail OAuth2
- [ ] Lista email inbox
- [ ] Leggere email
- [ ] Inviare email
- [ ] Reply
- [ ] UI base funzionante
- [ ] 5-10 keyboard shortcuts base

**Cosa PUO' aspettare:**
- AI drafts
- Auto labels
- Multi-account
- Offline mode

---

## TECH STACK

| Layer | Tecnologia |
|-------|------------|
| Frontend | React + Vite + Tailwind |
| State | Zustand o Redux Toolkit |
| Backend | FastAPI (Python) |
| Database | PostgreSQL (o SQLite per MVP) |
| Cache | Redis (o in-memory per MVP) |
| Auth | OAuth2 + JWT |
| AI | Claude API |
| Email | Gmail API |

---

## DECISIONI PRESE

### 1. Nome Progetto
- [x] **Miracallook** (Miracollo + Outlook)

### 2. Dove Deployare
- [x] **Locale prima** - meno casino, poi decidiamo insieme

### 3. Priorita AI
- [x] **Con AI da subito** - predisposto per Cervella/Claude

### 4. Account Gmail Team
- [x] **Focus Gmail** (98% usa Gmail) - altri provider dopo se serve

---

## TIMELINE STIMATA

| Fase | Durata Stimata |
|------|----------------|
| Fase 0: Studio | 1-2 giorni |
| Fase 1: Fondamenta | 2-3 giorni |
| Fase 2: Lettura | 2-3 giorni |
| Fase 3: Invio | 1-2 giorni |
| Fase 4: UI Base | 3-5 giorni |
| Fase 5: Shortcuts | 1-2 giorni |
| **MVP TOTALE** | **10-17 giorni** |
| Fase 6: AI Draft | 3-5 giorni |
| Fase 7: AI Smart | 5-7 giorni |
| Fase 8: Polish | 3-5 giorni |

**Note:** Tempi indicativi, dipende da disponibilita.

---

## RISORSE

### Documentazione
- [Gmail API Quickstart Python](https://developers.google.com/workspace/gmail/api/quickstart/python)
- [Gmail API Reference](https://developers.google.com/gmail/api/reference/rest)
- [OAuth2 for Web Apps](https://developers.google.com/identity/protocols/oauth2/web-server)

### Ispirazione UI
- [Superhuman](https://superhuman.com/)
- [Shortwave](https://www.shortwave.com/)
- [Spark](https://sparkmailapp.com/)

### Open Source Reference
- [Mailspring](https://github.com/Foundry376/Mailspring)
- [simplegmail](https://github.com/jeremyephron/simplegmail)

---

## PROSSIMO STEP IMMEDIATO

**FASE 0 - Completare Studio:**

1. [x] Rafa decide: nome progetto? -> **Miracallook!**
2. [x] Rafa decide: MVP con AI? -> **Si, con Cervella/Claude!**
3. [x] Rafa decide: dove deploy? -> **Locale prima!**
4. [x] Rafa decide: quale email? -> **Focus Gmail!**
5. [ ] Creare Google Cloud Project
6. [ ] Test connessione Gmail API base

---

*"Miracallook - Un client email che lavora per te, non contro di te."*

*Creato: 12 Gennaio 2026*
*Ultimo update: 12 Gennaio 2026*
