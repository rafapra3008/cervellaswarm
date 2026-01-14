# RICERCA CONTEXT MENU - PARTE 3
> Implementazione Tecnica React

---

## 6. IMPLEMENTAZIONE TECNICA REACT

### Overview

Implementare un context menu in React richiede gestire:

1. **Event Handling** - onContextMenu event
2. **Positioning** - Viewport bounds checking
3. **State Management** - Show/hide, selected item
4. **Keyboard Navigation** - Arrow keys, Enter, Escape
5. **Accessibility** - ARIA roles, focus management
6. **Portal Rendering** - Z-index e stacking context
7. **Click Outside** - Close quando click outside
8. **Dynamic Options** - Context-aware menu items

### Basic Implementation Pattern

```jsx
// ContextMenu.jsx - Basic structure
import React, { useState, useEffect, useRef } from 'react';
import ReactDOM from 'react-dom';

function ContextMenu({ x, y, options, onClose, onSelect }) {
  const menuRef = useRef(null);
  const [position, setPosition] = useState({ x, y });

  // Viewport bounds checking
  useEffect(() => {
    if (!menuRef.current) return;

    const menu = menuRef.current;
    const menuRect = menu.getBoundingClientRect();
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;

    let adjustedX = x;
    let adjustedY = y;

    // Check right edge
    if (x + menuRect.width > viewportWidth) {
      adjustedX = viewportWidth - menuRect.width - 10;
    }

    // Check bottom edge
    if (y + menuRect.height > viewportHeight) {
      adjustedY = viewportHeight - menuRect.height - 10;
    }

    // Check left edge (rare, but possible)
    if (adjustedX < 0) adjustedX = 10;

    // Check top edge (rare, but possible)
    if (adjustedY < 0) adjustedY = 10;

    setPosition({ x: adjustedX, y: adjustedY });
  }, [x, y]);

  // Click outside to close
  useEffect(() => {
    function handleClickOutside(event) {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        onClose();
      }
    }

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [onClose]);

  // Escape key to close
  useEffect(() => {
    function handleEscape(event) {
      if (event.key === 'Escape') {
        onClose();
      }
    }

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [onClose]);

  return ReactDOM.createPortal(
    <div
      ref={menuRef}
      role="menu"
      aria-label="Context menu"
      className="context-menu"
      style={{
        position: 'fixed',
        left: `${position.x}px`,
        top: `${position.y}px`,
        zIndex: 9999,
      }}
    >
      {options.map((option, index) => (
        <div
          key={option.id || index}
          role="menuitem"
          tabIndex={0}
          className="context-menu-item"
          onClick={() => {
            onSelect(option);
            onClose();
          }}
          onKeyDown={(e) => {
            if (e.key === 'Enter' || e.key === ' ') {
              e.preventDefault();
              onSelect(option);
              onClose();
            }
          }}
        >
          {option.icon && <span className="icon">{option.icon}</span>}
          <span className="label">{option.label}</span>
          {option.shortcut && (
            <span className="shortcut">{option.shortcut}</span>
          )}
        </div>
      ))}
    </div>,
    document.body
  );
}

export default ContextMenu;
```

### Usage Example

```jsx
// EmailList.jsx - Using the context menu
import React, { useState } from 'react';
import ContextMenu from './ContextMenu';

function EmailList() {
  const [contextMenu, setContextMenu] = useState(null);

  const handleContextMenu = (event, email) => {
    event.preventDefault(); // Prevent default browser menu

    setContextMenu({
      x: event.clientX,
      y: event.clientY,
      options: getMenuOptions(email),
    });
  };

  const getMenuOptions = (email) => {
    return [
      {
        id: 'reply',
        label: 'Reply',
        icon: '↩️',
        shortcut: 'R',
        action: () => replyToEmail(email),
      },
      {
        id: 'forward',
        label: 'Forward',
        icon: '➡️',
        shortcut: 'F',
        action: () => forwardEmail(email),
      },
      { id: 'separator-1', type: 'separator' },
      {
        id: 'mark',
        label: email.isRead ? 'Mark as Unread' : 'Mark as Read',
        icon: email.isRead ? '✉️' : '📭',
        action: () => toggleReadStatus(email),
      },
      { id: 'separator-2', type: 'separator' },
      {
        id: 'delete',
        label: 'Delete',
        icon: '🗑',
        shortcut: 'Del',
        action: () => deleteEmail(email),
        danger: true, // CSS class for red color
      },
    ];
  };

  return (
    <div>
      {emails.map((email) => (
        <div
          key={email.id}
          onContextMenu={(e) => handleContextMenu(e, email)}
        >
          {email.subject}
        </div>
      ))}

      {contextMenu && (
        <ContextMenu
          x={contextMenu.x}
          y={contextMenu.y}
          options={contextMenu.options}
          onClose={() => setContextMenu(null)}
          onSelect={(option) => option.action && option.action()}
        />
      )}
    </div>
  );
}
```

