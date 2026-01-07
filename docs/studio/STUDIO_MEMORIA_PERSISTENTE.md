# STUDIO: Sistema Memoria Persistente

> **Data:** 7 Gennaio 2026 - Sessione 112
> **Autore:** Cervella (Regina)
> **Origine:** Problema reale scoperto su Miracollo
> **Priorita:** ALTA

---

## IL PROBLEMA

```
+------------------------------------------------------------------+
|                                                                  |
|   OGNI CERVELLA PARTE DA ZERO.                                  |
|   NON HA MEMORIA TRA SESSIONI.                                  |
|                                                                  |
|   L'UNICA MEMORIA E' QUELLO CHE SCRIVIAMO.                      |
|                                                                  |
|   Se non scriviamo BENE → Perdiamo il lavoro.                   |
|   Se non scriviamo DOVE → Non lo troviamo.                      |
|   Se non scriviamo COSA → Rifaremmo le stesse cose.             |
|                                                                  |
+------------------------------------------------------------------+
```

### Caso Reale (7 Gennaio 2026)

**Progetto:** Miracollo
**Situazione:** WhatsApp era gia' configurato con Twilio
**Problema:** Una nuova sessione Cervella non lo sapeva
**Conseguenza:** Ha chiesto di nuovo "Meta o Twilio?"

**Impatto:**
- Doppio lavoro
- Tempo perso
- Energia sprecata
- Contesto perso
- Frustrazione per l'utente (Rafa)

---

## ANALISI

### Cosa Manca

| Cosa Manca | Conseguenza |
|------------|-------------|
| **Registro decisioni tecniche** | Non si sa cosa e' stato deciso |
| **Formato standard** | Ogni progetto documenta diversamente |
| **Checklist checkpoint dettagliata** | Checkpoint dice "fatto" ma non i DETTAGLI |
| **Verifica all'inizio sessione** | Cervella non legge tutto |
| **Cronologia configurazioni** | Non si sa cosa funziona ORA |

### Perche' Succede

1. **Fretta** - Si fa il lavoro ma non si documenta
2. **Non c'e' un posto standard** - Dove scrivo "Twilio configurato"?
3. **PROMPT_RIPRESA non basta** - E' narrativo, non strutturato
4. **Nessuna verifica** - Nessuno controlla se la doc e' completa

---

## SOLUZIONE PROPOSTA

### 1. Registro Decisioni (per ogni progetto)

```
docs/decisioni/DECISIONI_TECNICHE.md

| Data | Categoria | Decisione | Dettagli | Status |
|------|-----------|-----------|----------|--------|
| 5 Gen | WhatsApp | Twilio (non Meta) | Sandbox configurato, numero: +1... | ATTIVO |
| 3 Gen | Database | SQLite locale | Path: data/miracollo.db | ATTIVO |
| 2 Gen | Auth | No auth per MVP | Aggiungere dopo | PIANIFICATO |
```

### 2. Categorie Standard

```
- INFRASTRUTTURA: Server, deploy, porte
- DATABASE: Tipo, path, schema
- INTEGRAZIONI: API esterne, webhook
- AUTH: Autenticazione, token
- CONFIG: Variabili ambiente, settings
- UI: Scelte design, componenti
- ARCHITETTURA: Pattern, struttura codice
```

### 3. Checklist Checkpoint Aggiornata

```
CHECKPOINT CHECKLIST:

[ ] PROMPT_RIPRESA aggiornato (narrativo)
[ ] DECISIONI_TECNICHE aggiornato (strutturato)
[ ] Nuove decisioni documentate
[ ] Config/integrazioni verificate
[ ] ROADMAP aggiornata
```

### 4. Verifica Inizio Sessione

```
INIZIO SESSIONE:

La Cervella DEVE leggere:
1. PROMPT_RIPRESA.md (cosa e' successo)
2. DECISIONI_TECNICHE.md (cosa e' stato deciso)
3. ROADMAP (dove siamo)

E CONFERMARE: "Ho letto le decisioni tecniche attive"
```

---

## INTEGRAZIONE CON DASHBOARD MAPPA

La Dashboard MAPPA puo' mostrare:

```
+------------------------------------------------------------------+
|  DECISIONI ATTIVE                                  [+ Nuova]      |
+------------------------------------------------------------------+
|                                                                  |
|  INTEGRAZIONI                                                    |
|  +----------------------------------------------------------+   |
|  | WhatsApp: Twilio Sandbox       [ATTIVO] [Dettagli]       |   |
|  | Email: Non configurata          [TODO]                   |   |
|  +----------------------------------------------------------+   |
|                                                                  |
|  DATABASE                                                        |
|  +----------------------------------------------------------+   |
|  | SQLite: data/miracollo.db      [ATTIVO] [Dettagli]       |   |
|  +----------------------------------------------------------+   |
|                                                                  |
+------------------------------------------------------------------+
```

### Benefici

1. **Visibilita' immediata** - Vedo subito cosa e' configurato
2. **Non ripeto domande** - Le decisioni sono visibili
3. **Storico** - So perche' e' stato deciso
4. **Collaborazione** - Tutti vedono lo stesso stato

---

## IMPLEMENTAZIONE

### Fase 1: Template (Immediato)

Creare template `DECISIONI_TECNICHE.md` per ogni progetto.

### Fase 2: Processo (Breve termine)

Aggiornare CLAUDE.md per includere:
- Lettura decisioni all'inizio sessione
- Aggiornamento decisioni al checkpoint

### Fase 3: Dashboard (Medio termine)

Aggiungere widget "Decisioni Attive" alla Dashboard MAPPA.

### Fase 4: Automazione (Futuro)

- Auto-detect nuove configurazioni
- Reminder se decisione non documentata
- Validazione completezza

---

## TEMPLATE: DECISIONI_TECNICHE.md

```markdown
# Decisioni Tecniche - [NOME PROGETTO]

> Ultimo aggiornamento: [DATA]
> Sessione: [NUMERO]

## Decisioni Attive

| Data | Categoria | Decisione | Dettagli | Status |
|------|-----------|-----------|----------|--------|
| | | | | |

## Storico Decisioni

### [DATA] - [CATEGORIA]

**Decisione:** [Cosa e' stato deciso]
**Alternativa scartata:** [Cosa NON abbiamo scelto]
**Motivo:** [Perche' questa scelta]
**Implementato da:** [Chi/quale sessione]
**Dettagli tecnici:** [Config, path, credenziali (senza secrets!)]

---

*"La memoria e' potere. Documenta tutto."*
```

---

## CONCLUSIONE

```
+------------------------------------------------------------------+
|                                                                  |
|   IL PROBLEMA DELLA MEMORIA NON E' UN BUG.                      |
|   E' UNA FEATURE MANCANTE.                                       |
|                                                                  |
|   E NOI LA COSTRUIREMO.                                          |
|                                                                  |
|   Perche' CervellaSwarm non e' solo uno sciame che lavora.      |
|   E' uno sciame che RICORDA.                                     |
|                                                                  |
+------------------------------------------------------------------+
```

---

*"La comunicazione interna deve essere meglio"* - Rafa, 7 Gennaio 2026

*Questo studio nasce da un problema REALE. La soluzione sara' REALE.*

---

**Prossimi step:**
1. Creare template DECISIONI_TECNICHE.md
2. Applicare a Miracollo (dove e' nato il problema)
3. Applicare a CervellaSwarm
4. Applicare a Contabilita'
5. Integrare in Dashboard MAPPA

---

*Cervella & Rafa* 💙
*Sessione 112 - 7 Gennaio 2026*
