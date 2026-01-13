# Ricerca: useOptimistic di React 19 per MIRACOLLOOK

**Data**: 2026-01-13
**Ricercatrice**: Cervella Researcher
**Contesto**: Valutare se `useOptimistic` di React 19 può migliorare l'UX di MIRACOLLOOK rispetto al nostro approccio manuale attuale

---

## SINTESI ESECUTIVA

- **useOptimistic è DISPONIBILE**: React 19.2.0 è già nel nostro stack
- **PROBLEMA CRITICO**: Incompatibilità confermata con React Query (TanStack Query)
- **RACCOMANDAZIONE**: **NON usare useOptimistic per ora** - manteniamo approccio manuale
- **Motivazione**: Bug upstream non risolto causa flickering e stati inconsistenti
- **Alternativa**: Migliorare l'approccio manuale esistente con pattern avanzati

---

## 1. COS'È useOptimistic?

### Definizione

`useOptimistic` è un Hook di React 19 che permette di mostrare uno stato temporaneo "ottimistico" mentre un'azione asincrona è in corso.

### Sintassi

```typescript
const [optimisticState, addOptimistic] = useOptimistic(state, updateFn);
```

### Parametri

| Parametro | Tipo | Descrizione |
|-----------|------|-------------|
| `state` | T | Valore iniziale, usato quando nessuna azione è pendente |
| `updateFn` | `(currentState: T, optimisticValue: U) => T` | Funzione pura che calcola lo stato ottimistico |

### Return Values

| Valore | Descrizione |
|--------|-------------|
| `optimisticState` | Stato corrente (= `state` se no pending, altrimenti risultato di `updateFn`) |
| `addOptimistic` | Funzione per triggerare un update ottimistico |

### Come Funziona il Reset

**AUTOMATICO**: Lo stato ottimistico si resetta automaticamente quando:
- L'azione asincrona completa (success)
- L'azione asincrona fallisce (error)
- React riceve un nuovo valore per `state` (il primo parametro)

Non serve gestire manualmente il rollback - React lo fa per noi.

---

## 2. CONFRONTO CON APPROCCIO MANUALE

### Approccio Attuale (MIRACOLLOOK)

```typescript
export const useArchiveEmail = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (messageId: string) => emailApi.archiveEmail(messageId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['emails'] });
    },
  });
};
```

**Caratteristiche:**
- ✅ Funziona con React Query
- ✅ Semplice e prevedibile
- ❌ No feedback immediato (aspetta server response)
- ❌ Possibile percezione di lentezza

### Con Optimistic Updates Manuali

```typescript
export const useArchiveEmail = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (messageId: string) => emailApi.archiveEmail(messageId),
    onMutate: async (messageId) => {
      // 1. Cancella refetch in-flight
      await queryClient.cancelQueries({ queryKey: ['emails'] });

      // 2. Snapshot stato precedente
      const previousEmails = queryClient.getQueryData(['emails']);

      // 3. Optimistically update
      queryClient.setQueryData(['emails'], (old: Email[]) =>
        old.filter(email => email.id !== messageId)
      );

      // 4. Ritorna context per rollback
      return { previousEmails };
    },
    onError: (err, messageId, context) => {
      // Rollback su errore
      if (context?.previousEmails) {
        queryClient.setQueryData(['emails'], context.previousEmails);
      }
    },
    onSettled: () => {
      // Refetch comunque per sincronizzare
      queryClient.invalidateQueries({ queryKey: ['emails'] });
    },
  });
};
```

**Caratteristiche:**
- ✅ Feedback immediato
- ✅ Rollback automatico su errore
- ✅ Compatibile con React Query
- ⚠️ Più verboso (ma più controllo)

### Con useOptimistic (TEORICO)

```typescript
export const useArchiveEmail = () => {
  const { data: emails } = useEmails();
  const queryClient = useQueryClient();

  const [optimisticEmails, setOptimisticEmails] = useOptimistic(
    emails,
    (currentEmails, messageIdToRemove: string) =>
      currentEmails.filter(email => email.id !== messageIdToRemove)
  );

  const archiveMutation = useMutation({
    mutationFn: (messageId: string) => emailApi.archiveEmail(messageId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['emails'] });
    },
  });

  const archive = async (messageId: string) => {
    setOptimisticEmails(messageId); // Update UI immediatamente
    await archiveMutation.mutateAsync(messageId);
  };

  return { archive, emails: optimisticEmails };
};
```

**Caratteristiche:**
- ✅ API più pulita
- ✅ Reset automatico
- 🔴 **INCOMPATIBILE con React Query** (bug critico)
- 🔴 Causa flickering e stati inconsistenti

---

## 3. IL PROBLEMA DI INCOMPATIBILITÀ

