# SESSIONI GIORNALIERE CervellaSwarm

> "Un po' ogni giorno fino al 100000%!"
> Versione 1.0 - 14 Gennaio 2026

---

## 1. TEMPLATE SESSIONE GIORNALIERA (45-90 min)

```
+================================================================+
|                                                                |
|   DURATA: 45-90 minuti                                         |
|   FREQUENZA: Quotidiana (quando Miracollo non ha urgenze)      |
|   OBIETTIVO: +0.1 score REALE ogni sessione                    |
|                                                                |
+================================================================+
```

### FASE 1: APERTURA (5 min)

```markdown
[ ] Leggi stato.md del progetto
[ ] Esegui health-check.sh
[ ] Identifica UNA cosa da fare REALE
```

**Comando:**
```bash
./scripts/sncp/health-check.sh
cat .sncp/progetti/cervellaswarm/stato.md
```

### FASE 2: FOCUS (30-60 min)

```markdown
[ ] UNA cosa alla volta
[ ] Se task > 5 min → spawn-workers
[ ] Scrivi in SNCP mentre lavori (non accumulare)
[ ] Test REALE prima di dire "fatto"
```

**Regola:** Se in 30 min non hai risultato tangibile, FERMATI e rifletti.

### FASE 3: VERIFICA (5-10 min)

```markdown
[ ] Funziona REALE? (non "dovrebbe funzionare")
[ ] Test eseguito?
[ ] Documentato in SNCP?
```

### FASE 4: CHIUSURA (5-10 min)

```markdown
[ ] Aggiorna stato.md con +REALE
[ ] Compila CHECKLIST REALE VS SU CARTA (sotto)
[ ] Commit se modifiche significative
[ ] Esegui post-session-update.sh
```

**Comando:**
```bash
./scripts/sncp/post-session-update.sh
```

---

## 2. ROADMAP PRIMO MESE

### SETTIMANA 1: FONDAMENTA (14-20 Gennaio)

| Giorno | Focus | Output REALE Atteso |
|--------|-------|---------------------|
| Lun | Testare i 4 script SNCP | Tutti funzionano |
| Mar | Usare health-check 3 volte | Abitudine iniziata |
| Mer | Mappare cosa manca per 9.0 | Lista CONCRETA |
| Gio | Fixare 1 cosa della lista | Score +0.1 |
| Ven | Review settimana | Stato aggiornato |

**Obiettivo Settimana 1:**
- Score: 7.8 -> 8.0
- Abitudine: health-check automatico

### SETTIMANA 2: CONSOLIDAMENTO (21-27 Gennaio)

| Giorno | Focus | Output REALE Atteso |
|--------|-------|---------------------|
| Lun | Delegare task a worker | 1 task completato |
| Mar | Testare comunicazione inter-agent | Handoff funziona |
| Mer | Documentare pattern che funziona | 1 workflow in SNCP |
| Gio | Ottimizzare logging | Log piu puliti |
| Ven | Review settimana | Score +0.2 |

**Obiettivo Settimana 2:**
- Score: 8.0 -> 8.2
- Abitudine: delegare sempre ai worker

### SETTIMANA 3: OTTIMIZZAZIONE (28 Gen - 3 Feb)

| Giorno | Focus | Output REALE Atteso |
|--------|-------|---------------------|
| Lun | Identificare collo di bottiglia | 1 problema chiaro |
| Mar | Risolvere collo | Fix implementato |
| Mer | Testare soluzione | Funziona REALE |
| Gio | Documentare pattern | Aggiunto a workflow |
| Ven | Review settimana | Score +0.3 |

**Obiettivo Settimana 3:**
- Score: 8.2 -> 8.5
- Abitudine: compact-state quando serve

### SETTIMANA 4: MATURITA (4-10 Febbraio)

| Giorno | Focus | Output REALE Atteso |
|--------|-------|---------------------|
| Lun | Audit completo sistema | Report onesto |
| Mar | Fix problemi trovati | 2+ fix |
| Mer | Test stress (molti task) | Sistema regge |
| Gio | Documentazione finale mese | Mappa completa |
| Ven | Retrospettiva mese | Lezioni apprese |

**Obiettivo Settimana 4:**
- Score: 8.5 -> 8.8
- Sistema STABILE e USATO quotidianamente

---

## 3. REGOLE SESSIONE

### PERMESSO

```
+ Lavorare su UNA cosa per volta
+ Delegare ai worker (spawn-workers)
+ Scrivere in SNCP mentre lavori
+ Testare REALE prima di chiudere
+ Chiedere aiuto se bloccato > 15 min
+ Fermarsi se stanco/distratto
```

