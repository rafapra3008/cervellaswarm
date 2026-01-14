# RICERCA CONTEXT MENU - INDICE COMPLETO
> **Studio Approfondito per Miracollook**
> **Data:** 14 Gennaio 2026
> **Ricercatrice:** Cervella Researcher
> **Obiettivo:** Analisi completa dei context menu nei big email clients e raccomandazioni implementative

---

## STATUS RICERCA

```
✅ COMPLETATA al 100%

Parti totali: 4
File creati: 4
Fonti analizzate: 50+
Code examples: 20+
```

---

## STRUTTURA RICERCA

Questa ricerca è divisa in **4 parti** per facilitare la lettura e rispettare i limiti di dimensione file:

### 📄 [PARTE 1: Gmail + Outlook](./RICERCA_CONTEXT_MENU_PARTE1.md)
**Argomenti trattati:**
- Executive Summary
- Gmail: Context menu tradizionale (lista completa opzioni, comportamento dinamico)
- Outlook: Quick Actions + Context menu ibrido (Quick Steps, automazione)
- Confronto Gmail vs Outlook

**Dimensione:** ~500 righe
**Tempo lettura:** 10-15 min

---

### 📄 [PARTE 2: Superhuman + Apple Mail + Confronto](./RICERCA_CONTEXT_MENU_PARTE2.md)
**Argomenti trattati:**
- Superhuman: Command Palette (Cmd+K) philosophy
- 5 Rules per Command Palettes
- Fuzzy matching e alias system
- Apple Mail: Native macOS context menu
- Submenu dinamici (folders, flags)
- Confronto completo TUTTI i client
- Filosofie design a confronto

**Dimensione:** ~550 righe
**Tempo lettura:** 12-15 min

---

### 📄 [PARTE 3: Implementazione Tecnica React](./RICERCA_CONTEXT_MENU_PARTE3.md)
**Argomenti trattati:**
- Basic implementation pattern (codice completo)
- Positioning e viewport bounds (getBoundingClientRect)
- Keyboard navigation (WAI-ARIA compliant)
- Accessibility (ARIA roles, focus management)
- React Portal pattern (z-index, stacking context)
- Dynamic options (context-aware menu)
- Librerie React consigliate (react-contexify, @radix-ui, custom)

**Dimensione:** ~500 righe
**Tempo lettura:** 15-20 min (molto codice)

---

### 📄 [PARTE 4: Best Practices + Raccomandazioni](./RICERCA_CONTEXT_MENU_PARTE4.md)
**Argomenti trattati:**
- 10 Linee guida UX (Nielsen Norman Group)
- Design patterns email (Mark read/unread, Star/Flag, Delete, Move)
- Styling e animations (CSS completo, dark mode)
- Testing checklist (functional, keyboard, accessibility, performance)
- **RACCOMANDAZIONI FINALI per Miracollook**
- Approccio a fasi (MVP → Enhanced → Advanced)
- Priorità features e effort estimation
- Technical stack e metrics

**Dimensione:** ~600 righe
**Tempo lettura:** 15-20 min

---

## EXECUTIVE SUMMARY (5 MINUTI)

### Cosa Ho Scoperto

I big email clients usano **4 approcci diversi**:

| Client | Filosofia | Pro | Contro |
|--------|-----------|-----|--------|
| **Gmail** | Simplicity first (10-12 opzioni essenziali) | Fast, clean, easy | Mancano features avanzate |
| **Outlook** | Power & flexibility (20+ opzioni + Quick Steps) | Potente, personalizzabile | Complesso per beginners |
| **Superhuman** | Keyboard supremacy (Command Palette Cmd+K) | Velocissimo (quando imparato) | Alta learning curve |
| **Apple Mail** | Native integration (consistent con macOS) | Polished, accessible | Tied to Apple ecosystem |

### Pattern Comuni a TUTTI

Nonostante filosofie diverse, **tutti condividono**:

