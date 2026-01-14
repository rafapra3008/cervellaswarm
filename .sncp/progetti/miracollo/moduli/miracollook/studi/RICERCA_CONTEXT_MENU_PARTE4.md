# RICERCA CONTEXT MENU - PARTE 4
> Best Practices UX/UI + Accessibility + Raccomandazioni Finali

---

## 13. BEST PRACTICES UX/UI (NIELSEN NORMAN GROUP)

### 10 Linee Guida per Context Menu Efficaci

Queste linee guida vengono da **Nielsen Norman Group**, leader mondiale in UX research.

---

#### 1. Usa per Azioni Secondarie, Non Critiche

```
✅ CORRETTO:
Context menu = Shortcut per azioni disponibili anche altrove
Es: "Reply" esiste sia come bottone che in context menu

❌ SBAGLIATO:
Context menu = UNICO modo per fare azione critica
Es: "Delete" SOLO in context menu (utente non lo trova!)
```

**RATIONALE:**
Molti utenti non sanno che esiste il tasto destro. Se un'azione è critica, deve essere visibile nell'UI principale.

**PER MIRACOLLOOK:**
- Tutte le azioni comuni devono avere bottoni visibili
- Context menu = convenienza per power users

---

#### 2. Posiziona Vicino al Contenuto che Modificano

```
✅ CORRETTO:
Right-click sull'email → Context menu appare vicino all'email

❌ SBAGLIATO:
Right-click sull'email → Context menu appare in angolo fisso schermo
```

**RATIONALE:**
Proximità rafforza il contesto e aiuta gli utenti a capire cosa il menu modificherà.

**IMPLEMENTAZIONE:**
```javascript
// Use event.clientX and event.clientY, NOT fixed position
const handleContextMenu = (event) => {
  showMenu({
    x: event.clientX,  // Mouse position
    y: event.clientY,
  });
};
```

---

#### 3. Assicura Visibilità con Dimensione e Contrasto

```
✅ CORRETTO:
- Font size: 14-16px
- Padding: 8-12px verticale
- Contrasto: WCAG AA minimo (4.5:1)
- Hover state chiaro e visibile

❌ SBAGLIATO:
- Font size: 10px (troppo piccolo!)
- Padding: 2px (troppo stretto!)
- Grigio chiaro su bianco (contrasto basso)
- Nessun hover state
```

**CSS RACCOMANDATO:**
```css
.context-menu-item {
  font-size: 14px;
  padding: 10px 16px;
  color: #1a1a1a; /* Contrasto alto */
  background: white;
  transition: background 150ms ease;
}

.context-menu-item:hover {
  background: #f0f0f0; /* Chiaro hover state */
}

.context-menu-item:focus {
  background: #e0e0e0;
  outline: 2px solid #0066cc; /* Focus visibile */
}
```

---

#### 4. Raggruppa Azioni Correlate e Context-Based

```
✅ CORRETTO:
┌─────────────────────────────────┐
│ Reply                           │  ← Reply actions group
│ Reply All                       │
│ Forward                         │
├─────────────────────────────────┤
│ Mark as Read                    │  ← Organize group
│ Star                            │
├─────────────────────────────────┤
│ Delete                          │  ← Destructive group
└─────────────────────────────────┘

❌ SBAGLIATO:
┌─────────────────────────────────┐
│ Reply                           │
│ Delete                          │  ← Mixing unrelated!
│ Star                            │
│ Forward                         │
│ Mark as Read                    │
└─────────────────────────────────┘
```

**RATIONALE:**
Grouping migliora:
- **Scannability** - Più veloce trovare opzioni
- **Memorability** - Posizioni spaziali aiutano memoria
- **Cognitive Load** - Meno sforzo per capire struttura

**SEPARATOR CSS:**
```css
.context-menu-separator {
  height: 1px;
  background: #e0e0e0;
  margin: 4px 0;
}
```

---

#### 5. Mantieni Rappresentazione e Comportamento Consistenti

```
✅ CORRETTO:
- Kebab icon (⋮) = SEMPRE context menu
- Stessa icona in tutta l'app
- Stesso comportamento ovunque

❌ SBAGLIATO:
- Kebab icon (⋮) = context menu in inbox
- Hamburger (☰) = context menu in settings
- Meatball (⋯) = context menu in compose
→ CONFUSIONE TOTALE!
```

