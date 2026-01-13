# RICERCA: Resizable Panels per Miracollook

> **Ricercatrice:** Cervella Researcher
> **Data:** 13 Gennaio 2026
> **Contesto:** Miracollook - Email client React
> **Obiettivo:** Implementare pannelli ridimensionabili come Missive/Superhuman

---

## TL;DR - Raccomandazione

**Usa `react-resizable-panels` di bvaughn**

- Libreria matura (316k+ dipendenti npm, 3k+ stelle GitHub)
- API dichiarativa perfetta per React
- Persistenza localStorage built-in
- Accessibilità ARIA integrata
- TypeScript nativo
- Bundle ~8-10KB
- Maintainer attivo (ultima versione: 4.3.3, gen 2026)

**Alternativa se serve massimo controllo:** `react-resizable-layout` (headless, ma meno supporto)

---

## 1. LIBRERIE ANALIZZATE

### react-resizable-panels ⭐ RACCOMANDATA

| Aspetto | Valore |
|---------|--------|
| **GitHub** | bvaughn/react-resizable-panels |
| **Stelle** | 3,000+ |
| **Downloads** | 316k+ dipendenti |
| **Versione** | 4.3.3 (gennaio 2026) |
| **Bundle Size** | ~8-10KB minified |
| **License** | MIT |
| **TypeScript** | ✅ Nativo |

**Pro:**
- ✅ API dichiarativa semplice (`PanelGroup`, `Panel`, `PanelResizeHandle`)
- ✅ Persistenza localStorage con `autoSaveId` prop
- ✅ Supporto min/max size, collapsible panels
- ✅ Accessibilità ARIA out-of-the-box
- ✅ API imperativa (collapse/expand via ref)
- ✅ Nested layouts (pannelli dentro pannelli)
- ✅ Documentazione eccellente + demo interattive
- ✅ Manutenzione attiva (0 issue aperti)

**Contro:**
- ⚠️ Non puoi override `display`, `flex-direction`, `overflow` CSS
- ⚠️ Panel/Handle devono essere figli diretti di PanelGroup
- ⚠️ Persistenza manuale se serve custom storage
- ⚠️ Hydration shift con SSR (risolvibile con cookies)

