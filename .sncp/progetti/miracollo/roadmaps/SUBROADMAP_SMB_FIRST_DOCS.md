# SUB-ROADMAP: SMB-FIRST Documentation

> **Versione:** 1.0.0
> **Data:** 14 Gennaio 2026 - Sessione 202
> **Obiettivo:** Portare documentazione da 3/10 a 8/10
> **Owner:** cervella-docs

---

## PROBLEMA

```
README.md attuale:
- Data: 11 Dicembre 2025 (VECCHISSIMO!)
- Dice: "Fase Studio e Analisi"
- Realta: Prodotto 9.5/10 in produzione!

Conseguenza:
- Chi legge pensa sia un progetto demo
- Nessuna guida installazione
- SMB non possono usare da soli
```

---

## OBIETTIVO

```
+================================================================+
|   DA: Documentazione 3/10 (vecchia, incompleta)                 |
|   A:  Documentazione 8/10 (moderna, self-service)               |
+================================================================+

3 documenti chiave:
1. README.md      - Vetrina del progetto
2. INSTALL.md     - Guida installazione completa
3. QUICK_START.md - 5 minuti per partire
```

---

## TASK 1: README.md (Vetrina)

### Cosa Deve Contenere

```markdown
# Miracollo RMS

> Revenue Management System per hotel SMB

## Cos'e Miracollo
- AI-powered pricing suggestions
- Weather + Events integration
- Transparent AI (vedi perche suggerisce)
- WhatsApp auto-reply
- Direct booking engine

## Features
- [x] RateBoard intelligente
- [x] AI Suggestions (7 tipi)
- [x] Weather API integration
- [x] Local Events integration
- [x] Competitor monitoring (prep)
- [x] WhatsApp AI auto-reply
- [x] Direct booking API
- [x] Autopilot mode

## Quick Start
Link a QUICK_START.md

## Installation
Link a INSTALL.md

## Tech Stack
- Backend: Python 3.11, FastAPI
- Frontend: Vanilla JS, Chart.js
- Database: SQLite
- AI: Claude (WhatsApp), Gemini (Narrative)
- Deploy: Docker, Nginx

## Status
- Version: 1.7.0
- Score: 9.5/10
- Production: miracollo.com

## License
Proprietary - Rafa & Cervella
```

### Effort: 2 ore

---

## TASK 2: INSTALL.md (Guida Completa)

### Struttura

```markdown
# Installation Guide

## Prerequisites
- Docker + Docker Compose
- Domain con SSL (Let's Encrypt)
- API Keys: WeatherAPI, Stripe (optional)

## Option A: Docker (Recommended)
1. Clone repo
2. Copy .env.example to .env
3. Configure API keys
4. docker-compose up -d
5. Access https://yourdomain.com

## Option B: Manual
1. Python 3.11 setup
2. pip install requirements
3. Database migration
4. Uvicorn/Gunicorn
5. Nginx reverse proxy

## Configuration
- .env variables explained
- API keys setup
- SSL certificates

## Post-Install
- Create first hotel
- Configure rooms
- Test health endpoint

## Troubleshooting
- Common errors
- Log locations
- Support contact
```

### Effort: 4 ore

---

## TASK 3: QUICK_START.md (5 Minuti)

### Struttura

```markdown
# Quick Start (5 minutes)

## TL;DR

git clone ...
cp .env.example .env
# Edit .env with your API keys
docker-compose up -d

Done! Access https://localhost:8001

## Step 1: Clone (30 sec)
git clone https://github.com/...

## Step 2: Configure (2 min)
cp .env.example .env
nano .env
# Set: WEATHER_API_KEY, SECRET_KEY

## Step 3: Launch (1 min)
docker-compose up -d

## Step 4: Verify (30 sec)
curl http://localhost:8001/api/health

## Step 5: Access (1 min)
Open http://localhost:8001
Login: admin / (see .env)

## Next Steps
- Add your hotel
- Configure rooms
- Start receiving suggestions!

## Need Help?
- Full guide: INSTALL.md
- Troubleshooting: docs/troubleshooting.md
```

### Effort: 2 ore

---

## TIMELINE

```
TASK 1: README.md        [##########] 2h
TASK 2: INSTALL.md       [##########] 4h
TASK 3: QUICK_START.md   [##########] 2h

TOTALE: 8 ore (1 giorno di lavoro)
```

---

## DIPENDENZE

Prima di scrivere serve verificare:
- [ ] .env.example esiste? E' completo?
- [ ] docker-compose.yml e' documentato?
- [ ] Quali API keys sono REQUIRED vs OPTIONAL?
- [ ] Endpoint health funziona senza auth?

---

## OWNER

**cervella-docs** scrive i documenti
**Regina** verifica completezza
**Rafa** approva contenuto finale

---

## OUTPUT ATTESO

```
/miracollogeminifocus/
├── README.md           <- Aggiornato, moderno
├── INSTALL.md          <- Nuovo, completo
├── QUICK_START.md      <- Nuovo, 5 minuti
└── docs/
    └── troubleshooting.md  <- Bonus se tempo
```

---

## CRITERI SUCCESSO

| Criterio | Target |
|----------|--------|
| README riflette stato reale | SI |
| SMB puo installare da solo | SI |
| Tempo per quick start | < 5 min |
| API keys documentate | 100% |
| Troubleshooting base | SI |

---

*"Documentazione buona = Adoption facile"*
*"Se non e documentato, non esiste"*

---

**Creato:** 14 Gennaio 2026
**Sessione:** 202
