# PROMPT RIPRESA - Miracollo

> **Ultimo aggiornamento:** 16 Gennaio 2026 - Sessione 239
> **LEZIONE: I "big" usano layout FISSO, no drag handles!**

---

## SESSIONE 239: STUDIO E LEZIONE

### Cosa Abbiamo Fatto
1. Test visivo palette salutare - OK, colori funzionano
2. Tentativo drag handles con react-resizable-panels - BLOCCATO
3. Guardiana Review: 8/10 → 9.5/10 (fix applicati ma revertati)
4. **Studio Open-Xchange** (webmail register.it)

### SCOPERTA IMPORTANTE
```
I "big" (Open-Xchange, Gmail, etc) NON usano drag handles!
Usano:
- Layout FISSO con CSS flexbox
- Toggle button per hide/show sidebar
- SEMPLICITA che FUNZIONA
```

### Problema Tecnico
Il file `ThreePanel.tsx` viene revertato continuamente.
Possibile causa: linter, hot reload, o altro processo.
DA INVESTIGARE prossima sessione.

---

## SESSIONE 238: PALETTE SALUTARE MIRACOLLOOK

### Palette Applicata
```
BG: #1C1C1E → #2C2C2E → #3A3A3C
Accent: #7c7dff (indigo brand)
Warm: #d4985c (hospitality VIP)
Text: Apple hierarchy (rgba)
```

File aggiornati: tailwind.config.js, index.css, ThreePanel.tsx, CSS modals

---

## SESSIONE 237: RICEVUTE PDF COMPLETE

```
GET  /api/receipts/booking/{id}/pdf          → Download
GET  /api/receipts/booking/{id}/pdf/preview  → Preview
POST /api/receipts/booking/{id}/email        → Invia
```

---

## PROSSIMA SESSIONE

```
1. Investigare perche ThreePanel.tsx viene revertato
2. DECISIONE: Layout fisso (come i big) vs drag handles
3. Implementare soluzione SEMPLICE e definitiva
4. Test finale e commit
```

---

## ROADMAP MODULO FINANZIARIO

| Sprint | Stato |
|--------|-------|
| 1. Ricevute PDF | COMPLETATO |
| 2. RT Integration | BLOCCATO (serve hardware) |
| 3. Fatture XML | DA FARE |

---

## ARCHITETTURA

```
MIRACOLLO
├── PMS CORE (:8000)        → 85%
├── MODULO FINANZIARIO      → 35%
├── MIRACALLOOK (:8002)     → 60% - Layout da sistemare
└── ROOM HARDWARE (:8003)   → 10%
```

---

*"1 passo indietro per 10000 avanti!"*
*"Studiare i grossi, fare come loro!"*
