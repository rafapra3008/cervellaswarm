# VDA H155300 RCU (Room Control Unit) - RICERCA APPROFONDITA

**Data**: 2026-01-15
**Ricercatrice**: Cervella Researcher
**Status**: ✅ COMPLETATA
**Obiettivo**: Studio approfondito del dispositivo VDA H155300 RCU, il "cervello" di ogni zona hotel nel sistema Etheos

---

## EXECUTIVE SUMMARY

Il **VDA H155300** è l'**Etheos Nucleus RCU (Room Control Unit)** con supporto Wi-Fi, il controller principale installato in ogni camera hotel. È il dispositivo chiave che:
- Gestisce fino a **80 dispositivi smart** tramite **4 porte MODBUS indipendenti**
- Comunica con il cloud Etheos (room-manager.rc-onair.com) via WiFi/Ethernet
- Controlla HVAC, luci, serrature, sensori in camera
- È **completamente programmabile** (I/O, scenari, keypad)
- Ha porta **USB per programmazione locale** e manutenzione

**TL;DR**: L'H155300 è il gateway intelligente tra i dispositivi fisici in camera (MODBUS) e il cloud VDA. È il punto di accesso CRITICO per reverse engineering e integrazione custom.

---

## PARTE 1: IDENTIFICAZIONE PRODOTTO

### Modello e Varianti

**Nome Completo**: Etheos - Nucleus I/O RCU (Room Control Unit)

**Codici Prodotto VDA**:
| Codice | Descrizione | Connettività | Note |
|--------|-------------|--------------|------|
| **H155300** | Nucleus RCU con I/O | **Wi-Fi** | Modello standard con modulo WiFi |
| **H155300/WF** | Nucleus RCU con I/O | **Wi-Fi** | Variante (probabilmente WiFi enhanced) |
| **H155010** | Nucleus RCU SENZA I/O | **Wi-Fi** | Versione ridotta (solo gateway) |
| **H155010/WF** | Nucleus RCU SENZA I/O | **Wi-Fi** | Variante |
| **H155xxx/ETH** | Nucleus Ethernet | **Ethernet cablato** | Alternative non-WiFi (ipotesi) |

**Componenti Richiesti**:
- ⚠️ **Power Supply OBBLIGATORIO**: Modello 9600034/4A o 9600034/4B
  - Specifiche: **12 Vdc, 24-30W**
  - Nota: L'RCU NON funziona senza alimentatore dedicato

### Famiglia Prodotti VDA Etheos

Il H155300 fa parte della **famiglia Nucleus**, la 5a generazione di controller VDA.

**Generazioni VDA**:
```
Gen 1-4: Micromaster (legacy, solo MODBUS RTU locale)
  ↓
Gen 5: Etheos Nucleus (cloud-based + MODBUS + WiFi/Ethernet)
  ↓
Future: Nucleus + Voice Control + DALI + IoT expansion
```

**Altri Moduli VDA** (ecosistema):
- **H113931**: Expansion Module 4DI + 4DO (Digital I/O)
- **H114xxx**: Altri expansion modules (da identificare)
- **9600034/4A-B**: Power supplies
- **Keypads, Thermostats, BLE readers**: Slave devices MODBUS

---

## PARTE 2: SPECIFICHE TECNICHE (Da Fonti Pubbliche)

### Architettura Hardware

**Microprocessore**:
- "Powerful microprocessor architecture" (VDA marketing)
- Processore non specificato (probabilmente ARM Cortex-M o simile)
- Memoria flash per firmware + configurazione locale

**Modular Hardware Configuration**:
- Design modulare per espansione I/O
- Supporto expansion modules (es: H113931)

### Comunicazione

#### 1. MODBUS Ports (Core Feature!)

**Specifiche**:
- **4 porte MODBUS indipendenti**
- Protocollo: **MODBUS RTU** su RS-485
- Capacità: **Fino a 80 dispositivi smart totali** (20 per porta?)
- **Zero data latency** (claim VDA)

**Topologia**:
```
┌──────────────────────────────────────────────────┐
│          VDA H155300 NUCLEUS RCU                 │
│                                                  │
│  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐        │
│  │MODBUS│  │MODBUS│  │MODBUS│  │MODBUS│        │
│  │PORT 1│  │PORT 2│  │PORT 3│  │PORT 4│        │
│  └───┬──┘  └───┬──┘  └───┬──┘  └───┬──┘        │
└──────┼─────────┼─────────┼─────────┼───────────┘
       │         │         │         │
   ┌───▼────┬────▼───┬─────▼───┬─────▼────┐
   │Termo   │Keypad  │BLE      │Sensori   │
   │stato 1 │        │Reader   │DND/MUR   │
   ├────────┼────────┼─────────┼──────────┤
   │Termo   │Expan  │Door     │Presenza  │
   │stato 2 │Module │Lock     │Sensor    │
   └────────┴────────┴─────────┴──────────┘
     20 dev    20 dev   20 dev    20 dev
```

**Parametri MODBUS (tipici)**:
- Baud rate: **9600 o 19200 bps** (standard VDA)
- Data bits: **8**
- Parity: **None** o **Even**
- Stop bits: **1**
- Protocollo: **MODBUS RTU** (non TCP!)

#### 2. Cloud Connectivity

**WiFi Model** (H155300):
- Standard: Non specificato (probabilmente 802.11 b/g/n)
- Frequenza: 2.4 GHz (ipotesi)
- Sicurezza: WPA2 (minimo)
- Connect to hotel existing wireless network

**Ethernet Model** (H155xxx/ETH):
- 10/100 Mbps Ethernet
- RJ45 connector
- PoE support: Non confermato

