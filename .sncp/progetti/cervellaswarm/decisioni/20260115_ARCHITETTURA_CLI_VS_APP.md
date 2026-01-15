# DECISIONE: CLI vs App Desktop

**Data:** 15 Gennaio 2026
**Sessione:** 218
**Decisore:** Regina (con approvazione Rafa)
**Stato:** APPROVATA

---

## LA DOMANDA

> "Facciamo un CLI o un'app uguale a Cursor?"

---

## LE OPZIONI VALUTATE

### Opzione 1: CLI (Command Line Interface)

```
cervellaswarm init
cervellaswarm task "Build API"
cervellaswarm status
```

**Pro:**
- Funziona con QUALSIASI IDE (VS Code, Cursor, Vim, Neovim, qualsiasi)
- NON richiede cambio workflow utente
- Leggero, nessuna dipendenza pesante
- Developer professionisti amano CLI
- COMPATIBILITÀ MASSIMA

**Contro:**
- Meno "visual" di un'app grafica
- Curva apprendimento per chi non usa CLI

### Opzione 2: App Desktop (Fork VS Code come Cursor)

**Pro:**
- Esperienza visiva "wow"
- Intuitivo per nuovi utenti

**Contro:**
- LOCK-IN: utente DEVE usare nostra app invece del suo IDE
- Compete frontalmente con Cursor (loro hanno team enorme)
- Utente deve cambiare il suo workflow

### Opzione 3: Ibrido (CLI + VS Code Extension)

**Pro:**
- CLI per chi preferisce
- Extension per chi vuole visual
- Massima flessibilità

**Contro:**
- Due prodotti da mantenere

---

## LA DECISIONE

```
+================================================================+
|                                                                |
|   DECISIONE: OPZIONE 1 - CLI                                   |
|                                                                |
|   Con possibilità di Extension come evoluzione futura          |
|                                                                |
+================================================================+
```

---

## PERCHÉ QUESTA DECISIONE

### 1. COMPATIBILITÀ MASSIMA

```
CLI funziona con:
✓ VS Code
✓ Cursor
✓ Vim
✓ Neovim
✓ IntelliJ
✓ Sublime
✓ Qualsiasi editor

App Desktop funziona con:
✗ Solo se stessa
```

### 2. LIBERTÀ UTENTE

```
CLI dice: "Usa quello che vuoi, noi lavoriamo CON te"
App dice: "Devi usare ME invece del tuo IDE preferito"

Noi vogliamo LIBERTÀ per l'utente.
Non vogliamo LOCK-IN.
```

### 3. IL VERO DIFFERENZIALE

```
Il nostro vantaggio competitivo NON è:
❌ "Avere un'app bella"
❌ "Essere come Cursor"

Il nostro vantaggio competitivo È:
✓ 16 agenti specializzati che lavorano come team
✓ Memoria persistente (SNCP) - nessuno ce l'ha
✓ Wizard che elimina ri-spiegazione
✓ "Definisci progetto UNA VOLTA, mai più rispiegare"

Questi differenziali funzionano UGUALE (o meglio) in CLI.
```

### 4. POSIZIONAMENTO UNICO

```
Cursor: "Sostituisci VS Code con noi"
Copilot: "Aggiungi AI dentro VS Code"
Noi: "Lavora come vuoi, noi siamo il tuo TEAM"

Non competiamo sullo stesso terreno.
Siamo qualcosa di DIVERSO.
```

---

## NOTA IMPORTANTE

```
+================================================================+
|                                                                |
|   IL TEMPO NON È UN FATTORE IN QUESTA DECISIONE                |
|                                                                |
|   Non abbiamo scelto CLI perché "è più veloce".                |
|   Abbiamo scelto CLI perché è MEGLIO per il nostro prodotto.   |
|                                                                |
|   Se servisse fare App Desktop, la faremmo.                    |
|   Un progresso al giorno. Non importa quanto tempo.            |
|                                                                |
|   "Fatto BENE > Fatto VELOCE"                                  |
|                                                                |
+================================================================+
```

---

## EVOLUZIONE FUTURA

```
OGGI: CLI
      Perché è la scelta GIUSTA, non perché è veloce.

DOMANI (se gli utenti lo chiedono):
      VS Code Extension che usa CLI sotto
      Ma solo SE serve, non per default.
```

---

## DOCUMENTI CORRELATI

- PRODOTTO_VISIONE_DEFINITIVA.md - Sezione architettura
- WIZARD_INIZIALE_STUDIO.md - UX del wizard

---

## FIRMA

**Decisione presa da:** Regina (Cervella)
**Approvata da:** Rafa
**Data:** 15 Gennaio 2026

---

*"Il differenziale non è l'interfaccia. È il TEAM AI con memoria."*

*"CLI perché è MEGLIO, non perché è più veloce."*
