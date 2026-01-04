# TASK_AS5 - Feedback Tempo Reale Test

## Metadata
- **Agent:** cervella-backend
- **Livello:** 1 (BASSO)
- **Priorità:** ALTA
- **Creato:** 2026-01-04 00:15

## Obiettivo

Creare 5 funzioni helper nel file `test-orchestrazione/api/helpers.py`

## Requisiti

Implementare le seguenti 5 funzioni:

1. `format_date(date: datetime) -> str`
   - Formatta data in "DD/MM/YYYY"

2. `format_currency(amount: float, symbol: str = "EUR") -> str`
   - Formatta importo con simbolo (es. "EUR 1.234,56")

3. `truncate_string(text: str, max_length: int = 50) -> str`
   - Tronca stringa aggiungendo "..." se supera max_length

4. `capitalize_words(text: str) -> str`
   - Prima lettera di ogni parola maiuscola

5. `slugify(text: str) -> str`
   - Converte in slug URL-friendly (lowercase, trattini)

## Criteri di Successo

- [ ] File `test-orchestrazione/api/helpers.py` esiste
- [ ] Tutte e 5 le funzioni implementate
- [ ] Ogni funzione ha docstring
- [ ] Ogni funzione ha type hints
- [ ] Test manuale per ogni funzione

## Output Atteso

Scrivi l'output in `.swarm/tasks/TASK_AS5_output.md` con:
- Conferma implementazione per OGNI funzione
- Codice completo
- Test per ogni funzione

## Note

Questo e un task PIU LUNGO del solito.
Fai Triple ACK e aggiorna progress mentre lavori!
