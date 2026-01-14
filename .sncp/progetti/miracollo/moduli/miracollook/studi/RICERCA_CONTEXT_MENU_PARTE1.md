# RICERCA CONTEXT MENU - Email Clients Big Players
> **Ricerca per Miracollook**
> **Data:** 14 Gennaio 2026
> **Ricercatrice:** Cervella Researcher
> **Obiettivo:** Studio approfondito dei context menu (tasto destro) nei principali email clients

---

## INDICE RICERCA

Questa ricerca è divisa in 4 parti:

- **PARTE 1** (questo file): Executive Summary + Gmail + Outlook
- **PARTE 2**: Superhuman + Apple Mail + Confronto Comparativo
- **PARTE 3**: Implementazione Tecnica React
- **PARTE 4**: Best Practices UX/UI + Accessibility + Raccomandazioni

---

## EXECUTIVE SUMMARY

### Cosa Ho Scoperto

I big email clients utilizzano approcci DIVERSI per i context menu:

| Client | Approccio | Filosofia |
|--------|-----------|-----------|
| **Gmail** | Context menu tradizionale (tasto destro) | Molte opzioni, organizzate per frequenza |
| **Outlook** | Quick Actions hover + context menu | Mix di hover actions + menu completo |
| **Superhuman** | Command Palette (Cmd+K) > Context Menu | Keyboard-first, menu è secondario |
| **Apple Mail** | Native macOS context menu | Sistema nativo, coerente con OS |

### Pattern Identificati

**1. ORGANIZZAZIONE**
- Opzioni più frequenti in alto (Reply, Forward)
- Azioni distruttive in basso (Delete)
- Separatori per raggruppare azioni simili
- Shortcut mostrati accanto alle opzioni

**2. DINAMICITÀ**
- Menu cambia in base allo stato email (letta/non letta)
- Opzioni context-aware (es. "Mark as Read" diventa "Mark as Unread")
- Alcuni client nascondono opzioni irrilevanti

**3. ACCESSIBILITÀ**
- Tutti supportano keyboard navigation
- ARIA roles obbligatori (menu, menuitem)
- Focus management con Tab/Arrows/Enter/Escape
- Screen reader support

**4. POSIZIONAMENTO**
- Viewport bounds checking (mai fuori schermo)
- Smart positioning (flip se vicino ai bordi)
- Z-index alto per evitare sovrapposizioni

---

## 1. GMAIL - CONTEXT MENU TRADIZIONALE

### Overview

Gmail ha aggiunto il context menu (tasto destro) nel **Febbraio 2019** dopo anni di richieste degli utenti. Prima di allora, tutte le azioni erano disponibili solo tramite toolbar e shortcut.

### Opzioni Disponibili

**Categoria 1: REPLY/FORWARD** (conversazione aperta)
```
┌─────────────────────────────────┐
│ Reply                           │
│ Reply All                       │
│ Forward                         │
├─────────────────────────────────┤  <-- Separator
│ ...                             │
└─────────────────────────────────┘
```

**Categoria 2: SEARCH** (email selezionata)
```
┌─────────────────────────────────┐
│ Search messages from [sender]   │
│ Search messages with subject    │ (solo se conversation view OFF)
├─────────────────────────────────┤
│ ...                             │
└─────────────────────────────────┘
```

**Categoria 3: ORGANIZATION**
```
┌─────────────────────────────────┐
│ Snooze                          │
│ Mute                            │
│ Label as                        │
│ Move to                         │
├─────────────────────────────────┤
│ ...                             │
└─────────────────────────────────┘
```

**Categoria 4: QUICK ACTIONS**
```
┌─────────────────────────────────┐
│ Archive                         │
│ Mark as read / Mark as unread   │  <-- Dynamic!
│ Delete                          │
├─────────────────────────────────┤
│ ...                             │
└─────────────────────────────────┘
```

