# ROADMAP FIX SNCP - TUTTI I PROGETTI

> **Creato:** 11 Gennaio 2026 - Sessione 163
> **Priorità:** ALTA - Sistema Centrale!
> **Autore:** Regina + Guardiana Qualità

---

## PERCHÉ È CRITICO

```
+================================================================+
|                                                                |
|   "Se il sistema centrale non va, cosa succede?"               |
|                                                                |
|   SNCP = Sistema Nervoso Centrale Persistente                  |
|   È la MEMORIA di tutto. Senza memoria, siamo perse.           |
|                                                                |
|   Stato attuale: FUNZIONALE MA DISORDINATO (6/10)              |
|   Obiettivo: PULITO E SEMPLICE (10/10)                         |
|                                                                |
+================================================================+
```

---

## PROGETTI DA SISTEMARE

| Progetto | Path SNCP | Stato |
|----------|-----------|-------|
| Miracollo | ~/Developer/miracollogeminifocus/.sncp/ | 6/10 - Disordinato |
| CervellaSwarm | ~/Developer/CervellaSwarm/.sncp/ | Da verificare |
| Contabilita | ~/Developer/ContabilitaAntigravity/.sncp/ | Da verificare |

---

## DECISIONE: OPZIONE A - SEMPLIFICAZIONE RADICALE

La Guardiana Qualità raccomanda semplificazione:

> "SNCP funziona solo se lo VIVIAMO!"
> Solo 2 file vengono realmente aggiornati.
> Il resto è overhead. Semplificare = usare di più.

---

## NUOVA STRUTTURA SNCP (per TUTTI i progetti)

```
.sncp/
├── README.md              # Istruzioni chiare e REALI
├── stato/
│   └── oggi.md            # Stato OGGI - aggiornare ogni sessione!
├── coscienza/
│   └── pensieri.md        # Stream pensieri Regina
├── idee/
│   └── YYYYMMDD_nome.md   # Naming consistente con data
├── decisioni/
│   └── YYYYMMDD_cosa.md   # Decisioni prese con PERCHÉ
└── archivio/
    └── 2026-01/           # File vecchi, per mese
```

**ELIMINARE:**
- Cartelle vuote (memoria/sessioni/, memoria/lezioni/)
- File obsoleti (mappa_viva.md, prossimi_step.md vecchi)
- Sottocartelle mai usate (in_attesa/, in_studio/, integrate/)
- Cartella "perne" (typo, mai usata)

---

## ROADMAP FIX - PER SESSIONE

### SESSIONE PROSSIMA (CervellaSwarm Focus)

```
FASE 1: AUDIT TUTTI I PROGETTI (~30min)
[ ] Verificare SNCP Miracollo (già fatto - 6/10)
[ ] Verificare SNCP CervellaSwarm
[ ] Verificare SNCP Contabilita
[ ] Report con problemi per progetto

FASE 2: FIX MIRACOLLO (~1h)
[ ] Creare cartella archivio/2026-01/
[ ] Spostare file obsoleti in archivio
[ ] Eliminare cartelle vuote
[ ] Rinominare file idee/ con formato YYYYMMDD_nome.md
[ ] Aggiornare README.md con struttura REALE
[ ] Eliminare cartella "perne"

FASE 3: FIX CERVELLASWARM (~1h)
[ ] Stessa procedura di Miracollo
[ ] Allineare struttura

FASE 4: FIX CONTABILITA (~30min)
[ ] Stessa procedura
[ ] Allineare struttura

FASE 5: TEMPLATE STANDARD (~30min)
[ ] Creare template README.md per SNCP
[ ] Creare template oggi.md
[ ] Documentare regole naming
```

---

## REGOLE NAMING FILE (Nuove)

```
IDEE:
  YYYYMMDD_NOME_BREVE.md
  Esempio: 20260111_EMAIL_TEST_MODE.md

DECISIONI:
  YYYYMMDD_COSA_DECISO.md
  Esempio: 20260111_PRIORITA_SESSIONI.md

RICERCHE:
  YYYYMMDD_RICERCA_TOPIC.md
  Esempio: 20260111_RICERCA_AB_TESTING.md
```

---

## CHECKLIST MANUTENZIONE SNCP

**INIZIO SESSIONE:**
- [ ] Leggi stato/oggi.md
- [ ] Aggiorna con data/sessione corrente

**DURANTE SESSIONE:**
- [ ] Nuova idea? → idee/YYYYMMDD_nome.md
- [ ] Decisione importante? → decisioni/YYYYMMDD_cosa.md
- [ ] Pensiero? → coscienza/pensieri.md

**FINE SESSIONE:**
- [ ] Aggiorna stato/oggi.md con cosa fatto
- [ ] Commit SNCP insieme al codice

---

## STIMA TEMPO TOTALE

```
Audit tutti progetti:     30 min
Fix Miracollo:            1h
Fix CervellaSwarm:        1h
Fix Contabilita:          30 min
Template standard:        30 min
─────────────────────────────────
TOTALE:                   3h 30min (1 sessione)
```

---

## NOTE

- Fare BACKUP prima di eliminare/spostare
- Usare git per tracciare cambiamenti
- Testare che tutto funzioni dopo fix

---

*"Il sistema centrale DEVE funzionare!"*
*"Semplificare = usare di più"*

*Regina - Sessione 163*
