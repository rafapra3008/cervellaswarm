# VDA ROSETTA STONE - Piano Reverse Engineering

> **Data:** 16 Gennaio 2026
> **Decisione:** Facciamo il NOSTRO modo. Nessun contatto con VDA.
> **Filosofia:** "Non esistono cose difficili, esistono cose non studiate!"

---

## DISPOSITIVI DA MAPPARE

### Dalla Foto NUCLEUS (H155300)

```
VDA ETHEOS - NUCLEUS I/O RCU
Modello: H155300 v1.4
Firmware: 5.4.1
MAC Ethernet: 00:08:0C:20:1F:6D
```

| Sezione | Pin | Funzione |
|---------|-----|----------|
| MODBUS PORTS | M1, M2, M3, M4 | 4 porte RS-485 (qui ci colleghiamo!) |
| RS232 TTL | 5 | Seriale backup |
| POWER SUPPLY | 1-2 | 12Vdc input |
| POWER OUTPUT | 3-4 | 12Vdc 600mA |
| Digital Outputs | DO1-DO8 (6-25) | Relè 250Vac 10A |
| Digital Inputs | DI1-DI5 (26-32) | Contatti isolati |
| Analog Inputs | AI1, AI2 (36-41) | Sonde temperatura |
| Analog Outputs | AO1-AO3 (42-47) | 0-10V 10mA/ch |
| ETH PORT | RJ45 | Ethernet (Modbus TCP?) |

### Dal Room Manager VDA (Screenshot)

| Device | Catalogue ID | Protocol | Address | FW |
|--------|--------------|----------|---------|-----|
| RCU | H155300 | - | - | 5.4.1 |
| 6T KEYPAD | NE000056-KEYPAD | Modbus | ba:88 ch:1 add:0 | 0.132 |
| LT BLE 2.1 | VE503E00 | Modbus | ba:40 ch:1 add:0 | 1.0 |
| CON4 2.1 | VE503T00 | Modbus | ba:48 ch:2 add:0 | 1.6 |

### Decodifica Address

```
ba = baud rate (40=4800? 48=4800? 88=9600?)
ch = channel Modbus (1 o 2)
add = slave address (0 = broadcast? o 1-based?)
```

### Mappatura Nota (da Rafa)

```
AI1 = SONDA BAGNO
AI2 = SONDA INGRESSO
```

---

## HARDWARE ORDINATO (Amazon)

| Item | Modello | Prezzo | Uso |
|------|---------|--------|-----|
| USB-RS485 | DSD TECH SH-U11L (FTDI) | €19 | Converter per Mac |
| Multimetro | Electraline | €12 | Verifica tensioni |
| Cacciaviti | MAXWARE precisione | €10 | Aprire pannelli |
| Jumper | ELEGOO 120pcs | €8 | Collegamenti test |

**Totale:** ~€50
**Arrivo:** Amazon Prime 1-2 giorni

---

## PIANO REVERSE ENGINEERING

### STEP 1: Setup Mac

```bash
# Driver FTDI (probabilmente automatico su macOS)
# Verifica device
ls /dev/tty.usbserial*

# Software sniffing
# - CoolTerm (gratuito)
# - ModbusSniffer
# - Wireshark con plugin Modbus
```

### STEP 2: Prima Connessione (Zero Rischio)

```
OPZIONE A - Ethernet (più facile):
1. Collega cavo RJ45 da Mac a NUCLEUS
2. Cerca IP con nmap: nmap -sP 192.168.x.0/24
3. Test Modbus TCP porta 502
4. Se risponde → sniffing via TCP!

OPZIONE B - RS-485 (se Ethernet non va):
1. Collega USB-RS485 a porta M1 del NUCLEUS
2. Imposta parametri (9600 8N1 come default)
3. Sniffing passivo (solo ascolto)
```

### STEP 3: Sniffing Passivo

```
NON mandiamo comandi - solo ASCOLTIAMO!

Il NUCLEUS parla costantemente con:
- Termostati (VE503E00, VE503T00)
- Keypad (NE000056)
- Sensori

Registriamo TUTTO:
- Timestamp
- Device address
- Function code
- Register
- Value
```

