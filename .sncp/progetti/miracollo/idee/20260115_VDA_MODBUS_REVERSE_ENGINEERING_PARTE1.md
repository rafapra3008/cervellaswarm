# VDA MODBUS REVERSE ENGINEERING - STUDIO COMPLETO PARTE 1

**Data**: 2026-01-15
**Ricercatrice**: Cervella Researcher
**Status**: ✅ COMPLETATA
**Obiettivo**: Reverse engineering dispositivi VDA (termostati hotel) via MODBUS senza documentazione ufficiale

---

## EXECUTIVE SUMMARY

Questo studio fornisce una guida completa per fare reverse engineering di dispositivi VDA via MODBUS senza documentazione ufficiale. VDA usa protocollo **MODBUS RTU** su RS-485 per comunicare con termostati hotel. Con gli strumenti giusti (scanner, sniffer, librerie Python) possiamo scoprire i registri e implementare controllo completo.

**TL;DR**: MODBUS è un protocollo aperto e "hackerabile". Con pazienza e metodo possiamo capire TUTTO senza docs ufficiali.

---

## PARTE 1: FONDAMENTI PROTOCOLLO MODBUS

### Cos'è MODBUS

**MODBUS** è un protocollo di comunicazione seriale creato nel 1979 da Modicon (ora Schneider Electric) per controllare dispositivi industriali (PLC, sensori, attuatori).

**Caratteristiche chiave**:
- 🏭 Standard de-facto per automazione industriale
- 📖 Protocollo aperto e pubblico (nessun brevetto)
- 🔧 Semplice: master-slave architecture
- 🌍 Usato in milioni di dispositivi worldwide

### MODBUS RTU vs MODBUS TCP

| Feature | MODBUS RTU | MODBUS TCP |
|---------|------------|------------|
| **Mezzo fisico** | RS-485 (cavo twisted pair) | Ethernet / WiFi |
| **Topologia** | Bus (multi-drop) | TCP/IP network |
| **Velocità** | 9600-115200 baud | 100 Mbps - 1 Gbps |
| **Checksum** | CRC-16 | TCP checksum |
| **Setup** | Semplice (2-3 fili) | Più complesso |
| **Distanza max** | 1200m | Illimitata (via internet) |
| **Latenza** | Bassa (ms) | Variabile |
| **Uso tipico** | Industrial, building automation | Supervisory systems, cloud |

**VDA usa MODBUS RTU** perché:
- ✅ Affidabile in ambiente industriale
- ✅ Economico (cablaggio semplice)
- ✅ Bassa latenza (hotel needs real-time)
- ✅ Multi-drop (1 master, 247 slaves max)

### Struttura Messaggio MODBUS RTU

```
┌────────────────────────────────────────────────────────────┐
│  SLAVE ID  │  FUNCTION  │  DATA  │  CRC-16  │              │
│  (1 byte)  │  (1 byte)  │  (N)   │ (2 bytes)│              │
└────────────────────────────────────────────────────────────┘
    Indirizzo    Operazione  Payload  Checksum
    dispositivo  (read/write)
```

**Esempio concreto** (leggere temperatura da termostato):

```
MASTER → SLAVE:
[01] [03] [00 64] [00 01] [C5 D5]
 │    │      │       │       └─ CRC-16 checksum
 │    │      │       └────────── Count: 1 registro
 │    │      └────────────────── Start address: 100 (0x0064)
 │    └───────────────────────── Function: 03 (Read Holding Registers)
 └────────────────────────────── Slave ID: 1

SLAVE → MASTER:
[01] [03] [02] [01 0E] [B8 44]
 │    │    │      │       └─ CRC-16 checksum
 │    │    │      └────────── Data: 0x010E = 270 → 27.0°C
 │    │    └───────────────── Byte count: 2
 │    └────────────────────── Function: 03 (echo)
 └─────────────────────────── Slave ID: 1 (echo)
```

### Function Codes MODBUS (I Più Usati)