1. ✅ Reply/Forward in ALTO (azioni più frequenti)
2. ✅ Delete in BASSO (azione distruttiva lontana da clicks accidentali)
3. ✅ Separatori per grouping (visual organization)
4. ✅ Context-aware options (es. "Mark as Read" XOR "Mark as Unread")
5. ✅ Shortcut visibili (tranne Gmail web)

### Implementazione Tecnica (React)

**Core Requirements:**
```javascript
// 1. Event handling
onContextMenu={(e) => {
  e.preventDefault();
  showMenu({ x: e.clientX, y: e.clientY });
}}

// 2. Viewport bounds checking
if (x + menuWidth > window.innerWidth) {
  adjustedX = window.innerWidth - menuWidth - 10;
}

// 3. Portal rendering
ReactDOM.createPortal(menu, document.body)

// 4. ARIA completa
<div role="menu" aria-label="Email actions">
  <div role="menuitem" tabIndex={-1}>Reply</div>
</div>

// 5. Keyboard navigation
Arrow keys, Enter, Escape, Tab, Home, End, Type-ahead
```

### Raccomandazione per Miracollook

**FASE 1 (MVP):** Context menu essenziale
- 8-10 opzioni core (Reply, Forward, Mark, Star, Archive, Delete)
- Accessibility completa (ARIA + keyboard)
- Viewport bounds checking
- Custom implementation (non library)
- **Effort:** 2-3 giorni dev + 1 giorno testing

**FASE 2:** Quick Actions hover (tipo Outlook)
- Star/Read/Delete icons al hover
- **Effort:** +1-2 giorni

**FASE 3:** Command Palette (tipo Superhuman)
- Cmd+K palette con fuzzy search
- 100+ comandi disponibili
- **Effort:** +1-2 settimane

**START CON:** Fase 1 MVP. Valuta Fase 2-3 dopo feedback utenti!

---

## KEY TAKEAWAYS

### Per UX/UI Designer

1. **Organizza per frequenza d'uso** (Reply > Forward > Archive > Delete)
2. **Usa separatori** per raggruppare azioni simili
3. **Mostra shortcut** accanto alle opzioni (teaching users)
4. **Disable, don't hide** opzioni non disponibili (predictability)
5. **Danger actions** in basso + colore rosso (Delete)

### Per Frontend Developer

1. **Portal rendering** obbligatorio (evita z-index issues)
2. **getBoundingClientRect()** per viewport bounds checking
3. **ARIA completa** (role, tabindex, aria-label, aria-disabled)
4. **Keyboard navigation** full (Arrow, Enter, Escape, Tab, Type-ahead)
5. **Focus management** (on open → first item, on close → trigger)

### Per Rafa (Decisioni)

**DOMANDE DA RISPONDERE:**

1. **Scope MVP:** Context menu solo o anche Command Palette?
2. **Opzioni MVP:** Quali delle 20+ opzioni possibili sono essenziali?
3. **Personalizzazione:** Permettere agli utenti di configurare menu? (tipo Outlook Quick Actions)
4. **Submenu:** Supportare submenu (tipo Move to → folders) o modal picker?
5. **Priorità:** Fare MVP context menu PRIMA di altre features Miracollook?

**MIA RACCOMANDAZIONE:**

```
1. Scope MVP: SOLO context menu (no Command Palette ancora)
2. Opzioni MVP: 8 opzioni essenziali (vedi Fase 1)
3. Personalizzazione: NO per MVP, maybe later
4. Submenu: NO per MVP (usa modal picker), submenu in v2
5. Priorità: SI, context menu è core UX per email client

RATIONALE: Start simple, iterate fast, perfect later
```

---

## METRICHE DA TRACKARE

Post-implementazione, monitora:

```javascript
// Usage metrics
- % actions via context menu vs buttons
- Most used context menu options (top 5)
- Keyboard vs mouse usage ratio
- Average time to action

// Performance metrics
- Menu open time (<100ms target)
- No layout shift (CLS = 0)
- Animation smoothness (60fps)

// Accessibility metrics
- % users using keyboard navigation
- Screen reader error rate
- WCAG compliance score
```