### VIETATO

```
- "Fare veloce" senza testare
- Accumulare TODO senza fare
- Dire "fatto" senza test REALE
- Saltare health-check
- Ignorare errori "piccoli"
- Aggiungere "su carta" senza usare
```

### QUANDO FERMARSI E CHIEDERE

```
FERMATI SE:
- Bloccato > 15 minuti sullo stesso problema
- Non capisci PERCHE qualcosa non funziona
- Il fix richiede modifica architetturale
- Hai dubbi su approccio giusto

CHIEDI A:
- Regina (orchestrator) → decisioni strategiche
- Guardiana Qualita → review codice
- Guardiana Ricerca → come fanno gli altri
- Worker specifico → implementazione
```

### COME MISURARE SUCCESSO

```
SUCCESSO = Almeno 1 cosa REALE per sessione

REALE significa:
- Funziona (testato)
- Documentato (in SNCP)
- Usabile (non "in teoria")

NON contano:
- Codice scritto non testato
- Documentazione non usata
- Fix "parcheggiati"
```

---

## 4. INTEGRAZIONE CON MIRACOLLO

### PRIORITA

```
+================================================================+
|                                                                |
|   MIRACOLLO = REVENUE = PRIORITA #1                            |
|   CervellaSwarm = INFRASTRUTTURA = Priorita #2                 |
|                                                                |
|   Se c'e conflitto → Miracollo vince SEMPRE                    |
|                                                                |
+================================================================+
```

### ORARI SUGGERITI

| Orario | Attivita |
|--------|----------|
| Mattina (9-12) | Miracollo (focus massimo) |
| Pausa pranzo | Riposo |
| Pomeriggio (14-17) | Miracollo (se urgenze) OPPURE CervellaSwarm |
| Sera (dopo 18) | Solo se energia, CervellaSwarm leggero |

### SCHEMA SETTIMANALE IDEALE

```
Lunedi:    Miracollo AM + CervellaSwarm PM
Martedi:   Miracollo full (giorno focus)
Mercoledi: Miracollo AM + CervellaSwarm PM
Giovedi:   Miracollo full (giorno focus)
Venerdi:   Miracollo AM + Review CervellaSwarm PM
Weekend:   Riposo o sessione leggera se voglia
```

### REGOLA CONFLITTI

```
SE Miracollo ha urgenza:
  → CervellaSwarm si ferma
  → Tutto il focus su Miracollo
  → CervellaSwarm riprende quando urgenza risolta

SE CervellaSwarm ha bug critico che blocca Miracollo:
  → Diventa urgenza Miracollo
  → Fix immediato
  → Poi torna normale
```

---

## 5. CHECKLIST "REALE VS SU CARTA"

**Compila a FINE di ogni sessione CervellaSwarm:**

```markdown
## Sessione: [DATA] - CervellaSwarm

### REALE OGGI (cosa funziona ADESSO)
- [ ] ...
- [ ] ...

### SU CARTA (scritto ma non testato/usato)
- [ ] ...
- [ ] ...

### PROSSIMO REALE (da rendere reale prossima sessione)
- [ ] ...

### SCORE
- Prima: X.X/10
- Dopo:  X.X/10
- Delta: +/-X.X
```

### ESEMPIO COMPILATO

```markdown
## Sessione: 14 Gennaio 2026 - CervellaSwarm

### REALE OGGI
- [x] health-check.sh testato 2 volte
- [x] compact-state.sh funziona

### SU CARTA
- [ ] Workflow sessioni (questo file) - DA USARE domani!

### PROSSIMO REALE
- [ ] Usare questo workflow per sessione domani

### SCORE
- Prima: 7.8/10
- Dopo:  7.9/10
- Delta: +0.1
```

---

## 6. TEMPLATE RAPIDO FINE SESSIONE

Copia-incolla in stato.md:

```markdown
## [DATA] - Sessione CervellaSwarm

**Durata:** X min
**Focus:** [cosa]

**REALE:**
- ...

**SU CARTA:**
- ...

**Score:** X.X -> X.X (+X.X)

**Next:** [prossima cosa REALE]
```

---

## MANTRA SESSIONE

```
"Un po' ogni giorno fino al 100000%!"
"REALE > Su carta"
"Fatto BENE > Fatto veloce"
"UNA cosa alla volta"
```

---

*Documento creato: 14 Gennaio 2026*
*Autore: Cervella Guardiana Qualita*
*Review: Ogni fine mese*

*"Lavoriamo in pace! Senza casino! Dipende da noi!"*