| Code | Nome | Descrizione | Uso nei Termostati |
|------|------|-------------|-------------------|
| **0x01** | Read Coils | Legge output digitali ON/OFF | Fan ON/OFF, Heat ON/OFF |
| **0x02** | Read Discrete Inputs | Legge input digitali (read-only) | Window open, Presence sensor |
| **0x03** | Read Holding Registers | Legge registri R/W (16-bit) | Temperatura, Setpoint, Modalità |
| **0x04** | Read Input Registers | Legge registri read-only | Temperatura misurata |
| **0x05** | Write Single Coil | Scrive 1 output digitale | Accendi/spegni termosifone |
| **0x06** | Write Single Register | Scrive 1 registro | Imposta setpoint 22°C |
| **0x10** | Write Multiple Registers | Scrive N registri | Batch update |

**Per reverse engineering VDA**, ci concentreremo su:
- **0x03** (Read Holding Registers) → Leggere stato dispositivo
- **0x06** (Write Single Register) → Scrivere comandi
- **0x10** (Write Multiple Registers) → Batch commands

### Tipi di Dati MODBUS

MODBUS lavora con **registri da 16 bit** (2 byte). Per rappresentare dati più complessi:

| Tipo Dato | Dimensione | Registri | Esempio |
|-----------|-----------|----------|---------|
| **Boolean** | 1 bit | 1 coil | ON/OFF |
| **Int16** | 16 bit | 1 registro | -32768 to 32767 |
| **UInt16** | 16 bit | 1 registro | 0 to 65535 |
| **Int32** | 32 bit | 2 registri | Temperature x100 |
| **Float32** | 32 bit | 2 registri | Temperatura decimale |
| **String** | N bytes | N/2 registri | Device name |

**Trucco comune**: Temperature vengono moltiplicate per 10 o 100 per evitare float.

```
Esempio: 22.5°C
→ Salvato come: 225 (integer)
→ Display: 225 / 10 = 22.5°C
```

### Addressing: La Confusione dei Formati

MODBUS ha **2 sistemi di addressing** che creano confusione:

| Formato | Range | Descrizione |
|---------|-------|-------------|
| **Protocol Address** | 0-9998 | Address usato nel protocollo |
| **Logical Address** | 40001-49999 | Address nella documentazione (legacy) |

**Conversione**:
```
Logical Address = Protocol Address + 40001

Esempi:
  Doc dice: "Temperatura a 40101"
  → Protocol address = 40101 - 40001 = 100

  Doc dice: "Setpoint a 40005"
  → Protocol address = 40005 - 40001 = 4
```

**Per reverse engineering**: Ignoriamo logical addressing. Scanniamo 0-9998.

### RS-485: Il Layer Fisico

MODBUS RTU viaggia su **RS-485**, uno standard di comunicazione seriale differenziale.

**Caratteristiche RS-485**:
- 🔌 **2-wire** (half-duplex): A (+) e B (-)
- 📏 **Distanza**: fino a 1200m
- 🔗 **Multi-drop**: 1 master + fino a 247 slave
- ⚡ **Velocità**: 9600 - 115200 baud (tipicamente 9600 o 19200)
- 🛡️ **Robusto**: differenziale = immune a disturbi elettrici

**Wiring VDA (tipico)**:
```
┌─────────────┐
│   MASTER    │ (Computer con USB-RS485)
│  (PC/RCU)   │
└──┬──────┬───┘
   │A(+) │B(-)
   │     │
   ├─────┼─────┐
   │     │     │
┌──┴─────┴──┐ ┌┴──────────┐ ┌─────────┐
│ SLAVE 1   │ │  SLAVE 2  │ │ SLAVE N │
│(Termostato│ │(Sensore)  │ │ (...)   │
└───────────┘ └───────────┘ └─────────┘
  ID: 1         ID: 2         ID: N

Topology: Bus (daisy chain o star)
Resistenze terminazione: 120Ω su first/last device
```

**Parametri comunicazione tipici VDA**:
- Baud rate: **9600** o **19200** bps
- Data bits: **8**
- Parity: **None** o **Even**
- Stop bits: **1** o **2**

**Nota**: Questi parametri li scopriremo per tentativi (scanning).

---

## PARTE 2: VDA GROUP - CHI SONO E COSA FANNO

### Profilo Aziendale

**VDA Elettronica S.p.A.** (ora VDA Group):
- 🇮🇹 **Fondata**: 1980 a Pordenone, Italia
- 🏨 **Focus**: Automazione camere hotel (Guest Room Management Systems)
- 🌍 **Portata**: 250,000+ camere installate worldwide
- 🏆 **Clienti**: Accor, Hilton, Kempinski, Hyatt, Four Seasons, Rocco Forte
- 💰 **Acquisizioni**: 2022 → 53% di Telkonet (USA), creando colosso globale

