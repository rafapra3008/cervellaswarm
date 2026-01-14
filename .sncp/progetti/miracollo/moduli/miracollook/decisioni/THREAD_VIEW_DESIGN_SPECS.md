# Thread View - Design Specifications

**Data:** 14 Gennaio 2026
**Cervella:** Marketing (UX/UI Strategy)
**Progetto:** Miracollook v2.3.0
**Per:** Cervella Frontend

---

## Executive Summary

Specifiche design complete per implementare Thread View in Miracollook, integrando best practices da Gmail/Superhuman con il design system esistente (dark mode, cyan accent #6366f1).

**Obiettivi:**
- ✅ Raggruppare email conversazioni in thread visuali
- ✅ Keyboard-first navigation (come Superhuman)
- ✅ Collapse/expand fluido con animazioni smooth
- ✅ Multi-avatar stacking per 3+ partecipanti
- ✅ Performance ottimale (lazy loading)

---

## 1. COLLAPSED THREAD ROW (Lista Email)

### Layout Completo

```
┌─────────────────────────────────────────────────────────────────────┐
│ [○] [Avatar/Stack] [●] Subject (5)                    [Date] [Star] │
│                        Preview snippet text...                       │
└─────────────────────────────────────────────────────────────────────┘
Height: 72px
```

### Componenti Dettagliati

#### A. Structure

| Elemento | Posizione | Dimensioni | Descrizione |
|----------|-----------|------------|-------------|
| **Checkbox** | Left: 16px | 20x20px | Bulk selection (show on hover) |
| **Avatar/Stack** | Left: 48px | 40x40px | Single avatar o stack se 3+ |
| **Unread Dot** | Left: 100px | 8x8px | Cyan dot se thread ha unread |
| **Subject** | Left: 116px | Auto | Font-weight: 500 (unread) / 400 (read) |
| **Counter** | Inline dopo subject | Auto | "(N)" gray badge |
| **Chevron** | Right of counter | 16x16px | ∨ icon, rotates on expand |
| **Date** | Right: 80px | Auto | Font-mono, muted |
| **Star** | Right: 16px | 20x20px | Toggle starred |

#### B. CSS Specifiche

```css
.thread-row {
  /* Layout */
  height: 72px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;

  /* Colors */
  background: var(--miracollo-bg-card); /* #1a1f35 */
  border-bottom: 1px solid var(--miracollo-border); /* #2d3654 */

  /* Interactions */
  cursor: pointer;
  transition: all 150ms ease;

  /* States */
  &:hover {
    background: var(--miracollo-bg-hover); /* #232942 */
  }

  &.selected {
    background: rgba(99, 102, 241, 0.1); /* Accent 10% */
    border-left: 2px solid var(--miracollo-accent); /* #6366f1 */
  }

  &.unread {
    .subject {
      font-weight: 500;
      color: var(--miracollo-text); /* #f8fafc */
    }
  }

  &.read {
    .subject {
      font-weight: 400;
      color: var(--miracollo-text-secondary); /* #94a3b8 */
    }
  }
}
```

#### C. Unread Indicator

```css
.unread-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--miracollo-accent); /* #6366f1 */
  flex-shrink: 0;

  /* Pulse animation quando new message */
  &.new {
    animation: pulse 2s ease-in-out;
  }
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.6; transform: scale(1.2); }
}
```

#### D. Message Counter Badge

```css
.message-counter {
  /* Typography */
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  font-weight: 500;

  /* Colors */
  color: var(--miracollo-text-muted); /* #64748b */

  /* Layout */
  display: inline-block;
  margin-left: 6px;

  /* Format: "(N)" */
  &::before { content: "("; }
  &::after { content: ")"; }
}
```

#### E. Chevron Icon

```css
.thread-chevron {
  width: 16px;
  height: 16px;
  color: var(--miracollo-text-muted);

  /* Rotation animation */
  transition: transform 200ms ease;
  transform: rotate(0deg); /* ∨ collapsed */

  &.expanded {
    transform: rotate(-180deg); /* ∧ expanded */
  }
}
```

### Avatar Stack (3+ Participants)

#### Layout

```
┌──────────────────┐
│ ┌─┐┌─┐┌─┐       │
│ │1││2││3│  +2   │  ← Max 3 visible + overflow
│ └─┘└─┘└─┘       │
└──────────────────┘
```

#### CSS Specifiche

```css
.avatar-stack {
  display: flex;
  align-items: center;
  position: relative;

  .avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: 2px solid var(--miracollo-bg-card);

    /* Overlap effect */
    margin-left: -12px;

    &:first-child {
      margin-left: 0;
    }

    /* Z-index decreasing */
    &:nth-child(1) { z-index: 3; }
    &:nth-child(2) { z-index: 2; }
    &:nth-child(3) { z-index: 1; }
  }

  .overflow-badge {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: var(--miracollo-bg-secondary);
    border: 2px solid var(--miracollo-bg-card);

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 12px;
    font-weight: 600;
    color: var(--miracollo-text-muted);

    margin-left: -12px;
  }
}

/* Hover effect - raise avatar */
.avatar-stack .avatar:hover {
  z-index: 10;
  transform: translateY(-4px) scale(1.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
  transition: all 150ms ease;
}
```

---

## 2. EXPANDED THREAD VIEW

### Layout Completo

```
┌──────────────────────────────────────────────────────────────────┐
│ THREAD HEADER                                                    │
│ Subject: Re: Booking Confirmation                                │
│ 5 messages · 3 participants                                      │
│ [Expand All] [Collapse All]                                      │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ MESSAGE 1 (Collapsed)                                            │
│ [Avatar] John Doe                               Jan 10, 2:30 PM │
│          This is the preview snippet...                          │
│          [Click to expand]                                       │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ MESSAGE 2 (Collapsed)                                            │
│ [Avatar] Jane Smith                             Jan 11, 9:15 AM │
│          Thanks for the quick response...                        │
│          [Click to expand]                                       │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ MESSAGE 3 (Expanded) ← Latest/Selected                          │
│ [Avatar] John Doe                               Jan 12, 4:45 PM │
│          ┌────────────────────────────────────────────────┐    │
│          │ Full message body content here...              │    │
│          │ Can include multiple paragraphs.               │    │
│          │                                                 │    │
│          │ > Quoted previous message                      │    │
│          └────────────────────────────────────────────────┘    │
│          [Reply] [Forward] [Archive] [...]                      │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Thread Header

```css
.thread-header {
  padding: 24px;
  background: var(--miracollo-bg-card);
  border-bottom: 2px solid var(--miracollo-border);

  .thread-subject {
    font-family: 'Outfit', sans-serif;
    font-size: 20px;
    font-weight: 600;
    color: var(--miracollo-text);
    margin-bottom: 8px;
  }

  .thread-meta {
    font-size: 13px;
    color: var(--miracollo-text-muted);
    margin-bottom: 16px;

    /* Format: "5 messages · 3 participants" */
    span:not(:last-child)::after {
      content: " · ";
      margin: 0 4px;
    }
  }

  .thread-actions {
    display: flex;
    gap: 12px;
  }
}
```

### Message Collapsed State

```css
.message-collapsed {
  padding: 16px 24px;
  background: var(--miracollo-bg-card);
  border-bottom: 1px solid var(--miracollo-border);
  cursor: pointer;

  display: flex;
  align-items: start;
  gap: 12px;

  transition: background 150ms ease;

  &:hover {
    background: var(--miracollo-bg-hover);
  }

  .message-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    flex-shrink: 0;
  }

  .message-header {
    flex: 1;
    min-width: 0;

    .sender-name {
      font-weight: 500;
      font-size: 14px;
      color: var(--miracollo-text);
      margin-bottom: 4px;
    }

    .message-date {
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      color: var(--miracollo-text-muted);
      float: right;
    }

    .message-snippet {
      font-size: 13px;
      color: var(--miracollo-text-secondary);

      /* Single line truncate */
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
  }
}
```

### Message Expanded State

```css
.message-expanded {
  padding: 24px;
  background: var(--miracollo-bg-card);
  border-bottom: 1px solid var(--miracollo-border);

  /* Highlight effect */
  box-shadow: inset 2px 0 0 var(--miracollo-accent);

  .message-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;

    .sender-info {
      display: flex;
      align-items: center;
      gap: 12px;

      .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
      }

      .sender-name {
        font-weight: 600;
        font-size: 15px;
        color: var(--miracollo-text);
      }

      .sender-email {
        font-size: 13px;
        color: var(--miracollo-text-muted);
      }
    }

    .message-date {
      font-family: 'JetBrains Mono', monospace;
      font-size: 13px;
      color: var(--miracollo-text-muted);
    }
  }

  .message-body {
    padding: 20px;
    background: var(--miracollo-bg-secondary);
    border-radius: 8px;

    font-size: 14px;
    line-height: 1.6;
    color: var(--miracollo-text-secondary);

    /* Quoted text styling */
    blockquote {
      border-left: 3px solid var(--miracollo-border);
      padding-left: 12px;
      margin: 12px 0;
      color: var(--miracollo-text-muted);
      font-style: italic;
    }
  }

  .message-actions {
    margin-top: 16px;
    display: flex;
    gap: 8px;

    button {
      padding: 8px 16px;
      border-radius: 6px;
      font-size: 13px;
      font-weight: 500;

      background: var(--miracollo-bg-hover);
      border: 1px solid var(--miracollo-border);
      color: var(--miracollo-text-secondary);

      transition: all 150ms ease;
      cursor: pointer;

      &:hover {
        background: var(--miracollo-accent);
        color: white;
        border-color: var(--miracollo-accent);
      }
    }
  }
}
```

### Collapse/Expand Animations

```css
/* Smooth height animation */
.message {
  overflow: hidden;
  transition: all 250ms cubic-bezier(0.4, 0, 0.2, 1);

  &.collapsing {
    height: 72px; /* Collapsed height */
  }

  &.expanding {
    height: auto;
  }
}

