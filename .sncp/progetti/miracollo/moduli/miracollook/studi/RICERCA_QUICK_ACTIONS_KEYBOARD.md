# Ricerca: Quick Actions & Keyboard Shortcuts per Email List

**Data**: 13 Gennaio 2026
**Ricercatrice**: Cervella Researcher
**Progetto**: Miracollook (Email Client Hotel)
**Status**: ✅ Completata

---

## Executive Summary

Ho analizzato i pattern UX di Superhuman, Gmail, Apple Mail, Spark e Missive per quick actions e keyboard shortcuts. I dati mostrano convergenza su alcuni pattern fondamentali:

**TL;DR Raccomandazioni:**
- **Hover timing**: 150-200ms delay per azioni semplici (button states), 300-500ms per dropdown
- **Quick actions on hover**: Archive, Delete, Snooze, Star/Flag (max 4 azioni)
- **Keyboard shortcuts**: j/k navigation (standard de facto), e=archive, r=reply, c=compose
- **React implementation**: `useKeyPress` hook + `onMouseEnter` con `setTimeout` + ARIA labels

---

## 1. Quick Actions on Hover - Pattern dei Big Players

### 1.1 Gmail

**Pattern:**
- Hover su email → timestamp sostituito da icone azioni
- Azioni mostrate: Archive, Delete, Mark as read/unread, Snooze
- Posizione: Right-aligned, dove normalmente c'è la data/ora
- Disponibile in tutte e 3 le densità UI (Compact, Default, Comfortable)

**Pro:**
- Familiarità massima (utenti già lo conoscono)
- Non occupa spazio extra

**Contro:**
- Nasconde la data/ora (criticato da alcuni utenti)
- Non customizzabile oltre le 4 azioni base

