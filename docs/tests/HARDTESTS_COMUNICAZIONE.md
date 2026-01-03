# HARDTESTS - Flusso Comunicazione Guardiane

> **"Il segreto e la comunicazione! Testiamola!"**

**Data Creazione:** 2 Gennaio 2026
**Versione:** 1.0.0
**Scopo:** Verificare che il flusso Regina -> Guardiane -> Worker funzioni

---

## RIFERIMENTO

- **GUIDA_COMUNICAZIONE v2.0**: `docs/guide/GUIDA_COMUNICAZIONE.md`
- **3 Livelli di Rischio**: BASSO (1), MEDIO (2), ALTO (3)
- **Guardiane**: Qualita, Ops, Ricerca

---

## IL FLUSSO DA TESTARE

```
1. Regina riceve task
2. Regina + Guardiana decidono LIVELLO
3. Regina delega a Worker con CONTESTO COMPLETO
4. Worker completa
5. SE Livello 2-3: Guardiana verifica
6. SE problemi: Guardiana istruisce Worker
7. Task completato
```

---

## TEST 1: LIVELLO 1 (BASSO RISCHIO) - NO GUARDIANA

### Scenario
Task a basso rischio: documentazione, typo fix, ricerca.
La Guardiana NON deve intervenire (o solo spot check random).

### Setup

**Task:** Aggiornare un commento in un file di docs.

### Prompt da Usare (Regina -> Worker)

```markdown
## TASK PER cervella-docs

### CONTESTO

**PERCHE:**
Il README ha un typo nella sezione "Installation".

**LIVELLO RISCHIO:** 1 (BASSO)
**SUPERVISIONE:** Nessuna (trust-but-verify)

**CRITERI DI SUCCESSO:**
- [ ] Typo corretto
- [ ] Nessun altro cambiamento

**FILE DA MODIFICARE:**
- test-orchestrazione/README.md

### IL TASK

Correggi "instalation" -> "installation" nel README.

### OUTPUT ATTESO

File aggiornato con typo corretto.
```

### Comportamento Atteso

```
REGINA:
- Identifica: task Livello 1
- Delega DIRETTAMENTE a cervella-docs (NO consulto Guardiana)
- Verifica risultato (spot check)

WORKER (cervella-docs):
- Procede immediatamente
- Corregge typo
- Ritorna output

GUARDIANA:
- NON interviene (o random 10% spot check)
```

### Checklist Verifica

- [ ] Regina ha delegato SENZA consultare Guardiana?
- [ ] Worker ha proceduto immediatamente?
- [ ] Typo e stato corretto?
- [ ] Nessun overhead di verifica?

### Risultato Test

| Data | Esito | Note |
|------|-------|------|
| 2 Gen 2026 | PASS | Zero domande! Worker ha proceduto immediatamente. Typo corretti in ~5 sec. |

---

## TEST 2: LIVELLO 2 (MEDIO RISCHIO) - GUARDIANA DOPO

### Scenario
Task a medio rischio: nuova feature, refactoring.
La Guardiana verifica DOPO che il Worker completa.

### Setup

**Task:** Creare una nuova funzione utility in Python.

### Prompt 1: Regina -> Guardiana (Consultazione)

```markdown
## CONSULTAZIONE LIVELLO

**Task ricevuto:** Creare funzione `format_date()` in utils.py

**Domanda:** Che livello di rischio?

**Mia valutazione:**
- E' codice nuovo (non modifica esistente)
- File utility (non critico)
- Reversibile facilmente

**Propongo:** Livello 2 (MEDIO)
```

### Prompt 2: Regina -> Worker (Delega)

```markdown
## TASK PER cervella-backend

### CONTESTO

**PERCHE:**
Ci serve una funzione per formattare date in modo consistente.

**LIVELLO RISCHIO:** 2 (MEDIO)
**SUPERVISIONE:** cervella-guardiana-qualita verifichera dopo

**CRITERI DI SUCCESSO:**
- [ ] Funzione `format_date(date, format)` creata
- [ ] Gestisce formati: "DD/MM/YYYY", "YYYY-MM-DD", "human"
- [ ] Gestisce date None/invalid con fallback
- [ ] Type hints presenti
- [ ] Docstring presente

**FILE DA MODIFICARE:**
- test-orchestrazione/api/utils.py (creare se non esiste)

**CHI VERIFICHERA:**
La Guardiana della Qualita controllera:
- Type hints corretti
- Error handling presente
- Docstring completa

### IL TASK

Crea la funzione `format_date()` in utils.py.

### OUTPUT ATTESO

```python
def format_date(date: Optional[datetime], format: str = "DD/MM/YYYY") -> str:
    """..."""
```
```

### Prompt 3: Regina -> Guardiana (Verifica)

