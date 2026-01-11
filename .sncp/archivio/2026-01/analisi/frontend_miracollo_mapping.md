# Frontend Miracollo - Mappa Completa
**Data:** 11 Gennaio 2026
**Analista:** Cervella Frontend
**Obiettivo:** Mappare frontend esistente per Sprint 3.5 (badge confidence + dashboard ML)

---

## 1. STRUTTURA FRONTEND

### Pagine Principali (HTML)
```
frontend/
├── index-dashboard.html     → Dashboard KPI
├── planning.html            → Planning board (drag & drop)
├── frontdesk.html          → Check-in/out
├── guests.html             → Gestione ospiti
├── groups.html             → Gestione gruppi
├── rates.html              → Gestione tariffe
├── rateboard.html          → Rateboard AI
├── revenue.html            → Revenue Intelligence ⭐ FOCUS
├── settings.html           → Configurazioni
├── admin.html              → Admin (city tax, compliance)
└── reports.html            → Report
```

### CSS Architettura
```
css/
├── style.css               → Design system globale (DARK THEME)
├── revenue.css             → Revenue Intelligence specifico
├── rateboard.css           → Rateboard specifico
├── planning.css            → Planning + moduli (8 file)
│   ├── 01-variables.css
│   ├── 02-layout.css
│   ├── 03-grid.css
│   └── ...
├── settings.css
├── competitors.css
├── automation.css
├── night-audit.css
└── toast.css               → Toast notifications system
```

### JavaScript Moduli
```
js/
├── revenue.js              → Revenue Intelligence logic ⭐
├── api.js                  → API client globale
├── app.js                  → App principale
├── planning/               → 20+ moduli planning
├── rateboard/              → 4 moduli rateboard
│   ├── rateboard-app.js
│   ├── rateboard-ai.js     → AI suggestions
│   ├── rateboard-alerts.js
│   └── rateboard-data.js
├── settings/               → 6 moduli settings
├── automation/             → 3 moduli automation
└── utils/
    ├── modal.js
    ├── toast.js
    └── loader.js
```

---

## 2. DESIGN SYSTEM

### Theme: Dark Professional
```css
/* Colori Principali */
--bg-primary: #0a0e1a        (nero-blu molto scuro)
--bg-secondary: #111827      (sidebar)
--bg-card: #1a1f35          (card background)
--bg-card-hover: #232942
--bg-input: #151a2e

/* Accents */
--accent-primary: #6366f1    (indigo - principale)
--accent-secondary: #8b5cf6  (viola - secondario)
--accent-success: #10b981
--accent-warning: #f59e0b
--accent-danger: #ef4444

/* Testo */
--text-primary: #f8fafc      (quasi bianco)
--text-secondary: #94a3b8    (grigio chiaro)
--text-muted: #64748b        (grigio medio)

/* Bordi e Shadows */
--border-color: #2d3654
--border-radius: 12px
--border-radius-sm: 8px
--shadow-md: 0 4px 16px rgba(0,0,0,0.4)
```

### Font Stack
- **Headers:** `Outfit` (variabile 300-700)
- **Data/Code:** `JetBrains Mono` (monospace)
- **Body:** `Plus Jakarta Sans`

### Componenti Comuni
```css
/* Cards */
.overview-card
.bucco-card
.suggerimento-card
.evento-card

/* Badges */
.badge (success, warning, danger)
.tab-badge
.bucco-badge
.performance-badge

/* Buttons */
.btn
.btn-primary
.btn-secondary
.btn-action

/* States */
.loading
.empty-state
```

---

## 3. REVENUE INTELLIGENCE UI (revenue.html)

