# ROADMAP DESIGN - Miracollook

> **Creato:** 13 Gennaio 2026 - Sessione 181
> **Principio:** "DESIGN IMPONE RISPETTO"
> **Riferimento:** Miracollo PMS (lo standard da raggiungere)

---

## IL PROBLEMA

```
+================================================================+
|                                                                |
|   Miracollook FUNZIONA ma non ha lo stesso livello            |
|   di design di Miracollo PMS.                                  |
|                                                                |
|   Miracollo PMS = STUPENDO (fatto dalle Cervelle!)             |
|   Miracollook = Funzionale ma BASIC                            |
|                                                                |
|   "DESIGN IMPONE RISPETTO" - Non siamo ancora li.              |
|                                                                |
+================================================================+
```

---

## CONFRONTO VISIVO

### Miracollo PMS (Riferimento)

```
SIDEBAR:
- Icone colorate/emoji per ogni voce
- Spacing generoso
- Hover states eleganti
- Status "Connesso" in basso
- Dropdown hotel

CARDS/KPI:
- Grandi numeri bold
- Icone colorate per ogni metrica
- Background cards con bordi sottili
- Colori: verde, rosso, arancione, blu

HEADER:
- Tabs strutturati
- Bottoni azione evidenziati
- Badge numerici colorati
- Time filters eleganti

TYPOGRAPHY:
- Gerarchia chiara (titoli, sottotitoli, body)
- Pesi diversi (bold, medium, regular)
- Colori testo differenziati
```

### Miracollook (Attuale)

```
SIDEBAR:
- Solo testo
- Categorie basic
- No icone

EMAIL LIST:
- Densa, poco respiro
- No raggruppamento per data
- Preview basic

EMAIL DETAIL:
- Funzionale ma piatto
- Bottoni basic
- No badges

GUEST SIDEBAR:
- Funzionale
- Card basic
- Bottoni semplici
```

---

## GAP DA COLMARE

### Priorita 1 - CRITICO (Impatto visivo immediato)

| # | Elemento | Stato Attuale | Target | Riferimento |
|---|----------|---------------|--------|-------------|
| D1 | Sidebar con icone | Solo testo | Icone colorate per ogni categoria | Miracollo sidebar |
| D2 | Email list spacing | Denso | Piu respiro, gruppi per data | Missive |
| D3 | Header strutturato | Minimal | Logo + user avatar + azioni | Miracollo header |

### Priorita 2 - IMPORTANTE (Consistenza brand)

| # | Elemento | Stato Attuale | Target | Riferimento |
|---|----------|---------------|--------|-------------|
| D4 | Typography gerarchia | Piatta | Bold titoli, medium body | Miracollo |
| D5 | Colori accent | Solo blu | Verde/rosso/arancione per stati | Miracollo KPIs |
| D6 | Badges/tags | Basic | Colorati, arrotondati | Miracollo badges |

### Priorita 3 - NICE TO HAVE (Polish finale)

| # | Elemento | Stato Attuale | Target | Riferimento |
|---|----------|---------------|--------|-------------|
| D7 | Hover states | Basic | Smooth con colori | Miracollo sidebar |
| D8 | Animazioni | Poche | Subtle, professionali | Linear.app |
| D9 | Empty states | Nessuno | Illustrazioni/messaggi | Best practices |

---

## PROCESSO

```
Per OGNI elemento di design:

1. Marketing crea specs dettagliate
   - Colori esatti (hex)
   - Dimensioni (px, rem)
   - Spaziature
   - Stati (hover, active, disabled)

2. Guardiana Qualita valida specs
   - Coerenza con Miracollo
   - Accessibilita
   - Responsive

3. Frontend implementa
   - Segue specs ESATTAMENTE
   - Testa su mobile/desktop

4. Guardiana Qualita verifica implementazione
   - Screenshot comparison
   - Approve/Request changes
```

---

## ORDINE DI ESECUZIONE

```
SPRINT DESIGN 1: Sidebar + Header
  [D1] Sidebar con icone
  [D3] Header strutturato

  Perche prima: Impatto visivo IMMEDIATO
               Si vede appena apri l'app

SPRINT DESIGN 2: Email List
  [D2] Spacing e raggruppamento
  [D5] Colori per stati (unread, starred, etc)

  Perche: E' il cuore dell'app
          Dove l'utente passa piu tempo

SPRINT DESIGN 3: Polish
  [D4] Typography
  [D6] Badges
  [D7-D9] Animazioni e dettagli

  Perche: Rifinitura finale
          "I dettagli fanno la differenza"
```

---

## RIFERIMENTI DESIGN

### Miracollo PMS (PRINCIPALE)
- Screenshot: vedi cartella Desktop
- Colori: stesso palette
- Componenti: stessa libreria Tailwind

### Altri riferimenti
- Missive (email client premium)
- Superhuman (keyboard-first email)
- Linear.app (design moderno)

---

## METRICHE SUCCESSO

```
DESIGN COMPLETO quando:

[ ] Rafa guarda Miracollook e dice "WOW!"
[ ] Confronto con Miracollo PMS: stesso livello
[ ] Screenshot pubblicabili su landing page
[ ] Nessun "questo sembra basic"
```

---

## NOTE

```
"Non voglio che sia fatto tutto di una volta"
"Una cosa alla volta"
"Consultare Marketing, poi Guardiana verifica"

Questo e il PROCESSO CORRETTO!
```

---

*"DESIGN IMPONE RISPETTO"*
*"I dettagli fanno SEMPRE la differenza"*

*Roadmap creata: 13 Gennaio 2026 - Sessione 181*
