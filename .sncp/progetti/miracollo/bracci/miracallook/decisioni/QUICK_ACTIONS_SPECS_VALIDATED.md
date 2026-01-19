# Quick Actions & Keyboard Shortcuts - Specs UX Validated

**Data**: 13 Gennaio 2026
**Stratega**: Cervella Marketing
**Status**: ✅ VALIDATED - Ready for Frontend Implementation
**Progetto**: Miracollook Email Client (Hotel Workflow)

---

## Executive Summary UX

**DECISIONE FINALE:**
- Quick Actions: 4 azioni hover (Archive, Assign, Snooze, Flag)
- Keyboard Shortcuts: MVP set j/k/e/a/r/s (hotel-optimized)
- Design Pattern: Gmail-inspired right-aligned + Superhuman learning hints
- Mobile: NO hover, YES swipe gestures (Fase 2)
- Accessibility: WCAG 2.1 AA compliant, keyboard-first

**VALIDAZIONE:**
- Target User: Hotel reception staff, 70% mobile usage
- Critical Path: Triage email → Assign/Archive → Next
- Differenziatore: Assign action prioritario (non in altri email client)

---

## 1. Quick Actions - UX Specs

### 1.1 Azioni da Mostrare (Max 4)

| # | Azione | Icona Heroicons | Priority | Rationale | Shortcut |
|---|--------|----------------|----------|-----------|----------|
| 1 | **Assign to User** | `UserCircleIcon` (outline) | ⭐⭐⭐ | Hotel workflow CORE - assegna a receptionist/manager | `a` |
| 2 | **Archive** | `ArchiveBoxIcon` (outline) | ⭐⭐⭐ | Risolto = archivia (standard Gmail) | `e` |
| 3 | **Snooze** | `ClockIcon` (outline) | ⭐⭐ | Reminder per check-out guest, follow-up | `s` |
| 4 | **Flag/Star** | `StarIcon` (outline) | ⭐⭐ | VIP guest, urgent request | `f` |

**ELIMINATI dalla prima versione:**
- Delete (troppo rischioso, serve conferma → non quick action)
- Reply (apre editor → non instant action)
- Forward (idem)

**NOTA UX:**
- 4 azioni = massimo consigliato da NN/G (no cognitive overload)
- Assign PRIMA posizione (hotel differenziator)
- Mobile: icone + label (tablet), solo icone (desktop)

---

### 1.2 Posizionamento UI

**Pattern Scelto: Gmail Right-Aligned**

```
+----------------------------------------------------------------+
|  [Avatar] John Doe                              [Archive] [A] [Snooze] [Star]  |
|           Reservation Confirmation               (hover only)                  |
|           11:34 AM                                                             |
+----------------------------------------------------------------+
```

**Layout Desktop:**
- Posizione: Right side, sostituisce timestamp on hover
- Alignment: `flex justify-end items-center gap-1`
- Sempre visibile su hover (no dropdown, instant access)

**Layout Mobile/Tablet (Fase 2):**
- NO hover (touch devices)
- Swipe gestures: Left swipe = Archive, Right swipe = Assign
- Long press = mostra tutti i 4 button

---

### 1.3 Hover Behavior

**Timing Validato:**
| Evento | Timing | Rationale |
|--------|--------|-----------|
| Mouse enter → show actions | **200ms delay** | Previene accidental trigger durante scroll |
| Fade in animation | **150ms** | Smooth senza sluggishness |
| Mouse leave → hide actions | **Immediate** (0ms) | User ha già deciso di uscire |

**Implementation Pattern:**
```jsx
onMouseEnter → setTimeout(200ms) → setIsHovered(true)
onMouseLeave → clearTimeout + setIsHovered(false)
```

**CSS Transition:**
```css
.quick-actions {
  opacity: 0;
  transition: opacity 150ms ease-out;
}

.email-item:hover .quick-actions {
  opacity: 1;
  transition-delay: 200ms; /* Hover delay */
}
```

---

### 1.4 Icone & Stili

**Heroicons Mapping (v2 Outline):**
```jsx
import {
  UserCircleIcon,    // Assign
  ArchiveBoxIcon,    // Archive
  ClockIcon,         // Snooze
  StarIcon,          // Flag
} from '@heroicons/react/24/outline';
```

**Dimensioni:**
- Icon size: `w-5 h-5` (20px) - balance tra tap target e spazio
- Button padding: `p-1.5` (6px) - tap target totale = 32px (WCAG AA)
- Gap tra icone: `gap-1` (4px)