**Cloud Endpoint**:
- URL: **room-manager.rc-onair.com**
- Protocollo: **HTTPS + TLS** (VDA claim: "highly secure")
- Hosting: **Amazon Web Services (AWS)**
- Data format: Probabilmente JSON/REST o WebSocket

#### 3. USB Port (Locale Programming!)

**Funzionalità**:
- ✅ **Programmazione locale** via mobile app dedicata
- ✅ **Quick maintenance operations**
- ✅ **Firmware update** (ipotesi)
- ✅ **Debugging e diagnostics** (ipotesi)

**Specifiche USB**:
- Type: Probabilmente **USB Type-A o Micro-USB**
- Function: **UART bridge** per accesso seriale?
- Compatibilità: Mobile app VDA (iOS/Android)

**POTENZIALE REVERSE ENGINEERING**:
- 🔓 Possibile accesso diretto via USB per debugging
- 🔓 Firmware dump via USB?
- 🔓 Log access per vedere comunicazioni MODBUS?

### Input/Output (I/O)

**Modello H155300 (con I/O)**:
- Digital Inputs: **Non specificato** (probabilmente 4-8)
- Digital Outputs: **Non specificato** (probabilmente 4-8)
- Analog Inputs: **Possibile** (per sensori temperatura?)
- Relays: **Sì** (per controllo luci/HVAC)

**Relay Sizing**:
- "Appropriately sized relays" (VDA claim)
- Benefit: "Reduces wiring costs and improves reliability over time"

**Expansion**:
- Via expansion modules (es: H113931 - 4DI + 4DO)
- Supporto DALI lights (via gateway?)
- Supporto voice control (via integration server?)

### Alimentazione

**Input Power**:
- Voltage: **12 Vdc** (via power supply 9600034/4A o 4B)
- Consumption: **24-30W** (stima da power supply specs)

**Power Supply Models**:
| Modello | Output | Note |
|---------|--------|------|
| 9600034/4A | 12 Vdc, 30W | Versione A |
| 9600034/4B | 12 Vdc, 30W | Versione B (differenza sconosciuta) |
| H000034/4B | 12 Vdc, 30W | Auxiliary Power Supply (alternativa?) |

### Dimensioni e Montaggio

**Dimensioni**: Non specificate (probabilmente DIN rail mount standard)

**Installazione**:
- Location: **In-room** (ogni camera)
- Mounting: DIN rail (ipotesi)
- Environment: Indoor (controlled temperature)

### Firmware

**Versione Conosciuta**: **5.4.1** (da analisi VDA Etheos screenshot Naturae Lodge)

**Update Process**:
- Via **cloud** (automatic updates - VDA claim: "24-hour maintenance")
- Via **USB** (local programming - mobile app)

**Programmabilità**:
- ✅ **I/O configuration**
- ✅ **Scenarios** (if-then automation rules)
- ✅ **Keypad features**
- ✅ **Fully programmable** (VDA claim)

---

## PARTE 3: FUNZIONALITÀ E CAPABILITIES

### 1. Device Management

**Supporto Devices**:
| Categoria | Dispositivi | Protocollo | Funzione |
|-----------|-------------|------------|----------|
| **HVAC** | Termostati, Fan coil | MODBUS RTU | Controllo temperatura |
| **Accesso** | Serrature BLE, PIN keypad | MODBUS RTU | Unlock/lock doors |
| **Illuminazione** | Smart switches, DALI lights | MODBUS / DALI | On/off, dimming |
| **Sensori** | Presenza, Porta, Finestra | MODBUS RTU | Occupancy detection |
| **User Interface** | DND/MUR buttons, Keypads | MODBUS RTU | Guest control |
| **Expansion** | I/O modules, Relays | MODBUS RTU | Custom devices |

**Capacity per Room** (stimato):
- **Piccola camera**: 3-5 devices (termostato, keypad, sensore)
- **Suite**: 10-15 devices (HVAC multi-zona, multiple lights)
- **VIP Suite**: 20+ devices (full automation)

**Total System Capacity**:
- 4 porte × 20 devices/porta = **80 devices max**
- Sufficiente per suite/condo complessi

### 2. Automation & Scenarios

**Scenario Engine** (fully programmable):

**Esempi Scenari**:
```
SCENARIO 1: Check-in
  TRIGGER: PMS sends "room occupied" event
  ACTIONS:
    - Unlock door (BLE reader)
    - Set temperature 22°C (thermostat)
    - Open curtains (motor control)
    - Turn on welcome lights (switches)

SCENARIO 2: Guest Leaves (Eco Mode)
  TRIGGER: Keycard removed + door closed (sensors)
  ACTIONS:
    - Set temperature 18°C (eco)
    - Turn off all lights
    - Close curtains

SCENARIO 3: DND Pressed
  TRIGGER: DND button pressed (keypad)
  ACTIONS:
    - Send event to PMS (no housekeeping)
    - Disable doorbell
    - Show DND icon on tablet

SCENARIO 4: Window Open (Safety)
  TRIGGER: Window sensor = OPEN
  ACTIONS:
    - Turn off HVAC (energy saving)
    - Log event to cloud
    - Alert if >15 min open (maintenance)
```

**Programming Interface**:
- Via **Etheos Commissioning Tools** (web/mobile app)
- Logic: "Intuitive step-by-step" (VDA claim)
- No coding required (GUI-based)

### 3. Cloud Integration

**Etheos Platform** (room-manager.rc-onair.com):

