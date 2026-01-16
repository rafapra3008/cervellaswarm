# PROMPT RIPRESA - Miracollo

> **Ultimo aggiornamento:** 16 Gennaio 2026 - Sessione 231
> **NOVITA: Architettura 3 BRACCI definita e implementata!**

---

## ARCHITETTURA ECOSISTEMA (NUOVO!)

```
MIRACOLLO ECOSISTEMA
│
├── PMS CORE (:8000)        → 85% - Stabile, produzione
├── MIRACALLOOK (:8002)     → 60% - Email client, backlog presente
└── ROOM HARDWARE (:8003)   → 10% - Ricerca OK, attesa hardware
```

### Dove Trovare Stato Dettagliato

| Braccio | File Stato |
|---------|------------|
| PMS Core | `bracci/pms-core/stato.md` |
| Miracallook | `bracci/miracallook/stato.md` |
| Room Hardware | `bracci/room-hardware/stato.md` |

---

## SESSIONE 231: ARCHITETTURA 3 BRACCI

### Completato
- Struttura `bracci/` creata in SNCP
- Migrato `moduli/room_manager/` → `bracci/room-hardware/`
- Creato `stato.md` per ogni braccio
- Creato `room-hardware/` in miracollogeminifocus (skeleton)
- Documento decisionale: `decisioni/20260116_ARCHITETTURA_3_BRACCI.md`

### Struttura Codice

```
miracollogeminifocus/
├── backend/          # PMS Core
├── frontend/         # PMS Core UI
├── miracallook/      # Braccio 2
└── room-hardware/    # Braccio 3 (NUOVO!)
```

---

## PRIORITA BRACCI

| # | Braccio | Prossimo Task |
|---|---------|---------------|
| 1 | Miracallook | Applicare palette salutare |
| 2 | Room Hardware | Setup quando arriva hardware |
| 3 | PMS Core | Manutenzione al bisogno |

---

## ROOM HARDWARE - STATO

- Hardware Amazon in arrivo (1-2 giorni dal 16 Gen)
- Piano Rosetta Stone pronto
- Studi: `bracci/room-hardware/studi/` (21 file!)

---

## MAPPA PORTE

| Braccio | Backend | Frontend |
|---------|---------|----------|
| PMS Core | 8000 | 80/443 |
| Miracallook | 8002 | 5173 |
| Room Hardware | 8003 | - |

---

*"I dettagli fanno SEMPRE la differenza!"*
*Architettura pulita = scalabilita futura!*
