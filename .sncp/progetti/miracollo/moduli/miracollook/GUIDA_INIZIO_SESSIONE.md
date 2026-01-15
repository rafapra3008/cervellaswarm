# GUIDA INIZIO SESSIONE - MIRACOLLOOK

> **Leggi questo in 30 secondi. Non di più.**

---

## 1. STATO ATTUALE (15 Gennaio 2026)

```
FASE 0: ✅ COMPLETA (OAuth, Inbox, Send, Reply, Archive, Search, AI)
FASE 1: 30% (mancano 35h: Mark Read, Drafts, Bulk, Threads, Labels, Attachments)
FASE 2: 0% (PMS Integration)
```

---

## 2. COSA FARE OGGI

```
1. Apri stato.md → vedi cosa manca
2. Scegli UNA feature da implementare
3. Guarda se c'è ricerca in studi/ o decisioni/
4. IMPLEMENTA (scrivi codice VERO)
5. TESTA (verifica che funziona)
6. COMMITTA (git commit)
7. AGGIORNA stato.md (solo DOPO il commit!)
```

---

## 3. REGOLA SACRA

```
+====================================================================+
|                                                                    |
|   MAI scrivere "FATTO" senza COMMIT!                               |
|                                                                    |
|   ❌ SBAGLIATO: Scrivo docs → aggiorno stato.md → mai faccio codice|
|   ✅ GIUSTO: Faccio codice → testo → commit → aggiorno stato.md   |
|                                                                    |
+====================================================================+
```

---

## 4. COMANDI RAPIDI

```bash
# Backend
cd ~/Developer/miracollogeminifocus/miracallook/backend
source venv/bin/activate && uvicorn main:app --port 8002 --reload

# Frontend
cd ~/Developer/miracollogeminifocus/miracallook/frontend
npm run dev

# URL: http://localhost:5173
```

---

## 5. FILE IMPORTANTI

| File | Usa per |
|------|---------|
| `stato.md` | Cosa esiste DAVVERO |
| `NORD_MIRACOLLOOK.md` | Visione e roadmap |
| `studi/` | Ricerche già fatte |
| `decisioni/` | Design specs |

---

*"SU CARTA != REALE"*
*"Fatto BENE > Fatto VELOCE"*