**Categoria 5: ADVANCED** (da "More" menu)
```
┌─────────────────────────────────┐
│ Add to Tasks                    │
│ Create event                    │
│ Forward as attachment           │
│ Filter messages like these      │
└─────────────────────────────────┘
```

### Lista COMPLETA Opzioni Gmail Context Menu

| Opzione | Disponibile quando | Shortcut | Note |
|---------|-------------------|----------|------|
| **Reply** | Email aperta | `R` | Solo mittente |
| **Reply All** | Email aperta, più destinatari | `A` | Tutti i destinatari |
| **Forward** | Email aperta | `F` | Inoltra email |
| **Open in new window** | Qualsiasi | `Shift+Enter` | Pop-out window |
| **Search from [sender]** | Email selezionata | - | Cerca tutte email dal mittente |
| **Search subject** | Conversation view OFF | - | Cerca per subject |
| **Snooze** | Email non snoozata | `B` | Posticipa email |
| **Mute** | Conversazione | `M` | Silenzia thread |
| **Label as** | Qualsiasi | `L` | Aggiungi label |
| **Move to** | Qualsiasi | `V` | Sposta in cartella |
| **Archive** | Non archiviata | `E` | Archivia |
| **Mark as read** | Email non letta | `Shift+I` | Segna come letta |
| **Mark as unread** | Email letta | `Shift+U` | Segna come non letta |
| **Delete** | Qualsiasi | `#` | Elimina |

### Comportamento Dinamico

Gmail **cambia le opzioni** in base al contesto:

```javascript
// PSEUDO-CODICE comportamento Gmail
function getContextMenuOptions(email) {
  let options = [];

  // Reply/Forward solo se email aperta
  if (email.isOpen) {
    options.push('Reply', 'Reply All', 'Forward');
  }

  // Mark as read/unread - opzione dinamica
  if (email.isRead) {
    options.push('Mark as unread');
  } else {
    options.push('Mark as read');
  }

  // Search subject solo se conversation view OFF
  if (!conversationViewEnabled) {
    options.push('Search messages with subject');
  }

  // Sempre disponibili
  options.push('Archive', 'Delete', 'Move to', 'Label as');

  return options;
}
```

### Organizzazione Visiva

Gmail usa **separatori** per raggruppare azioni:

```
Reply/Reply All/Forward       ← Reply actions
─────────────────────────
Search from/Search subject    ← Search actions
─────────────────────────
Snooze/Mute                   ← Defer actions
─────────────────────────
Archive/Mark/Delete           ← Quick actions
```

### Keyboard Shortcuts Mostrati

Gmail **NON mostra** gli shortcut accanto alle opzioni nel context menu (a differenza di app native come Apple Mail o VS Code).

Questo è un **punto debole** dell'implementazione Gmail - gli utenti devono imparare gli shortcut separatamente.

### Limiti Gmail Context Menu

**MANCANZE RISPETTO AD APP NATIVE:**

1. ❌ Nessuno shortcut visibile nel menu
2. ❌ Nessuna icona accanto alle opzioni
3. ❌ Nessun submenu (es. "Move to" non mostra cartelle)
4. ❌ Stile visivo basico (bianco e nero, nessun colore)

**RAGIONI POSSIBILI:**
- Gmail è web-based, quindi limitato da browser
- Filosofia "less is more" di Google
- Performance (rendering veloce, poche DOM operations)

---

## 2. OUTLOOK - QUICK ACTIONS + CONTEXT MENU

### Overview

Outlook usa un **approccio ibrido**: Quick Actions che appaiono al **hover** + context menu completo al tasto destro.

Questa è una strategia interessante: azioni comuni visibili immediatamente, azioni avanzate nel context menu.

### Quick Actions (Hover)

Quando passi il mouse sopra un'email nella lista, appaiono **pulsanti inline**:

```
┌──────────────────────────────────────────────────────┐
│ 📧 John Doe - Meeting Tomorrow                       │
│    Here's the agenda for...                          │
│                                      [📌][✉][📁][🗑] │ ← Quick Actions
└──────────────────────────────────────────────────────┘
```

**Quick Actions Disponibili** (massimo 3 configurabili):

| Icona | Azione | Default | Configurabile |
|-------|--------|---------|---------------|
| 📌 | Flag / Clear Flag | ✅ | ✅ |
| ✉ | Mark as Read/Unread | ✅ | ✅ |
| 📁 | Move to folder | ❌ | ✅ |
| 📥 | Archive | ❌ | ✅ |
| 🗑 | Delete | **SEMPRE** | ❌ |

**NOTA:** Delete è SEMPRE presente, non può essere rimosso. Puoi scegliere altre 2 azioni da affiancare.

### Come Configurare Quick Actions

```
Right-click email → Set Quick Actions... → Scegli 2 opzioni
```

Questo è un **ottimo pattern UX**: l'utente personalizza il proprio workflow!

### Context Menu Completo (Tasto Destro)

Il context menu di Outlook Desktop contiene **molte più opzioni** rispetto a Gmail:

**Categoria 1: REPLY/FORWARD**
```
┌─────────────────────────────────┐
│ Reply              Ctrl+R       │
│ Reply All          Ctrl+Shift+R │
│ Forward            Ctrl+F       │
├─────────────────────────────────┤
│ ...                             │
└─────────────────────────────────┘
```

**Categoria 2: MARK/FLAG**
```
┌─────────────────────────────────┐
│ Mark as Read       Ctrl+Q       │
│ Mark as Unread     Ctrl+U       │
│ Flag               Insert       │
│ Clear Flag                      │
├─────────────────────────────────┤
│ ...                             │
└─────────────────────────────────┘
```

**Categoria 3: ORGANIZE**
```
┌─────────────────────────────────┐
│ Move                            │
│ Copy to Folder                  │
│ Categories                      │
│ Follow Up                       │
├─────────────────────────────────┤
│ ...                             │
└─────────────────────────────────┘
```

**Categoria 4: QUICK STEPS** (automation!)
```
┌─────────────────────────────────┐
│ Move to: [Folder]              │  ← Pre-configured!
│ To Manager                      │
│ Team Email                      │
│ Done                           │  ← Mark + Move automatico
├─────────────────────────────────┤
│ ...                             │
└─────────────────────────────────┘
```

**Categoria 5: ADVANCED**
```
┌─────────────────────────────────┐
│ Create Rule                     │
│ Block Sender                    │
│ Report as Junk                  │
│ Ignore                          │
├─────────────────────────────────┤
│ Delete             Ctrl+D       │
└─────────────────────────────────┘
```

### Lista COMPLETA Opzioni Outlook Context Menu

| Opzione | Shortcut Desktop | Note |
|---------|------------------|------|
| **Reply** | `Ctrl+R` | Risposta al mittente |
| **Reply All** | `Ctrl+Shift+R` | Risposta a tutti |
| **Forward** | `Ctrl+F` | Inoltra |
| **Mark as Read** | `Ctrl+Q` | Segna letta |
| **Mark as Unread** | `Ctrl+U` | Segna non letta |
| **Flag** | `Insert` | Aggiungi flag |
| **Clear Flag** | - | Rimuovi flag |
| **Move** | - | Sposta in cartella (submenu) |
| **Copy to Folder** | - | Copia in cartella (submenu) |
| **Categories** | - | Assegna categoria colore (submenu) |
| **Follow Up** | - | Imposta reminder (submenu) |
| **Create Rule** | - | Crea regola automatica |
| **Block Sender** | - | Blocca mittente |
| **Report as Junk** | - | Segnala spam |
| **Ignore** | - | Ignora conversazione |
| **Delete** | `Ctrl+D` | Elimina |

### Quick Steps - Automazione Email

Una feature **UNICA** di Outlook: Quick Steps nel context menu!

