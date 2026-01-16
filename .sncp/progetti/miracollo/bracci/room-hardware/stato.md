# Room Hardware - Stato

> **Ultimo aggiornamento:** 16 Gennaio 2026

## In Una Riga

**Fase ricerca completata. Hardware Amazon in arrivo. Prossimo: reverse engineering VDA.**

---

## Cosa Include

- Integrazione VDA ETHEOS (NUCLEUS H155300)
- Controllo HVAC (termostati VE503)
- Sensori temperatura (AI1 bagno, AI2 ingresso)
- Automazione stanze
- (Futuro) Sistema PIN porte

## Stack (Pianificato)

| Layer | Tech | Porta |
|-------|------|-------|
| Backend | FastAPI + pymodbus | 8003 |
| Protocollo | Modbus RTU/TCP | RS-485 |

## Stato: 10%

### Completato
- Ricerca VDA (950+ righe documentazione)
- Piano Rosetta Stone
- Ordine hardware Amazon (~50 EUR)

### In Attesa
- Arrivo hardware (1-2 giorni dal 16 Gen)

### Prossimi Step
```
1. [ ] Setup Mac (driver FTDI)
2. [ ] Prima connessione VDA Nucleus
3. [ ] Sniffing passivo Modbus
4. [ ] Mappatura registri (Rosetta Stone)
5. [ ] Backend skeleton
```

## File Chiave

| File | Contenuto |
|------|-----------|
| `studi/20260116_VDA_ROSETTA_STONE_PIANO.md` | Piano reverse engineering |
| `studi/20260114_RICERCA_VDA_HARDWARE.md` | Ricerca completa VDA |
| `ROADMAP_ROOM_MANAGER_COMPLETA.md` | Roadmap dettagliata |

---

*Braccio automazione dell'ecosistema Miracollo*
*"Non esistono cose difficili, esistono cose non studiate!"*
