# Ricerca: Pannelli Ridimensionabili React

**Data:** 13 Gennaio 2026
**Researcher:** Cervella Researcher
**Obiettivo:** Trovare libreria migliore per implementare pannelli ridimensionabili stile Superhuman/Gmail

---

## TL;DR - RACCOMANDAZIONE

**LIBRERIA CONSIGLIATA:** `react-resizable-panels`

**PERCHE:**
- Moderna, attivamente mantenuta (da Brian Vaughn, React core team)
- API semplice ma potente (Panel, PanelGroup, PanelResizeHandle)
- Built-in persistence localStorage
- Keyboard accessibility nativa (WAI-ARIA)
- Collapsible panels out-of-the-box
- Lightweight, zero dipendenze pesanti
- Documentazione eccellente + demo live

---

## Librerie Analizzate

| Libreria | Downloads/week | Stars | Pros | Cons |
|----------|----------------|-------|------|------|
| **react-resizable-panels** | ~100K+ | Active | Moderna, semplice API, persistence, accessibility | Piu recente |
| **react-split-pane** | 208K | 3.3K | Popolare, semplice | Meno features, API datata |
| **allotment** | 102K | 1.2K | Ispirata VS Code, ottimo look | Piu complessa, opinionated |
| **react-resizable** | 1.4M | 2.5K | Molto popolare | Low-level, richiede piu codice |

---

## react-resizable-panels - DETTAGLIO

### Installazione

```bash
npm install react-resizable-panels
```

### Esempio Base - Email Layout Verticale

```jsx
import { Panel, PanelGroup, PanelResizeHandle } from "react-resizable-panels";

function EmailLayout() {
  return (
    <PanelGroup direction="vertical">
      {/* Lista Email - top panel */}
      <Panel
        defaultSize={30}
        minSize={20}
        maxSize={50}
        collapsible
      >
        <div className="email-list">
          {/* Lista email */}
        </div>
      </Panel>

      <PanelResizeHandle />

      {/* Contenuto Email - bottom panel */}
      <Panel
        defaultSize={70}
        minSize={30}
      >
        <div className="email-content">
          {/* Contenuto email */}
        </div>
      </Panel>
    </PanelGroup>
  );
}
```

### Layout Orizzontale (Sidebar + Content)

```jsx
<PanelGroup direction="horizontal">
  <Panel defaultSize={25} minSize={15} maxSize={40}>
    <Sidebar />
  </Panel>

  <PanelResizeHandle />

  <Panel defaultSize={75}>
    <MainContent />
  </Panel>
</PanelGroup>
```

### Persistence con localStorage

```jsx
function EmailLayoutWithPersistence() {
  const [layout, setLayout] = useState(() => {
    const saved = localStorage.getItem('email-layout');
    return saved ? JSON.parse(saved) : null;
  });

  return (
    <PanelGroup
      direction="vertical"
      defaultLayout={layout}
      onLayout={(newLayout) => {
        setLayout(newLayout);
        localStorage.setItem('email-layout', JSON.stringify(newLayout));
      }}
    >
      {/* ... panels ... */}
    </PanelGroup>
  );
}
```

**NOTE PERSISTENCE:**
- `onLayout` fires DOPO il pointer release (non durante drag)
- Ideale per salvare in storage senza spam di writes
- Layout e un array di percentuali: `[30, 70]`

### Constraints & Collapsible

```jsx
<Panel
  minSize={20}        // Min 20% del parent
  maxSize={80}        // Max 80% del parent
  defaultSize={50}    // Default 50%
  collapsible         // Auto-collapse se < minSize/2
  collapsedSize={0}   // Size quando collapsed (default 0)
>
  Content
</Panel>
```

**UNITS SUPPORTATE:**
- Percentuali: `0-100` (default)
- Pixels: numeri senza unita
- CSS units: `em`, `rem`, `vh`, `vw`

### Keyboard Accessibility

**PanelResizeHandle** include automaticamente:
- `role="separator"`
- WAI-ARIA properties
- Keyboard navigation support

**BEST PRACTICE:** Sempre includere `PanelResizeHandle` tra panels!

```jsx
<PanelResizeHandle className="resize-handle" />
```