---

## 7. POSITIONING - VIEWPORT BOUNDS

### The Challenge

Il problema principale: menu vicino ai bordi dello schermo va fuori viewport!

```
┌────────────────────────────┐  ← Viewport
│                            │
│                            │
│                      [Email]  ← Right-click qui
│                            ┌──────────┐
│                            │ Reply    │
│                            │ Forward  │
└────────────────────────────│ Delete   │  ← Menu va FUORI!
                             └──────────┘
```

### Solution: getBoundingClientRect()

```javascript
function adjustPosition(x, y, menuWidth, menuHeight) {
  const viewport = {
    width: window.innerWidth,
    height: window.innerHeight,
  };

  let adjustedX = x;
  let adjustedY = y;

  // Check right overflow
  if (x + menuWidth > viewport.width) {
    // Flip to left side of cursor
    adjustedX = x - menuWidth;

    // Still overflows? Stick to right edge with padding
    if (adjustedX < 0) {
      adjustedX = viewport.width - menuWidth - 10;
    }
  }

  // Check bottom overflow
  if (y + menuHeight > viewport.height) {
    // Flip above cursor
    adjustedY = y - menuHeight;

    // Still overflows? Stick to bottom edge with padding
    if (adjustedY < 0) {
      adjustedY = viewport.height - menuHeight - 10;
    }
  }

  return { x: adjustedX, y: adjustedY };
}
```

### Advanced: Submenu Positioning

Per submenu la logica è più complessa:

```javascript
function getSubmenuPosition(parentItem, submenuWidth, submenuHeight) {
  const parentRect = parentItem.getBoundingClientRect();
  const viewport = {
    width: window.innerWidth,
    height: window.innerHeight,
  };

  // Default: Right side of parent
  let x = parentRect.right;
  let y = parentRect.top;

  // Check if submenu fits on right
  if (x + submenuWidth > viewport.width) {
    // Flip to left side
    x = parentRect.left - submenuWidth;
  }

  // Check if submenu fits vertically
  if (y + submenuHeight > viewport.height) {
    // Align bottom of submenu with bottom of parent
    y = parentRect.bottom - submenuHeight;
  }

  // Edge case: Too tall for viewport
  if (submenuHeight > viewport.height) {
    y = 10; // Stick to top with padding
    // Consider adding scrolling to submenu in this case
  }

  return { x, y };
}
```

### React Hook for Positioning

```javascript
// useContextMenuPosition.js
import { useState, useEffect } from 'react';

function useContextMenuPosition(initialX, initialY, menuRef) {
  const [position, setPosition] = useState({ x: initialX, y: initialY });

  useEffect(() => {
    if (!menuRef.current) return;

    const menuRect = menuRef.current.getBoundingClientRect();
    const adjustedPos = adjustPosition(
      initialX,
      initialY,
      menuRect.width,
      menuRect.height
    );

    setPosition(adjustedPos);
  }, [initialX, initialY, menuRef]);

  return position;
}

export default useContextMenuPosition;
```

---

## 8. KEYBOARD NAVIGATION

### Requirements (W3C WAI-ARIA)

Context menu DEVE supportare:

| Key | Action |
|-----|--------|
| `↓` | Focus next item (wrap to first if at end) |
| `↑` | Focus previous item (wrap to last if at start) |
| `Enter` | Activate focused item |
| `Space` | Activate focused item |
| `Escape` | Close menu |
| `Tab` | Focus next item (no wrap) |
| `Shift+Tab` | Focus previous item (no wrap) |
| `Home` | Focus first item |
| `End` | Focus last item |
| `→` | Open submenu (if exists) |
| `←` | Close submenu, focus parent |

### Implementation

