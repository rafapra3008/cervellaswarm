# GUIDA SESSIONE - Miracollook

> **Come iniziare ogni sessione su Miracollook**
> **Aggiornato: 19 Gennaio 2026**

---

## INIZIO SESSIONE (5 minuti)

### 1. Dire a Claude

```
INIZIA SESSIONE -> Miracollook
```

### 2. Claude legge:

| Ordine | File | Cosa contiene |
|--------|------|---------------|
| 1 | `INDICE.md` | Come navigare |
| 2 | `stato.md` | Stato REALE dal codice |
| 3 | `PROMPT_RIPRESA_miracollook.md` | Ultime sessioni |

### 3. Claude conferma:

```
- Fase corrente: FASE 1 (92%)
- Feature FATTE: Resizable, Context Menu, Thread, Drafts, etc
- Manca: Bulk API, Labels CRUD, Contacts, Settings
- Pronta per lavorare!
```

---

## STRUTTURA DOCUMENTAZIONE

```
CervellaSwarm/.sncp/progetti/miracollo/bracci/miracallook/
|
+-- CORE (sempre aggiornati)
|   +-- INDICE.md                     # Come navigare
|   +-- NORD_MIRACOLLOOK.md           # Visione e direzione
|   +-- stato.md                      # Stato REALE dal codice
|   +-- PROMPT_RIPRESA_miracollook.md # Checkpoint sessioni
|   +-- MAPPA_VERITA_20260119.md      # Analisi codice
|
+-- PRINCIPI
|   +-- COSTITUZIONE_MIRACOLLOOK.md   # Le regole sacre
|   +-- GUIDA_SESSIONE.md             # Questo file
|
+-- ROADMAPS
|   +-- ROADMAP_MIRACOLLOOK_MASTER.md # Piano lavori
|
+-- CARTELLE
|   +-- studi/            # Ricerche tecniche (DIAMANTE!)
|   +-- decisioni/        # Specs approvate
|   +-- ricerche/         # Competitor analysis
|   +-- reports/          # Audit storici
|   +-- archivio/         # File vecchi

REPO MIRACOLLOOK:
~/Developer/miracollogeminifocus/miracallook/
+-- backend/          # FastAPI Python (:8002)
+-- frontend/         # React TypeScript (:5173)
```

---

## FILE DA LEGGERE

### Sempre (inizio sessione)
1. **stato.md** - Stato REALE dal codice
2. **PROMPT_RIPRESA_miracollook.md** - Ultime sessioni

### Quando serve
| Situazione | File |
|------------|------|
| Perso sulla direzione | NORD_MIRACOLLOOK.md |
| Reference tecnico | MAPPA_VERITA_20260119.md |
| Piano dettagliato | ROADMAP_MIRACOLLOOK_MASTER.md |
| Principi | COSTITUZIONE_MIRACOLLOOK.md |
| Prima di implementare | studi/*.md |

---

## STATO ATTUALE (19 Gennaio 2026)

```
+================================================================+
|                                                                |
|   MIRACOLLOOK - FASE 1: 92%                                    |
|                                                                |
|   Frontend: 8.5/10 | ~4,600 righe | 40 file                   |
|   Backend:  8/10   | ~2,600 righe | 27 endpoint               |
|                                                                |
|   FATTO:                                                       |
|   - Resizable Panels, Context Menu, Thread View                |
|   - Drafts, Attachments, Mark Read/Unread                      |
|   - Design Salutare, Search, AI Summary                        |
|                                                                |
|   MANCA (~21h):                                                |
|   - Bulk Actions API (4h) - UI frontend pronta!                |
|   - Labels CRUD API (3h)                                       |
|   - Contacts (6h), Settings (8h)                               |
|                                                                |
+================================================================+
```

---

## COMANDI

```bash
# Backend
cd ~/Developer/miracollogeminifocus/miracallook/backend
source venv/bin/activate
uvicorn main:app --port 8002 --reload

# Frontend
cd ~/Developer/miracollogeminifocus/miracallook/frontend
npm run dev
```

---

## FINE SESSIONE

```
1. Aggiorna stato.md se cambiato qualcosa
2. Aggiorna PROMPT_RIPRESA_miracollook.md
3. Git commit + push
4. Handoff chiaro per prossima sessione
```

---

*"Non e un email client. E l'Outlook che CONOSCE il tuo hotel."*