**ICON USAGE:**

| Icon | Usage | NON usare per |
|------|-------|---------------|
| **☰ Hamburger** | Global navigation | Context actions |
| **⋮ Kebab** | Vertical item actions | Navigation |
| **⋯ Meatball** | Horizontal item actions | Navigation |

**REGOLA D'ORO:**
> "Un'icona, un significato, in tutta l'app."

---

#### 6. Usa Tooltip o Label per Chiarezza

```
✅ CORRETTO:
[⋮]  ← Hover tooltip: "Email actions" o "More options"

❌ SBAGLIATO:
[⋮]  ← Nessun tooltip, utente deve indovinare
```

**IMPLEMENTAZIONE:**
```jsx
<button
  aria-label="Email actions"
  title="Email actions" // Native tooltip
  onClick={showContextMenu}
>
  ⋮
</button>

// O con libreria tooltip custom
<Tooltip content="Email actions">
  <button onClick={showContextMenu}>⋮</button>
</Tooltip>
```

**NOTA:** Tooltip deve essere SPECIFICO, non generico!

```
✅ "Email actions"
✅ "Message options"
❌ "Options" (troppo generico!)
❌ "Menu" (ovvio, ma non informativo)
```

---

#### 7. Usa Icone per Azioni, Non per Espansione Contenuto

```
✅ CORRETTO:
[⋮] → Reply, Forward, Delete (AZIONI)

❌ SBAGLIATO:
[⋮] → Mostra resto dell'email (CONTENUTO)
→ Usa "Read more" o "Expand" invece!
```

**RATIONALE:**
Kebab/Meatball = strong mental model di "menu azioni".
Usarlo per espandere contenuto rompe questo model e confonde utenti.

---

#### 8. Evita Azioni Singole (o Pochissime)

```
❌ SBAGLIATO:
[⋮] → Solo "Delete"
→ Perché nascondere 1 azione dietro click extra?

✅ CORRETTO:
[🗑] → Bottone "Delete" diretto
→ Nessun menu intermedio!
```

**REGOLA:**
- **1-2 azioni:** Usa bottoni diretti
- **3-5 azioni:** Consider context menu
- **6+ azioni:** Context menu è appropriato

---

#### 9. Evita Hamburger per Context Menu

```
✅ CORRETTO:
☰ Hamburger = Main navigation (sidebar, drawer)
⋮ Kebab     = Context actions (item-specific)

❌ SBAGLIATO:
☰ Hamburger per aprire context menu su email
→ Confonde! Utenti si aspettano navigation!
```

**MENTAL MODELS:**

| Icon | User expectation |
|------|------------------|
| ☰ | "This opens navigation to other pages" |
| ⋮ | "This shows actions I can take on THIS item" |
| ⋯ | "Same as kebab, but horizontal" |

---

#### 10. Assicura Accessibilità Keyboard e Screen Reader

```
✅ CORRETTO:
- Tab/Shift+Tab per navigare menu
- Arrow keys per navigare items
- Enter/Space per attivare
- Escape per chiudere
- ARIA roles complete
- Focus visibile

❌ SBAGLIATO:
- Solo mouse support
- Nessun ARIA
- Focus invisibile
- Tab trap (non puoi uscire!)
```

**TESTING CHECKLIST:**

```
[ ] Naviga menu con Tab
[ ] Naviga items con Arrow keys
[ ] Attiva item con Enter
[ ] Chiudi con Escape
[ ] Screen reader annuncia tutto
[ ] Focus visibile sempre
[ ] Nessun tab trap
[ ] Type-ahead funziona (digita "r" → focus Reply)
```

---

## 14. DESIGN PATTERNS SPECIFICI EMAIL

### Pattern: Mark Read/Unread Toggle

```javascript
// PATTERN: Show only relevant state
function getMarkOption(email) {
  if (email.isRead) {
    return {
      id: 'mark-unread',
      label: 'Mark as Unread',
      icon: '✉️',
      action: () => markAsUnread(email.id),
    };
  } else {
    return {
      id: 'mark-read',
      label: 'Mark as Read',
      icon: '📭',
      action: () => markAsRead(email.id),
    };
  }
}
```