### Layout Struttura
```
┌─────────────────────────────────────┐
│ Header: "💡 Revenue Intelligence"   │
│ Subtitle: DESCOMPLICAR              │
│ Last Update + Refresh btn           │
├─────────────────────────────────────┤
│ FINESTRE TABS (4 tabs)              │
│ [1 SETTIMANA] [1 MESE] [3 MESI] ... │
│  URGENTE      SERIO    CONTROLLO    │
│    badge:0     badge:0   badge:0    │
├─────────────────────────────────────┤
│ OVERVIEW CARDS (3 card grid)        │
│ [📊 OCCUPANCY] [⚠️ BUCCHI] [💶 IMPATTO] │
├─────────────────────────────────────┤
│ BUCCHI PRIORITARI                   │
│ [ Bucco card 1 - CRITICA ]          │
│ [ Bucco card 2 - ALTA ]             │
│ [ ... ]                             │
├─────────────────────────────────────┤
│ SUGGERIMENTI AI                     │
│ [ 💰 Suggerimento 1 ]               │
│ [ 🏷️ Suggerimento 2 ]               │
│ [ ... ]                             │
├─────────────────────────────────────┤
│ PRICE HISTORY (Timeline + List)     │
├─────────────────────────────────────┤
│ EVENTI LOCALI | BOOKING PACE        │
│ (2-column grid)                     │
└─────────────────────────────────────┘
```

### Dove Inserire Badge Confidence

#### OPZIONE A: Suggerimenti AI (RACCOMANDATO)
**Posizione:** `.suggerimento-card`
**Layout attuale:**
```html
<div class="suggerimento-card">
  <div class="suggerimento-tipo" data-tipo="prezzo">💰</div>
  <div class="suggerimento-content">
    <div class="suggerimento-azione">Aumenta prezzo €20</div>
    <div class="suggerimento-motivo">Gap occupancy -15%</div>
  </div>
  <div class="suggerimento-priorita">P1</div>
</div>
```

**Inserimento Badge:**
```html
<!-- DOPO suggerimento-priorita -->
<div class="confidence-badge" data-level="high">
  <span class="confidence-icon">✓</span>
  <span class="confidence-text">95%</span>
</div>
```

**Styling proposto:**
```css
.confidence-badge {
  padding: 0.35rem 0.75rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.confidence-badge[data-level="high"] {
  background: rgba(34, 197, 94, 0.15);
  color: #22c55e;
}

.confidence-badge[data-level="medium"] {
  background: rgba(234, 179, 8, 0.15);
  color: #eab308;
}

.confidence-badge[data-level="low"] {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.confidence-icon {
  font-size: 0.85rem;
}
```

#### OPZIONE B: Bucchi Cards
**Posizione:** `.bucco-card .bucco-header`
**Inserire badge confidence accanto a badge urgenza:**
```html
<div class="bucco-header">
  <div>
    <span class="bucco-badge">CRITICA</span>
    <span class="confidence-badge" data-level="medium">78%</span>
  </div>
  <span class="bucco-expand-icon">▼</span>
</div>
```

#### OPZIONE C: Price History
**Posizione:** `.price-change-badge` (già esiste AI/MANUAL)
**Aggiungere confidence al badge esistente:**
```html
<span class="price-change-badge ai">
  AI <span class="confidence-mini">92%</span>
</span>
```

---

## 4. ADMIN/SETTINGS (dove mettere Dashboard ML)

### Settings.html - Tab Structure
```
Tabs attuali:
1. 🧙‍♂️ Wizard (setup iniziale)
2. 🏨 Hotel (info hotel)
3. 🛏️ Camere (room types + rooms)
4. 💰 Tariffe (rate plans)
5. 🎁 Extras (servizi extra)
6. 🔧 Avanzate (email, stripe, etc)
7. ⚡ Automation (templates, schedules)
8. 🌙 Night Audit
```

### PROPOSTA: Aggiungere Tab "ML Insights"

**Tab 9:** `🤖 ML Insights`

