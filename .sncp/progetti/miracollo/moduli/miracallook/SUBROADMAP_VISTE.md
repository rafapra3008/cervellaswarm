# SUB-ROADMAP: Viste Email (Archived, Starred, Snoozed)

**Data:** 13 Gennaio 2026 - Sessione 186
**Status:** IN PROGRESS
**Obiettivo:** Permettere all'utente di vedere email dopo azioni (archive, star, snooze)

---

## PROBLEMA

Attualmente quando l'utente:
- Archivia un'email -> sparisce, non sa dove trovarla
- Marca come VIP (star) -> nessuna vista dedicata
- Snooze un'email -> sparisce, non sa dove trovarla

**SOLUZIONE:** Aggiungere viste dedicate nella Sidebar

---

## ARCHITETTURA

```
ATTUALE:
  Sidebar -> Categories (all, vip, team, fornitori, etc.)
           -> Tutte filtrano da /gmail/inbox (solo INBOX label)

NUOVO:
  Sidebar -> Categories (esistenti)
          -> Special Views (NUOVE):
              - Archived (email senza INBOX label)
              - Starred (email con STARRED label)
              - Snoozed (email con SNOOZED label)
              - Trash (email con TRASH label)
```

---

## STEP IMPLEMENTAZIONE

### STEP 1: Backend API (cervella-backend)

1. **GET /gmail/archived** - Email archiviate (no INBOX, no TRASH)
   - Query Gmail: `-in:inbox -in:trash`
   - Return: lista email

2. **GET /gmail/starred** - Email con stella
   - Query Gmail: `is:starred`
   - Return: lista email

3. **GET /gmail/snoozed** - Email snoozate
   - Query Gmail: `label:SNOOZED`
   - Return: lista email

4. **GET /gmail/trash** - Email nel cestino
   - Query Gmail: `in:trash`
   - Return: lista email

### STEP 2: Frontend Types (cervella-frontend)

1. **email.ts** - Aggiungere tipi:
   ```typescript
   export type EmailView = 'inbox' | 'archived' | 'starred' | 'snoozed' | 'trash';
   ```

### STEP 3: Frontend API Service

1. **api.ts** - Aggiungere funzioni:
   - getArchivedEmails()
   - getStarredEmails()
   - getSnoozedEmails()
   - getTrashEmails()

### STEP 4: Frontend Hooks

1. **useEmails.ts** - Aggiungere hooks:
   - useArchivedEmails()
   - useStarredEmails()
   - useSnoozedEmails()
   - useTrashEmails()

### STEP 5: Frontend Sidebar

1. **Sidebar.tsx** - Aggiungere sezione "Views":
   - Separatore visivo tra Categories e Views
   - Icone appropriate (ArchiveBoxIcon, StarIcon, ClockIcon, TrashIcon)
   - Conteggi per ogni vista

### STEP 6: Frontend App.tsx

1. Gestire selectedView separato da selectedCategory
2. Chiamare l'endpoint appropriato in base alla vista
3. Aggiornare filteredEmails

---

## FILE DA MODIFICARE

| File | Cosa |
|------|------|
| backend/gmail/api.py | 4 nuovi endpoint GET |
| frontend/src/types/email.ts | EmailView type |
| frontend/src/services/api.ts | 4 nuove funzioni |
| frontend/src/hooks/useEmails.ts | 4 nuovi hooks |
| frontend/src/components/Sidebar/Sidebar.tsx | Sezione Views |
| frontend/src/App.tsx | State e logica vista |

---

## PRIORITA

1. Backend endpoint (senza questi nulla funziona)
2. Frontend API + Hooks
3. Sidebar UI
4. App.tsx integration

---

## NOTE TECNICHE

Gmail API query syntax:
- `is:starred` - email con stella
- `in:trash` - email nel cestino
- `-in:inbox -in:trash` - archiviate (non in inbox, non in trash)
- `label:SNOOZED` - email con label custom SNOOZED

---

*"I dettagli fanno SEMPRE la differenza!"*
