# GUIDA SESSIONE - Miracollook

> **Come iniziare ogni sessione su Miracollook**
> Creata: 13 Gennaio 2026 - Sessione 191

---

## INIZIO SESSIONE (5 minuti)

### 1. Dire a Claude

```
INIZIA SESSIONE -> Miracollook
```

### 2. Claude legge automaticamente:

| Ordine | File | Cosa contiene |
|--------|------|---------------|
| 1 | `COSTITUZIONE_MIRACOLLOOK.md` | Le REGOLE sacre |
| 2 | `stato.md` | Dove siamo ORA |
| 3 | `NORD_MIRACOLLOOK.md` | La VISIONE (se serve) |

### 3. Claude conferma:

```
- Versione attuale: 2.0.0
- Fase corrente: FASE 1 (75%)
- Prossimo step: [da stato.md]
- Pronta per lavorare!
```

---

## STRUTTURA DOCUMENTAZIONE

```
CervellaSwarm/.sncp/progetti/miracollo/moduli/miracallook/
|
+-- DOCUMENTI PRINCIPALI (sempre aggiornati)
|   +-- COSTITUZIONE_MIRACOLLOOK.md    # Le regole
|   +-- NORD_MIRACOLLOOK.md            # La visione
|   +-- stato.md                       # Stato attuale
|   +-- MAPPA_FUNZIONI.md              # Have vs Need
|   +-- ROADMAP_MIRACOLLOOK_MASTER.md  # Piano lavori
|   +-- GUIDA_SESSIONE.md              # Come iniziare
|
+-- CARTELLE SPECIFICHE
|   +-- ricerche/         # Analisi competitor
|   +-- studi/            # Ricerche tecniche
|   +-- decisioni/        # Decisioni con PERCHE
|   +-- reports/          # Validazioni Guardiane
|   +-- archivio/         # Documenti vecchi
|
+-- REPO MIRACOLLOOK
    ~/Developer/miracollook/
    +-- CLAUDE.md         # Istruzioni per Claude
    +-- backend/          # FastAPI Python
    +-- frontend/         # React TypeScript
```

---

## FILE DA LEGGERE

### Sempre (inizio sessione)
1. **COSTITUZIONE_MIRACOLLOOK.md** - I 5 principi sacri
2. **stato.md** - Dove siamo, cosa fare

### Quando serve
| Situazione | File |
|------------|------|
| Perso sulla direzione | NORD_MIRACOLLOOK.md |
| Cosa implementare | MAPPA_FUNZIONI.md |
| Piano dettagliato | ROADMAP_MIRACOLLOOK_MASTER.md |
| Decisione da prendere | decisioni/*.md |
| Ricerca fatta | studi/*.md o ricerche/*.md |

---

## STATO ATTUALE (13 Gennaio 2026)

```
+================================================================+
|                                                                |
|   MIRACOLLOOK v2.0.0                                           |
|                                                                |
|   FASE 0: Fondamenta      [####################] 100%          |
|   FASE P1: Performance    [####################] 100%          |
|   FASE P2: Offline/PWA    [####################] 100%          |
|   FASE 1: Email Solido    [###############.....] 75%           |
|                                                                |
|   PROSSIMO: Funzioni BASE mancanti (~40h)                      |
|   - Mark Read/Unread, Drafts, Bulk, Labels, Contacts           |
|                                                                |
+================================================================+
```

---

## COME AVVIARE L'APP

```bash
# Con Docker (raccomandato)
cd ~/Developer/miracollook
docker compose up

# Frontend: http://localhost:5173
# Backend:  http://localhost:8002
```

---

## REGOLE IMPORTANTI

### 1. Una cosa alla volta
```
Finisci una feature PRIMA di iniziare un'altra
```

### 2. Test REALE
```
"Su carta" != "Reale"
Testa SEMPRE prima di dire "fatto"
```

### 3. Consulta le esperte
```
UI/UX       -> cervella-marketing
Database    -> cervella-data
Sicurezza   -> cervella-security
Deploy      -> cervella-devops
Architettura -> cervella-ingegnera
Ricerca     -> cervella-researcher
```

### 4. Checkpoint
```
Ogni 30-45 minuti: aggiorna stato.md
Fine sessione: git commit + push
```

---

## CHECKLIST FINE SESSIONE

```
[ ] Aggiornare stato.md
[ ] Aggiornare NORD se serve
[ ] Git commit con messaggio chiaro
[ ] Git push
[ ] Handoff chiaro per prossima sessione
```

---

## PROSSIMI STEP (da implementare)

### CRITICI (fare prima)
- [ ] Mark as Read/Unread (2h)
- [ ] Drafts auto-save (6h)

### ALTI
- [ ] Bulk Actions (5h)
- [ ] Thread View (4h)
- [ ] Labels Custom (3h)
- [ ] Upload Attachments (4h)

### MEDI
- [ ] Contacts Autocomplete (6h)
- [ ] Settings Page (8h)
- [ ] Firma email (2h)

---

*"Lavoriamo in pace! Senza casino! Dipende da noi!"*
*"Il Centro Comunicazioni dell'Hotel Intelligente"*