```jsx
// KeyboardNavigableMenu.jsx
function KeyboardNavigableMenu({ options, onClose, onSelect }) {
  const [focusedIndex, setFocusedIndex] = useState(0);
  const itemRefs = useRef([]);

  useEffect(() => {
    // Focus first item on mount
    if (itemRefs.current[0]) {
      itemRefs.current[0].focus();
    }
  }, []);

  const handleKeyDown = (event) => {
    switch (event.key) {
      case 'ArrowDown':
        event.preventDefault();
        setFocusedIndex((prev) => {
          const next = (prev + 1) % options.length;
          itemRefs.current[next]?.focus();
          return next;
        });
        break;

      case 'ArrowUp':
        event.preventDefault();
        setFocusedIndex((prev) => {
          const next = prev === 0 ? options.length - 1 : prev - 1;
          itemRefs.current[next]?.focus();
          return next;
        });
        break;

      case 'Home':
        event.preventDefault();
        setFocusedIndex(0);
        itemRefs.current[0]?.focus();
        break;

      case 'End':
        event.preventDefault();
        const lastIndex = options.length - 1;
        setFocusedIndex(lastIndex);
        itemRefs.current[lastIndex]?.focus();
        break;

      case 'Enter':
      case ' ':
        event.preventDefault();
        const option = options[focusedIndex];
        if (option && !option.disabled) {
          onSelect(option);
          onClose();
        }
        break;

      case 'Escape':
        event.preventDefault();
        onClose();
        break;

      case 'Tab':
        // Allow default Tab behavior, but track focus
        if (event.shiftKey) {
          // Shift+Tab - previous
          setFocusedIndex((prev) => Math.max(0, prev - 1));
        } else {
          // Tab - next
          setFocusedIndex((prev) => Math.min(options.length - 1, prev + 1));
        }
        break;

      default:
        // Type-ahead: Focus first item starting with typed character
        if (event.key.length === 1) {
          const char = event.key.toLowerCase();
          const startIndex = (focusedIndex + 1) % options.length;

          for (let i = 0; i < options.length; i++) {
            const index = (startIndex + i) % options.length;
            const option = options[index];

            if (option.label.toLowerCase().startsWith(char)) {
              setFocusedIndex(index);
              itemRefs.current[index]?.focus();
              break;
            }
          }
        }
        break;
    }
  };

  return (
    <div
      role="menu"
      onKeyDown={handleKeyDown}
      className="context-menu"
    >
      {options.map((option, index) => (
        <div
          key={option.id}
          ref={(el) => (itemRefs.current[index] = el)}
          role="menuitem"
          tabIndex={-1}
          aria-disabled={option.disabled}
          className={`menu-item ${index === focusedIndex ? 'focused' : ''}`}
          onClick={() => {
            if (!option.disabled) {
              onSelect(option);
              onClose();
            }
          }}
        >
          {option.label}
        </div>
      ))}
    </div>
  );
}
```

### Type-Ahead Feature

Una feature spesso dimenticata ma **molto utile**:

```javascript
// Digita "r" → Focus su "Reply"
// Digita "d" → Focus su "Delete"
// Digita "m" → Focus su "Mark as Read"

// Implementation
function findNextMatchingItem(startIndex, char, items) {
  const lowerChar = char.toLowerCase();

  for (let i = 0; i < items.length; i++) {
    const index = (startIndex + i) % items.length;
    const item = items[index];

    if (item.label.toLowerCase().startsWith(lowerChar)) {
      return index;
    }
  }

  return startIndex; // No match, stay on current
}
```

---

## 9. ACCESSIBILITY (ARIA)

### Required ARIA Attributes

```jsx
<div
  role="menu"
  aria-label="Email actions"
  aria-orientation="vertical"
>
  <div
    role="menuitem"
    tabIndex={-1}
    aria-disabled={false}
  >
    Reply
  </div>

  <div role="separator" />

  <div
    role="menuitem"
    tabIndex={-1}
    aria-disabled={true}
  >
    Forward (unavailable)
  </div>

  <div
    role="menuitem"
    aria-haspopup="menu"
    aria-expanded={false}
    tabIndex={-1}
  >
    Move to
  </div>
</div>
```

### ARIA Roles Breakdown

| Role | Usage | Required Attributes |
|------|-------|---------------------|
| `menu` | Container menu | `aria-label` or `aria-labelledby` |
| `menuitem` | Standard menu item | `tabIndex="-1"` |
| `menuitemcheckbox` | Checkable item | `aria-checked` |
| `menuitemradio` | Radio button item | `aria-checked` |
| `separator` | Visual divider | None (decorative) |
| `group` | Group of items | `aria-label` (optional) |

### Focus Management

