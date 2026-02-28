<!-- DISCRIMINATORE: ECOSISTEMA MIRACOLLO - PANORAMA -->

# PROMPT RIPRESA - Ecosistema Miracollo

> **Ultimo aggiornamento:** 27 Febbraio 2026 - FASE 3 Documentazione COMPLETATA!
> **Status:** miracollo.com LIVE! | FASE 0-3 DONE | Prossima: FASE 4 Qualita Codice

---

## I 3 BRACCI

| Braccio | Porta | Score | Focus |
|---------|-------|-------|-------|
| **PMS Core** | 8001 | **90% LIVE** | FASE 2 Sicurezza + FASE 3 Docs DONE |
| **Miracollook** | 8002 | 10/10 | READ-ONLY. Non toccare fino PMS >= 9.0 |
| **Room Hardware** | 8003 | 10% | Bloccato VLAN, DOPO |

---

## SUBROADMAP RINASCITA - STATO (27 Feb 2026)

```
FASE 0 - Emergenze          ✅ COMPLETATA
FASE 1 - Online/Demo        ✅ COMPLETATA (miracollo.com LIVE)
FASE 2 - Sicurezza          ✅ COMPLETATA (9.2/10 Guardiana)
FASE 3 - Documentazione     ✅ COMPLETATA (9.0/10 Guardiana)
FASE 4 - Qualita Codice     ⬜ PROSSIMA (target: 8.5/10)
FASE 5 - Infrastruttura     ⬜ (CI/CD gia LIVE, script mancanti)
FASE 6 - Accessi/Stabilita  ⬜
```

---

## FASE 3 - DOCUMENTAZIONE (completata 27 Feb 2026)

### 3A - Fix Critici (P1)
```
✅ PROMPT_RIPRESA.md root -> verificato, era gia redirect corretto
✅ PROMPT_RIPRESA ecosistema -> gia aggiornato dalla sessione FASE 2
✅ .sncp/stato/oggi.md -> deprecato con redirect (hook non piu attivo)
```

### 3B - Fix Medi (P2) - 6 contraddizioni risolte
```
✅ NORD.md -> FASE 3 Feature da 60% a 80%, puntatori CervellaSwarm
✅ NORD_PMS-CORE.md -> porta :8000 corretta a :8001, score 85% a 90%
✅ stato.md PMS Core -> "React" a "HTML/CSS/JS", 85% a 90%, FASE 2 security
✅ stato.md Miracollook -> riscritto: da 92%/8.5 a 10/10, READ-ONLY
✅ FORTEZZA_MIRACOLLO.md -> container, rate limit, auth, CSP, GitHub Actions
✅ CLAUDE.md -> verificato, nessun errore
```

### 3C - Pulizia (P3) - 390 file rimossi da git
```
✅ .sncp/ locale -> README OBSOLETO, aggiunto .gitignore, git rm --cached 100 file
✅ .swarm/ -> git rm --cached 290 file, .gitignore, eliminati da disco
✅ .checkpoints/ -> 49 file eliminati (erano in .gitignore)
✅ reports/ -> 90+ file eliminati (erano in .gitignore)
✅ File orfani root -> BULK_HOUSEKEEPING + .task_output eliminati
```

### Guardiana Audit FASE 3
```
Score iniziale: 9.0/10 (4 P2 + 6 P3)
4 P2 tutti in FORTEZZA_MIRACOLLO.md:
  - Diagramma ASCII: "10r/s" -> "3 zone", "CSP Report-Only" -> "Enforce"
  - Tabella vulnerabilita: rimossi bug fixati, corretto innerHTML count
  - GitHub Actions: "DA AGGIORNARE" -> "ATTIVO, secrets aggiornati"
  - Data: "26 Feb" -> "27 Feb"
Fix P2 applicati. P3 fixati (PROMPT_RIPRESA, SUBROADMAP metriche).
```

---

## INFRASTRUTTURA LIVE

```
VM miracollo-cervella (GCP us-central1-b):
  - STATO: RUNNING
  - Machine: e2-small, x86_64, 2 vCPU, 2GB RAM (~$16/mese)
  - IP statico: 34.134.72.207
  - Path repo: /home/rafapra/app
  - Docker: backend + nginx (healthy)
  - SSL: Let's Encrypt valido fino 1 Apr 2026 (auto-renew)
  - GitHub Actions: auto-deploy ATTIVO (push master -> deploy)
  - Secrets: [tutti stored in VM .env, NON in git]
```

---

## PROSSIMI STEP

1. **FASE 4 - Qualita Codice** (prossima nella roadmap)
   - 4.1: Specializzare `except Exception` nei servizi critici
   - 4.2: Migrare `on_event("startup")` a `lifespan`
   - 4.3: Split `cm_reservation.py` (736L)
   - 4.4: Split `revenue.js` (1296L)
   - 4.5-4.7: Valutare altri split, async consistency, TODO/FIXME
2. Oppure: Fix P2 escapeHtml (security.js in 17 HTML mancanti)
3. Oppure: Nuove feature / Modulo Finanziario
4. Monitorare VM stabilita + SSL renewal (1 Apr)

## BUG NOTI RESIDUI (P3)

- ~434 innerHTML in 98 file JS (admin-only, mitigato CSP enforce + Basic Auth)
- 76 onclick handler inline (richiedono unsafe-inline in CSP)
- security.js incluso solo in 12/29 HTML (planning.html manca)
- `on_event("startup")` deprecato -> lifespan (FASE 4)

## DECISIONI CHIUSE

D1-D11 (sessioni precedenti) + D12: FASE 3 prima di FASE 4 (pulizia docs prima di codice)

## PUNTATORI

| Cosa | Path |
|------|------|
| **Subroadmap Rinascita** | `roadmaps/SUBROADMAP_RECAP_RINASCITA_2026.md` |
| Bracci | `bracci/pms-core/`, `bracci/miracallook/`, `bracci/room-hardware/` |
| FORTEZZA (guida infra) | `guide/FORTEZZA_MIRACOLLO.md` |

---

## Lezioni Apprese (Sessione FASE 3 Docs - 27 Feb 2026)

### Funzionato bene
- **Guardiana POST-audit con fix immediato** - 4a sessione consecutiva! Pattern GOLD confermato
- **git rm --cached per file storici** - rimuove dal tracking senza cancellare dal disco
- **Mappa contraddizioni PRIMA di fixare** - trovare tutte le divergenze, poi fixare in batch
- **FORTEZZA come documento critico** - contiene molte info operative, va tenuta allineata

### Non funzionato
- **FORTEZZA dimenticata nei fix P2** - la Guardiana ha trovato 4 P2 tutti li. Lezione: quando fix docs, controllare SEMPRE anche FORTEZZA

### Pattern candidato
- **Dopo ogni FASE: aggiornare FORTEZZA** - non solo NORD e PROMPT_RIPRESA, anche la guida operativa
- **390 file tracked inutilmente** - .sncp/ e .swarm/ andavano in .gitignore dal giorno 1

---

*"Lavoriamo in pace! Senza casino! Dipende da noi!"*
*Cervella & Rafa - 27 Febbraio 2026*