### Styling

```css
/* PanelGroup - NON sovrascrivere questi: */
/* display, flex-direction, flex-wrap, overflow */

/* PanelResizeHandle - customizzabile */
.resize-handle {
  background: #e5e7eb;
  width: 2px; /* per vertical */
  cursor: col-resize;
}

.resize-handle:hover {
  background: #3b82f6;
}

/* Horizontal resize handle */
.resize-handle-horizontal {
  height: 2px;
  cursor: row-resize;
}
```

---

## Pattern Superhuman/Gmail

### Caratteristiche Chiave

1. **Split Inbox:**
   - Panel superiore: lista email (Important/Other splits)
   - Panel inferiore: contenuto email selezionata
   - Resize verticale tra i due

2. **Navigation:**
   - Tab / Shift+Tab per muoversi tra splits
   - Keyboard-first interaction

3. **Persistence:**
   - User resize salvato in localStorage
   - Ripristinato al prossimo login

4. **Constraints:**
   - Min size per leggibilita (es. 20%)
   - Max size per non nascondere l'altro panel (es. 80%)

### Implementazione Consigliata

```jsx
import { Panel, PanelGroup, PanelResizeHandle } from "react-resizable-panels";

function SuperhumanStyleLayout() {
  // Persistence
  const LAYOUT_KEY = 'superhuman-layout';
  const [savedLayout, setSavedLayout] = useState(() => {
    const saved = localStorage.getItem(LAYOUT_KEY);
    return saved ? JSON.parse(saved) : [30, 70]; // default
  });

  const handleLayoutChange = (layout) => {
    setSavedLayout(layout);
    localStorage.setItem(LAYOUT_KEY, JSON.stringify(layout));
  };

  return (
    <PanelGroup
      direction="vertical"
      defaultLayout={savedLayout}
      onLayout={handleLayoutChange}
      className="h-screen"
    >
      {/* Email List Panel */}
      <Panel
        defaultSize={savedLayout[0]}
        minSize={20}
        maxSize={60}
        collapsible
      >
        <div className="email-list-container">
          {/* Important Split */}
          <div className="split important">
            <h3>Important</h3>
            {/* email items */}
          </div>

          {/* Other Split */}
          <div className="split other">
            <h3>Other</h3>
            {/* email items */}
          </div>
        </div>
      </Panel>

      {/* Resize Handle */}
      <PanelResizeHandle className="h-[2px] bg-gray-200 hover:bg-blue-500 transition-colors" />

      {/* Email Content Panel */}
      <Panel
        defaultSize={savedLayout[1]}
        minSize={30}
      >
        <div className="email-content-container">
          {/* email content */}
        </div>
      </Panel>
    </PanelGroup>
  );
}
```

---

## Best Practices Generali

### 1. Constraints Intelligenti

```jsx
// Lista email deve essere sempre leggibile
<Panel minSize={20} maxSize={60}>
  <EmailList />
</Panel>

// Contenuto email deve avere spazio minimo
<Panel minSize={30}>
  <EmailContent />
</Panel>
```

### 2. Collapsible con Senso

```jsx
// Sidebar può collassare completamente
<Panel collapsible minSize={15} collapsedSize={0}>
  <Sidebar />
</Panel>

// Main content NON collapsible
<Panel minSize={40}>
  <MainContent />
</Panel>
```

### 3. Persistence Smart

```jsx
// Salva SOLO dopo resize completo
onLayout={(layout) => {
  // NO: saveToAPI(layout) - troppi calls!
  // YES: localStorage (local, fast)
  localStorage.setItem('layout', JSON.stringify(layout));
}}

// Sync con backend in background (debounced)
useEffect(() => {
  const timer = setTimeout(() => {
    syncLayoutToBackend(savedLayout);
  }, 5000);
  return () => clearTimeout(timer);
}, [savedLayout]);
```

### 4. Accessibility

```jsx
// Sempre includere handle per keyboard users
<PanelResizeHandle
  aria-label="Resize email panels"
  className="focus:ring-2 focus:ring-blue-500"
/>

// Dare dimensioni minime leggibili
minSize={20} // mai < 20% per panels con testo
```

