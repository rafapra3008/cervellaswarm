<!-- DISCRIMINATORE: MIRACOLLO PMS CORE -->
<!-- PORTA: 8001 | TIPO: Sistema alberghiero principale -->
<!-- PATH: ~/Developer/miracollogeminifocus/ (backend principale) -->
<!-- NON CONFONDERE CON: Miracollook (8002), Room Hardware (8003) -->

# PROMPT RIPRESA - PMS Core

> **Ultimo aggiornamento:** 27 Febbraio 2026 - FASE 3 Documentazione COMPLETATA
> **STATO:** 90% LIVE | FASE 2 Sicurezza DONE | FASE 3 Docs DONE

---

## COSA E SUCCESSO QUESTA SESSIONE

```
FASE 3 - DOCUMENTAZIONE (27 Feb 2026)

Obiettivo: portare Health Docs da 6.5/10 a 9.5/10
Risultato: 9.0/10 (Guardiana) + fix P2 applicati

Cosa abbiamo fatto:
1. Verificato e aggiornato PROMPT_RIPRESA root (redirect OK)
2. Fixato 6 contraddizioni nei docs (score, porte, stack, container)
3. Rimosso 390 file da git tracking (.sncp/ + .swarm/ obsoleti)
4. Eliminato 250+ file locali (checkpoints, reports, task output)
5. Allineato FORTEZZA_MIRACOLLO.md con realta FASE 2
6. Aggiornato metriche nella SUBROADMAP

Guardiana: 9.0/10 -> 4 P2 fixati (FORTEZZA), 6 P3 fixati
Commit: 1a72310 | 393 file, -51,179 righe | PUSHATO
```

---

## FASE 2 SICUREZZA - COMPLETATA (sessione precedente)

```
2.1 Auth Middleware       ✅ LIVE (9.5/10) - API Key + Nginx Basic Auth
2.2 CSP Enforce          ✅ DONE (9.0/10) - unsafe-eval rimosso, HSTS
2.3 escapeHtml globale   ✅ DONE (9.3/10) - 8 copie -> 1 centralizzata
2.4 DB purge git history ✅ DONE (9.3/10) - .git 17->8.7 MB
2.5 Rate limiting Nginx  ✅ DONE (9.3/10) - 3 zone granulari
```

---

## BUG NOTI RESIDUI (P3)

| Bug | Severita | Mitigazione |
|-----|----------|-------------|
| ~434 innerHTML admin-only | P3 | CSP enforce + Basic Auth |
| 76 onclick inline | P3 | richiedono unsafe-inline in CSP |
| security.js in 12/29 HTML | P2 | planning.html manca (93 innerHTML!) |
| `on_event("startup")` deprecato | P3 | funziona ma deprecated warning |
| except Exception generico 100+ | P3 | FASE 4 |
| Rate limiting Python in-memory | P3 | Nginx rate limiting 3 zone |

---

## ARCHITETTURA ATTUALE

```
396 endpoint API in 83 file router
Backend: Python 3.11, FastAPI, SQLite, Gunicorn (2 workers)
Frontend: HTML/CSS/JS puro (NON React!)
Docker: Multi-stage build, non-root user, Nginx reverse proxy
5 middleware: APIKeyAuth -> SecurityHeaders -> CORS -> Logging -> GZip
```

---

## FASE 3 FEATURE - PROGRESSO: 4/5 (80%)

| Task | Status |
|------|--------|
| F3.1 Batch Operations | DONE 9/10 |
| F3.2 Webhooks Outbound | DONE 9/10 |
| F3.3 Revenue Dashboard | DONE 8/10 |
| F3.4 Housekeeping QW | DONE 9/10 |
| F3.5 Channel Manager | FUTURO |

---

## PROSSIMI STEP

1. **FASE 4 - Qualita Codice** (target: 8.5/10)
2. O fix security.js in HTML mancanti (P2 residuo)
3. Decidere con Rafa
4. **Subroadmap:** `roadmaps/SUBROADMAP_RECAP_RINASCITA_2026.md`

---

*"Lavoriamo in pace! Senza casino! Dipende da noi!"*
*27 Febbraio 2026*
