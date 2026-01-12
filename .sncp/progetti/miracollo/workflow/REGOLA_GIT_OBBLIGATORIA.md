# REGOLA GIT OBBLIGATORIA - Miracollo

> **QUESTA REGOLA È SACRA. TUTTI DEVONO SEGUIRLA.**
> Regina, Guardiane, Cervelle, Rafa - NESSUNA ECCEZIONE!

---

## LA REGOLA UNICA

```
+----------------------------------------------------------+
|                                                          |
|   PRIMA DI OGNI LAVORO:     git pull origin main        |
|   DOPO OGNI MODIFICA:       git commit + git push       |
|                                                          |
|   SEMPRE. SUBITO. SENZA ECCEZIONI.                      |
|                                                          |
+----------------------------------------------------------+
```

---

## PERCHÉ È IMPORTANTE

Se NON segui questa regola:
- Il tuo lavoro può essere PERSO
- Puoi SOVRASCRIVERE il lavoro di altri
- Crei CAOS nel progetto

---

## PROTEZIONE AUTOMATICA

Abbiamo installato un **GIT HOOK** che blocca push pericolosi.

Se provi a pushare senza aver fatto pull:
```
=========================================
  STOP! Push bloccato per sicurezza!
=========================================

Origin ha X commit che tu non hai!
PRIMA fai: git pull origin main
```

---

## PER LE CERVELLE (Agenti)

Quando lavori su Miracollo:

### INIZIO SESSIONE
```bash
cd /app/miracollo  # o ~/Developer/miracollogeminifocus
git pull origin main
```

### FINE LAVORO
```bash
git add .
git commit -m "Descrizione chiara del lavoro"
git push origin main
```

### SE SEI SULLA VM
```bash
# Dopo ogni fix, SUBITO:
git add .
git commit -m "Fix: descrizione"
git push origin main
```

---

## PER LA REGINA

Prima di delegare lavoro che tocca codice Miracollo:
1. Verifica che l'agente faccia `git pull` prima
2. Verifica che faccia `git commit + push` dopo
3. Se l'agente lavora su VM, ricordagli di committare SUBITO

---

## PER LE GUARDIANE

Durante le review:
1. Verifica che i commit siano stati pushati
2. Verifica che non ci siano modifiche non committate
3. Se trovi problemi di sync, BLOCCA e risolvi prima

---

## CHECKLIST RAPIDA

```
[ ] Ho fatto git pull prima di iniziare?
[ ] Ho fatto git commit dopo ogni modifica?
[ ] Ho fatto git push alla fine?
[ ] Se sono su VM, ho pushato SUBITO dopo il fix?
```

---

*"Mai perdere lavoro. Mai sovrascrivere lavoro di altri."*
*"Git è la fonte di verità. Sempre."*