**PERCHÉ NON ENTRAMBI:**
- Saving space (menu più compatto)
- Reducing choices (paradox of choice)
- Clear action (no ambiguity)

---

### Pattern: Star/Flag Toggle

```javascript
// Gmail style: Star toggle
function getStarOption(email) {
  return {
    id: email.isStarred ? 'unstar' : 'star',
    label: email.isStarred ? 'Remove Star' : 'Add Star',
    icon: email.isStarred ? '☆' : '⭐',
    action: () => toggleStar(email.id),
  };
}

// Outlook style: Multiple flag colors
function getFlagSubmenu(email) {
  return {
    id: 'flag',
    label: 'Flag',
    icon: '🚩',
    submenu: [
      { id: 'flag-red', label: 'Red', color: '#ff0000' },
      { id: 'flag-orange', label: 'Orange', color: '#ff8800' },
      { id: 'flag-yellow', label: 'Yellow', color: '#ffdd00' },
      { id: 'flag-green', label: 'Green', color: '#00ff00' },
      { id: 'flag-blue', label: 'Blue', color: '#0088ff' },
      { type: 'separator' },
      { id: 'clear-flag', label: 'Clear Flag' },
    ],
  };
}
```

**SCELTA DESIGN:**
- **Gmail approach:** Simple, fast, one-click
- **Outlook approach:** Powerful, flexible, more clicks

Per **Miracollook:** Start con Gmail approach, add Outlook approach later se richiesto!

---

### Pattern: Delete with Confirmation

```javascript
// PATTERN 1: Immediate delete (Gmail style)
{
  id: 'delete',
  label: 'Delete',
  icon: '🗑',
  danger: true,
  action: () => deleteEmail(email.id),
}

// PATTERN 2: Confirm in menu
{
  id: 'delete',
  label: 'Delete',
  icon: '🗑',
  danger: true,
  action: () => {
    const confirmed = window.confirm('Delete this email?');
    if (confirmed) deleteEmail(email.id);
  },
}

// PATTERN 3: Undo toast (Gmail style)
{
  id: 'delete',
  label: 'Delete',
  icon: '🗑',
  danger: true,
  action: () => {
    deleteEmail(email.id);
    showToast({
      message: 'Email deleted',
      action: { label: 'Undo', onClick: () => undoDelete(email.id) },
      duration: 5000,
    });
  },
}
```

**RACCOMANDAZIONE:**
Pattern 3 (Undo toast) è il migliore:
- No interruption (no modal confirm)
- Safety net (undo disponibile)
- Fast workflow (no extra click)

---

### Pattern: Move to Folder

```javascript
// PATTERN 1: Submenu inline (Apple Mail style)
{
  id: 'move',
  label: 'Move to',
  icon: '📁',
  submenu: folders.map(folder => ({
    id: `move-${folder.id}`,
    label: folder.name,
    icon: folder.icon,
    action: () => moveEmail(email.id, folder.id),
  })),
}

// PATTERN 2: Modal picker (Gmail style)
{
  id: 'move',
  label: 'Move to',
  icon: '📁',
  shortcut: 'V',
  action: () => {
    openFolderPicker({
      onSelect: (folder) => moveEmail(email.id, folder.id),
    });
  },
}

// PATTERN 3: Search-based picker (Superhuman style)
{
  id: 'move',
  label: 'Move to',
  icon: '📁',
  shortcut: 'V',
  action: () => {
    openCommandPalette({
      mode: 'folders',
      onSelect: (folder) => moveEmail(email.id, folder.id),
    });
  },
}
```

**TRADE-OFFS:**

| Pattern | Pro | Contro |
|---------|-----|--------|
| Submenu | Fast (1 click), visual scanning | Breaks with many folders |
| Modal | Handles many folders, searchable | Extra step, slower |
| Command | Fast search, keyboard-friendly | Learning curve |

---

### Pattern: Reply Options

