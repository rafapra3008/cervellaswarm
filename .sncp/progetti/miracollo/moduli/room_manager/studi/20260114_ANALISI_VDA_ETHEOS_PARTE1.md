# ANALISI VDA ETHEOS - PARTE 1

**Data**: 2026-01-14 (Sessione 210)
**Analista**: Cervella Regina
**Screenshot analizzati**: 3 di 26
**Status**: IN CORSO (continua prossima sessione)

---

## OBIETTIVO

Studiare il sistema VDA Etheos installato a Naturae Lodge per:
1. Capire cosa fa e come funziona
2. Identificare punti di forza/debolezza
3. Progettare il NOSTRO sistema (più smart, fluido, bello)
4. Riutilizzare l'hardware esistente

---

## INFORMAZIONI GENERALI

| Campo | Valore |
|-------|--------|
| **Software** | Etheos Room Manager |
| **Versione** | 1.10.1 |
| **Hotel** | Naturae Lodge |
| **Codice Hotel** | itblxalle00847 |
| **Hotel Chain** | n.a. (indipendente) |
| **Camere totali** | 32 |
| **Stato attuale** | 100% online, 0 allarmi |

---

## SCREENSHOT 1: Check-in/Check-out

**Funzione**: Seleziona le camere per fare il check-in o il check-out

### Layout Camere

```
PIANO 1: 101, 102, 103, 104, 105
PIANO 2: 201, 202, 203, 204, 205, 206
PIANO 3: 301, 302, 303, 304, 305, 306
PIANO 4: 401, 402, 403, 404, 405

AREE COMUNI:
- Atrio-2P, Atrio-3P
- BAR
- Clima1P, Clima2P, Clima4P (climatizzazione per piano?)
- Custode
- Massaggi (troncato)
- Saletta (troncato)
- Accessi (troncato)
```

### Indicatori Visivi

| Icona | Significato |
|-------|-------------|
| Check BLU pieno | Camera attiva/online |
| Check VERDE outline | Disponibile |
| Icona persona | Ospite presente |
| Pallino verde | Dispositivi online |

### Menu Principale

- **ROOM MANAGER** (dropdown)
- **CHIAVI** (dropdown)
- **Ultimi allarmi** (button)
- **Reception** (user menu)

### Filtri Laterali

- Common Areas
- Rooms
- Accessi comuni
- Cerca per camera/area

### Note UX

- Grid view con card per camera
- Selezione singola o combinata
- Paginazione: 1-32 of 32
- Vista: griglia o lista

---

## SCREENSHOT 2: Ultimi Allarmi

**Funzione**: Visualizza e gestisce gli allarmi del sistema

### Filtri Stato

| Stato | Significato |
|-------|-------------|
| Open | Allarmi aperti/attivi |
| Closed | Allarmi chiusi/risolti |
| Closing | In fase di chiusura |
| In charge | Presi in carico |

### Tipi di Allarme

| Tipo | Descrizione |
|------|-------------|
| **sos** | Emergenza attiva (pulsante SOS in camera?) |
| **sos-disabled** | Emergenza disabilitata |
| **SCATTO-TERMICO** | Problema temperatura/termosifone |
| **MUR** | Allarme tecnico (da investigare) |

### Stato Attuale

**"Nessun risultato trovato"** = 0 allarmi attivi!

Questo conferma le statistiche: sistema stabile, tutto funziona.

---

## SCREENSHOT 3: Sites (Menu Principale)

**Funzione**: Selezione moduli principali

### Moduli Disponibili

| Modulo | Icona | Funzione |
|--------|-------|----------|
| **Dashboard** | Casa | Vista generale, statistiche |
| **Room Manager** | Letto | Gestione camere, check-in/out |
| **Alarm Viewer** | Antenna | Visualizzazione allarmi |

---

## PRIME OSSERVAZIONI

### Punti di Forza VDA

1. **UI pulita** - Design moderno, chiaro
2. **Grid view** - Tutte le camere a colpo d'occhio
3. **Sistema allarmi** - Categorizzato per tipo e stato
4. **Multi-area** - Gestisce camere + aree comuni
5. **Indicatori visivi** - Stato chiaro con icone/colori

### Punti di Debolezza (da confermare)

1. **Closed source** - Nessuna API pubblica
2. **Vendor lock-in** - Hardware proprietario
3. **Limitato** - Solo 3 moduli visibili
4. **No AI** - Dashboard statica, no predizioni

### Domande Aperte (per prossimi screenshot)

1. Come funziona il controllo TEMPERATURA?
2. Come si gestiscono i CODICI ACCESSO?
3. C'è una vista DISPOSITIVI/SENSORI?
4. Come si settano le AUTOMAZIONI?
5. Come si integra con PMS esterno?

---

## PROSSIMI STEP

- [ ] Analizzare screenshot 4-26 (prossime sessioni)
- [ ] Documentare ogni funzionalità
- [ ] Identificare gap per Miracollo
- [ ] Studiare i big players (Mews, Opera, etc.)
- [ ] Progettare il NOSTRO sistema

---

## HARDWARE ESISTENTE (da ricerca precedente)

Naturae Lodge ha installato:
- **32 camere** con dispositivi
- **112 dispositivi totali** (~3.5 per camera)
- Sensori temperatura
- Controllo termosifoni
- Sistema codici accesso
- Tutto connesso e online!

**VANTAGGIO**: L'hardware c'è già, dobbiamo solo collegarlo a Miracollo!

---

*Parte 1 di N - Continua prossima sessione*
*"Non copiamo VDA - facciamo PIÙ SMART, FLUIDO, BELLO!"*