```markdown
## VERIFICA PER cervella-guardiana-qualita

### Task Originale
Creare funzione `format_date()` in utils.py

### PERCHE Originale
Ci serve una funzione per formattare date in modo consistente.

### Criteri di Successo
- [ ] Funzione `format_date(date, format)` creata
- [ ] Gestisce formati: "DD/MM/YYYY", "YYYY-MM-DD", "human"
- [ ] Gestisce date None/invalid con fallback
- [ ] Type hints presenti
- [ ] Docstring presente

### File da Verificare
- test-orchestrazione/api/utils.py

### Worker che ha eseguito
cervella-backend

### Output del Worker
[Output ricevuto dal worker]

### Richiesta
Verifica che il codice rispetti i criteri. Report strutturato.
```

### Comportamento Atteso

```
REGINA:
1. Riceve task
2. Identifica dominio: codice (Guardiana Qualita)
3. Consulta Guardiana per livello -> LIVELLO 2
4. Delega a cervella-backend con CONTESTO COMPLETO
5. Riceve output
6. Passa output a Guardiana per verifica

WORKER (cervella-backend):
- Riceve task con contesto completo
- Procede (sa che verra verificato)
- Crea funzione con criteri
- Ritorna output strutturato

GUARDIANA:
- Riceve output + PERCHE + criteri
- Verifica punto per punto
- Ritorna report: APPROVATO o PROBLEMI

SE PROBLEMI:
- Guardiana indica fix specifici
- Regina istruisce Worker
- Worker corregge
- Loop fino ad APPROVATO
```

### Checklist Verifica

- [ ] Regina ha consultato Guardiana PRIMA di delegare?
- [ ] Worker ha ricevuto CONTESTO COMPLETO?
- [ ] Worker sapeva che sarebbe stato verificato?
- [ ] Guardiana ha ricevuto PERCHE + criteri + output?
- [ ] Report Guardiana e strutturato?
- [ ] SE problemi: loop corretto fino ad approvazione?

### Risultato Test

| Data | Esito | Note |
|------|-------|------|
| 2 Gen 2026 | PASS | Flusso completo funzionante! Guardiana ha verificato e APPROVATO. Report strutturato eccellente. |

---

## TEST 3: LIVELLO 3 (ALTO RISCHIO) - GUARDIANA SEMPRE + RAFA

### Scenario
Task ad alto rischio: modifica auth, deploy, dati sensibili.
La Guardiana verifica SEMPRE + serve conferma Rafa.

### Setup

**Task:** Script per eliminare dati vecchi dal database.

### Prompt 1: Regina -> Guardiana Ops (Consultazione)

```markdown
## CONSULTAZIONE LIVELLO

**Task ricevuto:** Creare script cleanup per eliminare record vecchi

**Domanda:** Che livello di rischio?

**Mia valutazione:**
- DELETE su database
- IRREVERSIBILE
- Dati potenzialmente importanti

**Propongo:** Livello 3 (ALTO) + conferma Rafa
```

### Prompt 2: Regina -> Rafa (Conferma)

```markdown
## RICHIESTA APPROVAZIONE

**Task:** Script cleanup database

**Livello:** 3 (ALTO RISCHIO)

**Motivo alto rischio:**
- DELETE irreversibile
- Dati utenti coinvolti

**Proposta:**
1. Creo script con DRY RUN mode
2. Prima eseguo DRY RUN (mostra cosa eliminerebbe)
3. Solo dopo tua conferma, eseguo reale

**Procedo con creazione script (solo DRY RUN)?**
```

### Prompt 3: Regina -> Worker (Delega)

```markdown
## TASK PER cervella-backend

### CONTESTO

**PERCHE:**
Dobbiamo pulire record vecchi dal database per mantenere performance.

**LIVELLO RISCHIO:** 3 (ALTO)
**SUPERVISIONE:**
- cervella-guardiana-ops verifichera
- Rafa ha approvato creazione (solo DRY RUN mode!)

**CRITERI DI SUCCESSO:**
- [ ] Script cleanup.py creato
- [ ] Flag --dry-run OBBLIGATORIO per default
- [ ] Flag --force per esecuzione reale
- [ ] Log dettagliato di cosa eliminerebbe
- [ ] Conferma manuale prima di DELETE reale

**FILE DA MODIFICARE:**
- test-hardtests/src/api/cleanup.py

**CHI VERIFICHERA:**
La Guardiana delle Operazioni controllera:
- DRY RUN mode funzionante
- Nessuna esecuzione automatica DELETE
- Log chiaro e completo
- Conferma manuale presente

**ATTENZIONE:**
Questo e un task ALTO RISCHIO. Il codice NON deve MAI eseguire
DELETE senza --force esplicito e conferma utente.

### IL TASK

Crea script cleanup.py con:
1. DRY RUN mode di default
2. --force per esecuzione reale
3. Conferma manuale prima di DELETE

### OUTPUT ATTESO

Script funzionante che in DRY RUN mostra solo cosa eliminerebbe.
```