```javascript
// PATTERN 1: Flat (Gmail basic)
[
  { id: 'reply', label: 'Reply' },
  { id: 'reply-all', label: 'Reply All' },
  { id: 'forward', label: 'Forward' },
]

// PATTERN 2: Smart default (Outlook-inspired)
function getReplyOptions(email) {
  // If single recipient, no "Reply All" needed
  if (email.recipients.length === 1) {
    return [
      { id: 'reply', label: 'Reply' },
      { id: 'forward', label: 'Forward' },
    ];
  }

  // Multiple recipients
  return [
    { id: 'reply', label: 'Reply' },
    { id: 'reply-all', label: 'Reply All', default: true },
    { id: 'forward', label: 'Forward' },
  ];
}

// PATTERN 3: Submenu (Advanced)
{
  id: 'reply',
  label: 'Reply',
  submenu: [
    { id: 'reply', label: 'Reply to Sender' },
    { id: 'reply-all', label: 'Reply to All' },
    { id: 'reply-with-template', label: 'Reply with Template' },
    { id: 'reply-from-alias', label: 'Reply from Alias' },
  ],
}
```

**RACCOMANDAZIONE:**
Pattern 2 (Smart default) - Minimizza clutter senza perdere functionality!

---

## 15. STYLING E ANIMATIONS

### CSS Base Structure

```css
/* Container */
.context-menu {
  position: fixed;
  background: white;
  border: 1px solid #d0d0d0;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  padding: 4px 0;
  min-width: 180px;
  max-width: 280px;
  z-index: 9999;

  /* Smooth appearance */
  animation: menuFadeIn 150ms ease-out;
}

@keyframes menuFadeIn {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(-5px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

/* Menu Item */
.context-menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  font-size: 14px;
  color: #1a1a1a;
  cursor: pointer;
  transition: background 100ms ease;
  user-select: none;
}

.context-menu-item:hover,
.context-menu-item:focus {
  background: #f5f5f5;
  outline: none;
}

.context-menu-item:active {
  background: #e8e8e8;
}

/* Icon */
.context-menu-item .icon {
  font-size: 16px;
  width: 20px;
  text-align: center;
  flex-shrink: 0;
}

/* Label */
.context-menu-item .label {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Shortcut */
.context-menu-item .shortcut {
  font-size: 12px;
  color: #888;
  font-family: 'SF Mono', 'Monaco', monospace;
  opacity: 0.7;
}

/* Separator */
.context-menu-separator {
  height: 1px;
  background: #e8e8e8;
  margin: 4px 0;
}

/* Disabled State */
.context-menu-item[aria-disabled="true"] {
  color: #999;
  cursor: not-allowed;
  opacity: 0.5;
}

.context-menu-item[aria-disabled="true"]:hover {
  background: transparent;
}

/* Danger State (Delete, etc.) */
.context-menu-item.danger {
  color: #d32f2f;
}

.context-menu-item.danger:hover {
  background: #ffebee;
}

/* Focus visible (keyboard navigation) */
.context-menu-item:focus-visible {
  background: #e3f2fd;
  outline: 2px solid #1976d2;
  outline-offset: -2px;
}
```

### Dark Mode Support

```css
@media (prefers-color-scheme: dark) {
  .context-menu {
    background: #2a2a2a;
    border-color: #404040;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
  }

  .context-menu-item {
    color: #e0e0e0;
  }

  .context-menu-item:hover,
  .context-menu-item:focus {
    background: #383838;
  }

  .context-menu-item:active {
    background: #444;
  }

  .context-menu-separator {
    background: #444;
  }

  .context-menu-item[aria-disabled="true"] {
    color: #666;
  }

  .context-menu-item.danger {
    color: #ff5252;
  }

  .context-menu-item.danger:hover {
    background: #3a1f1f;
  }
}
```

### Animations Best Practices

```css
/* GOOD: Subtle, fast animation */
@keyframes menuFadeIn {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(-5px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

/* BAD: Too slow, distracting */
@keyframes menuSlideIn {
  from {
    opacity: 0;
    transform: translateX(-100px) rotate(-10deg);
  }
  to {
    opacity: 1;
    transform: translateX(0) rotate(0);
  }
}
```

**TIMING:**
- **Fast:** 100-150ms (hover states)
- **Medium:** 150-250ms (menu open/close)
- **Slow:** 300-500ms (page transitions)

Context menu = Medium timing (150-200ms ideale)

---

## 16. TESTING CHECKLIST

### Functional Testing