**Colori (Design Salutare Integration):**

| Stato | Colore | Token | Hex |
|-------|--------|-------|-----|
| **Default** | Gray 400 | `text-gray-400` | - |
| **Hover** | Miracollo Accent | `text-miracollo-accent` | #3B82F6 |
| **Active** | Accent dark | `text-miracollo-accent-dark` | #2563EB |
| **Focus** | Accent + ring | `ring-2 ring-miracollo-accent` | - |
| **Disabled** | Gray 300 | `text-gray-300 opacity-50` | - |

**ECCEZIONE - Star/Flag:**
- Unflagged: `text-gray-400` (outline)
- Flagged: `text-yellow-500 fill-yellow-500` (solid)

---

### 1.5 States Design

**Button States (per ogni action):**

```css
/* Default */
.quick-action-btn {
  @apply text-gray-400 hover:text-miracollo-accent
         transition-colors duration-150
         rounded p-1.5
         focus:outline-none focus:ring-2 focus:ring-miracollo-accent;
}

/* Hover */
.quick-action-btn:hover {
  @apply text-miracollo-accent bg-gray-50;
}

/* Active (click) */
.quick-action-btn:active {
  @apply text-miracollo-accent-dark bg-gray-100;
}

/* Focus (keyboard) */
.quick-action-btn:focus-visible {
  @apply ring-2 ring-miracollo-accent ring-offset-2;
}
```

**Loading State (durante API call):**
```jsx
<button disabled>
  <ClockIcon className="w-5 h-5 animate-spin text-gray-400" />
</button>
```

---

### 1.6 Accessibility (WCAG 2.1 AA)

**ARIA Labels (Dynamic):**
```jsx
<button
  aria-label={`Archive email from ${email.sender}: ${email.subject}`}
  onClick={() => handleArchive(email.id)}
  className="quick-action-btn"
>
  <ArchiveBoxIcon className="w-5 h-5" />
</button>
```

**Tooltip con Shortcut Hint:**
```jsx
<Tooltip content="Archive (e)" position="top">
  <ArchiveBoxIcon />
</Tooltip>
```

**Keyboard Navigation:**
- Tab: Focus su ogni quick action button
- Enter/Space: Trigger azione
- Escape: Esce dal focus
- Focus visible: Ring blue 2px

**Role Attributes:**
```jsx
<div role="toolbar" aria-label="Quick actions">
  <button role="button" aria-label="...">
</div>
```

---

## 2. Keyboard Shortcuts - UX Specs

### 2.1 MVP Shortcuts (Fase 1)

**VALIDATO per Hotel Workflow:**

| Shortcut | Azione | Priority | Rationale | Visual Hint |
|----------|--------|----------|-----------|-------------|
| `j` | Next email (older) | ⭐⭐⭐ | Standard Gmail/Superhuman | "↓ j" |
| `k` | Previous email (newer) | ⭐⭐⭐ | Standard Gmail/Superhuman | "↑ k" |
| `Enter` | Open email | ⭐⭐⭐ | Universal | "⏎ Open" |
| `Escape` | Close email / Back to list | ⭐⭐⭐ | Universal | "Esc Back" |
| `e` | Archive | ⭐⭐⭐ | Gmail standard | "e Archive" |
| `a` | **Assign to User** | ⭐⭐⭐ | **Hotel differenziator** | "a Assign" |
| `r` | Reply | ⭐⭐ | Gmail standard | "r Reply" |
| `s` | Snooze | ⭐⭐ | Custom (Gmail usa `b`) | "s Snooze" |
| `f` | Toggle Flag/Star | ⭐⭐ | Custom | "f Flag" |
| `c` | Compose new email | ⭐ | Gmail standard | "c Compose" |
| `Delete` | Delete email (con conferma!) | ⭐ | Universal | "Del Delete" |

**NOTA CRITICAL:**
- `a` = Assign (NON Reply All) - differenza da Gmail intenzionale
- `s` = Snooze (NON Star) - più utile per hotel workflow
- Delete richiede SEMPRE conferma modal (no instant delete)

---

### 2.2 Shortcuts Esclusi da MVP (Fase 2)

| Shortcut | Azione | Motivo Esclusione |
|----------|--------|-------------------|
| `Cmd+K` | Command Palette | Fase 2 - richiede search UI |
| `g + i` | Go to Inbox | Fase 2 - navigation complessa |
| `x` | Select email | Fase 2 - bulk actions |
| `Shift+j/k` | Select multiple | Fase 2 - bulk actions |
| `*+a` | Select all | Fase 2 - bulk actions |
| `/` | Search focus | Fase 2 - search implementation |