/* Fade in content */
.message-body {
  animation: fadeIn 200ms ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

---

## 3. STATES & INTERACTIONS

### A. Hover States

| Element | Default | Hover | Cursor |
|---------|---------|-------|--------|
| Thread row | bg-card | bg-hover | pointer |
| Message collapsed | bg-card | bg-hover | pointer |
| Message expanded | bg-card | (no change) | default |
| Chevron icon | muted | text-secondary | pointer |
| Avatar | normal | scale(1.1) + shadow | pointer |
| Action button | bg-hover | accent | pointer |

### B. Selected State

```css
.thread-row.selected,
.message.selected {
  /* Highlight border */
  border-left: 2px solid var(--miracollo-accent);

  /* Subtle background tint */
  background: rgba(99, 102, 241, 0.1);
}
```

### C. Loading State

```css
.thread-loading {
  .skeleton {
    background: linear-gradient(
      90deg,
      var(--miracollo-bg-secondary) 25%,
      var(--miracollo-bg-hover) 50%,
      var(--miracollo-bg-secondary) 75%
    );
    background-size: 200% 100%;
    animation: shimmer 1.5s infinite;
    border-radius: 4px;
  }
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

**Layout Skeleton:**
```html
<div class="thread-loading">
  <div class="skeleton" style="width: 40px; height: 40px; border-radius: 50%;"></div>
  <div class="skeleton" style="width: 70%; height: 16px;"></div>
  <div class="skeleton" style="width: 90%; height: 12px; margin-top: 8px;"></div>
</div>
```

### D. Unread Indicator nel Thread

**Problema:** Se thread ha 5 messaggi, 2 unread, come mostrarlo?

**Soluzione:** Badge counter differenziato

```css
.message-counter {
  /* Default: all read */
  color: var(--miracollo-text-muted);

  /* Unread present */
  &.has-unread {
    color: var(--miracollo-accent);
    font-weight: 600;

    /* Format: "(3 unread)" o "(3)" */
  }
}
```

**Visual:**
```
Subject (5)          ← All read, gray
Subject (2)          ← Has unread, cyan + bold
```

---

## 4. KEYBOARD SHORTCUTS

### Mapping Completo

| Key | Action | Context | Visual Feedback |
|-----|--------|---------|-----------------|
| `j` | Next thread | Thread list | Highlight next row |
| `k` | Previous thread | Thread list | Highlight prev row |
| `Enter` | Expand thread | Thread selected | Open thread view |
| `Esc` | Collapse thread | Thread expanded | Return to list |
| `;` | Expand all messages | Thread view | All messages open |
| `:` | Collapse all messages | Thread view | All messages collapsed |
| `r` | Reply to message | Message selected | Open compose modal |
| `f` | Forward message | Message selected | Open compose modal |
| `a` | Archive thread | Thread selected | Optimistic remove |
| `#` | Delete thread | Thread selected | Confirm modal |
| `s` | Star thread | Thread selected | Toggle star icon |
| `u` | Mark as unread | Thread selected | Toggle read status |

### Visual Feedback

```css
/* Keyboard focus ring */
.thread-row:focus-visible,
.message:focus-visible {
  outline: 2px solid var(--miracollo-accent);
  outline-offset: 2px;
  border-radius: 4px;
}

/* Keyboard hint tooltip */
.keyboard-hint {
  position: absolute;
  top: -28px;
  right: 8px;

  padding: 4px 8px;
  background: var(--miracollo-bg-secondary);
  border: 1px solid var(--miracollo-border);
  border-radius: 4px;

  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: var(--miracollo-text-muted);

  /* Show on focus */
  opacity: 0;
  pointer-events: none;
  transition: opacity 150ms ease;

  &.visible {
    opacity: 1;
  }
}
```

### Keyboard Shortcut Help Overlay

Integra con `CommandPalette.tsx` esistente:

```
Cmd+K → Command Palette
  → Type "thread"
    → "Expand all messages" (;)
    → "Collapse all messages" (:)
    → "Next thread" (j)
    → "Previous thread" (k)
```

---

## 5. RESPONSIVE BEHAVIOR

### Breakpoints

```css
/* Mobile: < 640px */
@media (max-width: 640px) {
  .thread-row {
    height: auto;
    padding: 12px;
    flex-direction: column;
    align-items: flex-start;
  }

  .message-counter {
    /* Move to new line on mobile */
    display: block;
    margin-top: 4px;
    margin-left: 0;
  }

  .thread-chevron {
    /* Fixed position on mobile */
    position: absolute;
    right: 16px;
    top: 16px;
  }

  .avatar-stack .avatar {
    width: 32px;
    height: 32px;
  }
}

/* Tablet: 640px - 1024px */
@media (min-width: 640px) and (max-width: 1024px) {
  .thread-row {
    height: 64px; /* Slightly smaller */
  }

  .message-expanded .message-body {
    padding: 16px; /* Reduce padding */
  }
}
```

### Mobile-Specific UX

**Touch Targets:**
- Min 44x44px for all clickable elements
- Increase padding on buttons

```css
@media (max-width: 640px) {
  .message-actions button {
    padding: 12px 20px; /* Larger touch area */
    min-height: 44px;
  }

  .thread-chevron {
    width: 24px;
    height: 24px; /* Larger for touch */
  }
}
```

**Swipe Gestures (Future Enhancement):**
- Swipe left → Archive thread
- Swipe right → Mark as read/unread

---

## 6. ACCESSIBILITY

### ARIA Labels

```html
<!-- Thread Row -->
<div
  role="button"
  aria-expanded="false"
  aria-label="Thread: Booking Confirmation, 5 messages, 2 unread, from John Doe"
  tabindex="0"
>
  ...
</div>

<!-- Message Collapsed -->
<div
  role="button"
  aria-expanded="false"
  aria-label="Message from John Doe, January 10 at 2:30 PM. Click to expand."
  tabindex="0"
>
  ...
</div>

<!-- Expand All Button -->
<button
  aria-label="Expand all messages in thread"
  aria-keyshortcuts=";"
>
  Expand All
</button>
```

### Focus Management

**Regola:** Quando thread si espande, focus va al primo messaggio

```typescript
function expandThread(threadId: string) {
  setExpandedThreads([...expandedThreads, threadId]);

  // Focus management
  nextTick(() => {
    const firstMessage = document.querySelector(
      `[data-thread-id="${threadId}"] .message:first-child`
    );
    firstMessage?.focus();
  });
}
```

### Screen Reader Announcements

```typescript
// Announce expand action
function announceExpand(messageCount: number) {
  const announcement = `Thread expanded. ${messageCount} messages.`;

  // Use aria-live region
  const liveRegion = document.getElementById('aria-live-region');
  liveRegion.textContent = announcement;
}
```

**HTML:**
```html
<div
  id="aria-live-region"
  aria-live="polite"
  aria-atomic="true"
  class="sr-only"
></div>
```

---

## 7. ANIMATIONS & TIMING

### Timing Functions

```css
:root {
  /* Fast interactions */
  --timing-fast: 150ms;
  --easing-fast: cubic-bezier(0.4, 0, 1, 1); /* ease-in */

  /* Normal interactions */
  --timing-normal: 250ms;
  --easing-normal: cubic-bezier(0.4, 0, 0.2, 1); /* ease-in-out */

  /* Slow, dramatic */
  --timing-slow: 400ms;
  --easing-slow: cubic-bezier(0.2, 0, 0, 1); /* ease-out */
}
```

### Animation Catalog

| Animation | Duration | Easing | Trigger |
|-----------|----------|--------|---------|
| **Thread expand** | 250ms | ease-in-out | Click thread row |
| **Chevron rotate** | 200ms | ease-in-out | Thread toggle |
| **Message expand** | 250ms | ease-in-out | Click message |
| **Hover scale** | 150ms | ease-in | Hover avatar |
| **Button hover** | 150ms | ease-in | Hover button |
| **Fade in body** | 200ms | ease-in | Message expand |
| **Skeleton shimmer** | 1500ms | linear infinite | Loading |

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 8. INTEGRATION CON EXISTING DESIGN

### Design System Compliance

**Utilizzo Tailwind Esistente:**

```tsx
// Thread row classes
className="
  h-18 px-4 py-4
  bg-miracollo-bg-card
  border-b border-miracollo-border
  hover:bg-miracollo-bg-hover
  transition-fast
  cursor-pointer
"

// Message counter
className="
  font-mono-data
  text-xs
  text-miracollo-text-muted
"

// Chevron icon
className="
  w-4 h-4
  text-miracollo-text-muted
  transition-normal
  rotate-0
  data-[expanded=true]:rotate-180
"

// Avatar
className="
  w-10 h-10
  rounded-full
  border-2 border-miracollo-bg-card
"

// Button
className="
  px-4 py-2
  rounded-md
  text-sm font-medium
  bg-miracollo-bg-hover
  border border-miracollo-border
  text-miracollo-text-secondary
  hover:bg-miracollo-accent
  hover:text-white
  hover:border-miracollo-accent
  transition-fast
"
```

### Existing Components to Reuse

| Component | File | Usage |
|-----------|------|-------|
| **EmailListItem** | `EmailListItem.tsx` | Base per ThreadListItem |
| **Avatar** | Create new `Avatar.tsx` | Avatar stacking |
| **Button** | Tailwind classes | Action buttons |
| **Skeleton** | Create utility | Loading states |

---

## 9. PERFORMANCE CONSIDERATIONS

### Lazy Loading Strategy

**Opzione 1: Viewport Intersection (Raccomandato)**

```typescript
const options = {
  root: null,
  rootMargin: '100px', // Preload 100px before visible
  threshold: 0.1
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      loadThreadMessages(entry.target.dataset.threadId);
    }
  });
}, options);

// Observe all thread rows
document.querySelectorAll('.thread-row').forEach(row => {
  observer.observe(row);
});
```

**Opzione 2: Virtual Scrolling (Se > 100 thread)**

Usa `react-window` o `@tanstack/react-virtual`:

```tsx
import { useVirtualizer } from '@tanstack/react-virtual';

function ThreadList({ threads }) {
  const parentRef = useRef(null);

  const virtualizer = useVirtualizer({
    count: threads.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 72, // Thread row height
    overscan: 5 // Render 5 extra rows
  });

  return (
    <div ref={parentRef} style={{ height: '100vh', overflow: 'auto' }}>
      {virtualizer.getVirtualItems().map(virtualRow => (
        <ThreadRow
          key={virtualRow.key}
          thread={threads[virtualRow.index]}
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: `${virtualRow.size}px`,
            transform: `translateY(${virtualRow.start}px)`
          }}
        />
      ))}
    </div>
  );
}
```

### Optimistic Updates

```typescript
// Archive thread immediately (before API)
function archiveThread(threadId: string) {
  // 1. Update UI immediately
  setThreads(threads.filter(t => t.id !== threadId));

  // 2. Call API in background
  api.archiveThread(threadId)
    .catch(error => {
      // 3. Rollback on error
      toast.error('Failed to archive. Undoing...');
      setThreads([...threads]); // Restore
    });
}
```

---

## 10. COMPONENTS STRUCTURE

### File Organization

```
src/components/Thread/
├── ThreadList.tsx              # Main container
├── ThreadListItem.tsx          # Single thread row (collapsed)
├── ThreadView.tsx              # Expanded thread container
├── ThreadHeader.tsx            # Subject, meta, actions
├── MessageCollapsed.tsx        # Message preview
├── MessageExpanded.tsx         # Full message view
├── AvatarStack.tsx             # Multi-avatar component
├── MessageCounter.tsx          # "(N)" badge
├── ThreadChevron.tsx           # Expand/collapse icon
└── types.ts                    # TypeScript interfaces
```

### TypeScript Interfaces

```typescript
// types.ts

interface Thread {
  id: string;
  subject: string;
  snippet: string;
  messageCount: number;
  unreadCount: number;
  participants: Participant[];
  lastMessageDate: Date;
  labels: string[];
  starred: boolean;
}

interface Message {
  id: string;
  threadId: string;
  from: EmailAddress;
  to: EmailAddress[];
  subject: string;
  date: Date;
  snippet: string;
  body?: string; // null se non ancora caricato
  labels: string[];
  isUnread: boolean;
}

interface Participant {
  name: string;
  email: string;
  avatar?: string;
}

interface ThreadViewState {
  expandedThreads: string[];
  expandedMessages: string[];
  selectedThread: string | null;
  selectedMessage: string | null;
}
```

---

## 11. ANTI-PATTERNS (NON FARE!)

### ❌ Don'ts

1. **Non auto-expand tutti i thread**
   - Performance killer
   - User overwhelm
   - Lazy load on-demand

2. **Non nascondere il chevron icon**
   - User deve vedere chiaramente come espandere
   - Deve essere > 16px (touch target)

3. **Non usare solo subject per threading**
   - False positives (vedi ricerca UX)
   - Usare email headers (Message-ID, References)

4. **Non mostrare tutti i partecipanti inline**
   - Max 3 avatars + overflow
   - Tooltip on hover per lista completa

5. **Non ignorare keyboard users**
   - Focus management critico
   - ARIA labels obbligatori

6. **Non dimenticare loading states**
   - Skeleton sempre visibile durante fetch
   - Spinner per azioni lente (> 300ms)

7. **Non fare expand animation troppo lenta**
   - Max 250ms
   - User perception: < 200ms = instant

8. **Non mescolare thread e messaggi singoli**
   - Vista consistente
   - Se messaggio singolo = thread con 1 msg

---

## 12. ACCEPTANCE CRITERIA

### Definition of Done

**Thread View è completo quando:**

- [ ] Thread collapsed mostra counter "(N)"
- [ ] Chevron icon visibile e ruota 180° on expand
- [ ] Click su thread row espande tutti i messaggi
- [ ] Avatar stacking funziona per 3+ partecipanti
- [ ] Messaggi in ordine cronologico (newest bottom)
- [ ] Keyboard shortcuts funzionano (j/k, ;/:)
- [ ] Hover states su tutti gli elementi interattivi
- [ ] Loading skeleton visibile durante fetch
- [ ] Unread indicator (cyan dot) visibile
- [ ] Expand/collapse animation smooth (250ms)
- [ ] Focus management corretto (ARIA compliant)
- [ ] Mobile responsive (touch targets 44x44px min)
- [ ] Performance: expand < 300ms perceived
- [ ] No layout shift durante animazioni

### Testing Checklist

**Manual Testing:**
- [ ] Espandi thread con 2 messaggi
- [ ] Espandi thread con 10+ messaggi
- [ ] Test keyboard navigation completa
- [ ] Test su mobile (touch)
- [ ] Test con screen reader (NVDA/VoiceOver)
- [ ] Test con prefers-reduced-motion
- [ ] Test loading state (network throttling)

**Visual Regression:**
- [ ] Screenshot collapsed state
- [ ] Screenshot expanded state (2 msg)
- [ ] Screenshot expanded state (5+ msg)
- [ ] Screenshot avatar stack (3, 4, 5+ participants)

---

## 13. ROADMAP IMPLEMENTAZIONE

### Phase 1: MVP (4h)
- [x] Ricerca completata
- [ ] ThreadListItem con counter badge
- [ ] Chevron icon + click handler
- [ ] ThreadView container basic
- [ ] MessageCollapsed component
- [ ] Chronological ordering

### Phase 2: Interactions (2h)
- [ ] Keyboard shortcuts (j/k, Enter, Esc)
- [ ] Expand/collapse animations
- [ ] Hover states completi
- [ ] Focus management

### Phase 3: Visual Polish (2h)
- [ ] Avatar stacking component
- [ ] Loading skeletons
- [ ] Unread indicators
- [ ] Mobile responsive

### Phase 4: Advanced (Future)
- [ ] Virtual scrolling (se needed)
- [ ] Swipe gestures mobile
- [ ] Thread actions menu (split/merge)
- [ ] AI thread summary card

**Total Estimate:** 8 hours MVP + 4 hours polish = **12 hours**

---

## 14. REFERENCES

### Design System
- Colors: `tailwind.config.js` → miracollo-* tokens
- Fonts: Inter (body), Outfit (headers), JetBrains Mono (data)
- Spacing: Tailwind default scale (4px base)

### Existing Components
- `EmailListItem.tsx` - Base pattern per ThreadListItem
- `CommandPalette.tsx` - Keyboard shortcuts reference
- `HelpModal.tsx` - Keyboard help overlay pattern

### Research
- [Thread View UX Research](./ricerche/THREAD_VIEW_UX_Research.md)
- [Gmail API Thread Management](./ricerche/20260114_THREAD_VIEW_API_Research.md)

---

## HANDOFF NOTES

**Per Cervella Frontend:**

Questo documento contiene TUTTE le specifiche per implementare Thread View. Segui l'ordine:

1. **Leggi TypeScript interfaces** (sezione 10) - crea `types.ts`
2. **Inizia con ThreadListItem** (sezione 1) - modifica EmailListItem esistente
3. **Aggiungi AvatarStack** (sezione 1E) - nuovo component riusabile
4. **Crea ThreadView** (sezione 2) - container espanso
5. **Implementa keyboard shortcuts** (sezione 4) - useKeyboard hook
6. **Aggiungi animations** (sezione 7) - CSS transitions
7. **Test accessibility** (sezione 6) - ARIA + focus

**Domande?**
- Design ambiguity → Chiedi a Marketing
- API integration → Chiedi a Backend
- Performance issues → Chiedi a Tester

**Design Token Quick Reference:**
```css
--miracollo-accent: #6366f1  /* Primary (cyan/indigo) */
--miracollo-bg-card: #1a1f35  /* Card background */
--miracollo-bg-hover: #232942  /* Hover state */
--miracollo-text: #f8fafc  /* Primary text */
--miracollo-text-muted: #64748b  /* Secondary text */
--miracollo-border: #2d3654  /* Borders */
```

---

**Fine Specs.**

*Cervella Marketing - 14 Gennaio 2026*
*"Ogni pixel deve contare. Ogni interazione deve essere fluida."*
