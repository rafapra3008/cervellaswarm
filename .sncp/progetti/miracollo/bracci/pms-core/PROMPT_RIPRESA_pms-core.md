<!-- DISCRIMINATORE: MIRACOLLO PMS CORE -->
<!-- PORTA: 8001 | TIPO: Sistema alberghiero principale -->
<!-- PATH: ~/Developer/miracollogeminifocus/ (backend principale) -->
<!-- NON CONFONDERE CON: Miracollook (8002 - repo separato), Room Hardware (8003) -->

# PROMPT RIPRESA - PMS Core

> **Ultimo aggiornamento:** 6 Marzo 2026 - Sessione 2 post-RINASCITA
> **STATO:** 90% LIVE | Health 9.3/10 | Security 10/10

---

## ULTIMA SESSIONE (6 Mar - pulizia profonda)

```
Da 7.8 a 9.3/10 in una sessione!

Security (3 MEDIO risolti):
  - WhatsApp verify: secrets.compare_digest() + no log token
  - /docs /redoc /openapi.json OFF in produzione (ENVIRONMENT check)
  - Token Telegram rimosso (deploy.sh.DEPRECATED eliminato)

Codice:
  - 22 except Exception -> tipi concreti (sqlite3.Error, httpx.HTTPError, etc.)
  - 25 except Exception annotati "Intentional broad catch: [motivo]"
  - 1 bare except: fixato (what_if_api.py)
  - 22 print() -> logger (compliance, direct_scraping, playwright_scraping)
  - 28 console.log debug rimossi (rateboard-core.js)

Pulizia:
  - File duplicato models/subscription.py eliminato (= modules/subscription/models.py)
  - 2 file esempio rimossi + backend/backend/ anomalia
  - miracallook/ rimosso dal repo (workspace separato)
  - 2 deploy scripts DEPRECATED eliminati

5 commit: dea5dd4, e34c57f, 95e8b22, 956a263, 440b01d
```

---

## ARCHITETTURA

```
396 endpoint API in 83 router files
Backend: Python 3.11, FastAPI, SQLite, Gunicorn (2 workers)
Frontend: HTML/CSS/JS puro (NON React!)
Docker: WORKDIR=/app, backend.main:app, non-root user
5 middleware: APIKeyAuth -> SecurityHeaders -> CORS -> Logging -> GZip
Import path: from backend.services... = CORRETTO (WORKDIR=/app)
```

---

## SICUREZZA (10/10 Guardiana)

```
Auth Middleware 100%:   API Key + Nginx Basic Auth (defense in depth)
HMAC webhook:           secrets.compare_digest() (timing-safe)
API Docs:               DISABILITATI in prod (/docs /redoc /openapi.json)
CSP Enforce:            + HSTS + Permissions-Policy
escapeHtml:             centralizzata 28/29 HTML (97%)
Rate limiting:          3 zone Nginx granulari
Secrets:                0 in codice, tutti in VM .env
SSL:                    Auto-renew CONFERMATO (valido fino 31 Mag 2026)
```

---

## PROSSIMO: 25 bare `except:` (9.3 -> 9.5)

```
15 file, 25 occorrenze - task meccanico ~30 min:

magic_link_service.py:167
merge.py:100, 170, 177, 187
research_orchestrator.py:92, 128, 318
receipts.py:48
analytics.py:157
city_tax/models.py:73
email/schedules.py:121, 231
room_types.py:42, 146
subscription/models.py:99
subscription/service.py:129, 164, 191
playwright_scraping_client.py:139
document_scanner.py:260
narrative_generator.py:211
availability.py:163
notifications.py:79
```

---

## BUG RESIDUI P3 (mitigati)

- ~434 innerHTML admin-only (CSP enforce + Basic Auth)
- ~76 onclick inline + 133 generati in JS
- 109 console.log in 70 file JS (molti in catch blocks)

---

## INFRASTRUTTURA

```
VM: e2-small RUNNING | IP 34.134.72.207 | SSL fino 31 Mag 2026
Deploy: GitHub Actions auto (push master -> LIVE)
Backup: cron 2x/giorno, 7d retention
```

---

*"Lavoriamo in pace! Senza casino! Dipende da noi!"*
*6 Marzo 2026*