**Rationale UX:**
- MVP focus: Single email workflow (triage veloce)
- Bulk actions = Fase 2 (80% use case è single email)
- Command Palette = nice-to-have, non blocker

---

### 2.3 Learning Strategy (Superhuman-Inspired)

**Metodo: Progressive Disclosure**

**Step 1 - Week 1:**
Mostra solo:
- `j / k` navigation
- `e` archive
- `a` assign

**Step 2 - Week 2:**
Aggiungi:
- `r` reply
- `s` snooze
- `f` flag

**Step 3 - Week 3:**
Aggiungi:
- `c` compose
- `Enter` open
- `Escape` back

**UI Implementation:**

1. **Tooltip Hints (sempre visibili):**
   - Hover su icona → tooltip mostra shortcut
   - Es: "Archive (e)"

2. **Footer Bar (opzionale, Settings toggle):**
   ```
   +----------------------------------------------------------------+
   |  j/k: Navigate  |  e: Archive  |  a: Assign  |  r: Reply      |
   +----------------------------------------------------------------+
   ```
   - Posizione: Fixed bottom
   - Colore: Gray 100 background, Gray 600 text
   - Dismissible: X button + "Don't show again"

3. **Onboarding Modal (first login):**
   - Spotlight: "Speed up with shortcuts!"
   - Show 3 essenziali: j/k, e, a
   - CTA: "Try it now" (chiude modal, resta in list)

---

### 2.4 Conflicts Prevention

**Problema: Browser/OS shortcuts conflict**

| Shortcut | Conflict Potenziale | Soluzione |
|----------|---------------------|-----------|
| `c` | Chrome DevTools (Ctrl+C) | Solo quando focus su email list |
| `r` | Browser Refresh (Ctrl+R) | Solo quando focus su email list |
| `f` | Browser Find (Ctrl+F) | Solo quando focus su email list |
| `Delete` | Browser Back | `preventDefault()` + conferma modal |

**Implementation:**
```jsx
useEffect(() => {
  const handleKeyDown = (e) => {
    // Only if focus is on email list, not input field
    if (document.activeElement.tagName === 'INPUT') return;

    // Prevent browser defaults
    if (['e', 'r', 'c', 'f'].includes(e.key.toLowerCase())) {
      e.preventDefault();
    }

    // Execute action
    handleShortcut(e.key);
  };

  window.addEventListener('keydown', handleKeyDown);
  return () => window.removeEventListener('keydown', handleKeyDown);
}, []);
```

---

### 2.5 Visual Feedback

**Quando utente preme shortcut:**

1. **Instant Visual Feedback:**
   - Email row flash background: `bg-miracollo-accent-light` (100ms)
   - Icon animation: Scale 1.1 → 1 (150ms)

2. **Toast Notification (azioni irreversibili):**
   - Archive: "Email archived" + Undo button (5s)
   - Delete: Modal conferma (blocking)
   - Assign: "Assigned to [User]" + Undo (5s)

3. **Error State:**
   - API fail: Toast rosso "Action failed. Try again."
   - No connection: Toast arancione "No connection. Action queued."

**CSS Animation:**
```css
@keyframes flash-action {
  0% { background-color: transparent; }
  50% { background-color: rgba(59, 130, 246, 0.1); }
  100% { background-color: transparent; }
}

.email-item.action-flash {
  animation: flash-action 300ms ease-out;
}
```

---

## 3. Design Salutare Integration

### 3.1 Spacing System

**Tailwind Classes Validated:**

```jsx
<div className="
  group                          // Gruppo hover
  flex items-center              // Vertical align
  gap-4                          // Gap tra avatar e testo (16px)
  px-4 py-3                      // Padding email row
  hover:bg-gray-50               // Hover background
  cursor-pointer
  transition-colors duration-150
">
  {/* Avatar */}
  <div className="flex-shrink-0">
    <Avatar size="sm" />
  </div>

  {/* Email Content */}
  <div className="flex-1 min-w-0">
    <div className="flex items-center justify-between gap-4">
      <div className="flex-1 truncate">
        <p className="text-sm font-medium text-gray-900">
          {sender}
        </p>
        <p className="text-sm text-gray-500 truncate">
          {subject}
        </p>
      </div>

      {/* Quick Actions (right-aligned) */}
      <div className="
        flex items-center gap-1       // Gap tra icone
        opacity-0 group-hover:opacity-100  // Fade in on hover
        transition-opacity duration-150 delay-200  // 200ms delay
      ">
        {/* Assign */}
        <button className="quick-action-btn" aria-label="Assign">
          <UserCircleIcon className="w-5 h-5" />
        </button>

        {/* Archive */}
        <button className="quick-action-btn" aria-label="Archive">
          <ArchiveBoxIcon className="w-5 h-5" />
        </button>

        {/* Snooze */}
        <button className="quick-action-btn" aria-label="Snooze">
          <ClockIcon className="w-5 h-5" />
        </button>

        {/* Flag */}
        <button className="quick-action-btn" aria-label="Flag">
          <StarIcon className="w-5 h-5" />
        </button>
      </div>

      {/* Timestamp (hidden on hover) */}
      <div className="
        text-xs text-gray-400
        opacity-100 group-hover:opacity-0
        transition-opacity duration-150
      ">
        11:34 AM
      </div>
    </div>
  </div>
</div>
```

