# PROMPT RIPRESA - Miracollo

> **Ultimo aggiornamento:** 15 Gennaio 2026 - Sessione 219
> **LEGGI E AGISCI. NON RI-ANALIZZARE.**

---

## STATO IN UNA RIGA

**Room Manager MVP LIVE. VDA: studiato, pronto per reverse engineering se Rafa decide.**

---

## COSA È LIVE

```
✅ PMS Core (prenotazioni, planning, ospiti, tariffe)
✅ Rateboard AI (meteo, eventi, learning)
✅ Room Manager MVP (grid, housekeeping, activity log)
   URL: https://miracollo.com/room-manager.html
```

---

## VDA - SESSIONE 219 (STUDIO COMPLETO)

```
OBIETTIVO: ELIMINARE VDA (non integrare)
APPROCCIO: Reverse engineering MODBUS, senza parlare con VDA

ARCHITETTURA SCOPERTA:
┌─────────────────────────────────────────┐
│ [Cloud VDA] emc.rc-onair.com            │
│      ↓                                  │
│ [Gateway Lex] 192.168.200.15            │
│      ↓ (VLAN VDA CAMERE 10.0.0.x)       │
│ [RCU H155300] → Bus MODBUS RS-485       │
│      ↓                                  │
│ [Termostati, Keypad, Controller]        │
└─────────────────────────────────────────┘

PIANO: Bypassare gateway, collegare diretto al bus MODBUS

HARDWARE DA COMPRARE (se si procede):
- USB-RS485 FTDI (~€20) - Amazon.it

RICERCHE SALVATE:
.sncp/progetti/miracollo/idee/
├── 20260115_VDA_MODBUS_REVERSE_ENGINEERING_PARTE1-3.md
├── 20260115_VDA_VE503_TERMOSTATI_RESEARCH.md
├── 20260115_VDA_H155300_RCU_RESEARCH.md
├── 20260115_VDA_ARCHITETTURA_SISTEMA_RESEARCH.md
├── 20260115_MODBUS_SNIFFING_GUIDA_PRATICA.md
└── 20260115_LEX_COMPUTECH_GATEWAY_RESEARCH.md
```

---

## PROSSIMO STEP

**DECISIONE RAFA:**
- GO → Compra USB-RS485, inizia sniffing (6-8 settimane totali)
- NO-GO → Focus su altro, VDA resta com'è

---

## FILE CHIAVE

| Cosa | Path |
|------|------|
| **NORD** | `miracollogeminifocus/NORD.md` |
| **ROADMAP** | `.sncp/progetti/miracollo/moduli/room_manager/ROADMAP_ROOM_MANAGER_COMPLETA.md` |
| **Server Hotel** | SSH rafael@192.168.200.5 |

---

*"Non esistono cose difficili, esistono cose non studiate!"*
