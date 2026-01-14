# ANALISI VDA ETHEOS - PARTE 2

**Data**: 2026-01-14 (Sessione 211)
**Analista**: Cervella Regina
**Screenshot analizzati**: 4-21 (18 screenshot)
**Status**: IN CORSO (mancano 5 screenshot: 22-26)

---

## RIEPILOGO SESSIONE 211

Continuazione studio VDA Etheos. Analizzati 3 blocchi:
- BLOCCO 2: Screenshot 4-9 (Chiavi, DND, MUR)
- BLOCCO 3: Screenshot 10-15 (Pulizia, Occupazione, HVAC, Room Control)
- BLOCCO 4: Screenshot 16-21 (Staff, Dashboard, Device Manager)

---

## BLOCCO 2: SISTEMA CHIAVI E SERVIZI (Screenshot 4-9)

### Screenshot 4: Azioni Camera Selezionata

```
Camera selezionata (101) -> Footer azioni:
├── Annulla
├── Crea chiave
├── Modifica dati
├── Check-Out
└── Controlla
```

### Screenshot 5: Creazione Chiave Ospite

```
TIPO CHIAVE:
├── BLE (Bluetooth Low Energy) - badge fisico
└── CODICE (numerico) - PIN digitale

CONFIGURAZIONE:
├── Camera: numero (virgola per multiple)
├── Profilo ospite: dropdown (guest-default)
├── Regole accesso: personalizzabili
└── Periodo validità:
    ├── Periodo di check-in (automatico)
    └── Data/ora personalizzate
```

### Screenshot 6: Check-In Multi-Lingua

```
URL: room-manager.rc-onair.com
Lingue disponibili:
├── Italiano
└── English

→ Istruzioni check-in nella lingua dell'ospite!
```

### Screenshot 7: Altro Esempio Chiave

Camera 203, stesso flow - conferma consistenza UI.

### Screenshot 8: DND (Do Not Disturb)

```
STATO DND per camera:
├── Grid 24 camere + aree comuni
├── Icona lucchetto per ogni camera
├── Pallino verde = dispositivo online
└── Filtri: Common Areas, Rooms, Accessi comuni

→ Ospite attiva DND -> reception vede in tempo reale
```

### Screenshot 9: MUR (Make Up Room)

```
RICHIESTE PULIZIA:
├── Grid 22 camere con sensore MUR
├── Icona secchiello = pulizia
├── "Seleziona tutto" checkbox
└── Filtri laterali

→ Ospite preme bottone in camera -> richiesta visibile a reception
```

---

## BLOCCO 3: HVAC E ROOM CONTROL (Screenshot 10-15)

### Screenshot 10: Stato Pulizia Camera (Housekeeping)

```
HOUSEKEEPING STATUS:
├── Icona scopa GRIGIA = da pulire
├── Icona scopa BLU = pulizia completata
└── Camere 205, 206 = pulizia fatta

→ Housekeeping aggiorna stato dopo pulizia
```

### Screenshot 11: Occupazione Corrente (REAL-TIME!)

```
SENSORE PRESENZA:
├── Icona persona BLU piena = OCCUPATA (ospite dentro)
├── Icona persona outline = LIBERA
├── Icona quadrata (403) = Staff?

Camere occupate ORA: 101, 104, 105, 204, 304, 403, 405

→ PRESENZA REALE rilevata da sensori!
→ Non basato su check-in ma su SENSORE FISICO!
```

### Screenshot 12: HVAC - Controllo Temperatura (FONDAMENTALE!)

```
58 DISPOSITIVI TERMICI!

Ogni camera ha DUE termostati:
├── BAGNO (controllo separato)
└── CAMERA (controllo separato)

Per ogni termostato:
├── Icona termometro (verde = online)
├── Modalità: "Heat" (riscaldamento)
├── Temperatura ATTUALE (es. 22.5°C)
├── Temperatura TARGET (es. 25.2°C)
├── Indicatore livello termosifone (barre)
└── Stato finestra: "Open" = FINESTRA APERTA!

RILEVAMENTO FINESTRE:
Camera 205 CAMERA mostra "Open"
→ Sistema RILEVA quando finestra è aperta!
→ Possibile automazione: spegni riscaldamento se finestra aperta
```

### Screenshot 13: Regola Termostato Singolo

```
Camera 105 - BAGNO:
├── Temperatura attuale: 21.7°C
├── Temperatura target: 22.5°C
├── Frecce su/giù per regolare
├── Bottone ON/OFF (verde = attivo)
└── Pulsanti: Annulla, Applica
```

### Screenshot 14: Room Control - Vista Completa Camera