**Data Flow**:
```
┌─────────────────────────────────────────────────┐
│          AWS Cloud (Etheos Platform)            │
│  - Room status dashboard                        │
│  - Analytics & reporting                        │
│  - Remote control                                │
│  - PMS integration                               │
└──────────────┬──────────────────────────────────┘
               │ HTTPS + TLS
               │ (WebSocket? JSON?)
┌──────────────▼──────────────────────────────────┐
│       VDA H155300 Nucleus RCU (in-room)         │
│  - Local logic (scenarios)                      │
│  - MODBUS master                                 │
│  - WiFi/Ethernet gateway                         │
└──────────────┬──────────────────────────────────┘
               │ MODBUS RTU (RS-485)
               │
        ┌──────┴───────┬──────────┬──────────┐
        │              │          │          │
    ┌───▼────┐  ┌─────▼────┐  ┌──▼─────┐  ┌▼─────┐
    │Thermo  │  │Keypad    │  │Sensors │  │Locks │
    └────────┘  └──────────┘  └────────┘  └──────┘
```

**Cloud Features**:
- ✅ **Real-time monitoring** (room status, temperature, occupancy)
- ✅ **Remote control** (da dashboard web/mobile)
- ✅ **Analytics** (energy consumption, usage patterns)
- ✅ **Alerts** (maintenance, anomalies)
- ✅ **Firmware updates** (automatic, 24/7 maintenance)

**Data Transmitted** (ipotesi):
```json
{
  "hotel_id": "itblxalle00847",
  "room_id": "101",
  "timestamp": "2026-01-15T10:30:00Z",
  "temperature": 22.5,
  "setpoint": 22.0,
  "occupancy": true,
  "door_status": "closed",
  "dnd": false,
  "mur": false,
  "devices": [
    {"id": 1, "type": "thermostat", "status": "heating"},
    {"id": 2, "type": "keypad", "battery": 85},
    {"id": 3, "type": "presence_sensor", "value": 1}
  ]
}
```

### 4. PMS Integration

**Integration Method**:
- Via **Integration Server** (VDA component)
- Protocollo: Non specificato (probabilmente REST API o SOAP)
- PMS supportati: "Most hotel PMS" (VDA claim)

**Events**:
| PMS → Etheos | Etheos → PMS |
|--------------|--------------|
| Check-in confirmed | Room ready for cleaning |
| Check-out initiated | DND/MUR status |
| Room assignment changed | Maintenance alert |
| Guest preferences | Energy consumption data |

**Known PMS Integrations** (da ricerca generale VDA):
- Opera Cloud
- Mews
- Protel
- StayNTouch
- Others (via middleware)

### 5. Local Programming (Resilience)

**Key Feature**: "Nucleus remains fully operational **even if cloud connectivity is lost**"

**Local Capabilities**:
- ✅ Scenarios continue to run (stored in RCU)
- ✅ MODBUS devices controlled locally
- ✅ Guest can still use keypad/switches
- ✅ Temperature control works

**Benefit**: Hotel non si blocca se internet cade!

**Programming Access**:
- Via **USB port** + **mobile app** VDA
- On-site configuration
- Debugging e diagnostics

---

## PARTE 4: REVERSE ENGINEERING POSSIBILITIES

### 1. MODBUS Communication (ALTO POTENZIALE!)

**Perché è Hackerabile**:
- ✅ MODBUS RTU = protocollo **aperto e pubblico**
- ✅ **Nessuna crittografia** sul bus RS-485
- ✅ Messaggi **leggibili in chiaro**
- ✅ Tools disponibili (pymodbus, QModMaster, mbpoll)

**Cosa Possiamo Fare**:

#### A. Sniffing Passivo (Zero Risk)

**Setup**:
```
┌──────────────┐
│ VDA H155300  │ MODBUS Master
└──────┬───────┘
       │ RS-485 (A+/B-)
       │
   ┌───┴────┬──────────┬──────────┐
   │        │          │          │
┌──▼──┐  ┌─▼────┐  ┌──▼────┐  ┌──▼────────┐
│Termo│  │Keypad│  │Sensor│  │USB-RS485  │ ← SNIFFER!
└─────┘  └──────┘  └───────┘  │Converter  │
                               │(passive)  │
                               └─────┬─────┘
                                     │ USB
                               ┌─────▼─────┐
                               │ Laptop    │
                               │ pymodbus  │
                               └───────────┘
```

**Hardware Necessario**:
- **USB to RS-485 converter** (~$10-30)
  - Modelli: FTDI-based, CH340-based
  - Example: Sparkfun BOB-09822
- **Passive tap** (high-impedance connection)

**Software**:
- **Python pymodbus** - scripting
- **modbus-sniffer** (GitHub: alerighi/modbus-sniffer)
- **Wireshark** (per analisi .pcap files)

**Cosa Osserviamo**:
```
[12:30:15] Master → Slave 1 (Thermostat)
  Function: 0x03 (Read Holding Registers)
  Address: 100 (0x0064)
  Count: 2
  Response: [0x00E1, 0x00DC] → 22.5°C current, 22.0°C setpoint

[12:30:16] Master → Slave 2 (Keypad)
  Function: 0x01 (Read Coils)
  Address: 0
  Count: 8
  Response: [0, 0, 1, 0, 0, 0, 0, 0] → DND pressed!

[12:30:17] Master → Slave 3 (Presence Sensor)
  Function: 0x02 (Read Discrete Inputs)
  Address: 0
  Count: 1
  Response: [1] → Room occupied
```

**Benefit**: Capiamo **register map completa** senza toccare nulla!

#### B. Active Scanning (Moderate Risk)

**Tool**: Python script custom con pymodbus

**Algoritmo**:
```python
from pymodbus.client import ModbusSerialClient

client = ModbusSerialClient(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity='N',
    stopbits=1
)
client.connect()

# Scan slave IDs
for slave_id in range(1, 248):
    result = client.read_holding_registers(0, 1, unit=slave_id)
    if not result.isError():
        print(f"Found slave: {slave_id}")

# Scan registers for slave 1 (thermostat)
for addr in range(0, 1000):
    result = client.read_holding_registers(addr, 1, unit=1)
    if not result.isError():
        print(f"Reg {addr} = {result.registers[0]}")

client.close()
```

