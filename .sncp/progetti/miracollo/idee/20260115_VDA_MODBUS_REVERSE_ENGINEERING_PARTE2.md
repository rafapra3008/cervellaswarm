# VDA MODBUS REVERSE ENGINEERING - STUDIO COMPLETO PARTE 2

**Data**: 2026-01-15
**Ricercatrice**: Cervella Researcher
**Status**: ✅ COMPLETATA
**Obiettivo**: Implementazione Python + Hardware setup per reverse engineering VDA MODBUS

---

## PARTE 5: IMPLEMENTAZIONE PYTHON CON PYMODBUS

### Setup Ambiente

```bash
# Installa pymodbus
pip install pymodbus

# Opzionale: minimalmodbus (più semplice per RTU)
pip install minimalmodbus

# Tools utili
pip install pyserial    # Per comunicazione seriale
pip install pandas      # Per export dati
```

### PyModbus: Complete Example

```python
#!/usr/bin/env python3
"""
VDA MODBUS Scanner - Reverse Engineering Tool
Scansiona dispositivi MODBUS RTU su RS-485
"""

from pymodbus.client import ModbusSerialClient
import time
import json
from datetime import datetime


class VDAModbusScanner:
    """Scanner per dispositivi VDA MODBUS RTU"""

    def __init__(self, port='/dev/ttyUSB0', baudrate=9600,
                 parity='N', stopbits=1, bytesize=8, timeout=1):
        """
        Inizializza client MODBUS RTU

        Args:
            port: Porta seriale (es. /dev/ttyUSB0 su Linux, COM3 su Windows)
            baudrate: Velocità comunicazione (tipicamente 9600 o 19200)
            parity: Parità ('N'=None, 'E'=Even, 'O'=Odd)
            stopbits: Bit di stop (1 o 2)
            bytesize: Dimensione byte (8)
            timeout: Timeout in secondi
        """
        self.client = ModbusSerialClient(
            port=port,
            baudrate=baudrate,
            parity=parity,
            stopbits=stopbits,
            bytesize=bytesize,
            timeout=timeout
        )

        self.scan_results = {}
        self.device_info = {}

    def connect(self):
        """Connette al bus MODBUS"""
        if self.client.connect():
            print(f"✅ Connected to {self.client.port} @ {self.client.baudrate} baud")
            return True
        else:
            print(f"❌ Failed to connect to {self.client.port}")
            return False

    def disconnect(self):
        """Disconnette dal bus"""
        self.client.close()
        print("🔌 Disconnected")

    def scan_slave_ids(self, start_id=1, end_id=247):
        """
        Scansiona slave IDs per trovare dispositivi attivi

        Args:
            start_id: Primo ID da testare (default 1)
            end_id: Ultimo ID da testare (default 247)

        Returns:
            Lista di slave IDs che hanno risposto
        """
        print(f"\n🔍 Scanning slave IDs {start_id}-{end_id}...")
        active_slaves = []

        for slave_id in range(start_id, end_id + 1):
            try:
                # Prova leggere 1 registro da address 0
                result = self.client.read_holding_registers(
                    address=0,
                    count=1,
                    slave=slave_id
                )

                if not result.isError():
                    print(f"  ✅ Found slave: {slave_id}")
                    active_slaves.append(slave_id)
                else:
                    # Silent fail (slave non presente)
                    pass

            except Exception as e:
                # Silent fail
                pass

            # Delay per non saturare bus
            time.sleep(0.05)

        print(f"\n✅ Found {len(active_slaves)} active devices: {active_slaves}")
        return active_slaves

    def scan_registers(self, slave_id, start_addr=0, end_addr=1000,
                      block_size=50, delay=0.5):
        """
        Scansiona registri holding di un dispositivo

        Args:
            slave_id: ID del dispositivo
            start_addr: Primo indirizzo da scansionare
            end_addr: Ultimo indirizzo da scansionare
            block_size: Numero registri per richiesta
            delay: Delay (secondi) tra richieste

        Returns:
            Dict {address: value} con registri trovati
        """
        print(f"\n🔍 Scanning registers {start_addr}-{end_addr} " +
              f"for slave {slave_id}...")

        registers = {}
        scanned = 0
        found = 0

        for address in range(start_addr, end_addr, block_size):
            count = min(block_size, end_addr - address)

            try:
                result = self.client.read_holding_registers(
                    address=address,
                    count=count,
                    slave=slave_id
                )

                if not result.isError():
                    # Salva registri trovati
                    for i, value in enumerate(result.registers):
                        registers[address + i] = value
                        found += 1

                scanned += count

                # Progress
                if scanned % 200 == 0:
                    print(f"  ... scanned {scanned}/{end_addr - start_addr} " +
                          f"(found {found} registers)")

            except Exception as e:
                # Silent fail per blocchi non esistenti
                pass

            time.sleep(delay)

        print(f"✅ Scan complete: found {found} registers")
        self.scan_results[slave_id] = registers
        return registers

    def read_register(self, slave_id, address):
        """
        Legge un singolo registro holding

        Args:
            slave_id: ID dispositivo
            address: Indirizzo registro (0-based)

        Returns:
            Valore (int) o None se errore
        """
        try:
            result = self.client.read_holding_registers(
                address=address,
                count=1,
                slave=slave_id
            )

            if not result.isError():
                return result.registers[0]
            else:
                return None

        except Exception as e:
            print(f"❌ Error reading register {address}: {e}")
            return None

    def write_register(self, slave_id, address, value):
        """
        Scrive un singolo registro holding

        Args:
            slave_id: ID dispositivo
            address: Indirizzo registro (0-based)
            value: Valore da scrivere (0-65535)

        Returns:
            True se successo, False altrimenti
        """
        try:
            result = self.client.write_register(
                address=address,
                value=value,
                slave=slave_id
            )

            if not result.isError():
                print(f"✅ Written {value} to register {address}")
                return True
            else:
                print(f"❌ Failed to write register {address}")
                return False

        except Exception as e:
            print(f"❌ Error writing register {address}: {e}")
            return False

    def monitor_register(self, slave_id, address, interval=1.0, duration=60):
        """
        Monitora un registro in tempo reale

        Args:
            slave_id: ID dispositivo
            address: Indirizzo registro
            interval: Intervallo polling (secondi)
            duration: Durata totale monitoring (secondi)

        Returns:
            Lista di tuple (timestamp, value)
        """
        print(f"\n📊 Monitoring register {address} for {duration}s...")
        print(f"   (Interval: {interval}s)")
        print("\nTime                 | Value (dec) | Value (hex) | Change")
        print("-" * 65)

        history = []
        prev_value = None
        start_time = time.time()

        while time.time() - start_time < duration:
            value = self.read_register(slave_id, address)

            if value is not None:
                timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                change = ""

                if prev_value is not None:
                    if value > prev_value:
                        change = f"↑ +{value - prev_value}"
                    elif value < prev_value:
                        change = f"↓ {value - prev_value}"

                print(f"{timestamp} | {value:11d} | 0x{value:08X} | {change}")

                history.append((timestamp, value))
                prev_value = value

            time.sleep(interval)

        print("\n✅ Monitoring complete")
        return history

    def decode_temperature(self, value, scale=10):
        """
        Decodifica valore temperatura (tipicamente scaled x10 o x100)

        Args:
            value: Valore raw registro (int)
            scale: Fattore scala (10 o 100)

        Returns:
            Temperatura in °C (float)
        """
        return value / scale

    def encode_temperature(self, temp_celsius, scale=10):
        """
        Codifica temperatura per scrittura registro

        Args:
            temp_celsius: Temperatura in °C (float)
            scale: Fattore scala (10 o 100)

        Returns:
            Valore intero per registro
        """
        return int(temp_celsius * scale)

    def export_scan_results(self, filename="vda_scan_results.json"):
        """
        Esporta risultati scan in file JSON

        Args:
            filename: Nome file output
        """
        data = {
            'timestamp': datetime.now().isoformat(),
            'device_info': self.device_info,
            'scan_results': self.scan_results
        }

        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"💾 Results exported to {filename}")

    def import_scan_results(self, filename="vda_scan_results.json"):
        """
        Importa risultati scan da file JSON

        Args:
            filename: Nome file input
        """
        with open(filename, 'r') as f:
            data = json.load(f)

        self.device_info = data.get('device_info', {})
        self.scan_results = data.get('scan_results', {})

        print(f"📂 Results imported from {filename}")


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

def example_1_discover_devices():
    """Esempio 1: Scoprire dispositivi sul bus"""

    scanner = VDAModbusScanner(
        port='/dev/ttyUSB0',    # Linux: /dev/ttyUSB0, Windows: COM3
        baudrate=9600,
        parity='N',
        stopbits=1
    )

    if scanner.connect():
        # Trova dispositivi attivi
        active_slaves = scanner.scan_slave_ids(start_id=1, end_id=20)

        # Per ogni dispositivo, scansiona primi 200 registri
        for slave_id in active_slaves:
            registers = scanner.scan_registers(
                slave_id=slave_id,
                start_addr=0,
                end_addr=200,
                block_size=20,
                delay=0.5
            )

            print(f"\n📋 Slave {slave_id} - Found {len(registers)} registers")
            for addr, value in sorted(registers.items())[:10]:
                print(f"   Register {addr:4d}: {value:5d} (0x{value:04X})")

        # Salva risultati
        scanner.export_scan_results("vda_discovery.json")

        scanner.disconnect()


def example_2_monitor_temperature():
    """Esempio 2: Monitorare temperatura in tempo reale"""

    scanner = VDAModbusScanner(port='/dev/ttyUSB0', baudrate=9600)

    if scanner.connect():
        # Monitor registro 2 (ipotizziamo sia temperatura attuale)
        history = scanner.monitor_register(
            slave_id=1,
            address=2,
            interval=2.0,     # Ogni 2 secondi
            duration=60       # Per 1 minuto
        )

        # Decodifica e stampa statistiche
        temps = [scanner.decode_temperature(v) for _, v in history]
        print(f"\n📊 Temperature statistics:")
        print(f"   Min: {min(temps):.1f}°C")
        print(f"   Max: {max(temps):.1f}°C")
        print(f"   Avg: {sum(temps)/len(temps):.1f}°C")

        scanner.disconnect()


def example_3_set_temperature():
    """Esempio 3: Impostare setpoint temperatura"""

    scanner = VDAModbusScanner(port='/dev/ttyUSB0', baudrate=9600)

    if scanner.connect():
        slave_id = 1
        setpoint_register = 3  # Ipotizziamo registro 3 = setpoint

        # Leggi setpoint corrente
        current = scanner.read_register(slave_id, setpoint_register)
        current_temp = scanner.decode_temperature(current)
        print(f"📖 Current setpoint: {current_temp:.1f}°C")

        # Imposta nuovo setpoint: 22.5°C
        new_setpoint = 22.5
        new_value = scanner.encode_temperature(new_setpoint)

        # ⚠️ ATTENZIONE: Verifica prima che sia il registro giusto!
        confirm = input(f"Set temperature to {new_setpoint}°C? (yes/no): ")

        if confirm.lower() == 'yes':
            scanner.write_register(slave_id, setpoint_register, new_value)

            # Verifica scrittura
            time.sleep(1)
            verify = scanner.read_register(slave_id, setpoint_register)
            verify_temp = scanner.decode_temperature(verify)
            print(f"✅ Verified setpoint: {verify_temp:.1f}°C")

        scanner.disconnect()


def example_4_correlation_test():
    """
    Esempio 4: Test correlazione fisica-digitale

    PROCEDURA:
    1. Monitor registro sospetto
    2. Manualmente cambia temperatura sul dispositivo fisico
    3. Osserva quale registro cambia → BINGO!
    """

    scanner = VDAModbusScanner(port='/dev/ttyUSB0', baudrate=9600)

    if scanner.connect():
        slave_id = 1

        print("\n" + "="*60)
        print("CORRELATION TEST")
        print("="*60)
        print("\nMonitoring multiple registers simultaneously.")
        print("NOW: Go to physical device and change temperature!")
        print("Watch which register changes...\n")

        # Monitor 10 registri simultaneamente
        registers_to_monitor = list(range(0, 10))
        prev_values = {}

        for _ in range(60):  # 1 minuto
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}]")

            for addr in registers_to_monitor:
                value = scanner.read_register(slave_id, addr)

                if value is not None:
                    change = ""
                    if addr in prev_values and value != prev_values[addr]:
                        change = f" ← CHANGED! (was {prev_values[addr]})"

                    print(f"  Reg {addr:3d}: {value:5d} (0x{value:04X}){change}")
                    prev_values[addr] = value

            time.sleep(2)

        scanner.disconnect()


if __name__ == "__main__":
    print("VDA MODBUS Scanner - Reverse Engineering Tool")
    print("=" * 60)
    print("\nAvailable examples:")
    print("  1. Discover devices on bus")
    print("  2. Monitor temperature register")
    print("  3. Set temperature setpoint")
    print("  4. Correlation test (physical ↔ digital)")
    print("\nUncomment the example you want to run in main()\n")

    # Uncomment one:
    # example_1_discover_devices()
    # example_2_monitor_temperature()
    # example_3_set_temperature()
    # example_4_correlation_test()
```