### Bug Confermato

**Issue**: [TanStack/query #9742](https://github.com/TanStack/query/issues/9742)
**Status**: Upstream, non risolto (Ottobre 2025)
**Severità**: Critica

### Root Cause

React Query usa `useSyncExternalStore` che aggiorna lo stato **sincronamente**.

Quando un refetch completa durante una transition:
1. React Query aggiorna sincronamente lo store
2. React rebasa lo stato ottimistico sul nuovo valore
3. Risultato: UI mostra valori **SBAGLIATI** temporaneamente

**Esempio concreto:**
```
1. Count = 1
2. User clicca +1 → optimistic UI mostra 2 ✓
3. Refetch completa → React Query aggiorna a count=1 (dal server)
4. React rebasa optimistic → mostra 2+1 = 3 ✗ (SBAGLIATO!)
5. Mutation completa → optimistic drop → mostra 2 ✓
```

Flickering: `2 → 3 → 2`

### Cosa Servirebbe

Per risolvere il problema React Query dovrebbe:
- Implementare "concurrent stores" (store mutabili in modo concorrente)
- Abbandonare aggiornamenti sincron in favore di asincroni
- Questo richiede un refactoring architetturale importante

**Timeline**: Nessuna ETA comunicata

---

## 4. USE CASES PER EMAIL CLIENT

### Caso 1: Archive Email

**Azione**: Rimuovere email dalla lista inbox

**Pattern Manuale Raccomandato**:
```typescript
onMutate: async (messageId) => {
  await queryClient.cancelQueries({ queryKey: ['emails'] });
  const previous = queryClient.getQueryData(['emails']);

  queryClient.setQueryData(['emails'], (old: Email[]) =>
    old.filter(email => email.id !== messageId)
  );

  return { previous };
}
```

**Benefici**:
- Rimozione immediata dalla UI
- Rollback automatico su errore
- Nessun flickering

### Caso 2: Trash Email

**Identico ad Archive** - stesso pattern

### Caso 3: Star/Unstar (Toggle)

**Pattern Manuale**:
```typescript
onMutate: async (messageId) => {
  await queryClient.cancelQueries({ queryKey: ['emails'] });
  const previous = queryClient.getQueryData(['emails']);

  queryClient.setQueryData(['emails'], (old: Email[]) =>
    old.map(email =>
      email.id === messageId
        ? { ...email, isStarred: !email.isStarred }
        : email
    )
  );

  return { previous };
}
```

### Caso 4: Mark Read/Unread

**Pattern Manuale**:
```typescript
onMutate: async (messageId) => {
  await queryClient.cancelQueries({ queryKey: ['emails'] });
  const previous = queryClient.getQueryData(['emails']);

  queryClient.setQueryData(['emails'], (old: Email[]) =>
    old.map(email =>
      email.id === messageId
        ? { ...email, isUnread: !email.isUnread }
        : email
    )
  );

  return { previous };
}
```

---

## 5. BEST PRACTICES 2025-2026

### Pattern: Concurrent Optimistic Updates

**Problema**: Più azioni ottimistiche contemporanee possono sovrascriversi

**Soluzione**: Query Cancellation + Mutation Keys

```typescript
export const useArchiveEmail = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationKey: ['archive-email'], // TAG la mutation
    mutationFn: (messageId: string) => emailApi.archiveEmail(messageId),
    onMutate: async (messageId) => {
      // Cancella refetch per evitare race condition
      await queryClient.cancelQueries({ queryKey: ['emails'] });

      const previous = queryClient.getQueryData(['emails']);

      queryClient.setQueryData(['emails'], (old: Email[]) =>
        old.filter(email => email.id !== messageId)
      );

      return { previous };
    },
    onError: (err, messageId, context) => {
      if (context?.previous) {
        queryClient.setQueryData(['emails'], context.previous);
      }
    },
    onSettled: () => {
      // Invalida SOLO se non ci sono altre mutations in corso
      if (queryClient.isMutating({ mutationKey: ['archive-email'] }) === 1) {
        queryClient.invalidateQueries({ queryKey: ['emails'] });
      }
    },
  });
};
```

**Key Points:**
- `mutationKey` permette di tracciare mutations concorrenti
- `isMutating()` evita invalidazioni premature
- `cancelQueries` previene "window of inconsistency"

### Pattern: Visual Feedback Ottimistico

```typescript
queryClient.setQueryData(['emails'], (old: Email[]) =>
  old.map(email =>
    email.id === messageId
      ? { ...email, isArchiving: true } // Flag UI
      : email
  )
);
```

Poi nel component:
```tsx
{email.isArchiving && (
  <span className="text-xs text-gray-500">Archiving...</span>
)}
```

### Pattern: Error Recovery

```typescript
onError: (err, messageId, context) => {
  // 1. Rollback
  if (context?.previous) {
    queryClient.setQueryData(['emails'], context.previous);
  }

  // 2. Notifica utente
  toast.error('Failed to archive email. Please try again.');

  // 3. Log per debugging
  console.error('Archive failed:', err);
}
```

---

## 6. CODICE ESEMPIO COMPLETO

### Implementazione Raccomandata: useEmailActions.ts

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { emailApi } from '../services/api';
import type { Email } from '../types/email';

/**
 * Hook per azioni ottimistiche sulle email
 * Pattern: Manual Optimistic Updates con React Query
 *
 * Benefici:
 * - Feedback immediato all'utente
 * - Rollback automatico su errore
 * - Compatibile con React Query
 * - Gestisce concurrent updates
 */

export const useArchiveEmail = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationKey: ['archive-email'],
    mutationFn: (messageId: string) => emailApi.archiveEmail(messageId),

    onMutate: async (messageId) => {
      // 1. Cancella refetch in-flight per evitare race conditions
      await queryClient.cancelQueries({ queryKey: ['emails'] });

      // 2. Snapshot dello stato precedente (per rollback)
      const previousEmails = queryClient.getQueryData<Email[]>(['emails']);

      // 3. Optimistically update: rimuovi email dalla lista
      queryClient.setQueryData<Email[]>(['emails'], (old = []) =>
        old.filter(email => email.id !== messageId)
      );

      // 4. Ritorna context per onError e onSettled
      return { previousEmails };
    },

    onError: (err, messageId, context) => {
      // Rollback su errore
      if (context?.previousEmails) {
        queryClient.setQueryData(['emails'], context.previousEmails);
      }

      // Opzionale: notifica utente
      console.error('Archive failed:', err);
    },

    onSettled: () => {
      // Invalida query SOLO se non ci sono altre archive in corso
      if (queryClient.isMutating({ mutationKey: ['archive-email'] }) === 1) {
        queryClient.invalidateQueries({ queryKey: ['emails'] });
      }
    },
  });
};