---

### 3.2 Animazioni Validate

**Principi:**
- Tutte le animazioni < 200ms (Design Salutare rule)
- Easing: `ease-out` per entrata, `ease-in` per uscita
- No animazioni durante scroll (performance)

**Animation Catalog:**

| Elemento | Animation | Duration | Easing |
|----------|-----------|----------|--------|
| Hover background | `background-color` | 150ms | ease-out |
| Quick actions fade in | `opacity` | 150ms | ease-out (+ 200ms delay) |
| Icon hover color | `color` | 150ms | ease-out |
| Button click scale | `transform: scale(0.95)` | 100ms | ease-in-out |
| Email flash (shortcut) | `background-color` | 300ms | ease-out |
| Focus ring | `box-shadow` | 150ms | ease-out |

---

### 3.3 Responsive Breakpoints

**Email List Layout:**

| Breakpoint | Layout | Quick Actions |
|------------|--------|---------------|
| **Mobile** (< 640px) | Stack vertical | Hidden (swipe Fase 2) |
| **Tablet** (640-1024px) | Flex horizontal | Icons + label (visible on hover) |
| **Desktop** (> 1024px) | Flex horizontal | Icons only (visible on hover) |

**Tailwind Implementation:**
```jsx
<div className="
  hidden sm:flex           // Hidden mobile, flex tablet+
  items-center gap-1
  opacity-0 group-hover:opacity-100
">
  {/* Icons */}
</div>

{/* Mobile: show timestamp always, no quick actions */}
<div className="sm:hidden text-xs text-gray-400">
  {timestamp}
</div>
```

---

## 4. Implementation Roadmap

### Sprint 1: Hover Actions (5 giorni)
**Goal:** Quick actions funzionanti desktop

- [ ] QuickActions component con 4 icone
- [ ] Hover delay 200ms (CSS transition-delay)
- [ ] onClick handlers (Archive, Assign, Snooze, Flag)
- [ ] Toast feedback per azioni
- [ ] ARIA labels + tooltips
- [ ] Responsive hide su mobile

**Output:** Email list con hover actions desktop-only

---

### Sprint 2: Keyboard Shortcuts (5 giorni)
**Goal:** Shortcuts j/k/e/a/r/s/f funzionanti

- [ ] `useKeyPress` hook
- [ ] `useListNavigation` hook (j/k navigation)
- [ ] Shortcuts actions (e/a/r/s/f)
- [ ] Focus management + scroll into view
- [ ] Visual feedback (flash animation)
- [ ] Conflict prevention (preventDefault)

**Output:** Full keyboard navigation funzionante

---

### Sprint 3: Learning & Polish (3 giorni)
**Goal:** User impara shortcuts facilmente

- [ ] Tooltip hints con shortcuts
- [ ] Footer bar opzionale (Settings toggle)
- [ ] Onboarding modal (first login)
- [ ] Settings: Enable/disable shortcuts
- [ ] Keyboard shortcuts cheat sheet (modal)

**Output:** UX completa con learning aids

---

### Sprint 4: Mobile & Touch (Fase 2 - 5 giorni)
**Goal:** Swipe gestures mobile

- [ ] Swipe left = Archive
- [ ] Swipe right = Assign
- [ ] Long press = Show all 4 actions
- [ ] Touch-friendly button size (min 44px)
- [ ] Haptic feedback (vibrazione)

**Output:** Mobile UX pari a desktop

---

## 5. File Structure

