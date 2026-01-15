# GUIDA PRATICA: Sniffing e Reverse Engineering MODBUS RS485

> **Obiettivo**: Intercettare traffico MODBUS RTU su bus RS485 del sistema VDA senza documentazione
> **Ricerca**: 15 Gennaio 2026
> **Progetto**: Miracollo - Sistema Hotel VDA

---

## 📋 INDICE

1. [Hardware Necessario](#hardware-necessario)
2. [Software Tools](#software-tools)
3. [Setup Fisico](#setup-fisico)
4. [Cattura Traffico](#cattura-traffico)
5. [Tecniche Reverse Engineering](#tecniche-reverse-engineering)
6. [Precauzioni e Sicurezza](#precauzioni-e-sicurezza)

---

## 🔌 HARDWARE NECESSARIO

### Convertitore USB-RS485 Raccomandato

**OPZIONE 1: WITMOTION USB to RS485 Modbus RTU Converter (Raccomandato)**
- Chip: CH340
- Connessione: 4-way female socket (A, B, VCC, GND)
- Lunghezza cavo: 1m
- Compatibilità: Windows 10/8/7, Linux, Mac OS
- Dove: Amazon UK/US (~€15-25)
- PRO: Economico, plug-and-play, funziona con software gratuiti
- CONTRO: Driver CH340 richiesto

**OPZIONE 2: USB-RS485 con chip FTDI**
- Chip: FTDI (più affidabile)
- Supporto: 3.3V/5V
- Terminazione: Resistore 120Ω incluso
- Dove: Amazon (~€25-35)
- PRO: Driver nativi su molti OS, più stabile
- CONTRO: Più costoso

**OPZIONE 3: Stratus Engineering Versa-Tap (Professionale)**
- Sniffer hardware dedicato
- Supporto RS485/RS422
- Isolamento elettrico
- Dove: Vendor specializzati (~€200+)
- PRO: Non influenza il bus, professionale
- CONTRO: Costo elevato

### Hardware DIY (Avanzato)

Se hai esperienza con elettronica:
- Modulo MAX485/MAX3485
- Arduino/ESP32
- Resistori terminazione 120Ω

**⚠️ Per il nostro caso: WITMOTION o FTDI (budget-friendly e sufficiente!)**

---

## 💻 SOFTWARE TOOLS

### 1. ModbusSniffer (⭐ RACCOMANDATO per iniziare)

**Caratteristiche:**
- GUI cross-platform (Windows/Linux/Mac)
- Real-time monitoring traffico Modbus RTU
- Funziona con convertitori USB-RS485 economici
- Visualizzazione pacchetti in tempo reale
- Export dati per analisi

**Download:**
- GitHub: https://github.com/niwciu/ModbusSniffer
- Hackaday: https://hackaday.io/project/203288-modbussniffer

**Setup:**
```bash
1. Scarica e installa ModbusSniffer
2. Collega USB-RS485
3. Seleziona COM port
4. Configura baud rate (9600, 19200, 38400 comuni)
5. Start monitoring!
```

**PRO:**
- GUI semplice e intuitiva
- Non richiede configurazione complessa
- Ottimo per iniziare

### 2. Wireshark con PCAP Serial

**Caratteristiche:**
- Analisi approfondita protocollo
- Filtri avanzati
- Export e comparazione sessioni
- Decodifica MODBUS nativa

**Setup:**

**Tool helper: SerialPCAP**
```bash
# GitHub: https://github.com/j123b567/SerialPCAP
# Cattura traffico seriale → file PCAP

1. Installa SerialPCAP
2. Configura COM port e baud rate
3. Genera PCAP file
4. Apri con Wireshark
```

**Configurazione Wireshark per MODBUS RTU:**
1. Installa Wireshark
2. Edit → Preferences → Protocols → DLT_USER
3. Aggiungi encapsulation table:
   - DLT: User 0 (147)
   - Payload protocol: modbus
4. Capture → Options → seleziona porta serial adapter

**Tool Python per Wireshark (Linux/Mac):**
```bash
# GitHub: https://github.com/ddmesh/modbus-rs485-wireshark-monitor
# Crea FIFO pipe tra serial port e Wireshark

git clone https://github.com/ddmesh/modbus-rs485-wireshark-monitor
python3 modbus_monitor.py --port /dev/ttyUSB0 --baud 9600
# In Wireshark: cattura da named pipe
```

**PRO:**
- Potentissimo per analisi
- Filtri sofisticati
- Comparazione sessioni

**CONTRO:**
- Curva apprendimento più alta
- Setup più complesso

### 3. QModMaster (Testing e Sniffer)

**Caratteristiche:**
- Open source (LGPL)
- GUI Qt-based
- Modbus master simulator + **bus monitor**
- Supporto RTU e TCP
- Libreria libmodbus

**Download:**
- SourceForge: https://sourceforge.net/projects/qmodmaster/
- GitHub: https://github.com/zhanglongqi/qModMaster

**Setup:**
```bash
1. Scarica Windows binary (no install needed) o compila da source
2. Run QModMaster
3. Connection → Setup → Serial RTU
4. Configure: COM port, baud, parity, stop bits
5. Bus Monitor tab → Start monitoring
```

**PRO:**
- Open source e gratuito
- Bus monitor integrato
- Può anche fare polling attivo (utile per test)

**CONTRO:**
- GUI un po' datata
- Meno user-friendly di ModbusSniffer

### 4. Serial Port Monitor (Commerciale)

**HHD Software Serial Port Monitor:**
- Supporto MODBUS nativo
- Non-intrusive sniffer
- Windows only
- Trial gratuito, poi ~€60

**Free Serial Analyzer:**
- Alternativa gratuita
- Windows only
- Funzionalità base sufficienti

### 5. Altri Tool Utili

**modbus-sniffer (CLI):**
```bash
# GitHub: https://github.com/alerighi/modbus-sniffer
# Cattura pacchetti → .pcap per Wireshark

./modbus-sniffer /dev/ttyUSB0 -b 9600 -o output.pcap
# Poi: wireshark output.pcap
```

**CAS Modbus Scanner (Commerciale):**
- Auto-discovery dispositivi
- Scansione registri automatica
- ~€150+
- Ottimo per uso professionale

---

## 🔧 SETUP FISICO - COLLEGAMENTO AL BUS

### ARCHITETTURA RS485

```
Bus RS485 esistente (2-wire half-duplex):

[VDA Master] ←→ [Device 1] ←→ [Device 2] ←→ ...
     |              |             |
   [120Ω]                      [120Ω]  ← Terminazione ai capi
```

### MODALITÀ SNIFFER: Parallel Tap (Non-Intrusivo)

**⚠️ REGOLA D'ORO: Collega in PARALLELO, NON in serie!**

```
Bus RS485:
    A (Data+) ─────●─────●─────●─────●─────
                   │     │     │     │
                 [VDA] [Dev1] [Dev2] [SNIFFER]
                   │     │     │     │
    B (Data-) ─────●─────●─────●─────●─────
                   │                 │
                  [GND]            [GND]
```

### SCHEMA COLLEGAMENTO FISICO

**Per convertitore USB-RS485 (4 pin):**

| Pin Convertitore | Collegamento | Note |
|------------------|--------------|------|
| **A / D+ / TX+** | Bus RS485 A (Data+) | Parallelo sul bus |
| **B / D- / TX-** | Bus RS485 B (Data-) | Parallelo sul bus |
| **GND** | Ground bus (se disponibile) | Opzionale ma raccomandato |
| **VCC** | NON collegare | Alimentazione via USB |

**IMPORTANTE - Configurazione Sniffer Mode:**

Molti convertitori hanno jumper/switch per:
- **RE (Receiver Enable)**: Collegare a GND → Receiver SEMPRE attivo
- **DE (Driver Enable)**: Collegare a GND → Transmitter DISABILITATO

Questo mette l'adapter in **"listen-only mode"** (solo ricezione, non trasmette).

### PROCEDURA COLLEGAMENTO STEP-BY-STEP

```
1. SPEGNERE il sistema VDA (se possibile)
   ⚠️ Se non puoi spegnere: procedi con cautela!

2. IDENTIFICARE i cavi RS485:
   - Solitamente coppia twisted pair
   - Colori comuni: Rosso/Nero, Arancio/Blu, Verde/Bianco
   - Usa multimetro per confermare polarità (A=+, B=-)

3. COLLEGARE lo sniffer:
   - Strip piccola sezione cavo (NON tagliare!)
   - O usa connettori "vampire tap" (non invasivi)
   - Collega A → A, B → B in parallelo
   - GND se disponibile

4. VERIFICARE terminazione:
   - Lo sniffer NON deve avere resistore 120Ω attivo!
   - Solo i dispositivi ai CAPI del bus hanno terminazione
   - Se il tuo adapter ha jumper, RIMUOVI la terminazione

5. RIACCENDERE sistema

6. TEST:
   - Se il sistema continua a funzionare = OK!
   - Se errori comunicazione = Verifica connessioni/terminazione
```

### TOOLS FISICI UTILI

- **Multimetro**: Verificare polarità e continuità
- **Wire stripper**: Spellare cavi senza danneggiarli
- **Connettori a morsetto**: Collegamento non-permanente
- **Vampire tap connectors**: Perforare isolante senza tagliare cavo
- **Cavo twisted pair**: Per estendere connessioni

---

## 📡 CATTURA TRAFFICO - PROCEDURA

### STEP 1: Configurazione Seriale

**Parametri comuni MODBUS RTU:**

| Parametro | Valori Tipici | Come Trovare |
|-----------|---------------|--------------|
| Baud Rate | 9600, 19200, 38400, 115200 | Prova tutti finché vedi traffico |
| Data Bits | 8 | Standard MODBUS |
| Parity | None, Even | Prova entrambi |
| Stop Bits | 1 | Standard |

**Auto-detection (se il software lo supporta):**
- CAS Modbus Scanner: Auto-detect baud rate
- Serial Port Monitor: Baud rate analyzer

**Metodo manuale:**
```
1. Inizia con 9600-8-N-1 (più comune)
2. Se vedi garbage → prova altri baud rate
3. Se vedi frame corrotti → prova parity Even
```

### STEP 2: Avvio Cattura

**Con ModbusSniffer:**
```
1. Start → Select COM port
2. Configure: Baud 9600, 8-N-1
3. Click "Start"
4. Osserva pacchetti in real-time
```

**Con Wireshark + SerialPCAP:**
```bash
# Terminal 1: Cattura seriale
serialpcap /dev/ttyUSB0 9600 > capture.pcap

# Terminal 2: Wireshark
wireshark capture.pcap
```

**Con modbus-sniffer (CLI):**
```bash
./modbus-sniffer /dev/ttyUSB0 -b 9600 -l -o hotel_vda.pcap
# -l = low latency mode (riduce 16ms → 1ms)
```

### STEP 3: Generare Traffico (Trigger Events)

**⚠️ FONDAMENTALE per reverse engineering!**

Devi **correlare eventi fisici con pacchetti MODBUS**.

**Esempi:**
```
1. ACCENDI luce camera 101
   → Osserva quali pacchetti vengono inviati
   → Annota Slave ID, Function Code, Register Address, Valore

2. SPEGNI luce camera 101
   → Confronta con pacchetto precedente
   → Differential analysis: cosa è cambiato?

3. REGOLA temperatura camera 102
   → Identifica registri termostato
   → Vedi pattern scrittura setpoint

4. APRI/CHIUDI porta
   → Identifica sensori porta
   → Registri stato digitale

5. ATTIVA allarme
   → Pacchetti emergency
   → Priorità comunicazione
```

**STRATEGIA:**
```
1. BASELINE: Cattura traffico "idle" (10 minuti)
   → Identifica polling periodico
   → Quali slave, quali registri vengono letti sempre

2. SINGLE EVENT: Cambia UNA cosa alla volta
   → Confronta con baseline
   → Isola SOLO i pacchetti cambiati

3. DOCUMENTARE: Crea tabella correlazioni
   | Azione Fisica | Slave ID | Func | Register | Value | Note |
   |---------------|----------|------|----------|-------|------|
   | Luce 101 ON   | 0x01     | 0x05 | 0x0020   | 0xFF00| Coil |
   | Luce 101 OFF  | 0x01     | 0x05 | 0x0020   | 0x0000| Coil |
```

### STEP 4: Filtrare e Analizzare

**Wireshark Filters:**
```
# Solo MODBUS
modbus

# Specifico Slave ID
modbus.unit_id == 1

# Solo scritture
modbus.func_code == 5 || modbus.func_code == 6 || modbus.func_code == 15 || modbus.func_code == 16

# Solo letture
modbus.func_code == 1 || modbus.func_code == 2 || modbus.func_code == 3 || modbus.func_code == 4

# Errori
modbus.exception_code

# Specifico registro
modbus.reference_num == 32
```

**ModbusSniffer:**
- Usa filtri GUI per Slave ID
- Export CSV per analisi Excel/Python

---

## 🔍 TECNICHE REVERSE ENGINEERING

### 1. DIFFERENTIAL ANALYSIS (⭐ Tecnica Primaria)

**Principio:**
> "Cambia UNA variabile fisica → Osserva COSA cambia nel traffico MODBUS"

**Procedura:**
```
1. CATTURA BASELINE (stato iniziale)
   - Registra tutti i pacchetti per 5-10 min
   - Identifica pattern ciclici (polling)

2. SINGOLA MODIFICA
   - Cambia UNA variabile (es: accendi luce)
   - CATTURA nuovo traffico

3. CONFRONTO
   - Tool: Wireshark "Compare" feature
   - O export entrambi → diff in Python/Excel

4. ISOLAMENTO
   - Identifica pacchetti SOLO nella seconda cattura
   - Questi sono correlati alla tua azione!

5. VALIDAZIONE
   - Ripeti l'azione → vedi stesso pattern?
   - Prova azione opposta (spegni luce) → vedi inversione?
```

**Esempio Pratico:**

```
BASELINE (Luce OFF):
[Polling periodico ogni 1s]
Master → Slave 0x01, Func 0x03 (Read Holding), Reg 0x0020, Qty 1
Slave → Master, Value: 0x0000

EVENTO: Utente accende luce

DOPO EVENTO:
Master → Slave 0x01, Func 0x05 (Write Single Coil), Coil 0x0020, Value 0xFF00
Slave → Master, Echo (success)

[Nuovo polling:]
Master → Slave 0x01, Func 0x03, Reg 0x0020, Qty 1
Slave → Master, Value: 0x0001  ← CAMBIATO!

CONCLUSIONE:
- Registro 0x0020 controlla luce camera 101
- Func 0x05 = comando ON/OFF
- Func 0x03 = read stato
- 0xFF00 = ON, 0x0000 = OFF
```

### 2. PATTERN RECOGNITION

**Polling Patterns:**
```
Sistema tipico fa polling ciclico:
- Ogni 1-5 secondi
- Legge stato sensori (coils, inputs)
- Legge valori (temperatura, setpoint)

IDENTIFICA:
- Quali slave vengono interrogati?
- Con quale frequenza?
- Quali registri?
→ Questi sono i registri "importanti"!
```

**Write Patterns:**
```
Scritture sono EVENT-DRIVEN:
- Utente cambia qualcosa → Write command
- Sistema risponde a allarme → Write command

CERCA:
- Func 0x05 (Write Single Coil) → ON/OFF
- Func 0x06 (Write Single Register) → Valori (temp, setpoint)
- Func 0x0F/0x10 (Write Multiple) → Configurazione bulk
```

### 3. REGISTER MAPPING INCREMENTALE

**Obiettivo:** Costruire mappa completa registri

**Metodo Sicuro (Non-Invasivo):**
```
1. OSSERVA SOLO (Passive)
   - Non inviare comandi!
   - Registra tutto il traffico esistente
   - Costruisci tabella da traffico osservato

2. CORRELAZIONE EVENTI
   - Triggera eventi sul sistema (usa interfaccia esistente)
   - Osserva quali registri cambiano
   - Documenta correlazioni

3. TABELLA REGISTER MAP
   | Register | Type | R/W | Descrizione | Valori | Slave |
   |----------|------|-----|-------------|--------|-------|
   | 0x0000   | Coil | R/W | Luce Camera 101 | 0/1 | 0x01 |
   | 0x0001   | Coil | R/W | Luce Camera 102 | 0/1 | 0x01 |
   | 0x0100   | Hold | R/W | Temp Setpoint 101 | 15-30°C | 0x02 |
   | 0x0101   | Input| R   | Temp Attuale 101 | 0-50°C | 0x02 |
```

**Metodo Attivo (⚠️ Rischio - Solo ambiente test!):**

**ATTENZIONE:** Scansione attiva può:
- Causare DOS su dispositivi con risorse limitate
- Attivare comandi indesiderati
- Danneggiare sistema se scrivi su registri critici

**Se proprio necessario:**
```
1. USA CAS Modbus Scanner o QModMaster
2. INIZIA con READ-ONLY:
   - Func 0x03 (Read Holding Registers)
   - Func 0x04 (Read Input Registers)
   - Func 0x01 (Read Coils)
   - Func 0x02 (Read Discrete Inputs)

3. RANGE LIMITATO:
   - Non scansionare 0x0000-0xFFFF!
   - Inizia con range comuni: 0x0000-0x00FF
   - O range documentati in standard MODBUS

4. THROTTLE:
   - Delay tra richieste (100-500ms)
   - Non sovraccaricare il bus

5. LOGGING:
   - Registra TUTTE le risposte
   - Exception code 0x02 = "Illegal Data Address" → registro non esiste
   - Exception code 0x01 = "Illegal Function" → funzione non supportata
```

**Tool per Scanning:**
```bash
# ModBus Python brute-force scanner
# GitHub: https://github.com/nallamuthu/ModBus

python modbus_scanner.py --host /dev/ttyUSB0 --slave 1 --start 0 --end 100

# CAS Modbus Scanner (GUI)
# Auto-scan con throttling intelligente
```

### 4. DOCUMENTAZIONE STANDARD MODBUS

**Function Codes Reference:**

| Code | Nome | Descrizione | Uso |
|------|------|-------------|-----|
| 0x01 | Read Coils | Lettura bit digitali (R/W) | Luci, relè |
| 0x02 | Read Discrete Inputs | Lettura bit digitali (R only) | Sensori binari |
| 0x03 | Read Holding Registers | Lettura registri 16-bit (R/W) | Setpoint, config |
| 0x04 | Read Input Registers | Lettura registri 16-bit (R only) | Sensori analogici |
| 0x05 | Write Single Coil | Scrittura singolo bit | ON/OFF comando |
| 0x06 | Write Single Register | Scrittura singolo registro | Setpoint |
| 0x0F | Write Multiple Coils | Scrittura multipla bit | Batch commands |
| 0x10 | Write Multiple Registers | Scrittura multipli registri | Configurazione |

**Exception Codes:**

| Code | Significato |
|------|-------------|
| 0x01 | Illegal Function (funzione non supportata) |
| 0x02 | Illegal Data Address (registro non esiste) |
| 0x03 | Illegal Data Value (valore non valido) |
| 0x04 | Slave Device Failure (errore hardware) |

### 5. ANALISI DATI CATTURATI

**Script Python per Analisi PCAP:**

```python
from scapy.all import *
from scapy.contrib.modbus import *

# Leggi PCAP
packets = rdpcap('hotel_vda.pcap')

# Filtra MODBUS
modbus_packets = [p for p in packets if ModbusADURequest in p or ModbusADUResponse in p]

# Estrai statistiche
slave_ids = {}
registers = {}

for pkt in modbus_packets:
    if ModbusADURequest in pkt:
        req = pkt[ModbusADURequest]
        slave_id = req.unitId
        func_code = req.funcCode

        # Conta per slave
        if slave_id not in slave_ids:
            slave_ids[slave_id] = 0
        slave_ids[slave_id] += 1

        # Estrai registri letti/scritti
        if hasattr(req, 'startAddr'):
            reg = req.startAddr
            if reg not in registers:
                registers[reg] = []
            registers[reg].append({
                'func': func_code,
                'slave': slave_id,
                'timestamp': pkt.time
            })

print("Slave IDs trovati:", slave_ids)
print("Registri acceduti:", sorted(registers.keys()))
```

---

## ⚠️ PRECAUZIONI E SICUREZZA

### 1. NON INTERROMPERE IL BUS

**❌ MAI fare:**
- Tagliare cavi per inserire sniffer in serie
- Rimuovere terminazione dai dispositivi esistenti
- Aggiungere terminazione allo sniffer se non è ai capi

**✅ SEMPRE fare:**
- Collegamento PARALLELO (tap)
- Mantenere terminazione solo ai capi bus
- Modalità listen-only (RE=GND, DE=GND)

### 2. ISOLAMENTO ELETTRICO

**Considera adapter con isolamento galvanico se:**
- Dispositivi su diverse alimentazioni
- Presenza di ground loops
- Ambiente industriale rumoroso

**Adapter isolati:**
- USB-RS485 con isolamento ottico
- Costo: ~€40-60
- PRO: Protegge PC e bus da surge/noise

### 3. BACKUP E RECOVERY

**PRIMA di ogni test:**
```
1. BACKUP configurazione VDA esistente
   - Se possibile, esporta settings
   - Documenta stato attuale sistema

2. PIANO di ROLLBACK
   - Come ripristinare se qualcosa va storto?
   - Contatto tecnico disponibile?

3. AMBIENTE CONTROLLATO
   - Testa fuori orario ospiti (notte)
   - O in camera non occupata
   - Avvisa staff hotel del test
```

### 4. SCANSIONE SICURA vs AGGRESSIVA

**Approccio SAFE (Raccomandato per VDA produzione):**
```
✅ SOLO passive sniffing
✅ Trigger eventi tramite interfaccia esistente
✅ ZERO comandi diretti al bus
✅ Documentare solo traffico osservato
✅ Tempo: Più lungo, ma ZERO rischio
```

**Approccio AGGRESSIVO (Solo ambiente test!):**
```
⚠️ Scansione attiva registri
⚠️ Invio comandi di test
⚠️ Brute-force register discovery
⚠️ Rischio: DOS, comandi indesiderati
⚠️ SOLO se hai sistema clone o ambiente test!
```

**Per sistema VDA LIVE in hotel:**
```
RACCOMANDAZIONE: Approccio 100% PASSIVO

1. Installa sniffer in listen-only
2. Cattura traffico normale per giorni/settimane
3. Correla eventi naturali (ospiti usano camere)
4. Costruisci mappa registri SENZA mai scrivere
5. Testa SOLO in ambiente clone (se possibile)
```

### 5. DOCUMENTAZIONE DETTAGLIATA

**Mentre fai reverse engineering:**

```markdown
## Sessione Sniffing: 15 Gen 2026 - Hotel XYZ - Camera 101

**Setup:**
- Convertitore: WITMOTION USB-RS485
- Baud: 9600-8-N-1
- Software: ModbusSniffer v2.1
- Durata: 10:30-12:00

**Eventi Testati:**
1. 10:35 - Accensione luce camera
   - Pacchetto: Master→Slave 0x01, Func 0x05, Coil 0x0020, Val 0xFF00
   - Risultato: Luce accesa ✓

2. 10:40 - Regolazione temperatura 22°C
   - Pacchetto: Master→Slave 0x02, Func 0x06, Reg 0x0100, Val 0x00DC (220 = 22.0°C)
   - Risultato: Display mostra 22°C ✓

**Registri Identificati:**
| Reg | Slave | Func | Tipo | Descrizione | Range |
|-----|-------|------|------|-------------|-------|
| 0x0020 | 0x01 | 0x05 | Coil | Luce Principale | 0/1 |
| 0x0100 | 0x02 | 0x06 | Hold | Setpoint Temp | 150-300 (15-30°C) |

**Note:**
- Sistema risponde velocemente (<100ms)
- Nessun errore durante test
- Temperatura in decimi di grado (220 = 22.0°C)
```

### 6. COMPLIANCE E LEGALITÀ

**⚠️ Aspetti Legali:**

```
✅ CONSENTITO:
- Sniffing passivo su impianto di proprietà
- Reverse engineering per interoperabilità
- Documentazione per manutenzione

❌ NON CONSENTITO (senza autorizzazione):
- Intercettare comunicazioni di terzi
- Reverse engineering per violazione IP
- Condivisione codici proprietari

RACCOMANDAZIONE:
- Ottieni permesso scritto dal proprietario hotel
- Non pubblicare informazioni proprietarie VDA
- Usa conoscenza SOLO per Miracollo integration
```

---

## 🎯 CHECKLIST OPERATIVA

### Pre-Sniffing

```
[ ] Hardware acquistato e testato
[ ] Software installato e configurato
[ ] Driver USB-RS485 funzionanti
[ ] Documentazione sistema VDA raccolta (se disponibile)
[ ] Permesso proprietario hotel ottenuto
[ ] Piano backup/rollback pronto
[ ] Staff hotel informato
```

### Durante Sniffing

```
[ ] Collegamento parallelo verificato (bus funziona)
[ ] Listen-only mode attivo (non trasmette)
[ ] Cattura traffico funzionante (vedo pacchetti)
[ ] Baud rate corretto identificato
[ ] Eventi triggati e correlati
[ ] Documentazione in tempo reale
[ ] Nessun impatto su sistema esistente
```

### Post-Sniffing

```
[ ] File PCAP salvati e backuppati
[ ] Register map documentata
[ ] Correlazioni eventi-registri verificate
[ ] Test validazione in ambiente clone (se possibile)
[ ] Hardware sniffer rimosso
[ ] Sistema VDA funzionante normalmente
[ ] Documentazione completa archiviata
```

---

## 📚 RISORSE E RIFERIMENTI

### Hardware

- [WITMOTION USB-RS485 Converter - Amazon](https://www.amazon.com/WITMOTION-RS485-Converter-Terminated-Adapter/dp/B07VMFJ5Y3)
- [USB-RS485 FTDI Chip - Amazon](https://www.amazon.com/RS485-Converter-Adapter-Windows-Supported/dp/B07797T9HC)
- [Stratus Engineering Versa-Tap](https://stratusengineering.com/rs422rs483-communication-topologies-versa-tap-rs422rs485-sniffer/)

### Software Open Source

- [ModbusSniffer - GitHub](https://github.com/niwciu/ModbusSniffer)
- [ModbusSniffer - Hackaday](https://hackaday.io/project/203288-modbussniffer)
- [QModMaster - SourceForge](https://sourceforge.net/projects/qmodmaster/)
- [QModMaster - GitHub](https://github.com/zhanglongqi/qModMaster)
- [modbus-sniffer - GitHub](https://github.com/alerighi/modbus-sniffer)
- [SerialPCAP - GitHub](https://github.com/j123b567/SerialPCAP)
- [modbus-rs485-wireshark-monitor - GitHub](https://github.com/ddmesh/modbus-rs485-wireshark-monitor)

### Documentazione Tecnica

- [RS485 Sniffer - Blog Post](https://jheyman.github.io/blog/pages/RS485Sniffer/)
- [Correct Cabling Modbus RS485](https://electrical-engineering-portal.com/correct-cabling-modbus-rs485)
- [RS485 Wiring Best Practices](https://help.ekmmetering.com/support/solutions/articles/6000058103-rs485-wiring-how-to-best-practices)
- [How to Configure RS-422/RS-485 Networks](https://www.sealevel.com/how-to-properly-configure-and-wire-rs-422-and-rs-485-networks)

### Wireshark e Analisi

- [Wireshark Modbus RTU Capture - Ask Wireshark](https://ask.wireshark.org/question/12740/capturing-modbus-rtu-traffic-with-a-usb-to-rs-485-converter/)
- [Wireshark for Modbus RTU - ABB Technical Note](https://library.e.abb.com/public/053acd5e47a04d938e15537a5d253e74/Technical_Note_179_WiresharkForModbusRTU.pdf)

### Reverse Engineering

- [Quick Way to Reverse Engineer Modbus - EEVBlog](https://www.eevblog.com/forum/beginners/quick-way-to-reverse-engineer-modbus/)
- [Examining Modbus Through Offensive Security Lens](https://redbotsecurity.com/examining-the-modbus-protocol/)

### Tools Commerciali

- [CAS Modbus Scanner](https://store.chipkin.com/products/cas-modbus-scanner-modbus-tcp-and-rtu-network-discovery-tool)
- [Serial Port Monitor - HHD Software](https://hhdsoftware.com/serial-port-monitor)
- [Modbus Scanner - Virtual Serial Port](https://www.virtual-serial-port.org/article/modbus-scanner/)

---

## 🎬 PROSSIMI STEP PER MIRACOLLO

**Dopo aver completato reverse engineering VDA:**

1. **Validazione Mappa Registri**
   - Testare TUTTI i registri identificati
   - Verificare R/W permissions
   - Documentare range valori validi

2. **Protocollo Gateway**
   - Definire API Miracollo ↔ MODBUS RTU
   - Mapping comandi user → registri MODBUS
   - Error handling e retry logic

3. **Implementazione Driver**
   - Libreria Python modbus-tk o pymodbus
   - Gateway service in FastAPI
   - WebSocket per real-time updates

4. **Testing Ambiente Clone**
   - Setup banco test con PLC/simulatore MODBUS
   - Replicare register map VDA
   - Test stress e edge cases

5. **Deployment Produzione**
   - Hardware gateway dedicato (Raspberry Pi?)
   - Monitoring e logging
   - Fallback sistema VDA originale

---

## ✅ CONCLUSIONI

**Setup Raccomandato per Miracollo/VDA:**

```
HARDWARE:
- WITMOTION USB-RS485 (~€20) - budget-friendly, funzionale
- O FTDI-based (~€30) - più stabile

SOFTWARE:
- ModbusSniffer - Per monitoring iniziale (GUI semplice)
- Wireshark + SerialPCAP - Per analisi approfondita
- QModMaster - Per test attivi (ambiente clone)

APPROCCIO:
- 100% PASSIVO su sistema VDA live
- Sniffing prolungato (giorni/settimane)
- Differential analysis per correlazioni
- Testing attivo SOLO su ambiente clone

TIMELINE:
- Setup hardware: 1 giorno
- Cattura baseline: 1-2 settimane
- Analisi e mapping: 1-2 settimane
- Validazione: 1 settimana
- TOTALE: ~1 mese per register map completa
```

**Questa guida ci permette di fare reverse engineering SICURO del sistema VDA senza documentazione!**

---

*Guida compilata da Cervella Researcher - 15 Gennaio 2026*
*Progetto: Miracollo - Integrazione VDA Hotel*
*"Studiare prima di agire - i player grossi hanno già risolto questi problemi!"* 🔬
