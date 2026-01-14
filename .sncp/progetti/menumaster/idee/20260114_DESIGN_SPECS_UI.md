# MenuMaster Sesto Grado - Design Specs UI/UX

> **Data:** 14 Gennaio 2026 - Sessione 198
> **Autore:** cervella-marketing
> **Status:** APPROVATO - Pronto per implementazione

---

## LAYOUT GENERALE - DASHBOARD

### Desktop 3-Column Layout

```
+----------+---------------+----------+
| SIDEBAR  |    EDITOR     | PREVIEW  |
| (240px)  |    (fluid)    | (320px)  |
|          |               |          |
| Menu 1   | Form piatto   | [phone]  |
| Menu 2   | + allergeni   | Live     |
| Menu 3   | + tags        | render   |
| Menu 4   | [Salva]       |          |
| Menu 5   |               |          |
+----------+---------------+----------+
```

### Mobile Stack Layout

```
+---------------------------+
| [menu] Menu dropdown [QR] |
+---------------------------+
| Lista piatti              |
| [Edit drawer on tap]      |
+---------------------------+
```

---

## PALETTE COLORI

| Elemento | Colore | HEX | Uso |
|----------|--------|-----|-----|
| Background | Nero caldo | `#1C1C1E` | Sfondo dashboard |
| Sidebar/Cards | Grigio scuro | `#2C2C2E` | Sidebar, card piatto |
| CTA primario | Arancio | `#E97E21` | Bottone Salva, highlight |
| Hover/Focus | Marrone | `#7D3125` | Hover card, focus input |
| Accento | Verde chiaro | `#B1B073` | Tag GF, icone |
| Bordi | Grigio | `#38383A` | Separatori, border |
| Testo primario | Bianco | `#FFFFFF` | Titoli, labels |
| Testo secondario | Grigio | `#9B9BA5` | Descrizioni |

---

## NAVIGAZIONE 5 MENU

Sidebar con collapse/expand:

```
BISTROT LEGGERO (12)
  > Selezione Salumi
  > Insalatona Light
  > Spaghettoni Pesto  <-- editing
  > ...

BISTROT UNCONVENTIONAL (12)
DESSERT (5)
KIDS (4)
PIZZA (10)
```

---

## EDITOR PIATTO - FORM

```
+----------------------------------------+
| Nome Piatto (IT)*                      |
| [_________________________________]    |
|                                        |
| Nome Piatto (EN) - optional            |
| [_________________________________]    |
|                                        |
| Descrizione Ingredienti                |
| [_________________________________]    |
|                                        |
| Prezzo* [____] EUR                     |
|                                        |
| Allergeni (numeri EU 1-14)             |
| [1] [3] [7] [8] ...                    |
|                                        |
| Tag Speciali                           |
| [ ] GF option  [ ] Veg  [ ] Vegan      |
|                                        |
| [Annulla] [Salva Piatto]               |
+----------------------------------------+
```

---

## ALLERGENI

### Admin View (editor)
Numeri in pill: `[1] [7] [8]`

### Menu Pubblico (cliente)
Icone visive + legenda in fondo

---

## PREVIEW LIVE

Sidebar destra 320px con frame device:
- Aggiornamento real-time
- Bottone fullscreen per espandere

---

## FLOW UTENTE - MODIFICA PIATTO

1. Dashboard apre
2. Sidebar: click menu (es. BISTROT LEGGERO)
3. Click piatto da modificare
4. Editor carica form
5. Modifica campo (es. prezzo)
6. Preview aggiorna automaticamente
7. Click "Salva Piatto"
8. Toast verde "Salvato!"

**Tempo totale: < 30 secondi**

---

## PRIORITA MVP

### MUST HAVE (Sprint 1-2)
- [x] CRUD piatti
- [x] 5 menu separati
- [x] Allergeni numerici EU
- [x] Tag GF/Veg/Vegan
- [x] Preview live mobile
- [x] QR code generation
- [x] Menu pubblico responsive

### SHOULD HAVE (Sprint 3)
- [ ] Traduzioni IT/EN
- [ ] Search/filter piatti
- [ ] Drag-and-drop riordino
- [ ] Export PDF stampabile

### COULD HAVE (Post-MVP)
- [ ] AI auto-traduzione
- [ ] Upload immagini piatti
- [ ] Analytics

### OUT OF SCOPE
- Ordini online
- Pagamenti
- Prenotazioni
- Login pubblico

---

## CSS ESEMPIO BOTTONE

```css
.btn-primary {
  background: #E97E21;
  color: #FFFFFF;
  border: none;
  border-radius: 8px;
  padding: 12px 24px;
  font-weight: 600;
  transition: 0.2s;
}

.btn-primary:hover {
  background: #7D3125;
  transform: translateY(-1px);
}
```

---

*Design specs by cervella-marketing*
*14 Gennaio 2026*