### Prodotti Principali VDA

#### 1. **Etheos** (Cloud-Based System)

Sistema cloud per controllo remoto camere hotel.

**Funzionalità chiave**:
- 🔑 Controllo accessi (serrature BLE + PIN)
- 🌡️ Gestione climatizzazione (termostati + fan coil)
- 💡 Controllo luci e tende
- 📊 Dashboard analytics + energy monitoring
- 🔗 Integrazione PMS (Property Management System)
- 📱 Mobile control per staff

**Architettura Etheos** (da analisi screenshot):
```
┌────────────────────────────────────────────────────┐
│         ETHEOS CLOUD (room-manager.rc-onair.com)   │
│    Dashboard │ Room Manager │ Device Manager       │
└────────────┬───────────────────────────────────────┘
             │ HTTPS + WebSocket
             │
┌────────────▼───────────────┐
│  RCU (Room Control Unit)   │ ← Gateway in ogni camera
│  + KNX IP Coupler          │
└────────────┬───────────────┘
             │ MODBUS RTU (RS-485)
             │
    ┌────────┼────────┬────────┐
    │        │        │        │
┌───▼───┐ ┌─▼────┐ ┌─▼─────┐ ┌▼──────┐
│Termo  │ │Keypad│ │ BLE   │ │Sensori│
│stato  │ │      │ │Reader │ │DND/MUR│
└───────┘ └──────┘ └───────┘ └───────┘
  ID:1      ID:2     ID:3      ID:4
```

**Cosa abbiamo scoperto dall'analisi VDA Etheos** (vedi file `20260114_ANALISI_VDA_ETHEOS_PARTE*.md`):

| Feature | Dettaglio |
|---------|-----------|
| **Camere** | 32 camere (Naturae Lodge) su 4 piani + aree comuni |
| **Dispositivi** | 112 totali (~3.5 per camera) - 100% online |
| **HVAC** | 2 termostati/camera (BAGNO + CAMERA) |
| **Temperature** | Range 16-28°C configurabile, precisione 0.1°C |
| **Sensori** | Presenza, Porta open/close, Finestra open/close |
| **DND/MUR** | Pulsanti fisici in camera (Do Not Disturb / Make Up Room) |
| **Chiavi** | BLE (badge RFID) + CODE (PIN numerico) |
| **Protocollo** | MODBUS RTU (confermato!) |

#### 2. **Micromaster** (Distributed Intelligence System)

Sistema più vecchio basato su "intelligenza distribuita" con dispositivi Modbus low-voltage.

**Caratteristiche**:
- 🔧 Modular architecture
- 🏭 Installato in centinaia di hotel
- 🌡️ Integrazione VRV/VRF systems
- 🔌 Controllers + expansion devices + gateways

### Hardware VDA

VDA produce **4 collezioni** di smart switch proprietari (Made in Italy):

1. **Vitrum** - Design vetro temperato (premium)
2. **Axia** - Linee moderne
3. **Swing** - Stile classico
4. **Classic** - Entry-level

**⚠️ PROBLEMA**: Hardware proprietario = **vendor lock-in totale**. Hotel non può cambiare fornitore senza sostituire tutto.

### Perché VDA è "Squifoso" (Nostra Conclusione)

Da ricerca precedente (`20260114_RICERCA_VDA_HARDWARE.md`):

1. **Vendor Lock-In Totale**
   - Hardware proprietario (Vitrum, Axia, etc)
   - Gateway proprietario (Etheos)
   - Nessuna API pubblica documentata
   - Impossibile usare hardware terze parti

2. **Closed Architecture**
   - Zero documentazione tecnica pubblica
   - Protocollo MODBUS nascosto (no register maps)
   - Cloud infrastructure opaca
   - Self-hosting impossibile

3. **Tecnologia Legacy Mascherata**
   - MODBUS (1979) presentato come "cloud-based"
   - Meno flessibile di MQTT/KNX moderni
   - Difficile integrare con ecosistemi IoT moderni