**Link:**
- [GitHub](https://github.com/bvaughn/react-resizable-panels)
- [Demo interattiva](https://react-resizable-panels.vercel.app/)
- [npm](https://www.npmjs.com/package/react-resizable-panels)

---

### react-resizable-layout (Headless)

| Aspetto | Valore |
|---------|--------|
| **GitHub** | N/A |
| **Stelle** | ~50 |
| **Downloads** | ~3k/settimana |
| **Approccio** | Headless (solo logica) |

**Pro:**
- ✅ Massima flessibilità styling
- ✅ Separazione logica-UI pulita
- ✅ Libreria leggera

**Contro:**
- ❌ Comunità piccola
- ❌ Manutenzione meno attiva
- ❌ Richiede più codice custom

**Quando usarla:** Design molto custom, controllo totale su CSS.

---

### shadcn/ui Resizable

**Wrapper** su react-resizable-panels con stili predefiniti Tailwind + accessibilità.

- Include esempio "Mail" in repository
- Cookie-based persistence per SSR
- Usa stesso core di react-resizable-panels

**Pro:** Se già usi shadcn/ui
**Contro:** Dipendenza extra, stessi limiti di react-resizable-panels

**Link:**
- [Docs](https://ui.shadcn.com/docs/components/resizable)
- [Mail example](https://github.com/shadcn-ui/ui/tree/main/apps/www/app/(app)/examples/mail)

---

## 2. COME LO FANNO I BIG PLAYERS

### Missive (Email client)

**Tech Stack:**
- Electron + React + Backbone
- CoffeeScript core
- "Just CSS" per UI
- Web-first approach

**Layout:**
- 3 pannelli: inbox list | email view | detail panel
- Supporta resize verticale integrations
- Bug recente fixato: "Resizing integrations vertically"

**Insight:** No dettagli pubblici su implementazione resize, ma architettura Electron + React + CSS compatible con react-resizable-panels.

**Fonti:**
- [Missive Architecture](https://medium.com/missive-app/our-dirty-little-secret-cross-platform-email-client-with-nothing-but-html-aa12fc33bb02)
- [Missive App](https://missiveapp.com/)

---

### Superhuman (Email client)

**UI Design:**
- Minimalista, fixed layout
- Sidebar non pinnable (criticato da utenti)
- Metadata panel on right
- Priorità: simplicità > customization

**Insight:** NON sembra offrire resize pannelli. Layout fisso by design.

**Conclusione:** Superhuman scelta opposta - layout rigido. Noi puntiamo a flessibilità.

**Fonti:**
- [Superhuman Review](https://afit.co/superhuman-email-review)
- [Superhuman](https://superhuman.com/)

---

### VS Code (Editor)

**Approach:**
- Electron + custom implementation
- Panel size persists on container resize
- ResizeObserver + imperative API
- Fixed panel behavior (dimensione costante al resize container)

**Insight:** VS Code usa logica custom, ma `react-resizable-panels` supporta stesso pattern.

**Fonti:**
- [VS Code Issues](https://github.com/microsoft/vscode/issues/178611)
- [Fixed size panel](https://github.com/bvaughn/react-resizable-panels/issues/195)

---

### Linear (Project Management)

**UI:**
- Side panels per meta properties
- Multiple display modes (list, board, timeline, split, fullscreen)
- Redesign focus: ridurre visual noise

**Tech:** Probabilmente react-resizable-panels o custom (no info pubblica)

**Insight:** Linear esempio ottimo di UX pulita con pannelli flessibili.

**Fonti:**
- [Linear UI Redesign](https://linear.app/now/how-we-redesigned-the-linear-ui)

---

## 3. UX BEST PRACTICES

### Min/Max Width Constraints

**Regola base:** Previeni pannelli inutilizzabili o troppo espansi.

```jsx
<Panel
  minSize={15}  // 15% minimo (non collassare troppo)
  maxSize={50}  // 50% massimo (non dominare layout)
/>
```

**Recommended per Email Client:**

| Panel | Min | Max | Default | Note |
|-------|-----|-----|---------|------|
| **Sidebar** | 150px (10%) | 400px (30%) | 200px (15%) | Folders/labels visibili |
| **Email List** | 280px (20%) | 600px (40%) | 320px (25%) | Subject + preview leggibili |
| **Detail** | 400px (30%) | 100% | 60% | Email body confortevole |

---

### Snap Points

**Cosa sono:** Posizioni predefinite dove il resize "snappa" automaticamente.

**Esempio:**
```jsx
<Panel snapPoints={[20, 33, 50]} />
```

Pannello snappa a 20%, 33%, 50% durante drag.

**Quando usarli:**
- Layout predefiniti (es: "Compatto", "Bilanciato", "Lettura")
- Evitare dimensioni "strane" (es: 27.38%)
- Migliorare UX su touch devices

**Miracollook:** Considera snap a 15%, 25%, 40% per sidebar.

---

### Collapse Behavior

**Pattern comune:** Draggare sotto metà del minSize → auto-collapse.

```jsx
<Panel
  collapsible={true}
  collapsedSize={0}  // 0% quando collassato
  minSize={15}
  onCollapse={(collapsed) => {
    // Mostra/nascondi hamburger icon
  }}
/>
```

**Best Practice:**
- Indica visivamente quando panel è collapsable
- Fornisci bottone alternativo per collapse/expand
- Salva stato collapsed in localStorage

---

### Cursore Durante Drag

**Standard:** `cursor: col-resize` (orizzontale) o `row-resize` (verticale)

**react-resizable-panels gestisce automaticamente**, ma puoi customizzare:

```css
[data-panel-resize-handle] {
  cursor: col-resize;
  background: transparent;
  transition: background 0.2s;
}

[data-panel-resize-handle]:hover {
  background: rgba(0, 0, 0, 0.1);
}

[data-panel-resize-handle]:active {
  background: rgba(0, 0, 0, 0.2);
  cursor: col-resize !important;
}
```

---

### Keyboard Shortcuts

**react-resizable-panels include:**
- Arrow keys per resize
- Enter per collapse/expand

**Suggerimenti extra per Miracollook:**
```
Cmd+B → Toggle sidebar collapse
Cmd+[ → Espandi email list
Cmd+] → Espandi detail panel
```

Implementa con API imperativa:

```jsx
const panelRef = useRef();

useEffect(() => {
  const handleKeyboard = (e) => {
    if (e.metaKey && e.key === 'b') {
      panelRef.current?.collapse();
    }
  };

  window.addEventListener('keydown', handleKeyboard);
  return () => window.removeEventListener('keydown', handleKeyboard);
}, []);
```

---

### Animazioni/Transizioni

**Subtle è meglio:**
```css
[data-panel] {
  transition: flex-basis 0.2s ease-out;
}

[data-panel-resize-handle] {
  transition: background 0.15s;
}
```

**Non animare durante drag attivo** (performance + feels laggy).

---

### Layout Persistence

**Perché importante:** Utenti odiano ri-configurare layout ogni volta.

**react-resizable-panels rende facile:**

```jsx
<PanelGroup
  direction="horizontal"
  autoSaveId="miracollook-layout"  // Chiave localStorage
>
  {/* panels */}
</PanelGroup>
```

Salva automaticamente in `localStorage` con chiave `react-resizable-panels:layout:miracollook-layout`.

**Best Practice:**
- Un `autoSaveId` per layout (es: "miracollook-main")
- Considera export/import layout come feature avanzata
- Reset a default con button "Ripristina Layout"

---

### Mobile Considerations

**Problema:** Small screens + resize drag = UX pessima.

**Soluzioni:**
1. **Disable resize su mobile**, mostra layout predefinito
2. **Layout presets** (toggle tra "Compatto", "Lettura", "Anteprima")
3. **Stack verticale** invece di orizzontale

**Miracollook:** Probabilmente desktop-first, ma considera:
```jsx
const isMobile = window.innerWidth < 768;

<PanelGroup direction={isMobile ? "vertical" : "horizontal"}>
  {/* ... */}
</PanelGroup>
```

---

## 4. IMPLEMENTAZIONE SUGGERITA PER MIRACOLLOOK

### Tech Stack Miracollook

- ✅ React 19
- ✅ Vite
- ✅ Tailwind v4
- ✅ TypeScript (probabile)

**Compatibilità react-resizable-panels:** PERFETTA ✅

---

### Codice Base - 3 Pannelli (Sidebar, List, Detail)

```tsx
// src/layouts/EmailLayout.tsx
import { Panel, PanelGroup, PanelResizeHandle } from 'react-resizable-panels';
import Sidebar from '@/components/Sidebar';
import EmailList from '@/components/EmailList';
import EmailDetail from '@/components/EmailDetail';

export default function EmailLayout() {
  return (
    <div className="h-screen flex flex-col">
      {/* Header */}
      <header className="h-16 border-b flex items-center px-4">
        <h1>Miracollook</h1>
      </header>

      {/* Main Layout - 3 Panels */}
      <PanelGroup
        direction="horizontal"
        autoSaveId="miracollook-main-layout"
        className="flex-1"
      >
        {/* Sidebar Panel */}
        <Panel
          id="sidebar"
          defaultSize={15}
          minSize={10}
          maxSize={30}
          collapsible={true}
          onCollapse={(collapsed) => {
            console.log('Sidebar collapsed:', collapsed);
          }}
        >
          <Sidebar />
        </Panel>

        <PanelResizeHandle className="w-1 bg-gray-200 hover:bg-blue-400 transition-colors" />

        {/* Email List Panel */}
        <Panel
          id="email-list"
          defaultSize={25}
          minSize={20}
          maxSize={40}
        >
          <EmailList />
        </Panel>

        <PanelResizeHandle className="w-1 bg-gray-200 hover:bg-blue-400 transition-colors" />

        {/* Email Detail Panel */}
        <Panel
          id="email-detail"
          defaultSize={60}
          minSize={30}
        >
          <EmailDetail />
        </Panel>
      </PanelGroup>
    </div>
  );
}
```

---

### Styling con Tailwind

```tsx
// PanelResizeHandle con stile custom
function CustomResizeHandle({ className = '', ...props }) {
  return (
    <PanelResizeHandle
      className={`
        w-1
        bg-transparent
        hover:bg-gray-300
        active:bg-blue-500
        transition-colors
        cursor-col-resize
        group
        ${className}
      `}
      {...props}
    >
      <div className="w-full h-full flex items-center justify-center">
        <div className="w-0.5 h-8 bg-gray-400 group-hover:bg-blue-500 rounded-full" />
      </div>
    </PanelResizeHandle>
  );
}
```

---

### API Imperativa - Collapse/Expand Programmaticamente

```tsx
import { useRef } from 'react';
import { ImperativePanelHandle } from 'react-resizable-panels';

export default function EmailLayout() {
  const sidebarRef = useRef<ImperativePanelHandle>(null);

  const toggleSidebar = () => {
    const panel = sidebarRef.current;
    if (!panel) return;

    if (panel.isCollapsed()) {
      panel.expand();
    } else {
      panel.collapse();
    }
  };

  return (
    <div>
      <button onClick={toggleSidebar}>
        Toggle Sidebar
      </button>

      <PanelGroup direction="horizontal" autoSaveId="miracollook-main-layout">
        <Panel
          ref={sidebarRef}
          id="sidebar"
          defaultSize={15}
          collapsible={true}
        >
          <Sidebar />
        </Panel>
        {/* ... */}
      </PanelGroup>
    </div>
  );
}
```

---

### Keyboard Shortcuts Integration

```tsx
import { useEffect, useRef } from 'react';
import { ImperativePanelHandle } from 'react-resizable-panels';

export default function EmailLayout() {
  const sidebarRef = useRef<ImperativePanelHandle>(null);
  const listRef = useRef<ImperativePanelHandle>(null);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Cmd+B: Toggle sidebar
      if (e.metaKey && e.key === 'b') {
        e.preventDefault();
        const panel = sidebarRef.current;
        if (panel) {
          panel.isCollapsed() ? panel.expand() : panel.collapse();
        }
      }

      // Cmd+[: Espandi email list
      if (e.metaKey && e.key === '[') {
        e.preventDefault();
        listRef.current?.resize(40); // 40% width
      }

      // Cmd+]: Riduci email list
      if (e.metaKey && e.key === ']') {
        e.preventDefault();
        listRef.current?.resize(25); // 25% width
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <PanelGroup direction="horizontal" autoSaveId="miracollook-main-layout">
      <Panel ref={sidebarRef} id="sidebar" defaultSize={15} collapsible>
        <Sidebar />
      </Panel>
      <PanelResizeHandle />

      <Panel ref={listRef} id="email-list" defaultSize={25}>
        <EmailList />
      </Panel>
      <PanelResizeHandle />

      <Panel id="email-detail" defaultSize={60}>
        <EmailDetail />
      </Panel>
    </PanelGroup>
  );
}
```

---

### Reset Layout a Default

```tsx
import { useRef } from 'react';
import { ImperativePanelGroupHandle } from 'react-resizable-panels';

export default function EmailLayout() {
  const panelGroupRef = useRef<ImperativePanelGroupHandle>(null);

  const resetLayout = () => {
    const group = panelGroupRef.current;
    if (group) {
      group.setLayout([15, 25, 60]); // Default: 15% sidebar, 25% list, 60% detail
    }
  };

  return (
    <div>
      <button onClick={resetLayout} className="btn">
        Ripristina Layout Default
      </button>

      <PanelGroup
        ref={panelGroupRef}
        direction="horizontal"
        autoSaveId="miracollook-main-layout"
      >
        {/* panels */}
      </PanelGroup>
    </div>
  );
}
```

---

### Custom Storage (Alternative a localStorage)

Se vuoi salvare layout su backend o IndexedDB:

```tsx
const customStorage = {
  getItem: (name: string) => {
    // Fetch da backend o IndexedDB
    return localStorage.getItem(name); // Esempio semplice
  },
  setItem: (name: string, value: string) => {
    // Salva su backend o IndexedDB
    localStorage.setItem(name, value); // Esempio semplice
  }
};

<PanelGroup
  direction="horizontal"
  autoSaveId="miracollook-main-layout"
  storage={customStorage}
>
  {/* panels */}
</PanelGroup>
```

---

## 5. INSTALLAZIONE E SETUP

### Step 1: Installa Libreria

```bash
npm install react-resizable-panels
# oppure
pnpm add react-resizable-panels
# oppure
yarn add react-resizable-panels
```

---

### Step 2: Import Componenti

```tsx
import { Panel, PanelGroup, PanelResizeHandle } from 'react-resizable-panels';
```

No CSS import necessario - funziona con inline styles.

---

### Step 3: (Opzionale) Tailwind Config

Se vuoi customizzare colori handles:

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        'panel-handle': '#e5e7eb',
        'panel-handle-hover': '#3b82f6',
      }
    }
  }
}
```

---

### Step 4: TypeScript (se usato)

Types inclusi nel package, zero config:

```tsx
import { ImperativePanelHandle, ImperativePanelGroupHandle } from 'react-resizable-panels';

const panelRef = useRef<ImperativePanelHandle>(null);
const groupRef = useRef<ImperativePanelGroupHandle>(null);
```

---

## 6. CONSIDERAZIONI FINALI

### Pro dell'Approccio react-resizable-panels

- ✅ **Veloce da implementare** - Poche ore vs giorni con custom implementation
- ✅ **Manutenzione zero** - Libreria attiva, bug fix regolari
- ✅ **Bundle piccolo** - ~8-10KB non impatta performance
- ✅ **Accessibilità gratis** - ARIA labels, keyboard support inclusi
- ✅ **TypeScript-ready** - Miracollook probabilmente userà TS
- ✅ **Persistence built-in** - UX migliore senza sforzo

---

### Contro (Limitati)

- ⚠️ **CSS constraints** - Non puoi override `display`, `flex-direction`
  - **Soluzione:** Wrapper div dentro Panel se serve layout custom

- ⚠️ **Struttura rigida** - Panel/Handle figli diretti di PanelGroup
  - **Soluzione:** Nesting di PanelGroup se serve complessità

- ⚠️ **SSR hydration shift** - Layout default → layout salvato
  - **Soluzione:** Cookies invece di localStorage (vedi shadcn example)

---

### Alternative da Considerare

**Costruire Custom Implementation SE:**
- Budget tempo > velocità
- Requisiti design estremamente specifici
- Vuoi controllo totale su ogni pixel

**Costo stimato custom:**
- 2-3 giorni sviluppo base
- 1-2 giorni bug fixing edge cases
- 1 giorno accessibility + keyboard
- Ongoing maintenance

**react-resizable-panels risparmia ~5 giorni lavoro.**

---

## 7. PROSSIMI STEP SUGGERITI

### Fase 1: Prototipo (1-2 ore)
1. ✅ Installa `react-resizable-panels`
2. ✅ Crea `EmailLayout.tsx` con 3 pannelli base
3. ✅ Test resize manuale, verifica UX
4. ✅ Verifica localStorage persistence

### Fase 2: Styling (2-3 ore)
1. ✅ Customizza `PanelResizeHandle` con Tailwind
2. ✅ Aggiungi hover/active states
3. ✅ Test responsive (mobile collapse?)
4. ✅ Dark mode support se necessario

### Fase 3: Features Avanzate (3-4 ore)
1. ✅ Keyboard shortcuts (Cmd+B, Cmd+[, Cmd+])
2. ✅ Collapse/expand API imperativa
3. ✅ Reset layout button
4. ✅ Layout presets (Compatto, Bilanciato, Lettura)

### Fase 4: Polish (1-2 ore)
1. ✅ Animazioni subtle
2. ✅ Tooltip su resize handles
3. ✅ Onboarding tour (primo uso)
4. ✅ Analytics tracking (quanto utenti usano resize?)

**Totale stimato: 7-11 ore lavoro**

---

## 8. FONTI E RIFERIMENTI

### Librerie
- [react-resizable-panels GitHub](https://github.com/bvaughn/react-resizable-panels)
- [react-resizable-panels Demo](https://react-resizable-panels.vercel.app/)
- [react-resizable-panels npm](https://www.npmjs.com/package/react-resizable-panels)
- [shadcn/ui Resizable](https://ui.shadcn.com/docs/components/resizable)
- [shadcn Mail Example](https://github.com/shadcn-ui/ui/tree/main/apps/www/app/(app)/examples/mail)

### Best Practices
- [LogRocket: React Panel Layouts](https://blog.logrocket.com/essential-tools-implementing-react-panel-layouts/)
- [DhiWise: React Resizable Panels Guide](https://www.dhiwise.com/post/react-resizable-panels-crafting-fluid-interfaces-with-ease)

### Competitor Research
- [Missive Architecture](https://medium.com/missive-app/our-dirty-little-secret-cross-platform-email-client-with-nothing-but-html-aa12fc33bb02)
- [Missive App](https://missiveapp.com/)
- [Superhuman Review](https://afit.co/superhuman-email-review)
- [Linear UI Redesign](https://linear.app/now/how-we-redesigned-the-linear-ui)
- [VS Code Panel Issues](https://github.com/microsoft/vscode/issues/178611)

### UX Resources
- [GitHub: Resizable Panels Discussions](https://github.com/bvaughn/react-resizable-panels/discussions)
- [Best of JS: react-resizable-panels](https://bestofjs.org/projects/react-resizable-panels)

---

## Conclusione

**react-resizable-panels è la scelta migliore per Miracollook.**

- Risparmia giorni di sviluppo
- Libreria matura e ben mantenuta
- UX out-of-the-box + customizable
- Perfettamente compatible con React 19 + Vite + Tailwind v4

**"I big player ci insegnano - noi impariamo!"**

Missive, Linear, VS Code tutti usano panel resizabili perché **UX flexibility è critica** in productivity apps. Miracollook merita lo stesso livello di polish.

---

*Ricerca completata da Cervella Researcher - 13 Gennaio 2026*
