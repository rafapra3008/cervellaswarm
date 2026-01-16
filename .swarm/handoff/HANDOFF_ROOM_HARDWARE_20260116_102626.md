# HANDOFF - Room Hardware (Braccio 3)

> **Data:** 16 Gennaio 2026 - Sessione 231
> **Da:** Regina (Opus)
> **Per:** Prossima sessione Room Hardware

---

## COSA E ROOM HARDWARE

Braccio automazione stanze dell'ecosistema Miracollo.
Integrazione con sistema VDA ETHEOS esistente nell'hotel.

---

## STATO ATTUALE: 10%

| Fase | Stato |
|------|-------|
| Ricerca VDA | COMPLETA (21 file, 950+ righe) |
| Hardware Amazon | IN ARRIVO (1-2 giorni dal 16 Gen) |
| Codice | SKELETON (main.py porta 8003) |
| Registri VDA | DA MAPPARE |

---

## HARDWARE TARGET

```
VDA ETHEOS - NUCLEUS I/O RCU
Modello: H155300 v1.4
Firmware: 5.4.1
MAC: 00:08:0C:20:1F:6D

MODBUS: M1, M2, M3, M4 (RS-485)
ETHERNET: RJ45 (Modbus TCP?)
SENSORI: AI1=bagno, AI2=ingresso
```

---

## HARDWARE ORDINATO

| Item | Prezzo | Uso |
|------|--------|-----|
| USB-RS485 FTDI (SH-U11L) | 19 EUR | Converter Mac |
| Multimetro Electraline | 12 EUR | Verifica tensioni |
| Cacciaviti MAXWARE | 10 EUR | Apertura pannelli |
| Jumper ELEGOO | 8 EUR | Test collegamenti |

**Totale:** ~50 EUR

---

## PIANO ROSETTA STONE

### Quando Arriva Hardware:

```
STEP 1: Setup Mac
- Driver FTDI (probabilmente automatico macOS)
- ls /dev/tty.usbserial*
- Software: CoolTerm, ModbusSniffer

STEP 2: Prima Connessione
OPZIONE A (Ethernet):
- Cavo RJ45 Mac -> NUCLEUS
- nmap -sP 192.168.x.0/24
- Test Modbus TCP porta 502

OPZIONE B (RS-485):
- USB-RS485 -> porta M1
- Parametri: 9600 8N1

STEP 3: Sniffing PASSIVO
- NON mandare comandi!
- Solo ASCOLTARE traffico
- Registrare pattern

STEP 4: Mappatura Registri
- Documentare in VDA_REGISTER_MAP.md
- Ogni registro con: address, tipo, device, significato
```

---

## FILE CHIAVE

| File | Contenuto |
|------|-----------|
| `PROMPT_RIPRESA_room_hardware.md` | Stato completo |
| `stato.md` | Stato breve |
| `studi/20260116_VDA_ROSETTA_STONE_PIANO.md` | Piano dettagliato |
| `studi/20260114_RICERCA_VDA_HARDWARE.md` | Ricerca completa |
| `ROADMAP_ROOM_MANAGER_COMPLETA.md` | Roadmap |

**Path:** `.sncp/progetti/miracollo/bracci/room-hardware/`

---

## CODICE

```
miracollogeminifocus/room-hardware/
├── README.md
├── backend/
│   ├── main.py (skeleton FastAPI :8003)
│   ├── routers/
│   ├── services/
│   └── models/
├── docs/
└── tests/
```

---

## PROSSIMI STEP

```
1. [ ] Verificare arrivo hardware Amazon
2. [ ] Setup Mac (driver, software)
3. [ ] Prima connessione VDA
4. [ ] Sniffing passivo
5. [ ] Mappatura registri
6. [ ] Backend con pymodbus
```

---

## DECISIONE CHIAVE

```
DECISIONE: Facciamo il NOSTRO modo. Nessun contatto con VDA.
MOTIVO: VDA e' "squifoso" - vendor lock-in, closed system
OBIETTIVO: Indipendenza totale, controllo nostro
```

---

## ATTENZIONE

```
NESSUNO HA MAI DOCUMENTATO PUBBLICAMENTE I REGISTRI VDA!

Saremo i PRIMI a creare la Rosetta Stone.
Questo e' reverse engineering - procedi con cautela.
Sniffing PASSIVO prima di qualsiasi comando.
```

---

*"Non esistono cose difficili, esistono cose non studiate!"*
*"Il nostro modo. Indipendenza totale."*

*Braccio 3 - Automazione Stanze*
