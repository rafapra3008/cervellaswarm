# ANALISI VDA ETHEOS - PARTE 3 (FINALE)

> **Data:** 14 Gennaio 2026 - Sessione 212
> **Screenshot:** 22-26 (ultimi 5)
> **Autore:** Cervella (Regina)

---

## SCREENSHOT 22: ACCESSO-PRINCIPALE

```
+================================================================+
|   ZONA: Accesso-Principale                                      |
|   Template: ACCESSO PRINCIPALE                                  |
|   Dispositivi: 3                                                |
+================================================================+
```

### Dispositivi

| Nome | ID | Catalogue | Protocollo | Protocol ID | FW | Status |
|------|----|-----------|------------|-------------|-----|--------|
| RCU | d_1_rcu | H155300 | - | - | 5.4.1 | Offline |
| SSW6-KEY | d_2_ssw6-key | NE000056-KEYPAD | modbus | ba:88 ch:1 add:0 | 1.8 | Online |
| LT | d_3_lt | NE000033 | modbus | ba:40 ch:1 add:0 | 0.0 | Online |

### Note
- **SSW6-KEY**: Keypad 6 tasti per accesso
- **LT**: Lettore (card/badge)
- Zone accesso hanno configurazione diversa dalle camere

---

## SCREENSHOT 23: ATRIO-2P (Suite)

```
+================================================================+
|   ZONA: Atrio-2P                                                |
|   Template: Suite                                               |
|   Dispositivi: 3                                                |
+================================================================+
```

### Dispositivi

| Nome | ID | Catalogue | Protocollo | Protocol ID | FW | Status |
|------|----|-----------|------------|-------------|-----|--------|
| RCU | d_4_rcu | H155300 | - | - | 5.4.1 | Offline |
| 6T KEYPAD | d_7_6t-keypad | NE000056-KEYPAD | modbus | ba:88 ch:1 add:0 | 0.132 | Online |
| LT BLE 2.1 | d_8_lt-ble-2-1 | VE503E00 | modbus | ba:40 ch:1 add:0 | 1.0 | Online |

### Note
- **LT BLE 2.1**: Lettore BLE versione 2.1 - più moderno!
- Template "Suite" per aree comuni/atri
- Firmware diversi tra zone (0.132 vs 1.8)

---

## SCREENSHOT 24: CUSTODE

```
+================================================================+
|   ZONA: Custode                                                 |
|   Template: CUSTODE                                             |
|   Dispositivi: 2                                                |
+================================================================+
```

### Dispositivi

| Nome | ID | Catalogue | Protocollo | Protocol ID | FW | Status |
|------|----|-----------|------------|-------------|-----|--------|
| RCU | d_1_rcu | H155300 | - | - | 5.4.1 | Offline |
| LT | d_2_lt | D130000 | modbus | ba:40 ch:1 add:0 | 0.0 | Online |

### Note
- Zona semplificata (solo 2 dispositivi)
- Template dedicato "CUSTODE"
- Niente keypad - solo lettore

---

## SCREENSHOT 25: ACTIVITY LOG - KEYS

```
+================================================================+
|   MODULO: ACTIVITY LOG                                          |
|   TAB: Keys                                                     |
|   EVENTI TOTALI: 9,946                                          |
+================================================================+
```

### Struttura Log Chiavi

**Tab disponibili:**
- Access Control
- Global Status
- **Keys** (attivo)
- HVAC

**Filtri laterali:**
- Search by room name
- Search by room number
- Search by key name
- Search by key uid
- Search by operator
- Date range (From/To)
- Event type: created, deleted, updated

**Colonne:**
| Colonna | Descrizione |
|---------|-------------|
| DATETIME | Timestamp evento |
| ROOM NAME | Nome camera |
| ROOM NUMBER | Numero camera |
| EVENT | created/deleted/updated |
| KEY NAME | Nome chiave (ospite o staff) |
| KEY UID | ID univoco chiave |
| KEY TYPE | rfid, code |
| KEY ROLE | staff, guest |
| OPERATOR | Chi ha fatto l'azione |

### Eventi Esempio

| Datetime | Room | Event | Key Name | Type | Role | Operator |
|----------|------|-------|----------|------|------|----------|
| 14/01/2026 19:30:46 | - | created | Liana | rfid | staff | Reception-847 |
| 14/01/2026 17:53:56 | 403 | created | rm-403-cs0000000-jnl9 | code | guest | Reception-847 |
| 14/01/2026 16:42:14 | - | deleted | Asmae Piani | rfid | staff | Reception-847 |
| 14/01/2026 14:21:56 | 304 | created | rm-304-cs5636682-0hra | code | guest | Reception-847 |
| 14/01/2026 14:18:28 | 105 | created | rm-105-cs6536729-0vy6 | code | guest | Reception-847 |
| 14/01/2026 14:18:21 | 203 | deleted | - | code | guest | Reception-847 |
| 14/01/2026 13:02:39 | 206 | created | rm-206-cs5861840-zklg | code | guest | Reception-847 |
| 14/01/2026 13:02:25 | 205 | created | rm-205-cs1083477-ehor | code | guest | Reception-847 |
| 14/01/2026 13:00:47 | 401 | created | rm-401-cs3141302-ona5 | code | guest | Reception-847 |

### Insight Chiave

