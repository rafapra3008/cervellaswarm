# SUBROADMAP - Miracollook verso 10/10

> **Creato:** 20 Gennaio 2026 - Sessione 300
> **Obiettivo:** Portare Miracollook da 9.5/10 a 10/10 (Production-Ready)

---

## STATO ATTUALE

```
+================================================================+
|   MIRACOLLOOK: 9.5/10 (FASE 0-6 COMPLETATE)                   |
|                                                                |
|   Email client AI per hotel                                    |
|   Stack: FastAPI + React 19 + Gmail API + Claude AI           |
|   Porta: 8002                                                  |
+================================================================+
```

---

## MAPPA COMPLETATA (9.5/10)

| Fase | Score | Cosa | Status |
|------|-------|------|--------|
| 0 | 7.0 | CVE Fix | ✅ |
| 1 | 7.5 | Security (token encryption) | ✅ |
| 2 | 8.0 | LaunchAgents | ✅ |
| 3 | 8.5 | Rate Limiting | ✅ |
| 4 | 9.0 | Testing Backend (31 test) | ✅ |
| 5 | 9.2 | Structured Logging | ✅ |
| 6 | 9.5 | Frontend (env, errors, loading) | ✅ |

---

## VERSO 10/10 - LE 4 FASI RIMANENTI

```
FASE 7: Refactoring Code    → 9.6/10
FASE 8: Test Coverage       → 9.7/10
FASE 9: Docker/Infra        → 9.8/10
FASE 10: Documentation      → 10/10 PRODUCTION-READY!
```

---

## FASE 7 - REFACTORING CODE (9.5 → 9.6)

**Obiettivo:** Ridurre technical debt, funzioni < 100 righe

### Task

| # | Task | File | Righe Attuali | Target |
|---|------|------|---------------|--------|
| 7.1 | Split reply_email() | backend/gmail/compose.py | 152 | < 50 |
| 7.2 | Split batch_modify() | backend/gmail/actions.py | 152 | < 50 |
| 7.3 | Creare useAppState() | frontend/src/App.tsx | 311 | < 200 |
| 7.4 | Fix DB duplicati | backend/*.db | 2 file | 1 file |

### Dettaglio 7.1 - Split reply_email()

```python
# PRIMA: 152 righe monolitiche
def reply_email(...):
    # tutto insieme

# DOPO: funzioni piccole
def reply_email(...):
    creds = get_credentials(...)
    original = get_original_message(...)
    headers = build_reply_headers(original)
    message = create_reply_message(headers, body)
    return send_message(message)
```

### Dettaglio 7.3 - Creare useAppState()

```typescript
// PRIMA: App.tsx con 10+ useState
function AppContent() {
  const [selectedEmail, setSelectedEmail] = useState(...)
  const [isComposeOpen, setIsComposeOpen] = useState(...)
  // ... 10+ useState

// DOPO: hook dedicato
function AppContent() {
  const appState = useAppState();
  const emailHandlers = useEmailHandlers(appState);
  // ... logica separata
}
```

---

## FASE 8 - TEST COVERAGE (9.6 → 9.7)

**Obiettivo:** Coverage > 70%, test frontend

### Task

| # | Task | Tipo | Coverage Target |
|---|------|------|-----------------|
| 8.1 | Test Gmail API endpoints | Backend | 70% |
| 8.2 | Test AI summarization | Backend | 80% |
| 8.3 | Setup Vitest | Frontend | - |
| 8.4 | Test custom hooks | Frontend | 60% |
| 8.5 | Test services/api.ts | Frontend | 80% |

### Setup Frontend Tests

```bash
# Installare
npm install -D vitest @testing-library/react @testing-library/jest-dom

# Configurare vitest.config.ts
# Creare __tests__/ folder
```

### Priorità Test Backend

```
1. test_inbox.py      - GET /gmail/inbox
2. test_compose.py    - POST /gmail/send, /reply, /forward
3. test_actions.py    - POST /gmail/archive, /trash
4. test_ai.py         - AI summarization
```

---

## FASE 9 - DOCKER/INFRA (9.7 → 9.8)

**Obiettivo:** Containerizzazione per deploy facile

### Task

| # | Task | File |
|---|------|------|
| 9.1 | Dockerfile backend | backend/Dockerfile |
| 9.2 | Dockerfile frontend | frontend/Dockerfile |
| 9.3 | docker-compose.yml | docker-compose.yml |
| 9.4 | Health check avanzato | backend/main.py |
| 9.5 | .env.production | backend/.env.production |

### Dockerfile Backend (esempio)

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8002
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
```

### docker-compose.yml (esempio)

```yaml
services:
  backend:
    build: ./backend
    ports:
      - "8002:8002"
    env_file:
      - ./backend/.env

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
```

---

## FASE 10 - DOCUMENTATION (9.8 → 10/10)

**Obiettivo:** Documentazione completa, production-ready

### Task

| # | Task | Output |
|---|------|--------|
| 10.1 | API docs (Swagger) | /docs endpoint attivo |
| 10.2 | README completo | README.md |
| 10.3 | Setup guide | docs/SETUP.md |
| 10.4 | Architecture docs | docs/ARCHITECTURE.md |
| 10.5 | Deploy guide | docs/DEPLOY.md |

### README Structure

```markdown
# Miracollook

Email client AI per hotel.

## Quick Start
## Features
## Architecture
## API Reference
## Development
## Deployment
## Contributing
```

---

## TIMELINE SUGGERITA

```
FASE 7: Refactoring     ~2-3 sessioni
FASE 8: Test Coverage   ~3-4 sessioni
FASE 9: Docker/Infra    ~2-3 sessioni
FASE 10: Documentation  ~1-2 sessioni

TOTALE: ~8-12 sessioni per 10/10
```

---

## FEATURE BONUS (OLTRE 10/10)

Dalla ricerca cervella-researcher, feature per competitività:

| Feature | Impatto | Complessità |
|---------|---------|-------------|
| Email Snooze | ALTO | Media |
| Templates/Canned Responses | ALTO | Bassa |
| Virtual Scrolling (1000+ email) | MEDIO | Media |
| Keyboard Shortcuts Avanzati | MEDIO | Bassa |
| Multi-Account | ALTO | Alta |

---

## DECISIONI ARCHITETTURALI

### Già Prese (non cambiare)

- ✅ SQLite per development (PostgreSQL per prod)
- ✅ React Query (no Redux)
- ✅ Fernet encryption per tokens
- ✅ structlog per logging

### Da Decidere

- ❓ Redis per AI cache (vs SQLite table)
- ❓ Vercel/Fly.io per frontend deploy
- ❓ Monitoring (Sentry? Grafana?)

---

## CHECKLIST PRODUCTION-READY

```
[ ] FASE 7 completata (refactoring)
[ ] FASE 8 completata (test > 70%)
[ ] FASE 9 completata (Docker)
[ ] FASE 10 completata (docs)
[ ] Security audit finale
[ ] Performance test (load testing)
[ ] Backup strategy definita
[ ] Monitoring configurato
```

---

*"Un progresso alla volta - arriveremo al 10/10!"*

*Creato: Sessione 300 - Cervella & Rafa*