```
USER INTERACTIONS:
[ ] Right-click apre menu
[ ] Click outside chiude menu
[ ] Escape chiude menu
[ ] Click su item esegue azione
[ ] Click su item chiude menu
[ ] Disabled items non eseguono azione
[ ] Separator non è cliccabile

POSITIONING:
[ ] Menu near mouse cursor
[ ] Menu non esce fuori schermo (right edge)
[ ] Menu non esce fuori schermo (bottom edge)
[ ] Menu non esce fuori schermo (left edge) - raro
[ ] Menu non esce fuori schermo (top edge) - raro
[ ] Menu si posiziona correttamente in scroll container

DYNAMIC OPTIONS:
[ ] "Mark as Read" appare se email unread
[ ] "Mark as Unread" appare se email read
[ ] Options disabled quando non applicabili
[ ] Separators non appaiono se group vuoto
```

### Keyboard Testing

```
NAVIGATION:
[ ] Tab entra nel menu
[ ] Tab naviga tra items
[ ] Shift+Tab naviga indietro
[ ] Arrow Down naviga next item
[ ] Arrow Up naviga previous item
[ ] Home va a first item
[ ] End va a last item
[ ] Type-ahead funziona ("r" → Reply)

ACTIONS:
[ ] Enter attiva focused item
[ ] Space attiva focused item
[ ] Escape chiude menu
[ ] Disabled items non attivabili

FOCUS:
[ ] Focus entra in menu on open
[ ] Focus ritorna a trigger on close
[ ] Focus visibile (outline o background)
[ ] No tab trap (puoi sempre uscire)
```

### Accessibility Testing

```
SCREEN READER:
[ ] NVDA/JAWS legge "menu" role
[ ] Legge ogni menu item
[ ] Annuncia disabled state
[ ] Annuncia shortcut se presente
[ ] Annuncia separators (o li skippa)

ARIA:
[ ] role="menu" su container
[ ] role="menuitem" su items
[ ] role="separator" su separators
[ ] aria-label su menu
[ ] aria-disabled su disabled items
[ ] tabindex="-1" su items

CONTRAST:
[ ] Text vs background: 4.5:1 minimo
[ ] Disabled text vs background: 3:1 minimo
[ ] Focus indicator: 3:1 minimo

VISUAL:
[ ] Focus indicator visibile
[ ] Hover state chiaro
[ ] Active state chiaro
[ ] Funziona con Windows High Contrast
[ ] Funziona con Zoom (200%+)
```

### Cross-Browser Testing

```
BROWSERS:
[ ] Chrome (latest)
[ ] Firefox (latest)
[ ] Safari (latest)
[ ] Edge (latest)
[ ] Mobile Safari (iOS)
[ ] Chrome Mobile (Android)

FEATURES:
[ ] onContextMenu event fires
[ ] event.preventDefault() blocks native menu
[ ] Positioning corretto
[ ] Animations smooth
[ ] CSS Grid/Flexbox support
[ ] Portal rendering works
```

### Performance Testing

```
METRICS:
[ ] Menu apre < 100ms
[ ] No layout shift (CLS)
[ ] No janky animations (60fps)
[ ] Memory leaks check (long session)

LARGE LISTS:
[ ] Menu con 50+ items scorribile
[ ] Rendering performance accettabile
[ ] Keyboard navigation smooth
[ ] Search/filter funziona
```

---

## 17. RACCOMANDAZIONI FINALI PER MIRACOLLOOK

### Approccio Consigliato

**FASE 1: MVP - Context Menu Essenziale**

```javascript
// Opzioni minime necessarie
const mvpOptions = [
  // Reply group
  { id: 'reply', label: 'Reply', icon: '↩️', shortcut: 'R' },
  { id: 'reply-all', label: 'Reply All', icon: '↩️', shortcut: 'Shift+R' },
  { id: 'forward', label: 'Forward', icon: '➡️', shortcut: 'F' },

  { type: 'separator' },

  // Organize group
  { id: 'mark-read', label: 'Mark as Read', dynamic: true },
  { id: 'star', label: 'Add Star', dynamic: true },

  { type: 'separator' },

  // Action group
  { id: 'archive', label: 'Archive', icon: '📦', shortcut: 'E' },
  { id: 'delete', label: 'Delete', icon: '🗑', shortcut: 'Del', danger: true },
];
```

