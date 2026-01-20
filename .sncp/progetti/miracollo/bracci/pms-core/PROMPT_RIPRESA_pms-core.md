<!-- DISCRIMINATORE: MIRACOLLO PMS CORE -->
<!-- PORTA: 8001 | TIPO: Sistema alberghiero principale -->
<!-- PATH: ~/Developer/miracollogeminifocus/ (backend principale) -->
<!-- NON CONFONDERE CON: Miracollook (8002), Room Hardware (8003) -->

# PROMPT RIPRESA - PMS Core

> **Ultimo aggiornamento:** 20 Gennaio 2026 - Sessione 303
> **STATO:** 90% LIVE | Health 9.5/10 (FASE 1 FONDAMENTA 100%!)

---

## SESSIONE 303 - FASE 1 FONDAMENTA COMPLETATA!

```
+================================================================+
|   FASE 1: FONDAMENTA - 4/4 COMPLETATI!                         |
|                                                                |
|   [x] F1.1 Rate Limiting Globale    10/10 APPROVED            |
|   [x] F1.2 Backup Automation         9/10 APPROVED            |
|   [x] F1.3 Health Checks Avanzati   9.5/10 APPROVED           |
|   [x] F1.4 Structured Logging        9/10 APPROVED            |
|                                                                |
|   Media audit: 9.4/10 - PMS BLINDATO!                         |
+================================================================+
```

**Cosa implementato:**
- Rate limiting: slowapi 30/min, proxy-aware (get_ipaddr)
- Backup: scripts/backup_db.sh + test_restore.sh (gzip 90% compression)
- Health: Kubernetes-style /live, /ready, /startup, /detailed
- Logging: structlog JSON (prod) + Pretty (dev), Request ID automatico

---

## SUBROADMAP ATTIVA

**File:** `.sncp/roadmaps/SUBROADMAP_PMS_MIGLIORAMENTI.md`

| Fase | Status | Sessioni |
|------|--------|----------|
| 1 Fondamenta | ✅ DONE | 1 (S303) |
| 2 Performance | TODO | 8-10 |
| 3 Feature | TODO | 15-25 |

---

## SESSIONE 302 - PULIZIA CASA

```
SPLIT FILE GIGANTI: 6/6 COMPLETATI!
4,522 righe -> 39 file modulari
```

---

## MODULO FINANZIARIO (PARCHEGGIATO)

| Fase | Componente | Stato |
|------|------------|-------|
| 1-1B | Ricevute + Checkout | 100% REALE |
| 2 | Scontrini RT | 90% |
| 3-4 | Fatture/Export | PARCHEGGIATO |

---

## WARNING

- **FK violations:** 1262 nel DB (problema esistente, task separato)

---

## ARCHITETTURA

```
Internet -> Nginx (443) -> Backend (8001) -> SQLite
VM: miracollo-cervella (Google Cloud)
```

---

*"FASE 1 FONDAMENTA 100%! Health 9.5/10!" - Sessione 303*