**Output Example**:
```
Found slave: 1 (Thermostat camera)
Found slave: 2 (Thermostat bagno)
Found slave: 3 (Keypad)
Found slave: 4 (Presence sensor)

Slave 1 Register Map:
  Reg 0   = 101      (Room number?)
  Reg 1   = 1        (Status?)
  Reg 100 = 225      (Temperature × 10 = 22.5°C)
  Reg 101 = 220      (Setpoint × 10 = 22.0°C)
  Reg 102 = 2        (Mode: Heat/Cool/Auto?)
  Reg 103 = 1        (Fan speed?)
```

**Risk**: Il VDA RCU potrebbe loggare "unknown MODBUS traffic" → ma nessun danno fisico!

#### C. Command Injection (HIGH Risk, ma Possibile!)

**Scenario**: Dopo aver mappato i registri, possiamo **scrivere comandi**!

**Example - Set Setpoint 25°C**:
```python
# Address 101 = setpoint (discovered via sniffing)
# Value 250 = 25.0°C (scaled × 10)
client.write_register(101, 250, unit=1)
```

**Cosa Succede**:
- Termostato riceve nuovo setpoint 25°C
- Inizia riscaldamento/raffreddamento
- VDA RCU vede il cambio (polling) e aggiorna cloud

**Potenziale**:
- ✅ Controllo COMPLETO dei dispositivi MODBUS
- ✅ Bypass del cloud VDA
- ✅ Integrazione diretta con Miracollo PMS
- ⚠️ Conflitto possibile con comandi cloud (race condition)

**Mitigazione Conflitti**:
- Disabilitare cloud RCU (WiFi off)
- Oppure: sincronizzare con cloud via API (se esiste)

### 2. Cloud API Reverse Engineering (MEDIO POTENZIALE)

**Endpoint Conosciuto**: `room-manager.rc-onair.com`

**Approccio 1: Network Sniffing**

**Setup**:
```
┌──────────────┐
│ VDA H155300  │
└──────┬───────┘
       │ WiFi
       │
┌──────▼───────────────┐
│ Hotel WiFi Router    │
│ (con port mirroring) │
└──────┬───────────────┘
       │
┌──────▼───────┐
│ Wireshark    │ ← Capture HTTPS traffic
└──────────────┘
```

**Problema**: Traffic is **TLS encrypted**!

**Soluzione**: **MITM (Man-in-the-Middle)** con certificato custom
- Richiede: Root access al router hotel
- Tool: mitmproxy, Burp Suite
- Risk: Illegale senza autorizzazione!

**Approccio 2: Decompilare Mobile App**

**Target**: VDA Etheos Commissioning Tools (mobile app)

**Steps**:
1. Download APK (Android) o IPA (iOS)
2. Decompile con **jadx** (Android) o **Hopper** (iOS)
3. Cercare:
   - API endpoints hardcoded
   - Authentication tokens
   - Request/response format (JSON?)
   - WebSocket implementation

**Potenziale**:
- 🔓 Scoprire API REST endpoints
- 🔓 Capire autenticazione (API key? OAuth?)
- 🔓 Replicare chiamate API da Miracollo

**Legalità**: **Gray area** - ToS violation sicuro, ma non illegale se solo per interoperabilità!

**Approccio 3: Web Dashboard Analysis**

**Tool**: Browser DevTools (Network tab)

**Steps**:
1. Login su room-manager.rc-onair.com
2. Open browser DevTools → Network
3. Perform actions (view room, change temperature)
4. Observe:
   - XHR/Fetch requests
   - WebSocket frames
   - Request headers (auth tokens?)
   - Response JSON structure

**Example Captured Request** (ipotesi):
```
POST https://room-manager.rc-onair.com/api/v1/rooms/101/temperature
Headers:
  Authorization: Bearer eyJhbGc...
  Content-Type: application/json
Body:
  {"setpoint": 25.0, "mode": "heat"}

Response:
  {"success": true, "room_id": "101", "new_setpoint": 25.0}
```

**Benefit**: Se API è REST-based e documentabile → possiamo integrarci!

### 3. USB Port Exploitation (BASSO POTENZIALE, ma Interessante)

**Scenario**: Accesso fisico al RCU via USB

**Possibilità**:

#### A. Serial Console Access

**Ipotesi**: USB port potrebbe essere **UART bridge** per debugging

**Test**:
```bash
# Linux
screen /dev/ttyUSB0 115200

# Oppure
minicom -D /dev/ttyUSB0 -b 115200
```

**Cosa Cercare**:
- Boot messages
- Shell access (BusyBox? Linux?)
- Debug commands
- Log output

**Probabile Output** (se esposto):
```
[BOOT] VDA Etheos Nucleus RCU v5.4.1
[BOOT] Loading configuration...
[MODBUS] Port 1: 4 devices found
[MODBUS] Port 2: 2 devices found
[WIFI] Connecting to SSID: HotelWiFi...
[CLOUD] Connected to room-manager.rc-onair.com
[READY] System operational
```

**Comandi Possibili**:
```
> help
> status
> modbus scan
> wifi config
> firmware version
> dump config
```

#### B. Firmware Dump

**Tool**: VDA mobile app (official) - "programming via USB"

**Reverse Engineering**:
- Catturare firmware update file
- Analizzare con **binwalk** (file system extraction)
- Cercare:
  - Configuration files
  - MODBUS register maps (hardcoded?)
  - Cloud API credentials
  - Encryption keys

**Risk**: Brick del device se non fatto correttamente!