```
src/
├── components/
│   └── EmailList/
│       ├── EmailList.tsx              // List container + keyboard nav
│       ├── EmailItem.tsx              // Single email row
│       ├── QuickActions.tsx           // 4 action buttons
│       ├── QuickActionButton.tsx      // Reusable button component
│       └── styles.css                 // Animations custom
│
├── hooks/
│   ├── useKeyPress.ts                 // Single key detection
│   ├── useListNavigation.ts           // j/k navigation logic
│   ├── useHover.ts                    // Hover delay management
│   └── useKeyboardShortcuts.ts        // Global shortcuts orchestrator
│
├── constants/
│   └── shortcuts.ts                   // Shortcuts mapping centralized
│
└── utils/
    └── emailActions.ts                // Archive, assign, snooze logic
```

---

## 6. Success Metrics (Post-Launch)

**Adoption Rate:**
- % utenti che usano keyboard shortcuts (target: 40% entro 1 mese)
- % utenti che usano hover actions (target: 80% desktop users)

**Speed Metrics:**
- Tempo medio triage 1 email (target: < 5 secondi)
- Email archiviate/giorno per utente (target: +30% vs pre-shortcuts)

**Usability:**
- Accidental triggers rate (target: < 2%)
- Shortcut conflict reports (target: 0)
- Accessibility compliance (target: WCAG 2.1 AA 100%)

**Tracking:**
```js
analytics.track('quick_action_used', {
  action: 'archive',
  method: 'hover_click',
  email_id: email.id,
  timestamp: Date.now()
});

analytics.track('keyboard_shortcut_used', {
  shortcut: 'e',
  action: 'archive',
  email_id: email.id,
  timestamp: Date.now()
});
```

---

## 7. Testing Checklist

**Desktop:**
- [ ] Hover delay 200ms non causa accidental triggers
- [ ] Quick actions visibili on hover
- [ ] Timestamp nascosto on hover
- [ ] Keyboard shortcuts j/k navigation
- [ ] Shortcuts e/a/r/s/f funzionanti
- [ ] Focus indicators visibili
- [ ] Toast notifications corrette
- [ ] Modal conferma delete

**Accessibility:**
- [ ] Screen reader legge ARIA labels
- [ ] Tab navigation tra quick actions
- [ ] Focus visible su tutti elementi
- [ ] Keyboard-only workflow completo
- [ ] No focus trap
- [ ] Lighthouse Accessibility 100

**Cross-Browser:**
- [ ] Chrome (80% utenti)
- [ ] Safari (15% utenti)
- [ ] Firefox (5% utenti)
- [ ] Edge (test)

**Performance:**
- [ ] No lag con 1000+ email in list
- [ ] Smooth animations 60fps
- [ ] No memory leaks (long sessions)

---

## 8. Next Steps (Post-Validation)

1. **Frontend Implementation:**
   - Cervella Frontend riceve queste specs
   - Implementa Sprint 1 (hover actions)
   - Daily standup con Regina

2. **User Testing:**
   - Beta con 5 hotel staff (1 settimana)
   - Raccolta feedback shortcuts usati/ignorati
   - Iterazione su timing/colori se necessario

3. **Analytics Setup:**
   - Tracking shortcuts usage
   - Heatmap hover areas
   - Error rate monitoring

4. **Documentation:**
   - Keyboard shortcuts cheat sheet PDF
   - Video tutorial 2 min (registra Rafa)
   - In-app help tooltip

---

## Appendice: Color Tokens

**Miracollo Design System:**

```css
:root {
  /* Primary */
  --miracollo-accent: #3B82F6;           /* Blue 500 */
  --miracollo-accent-light: #DBEAFE;     /* Blue 100 */
  --miracollo-accent-dark: #2563EB;      /* Blue 600 */

  /* Neutrals */
  --gray-50: #F9FAFB;
  --gray-100: #F3F4F6;
  --gray-300: #D1D5DB;
  --gray-400: #9CA3AF;
  --gray-500: #6B7280;
  --gray-600: #4B5563;
  --gray-900: #111827;

  /* Semantic */
  --success: #10B981;    /* Green 500 */
  --error: #EF4444;      /* Red 500 */
  --warning: #F59E0B;    /* Amber 500 */

  /* Flag/Star */
  --star-yellow: #EAB308;  /* Yellow 500 */
}
```

---

## Firma UX

**Validato da:** Cervella Marketing
**Data:** 13 Gennaio 2026
**Status:** ✅ APPROVED - Ready for Frontend

**Prossimo Passaggio:** Handoff a Cervella Frontend per implementazione Sprint 1.

---

**FINE SPECS** ✅

*"I dettagli fanno SEMPRE la differenza!"*
*- Cervella Marketing*
