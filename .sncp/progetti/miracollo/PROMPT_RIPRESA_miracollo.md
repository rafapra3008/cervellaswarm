# PROMPT RIPRESA - Miracollo

> **Ultimo aggiornamento:** 15 Gennaio 2026 - Sessione 228
> **PROBLEMI DA RISOLVERE - LAYOUT + EMAIL RENDER**

---

## STATO IN UNA RIGA

**MIRACOLLOOK: Layout fixato parzialmente, 2 bug da risolvere**

---

## SESSIONE 228: PULIZIA E DEBUG

### FATTO
1. Docker Miracallook AZZERATO (pulito)
2. Porte unificate: Miracallook = **8002** (era 8001 che conflittava con PMS)
3. Fix Tailwind v4: `@import "tailwindcss"` invece di `@tailwind base/components/utilities`
4. Trovato bug react-resizable-panels: calcolava dimensioni sbagliate
5. Creato layout flexbox temporaneo (funziona ma senza resize)

### BUG DA RISOLVERE

**BUG 1: react-resizable-panels non funziona**
```
Sintomi:
- Layout si schiaccia a sinistra (sidebar 3% invece di 15%)
- La libreria calcola dimensioni sbagliate dal DOM
- Anche con stili inline corretti, misura valori sbagliati

Soluzione temporanea:
- ThreePanel.tsx ora usa layout flexbox semplice (senza libreria)
- Funziona ma NON ha ridimensionamento

Da fare:
- Investigare perche react-resizable-panels v4.4.1 non funziona
- Oppure implementare resize manuale con CSS resize/drag
```

**BUG 2: Email mostra HTML grezzo**
```
Sintomi:
- Contenuto email mostra codice invece di renderizzarlo
- Si vedono tag markdown/HTML come testo

Da investigare:
- Componente EmailDetail o ThreadView
- Come viene parsato il body dell'email
- Potrebbe essere problema di escape HTML
```

---

## COSA ABBIAMO TOLTO (DA RIMETTERE)

**ThreePanel.tsx - Layout ridimensionabile**
```
TOLTO:
- import { Group, Panel, Separator } from 'react-resizable-panels'
- Layout con Panel ridimensionabili
- Persistenza layout in localStorage
- ResizeHandle custom

ORA:
- Layout flexbox semplice con width % fisse
- NON ridimensionabile

DA RIMETTERE:
- Quando fixiamo react-resizable-panels
- Oppure implementiamo resize CSS nativo
```

**Debug logs**
```
AGGIUNTI (da rimuovere dopo):
- console.log in ThreePanel.tsx
- console.warn per layout corrotti
```

---

## FILE MODIFICATI (Sessione 228)

```
miracallook/frontend/src/index.css          <- Fix @import tailwindcss + CSS esplicito
miracallook/frontend/src/components/Layout/ThreePanel.tsx <- Layout semplificato
miracallook/frontend/src/services/api.ts    <- Porta 8002
miracallook/backend/main.py                 <- Porta 8002
miracallook/backend/auth/google.py          <- Porta 8002
miracallook/.env                            <- Porta 8002
miracallook/start_dev.sh                    <- Porta 8002
miracallook/README.md + TEST_*.md           <- Documentazione porte
```

---

## PROSSIMA SESSIONE

```
PRIORITA 1: Fixare rendering email (BUG 2)
- Controllare EmailDetail.tsx / ThreadView.tsx
- Verificare come viene mostrato email.body

PRIORITA 2: Ripristinare resize pannelli (BUG 1)
- Opzione A: Fixare react-resizable-panels
- Opzione B: Implementare resize CSS nativo

PRIORITA 3: Test completo Bulk Actions
- Feature era pronta ma non testata per problemi layout
```

---

## MAPPA PORTE (DEFINITIVA)

| Progetto | Backend | Frontend |
|----------|---------|----------|
| Miracollo PMS | 8001 | 80/443 |
| Miracallook | **8002** | 5173 |
| MenuMaster | 8003 | - |
| Contabilita | 8004 | - |

---

*"Due bug trovati, capiti, documentati. Prossima sessione li risolviamo!"*
