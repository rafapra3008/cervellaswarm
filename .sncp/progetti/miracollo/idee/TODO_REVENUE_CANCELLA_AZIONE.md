# TODO: Cancellare Azione in Revenue Intelligence

> Data: 12 Gennaio 2026 - Sessione 173
> Segnalato da: Rafa
> Priorità: Media

---

## Cosa Manca

In Revenue Intelligence, quando si crea un'azione (suggerimento accettato), non c'è modo di **cancellarla** se cambiamo idea.

## Cosa Serve

1. **Bottone "Cancella"** su ogni azione nella lista
2. **Conferma modale** prima di cancellare
3. **API endpoint** per eliminare azione (soft delete o hard delete)
4. **Audit trail** - registrare chi ha cancellato e quando

## Dove Implementare

- Backend: `routers/action_tracking.py` - aggiungere DELETE endpoint
- Frontend: `revenue.html` o `action-history.html` - bottone cancella

## Note

Questa funzionalità era stata dimenticata durante lo sviluppo Revenue Intelligence.

---

*"I dettagli fanno SEMPRE la differenza!"*

---

## ALTRO TODO: What-If Applica Prezzo

Quando si clicca "Applica Prezzo" nel What-If Simulator:
- Attualmente mostra solo alert di successo (simulato)
- **Da implementare**: Salvare realmente il prezzo nel DB
- **Da verificare**: Che il prezzo applicato sia visibile in RateBoard/altre pagine

Questo va fatto quando implementiamo la connessione reale con il backend.