```
Camera 105 - CONTROLLO TOTALE:

SENSORI STATO:
├── ROOMSTATE_PRESENCE (toggle + lock icon)
└── ROOMSTATE_DOOROPEN (toggle + lock icon)

TABS DISPONIBILI:
├── Thermal-zone (temperatura)
├── Lights (luci)
└── Door-unlock (apertura porta)

THERMAL-ZONE DETTAGLIO:

BAGNO:                      CAMERA:
├── Mode: Comfort           ├── Mode: Comfort
├── Attuale: 21.7°C         ├── Attuale: 21.2°C
├── Target: 22.5°C          ├── Target: 22.0°C
├── Range: 16.5-28.5°C      ├── Range: 16-28°C
├── Slider regolazione      ├── Slider regolazione
└── Power ON/OFF            ├── "Closed" (finestra)
                            └── Power ON/OFF

→ Controllo GRANULARE per zona!
→ Stato finestra per ogni zona!
```

### Screenshot 15: Elenco Chiavi Ospiti

```
23 CHIAVI ATTIVE

COLONNE:
├── STATO (Attivo/Disattivo)
├── NOME CHIAVE (rm-101-cs4113073-le8s)
├── PROFILO (Cliente STD SPA)
├── ACCESSO (Camera + zone)
├── VALIDO DA
├── VALIDO FINO
└── AZIONI (Edit, Disable, Duplicate, Delete)

FORMATO NOME CHIAVE:
rm-{camera}-cs{id}-{suffix}
Esempio: rm-101-cs4113073-le8s

ZONE ACCESSO PER CHIAVE:
├── Camera principale (101, 102...)
├── Accesso-Principale
├── Clima1P (climatizzazione piano 1)
└── Clima2P (climatizzazione piano 2)

→ Una chiave può aprire MULTIPLE ZONE!
→ Profili definiscono quali zone accessibili
```

---

## BLOCCO 4: STAFF, DASHBOARD, DEVICES (Screenshot 16-21)

### Screenshot 16: Chiavi del Personale (Staff)

```
33 CHIAVI STAFF (separate da ospiti!)

STRUTTURA:
├── Nome REALE (Marta, Francesca, Thais, Daniele...)
├── Tipo: RFID o CODE
├── Profilo: Default
├── Accesso: "Tutte le camere" + "Common Areas"

PATTERN INTERESSANTE:
├── "Marta" - ID: 8503cd30 - RFID (badge fisico)
├── "Marta" - ID: b2d4eea6 - CODE (codice backup)

→ Ogni staff ha DOPPIO accesso: RFID + CODE!
→ Se perde badge, ha codice backup
→ "Signora Daniela" ha anche "Accessi comuni" extra
```

### Screenshot 17: Menu CHIAVI (Separazione)

```
Dropdown CHIAVI:
├── CHIAVI OSPITI
└── CHIAVI DEL PERSONALE

→ Gestione completamente SEPARATA!
→ Permessi diversi (staff = tutte camere)
```

### Screenshot 18: Preferenze Utente

```
CONFIGURAZIONI PERSONALIZZABILI:
├── Lingua app: Italiano
├── Measurement unit: Celsius (°C)
├── Codificatore predefinito: 1
├── Elementi tabella: 50
├── Formato data: E dd/MM/yyyy (Wed 14/01/2026)
└── Formato orario: 24h (checkbox)
```

### Screenshot 19: Dashboard Principale (KPI!)

```
HEADER:
├── SITES > Naturae Lodge
├── Code: itblxalle00847
└── Hotel Chain: n.a.

MODULI DISPONIBILI (7):
├── Dashboard
├── Room Manager
├── Device Manager
├── Site Users
├── Scheduler        ← PROGRAMMAZIONI!
├── Activity Log     ← STORICO!
└── Alarm Viewer

KPI CARDS (Salute Sistema):
┌────────────────────────┬───────────────────────┐
│ ONLINE ROOMS           │ 32/32 (100%)          │
│ OFFLINE ROOMS          │ 0/32                  │
│ OFFLINE DEVICES        │ 0/112 devices         │
│ ROOMS WITH OFFLINE DEV │ 0/32                  │
└────────────────────────┴───────────────────────┘

→ Monitoraggio SALUTE in tempo reale!
→ 112 dispositivi totali confermati
```

### Screenshot 20: Menu Moduli (Popup)

```
7 MODULI TOTALI:
1. Dashboard      - Vista generale KPI
2. Room Manager   - Gestione camere/check-in
3. Device Manager - Hardware/dispositivi
4. Site Users     - Utenti sistema
5. Scheduler      - Programmazioni automatiche
6. Activity Log   - Log attività/audit
7. Alarm Viewer   - Gestione allarmi
```

### Screenshot 21: Device Manager - Dettaglio Hardware