export const useTrashEmail = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationKey: ['trash-email'],
    mutationFn: (messageId: string) => emailApi.trashEmail(messageId),

    onMutate: async (messageId) => {
      await queryClient.cancelQueries({ queryKey: ['emails'] });
      const previousEmails = queryClient.getQueryData<Email[]>(['emails']);

      queryClient.setQueryData<Email[]>(['emails'], (old = []) =>
        old.filter(email => email.id !== messageId)
      );

      return { previousEmails };
    },

    onError: (err, messageId, context) => {
      if (context?.previousEmails) {
        queryClient.setQueryData(['emails'], context.previousEmails);
      }
    },

    onSettled: () => {
      if (queryClient.isMutating({ mutationKey: ['trash-email'] }) === 1) {
        queryClient.invalidateQueries({ queryKey: ['emails'] });
      }
    },
  });
};

export const useToggleStarEmail = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationKey: ['toggle-star'],
    mutationFn: ({ messageId, starred }: { messageId: string; starred: boolean }) =>
      emailApi.starEmail(messageId, starred),

    onMutate: async ({ messageId, starred }) => {
      await queryClient.cancelQueries({ queryKey: ['emails'] });
      const previousEmails = queryClient.getQueryData<Email[]>(['emails']);

      // Toggle starred status ottimisticamente
      queryClient.setQueryData<Email[]>(['emails'], (old = []) =>
        old.map(email =>
          email.id === messageId
            ? { ...email, isStarred: starred }
            : email
        )
      );

      return { previousEmails };
    },

    onError: (err, variables, context) => {
      if (context?.previousEmails) {
        queryClient.setQueryData(['emails'], context.previousEmails);
      }
    },

    onSettled: () => {
      if (queryClient.isMutating({ mutationKey: ['toggle-star'] }) === 1) {
        queryClient.invalidateQueries({ queryKey: ['emails'] });
      }
    },
  });
};

export const useMarkReadEmail = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationKey: ['mark-read'],
    mutationFn: ({ messageId, read }: { messageId: string; read: boolean }) =>
      emailApi.markRead(messageId, read),

    onMutate: async ({ messageId, read }) => {
      await queryClient.cancelQueries({ queryKey: ['emails'] });
      const previousEmails = queryClient.getQueryData<Email[]>(['emails']);

      queryClient.setQueryData<Email[]>(['emails'], (old = []) =>
        old.map(email =>
          email.id === messageId
            ? { ...email, isUnread: !read }
            : email
        )
      );

      return { previousEmails };
    },

    onError: (err, variables, context) => {
      if (context?.previousEmails) {
        queryClient.setQueryData(['emails'], context.previousEmails);
      }
    },

    onSettled: () => {
      if (queryClient.isMutating({ mutationKey: ['mark-read'] }) === 1) {
        queryClient.invalidateQueries({ queryKey: ['emails'] });
      }
    },
  });
};
```

### Usage nel Component

```tsx
import { useArchiveEmail } from '../hooks/useEmailActions';

