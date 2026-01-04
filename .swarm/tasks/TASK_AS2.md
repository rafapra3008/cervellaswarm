# TASK_AS2 - Triple Check Automatico Test

## Metadata
- **Agent:** cervella-backend
- **Livello:** 2 (MEDIO) - Richiede review Guardiana!
- **Priorità:** ALTA
- **Creato:** 2026-01-04 00:15

## Obiettivo

Creare la funzione `validate_name()` nel file `test-orchestrazione/api/validators.py`

## Requisiti

1. Creare il file `test-orchestrazione/api/validators.py`
2. Implementare la funzione `validate_name(name: str) -> bool`
3. Validare che:
   - Nome non sia vuoto
   - Nome non superi 100 caratteri
   - Nome contenga solo lettere, spazi e trattini
4. Ritornare `True` se valido, `False` altrimenti

## Criteri di Successo

- [ ] File `test-orchestrazione/api/validators.py` esiste
- [ ] Funzione `validate_name()` esiste
- [ ] Validazione nome vuoto funziona
- [ ] Validazione lunghezza max 100 funziona
- [ ] Validazione caratteri funziona
- [ ] Ha docstring con esempi

## Output Atteso

Scrivi l'output in `.swarm/tasks/TASK_AS2_output.md` con:
- Conferma implementazione
- Codice scritto
- Test con casi validi e invalidi

## Note

LIVELLO 2 = Dopo completamento, la Guardiana fara review!
Fai Triple ACK prima di iniziare!
