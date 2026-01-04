# TASK_AS3 - Error Handling Graceful Test

## Metadata
- **Agent:** cervella-backend
- **Livello:** 1 (BASSO)
- **Priorità:** ALTA
- **Creato:** 2026-01-04 00:00

## Obiettivo

Creare una funzione che tenta di leggere un file che NON ESISTE.
Questo task è intenzionalmente impossibile - vogliamo vedere come gestisci l'errore!

## Requisiti

1. Creare il file `test-orchestrazione/api/file_reader.py`
2. Implementare la funzione `read_config()` che tenta di leggere `/path/che/non/esiste/config.json`
3. La funzione DEVE gestire l'errore gracefully (try/except)
4. Ritornare un dict con `{"error": "File not found", "fallback": "default_config"}`

## Criteri di Successo

- [ ] File `test-orchestrazione/api/file_reader.py` esiste
- [ ] Funzione `read_config()` esiste
- [ ] Gestisce FileNotFoundError
- [ ] Ritorna fallback invece di crashare
- [ ] Ha docstring che spiega il comportamento

## Output Atteso

Scrivi l'output in `.swarm/tasks/TASK_AS3_output.md` con:
- Conferma implementazione
- Codice scritto
- Test manuale (chiamata funzione - deve ritornare fallback!)
- Spiegazione di come hai gestito l'errore

## Note

Questo è un HARDTEST per verificare ERROR HANDLING GRACEFUL.
Il file /path/che/non/esiste/config.json NON ESISTE - è intenzionale!
Fai Triple ACK prima di iniziare!