function EmailList() {
  const { data: emails } = useEmails();
  const archiveMutation = useArchiveEmail();

  const handleArchive = (emailId: string) => {
    archiveMutation.mutate(emailId);
    // UI si aggiorna IMMEDIATAMENTE
    // Rollback automatico se errore
  };

  return (
    <div>
      {emails?.map(email => (
        <div key={email.id}>
          <span>{email.subject}</span>
          <button onClick={() => handleArchive(email.id)}>
            Archive
          </button>
        </div>
      ))}
    </div>
  );
}
```

---

## 7. REQUISITI TECNICI

### Versione React

- **Minima**: React 19.0.0
- **MIRACOLLOOK ha**: React 19.2.0 ✅

### Compatibilità Stack

| Libreria | Versione MIRACOLLOOK | Compatibilità useOptimistic |
|----------|---------------------|----------------------------|
| React | 19.2.0 | ✅ Supportata |
| React DOM | 19.2.0 | ✅ Supportata |
| React Query | 5.90.16 | 🔴 **Incompatibile** (bug upstream) |

### Quando Sarà Utilizzabile?

`useOptimistic` diventerà utilizzabile con React Query quando:
1. React Query implementerà concurrent stores
2. Oppure React modificherà il comportamento di `useSyncExternalStore`

**Nessuna timeline ufficiale** al momento (Gennaio 2026)

---

## 8. RACCOMANDAZIONE FINALE

### NON usare useOptimistic per MIRACOLLOOK (per ora)

**Motivi:**
1. 🔴 Bug critico confermato con React Query
2. 🔴 Causa flickering e stati inconsistenti
3. 🔴 Nessuna timeline per fix upstream
4. ✅ Pattern manuale funziona perfettamente

### INVECE: Migliorare Approccio Manuale

**Step concreti per MIRACOLLOOK:**

1. **Implementare optimistic updates manuali** con pattern completo:
   - Query cancellation
   - Context per rollback
   - Conditional invalidation

2. **Aggiungere mutation keys** per gestire concurrent updates

3. **Implementare visual feedback** durante pending:
   ```tsx
   {email.isArchiving && <LoadingSpinner />}
   ```

4. **Error handling robusto** con toast notifications

5. **Testing**: Testare scenari di errore e concurrent updates

### Monitoraggio Futuro

Tenere d'occhio:
- [Issue #9742](https://github.com/TanStack/query/issues/9742) su TanStack Query
- Release notes React Query future
- Quando/se bug risolto → rivalutare useOptimistic

---

## 9. PROSSIMI STEP SUGGERITI

### Immediate (P1)

1. Creare file `hooks/useEmailActions.ts` con pattern ottimistico manuale
2. Implementare optimistic updates per:
   - Archive
   - Trash
   - Star/unstar
   - Mark read/unread

### Short-term (P2)

3. Aggiungere visual feedback durante pending states
4. Implementare error notifications con toast
5. Scrivere test per rollback su errore

### Future (P3)

6. Monitorare issue React Query
7. Se bug risolto → migration guide a useOptimistic
8. Performance benchmarking delle due soluzioni

---

## FONTI

### Documentazione Ufficiale
- [useOptimistic - React Official Docs](https://react.dev/reference/react/useOptimistic)
- [React v19 Release Notes](https://react.dev/blog/2024/12/05/react-19)

### Best Practices React Query
- [Optimistic Updates - TanStack Query Docs](https://tanstack.com/query/latest/docs/framework/react/guides/optimistic-updates)
- [Concurrent Optimistic Updates - TkDodo's Blog](https://tkdodo.eu/blog/concurrent-optimistic-updates-in-react-query)

### Bug e Incompatibilità
- [React Query incompatible with useOptimistic - Issue #9742](https://github.com/TanStack/query/issues/9742)

### Guide e Tutorial 2025-2026
- [React 19 New Hooks - freeCodeCamp](https://www.freecodecamp.org/news/react-19-new-hooks-explained-with-examples/)
- [Mastering Optimistic Updates - 10X Developer](https://www.tenxdeveloper.com/blog/optimistic-updates-react-query-guide)
- [useOptimistic Hook Breakdown - DEV Community](https://dev.to/dthompsondev/react-19-useoptimistic-hook-breakdown-5g9k)

---

**Fine Report**
*Cervella Researcher - 13 Gennaio 2026*