```
CAMERA 101 - Template: CAMERE
4 DISPOSITIVI PER CAMERA:

┌─────────────┬──────────────────┬──────────┬───────────────────┬─────────┐
│ DEVICE      │ CATALOGUE ID     │ PROTOCOL │ PROTOCOL ID       │ FW VER  │
├─────────────┼──────────────────┼──────────┼───────────────────┼─────────┤
│ RCU         │ H155300          │ -        │ -                 │ 5.4.1   │
│ d_4_rcu     │                  │          │                   │         │
├─────────────┼──────────────────┼──────────┼───────────────────┼─────────┤
│ 6T KEYPAD   │ NE000056-KEYPAD  │ modbus   │ ba:88 ch:1 add:0  │ 0.132   │
│ d_7_6t-keyp │                  │          │                   │         │
├─────────────┼──────────────────┼──────────┼───────────────────┼─────────┤
│ LT BLE 2.1  │ VE503E00         │ modbus   │ ba:40 ch:1 add:0  │ 1.0     │
│ d_8_lt-ble  │                  │          │                   │         │
├─────────────┼──────────────────┼──────────┼───────────────────┼─────────┤
│ CON4 2.1    │ VE503T00         │ modbus   │ ba:48 ch:2 add:0  │ 1.6     │
│ d_9_con4    │                  │          │                   │         │
└─────────────┴──────────────────┴──────────┴───────────────────┴─────────┘

PROTOCOLLO: MODBUS (standard industriale!)

DISPOSITIVI SPIEGATI:
├── RCU = Room Control Unit (cervello della camera)
├── 6T KEYPAD = Tastierino 6 tasti (DND, MUR, SOS...)
├── LT BLE 2.1 = Lettore Bluetooth Low Energy (badge)
└── CON4 2.1 = Controller 4 canali (relè, output)

ZONE ID: z_q-e (identificativo zona)

→ Hardware MODBUS = standard industriale!
→ Potenzialmente COMPATIBILE con nostro sistema!
```

---

## RIEPILOGO SCOPERTE SESSIONE 211

### Funzionalità Confermate

| Categoria | Feature | Dettaglio |
|-----------|---------|-----------|
| **CHIAVI** | BLE + CODICE | Due tipi accesso |
| **CHIAVI** | Profili | Template permessi |
| **CHIAVI** | Zone multiple | Una chiave = più aree |
| **CHIAVI** | Staff separati | Gestione dedicata |
| **CHIAVI** | RFID + CODE backup | Doppio accesso staff |
| **SERVIZI** | DND | Do Not Disturb real-time |
| **SERVIZI** | MUR | Make Up Room request |
| **SERVIZI** | Multi-lingua | IT/EN check-in |
| **HVAC** | 2 zone/camera | Bagno + Camera separati |
| **HVAC** | Rilevamento finestre | "Open" quando aperta |
| **HVAC** | Comfort mode | Preset temperature |
| **SENSORI** | Presenza | Occupazione real-time |
| **SENSORI** | Porta | Aperta/chiusa |
| **CONTROLLO** | Luci | Tab dedicato |
| **CONTROLLO** | Door-unlock | Apertura remota |
| **DASHBOARD** | KPI | Online/offline devices |
| **SISTEMA** | Scheduler | Programmazioni |
| **SISTEMA** | Activity Log | Audit trail |
| **HARDWARE** | MODBUS | Protocollo standard |
| **HARDWARE** | 4 device/camera | RCU, Keypad, BLE, CON4 |

### Hardware Naturae Lodge

```
TOTALI:
├── 32 camere
├── 112 dispositivi (~3.5/camera)
├── 58 termostati (bagno + camera)
├── 100% online

PER CAMERA:
├── 1x RCU (Room Control Unit)
├── 1x 6T KEYPAD (tastierino)
├── 1x LT BLE (lettore badge)
└── 1x CON4 (controller)
```

---

## PROSSIMA SESSIONE (PARTE 3)

- [ ] Analizzare screenshot 22-26 (ultimi 5)
- [ ] Studiare Scheduler (automazioni)
- [ ] Studiare Activity Log
- [ ] Confronto con big players (Mews, Opera, etc.)
- [ ] Definire architettura Miracollo Room Manager

---

## NOTE PER MIRACOLLO

### Cosa Copiare (Best Practices)
- Separazione chiavi ospiti/staff
- Doppio accesso (badge + codice)
- Zone multiple per chiave
- 2 termostati per camera
- Dashboard KPI salute sistema
- Activity Log per audit

### Cosa Migliorare (PIÙ SMART!)
- AI per temperatura ottimale
- Automazione finestra aperta -> spegni
- Scheduling intelligente pulizie
- Notifiche push DND/MUR
- Analytics occupazione
- Predizione consumi energia

### Compatibilità Hardware
- Protocollo MODBUS = STANDARD!
- Possibile integrazione con hardware esistente
- Da verificare: API VDA o accesso diretto MODBUS?

---

*Parte 2 di N - Sessione 211*
*"Non copiamo VDA - facciamo PIÙ SMART, FLUIDO, BELLO!"*