4. **Costo Alto e Opaco**
   - Hardware proprietario = premium pricing
   - Nessuna competizione (locked-in)
   - Customizzazioni = consulting fees VDA

5. **Mancanza Innovazione**
   - Dashboard analytics generiche (no AI/ML)
   - No integrazione ecosistemi moderni (Alexa, Google Home)
   - No API pubblica = no developer community

**Conclusione**: VDA domina mercato con tech legacy + lock-in. **Opportunità per Miracollo**: fare meglio con protocolli aperti (MQTT, KNX) + API pubblica.

---

## PARTE 3: REVERSE ENGINEERING MODBUS - TEORIA E METODO

### Perché Reverse Engineering è Possibile

MODBUS è un protocollo **aperto e standardizzato**. Questo significa:

1. ✅ **Protocollo pubblico**: Sappiamo come funzionano i messaggi
2. ✅ **Nessuna crittografia**: Messaggi in chiaro sul bus
3. ✅ **Standard prevedibile**: I dispositivi seguono convenzioni comuni
4. ✅ **Tools disponibili**: Scanner, sniffer, debugger MODBUS esistono

**Cosa NON sappiamo** (e dobbiamo scoprire):
- ❓ Quali registri esistono (0-9998)
- ❓ Cosa rappresenta ogni registro (temperatura? setpoint? modalità?)
- ❓ Formato dati (int16? float32? scaled?)
- ❓ Read/write permissions
- ❓ Side effects (scrivere registro X cosa fa?)

### Il Metodo Scientifico per Reverse Engineering

```
┌──────────────────────────────────────────────────────┐
│  FASE 1: DISCOVERY                                   │
│  → Trova dispositivi sul bus                         │
│  → Identifica slave IDs attivi                       │
└────────────┬─────────────────────────────────────────┘
             │
┌────────────▼─────────────────────────────────────────┐
│  FASE 2: REGISTER SCANNING                           │
│  → Scansiona registri 0-9998                         │
│  → Identifica registri readable                      │
│  → Identifica registri writable                      │
└────────────┬─────────────────────────────────────────┘
             │
┌────────────▼─────────────────────────────────────────┐
│  FASE 3: DATA CORRELATION                            │
│  → Cambia temperatura fisica → quale registro cambia?│
│  → Premi pulsante → quale registro cambia?          │
│  → Match registro ↔ funzione reale                   │
└────────────┬─────────────────────────────────────────┘
             │
┌────────────▼─────────────────────────────────────────┐
│  FASE 4: COMMAND TESTING                             │
│  → Scrivi valore in registro → cosa succede?        │
│  → Test safe first (read-only registers)            │
│  → Test write con cautela                            │
└────────────┬─────────────────────────────────────────┘
             │
┌────────────▼─────────────────────────────────────────┐
│  FASE 5: DOCUMENTATION                               │
│  → Crea register map completa                        │
│  → Documenta formato dati, range, unità             │
│  → Scrivi API wrapper Python                         │
└──────────────────────────────────────────────────────┘
```

### Case Study: Come Qualcuno Ha Fatto Reverse Engineering PLC

