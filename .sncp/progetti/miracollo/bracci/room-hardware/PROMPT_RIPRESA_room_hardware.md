# PROMPT RIPRESA - Room Hardware

> **Ultimo aggiornamento:** 16 Gennaio 2026 - Sessione 231
> **Braccio 3 dell'ecosistema Miracollo**

---

## STATO IN UNA RIGA

**Ricerca VDA completata (21 file). Hardware Amazon in arrivo. Prossimo: reverse engineering Modbus.**

---

## COS'E ROOM HARDWARE

Braccio automazione stanze dell'ecosistema Miracollo.

| Funzione | Descrizione |
|----------|-------------|
| HVAC | Controllo termostati VDA VE503 |
| Sensori | Temperatura bagno (AI1), ingresso (AI2) |
| Automazione | Check-in/out automatico |
| Energia | Risparmio energetico quando camera vuota |
| (Futuro) | Sistema PIN porte |

---

## HARDWARE TARGET

```
VDA ETHEOS - NUCLEUS I/O RCU
Modello: H155300 v1.4
Firmware: 5.4.1
Protocollo: Modbus RTU (RS-485) / TCP (Ethernet)

PORTE MODBUS: M1, M2, M3, M4
DIGITAL OUT: DO1-DO8 (Rele 250Vac)
DIGITAL IN: DI1-DI5 (Contatti)
ANALOG IN: AI1 (bagno), AI2 (ingresso)
ANALOG OUT: AO1-AO3 (0-10V)
```

---

## HARDWARE ORDINATO (Amazon)

| Item | Uso | Stato |
|------|-----|-------|
| USB-RS485 FTDI | Converter Mac | In arrivo |
| Multimetro | Verifica tensioni | In arrivo |
| Cacciaviti | Apertura pannelli | In arrivo |
| Jumper | Test collegamenti | In arrivo |

**Totale:** ~50 EUR | **Arrivo:** 1-2 giorni dal 16 Gen

---

## PIANO ROSETTA STONE

```
1. [ ] Setup Mac (driver FTDI, software sniffing)
2. [ ] Prima connessione (Ethernet o RS-485)
3. [ ] Sniffing PASSIVO (solo ascolto!)
4. [ ] Decodifica pattern Modbus
5. [ ] Mappatura registri -> VDA_REGISTER_MAP.md
6. [ ] Backend skeleton con pymodbus
```

**Filosofia:** "Non esistono cose difficili, esistono cose non studiate!"

---

## FILE CHIAVE

| File | Contenuto |
|------|-----------|
| `studi/20260116_VDA_ROSETTA_STONE_PIANO.md` | Piano reverse engineering |
| `studi/20260114_RICERCA_VDA_HARDWARE.md` | Ricerca completa (950 righe) |
| `ROADMAP_ROOM_MANAGER_COMPLETA.md` | Roadmap dettagliata |
| `stato.md` | Stato breve |

---

## STACK PIANIFICATO

| Layer | Tech | Porta |
|-------|------|-------|
| Backend | FastAPI + pymodbus | 8003 |
| Codice | `miracollogeminifocus/room-hardware/` | - |

---

## STATO: 10%

- Ricerca: COMPLETA
- Hardware: IN ARRIVO
- Codice: SKELETON
- Registri VDA: DA MAPPARE

---

*Braccio 3 - Automazione Stanze*
*"Il nostro modo. Indipendenza totale."*