**Fonte**: [Gmail Hover Actions](https://www.emailoverloadsolutions.com/blog/gmail-hover-actions), [Gmail Community](https://support.google.com/mail/thread/2975903)

---

### 1.2 Superhuman

**Pattern:**
- Hover sulle icone mostra keyboard shortcut relativo
- Command Palette (Cmd+K) = azione universale da ovunque
- Mobile: Swipe left per azioni rapide (1 secondo per "Done")
- Focus su velocità: ogni azione ha shortcut dedicato

**Filosofia:**
- "Keyboard-first" design
- Minimal mouse interaction
- Instant Reply con suggerimenti contestuali

**Differenziatore:**
- Mostra shortcut hints on hover (insegna all'utente)
- Command bar universale (Cmd+K) invece di menu tradizionali

**Fonte**: [Superhuman Help](https://help.superhuman.com/hc/en-us/articles/45191759067411-Speed-Up-With-Shortcuts), [Superhuman Review 2026](https://efficient.app/apps/superhuman)

---

### 1.3 Apple Mail (macOS)

**Pattern:**
- Swipe con trackpad (2 dita): Right = Mark read/unread, Left = Delete/Archive
- Short swipe = mostra button, Long swipe = esegue azione
- Hover notification mostra l'azione che verrà eseguita
- **LIMITAZIONE**: Non customizzabile (solo toggle Delete/Archive)

**Key Insight:**
- macOS ha MENO customization di iOS (frustrante per utenti)
- iOS app ha full swipe customization, macOS no

**Pattern hover:**
- Hover su notification → mostra azione che verrà eseguita

**Fonte**: [MacRumors Guide](https://www.macrumors.com/how-to/customize-apple-mail-inbox-gestures-ios-11/), [Canary Mail Blog](https://canarymail.io/blog/mac-mail-customize-swipe-actions)

---

### 1.4 Spark

**Pattern:**
- Command Center (Ctrl+K) agisce sull'email evidenziato in blu (hover)
- Pointer cambia apparenza su hover di toolbar
- Smart Inbox con prioritizzazione
- Trackpad swipe actions supportate

**Filosofia:**
- Riduzione distrazioni
- Email prioritization automatica

**Fonte**: [Spark Command Center](https://sparkmailapp.com/help/general/spark-command-center), [Spark Shortcuts](https://sparkmailapp.com/help/tips-tricks/use-keyboard-shortcuts)

---

### 1.5 Missive (Team Collaboration)

**Pattern:**
- Cmd+Shift+K apre assignment popup (quick action)
- Cmd+D = assign to self (ultra rapido)
- Supporta Gmail shortcuts nativi
- 83 keyboard shortcuts totali
- **Team features**: Assign to team/person, internal chat, real-time editing

**Quick Actions:**
- Assign, Close, Reopen conversations via keyboard
- Send & Archive in one button
- Drag-and-drop attachments

**Fonte**: [Missive Features](https://missiveapp.com/features), [Missive Shortcuts](https://usethekeyboard.com/missive/)

---

## 2. Keyboard Shortcuts - Standard de Facto

### 2.1 Navigazione Core (Universal)

| Shortcut | Azione | Derivazione |
|----------|--------|-------------|
| `j` | Next email (older) | Vim/Gmail standard |
| `k` | Previous email (newer) | Vim/Gmail standard |
| `o` o `Enter` | Open email | Gmail |
| `u` | Back to list | Gmail (undo/back) |
| `Escape` | Close/cancel | Universal |

**Nota**: j/k è il pattern dominante, usato in Gmail, Superhuman, Fastmail, eM Client

---

### 2.2 Azioni su Email (High-Impact)

| Shortcut | Azione | Priorità | Note |
|----------|--------|----------|------|
| `e` | Archive | ⭐⭐⭐ | Gmail, Superhuman |
| `#` o `Delete` | Delete | ⭐⭐⭐ | Gmail usa `#`, altri `Del` |
| `r` | Reply | ⭐⭐⭐ | Universal |
| `a` | Reply all | ⭐⭐ | Gmail |
| `f` | Forward | ⭐⭐ | Gmail |
| `c` | Compose new | ⭐⭐⭐ | Gmail, Superhuman |
| `s` | Star/Flag | ⭐⭐ | Gmail |
| `b` | Snooze | ⭐ | Gmail (newer) |

---

### 2.3 Selezione e Bulk Actions

| Shortcut | Azione | Note |
|----------|--------|------|
| `x` | Select email | Gmail |
| `*` + `a` | Select all | Gmail |
| `*` + `n` | Deselect all | Gmail |
| `Shift + j/k` | Select multiple | Common pattern |

---

### 2.4 Command Palette (Modern Pattern)

| Shortcut | Client | Funzione |
|----------|--------|----------|
| `Cmd+K` / `Ctrl+K` | Superhuman | Master command palette |
| `Ctrl+K` | Spark | Command Center |
| `/` | Gmail | Search focus |

**Best Practice**: Command Palette = fallback per shortcuts dimenticati

---

### 2.5 Learning Strategy (da Superhuman)

**Tip Bar**: Mostra shortcut hints in basso (abilitabile in Settings)
**Hover hints**: Icone mostrano shortcut relativo on hover
**Progressive disclosure**: Impara 3-5 shortcuts alla volta, non tutti insieme

**Calcoli**: Americani potrebbero risparmiare **8 giorni/anno** con keyboard shortcuts (fonte Gmail research)

**Fonte**: [Gmail Shortcuts Guide](https://www.getinboxzero.com/blog/post/gmail-shortcuts-cheat-sheet), [Superhuman Shortcuts](https://nickgray.net/superhuman/)

---

## 3. UX Patterns - Best Practices

### 3.1 Hover Timing - Research-Backed

| Tipo Azione | Delay Consigliato | Motivo | Fonte |
|-------------|-------------------|--------|-------|
| Button hover state | **150-200ms** | Previene color change accidentale durante movimento mouse | Nielsen Norman Group |
| Quick actions email | **150-200ms** | Balance tra reattività e accidental trigger | Best practice email clients |
| Dropdown menus | **300-500ms** | Previene "flickering" (60% siti non lo fa!) | Baymard Institute |
| Tooltip | **300-500ms** | User intent chiaro = mouse si ferma sull'elemento | NN/G |

**Key Insight**:
- Troppo veloce (< 100ms) = accidental activations, jarring UX
- Troppo lento (> 500ms) = sistema sluggish, utenti perdono pazienza
- **Best cue for intent**: Mouse actually STOPS on element

**Fonte**: [NN/G Timing Guidelines](https://www.nngroup.com/articles/timing-exposing-content/), [Baymard Dropdown Study](https://baymard.com/blog/dropdown-menu-flickering-issue)

---

### 3.2 Hover Animation - Smoothness

**CSS Transition consigliata**:
```css
.email-item {
  transition: background-color 150ms ease-out;
}

.quick-actions {
  opacity: 0;
  transition: opacity 200ms ease-in-out;
}

.email-item:hover .quick-actions {
  opacity: 1;
}
```

**Mobile**: Transitions < 200ms migliori su schermi piccoli

**Fonte**: [NN/G Animation Duration](https://www.nngroup.com/articles/animation-duration/)

---

### 3.3 Touch/Mobile Fallback

**Problemi:**
- Touch devices NON hanno true hover state
- Hover-only UI = inaccessibile su mobile

**Soluzioni:**
1. **Swipe gestures** (Apple Mail pattern): Right/Left swipe per azioni
2. **Always visible on mobile** (Gmail pattern): Mostra icone sempre su mobile
3. **Tap-and-hold** (alternative pattern): Long press mostra menu contestuale
4. **Hybrid**: Touch first tap = select (mostra actions), second tap = open

**Best Practice**: Non mettere info CRITICHE in hover-only state (tablet hazard)

**Fonte**: [React Hover Best Practices](https://www.rickyspears.com/technology/mastering-hover-events-in-react-a-comprehensive-guide-for-interactive-uis/)

---

### 3.4 Accessibility - WCAG Compliance

**Regole fondamentali:**

1. **Hover = Focus**: Ogni hover DEVE avere equivalente focus (keyboard users)
   ```jsx
   <div
     onMouseEnter={handleHover}
     onFocus={handleHover}
     onMouseLeave={handleLeave}
     onBlur={handleLeave}
   >
   ```

2. **ARIA Labels**: Descrizioni per screen readers
   ```jsx
   <button
     aria-label="Archive email from John Doe"
     aria-describedby="email-123-subject"
   >
   ```

3. **Role Attributes**:
   - Email list: `role="list"`
   - Email item: `role="listitem"` (ma attenzione: aria-label ignorato su listitem in alcuni SR)
   - Action buttons: `role="button"`, `tabIndex="0"`

4. **Focus visible**: Clear focus indicators (non solo `outline: none`!)

**Caveat listitem role**:
- `role="listitem"` è static role
- `aria-label` ignorato da molti screen reader (eccetto Talkback)
- Meglio usare `aria-describedby` con testo visibile

**Fonte**: [MDN ARIA Labels](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-label), [TPGi aria-describedby](https://www.tpgi.com/describing-aria-describedby/)

---

## 4. Implementazione React - Specs Tecniche

### 4.1 Hover State Management

**Approccio 1: React State (raccomandato per interazioni complesse)**

```jsx
import { useState, useCallback } from 'react';

function EmailItem({ email }) {
  const [isHovered, setIsHovered] = useState(false);
  const [hoverTimer, setHoverTimer] = useState(null);

  const handleMouseEnter = useCallback(() => {
    // Delay 200ms prima di mostrare actions
    const timer = setTimeout(() => {
      setIsHovered(true);
    }, 200);
    setHoverTimer(timer);
  }, []);

  const handleMouseLeave = useCallback(() => {
    // Clear timer se utente esce prima
    if (hoverTimer) {
      clearTimeout(hoverTimer);
    }
    setIsHovered(false);
  }, [hoverTimer]);

  return (
    <div
      className="email-item"
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      onFocus={handleMouseEnter} // Accessibility!
      onBlur={handleMouseLeave}
      tabIndex={0}
      role="article"
      aria-label={`Email from ${email.sender}: ${email.subject}`}
    >
      <div className="email-content">{/* ... */}</div>

      {isHovered && (
        <div className="quick-actions" role="toolbar" aria-label="Quick actions">
          <button aria-label="Archive">Archive</button>
          <button aria-label="Delete">Delete</button>
          <button aria-label="Snooze">Snooze</button>
        </div>
      )}
    </div>
  );
}
```

**Approccio 2: CSS-only (raccomandato per hover semplici)**

```css
.email-item .quick-actions {
  opacity: 0;
  pointer-events: none;
  transition: opacity 200ms ease-in-out;
}

.email-item:hover .quick-actions,
.email-item:focus-within .quick-actions {
  opacity: 1;
  pointer-events: auto;
  transition-delay: 200ms; /* Hover delay */
}
```

**Quando usare cosa:**
- CSS-only: Semplici fade in/out, no logic
- React state: Tracking analytics, condizional logic, animazioni complesse

**Fonte**: [React Hover Events Guide](https://plainenglish.io/blog/how-to-handle-mouse-hover-events-in-react), [React Aria useHover](https://react-spectrum.adobe.com/react-aria/useHover.html)

---

### 4.2 Keyboard Navigation - Hook Pattern

**Custom Hook: `useKeyPress`**

```jsx
import { useState, useEffect } from 'react';

const useKeyPress = (targetKey) => {
  const [keyPressed, setKeyPressed] = useState(false);

  useEffect(() => {
    const downHandler = ({ key }) => {
      if (key === targetKey) {
        setKeyPressed(true);
      }
    };

    const upHandler = ({ key }) => {
      if (key === targetKey) {
        setKeyPressed(false);
      }
    };

    window.addEventListener('keydown', downHandler);
    window.addEventListener('keyup', upHandler);

    return () => {
      window.removeEventListener('keydown', downHandler);
      window.removeEventListener('keyup', upHandler);
    };
  }, [targetKey]);

  return keyPressed;
};
```

**Hook per List Navigation: `useListNavigation`**

```jsx
import { useReducer, useEffect } from 'react';

const initialState = { selectedIndex: 0 };

const reducer = (state, action) => {
  const { listLength } = action;

  switch (action.type) {
    case 'arrowDown':
    case 'j':
      return {
        selectedIndex: state.selectedIndex !== listLength - 1
          ? state.selectedIndex + 1
          : 0, // Wrap to first
      };
    case 'arrowUp':
    case 'k':
      return {
        selectedIndex: state.selectedIndex !== 0
          ? state.selectedIndex - 1
          : listLength - 1, // Wrap to last
      };
    case 'select':
      return { selectedIndex: action.payload };
    case 'home':
      return { selectedIndex: 0 };
    case 'end':
      return { selectedIndex: listLength - 1 };
    default:
      throw new Error(`Unhandled action type: ${action.type}`);
  }
};

function useListNavigation(listLength) {
  const [state, dispatch] = useReducer(reducer, initialState);

  useEffect(() => {
    const handleKeyDown = (e) => {
      const key = e.key.toLowerCase();

      // Prevent default scroll behavior
      if (['arrowdown', 'arrowup', 'j', 'k'].includes(key)) {
        e.preventDefault();
      }

      dispatch({
        type: key === 'arrowdown' ? 'arrowDown' :
              key === 'arrowup' ? 'arrowUp' :
              key === 'j' ? 'j' :
              key === 'k' ? 'k' :
              key === 'home' ? 'home' :
              key === 'end' ? 'end' : null,
        listLength
      });
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [listLength]);

  return [state.selectedIndex, dispatch];
}
```

**Usage:**

```jsx
function EmailList({ emails }) {
  const [selectedIndex, dispatch] = useListNavigation(emails.length);
  const downPressed = useKeyPress('e'); // Archive
  const deletePressed = useKeyPress('Delete');

  // Archive on 'e' press
  useEffect(() => {
    if (downPressed) {
      handleArchive(emails[selectedIndex]);
    }
  }, [downPressed, selectedIndex]);

  return (
    <div role="list" aria-label="Email list">
      {emails.map((email, idx) => (
        <EmailItem
          key={email.id}
          email={email}
          isSelected={idx === selectedIndex}
          onClick={() => dispatch({ type: 'select', payload: idx })}
        />
      ))}
    </div>
  );
}
```

**Fonte**: [whereisthemouse.com React List Navigation](https://whereisthemouse.com/create-a-list-component-with-keyboard-navigation-in-react), [GitHub use-keyboard-list-navigation](https://github.com/dzucconi/use-keyboard-list-navigation)

---

### 4.3 Focus Management - Best Practices

**Principi:**

1. **Focus visible**: Selected item deve avere chiaro focus indicator
2. **Scroll into view**: Auto-scroll quando navighi con keyboard
3. **Focus trap**: No focus trap nella list (deve poter uscire con Tab)

```jsx
function EmailItem({ email, isSelected }) {
  const itemRef = useRef(null);

  useEffect(() => {
    if (isSelected && itemRef.current) {
      // Scroll into view quando selected via keyboard
      itemRef.current.scrollIntoView({
        behavior: 'smooth',
        block: 'nearest',
      });

      // Focus per accessibility
      itemRef.current.focus();
    }
  }, [isSelected]);

  return (
    <div
      ref={itemRef}
      tabIndex={isSelected ? 0 : -1}
      className={isSelected ? 'selected' : ''}
      aria-selected={isSelected}
    >
      {/* ... */}
    </div>
  );
}
```

**CSS Focus Styles:**

```css
.email-item:focus-visible {
  outline: 2px solid var(--focus-color);
  outline-offset: 2px;
}

/* Non rimuovere outline senza alternativa! */
.email-item:focus {
  /* Fornisci sempre feedback visivo */
  background-color: var(--focus-bg);
}
```

**Fonte**: [FreeCodeCamp Keyboard Accessibility](https://www.freecodecamp.org/news/designing-keyboard-accessibility-for-complex-react-experiences/)

---

### 4.4 Libraries Raccomandate

**Per Keyboard Navigation:**
- `use-keyboard-list-navigation` (GitHub): Lightweight, well-tested
- `react-aria` (`useListBox`, `useOption`): Adobe, full accessibility
- `@react-aria/focus` (`useFocusRing`, `useFocusManager`): Focus management pro

**Per Focus Trap (modals):**
- `focus-trap-react`: Standard, escape key handling built-in
- `react-focus-lock`: Alternative, più customizable

**Per Hover Detection:**
- `react-use` (`useHoverDirty`, `useHover`): Hook utilities
- `@react-aria/interactions` (`useHover`): Adobe, touch-aware

**Raccomandazione**: Inizia con custom hooks (controllo totale), passa a library se complessità aumenta.

**Fonte**: [NPM react-keyboard-navigation](https://www.npmjs.com/package/react-keyboard-navigation), [React Aria](https://react-spectrum.adobe.com/react-aria/)

---

## 5. Raccomandazione per Miracollook

### 5.1 Quick Actions (Hover)

**Azioni da mostrare** (max 4 per non sovraccaricare):

| Azione | Icona | Priority | Shortcut | Hotel Use Case |
|--------|-------|----------|----------|----------------|
| **Archive** | `📥` | ⭐⭐⭐ | `e` | Risolto, archivia |
| **Assign to User** | `👤` | ⭐⭐⭐ | `a` | Assegna a receptionist |
| **Snooze/Follow-up** | `⏰` | ⭐⭐⭐ | `s` | Reminder per guest check-out |
| **Flag/Star** | `⭐` | ⭐⭐ | `f` | Email VIP guest |

**Pattern UI:**
- Posizione: Right-aligned (come Gmail)
- Hover delay: **200ms** (balance tra reattività e accidents)
- Fade in: 150ms ease-out
- Icons only on desktop, icons + label su tablet
- Mobile: Swipe gestures (no hover)

---

### 5.2 Keyboard Shortcuts (Fase 1 - MVP)

**Core Navigation:**
- `j` / `k` - Next/Previous email (standard)
- `Enter` - Open email
- `Escape` - Close email / Back to list
- `g` + `i` - Go to Inbox (Superhuman pattern)

**Core Actions:**
- `e` - Archive (Gmail)
- `a` - Assign to user (custom per hotel)
- `r` - Reply
- `s` - Snooze
- `c` - Compose new
- `Delete` - Delete email

**Command Palette** (Fase 2):
- `Cmd+K` / `Ctrl+K` - Universal command search

---

### 5.3 Implementation Roadmap

**Sprint 1: Hover Actions**
- [ ] `useHover` hook con 200ms delay
- [ ] QuickActions component (Archive, Assign, Snooze, Flag)
- [ ] CSS transitions smooth
- [ ] ARIA labels per accessibility
- [ ] Mobile: Hide hover, prepare per swipe gestures

**Sprint 2: Keyboard Navigation**
- [ ] `useKeyPress` hook (j, k, e, r, s, c, Delete)
- [ ] `useListNavigation` hook con circular navigation
- [ ] Focus management con `scrollIntoView`
- [ ] Visual focus indicators (outline, background)
- [ ] Prevent default scroll on arrow keys

**Sprint 3: Advanced Features**
- [ ] Command Palette (Cmd+K)
- [ ] Keyboard hints tooltip (insegna shortcuts)
- [ ] Settings: Enable/disable shortcuts
- [ ] Analytics: Track shortcut usage

**Sprint 4: Mobile & Touch**
- [ ] Swipe gestures (left/right)
- [ ] Touch-friendly action buttons
- [ ] Long-press context menu

---

### 5.4 File Structure Suggerita

```
src/
├── components/
│   ├── EmailList/
│   │   ├── EmailList.tsx
│   │   ├── EmailItem.tsx
│   │   ├── QuickActions.tsx
│   │   └── styles.css
│   └── CommandPalette/
│       ├── CommandPalette.tsx
│       └── commands.ts
├── hooks/
│   ├── useKeyPress.ts
│   ├── useListNavigation.ts
│   ├── useHover.ts
│   └── useKeyboardShortcuts.ts
└── constants/
    └── shortcuts.ts
```

**`shortcuts.ts` example:**

```typescript
export const SHORTCUTS = {
  navigation: {
    next: ['j', 'ArrowDown'],
    prev: ['k', 'ArrowUp'],
    open: ['Enter', 'o'],
    back: ['Escape', 'u'],
  },
  actions: {
    archive: ['e'],
    assign: ['a'],
    reply: ['r'],
    snooze: ['s'],
    compose: ['c'],
    delete: ['Delete', '#'],
    flag: ['f'],
  },
  global: {
    commandPalette: ['Meta+k', 'Control+k'], // Cmd/Ctrl+K
    search: ['/'],
  },
} as const;
```

---

## 6. Testing & Validation

**Test Checklist:**

- [ ] **Keyboard-only navigation**: Completa workflow senza mouse
- [ ] **Screen reader**: NVDA/JAWS/VoiceOver compatibility
- [ ] **Mobile touch**: Swipe gestures funzionano
- [ ] **Focus indicators**: Visibili su tutti browser
- [ ] **Hover delay**: No accidental triggers con 200ms
- [ ] **Performance**: No lag con 1000+ emails in list
- [ ] **Cross-browser**: Chrome, Firefox, Safari, Edge

**Accessibility Audit Tools:**
- axe DevTools (Chrome extension)
- Lighthouse Accessibility Score (target: 100)
- WAVE Web Accessibility Tool

---

## 7. Fonti & Riferimenti

### Email Clients Analizzati
- [Superhuman Help Center](https://help.superhuman.com/hc/en-us/articles/45191759067411-Speed-Up-With-Shortcuts)
- [Superhuman 2026 Review](https://efficient.app/apps/superhuman)
- [Gmail Hover Actions](https://www.emailoverloadsolutions.com/blog/gmail-hover-actions)
- [Gmail Community Discussion](https://support.google.com/mail/thread/2975903)
- [Apple Mail Swipe Gestures](https://www.macrumors.com/how-to/customize-apple-mail-inbox-gestures-ios-11/)
- [Spark Command Center](https://sparkmailapp.com/help/general/spark-command-center)
- [Missive Features](https://missiveapp.com/features)

### UX Research
- [Nielsen Norman Group - Timing Guidelines](https://www.nngroup.com/articles/timing-exposing-content/)
- [Baymard Institute - Dropdown Delay Study](https://baymard.com/blog/dropdown-menu-flickering-issue)
- [NN/G Button States](https://www.nngroup.com/articles/button-states-communicate-interaction/)

### React Implementation
- [React Hover Events Guide](https://www.rickyspears.com/technology/mastering-hover-events-in-react-a-comprehensive-guide-for-interactive-uIs/)
- [React Aria useHover](https://react-spectrum.adobe.com/react-aria/useHover.html)
- [Create List with Keyboard Navigation](https://whereisthemouse.com/create-a-list-component-with-keyboard-navigation-in-react)
- [GitHub use-keyboard-list-navigation](https://github.com/dzucconi/use-keyboard-list-navigation)

### Accessibility
- [MDN ARIA Labels](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-label)
- [TPGi aria-describedby](https://www.tpgi.com/describing-aria-describedby/)
- [FreeCodeCamp Keyboard Accessibility](https://www.freecodecamp.org/news/designing-keyboard-accessibility-for-complex-react-experiences/)
- [Focus Trap React Guide](https://dev.to/colettewilson/how-i-approach-keyboard-accessibility-for-modals-in-react-152p)

### Keyboard Shortcuts
- [Gmail Shortcuts Cheat Sheet](https://www.getinboxzero.com/blog/post/gmail-shortcuts-cheat-sheet)
- [Superhuman Shortcuts List](https://nickgray.net/superhuman/)
- [UseTheKeyboard - Missive](https://usethekeyboard.com/missive/)

---

## 8. Appendice: Confronto Completo Shortcuts

| Azione | Gmail | Superhuman | Fastmail | Outlook | Raccomandazione Miracollook |
|--------|-------|------------|----------|---------|----------------------------|
| Next email | `j` | `j` | `j` | `Ctrl+.` | `j` ⭐ |
| Previous email | `k` | `k` | `k` | `Ctrl+,` | `k` ⭐ |
| Open | `o` / `Enter` | `Enter` | `Enter` | `Enter` | `Enter` ⭐ |
| Archive | `e` | `e` | `a` | `e` | `e` ⭐ |
| Delete | `#` | `#` | `Delete` | `Delete` | `Delete` ⭐ |
| Reply | `r` | `r` | `r` | `Ctrl+R` | `r` ⭐ |
| Reply all | `a` | `a` | `a` | `Ctrl+Shift+R` | (Fase 2) |
| Forward | `f` | `f` | `f` | `Ctrl+F` | (Fase 2) |
| Compose | `c` | `c` | `w` | `Ctrl+N` | `c` ⭐ |
| Search | `/` | `/` | `/` | `Ctrl+E` | `/` |
| Star/Flag | `s` | `h` | `s` | - | `f` ⭐ |
| Snooze | `b` | `h` | - | - | `s` ⭐ (custom) |
| Select | `x` | `x` | `x` | - | (Fase 2) |
| Command Palette | - | `Cmd+K` | - | - | `Cmd+K` ⭐ (Fase 2) |
| Go to Inbox | `g` + `i` | `g` + `i` | `g` + `i` | - | `g` + `i` (Fase 2) |

**Legenda:**
- ⭐ = Implementare in MVP (Fase 1)
- (Fase 2) = Feature successive

---

## Conclusioni

**Pattern dominanti:**
1. j/k navigation = standard universale (Vim heritage)
2. Hover delay 200ms = sweet spot per email actions
3. Command Palette (Cmd+K) = trend moderno (Superhuman, Slack, VSCode)
4. Accessibility FIRST, non afterthought

**Differenziatore Miracollook:**
- Focus su workflow hotel (Assign to Staff, Snooze per check-out, Guest flags)
- Semplicità > Feature overload (Gmail ha troppi shortcuts, confusione)
- Progressive learning (tooltip hints, keyboard shortcuts cheat sheet)

**Next Steps:**
1. Validare shortcuts con Rafa (hotel workflow-specific)
2. Prototipo Sprint 1 (hover actions)
3. User testing con staff hotel
4. Iterare su feedback

---

**Fine Ricerca** ✅

*"Non esistono cose difficili, esistono cose non studiate!"*
*- Cervella Researcher*
