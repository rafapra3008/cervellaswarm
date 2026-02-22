<!-- DISCRIMINATORE: ECOSISTEMA MIRACOLLO - PANORAMA -->
<!-- QUESTO FILE: Overview dei 3 bracci, NON dettagli specifici -->
<!-- Per dettagli: vai in bracci/{nome}/PROMPT_RIPRESA_{nome}.md -->

# PROMPT RIPRESA - Ecosistema Miracollo

> **Ultimo aggiornamento:** 22 Febbraio 2026
> **Status:** VM in pausa, audit completato, SUBROADMAP RINASCITA pronta

---

## I 3 BRACCI

```
+================================================================+
|   ECOSISTEMA MIRACOLLO = 3 BRACCI INDIPENDENTI                 |
+================================================================+

├── PMS CORE (:8001)        Sistema alberghiero     90% LIVE
├── MIRACOLLOOK (:8002)     Email client AI         10/10
└── ROOM HARDWARE (:8003)   Domotica                10% (bloccato VLAN)
```

---

## STATO RAPIDO

| Braccio | Porta | Score | Focus Attuale |
|---------|-------|-------|---------------|
| **PMS Core** | 8001 | 90% LIVE | RINASCITA: audit code 6.5/10, serve auth+security |
| **Miracollook** | 8002 | 10/10 | READ-ONLY da Ericsoft. Non toccare fino PMS >= 9.0 |
| **Room Hardware** | 8003 | 10% | Bloccato: serve admin VLAN 1101 |

---

## SITUAZIONE INFRASTRUTTURA (22 Feb 2026)

```
VM miracollo-cervella (GCP us-central1-b):
  - STATO: IN PAUSA (costi sospesi)
  - Internal IP: 10.128.0.7
  - External IP: NON FISSO (rilasciato in pausa)
  - Specs: ARM64, 2 vCPU, 4GB RAM

DNS miracollo.com:
  - DA AGGIORNARE dopo riattivazione VM + IP statico

SSH config (~/.ssh/config):
  - miracollo-vm -> 34.27.179.164 (IP VECCHIO, da aggiornare)
  - cervellamiracollo -> 104.197.100.249 (PROBABILMENTE OBSOLETO, chiedere Rafa)
```

---

## AUDIT 22 FEBBRAIO - RISULTATI

```
INGEGNERA (codice):    6.5/10 - 4 critici, 5 alti
GUARDIANA QA (docs):   6.5/10 - 3 critici, 8 medi, ~250 file orfani
DEVOPS (infra):        VM spenta, DNS sbagliato, raccomanda ~$36/mese
```

**BUG CRITICO:** `guests.py:74-88` - INSERT 22 colonne ma 9 placeholder
**SICUREZZA:** Solo 23/396 endpoint hanno autenticazione (5.8%)
**XSS:** ~362 innerHTML senza escape in 82 file JS

---

## SUBROADMAP ATTIVA

**File:** `roadmaps/SUBROADMAP_RECAP_RINASCITA_2026.md`
**Score Guardiana:** 8.8/10 (APPROVED WITH NOTES, correzioni applicate)

```
FASE 0 - Emergenze (bug, .gitignore)
FASE 1 - Demo ditta tedesca (VM, IP, DNS)
FASE 2 - Sicurezza (auth, XSS, CSP)
FASE 3 - Documentazione (sync, pulizia)
FASE 4 - Qualita codice (except, split)
FASE 5 - Infrastruttura (SSH, porte, CI/CD)
FASE 6 - Accessi (verifiche finali)
```

---

## DECISIONI CHIUSE (22 Feb 2026)

| # | Decisione | Risposta |
|---|-----------|----------|
| D1 | VM size | **e2-small** (~$16/mese) |
| D2 | cervellamiracollo SSH | VM probabilmente eliminata. Rimuovere entry SSH config |
| D3 | DNS | **register.it** - Rafa aggiorna record A |
| D4 | Demo tedesca | NON urgente, piano piano |
| D5 | Room Hardware | DOPO, non ora |

---

## PROMPT_RIPRESA PER BRACCIO

| Braccio | File |
|---------|------|
| PMS Core | `bracci/pms-core/PROMPT_RIPRESA_pms-core.md` |
| Miracollook | `bracci/miracallook/PROMPT_RIPRESA_miracollook.md` |
| Room Hardware | `bracci/room-hardware/PROMPT_RIPRESA_room_hardware.md` |

---

## REGOLA DISAMBIGUAZIONE

```
Se Rafa dice "Miracollo" senza specificare -> CHIEDI quale braccio!

Keywords:
- "PMS", "prenotazioni", "fatture" -> PMS Core (8001)
- "email", "Gmail", "Look" -> Miracollook (8002)
- "room", "domotica", "sensori" -> Room Hardware (8003)
```

---

*"Non abbiamo fretta. Vogliamo la PERFEZIONE."*
*Cervella & Rafa - 22 Febbraio 2026*

