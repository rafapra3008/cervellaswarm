# OUTPUT: Thread View Components

**Data**: 20260114 | **Worker**: cervella-frontend
**Specs seguite**: `.sncp/progetti/miracollo/moduli/miracallook/decisioni/THREAD_VIEW_DESIGN_SPECS.md`

---

## File Creati/Modificati

### Componenti Creati
- `miracollook/frontend/src/components/ThreadList/ThreadListItem.tsx` - Thread collapsed row (72px height)
- `miracollook/frontend/src/components/ThreadList/ThreadMessage.tsx` - Singolo messaggio (collapsed/expanded)
- `miracollook/frontend/src/components/ThreadList/ThreadExpandedView.tsx` - Container thread espanso
- `miracollook/frontend/src/components/ThreadList/index.ts` - Export principale

---

## Verifica Acceptance Criteria

### ThreadListItem
- [x] Height 72px
- [x] Message counter badge "(N)" accanto al subject (solo se messageCount > 1)
- [x] Chevron icon (ChevronDown da Heroicons) che ruota 180° quando espanso
- [x] Unread dot cyan se almeno un messaggio unread
- [x] Hover state (bg-miracollo-bg-hover)
- [x] Selected state (bg-miracollo-accent/15 + border-left accent)
- [x] Font-mono JetBrains Mono per counter e date
- [x] Transition duration-200 ease-in-out

### ThreadExpandedView
- [x] Header con subject + "N messages" + "N participants"
- [x] Bottoni "Expand All" / "Collapse All"
- [x] Lista di ThreadMessage con toggle individuale

### ThreadMessage
- [x] Collapsed: From, Date, snippet (single line)
- [x] Expanded: From, Date, full body in bg-secondary rounded box
- [x] Auto-expand ultimo messaggio (isLast prop)
- [x] Click header per toggle
- [x] Bottoni Reply/Forward (placeholder)
- [x] Transition smooth

---

## Pattern Seguiti

### Da EmailListItem.tsx
- ✅ Stesso formatDate() logic
- ✅ Stesso hover/selected state system
- ✅ Stesso unread indicator (cyan dot)
- ✅ Stesso font-mono per date
- ✅ Keyboard navigation (Enter/Space)

### Da Design Specs
- ✅ Tailwind classes miracollo-* (bg-card, accent, text-muted, border)
- ✅ Heroicons invece di lucide-react
- ✅ Mobile-first approach (min-w-0, truncate)
- ✅ Duration 150-200ms per animazioni

---

## Come Testare

### Test Base
1. **Import componenti**:
   ```tsx
   import { ThreadListItem, ThreadExpandedView } from './components/ThreadList';
   ```

2. **ThreadListItem test**:
   ```tsx
   const thread: Thread = {
     id: '1',
     snippet: 'Preview text...',
     historyId: 'h1',
     messageCount: 3,
     messages: [
       { id: 'm1', threadId: '1', from: 'John', to: 'me', subject: 'Test',
         date: new Date().toISOString(), snippet: 'Hi...', labelIds: ['UNREAD'], internalDate: '' }
     ]
   };

   <ThreadListItem
     thread={thread}
     isSelected={false}
     onClick={() => console.log('clicked')}
     onExpand={() => console.log('expand')}
     isExpanded={false}
   />
   ```

3. **Verifica visivamente**:
   - Counter "(3)" appare se messageCount > 1
   - Chevron ruota on click
   - Unread dot appare se UNREAD label presente
   - Hover cambia background

### Test Expanded
```tsx
const [expandedIds, setExpandedIds] = useState<Set<string>>(new Set());

<ThreadExpandedView
  threadId="1"
  messages={thread.messages || []}
  expandedMessageIds={expandedIds}
  onToggleMessage={(id) => {
    const newSet = new Set(expandedIds);
    if (newSet.has(id)) newSet.delete(id);
    else newSet.add(id);
    setExpandedIds(newSet);
  }}
  onExpandAll={() => setExpandedIds(new Set(thread.messages?.map(m => m.id)))}
  onCollapseAll={() => setExpandedIds(new Set())}
/>
```

### Visual Checks
- [ ] Thread row height = 72px
- [ ] Chevron rotates smoothly (200ms)
- [ ] Ultimo messaggio auto-expanded
- [ ] Click message collapsed → expands
- [ ] Expand All / Collapse All buttons work
- [ ] Reply/Forward buttons visible (no action yet)

---

## Note per Guardiana

### Build Status
✅ TypeScript build passa senza errori

### Prossimi Step (non implementati)
- **AvatarStack component** - Per thread con 3+ partecipanti (specs sezione 1E)
- **Keyboard shortcuts** - j/k navigation, ;/: expand/collapse all (specs sezione 4)
- **Integrazione con API** - fetch messages on expand
- **Reply/Forward handlers** - collegare a compose modal
- **Loading skeletons** - durante fetch messaggi

### Limiti Attuali
- `onReply`/`onForward` props in ThreadExpandedView dichiarate ma non usate (placeholder)
- Message body usa `body || snippet` fallback (API potrebbe non caricare body)
- Avatar non implementato (solo from name as text)
- Focus management non implementato (specs sezione 6)

### Design Consistency
✅ Stesso design system di EmailListItem
✅ Stesse classi Tailwind (miracollo-*)
✅ Stesso pattern hover/selected
✅ Heroicons invece di lucide-react (consistente con codebase)

---

**Status**: ✅ MVP COMPLETO
**Time**: ~45 minuti
**Next**: Integrare in EmailList o creare ThreadList container separato

*Cervella Frontend - 14 Gennaio 2026*
