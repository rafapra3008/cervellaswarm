# FRONTEND: Folders Sidebar UI

**Data**: 20260116 | **Worker**: cervella-frontend
**Progetto**: Miracallook

## Task Completato

Aggiunta sezione FOLDERS alla Sidebar con 6 folders navigabili.

## File Modificati

- `miracallook/frontend/src/components/Sidebar/Sidebar.tsx`

## Cosa È Stato Fatto

1. **Import Heroicons** - Aggiunto import icone:
   - InboxIcon
   - PaperAirplaneIcon
   - ArchiveBoxIcon
   - StarIcon
   - DocumentIcon
   - TrashIcon

2. **Type Folder** - Esportato nuovo type:
   ```typescript
   export type Folder = 'inbox' | 'sent' | 'archived' | 'starred' | 'drafts' | 'trash';
   ```

3. **Props Sidebar** - Aggiunte nuove props opzionali:
   - `selectedFolder?: Folder` (default 'inbox')
   - `onSelectFolder?: (folder: Folder) => void`

4. **UI Folders Section** - Creata sezione con:
   - Label "FOLDERS" (stile consistente con "CATEGORIES")
   - 6 bottoni folder con icone Heroicons
   - Stile attivo/inattivo (uguale a categories)
   - Hover states
   - Divider tra Folders e Categories

## Struttura Sidebar Finale

```
├── Logo
├── Compose Button
├── FOLDERS:
│   ├── Inbox
│   ├── Sent
│   ├── Archive
│   ├── Starred
│   ├── Drafts
│   └── Trash
├── ─────────── (divider)
├── All
├── CATEGORIES:
│   ├── VIP
│   ├── Check-in
│   └── ...
└── Footer (shortcuts)
```

## Build Status

✅ TypeScript compilation passed
✅ Vite build passed (731ms)

## Prossime Azioni

### Nel Parent Component (App.tsx)

1. **Aggiungere state folder**:
   ```typescript
   const [selectedFolder, setSelectedFolder] = useState<Folder>('inbox');
   ```

2. **Passare props a Sidebar**:
   ```typescript
   <Sidebar
     selectedFolder={selectedFolder}
     onSelectFolder={setSelectedFolder}
     // ... altre props esistenti
   />
   ```

3. **Implementare logica fetch per folder**:
   - Inbox → `/gmail/inbox` (già funziona)
   - Sent → `/gmail/sent`
   - Archive → `/gmail/archived`
   - Starred → `/gmail/starred`
   - Drafts → `/gmail/drafts` (endpoint esiste)
   - Trash → `/gmail/trash-list`

4. **Hook per folders**:
   - Creare `useSentEmails()`
   - Creare `useArchivedEmails()`
   - Creare `useStarredEmails()`
   - Creare `useTrashEmails()`
   - `useDrafts()` potrebbe già esistere

5. **Logica display**:
   - Quando folder !== 'inbox': mostrare emails del folder
   - Disabilitare categories quando folder selezionato
   - Oppure: resettare folder quando category selezionata

## Note per la Regina

- UI è PRONTA e funzionante
- Stile coerente con resto app (colors, spacing, hover)
- Type esportato per riutilizzo
- Props opzionali (non rompe esistente)
- La logica di fetch rimane da implementare nel parent

---

**COSTITUZIONE-APPLIED**: SI
**Principio usato**: "Fatto BENE > Fatto VELOCE" - Ho mantenuto consistenza stile, verificato build, documentato chiaramente next steps.
