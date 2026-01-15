# Miracallook - Studi e Ricerche

> Cartella centralizzata per analisi UX, competitor research, user testing
> **Progetto:** Miracallook (Email Client PMS-Integrated)

---

## Indice Studi

### Strategic Research

| File | Data | Tipo | Status |
|------|------|------|--------|
| [STUDIO_MACRO_PMS_INTEGRATION.md](./STUDIO_MACRO_PMS_INTEGRATION.md) | 2026-01-15 | Strategic Research - MACRO | ✅ Complete |
| [STUDIO_MACRO_SETTINGS_UI.md](./STUDIO_MACRO_SETTINGS_UI.md) | 2026-01-15 | Strategic Research - MACRO | ✅ Complete |

**STUDIO_MACRO_PMS_INTEGRATION:**
- Guest identification strategy (5 metodi, confidence score algorithm)
- Architettura PMS integration (API endpoints, cache strategy, real-time vs on-demand)
- UX pattern consigliato (Guest Sidebar design, data priority, progressive enhancement)
- Hotel-specific features (quick actions, email templates, staff assignment)
- Competitor analysis (Canary, Mews, Superhuman, Missive)
- Effort stimato Fase 2: **32-38 ore** (~1 settimana dev time)
- **59 fonti** ricercate da big players 2026

**STUDIO_MACRO_SETTINGS_UI:**
- 7 categorie settings standard + 2 hotel-specific
- Pattern UX: Settings Drawer (Outlook-like) vs Modal vs Full Page
- Save behavior: Auto-save vs Explicit (hybrid approach)
- Storage strategy: localStorage (UI prefs) + DB (business data)
- Hotel features: Signature editor, Quick reply templates, Staff assignment
- Competitor analysis (Gmail, Outlook, Superhuman)
- Effort stimato: **8-12 ore** (~1.5 giorni dev time)
- **15+ fonti** UX patterns + best practices 2026

---

### UX Strategy

| File | Data | Tipo | Status |
|------|------|------|--------|
| [UX_STRATEGY_MIRACALLOOK.md](./UX_STRATEGY_MIRACALLOOK.md) | 2026-01-12 | UX Strategy completa | ✅ Complete |

**Contenuto:**
- User personas (3 personas dettagliate)
- User flows prioritari (4 flows critici)
- Emotional design
- Visual hierarchy
- Density recommendations
- Brand consistency
- Competitive positioning
- Recommendations + metrics

---

### Technical Research

| File | Data | Tipo | Status |
|------|------|------|--------|
| [RICERCA_RESIZE_PANNELLI.md](./RICERCA_RESIZE_PANNELLI.md) | 2026-01-13 | Tech Research | ✅ Complete |

**Contenuto:**
- Analisi librerie React resizable panels
- Competitor analysis (Missive, Superhuman, VS Code, Linear)
- UX best practices (min/max, snap points, keyboard shortcuts)
- Implementazione suggerita per Miracollook
- Code examples con React 19 + Tailwind v4
- **Raccomandazione:** react-resizable-panels (bvaughn)

---

## TODO - Studi Futuri

### User Testing
- [ ] Usability test con receptionist (3-5 users)
- [ ] A/B test: Dashboard vs List mobile
- [ ] Eye-tracking: Visual hierarchy validation
- [ ] Heatmap: Click patterns inbox list

### Competitor Deep-Dives
- [x] Canary Guest Messaging (FATTO - STUDIO_MACRO_PMS_INTEGRATION.md)
- [x] Mews PMS API (FATTO - STUDIO_MACRO_PMS_INTEGRATION.md)
- [x] Superhuman Settings & Shortcuts (FATTO - STUDIO_MACRO_SETTINGS_UI.md)
- [ ] Front: Team collaboration patterns
- [ ] Shortwave: AI implementation analysis

### Technical UX
- [ ] Performance budget: Load time impact
- [ ] Accessibility audit: WCAG 2.1 AA
- [ ] Internationalization: Multi-language support
- [ ] Offline mode: Email sync strategies

---

## Naming Convention

```
FORMATO: {TIPO}_{NOME}_{DATE}.md

ESEMPI:
- UX_STRATEGY_MIRACALLOOK.md
- RICERCA_RESIZE_PANNELLI.md
- STUDIO_MACRO_PMS_INTEGRATION.md
- STUDIO_MACRO_SETTINGS_UI.md
- COMPETITOR_SUPERHUMAN_20260115.md
- USERTEST_RECEPTIONIST_20260120.md
- ACCESSIBILITY_AUDIT_20260125.md
```

---

*Ultimo aggiornamento: 15 Gennaio 2026 - Aggiunto STUDIO_MACRO_SETTINGS_UI*