**Layout Dashboard ML:**
```
┌─────────────────────────────────────┐
│ 🤖 ML Performance Dashboard         │
├─────────────────────────────────────┤
│ OVERVIEW METRICS (4 cards)          │
│ [Accuracy] [Suggestions] [Applied] [ROI] │
├─────────────────────────────────────┤
│ CONFIDENCE DISTRIBUTION (chart)     │
│ [Grafico distribuzione confidence]  │
├─────────────────────────────────────┤
│ MODEL PERFORMANCE                   │
│ [Tabella: date, accuracy, errors]   │
├─────────────────────────────────────┤
│ RECENT PREDICTIONS                  │
│ [Lista ultime predizioni con badge] │
└─────────────────────────────────────┘
```

**HTML Template:**
```html
<!-- TAB: ML INSIGHTS -->
<section class="tab-panel" id="tab-ml-insights">
  <!-- Dashboard Header -->
  <div class="ml-dashboard-header">
    <h3>🤖 ML Performance Dashboard</h3>
    <div class="ml-header-actions">
      <span class="ml-last-training">Last training: 10 Gen 2026</span>
      <button class="btn btn-secondary" id="btnRefreshML">🔄 Refresh</button>
    </div>
  </div>

  <!-- Overview Cards -->
  <div class="ml-overview-cards">
    <div class="ml-card">
      <div class="ml-card-icon">🎯</div>
      <div class="ml-card-content">
        <div class="ml-card-value" id="mlAccuracy">--</div>
        <div class="ml-card-label">Accuracy Media</div>
      </div>
    </div>
    <!-- altre 3 card -->
  </div>

  <!-- Confidence Distribution Chart -->
  <div class="ml-chart-section">
    <h4>Distribuzione Confidence</h4>
    <canvas id="mlConfidenceChart"></canvas>
  </div>

  <!-- Performance Table -->
  <div class="ml-performance-section">
    <h4>Model Performance History</h4>
    <table class="data-table" id="mlPerformanceTable">
      <thead>
        <tr>
          <th>Data</th>
          <th>Accuracy</th>
          <th>Suggestions</th>
          <th>Applied</th>
          <th>Avg Confidence</th>
        </tr>
      </thead>
      <tbody>
        <!-- popolato da JS -->
      </tbody>
    </table>
  </div>
</section>
```

**Posizionamento:** Dopo tab "Night Audit", prima del modal container.

---

## 5. API INTEGRATION

### Endpoint Calls (da revenue.js)

```javascript
// API Base
const API_BASE = '/api/revenue';

// Funzioni fetch esistenti:
fetchBucchi()           → /api/revenue/bucchi
fetchSuggestions()      → /api/revenue/suggestions
fetchOccupancyForecast() → /api/revenue/occupancy-forecast
fetchEventi()           → /api/revenue/eventi
fetchBookingPace()      → /api/revenue/booking-pace
fetchPriceHistory()     → /api/revenue/price-history
fetchAIHealth()         → /api/revenue/ai-health

// NUOVE funzioni da aggiungere:
fetchMLMetrics()        → /api/ml/metrics
fetchConfidenceDistribution() → /api/ml/confidence-dist
fetchRecentPredictions() → /api/ml/predictions/recent
```

### Security Measures (già implementate)
```javascript
// XSS Protection
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// Toast system per feedback
showToast(message, type)  // success, error, warning
```

---

## 6. COMPONENTI RIUSABILI

### Toast System (già presente)
```javascript
// Posizione: fixed top-right
// Auto-remove dopo 5-7 secondi
// Tipi: success (verde), error (rosso), warning (arancione)
showToast('Confidence badge aggiunto!', 'success');
```

### Modal System
```html
<!-- Modal Container (già presente in settings.html) -->
<div class="modal-overlay" id="modalOverlay">
  <div class="modal" id="editModal">
    <div class="modal-header">...</div>
    <div class="modal-body">...</div>
    <div class="modal-footer">...</div>
  </div>
</div>
```

