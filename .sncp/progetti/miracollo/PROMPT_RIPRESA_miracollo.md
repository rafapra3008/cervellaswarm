# PROMPT RIPRESA - Miracollo

> **Ultimo aggiornamento:** 15 Gennaio 2026 - Sessione 220
> **LEGGI E AGISCI. NON RI-ANALIZZARE.**

---

## STATO IN UNA RIGA

**Room Manager MVP LIVE. VDA: DECISIONE GO! Hardware ordinato, in attesa consegna.**

---

## COSA È LIVE

```
✅ PMS Core (prenotazioni, planning, ospiti, tariffe)
✅ Rateboard AI (meteo, eventi, learning)
✅ Room Manager MVP (grid, housekeeping, activity log)
   URL: https://miracollo.com/room-manager.html
```

---

## VDA - SESSIONE 220: GO CONFERMATO!

```
DECISIONE: GO - ELIMINARE VDA via reverse engineering MODBUS
DATA: 15 Gennaio 2026

HARDWARE ORDINATO (Amazon.it):
├── USB-RS485 FTDI (DSD TECH SH-U11L) - €19
├── Multimetro Electraline - €12
├── Cacciaviti precisione MAXWARE - €10
└── Cavetti jumper ELEGOO 120pcs - €8
TOTALE: ~€50 | Arrivo: 1-2 giorni

ARCHITETTURA VDA (già mappata sessione 219):
[Cloud VDA] → [Gateway Lex 192.168.200.15] → [RCU] → [Bus MODBUS RS-485]

RICERCHE SALVATE: .sncp/progetti/miracollo/idee/20260115_*.md
```

---

## PROSSIMO STEP (quando arriva hardware)

```
1. Setup Mac: driver FTDI + ModbusSniffer
2. Test converter funziona
3. In hotel: trova punto tap sul bus RS-485
4. Sniffing passivo (1-2 settimane)
5. Costruisci register map VDA completa
```

---

## FILE CHIAVE

| Cosa | Path |
|------|------|
| **Guida Sniffing** | `.sncp/progetti/miracollo/idee/20260115_MODBUS_SNIFFING_GUIDA_PRATICA.md` |
| **Architettura VDA** | `.sncp/progetti/miracollo/idee/20260115_VDA_ARCHITETTURA_SISTEMA_RESEARCH.md` |
| **Server Hotel** | SSH rafael@192.168.200.5 |

---

*"Non esistono cose difficili, esistono cose non studiate!"*