```javascript
// CORRECT: Menu manages focus internally
function ContextMenu() {
  const [focusedItem, setFocusedItem] = useState(0);

  // On mount, focus first item
  useEffect(() => {
    itemRefs.current[0]?.focus();
  }, []);

  // On arrow key, move focus
  const moveFocus = (direction) => {
    const nextIndex = direction === 'down'
      ? (focusedItem + 1) % items.length
      : focusedItem === 0 ? items.length - 1 : focusedItem - 1;

    setFocusedItem(nextIndex);
    itemRefs.current[nextIndex]?.focus();
  };

  // On close, return focus to trigger element
  const handleClose = () => {
    triggerRef.current?.focus();
    onClose();
  };

  return ...;
}
```

### Screen Reader Announcements

```jsx
// Use aria-live for dynamic updates
<div aria-live="polite" aria-atomic="true" className="sr-only">
  {announcement}
</div>

// Example announcements
setAnnouncement('Context menu opened. 5 actions available.');
setAnnouncement('Reply selected.');
setAnnouncement('Context menu closed.');
```

### Disabled Items Pattern

```jsx
// CORRECT: Keep item in DOM, disable and announce
<div
  role="menuitem"
  tabIndex={-1}
  aria-disabled={true}
  className="menu-item disabled"
  onClick={(e) => e.preventDefault()} // Prevent action
>
  Forward (no email selected)
</div>

// WRONG: Removing from DOM confuses screen readers
{!disabled && <div role="menuitem">Forward</div>}
```

---

## 10. REACT PORTAL PATTERN

### Why Use Portals?

Context menu deve essere renderizzato **fuori** dal parent component per evitare:

1. **Z-index issues** - Parent con `z-index: 1` limita child
2. **Overflow hidden** - Parent con `overflow: hidden` taglia menu
3. **Stacking context** - Parent con `position: relative` crea nuovo context

### Portal Implementation

```jsx
// ContextMenu.jsx
import ReactDOM from 'react-dom';

function ContextMenu({ children, x, y }) {
  const menuContent = (
    <div
      className="context-menu"
      style={{
        position: 'fixed', // NOT absolute!
        left: `${x}px`,
        top: `${y}px`,
        zIndex: 9999,
      }}
    >
      {children}
    </div>
  );

  // Render to body, not in parent hierarchy
  return ReactDOM.createPortal(
    menuContent,
    document.body
  );
}
```

### Portal with Custom Container

```jsx
// Create dedicated container for context menus
const portalRoot = document.getElementById('context-menu-root');

if (!portalRoot) {
  const div = document.createElement('div');
  div.id = 'context-menu-root';
  document.body.appendChild(div);
}

// Render to dedicated container
return ReactDOM.createPortal(
  menuContent,
  document.getElementById('context-menu-root')
);
```

### Z-Index Strategy

```css
/* z-index hierarchy for app */
:root {
  --z-base: 0;
  --z-dropdown: 1000;
  --z-modal: 2000;
  --z-popover: 3000;
  --z-tooltip: 4000;
  --z-context-menu: 9999; /* Highest! */
}

.context-menu {
  z-index: var(--z-context-menu);
  position: fixed;
}
```

---

## 11. DYNAMIC OPTIONS (CONTEXT-AWARE)

### Pattern: Options Factory

```javascript
// getContextMenuOptions.js
function getEmailContextOptions(email, userPermissions) {
  const options = [];

  // Always available
  options.push(
    { id: 'reply', label: 'Reply', icon: '↩️', shortcut: 'R' },
    { id: 'forward', label: 'Forward', icon: '➡️', shortcut: 'F' }
  );

  options.push({ type: 'separator' });

  // Dynamic: Read/Unread toggle
  if (email.isRead) {
    options.push({
      id: 'mark-unread',
      label: 'Mark as Unread',
      icon: '✉️',
    });
  } else {
    options.push({
      id: 'mark-read',
      label: 'Mark as Read',
      icon: '📭',
    });
  }

  // Dynamic: Star/Unstar toggle
  if (email.isStarred) {
    options.push({
      id: 'unstar',
      label: 'Remove Star',
      icon: '☆',
    });
  } else {
    options.push({
      id: 'star',
      label: 'Add Star',
      icon: '⭐',
    });
  }

  options.push({ type: 'separator' });

  // Conditional: Archive (only if not already archived)
  if (!email.isArchived) {
    options.push({
      id: 'archive',
      label: 'Archive',
      icon: '📦',
      shortcut: 'E',
    });
  }

  // Conditional: Delete (only if user has permission)
  if (userPermissions.canDelete) {
    options.push({
      id: 'delete',
      label: 'Delete',
      icon: '🗑',
      shortcut: 'Del',
      danger: true,
    });
  } else {
    // Show disabled
    options.push({
      id: 'delete',
      label: 'Delete (no permission)',
      icon: '🗑',
      disabled: true,
    });
  }

  return options;
}
```

