# Fix Errori Agenti - Script Swarm

> **Data:** 12 Gennaio 2026
> **Status:** DA FIXARE

---

## PROBLEMA

14 agenti hanno riferimenti a `scripts/swarm/` che:
1. Non esistono
2. Richiedono tool Bash (non disponibile per tutti)
3. Causano errori all'avvio

**Agenti interessati:**
- cervella-backend
- cervella-frontend
- cervella-data
- cervella-devops
- cervella-docs
- cervella-ingegnera
- cervella-marketing
- cervella-orchestrator
- cervella-scienziata
- cervella-security
- cervella-tester
- cervella-guardiana-qualita
- cervella-guardiana-ops
- cervella-guardiana-ricerca

---

## CAUSA ROOT

Sezione "PROTOCOLLI COMUNICAZIONE SWARM" nei DNA contiene:
```bash
scripts/swarm/update-status.sh WORKING "message"
scripts/swarm/heartbeat-worker.sh &
scripts/swarm/ask-regina.sh QUESTION "..."
```

Ma:
1. Script non esistono
2. Agenti senza tool Bash non possono eseguirli
3. Read su `.swarm/` causa EISDIR

---

## FIX GIA' APPLICATO

**cervella-researcher.md** - Sessione 172
- Sostituita sezione script con istruzioni sui tool disponibili
- Aggiunto warning EISDIR

---

## FIX DA APPLICARE

Per ogni agente:
1. Rimuovere riferimenti a `scripts/swarm/`
2. Sostituire con istruzioni appropriate per i tool disponibili
3. Aggiungere sezione "TOOL DISPONIBILI"

**Template fix:**
```markdown
## TOOL DISPONIBILI

I tuoi tool:
- [lista tool specifici per agente]

NON HAI:
- [tool non disponibili]

## COMUNICAZIONE

La tua comunicazione e' il RISULTATO che restituisci.
La Regina leggera' il tuo output.
```

---

## PRIORITA'

- ALTA: Guardiane (usate frequentemente)
- MEDIA: Worker specializzati
- BASSA: Agenti meno usati

---

## PIANO

1. [ ] Fix cervella-guardiana-qualita
2. [ ] Fix cervella-guardiana-ops
3. [ ] Fix cervella-guardiana-ricerca
4. [ ] Fix cervella-backend
5. [ ] Fix cervella-frontend
6. [ ] Fix altri (batch)

---

*Da completare in prossima sessione dedicata*
