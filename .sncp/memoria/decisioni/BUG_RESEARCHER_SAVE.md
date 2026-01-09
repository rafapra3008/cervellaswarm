# BUG TROVATO: cervella-researcher non salva file

> **Data:** 9 Gennaio 2026 - Sessione 139
> **Severity:** MEDIA
> **Status:** WORKAROUND attivo

---

## Il Problema

`cervella-researcher` a volte dice "salvo il file" ma **NON lo salva effettivamente**.

### Esempio Sessione 139
1. Researcher chiamato per CURSOR_ANALYSIS
2. Risponde "Ho completato... sto salvando il file"
3. File NON esiste!
4. Regina deve salvare manualmente

---

## Causa Probabile

- Task agent ha context limitato
- Write tool potrebbe fallire silenziosamente
- Agent non verifica se file esiste dopo write

---

## Workaround Attuale

**Dopo ogni Task con researcher:**
1. Verificare con `ls` se file esiste
2. Se non esiste, salvare manualmente i risultati

---

## Fix Proposto

Aggiungere al DNA di cervella-researcher:
```
DOPO AVER SCRITTO UN FILE:
1. Verifica che esista con Read
2. Se non esiste, riprova
3. Conferma a Regina solo DOPO verifica
```

---

## Impatto

- CURSOR_ANALYSIS.md era "FATTO" nella mappa ma non esisteva
- Potenziale perdita di ricerche importanti
- Richiede verifica manuale (overhead)

---

*Documentato per fix futuro*