### Pattern: Option Groups

```javascript
// Group options by category
function groupMenuOptions(flatOptions) {
  return [
    {
      group: 'Actions',
      items: flatOptions.filter(o => ['reply', 'forward'].includes(o.id)),
    },
    {
      group: 'Organize',
      items: flatOptions.filter(o => ['mark-read', 'star', 'archive'].includes(o.id)),
    },
    {
      group: 'Danger Zone',
      items: flatOptions.filter(o => o.danger),
    },
  ];
}
```

---

## 12. LIBRERIE REACT CONSIGLIATE

### react-contexify

**Pro:**
- ✅ Lightweight (3KB gzipped)
- ✅ Built-in animations
- ✅ Submenu support
- ✅ Dark mode
- ✅ TypeScript
- ✅ Viewport bounds auto-handling

**Cons:**
- ❌ Last update 3 years ago
- ❌ Limited customization

**Usage:**
```jsx
import { Menu, Item, Separator, useContextMenu } from 'react-contexify';

function MyComponent() {
  const { show } = useContextMenu({ id: 'menu-id' });

  const handleContextMenu = (event) => {
    show({ event });
  };

  return (
    <>
      <div onContextMenu={handleContextMenu}>Right-click me</div>

      <Menu id="menu-id">
        <Item onClick={handleReply}>Reply</Item>
        <Item onClick={handleForward}>Forward</Item>
        <Separator />
        <Item onClick={handleDelete}>Delete</Item>
      </Menu>
    </>
  );
}
```

### use-context-menu (Hook-based)

**Pro:**
- ✅ Modern hooks approach
- ✅ Full UI control
- ✅ A11y built-in
- ✅ Recently maintained

**Cons:**
- ❌ More setup required
- ❌ No built-in styling

**Usage:**
```jsx
import { useContextMenu } from 'use-context-menu';

function MyComponent() {
  const {
    bindMenu,
    bindMenuItems,
    useContextTrigger,
  } = useContextMenu();

  const { triggerContextMenu } = useContextTrigger({
    collect: () => ({ email: currentEmail }),
  });

  return (
    <>
      <div {...triggerContextMenu}>Right-click me</div>

      <nav {...bindMenu} className="my-menu">
        <button {...bindMenuItems}>Reply</button>
        <button {...bindMenuItems}>Forward</button>
      </nav>
    </>
  );
}
```

### @radix-ui/react-context-menu

**Pro:**
- ✅ Production-ready
- ✅ Perfect accessibility
- ✅ Unstyled (full control)
- ✅ Submenu support
- ✅ Active development

**Cons:**
- ❌ Larger bundle size
- ❌ More complex API

**Usage:**
```jsx
import * as ContextMenu from '@radix-ui/react-context-menu';

function MyComponent() {
  return (
    <ContextMenu.Root>
      <ContextMenu.Trigger>
        Right-click me
      </ContextMenu.Trigger>

      <ContextMenu.Portal>
        <ContextMenu.Content>
          <ContextMenu.Item onSelect={handleReply}>
            Reply
          </ContextMenu.Item>
          <ContextMenu.Item onSelect={handleForward}>
            Forward
          </ContextMenu.Item>
          <ContextMenu.Separator />
          <ContextMenu.Item onSelect={handleDelete}>
            Delete
          </ContextMenu.Item>
        </ContextMenu.Content>
      </ContextMenu.Portal>
    </ContextMenu.Root>
  );
}
```

### Comparison

| Library | Bundle Size | A11y | Customization | Maintenance |
|---------|-------------|------|---------------|-------------|
| **react-contexify** | 3KB | Good | Medium | Stale |
| **use-context-menu** | 2KB | Excellent | Full | Active |
| **@radix-ui** | 15KB | Perfect | Full | Active |
| **Custom (DIY)** | <1KB | Your effort | Full | Your effort |

### Raccomandazione

**Per Miracollook:**

```
PROTOTIPO VELOCE:
→ react-contexify (fast setup, good enough)

PRODUZIONE:
→ Custom implementation
  - Basato su pattern di questo documento
  - Pieno controllo su UX
  - Bundle size ottimale
  - Integrazione profonda con app

ALTERNATIVA:
→ @radix-ui/react-context-menu
  - Se hai tempo per styling
  - Se vuoi accessibility perfetta out-of-box
```

---

*Continua in PARTE 4...*
