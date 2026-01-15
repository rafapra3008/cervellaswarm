# STATO OGGI - 15 Gennaio 2026

> **Sessione:** 219 Miracollo
> **Ultimo aggiornamento:** 10:00

---

## SESSIONE 219 - STUDIO VDA COMPLETO

```
+================================================================+
|   OBIETTIVO: ELIMINARE VDA                                     |
|   Reverse engineering se serve, senza parlare con VDA          |
+================================================================+

COMPLETATO:
- Accesso SSH al server hotel (192.168.200.5)
- Network discovery completo
- Trovato gateway VDA Lex Computech (192.168.200.15)
- Mappata architettura VDA (Cloud + Gateway + MODBUS)
- 6 ricerche approfondite salvate in SNCP

SCOPERTE CHIAVE:
- VDA Nucleus Gateway = black box (no docs pubbliche)
- Bus MODBUS RS-485 = open standard (accessibile)
- Piano: bypassare gateway, parlare diretto coi dispositivi

HARDWARE IDENTIFICATO:
- H155300 (RCU Nucleus)
- VE503E00 (termostato BLE)
- VE503T00 (controller fancoil)
- NE000056 (keypad)
```

---

## PROSSIMA SESSIONE

```
SE si decide di procedere:
1. Comprare USB-RS485 FTDI (~€20)
2. Collegare al bus MODBUS nel quadro
3. Sniffing passivo (2-4 settimane)
4. Creare register map
5. Integrare con Miracollo
```

---

*"Non esistono cose difficili, esistono cose non studiate!"*