### 5. Responsive

```jsx
// Desktop: horizontal split
// Mobile: vertical stack (no resize)
<PanelGroup
  direction={isMobile ? "vertical" : "horizontal"}
>
  {/* panels */}
</PanelGroup>

// O nascondere resize handle su mobile
{!isMobile && <PanelResizeHandle />}
```

---

## CSS Necessario

```css
/* Base container */
.panel-group {
  height: 100vh;
  width: 100%;
}

/* Resize handles */
.resize-handle-vertical {
  width: 2px;
  background: #e5e7eb;
  cursor: col-resize;
  transition: background-color 150ms;
}

.resize-handle-vertical:hover,
.resize-handle-vertical:focus {
  background: #3b82f6;
}

.resize-handle-horizontal {
  height: 2px;
  background: #e5e7eb;
  cursor: row-resize;
  transition: background-color 150ms;
}

.resize-handle-horizontal:hover,
.resize-handle-horizontal:focus {
  background: #3b82f6;
}

/* Panel content */
.panel-content {
  height: 100%;
  overflow: auto;
  padding: 1rem;
}

/* Accessibility */
.resize-handle:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}
```

---

## Alternative Considerate

### react-split-pane

**PRO:**
- Molto popolare (208K downloads/week)
- Semplice API

**CONTRO:**
- API datata
- Meno features built-in
- No collapsible nativo
- Persistence manuale

**QUANDO USARE:** Progetti legacy che gia la usano.

### allotment

**PRO:**
- Look professionale (ispirato VS Code)
- Ottimo default styling
- 102K downloads/week

**CONTRO:**
- Piu opinionated
- API leggermente piu complessa
- Meno documentazione/esempi

**QUANDO USARE:** Se vuoi look VS Code out-of-the-box.

### react-resizable

**PRO:**
- Molto popolare (1.4M downloads/week)
- Massima flessibilita

**CONTRO:**
- Low-level (devi gestire tutto tu)
- Richiede piu codice boilerplate
- No split panels ready-made

**QUANDO USARE:** Custom resize behavior non supportato da altre librerie.

---

## Prossimi Step Implementazione

1. **Install:**
   ```bash
   npm install react-resizable-panels
   ```

2. **Setup base layout:**
   - PanelGroup direction="vertical"
   - 2 Panels (email list + content)
   - PanelResizeHandle in mezzo

3. **Add persistence:**
   - localStorage per salvare layout
   - defaultLayout da localStorage
   - onLayout per aggiornare

4. **Add constraints:**
   - minSize={20} per email list
   - minSize={30} per content
   - collapsible su list (opzionale)

5. **Styling:**
   - Custom resize handle (2px line)
   - Hover effect (blu)
   - Focus ring per accessibility

6. **Testing:**
   - Resize funziona smooth
   - Persistence funziona tra refresh
   - Keyboard navigation ok
   - Mobile responsive

---

## Fonti

- [GitHub - react-resizable-panels](https://github.com/bvaughn/react-resizable-panels)
- [NPM - react-resizable-panels](https://www.npmjs.com/package/react-resizable-panels)
- [Official Docs - react-resizable-panels](https://react-resizable-panels.vercel.app/)
- [LogRocket - React Panel Layouts](https://blog.logrocket.com/essential-tools-implementing-react-panel-layouts/)
- [NPM Compare - Allotment vs react-resizable](https://npmtrends.com/allotment-vs-react-resizable-vs-react-split-pane-vs-react-splitter-layout)
- [Superhuman - Split Inbox Basics](https://help.superhuman.com/hc/en-us/articles/38449611367187-Split-Inbox-Basics)
- [GitHub - allotment](https://github.com/johnwalley/allotment)

---

**CONCLUSIONE:**

`react-resizable-panels` e la scelta migliore per implementare pannelli ridimensionabili stile Superhuman/Gmail. API moderna, features built-in (persistence, accessibility, collapsible), documentazione chiara. Pronta per produzione.

**Next:** Implementare in Miracollo con pattern Superhuman (vertical split + localStorage persistence).

---

*Ricerca completata da Cervella Researcher - 13 Gen 2026*