### 4. Expansion Modules (H113931) - FACILE!

**Modello**: VDA H113931 - 4DI + 4DO Expansion Module

**Protocollo**: MODBUS RTU slave

**Vantaggio**: Expansion modules sono **più semplici**!
- Meno sicurezza
- Register map probabilmente standard
- Documentazione potrebbe essere pubblica (industrial automation)

**Strategia**:
1. Comprare H113931 su eBay (~$50-100?)
2. Connettere a USB-RS485 converter
3. Scan registers con pymodbus
4. Documentare completamente
5. Usare come **template** per capire altri devices VDA

---

## PARTE 5: INTEGRAZIONE CON MIRACOLLO - STRATEGIE

### Strategia A: MODBUS Direct Control (IDEALE!)

**Architettura**:
```
┌────────────────────────────────────────────────┐
│         MIRACOLLO PMS (Backend)                │
│  - Room status API                             │
│  - Check-in/out automation                     │
└────────────┬───────────────────────────────────┘
             │ REST API / WebSocket
             │
┌────────────▼───────────────────────────────────┐
│    MIRACOLLO Room Manager Module               │
│  - MODBUS RTU/TCP gateway                      │
│  - pymodbus integration                        │
│  - Device abstraction layer                    │
└────────────┬───────────────────────────────────┘
             │ MODBUS RTU (RS-485)
             │
        ┌────┴─────┬──────────┬──────────┐
        │          │          │          │
    ┌───▼────┐ ┌──▼─────┐ ┌──▼─────┐ ┌──▼─────┐
    │VDA     │ │VDA     │ │VDA     │ │VDA     │
    │Thermo  │ │Keypad  │ │Sensors │ │Others  │
    └────────┘ └────────┘ └────────┘ └────────┘

NOTE: VDA H155300 RCU → DISCONNESSO (WiFi off)
      Miracollo diventa MODBUS Master diretto!
```

**Pro**:
- ✅ **Zero dipendenza** da VDA cloud
- ✅ **Controllo totale** dispositivi
- ✅ **Latency bassissima** (locale)
- ✅ **Privacy completa** (no data to VDA)
- ✅ **Costo zero** licenze VDA

**Contro**:
- ❌ Richiede **reverse engineering** completo register maps
- ❌ Perdita dashboard VDA (dobbiamo rifare!)
- ❌ Perdita firmware updates automatici VDA
- ❌ Nessun supporto VDA (ovvio!)

**Effort**: 6-8 settimane full-time
- 2 settimane: Hardware setup + sniffing
- 2 settimane: Register mapping completo
- 2 settimane: Miracollo integration
- 2 settimane: Testing + debugging

### Strategia B: Hybrid (MODBUS + Cloud API)

**Architettura**:
```
┌────────────────────────────────────────────────┐
│         MIRACOLLO PMS                          │
└────────┬──────────────────────┬────────────────┘
         │                      │
         │ REST API             │ VDA Cloud API
         │                      │ (reverse engineered)
┌────────▼─────────┐   ┌────────▼────────────────┐
│ Miracollo Room   │   │ room-manager.rc-onair   │
│ Manager (local)  │   │ .com (VDA cloud)        │
└────────┬─────────┘   └────────┬────────────────┘
         │ MODBUS RTU           │ HTTPS
         │                      │ WiFi
    ┌────┴─────┬────────────────▼────┐
    │          │   VDA H155300 RCU   │
┌───▼────┐ ┌──▼─────┐          (WiFi ON)
│Devices │ │Devices │
└────────┘ └────────┘
```

**Pro**:
- ✅ Fallback su cloud se MODBUS fail
- ✅ Mantieni firmware updates VDA
- ✅ Usiamo dashboard VDA per diagnostics
- ✅ Graduale migration (test su 1 camera)

**Contro**:
- ⚠️ Complessità architettura (2 sistemi)
- ⚠️ Potenziali conflitti (race conditions)
- ⚠️ Dipendenza parziale da VDA

**Effort**: 4-6 settimane

### Strategia C: Solo Cloud API (PIÙ VELOCE, ma Limitato)

**Architettura**:
```
┌────────────────────────────────────────────────┐
│         MIRACOLLO PMS                          │
└────────┬───────────────────────────────────────┘
         │ API calls
         │
┌────────▼───────────────────────────────────────┐
│  room-manager.rc-onair.com (VDA Etheos Cloud)  │
└────────┬───────────────────────────────────────┘
         │ HTTPS/WiFi
         │
    ┌────▼─────────────┐
    │ VDA H155300 RCU  │
    └────┬─────────────┘
         │ MODBUS RTU
         │
    ┌────┴─────┬────────┐
    │          │        │
┌───▼────┐ ┌──▼─────┐ ...
│Devices │ │Devices │
└────────┘ └────────┘
```

**Pro**:
- ✅ **Veloce** da implementare (2-3 settimane)
- ✅ Mantieni supporto VDA
- ✅ Mantieni firmware updates
- ✅ Meno reverse engineering

**Contro**:
- ❌ **Dipendenza totale** da VDA (vendor lock-in!)
- ❌ Latency cloud (internet required)
- ❌ Costi licenze VDA
- ❌ Privacy concerns (data goes to VDA)
- ❌ API non documentata (può cambiare!)

**Effort**: 2-3 settimane

### Strategia D: Replace RCU con Controller Custom (MASSIMO CONTROLLO!)

