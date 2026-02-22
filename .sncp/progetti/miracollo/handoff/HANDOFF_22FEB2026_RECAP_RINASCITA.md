# HANDOFF - 22 Febbraio 2026 - Recap & Rinascita

> **Per la prossima Cervella: leggi TUTTO questo file prima di agire.**

---

## COSA E SUCCESSO

Rafa e tornato su Miracollo dopo ~1 mese. Prima sessione con Opus 4.6.
Ha chiesto un "recap gigante" - analisi completa di codice, docs, infrastruttura.

### 3 Audit Paralleli Eseguiti

**1. INGEGNERA (Code Review)**
- Health codice: 6.5/10
- 4 CRITICI: bug guests.py, auth 5.8%, DB backup in git, .env.production locale
- 5 ALTI: except generico, f-string SQL, rate limiting in-memory, report in git, on_event deprecato
- 396 endpoint in 83 router files analizzati
- 13 file Python >650 righe, revenue.js 1296 righe
- ~362 innerHTML senza escape in 82 file JS

**2. GUARDIANA QUALITA (Docs)**
- Health docs: 6.5/10
- 3 CRITICI: PROMPT_RIPRESA root fossile (S167), ecosistema stale (S300), SNCP locale morto
- 6+ contraddizioni tra file (scores, porte, container names)
- ~250 file orfani (.checkpoints, .swarm/tasks, reports/)
- NORD.md: FASE 3 dice 60% ma e 80% (4/5 done)

**3. DEVOPS (Infrastruttura)**
- VM miracollo-cervella: PAUSA, zona us-central1-b, internal 10.128.0.7
- IP esterno NON fisso (rilasciato in pausa)
- DNS miracollo.com punta a IP sbagliato
- SSH config ha 2 entry (miracollo-vm + cervellamiracollo), entrambe probabilmente stale
- Raccomandazione: 2 VM separate (Miracollo e2-small + Contabilita g1-small) = ~$36/mese
- Contabilita NON si tocca!

---

## COSA E STATO CREATO/AGGIORNATO

| File | Azione |
|------|--------|
| `roadmaps/SUBROADMAP_RECAP_RINASCITA_2026.md` | CREATO - Piano 6 fasi, validato Guardiana 8.8/10 |
| `PROMPT_RIPRESA_miracollo.md` | AGGIORNATO - Panorama ecosistema con audit |
| `bracci/pms-core/PROMPT_RIPRESA_pms-core.md` | AGGIORNATO - Con risultati audit |
| `miracollogeminifocus/PROMPT_RIPRESA.md` (ROOT) | RISCRITTO - Ora e solo un redirect |
| Questo handoff | CREATO |

## COSA NON E STATO TOCCATO

- ZERO righe di codice modificate
- ZERO file di produzione
- NORD.md NON aggiornato (servira in FASE 3)
- Miracollook PROMPT_RIPRESA non modificato (era gia OK, S324)
- Room Hardware PROMPT_RIPRESA non modificato (bloccato su VLAN)
- VM non riattivata
- DNS non toccato

---

## SUBROADMAP - LE 6 FASI

```
FASE 0 - EMERGENZE (~25 min)
  0.1 Fix BUG guests.py (22 colonne, 9 placeholder)
  0.2 Verificare .env.production non in git history
  0.3 Aggiungere reports/ a .gitignore
  0.4 Fix uptime_seconds

FASE 1 - DEMO DITTA TEDESCA (1-2 sessioni, serve Rafa)
  1.1-1.3  Riattivare VM + IP statico + SSH config
  1.4      Chiarire cervellamiracollo (VM vecchia?)
  1.5      Aggiornare DNS miracollo.com
  1.6-1.9  Tag HTTPS, SSL, docker-compose up, smoke test
  1.10     Valutare downgrade VM

FASE 2 - SICUREZZA (3-5 giorni)
  2.1 Auth su 396 endpoint (1-2 giorni)
  2.2 Content-Security-Policy header
  2.3 Triage + fix XSS (~362 innerHTML)
  2.4 Rimuovere DB backup da git history
  2.5 Valutare rate limiting Redis

FASE 3 - DOCUMENTAZIONE (1-2 sessioni)
  3A Fix critici (3 file stale/contraddittori)
  3B Fix medi (NORD.md, stati, container names)
  3C Pulizia (~250 file orfani)

FASE 4 - QUALITA CODICE (2-3 sessioni)
  except Exception, on_event, split file, async/def, TODO

FASE 5 - INFRASTRUTTURA (1-2 sessioni)
  SSH, porte, nginx, deploy scripts, backup cron, CI/CD
  (deploy.sh, pre_deploy_snapshot.sh, rollback.sh, cron_backup_db.sh)

FASE 6 - ACCESSI (1 sessione)
  Verifiche finali
```

---

## DECISIONI CHIUSE (22 Feb 2026 - Rafa ha risposto)

| # | Decisione | Risposta |
|---|-----------|----------|
| D1 | VM size | **e2-small** (~$16/mese) - piu economica per ora |
| D2 | cervellamiracollo | VM probabilmente gia eliminata su GCP. Rimuovere entry SSH config |
| D3 | DNS registrar | **register.it** - Rafa aggiorna record A quando serve |
| D4 | Timeline demo | NON urgente - piano piano, con calma |
| D5 | VLAN 1101 | DOPO - non preoccuparsi ora |

---

## CONTESTO IMPORTANTE

- Rafa ha detto "abbiamo trovato ORO su contabilita per i dati Ericsoft SQL"
  (connessione diretta al DB SQL di Ericsoft funziona)
- Rafa vuole "sistemare la struttura Docker/VM/porte"
  (conflitto porte con Contabilita in locale)
- Contabilita e ben impostata su Docker (porte 8000, 8001, 8003)
  MA: NON toccare Contabilita! Solo studiare.
- Prima sessione con Opus 4.6 - "la famiglia e molto piu avanti"

---

## COME RIPRENDERE

1. Leggi questo handoff
2. Leggi la SUBROADMAP: `roadmaps/SUBROADMAP_RECAP_RINASCITA_2026.md`
3. Chiedi a Rafa: "Da quale FASE partiamo?"
4. Se Rafa non sa: FASE 0 (emergenze, 25 min) e il default sicuro
5. Ogni FASE completata -> Guardiana audit -> target 9.5

---

*"Lavoriamo in pace! Senza casino! Dipende da noi!"*
*22 Febbraio 2026 - Recap & Rinascita*