```
PATTERN NOMI CHIAVI:
├── Staff: Nome persona (es. "Liana", "Asmae Piani")
└── Guest: rm-{room}-cs{random}-{suffix} (es. "rm-403-cs0000000-jnl9")

OPERATORE:
└── Reception-847 = Postazione reception (ID 847)

TRACCIABILITA' COMPLETA:
- Chi ha creato la chiave
- Quando
- Per quale camera
- Tipo (rfid/code)
- Ruolo (staff/guest)
```

---

## SCREENSHOT 26: ACTIVITY LOG - ACCESS CONTROL

```
+================================================================+
|   MODULO: ACTIVITY LOG                                          |
|   TAB: Access Control                                           |
|   EVENTI TOTALI: 462,329 !!!                                    |
+================================================================+
```

### Struttura Log Accessi

**Tab disponibili:**
- **Access Control** (attivo)
- Global Status
- Keys
- HVAC

**Filtri laterali:**
- Search by room name
- Search by room number
- Search by key name
- Search by key uid
- Date range (From/To)
- Event type:
  - door-close
  - door-open
  - door-unlock
  - indoor-key-in

**Colonne:**
| Colonna | Descrizione |
|---------|-------------|
| DATETIME | Timestamp evento |
| ROOM NAME | Nome camera |
| ROOM NUMBER | Numero camera |
| EVENT | Tipo evento porta |
| KEY NAME | Nome chiave usata |
| KEY UID | ID chiave |
| KEY TYPE | Tipo chiave |
| KEY ROLE | Ruolo |
| ACCESS | Risultato accesso |

### Eventi Esempio

| Datetime | Room | Event |
|----------|------|-------|
| 14/01/2026 20:18:11 | 105 | door-close |
| 14/01/2026 20:17:42 | 105 | door-open |
| 14/01/2026 20:17:33 | 105 | door-close |
| 14/01/2026 20:17:30 | 105 | door-open |
| 14/01/2026 20:17:27 | 403 | door-close |
| 14/01/2026 20:17:21 | 403 | door-open |
| 14/01/2026 20:16:55 | 104 | door-close |
| 14/01/2026 20:16:52 | 104 | door-open |
| 14/01/2026 20:15:16 | 104 | door-close |

### Insight Chiave

```
VOLUME DATI:
└── 462,329 eventi! (vs 9,946 chiavi)
    = ~50x più eventi accesso che chiavi
    = Ogni apertura/chiusura loggata

TIPI EVENTO:
├── door-open: Porta aperta
├── door-close: Porta chiusa
├── door-unlock: Sblocco serratura
└── indoor-key-in: Chiave inserita interno

PATTERN VISIBILE:
└── Camera 105: open→close→open→close in pochi secondi
    = Qualcuno entra/esce rapidamente

UTILITA':
├── Sicurezza: Chi è entrato quando
├── Analytics: Pattern movimento ospiti
├── Housekeeping: Quando camera libera
└── Energia: Ottimizzare HVAC se porta aperta
```

---

## RIEPILOGO PARTE 3

### Nuove Scoperte

```
TEMPLATE ZONE:
├── ACCESSO PRINCIPALE - Zone ingresso
├── Suite - Aree comuni/atri
├── CUSTODE - Zone custode
└── (Camera, Staff visti in Parte 1-2)

ACTIVITY LOG - 4 TAB:
├── Access Control (462K eventi!)
├── Global Status
├── Keys (10K eventi)
└── HVAC

VOLUME DATI IMPRESSIONANTE:
├── Keys: ~10,000 eventi
├── Access Control: ~462,000 eventi
└── = Sistema TRACCIA TUTTO!
```

### Hardware Identificato (Totale)

| Tipo | Modello | Funzione |
|------|---------|----------|
| RCU | H155300 | Room Control Unit (offline in molti casi) |
| 6T KEYPAD | NE000056-KEYPAD | Tastierino 6 tasti |
| SSW6-KEY | NE000056-KEYPAD | Keypad switch |
| LT | NE000033 / D130000 | Lettore base |
| LT BLE | VE503E00 | Lettore BLE 2.1 |
| CON4 | - | Connettore 4 vie |

### Pattern Naming

```
CHIAVI OSPITI:
rm-{room_number}-cs{random_id}-{suffix}
Esempio: rm-403-cs0000000-jnl9

CHIAVI STAFF:
Nome persona
Esempio: "Liana", "Asmae Piani"

OPERATORI:
Reception-{id}
Esempio: Reception-847
```

---

## STUDIO VDA COMPLETO!

```
+================================================================+
|                                                                |
|   PARTE 1 (Sess 210): Screenshot 1-3    ✅                     |
|   PARTE 2 (Sess 211): Screenshot 4-21   ✅                     |
|   PARTE 3 (Sess 212): Screenshot 22-26  ✅                     |
|                                                                |
|   TOTALE: 26 SCREENSHOT ANALIZZATI!                            |
|                                                                |
+================================================================+
```

---

## PROSSIMO STEP

1. **Studio Big Players** - Mews, Opera, Cloudbeds
2. **Confronto** - VDA vs Big Players
3. **Decisioni architettura** - NOSTRO Room Manager

---

*"Non copiamo VDA - facciamo PIU' SMART, FLUIDO, BELLO!"*

*Analisi completata: 14 Gennaio 2026 - Sessione 212*