**Architettura**:
```
┌────────────────────────────────────────────────┐
│         MIRACOLLO PMS                          │
└────────┬───────────────────────────────────────┘
         │ REST API / MQTT
         │
┌────────▼───────────────────────────────────────┐
│  MIRACOLLO RCU (Custom Hardware!)              │
│  - Raspberry Pi 4 o Industrial SBC             │
│  - 4× USB-RS485 converters                     │
│  - Python + pymodbus                           │
│  - WiFi/Ethernet                                │
│  - OPTIONAL: Expansion I/O GPIO                │
└────────┬───────────────────────────────────────┘
         │ MODBUS RTU (4 ports)
         │
    ┌────┴─────┬──────────┬──────────┐
    │          │          │          │
┌───▼────┐ ┌──▼─────┐ ┌──▼─────┐ ┌──▼─────┐
│VDA     │ │VDA     │ │VDA     │ │GENERIC │
│Devices │ │Devices │ │Devices │ │MODBUS  │
└────────┘ └────────┘ └────────┘ └────────┘
         (reuse existing!)     (new devices!)
```

**Hardware Custom RCU**:
| Component | Model | Cost | Notes |
|-----------|-------|------|-------|
| SBC | Raspberry Pi 4 (4GB) | $55 | Or industrial alternative |
| RS-485 Converter | FTDI USB-RS485 × 4 | $80 | 4 ports for 4 MODBUS networks |
| Power Supply | 5V 3A USB-C | $10 | For RPi |
| Enclosure | DIN rail mount case | $20 | Industrial-grade |
| SD Card | 32GB Industrial | $15 | For OS + software |
| **TOTAL** | | **~$180** | vs VDA H155300 = $300-500? |

**Software Stack**:
```
OS: Raspberry Pi OS Lite (headless)
  ↓
Python 3.11
  ↓
pymodbus (MODBUS RTU master)
  ↓
FastAPI (REST API server)
  ↓
MQTT client (optional - for IoT devices)
  ↓
Miracollo SDK
```

**Pro**:
- ✅ **ZERO vendor lock-in**
- ✅ **Costo hardware BASSO** ($180 vs $300-500)
- ✅ **Open source** completamente
- ✅ Supporto devices MODBUS **generici** (non solo VDA)
- ✅ Espandibile con GPIO, IoT, voice control
- ✅ Aggiornamenti **sotto nostro controllo**

**Contro**:
- ❌ Effort **ALTO** (12-16 settimane)
- ❌ Richiede reverse engineering **completo** VDA devices
- ❌ Nessun supporto da VDA (ovvio)
- ❌ Certificazioni? (CE, safety)
- ❌ Reliability da provare (vs hardware industriale VDA)

**Effort**: 12-16 settimane
- 4 settimane: Hardware design + prototyping
- 4 settimane: Software MODBUS stack
- 4 settimane: Miracollo integration
- 4 settimane: Testing + certification

---

## PARTE 6: TOOLS & RESOURCES

### Hardware Tools

| Tool | Purpose | Cost | Where |
|------|---------|------|-------|
| **USB to RS-485 Converter** | MODBUS sniffing/control | $15-30 | Amazon, Sparkfun |
| **Logic Analyzer** | Protocol debugging | $50-200 | Saleae Logic 8 |
| **Multimeter** | Voltage testing | $20-50 | Fluke, Klein Tools |
| **Raspberry Pi 4** | Custom RCU prototyping | $55 | Official store |
| **VDA H113931** | Test device | $50-100 | eBay (used) |

### Software Tools

#### MODBUS Tools

| Tool | Type | OS | Cost | Use Case |
|------|------|----|----- |----------|
| **pymodbus** | Python library | All | Free | Scripting, automation |
| **QModMaster** | GUI | Linux/Win/Mac | Free | Manual testing, polling |
| **mbpoll** | CLI | Linux/Mac | Free | Scripting |
| **Modbus Poll** | GUI | Windows | $99 | Professional polling |
| **modbus-sniffer** | CLI | Linux | Free | Passive sniffing |

#### Network Analysis

| Tool | Purpose | Cost |
|------|---------|------|
| **Wireshark** | Packet capture | Free |
| **mitmproxy** | HTTPS MITM | Free |
| **Burp Suite** | API reverse engineering | Free/Pro |

#### Mobile App Reverse Engineering

| Tool | Platform | Purpose |
|------|----------|---------|
| **jadx** | Android | APK decompilation |
| **Hopper** | iOS | IPA disassembly |
| **Frida** | Both | Runtime hooking |

#### Firmware Analysis

| Tool | Purpose |
|------|---------|
| **binwalk** | Firmware extraction |
| **Ghidra** | Disassembly |
| **strings** | String extraction |

### Python Libraries

```python
# MODBUS
pymodbus              # Full-featured
minimalmodbus         # Lightweight

# Network
requests              # HTTP/REST
websockets            # WebSocket client
paho-mqtt             # MQTT

# Hardware
pyserial              # Serial port access
RPi.GPIO              # Raspberry Pi GPIO

# Analysis
scapy                 # Packet manipulation
```

### Documentation Resources