### Prompt 4: Regina -> Guardiana Ops (Verifica)

```markdown
## VERIFICA PER cervella-guardiana-ops

### Task Originale
Script cleanup database con DRY RUN

### LIVELLO
3 (ALTO RISCHIO) - Approvato da Rafa solo per DRY RUN

### PERCHE Originale
Pulire record vecchi mantenendo performance.

### Criteri di Successo
- [ ] Script cleanup.py creato
- [ ] Flag --dry-run OBBLIGATORIO per default
- [ ] Flag --force per esecuzione reale
- [ ] Log dettagliato
- [ ] Conferma manuale presente

### ATTENZIONE SPECIALE
Verifica che NON ci sia modo di eseguire DELETE senza:
1. Flag --force
2. Conferma manuale

### File da Verificare
- test-hardtests/src/api/cleanup.py

### Worker che ha eseguito
cervella-backend

### Output del Worker
[Output ricevuto dal worker]

### Richiesta
Verifica RIGOROSA. Questo e codice ad alto rischio.
Report con APPROVATO/BLOCCATO.
```

### Comportamento Atteso

```
REGINA:
1. Riceve task
2. Identifica: DELETE = ALTO RISCHIO
3. Consulta Guardiana Ops -> LIVELLO 3
4. Chiede conferma a Rafa
5. Rafa approva (solo DRY RUN)
6. Delega con CONTESTO + ATTENZIONE
7. Passa output a Guardiana per verifica RIGOROSA

WORKER (cervella-backend):
- Riceve task con ATTENZIONE evidenziata
- Crea script con safety by default
- DRY RUN mode obbligatorio
- Conferme multiple

GUARDIANA OPS:
- Verifica RIGOROSA
- Cerca ogni modo per bypassare safety
- APPROVATO solo se 100% sicuro
- BLOCCATO se trova rischi

SE BLOCCATO:
- Guardiana spiega rischi specifici
- Worker deve correggere
- Loop fino a APPROVATO
- Poi Regina riporta a Rafa
```

### Checklist Verifica

- [ ] Regina ha consultato Guardiana PRIMA?
- [ ] Regina ha chiesto conferma a Rafa?
- [ ] Worker ha ricevuto ATTENZIONE chiara?
- [ ] Script ha DRY RUN di default?
- [ ] Script richiede --force + conferma?
- [ ] Guardiana ha verificato RIGOROSAMENTE?
- [ ] Report indica ogni potenziale rischio?
- [ ] Nessun modo per eseguire DELETE accidentale?

### Risultato Test

| Data | Esito | Note |
|------|-------|------|
| 2 Gen 2026 | PASS | Loop completo! Guardiana ha BLOCCATO (2 vulnerabilità), Worker ha corretto, Guardiana ha APPROVATO. Flusso sicurezza perfetto! |

---

## METRICHE SUCCESSO

| Metrica | Target | Attuale |
|---------|--------|---------|
| Test 1 (Livello 1 senza Guardiana) | PASS | PASS |
| Test 2 (Livello 2 con Guardiana dopo) | PASS | PASS |
| Test 3 (Livello 3 con Guardiana sempre) | PASS | PASS |
| Comunicazione strutturata | SI | SI |
| PERCHE sempre presente | SI | SI |
| Criteri sempre chiari | SI | SI |
| Report Guardiana strutturato | SI | SI |

**TUTTI I TEST PASSATI! 3/3**

---

## STORICO TEST

### Sessione 58 - 2 Gennaio 2026 - TUTTI I TEST PASSATI!

- **Test eseguiti:** 3/3 completati con successo!
- **Risultati:**
  - TEST 1 (Livello 1): PASS - Worker procede senza Guardiana, zero overhead
  - TEST 2 (Livello 2): PASS - Guardiana verifica dopo, report strutturato
  - TEST 3 (Livello 3): PASS - Guardiana BLOCCA vulnerabilita, loop di fix funziona!
- **Scoperte:**
  - Guardiana Ops ha trovato 2 vulnerabilita REALI (LIMIT in SQLite, bypass legacy)
  - Il flusso di sicurezza funziona: BLOCCO -> FIX -> RI-VERIFICA -> APPROVATO
- **Conclusione:** IL SISTEMA DI COMUNICAZIONE FUNZIONA!

### Sessione 57 - 2 Gennaio 2026

- **GUIDA_COMUNICAZIONE v2.0 creata**
- **3 livelli di rischio definiti**
- **Flusso Regina -> Guardiane -> Worker progettato**

---

*"Il segreto e la comunicazione!"*

*"Se risolviamo la comunicazione, sara MAGIA!"*

**CervellaSwarm Team**