### Loading States
```html
<div class="loading">Caricamento...</div>
<div class="empty-state">
  <div class="emoji">✅</div>
  <div>Nessun dato disponibile</div>
</div>
```

---

## 7. RESPONSIVE DESIGN

### Breakpoints (da revenue.css)
```css
@media (max-width: 1024px) {
  .overview-cards { grid-template-columns: 1fr; }
  .insights-grid { grid-template-columns: 1fr; }
}

@media (max-width: 768px) {
  .finestre-tabs { flex-wrap: wrap; }
  .tab-btn { flex: 1 1 45%; min-width: 150px; }
  /* Padding ridotto per mobile */
}
```

**Pattern Mobile-First:** NO
**Approccio attuale:** Desktop-first con media queries per mobile.

---

## 8. ANIMAZIONI E TRANSIZIONI

### Transition System
```css
--transition-fast: 0.15s ease
--transition-normal: 0.25s ease

/* Hover effects comuni */
transform: translateY(-2px)  /* cards hover */
transform: translateX(4px)   /* list items hover */
transform: rotate(180deg)    /* refresh button */
```

### Animazioni Esistenti
```css
@keyframes pulse {
  /* Status dot pulsante */
}

@keyframes slideIn {
  /* Toast notification */
}

@keyframes fadeIn {
  /* Wizard panels */
}
```

---

## 9. Z-INDEX HIERARCHY

```
Modals:     1000+
Toast:      9999
Dropdowns:  300-400
Sticky:     60-200
Cards:      1 (default)
```

---

## 10. PUNTI INTEGRAZIONE SPRINT 3.5

### Task 1: Badge Confidence sui Suggerimenti

**File da modificare:**
1. `frontend/css/revenue.css` - Aggiungere `.confidence-badge` styles
2. `frontend/js/revenue.js` - Modificare `renderSuggestions()` per includere badge
3. Backend API: Assicurare che `/api/revenue/suggestions` ritorni campo `confidence`

**HTML Output:**
```html
<div class="suggerimento-card">
  <div class="suggerimento-tipo">💰</div>
  <div class="suggerimento-content">
    <div class="suggerimento-azione">Aumenta prezzo</div>
    <div class="suggerimento-motivo">Gap -15%</div>
  </div>
  <div class="suggerimento-priorita">P1</div>
  <div class="confidence-badge" data-level="high">
    <span class="confidence-icon">✓</span>
    <span class="confidence-text">95%</span>
  </div>
</div>
```

**JavaScript Logic:**
```javascript
// In renderSuggestions()
const confidenceLevel = sugg.confidence >= 0.8 ? 'high' :
                        sugg.confidence >= 0.6 ? 'medium' : 'low';

const confidenceIcon = confidenceLevel === 'high' ? '✓' :
                       confidenceLevel === 'medium' ? '~' : '!';

// Aggiungere al template HTML
```

### Task 2: Dashboard ML in Settings

**File da creare/modificare:**
1. `frontend/css/ml-dashboard.css` - Nuovo file per dashboard ML
2. `frontend/js/ml-dashboard.js` - Logica dashboard ML
3. `frontend/settings.html` - Aggiungere tab ML Insights

**Componenti necessari:**
- Overview cards (riusare stile `overview-card`)
- Chart.js o simile per distribuzione confidence
- Tabella performance (riusare `data-table`)
- Lista predizioni recenti

**API Endpoint da chiamare:**
- `/api/ml/metrics` - Metriche aggregate
- `/api/ml/confidence-distribution` - Dati grafico
- `/api/ml/performance-history` - Storico performance
- `/api/ml/predictions/recent` - Ultime 20 predizioni

---

## 11. BEST PRACTICES OSSERVATE

✅ **Consistenza Stile:**
- Tutti i badge usano `border-radius: 999px`
- Font-size badge: `0.7rem - 0.8rem`
- Padding badge: `0.3rem 0.75rem`