Questi dati ti diranno SE funziona e COME migliorarlo!

---

## PROSSIMI STEP

### Immediati (Questa Settimana)

1. ✅ Ricerca completata (FATTO!)
2. 🎯 **Review con Rafa** - Mostra questa ricerca
3. 💭 **Decisioni scope** - MVP solo o full feature?
4. 🎨 **Designer mockup** - Visual design context menu

### Prossima Settimana

5. 💻 **Frontend implement** - Context menu component
6. 🎹 **Keyboard nav** - ARIA + keyboard handling
7. 🧪 **Tester validate** - Accessibility + cross-browser

### Settimana Dopo

8. 📊 **Deploy staging** - Test con utenti reali
9. 📈 **Analytics setup** - Track metrics
10. 🔄 **Iterate** - Based on feedback

---

## FONTI PRINCIPALI

### Documentazione Clients
- Gmail: [Google Support](https://support.google.com/mail/answer/16356082)
- Outlook: [Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/4620041/outlook-item-list-email-quick-actions-options)
- Superhuman: [Help Center](https://help.superhuman.com/hc/en-us/articles/45191759067411-Speed-Up-With-Shortcuts)
- Apple Mail: [Apple Support](https://support.apple.com/guide/mail/reply-to-or-forward-emails-mlhlp1010/mac)

### UX Research
- [Nielsen Norman Group - Context Menu Guidelines](https://www.nngroup.com/articles/contextual-menus-guidelines/)
- [LogRocket - Creating Context Menus](https://blog.logrocket.com/ux-design/creating-context-menus/)
- [Height - Guide to Context Menus](https://height.app/blog/guide-to-build-context-menus)

### Technical
- [MDN - ARIA menu role](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/menu_role)
- [W3C - Menu Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/menubar/)
- [React Portals](https://legacy.reactjs.org/docs/portals.html)
- [Superhuman - Command Palette Blog](https://blog.superhuman.com/how-to-build-a-remarkable-command-palette/)

### Libraries
- [react-contexify](https://github.com/fkhadra/react-contexify) (3KB, stale but good)
- [use-context-menu](https://github.com/cluk3/use-context-menu) (Hook-based, active)
- [@radix-ui/react-context-menu](https://www.npmjs.com/package/@radix-ui/react-context-menu) (Production-ready)

---

## CONCLUSIONE

Context menu è una **feature fondamentale** per un email client moderno. Ogni big player lo implementa (con filosofie diverse), ma **tutti lo hanno**.

**Per Miracollook:**
- Start con MVP semplice (ispirazione Gmail + polish Apple Mail)
- Custom implementation (full control, small bundle)
- Accessibility first (non dopo!)
- Iterate based su user feedback

**Non reinventiamo la ruota - studiamo chi l'ha già fatta bene!**

Questa ricerca ti dà tutto quello che serve per implementare un context menu **professionale, accessible, e user-friendly**.

---

*"Non esistono cose difficili, esistono cose non studiate!"*

**Ricerca completata da Cervella Researcher**
**Per Miracollook - 14 Gennaio 2026**

---

## FILES

```
.sncp/progetti/miracollo/moduli/miracollook/studi/
├── RICERCA_CONTEXT_MENU.md          (questo file - INDICE)
├── RICERCA_CONTEXT_MENU_PARTE1.md   (Gmail + Outlook)
├── RICERCA_CONTEXT_MENU_PARTE2.md   (Superhuman + Apple Mail)
├── RICERCA_CONTEXT_MENU_PARTE3.md   (Implementazione React)
└── RICERCA_CONTEXT_MENU_PARTE4.md   (Best Practices + Raccomandazioni)
```

**Leggi nell'ordine:** INDICE → PARTE1 → PARTE2 → PARTE3 → PARTE4

**O leggi solo:** INDICE (questo file) per summary, poi approfondisci parti specifiche che ti interessano!
