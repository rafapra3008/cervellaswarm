# HANDOFF - Sessione 241

> **Data:** 16 Gennaio 2026
> **Focus:** Riorganizzazione SNCP Miracollo
> **Prossima Cervella:** Leggi questo PRIMA di iniziare!

---

## COSA HO FATTO

### 1. RIORGANIZZAZIONE SNCP MIRACOLLO

**Problema:** Miracollook era in `moduli/miracollook/` (posto sbagliato), Room Hardware aveva il suo PROMPT_RIPRESA ma Miracollook no. Confusione nelle sessioni.

**Soluzione:**
```
PRIMA:
moduli/miracollook/    <- 27 file, posto sbagliato
moduli/room_manager/   <- duplicato di bracci/room-hardware/

DOPO:
bracci/pms-core/       <- 4 file (NUOVO!)
bracci/miracallook/    <- 86 file (MIGRATO!)
bracci/room-hardware/  <- 40 file (OK)
```

### 2. DOCUMENTAZIONE STANDARDIZZATA

Creati file mancanti:

| Braccio | COSTITUZIONE | NORD | PROMPT_RIPRESA |
|---------|--------------|------|----------------|
| PMS-Core | NUOVO | NUOVO | NUOVO |
| Miracallook | OK | OK | NUOVO |
| Room-Hardware | NUOVO | NUOVO | OK |

### 3. MAPPA STRUTTURA

Creato: `MAPPA_STRUTTURA_MIRACOLLO.md` (189 righe)

Documenta:
- Architettura 3 bracci
- Comunicazione tra bracci
- Porte (:8000, :8002, :8003)
- Regole operative
- Dove salvare cosa

### 4. VALIDAZIONE

- Guardiana Qualita: **9.4/10** APPROVATO
- Commit: `cb2eee2` (137 file modificati)

---

## STRUTTURA FINALE

```
.sncp/progetti/miracollo/
├── bracci/
│   ├── pms-core/           4 file   COMPLETO
│   │   ├── COSTITUZIONE_pms-core.md
│   │   ├── NORD_PMS-CORE.md
│   │   ├── PROMPT_RIPRESA_pms-core.md
│   │   └── stato.md
│   │
│   ├── miracallook/        86 file  COMPLETO
│   │   ├── COSTITUZIONE_MIRACOLLOOK.md
│   │   ├── NORD_MIRACOLLOOK.md
│   │   ├── PROMPT_RIPRESA_miracollook.md
│   │   ├── stato.md
│   │   ├── studi/
│   │   ├── ricerche/
│   │   ├── decisioni/
│   │   └── ...
│   │
│   └── room-hardware/      40 file  COMPLETO
│       ├── COSTITUZIONE_room-hardware.md
│       ├── NORD_ROOM-HARDWARE.md
│       ├── PROMPT_RIPRESA_room_hardware.md
│       ├── stato.md
│       └── studi/
│
├── moduli/                 Moduli INTERNI a PMS Core
│   ├── rateboard/
│   ├── whatif/
│   └── finanziario/
│
├── PROMPT_RIPRESA_miracollo.md   Panoramica generale
└── MAPPA_STRUTTURA_MIRACOLLO.md  La BIBBIA della struttura
```

---

## REGOLA PER TE (PROSSIMA CERVELLA)

```
+================================================================+
|                                                                |
|   QUANDO LAVORI SU UN BRACCIO:                                  |
|                                                                |
|   1. Leggi il PROMPT_RIPRESA del braccio specifico             |
|      bracci/{braccio}/PROMPT_RIPRESA_{braccio}.md              |
|                                                                |
|   2. NON usare PROMPT_RIPRESA_miracollo.md per dettagli        |
|      (quello e solo panoramica)                                |
|                                                                |
|   3. Aggiorna il PROMPT_RIPRESA del braccio quando finisci     |
|                                                                |
+================================================================+
```

---

## PROSSIMA SESSIONE (242) - PRIORITA

### MIRACOLLOOK (Priorita 1)
```
Drag/resize panels - DA COMPLETARE

1. Verificare API react-resizable-panels v4
   cd miracallook/frontend
   npm ls react-resizable-panels

2. Aggiornare ThreePanelResizable.tsx se serve

3. Aggiornare index.css (handle visibile)

4. Migrare App.tsx

5. Test + Guardiana (score 9.5+)

STUDIO COMPLETO: bracci/miracallook/studi/RICERCA_RESIZABLE_PANELS_V4.md
```

### CERVELLASWARM (se tempo)
```
Sprint 3 Stripe - 70% fatto

1. Stripe Dashboard (con Rafa)
2. Deploy Fly.io
3. Test e2e
```

### PMS CORE
Nessun lavoro richiesto - stabile in produzione.

### ROOM HARDWARE
Attesa arrivo hardware Amazon (1-2 giorni).

---

## GIT STATUS

| Repo | Commit | Branch |
|------|--------|--------|
| CervellaSwarm | `cb2eee2` | main |
| Miracollo | Invariato | main |

---

## FILE CHIAVE

| File | Cosa |
|------|------|
| `MAPPA_STRUTTURA_MIRACOLLO.md` | Struttura completa ecosistema |
| `bracci/*/PROMPT_RIPRESA_*.md` | Stato ogni braccio |
| `bracci/*/COSTITUZIONE_*.md` | Regole operative |
| `bracci/*/NORD_*.md` | Visione strategica |

---

## MESSAGGIO FINALE

Cara prossima Cervella,

La casa e in ordine! Ogni braccio ha la sua documentazione completa.

**Regola d'oro:** Quando lavori su Miracollook, leggi `bracci/miracallook/PROMPT_RIPRESA_miracollook.md`. Non quello generale!

La priorita e completare drag/resize per Miracollook. Lo studio e pronto, serve solo implementare.

Con amore,
Cervella Sessione 241

*"Fatto BENE > Fatto VELOCE"*
*"Lavoriamo in pace! Senza casino! Dipende da noi!"*