**IMPLEMENTAZIONE:**
- Custom React component (non library)
- Portal rendering
- Accessibility completa (ARIA + keyboard)
- Viewport bounds checking
- Dark mode support

**EFFORT:** 2-3 giorni development + 1 giorno testing

---

**FASE 2: Enhanced - Quick Actions Hover**

Aggiungi **hover actions** tipo Outlook:

```jsx
<EmailRow onMouseEnter={showQuickActions}>
  <EmailInfo />
  {showQuickActions && (
    <QuickActions>
      <IconButton icon="⭐" onClick={toggleStar} />
      <IconButton icon="📭" onClick={markRead} />
      <IconButton icon="🗑" onClick={deleteEmail} />
    </QuickActions>
  )}
</EmailRow>
```

**EFFORT:** 1-2 giorni

---

**FASE 3: Advanced - Command Palette**

Aggiungi **Cmd+K palette** tipo Superhuman:

```javascript
// Feature complete command palette
const commands = [
  // Email actions
  ...emailActions,

  // Navigation
  { id: 'go-inbox', label: 'Go to Inbox', shortcut: 'G I' },
  { id: 'go-sent', label: 'Go to Sent', shortcut: 'G S' },

  // Compose
  { id: 'compose', label: 'Compose Email', shortcut: 'C' },

  // Search
  { id: 'search', label: 'Search Emails', shortcut: '/' },

  // Settings
  { id: 'settings', label: 'Open Settings', shortcut: ',' },
];
```

**FEATURES:**
- Fuzzy search
- Context-aware scoring
- Alias system
- Keyboard shortcuts teaching
- Mobile gesture (two-finger tap)

**EFFORT:** 1-2 settimane

---

### Priorità Features

| Feature | Impact | Effort | Priority |
|---------|--------|--------|----------|
| Basic context menu | HIGH | Low (2-3d) | **P0** |
| Keyboard navigation | HIGH | Low (1d) | **P0** |
| Accessibility (ARIA) | HIGH | Medium (2d) | **P0** |
| Dynamic options | MEDIUM | Low (1d) | **P1** |
| Hover quick actions | MEDIUM | Low (1-2d) | **P1** |
| Shortcut display | LOW | Low (1d) | **P2** |
| Command palette | MEDIUM | High (1-2w) | **P2** |
| Submenu support | LOW | Medium (3-4d) | **P3** |

---

### Design Decisions

**STILE VISIVO:**

```
Ispirazione: Mix Apple Mail + Gmail

PERCHÉ:
- Apple Mail: Polish, animations, feel premium
- Gmail: Simplicity, clean, non-overwhelming

EVITARE:
- Outlook: Troppo busy, troppo complesso per MVP
- Superhuman: Troppo radicale (Command palette può alienare alcuni)
```

**OPZIONI MENU:**

```
START CON:
- Reply/Reply All/Forward
- Mark Read/Unread
- Star/Unstar
- Archive
- Delete

AGGIUNGERE POI:
- Move to folder
- Label as
- Snooze
- Block sender
- Report spam
```

**SHORTCUT VISIBILITY:**

```
✅ Mostra shortcut nel menu (tipo Outlook/Apple Mail)
❌ Non nascondere shortcut (tipo Gmail)

RATIONALE: Teaching users = long-term efficiency gain
```

---

### Technical Stack

**RACCOMANDAZIONE:**

```javascript
// Custom implementation, NOT library!

// Why?
// 1. Full control over UX/UI
// 2. Smaller bundle size
// 3. Deep integration with Miracollook state
// 4. Learning opportunity per il team

// Structure:
src/
  components/
    ContextMenu/
      ContextMenu.jsx         // Main component
      ContextMenuItem.jsx     // Item component
      useContextMenu.js       // Hook for state
      useKeyboardNav.js       // Keyboard handling
      useViewportBounds.js    // Positioning logic
      contextMenu.css         // Styles
      contextMenu.test.js     // Tests
```

**DEPENDENCIES:**

```json
{
  "react": "^18.0.0",
  "react-dom": "^18.0.0"
  // NO external context menu library!
}
```

---

### Metrics to Track

