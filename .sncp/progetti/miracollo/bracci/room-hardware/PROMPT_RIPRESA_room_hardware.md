# PROMPT RIPRESA - Room Hardware

> **Ultimo aggiornamento:** 22 Gennaio 2026 - Sessione 311
> **Braccio 3 dell'ecosistema Miracollo**

---

## STATO IN UNA RIGA

**BLOCCATI su accesso VLAN 1101. Rafa sta cercando di ottenere admin UniFi o FortiGate per creare regola firewall/WiFi dedicato.**

---

## SESSIONE 311 - COSA ABBIAMO FATTO

| Cosa | Stato |
|------|-------|
| Studio architettura rete hotel | DONE |
| Mappatura TUTTE le opzioni accesso VLAN | DONE - 6 opzioni documentate |
| Test accesso FortiGate via rete | FAIL - GUI disabilitata da rete |
| Gateway hotel identificato | 192.168.200.253 (non risponde HTTPS) |
| FortiGate fisico trovato | FG-70G, Serial: FGT70GTK25025291 |

## PROBLEMA ATTUALE

```
Rafa ha VIEW-ONLY su UniFi → non può creare WiFi VLAN 1101
FortiGate GUI disabilitata dalla rete → non può creare firewall rule
Serve: Admin UniFi OPPURE Admin FortiGate
```

---

## NUCLEUS CUSTODE (da UniFi)

```
Nome:     rcu-Custode-1
IP:       10.0.101.12
MAC:      00:08:0C:20:1F:6D
VLAN:     VDA CAMERE (ID 1101)
Porta:    Armadio P2, Port 47
Modello:  H155300 v1.4
```

---

## STRUTTURA RETE VDA

```
VLAN 1101 "VDA CAMERE" (10.0.101.0/24)
├── rcu-Custode-1 (10.0.101.12) ← TARGET TEST
├── Altri NUCLEUS camere (visti in UniFi)
└── Isolata dalle altre VLAN (no ping da WiFi normale)
```

---

## PORTE MODBUS NUCLEUS CUSTODE

```
M1: OCCUPATA (modulo VDA CS1553.1)
M2: LIBERA ← possiamo usarla!
M3: OCCUPATA
M4: OCCUPATA

NOTA: Sono connettori RJ11, non morsetti a vite!
      Per RS-485 serve cavo RJ11 da tagliare.
```

---

## DUE PORTE DI ENTRATA AL NUCLEUS

```
NUCLEUS H155300 - Come comunicare:

1. ETH PORT (RJ45) → Modbus TCP (porta 502)
   └── Via rete, se accedi VLAN 1101
   └── PREFERITA - controlli TUTTO l'albergo!

2. PORTE M1-M4 (RJ11) → Modbus RS-485
   └── Via cavo fisico diretto
   └── BACKUP - se TCP non funziona
```

**Cavo RJ11:** Opzionale, compralo come backup (3 EUR)

---

## STEP BY STEP DOMANI (22 Gen)

### OPZIONE A - Porta fisica VLAN 1101 (più veloce, NO admin!)

```
1. Vai all'Armadio P2
2. Trova il cavo del NUCLEUS Custode (Port 47 switch)
3. Cerca porta LIBERA sullo stesso switch (stessa VLAN!)
4. Collega Mac → dovrebbe prendere IP 10.0.101.xxx
5. Test: ping 10.0.101.12
6. Se funziona → Test Modbus TCP!
```

**ALTERNATIVA:** Scollega temporaneamente un NUCLEUS non critico, collegati al suo posto, testa, ricollega.

### OPZIONE B - Admin UniFi (permanente)

```
1. Accedi UniFi con credenziali admin
2. Settings > Security > Traffic & Firewall Rules
3. Crea regola "DEV-Mac-to-VDA"
4. Source: IP tuo Mac | Dest: 10.0.101.0/24
5. Test da qualsiasi WiFi!
```

### OPZIONE C - Via RS-485 (backup fisico)

```
1. Compra cavo RJ11 (3 EUR Amazon)
2. Taglia e collega fili A/B a USB-RS485
3. Inserisci RJ11 in porta M2 NUCLEUS
4. Test con pymodbus RTU
```

### Test Modbus TCP (una volta connesso)

```bash
pip install pymodbus

python3 << 'EOF'
from pymodbus.client import ModbusTcpClient
client = ModbusTcpClient('10.0.101.12', port=502)
if client.connect():
    print("CONNESSO!")
    result = client.read_holding_registers(0, 10)
    print(result)
else:
    print("Connessione fallita")
EOF
```

---

## OPZIONI UNIFI (studiate con devops)

| Opzione | Pro | Contro |
|---------|-----|--------|
| Firewall Rule | Sicura, granulare | Serve admin |
| WiFi Dedicato | Semplice | Password da proteggere |
| Porta fisica VLAN | Immediato | Devi stare in armadio |

**Consigliata:** Firewall Rule o porta fisica domani

---

## HARDWARE DISPONIBILE

| Item | Stato | Note |
|------|-------|------|
| USB-RS485 FTDI | OK | `/dev/tty.usbserial-BG01VEKH` |
| Multimetro | OK | Per verifiche |
| Cacciaviti | OK | - |
| Jumper | OK | - |
| Cavo RJ11 | MANCA | Da comprare per RS-485 |

---

## FILE CHIAVE

| File | Contenuto |
|------|-----------|
| `.sncp/.../studi/20260116_VDA_ROSETTA_STONE_PIANO.md` | Piano reverse engineering |
| `miracollogeminifocus/room-hardware/backend/main.py` | Skeleton FastAPI |

---

## PROSSIMI OBIETTIVI

1. [ ] **Rafa ottiene admin** (UniFi o FortiGate)
2. [ ] Creare accesso VLAN 1101 (WiFi o Firewall Rule)
3. [ ] Test Modbus TCP porta 502
4. [ ] Scan tutti i NUCLEUS hotel
5. [ ] Mappatura registri → Rosetta Stone

## OPZIONI ACCESSO VLAN 1101 (studio completo)

| Opzione | Costo | Serve Admin? |
|---------|-------|--------------|
| Firewall Rule FortiGate | 0€ | Sì (FortiGate) |
| WiFi dedicato VLAN 1101 | 0€ | Sì (UniFi) |
| Porta Switch Diretta | 0€ | No (ma devi stare in armadio) |
| TP-Link TL-SG108E | 30€ | No |
| Mikrotik hAP Lite | 22€ | No |

**Studio completo:** `.sncp/progetti/miracollo/bracci/room-hardware/studi/STUDIO_VLAN_1101_ACCESSO_COMPLETO.md`

---

*Braccio 3 - Automazione Stanze*
*"Non esistono cose difficili, esistono cose non studiate!"*
