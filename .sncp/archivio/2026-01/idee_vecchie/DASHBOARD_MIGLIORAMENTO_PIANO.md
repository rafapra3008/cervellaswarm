# Dashboard - Piano Miglioramento

> **Data:** 9 Gennaio 2026 - Sessione 140
> **Status:** DA FARE (dopo MVP essenziale)

---

## STATO ATTUALE

La dashboard **esiste e funziona** ma e' un prototipo.

| Cosa | Status |
|------|--------|
| Backend FastAPI | Funziona (porta 8100) |
| Frontend React | Funziona (porta 5173) |
| 4 Widget | NordWidget, SwarmWidget, RoadmapWidget, SessioneWidget |
| Dati reali | Si, legge NORD.md e ROADMAP_SACRA.md |

---

## DA FARE: RICERCA BIG PLAYERS

### Domande da Rispondere

1. **Come usano le dashboard i competitor?**
   - Cursor: ha dashboard? cosa mostra?
   - Windsurf: ha dashboard? cosa mostra?
   - Google Antigravity: Manager Surface - studiare!

2. **Cosa vogliono vedere gli utenti?**
   - Task in corso?
   - Storia sessioni?
   - Consumo token/costi?
   - Team activity?

3. **Esempi da studiare:**
   - Vercel Dashboard (deploy + analytics)
   - Linear (project management)
   - Notion (workspace)
   - GitHub Projects (kanban)

### Da Cercare

| Competitor | Cosa Cercare | Priority |
|------------|--------------|----------|
| Google Antigravity | Manager Surface screenshots | ALTA |
| Cursor | Se ha dashboard team | MEDIA |
| Vercel | Layout + UX patterns | MEDIA |
| Linear | Task visualization | BASSA |

---

## FUNZIONALITA' POSSIBILI

### Essenziali (MVP)
- [x] Status agenti (chi e' attivo)
- [x] Sessione corrente
- [x] Roadmap progresso
- [ ] Task list (todo attivi)

### Nice-to-Have
- [ ] Consumo token real-time
- [ ] Storia sessioni
- [ ] Team view (chi sta lavorando)
- [ ] Notifiche/alerts

### Future
- [ ] Analytics (trend uso)
- [ ] Cost tracking
- [ ] Multi-progetto
- [ ] Mobile view

---

## DECISIONI DA PRENDERE

1. **Target utente dashboard:**
   - Solo dev (CLI primary, dashboard secondary)?
   - O team lead (dashboard primary)?

2. **Real-time vs polling:**
   - SSE per live updates?
   - O polling ogni 30 sec ok?

3. **Hosting:**
   - Locale (come ora)?
   - Cloud (per team)?

---

## AZIONI CONCRETE

### Fase 1: Ricerca (1-2 ore)
- [ ] Screenshot Google Antigravity Manager Surface
- [ ] Analisi Vercel dashboard UX
- [ ] Definire 5 "must have" features

### Fase 2: Design (2-4 ore)
- [ ] Wireframe nuovo layout
- [ ] Decidere palette colori (brand)
- [ ] Mobile-first o desktop-first?

### Fase 3: Implementazione (1-2 giorni)
- [ ] Refactor componenti
- [ ] Aggiungere features prioritarie
- [ ] Test e polish

---

## NOTE

> "Possiamo prendere una cosa professionale di esempio"
> "Capire bene la funzionalita' della dashboard"
> "Come i big players utilizzano? Cosa faremmo sulla nostra?"
> - Rafa, 9 Gennaio 2026

**Priorita':** Questo viene DOPO landing page e early bird.
La dashboard attuale e' sufficiente per dimostrare il prodotto.

---

## LINK UTILI

- Dashboard attuale: http://localhost:5173
- API docs: http://localhost:8100/docs
- Codice: `/dashboard/`
- Design inspiration: TBD

---

*"Prima funziona, poi bello!"*

*Creato: 9 Gennaio 2026 - Sessione 140*