### STEP 4: Decodifica Pattern

```
ESEMPIO tipico Modbus RTU:

[01] [03] [00 64] [00 01] [CRC]
 │    │     │       │
 │    │     │       └── Quanti registri leggere
 │    │     └────────── Registro iniziale (100 dec)
 │    └──────────────── Function code (03 = Read Holding)
 └───────────────────── Slave address

RISPOSTA:
[01] [03] [02] [00 E6] [CRC]
             └── Valore: 230 = 23.0°C?
```

### STEP 5: Costruzione Rosetta Stone

```
Per ogni registro scoperto documentiamo:

| Register | Tipo | Device | Significato | Unità | Range |
|----------|------|--------|-------------|-------|-------|
| 40001 | Holding | VE503E00 | Temp camera | °C/10 | 150-300 |
| 40002 | Holding | VE503E00 | Setpoint | °C/10 | 160-280 |
| 00001 | Coil | NUCLEUS | Relè DO1 | bool | 0-1 |
| ... | ... | ... | ... | ... | ... |
```

---

## RICERCA COMPLETATA (16 Gen 2026)

### Cosa Abbiamo Cercato

- VDA ETHEOS Modbus register map → NON TROVATO
- H155300 documentation → Solo cataloghi
- VE503 thermostat registers → NON TROVATO
- Reverse engineering esistente → NESSUNO
- Home Assistant integration → NON ESISTE
- OEM manufacturer → VDA produce internamente (Pordenone)

### Conclusione Ricerca

```
NESSUNO HA MAI DOCUMENTATO PUBBLICAMENTE I REGISTRI VDA!

Motivi:
1. VDA tiene tutto proprietario
2. Target B2B (hotel), non maker
3. Nicchia troppo specifica
4. Nessun incentivo a documentare

CONSEGUENZA:
Saremo i PRIMI a creare la Rosetta Stone!
```

---

## ECOSISTEMA CAMERA (da conversazione Rafa)

### Controllato dal NUCLEUS (probabile)

- Sonda temperatura bagno (AI1)
- Sonda temperatura ingresso (AI2)
- Termosifone bagno (AO?)
- Termosifone camera (AO?)
- Sensore presenza (DI?)
- Sensore finestre (DI?)
- Sensore porte (DI?)
- Corrente camera (DO? relè)

### Sistema Separato (Pannello Codici Porta)

- LED Verde = occupato
- LED Giallo = pulita
- LED Viola = MUR
- Inserimento codice → apertura

### Sistema Separato (Legrand/BTicino)

- Luci Spa e Bar
- App Home + Control
- Protocollo Zigbee/WiFi

---

## OPPORTUNITÀ

```
CON LA ROSETTA STONE:
├── Controllare TUTTO da Miracollo
├── Bypass software VDA
├── Automazioni custom
├── Dashboard unificata
├── Energy monitoring avanzato
└── INDIPENDENZA TOTALE!
```

---

## FOTO RIFERIMENTO

```
NUCLEUS etichetta: ~/Downloads/WhatsApp Image 2026-01-16 at 02.48.33 (2).jpeg
Power supply: ~/Downloads/WhatsApp Image 2026-01-16 at 02.48.33 (1).jpeg
Vista insieme: ~/Downloads/WhatsApp Image 2026-01-16 at 02.48.32.jpeg
Room Manager: ~/Desktop/Screenshot 2026-01-16 alle 03.13.49.png
```

---

## PROSSIMI STEP

```
1. [ ] Aspettare hardware Amazon (1-2 giorni)
2. [ ] Setup Mac (driver, software)
3. [ ] Prima connessione (Ethernet o RS-485)
4. [ ] Sniffing passivo
5. [ ] Iniziare mappatura registri
6. [ ] Documentare Rosetta Stone
```

---

*"Non esistono cose difficili, esistono cose non studiate!"*
*"Il nostro modo. Indipendenza totale."*

*Creato: 16 Gennaio 2026 - Sessione 230*
