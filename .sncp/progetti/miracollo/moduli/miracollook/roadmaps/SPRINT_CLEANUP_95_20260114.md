# SPRINT CLEANUP - Da 8.5 a 9.5

> **Data**: 14 Gennaio 2026
> **Obiettivo**: Portare qualità da 8.5/10 a 9.5/10
> **Filosofia**: "Fatto BENE > Fatto VELOCE"

---

## PROBLEMI DA RISOLVERE

| # | Problema | Impatto | Tempo | Priorità |
|---|----------|---------|-------|----------|
| 1 | 31 console.log sparsi | Codice non pulito | 30min | ALTA |
| 2 | 3 TODO in CommandPalette | Feature incompleta | 1h | MEDIA |
| 3 | api.py 1857 righe | File troppo lungo | 2-3h | MEDIA |

---

## FASE 1: CLEANUP CONSOLE.LOG (30 min)

**Obiettivo**: Rimuovere o condizionare console.log

**File da pulire**:
```
hooks/useEmails.ts         - 3 console.log
hooks/usePrefetchEmails.ts - 3 console.log
hooks/useOfflineSync.ts    - 4 console.log
hooks/useEmailCache.ts     - 6 console.log
hooks/useHoverPrefetch.ts  - 2 console.log
services/db.ts             - 9 console.log
main.tsx                   - 1 console.log
hooks/usePrefetchTopUnread.ts - 3 console.log (nuovo)
```

**Approccio**:
- Opzione A: Rimuovere tutti (più pulito)
- Opzione B: Wrappare con `if (import.meta.env.DEV)` (mantiene debug)

**Raccomandazione**: Opzione B per file critici (db.ts, useEmails.ts), Opzione A per altri.

---

## FASE 2: TODO COMMANDPALETTE (1h)

**Obiettivo**: Implementare navigazione mancante

**File**: `frontend/src/components/CommandPalette/CommandPalette.tsx`

**TODO da implementare**:
```typescript
// Riga 128: TODO: Navigate to Inbox
// Riga 138: TODO: Navigate to Sent
// Riga 148: TODO: Navigate to Drafts
```

**Cosa serve**:
1. Prop `onNavigate` da App.tsx
2. Handler per cambiare view (inbox/sent/drafts)
3. Collegare ai TODO esistenti

---

## FASE 3: SPLIT API.PY (2-3h)

**Obiettivo**: Dividere api.py in moduli logici

**Struttura proposta**:
```
backend/gmail/
├── api.py           # Router principale (import altri)
├── auth.py          # OAuth, token management
├── messages.py      # CRUD email (read, list, send)
├── actions.py       # Quick actions (archive, trash, star, mark read)
├── search.py        # Search endpoint
├── labels.py        # Labels management
└── utils.py         # Helper functions
```

**Approccio**:
1. Creare nuovi file con funzioni raggruppate
2. Import nel api.py principale
3. Test che tutto funzioni
4. Graduale (non tutto insieme)

---

## CHECKLIST

### Pre-Sprint
- [ ] Leggere questo documento
- [ ] Decidere priorità (tutte o alcune?)

### Fase 1 - Console.log
- [ ] Pulire useEmails.ts
- [ ] Pulire usePrefetchEmails.ts
- [ ] Pulire useOfflineSync.ts
- [ ] Pulire useEmailCache.ts
- [ ] Pulire useHoverPrefetch.ts
- [ ] Pulire services/db.ts
- [ ] Pulire main.tsx
- [ ] Pulire usePrefetchTopUnread.ts
- [ ] Verificare build OK

### Fase 2 - CommandPalette
- [ ] Aggiungere prop onNavigate
- [ ] Implementare navigazione Inbox
- [ ] Implementare navigazione Sent (se esiste view)
- [ ] Implementare navigazione Drafts (se esiste view)
- [ ] Test funzionamento

### Fase 3 - Split api.py
- [ ] Creare auth.py
- [ ] Creare messages.py
- [ ] Creare actions.py
- [ ] Creare search.py
- [ ] Aggiornare imports in api.py
- [ ] Test backend funziona
- [ ] Verificare tutti endpoint OK

### Post-Sprint
- [ ] Ri-audit Guardiana Qualità
- [ ] Conferma 9.5/10

---

## NOTE

```
"Non abbiamo fretta. Vogliamo la PERFEZIONE."
"I dettagli fanno SEMPRE la differenza."
```

---

*Creato: 14 Gennaio 2026*
*"Da 8.5 a 9.5 - Perché i dettagli contano!"*