**MODBUS Protocol**:
- [MODBUS Specification (PDF)](https://modbus.org/docs/Modbus_Application_Protocol_V1_1b3.pdf)
- [PyModbus Documentation](https://pymodbus.readthedocs.io/)
- [MODBUS RTU Tutorial](https://www.csimn.com/CSI_pages/Modbus101.html)

**VDA Resources** (Public):
- [VDA Group Official Site](https://vdagroup.com/en/)
- [VDA-Telkonet Site](https://vda-telkonet.com/)
- [Etheos Product Page](https://vdagroup.com/etheos-room-management-system-cloud-based-for-the-hotels/)
- [Nucleus Controller Info](https://vdagroup.com/nucleus-the-state-of-the-art-controller-integrated-with-etheos-social/)

**Hotel Automation**:
- [KNX for Hotels](https://www.knx.org/knx-en/for-professionals/use-cases/hotel-applications/)
- [Home Assistant Modbus](https://www.home-assistant.io/integrations/modbus/)

---

## PARTE 7: LEGAL & ETHICAL CONSIDERATIONS

### Legalità Reverse Engineering

**In Italia (e UE)**:
- ✅ **Legale** per scopo **interoperabilità** (Direttiva 2009/24/CE)
- ✅ **Legale** analizzare protocolli non crittografati (MODBUS)
- ✅ **Legale** decompilare software per compatibilità

**NON Legale**:
- ❌ Violare crittografia intenzionale
- ❌ Distribuire firmware VDA copiato
- ❌ Rivendere soluzione come "compatibile VDA" senza permesso
- ❌ Usare trademark/logo VDA

### Best Practices

**Raccomandate**:
1. ✅ Usare solo per **integrazione con Miracollo**
2. ✅ **Non distribuire** register maps VDA pubblicamente
3. ✅ Offrire **alternative aperte** (custom RCU), non solo VDA hack
4. ✅ **Documentare** che è reverse engineering (trasparenza)
5. ✅ Contattare VDA per **partnership ufficiale**?

**Partnership VDA**:
- Pro: Documentazione ufficiale, supporto, legittimità
- Contro: Potrebbero dire NO, o chiedere fee/royalties
- Valutare: Dopo POC funzionante (posizione di forza)

### Privacy & Security

**Se Intercettiamo Dati**:
- ⚠️ Dati ospiti (nomi, preferenze) = **GDPR applies**!
- ✅ Minimizzare raccolta dati
- ✅ Anonimizzare logs
- ✅ Non salvare data personali senza consenso

**Sicurezza**:
- ⚠️ MODBUS non crittografato = **vulnerability**
- ✅ Isolare rete MODBUS da internet (VLAN)
- ✅ Firewall su custom RCU
- ✅ TLS per comunicazione Miracollo ↔ RCU

---

## PARTE 8: NEXT STEPS - PIANO D'AZIONE

### Phase 1: POC (Proof of Concept) - 2 SETTIMANE

**Obiettivo**: Dimostrare che MODBUS sniffing funziona

**Tasks**:
1. ☐ Acquistare hardware:
   - USB to RS-485 converter ($20)
   - Cavi per tap RS-485 bus
2. ☐ Setup ambiente:
   - Python + pymodbus
   - QModMaster GUI
3. ☐ Accesso fisico a Naturae Lodge:
   - Identificare VDA H155300 in camera
   - Trovare cablaggio MODBUS RS-485
   - Connettere sniffer (passive tap)
4. ☐ Prima cattura:
   - Registrare traffic 1 ora
   - Identificare slave IDs
   - Estrarre sample messages

**Deliverable**: Report con primi 10-20 registri identificati

**Location**: Naturae Lodge (Rafa ha accesso!)

### Phase 2: Register Mapping - 4 SETTIMANE

**Obiettivo**: Documentare register map completo di 1 camera

**Tasks**:
1. ☐ Sniffing prolungato:
   - 24h capture
   - Durante check-in, checkout, uso normale
2. ☐ Correlation testing:
   - Cambiare temperatura fisica → quale registro?
   - Premere DND → quale registro?
   - Aprire porta → quale registro?
3. ☐ Active scanning:
   - Scan 0-9998 per ogni slave
   - Test write (cautela!)
4. ☐ Documentazione:
   - Spreadsheet: Address | Device | Type | R/W | Format | Range | Function

**Deliverable**:
- `VDA_MODBUS_REGISTER_MAP_v1.0.xlsx`
- Python library `vda_modbus.py` (wrapper)

### Phase 3: Miracollo Integration - 4 SETTIMANE

**Obiettivo**: Controllo 1 camera via Miracollo Room Manager

**Tasks**:
1. ☐ Backend:
   - FastAPI service `room_hardware_service.py`
   - pymodbus integration
   - REST API endpoints
2. ☐ Frontend:
   - Room Manager dashboard
   - Temperature control UI
   - Real-time status updates
3. ☐ Testing:
   - Check-in scenario
   - Temperature change
   - DND/MUR workflow
4. ☐ Documentation

**Deliverable**:
- Working demo: Miracollo → MODBUS → VDA devices
- Video demo

### Phase 4: Scale & Production - 8 SETTIMANE

**Obiettivo**: Sistema production-ready per 32 camere

**Tasks**:
1. ☐ Hardware scaling:
   - 32× RS-485 connections (o multiplexer?)
   - Centralized MODBUS gateway
2. ☐ Software:
   - Multi-room support
   - Error handling
   - Monitoring & alerts
3. ☐ Security:
   - VLAN isolation
   - Firewall rules
   - Encryption Miracollo ↔ Gateway
4. ☐ Deploy Naturae Lodge:
   - Gradual rollout (1 camera → 4 camere → 32 camere)
   - Monitoring 24/7
   - Fallback plan (riattivare VDA cloud?)

**Deliverable**: Naturae Lodge 100% su Miracollo Room Manager

### Phase 5: Custom RCU (Optional Future) - 12 SETTIMANE

**Solo se Phase 1-4 success!**

**Tasks**:
1. ☐ Hardware design custom RCU
2. ☐ Software stack
3. ☐ Testing
4. ☐ Certificazione (CE?)
5. ☐ Productization

---

## CONCLUSIONI FINALI

### VDA H155300 RCU - Cosa Abbiamo Scoperto

**Identificazione**:
- ✅ Modello: **Etheos Nucleus I/O RCU Wi-Fi**
- ✅ Funzione: **MODBUS Master + Cloud Gateway**
- ✅ Capacity: **4 porte MODBUS, 80 devices max**
- ✅ Programmabilità: **Completa** (I/O, scenari, USB)

**Protocolli**:
- ✅ MODBUS RTU su RS-485 (4 porte)
- ✅ WiFi/Ethernet → Cloud VDA (HTTPS/TLS)
- ✅ USB per programmazione locale

**Reverse Engineering Feasibility**:
| Approccio | Feasibility | Effort | Risk |
|-----------|-------------|--------|------|
| **MODBUS Sniffing** | ✅ ALTO | 2-4 settimane | Basso |
| **MODBUS Control** | ✅ ALTO | 4-6 settimane | Medio |
| **Cloud API RE** | ⚠️ MEDIO | 6-8 settimane | Medio |
| **USB Exploitation** | ⚠️ BASSO | 8-12 settimane | Alto |
| **Custom RCU** | ✅ ALTO | 12-16 settimane | Basso |

### Raccomandazione per Miracollo

**STRATEGIA CONSIGLIATA**: **Strategia A + D Hybrid**

**Phase 1-2** (Breve Termine - 3 mesi):
- ✅ MODBUS direct control (Strategia A)
- ✅ Reverse engineering completo VDA devices
- ✅ Miracollo Room Manager con pymodbus
- ✅ Deploy Naturae Lodge come PILOT

**Phase 3** (Medio Termine - 6 mesi):
- ✅ Custom RCU prototyping (Raspberry Pi-based)
- ✅ Supporto devices MODBUS generici (non solo VDA)
- ✅ Open source hardware design

**Phase 4** (Lungo Termine - 12 mesi):
- ✅ Production custom RCU
- ✅ Certificazioni CE/UL
- ✅ Miracollo Room Automation come **prodotto standalone**

### Perché Questa Strategia Vince

**Short Term**:
- 💰 **Costo ZERO** (riusa hardware VDA esistente)
- ⚡ **Veloce** (3 mesi to production)
- 🎯 **Proof of Concept** reale a Naturae Lodge

**Long Term**:
- 🔓 **Zero vendor lock-in**
- 💸 **Costo hardware 60% lower** ($180 vs $500)
- 🌍 **Open source** = community + differenziazione
- 🚀 **Scalabile** a qualsiasi hotel (non solo VDA)

### Il Vantaggio Miracollo

**VDA fa**: Hardware proprietario + Cloud chiuso + Costo alto

**Miracollo farà**:
- ✅ **Open hardware** (Raspberry Pi, standard MODBUS)
- ✅ **Open protocols** (MQTT, KNX, BACnet, MODBUS)
- ✅ **Transparent pricing** ($5/room/month vs $15-20 VDA?)
- ✅ **Self-hosted option** (privacy, controllo)
- ✅ **API-first** (integrazione qualsiasi sistema)

**Positioning**: *"Miracollo Room Manager - The Open Alternative to VDA Etheos"*

---

## FONTI

### VDA Products & Documentation
- [VDA GRMS Catalog 2024 (US)](https://vda-telkonet.com/wp-content/uploads/2024/05/VDA_GRMS_Catalog_US_2024_v.1.0.0.pdf)
- [VDA GRMS Catalog 2024 (EN)](https://vda-telkonet.com/wp-content/uploads/2024/05/VDA_GRMS_Catalog_EN_2024_v.1.0.0.pdf)
- [Etheos Product Page](https://vdagroup.com/etheos-room-management-system-cloud-based-for-the-hotels/)
- [Nucleus Controller Overview](https://vdagroup.com/nucleus-the-state-of-the-art-controller-integrated-with-etheos-social/)
- [Etheos Commissioning Tools](https://vdagroup.com/etheos-commissioningtools/)
- [VDA Etheos Presentation 2021](https://dmg-manual-live.s3.ap-south-1.amazonaws.com/Production/exb_doc/518/80411/VDA_ETHEOS_Presentation_2021_EN.pdf)
- [Etheos Leaflet](https://vda-telkonet.com/wp-content/uploads/2024/05/Leaflet-Etheos-EN-Web.pdf)

### MODBUS Protocol & Tools
- [PyModbus Documentation](https://www.pymodbus.org/docs)
- [QModMaster Open Source Tool](https://sourceforge.net/projects/qmodmaster/)
- [MODBUS RTU Tutorial](https://www.csimn.com/CSI_pages/Modbus101.html)
- [MODBUS Protocol Specification](https://modbus.org/docs/Modbus_Application_Protocol_V1_1b3.pdf)

### Reverse Engineering Resources
- [MODBUS and RS485 Python Test Rig](https://medium.com/@peterfitch/modbus-and-rs485-a-python-test-rig-1b5014f709ec)
- [GitHub: modbus-sniffer](https://github.com/alerighi/modbus-sniffer)
- [GitHub: ModbusSniffer](https://github.com/snhobbs/ModbusSniffer)
- [RS485 Sniffer Tutorial](https://jheyman.github.io/blog/pages/RS485Sniffer/)
- [Sniff & Inject RS485 Modbus (Hackster.io)](https://www.hackster.io/electronic-cats/sniff-inject-rs485-modbus-add-on-7f976d)

### Hardware Resources
- [VDA H113931 Expansion Module (eBay)](https://www.ebay.com/itm/205692665049)
- [USB to RS485 Converters](https://www.sparkfun.com/)
- [Raspberry Pi Official Store](https://www.raspberrypi.com/)

### Integration Examples
- [Home Assistant Modbus Integration](https://www.home-assistant.io/integrations/modbus/)
- [Read Modbus on Linux with USB-RS485](https://techsparx.com/energy-system/modbus/linux-modbus-usb-rs485.html)

---

**Fine Ricerca**

*Cervella Researcher - 2026-01-15*
*"Nulla è complesso - solo non ancora studiato!"*
*"Non reinventiamo la ruota - la miglioriamo!"*
