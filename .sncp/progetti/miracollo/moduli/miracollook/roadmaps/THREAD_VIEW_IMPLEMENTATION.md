# Thread View - Implementation Roadmap

**Data:** 14 Gennaio 2026
**Sessione:** 195
**Target:** Miracollook v2.4.0

---

## Overview

Implementare Thread View per raggruppare email in conversazioni.
Design specs: `decisioni/THREAD_VIEW_DESIGN_SPECS.md`
Ricerche: `ricerche/THREAD_VIEW_*_Research.md`

---

## FASE 1: BACKEND (1.5h)

### Task 1.1: threads.py - Endpoint lista thread
```python
GET /gmail/threads
- Usa threads.list() invece di messages.list()
- Restituisce: threadId, snippet, messageCount, historyId
- Parametri: maxResults, labelIds
```
**File:** `backend/gmail/threads.py` (NUOVO)
**Stima:** 30min

### Task 1.2: threads.py - Endpoint expand thread
```python
GET /gmail/threads/{threadId}
- Usa threads.get(format=metadata)
- Restituisce tutti i messaggi del thread
- Headers: From, To, Subject, Date
- Parametri: format (metadata/full)
```
**Stima:** 30min

### Task 1.3: Registra router
```python
# In api.py
from .threads import router as threads_router
router.include_router(threads_router)
```
**Stima:** 5min

### Task 1.4: Test backend
- Test threads.list endpoint
- Test threads.get endpoint
- Verifica con thread reale (multi-message)
**Stima:** 25min

---

## FASE 2: FRONTEND HOOKS (1h)

### Task 2.1: useThreads.ts - Hook principale
```typescript
- useThreads() - lista thread con cache
- useThread(threadId) - singolo thread espanso
- Integrazione con IndexedDB
```
**File:** `frontend/src/hooks/useThreads.ts` (NUOVO)
**Stima:** 30min

### Task 2.2: api.ts - Metodi API
```typescript
- getThreads(params)
- getThread(threadId, format)
- Tipizzazione Thread/ThreadMessage
```
**File:** `frontend/src/services/api.ts` (MOD)
**Stima:** 15min

### Task 2.3: types/thread.ts - TypeScript types
```typescript
interface Thread {
  id: string;
  snippet: string;
  messageCount: number;
  messages?: ThreadMessage[];
  isExpanded?: boolean;
}
```
**File:** `frontend/src/types/thread.ts` (NUOVO)
**Stima:** 15min

---

## FASE 3: FRONTEND COMPONENTS (2h)

### Task 3.1: ThreadListItem.tsx - Row collapsed
```tsx
- Layout 72px come da specs
- Message counter "(N)"
- Chevron icon con rotation
- Unread dot indicator
- Click to expand
```
**File:** `frontend/src/components/ThreadList/ThreadListItem.tsx` (NUOVO)
**Stima:** 45min

### Task 3.2: ThreadExpandedView.tsx - Thread aperto
```tsx
- Header con subject + participants
- Lista messaggi collapsati
- Expand All / Collapse All buttons
- Singolo messaggio espandibile
```
**File:** `frontend/src/components/ThreadList/ThreadExpandedView.tsx` (NUOVO)
**Stima:** 45min

### Task 3.3: ThreadMessage.tsx - Singolo messaggio
```tsx
- Header: From, Date
- Body preview / full
- Click to expand body
- Actions: Reply, Forward
```
**File:** `frontend/src/components/ThreadList/ThreadMessage.tsx` (NUOVO)
**Stima:** 30min

---

## FASE 4: INTEGRATION & POLISH (0.5h)

### Task 4.1: Keyboard shortcuts
```typescript
// In useKeyboardShortcuts.ts
';' -> expandAllMessages
':' -> collapseAllMessages
'o' -> openThread
'Esc' -> closeThread
```
**File:** `frontend/src/hooks/useKeyboardShortcuts.ts` (MOD)
**Stima:** 15min

### Task 4.2: Replace EmailList with ThreadList
- Aggiorna imports
- Mantieni backward compatibility
- Test UI completa
**Stima:** 15min

---

## Checklist Pre-Implementazione

- [x] Ricerca Gmail API threads ✓
- [x] Ricerca UX competitors ✓
- [x] Design specs complete ✓
- [x] Sub-roadmap scritta ✓
- [ ] Backend threads.py
- [ ] Frontend hooks
- [ ] UI components
- [ ] Integration test

---

## File Coinvolti

| File | Tipo | Descrizione |
|------|------|-------------|
| `backend/gmail/threads.py` | NUOVO | Endpoint threads |
| `backend/gmail/api.py` | MOD | Include threads router |
| `frontend/src/services/api.ts` | MOD | API methods |
| `frontend/src/types/thread.ts` | NUOVO | TypeScript types |
| `frontend/src/hooks/useThreads.ts` | NUOVO | React hooks |
| `frontend/src/hooks/useKeyboardShortcuts.ts` | MOD | Thread shortcuts |
| `frontend/src/components/ThreadList/` | NUOVO | 4 componenti |

---

## Stima Totale

| Fase | Tempo |
|------|-------|
| Backend | 1.5h |
| Frontend Hooks | 1h |
| Frontend Components | 2h |
| Integration | 0.5h |
| **TOTALE** | **5h** |

---

## Note

- Approccio: Hybrid (metadata per lista, full on-demand)
- Cache: IndexedDB esistente
- Keyboard: Standard Gmail (j/k, ;/:)
- Design: Dark mode, accent #6366f1

---

*Roadmap pronta per implementazione!*
*"Una cosa alla volta, facciamo BENE!"*