✅ **Hover Effects:**
- Tutte le card hanno hover con `translateY(-2px)` o `translateX(4px)`
- Box-shadow su hover: `var(--shadow-md)`

✅ **Color Coding:**
- Rosso (#ef4444): Critico/Danger
- Arancione (#f97316): Warning/Alta
- Giallo (#eab308): Medium/Attenzione
- Verde (#22c55e): Success/Bassa
- Viola (#8b5cf6): AI/ML Related

✅ **Spacing Consistente:**
- Gap tra card: `1rem - 1.5rem`
- Padding interno card: `1.25rem - 1.75rem`
- Margin sezioni: `2rem`

✅ **Loading States:**
- Sempre mostrare loading prima del fetch
- Empty state se nessun dato
- Error toast se fetch fallisce

---

## 12. FILE DEPENDENCIES

### Revenue Intelligence
```
revenue.html
  ├── css/style.css (design system)
  ├── css/revenue.css (specific)
  ├── css/toast.css (notifications)
  └── js/revenue.js (logic)
```

### Settings + ML Dashboard (proposto)
```
settings.html
  ├── css/style.css
  ├── css/settings.css
  ├── css/automation.css
  ├── css/night-audit.css
  ├── css/ml-dashboard.css (NEW)
  ├── js/settings/settings-*.js (6 files)
  ├── js/automation/automation-*.js (3 files)
  ├── js/night-audit/night-audit-app.js
  ├── js/wizard/wizard-app.js
  └── js/ml-dashboard.js (NEW)
```

---

## 13. PRIORITÀ IMPLEMENTAZIONE

### FASE 1: Badge Confidence (1-2 giorni)
1. ✅ Aggiungere CSS `.confidence-badge` in `revenue.css`
2. ✅ Modificare `renderSuggestions()` in `revenue.js`
3. ✅ Test visivo su revenue.html
4. ✅ Responsive check (mobile)

### FASE 2: Dashboard ML (2-3 giorni)
1. ✅ Creare `ml-dashboard.css`
2. ✅ Creare `ml-dashboard.js`
3. ✅ Aggiungere tab in `settings.html`
4. ✅ Implementare overview cards
5. ✅ Implementare chart confidence
6. ✅ Implementare tabella performance
7. ✅ Test integrazione API

### FASE 3: Polish & Testing (1 giorno)
1. ✅ Animations e transitions
2. ✅ Loading states
3. ✅ Error handling
4. ✅ Cross-browser test
5. ✅ Mobile responsive final check

---

## 14. NOTE TECNICHE

### Browser Compatibility
- CSS Variables: Supportato (modern browsers)
- Grid/Flexbox: Supportato
- Backdrop-filter: Usato in modali (supporto moderno)

### Performance Considerations
- Auto-refresh revenue data: ogni 5 min
- Debounce su filtri/search (se implementati)
- Lazy load per chart.js (solo quando tab ML visibile)

### Accessibility (da migliorare)
- Mancano `aria-label` su molti bottoni
- Nessun focus visible sui bottoni
- Mancano `alt` su icone semantiche (usano emoji)

---

## CONCLUSIONI

**Frontend ben strutturato:**
- Design system coerente
- Moduli JS separati
- CSS componentizzato
- API layer ben definito

**Pronto per Sprint 3.5:**
- Badge confidence: facilmente integrabile in suggerimenti
- Dashboard ML: nuovo tab in settings già strutturato
- Componenti riusabili: badge system già presente

**Raccomandazioni:**
1. Badge confidence → Suggerimenti AI (massima visibilità)
2. Dashboard ML → Nuovo tab in settings.html
3. Riusare design system esistente (badge, cards, tables)
4. Mantenere pattern di loading/error/empty states
5. Test responsive su mobile per nuovi componenti

---

**Prossimo Step:** Implementare badge confidence in `revenue.js` + `revenue.css`.
