# CONTEXT MENU - Design Specs Finale
> **Data:** 14 Gennaio 2026
> **Status:** APPROVATO - Ready for Implementation
> **Effort:** ~13h totali (3 sprint)

---

## DECISIONE

Implementare context menu (tasto destro) per Miracollook con **3 gruppi di opzioni**:
- Gruppo 1: Quick Actions (Reply, Forward, Archive, Star)
- Gruppo 2: Organize (Label, Move, Assign, Mark Read)
- Gruppo 3: **Hotel Actions** (Link Booking, Create Note, Guest Profile, Snooze)

**IL DIFFERENZIATORE:** Hotel Actions nel context menu = NESSUN competitor ha questo!

---

## PERCHE

1. **Gmail, Outlook, Superhuman** - tutti hanno context menu
2. **UX standard** - utenti si aspettano right-click per azioni
3. **Hotel workflow** - Link to Booking da context menu = GAME CHANGER
4. **Progressive disclosure** - menu mostra shortcuts → educa utenti

---

## MENU STRUCTURE FINALE

```
┌───────────────────────────────────────────────┐
│ GRUPPO 1: QUICK ACTIONS (80% frequenza)       │
├───────────────────────────────────────────────┤
│ ↩️  Reply                              R      │
│ ⤴️  Forward                            F      │
│ 📦 Archive                             E      │
│ ⭐ Star / Unstar                       S      │
├───────────────────────────────────────────────┤
│ GRUPPO 2: ORGANIZE (15% frequenza)            │
├───────────────────────────────────────────────┤
│ 🏷️  Add Label...                       L      │
│ 📁 Move to...                          V      │
│ 👥 Assign to Team...                   A      │
│ ✉️  Mark as Read / Unread              U      │
├───────────────────────────────────────────────┤
│ GRUPPO 3: HOTEL ACTIONS (5% freq - CRITICO!)  │
├───────────────────────────────────────────────┤
│ 🔗 Link to Booking                     ⌘B     │ <- AMBER!
│ 📝 Create Booking Note                 ⌘N     │ <- AMBER!
│ 👁️  View Guest Profile                 ⌘G     │ <- AMBER!
│ ⏰ Snooze until Check-in               Z      │
└───────────────────────────────────────────────┘

TOTALE: 12 opzioni (sweet spot UX)
```

---

## SPRINT PLAN

### Sprint 1 - Menu Base (3h)
```
[ ] ContextMenu component structure
[ ] Portal rendering (z-index safe)
[ ] Position logic (viewport bounds)
[ ] Quick Actions (Reply, Forward, Archive, Star)
[ ] Organize Actions (Label, Move, Assign, Mark Read)
[ ] Keyboard navigation (↑↓, Enter, Escape)
[ ] ARIA accessibility
```

### Sprint 2 - Hotel Actions (6h)
```
[ ] Hotel Actions group (amber styling!)
[ ] Link to Booking modal
[ ] Create Booking Note input
[ ] View Guest Profile (trigger sidebar)
[ ] Context-aware menu (email letta vs non letta)
[ ] Context-aware: email con allegati
[ ] Context-aware: email da ospite PMS
```

### Sprint 3 - Polish (4h)
```
[ ] Snooze until Check-in (smart date)
[ ] Save to Booking Files (allegati)
[ ] Escalate to Manager
[ ] Onboarding tooltip
[ ] Analytics tracking
[ ] User testing
```

---

## VISUAL SPECS

### Dimensions
- Width: 280px (fixed)
- Item height: 36px
- Border radius: 8px
- Shadow: 0 4px 12px rgba(0,0,0,0.15)

### Colors
```
DEFAULT:
- Background: white
- Text: gray-900
- Icon: gray-600

HOVER:
- Background: indigo-50
- Text: indigo-900

HOTEL ACTIONS (Gruppo 3):
- Icon color: amber-600 (gold!)
- Hover: amber-50
```

---

## CONTEXT-AWARE VARIANTS

| Contesto | Opzioni Speciali |
|----------|------------------|
| Email non letta | "Mark as Read" emphasis |
| Email già letta | "Mark as Unread" |
| Email con allegati | "Download All", "Save to Booking Files" |
| Email da ospite PMS | "Open Booking #X", "Add to Notes", "Guest Profile" |
| Email team assignment | "Add Comment", "Reassign", "Escalate" |

---

## FILES DA CREARE

```
frontend/src/components/EmailContextMenu/
├── EmailContextMenu.tsx          // Container + logic
├── ContextMenuItem.tsx           // Single item
├── ContextMenuSeparator.tsx      // Divider
├── useContextMenu.ts             // Hook (position, items)
└── contextMenuItems.ts           // Items configuration
```

---

## SUCCESS METRICS

| Metric | Target 1mo |
|--------|------------|
| Context menu usage | 40% actions |
| Hotel actions usage | 15% of menu |
| Time to action | < 2s |
| PMS app switches | -30% |

---

## RICERCHE CORRELATE

- `studi/RICERCA_CONTEXT_MENU.md` (Indice + 4 parti)
- `studi/CONTEXT_MENU_UX_STRATEGY.md` (UX completa)

---

*"I dettagli fanno SEMPRE la differenza!"*
*Fatto BENE > Fatto VELOCE*