```
Quick Steps = Macro pre-configurate per azioni ripetitive

Esempio "Done":
1. Mark as Read
2. Flag as Complete
3. Move to "Completed" folder

Tutto con 1 click!
```

**Quick Steps Predefiniti:**

| Quick Step | Azione |
|------------|--------|
| **Move to** | Segna come letta + Sposta in cartella specifica |
| **To Manager** | Forward al tuo manager + CC te stesso |
| **Team Email** | Inoltra al team + Aggiungi categoria |
| **Done** | Segna come completata + Sposta + Flag verde |
| **Reply & Delete** | Apri reply + Elimina originale dopo invio |

Gli utenti possono **creare Quick Steps personalizzati** - questa è una feature che potrebbe ispirare Miracollook!

### Differenze Outlook Web vs Desktop

**Outlook Web** ha un context menu **più limitato** rispetto al Desktop:

```
Desktop:  20+ opzioni, Quick Steps, Submenu complessi
Web:      10-15 opzioni base, nessun Quick Steps

PERCHÉ? Performance + Limitazioni browser
```

Outlook Web si concentra su opzioni essenziali:
- Reply/Forward
- Mark Read/Unread
- Move/Delete
- Flag

**LEZIONE:** Anche i big devono fare compromessi nel web!

### Behavior Dinamico Outlook

Outlook **abilita/disabilita** opzioni in base al contesto:

```
Email NON LETTA:
  ✅ Mark as Read
  🔲 Mark as Unread (disabled, grigio)

Email LETTA:
  🔲 Mark as Read (disabled)
  ✅ Mark as Unread

Email CON FLAG:
  🔲 Flag (disabled)
  ✅ Clear Flag

Email SENZA FLAG:
  ✅ Flag
  🔲 Clear Flag (disabled)
```

**IMPORTANTE:** Outlook usa il pattern **disable, non hide**!

Nielsen Norman Group raccomanda questo approccio:
> "Disable menu items instead of removing them. It's clearer to users that an action isn't supported when it's greyed out rather than just completely missing."

### Keyboard Shortcuts Visibili

Outlook **MOSTRA gli shortcut** accanto alle opzioni:

```
┌─────────────────────────────────┐
│ Reply              Ctrl+R       │  ← Shortcut visibile!
│ Reply All          Ctrl+Shift+R │
│ Forward            Ctrl+F       │
│ Mark as Read       Ctrl+Q       │
│ Delete             Ctrl+D       │
└─────────────────────────────────┘
```

Questo è un **pattern standard** per app desktop native.

**BENEFICIO:** Gli utenti imparano gli shortcut mentre usano il menu!

---

## CONFRONTO GMAIL vs OUTLOOK

| Aspetto | Gmail | Outlook |
|---------|-------|---------|
| **Numero opzioni** | 10-12 | 20+ |
| **Organizzazione** | Flat (1 livello) | Gerarchica (submenu) |
| **Shortcut visibili** | ❌ No | ✅ Si |
| **Quick Actions hover** | ❌ No | ✅ Si (configurabili) |
| **Automazione** | ❌ No | ✅ Si (Quick Steps) |
| **Behavior opzioni** | Hide irrilevanti | Disable irrilevanti |
| **Stile visivo** | Minimale | Rich (icone, colori) |
| **Submenu** | ❌ No | ✅ Si (Move, Categories, etc.) |
| **Personalizzazione** | ❌ No | ✅ Si (Quick Actions) |
| **Context-aware** | Parziale | Completo |

### Cosa Impariamo

**DA GMAIL:**
- Semplicità > Complessità
- Context menu veloce da renderizzare
- Focus su azioni più comuni (80/20 rule)

**DA OUTLOOK:**
- Power users apprezzano opzioni avanzate
- Quick Actions hover = ottimo compromesso
- Disable > Hide per predictability
- Automazione (Quick Steps) = differenziatore

---

*Continua in PARTE 2...*
