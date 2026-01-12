# WORKFLOW SOLO VM - Decisione Definitiva

> **Data:** 12 Gennaio 2026 - Sessione 173
> **Decisione di:** Rafa + Regina
> **Status:** APPROVATO E ATTIVO

---

## LA DECISIONE

```
+================================================================+
|                                                                |
|   WORKFLOW: SOLO VM                                            |
|                                                                |
|   - Tutto il lavoro su VM produzione                           |
|   - Lab sulla stessa VM quando serve                           |
|   - UNA cosa alla volta                                        |
|   - NIENTE sessioni parallele                                  |
|   - Commit frequenti (ogni feature completata)                 |
|   - Pull locale periodico (backup)                             |
|                                                                |
+================================================================+
```

---

## PERCHE QUESTA DECISIONE

1. **Semplicita** - Un solo posto dove lavorare
2. **Zero confusione** - Niente divergenze VM/Locale
3. **Deploy immediato** - Modifichi e vedi subito
4. **Una cosa alla volta** - Focus, qualita, pace

---

## COME LAVORIAMO

### Sviluppo Normale

```
1. SSH alla VM
   ssh miracollo-cervella
   cd /app/miracollo

2. Lavora sui file
   - Backend: backend/routers/
   - Frontend: frontend/

3. Testa subito
   docker restart miracollo-backend-12
   curl https://miracollo.com/api/health

4. COMMIT quando feature completa
   git add .
   git commit -m "Feature: [descrizione]"
   git push origin master

5. Pull locale (backup periodico)
   # Su MacBook
   cd ~/Developer/miracollogeminifocus
   git pull origin master
```

### Lab (quando serve)

```
Per feature rischiose o test distruttivi:

1. Crea branch su VM
   git checkout -b test/feature-name

2. Lavora e testa

3. Se OK: merge in master
   git checkout master
   git merge test/feature-name

4. Se KO: abbandona branch
   git checkout master
   git branch -D test/feature-name
```

---

## LE 5 REGOLE

| # | Regola | Perche |
|---|--------|--------|
| 1 | **UNA cosa alla volta** | Focus, qualita |
| 2 | **Commit ogni feature** | Mai perdere lavoro |
| 3 | **Testa prima di commit** | Produzione sempre OK |
| 4 | **Pull locale settimanale** | Backup |
| 5 | **NIENTE sessioni parallele** | Zero casino |

---

## CHECKLIST GIORNALIERA

```
INIZIO SESSIONE:
[ ] SSH alla VM
[ ] git status (niente pending?)
[ ] Leggi SNCP stato.md

DURANTE:
[ ] Una feature alla volta
[ ] Test dopo ogni modifica
[ ] Commit quando completo

FINE SESSIONE:
[ ] git status (tutto committato?)
[ ] git push origin master
[ ] Aggiorna SNCP
```

---

## COSA CAMBIA DAL PROTOCOLLO IBRIDO

| Prima (Ibrido) | Ora (Solo VM) |
|----------------|---------------|
| Sviluppo locale | Sviluppo su VM |
| Lab separato | Branch temporaneo |
| Sessioni parallele | Una alla volta |
| Worktrees | Non servono |
| Sync complesso | Pull periodico |

---

## DOCUMENTI OBSOLETI

I seguenti documenti sono superati da questa decisione:

- `20260111_PROTOCOLLO_IBRIDO_DEFINITIVO.md` - Non piu applicato
- `WORKFLOW_MIRACOLLO_SOLO_VM.md` (Sessione 166) - Sostituito da questo

---

## LEZIONE APPRESA

```
Sessione 172: What-If deployato su VM ma non committato
Sessione 173: Scoperto divergenza, salvato lavoro, decisione workflow

LEZIONE: Commit frequenti + Un workflow chiaro = Zero problemi
```

---

*"Lavoriamo in pace! Senza casino! Dipende da noi!"*

*"Una cosa alla volta, fatta BENE!"*

---

*Sessione 173 - Rafa & Regina*