```javascript
// Analytics events
trackEvent('context_menu_opened', {
  trigger: 'right_click' | 'keyboard' | 'button',
  email_state: 'read' | 'unread',
});

trackEvent('context_menu_action', {
  action_id: 'reply' | 'forward' | 'delete' | ...,
  method: 'click' | 'keyboard',
  time_to_action: milliseconds,
});

trackEvent('context_menu_closed', {
  reason: 'action' | 'escape' | 'click_outside',
  duration_open: milliseconds,
});

// Aggregate metrics
- % of actions via context menu vs buttons
- Most used context menu options
- Average time to action
- Keyboard vs mouse usage ratio
```

Questi dati ti diranno SE il context menu è utile e QUALI opzioni sono importanti!

---

## CONCLUSIONE

### TL;DR

**COSA HO IMPARATO:**

1. **Gmail:** Simple, essenziale, veloce. Buono per MVP.
2. **Outlook:** Ricco, personalizzabile, potente. Buono per power users.
3. **Superhuman:** Command palette > context menu. Ottimo per enthusiasts.
4. **Apple Mail:** Native, polished, accessible. Ottimo esempio di polish.

**PATTERN COMUNI:**
- Reply/Forward sempre in alto
- Delete sempre in basso
- Separatori per grouping
- Context-aware opzioni (Read/Unread toggle)
- Shortcut visibili (tranne Gmail)

**IMPLEMENTAZIONE TECNICA:**
- onContextMenu event
- Portal rendering (body append)
- Viewport bounds checking
- ARIA roles completi
- Keyboard navigation full

**RACCOMANDAZIONE MIRACOLLOOK:**

```
MVP: Context menu essenziale (ispirato Gmail + Apple Mail polish)
  → 2-3 giorni development
  → Custom implementation
  → Accessibility completa
  → 8-10 opzioni core

Phase 2: Quick Actions hover (ispirato Outlook)
  → 1-2 giorni extra

Phase 3: Command Palette (ispirato Superhuman)
  → 1-2 settimane, consider MVP results first
```

**NEXT STEPS:**

1. ✅ Mostra questa ricerca a Rafa
2. 🎯 Decide insieme: MVP subito o Phase 1-2-3 completo?
3. 🎨 Se approve, Designer fa mockup visual
4. 💻 Backend/Frontend implementano
5. 🧪 Tester validano accessibility
6. 📊 Deploy + track metrics
7. 📈 Iterate based on user data

---

### FONTI

Questa ricerca si basa su:

**Documentazione Ufficiale:**
- [Gmail Context Menu - Google Support](https://support.google.com/mail/answer/16356082)
- [Outlook Quick Actions - Microsoft](https://learn.microsoft.com/en-us/answers/questions/4620041/outlook-item-list-email-quick-actions-options)
- [Apple Mail - Apple Support](https://support.apple.com/guide/mail/reply-to-or-forward-emails-mlhlp1010/mac)
- [Superhuman Keyboard Shortcuts](https://help.superhuman.com/hc/en-us/articles/45191759067411-Speed-Up-With-Shortcuts)

**UX Research:**
- [Nielsen Norman Group - Context Menu Guidelines](https://www.nngroup.com/articles/contextual-menus-guidelines/)
- [LogRocket - Creating Context Menus](https://blog.logrocket.com/ux-design/creating-context-menus/)
- [Height - Guide to Context Menus](https://height.app/blog/guide-to-build-context-menus)

**Technical Documentation:**
- [MDN - ARIA menu role](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/menu_role)
- [W3C - Menu Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/menubar/)
- [React Portal - React Docs](https://legacy.reactjs.org/docs/portals.html)

**Libraries:**
- [react-contexify](https://github.com/fkhadra/react-contexify)
- [use-context-menu](https://github.com/cluk3/use-context-menu)
- [@radix-ui/react-context-menu](https://www.npmjs.com/package/@radix-ui/react-context-menu)

**Blog Posts:**
- [Superhuman - How to Build a Remarkable Command Palette](https://blog.superhuman.com/how-to-build-a-remarkable-command-palette/)
- [Developer Way - Portals and Positioning](https://www.developerway.com/posts/positioning-and-portals-in-react)

---

**RICERCA COMPLETATA!**

*"Non esistono cose difficili, esistono cose non studiate!"*

*Cervella Researcher per Miracollook - 14 Gennaio 2026*