Da [forum NI Community](https://forums.ni.com/t5/LabVIEW/finding-registers-in-modbus/td-p/884423):

> "I successfully reverse engineered a PLC with zero documentation.
>
> My approach:
> 1. Used **Modbus Poll** to view many channels at once
> 2. Started **writing values** and seeing what changed on the device
> 3. Started **wiring inputs** and watching what registers changed
> 4. Tedious but worked! Documented everything in a spreadsheet."

**Key Insights**:
- 🔍 **Monitor molti registri simultaneamente** (polling)
- ✍️ **Write & observe** (causa → effetto)
- 🔌 **Physical manipulation & observe** (input fisico → registro digitale)
- 📝 **Documentare tutto in spreadsheet** (sistematico!)

### Tools per Reverse Engineering MODBUS

#### 1. **Modbus Poll** (Windows, €99 commercial)

Tool GUI per polling devices.

**Features**:
- ✅ Monitor multiple registers in real-time
- ✅ Read/write operations
- ✅ Graphical display (chart per vedere trend)
- ✅ Log traffic to file
- ✅ Supporto RTU + TCP

**Uso per reverse engineering**:
1. Connect al bus RS-485
2. Scan slave IDs (1-247)
3. Monitor registri 0-1000 in finestre multiple
4. Cambia temperatura fisica → vedi quale registro si aggiorna
5. Write test values → osserva effetto

**Limitation**: Commercial (€99), solo Windows.

#### 2. **QModMaster** (Free, Open Source, Cross-Platform)

Alternative GRATUITA a Modbus Poll.

**Features**:
- ✅ Qt-based GUI (Linux, Mac, Windows)
- ✅ RTU + TCP support
- ✅ Bus monitor (sniffing traffic)
- ✅ Read/write coils and registers
- ✅ Open source (GitHub)

**Download**: [SourceForge QModMaster](https://sourceforge.net/projects/qmodmaster/)

**Uso**:
1. Setup connection (serial port, baud rate, parity)
2. Define polls (slave ID, function, address, quantity)
3. Monitor results in table view
4. Bus monitor shows raw frames

**Vantaggio**: Free + cross-platform = ideale per noi!

#### 3. **ModbusMechanic** (Windows, Free)

Simple Windows GUI tool.

**Features**:
- ✅ RTU + TCP
- ✅ Read/write functions
- ✅ Auto-polling
- ✅ Export data to CSV

#### 4. **mbpoll** (Command-Line, Free)

Command-line tool per Linux/Mac.

**Usage example**:
```bash
# Read 10 holding registers starting from address 0, slave 1
mbpoll -a 1 -r 0 -c 10 -t 4 /dev/ttyUSB0

# Write value 225 to register 4 (setpoint 22.5°C)
mbpoll -a 1 -r 4 -t 4 /dev/ttyUSB0 225
```

**Vantaggio**: Scriptable! Possiamo automatizzare scanning.

#### 5. **Wireshark + MODBUS Plugin** (Per TCP, non RTU direttamente)

Se MODBUS TCP, Wireshark può decodificare pacchetti.

**Limitation**: Per MODBUS RTU su RS-485, serve logic analyzer hardware.

#### 6. **Python pymodbus** (Library per scripting)

La nostra **arma segreta** per automazione!

**Features**:
- ✅ Supporto RTU + TCP
- ✅ Tutte le function codes
- ✅ Scriptable (automated scanning)
- ✅ Cross-platform
- ✅ Open source

**Vedremo dettagli implementazione in PARTE 2 di questo studio.**

---

## PARTE 4: REGISTER SCANNING - TECNICHE PRATICHE

### Automated Scanning con Python

#### Tool: modbus-scanner (GitHub)

[GitHub: nemmusu/modbus-scanner](https://github.com/nemmusu/modbus-scanner)

**Cosa fa**:
- Scansiona registri 0-9998 in blocchi (default 50 registri/request)
- Delay tra blocchi (default 4 secondi) per non sovraccaricare device
- Output: registri che rispondono + valori

**Concetto**:
```python
for address in range(0, 10000, 50):
    try:
        result = client.read_holding_registers(address, 50, unit=1)
        if not result.isError():
            # Registro esiste! Salva address + value
            print(f"Found: {address} = {result.registers}")
    except Exception as e:
        # Registro non esiste, skip
        pass
    time.sleep(4)  # Delay per non stressare device
```

#### PyModbus scan_slaves() Function

PyModbus include funzione per **trovare slave IDs attivi**:

```python
from pymodbus.client import ModbusSerialClient

client = ModbusSerialClient(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity='N',
    stopbits=1,
    bytesize=8
)
client.connect()

# Scan slave IDs from 1 to 247
for slave_id in range(1, 248):
    try:
        result = client.read_holding_registers(0, 1, unit=slave_id)
        if not result.isError():
            print(f"✅ Found slave: {slave_id}")
    except:
        pass

client.close()
```

**Output example**:
```
✅ Found slave: 1   (termostato camera)
✅ Found slave: 2   (termostato bagno)
✅ Found slave: 3   (sensore presenza)
✅ Found slave: 4   (keypad)
```

### Strategy: Block Scanning con Adaptive Step

**Problema**: Scansionare 0-9998 con read_holding_registers(addr, 1) = **10,000 richieste** = LENTO!

**Soluzione**: Usare step adattivo.

**Algorithm**:
```python
def scan_registers_adaptive(client, slave_id, start=0, end=10000):
    """
    Scansiona registri con step adattivo.
    1. Prova blocchi grandi (100 registri)
    2. Se fallisce, dividi a metà (binary search)
    3. Continua fino a trovare registri validi
    """

    found_registers = []
    step = 100

    for address in range(start, end, step):
        try:
            # Prova leggere blocco
            result = client.read_holding_registers(
                address,
                min(step, end - address),
                unit=slave_id
            )

            if not result.isError():
                # Blocco valido! Salva tutti i registri
                for i, value in enumerate(result.registers):
                    found_registers.append({
                        'address': address + i,
                        'value': value
                    })
        except Exception as e:
            # Blocco fallito, prova step più piccolo
            if step > 1:
                # Retry con step dimezzato
                sub_result = scan_registers_adaptive(
                    client, slave_id, address, address + step, step // 2
                )
                found_registers.extend(sub_result)

        time.sleep(0.5)  # Delay between blocks

    return found_registers
```

**Vantaggio**: Molto più veloce! Se device ha 50 registri sparsi, troviamo in ~200 richieste invece di 10,000.

### Interpreting Scan Results

**Output tipico** di scan:

```
Address | Value (dec) | Value (hex) | Probable Meaning
--------|-------------|-------------|------------------
0       | 101         | 0x0065      | Room number?
1       | 1           | 0x0001      | Status flag?
2       | 225         | 0x00E1      | Temperature? (22.5°C)
3       | 220         | 0x00DC      | Setpoint? (22.0°C)
4       | 2           | 0x0002      | Mode? (Heat/Cool?)
5       | 1           | 0x0001      | Fan speed? (Low/Med/High?)
10      | 0           | 0x0000      | Unknown
11      | 0           | 0x0000      | Unknown
100     | 32768       | 0x8000      | Float upper word?
101     | 16384       | 0x4000      | Float lower word?
```

**Tecniche interpretazione**:

1. **Look for patterns**
   - Valori piccoli (0-3) = probabilmente enum (modalità, fan speed)
   - Valori 200-300 = probabilmente temperatura scaled x10
   - Valori >1000 = probabilmente parte di int32/float32

2. **Test correlation**
   - Cambia temperatura fisica → quale registro cambia?
   - Imposta setpoint 25°C → quale registro diventa 250?

3. **Known ranges**
   - Temperature hotel: 16-28°C → cercare 160-280
   - Fan speed: 0-2 o 0-3 (Auto/Low/Med/High)
   - Boolean: 0 = OFF, 1 = ON

---

*Continua in PARTE 2...*

---

## FONTI PARTE 1

### MODBUS Protocol & Tools
- [Modbus RTU Protocol Tutorial 2025 | Complete Implementation Guide](https://plcprogramming.io/blog/modbus-rtu-protocol-tutorial-complete-guide)
- [QModMaster Open Source Tool](https://sourceforge.net/projects/qmodmaster/)
- [Modbus Tools & Test](https://www.modbustools.com/)
- [Modbus RTU Made Simple - IPC2U](https://ipc2u.com/articles/knowledge-base/modbus-rtu-made-simple-with-detailed-descriptions-and-examples/)

### Python MODBUS Libraries
- [GitHub: nemmusu/modbus-scanner](https://github.com/nemmusu/modbus-scanner)
- [PyModbus Documentation](https://www.pymodbus.org/docs)
- [MinimalModbus Documentation](https://minimalmodbus.readthedocs.io/en/stable/)
- [MODBUS and RS485 Python Test Rig - Medium](https://medium.com/@peterfitch/modbus-and-rs485-a-python-test-rig-1b5014f709ec)

### Reverse Engineering Resources
- [Finding Registers in Modbus - NI Community](https://forums.ni.com/t5/LabVIEW/finding-registers-in-modbus/td-p/884423)
- [Protocol Reverse Engineering Example - GitHub](https://gist.github.com/longdog/0ca8acdd2e88454be740fc051e951409)

### VDA Group Research
- [Ricerca VDA Hardware Completa](file://20260114_RICERCA_VDA_HARDWARE.md)
- [Analisi VDA Etheos Parte 2](file://20260114_ANALISI_VDA_ETHEOS_PARTE2.md)

---

*Cervella Researcher - 2026-01-15*
*"Nulla è complesso - solo non ancora studiato!"*
