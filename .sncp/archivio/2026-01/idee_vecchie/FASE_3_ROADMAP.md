# FASE 3: FARE - Roadmap Dettagliata

> **Data:** 9 Gennaio 2026 - Sessione 140
> **Status:** IN CORSO

---

## STATO REALE (Scoperte)

| Item | Status | Note |
|------|--------|------|
| **MVP Dashboard** | 80% FATTO! | Backend + Frontend esistono |
| **Landing Page** | 0% | Da fare da zero |
| **Early Bird** | 0% | Da pianificare |
| **Pitch Anthropic** | 0% | Da preparare |

---

## 1. MVP WEB DASHBOARD

### Cosa Esiste Gia'

**Backend FastAPI (porta 8100):**
- `/api/mappa` - Mappa completa progetto
- `/api/nord` - IL NORD
- `/api/roadmap` - Roadmap step
- `/api/tasks` - Tasks attivi
- `/api/workers` - Stato 16 agenti
- `/api/events` - SSE real-time

**Frontend React (porta 5173):**
- Layout responsive
- NordWidget - Visualizza IL NORD
- SwarmWidget - Mostra famiglia 16 agenti
- RoadmapWidget - Step progetto
- SessioneWidget - Task corrente

**Script:** `dashboard/start-dashboard.sh`

### Gap da Completare

| Feature | Priorita' | Effort |
|---------|-----------|--------|
| Auth/Login | ALTA | 2-3 giorni |
| Multi-progetto | MEDIA | 1-2 giorni |
| Task real-time update | MEDIA | 1 giorno |
| Deploy production | ALTA | 1-2 giorni |

### Da Verificare
- [ ] Dashboard si avvia correttamente?
- [ ] Tutti gli endpoint funzionano?
- [ ] Frontend mostra dati reali?

---

## 2. LANDING PAGE

### Contenuti Richiesti

**Header:**
- Logo CervellaSwarm
- Tagline: "16 specialisti AI. $19/mese. Meno di Cursor, piu' di tutto."

**Hero Section:**
- Headline: "Why pay for one AI assistant when you can have a team?"
- Sub: "CervellaSwarm: 16 specialized AI agents that work together"
- CTA: "Start Free (BYOK)" + "Get Early Bird $99/year"

**Features:**
1. **16 Specialized Agents** - Backend, Frontend, Tester, Reviewer...
2. **SNCP Memory** - Persistent project memory (trade secret)
3. **Quality Gates** - 3 Guardiane che verificano ogni output
4. **IDE Agnostic** - Funziona con qualsiasi editor
5. **Privacy First** - Mai per training, tutto locale

**Pricing Table:**
| Free (BYOK) | Essentials $19 | Professional $39 |
|-------------|----------------|------------------|
| Your API key | Hosted tokens | Unlimited |
| CLI full | Web dashboard | Teams |
| 16 agents | 100 task/mese | Custom agents |

**Early Bird Banner:**
- "Primi 500 utenti: $99/anno invece di $228"
- Countdown timer
- Email capture

**Footer:**
- Contact: sales@cervellaswarm.com
- Links: Docs, GitHub, Discord

### Stack Tecnico
- React (stesso stack dashboard)
- Tailwind CSS
- Deploy: Vercel o Netlify

### Effort: 2-3 giorni

---

## 3. EARLY BIRD CAMPAIGN

### Piano

**Target:** Primi 500 utenti
**Prezzo:** $99/anno (invece di $228)
**Risparmio comunicato:** 57%

**Canali:**
1. Twitter/X - Dev community
2. Reddit - r/programming, r/artificial
3. Hacker News - Show HN
4. Dev.to - Article
5. LinkedIn - Professional network

**Timeline:**
1. Settimana 1: Landing page + Email capture
2. Settimana 2: Soft launch (amici/network)
3. Settimana 3: Public launch

**Metriche:**
- Email signups
- Early bird conversions
- Referrals

### Effort: Ongoing (1-2 settimane prep)

---

## 4. CONTATTARE ANTHROPIC

### Obiettivo
Partnership o licenza bulk per API

### Contatti
- Sales: sales@anthropic.com
- VC Partner: claude.com/contact-sales/vc-partner

### Pitch Elements
1. **Chi siamo:** CervellaSwarm - Multi-agent orchestration
2. **Cosa facciamo:** 16 specialized agents su Claude
3. **Perche' contattarli:** Volume pricing, partnership
4. **Ask:** Volume discount o partner program

### Template Email
```
Subject: CervellaSwarm - Multi-Agent Platform on Claude API

Hi Anthropic Team,

We're building CervellaSwarm, a multi-agent orchestration
platform powered by Claude. We have 16 specialized agents
that work together on complex software projects.

We're launching soon and expect significant API usage.
We'd love to discuss:
- Volume pricing options
- Partner program eligibility
- Technical partnership opportunities

Would someone be available for a brief call?

Best,
[Nome]
```

### Effort: 1 giorno prep + follow-up

---

## PRIORITA' SESSIONE 140

```
1. [ALTA] Verificare Dashboard funziona
2. [ALTA] Identificare gap Dashboard
3. [MEDIA] Iniziare Landing Page
4. [BASSA] Preparare pitch Anthropic
```

---

## TIMELINE SUGGERITA

| Settimana | Focus |
|-----------|-------|
| Settimana 1 | Dashboard + Landing Page |
| Settimana 2 | Landing Page + Early Bird prep |
| Settimana 3 | Launch + Anthropic outreach |

---

*"Una cosa alla volta, fatta BENE!"*

*Creato: 9 Gennaio 2026 - Sessione 140*