### MinimalModbus: Alternative Più Semplice

Per casi d'uso semplici, `minimalmodbus` è più facile:

```python
#!/usr/bin/env python3
"""
VDA Thermostat Controller - Simple Version con MinimalModbus
"""

import minimalmodbus
import time


class VDAThermostat:
    """Controllo semplice termostato VDA via MODBUS RTU"""

    def __init__(self, port='/dev/ttyUSB0', slave_id=1,
                 baudrate=9600, timeout=1):
        """
        Inizializza connessione termostato

        Args:
            port: Porta seriale
            slave_id: ID MODBUS del termostato
            baudrate: Velocità comunicazione
            timeout: Timeout in secondi
        """
        self.instrument = minimalmodbus.Instrument(port, slave_id)
        self.instrument.serial.baudrate = baudrate
        self.instrument.serial.timeout = timeout

        # Settings comuni VDA (ipotesi)
        self.REGISTER_TEMP_CURRENT = 2
        self.REGISTER_SETPOINT = 3
        self.REGISTER_MODE = 4
        self.REGISTER_FAN_SPEED = 5

    def read_temperature(self):
        """
        Legge temperatura corrente

        Returns:
            Temperatura in °C (float)
        """
        try:
            # Legge registro, decodifica scaled x10
            value = self.instrument.read_register(
                self.REGISTER_TEMP_CURRENT,
                functioncode=3
            )
            return value / 10.0

        except Exception as e:
            print(f"❌ Error reading temperature: {e}")
            return None

    def read_setpoint(self):
        """
        Legge setpoint temperatura

        Returns:
            Setpoint in °C (float)
        """
        try:
            value = self.instrument.read_register(
                self.REGISTER_SETPOINT,
                functioncode=3
            )
            return value / 10.0

        except Exception as e:
            print(f"❌ Error reading setpoint: {e}")
            return None

    def set_setpoint(self, temp_celsius):
        """
        Imposta setpoint temperatura

        Args:
            temp_celsius: Temperatura desiderata in °C (float)

        Returns:
            True se successo
        """
        try:
            # Codifica temperatura scaled x10
            value = int(temp_celsius * 10)

            self.instrument.write_register(
                self.REGISTER_SETPOINT,
                value,
                functioncode=6
            )

            print(f"✅ Setpoint set to {temp_celsius}°C")
            return True

        except Exception as e:
            print(f"❌ Error setting setpoint: {e}")
            return False

    def read_mode(self):
        """
        Legge modalità operativa (Heat/Cool/Fan/Auto)

        Returns:
            Codice modalità (int) o None
        """
        try:
            return self.instrument.read_register(
                self.REGISTER_MODE,
                functioncode=3
            )

        except Exception as e:
            print(f"❌ Error reading mode: {e}")
            return None

    def set_mode(self, mode):
        """
        Imposta modalità operativa

        Args:
            mode: 1=Cool, 2=Heat, 3=Fan, 4=Auto (tipico)

        Returns:
            True se successo
        """
        try:
            self.instrument.write_register(
                self.REGISTER_MODE,
                mode,
                functioncode=6
            )

            mode_names = {1: 'Cool', 2: 'Heat', 3: 'Fan', 4: 'Auto'}
            print(f"✅ Mode set to {mode_names.get(mode, 'Unknown')}")
            return True

        except Exception as e:
            print(f"❌ Error setting mode: {e}")
            return False

    def get_status(self):
        """
        Legge stato completo termostato

        Returns:
            Dict con temperatura, setpoint, mode
        """
        return {
            'temperature': self.read_temperature(),
            'setpoint': self.read_setpoint(),
            'mode': self.read_mode()
        }


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

if __name__ == "__main__":
    # Connetti al termostato
    thermostat = VDAThermostat(
        port='/dev/ttyUSB0',
        slave_id=1,
        baudrate=9600
    )

    # Leggi stato
    print("📊 Current Status:")
    status = thermostat.get_status()
    print(f"   Temperature: {status['temperature']}°C")
    print(f"   Setpoint: {status['setpoint']}°C")
    print(f"   Mode: {status['mode']}")

    # Imposta temperatura 22.5°C
    thermostat.set_setpoint(22.5)

    # Verifica
    time.sleep(1)
    new_setpoint = thermostat.read_setpoint()
    print(f"\n✅ Verified: {new_setpoint}°C")
```

