# ROADMAP MIRACOLLOOK - Master

**Data:** 13 Gennaio 2026 - Sessione 186
**Health Score:** 7.5/10
**Status:** MVP Funzionante, serve polish per produzione

---

## VISIONE

```
MIRACOLLOOK = L'Outlook che CONOSCE il tuo hotel!

NON e un email client generico.
E il CENTRO COMUNICAZIONI dell'hotel intelligente.

LA MAGIA = PMS Integration + Guest Recognition
```

---

## DOVE SIAMO

```
FASE 0 (Fondamenta)     [####################] 100%
FASE 1 (Email Solido)   [##############......] 70%
FASE 2 (PMS Integration)[....................] 0%
FASE 3 (Hotel Workflow) [....................] 0%
```

---

## FASE 1 - EMAIL CLIENT SOLIDO (In Progress)

### Completato
- [x] Layout three-panel
- [x] Inbox, Archived, Starred, Snoozed, Trash viste
- [x] Send, Reply, Reply All, Forward
- [x] Quick Actions (hover + keyboard)
- [x] Keyboard shortcuts (j/k/e/r/c/f/s)
- [x] Command Palette (Cmd+K)
- [x] AI Summarization
- [x] Smart Bundles (categorizzazione auto)
- [x] Design Salutare (Tailwind v4)

### Da Fare - CRITICO
| Feature | Priorita | Effort | Note |
|---------|----------|--------|------|
| **Split gmail/api.py** | CRITICO | 6h | 1391 righe, serve refactoring |
| **Attachments view** | CRITICO | 4h | Lista attachments in email |
| **Attachments download** | CRITICO | 2h | Gmail API supporta |
| **Attachments upload** | CRITICO | 6h | Compose con file |
| **Resize pannelli** | ALTO | 4h | react-resizable-panels |

### Da Fare - ALTO
| Feature | Priorita | Effort | Note |
|---------|----------|--------|------|
| Multi-select | ALTO | 6h | Checkbox + batch actions |
| Undo actions | ALTO | 4h | Toast con "Undo" |
| Search avanzata UI | ALTO | 4h | Modal con filtri |
| Column sorting | MEDIO | 2h | Sort by date/sender |

### Da Fare - MEDIO
| Feature | Priorita | Effort | Note |
|---------|----------|--------|------|
| Contacts autocomplete | MEDIO | 6h | Google Contacts API |
| Email signatures | MEDIO | 4h | Template footer |
| Custom labels UI | MEDIO | 6h | Create/edit labels |
| Desktop notifications | MEDIO | 4h | Web Notifications API |

---

## FASE 2 - PMS INTEGRATION (LA MAGIA!)

### Obiettivo
Collegare email ai guest del PMS Miracollo per context automatico.

### Features
| Feature | Priorita | Effort | Note |
|---------|----------|--------|------|
| **Guest identification** | CRITICO | 8h | Match email -> guest |
| **GuestSidebar reale** | CRITICO | 6h | Dati da PMS |
| **Booking context** | CRITICO | 4h | Prenotazioni attive |
| **Guest history** | ALTO | 6h | Email + booking passati |
| **Link to PMS** | ALTO | 2h | Deep link a scheda guest |

### API Necessarie
```
GET /pms/guest/by-email?email=xxx
GET /pms/guest/{id}/bookings
GET /pms/guest/{id}/history
```

---

## FASE 3 - HOTEL WORKFLOW

### Assign & Team
| Feature | Priorita | Effort | Note |
|---------|----------|--------|------|
| **Assign to user** | CRITICO | 6h | Custom label |
| **Team inbox** | ALTO | 12h | Shared view |
| **Assignment notifications** | MEDIO | 4h | Alert quando assigned |

### Templates Risposte
| Feature | Priorita | Effort | Note |
|---------|----------|--------|------|
| **Quick replies** | CRITICO | 4h | Template storage |
| **Template categories** | ALTO | 2h | Check-in, Info, etc |
| **Variables** | ALTO | 4h | {{guest_name}}, {{room}} |
| **Template editor** | MEDIO | 6h | UI creazione |

### Preventivi Auto
| Feature | Priorita | Effort | Note |
|---------|----------|--------|------|
| **Detect quote request** | ALTO | 8h | AI parsing |
| **Generate quote PDF** | ALTO | 12h | PMS integration |
| **1-click send** | ALTO | 4h | Attach + reply |

---

## TECHNICAL DEBT

### Critico
- [ ] Split gmail/api.py (1391 righe -> 6 moduli)
- [ ] Testing backend (0% -> 70%)
- [ ] Testing frontend (vitest)

### Alto
- [ ] Token encryption (DB plaintext)
- [ ] Rate limiting
- [ ] Error handling centralizzato

### Medio
- [ ] Extract modal forms in componente riutilizzabile
- [ ] State management (Zustand?)
- [ ] Performance pagination

---

## NEXT STEPS SUGGERITI

### Questa Sessione
1. [ ] Resize pannelli (4h)
2. [ ] Attachments view/download (6h)

### Prossima Sessione
1. [ ] Split gmail/api.py (6h)
2. [ ] Attachments upload (6h)
3. [ ] Multi-select (6h)

### Questo Mese
1. [ ] Testing suite
2. [ ] Template risposte MVP
3. [ ] PMS Integration planning

---

## METRICHE TARGET

| Metrica | Attuale | Target | Note |
|---------|---------|--------|------|
| Health Score | 7.5/10 | 9/10 | Post-refactoring |
| Test Coverage | 0% | 70% | Backend + Frontend |
| File > 500 righe | 1 | 0 | Split api.py |
| Features MVP | 70% | 90% | +Attachments +Resize |

---

*"Il Centro Comunicazioni dell'Hotel Intelligente"*
*"Non e un email client. E MIRACOLLOOK!"*