**Vantaggi MinimalModbus**:
- ✅ Sintassi più semplice
- ✅ Meno codice boilerplate
- ✅ Perfetto per casi d'uso semplici

**Quando usare PyModbus invece**:
- Necessario controllo granulare
- Operazioni batch (write multiple registers)
- Debugging avanzato
- MODBUS TCP oltre RTU

---

## PARTE 6: HARDWARE NECESSARIO

### 1. Convertitore RS485-USB

**Essenziale** per connettere PC al bus MODBUS RTU.

#### Opzione Professionale (Consigliata)

**Q-USB-485 (Qeed USA)** - ~$60

Features:
- ✅ **5 kV isolation** (protegge da surge elettrici)
- ✅ **FTDI chipset** (driver affidabili, long-term support)
- ✅ Auto-termination e biasing resistors
- ✅ Supporto Windows/Mac/Linux
- ✅ Industrial-grade (adatto hotel)

[Link: Qeed USA Q-USB-485](https://www.qeedusa.com/usb-to-modbus-rs485-q-usb-485.html)

#### Opzione Budget (Testing)

**WITMOTION USB to RS485** - ~$15 Amazon

Features:
- ✅ CH340 chipset (economico ma funzionale)
- ✅ Cavo 1m con terminazione
- ✅ Plug and play
- ⚠️ NO isolation (ok per testing, meno per produzione)

[Link: Amazon WITMOTION](https://www.amazon.com/WITMOTION-RS485-Converter-Terminated-Adapter/dp/B07VMFJ5Y3)

#### Opzione DIY (Advanced)

**Research Design Lab USB-RS485 Module** - ~$25

Features:
- ✅ Bi-directional
- ✅ Supporta fino a 32 slave devices
- ✅ 300 baud - 5 Mbaud
- ✅ Good for debugging

[Link: Research Design Lab](https://researchdesignlab.com/usb-to-rs485-converter-module.html)

### 2. Cablaggio RS-485

**Essentials**:
- 🔌 **Twisted pair cable** (Cat5e/Cat6 ok per brevi distanze)
- 🔩 **Terminal blocks** per connessioni
- ⚡ **Resistenze terminazione** 120Ω (se bus lungo >10m)

**Schema connessione**:
```
┌──────────────┐
│  USB-RS485   │
│  Converter   │
└──┬────────┬──┘
   │ A(+)   │ B(-)
   │        │
   ├────────┼──────┐ Twisted pair
   │        │      │
┌──┴────────┴───┐  │
│  VDA Device   │  │
│  (Termostato) │  │
└───────────────┘  │
                   │
            ┌──────▼──────┐
            │ 120Ω        │ (Terminazione se bus lungo)
            └─────────────┘
```

**Wire colors** (standard Cat5e):
- A(+) → Orange (pin 1-2)
- B(-) → Orange/White (pin 1-2)
- GND → Blue (pin 4-5) - opzionale ma raccomandato

### 3. Tools di Diagnostica (Opzionali ma Utili)

#### Logic Analyzer

Per debugging avanzato, capture raw RS-485 frames.

**Saleae Logic 8** - ~$400
- 8 canali digital
- Software eccellente
- Decodifica MODBUS nativa

**Alternative budget**: Logic analyzer cinesi ~$10 (funzionano per basic debug)

#### Multimetro

Per verificare:
- Voltaggio RS-485 (differential 1.5-5V tipico)
- Continuità cavi
- GND connesso correttamente

### 4. Setup Fisico Completo (What You Need to Buy)

| Item | Quantità | Costo | Link |
|------|----------|-------|------|
| **USB-RS485 Converter** | 1 | $15-60 | [Qeed USA](https://www.qeedusa.com/usb-to-modbus-rs485-q-usb-485.html) |
| **Twisted Pair Cable** | 5-10m | $5-10 | Cat5e locale |
| **Terminal Blocks** | 2-4 | $5 | Amazon |
| **120Ω Resistors** | 2 | $1 | Amazon/DigiKey |
| **Multimetro** (se non hai) | 1 | $20-50 | Amazon |
| **(Optional) Logic Analyzer** | 1 | $10-400 | Saleae / AliExpress |

**TOTAL COST**: $50-150 (senza logic analyzer)

### 5. Setup Procedure

**Step 1**: Connetti USB-RS485 Converter
```bash
# Linux: Check device name
dmesg | grep tty
# Output: ttyUSB0 (or similar)

# Windows: Check Device Manager → COM ports
# Output: COM3 (or similar)

# Test connessione
python -m serial.tools.list_ports
```

**Step 2**: Identifica wiring VDA device

Trova terminali RS-485 sul termostato VDA:
- Tipicamente: A, B, GND (o +, -, G)
- Consulta manuale (se disponibile) o cerca silk screen su PCB

**Step 3**: Cablaggio

```
USB-RS485 Converter    →    VDA Thermostat
─────────────────────────────────────────
A(+)                   →    A / + / Data+
B(-)                   →    B / - / Data-
GND (optional)         →    GND / G
```

**Step 4**: Verifica connessione

```bash
# Test con mbpoll (Linux)
mbpoll -a 1 -r 0 -c 1 -t 4 /dev/ttyUSB0

# Se risponde: SUCCESS!
# Se timeout: Check wiring, baudrate, slave ID
```

**Step 5**: Python scan

```bash
python vda_scanner.py
# Esegui example_1_discover_devices()
```

---

## PARTE 7: REGISTER MAP TIPICI TERMOSTATI

Basato su ricerca di termostati MODBUS hotel standard.

### Honeywell / ABB / Standard Thermostats

| Register | Function | Data Type | Range | Notes |
|----------|----------|-----------|-------|-------|
| **0** | Device ID / Room number | UInt16 | 0-9999 | Identificativo camera |
| **1** | Device status | UInt16 | 0-255 | Bitmask (online, error, etc) |
| **2** | Temperature current | Int16 (x10) | 160-280 | 16.0-28.0°C |
| **3** | Setpoint temperature | Int16 (x10) | 160-280 | Target temp |
| **4** | Operating mode | Enum | 0-4 | 0=Off, 1=Cool, 2=Heat, 3=Fan, 4=Auto |
| **5** | Fan speed | Enum | 0-3 | 0=High, 1=Med, 2=Low, 3=Auto |
| **6** | Setpoint upper limit | Int16 (x10) | 50-350 | Config limite max |
| **7** | Setpoint lower limit | Int16 (x10) | 50-350 | Config limite min |
| **10** | Valve position | UInt8 | 0-100 | % apertura valvola (heating) |
| **11** | Window open status | Bool | 0-1 | 0=Closed, 1=Open |
| **12** | Occupancy sensor | Bool | 0-1 | 0=Vacant, 1=Occupied |
| **13** | Door open status | Bool | 0-1 | 0=Closed, 1=Open |
| **20** | DND status | Bool | 0-1 | Do Not Disturb flag |
| **21** | MUR status | Bool | 0-1 | Make Up Room request |
| **30** | Energy saving mode | Bool | 0-1 | ECO mode enable |
| **31** | Night mode | Bool | 0-1 | Reduced temperature night |
| **60** | Display mode | Enum | 0-2 | 0=Temp, 1=Setpoint, 2=Humidity |

### Operating Mode Encoding (Tipico)

```python
MODE_OFF = 0
MODE_COOL = 1
MODE_HEAT = 2
MODE_FAN = 3
MODE_AUTO = 4

mode_names = {
    0: 'Off',
    1: 'Cool',
    2: 'Heat',
    3: 'Fan Only',
    4: 'Auto'
}
```

### Fan Speed Encoding

```python
FAN_HIGH = 0
FAN_MEDIUM = 1
FAN_LOW = 2
FAN_AUTO = 3

fan_names = {
    0: 'High',
    1: 'Medium',
    2: 'Low',
    3: 'Auto'
}
```

### Temperature Scaling

**Esempio**: Register value = 225

```python
# Decode
temperature_celsius = value / 10.0
# Result: 22.5°C

# Encode
value = int(22.5 * 10)
# Result: 225
```

**Alternative scaling**: x100 per più precisione (es. 2250 = 22.50°C)

### Bitmask Status Example

Register 1 = Device Status (16-bit bitmask)

```python
STATUS_ONLINE       = 0b0000000000000001  # Bit 0
STATUS_ERROR        = 0b0000000000000010  # Bit 1
STATUS_HEATING      = 0b0000000000000100  # Bit 2
STATUS_COOLING      = 0b0000000000001000  # Bit 3
STATUS_FAN_RUNNING  = 0b0000000000010000  # Bit 4

def decode_status(value):
    """Decodifica bitmask status"""
    return {
        'online': bool(value & STATUS_ONLINE),
        'error': bool(value & STATUS_ERROR),
        'heating': bool(value & STATUS_HEATING),
        'cooling': bool(value & STATUS_COOLING),
        'fan_running': bool(value & STATUS_FAN_RUNNING)
    }

# Esempio
status_value = 0b00010101  # = 21 decimal
status = decode_status(status_value)
# {'online': True, 'error': False, 'heating': True,
#  'cooling': False, 'fan_running': True}
```

---

*Continua in PARTE 3...*

---

## FONTI PARTE 2

### Hardware RS485-USB
- [Qeed USA Q-USB-485](https://www.qeedusa.com/usb-to-modbus-rs485-q-usb-485.html)
- [Amazon WITMOTION USB RS485](https://www.amazon.com/WITMOTION-RS485-Converter-Terminated-Adapter/dp/B07VMFJ5Y3)
- [Research Design Lab USB-RS485](https://researchdesignlab.com/usb-to-rs485-converter-module.html)
- [US Converters XS885](https://www.usconverters.com/usb-rs485-converter-xs885)

### PyModbus Documentation
- [PyModbus Read Holding Registers Guide](https://www.pymodbus.org/docs/reading-registers)
- [PyModbus Writing Registers](https://www.pymodbus.org/docs/writing-registers)
- [PyModbus Quick Start](https://www.pymodbus.org/docs/quick-start)
- [PyModbus Examples](https://pymodbus.readthedocs.io/en/dev/source/examples.html)

### MinimalModbus
- [MinimalModbus API Documentation](https://minimalmodbus.readthedocs.io/en/stable/apiminimalmodbus.html)
- [MinimalModbus PyPI](https://pypi.org/project/minimalmodbus/)

### Thermostat MODBUS Registers
- [Johnson Controls T9800 Modbus Data Table](https://docs.johnsoncontrols.com/bas/api/khub/documents/509RgEzOcLWz9_GXP8Bnow/content)
- [ABB BR Series Thermostat Modbus Protocol](https://library.e.abb.com/public/4605e32dd15644d3a667db00323071a3/ABB+ON+OFF+version+BS+Thermostat+Universal+interface+Protocol+(Modbus)+V1.0.pdf)
- [Honeywell TR100 Modbus Integration Guide](https://prod-edam.honeywell.com/content/dam/honeywell-edam/hbt/en-us/documents/manuals-and-guides/installation-guides/tr-100/hon-ba-bms-tr100-modbus-integration-guide-31-00748-drop-3-d1-3.pdf)

---

*Cervella Researcher - 2026-01-15*
*"Studiare prima di agire - sempre!"*
